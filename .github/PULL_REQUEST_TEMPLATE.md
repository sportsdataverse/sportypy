## Summary

<!-- What this PR changes and why, in 1-3 sentences. Link the issue it fixes. -->

## Type of change

- [ ] Bug fix (non-breaking)
- [ ] New sport, league or feature (non-breaking)
- [ ] Breaking change (a surface's output or the API changes)
- [ ] Documentation only
- [ ] Tooling / CI / packaging

## Test plan

<!-- The gates CI runs, after `uv sync --locked`. -->

- [ ] `uv run --no-sync ruff check .` is clean
- [ ] `uv run --no-sync pre-commit run --all-files` is clean
- [ ] `uv run --no-sync pytest tests/` passes, and new code is covered
- [ ] A change to a surface that sportyR also draws is checked against sportyR (a parity test, or the fixture regenerated with `tools/<sport>_fixture.R`)
- [ ] `uv.lock` is unchanged, or changed only with the `pyproject.toml` edit that caused it

## Documentation

- [ ] `CHANGELOG.md` bullet under the next version (a user-visible change)
- [ ] Docstrings, and the `docs/` pages for a new sport or league
- [ ] `CLAUDE.md` / `.github/copilot-instructions.md` (only if a convention changes)

## Checklist

- [ ] I have NOT included AI agents (Claude, Copilot, GPT, etc.) as commit co-authors.
- [ ] I have searched existing PRs to confirm this isn't a duplicate.
