# sportypy Copilot instructions

## Project context

`sportypy` draws regulation sports surfaces with matplotlib and is the Python
counterpart of `sportyR`, with which it keeps parity. Source is `sportypy/`;
follow `CLAUDE.md`, `CONTRIBUTING.md` and `tests/` when they differ from this
file.

## Workflow

- Use feature branches and pull requests; do not push to `main`.
- Set up with `uv sync --locked`. The local gates:
  `uv run --no-sync ruff check .`, `uv run --no-sync pre-commit run --all-files`,
  `uv run --no-sync pytest tests/` and the docs site build (`yarn build` in
  `docs/`, which fails on a broken link). CI also runs
  zizmor on `upload-to-pypi.yml` and checks the built distributions
  (`uv build`, `twine check --strict`, the wheel ships the data JSON).
- Never let a `uv.lock` change ride into an unrelated commit.

## Commits

Conventional Commits. No AI co-author trailers or "Generated with" footers.
Stage explicit paths. Do not edit `CHANGELOG.md`: the release workflow
writes it from the commit messages.

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

Never hand-edit the sportyR fixtures under `tests/data/` or `uv.lock`. The
docs site's API reference, usage guide, News page and cookbook pages are written
by `tools/gen_docs.py` on every build and are not committed: change the
docstring, the README, `CHANGELOG.md` or the notebook instead.
