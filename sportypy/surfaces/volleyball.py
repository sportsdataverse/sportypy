"""Extension of the ``BaseSurfacePlot`` class to create a volleyball court.

This is a second-level child class of the ``BaseSurface`` class, and as such
will have access to its attributes and methods. ``sportypy`` will ship with
pre-defined leagues that will have their own subclass, but a user can manually
specify their own court parameters to create a totally-customized court. The
court's features are parameterized by the basic dimensions of the court, which
comprise the attributes of the class.

@author: Ross Drucker
"""
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.volleyball as volleyball_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class VolleyballCourt(BaseSurfacePlot):
    """A subclass of ``BaseSurfacePlot`` to make a generic volleyball court.

    This allows for the creation of the volleyball court in a way that is
    entirely parameterized by the court's baseline characteristics.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid volleyball court. The attributes needed to instantiate a
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
        Volleyball Association" should be either "NBA" or "nba"). The default
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

        - free_zone_end_line : float
            The distance beyond the end line that the free zone extends. This
            is measured from the exterior edge of the end line

        - free_zone_sideline : float
            The distance beyond the sideline that the free zone extends. This
            is measured from the exterior edge of the sideline

        - court_apron_endline : float
            The thickness of the court's apron beyond the end line

        - court_apron_sideline : float
            The thickness of the court's apron beyond the sideline

        - line_thickness : float
            The thickness of the lines of the court in the court's specified
            units

        - attack_line_edge_to_center_line : float
            The distance from the edge of the attack line to the center line,
            measuring from the outer (end line side) edge of the attack line
            to the center of the center line (``x = 0`` in TV view)

        - substitution_zone_dash_length : float
            The length of a substitution zone dash measured in the direction
            perpendicular to the sideline

        - substitution_zone_dash_breaks : float
            The separation between dashes in the substitution zone

        - substitution_zone_rep_pattern : str
            The number of times that the break-dash pattern should be repeated
            to generate the substitution zone

        - service_zone_mark_length : float
            The length of the service zone marker when measured in the
            direction perpendicular to the end line

        - service_zone_mark_to_end_line : float
            The separation between the outer edge of the end line and the inner
            edge of the service zone mark
    """

    def __init__(self, league_code = "", court_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a ``VolleyballCourt`` class.

        Parameters
        ----------
        league_code : str
            The league for which the plot should be drawn. This is
            case-insensitive but should be the shortened name of the league
            (e.g. "National Collegiate Athletic Association" should be either
            "NCAA" or "ncaa"). The default is an empty string

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
            A dictionary of updated parameters to use to create the volleyball
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
        self._load_preset_dimensions(sport = "volleyball")

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
            "free_zone": "#d2ab6f",
            "front_zone": "#d2ab6f",
            "defensive_backcourt": "#d2ab6f",
            "offensive_backcourt": "#d2ab6f",
            "court_apron": "#d2ab6f",
            "end_line": "#000000",
            "sideline": "#000000",
            "attack_line": "#000000",
            "center_line": "#000000",
            "service_zone_mark": "#000000",
            "substitution_zone": "#000000"
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
        # it's created by the volleyball.court class)
        court_constraint_params = {
            "class": volleyball_features.CourtConstraint,
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

        # Initialize the free zone
        free_zone_params = {
            "class": volleyball_features.FreeZone,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "free_zone_end_line": self.court_params.get(
                "free_zone_end_line",
                0.0
            ),
            "free_zone_sideline": self.court_params.get(
                "free_zone_sideline",
                0.0
            ),
            "facecolor": self.feature_colors["free_zone"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(free_zone_params)

        # Initialize the court apron
        court_apron_params = {
            "class": volleyball_features.CourtApron,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "is_constrained": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "court_apron_end_line": self.court_params.get(
                "court_apron_end_line",
                0.0
            ),
            "court_apron_sideline": self.court_params.get(
                "court_apron_sideline",
                0.0
            ),
            "facecolor": self.feature_colors["court_apron"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(court_apron_params)

        # Initialize the front zone
        front_zone_params = {
            "class": volleyball_features.FrontZone,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "attack_line_edge_to_center_line": self.court_params.get(
                "attack_line_edge_to_center_line",
                0.0
            ),
            "facecolor": self.feature_colors["front_zone"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(front_zone_params)

        # Initialize the defensive backcourt
        defensive_backcourt_params = {
            "class": volleyball_features.Backcourt,
            "x_anchor": -self.court_params.get(
                "attack_line_edge_to_center_line",
                0.0
            ) -
            (
                (
                    (self.court_params.get("court_length", 0.0) / 2.0) -
                    self.court_params.get(
                        "attack_line_edge_to_center_line",
                        0.0
                    )
                ) / 2.0
            ),
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "attack_line_edge_to_center_line": self.court_params.get(
                "attack_line_edge_to_center_line",
                0.0
            ),
            "facecolor": self.feature_colors["defensive_backcourt"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(defensive_backcourt_params)

        # Initialize the offensive backcourt
        offensive_backcourt_params = {
            "class": volleyball_features.Backcourt,
            "x_anchor": (
                self.court_params.get("attack_line_edge_to_center_line", 0.0) +
                (
                    (
                        (self.court_params.get("court_length", 0.0) / 2.0) -
                        (
                            self.court_params.get(
                                "attack_line_edge_to_center_line",
                                0.0
                            )
                        )
                    ) / 2.0
                )
            ),
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "attack_line_edge_to_center_line": self.court_params.get(
                "attack_line_edge_to_center_line",
                0.0
            ),
            "facecolor": self.feature_colors["offensive_backcourt"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(offensive_backcourt_params)

        # Initialize the service zone marks
        service_zone_mark_params = {
            "class": volleyball_features.ServiceZoneMark,
            "x_anchor": (
                (self.court_params.get("court_length", 0.0) / 2.0) +
                self.court_params.get("service_zone_mark_to_end_line", 0.0)
            ),
            "y_anchor": self.court_params.get("court_width", 0.0) / 2.0,
            "reflect_x": True,
            "reflect_y": True,
            "is_constrained": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "service_zone_mark_length": self.court_params.get(
                "service_zone_mark_length",
                0.0
            ),
            "facecolor": self.feature_colors["service_zone_mark"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(service_zone_mark_params)

        # Initialize the substitution zone dashes
        n_substitution_zone_reps = self.court_params.get(
            "substitution_zone_rep_pattern",
            1
        )
        n_substitution_zone_reps = int(n_substitution_zone_reps)
        substitution_zone_y_anchor = (
            (self.court_params.get("court_width", 0.0) / 2.0) +
            self.court_params.get("substitution_zone_dash_breaks", 0.0)
        )
        for n_dash in range(0, n_substitution_zone_reps):
            substitution_zone_params = {
                "class": volleyball_features.SubstitutionZoneDash,
                "x_anchor": self.court_params.get(
                    "attack_line_edge_to_center_line",
                    0.0
                ),
                "y_anchor": substitution_zone_y_anchor,
                "reflect_x": True,
                "reflect_y": True,
                "is_constrained": False,
                "court_length": self.court_params.get("court_length", 0.0),
                "court_width": self.court_params.get("court_width", 0.0),
                "feature_thickness": self.court_params.get(
                    "line_thickness",
                    0.0
                ),
                "dash_length": self.court_params.get(
                    "substitution_zone_dash_length",
                    0.0
                ),
                "facecolor": self.feature_colors["substitution_zone"],
                "edgecolor": None,
                "zorder": 16
            }
            self._initialize_feature(substitution_zone_params)

            # Increase the y-anchor
            substitution_zone_y_anchor += (
                self.court_params.get("substitution_zone_dash_breaks", 0.0) +
                self.court_params.get("substitution_zone_dash_length", 0.0)
            )

        # Initialize the end lines
        end_line_params = {
            "class": volleyball_features.EndLine,
            "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["end_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(end_line_params)

        # Initialize the sidelines
        sideline_params = {
            "class": volleyball_features.Sideline,
            "x_anchor": 0.0,
            "y_anchor": self.court_params.get("court_width", 0.0) / 2.0,
            "reflect_x": False,
            "reflect_y": True,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["sideline"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(sideline_params)

        # Initialize the center line
        center_line_params = {
            "class": volleyball_features.CenterLine,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["center_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(center_line_params)

        # Initialize the attack line
        attack_line_params = {
            "class": volleyball_features.AttackLine,
            "x_anchor": self.court_params.get(
                "attack_line_edge_to_center_line",
                0.0
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("court_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["attack_line"],
            "edgecolor": None,
            "zorder": 16
        }
        self._initialize_feature(attack_line_params)

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
                - ``"in bounds only"``: The full in-bound area of the court
                - ``"in_bounds_only"``: The full in-bound area of the court
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
                    volleyball_features.CourtConstraint
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

        A user may wish to know if a specific volleyball league can be plotted.
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
            print("The following volleyball leagues are available with "
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
            "free_zone": "#d2ab6f",
            "front_zone": "#d2ab6f",
            "defensive_backcourt": "#d2ab6f",
            "offensive_backcourt": "#d2ab6f",
            "court_apron": "#d2ab6f",
            "end_line": "#000000",
            "sideline": "#000000",
            "attack_line": "#000000",
            "center_line": "#000000",
            "service_zone_mark": "#000000",
            "substitution_zone": "#000000"
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
                - ``"in bounds only"``: The full in-bound area of the court
                - ``"in_bounds_only"``: The full in-bound area of the court
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
                self.court_params.get("free_zone_end_line", 0.0)
            )

            half_court_width = (
                (self.court_params.get("court_width", 0.0) / 2.0) +
                self.court_params.get("free_zone_sideline", 0.0)
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (-half_court_length, half_court_length),
                "inboundsonly": (
                    -(self.court_params.get("court_length", 0.0) / 2.0),
                    self.court_params.get("court_length", 0.0) / 2.0,
                ),
                "in_bounds_only": (
                    -(self.court_params.get("court_length", 0.0) / 2.0),
                    self.court_params.get("court_length", 0.0) / 2.0,
                ),

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
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                "full": (-(half_court_width), half_court_width),
                "inboundsonly": (
                    -(self.court_params.get("court_width", 0.0) / 2.0),
                    self.court_params.get("court_width", 0.0) / 2.0,
                ),
                "in_bounds_only": (
                    -(self.court_params.get("court_width", 0.0) / 2.0),
                    self.court_params.get("court_width", 0.0) / 2.0,
                ),
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


class FIVBCourt(VolleyballCourt):
    """A subclass of ``VolleyballCourt`` specific to FIVB.

    See ``VolleyballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the VolleyballCourt class with the relevant parameters
        super().__init__(
            league_code = "fivb",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class NCAACourt(VolleyballCourt):
    """A subclass of ``VolleyballCourt`` specific to NCAA.

    See ``VolleyballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the VolleyballCourt class with the relevant parameters
        super().__init__(
            league_code = "ncaa",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class USAVolleyballCourt(VolleyballCourt):
    """A subclass of ``VolleyballCourt`` specific to FIVB.

    See ``VolleyballCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the VolleyballCourt class with the relevant parameters
        super().__init__(
            league_code = "fivb",
            court_updates = court_updates,
            *args,
            **kwargs
        )
