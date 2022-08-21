"""Draw the plots that appear in the README.

@author: Ross Drucker
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import sportypy.surfaces.hockey as hockey
import sportypy.surfaces.curling as curling
import sportypy.surfaces.football as football
import sportypy.surfaces.basketball as basketball

# Draw the NFL Red Zone plot
nfl = football.NFLField(x_trans = 50.0, y_trans = 26.6667)
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)
nfl.draw(ax = ax, display_range = "red zone")
plt.savefig(
    "img/nfl-red-zone.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Draw the NHL rink
nhl = hockey.NHLRink()
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)
nhl.draw(ax = ax)
plt.savefig(
    "img/nhl-rink.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Draw the curling house
wcf = curling.WCFSheet()
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)
wcf.draw(ax = ax, display_range = "house")
plt.savefig(
    "img/curling-house.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Customize a college basketball court to replicate that of the University of
# Illinois Fighting Illini
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)
custom_ncaa = basketball.NCAACourt(
    color_updates = {
        "plot_background": "#ffffff00",
        "offensive_half_court": "#e8e0d7",
        "defensive_half_court": "#e8e0d7",
        "court_apron": "#e84a27",
        "two_point_range": ["#e8e0d7", "#ffffff66"],
        "center_circle_fill": "#e8e0d7",
        "painted_area": ["#e84a27", None],
        "free_throw_circle_fill": "#e8e0d7",
        "sideline": "#13294b",
        "endline": "#13294b",
        "division_line": "#13294b",
        "center_circle_outline": "#13294b",
        "lane_boundary": ["#ffffff", "#ffffff00"],
        "three_point_line": ["#13294b", "#ffffff"],
        "free_throw_circle_outline": "#ffffff",
        "lane_space_mark": "#ffffff",
        "restricted_arc": "#13294b",
        "backboard": "#13294b"
    }
)
custom_ncaa.draw(ax = ax)
plt.savefig(
    "img/custom-ncaa-court.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Draw the BDC shot data

# Read in the Big Data Cup (BDC) data from 2021
bdc = pd.read_csv(os.path.join("tests", "data", "bdc_2021_data.csv"))

# Filter to only be shots
shots = bdc.loc[bdc["Event"].isin(["Shot", "Goal"])]

# Separate shots by team
bos_shots = shots[shots["Team"] == "Boston Pride"]
min_shots = shots[shots["Team"] == "Minnesota Whitecaps"]

# Instantiate a PHF rink, adjusting the coordinates to match the data
# (The coordinate (0, 0) is in the bottom-left of the plot)
phf = hockey.PHFRink(x_trans = 100.0, y_trans = 42.5)

# Draw the rink on a matplotlib.Axes object
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)
phf.draw(ax = ax)

# Add the plot of each team's shots
phf.scatter(
    bos_shots["X Coordinate"],
    bos_shots["Y Coordinate"],
    color = "#fec52e"
)
phf.scatter(
    200.0 - min_shots["X Coordinate"],
    85.0 - min_shots["Y Coordinate"],
    color = "#2251b8"
)
plt.savefig(
    "img/phf-shots-scatterplot.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Draw the arrow plot from BDC data

# Filter to only be Boston's passes
passes = bdc.loc[
    (bdc["Team"] == "Boston Pride") &
    (bdc["Event"] == "Play")
]

# Instantiate a PHF rink, adjusting the coordinates to match the data
# (The coordinate (0, 0) is in the bottom-left of the plot)
phf = hockey.PHFRink(x_trans = 100.0, y_trans = 42.5)

# Draw the rink on a matplotlib.Axes object
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)
phf.draw(ax = ax)

# Add the arrow plot of Boston's passes
phf.arrow(
    passes["X Coordinate"],
    passes["Y Coordinate"],
    passes["X Coordinate 2"],
    passes["Y Coordinate 2"],
    color = "#ffcb05"
)
plt.savefig(
    "img/phf-passes-arrowplot.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Draw Ayo Dosunmu's rookie season shot heat map

# Read in the shot chart data
shot_data = pd.read_csv(
    os.path.join("tests", "data", "nba_example_shot_chart.csv")
)

# Define the matplotlib instances to plot onto
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(20, 10)

# Start by instantiating a court class. NBA shot data is what's used, so
# an NBA court is selected. The rotation is to display a traditional shot
# chart of only the offensive half
nba = basketball.NBACourt(x_trans = -41.75)
ax = nba.draw(ax = ax, display_range = "offense")
nba.heatmap(
    shot_data["LOC_X"],
    shot_data["LOC_Y"],
    values = shot_data["SHOT_RESULT"],
    ax = ax,
    alpha = 0.75,
    cmap = "hot"
)
plt.savefig(
    "img/ayo-dosunmu-rookie-shot-chart.png",
    format = "png",
    dpi = 600,
    transparent = True
)
plt.close()

# Load in the data
pbp = pd.read_csv(
    os.path.join("tests", "data", "nhl_pbp_data.csv")
)

# Create a matplotlib.Axes object for the test plots to lie on
fig, axs = plt.subplots(1, 3)
fig.set_size_inches(20, 10)

# Instantiate an NHL rink
nhl = hockey.NHLRink(rotation = 270)

# Draw a rink on each of the three matplotlib.Axes objects defined above
# and subset them to only the offensive zone
for i in range(3):
    nhl.draw(ax = axs[i], display_range = "ozone")

# Add the contour plot
contour_img = nhl.contourf(
    pbp["x"],
    pbp["y"],
    values = pbp["goal"],
    ax = axs[0],
    cmap = "bwr",
    plot_range = "ozone",
    binsize = 10,
    levels = 50,
    statistic = "mean"
)

# Add a colorbar legend to the bottom to make the metrics easier to read
plt.colorbar(contour_img, ax = axs[0], orientation = "horizontal")

# Add the heatmap plot
nhl.heatmap(
    pbp["x"],
    pbp["y"],
    values = pbp["goal"],
    ax = axs[1],
    cmap = "magma",
    plot_xlim = (25, 89),  # offensive-side blue line to the goal line
    statistic = "mean",
    vmax = 0.2,
    binsize = 3
)

# Add the hexbin plot
nhl.hexbin(
    pbp["x"],
    pbp["y"],
    values = pbp["goal"],
    ax = axs[2],
    binsize = (8, 12),
    plot_range = "ozone",
    zorder = 25,
    alpha = 0.85
)

plt.savefig(
    "img/nhl-matplotlib-demo.png",
    format = "png",
    dpi = 600,
    transparent = True
)
