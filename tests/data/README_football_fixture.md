# sportyr_football_fixture.json

What sportyR's own `geom_football()` draws for `ncaa`, `nfl`, `nfhs11`,
`nfhs9`, `nfhs8`, `nfhs6` and `cfl`. For each league: the league's parameters,
every ggplot layer in drawing order (geom; point count; sums of x, y, x², y²,
xy over every point; every 25th point plus the last; fill and outline colour),
the plot's x/y limits, and the limits of the `full`, `in_bounds_only`, `offense`,
`defense`, `redzone` and `dredzone` display ranges (`range_limits`).

- sportyR checkout: `<sportyR checkout>`, branch
  `fix/geometry-quirks` (sportyR PR #68, final head), commit 972da8ca0a7bef02b2be674bbe2f001275365cb6
  (see `provenance` in the JSON)
- Captured 2026-10-18 (Rscript 4.6.1); loaded with `pkgload::load_all()`, not installed
- Regenerate: `Rscript tools/football_fixture.R <path to sportyR> tests/data/sportyr_football_fixture.json`
  (or set `SPORTYR_PATH` and pass only the output path)
- tests/test_football_parity.py pairs every sportyR polygon with one sportypy
  feature point for point (1e-9) and checks its fill. The yard numbers' boxes
  (fully transparent, no outline) are the only polygons sportypy does not draw:
  it draws the numbers as text. Each display range's limits are compared too.
- `unit_cases`: the same summaries for the surface drawn in other units and / or
  shifted (sportyR #74 / #76), compared in tests/test_unit_parity.py.
