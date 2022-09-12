"""Extensions of the ``BaseFeature`` class to be specific to ice hockey rinks.

The features are all parameterized by the basic characteristics of an ice rink.
A user can manually specify their own rink parameters in the ``HockeyRink``
class that will adjust the placement of these features, however the features
themselves will be consistent across all hockey surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseHockeyFeature(BaseFeature):
    """An extension of the ``BaseFeature`` class for hockey features.

    The following attributes are specific to hockey features only. For more
    information on inherited attributes, please see the ``BaseFeature`` class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
    rink_length : float
        The length of the rink in TV view. The default is ``0.0``

    rink_width : float
        The width of the rink in TV view. The default is ``0.0``

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

    def __init__(self, rink_length = 0.0, rink_width = 0.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = "ft", *args, **kwargs):

        # Set the full-sized dimensions of the rink
        self.rink_length = rink_length
        self.rink_width = rink_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class Boards(BaseHockeyFeature):
    """A parameterization of the boards of a hockey rink.

    The method below specifies one half of the rink's boards. The rest of the
    boards are produced via a reflection over the x-axis when viewing the rink
    in TV view.

    The rink's boards are rounded in the arc of a circle of a specified radius,
    so the x and y coordinates of its center must be taken and shifted to their
    correct location on the ice surface
    """

    def _get_centered_feature(self):
        """Generate the coordinates of a hockey rink's boards.

        The boards are comprised of a closed polygon of defined thickness via
        the board_thickness attribute
        """
        # Specify the half-dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find the point to use as the center of the circle with the given
        # radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Create the points along the corner arc's inner radii
        arc_inner_upper = self.create_circle(
            center = (center_x, center_y),
            start = 0.5,
            end = 0.0,
            r = self.feature_radius
        )

        arc_inner_lower = self.create_circle(
            center = (center_x, -center_y),
            start = 0.0,
            end = -0.5,
            r = self.feature_radius
        )

        # Calculate the corner arc's outer radius
        arc_outer_upper = self.create_circle(
            center = (center_x, center_y),
            start = 0.0,
            end = 0.5,
            r = self.feature_radius + self.feature_thickness
        )

        arc_outer_lower = self.create_circle(
            center = (center_x, -center_y),
            start = -0.5,
            end = 0.0,
            r = self.feature_radius + self.feature_thickness
        )

        # Combine the boards' inner and outer arcs with its guaranteed
        # coordinates
        boards_df = pd.concat([
            # Start at the top of the rink in TV view tih the boards' inner
            # boundary
            pd.DataFrame({
                "x": [0.0],
                "y": [half_width]
            }),

            # Then add in its upper innner arc
            arc_inner_upper,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                "x": [half_length],
                "y": [0.0]
            }),

            # Then its lower inner arc
            arc_inner_lower,

            # Then go to the bottom of the rink in TV view with the boards'
            # inner boundary before flipping to the outer boundary
            pd.DataFrame({
                "x": [0.0, 0.0],
                "y": [-half_width, -half_width - self.feature_thickness]
            }),

            # Back to the lower arc on the outer boundary
            arc_outer_lower,

            # Then back to the middle
            pd.DataFrame({
                "x": [half_length + self.feature_thickness],
                "y": [0.0]
            }),

            # Then back to the upper arc
            arc_outer_upper,

            # Finally back to the top and original starting point
            pd.DataFrame({
                "x": [0.0, 0.0],
                "y": [half_width + self.feature_thickness, half_width]
            })
        ])

        return boards_df


class BoardsConstraint(BaseHockeyFeature):
    """A parameterization of the constraint of the boards of a hockey rink.

    This corresponds to the inner edges of the boards and is used to constrain
    other features from extending beyond the inner boundary of the ice rink.

    Unlike the Boards class (defined above), this feature is designed to
    function over the entire surface of an ice rink
    """

    def _get_centered_feature(self):
        """Generate the coordinates that constrain a hockey rink's interior.

        As stated in the above class documentation, this corresponds only to
        the interior edge of the boards
        """
        # Define the length and width of the rink as length and width
        # attributes. These will be used to constrain plotted points to be
        # defined inside the surface
        self.length = self.rink_length
        self.width = self.rink_width

        # Specify the half-dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find the point to use as the center of the circle with the given
        # radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Create the points along the corner arc's inner radii
        arc_upper_right = self.create_circle(
            center = (center_x, center_y),
            start = 0.5,
            end = 0.0,
            r = self.feature_radius
        )

        arc_lower_right = self.create_circle(
            center = (center_x, -center_y),
            start = 0.0,
            end = -0.5,
            r = self.feature_radius
        )

        arc_lower_left = self.create_circle(
            center = (-center_x, -center_y),
            start = -0.5,
            end = -1.0,
            r = self.feature_radius
        )

        arc_upper_left = self.create_circle(
            center = (-center_x, center_y),
            start = 1.0,
            end = 0.5,
            r = self.feature_radius
        )

        # Combine the boards' inner and outer arcs with its guaranteed
        # coordinates
        boards_constraint_df = pd.concat([
            # Start at the top of the rink in TV view with the boards' inner
            # boundary
            pd.DataFrame({
                "x": [0.0],
                "y": [half_width]
            }),

            # Then add in its upper right corner
            arc_upper_right,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                "x": [half_length],
                "y": [0.0]
            }),

            # Then its lower right corner
            arc_lower_right,

            # Then go to the bottom of the rink in TV view
            pd.DataFrame({
                "x": [0.0],
                "y": [-half_width]
            }),

            # Now continue to the lower left corner
            arc_lower_left,

            # Then back to the middle
            pd.DataFrame({
                "x": [-half_length],
                "y": [0.0]
            }),

            # Then the upper left corner
            arc_upper_left,

            # Finally back to the top and original starting point
            pd.DataFrame({
                "x": [0.0],
                "y": [half_width]
            })
        ])

        return boards_constraint_df


