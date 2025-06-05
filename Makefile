.PHONY: help install dev run clean test lint format check sync update build serve
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Fever Tracker - UV Environment Management$(RESET)"
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies using uv
	@echo "$(BLUE)Installing dependencies with uv...$(RESET)"
	uv sync

dev: install ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	uv sync --dev

run: install ## Run the Streamlit application
	@echo "$(BLUE)Starting Fever Tracker application...$(RESET)"
	uv run streamlit run main.py --server.port 8501

serve: run ## Alias for run command

build: ## Build the project
	@echo "$(BLUE)Building the project...$(RESET)"
	uv build

clean: ## Clean up temporary files and caches
	@echo "$(BLUE)Cleaning up...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/

sync: ## Sync dependencies (update uv.lock)
	@echo "$(BLUE)Syncing dependencies...$(RESET)"
	uv sync

update: ## Update all dependencies to latest versions
	@echo "$(BLUE)Updating dependencies...$(RESET)"
	uv sync --upgrade

lock: ## Generate/update the lock file
	@echo "$(BLUE)Updating lock file...$(RESET)"
	uv lock

check-uv: ## Check if uv is installed
	@which uv > /dev/null || (echo "$(RED)uv is not installed. Please install it first: https://docs.astral.sh/uv/getting-started/installation/$(RESET)" && exit 1)
	@echo "$(GREEN)uv is installed$(RESET)"

init: check-uv install ## Initialize the project (check uv and install dependencies)
	@echo "$(GREEN)Project initialized successfully!$(RESET)"
	@echo "$(YELLOW)Run 'make run' to start the application$(RESET)"

shell: ## Open a shell in the uv environment
	@echo "$(BLUE)Opening shell in uv environment...$(RESET)"
	uv run bash

python: ## Open Python REPL in the uv environment
	@echo "$(BLUE)Opening Python REPL in uv environment...$(RESET)"
	uv run python

info: ## Show project and environment information
	@echo "$(BLUE)Project Information:$(RESET)"
	@echo "Name: fever-tracker"
	@echo "Python version: $(shell uv run python --version)"
	@echo "UV version: $(shell uv --version)"
	@echo ""
	@echo "$(BLUE)Dependencies:$(RESET)"
	@uv tree 2>/dev/null || echo "Run 'make install' first to see dependency tree"

status: ## Show current environment status
	@echo "$(BLUE)Environment Status:$(RESET)"
	@if [ -f "uv.lock" ]; then \
		echo "$(GREEN)✓ Lock file exists$(RESET)"; \
	else \
		echo "$(RED)✗ Lock file missing$(RESET)"; \
	fi
	@if [ -d ".venv" ]; then \
		echo "$(GREEN)✓ Virtual environment exists$(RESET)"; \
	else \
		echo "$(YELLOW)! Virtual environment not found$(RESET)"; \
	fi

reset: clean ## Reset the environment (clean + fresh install)
	@echo "$(BLUE)Resetting environment...$(RESET)"
	rm -rf .venv
	rm -f uv.lock
	$(MAKE) install
	@echo "$(GREEN)Environment reset complete!$(RESET)"

test: install ## Run application tests
	@echo "$(BLUE)Running application tests...$(RESET)"
	uv run python test_app.py

# Development shortcuts
start: run ## Alias for run
dev-run: dev run ## Install dev dependencies and run
quick-start: install run ## Quick start (install + run)
