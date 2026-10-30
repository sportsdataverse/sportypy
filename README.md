# sportypy <img src="https://raw.githubusercontent.com/sportsdataverse/sportypy/main/logos/sportypy-logo-200.png" align="right" width="120"/>

[![PyPI](https://img.shields.io/pypi/v/sportypy?color=ff552e&logo=pypi&logoColor=white)](https://pypi.org/project/sportypy/)
[![Python](https://img.shields.io/pypi/pyversions/sportypy?color=ff552e&logo=python&logoColor=white)](https://pypi.org/project/sportypy/)
[![package-coverage](https://img.shields.io/github/actions/workflow/status/sportsdataverse/sportypy/package-coverage.yml?branch=main&label=tests&logo=github)](https://github.com/sportsdataverse/sportypy/actions/workflows/package-coverage.yml)
[![quality](https://img.shields.io/github/actions/workflow/status/sportsdataverse/sportypy/quality.yml?branch=main&label=quality&logo=github)](https://github.com/sportsdataverse/sportypy/actions/workflows/quality.yml)
[![codecov](https://img.shields.io/codecov/c/github/sportsdataverse/sportypy?color=ff552e&label=codecov&logo=codecov)](https://codecov.io/gh/sportsdataverse/sportypy)
[![Lifecycle:maturing](https://img.shields.io/badge/lifecycle-maturing-blue.svg?style=flat&logo=github&color=ff552e)](https://github.com/sportsdataverse/sportypy/)
[![npm](https://img.shields.io/npm/v/@sportsdataverse/sporty?label=sporty&logo=npm&style=flat&color=ff552e)](https://www.npmjs.com/package/@sportsdataverse/sporty)

As the field of sports analytics evolves, there's a growing need for methods to both track and visualize players throughout the game. This package aims to make this easy regardless of sport needed to be plotted.

This repository contains code necessary to draw scale versions of playing surfaces to visualize play-by-play data for baseball, basketball, curling, football, hockey, lacrosse, soccer, softball, tennis, and volleyball in **Python**. The **R** version of this package is [`sportyR`](https://github.com/sportsdataverse/sportyR).

For **JavaScript / TypeScript**, [`@sportsdataverse/sporty`](https://www.npmjs.com/package/@sportsdataverse/sporty) is the TypeScript port of `sportyR` and `sportypy` (`npm install @sportsdataverse/sporty`). It lives in the [sdvplot-js repo](https://github.com/sportsdataverse/sdvplot-js), and its docs are at [plot.sportsdataverse.org](https://plot.sportsdataverse.org/).

In Python, `sportypy` pairs with two other SportsDataverse packages: [`sportsdataverse-py`](https://py.sportsdataverse.org/) (`pip install sportsdataverse`) loads the play-by-play and shot data, and [`sdvplot`](https://sdvplot.sportsdataverse.org/) (`pip install "sdvplot[surfaces]"`) draws these surfaces in team colors and moves provider coordinates onto them. The [cookbooks](https://sportypy.sportsdataverse.org/docs/cookbooks) use all three.

**Documentation:** [sportypy.sportsdataverse.org](https://sportypy.sportsdataverse.org/) has a guide, the [API reference](https://sportypy.sportsdataverse.org/docs/reference/) for every surface class, and the [changelog](https://sportypy.sportsdataverse.org/CHANGELOG).

## Installation

`sportypy` supports Python 3.10 and newer. To install it via `pip`, please run

```bash
pip install sportypy
```

or, in a [`uv`](https://docs.astral.sh/uv/) project,

```bash
uv add sportypy
```

## Using the Package

Each league that is supported by `sportypy` has its own class in its respective sport under the `surfaces` submodule. The one exception is high school football: the 11-, 9-, 8- and 6-player NFHS fields are all `NFHSField`, chosen with `n_players` (see Surface Units below). As an example, you can instantiate an NHL rink like so:

```python
# Load from the hockey submodule in surfaces
from sportypy.surfaces.hockey import NHLRink

# Create the NHL rink
nhl = NHLRink()
```

If you want to see what this would yield, you may call the `draw()` method that belongs to each league surface, like so:

```python
# Draw the NHL rink
nhl.draw()
```

![Full NHL rink output from sportypy](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/nhl-rink.png)

Each league's class may take on the following arguments when it is created:

- `{surface_type}_updates` (`rink_updates`, `court_updates`, `field_updates`, `pitch_updates` or `sheet_updates`, depending on the sport): A dictionary of updates to the parameters that define the surface. To get the list of parameters you can change, run `cani_change_dimensions()` on your league's surface

- `color_updates`: A dictionary of updates to the features' colors on the plot. These are named by what the feature is, using `snake_case` to specify the names. To get the list of color names you can change, run `cani_color_features()` on your league's surface (e.g. `NHLRink().cani_color_features()`)

- `rotation`: An angle (in degrees) that you'd like to rotate the plot by, where +θ is counterclockwise

- `x_trans` and `y_trans`: By default, the origin of the coordinate system *always* lies at the center of the plot. For example, `(0.0, 0.0)` on a basketball court lies along the division line and on the line that connects the center of each basket. If you want to shift the origin (and therefore the entire plot), use `x_trans` and `y_trans` to do so

- `units`: If your data is in units that are different than how the rule book of the league specifies the units (e.g. you've got NHL data in inches, but the rule book describes the rink in feet), set this to the units you've got your data in, as in `NHLRink(units = "in")`. You're welcome to change the units of the data as well, but this is provided for convenience

The `draw()` method then takes:

- `ax`: The `matplotlib.Axes` object to draw on (a new figure is created if you don't pass one). `draw()` returns the `Axes` it drew on

- `display_range`: This automatically "zooms" in on the area of the plot you're interested in. Valid ranges here vary by sport, and are listed for each sport in the [API reference](https://sportypy.sportsdataverse.org/docs/reference/)

- `xlim` and `ylim`: Any limits you'd like to put on the plot in the x and y direction. These will overwrite anything set by the `display_range` parameter

- `rotation`: An angle (in degrees) to rotate this drawing by, in place of the surface's own `rotation`

`cani_plot_leagues()` lists the leagues that a sport's surface can be drawn for.

Some class names exist in several sports (e.g. `NCAACourt` in basketball, tennis and volleyball; `NCAAField` and `NFHSField` in baseball and football). The package-level `sportypy.surfaces.<name>` resolves to only one of them, so always import colliding names from their sport module, e.g. `from sportypy.surfaces.volleyball import NCAACourt`.

## TV View and Display Ranges

### TV View

All of the `draw()` methods, by default, will draw the surface in what can be considered "TV view", or the way that the surface would typically be displayed on a television broadcast. This typically means the action moves from left to right across the screen (a basketball game that has the baskets on the left and right end of the court). As mentioned above, it is possible to change this to be in any orientation through the `rotation` parameter to each `draw()` method.

There are a few exceptions to this:

- `{baseball league}Field` plots are displayed from the high-home view by default, as baseball coordinates typically have the `+y` axis extending from the back tip of home plate towards center field

- `{tennis league}Court` is displayed with the court diagrammed from the perspective of the chair umpire

### Display Ranges

Related to the idea of custom displays of the plot is the concept of the `display_range` parameter in the league's class `draw()` method. This is unique to each sport, but globally supported across the package. This parameter allows the specification of a designated region of the surface to display. As an example, if you're trying to limit the analysis of NFL data to being inside of the red zone, you may want to do something similar to the following:

```python
# Import football fields
from sportypy.surfaces.football import NFLField

# Draw the red zone of an NFL field
NFLField().draw(display_range = "red zone")
```

![Red zone rendered from NFL Field](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/nfl-red-zone.png)

Another use case would be to make the data you're viewing easier to see. Say you wanted to look at curling data, but only cared about stone positions in the house (and not the path as to how the stones got there). You might do this:

```python
# Import the curling sheets
from sportypy.surfaces.curling import WCFSheet

# Draw only the house of a curling sheet
WCFSheet().draw(display_range = "house")
```

![Curling house rendered from World Curling Federation sheet](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/curling-house.png)

## Surface Units

Each league's surface has a standardized unit of measure in which the plot is created, and is standardized by the primary units specified in their respective rule books. They are as follows (and any explanation is in parentheses):

|    Sport   |              League              | Primary Plotting Unit |
|:----------:|:--------------------------------:|:---------------------:|
|  Baseball  |           Little League          |          `ft`         |
|  Baseball  |               MiLB               |          `ft`         |
|  Baseball  |                MLB               |          `ft`         |
|  Baseball  |               NCAA               |          `ft`         |
|  Baseball  |        NFHS (High School)        |          `ft`         |
|  Baseball  |               Pony               |          `ft`         |
| Basketball |               FIBA               |          `m`          |
| Basketball |                NBA               |          `ft`         |
| Basketball |           NBA G League           |          `ft`         |
| Basketball |               NCAA               |          `ft`         |
| Basketball |               NFHS               |          `ft`         |
| Basketball |               WNBA               |          `ft`         |
|   Curling  |          Curling Canada          |          `ft`         |
|   Curling  |  WCF (World Curling Federation)  |          `ft`         |
|  Football  |                CFL               |          `yd`         |
|  Football  |               NCAA               |          `yd`         |
|  Football  | NFHS11 (High School, 11 players) |          `yd`         |
|  Football  |  NFHS6 (High School, 6 players)  |          `yd`         |
|  Football  |  NFHS8 (High School, 8 players)  |          `yd`         |
|  Football  |  NFHS9 (High School, 9 players)  |          `yd`         |
|  Football  |                NFL               |          `yd`         |
|   Hockey   |                AHL               |          `ft`         |
|   Hockey   |               ECHL               |          `ft`         |
|   Hockey   |               IIHF               |          `m`          |
|   Hockey   |               NCAA               |          `ft`         |
|   Hockey   |                NHL               |          `ft`         |
|   Hockey   |               NWHL               |          `ft`         |
|   Hockey   |                OHL               |          `ft`         |
|   Hockey   |                PHF               |          `ft`         |
|   Hockey   |               PWHL               |          `ft`         |
|   Hockey   |               QMJHL              |          `ft`         |
|   Hockey   |               USHL               |          `ft`         |
|  Lacrosse  |           NCAA (Men's)           |          `yd`         |
|  Lacrosse  |          NCAA (Women's)          |          `m`          |
|  Lacrosse  |        NLL (box lacrosse)        |          `ft`         |
|  Lacrosse  |                PLL               |          `yd`         |
|  Lacrosse  |       USA Lacrosse (Men's)       |          `yd`         |
|  Lacrosse  |      USA Lacrosse (Women's)      |          `m`          |
|  Lacrosse  |       World Lacrosse (box)       |          `ft`         |
|   Soccer   |                EPL               |          `m`          |
|   Soccer   |               FIFA               |          `m`          |
|   Soccer   |                MLS               |          `yd`         |
|   Soccer   |               NCAA               |          `yd`         |
|   Soccer   |               NWSL               |          `yd`         |
|  Softball  |               NCAA               |          `ft`         |
|   Tennis   |                ATP               |          `ft`         |
|   Tennis   |                ITA               |          `ft`         |
|   Tennis   |                ITF               |          `ft`         |
|   Tennis   |               NCAA               |          `ft`         |
|   Tennis   |               USTA               |          `ft`         |
|   Tennis   |                WTA               |          `ft`         |
| Volleyball |               FIVB               |          `m`          |
| Volleyball |               NCAA               |          `m`          |
| Volleyball |          USA Volleyball          |          `m`          |

The four NFHS football fields share the `NFHSField` class: `NFHSField()` draws the 11-player field, and `NFHSField(n_players = 9)`, `NFHSField(n_players = 8)` and `NFHSField(n_players = 6)` draw the others.

```python
# Draw a 6-player high school football field
from sportypy.surfaces.football import NFHSField

NFHSField(n_players = 6).draw()
```

However, since the data that is supplied may come in various units of measure, the plots are able to be generated in the data's units. This is done with the `units` argument to the class constructor, or via the `{surface_name}_updates` attribute in the class constructor, using the `{surface_name}_units` key (e.g. `NHLRink(rink_updates = {"rink_units": "in"})`). The features themselves will look visually identical, but the underlying coordinate grid will change.

## Examples

Some examples to help navigate the package:

```python
# Draw an NBA court
from sportypy.surfaces.basketball import NBACourt

NBACourt().draw()
```

```python
# Customize a college basketball court to replicate that of the University of
# Illinois Fighting Illini
from sportypy.surfaces.basketball import NCAACourt

NCAACourt(
    color_updates = {
        "offensive_half_court": "#e8e0d7",
        "defensive_half_court": "#e8e0d7",
        "court_apron": "#e84a27",
        "two_point_range": ["#e8e0d7", "#ffffff66"],
        "center_circle_fill": "#e8e0d7",
        "painted_area": "#e84a27",
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
).draw()
```

![sportypy-rendered Illini basketball court (sans logos/branding)](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/custom-ncaa-court.png)

## Adding Analyses and Plotting Data

In addition to just creating the baseline plots, `sportypy` has several methods to display analyses on top of the surfaces that the classes create. The syntax is meant to wrap `matplotlib` methods.

Due to the nature of the layering of the surface's features, it's recommended to use the `zorder` parameter in the range of `11` to `15` to display model outputs, and `zorder >= 20` to display individual tracking data points. This allows the features of the surface to be displayed when plotting models while also representing a birds-eye view of any action on the surface (e.g. player positions).

The first two examples use the Big Data Cup 2021 data from the 2021 NWHL season (the league became the PHF later that year).

```python
# Plot shot locations provided by the Big Data Cup

# Import packages
import matplotlib.pyplot as plt
import pandas as pd
from sportypy.surfaces.hockey import PHFRink

# Download the data
bdc = pd.read_csv(
    "https://raw.githubusercontent.com/bigdatacup/Big-Data-Cup-2021/"
    "main/hackathon_nwhl.csv"
)

# Select the Minnesota Whitecaps vs. Boston Pride game (first game in sample)
bdc = bdc.loc[
    (bdc["Home Team"] == "Minnesota Whitecaps") &
    (bdc["Away Team"] == "Boston Pride")
]

# Filter to only be shots
shots = bdc.loc[bdc["Event"].isin(["Shot", "Goal"])]

# Separate shots by team
bos_shots = shots[shots["Team"] == "Boston Pride"]
min_shots = shots[shots["Team"] == "Minnesota Whitecaps"]

# Instantiate a PHF rink, adjusting the coordinates to match the data
# (The coordinate (0, 0) is in the bottom-left of the plot)
phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

# Draw the rink on a matplotlib.Axes object
fig, ax = plt.subplots(1, 1)
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
```

![Boston Pride and Minnesota Whitecaps shots (data courtesy Big Data Cup 2021)](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/phf-shots-scatterplot.png)

The Whitecaps shots are on the left side. To add team colors and logos, see [`sdvplot`](https://sdvplot.sportsdataverse.org/).

```python
# Show passing start/end locations with an arrow plot

# Import packages
import matplotlib.pyplot as plt
import pandas as pd
from sportypy.surfaces.hockey import PHFRink

# Download the same Big Data Cup data as above
bdc = pd.read_csv(
    "https://raw.githubusercontent.com/bigdatacup/Big-Data-Cup-2021/"
    "main/hackathon_nwhl.csv"
)
bdc = bdc.loc[
    (bdc["Home Team"] == "Minnesota Whitecaps") &
    (bdc["Away Team"] == "Boston Pride")
]

# Filter to only be Boston's passes
passes = bdc.loc[
    (bdc["Team"] == "Boston Pride") &
    (bdc["Event"] == "Play")
]

# Instantiate a PHF rink, adjusting the coordinates to match the data
# (The coordinate (0, 0) is in the bottom-left of the plot)
phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

# Draw the rink on a matplotlib.Axes object
fig, ax = plt.subplots(1, 1)
phf.draw(ax = ax)

# Add the arrow plot of Boston's passes
phf.arrow(
    passes["X Coordinate"],
    passes["Y Coordinate"],
    passes["X Coordinate 2"],
    passes["Y Coordinate 2"],
    color = "#ffcb05"
)
```

![Boston Pride passes](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/phf-passes-arrowplot.png)

The next two examples load their data with [`sportsdataverse-py`](https://py.sportsdataverse.org/) (`pip install sportsdataverse`), which reads the files the SportsDataverse publishes on GitHub, and work with [`polars`](https://pola.rs/) frames, which it returns. The [cookbooks](https://sportypy.sportsdataverse.org/docs/cookbooks) take both further.

```python
# This example is adapted from the hockey_rink package's documentation, which
# can be found here: https://github.com/the-bucketless/hockey_rink#examples

# Import packages
import matplotlib.pyplot as plt
import polars as pl
import sportsdataverse.nhl as nhl
from sportypy.surfaces.hockey import NHLRink

# Load the 2019-20 NHL play-by-play (fastRhockey's, through sportsdataverse-py;
# this loader names a season by the year it ends)
pbp = nhl.load_nhl_pbp_lite(seasons = [2020])

# Keep the unblocked shots (shots on goal, misses and goals) with a location
pbp = pbp.filter(
    pl.col("event_type").is_in(["SHOT", "MISSED_SHOT", "GOAL"]) &
    pl.col("x_fixed").is_not_null() &
    pl.col("y_fixed").is_not_null()
)

# x_fixed and y_fixed are in feet on the NHL rink, with the origin at center
# ice. Force all x coordinates to be on the same side of the ice, and adjust
# the y coordinates so the shots are from the same direction
pbp = pbp.with_columns(
    x = pl.col("x_fixed").abs(),
    y = pl.col("y_fixed") * pl.col("x_fixed").sign(),
    goal = (pl.col("event_type") == "GOAL").cast(pl.Int8)
)

# Subset to only shots in the offensive zone (the blue line is 25 ft from
# center ice)
pbp = pbp.filter(pl.col("x") > 25)

# Create a matplotlib.Axes object for the test plots to lie on
fig, axs = plt.subplots(1, 3, figsize = (14, 8))

# Instantiate an NHL rink
nhl_rink = NHLRink()

# Draw a rink on each of the three matplotlib.Axes objects defined above
# and subset them to only the offensive zone
for i in range(3):
    nhl_rink.draw(ax = axs[i], display_range = "ozone")

# Add the contour plot
contour_img = nhl_rink.contourf(
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
nhl_rink.heatmap(
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
nhl_rink.hexbin(
    pbp["x"],
    pbp["y"],
    values = pbp["goal"],
    ax = axs[2],
    binsize = (8, 12),
    plot_range = "ozone",
    zorder = 25,
    alpha = 0.85
)
```

![Replicating the-bucketless' demonstration of hockey_rink package with sportypy](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/nhl-matplotlib-demo.png)

```python
# Create an NBA shot heat map. The example below uses Ayo Dosunmu's rookie
# season

# Import packages
import matplotlib.pyplot as plt
import polars as pl
import sportsdataverse.nba as nba
from sportypy.surfaces.basketball import NBACourt

# Load the 2021-22 NBA stats API shots (the shot file the SportsDataverse
# publishes, through sportsdataverse-py; this loader names a season by the
# year it starts), and keep Ayo Dosunmu's regular-season shots
shot_data = nba.load_nba_stats_shots(seasons = 2021).filter(
    (pl.col("person_id") == 1630245) &
    (pl.col("season_type_id") == "2")
)

# x_legacy and y_legacy are the stats API's LOC_X and LOC_Y: tenths of a foot,
# with the basket at the origin. Rotate them by 90 degrees to align with the
# sportypy convention, and divide by 10 to get feet
shot_data = shot_data.with_columns(
    x = -pl.col("y_legacy") / 10.0,
    y = pl.col("x_legacy") / 10.0,
    shot_made = (pl.col("shot_result") == "Made").cast(pl.Int8)
)

# Define the matplotlib instances to plot onto
fig, ax = plt.subplots(1, 1)

# Start by instantiating a court class. NBA shot data is what's used, so an
# NBA court is selected. Shifting the court by the basket's distance from
# center court puts the right-hand basket at the data's origin, and the
# "offense" display range shows only that half
nba_court = NBACourt(x_trans = -41.75)
nba_court.draw(ax = ax, display_range = "offense")
nba_court.heatmap(
    shot_data["x"],
    shot_data["y"],
    values = shot_data["shot_made"],
    ax = ax,
    alpha = 0.75,
    cmap = "hot"
)
```

![Ayo Dosunmu's rookie season heat map](https://raw.githubusercontent.com/sportsdataverse/sportypy/main/img/ayo-dosunmu-rookie-shot-chart.png)

## Follow the SportsDataverse (@SportsDataverse) on X and star this repo

[![X Follow](https://img.shields.io/twitter/follow/SportsDataverse?color=blue&label=%40SportsDataverse&logo=x&style=for-the-badge)](https://x.com/SportsDataverse)

[![GitHub stars](https://img.shields.io/github/stars/sportsdataverse/sportypy.svg?color=eee&logo=github&style=for-the-badge&label=Star%20sportypy&maxAge=2592000)](https://github.com/sportsdataverse/sportypy)

<a href="https://github.com/sportsdataverse/sportypy/stargazers">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/sportsdataverse/sportypy/star-history/star-history-dark.svg">
    <img alt="Star history of sportsdataverse/sportypy" src="https://raw.githubusercontent.com/sportsdataverse/sportypy/star-history/star-history.png" width="600">
  </picture>
</a>

## License

This package is released under the [GPL 3.0 License](https://github.com/sportsdataverse/sportypy/blob/main/LICENSE).

## Contributions

Contributions are welcome: [CONTRIBUTING.md](https://github.com/sportsdataverse/sportypy/blob/main/CONTRIBUTING.md) explains how to set up the development environment, run the checks and open a pull request.

### League Office

The package maintainers and functional engineers

- [Ross Drucker](https://github.com/rossdrucker) - `sportypy` Commissioner

### General Managers

Contribute by adding a new sport and become its general manager. Current general managers (and their sports) are:

- [Ross Drucker](https://github.com/rossdrucker) - Baseball
- [Ross Drucker](https://github.com/rossdrucker) - Basketball
- [Ross Drucker](https://github.com/rossdrucker) - Curling
- [Ross Drucker](https://github.com/rossdrucker) - Football
- [Ross Drucker](https://github.com/rossdrucker) - Hockey
- [Ross Drucker](https://github.com/rossdrucker) - Soccer
- [Ross Drucker](https://github.com/rossdrucker) - Tennis
- [Ross Drucker](https://github.com/rossdrucker) - Volleyball

Lacrosse and softball were ported from [`sportyR`](https://github.com/sportsdataverse/sportyR) and have no general manager yet: contribute to either and the job is yours.

### Coaching Staffs

Notice something for a sport that already exists, but isn't quite right? Join that sport's coaching staff!

### Scout Team

By regularly reporting issues, making very slight modifications, fixing typos, or just helping others navigate their own issues, you're able to join the Scout Team!

## Cheat sheet

A printable one-page reference for `sportypy` — the surface classes and the
arguments that shape them — is available as a free PDF. It predates the
lacrosse and softball surfaces, the PWHL rink and the Curling Canada sheet:

📄 **[Download the sportypy cheat sheet (PDF)](https://sportsdataverse.org/cheatsheets/sportypy.pdf)**

Light and dark, US Letter landscape. Every SportsDataverse package has one —
browse them all at **[sportsdataverse.org/cheatsheets](https://sportsdataverse.org/cheatsheets)**.

## Citation

To cite `sportypy` in publications, use:

```bibtex
@misc{drucker_sportypy,
  author = {Ross Drucker},
  title = {sportypy: Draw sports surfaces according to rulebook specifications.},
  url = {https://github.com/sportsdataverse/sportypy},
  version = {1.2.3},
  year = {2026}
}
```

### Acknowledgements

Much of the underlying code structure in `sportypy` was directly influenced and inspired by [The Bucketless](https://github.com/the-bucketless)'s work on the [hockey_rink](https://github.com/the-bucketless/hockey_rink) package. This package is meant to extend the capability that `hockey_rink` provides hockey analysts to analysts of a wider variety of sports

### `sportypy` Logo Artist

The `sportypy` logo was created by Lindsey Kelso. Check her out on [Instagram](http://Instagram.com/kelsokreationsbylindsey)!
