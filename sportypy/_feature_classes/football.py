"""Extensions of the BaseFeature class to be specific to football field.

The features are all parameterized by the basic characteristics of a football
field. A user can manually specify their own field parameters in the
FootballField class that will adjust the placement of these features, however
the features themselves will be consistent across all football surfaces.

@author: Ross Drucker
"""
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseFootballFeature(BaseFeature):
    """An extension of the BaseFeature class for football features.

    The following attributes are specific to football features only. For more
    information on inherited attributes, please see the BaseFeature class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
    field_length : float (default: 0.0)
        The length of the field in TV view

    field_width : float (default: 0.0)
        The width of the field in TV view

    feature_radius : float (default: 0.0)
        The radius needed to draw the feature. This may not be needed for all
        features

    feature_thickness : float (default: 0.0)
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed
    """

    def __init__(self, field_length = 0.0, field_width = 0.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = 'yd', *args, **kwargs):

        # Set the full-sized dimensions of the field
        self.field_length = field_length
        self.field_width = field_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class FieldConstraint(BaseFootballFeature):
    """The constraint around the interior edge of the field's boundary lines.

    This confines all interior features to be constrained inside the field, as
    well as any interior plots.
    """

    def __init__(self, endzone_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.endzone_length = endzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the inner boundary of the field.

        This is done to constrain any features from extending needlessly beyond
        the edge of the field
        """
        field_constraint_df = self.create_rectangle(
            x_min = -self.field_length / 2.0,
            x_max = self.field_length / 2.0,
            y_min = -self.field_width / 2.0,
            y_max = self.field_width / 2.0
        )

        return field_constraint_df


class OffensiveHalf(BaseFootballFeature):
    """The offensive half of the field.

    This is the right half of the field in TV view
    """

    def __init__(self, endzone_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.endzone_length = endzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the offensive half of the field.

        These points will provide the base of the plot
        """
        offensive_half_df = self.create_rectangle(
            x_min = 0.0,
            x_max = (self.field_length / 2.0) + self.endzone_length,
            y_min = -((self.field_width / 2.0) + self.feature_thickness),
            y_max = (self.field_width / 2.0) + self.feature_thickness
        )

        return offensive_half_df


class DefensiveHalf(BaseFootballFeature):
    """The defensive half of the field.

    This is the left half of the field in TV view
    """

    def __init__(self, endzone_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.endzone_length = endzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the defensive half of the field.

        These points will provide the base of the plot
        """
        defensive_half_df = self.create_rectangle(
            x_min = -((self.field_length / 2.0) + self.endzone_length),
            x_max = 0.0,
            y_min = -((self.field_width / 2.0) + self.feature_thickness),
            y_max = (self.field_width / 2.0) + self.feature_thickness
        )

        return defensive_half_df


class Endzone(BaseFootballFeature):
    """The endzones.

    The area beyond the goal line.
    """

    def __init__(self, endzone_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.endzone_length = endzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the endzone.

        The endzone will lie on top of the offensive and defensive halves
        """
        endzone = self.create_rectangle(
            x_min = -self.endzone_length / 2.0,
            x_max = self.endzone_length / 2.0,
            y_min = -((self.field_width / 2.0) + self.feature_thickness),
            y_max = (self.field_width / 2.0) + self.feature_thickness
        )

        return endzone


class EndLine(BaseFootballFeature):
    """The line beyond the endzone.

    The end line is typically white in color, and its interior edge is out of
    bounds
    """

    def _get_centered_feature(self):
        """Generate the points comprising the end line.

        The end line is typically white in color
        """
        end_line_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = -((self.field_width / 2.0) + self.feature_thickness),
            y_max = (self.field_width / 2.0) + self.feature_thickness
        )

        return end_line_df


class Sideline(BaseFootballFeature):
    """The lines that run the length of the field.

    The sidelines are typically white in color, and its interior edge is out of
    bounds
    """

    def __init__(self, endzone_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.endzone_length = endzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the sideline.

        The side line is typically white in color
        """
        sideline_df = self.create_rectangle(
            x_min = -((self.field_length / 2.0) + self.endzone_length),
            x_max = (self.field_length / 2.0) + self.endzone_length,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return sideline_df


class FieldBorder(BaseFootballFeature):
    """The border around the outside of the sideline and end line.

    This is not present on every field, but is not the same as the sideline
    or end line (although they may be the same in color)
    """

    def __init__(self, endzone_length = 0.0, boundary_thickness = 0.0,
                 restricted_area_length = 0.0, restricted_area_width = 0.0,
                 coaching_box_length = 0.0, coaching_box_width = 0.0,
                 team_bench_length_field_side = 0.0,
                 team_bench_length_back_side = 0.0, team_bench_width = 0.0,
                 team_bench_border_thickness = 0.0, bench_shape = '',
                 surrounds_team_bench_area = False, *args, **kwargs):
        # Initialize the attributes that are unique to this feature
        self.endzone_length = endzone_length
        self.boundary_thickness = boundary_thickness
        self.restricted_area_length = restricted_area_length
        self.restricted_area_width = restricted_area_width
        self.coaching_box_length = coaching_box_length
        self.coaching_box_width = coaching_box_width
        self.team_bench_length_field_side = team_bench_length_field_side
        self.team_bench_length_back_side = team_bench_length_back_side
        self.team_bench_width = team_bench_width
        self.team_bench_border_thickness = team_bench_border_thickness
        self.surrounds_team_bench_area = surrounds_team_bench_area
        self.bench_shape = bench_shape
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the field border.

        This should run along the entirety of the field and will be the same
        at all points around the field
        """
        if not self.surrounds_team_bench_area:
            field_border_df = pd.DataFrame({
                'x': [
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    )
                ],

                'y': [
                    (self.field_width / 2.0) + self.boundary_thickness,
                    (self.field_width / 2.0) + self.boundary_thickness,
                    -((self.field_width / 2.0) + self.boundary_thickness),
                    -((self.field_width / 2.0) + self.boundary_thickness),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (self.field_width / 2.0) + self.boundary_thickness
                ]
            })
        else:
            starting_depth = (
                (self.field_width / 2.0) +
                self.boundary_thickness +
                self.restricted_area_width +
                self.coaching_box_width +
                self.team_bench_width +
                self.team_bench_border_thickness
            )

            if self.bench_shape.lower() not in ['rectangle', 'rectangular']:
                m = self.team_bench_width / (
                    (self.team_bench_length_back_side / 2.0) -
                    (self.team_bench_length_field_side / 2.0)
                )

                y2 = starting_depth + self.feature_thickness
                y1 = (
                    starting_depth -
                    self.team_bench_width -
                    self.team_bench_border_thickness
                )
                x1 = (
                    (self.team_bench_length_field_side / 2.0) +
                    self.team_bench_border_thickness +
                    self.feature_thickness
                )

                outer_corner_x_dist = (((y2 - y1) / m) + x1)
            else:
                outer_corner_x_dist = (self.team_bench_length_back_side / 2.0)
                outer_corner_x_dist += self.team_bench_border_thickness
                outer_corner_x_dist += self.feature_thickness

            field_border_df = pd.DataFrame({
                'x': [
                    0.0,
                    (
                        (self.team_bench_length_back_side / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.team_bench_length_back_side / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    0.0,
                    0.0,
                    outer_corner_x_dist,
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness +
                        self.feature_thickness
                    ),
                    outer_corner_x_dist,
                    0.0,
                    0.0
                ],

                'y': [
                    starting_depth,
                    starting_depth,
                    (
                        starting_depth -
                        self.team_bench_width -
                        self.team_bench_border_thickness
                    ),
                    (
                        starting_depth -
                        self.team_bench_width -
                        self.coaching_box_width -
                        self.team_bench_border_thickness
                    ),
                    ((self.field_width / 2.0) + self.boundary_thickness),
                    ((self.field_width / 2.0) + self.boundary_thickness),
                    -((self.field_width / 2.0) + self.boundary_thickness),
                    -((self.field_width / 2.0) + self.boundary_thickness),
                    -(
                        starting_depth -
                        self.team_bench_width -
                        self.coaching_box_width -
                        self.team_bench_border_thickness
                    ),
                    -(
                        starting_depth -
                        self.team_bench_width -
                        self.team_bench_border_thickness
                    ),
                    -starting_depth,
                    -starting_depth,
                    -(starting_depth + self.feature_thickness),
                    -(starting_depth + self.feature_thickness),
                    -(
                        starting_depth -
                        self.team_bench_width -
                        self.team_bench_border_thickness
                    ),
                    -(
                        starting_depth -
                        self.team_bench_width -
                        self.coaching_box_width -
                        self.team_bench_border_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.feature_thickness
                    ),
                    (
                        starting_depth -
                        self.team_bench_width -
                        self.coaching_box_width -
                        self.team_bench_border_thickness
                    ),
                    (
                        starting_depth -
                        self.team_bench_width -
                        self.team_bench_border_thickness
                    ),
                    starting_depth + self.feature_thickness,
                    starting_depth + self.feature_thickness,
                    starting_depth
                ]
            })

        return field_border_df


class FieldBorderOutline(BaseFootballFeature):
    """The outline of the border around the field.

    This is not present on every field, but is not the same as the sideline
    or end line (although they may be the same in color)
    """

    def __init__(self, endzone_length = 0.0, boundary_thickness = 0.0,
                 restricted_area_length = 0.0, restricted_area_width = 0.0,
                 coaching_box_length = 0.0, coaching_box_width = 0.0,
                 team_bench_length_field_side = 0.0,
                 team_bench_length_back_side = 0.0, team_bench_width = 0.0,
                 team_bench_border_thickness = 0.0, bench_shape = '',
                 field_border_thickness = 0.0,
                 surrounds_team_bench_area = True, *args, **kwargs):
        # Initialize the attributes that are unique to this feature
        self.endzone_length = endzone_length
        self.boundary_thickness = boundary_thickness
        self.restricted_area_length = restricted_area_length
        self.restricted_area_width = restricted_area_width
        self.coaching_box_length = coaching_box_length
        self.coaching_box_width = coaching_box_width
        self.team_bench_length_field_side = team_bench_length_field_side
        self.team_bench_length_back_side = team_bench_length_back_side
        self.team_bench_width = team_bench_width
        self.team_bench_border_thickness = team_bench_border_thickness
        self.field_border_thickness = field_border_thickness
        self.surrounds_team_bench_area = surrounds_team_bench_area
        self.bench_shape = bench_shape
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the field border's outline.

        This should run along the entirety of the field and will be the same
        at all points around the field
        """
        if not self.surrounds_team_bench_area:
            field_border_outline_df = pd.DataFrame({
                'x': [
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    ),
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness
                    )
                ],

                'y': [
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    )
                ]
            })
        else:
            starting_depth = (
                (self.field_width / 2.0) +
                self.boundary_thickness +
                self.restricted_area_width +
                self.coaching_box_width +
                self.team_bench_width +
                self.team_bench_border_thickness
            )

            if self.bench_shape.lower() not in ['rectangle', 'rectangular']:
                m = self.team_bench_width / (
                    (self.team_bench_length_back_side / 2.0) -
                    (self.team_bench_length_field_side / 2.0)
                )

                y2 = starting_depth + self.field_border_thickness
                y1 = (
                    starting_depth -
                    self.team_bench_width -
                    self.team_bench_border_thickness
                )
                x1 = (
                    (self.team_bench_length_field_side / 2.0) +
                    self.team_bench_border_thickness +
                    self.field_border_thickness
                )

                outer_corner_x_dist = (((y2 - y1) / m) + x1)
            else:
                outer_corner_x_dist = (self.team_bench_length_back_side / 2.0)
                outer_corner_x_dist += self.team_bench_border_thickness
                outer_corner_x_dist += self.field_border_thickness

            field_border_outline_df = pd.DataFrame({
                'x': [
                    # Start
                    0.0,
                    # Short edge of bench (top)
                    outer_corner_x_dist,
                    # Long edge of bench (top)
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Coaching box (top)
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Restricted area (top)
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Edge of field (top)
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    # Edge of field (bottom)
                    (
                        (self.field_length / 2.0) +
                        self.endzone_length +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    # Restricted area (bottom)
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Coaching box (bottom)
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Long edge of bench (bottom)
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Short edge of bench (bottom)
                    outer_corner_x_dist,
                    # Zero
                    0.0,
                    # Outward
                    0.0,
                    # Short edge of bench (bottom)
                    outer_corner_x_dist + self.feature_thickness,
                    # Long edge of bench (bottom)
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Coaching box (bottom)
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Restricted area (bottom)
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Edge of field (bottom)
                    (
                        (self.field_length / 2.0) +
                        self.boundary_thickness +
                        self.endzone_length +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Edge of field (top)
                    (
                        (self.field_length / 2.0) +
                        self.boundary_thickness +
                        self.endzone_length +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Restricted area (top)
                    (
                        (self.restricted_area_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Coaching box (top)
                    (
                        (self.coaching_box_length / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Long edge of bench (top)
                    (
                        (self.team_bench_length_field_side / 2.0) +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Short edge of bench (top)
                    outer_corner_x_dist + self.feature_thickness,
                    # Zero
                    0.0,
                    # End
                    0.0,
                ],

                'y': [
                    # Start
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Short edge of bench (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Long edge of bench (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width
                    ),
                    # Coaching box (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width
                    ),
                    # Restricted area (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    # Edge of field (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    # Edge of field (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    # Restricted area (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness
                    ),
                    # Coaching box (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width
                    ),
                    # Long edge of bench (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width
                    ),
                    # Short edge of bench (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Zero
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    ),
                    # Outward
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Short edge of bench (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Long edge of bench (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width
                    ),
                    # Coaching box (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width
                    ),
                    # Restricted area (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Edge of field (bottom)
                    -(
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Edge of field (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Restricted area (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Coaching box (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width
                    ),
                    # Long edge of bench (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width
                    ),
                    # Short edge of bench (top)
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # Zero
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness +
                        self.feature_thickness
                    ),
                    # End
                    (
                        (self.field_width / 2.0) +
                        self.boundary_thickness +
                        self.restricted_area_width +
                        self.coaching_box_width +
                        self.team_bench_width +
                        self.team_bench_border_thickness +
                        self.field_border_thickness
                    )
                ]
            })

        return field_border_outline_df


class MajorYardLine(BaseFootballFeature):
    """The major yard lines on the field.

    These are the yard lines that span the entire width of the field
    """

    def __init__(self, dist_to_sideline = 0.0, cross_hash_length = 0.0,
                 cross_hash_separation = 0.0, yard_line_name = '', *args,
                 **kwargs):
        # Initialize the attributes unique to this feature
        self.dist_to_sideline = dist_to_sideline
        self.cross_hash_length = cross_hash_length
        self.cross_hash_separation = cross_hash_separation
        self.yard_line_name = yard_line_name
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the major yard line.

        The major yard line should typically be white in color
        """
        major_yard_line_df = pd.DataFrame({
            'x': [
                -self.feature_thickness / 2.0,
                -self.feature_thickness / 2.0,
                -((self.feature_thickness / 2.0) + self.cross_hash_length),
                -((self.feature_thickness / 2.0) + self.cross_hash_length),
                -self.feature_thickness / 2.0,
                -self.feature_thickness / 2.0,
                -((self.feature_thickness / 2.0) + self.cross_hash_length),
                -((self.feature_thickness / 2.0) + self.cross_hash_length),
                -self.feature_thickness / 2.0,
                -self.feature_thickness / 2.0,
                self.feature_thickness / 2.0,
                self.feature_thickness / 2.0,
                (self.feature_thickness / 2.0) + self.cross_hash_length,
                (self.feature_thickness / 2.0) + self.cross_hash_length,
                self.feature_thickness / 2.0,
                self.feature_thickness / 2.0,
                (self.feature_thickness / 2.0) + self.cross_hash_length,
                (self.feature_thickness / 2.0) + self.cross_hash_length,
                self.feature_thickness / 2.0,
                self.feature_thickness / 2.0,
                -self.feature_thickness / 2.0
            ],

            'y': [
                -((self.field_width / 2.0) - self.dist_to_sideline),
                -((self.cross_hash_separation / 2.0) + self.feature_thickness),
                -((self.cross_hash_separation / 2.0) + self.feature_thickness),
                -self.cross_hash_separation / 2.0,
                -self.cross_hash_separation / 2.0,
                self.cross_hash_separation / 2.0,
                self.cross_hash_separation / 2.0,
                (self.cross_hash_separation / 2.0) + self.feature_thickness,
                (self.cross_hash_separation / 2.0) + self.feature_thickness,
                (self.field_width / 2.0) - self.dist_to_sideline,
                (self.field_width / 2.0) - self.dist_to_sideline,
                (self.cross_hash_separation / 2.0) + self.feature_thickness,
                (self.cross_hash_separation / 2.0) + self.feature_thickness,
                self.cross_hash_separation / 2.0,
                self.cross_hash_separation / 2.0,
                -self.cross_hash_separation / 2.0,
                -self.cross_hash_separation / 2.0,
                -((self.cross_hash_separation / 2.0) + self.feature_thickness),
                -((self.cross_hash_separation / 2.0) + self.feature_thickness),
                -((self.field_width / 2.0) - self.dist_to_sideline),
                -((self.field_width / 2.0) - self.dist_to_sideline)
            ]
        })

        return major_yard_line_df


class GoalLine(BaseFootballFeature):
    """The goal line.

    The interior edge (relative to the field of play) should lie at the 0 yard
    line. The center of the 1 yard line should be exactly 1 yard from this edge
    of the goal line
    """

    def _get_centered_feature(self):
        """Generate the points comprising the goal line.

        The goal line should extend towards the end zone, not in to the field
        of play
        """
        goal_line_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = -self.field_width / 2.0,
            y_max = self.field_width / 2.0
        )

        return goal_line_df


class MinorYardLine(BaseFootballFeature):
    """The minor yard lines on the field.

    These are the yard lines spaced closer than every five yards on the field
    """

    def __init__(self, yard_line_height = 0.0, yard_line_name = '',
                 dist_to_sideline = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.yard_line_height = yard_line_height
        self.yard_line_name = yard_line_name
        self.dist_to_sideline = dist_to_sideline
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising a minor yard line.

        The yard line's height is given as the longer distance when viewing the
        field in TV view
        """
        minor_yard_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = 0.0,
            y_max = self.yard_line_height
        )

        return minor_yard_line_df


class Arrow(BaseFootballFeature):
    """The arrows pointing to the nearest end zone.

    These arrows are described by their base (which runs parallel to the goal
    line) and their length, which extends from the tip to the base
    """

    def __init__(self, arrow_base = 0.0, arrow_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.arrow_base = arrow_base
        self.arrow_length = arrow_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising a directional arrow.

        The arrow should be located near major yard lines and point in the
        direction of the nearest endzone
        """
        arrow_df = pd.DataFrame({
            'x': [
                0.0,
                self.arrow_length,
                0.0,
                0.0
            ],

            'y': [
                self.arrow_base / 2.0,
                0.0,
                -self.arrow_base / 2.0,
                self.arrow_base / 2.0
            ]
        })

        return arrow_df


class TryMark(BaseFootballFeature):
    """The marking where a two-point try begins.

    This is usually around the two or three yard line and located in the
    vertical center of the field (in TV view)
    """

    def __init__(self, try_mark_width = 0.0, *args, **kwargs):
        # Initialize the attribute unique to this feature
        self.try_mark_width = try_mark_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the try marking.

        The try mark is a rectangle
        """
        try_mark_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.try_mark_width / 2.0,
            y_max = self.try_mark_width / 2.0
        )

        return try_mark_df


class RestrictedArea(BaseFootballFeature):
    """The restricted area.

    This is the area between the coaching box and the exterior edge of the
    sideline
    """

    def __init__(self, restricted_area_length = 0.0, *args, **kwargs):
        # Initialize the attribute unique to this feature
        self.restricted_area_length = restricted_area_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        restricted_area_df = self.create_rectangle(
            x_min = -self.restricted_area_length / 2.0,
            x_max = self.restricted_area_length / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return restricted_area_df


class CoachingBoxLine(BaseFootballFeature):
    """The line separating the coaching box from the team bench area.

    The line should be a different color than either the team bench area or the
    coaching box
    """

    def __init__(self, coaching_box_line_length = 0.0, *args, **kwargs):
        self.coaching_box_line_length = coaching_box_line_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the coaching box line.

        The line should span the entirety of the coaching box
        """
        coaching_box_line_df = self.create_rectangle(
            x_min = -self.coaching_box_line_length / 2.0,
            x_max = self.coaching_box_line_length / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return coaching_box_line_df


class CoachingBox(BaseFootballFeature):
    """The coaching box.

    This is the area beyond the restricted area designated for coaches. It is
    between the restricted area and the team area
    """

    def __init__(self, coaching_box_length = 0.0, *args, **kwargs):
        # Initialize the attribute unique to this feature
        self.coaching_box_length = coaching_box_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        coaching_box_df = self.create_rectangle(
            x_min = -self.coaching_box_length / 2.0,
            x_max = self.coaching_box_length / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return coaching_box_df


class TeamBenchArea(BaseFootballFeature):
    """The team bench area.

    This is the area beyond the restricted area and coaching box. It is where
    the team benches, non-playing players, and team staff are to remain during
    the game
    """

    def __init__(self, team_bench_length_field_side = 0.0,
                 team_bench_length_back_side = 0.0, team_bench_width = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.team_bench_length_field_side = team_bench_length_field_side
        self.team_bench_length_back_side = team_bench_length_back_side
        self.team_bench_width = team_bench_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the team bench area.

        This area can be either rectangular or trapezoidal in shape
        """
        team_bench_area_df = pd.DataFrame({
            'x': [
                -self.team_bench_length_field_side / 2.0,
                self.team_bench_length_field_side / 2.0,
                self.team_bench_length_back_side / 2.0,
                -self.team_bench_length_back_side / 2.0,
                -self.team_bench_length_field_side / 2.0
            ],

            'y': [
                0.0,
                0.0,
                self.team_bench_width,
                self.team_bench_width,
                0.0
            ]
        })

        return team_bench_area_df


class TeamBenchAreaOutline(BaseFootballFeature):
    """The outline of the bench area (border, not broken line).

    The border may not be necessary in all drawings
    """

    def __init__(self, restricted_area_length = 0.0,
                 restricted_area_width = 0.0, coaching_box_length = 0.0,
                 coaching_box_width = 0.0, team_bench_length_field_side = 0.0,
                 team_bench_length_back_side = 0.0, team_bench_width = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.restricted_area_length = restricted_area_length
        self.restricted_area_width = restricted_area_width
        self.coaching_box_length = coaching_box_length
        self.coaching_box_width = coaching_box_width
        self.team_bench_length_field_side = team_bench_length_field_side
        self.team_bench_length_back_side = team_bench_length_back_side
        self.team_bench_width = team_bench_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the team bench area's outline.

        The outline may not be needed
        """
        team_bench_area_outline_df = pd.DataFrame({
            'x': [
                -self.restricted_area_length / 2.0,
                -self.coaching_box_length / 2.0,
                -self.team_bench_length_field_side / 2.0,
                -self.team_bench_length_back_side / 2.0,
                self.team_bench_length_back_side / 2.0,
                self.team_bench_length_field_side / 2.0,
                self.coaching_box_length / 2.0,
                self.restricted_area_length / 2.0,
                (self.restricted_area_length / 2.0) + self.feature_thickness,
                (self.coaching_box_length / 2.0) + self.feature_thickness,
                (
                    (self.team_bench_length_field_side / 2.0) +
                    self.feature_thickness
                ),
                (
                    (self.team_bench_length_back_side / 2.0) +
                    self.feature_thickness
                ),
                -(
                    (self.team_bench_length_back_side / 2.0) +
                    self.feature_thickness
                ),
                -(
                    (self.team_bench_length_field_side / 2.0) +
                    self.feature_thickness
                ),
                -((self.coaching_box_length / 2.0) + self.feature_thickness),
                -(
                    (self.restricted_area_length / 2.0) +
                    self.feature_thickness
                ),
                -self.restricted_area_length / 2.0
            ],

            'y': [
                0.0,
                self.restricted_area_width,
                self.restricted_area_width + self.coaching_box_width,
                (
                    self.restricted_area_width +
                    self.coaching_box_width +
                    self.team_bench_width
                ),
                (
                    self.restricted_area_width +
                    self.coaching_box_width +
                    self.team_bench_width
                ),
                self.restricted_area_width + self.coaching_box_width,
                self.restricted_area_width,
                0.0,
                0.0,
                self.restricted_area_width,
                self.restricted_area_width + self.coaching_box_width,
                (
                    self.restricted_area_width +
                    self.coaching_box_width +
                    self.team_bench_width +
                    self.feature_thickness
                ),
                (
                    self.restricted_area_width +
                    self.coaching_box_width +
                    self.team_bench_width +
                    self.feature_thickness
                ),
                self.restricted_area_width + self.coaching_box_width,
                self.restricted_area_width,
                0.0,
                0.0
            ]
        })

        return team_bench_area_outline_df