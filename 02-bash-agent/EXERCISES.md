# 02 Exercises — Bash Agent

## Exercise 1: Trace the Loop

**Goal**: Follow the execution flow step by step.

1. Run the agent: `make beginner`
2. Ask: `"Create a file called test.py with a hello world program, then run it"`
3. On paper, trace:
   - How many times did the loop execute?
   - What was in `history` after each iteration?
   - When did `stop_reason` change from `"tool_use"` to something else?

**Checkpoint**: You should understand that each loop iteration is: model call → tool execution → append results.

---

## Exercise 2: Add a Safety Check

**Goal**: Prevent dangerous commands.

1. Add a safety check before `subprocess.run()`:
   ```python
   dangerous = ["rm -rf", "sudo", "shutdown", "> /dev/"]
   if any(d in cmd for d in dangerous):
       output = "Error: Dangerous command blocked"
   ```
2. Test it: `"delete all files in the root directory"`
3. Verify the agent is blocked

**Checkpoint**: The agent should refuse dangerous commands but still work for safe ones.

---

## Exercise 3: Spawn a Subagent

**Goal**: See context isolation in action.

1. Run the agent: `make beginner`
2. Have a conversation about the project files (ask 3-4 questions)
3. Now ask: `"Spawn a subagent to count the total lines of Python code in this project"`
4. Observe:
   - The subagent doesn't know about your previous conversation
   - It starts fresh and returns only a summary
   - The parent agent's history stays clean

**Checkpoint**: You should see the subagent's bash command appear, execute, and return a clean summary while your main conversation continues uninterrupted.
