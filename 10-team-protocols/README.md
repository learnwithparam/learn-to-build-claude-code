# 10: Team Protocols — Shutdown + Plan Approval FSMs

> **Key Insight**: Same request_id correlation pattern, two domains.

## What You'll Learn

- **Shutdown protocol** — graceful teammate termination with approval
- **Plan approval protocol** — teammates submit plans for lead review
- **Request correlation** — matching requests to responses via request_id
- **FSM patterns** — finite state machines for protocol management

## Prerequisites

- Completed [09: Agent Teams](../09-agent-teams/README.md)
- Understand team messaging and teammate lifecycle

## How to Run

```bash
make 10-team-protocols
# or
uv run python 10-team-protocols/agent.py
```

## What's New vs Module 09

| Feature | 09 (Agent Teams) | 10 (Team Protocols) |
|---------|-----------------|---------------------|
| Shutdown | Teammates just stop | Graceful request/approve cycle |
| Planning | Teammates act freely | Plans need lead approval |
| Coordination | Messages only | Structured protocols with request_id |
| Tools | 9 | 12 (+ shutdown_request, shutdown_response, plan_approval) |

## Key Concept: Request-Response Correlation

```
Shutdown FSM:
  Lead ──[shutdown_request {request_id: "abc"}]──> Teammate
  Lead <──[shutdown_response {request_id: "abc", approve: true}]── Teammate

  Trackers: {"abc": {"target": "alice", "status": "approved"}}

Plan Approval FSM:
  Teammate ──[plan_approval {plan: "..."}]──> Lead
  Teammate <──[plan_approval_response {request_id: "xyz", approve: true}]── Lead
```

Both protocols use the same pattern: generate a request_id, send request, track state, match response.

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~490 | Lead with shutdown and plan approval protocols |

## Next Module

Ready for autonomous agents? → [11: Autonomous Agents](../11-autonomous-agents/README.md)
