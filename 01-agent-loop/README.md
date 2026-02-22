# 01: The Agent Loop — The 17-Line Agent

> **Key Insight**: An AI coding agent is just a loop that lets a model call tools.

## What You'll Learn

- The **agent loop** — the pattern behind every AI coding agent
- That one tool (bash) is enough for full capability
- How simple the "magic" behind Claude Code, Cursor, etc. really is

## Prerequisites

- Python 3.10+ installed
- Anthropic API key configured in `.env`
- `make install` completed

## How to Run

```bash
make noob
# or
uv run python 01-agent-loop/agent.py
```

## What to Observe

1. **The loop** — the agent keeps calling bash until it decides the task is done
2. **The model decides** — you don't tell it which commands to run, it figures it out
3. **One tool is enough** — bash gives access to everything: files, search, execution

## Key Concept

```
User → Model → [bash → result]* → Response
                  ^____________|
```

The asterisk (*) means "repeat until done." That's the whole secret.

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | 17 | The complete agent |

## Next Module

Ready for more? → [02: Bash Agent](../02-bash-agent/README.md)
