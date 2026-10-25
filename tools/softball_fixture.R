# Regenerates tests/data/sportyr_softball_fixture.json from a local sportyR checkout.
# Usage: Rscript tools/softball_fixture.R PATH/TO/sportyR OUT.json
#    or: SPORTYR_PATH=PATH/TO/sportyR Rscript tools/softball_fixture.R OUT.json
# The checkout is loaded with pkgload::load_all() (never installed); its path
# and commit are recorded in the JSON's provenance.
args <- commandArgs(trailingOnly = TRUE)
sportyr <- if (length(args) >= 2) args[1] else Sys.getenv("SPORTYR_PATH")
out_path <- args[length(args)]
stopifnot(nzchar(sportyr), dir.exists(sportyr))
suppressMessages(pkgload::load_all(sportyr, quiet = TRUE))
p <- surface_dimensions[["softball"]][["ncaa"]]
df <- function(d) list(x = d$x, y = d$y)
b <- p$baseline_distance
f <- list(
  home_plate = df(softball_home_plate(p$home_plate_edge_length)),
  first_base = df(softball_base(p$base_side_length, TRUE, FALSE)),
  third_base = df(softball_base(p$base_side_length, FALSE, TRUE)),
  pitchers_plate = df(softball_pitchers_plate(p$pitchers_plate_length, p$pitchers_plate_width)),
  batters_box = df(softball_batters_box(p$batters_box_length, p$batters_box_width, p$batters_box_y_adj, p$line_width)),
  catchers_box = df(softball_catchers_box(p$catchers_box_depth, p$catchers_box_width, p$batters_box_length, p$batters_box_y_adj, p$line_width)),
  first_base_line = df(softball_foul_line(TRUE, p$right_field_distance, p$batters_box_length, p$batters_box_width, p$batters_box_y_adj, p$home_plate_side_to_batters_box, p$home_plate_edge_length, p$line_width)),
  third_base_line = df(softball_foul_line(FALSE, p$left_field_distance, p$batters_box_length, p$batters_box_width, p$batters_box_y_adj, p$home_plate_side_to_batters_box, p$home_plate_edge_length, p$line_width)),
  running_lane = df(softball_running_lane(p$running_lane_depth, p$running_lane_length, p$running_lane_start_distance, p$line_width)),
  pitchers_circle = df(softball_pitchers_circle(p$pitchers_circle_radius, p$line_width)),
  pitchers_lane = df(softball_pitchers_lane(p$pitchers_lane_length, p$pitchers_plate_length, p$pitchers_plate_front_to_home_plate, p$home_plate_edge_length, p$home_plate_side_to_batters_box, p$batters_box_length, p$batters_box_y_adj, p$line_width)),
  coaches_box = df(softball_coaches_box(b, p$coaches_box_depth, p$coaches_box_length, p$coaches_box_width, p$line_width)),
  infield_dirt = df(softball_infield_dirt(p$home_plate_circle_radius, p$foul_line_to_foul_grass, p$pitchers_plate_front_to_home_plate, p$infield_arc_radius))
)
anchors <- list(
  first_base = c(b * cos(pi / 4), b * sin(pi / 4)),
  second_base = c(0, b * sqrt(2)),
  third_base = c(b * cos(3 * pi / 4), b * sin(3 * pi / 4)),
  pitchers_plate = c(0, p$pitchers_plate_front_to_home_plate),
  pitchers_circle = c(0, p$pitchers_plate_front_to_home_plate),
  pitchers_lane = c(0, p$pitchers_plate_front_to_home_plate),
  batters_box = c(p$home_plate_edge_length / 2 + p$home_plate_side_to_batters_box + p$batters_box_width / 2, 0)
)
out <- list(provenance = list(
  sportyR_path = "<sportyR checkout>",  # the commit identifies it; a local path would leak
    sportyR_commit = system(paste("git -C", shQuote(sportyr), "rev-parse HEAD"), intern = TRUE),
  command = "Rscript tools/softball_fixture.R <sportyR checkout> tests/data/sportyr_softball_fixture.json",
  r_version = R.version.string, league = "ncaa"),
  params = p, anchors = anchors, features = f)
writeLines(jsonlite::toJSON(out, auto_unbox = TRUE, digits = NA, pretty = TRUE), out_path)
