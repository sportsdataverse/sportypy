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
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.colors import to_rgba

import sportypy
import sportypy._feature_classes.lacrosse as lacrosse_features
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
    field = CLASSES[league]()
    ax = field.draw()
    ref = LEAGUES[league]["limits"]["full"]
    assert np.allclose(ax.get_xlim(), ref["x"]) and np.allclose(ax.get_ylim(), ref["y"])
    # every feature that shows, + the surface constraint
    assert len(ax.patches) == sum(f._shows() for f in field._features) + 1
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


# Geometry fixes, each pinned on its own ------------------------------------


def _first(field, cls_name):
    return next(f for f in field._features if type(f).__name__ == cls_name)


def _xy(feat):
    df = feat._translate_feature()
    return df["x"].to_numpy(float), df["y"].to_numpy(float)


def _area(x, y):
    return abs(np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y)) / 2.0


@pytest.mark.parametrize("cls", [lacrosse.NLLField, lacrosse.WorldLacrosseField])
def test_neutral_zone_spans_restraining_lines(cls):
    """The zones read neutral_zone_length (85 ft)."""
    field = cls()
    x, _ = _xy(_first(field, "NeutralZone"))
    assert (x.min(), x.max()) == pytest.approx((-42.5, 42.5))
    assert _first(field, "OffensiveZone").dims["nzone_length"] == 85.0
    assert _first(field, "DefensiveZone").dims["nzone_length"] == 85.0


def test_penalty_box_fills_start_inside_the_boards():
    """The fills are anchored with boards_thickness."""
    p = lacrosse.NLLField().field_params
    want = p["penalty_box_separation"] / 2 + p["boards_thickness"] + p["penalty_box_length"] / 2
    fills = [f for f in lacrosse.NLLField()._features if type(f).__name__ == "PenaltyBoxFill"]
    assert sorted(abs(f.x_anchor) for f in fills) == pytest.approx([want, want])


@pytest.mark.parametrize("cls", [lacrosse.NCAAWLacrosseField, lacrosse.USAWLacrosseField])
def test_goal_fan_hash_marks_sit_on_the_arc_at_their_rotation(cls):
    """Each mark is placed at the angle it is rotated by,
    phi = s / R, about the goal-line centre, where R is the
    middle of the fan's line, goal_fan_radius - goal_fan_line_thickness / 2."""
    field = cls()
    p = field.field_params
    r = p["goal_fan_radius"] - p["goal_fan_line_thickness"] / 2
    cx = p["field_length"] / 2 - p["goal_line_center_to_end_line"]
    marks = [
        f
        for f in field._features
        if type(f).__name__ == "GoalFanHashMark" and (f.x_reflection, f.y_reflection) == (1, 1)
    ]
    seps = p["goal_fan_hash_mark_separation_from_center"]
    assert len(marks) == len(seps)
    for mark, s in zip(marks, seps):
        phi = s / r
        assert mark.dims["rotational_angle"] == pytest.approx(-phi * 180 / math.pi)
        assert np.hypot(mark.x_anchor - cx, mark.y_anchor) == pytest.approx(r)
        assert math.atan2(mark.y_anchor, mark.x_anchor - cx) == pytest.approx(math.pi - phi)


@pytest.mark.parametrize("cls", [lacrosse.NLLField, lacrosse.WorldLacrosseField])
def test_full_range_takes_in_benches_and_boxes(cls):
    """The box-lacrosse display reaches the benches' and
    penalty boxes' outer walls (y +/- 48 ft), half fields too."""
    field = cls()
    for rng, xlim in [("full", (-105, 105)), ("offense", (0, 105)), ("defense", (-105, 0))]:
        x, y = field._get_plot_range_limits(rng)
        assert x == pytest.approx(xlim) and y == pytest.approx((-48.0, 48.0))
    # the plotted-data limits stay the field itself
    assert field._get_plot_range_limits("full", for_plot=True) == ((-100.0, 100.0), (-42.5, 42.5))


def test_goal_arc_without_thickness_is_a_line_not_a_block():
    """Goal_arc_line_thickness defaults to 0."""
    field = lacrosse.NCAAMLacrosseField(
        field_updates={"goal_arc_radius": 15.0, "goal_arc_extension": 0.0}
    )
    assert _area(*_xy(_first(field, "GoalArc"))) == pytest.approx(0.0, abs=1e-9)


def test_center_line_recolour_stops_the_contrasting_default():
    """The contrasting #ffcb05 applies only when the user chose
    no marker colour and the marker would match the (user's) center line."""
    field = lacrosse.NCAAMLacrosseField(color_updates={"center_line": "#ff0000"})
    assert field.feature_colors["center_face_off_marker"] == "#ffffff"
    both = lacrosse.NCAAMLacrosseField(
        color_updates={"center_line": "#123456", "center_face_off_marker": "#123456"}
    )
    assert both.feature_colors["center_face_off_marker"] == "#123456"


