"""Feature polygons are simple closed rings, as in sportyR's
tests/testthat/test-feature-validity.R."""

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.colors import to_rgba

import sportypy._feature_classes.hockey as hockey_features
import sportypy._feature_classes.lacrosse as lacrosse_features
from sportypy._base_classes._base_feature import BaseFeature
from sportypy.surfaces.hockey import HockeyRink
from sportypy.surfaces.lacrosse import NCAAMLacrosseField

split_rings = BaseFeature._split_rings
has_area = BaseFeature._has_area


def _df(x, y):
    return pd.DataFrame({"x": np.asarray(x, float), "y": np.asarray(y, float)})


def _ring(df):
    return df[["x", "y"]].to_numpy(float)


def count_crossings(ring, tol=1e-9):
    """Pairs of non-adjacent edges of a ring that properly cross."""
    a, b = ring[:-1], ring[1:]
    n = len(a)

    def side(p, q, r):
        return (q[..., 0] - p[..., 0]) * (r[..., 1] - p[..., 1]) - (
            q[..., 1] - p[..., 1]
        ) * (r[..., 0] - p[..., 0])

    crossings = 0
    for i in range(n - 2):
        j = np.arange(i + 2, n)
        if i == 0:
            j = j[j != n - 1]
        crossed_i = side(a[i], b[i], a[j]) * side(a[i], b[i], b[j]) < -(tol**2)
        crossed_j = side(a[j], b[j], a[i]) * side(a[j], b[j], b[i]) < -(tol**2)
        crossings += int(np.sum(crossed_i & crossed_j))
    return crossings


def _area(ring):
    x, y = ring[:, 0], ring[:, 1]
    return abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])) / 2


def test_split_rings_and_has_area_read_back_to_back_rings():
    square = BaseFeature.create_square(2)
    other = BaseFeature.create_square(2, center=(5, 0))
    two = pd.concat([square, other], ignore_index=True)
    assert len(split_rings(two)) == 2
    assert has_area(two)
    # opposite windings do not cancel
    assert has_area(pd.concat([square, other[::-1]], ignore_index=True))
    # a line, a single point and a collapsed rectangle have no area
    assert not has_area(_df([0, 1, 0], [0, 0, 0]))
    assert not has_area(_df([0], [0]))
    assert len(split_rings(_df([1, 1, 1], [2, 2, 2]))) == 1
    assert not has_area(_df([1, 1, 1], [2, 2, 2]))
    assert not has_area(BaseFeature.create_rectangle(-100, 100, 0, 0))
    # a path that never closes is kept as one trailing ring
    assert len(split_rings(_df([0, 1, 1], [0, 0, 1]))) == 1
    assert len(split_rings(_df([0], [0]))) == 1


def test_nhl_trapezoid_is_two_simple_strips_from_the_goal_line():
    df = hockey_features.GoaltendersRestrictedArea(
        rink_length=200.0,
        feature_thickness=2 / 12,
        short_base_width=22.0,
        long_base_width=28.0,
        x_anchor=89.0,
    )._get_centered_feature()
    rings = split_rings(df)
    assert [len(r) for r in rings] == [5, 5]
    assert [count_crossings(r) for r in rings] == [0, 0]


def test_nhl_crease_inner_arc_meets_the_inner_straight_sides():
    crease = hockey_features.GoalCreaseOutline(
        feature_radius=6.0,
        feature_thickness=2 / 12,
        crease_style="nhl98",
        crease_length=4.5,
        crease_width=8.0,
        notch_dist_x=4.0,
        notch_width=0.5,
    )
    df = crease._get_centered_feature()
    # the inner arc starts and ends on the inner straight sides
    inner = 6.0 - 2 / 12
    on_side = np.abs(np.abs(df["y"]) - (4.0 - 2 / 12)) < 1e-9
    on_arc = np.abs(np.hypot(df["x"], df["y"]) - inner) < 1e-9
    assert int((on_side & on_arc).sum()) == 2


def test_nhl92_crease_is_its_arc_band_and_two_l_marks():
    df = hockey_features.GoalCreaseOutline(
        feature_radius=6.0,
        feature_thickness=2 / 12,
        crease_style="nhl92",
        crease_width=8.0,
        notch_dist_x=4.0,
        notch_width=0.5,
    )._get_centered_feature()
    rings = split_rings(df)
    assert [len(r) for r in rings] == [2001, 7, 7]
    assert [count_crossings(r) for r in rings] == [0, 0, 0]
    # the band is the half annulus between the two radii
    inner = 6.0 - 2 / 12
    assert _area(rings[0]) == pytest.approx(math.pi * (36 - inner**2) / 2, rel=1e-5)


def test_center_faceoff_circle_closes_on_its_first_point():
    df = hockey_features.CenterFaceoffCircle(
        feature_radius=15.0, feature_thickness=2 / 12
    )._get_centered_feature()
    ring = _ring(df)
    assert np.allclose(ring[0], ring[-1], atol=1e-9)
    assert count_crossings(ring) == 0
    assert len(split_rings(df)) == 1


