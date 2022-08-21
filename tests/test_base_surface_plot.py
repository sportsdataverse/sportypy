"""Tests for the BaseSurfacePlot class of the module.

@author: Ross Drucker
"""
import os
import pytest
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from sportypy.surfaces.soccer import EPLPitch
from sportypy.surfaces.tennis import ATPCourt
from sportypy.surfaces.curling import WCFSheet
from sportypy.surfaces.football import NFLField
from sportypy.surfaces.basketball import NBACourt
from sportypy.surfaces.hockey import NHLRink, PHFRink
from sportypy.surfaces.baseball import LittleLeagueField


def test_plot():
    """Test the plot() method of the BaseSurfacePlot.

    Data is NWHL (now PHF) data from the 2021 Big Data Cup. Mimics the example
    in the-bucketless/hockey_rink and sportsdataverse/sportyR on GitHub

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the Big Data Cup (BDC) data from 2021
    bdc = pd.read_csv(os.path.join("tests", "data", "bdc_2021_data.csv"))

    # Filter to only be shots
    shots = bdc.loc[bdc["Event"].isin(["Shot", "Goal"])]

    # Separate shots by team
    bos_shots = shots[shots["Team"] == "Boston Pride"]
    min_shots = shots[shots["Team"] == "Minnesota Whitecaps"]

    # Instantiate a PHF rink, adjusting the coordinates to match the data
    # (The coordinate (0, 0) is in the bottom-left of the plot)
    phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

    # Draw the rink on a matplotlib.Axes object
    ax = phf.draw()

    # Add the plot of each team's shots
    phf.plot(bos_shots["X Coordinate"], bos_shots["Y Coordinate"])
    phf.plot(
        200.0 - min_shots["X Coordinate"],
        85.0 - min_shots["Y Coordinate"]
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_scatter():
    """Test the scatter() method of the BaseSurfacePlot.

    Data is NWHL (now PHF) data from the 2021 Big Data Cup. Mimics the example
    in the-bucketless/hockey_rink and sportsdataverse/sportyR on GitHub

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the Big Data Cup (BDC) data from 2021
    bdc = pd.read_csv(os.path.join("tests", "data", "bdc_2021_data.csv"))

    # Filter to only be shots
    shots = bdc.loc[bdc["Event"].isin(["Shot", "Goal"])]

    # Separate shots by team
    bos_shots = shots[shots["Team"] == "Boston Pride"]
    min_shots = shots[shots["Team"] == "Minnesota Whitecaps"]

    # Instantiate a PHF rink, adjusting the coordinates to match the data
    # (The coordinate (0, 0) is in the bottom-left of the plot)
    phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

    # Draw the rink on a matplotlib.Axes object
    ax = phf.draw()

    # Add the scatter plots of each team's shots
    phf.scatter(bos_shots["X Coordinate"], bos_shots["Y Coordinate"])
    phf.scatter(min_shots["X Coordinate"], min_shots["Y Coordinate"])

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_arrow():
    """Test the arrow() method of the BaseSurfacePlot.

    Data is NWHL (now PHF) data from the 2021 Big Data Cup. Mimics the example
    in the-bucketless/hockey_rink

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the Big Data Cup (BDC) data from 2021
    bdc = pd.read_csv(os.path.join("tests", "data", "bdc_2021_data.csv"))

    # Filter to only be Boston's passes
    passes = bdc.loc[
        (bdc["Team"] == "Boston Pride") &
        (bdc["Event"] == "Play")
    ]

    # Instantiate a PHF rink, adjusting the coordinates to match the data
    # (The coordinate (0, 0) is in the bottom-left of the plot)
    phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

    # Draw the rink on a matplotlib.Axes object
    ax = phf.draw()

    # Add the arrow plot of Boston's passes
    phf.arrow(
        passes["X Coordinate"],
        passes["Y Coordinate"],
        passes["X Coordinate 2"],
        passes["Y Coordinate 2"],
        color = "#e84a27"  # Orange so they stand out
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_contour_heatmap_hexbin():
    """Test the contour() method of the BaseSurfacePlot.

    Data is NHL play-by-play data from the 2019-2020 season. Mimics the example
    in the-bucketless/hockey_rink on GitHub

    This test should pass so long as the plots are correctly drawn
    """
    # Read in the NHL play-by-play data
    pbp = pd.read_csv(os.path.join("tests", "data", "nhl_pbp_data.csv"))

    # Create a matplotlib.Axes object for the test plots to lie on
    fig, axs = plt.subplots(1, 3, figsize = (14, 8))

    # Instantiate an NHL rink
    nhl = NHLRink()

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

    assert isinstance(axs[0], matplotlib.axes._subplots.Subplot)
    assert isinstance(axs[1], matplotlib.axes._subplots.Subplot)
    assert isinstance(axs[2], matplotlib.axes._subplots.Subplot)


def test_hexbin_without_values():
    """Test the hexbin() method of the works without a values argument passed.

    Data is tennis serve data from the 2019 Australian Open Final

    This test should pass so long as the plot are correctly drawn
    """
    # Read in the tennis test data
    events = pd.read_csv(os.path.join("tests", "data", "tennis_events.csv"))

    # Subset to only contain serves
    serves = events.loc[events["isserve"], :]

    # Create a matplotlib.Axes object for the test plots to lie on
    fig, ax = plt.subplots(1, figsize = (14, 8))

    # Instantiate an ATP court
    atp = ATPCourt()

    # Draw a court on the matplotlib.Axes object defined above
    ax = atp.draw(display_range = "serving")

    # Add the hexbin plot
    atp.hexbin(
        x = serves["hitter_x"],
        y = serves["hitter_y"],
        ax = ax,
        zorder = 25,
        alpha = 0.85,
        is_constrained = False
    )

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)


def test_hexbin_impute_iterable():
    """Test the hexbin() method of the works without a non-iterable binsize.

    Data is NHL play-by-play data from the 2019-2020 season. Mimics the example
    in the-bucketless/hockey_rink on GitHub

    This test should pass so long as the plot are correctly drawn
    """
    # Read in the NHL play-by-play data
    pbp = pd.read_csv(os.path.join("tests", "data", "nhl_pbp_data.csv"))

    # Create a matplotlib.Axes object for the test plots to lie on
    fig, ax = plt.subplots(1, figsize = (14, 8))

    # Instantiate an NHL rink
    nhl = NHLRink()

    # Draw a rink on the matplotlib.Axes object defined above
    nhl.draw(ax = ax, display_range = "ozone")

    # Add the hexbin plot
    nhl.hexbin(
        pbp["x"],
        pbp["y"],
        values = pbp["goal"],
        ax = ax,
        binsize = 9,
        plot_range = "ozone",
        zorder = 25,
        alpha = 0.85
    )

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)


def test_is_constrained_update_display_range():
    """Test the is_constrained parameter of BaseSurfacePlot methods.

    This test should pass so long as the plot is correctly drawn
    """
    # Create a matplotlib.Axes instance onto which the plot may be drawn
    fig, ax = plt.subplots(1, figsize = (14, 8))

    # Start by instantiating a rink class. NHL is arbitrarily selected, and the
    # rotation is selected to match a previous test
    nhl = NHLRink(rotation = 270)

    # Draw the offensive zone
    nhl.draw(display_range = "ozone", ax = ax)

    # Add a point that's outside of the boards
    nhl.scatter(
        120.0,
        0.0,
        ax = ax,
        is_constrained = False,
        update_display_range = True
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_error_invalid_x_y():
    """Test that x and y values must be the same length for plots.

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the NHL play-by-play data
    pbp = pd.read_csv(os.path.join("tests", "data", "nhl_pbp_data.csv"))

    # Create a matplotlib.Axes instance onto which the plot may be drawn
    fig, ax = plt.subplots(1, figsize = (14, 8))

    # Start by instantiating a rink class. NHL is arbitrarily selected, and the
    # rotation is selected to match a previous test
    nhl = NHLRink(rotation = 270)

    # Draw the offensive zone
    nhl.draw(display_range = "ozone", ax = ax)

    with pytest.raises(
        Exception,
        match = "x, y, and values must all be of same length"
    ):
        # Try to create a contour plot with invalid x and y values
        nhl.contourf(
            [120.0, 120.0],
            0.0,
            values = pbp["goal"],
            ax = ax,
            cmap = "bwr",
            plot_range = "ozone",
            binsize = 10,
            levels = 50,
            statistic = "mean",
            symmetrize = True
        )


