# 12 Exercises — Worktree Isolation

## Exercise 1: Create and Use a Worktree

**Goal**: See directory-level isolation in action.

1. Run the agent in a git repository: `make 12-worktree-isolation`
2. Create a task and worktree:
   ```
   >> create a task "Add hello feature" and create a worktree for it
   ```
3. Run a command in the worktree: ask the agent to create a file inside it
4. Verify the file exists in the worktree but NOT in the main repo
5. Check worktree status with `worktree_status`

**Checkpoint**: Changes in the worktree are isolated from the main working directory.

---

## Exercise 2: Parallel Task Execution

**Goal**: Run two tasks in separate worktrees simultaneously.

1. Create two tasks: "Add feature A" and "Add feature B"
2. Create a worktree for each task
3. Run commands in both worktrees (create different files in each)
4. Verify that each worktree has only its own changes
5. List all worktrees and their bound tasks

**Checkpoint**: Two tasks execute in parallel without interfering with each other.

---

## Exercise 3: Complete the Full Lifecycle

**Goal**: Exercise create → work → remove with task completion.

1. Create a task and bind it to a worktree
2. Do some work inside the worktree (create/edit files)
3. Remove the worktree with `complete_task=True`
4. Verify the task status changed to "completed"
5. Check `worktree_events` to see the full lifecycle timeline

**Checkpoint**: The event log shows create → work → remove → task.completed.

---

## Exercise 4: Add Worktree Merge Support

**Goal**: Extend the workflow with branch merging.

1. Add a `worktree_merge` tool that:
   - Runs `git merge` from the worktree branch into main
   - Handles merge conflicts by reporting them
   - Optionally removes the worktree after successful merge
2. Add a `worktree.merge.before` and `worktree.merge.after` event
3. Test the full flow: create → work → commit → merge → remove
4. Handle the case where merge conflicts occur

**Checkpoint**: You can complete the full git workflow: branch → work → merge → cleanup.
