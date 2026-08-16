# Build Your Own Claude Code Workshop

Learn how modern AI coding agents work by building one from scratch: from a 17-line agent to a full production-grade system with teams and worktree isolation.

**This is teaching material, not a product.** The bar is that a learner can clone it and run it.
Optimise for a working first command and a clear error when something is missing, not for architecture.

## Running it

```bash
make help
make install
make run
make test
```

All targets: `help`, `install`, `run`, `test`, `clean`.

Python project (`pyproject.toml`). Use the repo's own virtualenv; never install into the system
interpreter.

## Rules

- **Never break the first-run path.** A learner hitting an error in step one abandons the workshop.
  If you change setup, run it from a clean clone before calling it done.
- **Explanations belong in the README and in notebook prose**, not in long code comments. The code is
  the lesson; it should read as the clearest version of the idea.
- **No em dashes** in prose, per the house rules in
  `/Users/param/.claude/skills/lwp-shared/house-rules.md`.
- **Pin what you can.** A workshop that worked last term and breaks this term because an upstream
  package moved is the most common failure here.
