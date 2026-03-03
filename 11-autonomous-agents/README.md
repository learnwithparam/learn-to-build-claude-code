# 11: Autonomous Agents — WORK/IDLE Lifecycle + Auto-Claim

> **Key Insight**: The agent finds work itself.

## What You'll Learn

- **WORK/IDLE lifecycle** — teammates alternate between active work and polling
- **Task board scanning** — finding unclaimed, unblocked tasks automatically
- **Auto-claiming** — teammates pick up work without being told
- **Identity re-injection** — preserving agent identity after context compression

## Prerequisites

- Completed [10: Team Protocols](../10-team-protocols/README.md)
- Understand shutdown and plan approval protocols

## How to Run

```bash
make 11-autonomous-agents
# or
uv run python 11-autonomous-agents/agent.py

# Check team/tasks status
# Type /team, /inbox, or /tasks in the REPL
```

## What's New vs Module 10

| Feature | 10 (Team Protocols) | 11 (Autonomous Agents) |
|---------|---------------------|----------------------|
| Task assignment | Lead assigns work | Teammates find work themselves |
| Idle behavior | Teammate stops | Polls for new tasks every 5s |
| Identity | Set once at spawn | Re-injected after compression |
| Lifecycle | spawn → work → idle | spawn → work → idle → work → ... |

## Key Concept: Autonomous Lifecycle

```
+-------+
| spawn |
+---+---+
    |
    v
+-------+  tool_use    +-------+
| WORK  | <----------- |  LLM  |
+---+---+              +-------+
    |
    | no more tool calls
    v
+--------+
| IDLE   | poll every 5s for up to 60s
+---+----+
    |
    +---> check inbox → message? → resume WORK
    |
    +---> scan .tasks/ → unclaimed? → claim → resume WORK
    |
    +---> timeout (60s) → shutdown
```

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~580 | Autonomous teammates with idle polling and auto-claim |

## Next Module

Ready for the final module? → [12: Worktree Isolation](../12-worktree-isolation/README.md)
