"""Extension of the ``BaseSurfacePlot`` class to create a basketball court.

This is a second-level child class of the ``BaseSurface`` class, and as such
will have access to its attributes and methods. ``sportypy`` will ship with
pre-defined leagues that will have their own subclass, but a user can manually
specify their own court parameters to create a totally-customized court. The
court's features are parameterized by the basic dimensions of the court, which
comprise the attributes of the class.

@author: Ross Drucker
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.basketball as basketball_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class BasketballCourt(BaseSurfacePlot):
    """A subclass of ``BaseSurfacePlot`` to make a generic basketball court.

    This allows for the creation of the basketball court in a way that is
    entirely parameterized by the court's baseline characteristics.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid basketball court. The attributes needed to instantiate a
    particular league's surface must be specified in the ``court_params``
    dictionary. For many leagues, these will be provided in the
    surface_dimensions.json file in the data/ subdirectory of ``sportypy``.

    See the ``BaseSurfacePlot`` and ``BaseSurface`` class definitions for full
    details.

    Attributes
    ----------
    league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "National
        Basketball Association" should be either "NBA" or "nba"). The default
        is an empty string

    rotation_amt : float
        The angle (in degrees) through which to rotate the final plot. The
        default is ``0.0``

    x_trans : float
        The amount that the ``x`` coordinates are to be shifted. By convention,
        the +``x`` axis extends from the center of the surface towards the
        right-hand basket when viewing the court in TV view. The default is
        ``0.0``

    y_trans : float
        The amount that the ``y`` coordinates are to be shifted. By convention,
        the +``y`` axis extends from the center of the surface towards the
        top of the court when viewing the court in TV view. The default is
        ``0.0``

    feature_colors : dict
        A dictionary of coloring parameters to pass to the plot

    court_params : dict
        A dictionary containing the following parameters of the court:

        - court_length : float
            The length of the court

        - court_width : float
            The width of the court

        - line_thickness : float
            The thickness of the lines of the court in the court's specified
            units

        - bench_side : str
            The side, in TV view where the team benches are located

        - court_apron_endline : float
            The thickness of the court's apron beyond the endline

        - court_apron_sideline : float
            The thickness of the court's apron beyond the sideline

        - court_apron_to_boundary : float
            The distance from the inner edge of the court apron to the outer
            edge of the court's boundary line (sideline and endline will be
            spaced the same)

        - center_circle_radius : list or float
            The radius (radii) of the court's center circle(s) in the court's
            specified units. These should be measured from the center of the
            court to the outer edge of the circle. When providing a list (e.g.
            for the NBA), these values should go in decreasing order

        - division_line_extension : float
            The distance that the division line extends beyond the sidelines.
            This may be omitted if the value is 0

        - basket_center_to_baseline : float
            The distance from the center of the basket ring to the inner edge
            of the baseline

        - basket_center_to_three_point_arc : float
            The distance from the cetner of the basket ring to the outer edge
            of the arc of the three point line

        - basket_center_to_corner_three : float
            The distance from the center of the basket ring to the outer edge
            of the three-point line in the corner

        - backboard_face_to_baseline : float
            The distance from the face of the backboard to the inner edge of
            the baseline

        - lane_length : float
            The distance from the inner edge of the baseline to the
            center-court side of the free-throw lane in the court's specified
            units in TV view

        - lane_width : float
            The distance from the outer edges of the free-throw lane when
            viewing the court in TV view

        - paint_margin : float
            The distance from the painted area of the lane to the lane boundary
            lines

        - free_throw_circle_radius : float
            The radius of the free-throw circle, measured from the center of
            the free-throw line, given

        - free_throw_line_to_backboard : float
            The distance from the free-throw line to the face of the backboard

        - free_throw_circle_overhang : float
            The arc length of any part of the free-throw circle that extends
            beyond the free-throw line

        - n_free_throw_circle_dashes : float
            The number of dashes that comprise the free-throw circle

        - free_throw_dash_length : float
            The arc length of each dash of the free-throw circle

        - free_throw_dash_spacing : float
            The arc length of the gap between each dash of the free-throw
            circle

        - lane_space_mark_lengths : float or list of either lists or floats
            The length (measurement in the baseline-to-free-throw-line
            direction) of lane space marks (blocks) of the free-throw lane

        - lane_space_mark_widths : float or list of either lists or floats
            The widths (measurement in the sideline-to-sideline direction) of
            the lane space marks (blocks) of the free-throw lane in the court's
            specified units

        - lane_space_mark_separations : float or list of either lists or floats
            The separations between each lane space mark in the court's
            specified dimensions. The first "spacing" measurement corresponds
            to the distance between the face of the backboard and the
            baseline-side edge of the first/"low" block

        - painted_area_visibility : bool or list of bools
            Whether or not to show the painted area. This is particularly
            useful if more than one free-throw lane is specified (e.g. an NBA
            court with an NCAA lane drawn in addition to the NBA-sized lane)

        - lane_boundary_visibility : bool or list of bools
            Whether or not to show the lane boundary. This is particularly
            useful if more than one free-throw lane is specified (e.g. an NBA
            court with an NCAA lane drawn in addition to the NBA-sized lane)


        - lane_space_mark_visibility : bool or list of bools
            Whether or not to draw the lane space marks. This is particularly
            useful if more than one free-throw lane is specified (e.g. an NBA
            court with an NCAA lane drawn in addition to the NBA-sized lane)

        - lane_lower_defensive_box_marks_visibility : bool or list of bools
            Whether or not to draw the lower defensive box markings that appear
            in the free-throw lane/painted area

        - baseline_lower_defensive_box_marks_int_sep : float
            The interior separation between the lower defensive box markings on
            the baseline

        - baseline_to_lane_lower_defensive_box_marks : float
            The interior distance from the inner edge of the baseline to the
            baseline-side edge of the lower defensive box markings located in
            the free-throw lane/painted area

        - lane_lower_defensive_box_marks_int_sep : float
            The interior separation between the lower defensive box markings in
            the free-throw lane/painted area

        - lower_defensive_box_mark_extension : float
            The distance that the lower defensive box markings extend from
            their anchor points

        - inbounding_line_to_baseline : float
            The interior distance from the inner edge of the baseline to the
            baseline-side edge of the inbounding line in the court's specified
            units

        - inbounding_line_anchor_side : float
            The side where the primary inbounding lines are located. This
            should be either ``1.0`` or ``-1.0``, corresponding to the top or
            bottom of the court in TV view, respectively

        - inbounding_line_in_play_ext : float
            The distance into the court (measured from the inner edge of the
            sideline) that the inbounding lines protrude into the court

        - inbounding_line_out_of_bounds_ext : float
            The distance away from the court (measured from the outer edge of
            the sideline) that the inbounding lines protrude away the court

        - symmetric_inbounding_line : bool
            Whether or not the inbounding lines are symmetric about the court

        - substitution_line_ext_sep : float
            The external separation of the lines marking the substitution area

        - substitution_line_width : float
            The distance away from the court (measured from the outer edge of
            the sideline) that the substitution lines protrude away from the
            court

        - team_bench_line_ext : float
            The distance that the team bench line extends from its anchor point

        - restricted_arc_radius : float
            The inner radius of the restricted arc in the court's specified
            units

        - backboard_width : float
            The distance the backboard spans across the lane in the court's
            specified units. This is the left-to-right dimension of the
            backboard a free-throw shooter would see when shooting their
            free-throws

        - backboard_thickness : float
            The thickness of the backboard. This
            is the observed thickness when viewing the court from a bird's eye
            view

        - basket_ring_inner_radius : float
            The inner radius of the basket ring

        - basket_ring_connector_width : float
            The dimension of the piece of the basket ring that connects the
            backboard to the basket ring. When viewing the court in TV view
            from above, this is the dimension in the ``y`` direction

        - basket_ring_connector_extension : float
            The distance the basket ring's connector extends from the backboard
            into the free-throw lane

        - basket_ring_thickness : float
            The thickness of the basket ring
    """

    def __init__(self, league_code = "", court_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a ``BasketballCourt`` class.

        Parameters
        ----------
        league_code : str
            The league for which the plot should be drawn. This is
            case-insensitive but should be the shortened name of the league
            (e.g. "National Basketball Association" should be either "NBA" or
            "nba"). The default is an empty string

        rotation : float
            The angle (in degrees) through which to rotate the final plot. The
            default is ``0.0``

        x_trans : float
            The amount that the ``x`` coordinates are to be shifted. By
            convention, the +``x`` axis extends from the center of the surface
            towards the right-hand basket when viewing the court in TV view.
            The default is ``0.0``

        y_trans : float
            The amount that the ``y`` coordinates are to be shifted. By
            convention, the +``y`` axis extends from the center of the surface
            towards the top of the court when viewing the court in TV view. The
            default is ``0.0``

        court_updates : dict
            A dictionary of updated parameters to use to create the basketball
            court. The default is an empty dictionary

        color_updates : dict
            A dictionary of coloring parameters to pass to the plot. Defaults
            are provided in the class per each rule book, but this allows the
            plot to be more heavily customized/styled. The default is an empty
            dictionary

        units : str
            The units that the final plot should utilize. The default units are
            the units specified in the rule book of the league. The default is
            ``"default"``

        Returns
        -------
        Nothing, but instantiates the class
        """
        # Load all pre-defined court dimensions for provided leagues
        self._load_preset_dimensions(sport = "basketball")

        # Load all unit conversions
        self._load_unit_conversions()

        # Set the league to be the lower-case version of the supplied value
        self.league_code = league_code.lower()

        # Try to get the league specified from the pre-defined set of leagues
        try:
            court_dimensions = self.league_dimensions[self.league_code]

        # If it can't be found, set the court_dimensions dictionary to be empty
        except KeyError:
            court_dimensions = {}

        # Combine the court dimensions (if found from in the pre-defined
        # leagues) with any parameter updates supplied by the user. This will
        # comprise the parameter set with which the court is to be drawn
        court_params = {
            **court_dimensions,
            **court_updates
        }

        # Set the passed parameters of the court to be the class' court_params
        # attribute
        self.court_params = court_params

        # Convert the court's units if needed
        if units.lower() != "default":
            for k, v in court_params.items():
                self.court_params[k] = self._convert_units(
                    v,
                    self.court_params["court_units"],
                    units.lower()
                )

            self.court_params["court_units"] = units.lower()

        # Set the rotation of the plot to be the supplied rotation value
        self.rotation_amt = rotation
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the court's necessary shifts. This will overwrite the default
        # values of x_trans and y_trans inherited from the BaseSurfacePlot
        # class (which is in turn inherited from BaseSurface)
        self.x_trans, self.y_trans = x_trans, y_trans

        # Create a container for the relevant features of a court
        self._features = []

        # Initialize the x and y limits for the plot be None. These will get
        # set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the default colors of the court
        default_colors = {
            "plot_background": "#d2ab6f00",
            "defensive_half_court": "#d2ab6f",
            "offensive_half_court": "#d2ab6f",
            "court_apron": "#d2ab6f",
            "center_circle_outline": "#000000",
            "center_circle_fill": "#d2ab6f",
            "division_line": "#000000",
            "endline": "#000000",
            "sideline": "#000000",
            "two_point_range": "#d2ab6f",
            "three_point_line": "#000000",
            "painted_area": "#d2ab6f",
            "lane_boundary": "#000000",
            "free_throw_circle_outline": "#000000",
            "free_throw_circle_fill": "#d2ab6f",
            "free_throw_circle_dash": "#000000",
            "lane_space_mark": "#000000",
            "inbounding_line": "#000000",
            "substitution_line": "#000000",
            "baseline_lower_defensive_box": "#000000",
            "lane_lower_defensive_box": "#000000",
            "team_bench_line": "#000000",
            "restricted_arc": "#000000",
            "backboard": "#000000",
            "basket_ring": "#f55b33",
            "net": "#ffffff"
        }

        # Combine the colors with a passed colors dictionary
        if not color_updates:
            color_updates = {}

        # Create the final color set for the features of the court
        self.feature_colors = {
            **default_colors,
            **color_updates
        }

        # Initialize the constraint on the court to confine all features to be
        # contained within the court. The feature itself is not visible (as
        # it's created by the basketball.court class)
        court_constraint_params = {
            "class": basketball_features.CourtConstraint,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "visible": False
        }
        self._initialize_feature(court_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the defensive half-court
        defensive_half_court_params = {
            "class": basketball_features.HalfCourt,
            "x_anchor": -0.25 * self.court_params.get("court_length", 0.0),
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["defensive_half_court"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(defensive_half_court_params)

        # Initialize the offensive half-court
        offensive_half_court_params = {
            "class": basketball_features.HalfCourt,
            "x_anchor": 0.25 * self.court_params.get("court_length", 0.0),
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["offensive_half_court"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(offensive_half_court_params)

        # Initialize the court apron
        court_apron_params = {
            "class": basketball_features.CourtApron,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "court_apron_endline": self.court_params.get(
                "court_apron_endline",
                0.0
            ),
            "court_apron_sideline": self.court_params.get(
                "court_apron_sideline",
                0.0
            ),
            "court_apron_to_boundary": self.court_params.get(
                "court_apron_to_boundary",
                0.0
            ),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["court_apron"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(court_apron_params)

        # Initialize the center circle(s)
        center_circle_params_type = type(
            self.court_params.get("center_circle_radius", [])
        )

        if center_circle_params_type == float:
            center_circle_radii = [
                self.court_params["center_circle_radius"]
            ]

        elif center_circle_params_type == list:
            center_circle_radii = self.court_params.get(
                "center_circle_radius",
                [0.0]
            )

        center_circle_outline_color_type = type(self.feature_colors[
            "center_circle_outline"
        ])

        if center_circle_outline_color_type == str:
            center_circle_outline_color = [
                self.feature_colors["center_circle_outline"]
            ]

        else:
            center_circle_outline_color = self.feature_colors.get(
                "center_circle_outline",
                ["#000000"]
            )

        center_circle_fill_color_type = type(self.feature_colors[
            "center_circle_fill"
        ])

        if center_circle_fill_color_type == str:
            center_circle_fill_color = [
                self.feature_colors["center_circle_fill"]
            ]

        else:
            center_circle_fill_color = self.feature_colors.get(
                "center_circle_fill",
                ["#d2ab6f"]
            )

        n_center_circles = max(
            len(center_circle_radii),
            len(center_circle_outline_color),
            len(center_circle_fill_color)
        )

        while (len(center_circle_radii) != n_center_circles):
            if len(center_circle_radii) < n_center_circles:
                center_circle_radii.append(0.0)

        while (len(center_circle_outline_color) != n_center_circles):
            if len(center_circle_outline_color) < n_center_circles:
                center_circle_outline_color.append("#000000")

        while (len(center_circle_fill_color) != n_center_circles):
            if len(center_circle_fill_color) < n_center_circles:
                center_circle_fill_color.append("#d2ab6f")

        center_circle_params = pd.DataFrame({
            "center_circle_radii": center_circle_radii,
            "center_circle_outline_color": center_circle_outline_color,
            "center_circle_fill_color": center_circle_fill_color
        })

        for circle_no, circle in center_circle_params.iterrows():
            center_circle_outline_params = {
                "class": basketball_features.CenterCircleOutline,
                "x_anchor": 0.0,
                "y_anchor": 0.0,
                "reflect_x": True,
                "reflect_y": False,
                "feature_radius": circle["center_circle_radii"],
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "facecolor": circle["center_circle_outline_color"],
                "edgecolor": None,
                "zorder": 16
            }
            self._initialize_feature(center_circle_outline_params)

            center_circle_fill_params = {
                "class": basketball_features.CenterCircleFill,
                "x_anchor": 0.0,
                "y_anchor": 0.0,
                "reflect_x": False,
                "reflect_y": False,
                "feature_radius": circle["center_circle_radii"],
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "facecolor": circle["center_circle_fill_color"],
                "edgecolor": None,
                "zorder": 6
            }
            self._initialize_feature(center_circle_fill_params)

        # Initialize the division line
        division_line_params = {
            "class": basketball_features.DivisionLine,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "division_line_extension": self.court_params.get(
                "division_line_extension",
                0.0
            ),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["division_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(division_line_params)

        # Initialize the two-point ranges (shapes inside the three-point line)
        # and the three-point lines

        # The three-point line parameters are more easily interpretable when
        # passed as lists so that more than one line may be drawn (e.g. if a
        # court has a college and professional line painted on it)

        # Start by getting the type of dimension passed
        three_point_params_type = type(
            self.court_params.get(
                "basket_center_to_three_point_arc",
                []
            )
        )

        # If the passed dimension is a singular number, convert it to a list
        # of length 1
        if three_point_params_type == float:
            basket_center_to_three_point_arc = [
                self.court_params["basket_center_to_three_point_arc"]
            ]

        else:
            basket_center_to_three_point_arc = self.court_params.get(
                "basket_center_to_three_point_arc",
                []
            )

        # Repeat the same thing with the basket_center_to_corner_three
        # parameter(s)
        basket_center_to_corner_three_type = type(
            self.court_params.get(
                "basket_center_to_corner_three",
                []
            )
        )

        if basket_center_to_corner_three_type == float:
            basket_center_to_corner_three = [
                self.court_params["basket_center_to_corner_three"]
            ]

        else:
            basket_center_to_corner_three = self.court_params.get(
                "basket_center_to_corner_three",
                []
            )

        n_three_point_lines = max(
            len(basket_center_to_three_point_arc),
            len(basket_center_to_corner_three)
        )

        while (len(basket_center_to_three_point_arc) != n_three_point_lines):
            if len(basket_center_to_three_point_arc) < n_three_point_lines:
                basket_center_to_three_point_arc.append(0.0)

        while (len(basket_center_to_corner_three) != n_three_point_lines):
            if len(basket_center_to_corner_three) < n_three_point_lines:
                basket_center_to_corner_three.append(0.0)

        if type(self.feature_colors["two_point_range"]) == str:
            two_point_range_colors = [
                self.feature_colors["two_point_range"]
            ]

        else:
            two_point_range_colors = self.feature_colors["two_point_range"]

        if type(self.feature_colors["three_point_line"]) == str:
            three_point_line_colors = [
                self.feature_colors["three_point_line"]
            ]

        else:
            three_point_line_colors = self.feature_colors["three_point_line"]

        while (len(two_point_range_colors) != n_three_point_lines):
            if len(two_point_range_colors) > n_three_point_lines:
                two_point_range_colors.pop(-1)
            if len(two_point_range_colors) < n_three_point_lines:
                two_point_range_colors.append("#d2ab6f")

        while (len(three_point_line_colors) != n_three_point_lines):
            if len(three_point_line_colors) > n_three_point_lines:
                three_point_line_colors.pop(-1)
            if len(three_point_line_colors) < n_three_point_lines:
                three_point_line_colors.append("#000000")

        # Get the arcs to be an iterable parameter. This may also be an empty
        # list, in which case no three-point line will be drawn
        three_point_arcs = pd.DataFrame({
            "basket_center_to_three_point_arc":
                basket_center_to_three_point_arc,
            "basket_center_to_corner_three": basket_center_to_corner_three,
            "three_point_line_color": three_point_line_colors,
            "two_point_range_color": two_point_range_colors
        })

        # The three-point arc distances should be sorted from greatest distance
        # to least to avoid plotting over each other
        three_point_arcs = three_point_arcs.sort_values(
            by = "basket_center_to_three_point_arc",
            ascending = False
        )

        # Iterate over the three-point arcs
        for arc_no, arc_dims in three_point_arcs.iterrows():
            # Create the two-point shot range. This is the area inside the
            # three-point arc
            two_point_range_params = {
                "class": basketball_features.TwoPointRange,
                "x_anchor": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0)
                ),
                "y_anchor": 0.0,
                "reflect_x": True,
                "reflect_y": False,
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "feature_radius": (
                    arc_dims["basket_center_to_three_point_arc"] -
                    self.court_params.get("line_thickness", 0.0)
                ),
                "basket_center_to_baseline": self.court_params.get(
                    "basket_center_to_baseline",
                    0.0
                ),
                "basket_center_to_corner_three": arc_dims[
                    "basket_center_to_corner_three"
                ],
                "court_length": self.court_params.get("court_length", 0.0),
                "court_width": self.court_params.get("court_width", 0.0),
                "facecolor": arc_dims["two_point_range_color"],
                "edgecolor": None,
                "zorder": 6
            }
            self._initialize_feature(two_point_range_params)

            # Create the three-point line
            three_point_line_params = {
                "class": basketball_features.ThreePointLine,
                "x_anchor": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0)
                ),
                "y_anchor": 0.0,
                "reflect_x": True,
                "reflect_y": False,
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "feature_radius": arc_dims["basket_center_to_three_point_arc"],
                "basket_center_to_baseline": self.court_params.get(
                    "basket_center_to_baseline",
                    0.0
                ),
                "basket_center_to_corner_three": arc_dims[
                    "basket_center_to_corner_three"
                ],
                "court_length": self.court_params.get("court_length", 0.0),
                "court_width": self.court_params.get("court_width", 0.0),
                "facecolor": arc_dims["three_point_line_color"],
                "edgecolor": None,
                "zorder": 17
            }
            self._initialize_feature(three_point_line_params)

        # Initialize the free-throw lanes and painted area

        # This will follow a similar pattern described above in the three-point
        # line drawing. However, to keep this a bit more organized, the Start
        # by getting the types of the lane parameters and force them to be
        # lists
        lane_length_type = type(self.court_params.get("lane_length", []))

        if lane_length_type == float:
            lane_lengths = [self.court_params["lane_length"]]

        else:
            lane_lengths = self.court_params.get("lane_length", [0.0])

        lane_width_type = type(self.court_params.get("lane_width", []))

        if lane_width_type == float:
            lane_widths = [self.court_params["lane_width"]]

        else:
            lane_widths = self.court_params.get("lane_width", [0.0])

        paint_margin_type = type(self.court_params.get("paint_margin", []))

        if paint_margin_type == float:
            paint_margins = [self.court_params["paint_margin"]]

        else:
            paint_margins = self.court_params.get("paint_margin", [0.0])

        painted_area_visibility_type = type(self.court_params.get(
            "painted_area_visibility",
            []
        ))

        if painted_area_visibility_type == bool:
            painted_area_visibility = [
                self.court_params["painted_area_visibility"]
            ]

        else:
            painted_area_visibility = self.court_params.get(
                "painted_area_visibility",
                [True]
            )

        lane_boundary_visibility_type = type(self.court_params.get(
            "lane_boundary_visibility",
            []
        ))

        if lane_boundary_visibility_type == bool:
            lane_boundary_visibility = [
                self.court_params["lane_boundary_visibility"]
            ]

        else:
            lane_boundary_visibility = self.court_params.get(
                "lane_boundary_visibility",
                [True]
            )

        n_lanes = max(
            len(lane_lengths),
            len(lane_widths),
            len(paint_margins),
            len(painted_area_visibility),
            len(lane_boundary_visibility)
        )

        painted_area_colors = self.feature_colors["painted_area"]

        if type(painted_area_colors) != list:
            painted_area_colors = [painted_area_colors]

        lane_boundary_colors = self.feature_colors["lane_boundary"]

        if type(lane_boundary_colors) != list:
            lane_boundary_colors = [lane_boundary_colors]

        while (len(painted_area_colors) != n_lanes):
            if len(painted_area_colors) < n_lanes:
                painted_area_colors.append("#d2ab6f00")

        while (len(lane_boundary_colors) != n_lanes):
            if len(lane_boundary_colors) < n_lanes:
                lane_boundary_colors.append("#00000000")

        while (len(lane_lengths) != n_lanes):
            if len(lane_lengths) < n_lanes:
                lane_lengths.append(0.0)

        while (len(lane_widths) != n_lanes):
            if len(lane_widths) < n_lanes:
                lane_widths.append(0.0)

        while (len(paint_margins) != n_lanes):
            if len(paint_margins) < n_lanes:
                paint_margins.append(0.0)

        while (len(painted_area_visibility) != n_lanes):
            if len(painted_area_visibility) < n_lanes:
                painted_area_visibility.append(False)

        while (len(lane_boundary_visibility) != n_lanes):
            if len(lane_boundary_visibility) < n_lanes:
                lane_boundary_visibility.append(False)

        # The lane dimensions are combined into a data frame here so that the
        # parameters may be ordered easily and together. The ordering
        # allows larger features (e.g. an NBA lane and painted area) to be
        # drawn before drawing smaller features (e.g. an NCAA lane and painted
        # area) in a manner that prevents the smaller feature from being hidden
        lane_params = pd.DataFrame({
            "lane_length": lane_lengths,
            "lane_width": lane_widths,
            "paint_margin": paint_margins,
            "painted_area_visibility": painted_area_visibility,
            "lane_boundary_visibility": lane_boundary_visibility,
            "painted_area_color": painted_area_colors,
            "lane_boundary_color": lane_boundary_colors
        })

        # Reorder from largest to smallest
        lane_params = lane_params.sort_values(
            by = ["lane_length", "lane_width"],
            ascending = [False, False]
        ).reset_index()

        # Loop over the rows of the data frame and instantiate the painted area
        # and lane boundary (as required)
        for lane_no, dims in lane_params.iterrows():
            painted_area_params = {
                "class": basketball_features.PaintedArea,
                "x_anchor": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    dims["lane_length"] +
                    self.court_params.get("line_thickness", 0.0)
                ),
                "y_anchor": 0.0,
                "visible": dims["painted_area_visibility"],
                "court_length": self.court_params.get("court_length", 0.0),
                "court_width": self.court_params.get("court_width", 0.0),
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "reflect_x": True,
                "reflect_y": False,
                "lane_length": dims["lane_length"],
                "lane_width": dims["lane_width"],
                "paint_margin": dims["paint_margin"],
                "facecolor": dims["painted_area_color"],
                "edgecolor": None,
                "zorder": 7
            }
            self._initialize_feature(painted_area_params)

            lane_boundary_params = {
                "class": basketball_features.FreeThrowLaneBoundary,
                "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
                "y_anchor": 0.0,
                "visible": dims["lane_boundary_visibility"],
                "court_length": self.court_params.get("court_length", 0.0),
                "court_width": self.court_params.get("court_width", 0.0),
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "reflect_x": True,
                "reflect_y": False,
                "lane_length": dims["lane_length"],
                "lane_width": dims["lane_width"],
                "facecolor": dims["lane_boundary_color"],
                "edgecolor": None,
                "zorder": 16
            }
            self._initialize_feature(lane_boundary_params)

        # Draw the lane space marks in the same way that the lane boundaries
        # and painted areas were just drawn
        lane_space_mark_lengths_type = type(self.court_params.get(
            "lane_space_mark_lengths",
            []
        ))

        if lane_space_mark_lengths_type == float:
            lane_space_mark_lengths = [[
                self.court_params["lane_space_mark_lengths"]
            ]]

        else:
            lane_space_mark_lengths = self.court_params.get(
                "lane_space_mark_lengths",
                [[0.0]]
            )

        lane_space_mark_widths_type = type(self.court_params.get(
            "lane_space_mark_widths",
            []
        ))

        if lane_space_mark_widths_type == float:
            lane_space_mark_widths = [
                self.court_params["lane_space_mark_widths"]
            ]

        else:
            lane_space_mark_widths = self.court_params.get(
                "lane_space_mark_widths",
                [[0.0]]
            )

        lane_space_mark_separations_type = type(self.court_params.get(
            "lane_space_mark_separations",
            []
        ))

        if lane_space_mark_separations_type == float:
            lane_space_mark_separations = [[
                self.court_params["lane_space_mark_separations"]
            ]]

        else:
            lane_space_mark_separations = self.court_params.get(
                "lane_space_mark_separations",
                [[0.0]]
            )

        lane_space_mark_visibility_types = type(self.court_params.get(
            "lane_space_mark_visibility",
            []
        ))

        if lane_space_mark_visibility_types == bool:
            lane_space_mark_visibility = [
                self.court_params["lane_space_mark_visibility"]
            ]

        else:
            lane_space_mark_visibility = self.court_params.get(
                "lane_space_mark_visibility",
                [False]
            )

        while (len(lane_space_mark_lengths) != n_lanes):
            if len(lane_space_mark_lengths) < n_lanes:
                lane_space_mark_lengths.append([])

        while (len(lane_space_mark_widths) != n_lanes):
            if len(lane_space_mark_widths) < n_lanes:
                lane_space_mark_widths.append([])

        while (len(lane_space_mark_separations) != n_lanes):
            if len(lane_space_mark_separations) < n_lanes:
                lane_space_mark_separations.append([])

        while (len(lane_space_mark_visibility) != n_lanes):
            if len(lane_space_mark_visibility) < n_lanes:
                lane_space_mark_visibility.append([])

        n_marks = max(
            len(lane_space_mark_lengths[0]),
            len(lane_space_mark_separations[0])
        )

        y_anchors = []
        for lane_no in range(0, n_lanes):
            while (len(lane_space_mark_lengths[lane_no]) != n_marks):
                if len(lane_space_mark_lengths[lane_no]) < n_marks:
                    lane_space_mark_lengths[lane_no].append(0.0)

            while (len(lane_space_mark_separations[lane_no]) != n_marks):
                if len(lane_space_mark_separations[lane_no]) < n_marks:
                    lane_space_mark_separations[lane_no].append(0.0)

            y_anchors.append(lane_widths[lane_no] / 2.0)

        # Combine the dimensions into a data frame
        dim_set = pd.DataFrame({
            "y_anchor": y_anchors,
            "lane_space_mark_lengths": lane_space_mark_lengths,
            "lane_space_mark_separations": lane_space_mark_separations,
            "lane_space_mark_depths": lane_space_mark_widths,
            "lane_space_mark_visibility": lane_space_mark_visibility
        })

        # Re-order from widest lane to smallest
        dim_set = dim_set.sort_values(by = "y_anchor").reset_index()

        # Instantiate the features
        for set_no, dims in dim_set.iterrows():
            # Get the starting parameters for each set of lane space marks
            x_anchor = (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0)
            )
            mark_lengths = dims["lane_space_mark_lengths"]
            separations = dims["lane_space_mark_separations"]
            mark_depth = dims["lane_space_mark_depths"]

            # Iterate over the lane space marks to instantiate them
            for mark_no in range(len(mark_lengths)):
                x_anchor -= separations[mark_no]

                mark_params = {
                    "class": basketball_features.LaneSpaceMark,
                    "x_anchor": x_anchor,
                    "y_anchor": dims["y_anchor"],
                    "reflect_x": True,
                    "reflect_y": True,
                    "visible": dims["lane_space_mark_visibility"],
                    "feature_thickness": mark_lengths[mark_no],
                    "mark_depth": mark_depth,
                    "facecolor": self.feature_colors["lane_space_mark"],
                    "edgecolor": None,
                    "zorder": 16
                }
                self._initialize_feature(mark_params)

                # Adjust the x-position for the next mark
                x_anchor -= mark_lengths[mark_no]

        # Initialize the free-throw circle
        free_throw_circle_outline_params = {
            "class": basketball_features.FreeThrowCircleOutline,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0) -
                self.court_params.get("free_throw_line_to_backboard", 0.0) +
                self.court_params.get("line_thickness", 0.0) / 2.0
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_radius": self.court_params.get(
                "free_throw_circle_radius",
                0.0
            ),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["free_throw_circle_outline"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(free_throw_circle_outline_params)

        free_throw_circle_fill_params = {
            "class": basketball_features.FreeThrowCircleFill,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0) -
                self.court_params.get("free_throw_line_to_backboard", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_radius": self.court_params.get(
                "free_throw_circle_radius",
                0.0
            ),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["free_throw_circle_fill"],
            "edgecolor": None,
            "zorder": 7
        }
        self._initialize_feature(free_throw_circle_fill_params)

        # Initialize the overhanging component of the free-throw circle
        overhang_s = self.court_params.get("free_throw_circle_overhang", 0.0)
        overhang_r = self.court_params.get("free_throw_circle_radius", 0.0)
        try:
            end_theta = (overhang_s / overhang_r) / np.pi
        except ZeroDivisionError:
            end_theta = 0.0

        end_theta = 0.5 - end_theta

        free_throw_circle_overhang_params = {
            "class": basketball_features.FreeThrowCircleOutlineDash,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0) -
                self.court_params.get("free_throw_line_to_backboard", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": True,
            "feature_radius": self.court_params.get(
                "free_throw_circle_radius",
                0.0
            ),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "start_angle": 0.5,
            "end_angle": end_theta,
            "facecolor": self.feature_colors["free_throw_circle_dash"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(free_throw_circle_overhang_params)

        # Initialize the dashed component of the free-throw circle
        n_dashes = self.court_params.get("n_free_throw_circle_dashes", 0.0)

        if n_dashes > 0:
            # Compute the angle through which the dash will be traced
            free_throw_circle_s = self.court_params.get(
                "free_throw_dash_length",
                0.0
            )
            free_throw_circle_r = self.court_params.get(
                "free_throw_circle_radius",
                0.0
            )

            free_throw_dash_spacing_s = self.court_params.get(
                "free_throw_dash_spacing",
                0.0
            )
            free_throw_dash_spacing_r = self.court_params.get(
                "free_throw_circle_radius",
                0.0
            )

            try:
                theta_dashes = (
                    free_throw_circle_s / free_throw_circle_r
                ) / np.pi
                theta_spaces = (
                    free_throw_dash_spacing_s / free_throw_dash_spacing_r
                ) / np.pi

            except ZeroDivisionError:
                theta_dashes = 0.0
                theta_spaces = 0.0

            # Get the starting angle for the first dash. This will be updated
            # by the below loop
            start_s = self.court_params.get("free_throw_circle_overhang", 0.0)
            try:
                start_angle = 0.5 - ((start_s / free_throw_circle_r) / np.pi)
                start_angle -= theta_spaces
            except ZeroDivisionError:
                start_angle = 0.5 - theta_spaces

            # Create the dashes
            for dash in range(0, int(n_dashes)):
                free_throw_circle_dash_params = {
                    "class": basketball_features.FreeThrowCircleOutlineDash,
                    "x_anchor": (
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "backboard_face_to_baseline",
                            0.0
                        ) -
                        self.court_params.get(
                            "free_throw_line_to_backboard",
                            0.0
                        ) +
                        self.court_params.get("line_thickness", 0.0) / 2.0
                    ),
                    "y_anchor": 0.0,
                    "reflect_x": True,
                    "reflect_y": False,
                    "court_length": self.court_params.get("court_length", 0.0),
                    "court_width": self.court_params.get("court_width", 0.0),
                    "start_angle": start_angle,
                    "end_angle": start_angle - theta_spaces,
                    "feature_radius": self.court_params.get(
                        "free_throw_circle_radius",
                        0.0
                    ),
                    "feature_thickness": self.court_params.get(
                        "line_thickness",
                        0.0
                    ),
                    "facecolor": self.feature_colors["free_throw_circle_dash"],
                    "zorder": 17
                }
                self._initialize_feature(free_throw_circle_dash_params)

                start_angle = start_angle - theta_dashes - theta_spaces

        # Initialize the end lines
        endline_params = {
            "class": basketball_features.Endline,
            "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["endline"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(endline_params)

        # Initialize the sidelines
        sideline_params = {
            "class": basketball_features.Sideline,
            "x_anchor": 0.0,
            "y_anchor": self.court_params.get("court_width", 0.0) / 2.0,
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["sideline"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(sideline_params)

        # Initialize the lower defensive box marks
        baseline_lower_defensive_box_mark_params = {
            "class": basketball_features.LowerDefensiveBoxMark,
            "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
            "y_anchor": self.court_params.get(
                "baseline_lower_defensive_box_marks_int_sep",
                0.0
            ) / 2.0,
            "reflect_x": True,
            "reflect_y": True,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "extension": self.court_params.get(
                "lower_defensive_box_mark_extension",
                0.0,
            ),
            "drawn_direction": "left_to_right",
            "facecolor": self.feature_colors["baseline_lower_defensive_box"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(baseline_lower_defensive_box_mark_params)

        lane_lower_defensive_box_mark_params = {
            "class": basketball_features.LowerDefensiveBoxMark,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get(
                    "baseline_to_lane_lower_defensive_box_marks",
                    0.0
                )
            ),
            "y_anchor": self.court_params.get(
                "lane_lower_defensive_box_marks_int_sep",
                0.0
            ) / 2.0,
            "reflect_x": True,
            "reflect_y": True,
            "visible": self.court_params.get(
                "lane_lower_defensive_box_marks_visibility",
                False
            ),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "extension": self.court_params.get(
                "lower_defensive_box_mark_extension",
                0.0,
            ),
            "drawn_direction": "top_down",
            "facecolor": self.feature_colors["lane_lower_defensive_box"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(lane_lower_defensive_box_mark_params)

        # Initialize the inbounding lines
        inbounding_line_to_baseline_type = type(self.court_params.get(
            "inbounding_line_to_baseline",
            []
        ))

        if inbounding_line_to_baseline_type == float:
            inbounding_line_to_baseline = [
                self.court_params["inbounding_line_to_baseline"]
            ]

        else:
            inbounding_line_to_baseline = self.court_params.get(
                "inbounding_line_to_baseline",
                [0.0]
            )

        inbounding_line_in_play_ext_type = type(self.court_params.get(
            "inbounding_line_in_play_ext",
            []
        ))

        if inbounding_line_in_play_ext_type == float:
            inbounding_line_in_play_ext = [
                self.court_params["inbounding_line_in_play_ext"]
            ]

        else:
            inbounding_line_in_play_ext = self.court_params.get(
                "inbounding_line_in_play_ext",
                [0.0]
            )

        inbounding_line_out_of_bounds_ext_type = type(self.court_params.get(
            "inbounding_line_out_of_bounds_ext",
            []
        ))

        if inbounding_line_out_of_bounds_ext_type == float:
            inbounding_line_oob_ext = [
                self.court_params["inbounding_line_out_of_bounds_ext"]
            ]

        else:
            inbounding_line_oob_ext = self.court_params.get(
                "inbounding_line_out_of_bounds_ext",
                [0.0]
            )

        symmetric_inbounding_line_type = type(self.court_params.get(
            "symmetric_inbounding_line",
            []
        ))

        if symmetric_inbounding_line_type == bool:
            symmetric_inbounding_line = [
                self.court_params["symmetric_inbounding_line"]
            ]

        else:
            symmetric_inbounding_line = self.court_params.get(
                "symmetric_inbounding_line",
                [False]
            )

        inbounding_line_anchor_side_type = type(self.court_params.get(
            "inbounding_line_anchor_side",
            []
        ))

        if inbounding_line_anchor_side_type == float:
            inbounding_line_anchor_side = [
                self.court_params["inbounding_line_anchor_side"]
            ]

        else:
            inbounding_line_anchor_side = self.court_params.get(
                "inbounding_line_anchor_side",
                [1.0]
            )

        max_n_inbounding_lines = max(
            len(inbounding_line_to_baseline),
            len(inbounding_line_in_play_ext),
            len(inbounding_line_oob_ext),
            len(symmetric_inbounding_line),
            len(inbounding_line_anchor_side)
        )

        while (len(inbounding_line_to_baseline) != max_n_inbounding_lines):
            if len(inbounding_line_to_baseline) < max_n_inbounding_lines:
                inbounding_line_to_baseline.append(
                    inbounding_line_to_baseline[0]
                )

        while (len(inbounding_line_in_play_ext) != max_n_inbounding_lines):
            if len(inbounding_line_in_play_ext) < max_n_inbounding_lines:
                inbounding_line_in_play_ext.append(
                    inbounding_line_in_play_ext[0]
                )

        while (len(inbounding_line_oob_ext) != max_n_inbounding_lines):
            if len(inbounding_line_oob_ext) < max_n_inbounding_lines:
                inbounding_line_oob_ext.append(
                    inbounding_line_oob_ext[0]
                )

        while (len(symmetric_inbounding_line) != max_n_inbounding_lines):
            if len(symmetric_inbounding_line) < max_n_inbounding_lines:
                symmetric_inbounding_line.append(False)

        while (len(inbounding_line_anchor_side) != max_n_inbounding_lines):
            if len(inbounding_line_anchor_side) < max_n_inbounding_lines:
                inbounding_line_anchor_side.append(
                    inbounding_line_anchor_side[0]
                )

        inbounding_lines = pd.DataFrame({
            "inbounding_line_to_baseline": inbounding_line_to_baseline,
            "inbounding_line_in_play_ext": inbounding_line_in_play_ext,
            "inbounding_line_oob_ext": inbounding_line_oob_ext,
            "symmetric_inbounding_line": symmetric_inbounding_line,
            "inbounding_line_anchor_side": inbounding_line_anchor_side
        })

        if self.court_params.get("bench_side", "top").lower() != "top":
            inbounding_lines["inbounding_line_anchor_side"] *= -1.0

        inbounding_lines["drawn_direction"] = "top_down"
        inbounding_lines.loc[
            inbounding_lines["inbounding_line_anchor_side"] < 1,
            "drawn_direction"
        ] = "bottom_up"

        for set_no, dims in inbounding_lines.iterrows():
            inbounding_line_params = {
                "class": basketball_features.InboundingLine,
                "x_anchor": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    dims["inbounding_line_to_baseline"]
                ),
                "y_anchor": (
                    dims["inbounding_line_anchor_side"] *
                    (self.court_params.get("court_width", 0.0) / 2.0)
                ),
                "reflect_x": True,
                "reflect_y": dims["symmetric_inbounding_line"],
                "is_constrained": False,
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "drawn_direction": dims["drawn_direction"],
                "in_play_ext": dims["inbounding_line_in_play_ext"],
                "out_of_bounds_ext": dims["inbounding_line_oob_ext"],
                "court_length": self.court_params.get("court_length", 0.0),
                "court_width": self.court_params.get("court_width", 0.0),
                "facecolor": self.feature_colors["inbounding_line"],
                "edgecolor": None,
                "zorder": 18
            }
            self._initialize_feature(inbounding_line_params)

        # Initialize the substitution areas
        if self.court_params.get("bench_side", "top").lower() == "top":
            bench_side = 1.0
            drawn_direction = "bottom_up"

        else:
            bench_side = -1.0
            drawn_direction = "top_down"

        substitution_line_params = {
            "class": basketball_features.SubstitutionLine,
            "x_anchor": (
                self.court_params.get("substitution_line_ext_sep", 0.0) / 2.0
            ),
            "y_anchor": (
                bench_side *
                self.court_params.get("court_width", 0.0) / 2.0
            ),
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "substitution_line_width": self.court_params.get(
                "substitution_line_width",
                0.0
            ),
            "drawn_direction": drawn_direction,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["substitution_line"],
            "edgecolor": None,
            "zorder": 18
        }
        self._initialize_feature(substitution_line_params)

        # Initialize the team bench areas
        team_bench_line_params = {
            "class": basketball_features.TeamBenchLine,
            "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
            "y_anchor": (
                bench_side * (
                    (self.court_params.get("court_width", 0.0) / 2.0) +
                    self.court_params.get("line_thickness", 0.0)
                )
            ),
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "extension": self.court_params.get("team_bench_line_ext", 0.0),
            "drawn_direction": drawn_direction,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["team_bench_line"],
            "edgecolor": None,
            "zorder": 18
        }
        self._initialize_feature(team_bench_line_params)

        # Initialize the restricted arcs
        restricted_arc_params = {
            "class": basketball_features.RestrictedArc,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "feature_radius": self.court_params.get(
                "restricted_arc_radius",
                0.0
            ),
            "backboard_to_center_of_basket": (
                self.court_params.get("basket_center_to_baseline", 0.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0)
            ),
            "visible": self.court_params.get("restricted_arc_visible", True),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["restricted_arc"],
            "edgecolor": None,
            "zorder": 25
        }
        self._initialize_feature(restricted_arc_params)

        # Initialize the backboards
        backboard_params = {
            "class": basketball_features.Backboard,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_thickness": self.court_params.get(
                "backboard_thickness",
                0.0
            ),
            "backboard_width": self.court_params.get(
                "backboard_width",
                0.0
            ),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["backboard"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(backboard_params)

        # Initialize the basket rings
        basket_ring_params = {
            "class": basketball_features.BasketRing,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "basket_ring_connector_extension": self.court_params.get(
                "basket_ring_connector_extension",
                0.0
            ),
            "basket_ring_connector_width": self.court_params.get(
                "basket_ring_connector_width",
                0.0
            ),
            "backboard_face_to_basket_center": (
                self.court_params.get("basket_center_to_baseline", 0.0) -
                self.court_params.get("backboard_face_to_baseline", 0.0)
            ),
            "feature_thickness": self.court_params.get(
                "basket_ring_thickness",
                0.0
            ),
            "feature_radius": self.court_params.get(
                "basket_ring_inner_radius",
                0.0
            ),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["basket_ring"],
            "edgecolor": None,
            "zorder": 18
        }
        self._initialize_feature(basket_ring_params)

        # Initialize the nets
        net_params = {
            "class": basketball_features.Net,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) -
                self.court_params.get("basket_center_to_baseline", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_radius": self.court_params.get(
                "basket_ring_inner_radius",
                0.0
            ),
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "facecolor": self.feature_colors["net"],
            "edgecolor": None,
            "zorder": 19
        }
        self._initialize_feature(net_params)

        # Initialize all other features passed as keyword arguments
        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = "full", xlim = None, ylim = None,
             rotation = None):
        """Draw the court.

        Parameters
        ----------
        ax : matplotlib.Axes
            An Axes object onto which the plot can be drawn. If ``None`` is
            supplied, then the currently-active Axes object will be used

        display_range : str, optional
            The portion of the surface to display. The entire surface will
            always be drawn under the hood, however this parameter limits what
            is shown in the final plot. The following explain what each display
            range corresponds to:

                - ``"full"``: The entire court
                - ``"offense"``: The attacking/offensive half court
                - ``"offence"``: The attacking/offensive half court
                - ``"offensivehalfcourt"``: The attacking/offensive half court
                - ``"offensive_half_court"``: The attacking/offensive half
                    court
                - ``"offensive half court"``: The attacking/offensive half
                    court
                - ``"defense"``: The defensive half court
                - ``"defence"``: The defensive half court
                - ``"defensivehalfcourt"``: The defensive half court
                - ``"defensive_half_court"``: The defensive half court
                - ``"defensive half court"``: The defensive half court
                - ``"offensivekey"``: The attacking/offensive key
                - ``"offensive_key"``: The attacking/offensive key
                - ``"offensive key"``: The attacking/offensive key
                - ``"attackingkey"``: The attacking/offensive key
                - ``"attacking_key"``: The attacking/offensive key
                - ``"attacking key"``: The attacking/offensive key
                - ``"defensivekey"``: The defensive key
                - ``"defensive_key"``: The defensive key
                - ``"defensive key"``: The defensive key
                - ``"defendingkey"``: The defensive key
                - ``"defending_key"``: The defensive key
                - ``"offensivepaint"``: The attacking/offensive painted area
                - ``"offensive_paint"``: The attacking/offensive painted area
                - ``"attackingpaint"``: The attacking/offensive painted area
                - ``"attacking_paint"``: The attacking/offensive painted area
                - ``"offensivelane"``: The attacking/offensive painted area
                - ``"offensive_lane"``: The attacking/offensive painted area
                - ``"offensive lane"``: The attacking/offensive painted area
                - ``"attackinglane"``: The attacking/offensive painted area
                - ``"attacking_lane"``: The attacking/offensive painted area
                - ``"attacking lane"``: The attacking/offensive painted area
                - ``"defensivepaint"``: The defensive painted area
                - ``"defensive_paint"``: The defensive painted area
                - ``"defendingpaint"``: The defensive painted area
                - ``"defending_paint"``: The defensive painted area
                - ``"defensivelane"``: The defensive painted area
                - ``"defendinglane"``: The defensive painted area
                - ``"defending_lane"``: The defensive painted area
                - ``"defending lane"``: The defensive painted area

            The default is ``"full"``

        xlim : float or tuple of floats or None
            The display range in the ``x`` direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the ``x`` coordinates to display and the upper bound will be the
            +``x`` end of the court. If a tuple, the two values will be
            used to determine the bounds. If ``None``, then the
            ``display_range`` will be used instead to set the bounds. The
            default is ``None``

        ylim : float or tuple of floats or None
            The display range in the ``y`` direction to be used. If a single
            float is provided, this will be used as the lower bound of the y
            coordinates to display and the upper bound will be the +``y`` side
            of the court. If a tuple, the two values will be used to determine
            the bounds. If ``None``, then the ``display_range`` will be used
            instead to set the bounds.  The default is ``None``

        rotation : float or None
            Angle (in degrees) through which to rotate the court when drawing.
            If used, this will set the class attribute of ``_rotation``. A
            value of ``0.0`` will correspond to a TV view of the court, where
            +``x`` is to the right and +``y`` is on top. The rotation occurs
            counterclockwise. The default is ``None``
        """
        # If there is a rotation to be applied, apply it first and set it as
        # the class attribute self._rotation
        if rotation:
            self._rotation = Affine2D().rotate_deg(rotation)

        # If an Axes object is not provided, create one to use for plotting
        if ax is None:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor(self.feature_colors["plot_background"])
            ax = plt.gca()

        # Set the aspect ratio to be equal and remove the axis to leave only
        # the plot
        ax.set_aspect("equal")
        ax.axis("off")

        # Get the transformation to apply
        transform = self._get_transform(ax)

        # Add each feature
        for feature in self._features:
            # Start by adding the feature to the current Axes object
            feature.draw(ax, transform)

            # Get the feature's visibility attribute
            visible = feature.visible

            # Define the surface's constraint
        constraint = self._add_surface_constraint(ax, transform)

        # Add each feature
        for feature in self._features:
            # Start by adding the feature to the current Axes object
            drawn_feature = feature.draw(ax, transform)

            if feature.is_constrained:
                drawn_feature.set_clip_path(constraint)

            else:
                # Get the feature's visibility attribute
                visible = feature.visible

                # Assuming the feature is visible (and is not the court
                # constraint), get the feature's x and y limits to ensure it
                # lies within the bounds of the court
                if visible and not isinstance(
                    feature,
                    basketball_features.CourtConstraint
                ):
                    feature_df = feature._translate_feature()

                    # If the feature doesn't have a limitation on x, set its
                    # limits to be its minimum and maximum values of x
                    if self._feature_xlim is None:
                        self._feature_xlim = [
                            feature_df["x"].min(),
                            feature_df["x"].max()
                        ]

                    # Otherwise, set the limits to be the smaller of its
                    # specified minimum and smallest x value or the larger
                    # of its specified maximum and largest x value
                    else:
                        self._feature_xlim = [
                            min(self._feature_xlim[0], feature_df["x"].min()),
                            max(self._feature_xlim[1], feature_df["x"].max())
                        ]

                    # If the feature doesn't have a limitation on y, set its
                    # limits to be its minimum and maximum values of y
                    if self._feature_ylim is None:
                        self._feature_ylim = [
                            feature_df["y"].min(),
                            feature_df["y"].max()
                        ]

                    # Otherwise, set the limits to be the smaller of its
                    # specified minimum and smallest y value or the larger
                    # of its specified maximum and largest y value
                    else:
                        self._feature_ylim = [
                            min(self._feature_ylim[0], feature_df["y"].min()),
                            max(self._feature_ylim[1], feature_df["y"].max())
                        ]

        # Set the plot's display range
        ax = self.set_plot_display_range(
            ax,
            display_range,
            xlim,
            ylim,
            for_plot = False,
            for_display = True
        )

        return ax

    def cani_plot_leagues(self, league_code = None):
        """Show if a league can be plotted, or what leagues are pre-defined.

        A user may wish to know if a specific basketball league can be plotted.
        This method allows a user to check if that specific league code comes
        shipped with ``sportypy`` for easier plotting (if they provide the
        league code), or can also show what leagues are available to be plotted

        Parameters
        ----------
        league_code : str or None
            A league code that may or may not be shipped with the package. If
            the league code is ``None``, this will display all leagues that do
            come shipped with ``sportypy``. The default is ``None``

        Returns
        -------
        Nothing, but a message will be printed out
        """
        # Define all available league codes
        available_league_codes = [k for k in self.league_dimensions.keys()]
        available_league_codes.sort()

        # If a user wants to know about a specific league, check if the league
        # comes pre-shipped with the package
        if league_code is not None:
            # Convert the league code to be all lower-case
            league_code = league_code.lower()

            # If the league code exists, return it as a list of length 1 with
            # a printed message
            if league_code in available_league_codes:
                print(f"{league_code.upper()} comes with sportypy and is "
                      "ready to use!")

            # Otherwise, alert the user that they will need to manually specify
            # the parameters of the league
            else:
                print(f"{league_code.upper()} does not come with sportypy, "
                      "but may be parameterized. Use the "
                      "cani_change_dimensions() to check what parameters are "
                      "needed.")

        # If no league code is provided, print out the list of all available
        else:
            # Preamble
            print("The following basketball leagues are available with "
                  "sportypy:\n")

            # Print the current leagues
            for league_code in available_league_codes:
                print(f"- {league_code.upper()}")

    def cani_color_features(self):
        """Determine what features of the court can be colored.

        This function is a helper function for the user to aid in plot styling
        and customization. The printed result of this method will be the names
        of the features that are able to be colored

        Returns
        -------
        Nothing, but a message will be printed out
        """
        # Preamble
        print("The following features can be colored via the color_updates "
              "parameter, with the current value in parenthesis:\n")

        # Print the current values of the colors
        for k, v in self.feature_colors.items():
            print(f"- {k} ({v})")

        # Footer
        print("\nThese colors may be updated with the update_colors() method")

    def cani_change_dimensions(self):
        """Determine what features of the court can be re-parameterized.

        This function is a helper function for the user to aid in customizing
        a court's parameters. The printed result of this method will be the
        names of the features that are able to be reparameterized. This method
        is also useful when defining new features and using an existing
        league's court dimensions as a starting point

        Returns
        -------
        Nothing, but a message will be printed out
        """
        # Preamble
        print("The following features can be reparameterized via the "
              "court_updates parameter, with the current value in "
              "parenthesis:\n")

        # Print the current values of the colors
        for k, v in self.court_params.items():
            print(f"- {k} ({v})")

        # Footer
        print("\nThese parameters may be updated with the "
              "update_court_params() method")

    def update_colors(self, color_updates = {}, *args, **kwargs):
        """Update the colors currently used in the plot.

        The colors can be passed at the initial instantiation of the class via
        the ``color_updates`` parameter, but this method allows the colors to
        be updated after the initial instantiation and will re-instantiate the
        class with the new colors

        Parameters
        ----------
        color_updates : dict
            A dictionary where the keys correspond to the name of the feature
            that's color is to be updated (see ``cani_color_features()`` method
            for a list of these names). The default is an empty dictionary

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated colors
        """
        # Start by getting the currently-used feature colors
        current_colors = self.feature_colors

        # Create a new dictionary to hold the updated colors via dictionary
        # comprehension
        updated_colors = {
            **current_colors,
            **color_updates
        }

        # Re-instantiate the class with the new colors
        self.__init__(
            court_updates = self.court_params,
            color_updates = updated_colors
        )

    def update_court_params(self, court_param_updates = {}, *args, **kwargs):
        """Update the court's defining parameters.

        This method should primarily be used in cases when plotting a league
        not currently supported by ``sportypy``

        Parameters
        ----------
        court_updates : dict
            A dictionary where the keys correspond to the name of the parameter
            of the court that is to be updated (see
            ``cani_change_dimensions()`` method for a list of these
            parameters). The default is an empty dictionary

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated parameters
        """
        # Start by getting the currently-used court parameters
        current_court_params = self.court_params

        # Create a new dictionary to hold the updated parameters via dictionary
        # comprehension
        updated_court_params = {
            **current_court_params,
            **court_param_updates
        }

        # Re-instantiate the class with the new parameters
        self.__init__(
            court_updates = updated_court_params,
            color_updates = self.feature_colors
        )

    def reset_colors(self):
        """Reset the features of the court to their default color set.

        The colors can be passed at the initial instantiation of the class via
        the ``color_updates`` parameter, and through the ``update_colors()``
        method, these can be changed. This method allows the colors to be reset
        to their default values after experiencing such a change
        """
        # Re-instantiate the class with the default colors
        default_colors = {
            "plot_background": "#d2ab6f00",
            "defensive_half_court": "#d2ab6f",
            "offensive_half_court": "#d2ab6f",
            "court_apron": "#d2ab6f",
            "center_circle_outline": "#000000",
            "center_circle_fill": "#d2ab6f",
            "division_line": "#000000",
            "endline": "#000000",
            "sideline": "#000000",
            "two_point_range": "#d2ab6f",
            "three_point_line": "#000000",
            "painted_area": "#d2ab6f",
            "lane_boundary": "#000000",
            "free_throw_circle_outline": "#000000",
            "free_throw_circle_fill": "#d2ab6f",
            "free_throw_circle_dash": "#000000",
            "lane_space_mark": "#000000",
            "inbounding_line": "#000000",
            "substitution_line": "#000000",
            "baseline_lower_defensive_box": "#000000",
            "lane_lower_defensive_box": "#000000",
            "team_bench_line": "#000000",
            "restricted_arc": "#000000",
            "backboard": "#000000",
            "basket_ring": "#f55b33",
            "net": "#ffffff"
        }

        self.__init__(
            court_updates = self.court_params,
            color_updates = default_colors
        )

    def reset_court_params(self):
        """Reset the features of the court to their default parameterizations.

        The court parameters can be passed at the initial instantiation of the
        class via the ``court_updates`` parameter, and through the
        ``update_court_params()`` method, these can be changed. This method
        allows the feature parameterization to be reset to their default values
        after experiencing such a change
        """
        # Re-instantiate the class with the default parameters
        default_params = self.league_dimensions[self.league_code]

        self.__init__(
            court_updates = default_params,
            color_updates = self.feature_colors
        )

    def _get_plot_range_limits(self, display_range = "full", xlim = None,
                               ylim = None, for_plot = False,
                               for_display = True):
        """Get the ``x`` and ``y`` limits for the displayed plot.

        Parameters
        ----------
        display_range : str
            The range of which to display the plot. This is a key that will
            be searched for in the possible display ranges. The following are
            valid ``display_range``s:

                - ``"full"``: The entire court
                - ``"offense"``: The attacking/offensive half court
                - ``"offence"``: The attacking/offensive half court
                - ``"offensivehalfcourt"``: The attacking/offensive half court
                - ``"offensive_half_court"``: The attacking/offensive half
                    court
                - ``"offensive half court"``: The attacking/offensive half
                    court
                - ``"defense"``: The defensive half court
                - ``"defence"``: The defensive half court
                - ``"defensivehalfcourt"``: The defensive half court
                - ``"defensive_half_court"``: The defensive half court
                - ``"defensive half court"``: The defensive half court
                - ``"offensivekey"``: The attacking/offensive key
                - ``"offensive_key"``: The attacking/offensive key
                - ``"offensive key"``: The attacking/offensive key
                - ``"attackingkey"``: The attacking/offensive key
                - ``"attacking_key"``: The attacking/offensive key
                - ``"attacking key"``: The attacking/offensive key
                - ``"defensivekey"``: The defensive key
                - ``"defensive_key"``: The defensive key
                - ``"defensive key"``: The defensive key
                - ``"defendingkey"``: The defensive key
                - ``"defending_key"``: The defensive key
                - ``"offensivepaint"``: The attacking/offensive painted area
                - ``"offensive_paint"``: The attacking/offensive painted area
                - ``"attackingpaint"``: The attacking/offensive painted area
                - ``"attacking_paint"``: The attacking/offensive painted area
                - ``"offensivelane"``: The attacking/offensive painted area
                - ``"offensive_lane"``: The attacking/offensive painted area
                - ``"offensive lane"``: The attacking/offensive painted area
                - ``"attackinglane"``: The attacking/offensive painted area
                - ``"attacking_lane"``: The attacking/offensive painted area
                - ``"attacking lane"``: The attacking/offensive painted area
                - ``"defensivepaint"``: The defensive painted area
                - ``"defensive_paint"``: The defensive painted area
                - ``"defendingpaint"``: The defensive painted area
                - ``"defending_paint"``: The defensive painted area
                - ``"defensivelane"``: The defensive painted area
                - ``"defendinglane"``: The defensive painted area
                - ``"defending_lane"``: The defensive painted area
                - ``"defending lane"``: The defensive painted area

            The default is ``"full"``

        xlim : float or None
            A specific limit on ``x`` for the plot. The default is ``None``

        ylim : float or None
            A specific limit on ``y`` for the plot. The default is ``None``

        for_plot : bool
            Whether the plot range limits are being set for a plot (e.g. a
            model being displayed over the surface). This utilizes the surface
            constraint to restrict the model to be inbounds. The default is
            ``False``

        for_display : bool
            Whether the plot range limits are being set for a display (e.g. to
            show the entirety of the surface in the resulting graphic). This
            will ignore the surface constraint in the resulting graphic, but
            the constraint will be respected when drawing features. The default
            is ``False``

        Returns
        -------
        xlim : tuple
            The ``x``-directional limits for displaying the plot

        ylim : tuple
            The ``y``-directional limits for displaying the plot
        """
        # Copy the supplied xlim and ylim parameters so as not to overwrite
        # the initial memory
        xlim = self.copy_(xlim)
        ylim = self.copy_(ylim)

        # If the limits are being gotten for plotting purposes, use the
        # dimensions that are internal to the surface
        if for_plot:
            half_court_length = self.court_params.get(
                "court_length",
                0.0
            ) / 2.0
            half_court_width = self.court_params.get("court_width", 0.0) / 2.0

        # If it's for display (e.g. the draw() method), add in the necessary
        # thicknesses of external features (e.g. team bench areas and
        # substitution areas)
        if for_display:
            half_court_length = (
                (self.court_params.get("court_length", 0.0) / 2.0) +
                self.court_params.get("court_apron_endline", 0.0)
            )

            half_court_width = (
                (self.court_params.get("court_width", 0.0) / 2.0) +
                self.court_params.get("court_apron_sideline", 0.0)
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            if type(
                self.court_params.get("basket_center_to_three_point_arc", 0.0)
            ) == list:
                three_point_arc_dists = self.court_params.get(
                    "basket_center_to_three_point_arc",
                    0.0
                )
                three_point_arc_dist = max(three_point_arc_dists)

            else:
                three_point_arc_dist = self.court_params.get(
                    "basket_center_to_three_point_arc",
                    0.0
                )

            if type(self.court_params.get("lane_length", 0.0)) == list:
                lane_lengths = self.court_params.get("lane_length", 0.0)
                lane_length = max(lane_lengths)

            else:
                lane_length = self.court_params.get("lane_length", 0.0)

            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (-half_court_length, half_court_length),

                # Offensive half-court
                "offense": (0.0, half_court_length),
                "offence": (0.0, half_court_length),
                "offensivehalfcourt": (0.0, half_court_length),
                "offensive_half_court": (0.0, half_court_length),
                "offensive half court": (0.0, half_court_length),

                # Defensive half-court
                "defense": (-half_court_length, 0.0),
                "defence": (-half_court_length, 0.0),
                "defensivehalfcourt": (-half_court_length, 0.0),
                "defensive_half_court": (-half_court_length, 0.0),
                "defensive half court": (-half_court_length, 0.0),

                # Offensive key area
                "offensivekey": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    three_point_arc_dist - 3.0,
                    half_court_length
                ),

                "offensive_key": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    three_point_arc_dist - 3.0,
                    half_court_length
                ),

                "offensive key": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    three_point_arc_dist - 3.0,
                    half_court_length
                ),

                "attackingkey": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    three_point_arc_dist - 3.0,
                    half_court_length
                ),

                "attacking_key": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    three_point_arc_dist - 3.0,
                    half_court_length
                ),

                "attacking key": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    three_point_arc_dist - 3.0,
                    half_court_length
                ),

                # Defensive key area
                "defensivekey": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        three_point_arc_dist - 3.0
                    )
                ),

                "defensive_key": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        three_point_arc_dist - 3.0
                    )
                ),

                "defensive key": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        three_point_arc_dist - 3.0
                    )
                ),

                "defendingkey": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        three_point_arc_dist - 3.0
                    )
                ),

                "defending_key": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        three_point_arc_dist - 3.0
                    )
                ),

                # Painted area
                "offensivepaint": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "offensive_paint": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "attackingpaint": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "attacking_paint": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "offensivelane": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "offensive_lane": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "offensive lane": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "attackinglane": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "attacking_lane": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "attacking lane": (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    lane_length -
                    self.court_params.get("basket_center_to_baseline", 0.0) -
                    self.court_params.get("free_throw_circle_radius", 0.0),
                    half_court_length
                ),

                "defensivepaint": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defensive_paint": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defendingpaint": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defending_paint": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defensivelane": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defensive_lane": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defendinglane": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defending_lane": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                ),

                "defending lane": (
                    -half_court_length,
                    -(
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        self.court_params.get(
                            "basket_center_to_baseline",
                            0.0
                        ) -
                        lane_length -
                        self.court_params.get("free_throw_circle_radius", 0.0)
                    )
                )
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # court
            xlim = xlims.get(
                display_range,
                (-half_court_length, half_court_length)
            )

        # If an x limit is provided, try to use it
        else:
            try:
                xlim = (xlim[0] - self.x_trans, xlim[1] - self.x_trans)

            # If the limit provided is not a tuple, use the provided value as
            # best as possible. This will set the provided value as the lower
            # limit of x, and display any x values greater than it
            except TypeError:
                # Apply the necessary shift to align the plot limit with the
                # data
                xlim = xlim - self.x_trans

                # If the provided value for the x limit is beyond the end of
                # the court, display the entire court
                if xlim >= half_court_length:
                    xlim = -half_court_length

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_court_length)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the court. Additional view regions may be
        # added here
        if not ylim:
            if type(self.court_params.get("lane_width", 0.0)) == list:
                lane_width = max(self.court_params.get("lane_width", 0.0))

            else:
                lane_width = self.court_params.get("lane_width", 0.0)

            # Divide the lane width in half as the full lane width should be
            # given in the surface specifications
            lane_width /= 2.0

            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                "full": (-(half_court_width), half_court_width),
                "offense": (-half_court_width, half_court_width),
                "offence": (-half_court_width, half_court_width),
                "offensivehalfcourt": (-half_court_width, half_court_width),
                "offensive_half_court": (-half_court_width, half_court_width),
                "offensive half court": (-half_court_width, half_court_width),
                "defense": (-half_court_width, half_court_width),
                "defence": (-half_court_width, half_court_width),
                "defensivehalfcourt": (-half_court_width, half_court_width),
                "defensive_half_court": (-half_court_width, half_court_width),
                "defensive half court": (-half_court_width, half_court_width),
                "offensivekey": (-half_court_width, half_court_width),
                "offensive_key": (-half_court_width, half_court_width),
                "offensive key": (-half_court_width, half_court_width),
                "attackingkey": (-half_court_width, half_court_width),
                "attacking_key": (-half_court_width, half_court_width),
                "attacking key": (-half_court_width, half_court_width),
                "defensivekey": (-half_court_width, half_court_width),
                "defensive_key": (-half_court_width, half_court_width),
                "defensive key": (-half_court_width, half_court_width),
                "defendingkey": (-half_court_width, half_court_width),
                "defending_key": (-half_court_width, half_court_width),
                "defending key": (-half_court_width, half_court_width),
                "offensivepaint": (-lane_width - 1.5, lane_width + 1.5),
                "offensive_paint": (-lane_width - 1.5, lane_width + 1.5),
                "offensive paint": (-lane_width - 1.5, lane_width + 1.5),
                "attackingpaint": (-lane_width - 1.5, lane_width + 1.5),
                "attacking_paint": (-lane_width - 1.5, lane_width + 1.5),
                "attacking paint": (-lane_width - 1.5, lane_width + 1.5),
                "offensivelane": (-lane_width - 1.5, lane_width + 1.5),
                "offensive_lane": (-lane_width - 1.5, lane_width + 1.5),
                "offensive lane": (-lane_width - 1.5, lane_width + 1.5),
                "attackinglane": (-lane_width - 1.5, lane_width + 1.5),
                "attacking_lane": (-lane_width - 1.5, lane_width + 1.5),
                "attacking lane": (-lane_width - 1.5, lane_width + 1.5),
                "defensivepaint": (-lane_width - 1.5, lane_width + 1.5),
                "defensive_paint": (-lane_width - 1.5, lane_width + 1.5),
                "defensive paint": (-lane_width - 1.5, lane_width + 1.5),
                "defendingpaint": (-lane_width - 1.5, lane_width + 1.5),
                "defending_paint": (-lane_width - 1.5, lane_width + 1.5),
                "defending paint": (-lane_width - 1.5, lane_width + 1.5),
                "defensivelane": (-lane_width - 1.5, lane_width + 1.5),
                "defensive_lane": (-lane_width - 1.5, lane_width + 1.5),
                "defensive lane": (-lane_width - 1.5, lane_width + 1.5),
                "defendinglane": (-lane_width - 1.5, lane_width + 1.5),
                "defending_lane": (-lane_width - 1.5, lane_width + 1.5),
                "defending lane": (-lane_width - 1.5, lane_width + 1.5),

            }

            # Extract the y limit from the dictionary, defaulting to the full
            # court
            ylim = ylims.get(
                display_range,
                (-half_court_width, half_court_width)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= half_court_width:
                    ylim = -half_court_width

                ylim = (ylim, half_court_width)

        # Smaller coordinate should always go first
        if xlim[0] > xlim[1]:
            xlim = (xlim[1], xlim[0])
        if ylim[0] > ylim[1]:
            ylim = (ylim[1], ylim[0])

        # Set backup limits in case the limits are the same. This avoids a
        # UserWarning
        if xlim[0] == xlim[1] == 0:
            xlim = (1, -1)
        if ylim[0] == ylim[1] == 0:
            ylim = (1, -1)

        # Constrain the limits from going beyond the end of the court (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_court_length),
            min(xlim[1], half_court_length)
        )

        ylim = (
            max(ylim[0], -half_court_width),
            min(ylim[1], half_court_width)
        )

        return xlim, ylim


