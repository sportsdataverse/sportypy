"""Volleyball courts against sportyR's own ``geom_volleyball()``.

tests/data/sportyr_volleyball_fixture.json holds, for each league, every layer
sportyR draws (see tests/data/README_volleyball_fixture.md). Polygons are
paired by coordinates (1e-9) as in test_football_parity.py.
"""

import json
from pathlib import Path

import pytest
from matplotlib.colors import to_rgba
from tests.test_football_parity import _hairline, _matches

import sportypy.surfaces.volleyball as volleyball

FIX = json.loads((Path(__file__).parent / "data/sportyr_volleyball_fixture.json").read_text())
LEAGUES = FIX["leagues"]
COURTS = {
    "fivb": volleyball.FIVBCourt,
    "usa volleyball": volleyball.USAVolleyballCourt,
    "ncaa": volleyball.NCAACourt,
}


@pytest.mark.parametrize("league", list(LEAGUES))
def test_params_match_sportyr(league):
    assert COURTS[league]().court_params == LEAGUES[league]["params"]


@pytest.mark.parametrize("league", list(LEAGUES))
def test_every_polygon_matches_sportyr(league):
    feats = [f for f in COURTS[league]()._features if f.visible]
    xy = []
    for f in feats:
        df = f._translate_feature()
        xy.append((df["x"].to_numpy(float), df["y"].to_numpy(float)))
    polys = [l for l in LEAGUES[league]["layers"] if l["geom"] == "GeomPolygon"]
    assert len(polys) == len(LEAGUES[league]["layers"])  # no text layers
    used = set()
    for k, ref in enumerate(polys):
        hit = next(
            (j for j in range(len(feats)) if j not in used and _matches(xy[j], ref)),
            None,
        )
        assert hit is not None, f"{league}: sportyR polygon {k} has no match"
        used.add(hit)
        feat = feats[hit]
        assert to_rgba(feat.plot_kwargs["facecolor"]) == to_rgba(ref["fill"]), (
            f"{league} polygon {k} ({type(feat).__name__})"
        )
        # no feature sportyR draws only as an outline (see test_football_parity)
        assert not _hairline(feat, ref), f"{league} polygon {k}"
    # sportyR leaves out a feature with no area and no visible outline
    extra = [
        type(feats[j]).__name__
        for j in range(len(feats))
        if j not in used and feats[j]._shows()
    ]
    assert extra == [], f"{league}: drawn by sportypy only: {extra}"
