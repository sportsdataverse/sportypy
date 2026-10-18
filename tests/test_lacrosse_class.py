"""Tests for the sportyR-ported lacrosse fields (7 leagues).

tests/data/sportyr_lacrosse_fixture.json holds, for each league, every polygon
layer that sportyR's ``geom_lacrosse()`` draws, in drawing order (point count,
moments over every point, every 25th point, colours) and its display limits;
see tests/data/README_lacrosse_fixture.md for provenance.

sportypy draws circles with the same 1000 points as sportyR, so every polygon
is compared point for point (1e-9). That covers each arc's radius, direction
and sweep; ``test_circles_radius_direction_sweep`` checks those explicitly too.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.colors import to_rgba

import sportypy
import sportypy.surfaces as surfaces
from sportypy.surfaces import lacrosse
from sportypy.surfaces.lacrosse import DEFAULT_COLORS, LacrosseField

FIX = json.loads(
    (Path(__file__).parent / "data/sportyr_lacrosse_fixture.json").read_text()
)
LEAGUES = FIX["leagues"]
CLASSES = {
    "ncaam": lacrosse.NCAAMLacrosseField,
    "ncaaw": lacrosse.NCAAWLacrosseField,
    "nll": lacrosse.NLLField,
    "pll": lacrosse.PLLField,
    "usam": lacrosse.USAMLacrosseField,
    "usaw": lacrosse.USAWLacrosseField,
    "world lacrosse": lacrosse.WorldLacrosseField,
}
TOL = 1e-9


def _layers(field):
    """sportypy's polygons in sportyR's drawing order.

    sportyR draws a feature reflected over both axes as (x, y), (-x, y),
    (-x, -y), (x, -y); sportypy creates those copies as (x, y), (x, -y),
    (-x, y), (-x, -y).
    """
    feats = list(field._features)
    out, i = [], 0
    while i < len(feats):
        f = feats[i]
        both = (
            (f.x_reflection, f.y_reflection) == (1, 1)
            and i + 3 < len(feats)
            and (feats[i + 1].x_reflection, feats[i + 1].y_reflection) == (1, -1)
            and (feats[i + 3].x_reflection, feats[i + 3].y_reflection) == (-1, -1)
        )
        block = [feats[i], feats[i + 2], feats[i + 3], feats[i + 1]] if both else [f]
        out += block
        i += len(block)
    return out


@pytest.mark.parametrize("league", list(LEAGUES))
def test_params_match_sportyr(league):
    assert CLASSES[league]().field_params == LEAGUES[league]["params"]
    assert LacrosseField(league_code=league).field_params == LEAGUES[league]["params"]


@pytest.mark.parametrize("league", list(LEAGUES))
def test_every_polygon_matches_sportyr(league):
    field = CLASSES[league]()
    mine = _layers(field)
    theirs = LEAGUES[league]["layers"]
    assert len(mine) == len(theirs)
    for k, (feat, ref) in enumerate(zip(mine, theirs)):
        df = feat._translate_feature()
        x, y = df["x"].to_numpy(float), df["y"].to_numpy(float)
        where = f"{league} layer {k} ({type(feat).__name__})"
        assert len(x) == ref["n"], where
        moments = [x.sum(), y.sum(), (x * x).sum(), (y * y).sum(), (x * y).sum()]
        assert np.allclose(moments, ref["moments"], rtol=1e-10, atol=TOL), where
        idx = np.asarray(ref["idx"], dtype=int)
        assert np.abs(x[idx] - np.asarray(ref["x"])).max(initial=0) < TOL, where
        assert np.abs(y[idx] - np.asarray(ref["y"])).max(initial=0) < TOL, where
        assert to_rgba(feat.plot_kwargs["facecolor"]) == to_rgba(ref["fill"]), where
        edge = feat.plot_kwargs.get("edgecolor")
        want_edge = ref["colour"] if ref["colour"] else "none"
        assert to_rgba(edge if edge is not None else "#ffffff00") == pytest.approx(
            to_rgba(want_edge) if to_rgba(want_edge)[3] else to_rgba("#ffffff00")
        ), where


def _arc_stats(x, y, cx, cy):
    r = np.hypot(x - cx, y - cy)
    theta = np.unwrap(np.arctan2(y - cy, x - cx))
    return r, theta[-1] - theta[0]


@pytest.mark.parametrize(
    "league, cls_name, first",
    [
        ("nll", "GoalCircle", 1),
        ("ncaam", "GoalCircle", 1),
        ("world lacrosse", "CenterCircle", 0),
        ("ncaaw", "GoalMouth", 2),
    ],
)
def test_circles_radius_direction_sweep(league, cls_name, first):
    """The outer arc of each circle: same radius about its anchor, same
    direction and total sweep as sportyR (from sportyR's sampled points)."""
    field = CLASSES[league]()
    mine = _layers(field)
    k, feat = next((k, f) for k, f in enumerate(mine) if type(f).__name__ == cls_name)
    ref = LEAGUES[league]["layers"][k]
    df = feat._translate_feature()
    n_ring = 1000  # sportyR create_circle() points
    ring = slice(first, first + n_ring)
    x, y = df["x"].to_numpy()[ring], df["y"].to_numpy()[ring]
    cx, cy = feat.x_anchor, feat.y_anchor
    r, sweep = _arc_stats(x, y, cx, cy)
    idx = np.asarray(ref["idx"])
    sel = (idx >= first) & (idx < first + n_ring)
    rr, rsweep = _arc_stats(
        np.asarray(ref["x"])[sel], np.asarray(ref["y"])[sel], cx, cy
    )
    assert np.allclose(r, r[0]) and np.allclose(rr, r[0])
    # the samples stop short of the ring's last point; compare the sampled span
    rx, ry = x[idx[sel] - first], y[idx[sel] - first]
    assert _arc_stats(rx, ry, cx, cy)[1] == pytest.approx(rsweep, abs=TOL)
    assert np.sign(sweep) == np.sign(rsweep) and sweep != 0


@pytest.mark.parametrize("league", list(LEAGUES))
@pytest.mark.parametrize(
    "display_range", ["full", "in_bounds_only", "offense", "defense"]
)
def test_display_limits_match_sportyr(league, display_range):
    field = CLASSES[league]()
    ref = LEAGUES[league]["limits"][display_range]
    xlim, ylim = field._get_plot_range_limits(display_range)
    assert np.allclose(xlim, ref["x"], atol=TOL) and np.allclose(
        ylim, ref["y"], atol=TOL
    )


@pytest.mark.parametrize("league", list(LEAGUES))
def test_draws(league):
    ax = CLASSES[league]().draw()
    ref = LEAGUES[league]["limits"]["full"]
    assert np.allclose(ax.get_xlim(), ref["x"]) and np.allclose(ax.get_ylim(), ref["y"])
    assert len(ax.patches) > len(LEAGUES[league]["layers"])  # + the surface constraint
    plt.close("all")


def test_draw_half_field_and_rotation():
    ax = lacrosse.PLLField().draw(display_range="offense", rotation=90)
    assert np.allclose(ax.get_xlim(), (-36.0, 36.0)) and np.allclose(
        ax.get_ylim(), (0.0, 56.0)
    )
    plt.close("all")


def test_colour_updates_reach_drawn_patches():
    colors = {k: "#123456" for k in DEFAULT_COLORS if k != "plot_background"}
    field = lacrosse.NLLField(color_updates=colors)
    ax = field.draw()
    faces = {
        tuple(np.round(p.get_facecolor(), 6)) for p in ax.patches if p.get_visible()
    }
    assert tuple(np.round(to_rgba("#123456"), 6)) in faces
    for feat in field._features:
        assert to_rgba(feat.plot_kwargs["facecolor"]) in (
            to_rgba("#123456"),
            to_rgba("#ffffff00"),
        )
    plt.close("all")


def test_center_face_off_marker_contrasting_colour():
    """sportyR colours the NCAA men's center face-off square #ffcb05 when it
    would otherwise match the center line."""
    assert (
        lacrosse.NCAAMLacrosseField().feature_colors["center_face_off_marker"]
        == "#ffcb05"
    )
    assert (
        lacrosse.USAMLacrosseField().feature_colors["center_face_off_marker"]
        == "#ffffff"
    )
    custom = lacrosse.NCAAMLacrosseField(
        color_updates={"center_face_off_marker": "#000000"}
    )
    assert custom.feature_colors["center_face_off_marker"] == "#000000"


def test_units_and_state_survive_update_and_reset():
    field = lacrosse.NLLField(units="m", rotation=90.0, x_trans=3.0)
    field.update_colors({"boards": "#000000"})
    field.reset_field_params()
    field.reset_colors()
    assert field.field_params["field_units"] == "m"
    assert field.field_params["field_length"] == pytest.approx(200.0 * 0.3048)
    assert field.x_trans == 3.0 and field.league_code == "nll"
    assert field.feature_colors["boards"] == DEFAULT_COLORS["boards"]


def test_unknown_league_has_no_params():
    assert LacrosseField(league_code="xyz").field_params == {}


def test_cani_methods(capsys):
    field = lacrosse.PLLField()
    field.cani_plot_leagues()
    field.cani_plot_leagues("nll")
    field.cani_color_features()
    field.cani_change_dimensions()
    out = capsys.readouterr().out
    assert "- WORLD LACROSSE" in out and "NLL comes with sportypy" in out
    assert "- boards (#ffa500)" in out and "- goal_arc_radius (15.0)" in out


def test_exports_do_not_rebind_package_names():
    names = {
        "LacrosseField",
        "NCAAMLacrosseField",
        "NCAAWLacrosseField",
        "NLLField",
        "PLLField",
        "USAMLacrosseField",
        "USAWLacrosseField",
        "WorldLacrosseField",
    }
    for module in (surfaces, sportypy):
        from_lacrosse = {
            n
            for n in dir(module)
            if getattr(getattr(module, n), "__module__", "") == lacrosse.__name__
        }
        assert from_lacrosse == names
    assert surfaces.NCAAField.__module__ == "sportypy.surfaces.football"
    assert surfaces.NCAACourt.__module__ == "sportypy.surfaces.tennis"
    assert sportypy.GoalLine.__module__ == "sportypy._feature_classes.soccer"  # pre-existing winner
