.PHONY: help install run 01-agent-loop 02-bash-agent 03-tool-design 04-structured-planning 05-subagents-and-skills test clean

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