class FIBACourt(BasketballCourt):
    """A subclass of ``BasketballCourt`` specific to FIBA.

    See ``BasketballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the BasketballCourt class with the relevant parameters
        super().__init__(
            league_code = "fiba",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class NBACourt(BasketballCourt):
    """A subclass of ``BasketballCourt`` specific to the NBA.

    See ``BasketballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the BasketballCourt class with the relevant parameters
        super().__init__(
            league_code = "nba",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class NBAGLeagueCourt(BasketballCourt):
    """A subclass of ``BasketballCourt`` specific to the NBA G League.

    See ``BasketballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the BasketballCourt class with the relevant parameters
        super().__init__(
            league_code = "nba g league",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class NCAACourt(BasketballCourt):
    """A subclass of ``BasketballCourt`` specific to the NBA.

    See ``BasketballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the BasketballCourt class with the relevant parameters
        super().__init__(
            league_code = "ncaa",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class NFHSCourt(BasketballCourt):
    """A subclass of ``BasketballCourt`` specific to the NFHS.

    See ``BasketballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the BasketballCourt class with the relevant parameters
        super().__init__(
            league_code = "nfhs",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class WNBACourt(BasketballCourt):
    """A subclass of ``BasketballCourt`` specific to the NBA.

    See ``BasketballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the BasketballCourt class with the relevant parameters
        super().__init__(
            league_code = "wnba",
            court_updates = court_updates,
            *args,
            **kwargs
        )
