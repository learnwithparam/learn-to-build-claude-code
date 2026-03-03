.PHONY: help install run 01-agent-loop 02-bash-agent 03-tool-design 04-structured-planning 05-subagents-and-skills 06-context-compaction 07-task-system 08-background-tasks 09-agent-teams 10-team-protocols 11-autonomous-agents 12-worktree-isolation test clean

help: ## Show this help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	@echo "📦 Installing dependencies..."
	@uv sync

run: 01-agent-loop ## Run the first module — start here!

# =============================================================================
# Workshop Modules
# =============================================================================

01-agent-loop: ## 01 The Agent Loop — 17-line agent (start here!)
	@echo "▶ Running 01: The Agent Loop..."
	@uv run python 01-agent-loop/agent.py

02-bash-agent: ## 02 Bash Agent — Expanded bash agent with subagent mode
	@echo "▶ Running 02: Bash Agent..."
	@uv run python 02-bash-agent/agent.py

03-tool-design: ## 03 Tool Design — 4-tool agent
	@echo "▶ Running 03: Tool Design..."
	@uv run python 03-tool-design/agent.py

04-structured-planning: ## 04 Structured Planning — Todo planning agent
	@echo "▶ Running 04: Structured Planning..."
	@uv run python 04-structured-planning/agent.py

05-subagents-and-skills: ## 05 Subagents & Skills — Full agent
	@echo "▶ Running 05: Subagents & Skills..."
	@uv run python 05-subagents-and-skills/agent.py

06-context-compaction: ## 06 Context Compaction — 3-layer compression
	@echo "▶ Running 06: Context Compaction..."
	@uv run python 06-context-compaction/agent.py

07-task-system: ## 07 Task System — File-based DAG tasks
	@echo "▶ Running 07: Task System..."
	@uv run python 07-task-system/agent.py

08-background-tasks: ## 08 Background Tasks — Daemon threads
	@echo "▶ Running 08: Background Tasks..."
	@uv run python 08-background-tasks/agent.py

09-agent-teams: ## 09 Agent Teams — TeammateManager + MessageBus
	@echo "▶ Running 09: Agent Teams..."
	@uv run python 09-agent-teams/agent.py

10-team-protocols: ## 10 Team Protocols — Shutdown + plan approval
	@echo "▶ Running 10: Team Protocols..."
	@uv run python 10-team-protocols/agent.py

11-autonomous-agents: ## 11 Autonomous Agents — WORK/IDLE lifecycle
	@echo "▶ Running 11: Autonomous Agents..."
	@uv run python 11-autonomous-agents/agent.py

12-worktree-isolation: ## 12 Worktree Isolation — Git worktrees per task
	@echo "▶ Running 12: Worktree Isolation..."
	@uv run python 12-worktree-isolation/agent.py

# =============================================================================
# Utilities
# =============================================================================

test: ## Run automated tests to verify all modules
	@echo "🧪 Running workshop tests..."
	@uv run python tests.py

clean: ## Clean up artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf .venv
	@find . -type d -name "__pycache__" -exec rm -rf {} +
