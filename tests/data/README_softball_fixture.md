# sportyr_softball_fixture.json

Coordinates computed by sportyR's own R code for the NCAA softball field
(`softball_*` feature functions in `R/features-softball.R`, parameters from
`data-raw/surface-dimensions.json`), plus the anchors `R/geom-softball.R`
places them at.

- sportyR checkout: `<sportyR checkout>`, `main` commit
  e021040cbdd9d7c3562051316ccc76d31c6ac0dc (sportyR 2.4.5)
  (see `provenance` in the JSON)
- Captured 2026-10-30 (Rscript 4.6.1); loaded with `pkgload::load_all()`, not installed
- Regenerate: `Rscript tools/softball_fixture.R <path to sportyR> tests/data/sportyr_softball_fixture.json`
  (or set `SPORTYR_PATH` and pass only the output path)
- sportyR and sportypy both draw circles with 1000 points, but circular
  features are still compared by ring endpoints, radius, direction and sweep,
  not point by point.
