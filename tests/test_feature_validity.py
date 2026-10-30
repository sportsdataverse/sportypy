"""Feature polygons are simple closed rings, as in sportyR's
tests/testthat/test-feature-validity.R."""


import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.colors import to_rgba

import sportypy._feature_classes.lacrosse as lacrosse_features
from sportypy._base_classes._base_feature import BaseFeature
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
