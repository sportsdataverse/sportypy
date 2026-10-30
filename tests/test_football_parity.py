"""Football fields against sportyR's own ``geom_football()``.

tests/data/sportyr_football_fixture.json holds, for each league, every layer
sportyR draws (see tests/data/README_football_fixture.md). Every polygon must
match one sportypy feature point for point (1e-9) with the same fill colour,
and every drawn sportypy polygon must be one of sportyR's.

sportypy draws its features in its own z-order, so polygons are paired by
their coordinates rather than by drawing order.
"""

import json
from pathlib import Path

import numpy as np
import pytest
from matplotlib.colors import to_rgba

import sportypy.surfaces.football as football

FIX = json.loads(
    (Path(__file__).parent / "data/sportyr_football_fixture.json").read_text()
)
LEAGUES = FIX["leagues"]
FIELDS = {
    "ncaa": lambda: football.NCAAField(),
    "nfl": lambda: football.NFLField(),
    "nfhs11": lambda: football.NFHSField(n_players=11),
    "nfhs9": lambda: football.NFHSField(n_players=9),
    "nfhs8": lambda: football.NFHSField(n_players=8),
    "nfhs6": lambda: football.NFHSField(n_players=6),
    "cfl": lambda: football.CFLField(),
}
TOL = 1e-9

# Zero-width features sportyR still draws, as a hairline in their own outline
# colour (sportyR outlines every football feature), but sportypy, which draws
# no outlines, does not. Each lies along the outer edge of a white sideline (or,
# for the field border, over the green apron), so the plots look the same
_HAIRLINES = ["FieldBorder"] * 2
HAIRLINES = {
    **{f"nfhs{n}": _HAIRLINES for n in (11, 9, 8, 6)},
    "cfl": sorted(
        _HAIRLINES
        + ["RestrictedArea", "CoachingBox", "TeamBenchArea", "TeamBenchAreaOutline"] * 2
    ),
}


def _hairline(feat, ref):
    """sportyR draws ``ref`` only as its outline, which sportypy leaves out."""
    colour = ref.get("colour")
    return (
        not feat._shows()
        and colour is not None
        and to_rgba(colour)[3] == 1
    )


def _split(layers):
    """sportyR's polygons, less each yard number's text box.

    sportyR draws every yard number as a fully transparent box followed by a
    text layer; sportypy draws the numbers as text only, with no box.
    """
    boxes = {i for i, l in enumerate(layers[1:]) if l["geom"] != "GeomPolygon"}
    polys = [
        l for i, l in enumerate(layers) if l["geom"] == "GeomPolygon" and i not in boxes
    ]
    number_boxes = [layers[i] for i in sorted(boxes)]
    return polys, number_boxes


def _matches(feat_xy, ref):
    x, y = feat_xy
    if len(x) != ref["n"]:
        return False
    moments = [x.sum(), y.sum(), (x * x).sum(), (y * y).sum(), (x * y).sum()]
    if not np.allclose(moments, ref["moments"], rtol=1e-10, atol=TOL):
        return False
    idx = np.asarray(ref["idx"], dtype=int)
    return (
        np.abs(x[idx] - np.asarray(ref["x"])).max(initial=0) < TOL
        and np.abs(y[idx] - np.asarray(ref["y"])).max(initial=0) < TOL
    )


@pytest.mark.parametrize("league", list(LEAGUES))
def test_params_match_sportyr(league):
    assert FIELDS[league]().field_params == LEAGUES[league]["params"]


@pytest.mark.parametrize("league", list(LEAGUES))
def test_every_polygon_matches_sportyr(league):
    field = FIELDS[league]()
    feats = [f for f in field._features if f.visible]
    xy = []
    for f in feats:
        df = f._translate_feature()
        xy.append((df["x"].to_numpy(float), df["y"].to_numpy(float)))

    polys, _ = _split(LEAGUES[league]["layers"])
    used, hairlines = set(), []
    for k, ref in enumerate(polys):
        hit = next(
            (j for j in range(len(feats)) if j not in used and _matches(xy[j], ref)),
            None,
        )
        assert hit is not None, f"{league}: sportyR polygon {k} has no match"
        used.add(hit)
        feat = feats[hit]
        where = f"{league} polygon {k} ({type(feat).__name__})"
        assert to_rgba(feat.plot_kwargs["facecolor"]) == to_rgba(ref["fill"]), where
        if _hairline(feat, ref):
            hairlines.append(type(feat).__name__)
    assert sorted(hairlines) == HAIRLINES.get(league, []), league
    # sportyR leaves out a feature with no area and no visible outline
    extra = [
        type(feats[j]).__name__
        for j in range(len(feats))
        if j not in used and feats[j]._shows()
    ]
    assert extra == [], f"{league}: drawn by sportypy only: {extra}"


@pytest.mark.parametrize("league", list(LEAGUES))
def test_yard_number_boxes_are_transparent(league):
    """The only sportyR polygons sportypy does not draw: the yard numbers'
    boxes, which are fully transparent with no outline."""
    _, boxes = _split(LEAGUES[league]["layers"])
    assert boxes
    for box in boxes:
        assert to_rgba(box["fill"])[3] == 0
        assert not box["colour"]


RANGES = ["full", "in_bounds_only", "offense", "defense", "redzone", "dredzone"]


@pytest.mark.parametrize("league", list(LEAGUES))
@pytest.mark.parametrize("display_range", RANGES)
def test_display_limits_match_sportyr(league, display_range):
    """The display limits of each range equal geom_football()'s."""
    ref = LEAGUES[league]["range_limits"][display_range]
    xlim, ylim = FIELDS[league]()._get_plot_range_limits(display_range)
    assert np.allclose(xlim, ref["x"], rtol=0, atol=TOL), (xlim, ref["x"])
    assert np.allclose(ylim, ref["y"], rtol=0, atol=TOL), (ylim, ref["y"])