class DefensiveZone(BaseHockeyFeature):
    """A parameterization of the defensive zone of a hockey rink.

    The offensive zone is the left "third" of the rink in TV view. This is the
    area that a team defends when attacking from left to right

    Attributes
    ----------
    nzone_length : float
        The length of the neutral zone, measured from the interior edges of the
        zone lines (blue lines)
    """

    def __init__(self, nzone_length = 0.0, *args, **kwargs):
        # Set the length of the neutral zone
        self.nzone_length = nzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that define the defensive zone.

        The defensive zone is rectangular in shape with rounded corners (that
        will be constrained by the boards), and is usually white in color
        """
        # Specify the dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find where the point to use as the center of the circle with the
        # given radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Calculate the corner arc's inner radius
        arc_inner_upper = self.create_circle(
            center = (-center_x, center_y),
            start = 0.5,
            end = 1.0,
            r = self.feature_radius
        )

        arc_inner_lower = self.create_circle(
            center = (-center_x, -center_y),
            start = 1.0,
            end = 1.5,
            r = self.feature_radius
        )

        dzone_df = pd.concat([
            # Start at the upper right corner of the zone line that is closest
            # to center ice
            pd.DataFrame({
                "x": [-self.nzone_length / 2.0],
                "y": [half_width]
            }),

            # Then draw the upper left arc of the boards
            arc_inner_upper,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                "x": [-half_length],
                "y": [0.0]
            }),

            # Then the lower left arc
            arc_inner_lower,

            # Then go to the bottom of the rink in TV view with the boards'
            # inner boundary before closing the path by returning to the
            # starting point
            pd.DataFrame({
                "x": [-self.nzone_length / 2.0, -self.nzone_length / 2.0],
                "y": [-half_width, half_width]
            })
        ])

        return dzone_df


class NeutralZone(BaseHockeyFeature):
    """A parameterization of the neutral zone of a hockey rink.

    The neutral zone is the middle "third" of the rink. This is the area
    between the two zone (blue) lines. The center of the neutral zone should
    lie along the line ``x = 0``
    """

    def _get_centered_feature(self):
        """Generate the coordinates that define the neutral zone.

        The zone is rectangular in shape, and usually is white in color. Note:
        because of the way the neutral zone is created below, ``reflect_x`` and
        ``reflect_y`` in the ``HockeyRink`` class should both be set to
        ``False``
        """
        # Generate the points of the neutral zone. This is a rectangular region
        # with known dimensions (from the passed parameters), so no reflection
        # is required
        nzone_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.rink_width / 2.0,
            y_max = self.rink_width / 2.0
        )

        return nzone_df


class OffensiveZone(BaseHockeyFeature):
    """A parameterization of the offensive zone of a hockey rink.

    The offensive zone is the right "third" of the rink in TV view. This is the
    area that a team attacks to try to score a goal when attacking from left to
    right

    Attributes
    ----------
    nzone_length : float
        The length of the neutral zone, measured from the interior edges of the
        zone lines (blue lines)
    """

    def __init__(self, nzone_length = 0.0, *args, **kwargs):
        # Set the length of the neutral zone
        self.nzone_length = nzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that define the offensive zone.

        The offensive zone is rectangular in shape with rounded corners (that
        will be constrained by the boards), and is usually white in color
        """
        # Specify the dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find where the point to use as the center of the circle with the
        # given radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Create the points along the corner arc's inner radii
        arc_inner_upper = self.create_circle(
            center = (center_x, center_y),
            start = 0.5,
            end = 0.0,
            r = self.feature_radius
        )

        arc_inner_lower = self.create_circle(
            center = (center_x, -center_y),
            start = 0.0,
            end = -0.5,
            r = self.feature_radius
        )

        ozone_df = pd.concat([
            # Start at the upper left corner of the zone line that is closest
            # to center ice
            pd.DataFrame({
                "x": [self.nzone_length / 2.0],
                "y": [half_width]
            }),

            # Then draw the upper right corner of the boards
            arc_inner_upper,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                "x": [half_length],
                "y": [0.0]
            }),

            # Then the lower right corner
            arc_inner_lower,

            # Then go to the bottom of the rink in TV view with the boards'
            # inner boundary before closing the path by returning to the
            # starting point
            pd.DataFrame({
                "x": [self.nzone_length / 2.0, self.nzone_length / 2.0],
                "y": [-half_width, half_width]
            })
        ])

        return ozone_df


