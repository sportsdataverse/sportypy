# sportyr_softball_fixture.json

Coordinates computed by sportyR's own R code for the NCAA softball field
(`softball_*` feature functions in `R/features-softball.R`, parameters from
`data-raw/surface-dimensions.json`), plus the anchors `R/geom-softball.R`
places them at.

- sportyR checkout: `<sportyR checkout>`, branch
  `fix/geometry-quirks` commit 972da8ca0a7bef02b2be674bbe2f001275365cb6
  (see `provenance` in the JSON)
- Captured 2026-10-18 (Rscript 4.6.1); loaded with `pkgload::load_all()`, not installed
- Regenerate: `Rscript tools/softball_fixture.R <path to sportyR> tests/data/sportyr_softball_fixture.json`
  (or set `SPORTYR_PATH` and pass only the output path)
- sportyR draws circles with 1000 points, sportypy with 10000, so circular
  features are compared by ring endpoints and radius, not point by point.
