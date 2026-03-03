# 08: Background Tasks — Daemon Threads + Notification Queue

> **Key Insight**: Fire and forget -- the agent doesn't block while the command runs.

## What You'll Learn

- **Background execution** — running commands in daemon threads
- **Notification queue** — thread-safe result delivery
- **Drain pattern** — injecting results before each LLM call
- **Non-blocking agents** — parallel command execution

## Prerequisites

- Completed [07: Task System](../07-task-system/README.md)
- Understand persistent task state

## How to Run

```bash
make 08-background-tasks
# or
uv run python 08-background-tasks/agent.py
```

## What's New vs Module 07

| Feature | 07 (Task System) | 08 (Background Tasks) |
|---------|-----------------|----------------------|
| Execution | Blocking (wait for each command) | Non-blocking (fire and forget) |
| Parallelism | Sequential tool calls | Multiple commands run simultaneously |
| Results | Immediate | Queued, delivered before next LLM call |
| Tools | 8 | 6 (+ background_run, check_background) |

## Key Concept: Drain Pattern

```
Agent ──[spawn A]──[spawn B]──[other work]──
            |           |
            v           v
         [A runs]    [B runs]      (parallel, daemon threads)
            |           |
            +── notification queue ──> [results injected before next LLM call]
```

The agent doesn't wait. It keeps working while background commands execute.

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~240 | Agent with BackgroundManager and notification queue |

## Next Module

Ready for multi-agent teams? → [09: Agent Teams](../09-agent-teams/README.md)