class CenterLine(BaseHockeyFeature):
    """A parameterization of the center line of a hockey rink.

    The center line is the line that divides the ice surface in half. Its
    center should lie directly in the center of the ice surface. Its line
    thickness should be given by ``major_line_thickness`` as this is a major
    line on the ice surface

    Attributes
    ----------
    center_faceoff_spot_gap : float
        The gap in the center line that surrounds the center faceoff spot. This
        is measured between the inner edges of the two halves of the center
        line
    """
    def __init__(self, center_faceoff_spot_gap = 0.0, *args, **kwargs):
        # Initialize the parameters unique to this feature
        self.center_faceoff_spot_gap = center_faceoff_spot_gap
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the center line.

        The line is rectangular in shape, and usually red in color
        """
        # Generate the points defining the center line
        center_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = self.center_faceoff_spot_gap / 2.0,
            y_max = self.rink_width / 2.0
        )

        return center_line_df


class RefereeCrease(BaseHockeyFeature):
    """A parameterization of the referee's crease.

    The referee's crease is a semi-circle on the "bottom" of the boards (in TV
    view), centered on the line ``y = 0`` (the center of the center line)
    """

    def _get_centered_feature(self):
        """Generate the points defining the referee's crease.

        The crease is semi-circular in shape. Its thickness should be given by
        ``minor_line_thickness``, and it's usually red in color
        """
        referee_crease_df = pd.concat([
            pd.DataFrame({
                "x": [self.feature_radius],

                "y": [0.0]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 0.0,
                end = 1.0,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    -self.feature_radius,
                    -self.feature_radius + self.feature_thickness
                ],

                "y": [
                    0.0,
                    0.0
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.0,
                end = 0.0,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                "x": [
                    self.feature_radius,
                ],

                "y": [
                    0.0
                ]
            })
        ])

        return referee_crease_df


class CenterFaceoffSpot(BaseHockeyFeature):
    """A parameterization of the center faceoff spot of a hockey rink.

    The center faceoff spot is the spot at which the game begins. Its center
    should lie directly in the center of the ice surface. Its radius is passed
    as a key in ``rink_params``
    """

    def _get_centered_feature(self):
        """Generate the points that define the center faceoff spot.

        The spot is perfectly round and filled in as a solid circle, and is
        usually dark blue in color
        """
        faceoff_spot_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return faceoff_spot_df


class ZoneLine(BaseHockeyFeature):
    """A parameterization of the zone lines of a hockey rink.

    The zone lines are the lines that separate the neutral zone from the
    offensive and defensive zones. Its line thickness should be given by
    ``major_line_thickness`` as this is a major line on the ice surface
    """

    def _get_centered_feature(self):
        """Generate the points defining the zone line.

        The line is rectangular in shape, and usually dark blue in color
        """
        # Generate the points defining the zone line
        zone_line_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = -self.rink_width / 2.0,
            y_max = self.rink_width / 2.0
        )

        return zone_line_df


class GoalLine(BaseHockeyFeature):
    """A parameterization of the goal lines of a hockey rink.

    The goal lines are the lines over which a puck must cross (within the goal
    frame) in order to be considered a goal. Its line thickness should be given
    by ``minor_line_thickness`` as this is a minor line on the ice surface
    """

    def _get_centered_feature(self):
        """Generate the points defining the goal line.

        This draws the right-side goal line (in TV view), starting with its
        left edge. This also accounts for a perfectly rectangular goal line if
        a user supplies a value that necessitates one. The line is rectangular
        in shape with rounded ends, and usually red in color
        """
        # Specify the half-dimension of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find the point to use as the center of the circle with the given
        # radius for the boards' corners' arc
        corner_arc_center_x = half_length - self.feature_radius
        corner_arc_center_y = half_width - self.feature_radius

        # First, check to see if the goal line will intersect the corner of the
        # rink. Usually, it will, but in case a user supplies a value where
        # this is not the case, this check will accomodate. The absolute value
        # is used here to always force the calculation to be done for the right
        # side of the ice (in TV view), which will be adjusted as necessary in
        # the feature's _translate_feature() method
        max_x = abs(self.x_anchor) + (self.feature_thickness / 2.0)

        # If the maximum value of x is going to be less than the x coordinate
        # of the center of the corner's arc, then the feature should be a
        # rectangle
        if max_x <= corner_arc_center_x:
            goal_line_df = self.create_rectangle(
                x_min = -self.feature_thickness / 2.0,
                x_max = self.feature_thickness / 2.0,
                y_min = -half_width,
                y_max = half_width
            )

            return goal_line_df

        # Otherwise, more calculation is necessary
        else:
            # The starting x position should be the left-hand edge of the
            # right-side goal line
            base_x = abs(self.x_anchor) - corner_arc_center_x
            start_x = base_x - (self.feature_thickness / 2.0)
            end_x = base_x + (self.feature_thickness / 2.0)

            # Finally, compute the starting and ending angles by taking the
            # inverse sine of the starting and ending x positions, then
            # dividing by the corner's radius. Divide by pi to ensure that the
            # angles are correctly passed to the self.create_circle() method
            # NOTE: this does not need a special ZeroDivisionError handling
            # since the feature radius and corner_arc_center_x parameters
            # work in concert with each other
            theta_start = math.asin(start_x / self.feature_radius) / np.pi
            theta_end = math.asin(end_x / self.feature_radius) / np.pi

            # Now create the feature's data frame
            goal_line_df = pd.concat([
                self.create_circle(
                    center = (corner_arc_center_x, corner_arc_center_y),
                    start = 0.5 - theta_start,
                    end = 0.5 - theta_end,
                    r = self.feature_radius
                ),

                self.create_circle(
                    center = (corner_arc_center_x, -corner_arc_center_y),
                    start = -0.5 + theta_end,
                    end = -0.5 + theta_start,
                    r = self.feature_radius
                )
            ])

            # To properly position the goal line, the x coordinate needs to be
            # brought back to x = 0 so that it can be re-anchored when
            # generated. See note above for an explanation of why the absolute
            # value is used here
            goal_line_df["x"] = goal_line_df["x"] - abs(self.x_anchor)

            return goal_line_df


class GoalCreaseOutline(BaseHockeyFeature):
    """A parameterization of the goal crease's outline.

    The goal crease is the area where a goaltender plays their position. It is
    comprised of two components: the outline of the crease, and the filling in
    its boundary (see documentation for ``GoalCreaseFill`` class). The goal
    crease may have two notches (one on each side of the line ``y = 0``).

    Attributes
    ----------
    crease_length : float
        The distance from the center of the goal line to the start of the arc
        of the goal crease

    crease_width : float
        The exterior width of the goal crease

    notch_dist_x : float
        The distance from the center of the goal line to the notch (if one
        exists) in the goal crease

    notch_width : float
        The width of the notch (if one exists) in the goal crease

    crease_style : str
        The style of goal crease to implement. Viable options are:
            - nhl98 : the current iteration of the NHL goal crease. This is
                what is used for most professional leagues

            - nhl92 : the previous iteration of an NHL goal crease. It is drawn
                as a semi-circle with two L-shaped notches at the edge of the
                crease intersecting the semi-circle

            - ushl1 : the current iteration of a USA Hockey goal crease. This
                is what is currently used in the USHL (United States Hockey
                League)
    """

    def __init__(self, crease_style = "", crease_length = 0.0,
                 crease_width = 0.0, notch_dist_x = 0.0, notch_width = 0.0,
                 *args, **kwargs):
        # Set the parameters about the crease's outline notches, as well as its
        # length, width, and style
        self.crease_length = crease_length
        self.crease_width = crease_width
        self.notch_dist_x = notch_dist_x
        self.notch_width = notch_width
        self.crease_style = crease_style
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the goal crease's outline.

        The outline of the goal crease should have thickness given by
        ``minor_line_thickness", as this is a minor line on the ice surface,
        and the outline is usually red in color.
        """
        # Start by getting the half-width of the crease
        half_crease_width = self.crease_width / 2.0

        # Calculate the starting angle theta of the goal crease's rounded front
        # by taking the inverse cosine of its half-width and dividing it by the
        # radius of the arc
        try:
            theta = (
                (math.acos(half_crease_width / self.feature_radius)) / np.pi
            )
        except ZeroDivisionError:
            theta = 0.0

        # nhl98 crease style: cut-off semi-circle (utilized in most North
        # American leagues, e.g. NHL, AHL)
        if self.crease_style.lower() == "nhl98":
            goal_crease_outline_df = pd.concat([
                pd.DataFrame({
                    "x": [0.0, -self.crease_length],
                    "y": [half_crease_width, half_crease_width]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5 + theta,
                    end = 1.5 - theta,
                    r = self.feature_radius
                ),

                pd.DataFrame({
                    "x": [
                        -self.crease_length,
                        0.0,
                        0.0,
                        -self.notch_dist_x,
                        -self.notch_dist_x,
                        -(self.notch_dist_x + self.feature_thickness),
                        -(self.notch_dist_x + self.feature_thickness)
                    ],

                    "y": [
                        -half_crease_width,
                        -half_crease_width,
                        -half_crease_width + self.feature_thickness,
                        -half_crease_width + self.feature_thickness,
                        (
                            -half_crease_width +
                            self.feature_thickness +
                            self.notch_width
                        ),
                        (
                            -half_crease_width +
                            self.feature_thickness +
                            self.notch_width
                        ),
                        -half_crease_width + self.feature_thickness
                    ]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 1.5 - theta,
                    end = 0.5 + theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        -(self.notch_dist_x + self.feature_thickness),
                        -(self.notch_dist_x + self.feature_thickness),
                        -self.notch_dist_x,
                        -self.notch_dist_x,
                        0.0,
                        0.0
                    ],

                    "y": [
                        half_crease_width - self.feature_thickness,
                        (
                            half_crease_width -
                            self.feature_thickness -
                            self.notch_width
                        ),
                        (
                            half_crease_width -
                            self.feature_thickness -
                            self.notch_width
                        ),
                        half_crease_width - self.feature_thickness,
                        half_crease_width - self.feature_thickness,
                        half_crease_width
                    ]
                })
            ])

        # ushl1 crease style: full semi-circle with NHL-style crease in the
        # interior; only NHL-style crease is painted light blue
        elif self.crease_style.lower() == "ushl1":
            goal_crease_outline_df = pd.concat([
                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5,
                    end = 1.5,
                    r = self.feature_radius
                ),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 1.5,
                    end = 1.5 - theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        -self.notch_dist_x,
                        0.0,
                        0.0,
                        -(self.notch_dist_x + self.feature_thickness),
                        -(self.notch_dist_x + self.feature_thickness),
                        -self.notch_dist_x,
                        -self.notch_dist_x
                    ],

                    "y": [
                        -half_crease_width,
                        -half_crease_width,
                        -half_crease_width + self.feature_thickness,
                        -half_crease_width + self.feature_thickness,
                        (
                            -half_crease_width +
                            self.feature_thickness +
                            self.notch_width
                        ),
                        (
                            -half_crease_width +
                            self.feature_thickness +
                            self.notch_width
                        ),
                        -half_crease_width
                    ]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 1.5 - theta,
                    end = 0.5 + theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        -self.notch_dist_x,
                        -self.notch_dist_x,
                        -(self.notch_dist_x + self.feature_thickness),
                        -(self.notch_dist_x + self.feature_thickness),
                        0.0,
                        0.0,
                        -self.notch_dist_x
                    ],

                    "y":[
                        half_crease_width,
                        (
                            half_crease_width -
                            self.notch_width -
                            self.feature_thickness
                        ),
                        (
                            half_crease_width -
                            self.notch_width -
                            self.feature_thickness
                        ),
                        half_crease_width - self.feature_thickness,
                        half_crease_width - self.feature_thickness,
                        half_crease_width,
                        half_crease_width
                    ]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5 + theta,
                    end = 0.5,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        0.0,
                        0.0
                    ],

                    "y": [
                        self.feature_radius - self.feature_thickness,
                        self.feature_radius
                    ]
                })
            ])

        # nhl92 crease style: full semi-circle outline with two L-shaped marks
        # adjoining the semi-circle, but not extending back towards the goal
        # line
        elif self.crease_style.lower() == "nhl92":
            goal_crease_outline_df = pd.concat([
                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5,
                    end = 1.5,
                    r = self.feature_radius
                ),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 1.5,
                    end = 1.5 - theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        -self.notch_dist_x,
                        -self.notch_dist_x + self.notch_width,
                        -self.notch_dist_x + self.notch_width,
                        -(self.notch_dist_x + self.feature_thickness),
                        -(self.notch_dist_x + self.feature_thickness),
                        -self.notch_dist_x,
                        -self.notch_dist_x
                    ],

                    "y": [
                        -half_crease_width,
                        -half_crease_width,
                        -half_crease_width + self.feature_thickness,
                        -half_crease_width + self.feature_thickness,
                        (
                            -half_crease_width +
                            self.feature_thickness +
                            self.notch_width
                        ),
                        (
                            -half_crease_width +
                            self.feature_thickness +
                            self.notch_width
                        ),
                        -half_crease_width
                    ]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 1.5 - theta,
                    end = 0.5 + theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        -self.notch_dist_x,
                        -self.notch_dist_x,
                        -(self.notch_dist_x + self.feature_thickness),
                        -(self.notch_dist_x + self.feature_thickness),
                        -self.notch_dist_x + self.notch_width,
                        -self.notch_dist_x + self.notch_width,
                        -self.notch_dist_x
                    ],

                    "y":[
                        half_crease_width,
                        (
                            half_crease_width -
                            self.notch_width -
                            self.feature_thickness
                        ),
                        (
                            half_crease_width -
                            self.notch_width -
                            self.feature_thickness
                        ),
                        half_crease_width - self.feature_thickness,
                        half_crease_width - self.feature_thickness,
                        half_crease_width,
                        half_crease_width
                    ]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5 + theta,
                    end = 0.5,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [
                        0.0,
                        0.0
                    ],

                    "y": [
                        self.feature_radius - self.feature_thickness,
                        self.feature_radius
                    ]
                })
            ])

        else:
            goal_crease_outline_df = pd.DataFrame({
                "x": [0.0],
                "y": [0.0]
            })

        return goal_crease_outline_df


