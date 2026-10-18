# sportyr_softball_fixture.json

Coordinates computed by sportyR's own R code for the NCAA softball field
(`softball_*` feature functions in `R/features-softball.R`, parameters from
`data-raw/surface-dimensions.json`), plus the anchors `R/geom-softball.R`
places them at.

- sportyR checkout: `C:/Users/saiem/Documents/GitHub-Data/sdv-dev/wt-syr-quirks`, branch
  `fix/geometry-quirks` (sportyR PR #68, final head), commit 00e364ad7916668a951ee1d008b64f77203d2e36
  (see `provenance` in the JSON)
- Captured 2026-10-18 (Rscript 4.6.1); loaded with `pkgload::load_all()`, not installed
- Regenerate: `Rscript tools/softball_fixture.R <path to sportyR> tests/data/sportyr_softball_fixture.json`
  (or set `SPORTYR_PATH` and pass only the output path)
- sportyR draws circles with 1000 points, sportypy with 10000, so circular
  features are compared by ring endpoints and radius, not point by point.
