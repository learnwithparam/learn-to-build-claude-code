# 08 Exercises — Background Tasks

## Exercise 1: Run Parallel Commands

**Goal**: See background execution in action.

1. Run the agent: `make 08-background-tasks`
2. Ask it to run multiple commands in parallel:
   ```
   >> run these three commands in the background: "sleep 3 && echo done1", "sleep 2 && echo done2", "sleep 1 && echo done3"
   ```
3. Observe that all three start immediately
4. Ask the agent to check on the tasks — the shortest should finish first
5. Notice how results appear in the conversation as background notifications

**Checkpoint**: Commands run concurrently. The agent doesn't wait for each one.

---

## Exercise 2: Observe the Drain Pattern

**Goal**: Understand when background results are injected.

1. Start a long background task: `background_run("sleep 5 && echo LONG_DONE")`
2. Immediately ask the agent a question (it should respond without waiting)
3. After 5 seconds, ask another question — the background result should appear
4. Look for the `<background-results>` tag in the conversation

**Checkpoint**: Background results appear between turns, not interrupting the current response.

---

## Exercise 3: Add a Progress Callback

**Goal**: Extend BackgroundManager with progress tracking.

1. Modify `_execute` to periodically update a progress field:
   - Track elapsed time and estimated completion
   - Update `self.tasks[task_id]["progress"]` every second
2. Add a `check_progress` tool that shows real-time progress
3. Test with a long-running command and poll progress

**Checkpoint**: You can monitor background task progress without waiting for completion.

---

## Exercise 4: Add Task Cancellation

**Goal**: Implement background task cancellation.

1. Store the `subprocess.Popen` object instead of using `subprocess.run`
2. Add a `cancel_background` tool that calls `process.kill()`
3. Update the notification queue to report cancellations
4. Test: start a `sleep 30` background task, then cancel it

**Checkpoint**: Background tasks can be stopped mid-execution without killing the agent.
