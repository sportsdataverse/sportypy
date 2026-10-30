"""Hockey rinks against what sportyR's ``geom_hockey()`` draws.

tests/data/sportyr_hockey_fixture.json holds, for each league, every polygon
layer sportyR draws (see tests/data/README_hockey_fixture.md). Each sportypy
feature is paired with one sportyR polygon point for point (1e-9).

Some hockey features still differ from sportyR (they did before sportyR 2.4);
``DRIFT`` lists them, so that the rest of each rink is held to sportyR.
"""

import itertools
import json
from pathlib import Path

import numpy as np
import pytest
from matplotlib.colors import to_rgba

from sportypy.surfaces.hockey import HockeyRink
from tests.test_football_parity import _matches

FIX = json.loads((Path(__file__).parent / "data/sportyr_hockey_fixture.json").read_text())
LEAGUES = FIX["leagues"]

# Features sportypy draws differently from sportyR, all from before sportyR
# 2.4: the goal frame and its fill, the crease fill and outline, the referee's
# crease and the penalty boxes
DRIFT = {
    "GoalFrame",
    "GoalFrameFill",
    "GoalCreaseFill",
    "RefereeCrease",
    "PenaltyBoxFill",
    "PenaltyBoxOutline",
}


def _xy(feature, x_trans=0.0, y_trans=0.0):
    df = feature._translate_feature()
    return df["x"].to_numpy(float) + x_trans, df["y"].to_numpy(float) + y_trans


def _check(rink, layers, x_trans=0.0, y_trans=0.0, where=""):
    drift = set(DRIFT) | {"GoalCreaseOutline"}
    feats = [f for f in rink._features if f.visible and f._shows()]
    xy = [_xy(f, x_trans, y_trans) for f in feats]
    used, refs = set(), list(range(len(layers)))
    for k in refs:
        hit = next(
            (j for j in range(len(feats)) if j not in used and _matches(xy[j], layers[k])),
            None,
        )
        if hit is not None:
            used.add(hit)
            assert to_rgba(feats[hit].plot_kwargs["facecolor"]) == to_rgba(
                layers[k]["fill"]
            ), f"{where} {type(feats[hit]).__name__}"

    # sportyR draws each pair of faceoff lines as one polygon
    lines = [j for j, f in enumerate(feats) if type(f).__name__ == "ODZoneFaceoffLines"]
    for k, layer in enumerate(layers):
        if layer["n"] != 14:
            continue
        pair = next(
            (
                (i, j)
                for i, j in itertools.permutations(lines, 2)
                if i not in used
                and j not in used
                and _matches(
                    (np.r_[xy[i][0], xy[j][0]], np.r_[xy[i][1], xy[j][1]]), layer
                )
            ),
            None,
        )
        if pair is not None:
            used.update(pair)

    unmatched = sorted(
        {type(feats[j]).__name__ for j in range(len(feats)) if j not in used} - drift
    )
    assert unmatched == [], f"{where}: unlike sportyR: {unmatched}"


@pytest.mark.parametrize("league", list(LEAGUES))
def test_every_polygon_matches_sportyr(league):
    _check(HockeyRink(league_code=league), LEAGUES[league]["layers"], where=league)


def test_rink_in_metres_and_shifted_matches_sportyr():
    case = FIX["unit_cases"]["nhl_m_shifted"]
    rink = HockeyRink(league_code="nhl", units="m", x_trans=3.0, y_trans=-2.0)
    _check(rink, case["layers"], rink.x_trans, rink.y_trans, where="nhl_m_shifted")


def test_nhl98_crease_inner_arc_matches_sportyr():
    """The nhl98 crease outline still differs from sportyR's (sportyR's runs
    back to the crease length on each side), but its inner arc starts on the
    inner straight sides at sportyR's angle."""
    rink = HockeyRink(league_code="nhl")
    crease = next(
        f
        for f in rink._features
        if type(f).__name__ == "GoalCreaseOutline" and f.x_anchor > 0
    )
    x, y = _xy(crease)
    layer = next(
        layer
        for layer in LEAGUES["nhl"]["layers"]
        if layer["fill"] == "#c8102e" and layer["n"] == len(x) + 2
        and np.mean(layer["x"]) > 0
    )
    # sportyR's inner arc is its points 1010 to 2009; sportypy's, 1009 to 2008
    idx = np.asarray(layer["idx"])
    on_arc = (idx >= 1010) & (idx <= 2009)
    assert on_arc.sum() > 30
    assert np.allclose(x[idx[on_arc] - 1], np.asarray(layer["x"])[on_arc], atol=1e-9)
    assert np.allclose(y[idx[on_arc] - 1], np.asarray(layer["y"])[on_arc], atol=1e-9)
