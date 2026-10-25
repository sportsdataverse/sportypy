"""Extensions of the ``BaseFeature`` class specific to softball fields.

Ported from sportyR's ``R/features-softball.R``. Features whose geometry is
identical to baseball's (field constraint, infield dirt, home plate, bases,
pitcher's plate, running lane) are reused from the baseball module; the
remaining features differ from baseball (see the classes below).
"""

import math

import numpy as np
import pandas as pd

from sportypy._feature_classes.baseball import (
    Base,
    BaseBaseballFeature,
    FieldConstraint,
    HomePlate,
    InfieldDirt,
    PitchersPlate,
    RunningLane,
)

__all__ = [
    "Base",
    "BattersBox",
    "CatchersBox",
    "CoachesBox",
    "FieldConstraint",
    "FoulLine",
    "HomePlate",
    "InfieldDirt",
    "PitchersCircle",
    "PitchersLane",
    "PitchersPlate",
    "RunningLane",
]


class BattersBox(BaseBaseballFeature):
    """The batter's box (half drawn, then reflected over the y axis).

    Attributes
    ----------
    batters_box_length, batters_box_width : float
        Outside-of-the-chalk dimensions of the box (``y`` and ``x``)

    batters_box_y_adj : float
        The shift in ``y`` needed to align the box with home plate
    """

    def __init__(self, batters_box_length=0.0, batters_box_width=0.0, batters_box_y_adj=0.0, *args, **kwargs):
        self.batters_box_length = batters_box_length
        self.batters_box_width = batters_box_width
        self.batters_box_y_adj = batters_box_y_adj
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        w, h, t = (self.batters_box_width / 2.0, self.batters_box_length / 2.0, self.feature_thickness)
        half = pd.DataFrame(
            {"x": [0.0, w, w, 0.0, 0.0, w - t, w - t, 0.0, 0.0], "y": [h, h, -h, -h, -h + t, -h + t, h - t, h - t, h]}
        )
        box = pd.concat([half, self._reflect(half, over_x=False, over_y=True)])
        box["y"] = box["y"] + self.batters_box_y_adj
        return box.reset_index(drop=True)


class CatchersBox(BaseBaseballFeature):
    """The catcher's box, behind the rear edge of the batter's boxes.

    Attributes
    ----------
    catchers_box_depth, catchers_box_width : float
        Dimensions of the box

    batters_box_length, batters_box_y_adj : float
        Batter's box values locating the box's front edge
    """

    def __init__(
        self,
        catchers_box_depth=0.0,
        catchers_box_width=0.0,
        batters_box_length=0.0,
        batters_box_y_adj=0.0,
        *args,
        **kwargs,
    ):
        self.catchers_box_depth = catchers_box_depth
        self.catchers_box_width = catchers_box_width
        self.batters_box_length = batters_box_length
        self.batters_box_y_adj = batters_box_y_adj
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        w, t = self.catchers_box_width / 2.0, self.feature_thickness
        front = (-self.batters_box_length / 2.0) + self.batters_box_y_adj
        back = front - self.catchers_box_depth
        return pd.DataFrame(
            {
                "x": [w, w, -w, -w, -w + t, -w + t, w - t, w - t, w],
                "y": [front, back, back, front, front, back + t, back + t, front, front],
            }
        )


class FoulLine(BaseBaseballFeature):
    """A foul line; it exits the batter's box by whichever edge it reaches first.

    Attributes
    ----------
    is_line_1b : bool
        Whether the line is the first base line

    line_distance : float
        The length of the foul line

    batters_box_length, batters_box_width, batters_box_y_adj : float
        Batter's box dimensions

    home_plate_side_to_batters_box, home_plate_edge_length : float
        Gap between home plate and the box, and the plate's edge length
    """

    def __init__(
        self,
        is_line_1b=False,
        line_distance=0.0,
        batters_box_length=0.0,
        batters_box_width=0.0,
        batters_box_y_adj=0.0,
        home_plate_side_to_batters_box=0.0,
        home_plate_edge_length=0.0,
        *args,
        **kwargs,
    ):
        self.is_line_1b = is_line_1b
        self.line_distance = line_distance
        self.batters_box_length = batters_box_length
        self.batters_box_width = batters_box_width
        self.batters_box_y_adj = batters_box_y_adj
        self.home_plate_side_to_batters_box = home_plate_side_to_batters_box
        self.home_plate_edge_length = home_plate_edge_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        outer_x = self.home_plate_edge_length / 2.0 + self.home_plate_side_to_batters_box + self.batters_box_width
        front_y = self.batters_box_length / 2.0 + self.batters_box_y_adj
        s = min(outer_x, front_y)
        d, t = self.line_distance, self.feature_thickness

        if not self.is_line_1b:
            end_x = d * math.cos(3.0 * np.pi / 4.0)
            end_y = d * math.sin(3.0 * np.pi / 4.0)
            xs = [-s, end_x, end_x + t, -s + t, -s]
        else:
            end_x = d * math.cos(np.pi / 4.0)
            end_y = d * math.sin(np.pi / 4.0)
            xs = [s, end_x, end_x - t, s - t, s]

        return pd.DataFrame({"x": xs, "y": [s, end_y, end_y, s, s]})


