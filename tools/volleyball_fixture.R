# Regenerates tests/data/sportyr_volleyball_fixture.json from a local sportyR checkout.
# Usage: Rscript tools/volleyball_fixture.R PATH/TO/sportyR OUT.json
#    or: SPORTYR_PATH=PATH/TO/sportyR Rscript tools/volleyball_fixture.R OUT.json
# The checkout is loaded with pkgload::load_all() (never installed); its path
# and commit are recorded in the JSON's provenance.
#
# For every league, geom_volleyball() is built and each ggplot polygon layer is
# summarised in drawing order: point count, coordinate moments over every
# point, every 25th point (plus the last), fill and outline colour.
args <- commandArgs(trailingOnly = TRUE)
sportyr <- if (length(args) >= 2) args[1] else Sys.getenv("SPORTYR_PATH")
out_path <- args[length(args)]
stopifnot(nzchar(sportyr), dir.exists(sportyr))
suppressMessages(pkgload::load_all(sportyr, quiet = TRUE))
leagues <- c("fivb", "usa volleyball", "ncaa")
summarise_layer <- function(layer) {
  x <- layer$data$x
  y <- layer$data$y
  n <- length(x)
  idx <- if (n > 0) unique(c(seq(1, n, by = 25), n)) else integer(0)
  list(
    geom = class(layer$geom)[1],
    n = n,
    moments = c(sum(x), sum(y), sum(x * x), sum(y * y), sum(x * y)),
    idx = idx - 1,
    x = x[idx],
    y = y[idx],
    fill = layer$aes_params$fill,
    colour = layer$aes_params$colour,
    box = if (all(c("x_min", "x_max", "y_min", "y_max") %in% names(layer$data))) {
      as.list(layer$data[c("x_min", "x_max", "y_min", "y_max")])
    } else {
      NULL
    }
  )
}
out <- list(
  provenance = list(
    sportyR_path = normalizePath(sportyr, winslash = "/"),
    sportyR_commit = system(paste("git -C", shQuote(sportyr), "rev-parse HEAD"), intern = TRUE),
    command = "Rscript tools/volleyball_fixture.R <sportyR checkout> tests/data/sportyr_volleyball_fixture.json",
    r_version = R.version.string
  ),
  leagues = lapply(stats::setNames(leagues, leagues), function(lg) {
    p <- geom_volleyball(lg)
    list(
      params = surface_dimensions[["volleyball"]][[lg]],
      layers = unname(lapply(p$layers, summarise_layer)),
      limits = list(x = p$coordinates$limits$x, y = p$coordinates$limits$y)
    )
  })
)
# Unit and translation cases (sportyR #74 / #76): the surface drawn in other
# units and / or shifted, as geom_volleyball() draws it
unit_cases <- list(
  fivb_in_shifted = list(league = "fivb", court_units = "in", x_trans = 12, y_trans = -6)
)
out$unit_cases <- lapply(unit_cases, function(args) {
  p <- do.call(geom_volleyball, args)
  list(
    args = args,
    layers = unname(lapply(p$layers, summarise_layer)),
    limits = list(x = p$coordinates$limits$x, y = p$coordinates$limits$y)
  )
})
writeLines(jsonlite::toJSON(out, auto_unbox = TRUE, digits = NA, pretty = FALSE, na = "null"), out_path)
