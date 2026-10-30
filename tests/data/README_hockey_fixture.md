# sportyr_hockey_fixture.json

What sportyR's own `geom_hockey()` draws for each of its hockey leagues. For
each league: every ggplot polygon layer in drawing order (point count; sums of
x, y, x², y², xy over every point; every 25th point plus the last; fill and
outline colour).

- sportyR checkout: `<sportyR checkout>`, `main` commit
  e021040cbdd9d7c3562051316ccc76d31c6ac0dc (sportyR 2.4.5)
  (see `provenance` in the JSON)
- Captured 2026-10-30 (Rscript 4.6.1); loaded with `pkgload::load_all()`, not installed
- Regenerate: `Rscript tools/hockey_fixture.R <path to sportyR> tests/data/sportyr_hockey_fixture.json`
  (or set `SPORTYR_PATH` and pass only the output path)
- tests/test_hockey_parity.py pairs every sportypy feature with one sportyR
  polygon (same point count, coordinate sums and moments, and sampled points,
  to 1e-9) and checks its fill; every sportyR polygon must be matched.
- `unit_cases`: the same summaries for the NHL rink drawn in metres and
  shifted, compared in the same test file.
