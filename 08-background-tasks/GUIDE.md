# 08 Guide: Background Tasks

## The Problem: Blocking Execution

Every tool call in modules 01-07 blocks the agent loop. The model waits for the command to finish before it can think about anything else.

```
Sequential:
  [run tests (30s)] ──wait── [lint (10s)] ──wait── [build (20s)]
  Total: 60s, agent idle for most of it

Parallel:
  [run tests (30s)]
  [lint (10s)]       ← all start immediately
  [build (20s)]
  Total: 30s, agent keeps working
```

## The Solution: BackgroundManager

```python
class BackgroundManager:
    def __init__(self):
        self.tasks = {}               # task_id -> {status, result, command}
        self._notification_queue = []  # completed results, thread-safe
        self._lock = threading.Lock()

    def run(self, command):
        """Start a daemon thread, return task_id immediately."""
        task_id = str(uuid.uuid4())[:8]
        thread = threading.Thread(target=self._execute, args=(task_id, command), daemon=True)
        thread.start()
        return f"Background task {task_id} started"

    def drain_notifications(self):
        """Return and clear all pending completions."""
        with self._lock:
            notifs = list(self._notification_queue)
            self._notification_queue.clear()
        return notifs
```

## The Drain Pattern

Before each LLM call, drain the notification queue:

```python
def agent_loop(messages):
    while True:
        # Drain background results and inject as context
        notifs = BG.drain_notifications()
        if notifs:
            messages.append({"role": "user", "content": format_notifications(notifs)})
            messages.append({"role": "assistant", "content": "Noted background results."})

        # Normal LLM call
        response = completion(model=MODEL, messages=messages, tools=TOOLS)
        # ... handle response ...
```

This ensures the model sees background results at the right time — between turns, not mid-tool-call.

## Thread Safety

The `_lock` protects the notification queue:
- Background threads write to it (append results)
- Main thread reads from it (drain before LLM call)
- Without the lock, concurrent access could corrupt the list

## Design Rationale

| Choice | Why |
|--------|-----|
| Daemon threads | Die when main process exits (no orphans) |
| UUID task IDs | No global counter needed |
| Notification queue | Decouples execution from delivery |
| Drain before LLM | Model gets fresh context each turn |

## The Bigger Picture

Claude Code runs background tasks for things like:
- Test suites while the agent continues coding
- Build processes that report back when done
- Linting that doesn't block the main loop

The pattern is always: spawn, continue, collect results later.

---

**Non-blocking is the default for production agents.**

[← Task System Guide](../07-task-system/GUIDE.md) | [Back to README](./README.md) | [Next: Agent Teams →](../09-agent-teams/GUIDE.md)
