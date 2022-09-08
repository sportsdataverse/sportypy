"""Extensions of the ``BaseFeature`` class to be specific to soccer pitches.

The features are all parameterized by the basic characteristics of a soccer
pitch. A user can manually specify their own pitch parameters in the
``SoccerPitch`` class that will adjust the placement of these features, however
the features themselves will be consistent across all soccer surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseSoccerFeature(BaseFeature):
    """An extension of the ``BaseFeature`` class for soccer features.

    The following attributes are specific to soccer features only. For more
    information on inherited attributes, please see the ``BaseFeature`` class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
    pitch_length : float
        The length of the pitch in TV view. The default is ``0.0``

    pitch_width : float
        The width of the pitch in TV view. The default is ``0.0``

    feature_radius : float
        The radius needed to draw the feature. This may not be needed for all
        features. The default is ``0.0``

    feature_thickness : float
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed. The default is ``0.0``

    field_units : str
        The units with which the feature is drawn. The default is ``"ft"``
    """

    def __init__(self, pitch_length = 0.0, pitch_width = 0.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = "ft", *args, **kwargs):

        # Set the full-sized dimensions of the pitch
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class PitchConstraint(BaseSoccerFeature):
    """The constraint around the interior edge of the pitch's boundary lines.

    This confines all interior features to be constrained inside the pitch, as
    well as any interior plots.
    """

    def _get_centered_feature(self):
        """Generate the points comprising the inner boundary of the pitch.

        This is done to constrain any features from extending needlessly beyond
        the edge of the pitch. Lines are considered in, so this should include
        the interior of the touchlines and goal lines
        """
        # Define the length and width of the pitch as length and width
        # attributes. These will be used to constrain plotted points to be
        # defined inside the surface
        self.length = self.pitch_length
        self.width = self.pitch_width

        pitch_constraint_df = self.create_rectangle(
            x_min = -self.pitch_length / 2.0,
            x_max = self.pitch_length / 2.0,
            y_min = -self.pitch_width / 2.0,
            y_max = self.pitch_width / 2.0
        )

        return pitch_constraint_df


class HalfPitch(BaseSoccerFeature):
    """One half, either the offensive or defensive half, of the pitch.

    This allows each half to take on its own color and be plotted
    independently, but the halves may take the same color so they look
    symmetrical
    """

    def _get_centered_feature(self):
        """Generate the points comprising the half of the pitch.

        The pitch half is constrained to be inside of the touchlines
        """
        pitch_half_df = self.create_rectangle(
            x_min = -self.pitch_length / 4.0,
            x_max = self.pitch_length / 4.0,
            y_min = -self.pitch_width / 2.0,
            y_max = self.pitch_width / 2.0,
        )

        return pitch_half_df


class PitchApron(BaseSoccerFeature):
    """The apron of the pitch beyond the touchline and goal line.

    This is to allow a more accurate representation of the pitch, as no ads are
    allowed within a certain distance of the exterior edge of the touchline and
    goal line
    """

    def __init__(self, pitch_apron_touchline = 0.0,
                  pitch_apron_goal_line = 0.0, goal_depth = 0.0, *args,
                  **kwargs):
        # Initialize the attributes unique to this feature
        self.pitch_apron_touchline = pitch_apron_touchline
        self.pitch_apron_goal_line = pitch_apron_goal_line
        self.goal_depth = goal_depth
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the pitch apron's boundary.

        This should extend fully outside of the pitch, and is forced to be
        symmetric
        """
        pitch_apron_df = pd.DataFrame({
            "x": [
                0.0,
                self.pitch_length / 2.0,
                self.pitch_length / 2.0,
                0.0,
                0.0,
                (
                    (self.pitch_length / 2.0) +
                    self.pitch_apron_goal_line +
                    self.goal_depth
                ),
                (
                    (self.pitch_length / 2.0) +
                    self.pitch_apron_goal_line +
                    self.goal_depth
                ),
                0.0,
                0.0
            ],

            "y": [
                self.pitch_width / 2.0,
                self.pitch_width / 2.0,
                -self.pitch_width / 2.0,
                -self.pitch_width / 2.0,
                # Adding/subtracting goal_depth here for symmetry
                (
                    (-self.pitch_width / 2.0) -
                    self.pitch_apron_touchline -
                    self.goal_depth
                ),
                (
                    (-self.pitch_width / 2.0) -
                    self.pitch_apron_touchline -
                    self.goal_depth
                ),
                (
                    (self.pitch_width / 2.0) +
                    self.pitch_apron_touchline +
                    self.goal_depth
                ),
                (
                    (self.pitch_width / 2.0) +
                    self.pitch_apron_touchline +
                    self.goal_depth
                ),
                self.pitch_width / 2.0
            ]
        })

        return pitch_apron_df