class GoalCreaseFill(BaseHockeyFeature):
    """A parameterization of the goal crease's filling.

    The goal crease is the area where a goaltender plays their position. It is
    comprised of two components: the outline of the crease (see documentation
    for ``GoalCreaseOutline`` class), and the filling in its boundary. The goal
    crease may have two notches (one on each side of the line ``y = 0``).

    Attributes
    ----------
    crease_length : float
        The distance from the center of the goal line to the start of the arc
        of the goal crease

    crease_width : float
        The exterior width of the goal crease

    notch_dist_x : float
        The distance from the center of the goal line to the notch (if one
        exists) in the goal crease

    notch_width : float
        The width of the notch (if one exists) in the goal crease

    crease_style : str
        The style of goal crease to implement. Viable options are:
            - nhl98 : the current iteration of the NHL goal crease. This is
                what is used for most professional leagues

            - nhl92 : the previous iteration of an NHL goal crease. It is drawn
                as a semi-circle with two L-shaped notches at the edge of the
                crease intersecting the semi-circle

            - ushl1 : the current iteration of a USA Hockey goal crease. This
                is what is currently used in the USHL (United States Hockey
                League)
    """

    def __init__(self, crease_style = "", crease_length = 0.0,
                 crease_width = 0.0, notch_dist_x = 0.0, notch_width = 0.0,
                 *args, **kwargs):
        # Set the parameters about the crease's outline notches, as well as its
        # length and width
        self.crease_length = crease_length
        self.crease_width = crease_width
        self.notch_dist_x = notch_dist_x
        self.notch_width = notch_width
        self.crease_style = crease_style
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the goal crease's outline.

        The filling of the goal crease should have thickness given by
        ``minor_line_thickness", as this refers to the crease's outline, which
        is a minor line on the ice surface. The goal crease's filling is
        usually light in color.
        """
        # Start by getting the half-width of the crease
        half_crease_width = self.crease_width / 2.0

        # Calculate the starting angle theta of the goal crease's rounded front
        # by taking the inverse cosine of its half-width and dividing it by the
        # radius of the arc
        try:
            theta = (
                (math.acos(half_crease_width / self.feature_radius)) / np.pi
            )
        except ZeroDivisionError:
            theta = 0.0

        if self.crease_style.lower() == "nhl98":
            goal_crease_fill_df = pd.concat([
                pd.DataFrame({
                    "x": [0.0],
                    "y": [half_crease_width - self.feature_thickness]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5 + theta,
                    end = 1.5 - theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [0.0],
                    "y": [-half_crease_width + self.feature_thickness]
                })
            ])

        elif self.crease_style.lower() == "ushl1":
            goal_crease_fill_df = pd.concat([
                pd.DataFrame({
                    "x": [0.0],
                    "y": [half_crease_width - self.feature_thickness]
                }),

                self.create_circle(
                    center = (0.0, 0.0),
                    start = 0.5 + theta,
                    end = 1.5 - theta,
                    r = self.feature_radius - self.feature_thickness
                ),

                pd.DataFrame({
                    "x": [0.0],
                    "y": [-half_crease_width + self.feature_thickness]
                })
            ])

        elif self.crease_style.lower() == "nhl92":
            goal_crease_fill_df = self.create_circle(
                center = (0.0, 0.0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius - self.feature_thickness
            )

        else:
            goal_crease_fill_df = pd.DataFrame({
                "x": [0.0],
                "y": [0.0]
            })

        return goal_crease_fill_df


class GoaltendersRestrictedArea(BaseHockeyFeature):
    """A parameterization of the goaltender's restricted area of a hockey rink.

    The goaltender's restricted area marks where a goaltender is legally
    allowed to handle the puck behind the net. This is often referred to as
    "the trapezoid" as it is trapezoidal in shape. Its line thickness should be
    given by ``minor_line_thickness`` as this is a minor line on the ice
    surface.

    NOTE: This is not a requirement in all leagues, and may be omitted via the
    ``has_trapezoid`` key in the ``rink_params`` passed to the ``HockeyRink``
    class

    Attributes
    ----------
    short_base_width : float
        The exterior base-width of the trapezoid (should it exist) that
        along the goal line

    long_base_width : float
        The exterior base-width of the trapezoid (should it exist) that lies
        along the boards
    """

    def __init__(self, short_base_width = 0.0, long_base_width = 0.0, *args,
                 **kwargs):
        # Set the short and long base widths of the trapezoid. These should be
        # provided as the exterior dimensions
        self.short_base_width = short_base_width
        self.long_base_width = long_base_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the goaltender's restricted area.

        This draws the goaltender's restricted area on the right side
        (in TV view) of the ice surface. The figure is composed of lines that
        outline a trapezoid in shape, and is usually red in color
        """
        # Start by defining the half-widths of both the short and long bases of
        # the trapezoid
        half_short_base_width = self.short_base_width / 2.0
        half_long_base_width = self.long_base_width / 2.0

        # Now trace out the trapezoid. NOTE: The absolute value is used here to
        # always force the calculation to be done for the right side of the ice
        # (in TV view), which will be adjusted as necessary in the feature's
        # _translate_feature() method
        trapezoid_df = pd.DataFrame({
            "x": [
                abs(self.x_anchor),
                self.rink_length / 2.0,
                self.rink_length / 2.0,
                abs(self.x_anchor) - (self.feature_thickness / 2.0),
                abs(self.x_anchor) - (self.feature_thickness / 2.0),
                self.rink_length / 2.0,
                self.rink_length / 2.0,
                abs(self.x_anchor),
                abs(self.x_anchor)
            ],

            "y": [
                half_short_base_width,
                half_long_base_width,
                half_long_base_width - self.feature_thickness,
                half_short_base_width - self.feature_thickness,
                -half_short_base_width + self.feature_thickness,
                -half_long_base_width + self.feature_thickness,
                -half_long_base_width,
                -half_short_base_width,
                half_short_base_width
            ]
        })

        # See note above for an explanation of why the absolute value is used
        # here
        trapezoid_df["x"] = trapezoid_df["x"] - abs(self.x_anchor)

        return trapezoid_df


