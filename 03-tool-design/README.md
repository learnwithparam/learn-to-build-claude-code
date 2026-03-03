# 03: Tool Design — The 4-Tool Agent

> **Key Insight**: The model IS the agent. Code just provides tools and runs the loop.

## What You'll Learn

- The **four essential tools** that cover 90% of coding tasks
- **Tool design** — how to give AI models real-world capabilities
- **Path safety** — preventing the agent from escaping the workspace
- **Separation of concerns** — tool definitions vs implementations vs agent loop

## Prerequisites

- Completed [02: Bash Agent](../02-bash-agent/README.md)
- Understand the one-tool agent pattern

## How to Run

```bash
make 03-tool-design
# or
uv run python 03-tool-design/agent.py
```

## What's New vs Beginner

| Feature | Beginner | Intermediate |
|---------|----------|--------------|
| Tools | 1 (bash) | 4 (bash, read, write, edit) |
| File ops | Via bash | Native tools |
| Safety | Minimal | Path validation |
| Edit precision | bash sed | Exact string match |

## The Four Essential Tools

```
bash       → Run any command (git, npm, python)
read_file  → Read file contents with line limits
write_file → Create/overwrite files
edit_file  → Surgical text replacement
```

With these 4 tools, the model can do everything Claude Code does for 90% of tasks.

## Key Concept: Tool Design

Each tool has:
1. **A name** — how the model refers to it
2. **A description** — what the model reads to decide when to use it
3. **An input schema** — structured parameters for reliable calling
4. **An implementation** — the actual Python function

The model never sees the implementation — only the schema and description.

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~270 | 4-tool agent with path safety |

## Next Module

Ready for structured planning? → [04: Structured Planning](../04-structured-planning/README.md)
