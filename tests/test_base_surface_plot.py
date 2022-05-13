"""Tests for the BaseSurfacePlot class of the module.

@author: Ross Drucker
"""
import warnings
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sportypy.surface_classes.hockey import NHLRink, PHFRink

# Filter warnings
warnings.filterwarnings('ignore')


def test_scatter():
    """Test the scatter() method of the BaseSurfacePlot.

    Data is NWHL (now PHF) data from the 2021 Big Data Cup. Mimics the example
    in the-bucketless/hockey_rink and sportsdataverse/sportyR on GitHub

    This test should pass so long as the plot is correctly drawn
    """
    # Download the Big Data Cup (BDC) data from 2021
    bdc = pd.read_csv(
        'https://raw.githubusercontent.com/bigdatacup/Big-Data-Cup-2021/'
        'main/hackathon_nwhl.csv'
    )

    # Find a particular game. This test will use the Minnesota Whitecaps vs.
    # Boston Pride game
    game_df = bdc.loc[
        (bdc['Home Team'] == 'Minnesota Whitecaps') &
        (bdc['Away Team'] == 'Boston Pride')
    ]

    # Filter to only be shots
    shots = game_df.loc[game_df['Event'].isin(['Shot', 'Goal'])]

    # Separate shots by team
    bos_shots = shots[shots['Team'] == 'Boston Pride']
    min_shots = shots[shots['Team'] == 'Minnesota Whitecaps']

    # Instantiate a PHF rink, adjusting the coordinates to match the data
    # (The coordinate (0, 0) is in the bottom-left of the plot)
    phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

    # Draw the rink on a matplotlib.Axes object
    ax = phf.draw()

    # Add the scatter plots of each team's shots
    phf.scatter(bos_shots['X Coordinate'], bos_shots['Y Coordinate'])
    phf.scatter(min_shots['X Coordinate'], min_shots['Y Coordinate'])

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_arrow():
    """Test the arrow() method of the BaseSurfacePlot.

    Data is NWHL (now PHF) data from the 2021 Big Data Cup. Mimics the example
    in the-bucketless/hockey_rink

    This test should pass so long as the plot is correctly drawn
    """
    # Download the Big Data Cup (BDC) data from 2021
    bdc = pd.read_csv(
        'https://raw.githubusercontent.com/bigdatacup/Big-Data-Cup-2021/'
        'main/hackathon_nwhl.csv'
    )

    # Find a particular game. This test will use the Minnesota Whitecaps vs.
    # Boston Pride game
    game_df = bdc.loc[
        (bdc['Home Team'] == 'Minnesota Whitecaps') &
        (bdc['Away Team'] == 'Boston Pride')
    ]

    # Filter to only be Boston's passes
    passes = game_df.loc[
        (game_df['Team'] == 'Boston Pride') &
        (game_df['Event'] == 'Play')
    ]

    # Instantiate a PHF rink, adjusting the coordinates to match the data
    # (The coordinate (0, 0) is in the bottom-left of the plot)
    phf = PHFRink(x_trans = 100.0, y_trans = 42.5)

    # Draw the rink on a matplotlib.Axes object
    ax = phf.draw()

    # Add the arrow plot of Boston's passes
    phf.arrow(
        passes['X Coordinate'],
        passes['Y Coordinate'],
        passes['X Coordinate 2'],
        passes['Y Coordinate 2'],
        color = '#e84a27' # Orange so they stand out
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_contour():
    """Test the contour() method of the BaseSurfacePlot.

    Data is NHL play-by-play data from the 2019-2020 season. Mimics the example
    in the-bucketless/hockey_rink on GitHub

    This test should pass so long as the plots are correctly drawn
    """
    # Download the NHL play-by-play data
    pbp = pd.read_csv(
        'https://hockey-data.harryshomer.com/pbp/nhl_pbp20192020.csv.gz',
        compression = "gzip"
    )

    # Find all shots
    pbp['goal'] = (pbp['Event'] == "GOAL").astype(int)

    # Force all x coordinates to be on the same side of the ice
    pbp['x'] = np.abs(pbp['xC'])

    # Adjust the y coordinates so the shots are from the same direction
    pbp['y'] = pbp['yC'] * np.sign(pbp['xC'])

    # Subset to only shots
    shots = pbp.loc[
        (pbp.Ev_Zone == 'Off') &
        ~pbp['x'].isna() &
        ~pbp['y'].isna() &
        (pbp.Event.isin(["GOAL", "SHOT", "MISS"]))
    ]

    # Create a matplotlib.Axes object for the test plots to lie on
    fig, axs = plt.subplots(1, 3, figsize = (14, 8))

    # Instantiate an NHL rink
    nhl = NHLRink()

    # Draw a rink on each of the three matplotlib.Axes objects defined above
    # and subset them to only the offensive zone
    for i in range(3):
        nhl.draw(ax = axs[i], display_range = 'ozone')

    # Add the contour plot
    contour_img = nhl.contourf(
        shots['x'],
        shots['y'],
        values = shots['goal'],
        ax = axs[0],
        cmap = 'bwr',
        plot_range = 'ozone',
        binsize = 10,
        levels = 50,
        statistic = 'mean'
    )

    # Add a colorbar legend to the bottom to make the metrics easier to read
    plt.colorbar(contour_img, ax = axs[0], orientation = 'horizontal')

    # Add the heatmap plot
    nhl.heatmap(
        shots['x'],
        shots['y'],
        values = shots['goal'],
        ax = axs[1],
        cmap = 'magma',
        plot_xlim = (25, 89), # offensive-side blue line to the goal line
        statistic = 'mean',
        vmax = 0.2,
        binsize = 3
    )

    # Add the hexbin plot
    nhl.hexbin(
        shots['x'],
        shots['y'],
        values = shots['goal'],
        ax = axs[2],
        binsize = (8, 12),
        plot_range = 'ozone',
        zorder = 25,
        alpha = 0.85
    )

    assert isinstance(axs[0], matplotlib.axes._subplots.Subplot)
    assert isinstance(axs[1], matplotlib.axes._subplots.Subplot)
    assert isinstance(axs[2], matplotlib.axes._subplots.Subplot)