class CenterFaceoffCircle(BaseHockeyFeature):
    """A parameterization of the faceoff circle at the center of a hockey rink.

    The center faceoff circle is where the each period of the game begins. It
    differs from the non-centered faceoff circles in that there are no
    adjoining hash marks on this circle. It is also a different color than the
    non-centered faceoff circles. Its line thickness should be given by
    ``minor_line_thickness`` as this is a minor line on the ice surface
    """

    def _get_centered_feature(self):
        """Generate the points defining the center faceoff circle.

        This draws the line defining the faceoff circle at center ice. The line
        is circular in shape, and usually dark blue in color
        """
        # The center circle has no external hash marks, so this circle just
        # needs to be a plain circle
        faceoff_circle_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    0.0,
                    0.0
                ],

                "y": [
                    -self.feature_radius,
                    -self.feature_radius - self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return faceoff_circle_df


class ODZoneFaceoffCircle(BaseHockeyFeature):
    """A parameterization of the off-centered faceoff circles of a hockey rink.

    The non-centered faceoff circles are located in the offensive and defensive
    zones of the ice, with one on each side of the ``x``-axis. These circles
    differ from the center faceoff circle because they have hash marks that
    extend towards the boards on each side of the circle

    Attributes
    ----------
    hashmark_width : float
        The width of the hashmarks on the exterior of the defensive and
        offensive faceoff circles. Note that width refers to a distance solely
        in the ``y`` direction

    hashmark_ext_spacing : float
        The exterior horizontal spacing between the hashmarks on the exterior
        of the defensive and offensive faceoff circles. Note that this is
        solely in the ``x`` direction
    """

    def __init__(self, hashmark_width = 0.0, hashmark_ext_spacing = 0.0, *args,
                 **kwargs):
        # Set the dimensions of the hash marks on the top and bottom of the
        # circles
        self.hashmark_width = hashmark_width
        self.hashmark_ext_spacing = hashmark_ext_spacing
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining a non-centered faceoff circle.

        The non-centered faceoff circles are where faceoffs are taken after an
        icing call or to start a powerplay. They differ from the center ice
        faceoff circle because there are adjoining hash marks on these circles.
        It is also a different color than the center ice faceoff circle, and
        the spot in the center of it varies in size and form. Its line
        thickness should be given by ``minor_line_thickness" as this is a minor
        line on the ice surface
        """
        # To create a faceoff circle, start by finding the angle needed to draw
        # the outer ring of the faceoff circle. This can be computed using some
        # simple trigonometry. The NHL is used to illustrate the trigonometry,
        # however the code is abstracted to allow for variable parameters

        # NHL hash marks are 5' 11" (71") apart on the exterior, with one hash
        # mark on each side of the line that vertically bisects the circle
        # through its center. This means that 35.5" of this distance lies on
        # either side of this line, and thus the arcsine of this over the
        # radius of the circle will give the correct starting angle (after
        # adding pi/2)
        ext_spacing = self.hashmark_ext_spacing / 2.0
        int_spacing = ext_spacing - self.feature_thickness

        try:
            theta1 = math.asin(ext_spacing / self.feature_radius) / np.pi
            theta2 = math.asin(int_spacing / self.feature_radius) / np.pi
        except ZeroDivisionError:
            theta1 = 0.0
            theta2 = 0.0

        faceoff_circle_df = pd.concat([
            pd.DataFrame({
                "x": [
                    0.0
                ],

                "y": [
                    self.feature_radius
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 0.5,
                end = 0.5 + theta2,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    -int_spacing,
                    -ext_spacing
                ],

                "y": [
                    self.feature_radius + self.hashmark_width,
                    self.feature_radius + self.hashmark_width
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 0.5 + theta1,
                end = 1.5 - theta1,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    -ext_spacing,
                    -int_spacing
                ],

                "y": [
                    -self.feature_radius - self.hashmark_width,
                    -self.feature_radius - self.hashmark_width,
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5 - theta2,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [0.0],
                "y": [-self.feature_radius + self.feature_thickness]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                "x": [0.0],
                "y": [self.feature_radius]
            })
        ])

        # Reflect the half-circle just created over the y axis
        faceoff_circle_df = pd.concat([
            faceoff_circle_df,
            self._reflect(faceoff_circle_df, over_x = False, over_y = True)
        ])

        return faceoff_circle_df


class NODZoneFaceoffSpotRing(BaseHockeyFeature):
    """A parameterization of the off-centered faceoff spot of a hockey rink.

    The non-centered faceoff spots are located in the neutral, offensive and
    defensive zones of the ice, with one on each side of the ``x``-axis. These
    spots differ from the center faceoff spot because they have a larger
    diameter, differ in color, and have a colored stripe that runs through its
    center.

    This class is responsible for creating the outer ring, not the colored
    stripe running through it. Please see the documentation for the
    ``NODZoneFaceoffSpotStripe`` class for more information on it
    """

    def _get_centered_feature(self):
        """Generate the points defining a non-centered faceoff spot ring.

        The non-centered faceoff spots are where faceoffs are taken after an
        icing call or to start a powerplay. They differ from the center ice
        faceoff spot in size, color, and form. The thickness should be given by
        ``minor_line_thickness`` as these are minor lines on the ice surface
        """
        # The non-centered faceoff spots are comprised of an outer and inner
        # ring
        faceoff_spot_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    0.0
                ],

                "y": [
                    -self.feature_radius + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                "x": [
                    0.0,
                    0.0
                ],

                "y": [
                    self.feature_radius - self.feature_thickness,
                    self.feature_radius
                ]
            })
        ])

        faceoff_spot_df = pd.concat([
            faceoff_spot_df,
            self._reflect(faceoff_spot_df, over_x = False, over_y = True)
        ])

        return faceoff_spot_df


class NODZoneFaceoffSpotStripe(BaseHockeyFeature):
    """A parameterization of the off-centered faceoff spot of a hockey rink.

    The non-centered faceoff spots are located in the neutral, offensive and
    defensive zones of the ice, with one on each side of the ``x``-axis. These
    spots differ from the center faceoff spot because they have a larger
    diameter, differ in color, and have a colored stripe that runs through its
    center.

    This class is responsible for creating the inner stripe, not the colored
    outer ring around it. Please see the documentation for the
    ``NODZoneFaceoffSpotRing`` class for more information on it

    Attributes
    ----------
    gap_width : float
        The gap between the interior edge of a non-centered faceoff spot ring
        and the stripe running across it
    """

    def __init__(self, gap_width = 0.0, *args, **kwargs):
        # Initialize the gap width between the stripe and the inner edge of the
        # spot's outer ring
        self.gap_width = gap_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining a non-centered faceoff spot stripe.

        The non-centered faceoff spots are where faceoffs are taken after an
        icing call or to start a powerplay. They differ from the center ice
        faceoff spot in size, color, and form. For the faceoff spot's stripe,
        the "feature_thickness" parameter should be the thickness of the outer
        ring, which is ``minor_line_thickness"
        """
        # The non-center face-off spots are wider in diameter, with a gap
        # between the top and bottom of the spot and the strip in the center.
        # First, find the angle at which to start the trace for the interior
        # of the spot. The following walkthrough uses NHL dimensions for the
        # explanation, but the process is equally applied through all leagues

        # The spot has a radius of 1', and a thickness of 2", so the inner
        # radius is 10". Since there is a 3" gap at theta = 180°, this
        # indicates that the stripe's curve starts at x = -7" from the center.
        # Using trigonometry, the angle can be computed

        # Start by getting the inner radius of the ring
        ring_inner_radius = self.feature_radius - self.feature_thickness

        # Then get the thickness of half of the stripe that runs through the
        # center of the spot
        stripe_thickness = ring_inner_radius - self.gap_width

        # Calculate the angle
        try:
            theta = math.asin(stripe_thickness / ring_inner_radius) / np.pi
        except ZeroDivisionError:
            theta = 0.0

        spot_stripe_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = 0.5 - theta,
                end = 0.5 + theta,
                r = ring_inner_radius
            ),

            self.create_circle(
                center = (0.0, 0.0),
                start = 1.5 - theta,
                end = 1.5 + theta,
                r = ring_inner_radius
            )
        ])

        return spot_stripe_df


