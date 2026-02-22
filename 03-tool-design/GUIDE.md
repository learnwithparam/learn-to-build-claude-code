# 03 Guide: The Model as Agent

## The Secret of Claude Code

**There is no secret.**

Strip away the CLI polish, the progress bars, the permission systems. What remains is surprisingly simple: a loop that lets the model call tools until the task is done.

### Traditional Assistant vs Agent

```
Traditional:  User → Model → Text Response
Agent:        User → Model → [Tool → Result]* → Response
                                ^____________|
```

The asterisk matters. The model calls tools **repeatedly** until it decides the task is complete.

## The Four Essential Tools

Claude Code has ~20 tools. But 4 cover 90% of use cases:

| Tool | Purpose | Example |
|------|---------|---------|
| `bash` | Run commands | `npm install`, `git status` |
| `read_file` | Read contents | View `src/index.ts` |
| `write_file` | Create/overwrite | Create `README.md` |
| `edit_file` | Precise changes | Replace a function |

### Why These Four?

- **bash** → gateway to everything (search, execute, install)
- **read_file** → structured reading with line limits (avoids context overflow)
- **write_file** → creates parent directories automatically
- **edit_file** → exact string matching for surgical precision

## The Agent Loop

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS
        )

        if response.stop_reason != "tool_use":
            return messages  # Done!

        results = []
        for tc in response.tool_calls:
            output = execute_tool(tc.name, tc.input)
            results.append({"type": "tool_result", ...})

        messages.append({"role": "assistant", ...})
        messages.append({"role": "user", "content": results})
```

**Why this works:**
1. Model controls the loop (keeps calling tools until done)
2. Results become context (fed back as "user" messages)
3. Memory is automatic (messages list accumulates history)

## Path Safety: `safe_path()`

```python
def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path
```

This prevents the model from accidentally (or intentionally) reading/writing files outside the project directory. Every file tool goes through this check.

## System Prompt

The only "configuration" needed:

```python
SYSTEM = f"""You are a coding agent at {WORKDIR}.

Rules:
- Prefer tools over prose. Act, don't just explain.
- Never invent file paths. Use ls/find first.
- Make minimal changes. Don't over-engineer.
- After finishing, summarize what changed."""
```

No complex logic. No state machines. Just clear instructions.

## Why This Design Works

1. **Simplicity** — no frameworks, no state machines
2. **Model does the thinking** — decides which tools, in what order, when to stop
3. **Transparency** — every tool call visible
4. **Extensibility** — add a tool = one function + one JSON schema

## The Bigger Picture

Claude Code, Cursor Agent, Codex CLI, Devin — all share this pattern:

```python
while not done:
    response = model(conversation, tools)
    results = execute(response.tool_calls)
    conversation.append(results)
```

Differences are in tools, display, safety. But the essence is always: **give the model tools and let it work**.

---

**Model as Agent. That's the whole secret.**

[← Bash Agent Guide](../02-bash-agent/GUIDE.md) | [Back to README](./README.md) | [Next: Structured Planning →](../04-structured-planning/GUIDE.md)
