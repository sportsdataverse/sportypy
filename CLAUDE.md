# sportypy — repository rules

`sportypy` draws regulation sports surfaces with matplotlib. It is the Python
counterpart of [`sportyR`](https://github.com/sportsdataverse/sportyR) and keeps
parity with it (geometry, dimensions, colours, display ranges). The shared
SportsDataverse rules (commits, attribution, safety) are in `.claude/CLAUDE.md`;
this file holds the repo-specific ones.

## Layout

- `sportypy/surfaces/<sport>.py`: one surface class per sport (`HockeyRink`,
  `LacrosseField`, ...) plus a subclass per league (`NHLRink`, `NLLField`).
  Each has `draw()`, `update_colors()`, `update_<surface>_params()`, the
  `reset_*` methods and `_get_plot_range_limits()`.
- `sportypy/_feature_classes/<sport>.py`: the features a surface draws (lines,
  circles, creases), each a `BaseFeature` subclass.
- `sportypy/_base_classes/`: `BaseSurface` (units, display ranges, `_reinit`,
  `_split_units_update`), `BaseSurfacePlot` (the plotting helpers: `scatter`,
  `heatmap`, `contour`, `hexbin`, `arrow`, ...) and `BaseFeature`.
- `sportypy/data/surface_dimensions.json`: every league's rule-book dimensions,
  in the league's own units. `unit_conversions.json`: the conversion table.
- `rule-books/`: the source rule books, for reference.
- `docs/`: the Sphinx site (myst-parser Markdown, bootstrap theme). The built
  site is committed under `docs/_build`; never edit it by hand.

## sportyR parity

- New leagues and dimension changes come from sportyR's
  `data-raw/surface-dimensions.json` through `tools/sync_dimensions.py`
  (`--check` reports drift; `--align` replaces drifted leagues). Do not retype
  values.
- `tests/data/sportyr_*_fixture.json` are what sportyR's own `geom_*()` draws,
  captured by `tools/<sport>_fixture.R` from a sportyR checkout (the README
  beside each fixture says how). They are generated: regenerate, never edit.
  `tests/test_*_parity.py` compare sportypy to them point for point.
- A port from sportyR keeps sportyR's semantics; where sportypy differs on
  purpose, say so in the docstring and the changelog.

## Code style

- Follow the surrounding code. The surface and feature modules space keyword
  arguments (`ax = ax`) and use NumPy-style docstrings; `ruff format` is NOT
  used (it would rewrite every file). `ruff check` is (see `ruff.toml`).
- Lengths are in the surface's units; counts (`_COUNT_PARAMS`, e.g. dash
  counts) are never unit-converted.
- The update and reset methods rebuild the surface through `self._reinit(...)`
  and keep its rotation, translation, league and units.

## Gates

```bash
uv sync --locked
uv run --no-sync ruff check .
uv run --no-sync pre-commit run --all-files
uv run --no-sync pytest tests/
uv run --no-sync sphinx-build -W --keep-going -b html docs "${TMPDIR:-/tmp}/sportypy-docs"
```

CI runs the same (`.github/workflows/`): `package-coverage` (tests, Python 3.10
and 3.14), `quality` (ruff, pre-commit, zizmor, build), `docs` (Sphinx).
`uv run` can re-lock: check `git status` and never let a `uv.lock` change ride
into an unrelated commit (`uv lock --check` is a pre-commit hook).

## Release

1. Bump `version` in `pyproject.toml` and add the version's section to
   `docs/changelog.md` (one bullet per user-visible change).
2. Merge to `main`, then create the GitHub Release `vX.Y.Z`: that runs
   `upload-to-pypi.yml` (`uv build` + `uv publish`).

## Windows

`.gitattributes` keeps text files LF in the index and the checkout (`make.bat`
is CRLF). If a diff shows every line of a file changed, it is a line-ending
flip: check `git diff --ignore-cr-at-eol` before committing.