class ODZoneFaceoffLines(BaseHockeyFeature):
    """A parameterization of the faceoff lines in the offensive/defensive zone.

    These lines are the L-shaped lines where players on each team line up when
    taking a faceoff in either the offensive or defensive zones. There are four
    of these faceoff lines around each offensive/defensive faceoff spot

    Attributes
    ----------
    faceoff_line_dist_x : float
        The distance from the center of the defensive and offensive faceoff
        spot to the left-most edge of the upper-right faceoff line

    faceoff_line_dist_y: float
        The distance from the center of the defensive and offensive faceoff
        spot to the bottom edge of the upper-right faceoff line

    faceoff_line_length : float
        The exterior length of the faceoff line

    faceoff_line_width : float
        The exterior width of the faceoff line

    over_x : bool
        Whether or not the line should be reflected over the ``x`` axis

    over_y : bool
        Whether or not the line should be reflected over the ``y`` axis
    """

    def __init__(self, faceoff_line_dist_x = 0.0, faceoff_line_dist_y = 0.0,
                 faceoff_line_length = 0.0, faceoff_line_width = 0.0,
                 over_x = True, over_y = True, *args, **kwargs):
        # Set the distance in each direction that the faceoff lines are from
        # the center of the faceoff spot, as well as their respective lengths
        # and widths
        self.faceoff_line_dist_x = faceoff_line_dist_x
        self.faceoff_line_dist_y = faceoff_line_dist_y
        self.faceoff_line_length = faceoff_line_length
        self.faceoff_line_width = faceoff_line_width
        self.over_x = over_x
        self.over_y = over_y
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the faceoff lines.

        These lines are L-shaped, but can be thought of as two rectangles with
        thickness given by ``minor_line_thickness", and are usually red in
        color
        """
        # Create the L-shaped path
        faceoff_line_df = pd.DataFrame({
            "x": [
                self.faceoff_line_dist_x,
                self.faceoff_line_dist_x + self.faceoff_line_length,
                self.faceoff_line_dist_x + self.faceoff_line_length,
                self.faceoff_line_dist_x + self.feature_thickness,
                self.faceoff_line_dist_x + self.feature_thickness,
                self.faceoff_line_dist_x,
                self.faceoff_line_dist_x
            ],

            "y": [
                self.faceoff_line_dist_y,
                self.faceoff_line_dist_y,
                self.faceoff_line_dist_y + self.feature_thickness,
                self.faceoff_line_dist_y + self.feature_thickness,
                self.faceoff_line_dist_y + self.faceoff_line_width,
                self.faceoff_line_dist_y + self.faceoff_line_width,
                self.faceoff_line_dist_y
            ]
        })

        # Reflect the L as necessary
        faceoff_line_df = self._reflect(
            faceoff_line_df,
            over_x = self.over_x,
            over_y = self.over_y
        )

        return faceoff_line_df


class GoalFrame(BaseHockeyFeature):
    """A parameterization of a goal frame.

    The goal frame is where the puck enters after crossing the goal line to
    score a legal goal. The front face of the goal is flush with the goal line,
    while the back edge features rounded corners and expands outside of the
    front posts. The goal frame is composed of two pieces: the frame (this
    class) and the fill (see ``GoalFrameFill`` documentation)

    Attributes
    ----------
    goal_mouth_width : float
        The interior distance between the goalposts

    goal_back_width : float
        The exterior distance between the widest part of the goal frame's
        footprint

    goal_depth : float
        The depth of the goal frame from the center of the goal line to the
        exterior of the back pipe of the goal frame

    post_diameter : float
        The diameter of the posts of the goal frame
    """

    def __init__(self, goal_mouth_width = 0.0, goal_back_width = 0.0,
                 goal_depth = 0.0, post_diameter = 0.0, *args, **kwargs):
        # Set the parameters specific to the goal frame
        self.goal_mouth_width = goal_mouth_width
        self.goal_back_width = goal_back_width
        self.goal_depth = goal_depth
        self.post_diameter = post_diameter
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the goal frame.

        The goal frame has two thicknesses to be careful of: the outer diameter
        of the posts, and the outer diameter of the pipe in the back of the
        goal. The frame of the goal is usually red in color
        """
        # Start by getting the half-width of the goal mouth
        half_goal_mouth = self.goal_mouth_width / 2.0

        # Compute the location of the point to use to trace out the rounded
        # corners of the goal
        goal_arc_center_x = self.goal_depth - self.feature_radius
        goal_arc_center_y = (self.goal_back_width / 2.0) - self.feature_radius

        # Trace the path of the goal frame, starting with the exterior
        goal_frame_df = pd.concat([
            pd.DataFrame({
                "x": [0.0],
                "y": [half_goal_mouth + self.post_diameter]
            }),

            self.create_circle(
                center = (goal_arc_center_x, goal_arc_center_y),
                start = .65,
                end = 0.0,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (goal_arc_center_x, -goal_arc_center_y),
                start = 0.0,
                end = -.65,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    0.0,
                    0.0
                ],

                "y": [
                    -(half_goal_mouth + self.post_diameter),
                    -half_goal_mouth
                ]
            }),

            self.create_circle(
                center = (goal_arc_center_x, -goal_arc_center_y),
                start = -.65,
                end = 0.0,
                r = self.feature_radius - self.post_diameter
            ),

            self.create_circle(
                center = (goal_arc_center_x, goal_arc_center_y),
                start = 0.0,
                end = .65,
                r = self.feature_radius - self.post_diameter
            ),

            pd.DataFrame({
                "x": [0.0, 0.0],
                "y": [half_goal_mouth, half_goal_mouth + self.post_diameter]
            })
        ])

        return goal_frame_df


