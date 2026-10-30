"""Hockey rinks against what sportyR's ``geom_hockey()`` draws.

tests/data/sportyr_hockey_fixture.json holds, for each league, every polygon
layer sportyR draws (see tests/data/README_hockey_fixture.md). Each sportypy
feature is paired with one sportyR polygon: the same point count, the same
coordinate sums and moments, and the same sampled points (every 25th and the
last), to 1e-9. Every feature and every polygon must find its match.
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


def _xy(feature, x_trans=0.0, y_trans=0.0):
    df = feature._translate_feature()
    return df["x"].to_numpy(float) + x_trans, df["y"].to_numpy(float) + y_trans


def _check(rink, layers, x_trans=0.0, y_trans=0.0, where=""):
    feats = [f for f in rink._features if f.visible and f._shows()]
    xy = [_xy(f, x_trans, y_trans) for f in feats]
    used, matched = set(), set()
    for k in range(len(layers)):
        hit = next(
            (j for j in range(len(feats)) if j not in used and _matches(xy[j], layers[k])),
            None,
        )
        if hit is not None:
            used.add(hit)
            matched.add(k)
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
            matched.add(k)
            for j in pair:
                assert to_rgba(feats[j].plot_kwargs["facecolor"]) == to_rgba(
                    layer["fill"]
                ), f"{where} {type(feats[j]).__name__}"

    unmatched = sorted(
        {type(feats[j]).__name__ for j in range(len(feats)) if j not in used}
    )
    assert unmatched == [], f"{where}: unlike sportyR: {unmatched}"

    # A shape that is its own mirror image (centred on the rink's centre line)
    # may be drawn twice by sportyR and once by sportypy (the centre faceoff
    # spot); sportyR's second copy matches the mirror of sportypy's one. A
    # feature drawn at both ends of the rink is not its own mirror image, so
    # each end must match on its own
    def mirror(j):
        return 2 * x_trans - xy[j][0], xy[j][1]

    # (centred to within 0.1% of its width: a sampled circle's extremes are
    # not exactly opposite)
    centred = {
        j
        for j in range(len(feats))
        if abs((xy[j][0].min() + xy[j][0].max()) / 2 - x_trans)
        <= 1e-3 * np.ptp(xy[j][0])
    }
    for k in range(len(layers)):
        if k not in matched and any(
            _matches(mirror(j), layers[k]) for j in used & centred
        ):
            matched.add(k)

    left = sorted(k for k in range(len(layers)) if k not in matched)
    assert left == [], f"{where}: sportyR polygons with no match: {left}"


@pytest.mark.parametrize("league", list(LEAGUES))
def test_every_polygon_matches_sportyr(league):
    _check(HockeyRink(league_code=league), LEAGUES[league]["layers"], where=league)


def test_rink_in_metres_and_shifted_matches_sportyr():
    case = FIX["unit_cases"]["nhl_m_shifted"]
    rink = HockeyRink(league_code="nhl", units="m", x_trans=3.0, y_trans=-2.0)
    _check(rink, case["layers"], rink.x_trans, rink.y_trans, where="nhl_m_shifted")


@pytest.mark.parametrize("cls_name", ["GoaltendersRestrictedArea", "CenterFaceoffCircle"])
def test_one_end_of_a_two_ended_feature_missing_fails(cls_name):
    """Dropping one copy of a feature drawn twice (one at each end, or each
    half of the centre circle) leaves a sportyR polygon with no match."""
    rink = HockeyRink(league_code="nhl")
    left = next(
        f for f in rink._features if type(f).__name__ == cls_name and f.x_reflection == -1
    )
    rink._features.remove(left)
    with pytest.raises(AssertionError, match="no match"):
        _check(rink, LEAGUES["nhl"]["layers"], where="nhl")
