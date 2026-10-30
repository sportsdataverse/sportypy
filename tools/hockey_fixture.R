# Regenerates tests/data/sportyr_hockey_fixture.json from a local sportyR checkout.
# Usage: Rscript tools/hockey_fixture.R PATH/TO/sportyR OUT.json
#    or: SPORTYR_PATH=PATH/TO/sportyR Rscript tools/hockey_fixture.R OUT.json
# The checkout is loaded with pkgload::load_all() (never installed); its path
# and commit are recorded in the JSON's provenance.
#
# For every league, geom_hockey() is built and each ggplot polygon layer is
# summarised in drawing order: point count, coordinate moments over every
# point, every 25th point (plus the last), fill and outline colour.
args <- commandArgs(trailingOnly = TRUE)
sportyr <- if (length(args) >= 2) args[1] else Sys.getenv("SPORTYR_PATH")
out_path <- args[length(args)]
stopifnot(nzchar(sportyr), dir.exists(sportyr))
suppressMessages(pkgload::load_all(sportyr, quiet = TRUE))
leagues <- setdiff(names(surface_dimensions[["hockey"]]), "custom")
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
    sportyR_path = "<sportyR checkout>",  # the commit identifies it; a local path would leak
    sportyR_commit = system(paste("git -C", shQuote(sportyr), "rev-parse HEAD"), intern = TRUE),
    command = "Rscript tools/hockey_fixture.R <sportyR checkout> tests/data/sportyr_hockey_fixture.json",
    r_version = R.version.string
  ),
  leagues = lapply(stats::setNames(leagues, leagues), function(lg) {
    p <- geom_hockey(lg)
    list(layers = unname(lapply(p$layers, summarise_layer)))
  })
)
# Unit and translation case: the rink drawn in metres and shifted, as
# geom_hockey() draws it
unit_cases <- list(
  nhl_m_shifted = list(league = "nhl", rink_units = "m", x_trans = 3, y_trans = -2)
)
out$unit_cases <- lapply(unit_cases, function(args) {
  p <- do.call(geom_hockey, args)
  list(args = args, layers = unname(lapply(p$layers, summarise_layer)))
})
writeLines(jsonlite::toJSON(out, auto_unbox = TRUE, digits = NA, pretty = FALSE, na = "null"), out_path)