class Touchline(BaseSoccerFeature):
    """The touchline of the pitch, aka the sideline.

    These are the lines that run the full length of the pitch
    """

    def _get_centered_feature(self):
        """Generate the points comprising the touchline.

        The line thickness will be uniform for all features on the pitch
        """
        touchline_df = self.create_rectangle(
            x_min = -self.pitch_length / 2.0,
            x_max = self.pitch_length / 2.0,
            y_min = -self.feature_thickness,
            y_max = 0.0
        )

        return touchline_df


class GoalLine(BaseSoccerFeature):
    """The goal line of the pitch, aka the endlines.

    These are the lines that run the full width of the pitch. The ball must
    completely cross the goal line to score a goal
    """

    def _get_centered_feature(self):
        """Generate the points comprising the goal line.

        The line thickness will be uniform for all features on the pitch
        """
        goal_line_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = -self.pitch_width / 2.0,
            y_max = self.pitch_width / 2.0
        )

        return goal_line_df


class CornerArc(BaseSoccerFeature):
    """The arc in each corner of the pitch.

    These are quarter-circles located where the touchline meets the goal line
    """

    def _get_centered_feature(self):
        """Generate the points comprising the corner arc.

        These arcs have the same thickness as the rest of the lines on the
        pitch
        """
        corner_arc_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = 1.0,
                end = 1.5,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5,
                end = 1.0,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return corner_arc_df


class HalfwayLine(BaseSoccerFeature):
    """The halfway line of the pitch, aka the midfield line or center line.

    This is the line that run the full width of the pitch
    """

    def _get_centered_feature(self):
        """Generate the points comprising the halfway line.

        The line thickness will be uniform for all features on the pitch
        """
        halfway_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.pitch_width / 2.0,
            y_max = self.pitch_width / 2.0
        )

        return halfway_line_df


class CenterCircle(BaseSoccerFeature):
    """The center circle on the pitch.

    The given radius should be to the outside of the circle.
    """

    def _get_centered_feature(self):
        """Generate the points comprising the center circle.

        The line thickness will be uniform for all features on the pitch
        """
        center_circle_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return center_circle_df


class PenaltyBox(BaseSoccerFeature):
    """The penalty box.

    This is usually the 16.5 m (18 yd) box, but may be parameterized

    Attributes
    ----------
    box_length : float
        The length of the penalty box in TV view. This is the larger of the two
        boxes, and is usually 16.5 m (18 yards) from the back edge of the goal
        line

    half_box_width : float
        Half the width of the penalty box

    penalty_mark_dist : float
        The distance from the back edge of the goal line to the center of the
        penalty mark
    """

    def __init__(self, box_length = 0.0, penalty_mark_dist = 0.0,
                 goal_width = 0.0, goal_post_to_box_edge = 0.0, *args,
                 **kwargs):
        # Initialize the attributes unique to this feature
        self.box_length = box_length
        self.half_box_width = (goal_width / 2.0) + goal_post_to_box_edge
        self.penalty_mark_dist = penalty_mark_dist
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the penalty box.

        This draws a half-box, which will include the circular portion at the
        top of the box. All dimensions given should be to the outside of the
        features
        """
        # Start by getting the angle at which to start the penalty arc
        try:
            x_out = self.box_length - self.penalty_mark_dist
            r_inner = self.feature_radius - self.feature_thickness
            start_angle_outer = math.acos(x_out / self.feature_radius) / np.pi
            start_angle_inner = math.acos(x_out / r_inner) / np.pi
            start_angle_outer = 1.0 - start_angle_outer
            start_angle_inner = 1.0 - start_angle_inner

        except ZeroDivisionError:
            start_angle_outer = 0.5
            start_angle_inner = 0.5

        penalty_box_df = pd.concat([
            pd.DataFrame({
                "x": [-self.feature_thickness, -self.box_length],
                "y": [self.half_box_width, self.half_box_width]
            }),

            self.create_circle(
                center = (-self.penalty_mark_dist, 0.0),
                start = start_angle_outer,
                end = 1.0,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (-self.penalty_mark_dist, 0.0),
                start = 1.0,
                end = start_angle_inner,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                "x": [
                    -self.box_length,
                    -(self.box_length - self.feature_thickness),
                    -(self.box_length - self.feature_thickness),
                    -self.feature_thickness,
                    -self.feature_thickness
                ],

                "y": [
                    0.0,
                    0.0,
                    self.half_box_width - self.feature_thickness,
                    self.half_box_width - self.feature_thickness,
                    self.half_box_width
                ]
            })
        ])

        return penalty_box_df


class GoalBox(BaseSoccerFeature):
    """The goal box.

    This is usually the 5.5 m (6 yd) box, but may be parameterized

    Attributes
    ----------
    box_length : float
        The length of the goal box in TV view. This is the smaller of the two
        boxes, and is usually 5.5 m (6 yards) from the back edge of the goal
        line

    half_box_width : float
        Half the width of the goal box
    """

    def __init__(self, box_length = 0.0, goal_width = 0.0,
                 goal_post_to_box_edge = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.box_length = box_length
        self.half_box_width = (goal_width / 2.0) + goal_post_to_box_edge
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the goal box.

        This box should be the closer of the two drawn boxes to the goal
        """
        goal_box_df = pd.DataFrame({
            "x": [
                -self.feature_thickness,
                -self.box_length,
                -self.box_length,
                -self.feature_thickness,
                -self.feature_thickness,
                -(self.box_length - self.feature_thickness),
                -(self.box_length - self.feature_thickness),
                -self.feature_thickness,
                -self.feature_thickness
            ],

            "y": [
                self.half_box_width,
                self.half_box_width,
                -self.half_box_width,
                -self.half_box_width,
                -(self.half_box_width - self.feature_thickness),
                -(self.half_box_width - self.feature_thickness),
                self.half_box_width - self.feature_thickness,
                self.half_box_width - self.feature_thickness,
                self.half_box_width
            ]
        })

        return goal_box_df


