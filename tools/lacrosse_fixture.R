# Regenerates tests/data/sportyr_lacrosse_fixture.json from a local sportyR checkout.
# Usage: Rscript tools/lacrosse_fixture.R PATH/TO/sportyR OUT.json
#    or: SPORTYR_PATH=PATH/TO/sportyR Rscript tools/lacrosse_fixture.R OUT.json
# The checkout is loaded with pkgload::load_all() (never installed); its path
# and commit are recorded in the JSON's provenance.
#
# For every league, geom_lacrosse() is built and each ggplot polygon layer is
# summarised in drawing order: point count, coordinate moments over every
# point, every 25th point (plus the last), fill and outline colour. Display
# limits are recorded for each display range.
args <- commandArgs(trailingOnly = TRUE)
sportyr <- if (length(args) >= 2) args[1] else Sys.getenv("SPORTYR_PATH")
out_path <- args[length(args)]
stopifnot(nzchar(sportyr), dir.exists(sportyr))
suppressMessages(pkgload::load_all(sportyr, quiet = TRUE))
leagues <- setdiff(names(surface_dimensions[["lacrosse"]]), "custom")
ranges <- c("full", "in_bounds_only", "offense", "defense")
summarise_layer <- function(layer) {
  x <- layer$data$x
  y <- layer$data$y
  n <- length(x)
  idx <- if (n > 0) unique(c(seq(1, n, by = 25), n)) else integer(0)
  list(
    n = n,
    moments = c(sum(x), sum(y), sum(x * x), sum(y * y), sum(x * y)),
    idx = idx - 1,
    x = x[idx],
    y = y[idx],
    fill = layer$aes_params$fill,
    colour = layer$aes_params$colour
  )
}
out <- list(
  provenance = list(
    sportyR_path = normalizePath(sportyr, winslash = "/"),
    sportyR_commit = system(paste("git -C", shQuote(sportyr), "rev-parse HEAD"), intern = TRUE),
    command = "Rscript tools/lacrosse_fixture.R <sportyR checkout> tests/data/sportyr_lacrosse_fixture.json",
    r_version = R.version.string
  ),
  leagues = lapply(stats::setNames(leagues, leagues), function(lg) {
    p <- geom_lacrosse(lg)
    list(
      params = surface_dimensions[["lacrosse"]][[lg]],
      layers = unname(lapply(p$layers, summarise_layer)),
      limits = lapply(stats::setNames(ranges, ranges), function(r) {
        q <- geom_lacrosse(lg, display_range = r)
        list(x = q$coordinates$limits$x, y = q$coordinates$limits$y)
      })
    )
  })
)
# Unit and translation cases (sportyR #74 / #76): the surface drawn in other
# units and / or shifted, as geom_lacrosse() draws it
unit_cases <- list(
  nll_m_shifted = list(league = "nll", field_units = "m", x_trans = 3, y_trans = -2),
  ncaaw_ft = list(league = "ncaaw", field_units = "ft")
)
out$unit_cases <- lapply(unit_cases, function(args) {
  p <- do.call(geom_lacrosse, args)
  list(
    args = args,
    layers = unname(lapply(p$layers, summarise_layer)),
    limits = list(x = p$coordinates$limits$x, y = p$coordinates$limits$y)
  )
})
writeLines(jsonlite::toJSON(out, auto_unbox = TRUE, digits = NA, pretty = FALSE, na = "null"), out_path)
