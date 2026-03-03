# 06 Exercises — Context Compaction

## Exercise 1: Observe Micro Compaction

**Goal**: See Layer 1 compression in action.

1. Run the agent: `make 06-context-compaction`
2. Give it a task that requires many tool calls:
   ```
   >> list all Python files in this project, read the first 10 lines of each
   ```
3. After 5+ tool calls, look at the conversation. Notice how old tool results show `[Previous: used read_file]` instead of full content.
4. The agent still works correctly despite the shortened history.

**Checkpoint**: You understand that micro compaction silently trims old results without affecting current behavior.

---

## Exercise 2: Trigger Auto Compaction

**Goal**: Force Layer 2 compression to fire.

1. Lower the `THRESHOLD` constant from `50000` to `5000` in `agent.py`
2. Run the agent and give it a multi-step task:
   ```
   >> explore this entire project structure, read every README, and summarize what you find
   ```
3. Watch for the `[auto_compact triggered]` message
4. Check the `.transcripts/` directory — you should see a saved transcript file
5. After compression, the agent continues with a summarized context

**Checkpoint**: The agent seamlessly continues after compression. The transcript file preserves the full original conversation.

---

## Exercise 3: Use the Manual Compact Tool

**Goal**: Understand when manual compression is useful.

1. Run the agent and do some exploration work
2. Then type: `compress the conversation and focus on what we learned about the project structure`
3. The model should call the `compact` tool
4. Observe how the summary preserves the information you asked for

**Checkpoint**: The model can strategically decide when to compress and what to preserve.

---

## Exercise 4: Customize the Compression Strategy

**Goal**: Modify the compression pipeline.

1. Change `KEEP_RECENT` from 3 to 1 — more aggressive micro compaction
2. Add a token counter display: after each turn, print `[tokens: ~{estimate_tokens(messages)}]`
3. Modify `auto_compact` to include task-specific context in the summary prompt
4. Test with a long session and compare behavior before and after changes

**Checkpoint**: You can tune the compression pipeline for different use cases — aggressive for long tasks, conservative for precision work.
