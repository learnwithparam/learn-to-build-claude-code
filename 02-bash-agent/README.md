# 02: Bash Agent — The Expanded Bash Agent

> **Key Insight**: One tool + proper structure = production-quality agent pattern.

## What You'll Learn

- How to **structure** an agent with proper error handling
- The difference between **interactive** and **subagent** modes
- How **process recursion** implements subagents for free
- Why **output truncation** and **timeouts** matter

## Prerequisites

- Completed [01: The Agent Loop](../01-agent-loop/README.md)
- Understand the basic agent loop

## How to Run

```bash
make 02-bash-agent
# or
uv run python 02-bash-agent/agent.py

# Subagent mode (try this!)
uv run python 02-bash-agent/agent.py "list all Python files and summarize what they do"
```

## What's New vs Noob

| Feature | Noob (17 lines) | Beginner (~50 lines) |
|---------|-----------------|---------------------|
| Structure | One-liner magic | Named functions, docstrings |
| Error handling | None | Timeouts, truncation |
| Modes | Interactive only | Interactive + Subagent |
| Comments | None | Full explanations |

## Key Concept: Subagent via Recursion

```
Main Agent
  └─ bash: python 02-bash-agent/agent.py "analyze architecture"
       └─ Subagent (isolated process, fresh history)
            ├─ bash: find . -name "*.py"
            ├─ bash: cat src/main.py
            └─ Returns summary via stdout
```

**Process isolation = Context isolation.** The subagent has no memory of the parent's conversation.

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~130 | Expanded bash agent with both modes |

## Next Module

Ready for multiple tools? → [03: Tool Design](../03-tool-design/README.md)
