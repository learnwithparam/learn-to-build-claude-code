# 03 Exercises — Tool Design

## Exercise 1: Add a `grep_file` Tool

**Goal**: Design and implement a new tool.

1. Add a 5th tool called `grep_file` with this schema:
   ```python
   {
       "name": "grep_file",
       "description": "Search for a pattern in a file. Returns matching lines.",
       "input_schema": {
           "type": "object",
           "properties": {
               "path": {"type": "string", "description": "File to search"},
               "pattern": {"type": "string", "description": "Text pattern to find"}
           },
           "required": ["path", "pattern"]
       }
   }
   ```
2. Implement `run_grep(path, pattern)` using Python's string matching
3. Add it to `execute_tool()`
4. Test: ask the agent to "find all functions in agent.py"

**Checkpoint**: The agent should automatically choose `grep_file` when searching file content instead of using `bash grep`.

---

## Exercise 2: Change Agent Personality

**Goal**: Understand how the system prompt controls behavior.

1. Change the system prompt to one of these:
   - **Cautious agent**: "Always explain what you're about to do before doing it. Ask for confirmation before writing files."
   - **Verbose agent**: "Show your reasoning step by step. Explain each tool choice."
   - **Minimal agent**: "Use the fewest possible tool calls. Combine operations when possible."
2. Run the same task with each personality: `"Add a LICENSE file for MIT license"`
3. Compare: how many tool calls? What order? What explanation style?

**Checkpoint**: Same code, same tools, dramatically different behavior — just from the prompt.

---

## Exercise 3: Handle Large Files

**Goal**: Improve the `read_file` tool for real-world use.

1. Current `read_file` has a `limit` parameter but the model doesn't always use it
2. Modify the tool to:
   - Count lines before reading
   - If > 200 lines, automatically return first 50 + last 20 + a summary
   - Print a warning: `"Large file (N lines). Showing head + tail."`
3. Test with a large file: create one with `python -c "for i in range(1000): print(f'line {i}')" > big.txt`

**Checkpoint**: The agent gracefully handles large files without overwhelming its context window.

---

## Exercise 4: Add Colored Output

**Goal**: Make the agent output more readable.

1. Add ANSI color formatting:
   - 🟡 Yellow for bash commands: `\033[33m`
   - 🟢 Green for success: `\033[32m`
   - 🔴 Red for errors: `\033[31m`
   - 🔵 Cyan for tool names: `\033[36m`
   - Reset: `\033[0m`
2. Color-code each tool call's output
3. Add a "thinking..." indicator when waiting for the model

**Checkpoint**: The agent output should be easy to scan visually, with clear distinction between commands, results, and errors.
