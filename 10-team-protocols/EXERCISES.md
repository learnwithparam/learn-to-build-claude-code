# 10 Exercises — Team Protocols

## Exercise 1: Test the Shutdown Protocol

**Goal**: See graceful shutdown in action.

1. Run the agent: `make 10-team-protocols`
2. Spawn a teammate: ask the lead to spawn "alice" as a coder
3. While alice is working, request shutdown: ask the lead to shut down alice
4. Use `/team` to watch alice's status change from "working" to "shutdown"
5. Check that the shutdown_request tracker shows the correct status

**Checkpoint**: Alice gracefully shuts down after approving the request, not abruptly killed.

---

## Exercise 2: Test Plan Approval

**Goal**: See the plan approval flow.

1. Spawn a teammate with instructions to submit a plan before coding
2. The teammate should call `plan_approval` with its proposed plan
3. The lead's inbox should receive the plan for review
4. Approve or reject the plan and observe the teammate's response

**Checkpoint**: Teammates can submit plans and wait for approval before proceeding.

---

## Exercise 3: Add a Rejection Counter

**Goal**: Track how often plans get rejected.

1. Add a `rejection_count` field to the plan tracker
2. If a plan is rejected 3 times, auto-approve the next attempt with a warning
3. Modify the teammate's prompt to revise rejected plans
4. Test with a plan that gets rejected, revised, and eventually approved

**Checkpoint**: The system handles repeated rejections gracefully without deadlocking.

---

## Exercise 4: Implement a Voting Protocol

**Goal**: Build a new protocol using the request_id pattern.

1. Create a `vote_request` message type
2. The lead broadcasts a proposal to all teammates
3. Each teammate responds with `vote_response {approve: true/false}`
4. The lead tallies votes and announces the result
5. Use the same tracker pattern as shutdown/plan approval

**Checkpoint**: You can create new coordination protocols by following the request_id correlation pattern.
