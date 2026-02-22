# 04 Guide: Structured Planning

## The Problem: Context Fade

In the Intermediate agent, plans exist only in the model's "head":

```
"I'll do A, then B, then C"  (invisible)
After 10 tool calls: "Wait, what was I doing?"
```

This is "Context Fade" — as the conversation grows, early intentions get buried under tool results. The model loses track.

## The Solution: TodoWrite

One new tool that fundamentally changes behavior:

```python
{
    "name": "TodoWrite",
    "input_schema": {
        "items": [{
            "content": "Task description",
            "status": "pending | in_progress | completed",
            "activeForm": "Present tense: 'Reading files'"
        }]
    }
}
```

The `activeForm` gives real-time visibility:

```
[>] Reading authentication code...  <- activeForm
[ ] Add unit tests
```

## The TodoManager

A list with constraints:

```python
class TodoManager:
    def __init__(self):
        self.items = []  # Max 20

    def update(self, items):
        # Each needs: content, status, activeForm
        # Status: pending | in_progress | completed
        # Only ONE can be in_progress
```

### Why These Constraints?

| Rule | Why |
|------|-----|
| Max 20 items | Prevents infinite task lists |
| One in_progress | Forces focus on one thing |
| Required fields | Structured, parseable output |

These aren't arbitrary — they're **guardrails** that make the model more effective.

## System Reminders (Soft Prompts)

```python
# Shown at conversation start
INITIAL_REMINDER = "<reminder>Use TodoWrite for multi-step tasks.</reminder>"

# Shown if model hasn't updated todos in 10+ rounds
NAG_REMINDER = "<reminder>10+ turns without todo update. Please update todos.</reminder>"
```

Key insight: NAG_REMINDER is injected **inside the agent loop**, so the model sees it during long-running tasks, not just between tasks.

## The Feedback Loop

When model calls `TodoWrite`:

```
Input:
  [x] Refactor auth (completed)
  [>] Add tests (in_progress)
  [ ] Update docs (pending)

Returned:
  "[x] Refactor auth
   [>] Add tests
   [ ] Update docs
   (1/3 completed)"
```

Model sees its own plan. Updates it. Continues with context.

## When Todos Help

Not every task needs them:

| Good For | Why |
|----------|-----|
| Multi-step work | 5+ steps to track |
| Long conversations | 20+ tool calls |
| Complex refactoring | Multiple files |
| Teaching | Visible "thinking" |

Rule of thumb: **if you'd write a checklist, use todos**.

## The Deeper Insight

> **Structure constrains AND enables.**

Todo constraints (max items, one in_progress) **enable** (visible plan, tracked progress).

This pattern appears everywhere in agent design:
- `max_tokens` constrains → enables manageable responses
- Tool schemas constrain → enable structured calls
- Todos constrain → enable complex task completion

Good constraints aren't limitations. They're scaffolding.

---

**Explicit planning makes agents reliable.**

[← Tool Design Guide](../03-tool-design/GUIDE.md) | [Back to README](./README.md) | [Next: Subagents & Skills →](../05-subagents-and-skills/GUIDE.md)
