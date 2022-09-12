"""Extension of the ``BaseSurfacePlot`` class to create a soccer pitch.

This is a second-level child class of the ``BaseSurface`` class, and as such
will have access to its attributes and methods. ``sportypy`` will ship with
pre-defined leagues that will have their own subclass, but a user can manually
specify their own pitch parameters to create a totally-customized pitch. The
pitch's features are parameterized by the basic dimensions of the pitch, which
comprise the attributes of the class.

@author: Ross Drucker
"""
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.soccer as soccer_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class SoccerPitch(BaseSurfacePlot):
    """A subclass of ``BaseSurfacePlot`` to make a generic soccer pitch.

    This allows for the creation of the soccer pitch in a way that is entirely
    parameterized by the pitch's baseline characteristics.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid soccer pitch. The attributes needed to instantiate a
    particular league's surface must be specified in the ``pitch_params``
    dictionary. For many leagues, these will be provided in the
    surface_dimensions.json file in the data/ subdirectory of ``sportypy``.

    See the ``BaseSurfacePlot`` and ``BaseSurface`` class definitions for full
    details.

    Attributes
    ----------
    league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "Major League
        Soccer" should be either "MLS" or "mls"). The default is an empty
        string

    rotation : float
        The angle (in degrees) through which to rotate the final plot. The
        default is ``0.0``

    x_trans : float
        The amount that the ``x`` coordinates are to be shifted. By convention,
        the +``x`` axis extends from the center of the surface towards the
        right-hand goal when viewing the pitch in TV view. The default is
        ``0.0``

    y_trans : float
        The amount that the ``y`` coordinates are to be shifted. By convention,
        the +``y`` axis extends from the center of the surface towards the
        top of the pitch when viewing the pitch in TV view. The default is
        ``0.0``

    pitch_updates : dict
        A dictionary of updated parameters to use for the soccer pitch. The
        default is an empty dictionary

    color_updates : dict
        A dictionary of coloring parameters to pass to the plot. Defaults are
        provided in the class per each rule book, but this allows the plot to
        be more heavily customized/styled. The default is an empty dictionary

    units : str
        The units that the final plot should utilize. The default units are the
        units specified in the rule book of the league. The default is
        ``"default"``

    pitch_params : dict
        A dictionary containing the following parameters of the pitch:

            - pitch_length : float
                The length of the pitch in TV view

            - pitch_width : float
                The width of the pitch in TV view

            - line_thickness : float
                The thickness of the lines on the pitch. All lines should have
                the same thickness

            - center_circle_radius : float
                The (outer) radius of the center circle on the pitch

            - center_mark_radius : float
                The radius of the mark at the center at the pitch

            - corner_arc_radius : float
                The (outer) radius of the arcs in the corners of the pitch

            - goal_line_defensive_mark_visible : boolean
                Whether or not the defensive marks beyond the goal line should
                be visible in the resulting plot

            - touchline_defensive_mark_visible : boolean
                Whether or not the defensive marks beyond the touchline should
                be visible in the resulting plot

            - defensive_mark_depth : float
                The depth (in any direction) of the defensive marks beyond the
                goal line or touchline

            - defensive_mark_distance : float
                The distance from the interior edge of the goal post to the
                defensive mark beyond the goal line. This will also be used to
                determine the distance from the goal line to the defensive mark
                beyond the touchline

            - defensive_mark_separation_from_line : float
                The distance from the exterior edge of the goal line to the
                interior edge of the defensive mark

            - penalty_box_length : float
                The length of the penalty box in TV view. This is the larger of
                the two boxes, and is usually 16.5 m (18 yards) from the back
                edge of the goal line

            - penalty_circle_radius : float
                The radius of the arc at the top of the penalty box. This is
                measured from the center of the penalty mark

            - penalty_mark_dist : float
                The distance from the back edge of the goal line to the center
                of the penalty mark

            - interior_of_goal_post_to_penalty_box : float
                The distance from the interior edge of the goal post to the
                nearest edge of the penalty box

            - interior_of_goal_post_to_goal_box : float
                The distance from the interior edge of the goal post to the
                nearest edge of the goal box

            - goal_box_length : float
                The length of the goal box in TV view. This is the smaller of
                the two boxes, and is usually 5.5 m (6 yards) from the back
                edge of the goal line

            - penalty_mark_radius : float
                The radius of the penalty mark

            - goal_width : float
                The interior distance between the goal posts

            - goal_depth : float
                The depth of the goal from the back edge of the goal line
    """

    def __init__(self, league_code = "", pitch_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a ``SoccerPitch`` class.

        Parameters
        ----------
        league_code : str
            The league for which the plot should be drawn. This is
            case-insensitive but should be the shortened name of the league
            (e.g. "Major League Soccer" should be either "MLS" or "mls"). The
            default is an empty string

        rotation : float
            The angle (in degrees) through which to rotate the final plot. The
            default is ``0.0``

        x_trans : float
            The amount that the ``x`` coordinates are to be shifted. By
            convention, the +``x`` axis extends from the center of the surface
            towards the right-hand goal when viewing the pitch in TV view. The
            default is ``0.0``

        y_trans : float
            The amount that the ``y`` coordinates are to be shifted. By
            convention, the +``y`` axis extends from the center of the surface
            towards the top of the pitch when viewing the pitch in TV view. The
            default is ``0.0``

        pitch_updates : dict
            A dictionary of updated parameters to use to create the soccer
            pitch. The default is an empty dictionary

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
        # Load all pre-defined pitch dimensions for provided leagues
        self._load_preset_dimensions(sport = "soccer")

        # Load all unit conversions
        self._load_unit_conversions()

        # Set the league to be the lower-case version of the supplied value
        self.league_code = league_code.lower()

        # Try to get the league specified from the pre-defined set of leagues
        try:
            pitch_dimensions = self.league_dimensions[self.league_code]

        # If it can't be found, set the pitch_dimensions dictionary to be empty
        except KeyError:
            pitch_dimensions = {}

        # Combine the pitch dimensions (if found from in the pre-defined
        # leagues) with any parameter updates supplied by the user. This will
        # comprise the parameter set with which the pitch is to be drawn
        pitch_params = {
            **pitch_dimensions,
            **pitch_updates
        }

        # Set the passed parameters of the pitch to be the class' pitch_params
        # attribute
        self.pitch_params = pitch_params

        # Convert the pitch's units if needed
        if units.lower() != "default":
            for k, v in pitch_params.items():
                self.pitch_params[k] = self._convert_units(
                    v,
                    self.pitch_params["pitch_units"],
                    units.lower()
                )

            self.pitch_params["pitch_units"] = units.lower()

        # Set the rotation of the plot to be the supplied rotation value
        self.rotation_amt = rotation
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the pitch's necessary shifts. This will overwrite the default
        # values of x_trans and y_trans inherited from the BaseSurfacePlot
        # class (which is in turn inherited from BaseSurface)
        self.x_trans, self.y_trans = x_trans, y_trans

        # Create a container for the relevant features of a pitch
        self._features = []

        # Initialize the x and y limits for the plot be None. These will get
        # set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the default colors of the pitch
        default_colors = {
            "plot_background": "#195f0c00",
            "defensive_half_pitch": "#195f0c",
            "offensive_half_pitch": "#195f0c",
            "pitch_apron": "#195f0c",
            "touchline": "#ffffff",
            "goal_line": "#ffffff",
            "corner_arc": "#ffffff",
            "halfway_line": "#ffffff",
            "center_circle": "#ffffff",
            "center_mark": "#ffffff",
            "penalty_box": "#ffffff",
            "goal_box": "#ffffff",
            "penalty_mark": "#ffffff",
            "corner_defensive_mark": "#ffffff",
            "goal": "#ffffff"
        }

        # Combine the colors with a passed colors dictionary
        if not color_updates:
            color_updates = {}

        # Create the final color set for the features of the pitch
        self.feature_colors = {
            **default_colors,
            **color_updates
        }

        # Initialize the constraint on the pitch to confine all features to be
        # contained within the pitch. The feature itself is not visible (as
        # it's created by the soccer.pitch class)
        pitch_constraint_params = {
            "class": soccer_features.PitchConstraint,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "visible": False
        }
        self._initialize_feature(pitch_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the offensive half of the pitch
        defensive_half_params = {
            "class": soccer_features.HalfPitch,
            "x_anchor": -self.pitch_params.get("pitch_length", 0.0) / 4.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["defensive_half_pitch"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(defensive_half_params)

        # Initialize the offensive half of the pitch
        offensive_half_params = {
            "class": soccer_features.HalfPitch,
            "x_anchor": self.pitch_params.get("pitch_length", 0.0) / 4.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["offensive_half_pitch"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(offensive_half_params)

        # Initialize the pitch apron
        pitch_apron_params = {
            "class": soccer_features.PitchApron,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "pitch_apron_touchline": self.pitch_params.get(
                "pitch_apron_touchline",
                0.0
            ),
            "pitch_apron_goal_line": self.pitch_params.get(
                "pitch_apron_goal_line",
                0.0
            ),
            "is_constrained": False,
            "goal_depth": self.pitch_params.get("goal_depth", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["pitch_apron"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(pitch_apron_params)

        # Initialize the touchlines
        touchline_params = {
            "class": soccer_features.Touchline,
            "x_anchor": 0.0,
            "y_anchor": self.pitch_params.get("pitch_width", 0.0) / 2.0,
            "reflect_x": False,
            "reflect_y": True,
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["touchline"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(touchline_params)

        # Initialize the goal lines
        goal_line_params = {
            "class": soccer_features.GoalLine,
            "x_anchor": self.pitch_params.get("pitch_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["goal_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(goal_line_params)

        # Initialize corner arcs
        corner_arc_params = {
            "class": soccer_features.CornerArc,
            "x_anchor": (
                (self.pitch_params.get("pitch_length", 0.0) / 2.0) -
                (self.pitch_params.get("line_thickness", 0.0) / 2.0)
            ),
            "y_anchor": (
                (self.pitch_params.get("pitch_width", 0.0) / 2.0) -
                (self.pitch_params.get("line_thickness", 0.0) / 2.0)
            ),
            "reflect_x": True,
            "reflect_y": True,
            "feature_radius": self.pitch_params.get("corner_arc_radius", 0.0),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["corner_arc"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(corner_arc_params)

        # Initialize the halfway line
        halfway_line_params = {
            "class": soccer_features.HalfwayLine,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["halfway_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(halfway_line_params)

        # Initialize the penalty (16.5m) box
        penalty_box_params = {
            "class": soccer_features.PenaltyBox,
            "x_anchor": self.pitch_params.get("pitch_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": True,
            "box_length": self.pitch_params.get("penalty_box_length", 0.0),
            "penalty_mark_dist": self.pitch_params.get(
                "penalty_mark_dist",
                0.0
            ),
            "goal_width": self.pitch_params.get("goal_width", 0.0),
            "goal_post_to_box_edge": self.pitch_params.get(
                "interior_of_goal_post_to_penalty_box",
                0.0
            ),
            "feature_radius": self.pitch_params.get(
                "penalty_circle_radius",
                0.0
            ),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["penalty_box"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(penalty_box_params)

        # Initialize the goal box (5.5 m box)
        goal_box_params = {
            "class": soccer_features.GoalBox,
            "x_anchor": self.pitch_params.get("pitch_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "box_length": self.pitch_params.get("goal_box_length", 0.0),
            "goal_width": self.pitch_params.get("goal_width", 0.0),
            "goal_post_to_box_edge": self.pitch_params.get(
                "interior_of_goal_post_to_goal_box",
                0.0
            ),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["goal_box"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(goal_box_params)

        # Initialize the center circle
        center_circle_params = {
            "class": soccer_features.CenterCircle,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_radius": self.pitch_params.get(
                "center_circle_radius",
                0.0
            ),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["center_circle"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(center_circle_params)

        # Initialize the penalty mark
        penalty_mark_params = {
            "class": soccer_features.PenaltyMark,
            "x_anchor": (
                (self.pitch_params.get("pitch_length", 0.0) / 2.0) -
                self.pitch_params.get("penalty_mark_dist", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_radius": self.pitch_params.get(
                "penalty_mark_radius",
                0.0
            ),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["penalty_mark"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(penalty_mark_params)

        # Initialize the center mark
        center_mark_params = {
            "class": soccer_features.CenterMark,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "feature_radius": self.pitch_params.get("center_mark_radius", 0.0),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["center_mark"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(center_mark_params)

        # Initialize the corner defensive mark on the touchline
        touchline_corner_defensive_mark_params = {
            "class": soccer_features.CornerDefensiveMark,
            "x_anchor": (
                (self.pitch_params.get("pitch_length", 0.0) / 2.0) -
                self.pitch_params.get("defensive_mark_distance", 0.0)
            ),
            "y_anchor": self.pitch_params.get("pitch_width", 0.0) / 2.0,
            "reflect_x": True,
            "reflect_y": True,
            "visible": self.pitch_params.get(
                "touchline_defensive_mark_visible",
                True
            ),
            "depth": self.pitch_params.get("defensive_mark_depth", 0.0),
            "separation_from_line": self.pitch_params.get(
                "defensive_mark_separation_from_line",
                0.0
            ),
            "is_touchline": True,
            "is_constrained": False,
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["corner_defensive_mark"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(touchline_corner_defensive_mark_params)

        # Initialize the corner defensive mark on the goal line
        goal_line_corner_defensive_mark_params = {
            "class": soccer_features.CornerDefensiveMark,
            "x_anchor": self.pitch_params.get("pitch_length", 0.0) / 2.0,
            "y_anchor": (
                (self.pitch_params.get("pitch_width", 0.0) / 2.0) -
                self.pitch_params.get("defensive_mark_distance", 0.0)
            ),
            "reflect_x": True,
            "reflect_y": True,
            "visible": self.pitch_params.get(
                "goal_line_defensive_mark_visible",
                True
            ),
            "depth": self.pitch_params.get("defensive_mark_depth", 0.0),
            "separation_from_line": self.pitch_params.get(
                "defensive_mark_separation_from_line",
                0.0
            ),
            "is_goal_line": True,
            "is_constrained": False,
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["corner_defensive_mark"],
            "edgecolor": None,
            "zorder": 17
        }
        self._initialize_feature(goal_line_corner_defensive_mark_params)

        # Initialize the goal
        goal_params = {
            "class": soccer_features.Goal,
            "x_anchor": (
                (self.pitch_params.get("pitch_length", 0.0) / 2.0) -
                self.pitch_params.get("line_thickness", 0.0)
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "visible": True,
            "goal_width": self.pitch_params.get("goal_width", 0.0),
            "goal_depth": self.pitch_params.get("goal_depth", 0.0),
            "feature_thickness": self.pitch_params.get("line_thickness", 0.0),
            "pitch_length": self.pitch_params.get("pitch_length", 0.0),
            "pitch_width": self.pitch_params.get("pitch_width", 0.0),
            "facecolor": self.feature_colors["goal"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(goal_params)

        # Initialize all other features passed as keyword arguments
        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = "full", xlim = None, ylim = None,
             rotation = None):
        """Draw the pitch.

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

                - ``"full"``: The entire pitch
                - ``"offense"``: The offensive half of the pitch. This is the
                        TV-right half
                - ``"offence"``: The offensive half of the pitch. This is the
                        TV-right half
                - ``"offensivehalfpitch"``: The offensive half of the pitch.
                        This is the TV-right half
                - ``"offensive_half_pitch"``: The offensive half of the pitch.
                        This is the TV-right half
                - ``"offensive half pitch"``: The offensive half of the pitch.
                        This is the TV-right half
                - ``"defense"``: The defensive half of the pitch. This is the
                        TV-left half
                - ``"defence"``: The defensive half of the pitch. This is the
                        TV-left half
                - ``"defensivehalfpitch"``: The defensive half of the pitch.
                        This is the TV-left half
                - ``"defensive_half_pitch"``: The defensive half of the pitch.
                        This is the TV-left half
                - ``"defensive half pitch"``: The defensive half of the pitch.
                        This is the TV-left half

            The default is ``"full"``


        xlim : float or tuple of floats or None
            The display range in the ``x`` direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the ``x`` coordinates to display and the upper bound will be the
            +``x`` end of the pitch. If a tuple, the two values will be
            used to determine the bounds. If ``None``, then the
            ``display_range`` will be used instead to set the bounds. The
            default is ``None``

        ylim : float or tuple of floats or None
            The display range in the ``y`` direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the ``y`` coordinates to display and the upper bound will be the
            +``y`` upper touchline. If a tuple, the two values will be used
            to determine the bounds. If ``None``, then the display_range
            ``will`` be used instead to set the bounds. The default is ``None``

        rotation : float or None
            Angle (in degrees) through which to rotate the pitch when
            drawing. If used, this will set the class attribute of
            ``_rotation``. A value of ``0.0`` will correspond to a TV view of
            the pitch, where +``x`` is to the right and +``y`` is on top. The
            rotation occurs counter clockwise. The default is ``None``
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

                # Assuming the feature is visible (and is not the pitch), get
                # the feature's x and y limits to ensure it lies within the
                # bounds of the pitch
                if visible and not isinstance(
                    feature,
                    soccer_features.PitchConstraint
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
            print("The following soccer leagues are available with "
                  "sportypy:\n")

            # Print the current leagues
            for league_code in available_league_codes:
                print(f"- {league_code.upper()}")

    def cani_color_features(self):
        """Determine what features of the pitch can be colored.

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
        """Determine what features of the pitch can be re-parameterized.

        This function is a helper function for the user to aid in customizing
        a pitch's parameters. The printed result of this method will be the
        names of the features that are able to be reparameterized. This method
        is also useful when defining new features and using an existing
        league's pitch dimensions as a starting point

        Returns
        -------
        Nothing, but a message will be printed out
        """
        # Preamble
        print("The following features can be reparameterized via the "
              "pitch_updates parameter, with the current value in "
              "parenthesis:\n")

        # Print the current values of the colors
        for k, v in self.pitch_params.items():
            print(f"- {k} ({v})")

        # Footer
        print("\nThese parameters may be updated with the "
              "update_pitch_params() method")

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
            pitch_updates = self.pitch_params,
            color_updates = updated_colors
        )

    def update_pitch_params(self, pitch_param_updates = {}, *args, **kwargs):
        """Update the pitch's defining parameters.

        This method should primarily be used in cases when plotting a league
        not currently supported by ``sportypy``

        Parameters
        ----------
        pitch_updates : dict
            A dictionary where the keys correspond to the name of the parameter
            of the pitch that is to be updated (see
            ``cani_change_dimensions()`` method for a list of these
            parameters). The default is an empty dictionary

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated parameters
        """
        # Start by getting the currently-used pitch parameters
        current_pitch_params = self.pitch_params

        # Create a new dictionary to hold the updated parameters via dictionary
        # comprehension
        updated_pitch_params = {
            **current_pitch_params,
            **pitch_param_updates
        }

        # Re-instantiate the class with the new parameters
        self.__init__(
            pitch_updates = updated_pitch_params,
            color_updates = self.feature_colors
        )

    def reset_colors(self):
        """Reset the features of the pitch to their default color set.

        The colors can be passed at the initial instantiation of the class via
        the ``color_updates`` parameter, and through the ``update_colors()``
        method, these can be changed. This method allows the colors to be reset
        to their default values after experiencing such a change
        """
        # Re-instantiate the class with the default colors
        default_colors = {
            "plot_background": "#195f0c00",
            "defensive_half_pitch": "#195f0c",
            "offensive_half_pitch": "#195f0c",
            "pitch_apron": "#195f0c",
            "touchline": "#ffffff",
            "goal_line": "#ffffff",
            "corner_arc": "#ffffff",
            "halfway_line": "#ffffff",
            "center_circle": "#ffffff",
            "center_mark": "#ffffff",
            "penalty_box": "#ffffff",
            "goal_box": "#ffffff",
            "penalty_mark": "#ffffff",
            "corner_defensive_mark": "#ffffff",
            "goal": "#ffffff"
        }

        self.__init__(
            pitch_updates = self.pitch_params,
            color_updates = default_colors
        )

    def reset_pitch_params(self):
        """Reset the features of the pitch to their default parameterizations.

        The pitch parameters can be passed at the initial instantiation of the
        class via the ``pitch_updates`` parameter, and through the
        ``update_pitch_params()`` method, these can be changed. This method
        allows the feature parameterization to be reset to their default values
        after experiencing such a change
        """
        # Re-instantiate the class with the default parameters
        default_params = self.league_dimensions[self.league_code]

        self.__init__(
            pitch_updates = default_params,
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

                - ``"full"``: The entire pitch
                - ``"offense"``: The offensive half of the pitch. This is the
                        TV-right half
                - ``"offence"``: The offensive half of the pitch. This is the
                        TV-right half
                - ``"offensivehalfpitch"``: The offensive half of the pitch.
                        This is the TV-right half
                - ``"offensive_half_pitch"``: The offensive half of the pitch.
                        This is the TV-right half
                - ``"offensive half pitch"``: The offensive half of the pitch.
                        This is the TV-right half
                - ``"defense"``: The defensive half of the pitch. This is the
                        TV-left half
                - ``"defence"``: The defensive half of the pitch. This is the
                        TV-left half
                - ``"defensivehalfpitch"``: The defensive half of the pitch.
                        This is the TV-left half
                - ``"defensive_half_pitch"``: The defensive half of the pitch.
                        This is the TV-left half
                - ``"defensive half pitch"``: The defensive half of the pitch.
                        This is the TV-left half

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
            half_pitch_length = (
                self.pitch_params.get("pitch_length", 0.0) / 2.0
            )
            half_pitch_width = (
                self.pitch_params.get("pitch_width", 0.0) / 2.0
            )

        # If it's for display (e.g. the draw() method), add in the necessary
        # thicknesses of external features (e.g. any out of bounds features)
        if for_display:
            half_pitch_length = (
                (self.pitch_params.get("pitch_length", 0.0) / 2.0) +
                self.pitch_params.get("goal_depth", 0.0) +
                self.pitch_params.get("pitch_apron_goal_line", 0.0)
            )

            half_pitch_width = (
                (self.pitch_params.get("pitch_width", 0.0) / 2.0) +
                (self.pitch_params.get("pitch_apron_touchline", 0.0))
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (-half_pitch_length, half_pitch_length),

                # Offensive half-pitch
                "offense": (0.0, half_pitch_length),
                "offence": (0.0, half_pitch_length),
                "offensivehalfpitch": (0.0, half_pitch_length),
                "offensive_half_pitch": (0.0, half_pitch_length),
                "offensive half pitch": (0.0, half_pitch_length),

                # Defensive half-pitch
                "defense": (-half_pitch_length, 0.0),
                "defence": (-half_pitch_length, 0.0),
                "defensivehalfpitch": (-half_pitch_length, 0.0),
                "defensive_half_pitch": (-half_pitch_length, 0.0),
                "defensive half pitch": (-half_pitch_length, 0.0)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # pitch
            xlim = xlims.get(
                display_range,
                (-half_pitch_length, half_pitch_length)
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
                # the pitch, display the entire pitch
                if xlim >= half_pitch_length:
                    xlim = -half_pitch_length

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_pitch_length)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the pitch. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                "full": (-(half_pitch_width), half_pitch_width),
                "offense": (-half_pitch_width, half_pitch_width),
                "offence": (-half_pitch_width, half_pitch_width),
                "offensivehalfpitch": (-half_pitch_width, half_pitch_width),
                "offensive_half_pitch": (-half_pitch_width, half_pitch_width),
                "offensive half pitch": (-half_pitch_width, half_pitch_width),
                "defense": (-half_pitch_width, half_pitch_width),
                "defence": (-half_pitch_width, half_pitch_width),
                "defensivehalfpitch": (-half_pitch_width, half_pitch_width),
                "defensive_half_pitch": (-half_pitch_width, half_pitch_width),
                "defensive half pitch": (-half_pitch_width, half_pitch_width)
            }

            # Extract the y limit from the dictionary, defaulting to the full
            # pitch
            ylim = ylims.get(
                display_range,
                (-half_pitch_width, half_pitch_width)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= half_pitch_width:
                    ylim = -half_pitch_width

                ylim = (ylim, half_pitch_width)

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

        # Constrain the limits from going beyond the end of the pitch (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_pitch_length),
            min(xlim[1], half_pitch_length)
        )

        ylim = (
            max(ylim[0], -half_pitch_width),
            min(ylim[1], half_pitch_width)
        )

        return xlim, ylim


class EPLPitch(SoccerPitch):
    """A subclass of ``SoccerPitch`` specific to the English Premier League.

    See ``SoccerPitch`` class documentation for full description.
    """

    def __init__(self, pitch_updates = {}, *args, **kwargs):
        # Initialize the SoccerPitch class with the relevant parameters
        super().__init__(
            league_code = "epl",
            pitch_updates = pitch_updates,
            *args,
            **kwargs
        )


class FIFAPitch(SoccerPitch):
    """A subclass of ``SoccerPitch`` specific to FIFA.

    See ``SoccerPitch`` class documentation for full description.
    """

    def __init__(self, pitch_updates = {}, *args, **kwargs):
        # Initialize the SoccerPitch class with the relevant parameters
        super().__init__(
            league_code = "fifa",
            pitch_updates = pitch_updates,
            *args,
            **kwargs
        )


class MLSPitch(SoccerPitch):
    """A subclass of ``SoccerPitch`` specific to FIFA.

    See ``SoccerPitch`` class documentation for full description.
    """

    def __init__(self, pitch_updates = {}, *args, **kwargs):
        # Initialize the SoccerPitch class with the relevant parameters
        super().__init__(
            league_code = "mls",
            pitch_updates = pitch_updates,
            *args,
            **kwargs
        )


class NCAAPitch(SoccerPitch):
    """A subclass of ``SoccerPitch`` specific to FIFA.

    See ``SoccerPitch`` class documentation for full description.
    """

    def __init__(self, pitch_updates = {}, *args, **kwargs):
        # Initialize the SoccerPitch class with the relevant parameters
        super().__init__(
            league_code = "ncaa",
            pitch_updates = pitch_updates,
            *args,
            **kwargs
        )


class NWSLPitch(SoccerPitch):
    """A subclass of ``SoccerPitch`` specific to FIFA.

    See ``SoccerPitch`` class documentation for full description.
    """

    def __init__(self, pitch_updates = {}, *args, **kwargs):
        # Initialize the SoccerPitch class with the relevant parameters
        super().__init__(
            league_code = "nwsl",
            pitch_updates = pitch_updates,
            *args,
            **kwargs
        )
