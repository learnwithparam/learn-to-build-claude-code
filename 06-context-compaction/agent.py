#!/usr/bin/env python3
"""
06: Context Compaction — Three-Layer Compression

Three-layer compression pipeline so the agent can work indefinitely:
  Layer 1: micro_compact — silently trim old tool results (every turn)
  Layer 2: auto_compact — save transcript + LLM summary (when tokens > threshold)
  Layer 3: compact tool — model triggers manual compression

Builds on 05 by adding memory management. Without compaction,
long conversations eventually exhaust the context window.

Usage:
    uv run python 06-context-compaction/agent.py
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from litellm import completion

load_dotenv(override=True)

WORKDIR = Path.cwd()
MODEL = os.getenv("MODEL_ID", "anthropic/claude-3-5-sonnet-20241022")
os.environ.setdefault("LITELLM_LOG", "ERROR")

SYSTEM = f"You are a coding agent at {WORKDIR}. Use tools to solve tasks."

THRESHOLD = 50000
TRANSCRIPT_DIR = WORKDIR / ".transcripts"
KEEP_RECENT = 3


def estimate_tokens(messages: list) -> int:
    """Rough token count: ~4 chars per token."""
    return len(str(messages)) // 4


# -- Layer 1: micro_compact — replace old tool results with placeholders --

def micro_compact(messages: list) -> list:
    """Trim old tool-result messages (role=tool) to short placeholders."""
    tool_indices = []
    for idx, msg in enumerate(messages):
        if msg.get("role") == "tool":
            tool_indices.append(idx)

    if len(tool_indices) <= KEEP_RECENT:
        return messages
    # Build tool_call_id -> tool_name map from assistant messages
    tool_name_map = {}
    for msg in messages:
        if msg.get("role") == "assistant":
            tool_calls = msg.get("tool_calls")
            if tool_calls:
                for tc in tool_calls:
                    fn = tc if isinstance(tc, dict) else tc
                    tc_id = fn.get("id", "") if isinstance(fn, dict) else getattr(fn, "id", "")
                    func = fn.get("function", {}) if isinstance(fn, dict) else getattr(fn, "function", None)
                    if isinstance(func, dict):
                        name = func.get("name", "unknown")
                    elif func:
                        name = getattr(func, "name", "unknown")
                    else:
                        name = "unknown"
                    tool_name_map[tc_id] = name

    to_clear = tool_indices[:-KEEP_RECENT]
    for idx in to_clear:
        msg = messages[idx]
        content = msg.get("content", "")
        if isinstance(content, str) and len(content) > 100:
            tool_call_id = msg.get("tool_call_id", "")
            tool_name = msg.get("name") or tool_name_map.get(tool_call_id, "unknown")
            msg["content"] = f"[Previous: used {tool_name}]"

    return messages


# -- Layer 2: auto_compact — save transcript + LLM summary --

def auto_compact(messages: list) -> list:
    """Save full transcript to disk, then ask LLM for a summary."""
    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    transcript_path = TRANSCRIPT_DIR / f"transcript_{int(time.time())}.jsonl"
    with open(transcript_path, "w") as f:
        for msg in messages:
            f.write(json.dumps(msg, default=str) + "\n")
    print(f"[transcript saved: {transcript_path}]")
    conversation_text = json.dumps(messages, default=str)[:80000]
    response = completion(
        model=MODEL,
        messages=[
            {"role": "user", "content":
                "Summarize this conversation for continuity. Include: "
                "1) What was accomplished, 2) Current state, 3) Key decisions made. "
                "Be concise but preserve critical details.\n\n" + conversation_text}
        ],
    )
    summary = response.choices[0].message.content or ""
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"[Conversation compressed. Transcript: {transcript_path}]\n\n{summary}"},
        {"role": "assistant", "content": "Understood. I have the context from the summary. Continuing."},
    ]


# -- Tool implementations --

def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR,
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"

def run_read(path: str, limit: int = None) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
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
        return f"Wrote {len(content)} bytes"
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


TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "compact":    lambda **kw: "Manual compression requested.",
}


def _tool(name, desc, props, required=None):
    t = {"type": "function", "function": {"name": name, "description": desc,
         "parameters": {"type": "object", "properties": props}}}
    if required:
        t["function"]["parameters"]["required"] = required
    return t

TOOLS = [
    _tool("bash", "Run a shell command.",
          {"command": {"type": "string"}}, ["command"]),
    _tool("read_file", "Read file contents.",
          {"path": {"type": "string"}, "limit": {"type": "integer"}}, ["path"]),
    _tool("write_file", "Write content to file.",
          {"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"]),
    _tool("edit_file", "Replace exact text in file.",
          {"path": {"type": "string"}, "old_text": {"type": "string"},
           "new_text": {"type": "string"}}, ["path", "old_text", "new_text"]),
    _tool("compact", "Trigger manual conversation compression.",
          {"focus": {"type": "string", "description": "What to preserve in the summary"}}),
]


# -- Agent loop with 3-layer compaction --

def agent_loop(messages: list):
    while True:
        # Layer 1: micro_compact before each LLM call
        micro_compact(messages)

        # Layer 2: auto_compact if token estimate exceeds threshold
        if estimate_tokens(messages) > THRESHOLD:
            print("[auto_compact triggered]")
            messages[:] = auto_compact(messages)

        response = completion(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_unset=True))

        if not message.tool_calls:
            return

        manual_compact = False
        for tc in message.tool_calls:
            args = json.loads(tc.function.arguments)

            if tc.function.name == "compact":
                manual_compact = True
                output = "Compressing..."
            else:
                handler = TOOL_HANDLERS.get(tc.function.name)
                try:
                    output = handler(**args) if handler else f"Unknown tool: {tc.function.name}"
                except Exception as e:
                    output = f"Error: {e}"

            print(f"> {tc.function.name}: {str(output)[:200]}")

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": tc.function.name,
                "content": str(output),
            })

        # Layer 3: manual compact triggered by the compact tool
        if manual_compact:
            print("[manual compact]")
            messages[:] = auto_compact(messages)


# -- Main REPL --

def main():
    print(f"Context Compaction Agent 06 - {WORKDIR}")
    print("Type 'exit' to quit.\n")

    history = [{"role": "system", "content": SYSTEM}]

    # One-shot mode via sys.argv
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        history.append({"role": "user", "content": query})
        agent_loop(history)
        last = history[-1]
        if isinstance(last, dict):
            print(last.get("content", ""))
        return

    while True:
        try:
            query = input("\033[36ms06 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break

        history.append({"role": "user", "content": query})
        agent_loop(history)

        # Print assistant response
        last = history[-1]
        if isinstance(last, dict):
            print(last.get("content") or "")
        print()


if __name__ == "__main__":
    main()
