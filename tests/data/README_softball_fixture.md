# sportyr_softball_fixture.json

Coordinates computed by sportyR's own R code for the NCAA softball field
(`softball_*` feature functions in `R/features-softball.R`, parameters from
`data-raw/surface-dimensions.json`), plus the anchors `R/geom-softball.R`
places them at.

- sportyR commit: 562e8c410d6f8ce255b7ead68eb6c6580889ad44 (see `provenance` in the JSON)
- R: 4.6.1; loaded with `pkgload::load_all()`
- Regenerate: `Rscript tools/softball_fixture.R <path to sportyR> tests/data/sportyr_softball_fixture.json`
- sportyR draws circles with 1000 points, sportypy with 10000, so circular
  features are compared by ring endpoints and radius, not point by point.
