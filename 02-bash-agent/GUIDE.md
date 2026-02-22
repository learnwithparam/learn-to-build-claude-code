# 02 Guide: Bash Agent Deep Dive

## From 17 Lines to Production Quality

The Noob agent proved the concept. Now we add the things that make it **reliable**:

### 1. Proper Function Structure

```python
def chat(prompt, history=None):
    """Named function with docstring, not a one-liner."""
    if history is None:
        history = []  # Avoid mutable default argument bug
    ...
```

### 2. Error Handling

```python
try:
    out = subprocess.run(cmd, shell=True, timeout=300, ...)
    output = out.stdout + out.stderr
except subprocess.TimeoutExpired:
    output = "(timeout after 300s)"
```

Without this, a `sleep 9999` command hangs your agent forever.

### 3. Output Truncation

```python
results.append({
    "content": output[:50000]  # Truncate very long outputs
})
```

A `cat` of a 10MB file would blow up the context window. Truncation is critical.

### 4. Dual Mode: Interactive + Subagent

```python
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(chat(sys.argv[1]))   # Subagent mode
    else:
        # Interactive REPL mode
        while True:
            query = input(">> ")
            print(chat(query, history))
```

This is how the agent calls itself: `python 02-bash-agent/agent.py "task"`.

## How Subagents Work

The key insight: **recursion through process spawning**.

```
Main Agent (PID 1234)
  history = [user1, asst1, user2, ...]
  │
  └─ bash: python 02-bash-agent/agent.py "find auth files"
       │
       Subagent (PID 5678)
         history = []  ← FRESH! No parent context
         │
         ├─ bash: find . -name "*auth*"
         ├─ bash: cat src/auth.py
         └─ Returns: "Auth module is in src/auth.py, uses JWT..."
              │
              └─ stdout captured by parent as tool result
```

**Why this is brilliant:**
- No framework needed — just `python script.py "task"`
- OS handles isolation — separate process, separate memory
- Unlimited nesting — subagent can spawn sub-subagents
- Clean context — parent only sees the summary

## What v0 Sacrifices (for Simplicity)

| Feature | This Level | Later Levels |
|---------|-----------|--------------|
| Multiple tools | ❌ bash only | [Tool Design](../03-tool-design/): 4 tools |
| Explicit plans | ❌ in model's head | [Structured Planning](../04-structured-planning/): TodoManager |
| Agent types | ❌ one type | [Subagents & Skills](../05-subagents-and-skills/): explore/code/plan |
| Safety checks | ❌ minimal | [Tool Design](../03-tool-design/): path validation |

## What This Proves

1. **Structure matters** — same concept, dramatically more maintainable
2. **Error handling is non-negotiable** — agents run untrusted commands
3. **Dual mode is free** — `sys.argv` check enables subagents with zero framework
4. **Truncation prevents disasters** — large outputs can break the model

---

**Same core loop. Better engineering.**

[← The Agent Loop Guide](../01-agent-loop/GUIDE.md) | [Back to README](./README.md) | [Next: Tool Design →](../03-tool-design/GUIDE.md)