# Goal-fan, two-point arc, penalty-box and goal-fan early-return fixes -------


def _goal_x(p):
    return p["field_length"] / 2 - p["goal_line_center_to_end_line"]


def _right_copies(field, cls_name):
    return [
        f
        for f in field._features
        if type(f).__name__ == cls_name and (f.x_reflection, f.y_reflection) == (1, 1)
    ]


@pytest.mark.parametrize("cls", [lacrosse.NCAAWLacrosseField, lacrosse.USAWLacrosseField])
def test_womens_8m_arc_follows_the_rule(cls):
    """Two 45-degree lines from where the goal line extended
    crosses the goal circle, joined by a 10.6 m arc about the goal-line
    centre; hash marks on that circle; goal-line-extended marks 0.305 m."""
    field = cls()
    p = field.field_params
    gx, r, gc = _goal_x(p), p["goal_fan_radius"], p["goal_circle_radius"]
    assert p["goal_mouth_hash_mark_length"] == 0.305
    x, y = _xy(_right_copies(field, "GoalFan")[0])
    dist = np.hypot(x - gx, y)
    assert dist.max() == pytest.approx(r, abs=1e-9)
    # B, where the goal line extended crosses the goal circle, is a vertex
    assert np.min(np.hypot(x - gx, y - gc)) < 1e-9
    assert np.min(np.hypot(x - gx, y + gc)) < 1e-9
    # C (on the 10.6 m circle) lies on the 45-degree line from B
    c = np.argmax(np.where((dist > r - 1e-9) & (y > 0), x, -np.inf))
    assert (y[c] - gc) == pytest.approx(-(x[c] - gx), abs=1e-9)
    # The marks bisect the fan's line, so they sit at its middle
    rm = r - p["goal_fan_line_thickness"] / 2
    assert rm == pytest.approx(10.5495)
    marks = _right_copies(field, "GoalFanHashMark")
    for mark, s in zip(marks, p["goal_fan_hash_mark_separation_from_center"]):
        phi = s / rm
        assert np.hypot(mark.x_anchor - gx, mark.y_anchor) == pytest.approx(rm)
        assert math.atan2(mark.y_anchor, mark.x_anchor - gx) == pytest.approx(math.pi - phi)
        assert mark.dims["rotational_angle"] == pytest.approx(-phi * 180 / math.pi)


def test_pll_two_point_arc_has_parallel_sides():
    """Lines 13 yd from the goal-line centre, parallel to the
    sidelines, from the end line until 15 yd out, joined by a 15 yd arc."""
    field = lacrosse.PLLField()
    p = field.field_params
    assert p["goal_arc_parallel_line_to_center"] == 13.0
    gx, r, t = _goal_x(p), p["goal_arc_radius"], p["goal_arc_line_thickness"]
    x, y = _xy(_right_copies(field, "GoalArc")[0])
    assert np.abs(y).max() == pytest.approx(13.0)
    side = x[np.isclose(np.abs(y), 13.0)]
    assert side.max() == pytest.approx(gx + p["goal_arc_extension"])
    assert side.min() == pytest.approx(gx - math.sqrt(r**2 - 13.0**2))
    front = x < gx - math.sqrt(r**2 - 13.0**2) - 1e-6
    d = np.hypot(x[front] - gx, y[front])
    assert np.all(np.isclose(d, r) | np.isclose(d, r - t))


def test_goal_arc_falls_back_to_a_semicircle():
    """Without goal_arc_parallel_line_to_center the arc is the old semicircle."""
    field = lacrosse.NCAAMLacrosseField(
        field_updates={"goal_arc_radius": 15.0, "goal_arc_extension": 0.0, "goal_arc_line_thickness": 0.1}
    )
    gx = _goal_x(field.field_params)
    x, y = _xy(_right_copies(field, "GoalArc")[0])
    assert np.abs(y).max() == pytest.approx(15.0)
    d = np.hypot(x[x < gx] - gx, y[x < gx])
    assert np.all(np.isclose(d, 15.0) | np.isclose(d, 14.9))


