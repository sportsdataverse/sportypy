# Regenerates tests/data/sportyr_lacrosse_fixture.json from a local sportyR checkout.
# Usage: Rscript tools/lacrosse_fixture.R PATH/TO/sportyR OUT.json
#
# For every league, geom_lacrosse() is built and each ggplot polygon layer is
# summarised in drawing order: point count, coordinate moments over every
# point, every 25th point (plus the last), fill and outline colour. Display
# limits are recorded for each display range.
args <- commandArgs(trailingOnly = TRUE)
suppressMessages(pkgload::load_all(args[1], quiet = TRUE))
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
    sportyR_commit = system(paste("git -C", shQuote(args[1]), "rev-parse HEAD"), intern = TRUE),
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
writeLines(jsonlite::toJSON(out, auto_unbox = TRUE, digits = NA, pretty = FALSE, na = "null"), args[2])
