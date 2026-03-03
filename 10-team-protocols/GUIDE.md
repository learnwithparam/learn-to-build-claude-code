# 10 Guide: Team Protocols

## The Problem: Uncoordinated Teams

Module 09's teammates work independently. But what happens when:
- You need to shut down a teammate that's mid-task?
- A teammate wants to make a major change and should check first?

Without protocols, the lead has no control over teammate behavior.

## The Shutdown Protocol

A finite state machine (FSM) with two states:

```
Lead sends:     shutdown_request {request_id: "abc"}
                        |
                        v
Teammate receives:  "Should I shut down?"
                    decides: approve or reject
                        |
                        v
Teammate sends:  shutdown_response {request_id: "abc", approve: true}
                        |
                        v
Lead receives:   status → "shutdown", teammate thread stops
```

The `request_id` correlates the request with the response. Without it, you couldn't match which shutdown request a response belongs to.

## The Plan Approval Protocol

Same pattern, different direction:

```
Teammate sends:   plan_approval {plan: "I want to refactor auth"}
                        |
                        v
Lead receives:    reviews the plan text
                  decides: approve or reject
                        |
                        v
Lead sends:       plan_approval_response {request_id: "xyz", approve: true}
                        |
                        v
Teammate:         proceeds with plan (or revises if rejected)
```

## The Unified Pattern: Request-ID Correlation

Both protocols share the same structure:

```python
# Trackers store pending requests
shutdown_requests = {}  # {request_id: {"target": name, "status": "pending"}}
plan_requests = {}      # {request_id: {"from": name, "plan": text, "status": "pending"}}

# Send: generate ID, track, send message
def send_request(target):
    req_id = str(uuid.uuid4())[:8]
    tracker[req_id] = {"target": target, "status": "pending"}
    bus.send("lead", target, content, msg_type, {"request_id": req_id})

# Receive: match ID, update status
def handle_response(request_id, approve):
    tracker[request_id]["status"] = "approved" if approve else "rejected"
```

## Thread Safety

The `_tracker_lock` protects shared state:

```python
_tracker_lock = threading.Lock()

with _tracker_lock:
    shutdown_requests[req_id] = {"target": name, "status": "pending"}
```

Both the lead thread and teammate threads access the trackers, so locking is essential.

## The Bigger Picture

Claude Code uses similar protocol patterns:
- Permission requests (can I run this command?)
- Plan approval (should I proceed with this approach?)
- Graceful shutdown (finish current work, then stop)

The request_id correlation pattern appears everywhere in distributed systems.

---

**Protocols turn chaos into coordination.**

[← Agent Teams Guide](../09-agent-teams/GUIDE.md) | [Back to README](./README.md) | [Next: Autonomous Agents →](../11-autonomous-agents/GUIDE.md)
