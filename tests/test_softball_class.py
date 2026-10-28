"""Tests for the sportyR-ported NCAA softball field.

tests/data/sportyr_softball_fixture.json holds sportyR's own coordinates
(see tests/data/README_softball_fixture.md for provenance).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
import pytest

import sportypy.surfaces as surfaces
import sportypy._feature_classes.softball as sf
from sportypy.surfaces.softball import DEFAULT_COLORS, NCAASoftballField, SoftballField

FIX = json.loads((Path(__file__).parent / "data/sportyr_softball_fixture.json").read_text())
FEAT, ANCH = FIX["features"], FIX["anchors"]
COLOR_KEYS = ["plot_background", "infield_dirt", "base", "pitchers_plate", "batters_box",
              "catchers_box", "foul_line", "running_lane", "pitchers_circle",
              "pitchers_lane", "coaches_box"]
TOL = 1e-9


def _of(field, cls):
    return [f for f in field._features if isinstance(f, cls)]


def _xy(df):
    return np.column_stack([df["x"].to_numpy(float), df["y"].to_numpy(float)])


def _fx(name):
    return np.column_stack([np.asarray(FEAT[name]["x"], float), np.asarray(FEAT[name]["y"], float)])


def _anchored(name, anchor=(0.0, 0.0)):
    return _fx(name) + np.asarray(anchor)


def test_params_come_from_sportyr():
    assert NCAASoftballField().field_params == FIX["params"]


def test_features_match_sportyr_to_1e9():
    field = NCAASoftballField()
    got = {}
    for cls, name in [(sf.HomePlate, "home_plate"), (sf.PitchersPlate, "pitchers_plate"),
                      (sf.CatchersBox, "catchers_box"), (sf.RunningLane, "running_lane"),
                      (sf.PitchersLane, "pitchers_lane"), (sf.CoachesBox, "coaches_box")]:
        feats = [f for f in _of(field, cls) if f.x_reflection == 1]
        assert len(feats) == 1, name
        got[name] = _xy(feats[0]._translate_feature())
    assert np.allclose(got["home_plate"], _anchored("home_plate"), atol=TOL)
    assert np.allclose(got["pitchers_plate"], _anchored("pitchers_plate", ANCH["pitchers_plate"]), atol=TOL)
    assert np.allclose(got["catchers_box"], _anchored("catchers_box"), atol=TOL)
    assert np.allclose(got["running_lane"], _anchored("running_lane"), atol=TOL)
    assert np.allclose(got["pitchers_lane"], _anchored("pitchers_lane", ANCH["pitchers_lane"]), atol=TOL)
    assert np.allclose(got["coaches_box"], _anchored("coaches_box"), atol=TOL)

    # the mirrored copies are exact x-reflections
    for cls in (sf.PitchersLane, sf.CoachesBox, sf.BattersBox):
        a, b = sorted(_of(field, cls), key=lambda f: f.x_reflection)[::-1]
        assert np.allclose(_xy(a._translate_feature()) * [-1, 1], _xy(b._translate_feature()), atol=TOL)


def test_bases_boxes_and_lines_match_sportyr():
    field = NCAASoftballField()
    bases = sorted(_of(field, sf.Base), key=lambda f: -f.x_anchor)
    first, second, third = bases
    assert np.allclose(_xy(first._translate_feature()), _anchored("first_base", ANCH["first_base"]), atol=TOL)
    assert np.allclose(_xy(third._translate_feature()), _anchored("third_base", ANCH["third_base"]), atol=TOL)
    assert second.y_anchor == pytest.approx(ANCH["second_base"][1], abs=TOL)

    box = [f for f in _of(field, sf.BattersBox) if f.x_reflection == 1][0]
    assert box.x_anchor == pytest.approx(ANCH["batters_box"][0], abs=TOL)
    assert np.allclose(_xy(box._get_centered_feature()), _fx("batters_box"), atol=TOL)

    lines = {f.is_line_1b: _xy(f._translate_feature()) for f in _of(field, sf.FoulLine)}
    assert np.allclose(lines[True], _fx("first_base_line"), atol=TOL)
    assert np.allclose(lines[False], _fx("third_base_line"), atol=TOL)


def _rings(df):
    xy = _xy(df)
    n = len(xy) // 2
    return xy[:n], xy[n:]


def _sweep(ring, c=(0.0, 0.0)):
    ang = np.unwrap(np.arctan2(ring[:, 1] - c[1], ring[:, 0] - c[0]))
    return ang[-1] - ang[0], np.sign(np.diff(ang))


def test_pitchers_circle_matches_sportyr():
    # compare endpoints, radius, direction and sweep of each ring
    circle = _of(NCAASoftballField(), sf.PitchersCircle)[0]
    assert circle.y_anchor == pytest.approx(ANCH["pitchers_circle"][1], abs=TOL)
    got, ref = _rings(circle._get_centered_feature()), _rings(pd.DataFrame(FEAT["pitchers_circle"]))
    for g, r in zip(got, ref):
        assert np.allclose(g[[0, -1]], r[[0, -1]], atol=TOL)
        assert np.allclose(np.hypot(*g.T), np.hypot(*r[0]), atol=TOL)
        (gs, gd), (rs, rd) = _sweep(g), _sweep(r)
        assert gs == pytest.approx(rs, abs=1e-6)
        assert set(gd) == set(rd)
    assert abs(_sweep(got[0])[0]) == pytest.approx(2 * np.pi, abs=1e-6)
    assert _sweep(got[0])[0] * _sweep(got[1])[0] < 0  # outer and inner run opposite ways


def test_infield_dirt_matches_sportyr_arcs():
    dirt = _of(NCAASoftballField(), sf.InfieldDirt)[0]
    got, ref = _rings(dirt._get_centered_feature()), _rings(pd.DataFrame(FEAT["infield_dirt"]))
    for g, r, c in zip(got, ref, [(0.0, FIX["params"]["pitchers_plate_front_to_home_plate"]), (0.0, 0.0)]):
        assert np.allclose(g[[0, -1]], r[[0, -1]], atol=TOL)
        r_ref = np.hypot(r[:, 0] - c[0], r[:, 1] - c[1])
        assert np.allclose(r_ref, r_ref[0], atol=TOL)
        assert np.allclose(np.hypot(g[:, 0] - c[0], g[:, 1] - c[1]), r_ref[0], atol=TOL)
        (gs, gd), (rs, rd) = _sweep(g, c), _sweep(r, c)
        assert gs == pytest.approx(rs, abs=1e-6) and set(gd) == set(rd)


@pytest.mark.parametrize("key", COLOR_KEYS)
def test_every_color_key_reaches_the_drawing(key):
    field = NCAASoftballField(color_updates={key: "#123456"})
    assert field.feature_colors[key] == "#123456"
    ax = field.draw()
    want = to_rgba("#123456")
    if key == "plot_background":
        assert to_rgba(ax.figure.get_facecolor()) == want
    else:
        assert any(np.allclose(p.get_facecolor(), want) for p in ax.patches), key
    plt.close("all")


def test_default_colors_match_sportyr():
    assert set(NCAASoftballField().feature_colors) == set(COLOR_KEYS)
    assert NCAASoftballField().feature_colors["infield_dirt"] == "#9b7653"


def test_reset_colors_restores_softball_defaults():
    field = NCAASoftballField(color_updates={"base": "#123456"})
    field.reset_colors()
    assert field.feature_colors == DEFAULT_COLORS
    assert "infield_grass" not in field.feature_colors and "pitchers_mound" not in field.feature_colors
    assert field.field_params == FIX["params"]


def test_draw_full_and_infield_limits_match_sportyr():
    p = FIX["params"]
    ax = NCAASoftballField().draw()
    full = ax.get_xlim(), ax.get_ylim()
    plt.close("all")
    ax = NCAASoftballField().draw(display_range="infield")
    inf = ax.get_xlim(), ax.get_ylim()
    plt.close("all")
    half = p["right_field_distance"] * np.cos(np.pi / 4)
    assert full[0] == pytest.approx((-134.3503, 134.3503), abs=1e-4)
    assert full[0] == pytest.approx((-half, half), abs=1e-9)
    assert full[1] == pytest.approx((-(p["backstop_radius"] + 5), p["center_field_distance"] + 5), abs=1e-9)
    arc, plate = p["infield_arc_radius"], p["pitchers_plate_front_to_home_plate"]
    assert inf[0] == pytest.approx((-(arc + 5), arc + 5), abs=1e-9)
    assert inf[1] == pytest.approx((-(p["home_plate_circle_radius"] + 5), plate + arc + 5), abs=1e-9)


def test_export_does_not_rebind_package_names():
    assert surfaces.NCAASoftballField is NCAASoftballField
    assert surfaces.SoftballField.__module__ == "sportypy.surfaces.softball"
    assert surfaces.NCAAField.__module__ == "sportypy.surfaces.football"  # pre-existing winner
    assert surfaces.NCAACourt.__module__ == "sportypy.surfaces.tennis"
    assert issubclass(NCAASoftballField, SoftballField)
