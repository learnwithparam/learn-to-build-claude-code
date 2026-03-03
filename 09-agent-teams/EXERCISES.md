# 09 Exercises — Agent Teams

## Exercise 1: Spawn a Two-Person Team

**Goal**: See team communication in action.

1. Run the agent: `make 09-agent-teams`
2. Ask the lead to spawn two teammates:
   ```
   >> spawn alice as a coder to create a hello.py file, and bob as a reviewer to check alice's work
   ```
3. Use `/team` to check teammate status
4. Use `/inbox` to see messages sent to the lead
5. Observe how teammates work independently in their threads

**Checkpoint**: Two teammates work in parallel, communicating through JSONL inboxes.

---

## Exercise 2: Trace the Message Flow

**Goal**: Understand the inbox append/drain pattern.

1. Spawn a teammate and send it a message
2. Before the teammate reads its inbox, check the file: `cat .team/inbox/alice.jsonl`
3. After the teammate processes the message, check again — the file should be empty (drained)
4. Send another message and repeat

**Checkpoint**: Messages accumulate in the JSONL file until drained (read + cleared).

---

## Exercise 3: Add a Broadcast Response

**Goal**: Implement team-wide acknowledgment.

1. After the lead broadcasts a message, each teammate should auto-reply with "Acknowledged"
2. Modify the teammate's system prompt to include: "When you receive a broadcast, acknowledge it"
3. Broadcast a message and verify all teammates respond
4. Check the lead's inbox for acknowledgments

**Checkpoint**: Broadcasts trigger responses from all active teammates.

---

## Exercise 4: Implement Team Status Dashboard

**Goal**: Build a real-time team overview.

1. Add a `/dashboard` REPL command that shows:
   - Each teammate's name, role, and status
   - Number of unread messages in each inbox
   - Time since last activity
2. Read inbox files without draining (peek, don't consume)
3. Format as a clean table

**Checkpoint**: A single command gives you full visibility into team state.