@pytest.mark.parametrize("cls", [lacrosse.NLLField, lacrosse.WorldLacrosseField])
def test_penalty_boxes_are_their_length_inside(cls):
    """Each penalty box is penalty_box_length inside its walls,
    so the three interiors add up to 24 ft."""
    field = cls()
    p = field.field_params
    t, sep, L = p["boards_thickness"], p["penalty_box_separation"], p["penalty_box_length"]
    x, _ = _xy(_right_copies(field, "PenaltyBoxOutline")[0])
    walls = sorted(set(np.round(x[x > 0], 9)))
    assert walls == pytest.approx([sep / 2, sep / 2 + t, sep / 2 + L + t, sep / 2 + L + 2 * t])
    assert (sep / 2 + L + t) - (sep / 2 + t) == L
    assert 2 * L + sep == 24.0


@pytest.mark.parametrize("cls", [lacrosse.NCAAMLacrosseField, lacrosse.NLLField, lacrosse.PLLField])
def test_leagues_without_a_goal_fan_draw_no_fan(cls):
    """sportyR 00e364a: no goal fan outside the goal circle, no fan polygon."""
    field = cls()
    fans = [f for f in field._features if type(f).__name__ == "GoalFan"]
    assert fans and all(len(_xy(f)[0]) == 0 for f in fans)
    field.draw()
    plt.close("all")


def test_update_colors_rederives_the_contrasting_marker():
    """sportyR's rule after update_colors(): the #ffcb05 contrast default is
    re-derived from the colours the user chose, not carried over."""
    field = lacrosse.NCAAMLacrosseField()
    assert field.feature_colors["center_face_off_marker"] == "#ffcb05"
    field.update_colors({"center_line": "#ff0000"})
    assert field.feature_colors["center_face_off_marker"] == "#ffffff"
    field.update_colors({"center_line": "#ffffff"})
    assert field.feature_colors["center_face_off_marker"] == "#ffcb05"
    field.update_colors({"center_face_off_marker": "#123456"})
    field.update_colors({"boards": "#000000"})
    assert field.feature_colors["center_face_off_marker"] == "#123456"
    field.update_field_params({"field_apron_thickness": 6.0})
    assert field.feature_colors["center_face_off_marker"] == "#123456"
    assert field.feature_colors["boards"] == "#000000"
    field.reset_colors()
    assert field.feature_colors["center_face_off_marker"] == "#ffcb05"


def test_scalar_and_array_limits_follow_the_base_surface_contract():
    """A single ``xlim``/``ylim`` value is the lower bound (the upper bound is
    the range's), as on every other surface; an array works like a tuple."""
    field = lacrosse.NCAAMLacrosseField()
    assert field._get_plot_range_limits(xlim=10.0) == ((10.0, 60.0), (-35.0, 35.0))
    assert field._get_plot_range_limits(xlim=np.float64(10.0), ylim=-5.0) == ((10.0, 60.0), (-5.0, 35.0))
    # a lower bound past the end of the range shows the whole range
    assert field._get_plot_range_limits(xlim=80.0) == ((-60.0, 60.0), (-35.0, 35.0))
    assert field._get_plot_range_limits(xlim=np.array([-5.0, 5.0])) == ((-5.0, 5.0), (-35.0, 35.0))
    field.draw(xlim=10.0)
    plt.close("all")


def test_cani_plot_leagues_unknown_league(capsys):
    lacrosse.PLLField().cani_plot_leagues("xyz")
    assert "XYZ does not come with sportypy" in capsys.readouterr().out


def test_goal_arc_without_parallel_lines_is_a_semicircle():
    # With no parallel-line distance the lines are goal_arc_radius out
    default = lacrosse_features.goal_arc(goal_arc_extension=2.0, goal_arc_radius=10.0)
    explicit = lacrosse_features.goal_arc(
        goal_arc_extension=2.0,
        goal_arc_radius=10.0,
        goal_arc_parallel_line_to_center=10.0,
    )
    assert len(default) > 0
    assert default.equals(explicit)


def test_face_off_marker_with_an_unknown_shape_is_empty():
    assert len(lacrosse_features.face_off_marker(shape="triangle")) == 0


def test_added_constrained_feature_is_drawn_and_clipped():
    constraint = {
        "class": lacrosse_features.FieldConstraint,
        "field_length": 100.0,
        "field_width": 50.0,
        "is_constrained": True,
        "visible": True,
        "facecolor": "#ffffff00",
        "edgecolor": None,
        "zorder": 1,
    }
    plain = lacrosse.PLLField()
    plain_ax = plain.draw()
    field = lacrosse.PLLField(new_feature_1=constraint)
    ax = field.draw()
    # the added feature is initialized, drawn last, and clipped to the field
    assert len(field._features) == len(plain._features) + 1
    assert len(ax.patches) == len(plain_ax.patches) + 1
    assert ax.patches[-1].get_clip_path() is not None
    plt.close(plain_ax.figure)
    plt.close(ax.figure)
