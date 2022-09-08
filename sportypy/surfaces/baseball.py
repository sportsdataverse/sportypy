"""Extension of the ``BaseSurfacePlot`` class to create a baseball field.

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
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.baseball as baseball_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class BaseballField(BaseSurfacePlot):
    """A subclass of the ``BaseSurfacePlot`` class to make a baseball field.

    This allows for the creation of the baseball field in a way that is
    entirely parameterized by the field's baseline characteristics. By
    convention, TV view for baseball is identical to the view from the high
    home plate camera.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid baseball field. The attributes needed to instantiate a
    particular league's surface must be specified in the ``field_params``
    dictionary. For many leagues, these will be provided in the
    surface_dimensions.json file in the data/ subdirectory of ``sportypy``.

    See the ``BaseSurfacePlot`` and ``BaseSurface`` class definitions for full
    details.

    Attributes
    ----------
    league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "Major League
        Baseball" should be either "MLB" or "mlb"). The default is an empty
        string

    rotation_amt : float
        The angle (in degrees) through which to rotate the final plot. The
        default is ``0.0``

    x_trans : float
        The amount that the ``x`` coordinates are to be shifted. By convention,
        the +``x`` axis extends from the pitcher's plate towards first base
        when viewing the field in TV view. The default is ``0.0``

    y_trans : float
        The amount that the ``y`` coordinates are to be shifted. By convention,
        the +``y`` axis extends from the back tip of home plate out towards
        center field when viewing the field in TV view. The default is ``0.0``

    feature_colors : dict
        A dictionary of coloring parameters to pass to the plot

    field_params : dict
        A dictionary containing the following parameters of the field:

            - field_units : str
                The units of the field

            - left_field_distance : float
                The straight-line distance from the back tip of home plate to
                the left field foul pole (along theta = -45°)

            - right_field_distance : float
                The straight-line distance from the back tip of home plate to
                the right field foul pole (along theta = +45°)

            - center_field_distance : float
                The straight-line distance from the back tip of home plate to
                straight-away center field (along theta = 0°)

            - baseline_distance : float
                The distance of each baseline

            - running_lane_start_distance : float
                The straight-line distance from the back tip of home plate to
                the start of the running lane

            - running_lane_depth : float
                The straight-line distance from the outer edge of the
                first-base line to the outer edge of the running lane

            - running_lane_length : float
                The straight-line length of the running lane measured from the
                point nearest home plate. As an example, if the base lines are
                90 feet, and the running lane starts a distance of 45 feet down
                the line from the back tip of home plate, and extends 3 feet
                beyond first base, this parameter would be given as ``48.0``

            - pitchers_mound_center_to_home_plate : float
                The distance from the center of the pitcher's mound to the back
                tip of home plate. NOTE: this does not necessarily align with
                the front edge of the pitcher's plate

            - pitchers_mound_radius : float
                The radius of the pitcher's mound

            - pitchers_plate_front_to_home_plate : float
                The distance from the front edge of the pitcher's plate to the
                back tip of home plate

            - pitchers_plate_width : float
                The width of the pitcher's plate (the dimension in the ``y``
                direction)

            - pitchers_plate_length : float
                The length of the pitcher's plate (the dimension in the ``x``
                direction)

            - base_side_length : float
                The length of one side of a square base

            - home_plate_edge_length : float
                The length of a full side of home plate

            - infield_arc_radius : float
                The distance from the front edge of the pitcher's mound to the
                back of the infield dirt

            - base_anchor_to_infield_grass_radius : float
                The distance from the anchor point of a base to the circular
                cutout in the infield grass. The anchor point of a base is
                defined as the point used in the definition of the base paths.
                As an example, in MLB, the anchor point of first base would be
                the corner of the first base bag along the foul line on the
                side furthest from the back tip of home plate

            - line_width : float
                The thickness of all chalk lines on the field

            - foul_line_to_infield_grass : float
                The distance from the outer edge of the foul line to the outer
                edge of the infield grass

            - foul_line_to_foul_grass : float
                The distance from the outer edge of the foul line to the inner
                edge of the grass in foul territory

            - batters_box_length : float
                The length of the batter's box (in the y direction) measured
                from the outside of the chalk lines

            - batters_box_width : float
                The width of the batter's box (in the x direction) measured
                from the outside of the chalk lines

            - batters_box_y_adj : float
                The shift off of center in the y direction that the batter's
                box needs to be moved to properly align

            - home_plate_side_to_batters_box : float
                The distance from the outer edge of the batter's box to the
                outer edge of home plate

            - catchers_box_shape : str
                The shape of the catcher's box. Currently-supported values are:
                - "rectangle" (default behavior)
                - "trapezoid" (see LittleLeagueField for example)

            - catchers_box_depth : float
                The distance from the back tip of home plate to the back edge
                of the catcher's box

            - backstop_radius : float
                The distance from the back tip of home plate to the interior
                edge of the backstop

            - home_plate_circle_radius : float
                The radius of the dirt circle surrounding home plate
    """

    def __init__(self, league_code = "", field_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a ``BaseballField`` class.

        Parameters
        ----------
        league_code : str
            The league for which the plot should be drawn. This is
            case-insensitive but should be the shortened name of the league
            (e.g. "Major League Baseball" should be either "MLB" or "mlb"). The
            default is an empty string

        rotation : float
            The angle (in degrees) through which to rotate the final plot. The
            default is 0.0

        x_trans : float
            The amount that the x coordinates are to be shifted. By convention,
            the +``x`` axis extends from the pitcher's plate towards first base
            when viewing the field in TV view. The default is ``0.0``

        y_trans : float
            The amount that the y coordinates are to be shifted. By convention,
            the +``y`` axis extends from the back tip of home plate out towards
            center field when viewing the field in TV view. The default is
            ``0.0``

        field_updates: dict
            A dictionary of updated parameters to use to create the baseball
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
        self._load_preset_dimensions(sport = "baseball")

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

        # Convert the field's units if needed
        if units.lower() != "default":
            for k, v in field_params.items():
                self.field_params[k] = self._convert_units(
                    v,
                    self.field_params["field_units"],
                    units.lower()
                )

            self.field_params["field_units"] = units.lower()

        # Set the rotation of the plot to be the supplied rotation value
        self.rotation_amt = rotation
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the field's necessary shifts. This will overwrite the default
        # values of x_trans and y_trans inherited from the BaseSurfacePlot
        # class (which is in turn inherited from BaseSurface)
        self.x_trans, self.y_trans = x_trans, y_trans

        # Create a container for the relevant features of an field
        self._features = []

        # Initialize the x and y limits for the plot be None. These will get
        # set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the default colors of the field
        default_colors = {
            "plot_background": "#395d33",
            "infield_dirt": "#9b7653",
            "infield_grass": "#395d33",
            "pitchers_mound": "#9b7653",
            "base": "#ffffff",
            "pitchers_plate": "#ffffff",
            "batters_box": "#ffffff",
            "catchers_box": "#ffffff",
            "foul_line": "#ffffff",
            "running_lane": "#ffffff"
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
        # contained within the field's boundary. The feature itself is not
        # visible
        field_constraint_params = {
            "class": baseball_features.FieldConstraint,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_radius": self.field_params.get("corner_radius", 0.0),
            "feature_thickness": self.field_params.get("board_thickness", 0.0),
            "visible": False
        }
        self._initialize_feature(field_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the infield dirt
        infield_dirt_params = {
            "class": baseball_features.InfieldDirt,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "home_plate_circle_radius": self.field_params.get(
                "home_plate_circle_radius",
                0.0
            ),
            "foul_line_to_foul_grass": self.field_params.get(
                "foul_line_to_foul_grass",
                0.0
            ),
            "infield_arc_radius": self.field_params.get(
                "infield_arc_radius",
                0.0
            ),
            "pitchers_plate_dist": self.field_params.get(
                "pitchers_plate_front_to_home_plate",
                0.0
            ),
            "facecolor": self.feature_colors["infield_dirt"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(infield_dirt_params)

        # Initialize the infield grass
        infield_grass_params = {
            "class": baseball_features.InfieldGrass,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "home_plate_circle_radius": self.field_params.get(
                "home_plate_circle_radius",
                0.0
            ),
            "foul_line_to_infield_grass": self.field_params.get(
                "foul_line_to_infield_grass",
                0.0
            ),
            "feature_radius": self.field_params.get(
                "base_anchor_to_infield_grass_radius",
                0.0
            ),
            "baseline_distance": self.field_params.get(
                "baseline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["infield_grass"],
            "edgecolor": None,
            "zorder": 6
        }
        self._initialize_feature(infield_grass_params)

        # Initialize the pitcher's mound
        pitchers_mound_params = {
            "class": baseball_features.PitchersMound,
            "x_anchor": 0.0,
            "y_anchor": self.field_params.get(
                "pitchers_mound_center_to_home_plate",
                0.0
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_radius": self.field_params.get(
                "pitchers_mound_radius",
                0.0
            ),
            "facecolor": self.feature_colors["pitchers_mound"],
            "edgecolor": None,
            "zorder": 7
        }
        self._initialize_feature(pitchers_mound_params)

        # Initialize home plate
        home_plate_params = {
            "class": baseball_features.HomePlate,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "home_plate_edge_length": self.field_params.get(
                "home_plate_edge_length",
                0.0
            ),
            "facecolor": self.feature_colors["base"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(home_plate_params)

        # Initialize first base
        first_base_params = {
            "class": baseball_features.Base,
            "x_anchor": (
                self.field_params.get("baseline_distance", 0.0) *
                math.cos(np.pi / 4.0)
            ),
            "y_anchor": (
                self.field_params.get("baseline_distance", 0.0) *
                math.sin(np.pi / 4.0)
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "base_side_length": self.field_params.get("base_side_length", 0.0),
            "adjust_x_left": True,
            "facecolor": self.feature_colors["base"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(first_base_params)

        # Initialize second base
        second_base_params = {
            "class": baseball_features.Base,
            "x_anchor": 0.0,
            "y_anchor": (
                self.field_params.get("baseline_distance", 0.0) *
                math.sqrt(2.0)
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "base_side_length": self.field_params.get("base_side_length", 0.0),
            "adjust_x_left": False,
            "facecolor": self.feature_colors["base"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(second_base_params)

        # Initialize third base
        third_base_params = {
            "class": baseball_features.Base,
            "x_anchor": (
                self.field_params.get("baseline_distance", 0.0) *
                math.cos(3.0 * np.pi / 4.0)
            ),
            "y_anchor": (
                self.field_params.get("baseline_distance", 0.0) *
                math.sin(3.0 * np.pi / 4.0)
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "base_side_length": self.field_params.get("base_side_length", 0.0),
            "adjust_x_right": True,
            "facecolor": self.feature_colors["base"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(third_base_params)

        # Initialize the pitcher's plate
        pitchers_plate_params = {
            "class": baseball_features.PitchersPlate,
            "x_anchor": 0.0,
            "y_anchor": self.field_params.get(
                "pitchers_plate_front_to_home_plate",
                0.0
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "pitchers_plate_length": self.field_params.get(
                "pitchers_plate_length"
            ),
            "feature_thickness": self.field_params.get(
                "pitchers_plate_width",
                0.0
            ),
            "facecolor": self.feature_colors["pitchers_plate"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(pitchers_plate_params)

        # Initialize the batter's boxes
        batters_box_params = {
            "class": baseball_features.BattersBox,
            "x_anchor": (
                (self.field_params.get("home_plate_edge_length", 0.0) / 2.0) +
                self.field_params.get("home_plate_side_to_batters_box", 0.0) +
                (self.field_params.get("batters_box_width", 0.0) / 2.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_thickness": self.field_params.get("line_width", 0.0),
            "batters_box_length": self.field_params.get(
                "batters_box_length",
                0.0
            ),
            "batters_box_width": self.field_params.get(
                "batters_box_width",
                0.0
            ),
            "batters_box_y_adj": self.field_params.get(
                "batters_box_y_adj",
                0.0
            ),
            "facecolor": self.feature_colors["batters_box"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(batters_box_params)

        # Initialize the batter's boxes
        catchers_box_params = {
            "class": baseball_features.CatchersBox,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_thickness": self.field_params.get("line_width", 0.0),
            "feature_radius": self.field_params.get(
                "home_plate_circle_radius",
                0.0
            ),
            "catchers_box_depth": self.field_params.get(
                "catchers_box_depth",
                0.0
            ),
            "catchers_box_width": self.field_params.get(
                "catchers_box_width",
                0.0
            ),
            "batters_box_length": self.field_params.get(
                "batters_box_length",
                0.0
            ),
            "batters_box_y_adj": self.field_params.get(
                "batters_box_y_adj",
                0.0
            ),
            "catchers_box_shape": self.field_params.get(
                "catchers_box_shape",
                "rectangle"
            ),
            "facecolor": self.feature_colors["catchers_box"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(catchers_box_params)

        # Initialize the left field foul line
        left_field_foul_line_params = {
            "class": baseball_features.FoulLine,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_thickness": self.field_params.get("line_width", 0.0),
            "is_line_1b": False,
            "line_distance": self.field_params.get(
                "left_field_distance",
                0.0
            ),
            "batters_box_length": self.field_params.get(
                "batters_box_length",
                0.0
            ),
            "batters_box_width": self.field_params.get(
                "batters_box_width",
                0.0
            ),
            "home_plate_side_to_batters_box": self.field_params.get(
                "home_plate_side_to_batters_box",
                0.0
            ),
            "batters_box_y_adj": self.field_params.get(
                "batters_box_y_adj",
                0.0
            ),
            "facecolor": self.feature_colors["foul_line"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(left_field_foul_line_params)

        # Initialize the right field foul line
        right_field_foul_line_params = {
            "class": baseball_features.FoulLine,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_thickness": self.field_params.get("line_width", 0.0),
            "is_line_1b": True,
            "line_distance": self.field_params.get(
                "right_field_distance",
                0.0
            ),
            "batters_box_length": self.field_params.get(
                "batters_box_length",
                0.0
            ),
            "batters_box_width": self.field_params.get(
                "batters_box_width",
                0.0
            ),
            "home_plate_side_to_batters_box": self.field_params.get(
                "home_plate_side_to_batters_box",
                0.0
            ),
            "batters_box_y_adj": self.field_params.get(
                "batters_box_y_adj",
                0.0
            ),
            "facecolor": self.feature_colors["foul_line"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(right_field_foul_line_params)

        # Initialize the running lane on the first base line
        running_lane_params = {
            "class": baseball_features.RunningLane,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "is_constrained": False,
            "feature_units": self.field_params.get("field_units", "ft"),
            "feature_thickness": self.field_params.get("line_width", 0.0),
            "running_lane_start_distance": self.field_params.get(
                "running_lane_start_distance",
                0.0
            ),
            "running_lane_length": self.field_params.get(
                "running_lane_length",
                0.0
            ),
            "running_lane_depth": self.field_params.get(
                "running_lane_depth",
                0.0
            ),
            "facecolor": self.feature_colors["running_lane"],
            "edgecolor": None,
            "zorder": 18
        }
        self._initialize_feature(running_lane_params)

        # Initialize all other features passed as keyword arguments
        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = "full", xlim = None, ylim = None,
             rotation = None):
        """Draw the field.

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

                - ``"full"``: The entire surface
                - ``"infield"``: The infield portion of the baseball diamond

            The default is ``"full"``

        xlim : float or tuple of floats or None
            The display range in the ``x`` direction to be used. If a single
            float is provided, this will be used as the lower bound of the
            ``x`` coordinates to display and the upper bound will be the +``x``
            end of the field. If a tuple, the two values will be used to
            determine the bounds. If ``None``, then the ``display_range`` will
            be used instead to set the bounds. The default is ``None``

        ylim : float or tuple of floats or None
            The display range in the ``y`` direction to be used. If a single
            float is provided, this will be used as the lower bound of the
            ``y`` coordinates to display and the upper bound will be the +``y`
            end of the field. If a tuple, the two values will be used to
            determine the bounds. If ``None``, then the ``display_range`` will
            be used instead to set the bounds. The default is ``None``

        rotation : float or None
            Angle (in degrees) through which to rotate the field when drawing.
            If used, this will set the class attribute of ``_rotation``. A
            value of ``0.0`` will correspond to a TV view of the field, where
            +``x`` is to the right and +``y`` is on top. The rotation occurs
            counter clockwise
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
        ax.grid(visible = False, which = "both")
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
                    feature, baseball_features.FieldConstraint
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

        A user may wish to know if a specific baseball league can be plotted.
        This method allows a user to check if that specific league code comes
        shipped with ``sportypy`` for easier plotting (if they provide the
        league code), or can also show what leagues are available to be plotted

        Parameters
        ----------
        league_code : str or None
            A league code that may or may not be shipped with the package. If
            the league code is ``None``, this will display all leagues that do
            come shipped with ``sportypy11. The default is ``None``

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
            print("The following baseball leagues are available with "
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
            "plot_background": "#395d33",
            "infield_dirt": "#9b7653",
            "infield_grass": "#395d33",
            "pitchers_mound": "#9b7653",
            "base": "#ffffff",
            "pitchers_plate": "#ffffff",
            "batters_box": "#ffffff",
            "catchers_box": "#ffffff",
            "foul_line": "#ffffff",
            "running_lane": "#ffffff"
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
                - ``"infield"``: The infield portion of the baseball diamond

            The default is ``"full"``

        xlim : float or None
            A specific limit on ``x`` for the plot. The default is ``None``

        ylim : float or None
            A specific limit on ``y`` for the plot. The default is `None``

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
            left_field_distance_x = (
                self.field_params.get("left_field_distance", 0.0) *
                math.cos(3.0 * np.pi / 4.0)
            )
            right_field_distance_x = (
                self.field_params.get("right_field_distance", 0.0) *
                math.cos(np.pi / 4.0)
            )
            left_infield_distance_x = (
                -self.field_params.get("infield_arc_radius", 0.0)
            )
            right_infield_distance_x = (
                self.field_params.get("infield_arc_radius", 0.0)
            )
            backstop_radius_y = -self.field_params.get("backstop_radius", 0.0)
            center_field_distance_y = self.field_params.get(
                "center_field_distance",
                0.0
            )
            home_plate_circle_y = -self.field_params.get(
                "home_plate_circle_radius",
                0.0
            )
            infield_arc_y = (
                self.field_params.get(
                    "pitchers_plate_front_to_home_plate",
                    0.0
                ) +
                self.field_params.get("infield_arc_radius", 0.0)
            )

        # If it's for display (e.g. the draw() method), add in the necessary
        # thicknesses of external features (e.g. running lane and other out of
        # play features)
        if for_display:
            left_field_distance_x = (
                self.field_params.get("left_field_distance", 0.0) *
                math.cos(3.0 * np.pi / 4.0)
            ) + 5.0
            right_field_distance_x = (
                self.field_params.get("right_field_distance", 0.0) *
                math.cos(np.pi / 4.0)
            ) + 5.0
            left_infield_distance_x = (
                -self.field_params.get("infield_arc_radius", 0.0)
            ) - 5.0
            right_infield_distance_x = (
                self.field_params.get("infield_arc_radius", 0.0)
            ) + 5.0
            backstop_radius_y = -(
                self.field_params.get("backstop_radius", 0.0) +
                5.0
            )
            center_field_distance_y = self.field_params.get(
                "center_field_distance",
                0.0
            ) + 5.0
            home_plate_circle_y = -(
                self.field_params.get(
                    "home_plate_circle_radius",
                    0.0
                ) + 5.0
            )
            infield_arc_y = (
                self.field_params.get(
                    "pitchers_plate_front_to_home_plate",
                    0.0
                ) +
                self.field_params.get("infield_arc_radius", 0.0) +
                5.0
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (left_field_distance_x, right_field_distance_x),
                "infield": (left_infield_distance_x, right_infield_distance_x)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # field
            xlim = xlims.get(
                display_range,
                (left_field_distance_x, right_field_distance_x)
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
                if xlim >= right_field_distance_x:
                    xlim = -left_field_distance_x

                # Set the x limit to be a tuple as described above
                xlim = (xlim, left_field_distance_x)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the field. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                "full": (backstop_radius_y, center_field_distance_y),
                "infield": (home_plate_circle_y, infield_arc_y)
            }

            # Extract the y limit from the dictionary, defaulting to the full
            # field
            ylim = ylims.get(
                display_range,
                (backstop_radius_y, center_field_distance_y)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= center_field_distance_y:
                    ylim = backstop_radius_y

                ylim = (ylim, center_field_distance_y)

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
            max(xlim[0], left_field_distance_x),
            min(xlim[1], right_field_distance_x)
        )

        ylim = (
            max(ylim[0], backstop_radius_y),
            min(ylim[1], center_field_distance_y)
        )

        return xlim, ylim


class LittleLeagueField(BaseballField):
    """A subclass of ``BaseballField`` specific to Little League.

    See ``BaseballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the BaseballField class with the relevant parameters
        super().__init__(
            league_code = "little_league",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class MiLBField(BaseballField):
    """A subclass of ``BaseballField`` specific to MiLB.

    See ``BaseballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the BaseballField class with the relevant parameters
        super().__init__(
            league_code = "milb",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class MLBField(BaseballField):
    """A subclass of ``BaseballField`` specific to MLB.

    See ``BaseballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the BaseballField class with the relevant parameters
        super().__init__(
            league_code = "mlb",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class NCAAField(BaseballField):
    """A subclass of ``BaseballField`` specific to NCAA baseball.

    See ``BaseballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the BaseballField class with the relevant parameters
        super().__init__(
            league_code = "ncaa",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class NFHSField(BaseballField):
    """A subclass of ``BaseballField`` specific to NFHS (high school baseball).

    See ``BaseballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the BaseballField class with the relevant parameters
        super().__init__(
            league_code = "nfhs",
            field_updates = field_updates,
            *args,
            **kwargs
        )


class PonyField(BaseballField):
    """A subclass of ``BaseballField`` specific to Pony League Baseball.

    See ``BaseballField`` class documentation for full description.
    """

    def __init__(self, field_updates = {}, *args, **kwargs):
        # Initialize the BaseballField class with the relevant parameters
        super().__init__(
            league_code = "pony",
            field_updates = field_updates,
            *args,
            **kwargs
        )