class PitchersCircle(BaseBaseballFeature):
    """The pitcher's circle: a ring of ``feature_thickness`` around the plate.

    ``feature_radius`` is the circle's outer radius.
    """

    def _get_centered_feature(self):
        return pd.concat(
            [
                self.create_circle(center=(0.0, 0.0), start=0.0, end=2.0, r=self.feature_radius),
                self.create_circle(
                    center=(0.0, 0.0), start=2.0, end=0.0, r=self.feature_radius - self.feature_thickness
                ),
            ]
        ).reset_index(drop=True)


class PitchersLane(BaseBaseballFeature):
    """The line from the pitcher's plate toward the batter's box (one side).

    Attributes
    ----------
    pitchers_lane_length, pitchers_plate_length : float
        Length of the lane line and of the pitcher's plate

    pitchers_plate_front_to_home_plate : float
        Distance from the plate's front edge to the back tip of home plate

    home_plate_edge_length, home_plate_side_to_batters_box : float
    batters_box_length, batters_box_y_adj : float
        Dimensions locating the inside front corner of the batter's box
    """

    def __init__(
        self,
        pitchers_lane_length=0.0,
        pitchers_plate_length=0.0,
        pitchers_plate_front_to_home_plate=0.0,
        home_plate_edge_length=0.0,
        home_plate_side_to_batters_box=0.0,
        batters_box_length=0.0,
        batters_box_y_adj=0.0,
        *args,
        **kwargs,
    ):
        self.pitchers_lane_length = pitchers_lane_length
        self.pitchers_plate_length = pitchers_plate_length
        self.pitchers_plate_front_to_home_plate = pitchers_plate_front_to_home_plate
        self.home_plate_edge_length = home_plate_edge_length
        self.home_plate_side_to_batters_box = home_plate_side_to_batters_box
        self.batters_box_length = batters_box_length
        self.batters_box_y_adj = batters_box_y_adj
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        inner_x = self.home_plate_edge_length / 2.0 + self.home_plate_side_to_batters_box
        front_y = self.batters_box_length / 2.0 + self.batters_box_y_adj
        start_x = self.pitchers_plate_length / 2.0
        dx = inner_x - start_x
        dy = front_y - self.pitchers_plate_front_to_home_plate

        theta = -np.pi / 2.0 if (dx == 0 and dy == 0) else math.atan2(dy, dx)

        end_x = start_x + self.pitchers_lane_length * math.cos(theta)
        end_y = self.pitchers_lane_length * math.sin(theta)
        t = self.feature_thickness

        return pd.DataFrame(
            {"x": [start_x, end_x, end_x - t, start_x - t, start_x], "y": [0.0, end_y, end_y, 0.0, 0.0]}
        )


class CoachesBox(BaseBaseballFeature):
    """An L-shaped coach's box beside the first base line (reflected for 3B).

    Attributes
    ----------
    baseline_distance : float
        Distance of each baseline

    coaches_box_depth, coaches_box_length, coaches_box_width : float
        Offset of the box from the foul line, and its length and width
    """

    def __init__(
        self,
        baseline_distance=0.0,
        coaches_box_depth=0.0,
        coaches_box_length=0.0,
        coaches_box_width=0.0,
        *args,
        **kwargs,
    ):
        self.baseline_distance = baseline_distance
        self.coaches_box_depth = coaches_box_depth
        self.coaches_box_length = coaches_box_length
        self.coaches_box_width = coaches_box_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # a: distance along the first base line; d: distance into foul
        # territory from the foul line's outer edge
        a_end = self.baseline_distance
        a_start = a_end - self.coaches_box_length
        d_in = self.coaches_box_depth
        d_out = d_in + self.coaches_box_width
        t = self.feature_thickness
        a = np.array([a_end, a_start, a_start, a_start + t, a_start + t, a_end, a_end])
        d = np.array([d_in, d_in, d_out, d_out, d_in + t, d_in + t, d_in])

        return pd.DataFrame({"x": (a + d) / math.sqrt(2.0), "y": (a - d) / math.sqrt(2.0)})