class GoalFrameFill(BaseHockeyFeature):
    """A parameterization of the filling of a goal frame.

    The goal frame is where the puck enters after crossing the goal line to
    score a legal goal. The front face of the goal is flush with the goal line,
    while the back edge features rounded corners and expands outside of the
    front posts. The goal frame is composed of two pieces: the frame (see
    ``GoalFrame`` documentation) and the fill (this class)

    Attributes
    ----------
    goal_mouth_width : float
        The interior distance between the goalposts

    goal_back_width : float
        The exterior distance between the widest part of the goal frame's
        footprint

    goal_depth : float
        The depth of the goal frame from the center of the goal line to the
        exterior of the back pipe of the goal frame

    post_diameter : float
        The diameter of the posts of the goal frame
    """

    def __init__(self, goal_mouth_width = 0.0, goal_back_width = 0.0,
                 goal_depth = 0.0, post_diameter = 0.0, *args, **kwargs):
        # Set the parameters specific to the goal frame
        self.goal_mouth_width = goal_mouth_width
        self.goal_back_width = goal_back_width
        self.goal_depth = goal_depth
        self.post_diameter = post_diameter
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the goal frame.

        The goal frame has two thicknesses to be careful of: the outer diameter
        of the posts, and the outer diameter of the pipe in the back of the
        goal. The frame of the goal is usually red in color
        """
        # Start by getting the half-width of the goal mouth
        half_goal_mouth = self.goal_mouth_width / 2.0

        # Compute the location of the point to use to trace out the rounded
        # corners of the goal
        goal_arc_center_x = self.goal_depth - self.feature_radius
        goal_arc_center_y = (self.goal_back_width / 2.0) - self.feature_radius

        # Trace the path of the goal frame, starting with the exterior
        goal_frame_fill_df = pd.concat([
            pd.DataFrame({
                "x": [
                    0.0
                ],

                "y": [
                    -half_goal_mouth
                ]
            }),

            self.create_circle(
                center = (goal_arc_center_x, -goal_arc_center_y),
                start = -.65,
                end = 0.0,
                r = self.feature_radius - self.post_diameter
            ),

            self.create_circle(
                center = (goal_arc_center_x, goal_arc_center_y),
                start = 0.0,
                end = .65,
                r = self.feature_radius - self.post_diameter
            ),

            pd.DataFrame({
                "x": [0.0],
                "y": [half_goal_mouth]
            })
        ])

        return goal_frame_fill_df


class PlayerBenchOutline(BaseHockeyFeature):
    """A parameterization of the player bench area's outline for a single team.

    The player benches are the areas outside the confines of the rink where
    players not currently on the ice are seated. They are to be on the same
    side of the ice surface and separate, as close to center ice as possible

    Attributes
    ----------
    bench_length : float
        The exterior length of a single team's bench area

    bench_depth : float
        The interior depth off the boards of a single team's bench area
    """

    def __init__(self, bench_length = 0.0, bench_depth = 0.0, *args, **kwargs):
        # Initialize the relevant features specific to the player bench area
        self.bench_length = bench_length
        self.bench_depth = bench_depth
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining player bench area.

        This will have the same thickness as the boards, but will be located
        outside the ice surface. Each bench's outline will share the same color
        as the boards
        """
        bench_outline_df = pd.DataFrame({
            "x": [
                -self.feature_thickness,
                -self.feature_thickness,
                self.bench_length + self.feature_thickness,
                self.bench_length + self.feature_thickness,
                self.bench_length,
                self.bench_length,
                0.0,
                0.0,
                -self.feature_thickness
            ],

            "y": [
                self.feature_thickness,
                (2.0 * self.feature_thickness) + self.bench_depth,
                (2.0 * self.feature_thickness) + self.bench_depth,
                self.feature_thickness,
                self.feature_thickness,
                self.feature_thickness + self.bench_depth,
                self.feature_thickness + self.bench_depth,
                self.feature_thickness,
                self.feature_thickness
            ]
        })

        return bench_outline_df


