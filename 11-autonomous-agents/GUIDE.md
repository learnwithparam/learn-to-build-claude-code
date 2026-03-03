# 11 Guide: Autonomous Agents

## The Problem: Passive Teammates

In modules 09-10, teammates only work when the lead tells them to. They can't find work on their own. If new tasks appear on the board, someone has to manually assign them.

## The Solution: WORK/IDLE Lifecycle

Instead of stopping when a task is done, teammates enter an **idle phase** where they actively look for more work:

```python
while True:
    # -- WORK PHASE --
    for _ in range(50):
        response = completion(...)
        if not message.tool_calls:
            break  # No more work → go idle
        # Execute tools...

    # -- IDLE PHASE --
    for _ in range(polls):
        time.sleep(5)

        # Check inbox for messages
        inbox = BUS.read_inbox(name)
        if inbox:
            resume = True
            break

        # Scan task board for unclaimed work
        unclaimed = scan_unclaimed_tasks()
        if unclaimed:
            claim_task(unclaimed[0]["id"], name)
            resume = True
            break

    if not resume:
        # Timed out → shutdown
        return
```

## Task Board Scanning

The key function finds actionable tasks:

```python
def scan_unclaimed_tasks():
    unclaimed = []
    for f in TASKS_DIR.glob("task_*.json"):
        task = json.loads(f.read_text())
        if (task["status"] == "pending"      # Not started
                and not task["owner"]         # Nobody claimed it
                and not task["blockedBy"]):   # No dependencies
            unclaimed.append(task)
    return unclaimed
```

Three conditions must all be true: pending status, no owner, and no blockers.

## Claiming with Thread Safety

Multiple teammates might scan simultaneously:

```python
_claim_lock = threading.Lock()

def claim_task(task_id, owner):
    with _claim_lock:
        task = load_task(task_id)
        task["owner"] = owner
        task["status"] = "in_progress"
        save_task(task)
```

The lock prevents two teammates from claiming the same task.

## Identity Re-Injection

After context compression, a teammate might lose its identity:

```python
def make_identity_block(name, role, team_name):
    return {
        "role": "user",
        "content": f"<identity>You are '{name}', role: {role}, team: {team_name}.</identity>",
    }

# Before resuming work after compression:
if len(messages) <= 4:  # Short history = likely compressed
    messages.insert(1, make_identity_block(name, role, team_name))
    messages.insert(2, {"role": "assistant", "content": f"I am {name}. Continuing."})
```

This ensures the teammate remembers who it is even after a summary replaces its history.

## Design Rationale

| Choice | Why |
|--------|-----|
| 5s poll interval | Responsive without being wasteful |
| 60s idle timeout | Don't keep idle threads forever |
| Claim lock | Prevent double-claiming |
| Identity re-injection | Context compression erases identity |

## The Bigger Picture

Claude Code's agent model is similar:
- Agents that pick up tasks from a queue
- Idle polling between work phases
- Identity preservation across context boundaries
- Autonomous decision-making about what to work on next

---

**The best agents don't wait to be told what to do.**

[← Team Protocols Guide](../10-team-protocols/GUIDE.md) | [Back to README](./README.md) | [Next: Worktree Isolation →](../12-worktree-isolation/GUIDE.md)
