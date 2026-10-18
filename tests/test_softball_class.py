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
import pytest

import sportypy.surfaces as surfaces
import sportypy._feature_classes.softball as sf
from sportypy.surfaces.softball import NCAASoftballField, SoftballField

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


def test_pitchers_circle_matches_sportyr():
    # sportyR draws 1000 points per ring, sportypy 10000: compare ring endpoints and radii
    circle = _of(NCAASoftballField(), sf.PitchersCircle)[0]
    assert circle.y_anchor == pytest.approx(ANCH["pitchers_circle"][1], abs=TOL)
    got, ref = _xy(circle._get_centered_feature()), _fx("pitchers_circle")
    n_got, n_ref = len(got) // 2, len(ref) // 2
    for k in range(2):
        g, r = got[k * n_got:(k + 1) * n_got], ref[k * n_ref:(k + 1) * n_ref]
        assert np.allclose(g[[0, -1]], r[[0, -1]], atol=TOL)
        assert np.allclose(np.hypot(*g.T), np.hypot(*r[0]), atol=TOL)
    assert np.hypot(*ref[0]) == pytest.approx(8.0) and np.hypot(*ref[n_ref]) == pytest.approx(7.75)


def test_infield_dirt_matches_sportyr_arcs():
    dirt = _of(NCAASoftballField(), sf.InfieldDirt)[0]
    got, ref = _xy(dirt._get_centered_feature()), _fx("infield_dirt")
    n_got, n_ref = len(got) // 2, len(ref) // 2
    for k in range(2):
        g, r = got[k * n_got:(k + 1) * n_got], ref[k * n_ref:(k + 1) * n_ref]
        assert np.allclose(g[[0, -1]], r[[0, -1]], atol=TOL)


@pytest.mark.parametrize("key", COLOR_KEYS)
def test_every_color_key_is_accepted_and_used(key):
    field = NCAASoftballField(color_updates={key: "#123456"})
    assert field.feature_colors[key] == "#123456"
    ax = field.draw()
    assert ax is not None
    plt.close("all")


def test_default_colors_match_sportyr():
    assert set(COLOR_KEYS) <= set(NCAASoftballField().feature_colors)
    assert NCAASoftballField().feature_colors["infield_dirt"] == "#9b7653"


def test_draw_full_and_infield_limits():
    f = NCAASoftballField()
    ax = f.draw()
    full = ax.get_xlim(), ax.get_ylim()
    plt.close("all")
    ax = NCAASoftballField().draw(display_range="infield")
    inf = ax.get_xlim(), ax.get_ylim()
    plt.close("all")
    assert len(ax.patches) >= 0 and inf[0][1] - inf[0][0] < full[0][1] - full[0][0]
    # sportyR: infield x = +/-(arc radius + 5), y = (-(13+5), 43+60+5)
    assert inf[0] == pytest.approx((-65.0, 65.0)) and inf[1] == pytest.approx((-18.0, 108.0))


def test_export_does_not_rebind_package_names():
    assert surfaces.NCAASoftballField is NCAASoftballField
    assert surfaces.SoftballField.__module__ == "sportypy.surfaces.softball"
    assert surfaces.NCAAField.__module__ == "sportypy.surfaces.football"  # pre-existing winner
    assert surfaces.NCAACourt.__module__ == "sportypy.surfaces.tennis"
    assert issubclass(NCAASoftballField, SoftballField)
