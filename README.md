# Build Your Own Claude Code Workshop

Learn how modern AI coding agents work by building one from scratch — from a 17-line agent to a full production-grade system.

## 🎯 Workshop Modules

| # | Module | Core Addition | Key Insight |
|---|--------|---------------|-------------|
| 01 | [The Agent Loop](./01-agent-loop/) | 1 bash tool, 17 lines | The loop is everything |
| 02 | [Bash Agent](./02-bash-agent/) | Structured code + subagent mode | Structure and recursion |
| 03 | [Tool Design](./03-tool-design/) | 4 tools (bash, read, write, edit) | The model IS the agent |
| 04 | [Structured Planning](./04-structured-planning/) | + TodoManager planning | Constraints enable |
| 05 | [Subagents & Skills](./05-subagents-and-skills/) | + Subagents + Skills | Divide, conquer, and know |

### What You'll Learn

- **The Agent Loop** — The simple pattern behind all AI coding agents
- **Tool Design** — How to give AI models real-world capabilities
- **Explicit Planning** — Using constraints to make AI behavior predictable
- **Context Management** — Keeping agent memory clean through subagent isolation
- **Knowledge Injection** — Loading domain expertise on-demand without retraining

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- An Anthropic API Key ([get one here](https://console.anthropic.com/)) or Claude Code Pro plan

### Setup

1.  **Install dependencies**:
    ```bash
    make install
    ```

2.  **Configure environment**:
    ```bash
    cp .env.example .env
    # Edit .env and add your ANTHROPIC_API_KEY
    ```

3.  **Run the first agent**:
    ```bash
    make 01-agent-loop
    ```

### Running Each Module

```bash
make 01-agent-loop          # Start here! 17-line agent
make 02-bash-agent          # Expanded bash agent with subagent mode
make 03-tool-design         # 4-tool agent (bash, read, write, edit)
make 04-structured-planning # + Todo planning system
make 05-subagents-and-skills # + Subagents + Skills (full agent)
```

## Learning Path

```
Start Here
    |
    v
01 [The Agent Loop] ────────> "The loop is everything"
    |                          17 lines, 1 tool
    v
02 [Bash Agent] ────────────> "Structure and recursion"
    |                          ~130 lines, 1 tool
    v
03 [Tool Design] ───────────> "The model IS the agent"
    |                          4 tools, ~270 lines
    v
04 [Structured Planning] ──> "Make plans explicit"
    |                          +TodoManager, ~310 lines
    v
05 [Subagents & Skills] ───> "Divide, conquer, and know"
                               +Subagents +Skills, ~780 lines
```

**Recommended approach:**
1. Read and run 01 first — understand the core loop
2. Compare 01 → 02 — see how structure evolves
3. Study 03 for tool design patterns
4. Explore 04 for planning strategies
5. Master 05 for production-grade agent architecture

## Each Module Includes

| File | Purpose |
|------|---------|
| `agent.py` | The runnable agent code |
| `README.md` | Module intro, learning goals, how to run |
| `GUIDE.md` | Deep-dive explanation of concepts |
| `EXERCISES.md` | 3-4 hands-on exercises |

## The Core Pattern

Every coding agent is just this loop:

```python
while True:
    response = model(messages, tools)
    if response.stop_reason != "tool_use":
        return response.text
    results = execute(response.tool_calls)
    messages.append(results)
```

That's it. The model calls tools until done. Everything else is refinement.

## Verifying Your Setup

```bash
make test    # Runs automated checks on all modules
```
