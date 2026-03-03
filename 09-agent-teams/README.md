# 09: Agent Teams — TeammateManager + MessageBus

> **Key Insight**: Teammates that can talk to each other.

## What You'll Learn

- **Persistent teammates** — named agents that live beyond a single task
- **JSONL inboxes** — file-based append/drain messaging
- **TeammateManager** — spawning and tracking team members
- **MessageBus** — structured communication between agents

## Prerequisites

- Completed [08: Background Tasks](../08-background-tasks/README.md)
- Understand threaded execution and notification patterns

## How to Run

```bash
make 09-agent-teams
# or
uv run python 09-agent-teams/agent.py

# Check team status
# Type /team in the REPL
# Type /inbox to read lead's inbox
```

## What's New vs Module 08

| Feature | 08 (Background Tasks) | 09 (Agent Teams) |
|---------|----------------------|-----------------|
| Agents | Single agent + bg threads | Lead + named teammates |
| Communication | Notification queue | Bidirectional JSONL inboxes |
| Lifecycle | Fire and forget | Persistent (spawn → work → idle) |
| Identity | Anonymous threads | Named roles (alice, bob) |

## Key Concept: JSONL Inboxes

```
.team/inbox/
  alice.jsonl    ← messages for alice (append-only)
  bob.jsonl      ← messages for bob
  lead.jsonl     ← messages for the lead

send_message("alice", "fix the auth bug"):
  → append to alice.jsonl

read_inbox("alice"):
  → read all lines, clear file (drain)
```

## Message Types

| Type | Purpose |
|------|---------|
| `message` | Normal text message |
| `broadcast` | Sent to all teammates |
| `shutdown_request` | Request graceful shutdown (used in module 10) |
| `shutdown_response` | Approve/reject shutdown (used in module 10) |
| `plan_approval_response` | Approve/reject plan (used in module 10) |

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~410 | Lead agent with TeammateManager and MessageBus |

## Next Module

Ready for team protocols? → [10: Team Protocols](../10-team-protocols/README.md)
