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
- `docs/`: the Docusaurus site (sportypy.sportsdataverse.org), in the
  SportsDataverse docs family (`src/css/sdv-theme.css` is byte-identical to
  sdvplot's; sportypy's colors and type are in `src/css/custom.css`).
  `yarn start` / `yarn build` first run `tools/gen_docs.py`, which writes the API
  reference, the usage guide (from the README), the News page (from
  `CHANGELOG.md`) and the homepage's surface drawings from the code. None of
  that is committed: change the docstring, the README or the changelog, never a
  generated page.
- Publishing: `docs-build` builds the site on pull requests; `docs-deploy`
  builds `main` and publishes it to the `gh-pages` branch (one orphan commit).
  Vercel serves `gh-pages` as static files and builds nothing (production
  branch `gh-pages`; an ignored-build step skips every other branch).
  `docs/static/vercel.json` lands at the branch root and redirects the old
  Sphinx URLs (`/surfaces/hockey/nhl.html` and so on).
- `examples/notebooks/`: the cookbooks (sportypy with sportsdataverse-py data
  and sdvplot colors). They load live data, so they are committed WITH their
  outputs and executed by hand, never in CI:
  `uv run --group cookbook jupyter nbconvert --to notebook --execute --inplace examples/notebooks/<name>.ipynb`.
  `gen_docs.py` turns each into a page under `docs/docs/cookbooks/` and
  fails the build on one not run top to bottom (execution counts 1..n) or with
  an error output. Print polars frames (`ASCII_MARKDOWN`) so they become tables;
  tag a figure's cell `gallery` for the overview and homepage. On this Windows
  box a global Jupyter config loads a missing nbextensions preprocessor: set
  `JUPYTER_CONFIG_DIR` to an empty folder when executing.

## sportyR parity

- New leagues and dimension changes come from sportyR's
  `data-raw/surface-dimensions.json` through `tools/sync_dimensions.py`
  (`--check` reports drift; `--align` replaces drifted leagues). The
  `dimensions-drift` workflow runs `--check` weekly and fails on drift. Do not
  retype values.
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
(cd docs && yarn install --frozen-lockfile && yarn build)  # fails on a broken link
```

CI runs the same (`.github/workflows/`): `package-coverage` (tests, Python 3.10
and 3.14), `quality` (ruff, pre-commit, zizmor, build), `docs-build` (the
site, on pull requests) and `docs-deploy` (`main` to `gh-pages`).
`uv run` can re-lock: check `git status` and never let a `uv.lock` change ride
into an unrelated commit (`uv lock --check` is a pre-commit hook).

## Release

Releases are cut by `release.yml` (semantic-release, config in `.releaserc.json`)
on every push to `main`. The conventional-commit types decide the bump: `fix` and
`perf` patch, `feat` minor, `!` or `BREAKING CHANGE:` major, anything else none.
It runs `uv version` (`pyproject.toml` and `uv.lock`), prepends the notes to
`CHANGELOG.md`, pushes a `chore(release)` commit and the `vX.Y.Z` tag, and creates
the GitHub Release, which runs `upload-to-pypi.yml` (`uv build` + `uv publish`).
Never bump the version or edit the generated changelog entries by hand.

## Windows

`.gitattributes` keeps text files LF in the index and the checkout. If a diff shows every line of a file changed, it is a line-ending
flip: check `git diff --ignore-cr-at-eol` before committing.
