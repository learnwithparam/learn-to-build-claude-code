# 12 Guide: Worktree Isolation

## The Problem: Shared State Conflicts

When multiple agents work on the same codebase, they share the same files. Agent A edits `src/auth.py` while Agent B is reading it. Chaos.

```
Without isolation:
  Agent A: edit src/auth.py (refactoring)
  Agent B: read src/auth.py (testing)    ← sees half-finished refactor
  Agent B: "Tests fail!"                 ← false alarm
```

## The Solution: Git Worktrees

Git worktrees create separate working directories, each on its own branch:

```
Main repo:           .worktrees/auth-refactor/    .worktrees/add-tests/
  src/auth.py          src/auth.py (modified)       src/auth.py (original)
  src/main.py          src/main.py                  src/main.py
```

Each worktree is a real directory with its own files. Changes in one don't affect others.

## Two-Plane Architecture

### Control Plane: Task Board

```python
class TaskManager:
    def bind_worktree(self, task_id, worktree_name):
        task["worktree"] = worktree_name
        task["status"] = "in_progress"
```

Tasks track *what* needs to be done and *where* it's being done.

### Execution Plane: Worktrees

```python
class WorktreeManager:
    def create(self, name, task_id=None):
        # git worktree add -b wt/name .worktrees/name HEAD
        # If task_id: bind task to this worktree

    def run(self, name, command):
        # Execute command inside the worktree directory
        subprocess.run(command, cwd=worktree_path)

    def remove(self, name, complete_task=False):
        # git worktree remove .worktrees/name
        # If complete_task: mark bound task as completed
```

## The Event Bus

Append-only lifecycle logging:

```python
class EventBus:
    def emit(self, event, task=None, worktree=None):
        payload = {"event": event, "ts": time.time(), "task": task, "worktree": worktree}
        with open("events.jsonl", "a") as f:
            f.write(json.dumps(payload) + "\n")
```

Events provide a timeline of everything that happened:
- `worktree.create.before` / `worktree.create.after`
- `worktree.remove.before` / `worktree.remove.after`
- `task.completed`
- `worktree.keep`

## Typical Workflow

```
1. task_create("Refactor auth module")         → task #1
2. worktree_create("auth-refactor", task_id=1) → .worktrees/auth-refactor/
3. worktree_run("auth-refactor", "npm test")   → runs in isolated dir
4. worktree_run("auth-refactor", "git add . && git commit -m 'refactor'")
5. worktree_remove("auth-refactor", complete_task=True)
   → removes worktree, marks task #1 completed
```

## Design Rationale

| Choice | Why |
|--------|-----|
| Git worktrees | Built-in, lightweight, branch-based |
| Name validation | Prevent path traversal attacks |
| Event bus | Observability without cluttering task state |
| Bidirectional binding | Tasks reference worktrees, index tracks tasks |
| Keep option | Sometimes you want to preserve a worktree |

## The Bigger Picture

Claude Code uses worktrees for exactly this purpose:
- Each task gets an isolated directory
- Commands run inside the worktree, not the main repo
- When done, the worktree can be kept (for review) or removed (cleanup)
- Events provide an audit trail

This is the culmination of the workshop: a complete system with task management, team coordination, and execution isolation.

---

**Isolation turns parallel work from dangerous to safe.**

[← Autonomous Agents Guide](../11-autonomous-agents/GUIDE.md) | [Back to README](./README.md)
