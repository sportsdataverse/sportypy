# sportyr_lacrosse_fixture.json

What sportyR's own `geom_lacrosse()` draws for each of its seven lacrosse
leagues (`ncaam`, `ncaaw`, `nll`, `pll`, `usam`, `usaw`, `world lacrosse`).
For each league: the league's parameters, every ggplot polygon layer in
drawing order (point count; sums of x, y, x², y², xy over every point; every
25th point plus the last; fill and outline colour), and the display limits of
the `full`, `in_bounds_only`, `offense` and `defense` ranges.

- sportyR commit: 562e8c410d6f8ce255b7ead68eb6c6580889ad44 (see `provenance` in the JSON)
- R: 4.6.1; loaded with `pkgload::load_all()`
- Regenerate: `Rscript tools/lacrosse_fixture.R <path to sportyR> tests/data/sportyr_lacrosse_fixture.json`
- sportypy's lacrosse features use sportyR's 1000-point circles, so every
  polygon is compared point for point (tests/test_lacrosse_class.py).
