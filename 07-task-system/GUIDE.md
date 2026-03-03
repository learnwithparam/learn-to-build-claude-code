# 07 Guide: Task System

## The Problem: State Lost to Compression

Module 06 added context compaction. But there's a catch: when the conversation is compressed, the agent's mental plan disappears with it.

```
Before compression:
  Agent: "I need to: 1) refactor auth, 2) add tests, 3) update docs"
  (This lives only in the conversation)

After compression:
  Agent: "Previous conversation was about refactoring..."
  (The detailed plan is gone)
```

Module 04's TodoManager had the same problem — it stored state in a Python object that only exists during the session.

## The Solution: File-Based Tasks

Tasks persist as JSON files in `.tasks/`:

```
.tasks/
  task_1.json  {"id": 1, "subject": "Refactor auth", "status": "completed"}
  task_2.json  {"id": 2, "subject": "Add tests", "blockedBy": [1], "status": "pending"}
  task_3.json  {"id": 3, "subject": "Update docs", "blockedBy": [2], "status": "pending"}
```

Even if the conversation is compressed, tasks survive because they live on disk.

## Dependency Resolution

The key insight is the DAG (Directed Acyclic Graph):

```python
def _clear_dependency(self, completed_id):
    """When task completes, remove it from all blockedBy lists."""
    for f in self.dir.glob("task_*.json"):
        task = json.loads(f.read_text())
        if completed_id in task.get("blockedBy", []):
            task["blockedBy"].remove(completed_id)
            self._save(task)
```

Completing task 1 automatically makes task 2 actionable.

## Task Tools

Four new tools for the agent:

| Tool | Purpose |
|------|---------|
| `task_create` | Create a new task with subject and description |
| `task_update` | Change status, add dependencies |
| `task_list` | Show all tasks with status markers |
| `task_get` | Get full details of one task |

## Why File-Based?

| Alternative | Problem |
|------------|---------|
| In-memory dict | Lost on process exit |
| Database | Overkill, adds dependency |
| Single JSON file | Lock contention with multiple agents |
| Individual JSON files | Simple, atomic, observable |

Individual files make it easy to inspect state (`cat .tasks/task_1.json`) and avoid file locking issues when multiple agents write concurrently.

## The Bigger Picture

Claude Code uses a similar approach with its task system:
- Tasks persist across conversation compression
- Dependencies track what's blocked
- Status tracking shows progress
- The agent can resume work after any interruption

---

**State outside the conversation is state that survives.**

[← Context Compaction Guide](../06-context-compaction/GUIDE.md) | [Back to README](./README.md) | [Next: Background Tasks →](../08-background-tasks/GUIDE.md)
