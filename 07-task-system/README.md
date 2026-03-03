# 07: Task System — File-Based DAG Task Graph

> **Key Insight**: State that survives compression -- because it's outside the conversation.

## What You'll Learn

- **Persistent task state** — JSON files in `.tasks/` that survive context compression
- **Dependency graphs** — blockedBy/blocks edges between tasks
- **Automatic unblocking** — completing a task frees its dependents
- **External state** — why keeping state outside the conversation is critical

## Prerequisites

- Completed [06: Context Compaction](../06-context-compaction/README.md)
- Understand the 3-layer compression pipeline

## How to Run

```bash
make 07-task-system
# or
uv run python 07-task-system/agent.py
```

## What's New vs Module 06

| Feature | 06 (Compaction) | 07 (Task System) |
|---------|----------------|-----------------|
| Planning | In conversation (lost on compress) | Persisted to .tasks/ |
| Dependencies | None | DAG with blockedBy/blocks |
| Visibility | TodoManager (in-memory) | File-based (survives restarts) |
| Tool count | 6 | 8 (+ task_create, task_update, task_list, task_get) |

## Key Concept: External State

```
.tasks/
  task_1.json  {"id":1, "subject":"...", "status":"completed"}
  task_2.json  {"id":2, "blockedBy":[1], "status":"pending"}
  task_3.json  {"id":3, "blockedBy":[2], "status":"pending"}

Dependency resolution:
  task_1 ──> task_2 ──> task_3
  (done)     (unblocked)  (still blocked)
```

Completing task 1 removes it from task 2's `blockedBy` list, making task 2 actionable.

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~250 | Agent with TaskManager and dependency graph |

## Next Module

Ready for background execution? → [08: Background Tasks](../08-background-tasks/README.md)