def test_symmetrize():
    """Test the symmetrize parameter of BaseSurfacePlot methods.

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the NHL play-by-play data
    pbp = pd.read_csv(os.path.join("tests", "data", "nhl_pbp_data.csv"))

    # Create a matplotlib.Axes instance onto which the plot may be drawn
    fig, ax = plt.subplots(1, figsize = (14, 8))

    # Start by instantiating a rink class. NHL is arbitrarily selected, and the
    # rotation is selected to match a previous test
    nhl = NHLRink(rotation = 270)

    # Draw the offensive zone
    nhl.draw(display_range = "ozone", ax = ax)

    # Add the contour plot
    contour_img = nhl.contourf(
        pbp["x"],
        pbp["y"],
        values = pbp["goal"],
        ax = ax,
        cmap = "bwr",
        binsize = 10,
        levels = 50,
        statistic = "mean",
        symmetrize = True,
        fill = False,
        plot_xlim = None,
        plot_ylim = None,
        plot_range = None
    )

    plt.colorbar(contour_img, ax = ax, orientation = "horizontal")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_nba_shot_chart():
    """Test that an NBA shot chart works as expected through nba.heatmap().

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the shot chart data
    shot_data = pd.read_csv(
        os.path.join("tests", "data", "nba_example_shot_chart.csv")
    )

    # Create a matplotlib.Axes instance onto which the plot may be drawn
    fig, ax = plt.subplots(1)

    # Start by instantiating a court class. NBA shot data is what's used, so
    # an NBA court is selected. The rotation is to display a traditional shot
    # chart of only the offensive half
    nba = NBACourt(x_trans = -41.75)
    ax = nba.draw(display_range = "offense")
    nba.heatmap(
        shot_data["LOC_X"],
        shot_data["LOC_Y"],
        values = shot_data["SHOT_RESULT"],
        ax = ax,
        alpha = 0.75,
        cmap = "hot"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_atp_hexbin():
    """Test that an ATP shot chart works as expected through atp.scatter().

    Data is tennis serve data from the 2019 Australian Open Final

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the tennis test data
    events = pd.read_csv(os.path.join("tests", "data", "tennis_events.csv"))

    # Subset to only contain serves
    serves = events.loc[events["isserve"], :]

    # Create a matplotlib.Axes object for the test plots to lie on
    fig, ax = plt.subplots(1, figsize = (14, 8))

    # Instantiate an ATP court
    atp = ATPCourt()

    # Draw a court on the matplotlib.Axes object defined above
    atp.draw(ax = ax, display_range = "serving")

    # Add the hexbin plot
    atp.hexbin(
        x = serves["hitter_x"],
        y = serves["hitter_y"],
        ax = ax,
        alpha = 0.85,
        is_constrained = False,
        plot_range = "serving"
    )

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)


def test_nfl_contour():
    """Test that an NFL contour plot works as expected through nfl.contour().

    Data is NFL field goal data provided by the 2022 Big Data Bowl

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the NFL field goal data
    field_goals = pd.read_csv(
        os.path.join("tests", "data", "nfl_field_goals.csv")
    )

    # Create a matplotlib Axes object for the contour plot
    fig, ax = plt.subplots()
    fig.set_size_inches(50, 50)

    # Instantiate an NFL field
    nfl = NFLField()

    # Draw the field
    nfl.draw(ax = ax)

    # Add the contour plot
    contour_img = nfl.contourf(
        field_goals["x"] - 50.0,
        field_goals["y"] - 26.66665,
        values = field_goals["kick_is_good"],
        plot_range = "offense",
        ax = ax,
        binsize = 50,
        levels = 500,
        statistic = "mean"
    )

    # Correct the figure background color
    fig.patch.set_facecolor(nfl.feature_colors["plot_background"])

    # Add the colorbar to explain the plot
    plt.colorbar(contour_img, ax = ax, orientation = "horizontal")

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)


