"""Extensions of the BaseFeature class to be specific to basketball courts.

The features are all parameterized by the basic characteristics of a basketball
court. A user can manually specify their own court parameters in the
``BasketballCourt`` class that will adjust the placement of these features,
however the features themselves will be consistent across all basketball
surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseBasketballFeature(BaseFeature):
    """An extension of the ``BaseFeature`` class for basketball features.

    The following attributes are specific to basketball features only. For more
    information on inherited attributes, please see the ``BaseFeature`` class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
    court_length : float
        The length of the court in TV view. The default is ``0.0``

    court_width : float
        The width of the court in TV view. The default is ``0.0``

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

    def __init__(self, court_length = 0.0, court_width = 0.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = "ft", *args, **kwargs):
        # Set the full-sized dimensions of the court
        self.court_length = court_length
        self.court_width = court_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class CourtConstraint(BaseBasketballFeature):
    """The constraint around the interior edge of the court's boundary lines.

    This confines all interior features to be constrained inside the court, as
    well as any interior plots.
    """

    def _get_centered_feature(self):
        """Generate the points comprising the inner boundary of the court.

        This is done to constrain any features from extending needlessly beyond
        the edge of the court. Lines are considered out, so this should only
        trace the interior
        """
        # Define the length and width of the court as length and width
        # attributes. These will be used to constrain plotted points to be
        # defined inside the surface
        self.length = self.court_length
        self.width = self.court_width

        court_constraint_df = self.create_rectangle(
            x_min = -self.court_length / 2.0,
            x_max = self.court_length / 2.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return court_constraint_df


class HalfCourt(BaseBasketballFeature):
    """One half of the basketball court.

    Each half court spans from the inner edge of the baseline to the center of
    the division line, and serves as the base layer of the court
    """

    def _get_centered_feature(self):
        """Generate the points comprising the half court.

        This allows each half of the court to be colored independently
        """
        half_court_df = self.create_rectangle(
            x_min = -self.court_length / 4.0,
            x_max = self.court_length / 4.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return half_court_df


class CourtApron(BaseBasketballFeature):
    """The apron of the court.

    The apron is the colored boundary around the exterior of some courts. If no
    such colored boundary exists, this should take the same color as the court
    floor

    Attributes
    ----------
    court_apron_endline : float
        The thickness of the court's apron beyond the endline

    court_apron_sideline : float
        The thickness of the court's apron beyond the sideline

    court_apron_to_boundary : float
        The distance from the inner edge of the court apron to the outer edge
        of the court's boundary line (sideline and endline will be spaced the
        same)
    """

    def __init__(self, court_apron_endline = 0.0, court_apron_sideline = 0.0,
                 court_apron_to_boundary = 0.0, *args, **kwargs):
        # Initialize the parameters unique to this feature
        self.court_apron_endline = court_apron_endline
        self.court_apron_sideline = court_apron_sideline
        self.court_apron_to_boundary = court_apron_to_boundary
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the court's apron.

        The apron exists on both the sidelines and the endlines, and may not
        always align with the outer edge of these lines
        """
        apron_df = pd.DataFrame({
            "x": [
                0.0,
                (self.court_length / 2.0) + self.court_apron_endline,
                (self.court_length / 2.0) + self.court_apron_endline,
                0.0,
                0.0,
                (
                    (self.court_length / 2.0) +
                    self.feature_thickness +
                    self.court_apron_to_boundary
                ),
                (
                    (self.court_length / 2.0) +
                    self.feature_thickness +
                    self.court_apron_to_boundary
                ),
                0.0,
                0.0
            ],

            "y": [
                (self.court_width / 2.0) + self.court_apron_sideline,
                (self.court_width / 2.0) + self.court_apron_sideline,
                -((self.court_width / 2.0) + self.court_apron_sideline),
                -((self.court_width / 2.0) + self.court_apron_sideline),
                -(
                    (self.court_width / 2.0) +
                    self.feature_thickness +
                    self.court_apron_to_boundary
                ),
                -(
                    (self.court_width / 2.0) +
                    self.feature_thickness +
                    self.court_apron_to_boundary
                ),
                (
                    (self.court_width / 2.0) +
                    self.feature_thickness +
                    self.court_apron_to_boundary
                ),
                (
                    (self.court_width / 2.0) +
                    self.feature_thickness +
                    self.court_apron_to_boundary
                ),
                (self.court_width / 2.0) + self.court_apron_to_boundary
            ]
        })

        return apron_df


class CenterCircleOutline(BaseBasketballFeature):
    """The outline of the circle(s) at the center of the court.

    The circle is where the tip-off to the game takes place. The supplied
    radius (radii) should be measured to the outside of the circle, with the
    center of the circle(s) being the exact center of the court
    """

    def _get_centered_feature(self):
        """Generate the points comprising the center circle(s).

        The circles are drawn as semi-circles and then reflected over the y
        axis
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


class CenterCircleFill(BaseBasketballFeature):
    """The interior of the circle(s) at the center of the court.

    The circle is where the tip-off to the game takes place. The supplied
    radius (radii) should be measured to the outside of the circle, with the
    center of the circle(s) being the exact center of the court
    """

    def _get_centered_feature(self):
        """Generate the points comprising the center circle(s).

        The circles are drawn as semi-circles and then reflected over the y
        axis
        """
        center_circle_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius - self.feature_thickness
        )

        return center_circle_df


class DivisionLine(BaseBasketballFeature):
    """The center court line.

    This line divides the court in half, and is sometimes referred to as the
    time line or half-court line. The center of this line goes through the y
    axis, with half of the line lying in a team's offensive half court and the
    other half in their defensive half court

    Attributes
    ----------
    division_line_extension : float
        The distance that the division line extends beyond the sidelines. This
        may be omitted if the value is 0
    """

    def __init__(self, division_line_extension = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.division_line_extension = division_line_extension
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the division line.

        The line may extend beyond the outer edges of the sideline as specified
        via the division_line_extension attribute afforded to objects of this
        class. This should be in the same units as the court
        """
        if self.division_line_extension > 0.0:
            division_line_df = self.create_rectangle(
                x_min = -self.feature_thickness / 2.0,
                x_max = self.feature_thickness / 2.0,
                y_min = -(
                    (self.court_width / 2.0) +
                    self.division_line_extension +
                    self.feature_thickness
                ),
                y_max = (
                    (self.court_width / 2.0) +
                    self.division_line_extension +
                    self.feature_thickness
                )
            )

        else:
            division_line_df = self.create_rectangle(
                x_min = -self.feature_thickness / 2.0,
                x_max = self.feature_thickness / 2.0,
                y_min = -self.court_width / 2.0,
                y_max = self.court_width / 2.0
            )

        return division_line_df


class TwoPointRange(BaseBasketballFeature):
    """The area of the court where made baskets are worth two points.

    This is the area enclosed by the three-point line's outer edge and the
    baseline's inner edge

    Attributes
    ----------
    basket_center_to_baseline : float
        The distance from the center of the basket ring to the inner edge of
        the baseline

    basket_center_to_corner_three : float
        The distance from the center of the basket ring to the outer edge of
        the three-point line in the corner
    """

    def __init__(self, basket_center_to_baseline = 0.0,
                 basket_center_to_corner_three = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.basket_center_to_baseline = basket_center_to_baseline
        self.basket_center_to_corner_three = basket_center_to_corner_three
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the two-point range on the court.

        The area extends from the baseline to the outer edge of the three-point
        line. A brief calculation is walked through in the following code
        comments
        """
        # Start by calculating the angle through which the arc will trace. The
        # following explanation uses NBA dimensions, however the process is
        # the same no matter the governing body.

        # First, a bit of math is needed to determine the starting and ending
        # angles of the three-point arc, relative to 0 radians. Since in the
        # end, the angle is what matters, the units of measure do not. Inches
        # are easier to use for this calculation.

        # It should also be noted that as this corresponds strictly to the area
        # contained by the three-point line, the interior angle is what's
        # needed. While utilizing the corner-three distance as the outer edge
        # should work generally, an issue may arise if the z-order of the
        # feature's plotting characteristic is changed to be greater than that
        # of the three-point line itself. This should not happen, but the
        # interior edge is therefore what is used
        start_y = self.basket_center_to_corner_three - self.feature_thickness

        # Next, get the starting angle with which to trace out the two-point
        # range
        try:
            angle = math.asin(start_y / self.feature_radius) / np.pi

        except ZeroDivisionError:
            # If no radius is supplied in the dimensions, then use a base angle
            # of 0. This allows the feature's plot to be wholly avoided
            angle = 0.0

        except ValueError:
            # If the resulting angle is outside of the domain of asin, use 0.0
            angle = 0.0

        # As the TV-right two-point range is what is drawn first, the starting
        # and ending angles need to be adjusted appropriately
        start_angle = 1 - angle
        end_angle = 1 + angle

        two_point_range_df = pd.concat([
            pd.DataFrame({
                "x": [self.basket_center_to_baseline],
                "y": [start_y]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = start_angle,
                end = end_angle,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [
                    self.basket_center_to_baseline,
                    self.basket_center_to_baseline
                ],
                "y": [-start_y, start_y]
            })
        ])

        return two_point_range_df


class ThreePointLine(BaseBasketballFeature):
    """The line separating two-point range from three-point range.

    Made shots inside this line count for two points, and made shots from
    beyond this line are worth three points. The radius of the feature should
    be to its exterior

    Attributes
    ----------
    basket_center_to_baseline : float
        The distance from the center of the basket ring to the inner edge of
        the baseline

    basket_center_to_corner_three : float
        The distance from the center of the basket ring to the outer edge of
        the three-point line in the corner
    """

    def __init__(self, basket_center_to_baseline = 0.0,
                 basket_center_to_corner_three = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.basket_center_to_baseline = basket_center_to_baseline
        self.basket_center_to_corner_three = basket_center_to_corner_three
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the three-point line.

        The line begins at the baseline and extends straight out towards half
        court before following an arc. The area extends from the baseline to
        the outer edge of the three-point line. A brief calculation is walked
        through in the following code comments
        """
        # Start by calculating the angle through which the arc will trace. The
        # following explanation uses NBA dimensions, however the process is
        # the same no matter the governing body.

        # First, a bit of math is needed to determine the starting and ending
        # angles of the three-point arc, relative to 0 radians. Since in the
        # end, the angle is what matters, the units of measure do not. Inches
        # are easier to use for this calculation.
        start_y_outer = self.basket_center_to_corner_three

        # The rule book describes the arc as having a radius of 23' 9" to the
        # outside of the three-point arc from the center of the basket
        radius_outer = self.feature_radius

        # From here, the calculation is relatively straightforward. To
        # determine the angle, the inverse sine is needed. It will be
        # multiplied by pi so that it can be passed to the self.create_circle()
        # method
        try:
            angle_outer = math.asin(start_y_outer / radius_outer) / np.pi

        except ZeroDivisionError:
            # If no radius is supplied in the dimensions, then use a base angle
            # of 0. This allows the feature's plot to be wholly avoided
            angle_outer = 0.0

        except ValueError:
            # If the resulting angle is outside of the domain of asin, use 0.0
            angle_outer = 0.0

        # The same technique can be used to find the inner angles, however,
        # since the inner radius will be traced from bottom to top, the angle
        # must be negative to start
        start_y_inner = start_y_outer - self.feature_thickness
        radius_inner = radius_outer - self.feature_thickness

        try:
            angle_inner = math.asin(start_y_inner / radius_inner) / np.pi

        except ZeroDivisionError:
            angle_inner = 0.0

        except ValueError:
            # If the resulting angle is outside of the domain of asin, use 0.0
            angle_inner = 0.0

        # Set the starting and ending angles for the outer and inner tracings
        start_angle_outer = 1 - angle_outer
        end_angle_outer = 1 + angle_outer
        start_angle_inner = 1 + angle_inner
        end_angle_inner = 1 - angle_inner

        three_point_line_df = pd.concat([
            pd.DataFrame({
                "x": [self.basket_center_to_baseline],
                "y": [start_y_outer]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = start_angle_outer,
                end = end_angle_outer,
                r = radius_outer
            ),

            pd.DataFrame({
                "x": [
                    self.basket_center_to_baseline,
                    self.basket_center_to_baseline
                ],

                "y": [
                    -start_y_outer,
                    -start_y_inner
                ]
            }),

            self.create_circle(
                center = (0.0, 0.0),
                start = start_angle_inner,
                end = end_angle_inner,
                r = radius_inner
            ),

            pd.DataFrame({
                "x": [
                    self.basket_center_to_baseline,
                    self.basket_center_to_baseline
                ],

                "y": [
                    start_y_inner,
                    start_y_outer
                ]
            })
        ])

        return three_point_line_df


class PaintedArea(BaseBasketballFeature):
    """The painted area inside the free-throw lane.

    The painted area may have a margin from the interior edges of the free
    throw lane, although this margin will default to 0.0 units

    Attributes
    ----------
    lane_length : float
        The distance from the inner edge of the baseline to the center-court
        side of the free-throw lane in TV view

    lane_width : float
        The distance from the outer edges of the free-throw lane when viewing
        the court in TV view

    paint_margin : float
        The distance from the painted area of the lane to the lane boundary
        lines
    """

    def __init__(self, lane_length = 0.0, lane_width = 0.0, paint_margin = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.lane_length = lane_length
        self.lane_width = lane_width
        self.paint_margin = paint_margin
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the painted area.

        These areas may be colored differently than the rest of the area inside
        of the two-point range, but may also be the same color
        """
        painted_area_df = self.create_rectangle(
            x_min = self.paint_margin,
            x_max = (
                self.lane_length - self.feature_thickness - self.paint_margin
            ),
            y_min = -(
                (self.lane_width / 2.0) -
                self.feature_thickness -
                self.paint_margin
            ),
            y_max = (
                (self.lane_width / 2.0) -
                self.feature_thickness -
                self.paint_margin
            )
        )

        return painted_area_df


class FreeThrowLaneBoundary(BaseBasketballFeature):
    """The outline of the free-throw lane.

    The lines providing the boundary to the free-throw lane. When a player is
    shooting a free-throw, all non-shooting players must be outside of this
    boundary. NOTE: This does not include lane space markings (blocks), which
    will be created via the ``LaneSpaceMark`` class

    Attributes
    ----------
    lane_length : float
        The distance from the inner edge of the baseline to the center-court
        side of the free-throw lane in TV view

    lane_width : float
        The distance from the outer edges of the free-throw lane when viewing
        the court in TV view
    """

    def __init__(self, lane_length = 0.0, lane_width = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.lane_length = lane_length
        self.lane_width = lane_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the free-throw lane boundary.

        The lane space markings will be created separately
        """
        lane_boundary_df = pd.DataFrame({
            "x": [
                0.0,
                -self.lane_length,
                -self.lane_length,
                0.0,
                0.0,
                -(self.lane_length - self.feature_thickness),
                -(self.lane_length - self.feature_thickness),
                0.0,
                0.0
            ],

            "y": [
                self.lane_width / 2.0,
                self.lane_width / 2.0,
                -self.lane_width / 2.0,
                -self.lane_width / 2.0,
                -((self.lane_width / 2.0) - self.feature_thickness),
                -((self.lane_width / 2.0) - self.feature_thickness),
                (self.lane_width / 2.0) - self.feature_thickness,
                (self.lane_width / 2.0) - self.feature_thickness,
                self.lane_width / 2.0
            ]
        })

        return lane_boundary_df


class FreeThrowCircleFill(BaseBasketballFeature):
    """The filling of the area where a play shoots a free-throw.

    The provided radius should be to the free-throw circle's exterior
    """

    def _get_centered_feature(self):
        """Generate the points comprising the interior of a free-throw circle.

        The outline of this area will be created separately via the
        FreeThrowCircleOutline class
        """
        free_throw_circle_fill_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.5,
            end = 1.5,
            r = self.feature_radius - self.feature_thickness
        )

        return free_throw_circle_fill_df


class FreeThrowCircleOutline(BaseBasketballFeature):
    """The outline of the circle around the free-throw line.

    The provided radius should be to the free-throw circle's exterior
    """

    def _get_centered_feature(self):
        """Generate the points comprising the outline of a free-throw circle.

        The interior of this area will be created separately via the
        FreeThrowCircleFill class
        """
        free_throw_circle_outline_df = pd.concat([
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

        return free_throw_circle_outline_df


class FreeThrowCircleOutlineDash(BaseBasketballFeature):
    """The dashed part of a free-throw circle.

    The dashes may not be required by certain leagues

    Attributes
    ----------
    start_angle : float
        The angle at which the dash should start

    end_angle : float
        The angle at which the dash should end
    """

    def __init__(self, start_angle = 0.0, end_angle = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.start_angle = start_angle
        self.end_angle = end_angle
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising one dash of the free-throw circle.

        The dashes should be the same color as the rest of the free-throw
        circle
        """
        free_throw_circle_dash_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = self.start_angle,
                end = self.end_angle,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (0.0, 0.0),
                start = self.end_angle,
                end = self.start_angle,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return free_throw_circle_dash_df


class LaneSpaceMark(BaseBasketballFeature):
    """The lane space marks (blocks) on the outside of the free-throw lane.

    These are the marks where non-shooting players stand during free-throws.
    Players may not cross these lines before the ball touches the rim on the
    shot attempt

    Attributes
    ----------
    mark_depth : float
        The length (measurement in the baseline-to-free-throw-line direction)
        of lane space marks (blocks) of the free-throw lane
    """

    def __init__(self, mark_depth = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.mark_depth = mark_depth
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the lane space marks.

        These are created independently of the free-throw lane boundary, which
        is created via the FreeThrowLaneBoundary class
        """
        lane_space_mark_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = 0.0,
            y_max = self.mark_depth
        )

        return lane_space_mark_df


class Endline(BaseBasketballFeature):
    """The endlines on the basketball court.

    These are sometimes referred to as the baselines, and are located beyond
    each basket
    """

    def _get_centered_feature(self):
        """Generate the points comprising the endline.

        In cases where the endline is the court apron, the endline should still
        be generated and its color should be set equal to the court apron's
        color
        """
        endline_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = -((self.court_width / 2.0) + self.feature_thickness),
            y_max = (self.court_width / 2.0) + self.feature_thickness
        )

        return endline_df


class Sideline(BaseBasketballFeature):
    """The sidelines on the basketball court.

    These are the lines that run the full length of the court, typically with
    the team bench areas and substitution areas on their exterior
    """

    def _get_centered_feature(self):
        """Generate the points comprising the sideline.

        In cases where the sideline is the court apron, the sideline should
        still be generated and its color should be set equal to the court
        apron's color
        """
        sideline_df = self.create_rectangle(
            x_min = -((self.court_length / 2.0) + self.feature_thickness),
            x_max = (self.court_length / 2.0) + self.feature_thickness,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return sideline_df


class InboundingLine(BaseBasketballFeature):
    """The inbounding line.

    This is where the ball is inbounded on the sideline when necessary. Lines
    drawn on the top of the court should be drawn in a top-down direction, and
    lines on the bottom of the court should be drawn in the bottom-up direction

    Attributes
    ----------
    in_play_ext : float
        The distance into the court (measured from the inner edge of the
        sideline) that the inbounding lines protrude into the court

    out_of_bounds_ext : float
        The distance away from the court (measured from the outer edge of the
        sideline) that the inbounding lines protrude away the court

    drawn_direction : str
        The direction in which to draw the inbounding line
    """

    def __init__(self, in_play_ext = 0.0, out_of_bounds_ext = 0.0,
                 drawn_direction = "", *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.in_play_ext = in_play_ext
        self.out_of_bounds_ext = out_of_bounds_ext
        self.drawn_direction = drawn_direction.lower()
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the inbounding line.

        The line may extend solely into the court, solely away from the court,
        or both into and away from the court
        """
        if self.drawn_direction == "top_down":
            inbounding_line_df = self.create_rectangle(
                x_min = -self.feature_thickness,
                x_max = 0.0,
                y_min = -self.in_play_ext,
                y_max = self.out_of_bounds_ext + self.feature_thickness
            )

        else:
            inbounding_line_df = self.create_rectangle(
                x_min = -self.feature_thickness,
                x_max = 0.0,
                y_min = -(self.feature_thickness + self.out_of_bounds_ext),
                y_max = self.in_play_ext
            )

        return inbounding_line_df


class SubstitutionLine(BaseBasketballFeature):
    """The substitution lines.

    This is where players checking into the game wait for a stoppage. Lines
    drawn on the top of the court should be drawn in a top-down direction, and
    lines on the bottom of the court should be drawn in the bottom-up direction

    Attributes
    ----------
    substitution_line_width : float
        The distance away from the court (measured from the outer edge of the
        sideline) that the substitution lines protrude away from the court

    drawn_direction : str
        The direction in which to draw the substitution line
    """

    def __init__(self, substitution_line_width = 0.0, drawn_direction = "",
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.substitution_line_width = substitution_line_width
        self.drawn_direction = drawn_direction.lower()
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the subtitution line.

        The line may extend solely into the court, solely away from the court,
        or both into and away from the court
        """
        if self.drawn_direction == "bottom_up":
            substitution_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = -self.feature_thickness,
                y_min = 0.0,
                y_max = self.substitution_line_width + self.feature_thickness
            )

        else:
            substitution_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = -self.feature_thickness,
                y_min = -(
                    self.substitution_line_width + self.feature_thickness
                ),
                y_max = -self.feature_thickness
            )

        return substitution_line_df


class LowerDefensiveBoxMark(BaseBasketballFeature):
    """The lower defensive box marks.

    The lower defensive box is an imaginary box on the court extending from the
    lines on the baseline to the lines inside the painted area. This box helps
    determine when a block/charge call should take place, as an offensive
    player is entitled to move outside of (and subsequently enter) this box
    without contact

    Attributes
    ----------
    extension : float
        The distance that the lower defensive box markings extend from their
        anchor points

    drawn_direction : str
        The direction in which to draw the lower defensive box mark
    """

    def __init__(self, extension = 0.0, drawn_direction = "", *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.extension = extension
        self.drawn_direction = drawn_direction.lower()
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the lower defensive box mark.

        These marks can be drawn in two directions: left_to_right, which is
        used for the marks anchored to the baselines, and top_down, which is
        used for the marks in the free-throw lane
        """
        if self.drawn_direction == "left_to_right":
            lower_defensive_box_mark_df = self.create_rectangle(
                x_min = -self.extension,
                x_max = 0.0,
                y_min = 0.0,
                y_max = self.feature_thickness
            )

        if self.drawn_direction == "top_down":
            lower_defensive_box_mark_df = self.create_rectangle(
                x_min = -self.feature_thickness,
                x_max = 0.0,
                y_min = -self.extension,
                y_max = 0.0
            )

        return lower_defensive_box_mark_df


class TeamBenchLine(BaseBasketballFeature):
    """The team bench line.

    Players not in the game must stay within these lines unless moving to the
    substitution area (see SubstitutionLine class)

    Attributes
    ----------
    extension : float
        The distance that the team bench line extends from its anchor point

    drawn_direction : str
        The direction in which to draw the lower defensive box mark
    """

    def __init__(self, extension = 0.0, drawn_direction = "", *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.extension = extension
        self.drawn_direction = drawn_direction.lower()
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the team bench line.

        The team bench lines can be drawn bottom_up (when the benches are on
        the top of the court) or top_down (when the benches are on the bottom
        of the court)
        """
        if self.drawn_direction == "bottom_up":
            team_bench_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = 0.0,
                y_max = self.extension
            )

        if self.drawn_direction == "top_down":
            team_bench_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.extension,
                y_max = 0.0
            )

        return team_bench_line_df


class RestrictedArc(BaseBasketballFeature):
    """The restricted arc.

    The arc located in the free-throw lane. The interior radius should be
    specified for this feature.

    Attributes
    ----------
    backboard_to_center_of_basket : float
        The distance from the front face of the backboard to the center of the
        basket ring
    """

    def __init__(self, backboard_to_center_of_basket = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.backboard_to_center_of_basket = backboard_to_center_of_basket
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the restricted arc.

        The arc extends from the face of the backboard in the shape of an arc
        with the supplied radius
        """
        restricted_arc_df = pd.concat([
            pd.DataFrame({
                "x": [0.0],
                "y": [self.feature_radius]
            }),

            self.create_circle(
                center = (-self.backboard_to_center_of_basket, 0.0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                "x": [0.0, 0.0],
                "y": [
                    -self.feature_radius,
                    -(self.feature_radius + self.feature_thickness)
                ]
            }),

            self.create_circle(
                center = (-self.backboard_to_center_of_basket, 0.0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius + self.feature_thickness
            ),

            pd.DataFrame({
                "x": [0.0, 0.0],
                "y": [
                    self.feature_radius + self.feature_thickness,
                    self.feature_radius
                ]
            })
        ])

        return restricted_arc_df


class Backboard(BaseBasketballFeature):
    """The backboard.

    This is the backing onto which the basket ring (created separately) is
    affixed

    Attributes
    ----------
    backboard_thickness : float
        The thickness of the backboard. This is the observed thickness when
        viewing the court from a bird's eye view
    """

    def __init__(self, backboard_width = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.backboard_width = backboard_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the backboard.

        The backboard will be a rectangle as the court is drawn from an arial
        view
        """
        backboard_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = -self.backboard_width / 2.0,
            y_max = self.backboard_width / 2.0
        )

        return backboard_df


class BasketRing(BaseBasketballFeature):
    """The basket ring.

    The hoop through which the ball must pass to score points for a team

    Attributes
    ----------
    basket_ring_connector_extension : float
        The distance the basket ring's connector extends from the backboard
        into the free-throw lane

    basket_ring_connector_width : float
        The dimension of the piece of the basket ring that connects the
        backboard to the basket ring. When viewing the court in TV view from
        above, this is the dimension in the ``y`` direction

    backboard_to_center_of_basket : float
        The distance from the front face of the backboard to the center of the
        basket ring
    """

    def __init__(self, basket_ring_connector_extension = 0.0,
                 backboard_face_to_basket_center = 0.0,
                 basket_ring_connector_width = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.basket_ring_connector_extension = basket_ring_connector_extension
        self.basket_ring_connector_width = basket_ring_connector_width
        self.backboard_face_to_basket_center = backboard_face_to_basket_center
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the basket ring and its connector.

        An explanation of the math is outlined in the following code comments
        """
        # The below mathematical description uses the dimensions for an NBA
        # basket ring, although the calculation is generalizable to any league

        # The connector has a width of 7", so 3.5" are on either side of the x
        # axis. The ring has a radius of 9", so the arcsine of these
        # measurements should give the angle at which point they connect
        try:
            start_angle = math.asin(
                (self.basket_ring_connector_width / 2.0) /
                (self.feature_radius + self.feature_thickness)
            ) / np.pi

        except ZeroDivisionError:
            start_angle = 0.0

        except ValueError:
            # If the resulting angle is outside of the domain of asin, use 0.0
            start_angle = 0.0

        end_angle = 2.0 - start_angle

        basket_ring_df = pd.concat([
            pd.DataFrame({
                "x": [
                    0.0,
                    -self.backboard_face_to_basket_center +
                    (
                        (self.feature_radius + self.feature_thickness) *
                        math.cos(start_angle * np.pi)
                    )
                ],

                "y": [
                    self.basket_ring_connector_width / 2.0,
                    self.basket_ring_connector_width / 2.0
                ]
            }),

            self.create_circle(
                center = (-self.backboard_face_to_basket_center, 0.0),
                start = start_angle,
                end = end_angle,
                r = self.feature_radius + self.feature_thickness
            ),

            pd.DataFrame({
                "x": [
                    -self.backboard_face_to_basket_center +
                    (
                        (self.feature_radius + self.feature_thickness) *
                        math.cos(start_angle * np.pi)
                    ),
                    0.0,
                    0.0
                ],

                "y": [
                    -self.basket_ring_connector_width / 2.0,
                    -self.basket_ring_connector_width / 2.0,
                    self.basket_ring_connector_width / 2.0
                ]
            })
        ])

        return basket_ring_df


class Net(BaseBasketballFeature):
    """The net.

    To make the basket ring easier to identify, the nets will also be drawn
    onto the plot. They will typically be white in color, although this is
    customizable for a user
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the net.

        The nets are simply a circle defined by the interior radius of the
        basket ring
        """
        net_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return net_df
