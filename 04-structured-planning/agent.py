#!/usr/bin/env python3
"""
04 STRUCTURED PLANNING — Todo Agent: Structured Planning

Core Philosophy: "Make Plans Visible"
=====================================
The intermediate agent works great for simple tasks. But ask it to
"refactor auth, add tests, update docs" and watch what happens:
  - Jumps between tasks randomly
  - Forgets completed steps
  - Loses focus mid-way

The solution: ONE new tool (TodoWrite) that fundamentally changes
how the agent works by making plans explicit and visible.

Usage:
    uv run python 04-structured-planning/agent.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from litellm import completion

load_dotenv(override=True)


# =============================================================================
# Configuration
# =============================================================================

WORKDIR = Path.cwd()
MODEL = os.getenv("MODEL_ID", "anthropic/claude-3-5-sonnet-20241022")
os.environ.setdefault("LITELLM_LOG", "ERROR")


# =============================================================================
# TodoManager - The core addition at this level
# =============================================================================

class TodoManager:
    """
    Manages a structured task list with enforced constraints.

    Key Design Decisions:
    - Max 20 items: Prevents the model from creating endless lists
    - One in_progress: Forces focus - can only work on ONE thing at a time
    - Required fields: Each item needs content, status, and activeForm
    """

    def __init__(self):
        self.items = []

    def update(self, items: list) -> str:
        """Validate and update the todo list."""
        validated = []
        in_progress_count = 0

        for i, item in enumerate(items):
            content = str(item.get("content", "")).strip()
            status = str(item.get("status", "pending")).lower()
            active_form = str(item.get("activeForm", "")).strip()

            if not content:
                raise ValueError(f"Item {i}: content required")
            if status not in ("pending", "in_progress", "completed"):
                raise ValueError(f"Item {i}: invalid status '{status}'")
            if not active_form:
                raise ValueError(f"Item {i}: activeForm required")

            if status == "in_progress":
                in_progress_count += 1

            validated.append({
                "content": content,
                "status": status,
                "activeForm": active_form
            })

        if len(validated) > 20:
            raise ValueError("Max 20 todos allowed")
        if in_progress_count > 1:
            raise ValueError("Only one task can be in_progress at a time")

        self.items = validated
        return self.render()

    def render(self) -> str:
        """Render the todo list as human-readable text."""
        if not self.items:
            return "No todos."

        lines = []
        for item in self.items:
            if item["status"] == "completed":
                lines.append(f"[x] {item['content']}")
            elif item["status"] == "in_progress":
                lines.append(f"[>] {item['content']} <- {item['activeForm']}")
            else:
                lines.append(f"[ ] {item['content']}")

        completed = sum(1 for t in self.items if t["status"] == "completed")
        lines.append(f"\n({completed}/{len(self.items)} completed)")

        return "\n".join(lines)


TODO = TodoManager()


# =============================================================================
# System Prompt & Reminders
# =============================================================================

SYSTEM_PROMPT = f"""You are a coding agent at {WORKDIR}.

Loop: plan -> act with tools -> update todos -> report.