@pytest.mark.parametrize("league", ["nhl", "ohl", "ushl"])
def test_hockey_fixed_features_are_simple_rings(league):
    names = {"GoaltendersRestrictedArea", "CenterFaceoffCircle", "PlayerBenchOutline"}
    if league == "ohl":
        names.add("GoalCreaseOutline")
    seen = set()
    for f in HockeyRink(league_code=league)._features:
        if type(f).__name__ in names:
            seen.add(type(f).__name__)
            for ring in split_rings(f._get_centered_feature()):
                assert count_crossings(ring) == 0, (league, type(f).__name__)
    assert seen == names


@pytest.mark.parametrize(
    "fn, kwargs",
    [
        (
            lacrosse_features.goal_frame,
            {"goal_frame_opening_interior": 6.0, "goal_post_thickness": 0.125, "goal_depth": 7.0},
        ),
        (
            lacrosse_features.goal_net,
            {"goal_frame_opening_interior": 6.0, "goal_post_thickness": 0.125, "goal_depth": 7.0},
        ),
        (
            lacrosse_features.player_bench_outline,
            {"bench_area_outline_thickness": 0.5, "bench_length": 30.0, "bench_depth": 6.0},
        ),
    ],
)
def test_lacrosse_goal_and_bench_outlines_close_on_their_first_point(fn, kwargs):
    df = fn(**kwargs)
    ring = _ring(df)
    assert np.allclose(ring[0], ring[-1])
    assert len(split_rings(df)) == 1
    assert count_crossings(ring) == 0


@pytest.mark.parametrize("league", ["ncaam", "ncaaw", "usaw"])
def test_lacrosse_goal_mouth_stubs_end_on_the_inner_arc(league):
    p = NCAAMLacrosseField().league_dimensions[league]
    r, t = p["goal_mouth_radius"], p["goal_mouth_line_thickness"]
    df = lacrosse_features.goal_mouth(r, t, p.get("goal_mouth_semi_circle_separation", 0.0))
    ring = _ring(df)
    assert np.allclose(ring[0], ring[-1])
    assert all(count_crossings(rg) == 0 for rg in split_rings(df))
    assert has_area(df)
    on_inner_edge = np.abs(df["x"] + t) < 1e-9
    on_inner_arc = np.abs(np.hypot(df["x"], df["y"]) - (r - t)) < 1e-9
    assert int((on_inner_edge & on_inner_arc).sum()) == 2


def _goal_mouth_area(radius, thickness, separation):
    """The half annulus plus the parts of the stubs inside its hole."""
    inner = radius - thickness
    if inner <= 0:
        return math.pi * radius**2 / 2
    c = -min(thickness, math.sqrt(max(inner**2 - separation**2, 0)))

    def antiderivative(x):  # of the inner arc's height, sqrt(inner^2 - x^2)
        return x * math.sqrt(inner**2 - x**2) / 2 + inner**2 * math.asin(x / inner) / 2

    stub = 2 * (antiderivative(0) - antiderivative(c) + separation * c)
    return math.pi * (radius**2 - inner**2) / 2 + stub


@pytest.mark.parametrize(
    "radius, thickness, separation",
    [
        (1, 0.6, 0.2),  # thick band
        (1, 0.6, 0),  # thick band, no separation
        (14.6, 0.101, 14.4995),  # separation past the stub's edge
        (3, 0.1, 2.95),  # separation past the inner arc
        (1, 1.2, 0.3),  # thicker than the radius
    ],
)
def test_custom_goal_mouths_are_the_band_and_stubs_union(radius, thickness, separation):
    df = lacrosse_features.goal_mouth(radius, thickness, separation)
    ring = _ring(df)
    assert np.allclose(ring[0], ring[-1])
    assert len(split_rings(df)) == 1
    assert count_crossings(ring) == 0
    assert _area(ring) == pytest.approx(
        _goal_mouth_area(radius, thickness, separation), rel=1e-4
    )


def test_features_with_no_area_and_no_outline_are_not_drawn():
    line = BaseFeature.create_rectangle(-1, 1, 0, 0)

    class Line(BaseFeature):
        def _get_centered_feature(self):
            return line.copy()

    ax = plt.gca()
    assert Line(facecolor="#123456").draw(ax, ax.transData) not in ax.patches
    # a visible outline keeps it; a transparent one does not
    assert Line(facecolor="#123456", edgecolor="#000000").draw(ax, ax.transData) in ax.patches
    assert Line(facecolor="#123456", edgecolor="#00000000").draw(ax, ax.transData) not in ax.patches
    # a goal arc added with no thickness is not drawn
    field = NCAAMLacrosseField(
        field_updates={"goal_arc_radius": 15.0, "goal_arc_extension": 15.0},
        color_updates={"goal_arc": "#123456"},
    )
    ax = field.draw()
    assert not [p for p in ax.patches if p.get_facecolor() == to_rgba("#123456")]
    plt.close("all")
