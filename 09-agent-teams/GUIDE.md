# 09 Guide: Agent Teams

## The Shift: From Subagents to Teammates

Module 05 introduced subagents — isolated agents that execute a task and return. But subagents are ephemeral: they're created, they work, they die.

```
Subagent (module 05):  spawn → execute → return summary → destroyed
Teammate (module 09):  spawn → work → idle → work → ... → shutdown
```

Teammates persist. They have names, roles, and can communicate with each other.

## The MessageBus

Communication happens through JSONL (JSON Lines) files:

```python
class MessageBus:
    def send(self, sender, to, content, msg_type="message"):
        msg = {"type": msg_type, "from": sender, "content": content, "timestamp": time.time()}
        with open(f"{to}.jsonl", "a") as f:  # append-only
            f.write(json.dumps(msg) + "\n")

    def read_inbox(self, name):
        messages = [json.loads(line) for line in read_all_lines(f"{name}.jsonl")]
        clear_file(f"{name}.jsonl")  # drain after reading
        return messages
```

Key design: **append/drain**. Writers append, readers drain (read + clear). This avoids complex locking.

## The TeammateManager

Manages the lifecycle of persistent teammates:

```python
class TeammateManager:
    def spawn(self, name, role, prompt):
        # 1. Register in config.json
        # 2. Start daemon thread with teammate's agent loop
        # 3. Teammate runs up to 50 iterations
        # 4. When done, status → "idle"
```

Each teammate gets:
- Its own system prompt (based on role)
- Its own message history (context isolation)
- Access to base tools + messaging tools
- A JSONL inbox for receiving messages

## Typical Team Flow

```
User: "Build a REST API with tests"

Lead Agent:
  1. spawn_teammate("alice", "backend", "Build the REST API endpoints")
  2. spawn_teammate("bob", "tester", "Write tests for the REST API")
  3. send_message("bob", "Wait for alice to finish the API first")

  alice: [works on API] → sends "API done" to lead
  bob:   [reads inbox] → [writes tests] → sends "Tests done" to lead

  Lead reads inbox: both done → summarizes to user
```

## Why JSONL?

| Alternative | Problem |
|------------|---------|
| Shared memory | Thread safety nightmare |
| Database | Heavy dependency |
| Sockets | Complex setup |
| JSONL files | Simple, append-only, observable |

You can inspect any inbox: `cat .team/inbox/alice.jsonl`

## The Bigger Picture

Claude Code's agent teams work similarly:
- Named agents with specific roles
- Message passing for coordination
- File-based state for observability
- The lead orchestrates, teammates execute

---

**Teams turn a single agent into an organization.**

[← Background Tasks Guide](../08-background-tasks/GUIDE.md) | [Back to README](./README.md) | [Next: Team Protocols →](../10-team-protocols/GUIDE.md)