class PenaltyBoxOutline(BaseHockeyFeature):
    """A parameterization of the penalty box for a single team.

    The penalty boxes are the areas outside the confines of the rink where
    players serve time for a penalty incurred. They are to be on the same
    side of the ice surface and separate, as close to center ice as possible,
    for each team. This will also include the off-ice officials' box

    Attributes
    ----------
    penalty_box_length : float
        The interior length of a single penalty box

    penalty_box_depth : float
        The interior depth off of the boards of a single team's penalty box

    penalty_box_separation : float
        The distance that separates each team's penalty box area. This should
        be equivalent to the length of the off-ice officials' box
    """

    def __init__(self, penalty_box_length = 0.0, penalty_box_depth = 0.0,
                 penalty_box_separation = 0.0, *args, **kwargs):
        # Initialize the relevant features specific to the penalty box
        self.penalty_box_length = penalty_box_length
        self.penalty_box_depth = penalty_box_depth
        self.penalty_box_separation = penalty_box_separation
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining penalty box area.

        This will have the same thickness as the boards, but will be located
        outside the ice surface. Each penalty box's outline will share the same
        color as the boards
        """
        penalty_box_outline_df = pd.DataFrame({
            "x": [
                0.0,
                (
                    (self.penalty_box_separation / 2.0) +
                    self.penalty_box_length +
                    self.feature_thickness
                ),
                (
                    (self.penalty_box_separation / 2.0) +
                    self.penalty_box_length +
                    self.feature_thickness
                ),
                (
                    (self.penalty_box_separation / 2.0) +
                    self.penalty_box_length
                ),
                (
                    (self.penalty_box_separation / 2.0) +
                    self.penalty_box_length
                ),
                (
                    (self.penalty_box_separation / 2.0) +
                    self.feature_thickness
                ),
                (
                    (self.penalty_box_separation / 2.0) +
                    self.feature_thickness
                ),
                self.penalty_box_separation / 2.0,
                self.penalty_box_separation / 2.0,
                0.0,
                0.0
            ],

            "y": [
                -((2.0 * self.feature_thickness) + self.penalty_box_depth),
                -((2.0 * self.feature_thickness) + self.penalty_box_depth),
                -(self.feature_thickness),
                -(self.feature_thickness),
                -(self.feature_thickness + self.penalty_box_depth),
                -(self.feature_thickness + self.penalty_box_depth),
                -(self.feature_thickness),
                -(self.feature_thickness),
                -(self.feature_thickness + self.penalty_box_depth),
                -(self.feature_thickness + self.penalty_box_depth),
                -((2.0 * self.feature_thickness) + self.penalty_box_depth)
            ]
        })

        return penalty_box_outline_df


class PlayerBenchFill(BaseHockeyFeature):
    """A parameterization of the interior of the player bench area.

    The player benches are the areas outside the confines of the rink where
    players not currently on the ice are seated. They are to be on the same
    side of the ice surface and separate, as close to center ice as possible

    Attributes
    ----------
    bench_length : float
        The exterior length of a single team's bench area

    bench_depth : float
        The interior depth off the boards of a single team's bench area
    """

    def __init__(self, bench_length = 0.0, bench_depth = 0.0, *args, **kwargs):
        # Initialize the relevant features specific to the player bench area
        self.bench_length = bench_length
        self.bench_depth = bench_depth
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining player bench's enclosed area.

        This will have the same thickness as the boards, but will be located
        outside the ice surface
        """
        bench_fill_df = self.create_rectangle(
            x_min = -self.bench_length / 2.0,
            x_max = self.bench_length / 2.0,
            y_min = self.feature_thickness,
            y_max = self.feature_thickness + self.bench_depth
        )

        return bench_fill_df


class PenaltyBoxFill(BaseHockeyFeature):
    """A parameterization of the interior of the penalty box for a single team.

    The penalty boxes are the areas outside the confines of the rink where
    players serve time for a penalty incurred. They are to be on the same
    side of the ice surface and separate, as close to center ice as possible,
    for each team. This will not include the off-ice officials' box; see the
    documentation for the ``OffIceOfficialsBox`` class for more information

    Attributes
    ----------
    penalty_box_length : float
        The interior length of a single penalty box

    penalty_box_depth : float
        The interior depth off of the boards of a single team's penalty box

    penalty_box_separation : float
        The distance that separates each team's penalty box area. This should
        be equivalent to the length of the off-ice officials' box
    """

    def __init__(self, penalty_box_length = 0.0, penalty_box_depth = 0.0,
                 penalty_box_separation = 0.0, *args, **kwargs):
        # Initialize the relevant features specific to the penalty box
        self.penalty_box_length = penalty_box_length
        self.penalty_box_depth = penalty_box_depth
        self.penalty_box_separation = penalty_box_separation
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining penalty box's enclosed area.

        This will have the same thickness as the boards, but will be located
        outside the ice surface
        """
        penalty_box_fill_df = self.create_rectangle(
            x_min = -self.penalty_box_length / 2.0,
            x_max = self.penalty_box_length / 2.0,
            y_min = -self.feature_thickness,
            y_max = -(self.feature_thickness + self.penalty_box_depth)
        )

        return penalty_box_fill_df


class OffIceOfficialsBox(BaseHockeyFeature):
    """A parameterization of the interior of the off-ice officials' box.

    The off-ice officials' box is located between the two penalty boxes,
    opposite the team bench areas

    Attributes
    ----------
    officials_box_length : float
        The interior length of the off-ice officials' box

    officials_box_depth : float
        The interior depth off of the boards of the off-ice officials' box
    """

    def __init__(self, officials_box_length = 0.0, officials_box_depth = 0.0,
                 *args, **kwargs):
        # Initialize the relevant features specific to the off-ice officials'
        # box
        self.officials_box_length = officials_box_length
        self.officials_box_depth = officials_box_depth
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points defining the off-ice officials' box area.

        This will have the same thickness as the boards, but will be located
        outside the ice surface
        """
        off_ice_officials_box_df = self.create_rectangle(
            x_min = -self.officials_box_length / 2.0,
            x_max = self.officials_box_length / 2.0,
            y_min = -self.feature_thickness,
            y_max = -(self.feature_thickness + self.officials_box_depth)
        )

        return off_ice_officials_box_df
