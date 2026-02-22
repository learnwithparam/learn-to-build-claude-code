# 05 Exercises — Subagents & Skills

## Exercise 1: Add a "test" Agent Type

**Goal**: Create a specialized subagent for running tests.

1. Add a new agent type to `AGENT_TYPES` in `subagent.py`:
   ```python
   "test": {
       "description": "Test runner agent for executing and analyzing tests",
       "tools": ["bash", "read_file"],  # Can run tests, can't modify code
       "prompt": "Run tests and analyze failures. Report: which passed, which failed, and why."
   }
   ```
2. Update the `Task` tool's enum to include "test"
3. Test it: ask the agent to "run all Python tests and report which pass"
4. Observe how the test agent's read-only access prevents it from accidentally fixing tests

**Checkpoint**: The agent should spawn a test-specific subagent that runs tests and reports results without modifying any files.

---

## Exercise 2: Create a Custom Skill

**Goal**: Write your own SKILL.md and see it loaded by the agent.

1. Create `skills/git-workflow/SKILL.md`:
   ```markdown
   ---
   name: git-workflow
   description: Git best practices. Use when committing, branching, or reviewing git history.
   ---

   # Git Workflow Skill

   ## Commit Messages
   Use conventional commits: feat:, fix:, docs:, refactor:, test:

   ## Branch Naming
   - feature/description
   - fix/issue-number
   - docs/topic

   ## Before Committing
   1. Run tests
   2. Check git diff
   3. Stage only related changes
   4. Write descriptive commit message
   ```
2. Run the agent: `make expert`
3. Ask: "help me commit my recent changes"
4. The agent should load the `git-workflow` skill and follow its guidelines

**Checkpoint**: Your custom skill should appear in the agent's startup message and be loaded when relevant.

---

## Exercise 3: Implement Parallel Subagents

**Goal**: Run multiple subagents concurrently.

1. In `subagent.py`, modify `run_task()` to support async execution
2. When the model makes multiple `Task` calls in a single response, run them in parallel using `concurrent.futures.ThreadPoolExecutor`:
   ```python
   from concurrent.futures import ThreadPoolExecutor, as_completed
   
   with ThreadPoolExecutor(max_workers=3) as pool:
       futures = {pool.submit(run_task, ...): tc for tc in task_calls}
       for future in as_completed(futures):
           result = future.result()
   ```
3. Test: ask for "explore the codebase structure AND analyze the README AND check for security issues"
4. Measure time: parallel should be ~3x faster than sequential

**Checkpoint**: Multiple subagents should run simultaneously, each reporting their progress independently.

---

## Exercise 4: Build a Full Workflow

**Goal**: Combine everything into a real-world task.

1. Ask the expert agent to perform this complete workflow:
   ```
   "Create a Python CLI calculator project with:
   - A main.py with add/subtract/multiply/divide functions
   - Unit tests in test_calc.py
   - A README.md with usage instructions
   - Run the tests and fix any failures"
   ```
2. Observe:
   - Does it use TodoWrite to plan?
   - Does it spawn subagents for exploration vs coding?
   - Does it load any skills?
   - Does it track progress through the todo list?
3. Compare the output to what you'd get from the Noob or Intermediate agents

**Checkpoint**: The expert agent should use todos, subagents, and possibly skills to complete a multi-step project creation task in an organized way — demonstrating the full power of the progressive system you've built.
