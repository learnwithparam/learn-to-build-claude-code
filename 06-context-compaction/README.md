# 06: Context Compaction — Three-Layer Compression

> **Key Insight**: The agent can forget strategically and keep working forever.

## What You'll Learn

- **Token management** — why conversations eventually exhaust the context window
- **Three-layer compression** — micro, auto, and manual compaction
- **Transcript persistence** — saving full history before summarizing
- **Threshold-based triggers** — automatic compression at token limits

## Prerequisites

- Completed [05: Subagents & Skills](../05-subagents-and-skills/README.md)
- Understand subagent isolation and tool dispatch

## How to Run

```bash
make 06-context-compaction
# or
uv run python 06-context-compaction/agent.py
```

## What's New vs Module 05

| Feature | 05 (Subagents & Skills) | 06 (Context Compaction) |
|---------|------------------------|------------------------|
| Context management | None (grows forever) | 3-layer compression |
| Long sessions | Eventually fails | Works indefinitely |
| History | In-memory only | Saved to .transcripts/ |
| Tool count | 7 | 6 (bash, read, write, edit, compact + compression) |

## The Three Layers

```
Every turn:
  Layer 1: micro_compact (silent, every turn)
    → Replace old tool results with "[Previous: used bash]"

  Token check: > 50,000?
    → no: continue
    → yes: Layer 2: auto_compact
        → Save transcript to .transcripts/
        → LLM summarizes conversation
        → Replace all messages with summary

  Layer 3: compact tool (model-triggered)
    → Same as auto, but the model decides when
```

## Key Concept: Append-Only Context

```
Without compaction:
  msg1 → msg2 → msg3 → ... → msg500 → CONTEXT OVERFLOW

With compaction:
  msg1 → msg2 → msg3 → [micro_compact: trim old results]
  → ... → [auto_compact: save + summarize] → fresh start
  → msg1 → msg2 → ... (forever)
```

## Files

| File | Lines | Description |
|------|-------|-------------|
| [`agent.py`](./agent.py) | ~280 | Agent with 3-layer compression pipeline |

## Next Module

Ready for persistent task management? → [07: Task System](../07-task-system/README.md)