class CenterMark(BaseSoccerFeature):
    """The center mark on the pitch.

    This is where the kickoffs for each half, as well as following any goal,
    are taken
    """

    def _get_centered_feature(self):
        """Generate the points comprising the center mark.

        The given radius should be to the outside of the mark.
        """
        center_mark_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return center_mark_df


class PenaltyMark(BaseSoccerFeature):
    """The penalty mark.

    This is the center point for arc of the penalty box, as well as where any
    penalty kick is taken
    """

    def _get_centered_feature(self):
        """Generate the points comprising the penalty mark.

        The penalty mark is assumed to be circular
        """
        penalty_mark_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return penalty_mark_df


class CornerDefensiveMark(BaseSoccerFeature):
    """The corner defensive marks.

    These are optional marks on the pitch, located 9.15 m (10 yd) from the
    corner of the pitch. Defenders should be beyond these marks (either more
    towards the goal or more towards the halfway line) during corner kicks

    Attributes
    ----------
    is_touchline : bool
        Whether or not the corner defensive mark is along the touchline

    is_goal_line : bool
        Whether or not the corner defensive mark is along the goal line

    depth : float
        The depth (in any direction) of the defensive marks beyond the goal
        line or touchline

    separation_from_line : float
        The distance from the exterior edge of the goal line to the interior
        edge of the defensive mark
    """

    def __init__(self, is_touchline = False, is_goal_line = False, depth = 0.0,
                 separation_from_line = 0.0, *args, **kwargs):
        self.is_touchline = is_touchline
        self.is_goal_line = is_goal_line
        self.depth = depth
        self.separation_from_line = separation_from_line
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the corner defensive marks.

        These marks should be outside the field of play
        """
        if self.is_touchline:
            corner_defensive_mark_df = self.create_rectangle(
                x_min = -self.feature_thickness / 2.0,
                x_max = self.feature_thickness / 2.0,
                y_min = self.separation_from_line,
                y_max = self.separation_from_line + self.depth
            )

        if self.is_goal_line:
            corner_defensive_mark_df = self.create_rectangle(
                x_min = self.separation_from_line,
                x_max = self.separation_from_line + self.depth,
                y_min = -self.feature_thickness / 2.0,
                y_max = self.feature_thickness / 2.0
            )

        return corner_defensive_mark_df


class Goal(BaseSoccerFeature):
    """The goal.

    The goals located beyond each goal line.

    Attributes
    ----------
    goal_width : float
        The interior distance between the goal posts

    goal_depth : float
        The depth of the goal from the back edge of the goal line
    """

    def __init__(self, goal_width = 0.0, goal_depth = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.goal_width = goal_width
        self.goal_depth = goal_depth
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the goal frame.

        By rule, the goal posts must be the same thickness as the goal line,
        and the posts must rest on the front edge of the goal line
        """
        goal_frame_df = pd.DataFrame({
            "x": [
                0.0,
                self.goal_depth + self.feature_thickness,
                self.goal_depth + self.feature_thickness,
                0.0,
                0.0,
                self.goal_depth,
                self.goal_depth,
                0.0,
                0.0
            ],

            "y": [
                (self.goal_width / 2.0) + self.feature_thickness,
                (self.goal_width / 2.0) + self.feature_thickness,
                -((self.goal_width / 2.0) + self.feature_thickness),
                -((self.goal_width / 2.0) + self.feature_thickness),
                -self.goal_width / 2.0,
                -self.goal_width / 2.0,
                self.goal_width / 2.0,
                self.goal_width / 2.0,
                (self.goal_width / 2.0) + self.feature_thickness
            ]
        })

        return goal_frame_df
