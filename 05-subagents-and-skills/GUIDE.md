# 05 Guide: Subagents & Skills

This level combines two powerful concepts that take the agent from capable to production-grade.

---

## Part 1: Subagent Mechanism

### The Problem: Context Pollution

A single agent exploring a codebase fills its context with file contents:

```
Main Agent History:
  [exploring...] cat file1.py → 500 lines
  [exploring...] cat file2.py → 300 lines
  ... 15 more files ...
  [now refactoring...] "wait, what did file1 contain?"
```

### The Solution: Isolated Context

```
Main Agent History:
  [Task: explore codebase]
    → Subagent explores 20 files (in its own context)
    → Returns ONLY: "Auth in src/auth/, DB in src/models/"
  [now refactoring with clean context]
```

### Agent Type Registry

```python
AGENT_TYPES = {
    "explore": {
        "tools": ["bash", "read_file"],  # No write access
        "prompt": "Search and analyze. Never modify. Return summary."
    },
    "code": {
        "tools": "*",  # All tools
        "prompt": "Implement changes efficiently."
    },
    "plan": {
        "tools": ["bash", "read_file"],  # Read-only
        "prompt": "Analyze and output numbered plan. Don't change files."
    }
}
```

### How Subagents Work

```python
def run_task(description, prompt, agent_type):
    # 1. Agent-specific system prompt
    # 2. Filtered tools (explore can't write)
    # 3. Isolated history (KEY: no parent context!)
    sub_messages = [{"role": "user", "content": prompt}]
    
    # 4. Same agent loop
    while True:
        response = client.messages.create(...)
        if response.stop_reason != "tool_use":
            break
        # Execute tools...
    
    # 5. Return ONLY final text
    return extract_final_text(response)
```

### Typical Flow

```
User: "Refactor auth to use JWT"

Main Agent:
  1. Task(explore): "Find all auth-related files"
     → Returns: "Auth in src/auth/login.py..."

  2. Task(plan): "Design JWT migration"
     → Returns: "1. Add jwt lib 2. Create utils..."

  3. Task(code): "Implement JWT tokens"
     → Returns: "Created jwt_utils.py, updated login.py"

  4. Summarize changes
```

---

## Part 2: Skills Mechanism

### The Paradigm Shift: Knowledge Externalization

**Traditional AI**: Knowledge locked in model parameters
- To teach new skills: collect data → train → deploy
- Cost: $10K-$1M+, Timeline: Weeks

**Skills**: Knowledge stored in editable files
- To teach new skills: write a SKILL.md file
- Cost: Free, Timeline: Minutes

### Tools vs Skills

| Concept | What it is | Example |
|---------|------------|---------|
| **Tool** | What model CAN do | bash, read_file, write |
| **Skill** | How model KNOWS to do | PDF processing, MCP dev |

Tools are capabilities. Skills are knowledge.

### Progressive Disclosure

```
Layer 1: Metadata (always loaded)     ~100 tokens/skill
         └─ name + description

Layer 2: SKILL.md body (on trigger)   ~2000 tokens
         └─ Detailed instructions

Layer 3: Resources (as needed)        Unlimited
         └─ scripts/, references/, assets/
```

### Cache-Preserving Injection

**Critical insight**: Skill content goes into `tool_result` (user message), NOT system prompt.

```python
# Wrong: edit system prompt each time → cache invalidated (20-50x cost)
system = f"Skills: {loaded_skill_content}"

# Right: append skill as tool result → prefix unchanged, cache hit
def run_skill(skill_name):
    content = SKILLS.get_skill_content(skill_name)
    return f'<skill-loaded name="{skill_name}">{content}</skill-loaded>'
```

This preserves prompt cache because the system prompt never changes.

### The SKILL.md Standard

```
skills/
├── pdf/
│   └── SKILL.md          # Required: YAML frontmatter + Markdown body
├── mcp-builder/
│   ├── SKILL.md
│   └── references/       # Optional: docs, specs
└── code-review/
    ├── SKILL.md
    └── scripts/          # Optional: helper scripts
```

### Caching Economics

| Anti-Pattern | Cost Multiplier |
|-------------|----------------|
| Dynamic system prompt | **20-50x** |
| Message compression | **5-15x** |
| Sliding window | **30-50x** |
| Message editing | **10-30x** |

> **Treat context as append-only log, not editable document.**

---

## Series Summary

| Level | Theme | Key Insight |
|-------|-------|-------------|
| 🟢 Noob | Hello World | The loop is everything |
| 🔵 Beginner | Bash Agent | One tool + structure = real agent |
| 🟡 Intermediate | Model as Agent | 4 tools cover 90% of use cases |
| 🟠 Advanced | Structured Planning | Constraints enable, not limit |
| 🔴 Expert | Subagents + Skills | Divide, conquer, and know |

---

**Tools let models act. Skills let models know how.**

[← Structured Planning Guide](../04-structured-planning/GUIDE.md) | [Back to README](./README.md)
