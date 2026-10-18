"""Surfaces drawn in other units and shifted, against sportyR (#74, #76).

sportyR draws a surface in its rule book's units, scales the finished plot to
the requested units, and moves the surface by ``x_trans`` / ``y_trans`` (in the
requested units). sportypy builds the surface in the requested units and
leaves it at the origin, shifting plotted data by ``-x_trans`` / ``-y_trans``
instead. The two agree when every sportyR polygon equals a sportypy polygon
moved by the translation. The cases come from the ``unit_cases`` of the
lacrosse, football and volleyball fixtures (sportyR 972da8c).
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.colors import to_rgba

import sportypy.surfaces.football as football
import sportypy.surfaces.lacrosse as lacrosse
import sportypy.surfaces.volleyball as volleyball
from tests.test_football_parity import TOL, _matches

DATA = Path(__file__).parent / "data"
FIX = {
    sport: json.loads((DATA / f"sportyr_{sport}_fixture.json").read_text())[
        "unit_cases"
    ]
    for sport in ("lacrosse", "football", "volleyball")
}
MAKE = {
    ("lacrosse", "nll_m_shifted"): lambda: lacrosse.NLLField(
        units="m", x_trans=3.0, y_trans=-2.0
    ),
    ("lacrosse", "ncaaw_ft"): lambda: lacrosse.NCAAWLacrosseField(units="ft"),
    ("football", "nfl_shifted"): lambda: football.NFLField(x_trans=10.0, y_trans=-5.0),
    ("football", "nfl_m_shifted"): lambda: football.NFLField(
        units="m", x_trans=3.0, y_trans=-2.0
    ),
    ("volleyball", "fivb_in_shifted"): lambda: volleyball.FIVBCourt(
        units="in", x_trans=12.0, y_trans=-6.0
    ),
}
CASES = list(MAKE)


def _shifted_polygons(surface):
    """sportypy's visible polygons, moved by the surface's translation."""
    feats = [f for f in surface._features if f.visible]
    out = []
    for f in feats:
        df = f._translate_feature()
        out.append(
            (
                df["x"].to_numpy(float) + surface.x_trans,
                df["y"].to_numpy(float) + surface.y_trans,
            )
        )
    return feats, out


@pytest.mark.parametrize("sport, case", CASES, ids=[f"{s}-{c}" for s, c in CASES])
def test_every_polygon_matches_sportyr(sport, case):
    ref = FIX[sport][case]
    surface = MAKE[(sport, case)]()
    feats, xy = _shifted_polygons(surface)
    layers = ref["layers"]
    # sportyR's yard-number boxes (transparent; sportypy draws text only)
    boxes = {i for i, l in enumerate(layers[1:]) if l.get("geom", "GeomPolygon") != "GeomPolygon"}
    polys = [
        l for i, l in enumerate(layers) if l.get("geom", "GeomPolygon") == "GeomPolygon" and i not in boxes
    ]
    used = set()
    for k, layer in enumerate(polys):
        hit = next(
            (j for j in range(len(feats)) if j not in used and _matches(xy[j], layer)),
            None,
        )
        assert hit is not None, f"{case}: sportyR polygon {k} has no match"
        used.add(hit)
        assert to_rgba(feats[hit].plot_kwargs["facecolor"]) == to_rgba(layer["fill"]), (
            case,
            k,
        )
    extra = [type(feats[j]).__name__ for j in range(len(feats)) if j not in used]
    assert extra == [], f"{case}: drawn by sportypy only: {extra}"


@pytest.mark.parametrize("sport, case", CASES, ids=[f"{s}-{c}" for s, c in CASES])
def test_display_limits_match_sportyr(sport, case):
    ref = FIX[sport][case]["limits"]
    surface = MAKE[(sport, case)]()
    xlim, ylim = surface._get_plot_range_limits("full")
    assert np.allclose(np.add(xlim, surface.x_trans), ref["x"], atol=TOL)
    assert np.allclose(np.add(ylim, surface.y_trans), ref["y"], atol=TOL)


@pytest.mark.parametrize("case", ["nfl_shifted", "nfl_m_shifted"])
def test_yard_numbers_follow_units_and_translation(case):
    """sportyR #76: the yard numbers' boxes are translated once and scaled with
    the units. sportypy's numbers sit at the boxes' x centres (moved by the
    translation). In y, sportyR's box is 1.5 number heights tall from the
    numbers' bottom edge, so its centre is a quarter number height further
    from the sideline than sportypy's text centre (bottom of the numbers plus
    half their height). sportypy also nudges a top "1" right of its line 0.75
    yd towards the line in the Clarendon font (the glyph is off-centre), in
    the field's units."""
    boxes = [
        l["box"] for l in FIX["football"][case]["layers"] if l.get("geom", "GeomPolygon") != "GeomPolygon"
    ]
    surface = MAKE[("football", case)]()
    ax = surface.draw()
    texts = [(t.get_position(), t.get_text()) for t in ax.texts]
    plt.close("all")
    assert len(texts) == len(boxes)
    quarter = surface.field_params["number_height"] / 4.0
    nudge = surface._yd(0.75)
    nudged = 0
    for ((x, y), label), box in zip(texts, boxes):
        cx = (box["x_min"] + box["x_max"]) / 2.0
        cy = (box["y_min"] + box["y_max"]) / 2.0
        if label == "1" and y > 0 and abs(x + surface.x_trans - (cx - nudge)) < 1e-9:
            nudged += 1
        else:
            assert x + surface.x_trans == pytest.approx(cx, abs=1e-9)
        # bottom numbers: sportyR's centre is above sportypy's; top: below
        want = y + surface.y_trans + (quarter if y < 0 else -quarter)
        assert want == pytest.approx(cy, abs=1e-9)
    assert nudged == 2  # the top "1"s drawn right of their yard line
