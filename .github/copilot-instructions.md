# sportypy Copilot instructions

## Project context

`sportypy` draws regulation sports surfaces with matplotlib and is the Python
counterpart of `sportyR`, with which it keeps parity. Source is `sportypy/`;
follow `CLAUDE.md`, `CONTRIBUTING.md` and `tests/` when they differ from this
file.

## Workflow

- Use feature branches and pull requests; do not push to `main`.
- Set up with `uv sync --locked`. The gates, as CI runs them:
  `uv run --no-sync ruff check .`, `uv run --no-sync pre-commit run --all-files`,
  `uv run --no-sync pytest tests/` and a Sphinx build with `-W`.
- Never let a `uv.lock` change ride into an unrelated commit.

## Commits

Conventional Commits. No AI co-author trailers or "Generated with" footers.
Stage explicit paths. A user-visible change gets a bullet in
`docs/changelog.md` under the next version.

## Code

- Python 3.10+. Follow the surrounding style: keyword arguments are spaced
  (`ax = ax`) and docstrings are NumPy style. `ruff format` is not used.
- A surface is `sportypy/surfaces/<sport>.py` (one class per sport, a subclass
  per league); its features are in `sportypy/_feature_classes/<sport>.py`.
- League dimensions live in `sportypy/data/surface_dimensions.json` and come
  from sportyR through `tools/sync_dimensions.py`; never retype them.
- Lengths are in the surface's units; counts are never unit-converted.

## Tests

- Every change keeps the suite at full coverage of what it touches.
- `tests/data/sportyr_*_fixture.json` are generated from sportyR by
  `tools/<sport>_fixture.R`; regenerate them, never hand-edit them.

## Generated files

Never hand-edit `docs/_build/**` (the committed Sphinx build), the sportyR
fixtures under `tests/data/` or `uv.lock`.
