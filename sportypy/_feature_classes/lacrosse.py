"""Extensions of the ``BaseFeature`` class specific to lacrosse fields.

Ported from sportyR's ``R/features-lacrosse.R``. Each feature's shape is a
direct port of the sportyR function of the same name (``lacrosse_<name>``),
kept as a module-level function; each class draws one of them with the
arguments it is given. Circles use sportyR's 1000 points so the coordinates
match sportyR's point for point.
"""

import math

import numpy as np
import pandas as pd

from sportypy._base_classes._base_feature import BaseFeature

NPOINTS = 1000  # sportyR's create_circle() default


def _circle(center=(0.0, 0.0), start=0.0, end=2.0, r=1.0):
    return BaseFeature.create_circle(
        center=center, npoints=NPOINTS, r=r, start=start, end=end
    )


def _rect(x_min, x_max, y_min, y_max):
    return BaseFeature.create_rectangle(x_min, x_max, y_min, y_max)


def _df(x, y):
    return pd.DataFrame(
        {"x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float)}
    )


def _bind(*dfs):
    return pd.concat(dfs, ignore_index=True)


def _rotate_deg(df, angle):
    """sportyR ``rotate_coords()``: rotate about (0, 0) by ``angle`` degrees."""
    theta = (angle / 180.0) * math.pi
    return _df(
        df["x"] * math.cos(theta) - df["y"] * math.sin(theta),
        df["x"] * math.sin(theta) + df["y"] * math.cos(theta),
    )


# Surface base features -------------------------------------------------------


def defensive_zone(
    field_length=0.0,
    field_width=0.0,
    corner_radius=0.0,
    nzone_length=0.0,
    field_shape="rectangle",
):
    if str(field_shape).lower() == "oval":
        half_length, half_width = field_length / 2.0, field_width / 2.0
        center_x, center_y = half_length - corner_radius, half_width - corner_radius
        return _bind(
            _df([-nzone_length / 2.0], [half_width]),
            _circle((-center_x, center_y), 0.5, 1.0, corner_radius),
            _df([-half_length], [0.0]),
            _circle((-center_x, -center_y), 1.0, 1.5, corner_radius),
            _df([-nzone_length / 2.0] * 2, [-half_width, half_width]),
        )
    return _rect(-field_length / 2.0, 0.0, -field_width / 2.0, field_width / 2.0)


def neutral_zone(nzone_length=0.0, field_width=0.0):
    return _rect(
        -nzone_length / 2.0, nzone_length / 2.0, -field_width / 2.0, field_width / 2.0
    )


def offensive_zone(
    field_length=0.0,
    field_width=0.0,
    corner_radius=0.0,
    nzone_length=0.0,
    field_shape="rectangle",
):
    if str(field_shape).lower() == "oval":
        half_length, half_width = field_length / 2.0, field_width / 2.0
        center_x, center_y = half_length - corner_radius, half_width - corner_radius
        return _bind(
            _df([nzone_length / 2.0], [half_width]),
            _circle((center_x, center_y), 0.5, 0.0, corner_radius),
            _df([half_length], [0.0]),
            _circle((center_x, -center_y), 0.0, -0.5, corner_radius),
            _df([nzone_length / 2.0] * 2, [-half_width, half_width]),
        )
    return _rect(0.0, field_length / 2.0, -field_width / 2.0, field_width / 2.0)


def field_apron(
    field_length=0.0,
    field_width=0.0,
    field_apron_thickness=0.0,
    field_shape="rectangle",
):
    if str(field_shape).lower() == "rectangle":
        hl, hw, t = field_length / 2.0, field_width / 2.0, field_apron_thickness
        return _df(
            [0.0, hl, hl, 0.0, 0.0, hl + t, hl + t, 0.0, 0.0],
            [hw, hw, -hw, -hw, -hw - t, -hw - t, hw + t, hw + t, hw],
        )
    return _df([0.0], [0.0])


# Surface boundaries ----------------------------------------------------------


def sideline(field_length=0.0, line_thickness=0.0):
    return _rect(-field_length / 2.0, field_length / 2.0, 0.0, line_thickness)


def end_line(field_width=0.0, line_thickness=0.0):
    return _rect(0.0, line_thickness, -field_width / 2.0, field_width / 2.0)


def boards(
    field_length=0.0, field_width=0.0, corner_radius=0.0, boundary_thickness=0.0
):
    half_length, half_width = field_length / 2.0, field_width / 2.0
    center_x, center_y = half_length - corner_radius, half_width - corner_radius
    outer = corner_radius + boundary_thickness
    return _bind(
        _df([0.0], [half_width]),
        _circle((center_x, center_y), 0.5, 0.0, corner_radius),
        _df([half_length], [0.0]),
        _circle((center_x, -center_y), 0.0, -0.5, corner_radius),
        _df([0.0, 0.0], [-half_width, -half_width - boundary_thickness]),
        _circle((center_x, -center_y), -0.5, 0.0, outer),
        _df([half_length + boundary_thickness], [0.0]),
        _circle((center_x, center_y), 0.0, 0.5, outer),
        _df([0.0, 0.0], [half_width + boundary_thickness, half_width]),
    )


# Surface lines ---------------------------------------------------------------


def center_line(center_line_width=0.0, line_thickness=0.0):
    return _rect(
        -line_thickness / 2.0,
        line_thickness / 2.0,
        -center_line_width / 2.0,
        center_line_width / 2.0,
    )


def wing_line(wing_line_length=0.0, line_thickness=0.0):
    return _rect(-wing_line_length / 2.0, wing_line_length / 2.0, 0.0, line_thickness)


def restraining_line(field_width=0.0, line_thickness=0.0):
    return _rect(-line_thickness, 0.0, -field_width / 2.0, field_width / 2.0)


def defensive_area_line(defensive_area_line_length=0.0, line_thickness=0.0):
    return _rect(0.0, defensive_area_line_length, 0.0, line_thickness)


def goal_line(
    goal_frame_width=0.0,
    line_thickness=0.0,
    goal_line_full_diameter=False,
    goal_circle_radius=0.0,
):
    if not goal_line_full_diameter:
        return _rect(
            -line_thickness / 2.0,
            line_thickness / 2.0,
            -goal_frame_width / 2.0,
            goal_frame_width / 2.0,
        )
    angle_dev = math.asin((line_thickness / 2.0) / goal_circle_radius) / math.pi
    return _bind(
        _circle((0.0, 0.0), 0.5 - angle_dev, 0.5 + angle_dev, goal_circle_radius),
        _circle((0.0, 0.0), -0.5 - angle_dev, -0.5 + angle_dev, goal_circle_radius),
    )


def referee_crease(referee_crease_radius=0.0, line_thickness=0.0):
    r = referee_crease_radius
    return _bind(
        _df([r], [0.0]),
        _circle((0.0, 0.0), 0.0, 1.0, r),
        _df([-r, -r + line_thickness], [0.0, 0.0]),
        _circle((0.0, 0.0), 1.0, 0.0, r - line_thickness),
        _df([r], [0.0]),
    )


def referee_crease_fill(referee_crease_radius=0.0, line_thickness=0.0):
    return _circle((0.0, 0.0), 0.0, 1.0, referee_crease_radius)


# Surface features ------------------------------------------------------------


def goal_circle(
    goal_circle_radius=0.0,
    line_thickness=0.0,
    goal_circle_full_360=True,
    goal_depth=0.0,
    goal_depth_to_circle=0.0,
):
    r, t = goal_circle_radius, line_thickness
    if goal_circle_full_360:
        half = _bind(
            _df([0.0], [r]),
            _circle((0.0, 0.0), 0.5, -0.5, r),
            _df([0.0, 0.0], [-r, -r + t]),
            _circle((0.0, 0.0), -0.5, 0.5, r - t),
            _df([0.0, 0.0], [r - t, r]),
        )
        return _bind(half, _df(-half["x"], half["y"]))
    depth = goal_depth_to_circle + goal_depth
    start = math.acos(depth / r) / math.pi
    end = 2.0 - start
    return _bind(
        _df([depth], [0.0]),
        _circle((0.0, 0.0), start, end, r),
        _df([depth, depth - t], [0.0, 0.0]),
        _circle((0.0, 0.0), 2.0 - start, 2.0 - end, r - t),
        _df([depth - t, depth], [0.0, 0.0]),
    )


def goal_circle_fill(
    goal_circle_radius=0.0,
    line_thickness=0.0,
    goal_circle_full_360=True,
    goal_depth=0.0,
    goal_depth_to_circle=0.0,
):
    r = goal_circle_radius - line_thickness
    if goal_circle_full_360:
        return _circle((0.0, 0.0), 0.0, 2.0, r)
    start = (
        math.acos((goal_depth_to_circle + goal_depth) / goal_circle_radius) / math.pi
    )
    end = 2.0 - start
    return _circle((0.0, 0.0), 2.0 - start, 2.0 - end, r)


def goal_arc(
    goal_arc_extension=0.0,
    goal_arc_radius=0.0,
    line_thickness=0.0,
    goal_arc_parallel_line_to_center=None,
):
    """The PLL two-point arc (2024 PLL Rulebook II.G).

    Two lines parallel to the sidelines, ``goal_arc_parallel_line_to_center``
    from the goal-line centre, run from the end line until they are
    ``goal_arc_radius`` from it, joined by an arc of ``goal_arc_radius``. When
    the lines are ``goal_arc_radius`` out (the default), it is a semicircle.
    """
    ext, r, t = goal_arc_extension, goal_arc_radius, line_thickness
    if goal_arc_parallel_line_to_center is None:
        goal_arc_parallel_line_to_center = r
    w_outer = min(goal_arc_parallel_line_to_center, r)
    w_inner = w_outer - t
    r_inner = r - t
    x_outer = -math.sqrt(max(r**2 - w_outer**2, 0.0))
    x_inner = -math.sqrt(max(r_inner**2 - w_inner**2, 0.0))
    theta_outer = math.atan2(w_outer, x_outer) / math.pi
    theta_inner = math.atan2(w_inner, x_inner) / math.pi
    return _bind(
        _df([ext, x_outer], [w_outer, w_outer]),
        _circle((0.0, 0.0), theta_outer, 2.0 - theta_outer, r),
        _df(
            [x_outer, ext, ext, x_inner],
            [-w_outer, -w_outer, -w_inner, -w_inner],
        ),
        _circle((0.0, 0.0), 2.0 - theta_inner, theta_inner, r_inner),
        _df([x_inner, ext, ext], [w_inner, w_inner, w_outer]),
    )


def goal_fan(goal_fan_radius=0.0, goal_circle_radius=0.0, line_thickness=0.0):
    """The women's 8 m arc (NCAA Women's Lacrosse Rule 1 Sec. 6).

    Two lines from where the goal line extended crosses the goal circle (B),
    at 45 degrees to the goal line extended, to an arc of ``goal_fan_radius``
    about the goal-line centre (C), joined by that arc. Leagues without an arc
    outside the goal circle have no fan (an empty frame).
    """
    if goal_fan_radius <= goal_circle_radius:
        return _df([], [])
    t = line_thickness
    direction = np.array([-1.0, 1.0]) / math.sqrt(2.0)

    def distance_to_circle(pt, radius):
        b = float(np.sum(pt * direction))
        return -b + math.sqrt(b**2 - float(np.sum(pt**2)) + radius**2)

    b_outer = np.array([0.0, goal_circle_radius])
    c_outer = b_outer + distance_to_circle(b_outer, goal_fan_radius) * direction
    inner_base = b_outer + t * np.array([-1.0, -1.0]) / math.sqrt(2.0)
    b_inner = inner_base + distance_to_circle(inner_base, goal_circle_radius) * direction
    c_inner = inner_base + distance_to_circle(inner_base, goal_fan_radius - t) * direction
    theta_outer = math.atan2(c_outer[1], c_outer[0]) / math.pi
    theta_inner = math.atan2(c_inner[1], c_inner[0]) / math.pi
    return _bind(
        _df([b_outer[0], c_outer[0]], [b_outer[1], c_outer[1]]),
        _circle((0.0, 0.0), theta_outer, 2.0 - theta_outer, goal_fan_radius),
        _df(
            [c_outer[0], b_outer[0], b_inner[0], c_inner[0]],
            [-c_outer[1], -b_outer[1], -b_inner[1], -c_inner[1]],
        ),
        _circle((0.0, 0.0), 2.0 - theta_inner, theta_inner, goal_fan_radius - t),
        _df(
            [c_inner[0], b_inner[0], b_outer[0]],
            [c_inner[1], b_inner[1], b_outer[1]],
        ),
    )


def goal_fan_hash_mark(
    goal_fan_hash_mark_length=0.0, line_thickness=0.0, rotational_angle=0.0
):
    return _rotate_deg(
        _rect(
            -goal_fan_hash_mark_length / 2.0,
            goal_fan_hash_mark_length / 2.0,
            -line_thickness / 2.0,
            line_thickness / 2.0,
        ),
        rotational_angle,
    )


def goal_mouth_hash_mark(goal_mouth_hash_mark_length=0.0, line_thickness=0.0):
    return _rect(-goal_mouth_hash_mark_length, 0.0, -line_thickness, 0.0)


def goal_mouth(
    goal_mouth_radius=0.0, line_thickness=0.0, goal_mouth_semi_circle_separation=0.0
):
    r, t, s = goal_mouth_radius, line_thickness, goal_mouth_semi_circle_separation
    return _bind(
        _df([0.0, 0.0], [s, r]),
        _circle((0.0, 0.0), 0.5, 1.5, r),
        _df([0.0, 0.0, -t, -t], [-r, -s, -s, -r + t]),
        _circle((0.0, 0.0), 1.5, 0.5, r - t),
        _df([-t, -t, 0.0], [r - t, s, s]),
    )


def below_goal_marking(below_goal_marking_radius=0.0):
    return _circle((0.0, 0.0), 0.0, 2.0, below_goal_marking_radius)


def goal_frame(
    goal_frame_opening_interior=0.0, goal_post_thickness=0.0, goal_depth=0.0
):
    w, t = goal_frame_opening_interior, goal_post_thickness
    return _df(
        [0.0, goal_depth - t, 0.0, 0.0, goal_depth, 0.0, 0.0],
        [w / 2.0, 0.0, -w / 2.0, -w / 2.0 - t, 0.0, w / 2.0 + t, 0.0],
    )


def goal_net(goal_frame_opening_interior=0.0, goal_post_thickness=0.0, goal_depth=0.0):
    w = goal_frame_opening_interior
    return _df(
        [0.0, goal_depth - goal_post_thickness, 0.0, 0.0], [w / 2.0, 0.0, -w / 2.0, w]
    )


def center_circle(center_circle_radius=0.0, center_circle_thickness=0.0):
    r, t = center_circle_radius, center_circle_thickness
    return _bind(
        _circle((0.0, 0.0), 0.5, 1.5, r),
        _df([0.0, 0.0], [-r, -r - t]),
        _circle((0.0, 0.0), 1.5, 0.5, r - t),
    )


def player_bench_outline(
    bench_area_outline_thickness=0.0, bench_length=0.0, bench_depth=0.0
):
    t, L, d = bench_area_outline_thickness, bench_length, bench_depth
    return _df(
        [-t, -t, L + t, L + t, L, L, 0.0, 0.0, t],
        [t, 2.0 * t + d, 2.0 * t + d, t, t, t + d, t + d, t, t],
    )


def player_bench_area_fill(
    bench_area_outline_thickness=0.0, bench_length=0.0, bench_depth=0.0
):
    t = bench_area_outline_thickness
    return _rect(-bench_length / 2.0, bench_length / 2.0, t, t + bench_depth)


def penalty_box_outline(
    penalty_box_outline_thickness=0.0,
    penalty_box_length=0.0,
    penalty_box_width=0.0,
    penalty_box_separation=0.0,
    penalty_box_depth=0.0,
):
    t, L, s, d = (
        penalty_box_outline_thickness,
        penalty_box_length,
        penalty_box_separation,
        penalty_box_depth,
    )
    return _df(
        [
            0.0,
            s / 2.0 + L + 2.0 * t,
            s / 2.0 + L + 2.0 * t,
            s / 2.0 + L + t,
            s / 2.0 + L + t,
            s / 2.0 + t,
            s / 2.0 + t,
            s / 2.0,
            s / 2.0,
            0.0,
            0.0,
        ],
        [
            -(2.0 * t + d),
            -(2.0 * t + d),
            -t,
            -t,
            -(t + d),
            -(t + d),
            -t,
            -t,
            -(t + d),
            -(t + d),
            -(2.0 * t + d),
        ],
    )


def penalty_box_fill(
    penalty_box_outline_thickness=0.0, penalty_box_length=0.0, penalty_box_depth=0.0
):
    t = penalty_box_outline_thickness
    return _rect(
        -penalty_box_length / 2.0,
        penalty_box_length / 2.0,
        -t,
        -(t + penalty_box_depth),
    )


def off_field_officials_box(
    officials_box_thickness=0.0, officials_box_length=0.0, officials_box_depth=0.0
):
    t = officials_box_thickness
    return _rect(
        -officials_box_length / 2.0,
        officials_box_length / 2.0,
        -t,
        -(t + officials_box_depth),
    )


def _x_shape(bar_length, bar_width, rotation=45.0):
    """sportyR ``create_x_shape()``."""
    L, w = bar_length / 2.0, bar_width / 2.0
    cross = _df(
        [0.0, w, w, L, L, w, w, -w, -w, -L, -L, -w, -w, 0.0],
        [L, L, w, w, -w, -w, -L, -L, -w, -w, w, w, L, L],
    )
    return _rotate_deg(cross, rotation)


def face_off_marker(
    shape="O", feature_thickness=0.0, side_length=0.0, feature_radius=0.0
):
    shape = str(shape).lower()
    if shape == "o":
        return _circle((0.0, 0.0), 0.0, 2.0, feature_radius)
    if shape == "x":
        return _x_shape(side_length, feature_thickness, 45.0)
    if shape == "square":
        return BaseFeature.create_square(side_length=side_length)
    return _df([], [])


def change_area_outline(
    change_area_length=0.0, change_area_width=0.0, feature_thickness=0.0
):
    L, w, t = change_area_length, change_area_width, feature_thickness
    return _df(
        [L, L, 0.0, 0.0, L + t, L + t, L], [0.0, -w, -w, -(w + t), -(w + t), 0.0, 0.0]
    )


def change_area_fill(change_area_length=0.0, change_area_width=0.0):
    return _rect(0.0, change_area_length, -change_area_width, 0.0)


class BaseLacrosseFeature(BaseFeature):
    """A lacrosse feature drawn by one of this module's shape functions.

    ``dims`` holds the shape function's arguments (in the field's units).
    """

    shape = None

    def __init__(self, dims=None, feature_units="ft", *args, **kwargs):
        self.dims = dict(dims or {})
        self.feature_units = feature_units
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        return type(self).shape(**self.dims)


class FieldConstraint(BaseLacrosseFeature):
    """The field's in-bounds area (a rectangle, or an oval with rounded
    corners when ``corner_radius`` is set); constrains plotted data."""

    def __init__(
        self, field_length=0.0, field_width=0.0, corner_radius=0.0, *args, **kwargs
    ):
        self.length, self.width, self.feature_radius = (
            field_length,
            field_width,
            corner_radius,
        )
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        hl, hw, r = self.length / 2.0, self.width / 2.0, self.feature_radius
        cx, cy = hl - r, hw - r
        return _bind(
            _df([0.0], [hw]),
            _circle((cx, cy), 0.5, 0.0, r),
            _df([hl], [0.0]),
            _circle((cx, -cy), 0.0, -0.5, r),
            _df([0.0], [-hw]),
            _circle((-cx, -cy), -0.5, -1.0, r),
            _df([-hl], [0.0]),
            _circle((-cx, cy), 1.0, 0.5, r),
            _df([0.0], [hw]),
        )


def _feature(name, fn):
    return type(
        name,
        (BaseLacrosseFeature,),
        {
            "shape": staticmethod(fn),
            "__doc__": f"sportyR's ``lacrosse_{fn.__name__}()`` feature.",
        },
    )


DefensiveZone = _feature("DefensiveZone", defensive_zone)
NeutralZone = _feature("NeutralZone", neutral_zone)
OffensiveZone = _feature("OffensiveZone", offensive_zone)
FieldApron = _feature("FieldApron", field_apron)
Sideline = _feature("Sideline", sideline)
EndLine = _feature("EndLine", end_line)
Boards = _feature("Boards", boards)
CenterLine = _feature("CenterLine", center_line)
WingLine = _feature("WingLine", wing_line)
RestrainingLine = _feature("RestrainingLine", restraining_line)
DefensiveAreaLine = _feature("DefensiveAreaLine", defensive_area_line)
GoalLine = _feature("GoalLine", goal_line)
RefereeCrease = _feature("RefereeCrease", referee_crease)
RefereeCreaseFill = _feature("RefereeCreaseFill", referee_crease_fill)
GoalCircle = _feature("GoalCircle", goal_circle)
GoalCircleFill = _feature("GoalCircleFill", goal_circle_fill)
GoalArc = _feature("GoalArc", goal_arc)
GoalFan = _feature("GoalFan", goal_fan)
GoalFanHashMark = _feature("GoalFanHashMark", goal_fan_hash_mark)
GoalMouthHashMark = _feature("GoalMouthHashMark", goal_mouth_hash_mark)
GoalMouth = _feature("GoalMouth", goal_mouth)
BelowGoalMarking = _feature("BelowGoalMarking", below_goal_marking)
GoalFrame = _feature("GoalFrame", goal_frame)
GoalNet = _feature("GoalNet", goal_net)
CenterCircle = _feature("CenterCircle", center_circle)
PlayerBenchOutline = _feature("PlayerBenchOutline", player_bench_outline)
PlayerBenchAreaFill = _feature("PlayerBenchAreaFill", player_bench_area_fill)
PenaltyBoxOutline = _feature("PenaltyBoxOutline", penalty_box_outline)
PenaltyBoxFill = _feature("PenaltyBoxFill", penalty_box_fill)
OffFieldOfficialsBox = _feature("OffFieldOfficialsBox", off_field_officials_box)
FaceOffMarker = _feature("FaceOffMarker", face_off_marker)
ChangeAreaOutline = _feature("ChangeAreaOutline", change_area_outline)
ChangeAreaFill = _feature("ChangeAreaFill", change_area_fill)