Rules:
- Use TodoWrite to track multi-step tasks
- Mark tasks in_progress before starting, completed when done
- Prefer tools over prose. Act, don't just explain.
- After finishing, summarize what changed."""

INITIAL_REMINDER = "System Reminder: Use the TodoWrite tool first to create a transparent plan for multi-step tasks."
NAG_REMINDER = "System Reminder: 10+ turns without todo update. Please update your todos using TodoWrite to keep the user informed."


# =============================================================================
# Tool Definitions (OpenAI Schema)
# =============================================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace exact text in file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_text": {"type": "string"},
                    "new_text": {"type": "string"}
                },
                "required": ["path", "old_text", "new_text"]
            }
        }
    },
    # NEW: TodoWrite - The Planning Tool
    {
        "type": "function",
        "function": {
            "name": "TodoWrite",
            "description": "Update the task list. Use to plan and track progress.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Complete list of tasks (replaces existing)",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "Task description"
                                },
                                "status": {
                                    "type": "string",
                                    "enum": ["pending", "in_progress", "completed"],
                                    "description": "Task status"
                                },
                                "activeForm": {
                                    "type": "string",
                                    "description": "Present tense action, e.g. 'Reading files'"
                                }
                            },
                            "required": ["content", "status", "activeForm"]
                        }
                    }
                },
                "required": ["items"]
            }
        }
    }
]


# =============================================================================
# Tool Implementations
# =============================================================================

def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

def run_bash(cmd: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot"]
    if any(d in cmd for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        result = subprocess.run(cmd, shell=True, cwd=WORKDIR, capture_output=True, text=True, timeout=60)
        output = (result.stdout + result.stderr).strip()
        return output[:50000] if output else "(no output)"
    except Exception as e:
        return f"Error: {e}"

def run_read(path: str, limit: int = None) -> str:
    try:
        text = safe_path(path).read_text()
        lines = text.splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more)"]
        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"Error: {e}"

def run_write(path: str, content: str) -> str:
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"

def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        fp = safe_path(path)
        content = fp.read_text()
        if old_text not in content:
            return f"Error: Text not found in {path}"
        fp.write_text(content.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"

def run_todo(items: list) -> str:
    try:
        return TODO.update(items)
    except Exception as e:
        return f"Error: {e}"

def execute_tool(name: str, args: dict) -> str:
    if name == "bash":
        return run_bash(args["command"])
    elif name == "read_file":
        return run_read(args["path"], args.get("limit"))
    elif name == "write_file":
        return run_write(args["path"], args["content"])
    elif name == "edit_file":
        return run_edit(args["path"], args["old_text"], args["new_text"])
    elif name == "TodoWrite":
        return run_todo(args["items"])
    return f"Unknown tool: {name}"


# =============================================================================
# Agent Loop (with todo tracking)
# =============================================================================

rounds_without_todo = 0

def agent_loop(messages: list) -> list:
    """Agent loop with todo usage tracking and nag reminders."""
    global rounds_without_todo

    while True:
        response = completion(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_unset=True))

        if message.content:
            print(f"\033[32m{message.content}\033[0m")

        if not message.tool_calls:
            return messages

        used_todo = False

        for tool_call in message.tool_calls:
            print(f"\n> {tool_call.function.name}")
            
            try:
                args = json.loads(tool_call.function.arguments)
                output = execute_tool(tool_call.function.name, args)
            except Exception as e:
                output = f"Invalid tool arguments: {e}"

            if tool_call.function.name == "TodoWrite":
                used_todo = True
                
            preview = output[:300] + "..." if len(output) > 300 else output
            print(f"  {preview}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(output)
            })

        if used_todo:
            rounds_without_todo = 0
        else:
            rounds_without_todo += 1

        # If it's been 10 tool calls without updating the plan, we 'nag' the model.
        # We append this explicitly to the instruction block.
        if rounds_without_todo >= 10:
            print(f"\n[System] Nagging model to update Todos...")
            messages.append({
                "role": "user",
                "content": NAG_REMINDER
            })
            # Reset counter so we don't nag every single turn forever
            rounds_without_todo = 0


# =============================================================================
# Main REPL
# =============================================================================

def main():
    global rounds_without_todo

    print(f"Structured Planning 04 - {WORKDIR}")
    print("Type 'exit' to quit.\n")

    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    first_turn = True

    while True:
        try:
            user_input = input("\033[36m>> \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q"):
            break

        if first_turn:
            # We inject the initial reminder alongside the first user prompt
            user_input = f"{user_input}\n\n{INITIAL_REMINDER}"
            first_turn = False
            
        history.append({"role": "user", "content": user_input})

        try:
            agent_loop(history)
        except Exception as e:
            print(f"Error: {e}")

        print()

if __name__ == "__main__":
    main()
