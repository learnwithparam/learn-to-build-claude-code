# 11 Exercises — Autonomous Agents

## Exercise 1: Watch Auto-Claiming

**Goal**: See a teammate find and claim work autonomously.

1. Run the agent: `make 11-autonomous-agents`
2. First, create some tasks on the board:
   ```
   >> create three tasks: "Write README", "Add tests", "Setup CI"
   ```
3. Then spawn a teammate: `>> spawn alice as a coder to work on available tasks`
4. Watch alice auto-claim a task from the board
5. Use `/tasks` to see which tasks are claimed and by whom

**Checkpoint**: Alice finds and claims pending tasks without being explicitly told.

---

## Exercise 2: Observe the IDLE Phase

**Goal**: See the idle polling cycle.

1. Spawn a teammate with a simple task that finishes quickly
2. Watch the teammate enter the IDLE phase (status changes to "idle" in `/team`)
3. Create a new task while the teammate is idle
4. Watch the teammate auto-claim the new task and resume WORK

**Checkpoint**: The WORK → IDLE → WORK cycle happens automatically.

---

## Exercise 3: Test Identity Re-Injection

**Goal**: Verify identity survives context compression.

1. Spawn a teammate and let it work on several tasks
2. After the teammate has accumulated many messages, manually compress its context (modify the code to reset `messages` to a short summary)
3. Verify that the identity block is re-injected
4. The teammate should continue working with its correct name and role

**Checkpoint**: Even after losing conversation history, the teammate remembers who it is.

---

## Exercise 4: Add Task Priority to Auto-Claim

**Goal**: Make auto-claiming smarter.

1. Add a `priority` field to tasks (1-5)
2. Modify `scan_unclaimed_tasks()` to return highest-priority tasks first
3. Test with mixed-priority tasks and verify teammates claim the important ones first
4. Add a log line: `"[alice] auto-claimed task #3 (priority: 5)"`

**Checkpoint**: Teammates prioritize important work when multiple tasks are available.
