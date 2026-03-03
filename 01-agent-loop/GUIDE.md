# 01 Guide: The Minimal Agent

## The Core Truth

Every AI coding agent — Claude Code, Cursor, Codex CLI, Devin — is built on the same pattern:

```python
while True:
    response = completion(model=MODEL, messages=messages, tools=TOOLS)
    message = response.choices[0].message
    if not message.tool_calls:
        return message.content
    for tc in message.tool_calls:
        result = execute(tc.function.name, tc.function.arguments)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
```

That's it. The model calls tools until it's done. Everything else is refinement.

## Why Bash is Enough

Unix philosophy: everything is a file, everything can be piped.

| You need | Bash command |
|----------|-------------|
| Read files | `cat`, `head`, `grep` |
| Write files | `echo '...' > file` |
| Search | `find`, `grep`, `rg` |
| Execute | `python`, `npm`, `make` |
| **Subagent** | `python 01-agent-loop/agent.py "task"` |

The last line is the key insight: **calling itself via bash implements subagents**. No special framework needed — just recursion through process spawning.

## How Subagents Work

```
Main Agent
  └─ bash: python 01-agent-loop/agent.py "analyze architecture"
       └─ Subagent (isolated process, fresh history)
            ├─ bash: find . -name "*.py"
            ├─ bash: cat src/main.py
            └─ Returns summary via stdout
```

**Process isolation = Context isolation**:
- Child process has its own `history=[]`
- Parent captures stdout as tool result
- Recursive calls enable unlimited nesting

## What 17 Lines Proves

1. **One tool is enough** — Bash is the gateway to everything
2. **Recursion = hierarchy** — Self-calls implement subagents
3. **Process = isolation** — OS provides context separation
4. **Prompt = constraint** — Instructions shape behavior

## What's Missing (and Why)

| Feature | Status | Added In |
|---------|--------|----------|
| Multiple tools | ❌ | [Tool Design](../03-tool-design/) |
| Todo tracking | ❌ | [Structured Planning](../04-structured-planning/) |
| Agent types | ❌ | [Subagents & Skills](../05-subagents-and-skills/) |
| Skills/knowledge | ❌ | [Subagents & Skills](../05-subagents-and-skills/) |

That's the point — you don't need any of it for a working agent.

---

**Bash is All You Need.**

[← README](./README.md) | [Next: Bash Agent →](../02-bash-agent/GUIDE.md)
