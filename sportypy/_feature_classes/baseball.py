"""Extensions of the ``BaseFeature`` class to be specific to baseball fields.

The features are all parameterized by the basic characteristics of a baseball
field. A user can manually specify their own field parameters in the
``BaseballField`` class that will adjust the placement of these features,
however the features themselves will be consistent across all baseball
surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseBaseballFeature(BaseFeature):
    """An extension of the ``BaseFeature`` class for baseball features.

    The following attributes are specific to baseball features only. For more
    information on inherited attributes, please see the ``BaseFeature`` class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
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

    def __init__(self, feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = "ft", *args, **kwargs):
        # Set the characteristics of the feature
        self.feature_units = feature_units
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class FieldConstraint(BaseBaseballFeature):
    """The constraint around the bounding box of the field.

    This can be a bit tricky, so large default values are set here.
    """

    def _get_centered_feature(self):
        """Generate the coordinates that constrain a baseball field's interior.

        As of right now, this is just a square since no outfield wall is
        applied. This should change once walls are included
        """
        # Define the length and width of the field as length and width
        # attributes. These will be used to constrain plotted points to be
        # defined inside the surface
        self.length = 400
        self.width = 525

        field_constraint_df = self.create_rectangle(
            x_min = -200.0,
            x_max = 200.0,
            y_min = -75.0,
            y_max = 450.0
        )

        return field_constraint_df


