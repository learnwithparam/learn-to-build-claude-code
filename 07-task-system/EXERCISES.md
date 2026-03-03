# 07 Exercises — Task System

## Exercise 1: Create a Task Graph

**Goal**: Build a dependency chain and watch auto-unblocking.

1. Run the agent: `make 07-task-system`
2. Ask it to create a 3-task plan with dependencies:
   ```
   >> create three tasks: "Setup project", "Implement feature", "Write tests".
   >> The feature should be blocked by setup, and tests blocked by feature.
   ```
3. Run `ls .tasks/` to see the JSON files
4. Read one: `cat .tasks/task_1.json`
5. Ask the agent to complete task 1 and observe task 2 becoming unblocked

**Checkpoint**: Completing a task automatically removes it from dependents' `blockedBy` lists.

---

## Exercise 2: Survive Context Compression

**Goal**: Prove that tasks persist across compression.

1. Create several tasks with the agent
2. Manually delete all messages except the system message (simulate compression by editing the agent to reset `messages` mid-session)
3. Ask the agent to `list all tasks` — they should still be there
4. The agent can continue working despite losing conversation history

**Checkpoint**: Tasks stored in `.tasks/` survive any conversation reset because they live on disk.

---

## Exercise 3: Add Priority Field

**Goal**: Extend the TaskManager with a new feature.

1. Add a `priority` field (1-5) to the task schema in `create()`
2. Update `task_create` tool parameters to accept `priority`
3. Modify `list_all()` to sort by priority (highest first)
4. Add a priority indicator: `[!]` for high (4-5), `[ ]` for normal
5. Test: create tasks with different priorities and verify sorting

**Checkpoint**: The task list shows high-priority tasks first with a visual indicator.

---

## Exercise 4: Add Task Search

**Goal**: Add a search tool for large task boards.

1. Add a `task_search` tool that searches task subjects and descriptions
2. Implement fuzzy matching (case-insensitive substring)
3. Return matching tasks with their full details
4. Test with 10+ tasks and various search queries

**Checkpoint**: The agent can quickly find relevant tasks without listing all of them.
