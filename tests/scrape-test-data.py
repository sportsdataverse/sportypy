"""Scrape some example data to use for tests in the tests/ directory.

This is not intended to be used by sportypy itself, rather solely for the
test suite.

@author: Ross Drucker
"""
import math
import json
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import shotchartdetail


# BDC 2021 Data ---------------------------------------------------------------

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

# Save filtered data to csv
bdc.to_csv("tests/data/bdc_2021_data.csv", index = False)

# NHL PBP Data ----------------------------------------------------------------

# Download the data
pbp = pd.read_csv(
    "https://hockey-data.harryshomer.com/pbp/nhl_pbp20192020.csv.gz",
    compression="gzip"
)

# Find all shots
pbp["goal"] = (pbp["Event"] == "GOAL").astype(int)

# Force all x coordinates to be on the same side of the ice
pbp["x"] = np.abs(pbp["xC"])

# Adjust the y coordinates so the shots are from the same direction
pbp["y"] = pbp["yC"] * np.sign(pbp["xC"])

# Subset to only shots
pbp = pbp.loc[
    (pbp.Ev_Zone == "Off") &
    ~pbp["x"].isna() &
    ~pbp["y"].isna() &
    (pbp.Event.isin(["GOAL", "SHOT", "MISS"]))
]

# Select only relevant columns to reduce data load time
pbp = pbp[["x", "y", "goal"]]

# Save filtered data to csv
pbp.to_csv("tests/data/nhl_pbp_data.csv", index = False)

# NBA Shot Chart Data ---------------------------------------------------------

# Make API request
response = shotchartdetail.ShotChartDetail(
    team_id = 0,
    player_id = 1630245,
    season_nullable = "2021-22",
    season_type_all_star = "Regular Season",
    context_measure_simple = "FGA"
)

# Extract the json content
content = json.loads(response.get_json())

# Form the data set
results = content["resultSets"][0]
headers = results["headers"]
rows = results["rowSet"]
df = pd.DataFrame(rows)
df.columns = headers

# Rotate the coordinates to align with sportypy convention
theta = 0.5 * np.pi
df["x_r"] = (df["LOC_X"] * math.cos(theta)) - (df["LOC_Y"] * math.sin(theta))
df["y_r"] = (df["LOC_X"] * math.sin(theta)) + (df["LOC_Y"] * math.cos(theta))

# Divide by 10 since NBA API gives coordinates in 1/10 of feet measurements
df["LOC_X"] = df["x_r"] / 10.0
df["LOC_Y"] = df["y_r"] / 10.0

# Drop extra columns
df.drop(labels = ["x_r", "y_r"], axis = 1)

# Create SHOT_RESULT used for heatmapping
df["SHOT_RESULT"] = np.where(df["EVENT_TYPE"] == "Made Shot", 1, 0)

# Save filtered data to csv
df.to_csv("tests/data/nba_example_shot_chart.csv", index = False)

# Tennis Event Data -----------------------------------------------------------

# Manually downloaded from this link:
# https://www.kaggle.com/robseidl/tennis-atp-tour-australian-open-final-2019

# Read in the data and rotate it to be in TV View
tennis_events = pd.read_csv("tests/data/tennis_events_raw.csv")

# Adjust the coordinates
tennis_events["hitter_x"] = tennis_events["hitter_x"] * (78.0 / 23.78)
tennis_events["hitter_x"] = tennis_events["hitter_x"] - 16.0
tennis_events["receiver_x"] = tennis_events["receiver_x"] * (78.0 / 23.78)
tennis_events["receiver_x"] = tennis_events["receiver_x"] - 16.0
tennis_events["hitter_y"] = tennis_events["hitter_y"] * (36.0 / 10.97)
tennis_events["hitter_y"] = tennis_events["hitter_y"] - 36.0
tennis_events["receiver_y"] = tennis_events["receiver_y"] * (36.0 / 10.97)
tennis_events["receiver_y"] = tennis_events["receiver_y"] - 36.0

# The x and y coordinates should be flipped
tennis_events.columns = [
    "DROPCOL",
    "rallyid",
    "frameid",
    "strokeid",
    "hitter",
    "receiver",
    "isserve",
    "serve",
    "type",
    "stroke",
    "hitter_y",
    "hitter_x",
    "receiver_y",
    "receiver_x",
    "time"
]

tennis_events = tennis_events[[
    "rallyid",
    "frameid",
    "strokeid",
    "hitter",
    "receiver",
    "isserve",
    "serve",
    "type",
    "stroke",
    "hitter_x",
    "hitter_y",
    "receiver_x",
    "receiver_y",
    "time"
]]

tennis_events.to_csv("tests/data/tennis_events.csv", index = False)

# NFL Data --------------------------------------------------------------------

# Manually downloaded from this link:
# https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/data

# Read in the data. This will be the play summaries and the tracking data
plays = pd.read_csv("tests/data/nfl_plays.csv")
tracking = pd.read_csv("tests/data/nfl_tracking.csv")

# Subset to only field goal plays
field_goal_plays = plays.loc[plays["specialTeamsPlayType"] == "Field Goal", :]
field_goal_play_ids = field_goal_plays["playId"].tolist()
fg_tracking = tracking.loc[tracking["playId"].isin(field_goal_play_ids), :]
fg_tracking = fg_tracking.loc[fg_tracking["displayName"] == "football", :]
fg_attempts = fg_tracking.loc[fg_tracking["event"] == "field_goal_attempt", :]

# Flip x coordinates on so all kicks are going left to right
fg_attempts.loc[
    fg_attempts["playDirection"] == "left",
    "x"
] = 120.0 - fg_attempts["x"]

# Join on the kick result from the plays table
field_goals = fg_attempts.join(
    field_goal_plays[["playId", "specialTeamsResult"]],
    on = "playId",
    how = "inner",
    lsuffix = "_fga",
    rsuffix = "_fgp"
)

# Force the kick result to be boolean
field_goals["kick_is_good"] = np.where(
    field_goals["specialTeamsResult"] == "Kick Attempt Good",
    1,
    0
)

# Keep only the x, y, and result columns
field_goals = field_goals[[
    "x",
    "y",
    "kick_is_good"
]]

field_goals.to_csv("tests/data/nfl_field_goals.csv", index = False)


# Curling Data ----------------------------------------------------------------
np.random.seed(2379)
shot_x = np.random.normal(0.0, 2.0, size = 100)
shot_y = np.random.normal(0.0, 3.0, size = 100)
scored = np.random.choice([1, 0], size = 100, replace = True)
curling_shot_data = pd.DataFrame({
    "x": shot_x,
    "y": shot_y + 57.0,
    "scored": scored
})

curling_shot_data.to_csv('tests/data/curling_shot_data.csv', index = False)

# Baseball Data ---------------------------------------------------------------
np.random.seed(2379)
x = np.random.normal(0.0, 20.0, size = 500)
y = np.random.normal(0.0, 10.0, size = 500)
is_hit = np.random.choice([1, 0], size = 500, replace = True)
hit_data = pd.DataFrame({
    "x": x,
    "y": y + 46.0,
    "is_hit": is_hit
})

hit_data.to_csv("tests/data/baseball_data.csv", index = False)
