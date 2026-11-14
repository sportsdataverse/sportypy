# Developer shortcuts for sportypy. Run `make help` to list targets.
# Mirrors the gates in CLAUDE.md and CI (.github/workflows/).

.PHONY: help install lint test check

help:  ## Show available targets
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

install:  ## Create .venv from uv.lock (default dev group)
	uv sync --locked

lint:  ## Run ruff and pre-commit hooks
	uv run --no-sync ruff check .
	uv run --no-sync pre-commit run --all-files

test:  ## Run the test suite
	uv run --no-sync pytest --cov=sportypy tests/ --cov-report=term

check:  ## Run lint, then tests (always in that order, even with make -j)
	$(MAKE) lint
	$(MAKE) test
