#!/usr/bin/env python3
"""
02: Bash Agent — Expand the Agent Loop

Core Philosophy: "Bash is All You Need"
=======================================
This is the expanded version of the agent loop. Same concept,
but with proper structure, error handling, and detailed comments.

Key difference from 01 The Agent Loop:
- Proper function structure with docstrings
- Error handling (timeouts, output truncation)
- Clear separation of concerns
- Interactive REPL AND subagent mode

The bash tool teaches the model common patterns AND how to spawn subagents.
Calling itself via bash implements subagents through process recursion.

Usage:
    # Interactive mode
    uv run python 02-bash-agent/agent.py

    # Subagent mode (called by parent agent)
    uv run python 02-bash-agent/agent.py "explore src/ and summarize"
"""
import json
import os
import subprocess
import sys

from dotenv import load_dotenv
from litellm import completion

load_dotenv(override=True)

# 1. Configuration
# Uses anthropic/claude-3-5-sonnet-20241022 via litellm by default
MODEL = os.getenv("MODEL_ID", "anthropic/claude-3-5-sonnet-20241022")
os.environ.setdefault("LITELLM_LOG", "ERROR")

# 2. Tool Definition
# The ONE tool that does everything (OpenAI JSON Schema)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Execute shell command. Common patterns:\n"
                           "- Read: cat/head/tail, grep/find/rg/ls, wc -l\n"
                           "- Write: echo 'content' > file, sed -i 's/old/new/g' file\n"
                           "- Subagent: uv run python 02-bash-agent/agent.py 'task' (spawns isolated agent, returns summary)",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                    }
                },
                "required": ["command"]
            }
        }
    }
]

# 3. System Prompt
# Teaches the model HOW to use bash effectively
SYSTEM_PROMPT = f"""You are a CLI agent at {os.getcwd()}. Solve problems using bash commands.

Rules:
- Prefer tools over prose. Act first, explain briefly after.
- Read files: cat, grep, find, ls, head, tail
- Write files: echo '...' > file, sed -i, or cat << 'EOF' > file
- Subagent: For complex subtasks, spawn a subagent to keep context clean:
  uv run python 02-bash-agent/agent.py "explore src/ and summarize the architecture"

When to use subagent:
- Task requires reading many files (isolate the exploration)
- Task is independent and self-contained
- You want to avoid polluting current conversation with intermediate details

The subagent runs in isolation and returns only its final summary."""


def chat(prompt: str, history: list = None) -> str:
    """
    The complete agent loop in ONE function.

    This is the core pattern that ALL coding agents share:
        while True:
            response = model(messages, tools)
            if no tool calls: return text
            execute tools, append results
    """
    if history is None:
        history = [{"role": "system", "content": SYSTEM_PROMPT}]

    history.append({"role": "user", "content": prompt})

    while True:
        # 1. Call the model with tools
        response = completion(
            model=MODEL,
            messages=history,
            tools=TOOLS,
        )
        
        # 2. Get the message object
        message = response.choices[0].message
        
        # 3. Save the model's message to history
        history.append(message.model_dump(exclude_unset=True))
        
        # If there's text output, print it to the user
        if message.content:
            print(message.content)

        # 4. If model didn't call tools, we're done with this turn
        if not message.tool_calls:
            return message.content or ""

        # 5. Execute each tool call and collect results
        for tool_call in message.tool_calls:
            if tool_call.function.name == "bash":
                # Parse the JSON arguments
                args = json.loads(tool_call.function.arguments)
                cmd = args["command"]
                
                print(f"\033[33m$ {cmd}\033[0m")  # Yellow color for commands

                try:
                    # Execute the bash command safely
                    out = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=300,
                        cwd=os.getcwd()
                    )
                    output = out.stdout + out.stderr
                except subprocess.TimeoutExpired:
                    output = "(timeout after 300s)"
                except Exception as e:
                    output = str(e)

                print(output[:1000] + ("..." if len(output) > 1000 else "") or "(empty)")
                
                # 6. Append tool result to history
                # OpenAI requires role="tool" with the tool_call_id
                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": output[:50000]  # Truncate very long outputs securely
                })

        # The loop automatically repeats, feeding the tool results back!


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Subagent mode: execute task and print result
        print(chat(" ".join(sys.argv[1:])))
    else:
        # Interactive REPL mode
        msg_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        print(f"Bash Agent 02 - {os.getcwd()}")
        print("Type 'exit' or 'q' to quit.\n")
        
        while True:
            try:
                query = input("\033[36m>> \033[0m")  # Cyan prompt
            except (EOFError, KeyboardInterrupt):
                break
            if query.lower() in ("q", "exit", "quit", ""):
                break
            print(chat(query, msg_history))
