# 04 Exercises — Structured Planning

## Exercise 1: Add a Priority Field

**Goal**: Extend the TodoManager with task priorities.

1. Add a `priority` field to the TodoWrite schema: `"high" | "medium" | "low"`
2. Update `TodoManager.update()` to validate it
3. Update `TodoManager.render()` to show priorities:
   ```
   [>] 🔴 Fix critical auth bug     <- Fixing auth...
   [ ] 🟡 Add tests
   [ ] 🟢 Update docs
   ```
4. Update the system prompt to tell the model about priorities
5. Test: ask the agent to do multiple tasks and observe priority ordering

**Checkpoint**: The agent should assign and display priorities, and tend to work on high-priority tasks first.

---

## Exercise 2: Implement Undo

**Goal**: Add the ability to undo the last todo update.

1. Store the previous state in `TodoManager`:
   ```python
   def update(self, items):
       self.previous = self.items.copy()
       # ... validation ...
   
   def undo(self):
       if self.previous:
           self.items = self.previous
           self.previous = None
           return self.render()
       return "Nothing to undo"
   ```
2. Add a `TodoUndo` tool (or add an `undo` parameter to `TodoWrite`)
3. Test: update todos, then call undo

**Checkpoint**: The agent should be able to recover from a bad todo update.

---

## Exercise 3: Add Time Tracking

**Goal**: Track how long the agent spends on each task.

1. Add a `started_at` timestamp when status changes to `in_progress`
2. Add `elapsed` time in the rendered output:
   ```
   [x] Fix auth (2.3s)
   [>] Add tests (1.5s elapsed) <- Writing test cases...
   [ ] Update docs
   ```
3. Show total elapsed time at the bottom
4. Store timing data even after completion

**Checkpoint**: You should see realistic timing data showing how long the model spent on each task — useful for understanding agent behavior and optimizing prompts.