def test_epl_contour():
    """Test that an EPL heat map plot works as expected through epl.heatmap().

    Data is Cristiano Ronaldo shot data from understat.com, scraped using the R
    package worldfootballR

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the EPL shot data
    shots = pd.read_csv(
        os.path.join("tests", "data", "ronaldo_shots.csv")
    )

    # Create a matplotlib Axes object for the contour plot
    fig, ax = plt.subplots()
    fig.set_size_inches(50, 50)

    # Instantiate an English Premier League pitch
    epl = EPLPitch()

    # Draw the pitch
    epl.draw(ax = ax, display_range = "offense")

    # Add the heatmap
    epl.heatmap(
        shots["x"],
        shots["y"],
        values = shots["shot_result"],
        ax = ax,
        alpha = 0.75,
        cmap = "hot"
    )

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)


def test_curling_heatmap():
    """Test that a WCF heat map plot works as expected through wcf.heatmap().

    Data is randomly generated.

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the curling data
    shots = pd.read_csv(
        os.path.join("tests", "data", "curling_shot_data.csv")
    )

    # Create a matplotlib Axes object for the contour plot
    fig, ax = plt.subplots()
    fig.set_size_inches(50, 50)

    # Instantiate a World Curling Federation sheet
    wcf = WCFSheet()

    # Draw the sheet
    wcf.draw(ax = ax, display_range = "house")

    # Add the heatmap
    wcf.heatmap(
        shots["x"],
        shots["y"],
        values = shots["scored"],
        plot_range = "house",
        ax = ax,
        alpha = 0.75,
        cmap = "hot",
        zorder = 20
    )

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)


def test_baseball_heatmap():
    """Test that a Little League heat map plot works as expected.

    Data is randomly generated.

    This test should pass so long as the plot is correctly drawn
    """
    # Read in the baseball data
    hits = pd.read_csv(
        os.path.join("tests", "data", "baseball_data.csv")
    )

    # Create a matplotlib Axes object for the contour plot
    fig, ax = plt.subplots()
    fig.set_size_inches(50, 50)

    # Instantiate a Little League field
    little_league = LittleLeagueField()

    # Draw the infield
    little_league.draw(ax = ax, display_range = "infield")

    # Add the heatmap
    little_league.heatmap(
        hits["x"],
        hits["y"],
        values = hits["is_hit"],
        plot_range = "infield",
        ax = ax,
        alpha = 0.75,
        cmap = "hot",
        zorder = 20
    )

    # Correct the figure background color
    fig.patch.set_facecolor(little_league.feature_colors["plot_background"])

    assert isinstance(ax, matplotlib.axes._subplots.Subplot)