class InfieldDirt(BaseBaseballFeature):
    """The dirt that comprises the infield.

    This includes the base paths, the infield arc, and the home plate circle.
    The home plate circle may be drawn over in other shapes as needed (example:
    Detroit's Comerica Park has a home plate shaped dirt area as the home plate
    "circle")

    Attributes
    ----------
    home_plate_circle_radius : float
        The radius of the dirt circle surrounding home plate

    foul_line_to_foul_grass : float
        The distance from the outer edge of the foul line to the inner edge of
        the grass in foul territory

    pitchers_plate_dist : float
        The distance from the front edge of the pitcher's plate to the back tip
        of home plate

    infield_arc_radius : float
        The distance from the front edge of the pitcher's mound to the back of
        the infield dirt
    """

    def __init__(self, home_plate_circle_radius = 0.0,
                 foul_line_to_foul_grass = 0.0, pitchers_plate_dist = 0.0,
                 infield_arc_radius = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.home_plate_circle_radius = home_plate_circle_radius
        self.foul_line_to_foul_grass = foul_line_to_foul_grass
        self.pitchers_plate_dist = pitchers_plate_dist
        self.infield_arc_radius = infield_arc_radius
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the infield dirt.

        The infield dirt should be anchored at the back tip of home plate
        """
        home_plate_x2 = 2.0
        home_plate_x1 = 2.0 * self.foul_line_to_foul_grass
        home_plate_x0 = (
            (self.foul_line_to_foul_grass ** 2) -
            (self.home_plate_circle_radius ** 2)
        )

        home_plate_roots = np.roots([
            home_plate_x2,
            home_plate_x1,
            home_plate_x0
        ])

        home_plate_x = home_plate_roots[home_plate_roots < 0][0]

        try:
            home_plate_start_theta = math.acos(
                home_plate_x / self.home_plate_circle_radius
            ) / np.pi

        except ValueError:
            home_plate_start_theta = 1.0

        home_plate_end_theta = 3.0 - home_plate_start_theta

        infield_x2 = 2.0
        infield_x1 = (
            (-2.0 * self.foul_line_to_foul_grass) -
            (2.0 * self.pitchers_plate_dist)
        )
        infield_x0 = (
            (self.foul_line_to_foul_grass ** 2) +
            (2.0 * self.foul_line_to_foul_grass * self.pitchers_plate_dist) +
            (self.pitchers_plate_dist ** 2) -
            (self.infield_arc_radius ** 2)
        )

        infield_roots = np.roots([infield_x2, infield_x1, infield_x0])

        infield_x = infield_roots[infield_roots > 0][0]

        try:
            infield_theta = math.acos(
                infield_x / self.infield_arc_radius
            ) / np.pi

        except ValueError:
            infield_theta = 0.25

        infield_dirt_df = pd.concat([
            self.create_circle(
                center = (0.0, self.pitchers_plate_dist),
                start = infield_theta,
                end = 1.0 - infield_theta,
                r = self.infield_arc_radius
            ),

            self.create_circle(
                center = (0.0, 0.0),
                start = home_plate_start_theta,
                end = home_plate_end_theta,
                r = self.home_plate_circle_radius
            )
        ])

        return infield_dirt_df


class InfieldGrass(BaseBaseballFeature):
    """The grass that comprises the infield.

    This is the area between the basepaths and the outfield that give the
    infield definition

    Attributes
    ----------
    foul_line_to_infield_grass : float
        The distance from the outer edge of the foul line to the outer edge of
        the infield grass

    home_plate_circle_radius : float
        The radius of the dirt circle surrounding home plate

    baseline_distance : float
        The distance of each baseline
    """

    def __init__(self, foul_line_to_infield_grass = 0.0,
                 home_plate_circle_radius = 0.0, baseline_distance = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.foul_line_to_infield_grass = foul_line_to_infield_grass
        self.home_plate_circle_radius = home_plate_circle_radius
        self.baseline_distance = baseline_distance
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the infield grass.

        The grass will have arcs at each base that are relative to the anchor
        point of the base
        """
        home_plate_1b_x2 = 2.0
        home_plate_1b_x1 = 2.0 * self.foul_line_to_infield_grass
        home_plate_1b_x0 = (
            (self.foul_line_to_infield_grass ** 2) -
            (self.home_plate_circle_radius ** 2)
        )

        home_plate_1b_roots = np.roots([
            home_plate_1b_x2,
            home_plate_1b_x1,
            home_plate_1b_x0
        ])

        if len(home_plate_1b_roots[home_plate_1b_roots > 0]) > 0:
            home_plate_1b_x = home_plate_1b_roots[home_plate_1b_roots > 0][0]

        else:
            home_plate_1b_x = self.home_plate_circle_radius

        try:
            home_plate_1b_theta = math.acos(
                home_plate_1b_x / self.home_plate_circle_radius
            ) / np.pi

        except ZeroDivisionError:
            home_plate_1b_theta = 0.0

        home_plate_3b_x2 = 2.0
        home_plate_3b_x1 = -2.0 * self.foul_line_to_infield_grass
        home_plate_3b_x0 = (
            (self.foul_line_to_infield_grass ** 2) -
            (self.home_plate_circle_radius ** 2)
        )

        home_plate_3b_roots = np.roots([
            home_plate_3b_x2,
            home_plate_3b_x1,
            home_plate_3b_x0
        ])

        if len(home_plate_3b_roots[home_plate_3b_roots < 0]) > 0:
            home_plate_3b_x = home_plate_3b_roots[home_plate_3b_roots < 0][0]

        else:
            home_plate_3b_x = self.home_plate_circle_radius

        try:
            home_plate_3b_theta = math.acos(
                home_plate_3b_x / self.home_plate_circle_radius
            ) / np.pi

        except ZeroDivisionError:
            home_plate_3b_theta = 1.0

        first_base_x2 = 2.0
        first_base_x1 = (
            (2.0 * self.foul_line_to_infield_grass) -
            (2.0 * math.sqrt(2.0) * self.baseline_distance)
        )
        first_base_x0 = (
            ((self.foul_line_to_infield_grass) ** 2) -
            (
                math.sqrt(2.0) *
                self.foul_line_to_infield_grass *
                self.baseline_distance
            ) +
            (self.baseline_distance ** 2) -
            (self.feature_radius ** 2)
        )

        first_base_roots = np.roots([
            first_base_x2,
            first_base_x1,
            first_base_x0
        ])

        first_base_x = first_base_roots[
            first_base_roots < (self.baseline_distance * math.cos(np.pi / 4.0))
        ][0]

        first_base_delta = abs(
            first_base_x -
            (self.baseline_distance * math.cos(np.pi / 4.0))
        )

        try:
            first_base_theta = math.acos(
                first_base_delta / self.feature_radius
            ) / np.pi

        except ValueError:
            first_base_theta = 0.0

        first_base_start_theta = 1.0 + first_base_theta
        first_base_end_theta = 1.0 - first_base_theta

        second_base_start_theta = 1.5 + first_base_theta
        second_base_end_theta = 1.5 - first_base_theta

        third_base_start_theta = 1.0 - first_base_end_theta
        third_base_end_theta = 1.0 - first_base_start_theta

        infield_grass_df = pd.concat([
            self.create_circle(
                center = (0.0, 0.0),
                start = home_plate_3b_theta,
                end = home_plate_1b_theta,
                r = self.home_plate_circle_radius
            ),

            self.create_circle(
                center = (
                    self.baseline_distance * math.cos(np.pi / 4.0),
                    self.baseline_distance * math.sin(np.pi / 4.0)
                ),
                start = first_base_start_theta,
                end = first_base_end_theta,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (0.0, self.baseline_distance * math.sqrt(2.0)),
                start = second_base_start_theta,
                end = second_base_end_theta,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (
                    -self.baseline_distance * math.cos(np.pi / 4.0),
                    self.baseline_distance * math.sin(np.pi / 4.0)
                ),
                start = third_base_start_theta,
                end = third_base_end_theta,
                r = self.feature_radius
            )
        ])

        return infield_grass_df


class HomePlate(BaseBaseballFeature):
    """Home plate.

    The back tip of home plate will be located at the origin.

    Attributes
    ----------
    home_plate_edge_length : float
        The length of a full side of home plate
    """

    def __init__(self, home_plate_edge_length = 0.0, *args, **kwargs):
        # Initialize the attribute unique to this feature
        self.home_plate_edge_length = home_plate_edge_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising home plate.

        The plate is usually a pentagon, where the angled sides intersect the
        base lines
        """
        home_plate_df = pd.DataFrame({
            "x": [
                0.0,
                self.home_plate_edge_length / 2.0,
                self.home_plate_edge_length / 2.0,
                -self.home_plate_edge_length / 2.0,
                -self.home_plate_edge_length / 2.0,
                0.0
            ],

            "y": [
                0.0,
                self.home_plate_edge_length / 2.0,
                self.home_plate_edge_length,
                self.home_plate_edge_length,
                self.home_plate_edge_length / 2.0,
                0.0
            ]
        })

        return home_plate_df


class Base(BaseBaseballFeature):
    """A base on the diamond.

    The base is where a runner is considered safe

    Attributes
    ----------
    base_side_length : float
        The length of one side of a square base

    adjust_x_left : bool
        Whether or not to adjust the base's ``x`` anchor to the left

    adjust_x_right : bool
        Whether or not to adjust the base's ``x`` anchor to the right
    """

    def __init__(self, base_side_length = 0.0, adjust_x_left = False,
                 adjust_x_right = False, *args, **kwargs):
        # Initialize the attribute unique to this feature
        self.base_side_length = base_side_length
        self.adjust_x_left = adjust_x_left
        self.adjust_x_right = adjust_x_right
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising a base.

        The base is a square with the back tip laying on the baseline, or its
        center located at the intersection of the lines connecting the back
        corner of each base
        """
        center_x_adj = 0.0

        if self.adjust_x_left:
            center_x_adj -= (self.base_side_length * math.sqrt(2.0) / 2.0)

        if self.adjust_x_right:
            center_x_adj += (self.base_side_length * math.sqrt(2.0) / 2.0)

        base_df = self.create_square(
            side_length = self.base_side_length,
            center = (0.0, 0.0)
        )

        base_df = self._rotate(base_df, angle = 0.25)

        base_df["x"] = base_df["x"] + center_x_adj

        return base_df


class PitchersMound(BaseBaseballFeature):
    """The mound from which the pitcher throws.

    The pitcher's plate (the rubber) is located on this mound, but is drawn
    separately
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the pitcher's mound.

        This is a circular feature in the middle of the infield
        """
        pitchers_mound_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return pitchers_mound_df


class PitchersPlate(BaseBaseballFeature):
    """The pitcher's plate.

    This is also known as the rubber. It is where a pitcher must throw the ball
    from to start the play

    Attributes
    ----------
    pitchers_plate_length : float
        The length of the pitcher's plate (the dimension in the ``x``
        direction)
    """

    def __init__(self, pitchers_plate_length = 0.0, *args, **kwargs):
        # Initialize the attribute unique to this feature
        self.pitchers_plate_length = pitchers_plate_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the pitcher's plate.

        The pitcher's plate is a rectangle with its front edge as its anchor
        point
        """
        pitchers_plate_df = self.create_rectangle(
            x_min = -self.pitchers_plate_length / 2.0,
            x_max = self.pitchers_plate_length / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return pitchers_plate_df


class BattersBox(BaseBaseballFeature):
    """The box in which batters stand when batting.

    The boxes are located around home plate

    Attributes
    ----------
    batters_box_length : float
        The length of the batter's box (in the ``y`` direction) measured from
        the outside of the chalk lines

    batters_box_width : float
        The width of the batter's box (in the ``x`` direction) measured from
        the outside of the chalk lines

    batters_box_y_adj : float
        The shift off of center in the ``y`` direction that the batter's box
        needs to be moved to properly align
    """

    def __init__(self, batters_box_length = 0.0, batters_box_width = 0.0,
                 batters_box_y_adj = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.batters_box_length = batters_box_length
        self.batters_box_width = batters_box_width
        self.batters_box_y_adj = batters_box_y_adj
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the batter's box.

        The batter's box is a rectangle with the thickness of the field lines
        """
        batters_box_df = pd.DataFrame({
            "x": [
                0.0,
                self.batters_box_width / 2.0,
                self.batters_box_width / 2.0,
                0.0,
                0.0,
                (self.batters_box_width / 2.0) - self.feature_thickness,
                (self.batters_box_width / 2.0) - self.feature_thickness,
                0.0,
                0.0
            ],

            "y": [
                self.batters_box_length / 2.0,
                self.batters_box_length / 2.0,
                -self.batters_box_length / 2.0,
                -self.batters_box_length / 2.0,
                -((self.batters_box_length / 2.0) - self.feature_thickness),
                -((self.batters_box_length / 2.0) - self.feature_thickness),
                (self.batters_box_length / 2.0) - self.feature_thickness,
                (self.batters_box_length / 2.0) - self.feature_thickness,
                self.batters_box_length
            ]
        })

        batters_box_df = pd.concat([
            batters_box_df,
            self._reflect(df = batters_box_df, over_y = True, over_x = False)
        ])

        batters_box_df["y"] = batters_box_df["y"] + self.batters_box_y_adj

        return batters_box_df


class CatchersBox(BaseBaseballFeature):
    """The box in which batters stand when batting.

    The catcher's box is located behind home plate, connecting to the back
    edges of the batters' boxes

    Attributes
    ----------
    catchers_box_depth : float
        The distance from the back tip of home plate to the back edge of the
        catcher's box

    catchers_box_width : float
        The distance between the outer edges of the catcher's box

    batters_box_length : float
        The length of the batter's box (in the ``y`` direction) measured from
        the outside of the chalk lines

    batters_box_width : float
        The width of the batter's box (in the ``x`` direction) measured from
        the outside of the chalk lines

    catchers_box_shape : str
        The shape of the catcher's box. Currently-supported values are:

            - ``"rectangle"`` (default behavior)
            - ``"trapezoid"`` (see ``sportypy.surfaces.LittleLeagueField`` for
                example)

    batters_box_y_adj : float
        The shift off of center in the ``y`` direction that the batter's box
        needs to be moved to properly align
    """

    def __init__(self, catchers_box_depth = 0.0, catchers_box_width = 0.0,
                 batters_box_length = 0.0, batters_box_y_adj = 0.0,
                 catchers_box_shape = "rectangle", *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.catchers_box_depth = catchers_box_depth
        self.catchers_box_width = catchers_box_width
        self.batters_box_length = batters_box_length
        self.batters_box_y_adj = batters_box_y_adj
        self.catchers_box_shape = catchers_box_shape
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the catcher's box.

        The catcher's box is 3/4 of a rectangle with the thickness of the field
        lines
        """
        if self.catchers_box_shape == "rectangle":
            catchers_box_df = pd.DataFrame({
                "x": [
                    self.catchers_box_width / 2.0,
                    self.catchers_box_width / 2.0,
                    -self.catchers_box_width / 2.0,
                    -self.catchers_box_width / 2.0,
                    -(
                        (self.catchers_box_width / 2.0) -
                        self.feature_thickness
                    ),
                    -(
                        (self.catchers_box_width / 2.0) -
                        self.feature_thickness
                    ),
                    (self.catchers_box_width / 2.0) - self.feature_thickness,
                    (self.catchers_box_width / 2.0) - self.feature_thickness,
                    self.catchers_box_width / 2.0
                ],

                "y": [
                    -self.batters_box_length / 2.0,
                    -self.catchers_box_depth,
                    -self.catchers_box_depth,
                    -self.batters_box_length / 2.0,
                    -self.batters_box_length / 2.0,
                    -self.catchers_box_depth + self.feature_thickness,
                    -self.catchers_box_depth + self.feature_thickness,
                    -self.batters_box_length / 2.0,
                    -self.batters_box_length / 2.0
                ]
            })

            catchers_box_df["y"] = (
                catchers_box_df["y"] + self.batters_box_y_adj
            )

        if self.catchers_box_shape == "trapezoid":
            catchers_box_b1_y = -self.batters_box_length / 2.0
            catchers_box_b1_y += self.batters_box_y_adj
            catchers_box_b1_r = catchers_box_b1_y / math.cos(np.pi / 4.0)
            catchers_box_b1 = 2.0 * (
                abs(catchers_box_b1_r) * math.sin(np.pi / 4.0)
            )

            catchers_box_b2_y_outer = -(
                self.catchers_box_depth +
                self.feature_thickness
            )

            catchers_box_b2_y_inner = -self.catchers_box_depth

            catchers_box_b2_r_inner = self.feature_radius - (
                self.feature_thickness / math.cos(np.pi / 4.0)
            )
            catchers_box_b2_r_outer = self.feature_radius

            catchers_box_b2_inner = 2.0 * (
                abs(catchers_box_b2_r_inner) * math.sin(np.pi / 4.0)
            )

            catchers_box_b2_outer = 2.0 * (
                abs(catchers_box_b2_r_outer) * math.sin(np.pi / 4.0)
            )

            catchers_box_df = pd.DataFrame({
                "x": [
                    catchers_box_b1 / 2.0,
                    (catchers_box_b2_outer / 2.0) - self.feature_thickness,
                    -(catchers_box_b2_outer / 2.0) + self.feature_thickness,
                    -catchers_box_b1 / 2.0,
                    -(catchers_box_b1 / 2.0) - self.feature_thickness,
                    (
                        -(catchers_box_b2_inner / 2.0) -
                        (2.0 * self.feature_thickness)
                    ),
                    (
                        (catchers_box_b2_inner / 2.0) +
                        (2.0 * self.feature_thickness)
                    ),
                    (catchers_box_b1 / 2.0) + self.feature_thickness,
                    catchers_box_b1 / 2.0
                ],

                "y": [
                    catchers_box_b1_y,
                    catchers_box_b2_y_inner + self.feature_thickness,
                    catchers_box_b2_y_inner + self.feature_thickness,
                    catchers_box_b1_y,
                    catchers_box_b1_y,
                    catchers_box_b2_y_outer + self.feature_thickness,
                    catchers_box_b2_y_outer + self.feature_thickness,
                    catchers_box_b1_y,
                    catchers_box_b1_y
                ]
            })

        return catchers_box_df


class FoulLine(BaseBaseballFeature):
    """The lines that designate fair territory from foul territory.

    Since a ball on the line is considered in fair territory, the outer edge of
    the baseline must lie in fair territory (aka the line ``y = +/- x``)

    Attributes
    ----------
    is_line_1b : bool
        Whether or not the foul line is the first base line

    line_distance : float
        The length of the foul line

    batters_box_length : float
        The length of the batter's box (in the ``y`` direction) measured from
        the outside of the chalk lines

    batters_box_width : float
        The width of the batter's box (in the ``x`` direction) measured from
        the outside of the chalk lines

    batters_box_y_adj : float
        The shift off of center in the ``y`` direction that the batter's box
        needs to be moved to properly align

    home_plate_side_to_batters_box : float
        The distance from the outer edge of the batter's box to the outer edge
        of home plate
    """

    def __init__(self, is_line_1b = False, line_distance = 0.0,
                 batters_box_length = 0.0, batters_box_width = 0.0,
                 batters_box_y_adj = 0.0, home_plate_side_to_batters_box = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.is_line_1b = is_line_1b
        self.line_distance = line_distance
        self.batters_box_length = batters_box_length
        self.batters_box_width = batters_box_width
        self.batters_box_y_adj = batters_box_y_adj
        self.home_plate_side_to_batters_box = home_plate_side_to_batters_box
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the baselines.

        The line distance should be given as a straight line distance measured
        from the back tip of home plate (aka looking down the line)
        """
        batters_box_corner_coord_x = (
            self.batters_box_width + self.home_plate_side_to_batters_box
        )

        batters_box_corner_coord_y = (
            (self.batters_box_length / 2.0) +
            self.batters_box_y_adj
        )

        if batters_box_corner_coord_x > batters_box_corner_coord_y:
            starting_coord = batters_box_corner_coord_y
        else:
            starting_coord = batters_box_corner_coord_x
            starting_coord += (self.batters_box_y_adj / 2.0)
            starting_coord += self.feature_thickness

        if not self.is_line_1b:
            foul_line_df = pd.DataFrame({
                "x": [
                    -starting_coord,
                    self.line_distance * math.cos(3.0 * np.pi / 4.0),
                    (
                        (self.line_distance * math.cos(3.0 * np.pi / 4.0)) +
                        self.feature_thickness
                    ),
                    -(starting_coord - self.feature_thickness),
                    -(starting_coord)
                ],

                "y": [
                    starting_coord,
                    self.line_distance * math.sin(3.0 * np.pi / 4.0),
                    self.line_distance * math.sin(3.0 * np.pi / 4.0),
                    starting_coord,
                    starting_coord
                ]
            })

        else:
            foul_line_df = pd.DataFrame({
                "x": [
                    starting_coord,
                    self.line_distance * math.cos(np.pi / 4.0),
                    (
                        (self.line_distance * math.cos(np.pi / 4.0)) -
                        self.feature_thickness
                    ),
                    starting_coord - self.feature_thickness,
                    starting_coord
                ],

                "y": [
                    starting_coord,
                    self.line_distance * math.sin(np.pi / 4.0),
                    self.line_distance * math.sin(np.pi / 4.0),
                    starting_coord,
                    starting_coord
                ]
            })

        return foul_line_df


class RunningLane(BaseBaseballFeature):
    """The running lane along the first base line.

    This is entirely in foul territory. The depth should be measured from the
    foul-side edge of the baseline to the outer edge of the running lane mark

    Attributes
    ----------
    running_lane_length : float
        The straight-line length of the running lane measured from the point
        nearest home plate. As an example, if the base lines are 90 feet, and
        the running lane starts a distance of 45 feet down the line from the
        back tip of home plate, and extends 3 feet beyond first base, this
        parameter would be given as ``48.0``

    running_lane_depth : float
        The straight-line distance from the outer edge of the first-base line
        to the outer edge of the running lane

    running_lane_start_distance : float
        The straight-line distance from the back tip of home plate to the start
        of the running lane
    """

    def __init__(self, running_lane_depth = 0.0, running_lane_length = 0.0,
                 running_lane_start_distance = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.running_lane_depth = running_lane_depth
        self.running_lane_length = running_lane_length
        self.running_lane_start_distance = running_lane_start_distance
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the running lane.

        The measurements should be given "looking down the line" (e.g. as they
        would be measured by an observer standing behind home plate)
        """
        # Define parameters as it is easier and shorter to work with
        rlsd = self.running_lane_start_distance
        rll = self.running_lane_length
        rld = self.running_lane_depth
        rlt = self.feature_thickness
        running_lane_df = pd.DataFrame({
            "x": [
                rlsd / math.sqrt(2.0),
                (rlsd + rld) / math.sqrt(2.0),
                (rlsd + rld + rll) / math.sqrt(2.0),
                (rlsd + rld + rll - rlt) / math.sqrt(2.0),
                (rlsd + rld) / math.sqrt(2.0),
                (rlsd + rlt) / math.sqrt(2.0),
                rlsd / math.sqrt(2.0)
            ],

            "y": [
                rlsd / math.sqrt(2.0),
                (rlsd - rld) / math.sqrt(2.0),
                (rlsd - rld + rll) / math.sqrt(2.0),
                (rlsd - rld + rll + rlt) / math.sqrt(2.0),
                (rlsd - rld + (2.0 * rlt)) / math.sqrt(2.0),
                (rlsd + rlt) / math.sqrt(2.0),
                rlsd / math.sqrt(2.0)
            ]
        })

        return running_lane_df
