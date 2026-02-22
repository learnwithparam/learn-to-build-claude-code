# 01 Exercises — The Agent Loop

## Exercise 1: Read the Code

**Goal**: Understand every line of the 17-line agent.

1. Open `agent.py` and identify:
   - Where is the **agent loop**? (the `while` loop)
   - Where is the **tool definition**? (the `T` variable)
   - Where does the model **decide to stop**? (the `stop_reason` check)
2. Write down in your own words: what does each line do?

**Checkpoint**: You should be able to explain the flow: user input → model call → tool execution → loop back.

---

## Exercise 2: Run and Observe

**Goal**: See the agent in action and understand the loop flow.

1. Run the agent: `make noob`
2. Try these prompts and watch the yellow `$` commands:
   ```
   >> list all files in the current directory
   >> what language is this project written in?
   >> create a file called hello.txt with "Hello from the agent!"
   ```
3. For each prompt, count:
   - How many bash commands did the agent run?
   - Did it run them in a logical order?
   - When did it decide to stop?

**Checkpoint**: You should see that the model autonomously decides which commands to run and when to stop.

---

## Exercise 3: Modify the System Prompt

**Goal**: See how the system prompt shapes agent behavior.

1. In `agent.py`, find the system prompt (the `S` variable)
2. Change it to make the agent behave differently. Try:
   - `"You are a pirate CLI agent. Talk like a pirate while solving problems."`
   - `"You are a cautious agent. Always explain what you're about to do before doing it."`
   - `"You are an agent that only uses one-liner bash commands."`
3. Run again and observe how behavior changes

**Checkpoint**: The system prompt is the ONLY thing that changes behavior. Same code, different personality.
