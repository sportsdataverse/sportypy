"""Extension of the ``BaseSurfacePlot`` class to create a football field.

This is a second-level child class of the ``BaseSurface`` class, and as such
will have access to its attributes and methods. ``sportypy`` will ship with
pre-defined leagues that will have their own subclass, but a user can manually
specify their own field parameters to create a totally-customized field. The
field's features are parameterized by the basic dimensions of the field, which
comprise the attributes of the class.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.transforms as mtrans
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.football as football_features
from sportypy._base_functions._plot_helpers import autoset_font_size
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class FootballField(BaseSurfacePlot):
    """A subclass of ``BaseSurfacePlot`` to make a generic football field.

    This allows for the creation of the football field in a way that is
    entirely parameterized by the field's baseline characteristics.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid football field. The attributes needed to instantiate a
    particular league's surface must be specified in the ``field_params``
    dictionary. For many leagues, these will be provided in the
    surface_dimensions.json file in the data/ subdirectory of ``sportypy``.

    NOTE: By convention of football data, the origin of the coordinate system
    will be located in the lower-left corner of the field when viewing the
    field in TV view. All features will be anchored according to this
    convention, although this may be adjusted via the ``x_trans`` and
    ``y_trans`` attributes.

    See the ``BaseSurfacePlot`` and ``BaseSurface`` class definitions for full
    details.

    Attributes
    ----------
    league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "National Football
        League" should be either "NFL" or "nfl"). The default is an empty
        string

    rotation : float
        The angle (in degrees) through which to rotate the final plot. The
        default is ``0.0``

    x_trans : float
        The amount that the ``x`` coordinates are to be shifted. By convention,
        the +``x`` axis extends from the center of the surface towards the
        right-hand endzone when viewing the field in TV view. The default is
        ``0.0``

    y_trans : float
        The amount that the ``y`` coordinates are to be shifted. By convention,
        the +``y`` axis extends from the center of the surface towards the
        top of the field when viewing the field in TV view. The default is
        ``0.0``

    field_updates : dict
        A dictionary of updated parameters to use for the football field. The
        default is an empty dictionary

    color_updates : dict
        A dictionary of coloring parameters to pass to the plot. Defaults are
        provided in the class per each rule book, but this allows the plot to
        be more heavily customized/styled. The default is an empty dictionary

    units : str
        The units that the final plot should utilize. The default units are the
        units specified in the rule book of the league. The default is
        ``"default"``

    field_params : dict
        A dictionary containing the following parameters of the field:

            - field_length : float
                The length of the field in TV view

            - field_width : float
                The width of the field in TV view

            - endzone_length : float
                The length of the endzone in TV view. This is measured from the
                field side of the goal line

            - minor_line_thickness : float
                The thickness of the minor lines on the field. These are
                usually the hash yard lines and try markings

            - goal_line_thickness : float
                The thickness of the goal line

            - boundary_line_thickness : float
                The thickness of the boundary lines. This should not include
                any border around the sidelines, the restricted areas, or team
                bench areas

            - minor_yard_line_height : float
                The height of the minor yard lines on the field in the ``y``
                direction when viewing the field in TV view

            - field_border_thickness : float
                The thickness of the border around the field. This will be
                uniform around the entirety of the field. This should not
                include the thickness of the boundary lines

            - field_border_behind_bench : bool
                Whether or not to draw the border of the field behind the team
                bench areas

            - major_yard_line_distance : float
                The separation between the midpoints of major yard lines. For
                example, an NFL field's major yard lines are separated by 5
                yards. Major yard lines are considered to be the yard lines
                that span the entire width of the field

            - sideline_to_major_yard_line : float
                The distance separating the major yard line from the interior
                edge of the boundary lines

            - inbound_cross_hashmark_length : float
                The length, in TV view, of the hash mark that crosses major
                yard lines

            - inbound_hashmark_separation : float
                The separation between the hash marks (i.e. the minor yard
                lines) when measured from their interior edges

            - inbound_cross_hashmark_separation : float
                The separation between the hash marks lying on the major yard
                lines when measured from their interior edges

            - sideline_to_outer_yard_line : float
                The distance between the interior edge of the sideline to the
                exterior edge of a minor yard line

            - sideline_to_bottom_of_numbers : float
                The distance between the sideline and the bottom edge of the
                bounding box of the yardage-marking numbers

            - number_height : float
                The height, in TV view, of the yardage-marking numbers

            - try_mark_distance : float
                The distance between the goal line and the try mark

            - try_mark_width : float
                The width of the try mark

            - arrow_line_dist : float
                The major yard line distances which should be marked with a
                directional arrow. These are measured from the goal line (e.g.
                a value of ``10.0`` will place a directional arrow every 10
                major yard lines from the goal line towards the middle of the
                field)

            - yard_line_to_arrow : float
                The distance between the inside edge of a directional arrow and
                the major yard line to which it refers

            - top_number_to_arrow : float
                The distance from the top of the bounding box of a
                yardage-marking number to the top of the directional arrow

            - arrow_base : float
                The length of the base of the directional arrow. This is the
                component of the arrow that is parallel to the major yard line
                to which the arrow corresponds

            - arrow_length : float
                The distance between the tip of the directional arrow and the
                base

            - number_to_yard_line : float
                The separation between the bounding box of the yardage-marking
                numeral and the nearest yard line

            - number_width : float
                The width of the bounding box of the yardage-marking numeral

            - numbers_bottom : list of strings
                The text of the markings that run along the bottom of the field
                in TV view

            - numbers_top : list of strings
                The text of the markings that run along the top of the field in
                TV view

            - number_font : string
                The font with which the numerals on the field should be written
                in. All fonts should be stored in the fonts/ subdirectory

            - restricted_area_width : float
                The width of the restricted area

            - coaching_box_width : float
                The width of the coaching box

            - team_bench_width : float
                The width of the team bench area

            - team_bench_length_field_side : float
                The length of the team bench's edge closest to the field

            - team_bench_length_back_side : float
                The length of the team bench's edge furthest from the field

            - team_bench_area_border_thickness : float
                The thickness of the border around the team bench area. This
                should not include any borders around the field

            - bench_shape : string
                The shape of the bench area. This should either be "trapezoid"
                or "rectangular"

            - additional_minor_yard_lines : list of floats
                Any additional yard lines that should be marked on the field,
                with ``0.0`` corresponding to the left-hand goal line in TV
                view

            - field_bordered : bool
                Whether or not the field should have a border

            - extra_apron_padding : float
                Any additional padding around the field apron
    """

    def __init__(self, league_code = "", field_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a ``FootballField`` class.

        Parameters
        ----------
        league_code : str
            The league for which the plot should be drawn. This is
            case-insensitive but should be the shortened name of the league
            (e.g. "National Football League" should be either "NFL" or "nfl").
            The default is an empty string

        rotation : float
            The angle (in degrees) through which to rotate the final plot. The
            default is ``0.0``

        x_trans : float
            The amount that the ``x`` coordinates are to be shifted. By
            convention, the +``x`` axis extends from the center of the surface
            towards the right-hand endzone when viewing the field in TV view.
            The default is ``0.0``

        y_trans : float
            The amount that the ``y`` coordinates are to be shifted. By
            convention, the +``y`` axis extends from the center of the surface
            towards the top of the field when viewing the field in TV view. The
            default is ``0.0``

        field_updates : dict
            A dictionary of updated parameters to use to create the football
            field. The default is an empty dictionary

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
        # Load all pre-defined field dimensions for provided leagues
        self._load_preset_dimensions(sport = "football")

        # Load all unit conversions
        self._load_unit_conversions()

        # Set the league to be the lower-case version of the supplied value
        self.league_code = league_code.lower()

        # Try to get the league specified from the pre-defined set of leagues
        try:
            field_dimensions = self.league_dimensions[self.league_code]

        # If it can't be found, set the field_dimensions dictionary to be empty
        except KeyError:
            field_dimensions = {}

        # Combine the field dimensions (if found from in the pre-defined
        # leagues) with any parameter updates supplied by the user. This will
        # comprise the parameter set with which the field is to be drawn
        field_params = {
            **field_dimensions,
            **field_updates
        }

        # Set the passed parameters of the field to be the class' field_params
        # attribute
        self.field_params = field_params

        # Set the rotation of the plot to be the supplied rotation value
        self.rotation_amt = rotation
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the field's necessary shifts. This will overwrite the default
        # values of x_trans and y_trans inherited from the BaseSurfacePlot
        # class (which is in turn inherited from BaseSurface)
        self.x_trans, self.y_trans = x_trans, y_trans

        # Create a container for the relevant features of a field
        self._features = []

        # Initialize the x and y limits for the plot be None. These will get
        # set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the default colors of the field
        default_colors = {
            "plot_background": "#196f0c00",
            "field_apron": "#196f0c",
            "offensive_half": "#196f0c",
            "defensive_half": "#196f0c",
            "offensive_endzone": "#196f0c",
            "defensive_endzone": "#196f0c",
            "end_line": "#ffffff",
            "sideline": "#ffffff",
            "field_border": "#196f0c",
            "field_border_outline": "#ffffff",
            "major_yard_line": "#ffffff",
            "goal_line": "#ffffff",
            "minor_yard_line": "#ffffff",
            "arrow": "#ffffff",
            "arrow_outline": "#ffffff00",
            "try_mark": "#ffffff",
            "yardage_marker": "#ffffff",
            "yardage_marker_outline": "#ffffff00",
            "restricted_area": "#ffffff",
            "coaching_box": "#ffffff",
            "team_bench_area": "#196f0c",
            "team_bench_area_outline": "#ffffff",
            "coaching_box_line": "#ffffff"
        }

        # Combine the colors with a passed colors dictionary
        if not color_updates:
            color_updates = {}

        # Create the final color set for the features of the field
        self.feature_colors = {
            **default_colors,
            **color_updates
        }

        # Initialize the constraint on the field to confine all features to be
        # contained within the field. The feature itself is not visible (as
        # it's created by the football.field class)
        field_constraint_params = {
            "class": football_features.FieldConstraint,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "visible": False
        }
        self._initialize_feature(field_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the offensive half of the field
        offensive_half_params = {
            "class": football_features.OffensiveHalf,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "feature_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["offensive_half"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(offensive_half_params)

        # Initialize the defensive half of the field
        defensive_half_params = {
            "class": football_features.DefensiveHalf,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "feature_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["defensive_half"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(defensive_half_params)

        # Initialize the field apron
        field_apron_params = {
            "class": football_features.FieldApron,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "boundary_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "field_border_thickness": self.field_params.get(
                "field_border_thickness",
                0.0
            ),
            "restricted_area_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "restricted_area_width": self.field_params.get(
                "restricted_area_width",
                0.0
            ),
            "coaching_box_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "coaching_box_width": self.field_params.get(
                "coaching_box_width",
                0.0
            ),
            "team_bench_length_field_side": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "team_bench_length_back_side": self.field_params.get(
                "team_bench_length_back_side",
                0.0
            ),
            "team_bench_width": self.field_params.get(
                "team_bench_width",
                0.0
            ),
            "team_bench_area_border_thickness": self.field_params.get(
                "team_bench_area_border_thickness",
                0.0
            ),
            "extra_apron_padding": self.field_params.get(
                "extra_apron_padding",
                0.0
            ),
            "is_constrained": False,
            "visible": True,
            "facecolor": self.feature_colors["field_apron"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(field_apron_params)

        # Initialize the endzones
        offensive_endzone_params = {
            "class": football_features.Endzone,
            "x_anchor": (
                (self.field_params.get("field_length", 0.0) / 2.0) +
                (self.field_params.get("endzone_length", 0.0)) / 2.0
            ),
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "feature_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["offensive_endzone"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(offensive_endzone_params)

        defensive_endzone_params = {
            "class": football_features.Endzone,
            "x_anchor": -(
                (self.field_params.get("field_length", 0.0) / 2.0) +
                (self.field_params.get("endzone_length", 0.0)) / 2.0
            ),
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "feature_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["defensive_endzone"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(defensive_endzone_params)

        # Initialize the restricted areas
        restricted_area_params = {
            "class": football_features.RestrictedArea,
            "x_anchor": 0.0,
            "y_anchor": (
                (self.field_params.get("field_width", 0.0) / 2.0) +
                self.field_params.get("boundary_line_thickness", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "feature_thickness": self.field_params.get(
                "restricted_area_width",
                0.0
            ),
            "restricted_area_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["restricted_area"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(restricted_area_params)

        # Initialize the coaching boxes
        coaching_box_params = {
            "class": football_features.CoachingBox,
            "x_anchor": 0.0,
            "y_anchor": (
                (self.field_params.get("field_width", 0.0) / 2.0) +
                self.field_params.get("boundary_line_thickness", 0.0) +
                self.field_params.get("restricted_area_width", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "feature_thickness": self.field_params.get(
                "coaching_box_width",
                0.0
            ),
            "coaching_box_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["coaching_box"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(coaching_box_params)

        # Initialize the team bench areas
        team_bench_area_params = {
            "class": football_features.TeamBenchArea,
            "x_anchor": 0.0,
            "y_anchor": (
                (self.field_params.get("field_width", 0.0) / 2.0) +
                self.field_params.get("boundary_line_thickness", 0.0) +
                self.field_params.get("restricted_area_width", 0.0) +
                self.field_params.get("coaching_box_width", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "feature_thickness": self.field_params.get(
                "team_bench_width",
                0.0
            ),
            "team_bench_length_field_side": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "team_bench_length_back_side": self.field_params.get(
                "team_bench_length_back_side",
                0.0
            ),
            "team_bench_width": self.field_params.get("team_bench_width", 0.0),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["team_bench_area"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(team_bench_area_params)

        # Initialize the outline of the team bench areas
        team_bench_area_outline_params = {
            "class": football_features.TeamBenchAreaOutline,
            "x_anchor": 0.0,
            "y_anchor": (
                (self.field_params.get("field_width", 0.0) / 2.0) +
                self.field_params.get("boundary_line_thickness", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "restricted_area_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "restricted_area_width": self.field_params.get(
                "restricted_area_width",
                0.0
            ),
            "coaching_box_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "coaching_box_width": self.field_params.get(
                "coaching_box_width",
                0.0
            ),
            "team_bench_length_field_side": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "team_bench_length_back_side": self.field_params.get(
                "team_bench_length_back_side",
                0.0
            ),
            "team_bench_width": self.field_params.get(
                "team_bench_width",
                0.0
            ),
            "feature_thickness": self.field_params.get(
                "team_bench_area_border_thickness",
                0.0
            ),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["team_bench_area_outline"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(team_bench_area_outline_params)

        # Restricted area line
        coaching_box_line_params = {
            "class": football_features.CoachingBoxLine,
            "x_anchor": 0.0,
            "y_anchor": (
                (self.field_params.get("field_width", 0.0) / 2.0) +
                self.field_params.get("boundary_line_thickness", 0.0) +
                self.field_params.get("restricted_area_width", 0.0) +
                self.field_params.get("coaching_box_width", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "feature_thickness": self.field_params.get(
                "minor_line_thickness",
                0.0
            ),
            "coaching_box_line_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["coaching_box_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(coaching_box_line_params)

        # Initialize the end lines
        end_line_params = {
            "class": football_features.EndLine,
            "x_anchor": (
                (self.field_params.get("field_length", 0.0) / 2.0) +
                self.field_params.get("endzone_length", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "feature_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["end_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(end_line_params)

        # Initialize the sidelines
        sideline_params = {
            "class": football_features.Sideline,
            "x_anchor": 0.0,
            "y_anchor": self.field_params.get("field_width", 0.0) / 2.0,
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "feature_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["sideline"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(sideline_params)

        # Initialize the field border
        field_border_params = {
            "class": football_features.FieldBorder,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "visible": self.field_params.get("field_bordered", False),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "restricted_area_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "restricted_area_width": self.field_params.get(
                "restricted_area_width",
                0.0
            ),
            "coaching_box_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "coaching_box_width": self.field_params.get(
                "coaching_box_width",
                0.0
            ),
            "team_bench_length_field_side": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "team_bench_length_back_side": self.field_params.get(
                "team_bench_length_back_side",
                0.0
            ),
            "team_bench_width": self.field_params.get(
                "team_bench_width",
                0.0
            ),
            "team_bench_border_thickness": self.field_params.get(
                "team_bench_area_border_thickness",
                0.0
            ),
            "surrounds_team_bench_area": self.field_params.get(
                "field_border_behind_bench",
                False,
            ),
            "bench_shape": self.field_params.get(
                "bench_shape",
                "rectangle"
            ),
            "feature_thickness": self.field_params.get(
                "field_border_thickness",
                0.0
            ),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "boundary_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["field_border"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(field_border_params)

        # Initialize the outline of the field border
        field_border_outline_params = {
            "class": football_features.FieldBorderOutline,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "visible": self.field_params.get("field_bordered", False),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "restricted_area_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "restricted_area_width": self.field_params.get(
                "restricted_area_width",
                0.0
            ),
            "coaching_box_length": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "coaching_box_width": self.field_params.get(
                "coaching_box_width",
                0.0
            ),
            "team_bench_length_field_side": self.field_params.get(
                "team_bench_length_field_side",
                0.0
            ),
            "team_bench_length_back_side": self.field_params.get(
                "team_bench_length_back_side",
                0.0
            ),
            "team_bench_width": self.field_params.get(
                "team_bench_width",
                0.0
            ),
            "team_bench_border_thickness": self.field_params.get(
                "team_bench_area_border_thickness",
                0.0
            ),
            "field_border_thickness": self.field_params.get(
                "field_border_thickness",
                0.0
            ),
            "feature_thickness": self.field_params.get(
                "minor_line_thickness",
                0.0
            ),
            "surrounds_team_bench_area": self.field_params.get(
                "field_border_behind_bench",
                False,
            ),
            "bench_shape": self.field_params.get(
                "bench_shape",
                "rectangle"
            ),
            "endzone_length": self.field_params.get("endzone_length", 0.0),
            "boundary_thickness": self.field_params.get(
                "boundary_line_thickness",
                0.0
            ),
            "facecolor": self.feature_colors["field_border_outline"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(field_border_outline_params)

        # Generate a sequence of numbers that represent each of the yard lines.
        # NOTE: These are the yard lines that are inside of the field of play
        # and do not include the goal lines. The additional 1.0 is added to the
        # half-length of the field to include the 50 yard line
        yard_lines = np.arange(
            1.0,
            (self.field_params.get("field_length", 0.0) / 2.0) + 1.0
        )

        # Identify all major yard lines. These are the yard lines that span the
        # width of the field
        major_yard_lines = yard_lines[
            yard_lines % self.field_params.get(
                "major_yard_line_distance",
                5.0
            ) == 0.0
        ]

        for major_line in major_yard_lines:
            # The yard line name is an added attribute to identify which yard
            # line is which if needed
            yard_line_name = int(
                (self.field_params.get("field_length", 0.0) / 2.0) -
                major_line
            )

            # Initialize the major yard line
            major_yard_line_params = {
                "class": football_features.MajorYardLine,
                "x_anchor": yard_line_name,
                "y_anchor": 0.0,
                "reflect_x": True,
                "reflect_y": False,
                "dist_to_sideline": self.field_params.get(
                    "sideline_to_major_yard_line",
                    0.0
                ),
                "cross_hash_length": self.field_params.get(
                    "inbound_cross_hashmark_length",
                    0.0
                ),
                "cross_hash_separation": self.field_params.get(
                    "inbound_cross_hashmark_separation",
                    0.0
                ),
                "feature_thickness": self.field_params.get(
                    "minor_line_thickness",
                    0.0
                ),
                "yard_line_name": f"{yard_line_name}",
                "field_length": self.field_params.get("field_length", 0.0),
                "field_width": self.field_params.get("field_width", 0.0),
                "facecolor": self.feature_colors["major_yard_line"],
                "edgecolor": None,
                "zorder": 16
            }
            self._initialize_feature(major_yard_line_params)

        # Initialize the goal lines
        goal_line_params = {
            "class": football_features.GoalLine,
            "x_anchor": self.field_params.get("field_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "feature_thickness": self.field_params.get(
                "goal_line_thickness",
                0.0
            ),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["goal_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(goal_line_params)

        # Identify all minor yard lines. These are the yard lines that need to
        # be marked between all major yard lines
        minor_yard_lines = yard_lines[
            yard_lines % self.field_params.get(
                "major_yard_line_distance",
                5.0
            ) != 0.0
        ]

        # Add additional yard lines to be marked (e.g. CFL's 5-yard intervals
        # in the endzones)
        minor_yard_lines = np.append(minor_yard_lines, self.field_params.get(
            "additional_minor_yard_lines",
            []
        ))

        for minor_line in minor_yard_lines:
            # The yard line name is an added attribute to identify which yard
            # line is which if needed
            yard_line_name = int(
                (self.field_params.get("field_length", 0.0) / 2.0) -
                minor_line
            )

            # Initialize the minor yard lines closest to the sideline
            outer_minor_yard_line_params = {
                "class": football_features.MinorYardLine,
                "x_anchor": yard_line_name,
                "y_anchor": (
                    (self.field_params.get("field_width", 0.0) / 2.0) -
                    self.field_params.get("sideline_to_outer_yard_line", 0.0) -
                    self.field_params.get("minor_yard_line_height", 0.0)
                ),
                "reflect_x": True,
                "reflect_y": True,
                "feature_thickness": self.field_params.get(
                    "minor_line_thickness",
                    0.0
                ),
                "yard_line_name": f"{yard_line_name}",
                "yard_line_height": self.field_params.get(
                    "minor_yard_line_height",
                    0.0
                ),
                "field_length": self.field_params.get("field_length", 0.0),
                "field_width": self.field_params.get("field_width", 0.0),
                "facecolor": self.feature_colors["minor_yard_line"],
                "edgecolor": None,
                "zorder": 16
            }
            self._initialize_feature(outer_minor_yard_line_params)

            # Initialize the minor yard lines closest to the center of the
            # field
            inner_minor_yard_line_params = {
                "class": football_features.MinorYardLine,
                "x_anchor": yard_line_name,
                "y_anchor": self.field_params.get(
                    "inbound_hashmark_separation",
                    0.0
                ) / 2.0,
                "reflect_x": True,
                "reflect_y": True,
                "feature_thickness": self.field_params.get(
                    "minor_line_thickness",
                    0.0
                ),
                "yard_line_name": f"{yard_line_name}",
                "yard_line_height": self.field_params.get(
                    "minor_yard_line_height",
                    0.0
                ),
                "field_length": self.field_params.get("field_length", 0.0),
                "field_width": self.field_params.get("field_width", 0.0),
                "facecolor": self.feature_colors["minor_yard_line"],
                "edgecolor": None,
                "zorder": 16
            }
            self._initialize_feature(inner_minor_yard_line_params)

        # Identify all yard lines around which there should be arrows
        arrow_lines = yard_lines[
            yard_lines % self.field_params.get(
                "arrow_line_dist",
                10.0
            ) == 0.0
        ] - (self.field_params.get("field_length", 0.0) / 2.0)

        # Remove arrows from the goal line
        arrow_lines = arrow_lines[arrow_lines != 0.0]

        for arrow_line in arrow_lines:
            # Initialize the directional arrows where necessary
            arrow_params = {
                "class": football_features.Arrow,
                "x_anchor": arrow_line - self.field_params.get(
                    "yard_line_to_arrow"
                ),
                "y_anchor": (
                    (self.field_params.get("field_width", 0.0) / 2.0) -
                    self.field_params.get(
                        "sideline_to_bottom_of_numbers",
                        0.0
                    ) -
                    self.field_params.get("number_height", 0.0) +
                    self.field_params.get("top_number_to_arrow", 0.0)
                ),
                "reflect_x": True,
                "reflect_y": True,
                "arrow_base": self.field_params.get("arrow_base", 0.0),
                "arrow_length": -self.field_params.get("arrow_length", 0.0),
                "field_length": self.field_params.get("field_length", 0.0),
                "field_width": self.field_params.get("field_width", 0.0),
                "facecolor": self.feature_colors["arrow"],
                "edgecolor": self.feature_colors["arrow_outline"],
                "zorder": 16
            }
            self._initialize_feature(arrow_params)

        # Initialize the try marking
        try_mark_params = {
            "class": football_features.TryMark,
            "x_anchor": (
                self.field_params.get("field_length", 0.0) / 2.0 -
                self.field_params.get("try_mark_distance", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "try_mark_width": self.field_params.get("try_mark_width", 0.0),
            "feature_thickness": self.field_params.get(
                "minor_line_thickness",
                0.0
            ),
            "field_length": self.field_params.get("field_length", 0.0),
            "field_width": self.field_params.get("field_width", 0.0),
            "facecolor": self.feature_colors["try_mark"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(try_mark_params)

        # Certain lines on the field may be marked with numbers and directional
        # arrows
        marked_lines = np.arange(
            1.0,
            self.field_params.get("field_length", 0.0)
        )

        marked_lines = marked_lines[
            marked_lines % self.field_params.get(
                "arrow_line_dist",
                10.0
            ) == 0.0
        ] - (self.field_params.get("field_length", 0.0) / 2.0)

        marked_lines = np.repeat(marked_lines, 2)

        # Handle cases like CFL where a "C" is required at the midfield line
        if 0.0 not in marked_lines and len(marked_lines) > 0.0:
            marked_lines = np.append(marked_lines, 0.0)
            marked_lines = np.sort(marked_lines)

        if len(self.field_params.get("numbers_bottom", [])) % 2 != 0:
            dist_to_line_bottom = np.repeat(
                self.field_params.get("number_to_yard_line", 0.0),
                (len(self.field_params.get("numbers_bottom", [])) / 2.0) - 0.5
            )

            dist_to_line_bottom = np.append(dist_to_line_bottom, 0.0)

            dist_to_line_bottom = np.append(dist_to_line_bottom, np.repeat(
                self.field_params.get("number_to_yard_line", 0.0),
                (len(self.field_params.get("numbers_bottom", [])) / 2.0) - 0.5
            ))
        else:
            dist_to_line_bottom = np.repeat(
                self.field_params.get("number_to_yard_line", 0.0),
                len(self.field_params.get("numbers_bottom", []))
            )

        if len(self.field_params.get("numbers_top", [])) % 2 != 0:
            dist_to_line_top = np.repeat(
                self.field_params.get("number_to_yard_line", 0.0),
                (len(self.field_params.get("numbers_top", [])) / 2.0) - 0.5
            )

            dist_to_line_top = np.append(dist_to_line_top, 0.0)

            dist_to_line_top = np.append(dist_to_line_top, np.repeat(
                self.field_params.get("number_to_yard_line", 0.0),
                (len(self.field_params.get("numbers_top", [])) / 2.0) - 0.5
            ))
        else:
            dist_to_line_top = np.repeat(
                self.field_params.get("number_to_yard_line", 0.0),
                len(self.field_params.get("numbers_top", []))
            )

        # Initialize the yardage markers
        self.yardage_markers = pd.concat([
            pd.DataFrame({
                "marking": self.field_params.get("numbers_bottom", []),
                "rotation": np.repeat(
                    0.0, len(self.field_params.get("numbers_bottom", []))
                ),
                "side": np.repeat(
                    "bottom", len(self.field_params.get("numbers_bottom", []))
                ),
                "marked_line": marked_lines,
                "dist_to_line": dist_to_line_bottom,
                "color": self.feature_colors["yardage_marker"],
                "outline_color": self.feature_colors[
                    "yardage_marker_outline"
                ]
            }),

            pd.DataFrame({
                "marking": self.field_params.get("numbers_top", []),
                "rotation": np.repeat(
                    180.0, len(self.field_params.get("numbers_top", []))
                ),
                "side": np.repeat(
                    "top", len(self.field_params.get("numbers_top", []))
                ),
                "marked_line": marked_lines,
                "dist_to_line": dist_to_line_top,
                "color": self.feature_colors["yardage_marker"],
                "outline_color": self.feature_colors[
                    "yardage_marker_outline"
                ]
            })
        ])

        self.yardage_markers.reset_index(inplace = True, drop = True)

        # Initialize all other features passed as keyword arguments
        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = "full", xlim = None, ylim = None,
             rotation = None):
        """Draw the field.

        Parameters
        ----------
        ax : matplotlib.Axes
            An axes object onto which the plot can be drawn. If ``None`` is
            supplied, then the currently-active Axes object will be used

        display_range : str
            The portion of the surface to display. The entire surface
            will always be drawn under the hood, however this parameter
            limits what is shown in the final plot. The following explain what
            each display range corresponds to:

                - ``"full"``: The entire surface
                - ``"offense"``: The offensive half of the field
                - ``"offence"``: The offensive half of the field
                - ``"offensivehalf"``: The offensive half of the field
                - ``"offensive_half"``: The offensive half of the field
                - ``"offensive half"``: The offensive half of the field
                - ``"offensivehalffield"``: The offensive half of the field
                - ``"offensive_half_field"``: The offensive half of the field
                - ``"offensive half field"``: The offensive half of the field
                - ``"defense"``: The defensive half of the field
                - ``"defence"``: The defensive half of the field
                - ``"defensivehalf"``: The defensive half of the field
                - ``"defensive_half"``: The defensive half of the field
                - ``"defensive half"``: The defensive half of the field
                - ``"defensivehalffield"``: The defensive half of the field
                - ``"defensive_half_field"``: The defensive half of the field
                - ``"defensive half field"``: The defensive half of the field
                - ``"redzone"``: The offensive red zone
                - ``"red_zone"``: The offensive red zone
                - ``"red zone"``: The offensive red zone
                - ``"oredzone"``: The offensive red zone
                - ``"offensive_red_zone"``: The offensive red zone
                - ``"offensive red zone"``: The offensive red zone
                - ``"dredzone"``: The defensive red zone
                - ``"defensive_red_zone"``: The defensive red zone
                - ``"defensive red zone"``: The defensive red zone

            The default is ``"full"``

        xlim : float or tuple of floats or None
            The display range in the ``x`` direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the ``x`` coordinates to display and the upper bound will be the
            +``x`` end of the field. If a tuple, the two values will be
            used to determine the bounds. If ``None``, then the
            ``display_range`` will be used instead to set the bounds. The
            default is ``None``

        ylim : float or tuple of floats or None
            The display range in the ``y`` direction to be used. If a single
            float is provided, this will be used as the lower bound of the y
            coordinates to display and the upper bound will be the +``y`` side
            of the field. If a tuple, the two values will be used to determine
            the bounds. If ``None``, then the ``display_range`` will be used
            instead to set the bounds.  The default is ``None``

        rotation : float or None
            Angle (in degrees) through which to rotate the field when drawing.
            If used, this will set the class attribute of ``_rotation``. A
            alue of ``0.0`` will correspond to a TV view of the field, where
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

                # Assuming the feature is visible (and is not the field
                # constraint), get the feature's x and y limits to ensure it
                # lies within the bounds of the field
                if visible and not isinstance(
                    feature,
                    football_features.FieldConstraint
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

        # Add the yardage markers
        line_side = "left"

        for idx, row in self.yardage_markers.iterrows():
            if row["dist_to_line"] == 0.0:
                line_side = "center"

            if line_side == "left":
                x_anchor = (
                    row["marked_line"] -
                    self.field_params.get("number_to_yard_line", 0.0) -
                    (self.field_params.get("number_width", 0.0) / 2.0) -
                    (self.field_params.get("minor_line_thickness", 0.0) / 2.0)
                )
            elif line_side == "center":
                x_anchor = 0.0
            else:
                x_anchor = (
                    row["marked_line"] +
                    self.field_params.get("number_to_yard_line", 0.0) +
                    (self.field_params.get("number_width", 0.0) / 2.0) +
                    (self.field_params.get("minor_line_thickness", 0.0) / 2.0)
                )

            if row["side"] == "bottom":
                y_anchor = (
                    -(self.field_params.get("field_width", 0.0) / 2.0) +
                    (self.field_params.get("number_height", 0.0) / 2.0) +
                    self.field_params.get("sideline_to_bottom_of_numbers", 0.0)
                )
            else:
                y_anchor = (
                    (self.field_params.get("field_width", 0.0) / 2.0) -
                    (self.field_params.get("number_height", 0.0) / 2.0) -
                    self.field_params.get("sideline_to_bottom_of_numbers", 0.0)
                )

            s = row["marking"]
            color = row["color"]
            outline_color = row["outline_color"]
            rotation = row["rotation"]

            number_font = self.field_params.get("number_font", "DejaVu Sans")

            # Ideally this should be removed, but for now this adjusts the "1"
            # on the top numbers to be in the correct spot
            if row["side"] == "top" and line_side == "right" and s == "1":
                if number_font == "Clarendon-Regular":
                    x_anchor -= 0.75
                else:
                    x_anchor = x_anchor

            if self.rotation_amt != 0.0:
                x_anchor_r = (
                    (x_anchor * math.cos(self.rotation_amt * np.pi / 180.0)) -
                    (y_anchor * math.sin(self.rotation_amt * np.pi / 180.0))
                )

                y_anchor_r = (
                    (x_anchor * math.sin(self.rotation_amt * np.pi / 180.0)) +
                    (y_anchor * math.cos(self.rotation_amt * np.pi / 180.0))
                )

                x_anchor = x_anchor_r
                y_anchor = y_anchor_r
                rotation += self.rotation_amt

            if idx == 0:
                font_size = autoset_font_size(
                    ax,
                    s,
                    (x_anchor, y_anchor),
                    self.field_params.get("number_width", 0.0),
                    self.field_params.get("number_height", 0.0),
                    rotation = rotation,
                    fontweight = "heavy",
                    fontname = number_font,
                    rotation_mode = "anchor"
                )

            ax.text(
                x = x_anchor,
                y = y_anchor,
                s = s,
                color = color,
                path_effects = [
                    pe.withStroke(
                        linewidth = 2,
                        foreground = outline_color
                    )
                ],
                ha = "center",
                va = "center",
                rotation = rotation,
                fontweight = 'heavy',
                fontname = number_font,
                rotation_mode = 'anchor',
                transform_rotates_text = True,
                fontsize = font_size,
                clip_on = True,
                zorder = 17
            )

            if line_side == "left":
                line_side = "right"
            else:
                line_side = "left"

        # Set the plot's display range
        ax = self.set_plot_display_range(
            ax,
            display_range,
            xlim,
            ylim,
            for_plot = False,
            for_display = True
        )

        # Clip yardage markings to not display if outside of plot range
        trans = mtrans.blended_transform_factory(ax.transAxes, ax.transAxes)
        clippath = plt.Rectangle(
            (0.0, 0.0),
            1,
            1,
            transform = trans,
            clip_on = False
        )

        for txt in ax.texts:
            txt.set_clip_path(clippath)

        return ax

    def cani_plot_leagues(self, league_code = None):
        """Show if a league can be plotted, or what leagues are pre-defined.

        A user may wish to know if a specific curling league can be plotted.
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
            print("The following football leagues are available with "
                  "sportypy:\n")

            # Print the current leagues
            for league_code in available_league_codes:
                print(f"- {league_code.upper()}")

    def cani_color_features(self):
        """Determine what features of the field can be colored.

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
        """Determine what features of the field can be re-parameterized.

        This function is a helper function for the user to aid in customizing
        a field's parameters. The printed result of this method will be the
        names of the features that are able to be reparameterized. This method
        is also useful when defining new features and using an existing
        league's field dimensions as a starting point

        Returns
        -------
        Nothing, but a message will be printed out
        """
        # Preamble
        print("The following features can be reparameterized via the "
              "field_updates parameter, with the current value in "
              "parenthesis:\n")

        # Print the current values of the colors
        for k, v in self.field_params.items():
            print(f"- {k} ({v})")

        # Footer
        print("\nThese parameters may be updated with the "
              "update_field_params() method")

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
            field_updates = self.field_params,
            color_updates = updated_colors
        )

    def update_field_params(self, field_param_updates = {}, *args, **kwargs):
        """Update the field's defining parameters.

        This method should primarily be used in cases when plotting a league
        not currently supported by ``sportypy``

        Parameters
        ----------
        field_updates : dict
            A dictionary where the keys correspond to the name of the parameter
            of the field that is to be updated (see
            ``cani_change_dimensions()`` method for a list of these
            parameters). The default is an empty dictionary

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated parameters
        """
        # Start by getting the currently-used field parameters
        current_field_params = self.field_params

        # Create a new dictionary to hold the updated parameters via dictionary
        # comprehension
        updated_field_params = {
            **current_field_params,
            **field_param_updates
        }

        # Re-instantiate the class with the new parameters
        self.__init__(
            field_updates = updated_field_params,
            color_updates = self.feature_colors
        )

    def reset_colors(self):
        """Reset the features of the field to their default color set.

        The colors can be passed at the initial instantiation of the class via
        the ``color_updates`` parameter, and through the ``update_colors()``
        method, these can be changed. This method allows the colors to be reset
        to their default values after experiencing such a change
        """
        # Re-instantiate the class with the default colors
        default_colors = {
            "plot_background": "#196f0c00",
            "field_apron": "#196f0c",
            "offensive_half": "#196f0c",
            "defensive_half": "#196f0c",
            "offensive_endzone": "#196f0c",
            "defensive_endzone": "#196f0c",
            "end_line": "#ffffff",
            "sideline": "#ffffff",
            "field_border": "#196f0c",
            "field_border_outline": "#ffffff",
            "major_yard_line": "#ffffff",
            "goal_line": "#ffffff",
            "minor_yard_line": "#ffffff",
            "arrow": "#ffffff",
            "arrow_outline": "#ffffff00",
            "try_mark": "#ffffff",
            "yardage_marker": "#ffffff",
            "yardage_marker_outline": "#ffffff00",
            "restricted_area": "#ffffff",
            "coaching_box": "#ffffff",
            "team_bench_area": "#196f0c",
            "team_bench_area_outline": "#ffffff",
            "coaching_box_line": "#ffffff"
        }

        self.__init__(
            field_updates = self.field_params,
            color_updates = default_colors
        )

    def reset_field_params(self):
        """Reset the features of the field to their default parameterizations.

        The field parameters can be passed at the initial instantiation of the
        class via the ``field_updates`` parameter, and through the
        ``update_field_params()`` method, these can be changed. This method
        allows the feature parameterization to be reset to their default values
        after experiencing such a change
        """
        # Re-instantiate the class with the default parameters
        default_params = self.league_dimensions[self.league_code]

        self.__init__(
            field_updates = default_params,
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

                - ``"full"``: The entire surface
                - ``"offense"``: The offensive half of the field
                - ``"offence"``: The offensive half of the field
                - ``"offensivehalf"``: The offensive half of the field
                - ``"offensive_half"``: The offensive half of the field
                - ``"offensive half"``: The offensive half of the field
                - ``"offensivehalffield"``: The offensive half of the field
                - ``"offensive_half_field"``: The offensive half of the field
                - ``"offensive half field"``: The offensive half of the field
                - ``"defense"``: The defensive half of the field
                - ``"defence"``: The defensive half of the field
                - ``"defensivehalf"``: The defensive half of the field
                - ``"defensive_half"``: The defensive half of the field
                - ``"defensive half"``: The defensive half of the field
                - ``"defensivehalffield"``: The defensive half of the field
                - ``"defensive_half_field"``: The defensive half of the field
                - ``"defensive half field"``: The defensive half of the field
                - ``"redzone"``: The offensive red zone
                - ``"red_zone"``: The offensive red zone
                - ``"red zone"``: The offensive red zone
                - ``"oredzone"``: The offensive red zone
                - ``"offensive_red_zone"``: The offensive red zone
                - ``"offensive red zone"``: The offensive red zone
                - ``"dredzone"``: The defensive red zone
                - ``"defensive_red_zone"``: The defensive red zone
                - ``"defensive red zone"``: The defensive red zone

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
        # Make the display_range full if an empty string is passed
        if display_range == "" or display_range is None:
            display_range = "full"

        # Copy the supplied xlim and ylim parameters so as not to overwrite
        # the initial memory
        xlim = self.copy_(xlim)
        ylim = self.copy_(ylim)

        # If the limits are being gotten for plotting purposes, use the
        # dimensions that are internal to the surface
        if for_plot:
            half_field_length = (
                self.field_params.get("field_length", 0.0) / 2.0
            )
            half_field_width = self.field_params.get("field_width", 0.0) / 2.0

            red_zone_start = (
                (self.field_params.get("field_length", 0.0) / 2.0) -
                20.0
            )

        # If it's for display (e.g. the draw() method), add in the necessary
        # thicknesses of external features (e.g. sidelines and boundaries)
        if for_display:
            # Determine the length of half of the field (including the
            # thickness of the field)
            half_field_length = (
                (self.field_params.get("field_length", 0.0) / 2.0) +
                self.field_params.get("endzone_length", 0.0) +
                self.field_params.get("boundary_line_thickness", 0.0) +
                self.field_params.get("field_border_thickness", 0.0) +
                self.field_params.get("minor_line_thickness", 0.0) +
                5.0
            )

            half_field_width = (
                (self.field_params.get("field_width", 0.0) / 2.0) +
                self.field_params.get("boundary_line_thickness", 0.0) +
                self.field_params.get("restricted_area_width", 0.0) +
                self.field_params.get("coaching_box_width", 0.0) +
                self.field_params.get("team_bench_width", 0.0) +
                self.field_params.get("field_border_thickness", 0.0) +
                self.field_params.get("minor_line_thickness", 0.0) +
                5.0
            )

            red_zone_start = (
                (self.field_params.get("field_length", 0.0) / 2.0) -
                # Setting to 22 so that entire 20 yard line is visible
                22.0
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (-half_field_length, half_field_length),

                # Offensive half-field
                "offense": (0.0, half_field_length),
                "offence": (0.0, half_field_length),
                "offensivehalf": (0.0, half_field_length),
                "offensive_half": (0.0, half_field_length),
                "offensive half": (0.0, half_field_length),
                "offensivehalffield": (0.0, half_field_length),
                "offensive_half_field": (0.0, half_field_length),
                "offensive half field": (0.0, half_field_length),

                # Defensive half-field
                "defense": (-half_field_length, 0.0),
                "defence": (-half_field_length, 0.0),
                "defensivehalf": (-half_field_length, 0.0),
                "defensive_half": (-half_field_length, 0.0),
                "defensive half": (-half_field_length, 0.0),
                "defensivehalffield": (-half_field_length, 0.0),
                "defensive_half_field": (-half_field_length, 0.0),
                "defensive half field": (-half_field_length, 0.0),

                # Offensive Red Zone
                "redzone": (red_zone_start, half_field_length),
                "red_zone": (red_zone_start, half_field_length),
                "red zone": (red_zone_start, half_field_length),
                "oredzone": (red_zone_start, half_field_length),
                "offensive_red_zone": (red_zone_start, half_field_length),
                "offensive red zone": (red_zone_start, half_field_length),

                # Defensive Red Zone
                "dredzone": (-half_field_length, -red_zone_start),
                "defensive_red_zone": (-half_field_length, -red_zone_start),
                "defensive red zone": (-half_field_length, -red_zone_start)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # field
            xlim = xlims.get(
                display_range,
                (-half_field_length, half_field_length)
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
                # the field, display the entire field
                if xlim >= half_field_length:
                    xlim = -half_field_length

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_field_length)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the field. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                "full": (-half_field_width, half_field_width),

                # Offensive half-field
                "offense": (-half_field_width, half_field_width),
                "offence": (-half_field_width, half_field_width),
                "offensivehalf": (-half_field_width, half_field_width),
                "offensive_half": (-half_field_width, half_field_width),
                "offensive half": (-half_field_width, half_field_width),
                "offensivehalffield": (-half_field_width, half_field_width),
                "offensive_half_field": (-half_field_width, half_field_width),
                "offensive half field": (-half_field_width, half_field_width),

                # Defensive half-field
                "defense": (-half_field_width, half_field_width),
                "defence": (-half_field_width, half_field_width),
                "defensivehalf": (-half_field_width, half_field_width),
                "defensive_half": (-half_field_width, half_field_width),
                "defensive half": (-half_field_width, half_field_width),
                "defensivehalffield": (-half_field_width, half_field_width),
                "defensive_half_field": (-half_field_width, half_field_width),
                "defensive half field": (-half_field_width, half_field_width),

                # Offensive Red Zone
                "redzone": (-half_field_width, half_field_width),
                "red_zone": (-half_field_width, half_field_width),
                "red zone": (-half_field_width, half_field_width),
                "oredzone": (-half_field_width, half_field_width),
                "offensive_red_zone": (-half_field_width, half_field_width),
                "offensive red zone": (-half_field_width, half_field_width),

                # Defensive Red Zone
                "dredzone": (-half_field_width, half_field_width),
                "defensive_red_zone": (-half_field_width, half_field_width),
                "defensive red zone": (-half_field_width, half_field_width)
            }

            # Extract the y limit from the dictionary, defaulting to the full
            # field
            ylim = ylims.get(
                display_range,
                (-half_field_width, half_field_width)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= half_field_width:
                    ylim = -half_field_width

                ylim = (ylim, half_field_width)

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

        # Constrain the limits from going beyond the end of the field (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_field_length),
            min(xlim[1], half_field_length)
        )

        ylim = (
            max(ylim[0], -half_field_width),
            min(ylim[1], half_field_width)
        )

        return xlim, ylim


class CFLField(FootballField):
    """A subclass of ``FootballField`` specific to the CFL.

    See ``FootballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the FootballField class with the relevant parameters
        super().__init__(
            league_code = "cfl",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class NCAAField(FootballField):
    """A subclass of ``FootballField`` specific to the CFL.

    See ``FootballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the FootballField class with the relevant parameters
        super().__init__(
            league_code = "ncaa",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class NFHSField(FootballField):
    """A subclass of ``FootballField`` specific to the NFHS.

    See ``FootballField`` class documentation for full description.
    """

    def __init__(self, n_players = 11, field_updates = {}, *args, **kwargs):
        # Initialize the FootballField class with the relevant parameters
        if n_players in [11, 9, 8, 6]:
            self.n_players = n_players
        else:
            self.n_players = 11
        super().__init__(
            league_code = f"nfhs{self.n_players}",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class NFLField(FootballField):
    """A subclass of ``FootballField`` specific to the NFL.

    See ``FootballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the FootballField class with the relevant parameters
        color_updates = {
            "coaching_box_line": "#ffcb05"
        }

        if "color_updates" in kwargs.keys():
            kwargs["color_updates"] = {
                **color_updates,
                **kwargs["color_updates"]
            }
        else:
            kwargs["color_updates"] = color_updates

        super().__init__(
            league_code = "nfl",
            field_updates = field_updates,
            *args,
            **kwargs
        )
