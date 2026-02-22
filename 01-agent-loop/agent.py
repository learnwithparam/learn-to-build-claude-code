#!/usr/bin/env python3
"""
01: The Agent Loop — Mini Claude Code

The entire AI coding agent in a clean, readable loop.

This is the "Hello World" of AI agents. It proves that a fully capable
coding agent needs nothing more than:
  1. An LLM (via litellm, allowing OpenAI, Anthropic, OpenRouter, etc)
  2. One tool (bash)
  3. A loop

Usage:
    uv run python 01-agent-loop/agent.py
"""
import json
import os
import subprocess
import sys

from dotenv import load_dotenv
from litellm import completion

load_dotenv(override=True)

# We use an open model schema, litellm will route it to the correct provider.
MODEL = os.getenv("MODEL_ID", "anthropic/claude-3-5-sonnet-20241022")
# Add a flag to drop litellm's noisy logs unless asked for
os.environ.setdefault("LITELLM_LOG", "ERROR")

# Standard OpenAI tool calling schema
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command. Use for: ls, grep, find, echo, cat.",
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

SYSTEM_PROMPT = f"""You are a CLI agent at {os.getcwd()}. 
Use bash to solve problems. Be concise. Act, don't just explain."""


def chat(user_prompt: str, history: list = None) -> str:
    """The core agent loop."""
    if history is None:
        history = [{"role": "system", "content": SYSTEM_PROMPT}]
        
    history.append({"role": "user", "content": user_prompt})

    while True:
        # Step 1: Call the model
        response = completion(
            model=MODEL,
            messages=history,
            tools=TOOLS,
        )
        message = response.choices[0].message
        
        # Step 2: Append the model's message exactly as generated
        history.append(message.model_dump(exclude_unset=True))
        
        # Step 3: Check if the model called any tools
        if not message.tool_calls:
            return message.content or ""
            
        # Step 4: Execute the tools and append the results
        for tool_call in message.tool_calls:
            # Parse arguments
            args = json.loads(tool_call.function.arguments)
            command = args["command"]
            
            print(f"\033[33m$ {command}\033[0m")
            
            # Execute bash
            try:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=300
                )
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)
                
            print(output[:500] + ("..." if len(output) > 500 else "") or "(empty)")
            
            # OpenAI requires a 'tool' role message containing the result
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": output[:50000] or "Command completed with no output."
            })
            
        # The loop automatically continues, feeding the tool result back to the LLM


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # One-shot command line mode
        print(chat(" ".join(sys.argv[1:])))
    else:
        # Interactive REPL mode
        msg_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        print(f"Mini Claude Code 01 - {os.getcwd()}\nType 'q' to quit.")
        while True:
            try:
                user_msg = input("\033[36m>> \033[0m")
                if user_msg.lower() in ["q", "quit", "exit"]:
                    break
                print(chat(user_msg, msg_history))
            except (EOFError, KeyboardInterrupt):
                break
