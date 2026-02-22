# 05: Subagents & Skills — Subagents + Skills

> **Key Insight**: Subagents isolate context. Skills inject expertise. Together they make a production-grade agent.

## What You'll Learn

- **Context isolation** — how subagents keep the main conversation clean
- **Agent types** — explore, code, plan — each with filtered tools
- **Knowledge externalization** — teaching AI through editable files instead of training
- **Cache-preserving injection** — why skills go in tool results, not system prompts
- **Progressive disclosure** — loading knowledge on-demand to keep context lean

## Prerequisites

- Completed [04: Structured Planning](../04-structured-planning/README.md)
- Understand TodoManager and structured planning

## How to Run

```bash
# Full agent with subagents + skills
make expert
# or
uv run python 05-subagents-and-skills/agent.py

# Subagent-only version (intermediate step)
uv run python 05-subagents-and-skills/subagent.py
```

## This Level Has Two Parts

### Part 1: Subagents (`subagent.py`)

The **Task tool** — spawn child agents with isolated context:

| Agent Type | Tools | Purpose |
|------------|-------|---------|
| `explore` | bash, read_file | Read-only search & analysis |
| `code` | all tools | Full implementation |
| `plan` | bash, read_file | Design without modifying |

### Part 2: Skills (`agent.py`)

The **Skill tool** — load domain knowledge on-demand:

| Skill | Description |
|-------|-------------|
| `agent-builder` | How to build AI agents |
| `code-review` | Systematic code review checklist |
| `mcp-builder` | MCP server development |
| `pdf` | PDF processing techniques |

## Key Concepts

### Context Pollution Problem
```
Single-Agent:  cat file1 → cat file2 → ... 15 files ... → "What was I doing?"
With Subagent: Task(explore) → clean summary → continue with clean context
```

### Tools vs Skills
```
Tools  = What model CAN do   (bash, read_file, write_file)
Skills = How model KNOWS to do   (PDF processing, MCP dev)
```

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`subagent.py`](./subagent.py) | ~620 | Part 1: Subagent mechanism |
| [`agent.py`](./agent.py) | ~780 | Part 2: Full agent with skills |

## Workshop Complete! 🎉

You've built a fully capable AI coding agent from scratch:

```
Noob       → 17 lines, 1 tool      → "The loop"
Beginner   → ~130 lines, 1 tool    → "Structure matters"
Intermediate → ~270 lines, 4 tools → "The model IS the agent"
Advanced   → ~310 lines, 5 tools   → "Make plans visible"
Expert     → ~780 lines, 7 tools   → "Divide, conquer, and know"
```
