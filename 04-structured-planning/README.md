# 04: Structured Planning — Structured Planning with Todos

> **Key Insight**: Structure constrains AND enables. Good constraints are scaffolding.

## What You'll Learn

- **Explicit planning** — making the model's plan visible to both you and the model
- **Constraint design** — how limits (max items, one in_progress) improve behavior
- **Soft prompting** — using reminders to guide behavior without forcing it
- **The "Context Fade" problem** — why invisible plans fail on complex tasks

## Prerequisites

- Completed [03: Tool Design](../03-tool-design/README.md)
- Understand the 4-tool agent pattern

## How to Run

```bash
make 04-structured-planning
# or
uv run python 04-structured-planning/agent.py
```

## What's New vs Intermediate

| Feature | Intermediate | Advanced |
|---------|-------------|----------|
| Planning | In model's head | Explicit TodoManager |
| Focus | Can drift | One in_progress enforced |
| Visibility | Opaque | See the checklist |
| Reminders | None | INITIAL + NAG reminders |

## The Problem

```
Intermediate: "I'll do A, then B, then C"  (invisible)
    After 10 tool calls: "Wait, what was I doing?"

Advanced:
  [ ] Refactor auth module
  [>] Add unit tests         <- Currently here
  [ ] Update documentation
```

## Key Concept: TodoManager Constraints

| Rule | Why |
|------|-----|
| Max 20 items | Prevents infinite lists |
| One in_progress | Forces focus |
| Required fields | Structured output |
| activeForm | Real-time visibility ("Reading files...") |

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~310 | 5-tool agent with TodoManager |

## Next Module

Ready for subagents and skills? → [05: Subagents & Skills](../05-subagents-and-skills/README.md)
