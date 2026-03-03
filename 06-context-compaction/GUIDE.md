# 06 Guide: Context Compaction

## The Problem: Context Overflow

Every agent loop iteration adds messages. After enough tool calls, the conversation exceeds the model's context window and the agent breaks.

```
Turn 1:   [user] + [assistant] + [tool_result]     = ~500 tokens
Turn 10:  ... accumulated history ...                = ~5,000 tokens
Turn 100: ... very long history ...                  = ~50,000 tokens
Turn 200: CONTEXT OVERFLOW                           = failure
```

Real-world tasks (refactoring a large codebase, debugging) can easily hit 100+ tool calls.

## The Solution: Three-Layer Compression

### Layer 1: Micro Compaction (Every Turn)

Replace old tool result contents with short placeholders:

```python
# Before: tool result from 50 turns ago still has full 2000-char output
{"role": "tool", "content": "line 1: import os\nline 2: ...(2000 chars)..."}

# After: replaced with a short marker
{"role": "tool", "content": "[Previous: used read_file]"}
```

Only the last 3 tool results keep their full content. This is invisible to the user and barely affects the model's behavior since old results are rarely re-read.

### Layer 2: Auto Compaction (Threshold Trigger)

When estimated tokens exceed 50,000:

```python
def auto_compact(messages):
    # 1. Save full transcript to .transcripts/ (never lose data)
    save_transcript(messages)

    # 2. Ask LLM to summarize the conversation
    summary = llm_summarize(messages)

    # 3. Replace ALL messages with compact summary
    return [
        {"role": "user", "content": f"[Compressed]\n{summary}"},
        {"role": "assistant", "content": "Understood. Continuing."},
    ]
```

The transcript is saved to disk first, so nothing is permanently lost.

### Layer 3: Manual Compact Tool

The model can call `compact` to trigger compression on demand:

```python
TOOLS = [
    # ... other tools ...
    {"type": "function", "function": {
        "name": "compact",
        "description": "Trigger manual conversation compression.",
        "parameters": {"type": "object", "properties": {
            "focus": {"type": "string", "description": "What to preserve"}
        }}
    }}
]
```

This is useful when the model knows it's about to switch to a different phase of work.

## Token Estimation

A rough but effective heuristic:

```python
def estimate_tokens(messages):
    return len(str(messages)) // 4  # ~4 chars per token
```

Not exact, but close enough for threshold decisions. The alternative (calling a tokenizer) adds latency.

## Design Rationale

| Design Choice | Why |
|--------------|-----|
| 3 layers, not 1 | Different situations need different strategies |
| Micro is silent | Doesn't require LLM call, runs every turn |
| Auto saves transcript | Data preservation before destruction |
| Manual exists | Model sometimes knows best when to compress |
| Keep last 3 results | Recent results are actively used |

## The Bigger Picture

Claude Code uses a similar strategy:
- Recent tool results kept in full
- Older results summarized
- System prompt cached (never changes)
- Conversation compressed when needed

The key insight is that context is precious real estate. Most of what happened 50 turns ago doesn't matter for the current task.

---

**Strategic forgetting is a feature, not a bug.**

[← Subagents & Skills Guide](../05-subagents-and-skills/GUIDE.md) | [Back to README](./README.md) | [Next: Task System →](../07-task-system/GUIDE.md)
