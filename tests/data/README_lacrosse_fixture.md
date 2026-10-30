# sportyr_lacrosse_fixture.json

What sportyR's own `geom_lacrosse()` draws for each of its seven lacrosse
leagues (`ncaam`, `ncaaw`, `nll`, `pll`, `usam`, `usaw`, `world lacrosse`).
For each league: the league's parameters, every ggplot polygon layer in
drawing order (point count; sums of x, y, x², y², xy over every point; every
25th point plus the last; fill and outline colour), and the display limits of
the `full`, `in_bounds_only`, `offense` and `defense` ranges.

- sportyR checkout: `<sportyR checkout>`, `main` commit
  e021040cbdd9d7c3562051316ccc76d31c6ac0dc (sportyR 2.4.5)
  (see `provenance` in the JSON)
- Captured 2026-10-30 (Rscript 4.6.1); loaded with `pkgload::load_all()`, not installed
- Regenerate: `Rscript tools/lacrosse_fixture.R <path to sportyR> tests/data/sportyr_lacrosse_fixture.json`
  (or set `SPORTYR_PATH` and pass only the output path)
- sportypy's lacrosse features use sportyR's 1000-point circles, so every
  polygon is compared point for point (tests/test_lacrosse_class.py). As in
  sportyR, a feature with no area and no visible outline is not drawn, so it
  has no layer here.
- `unit_cases`: the same summaries for the surface drawn in other units and / or
  shifted, compared in tests/test_unit_parity.py.
