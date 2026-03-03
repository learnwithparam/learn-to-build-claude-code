# 12: Worktree Isolation — Git Worktrees Per Task

> **Key Insight**: Isolate by directory, coordinate by task ID.

## What You'll Learn

- **Git worktrees** — parallel branches in separate directories
- **Task-worktree binding** — connecting tasks to execution environments
- **Control vs execution planes** — task board coordinates, worktrees execute
- **Event logging** — append-only lifecycle events for observability

## Prerequisites

- Completed [11: Autonomous Agents](../11-autonomous-agents/README.md)
- Understand autonomous task claiming and team coordination
- A git repository to work in (worktree tools require git)

## How to Run

```bash
make 12-worktree-isolation
# or
uv run python 12-worktree-isolation/agent.py
```

## What's New vs Module 11

| Feature | 11 (Autonomous) | 12 (Worktree Isolation) |
|---------|-----------------|------------------------|
| Isolation | Shared working directory | Separate worktree per task |
| Parallelism | Same files, risk of conflicts | Independent directories |
| Lifecycle | In-memory state | Persistent event log |
| Tools | 14 | 16 (+ worktree_create, worktree_run, etc.) |

## Key Concept: Two Planes

```
CONTROL PLANE (task board)     EXECUTION PLANE (worktrees)
+-------------------------+    +-------------------------+
| .tasks/                 |    | .worktrees/             |
|   task_1.json           |    |   auth-refactor/        |
|     worktree: "auth-*"  |--->|     (git worktree)      |
|   task_2.json           |    |   add-tests/            |
|     worktree: "add-*"   |--->|     (git worktree)      |
+-------------------------+    +-------------------------+
                               |   index.json            |
                               |   events.jsonl          |
                               +-------------------------+
```

Tasks track what needs to be done. Worktrees provide isolated environments to do it.

## Worktree Lifecycle

```
create  → active directory with its own branch
run     → execute commands inside the worktree
status  → check git status within the worktree
keep    → mark as kept (preserve for later)
remove  → delete worktree, optionally complete task
```

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~780 | Full agent with EventBus, TaskManager, WorktreeManager |

## Workshop Complete!

You've built a fully capable AI coding agent from scratch:

```
01  Agent Loop          → 17 lines, 1 tool     → "The loop"
02  Bash Agent          → ~130 lines, 1 tool   → "Structure matters"
03  Tool Design         → ~270 lines, 4 tools  → "The model IS the agent"
04  Structured Planning → ~310 lines, 5 tools  → "Make plans visible"
05  Subagents & Skills  → ~690 lines, 7 tools  → "Divide, conquer, know"
06  Context Compaction  → ~280 lines, 6 tools  → "Forget strategically"
07  Task System         → ~250 lines, 8 tools  → "State outside context"
08  Background Tasks    → ~240 lines, 6 tools  → "Don't block"
09  Agent Teams         → ~410 lines, 9 tools  → "Communicate"
10  Team Protocols      → ~490 lines, 12 tools → "Coordinate"
11  Autonomous Agents   → ~580 lines, 14 tools → "Find work"
12  Worktree Isolation  → ~780 lines, 16 tools → "Isolate execution"
```
