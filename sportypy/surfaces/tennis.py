"""Extension of the ``BaseSurfacePlot`` class to create a tennis court.

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
import sportypy._feature_classes.tennis as tennis_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class TennisCourt(BaseSurfacePlot):
    """A subclass of ``BaseSurfacePlot`` to make a generic tennis court.

    This allows for the creation of the tennis court in a way that is entirely
    parameterized by the court's baseline characteristics.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid tennis court. The attributes needed to instantiate a
    particular league's surface must be specified in the ``court_params``
    dictionary. For many leagues, these will be provided in the
    surface_dimensions.json file in the data/ subdirectory of ``sportypy``.

    See the ``BaseSurfacePlot`` and ``BaseSurface`` class definitions for full
    details.

    Attributes
    ----------
    league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "International
        Tennis Federation" should be either "ITF" or "itf"). The default is an
        empty string

    rotation : float
        The angle (in degrees) through which to rotate the final plot. The
        default is ``0.0``

    x_trans : float
        The amount that the ``x`` coordinates are to be shifted. By convention,
        the +``x`` axis extends from the center of the surface towards the
        right-hand baseline when viewing the court in TV view. The default is
        ``0.0``

    y_trans : float
        The amount that the ``y`` coordinates are to be shifted. By convention,
        the +``y`` axis extends from the center of the surface towards the
        top of the court when viewing the court in TV view. The default is
        ``0.0``

    court_updates : dict
        A dictionary of updated parameters to use for the tennis court. The
        default is an empty dictionary

    color_updates : dict
        A dictionary of coloring parameters to pass to the plot. Defaults are
        provided in the class per each rule book, but this allows the plot to
        be more heavily customized/styled. The default is an empty dictionary

    units : str
        The units that the final plot should utilize. The default units are the
        units specified in the rule book of the league. The default is
        ``"default"``. The default is ``"default"``

    court_params : dict
        A dictionary containing the following parameters of the court:

            - court_length : float
                The length of the court in the court's specified units

            - singles_width : float
                The width of a singles court in the court's specified units

            - doubles_width : float
                The width of a doubles court in the court's specified units

            - serviceline_distance : float
                The distance from the net to the outer edge of the serviceline
                (the line in front of which a serve must land)

            - center_serviceline_length : float
                The length of the center serviceline

            - center_mark_length : float
                The distance that the center mark on the baseline protrudes
                forward from its anchor point at the back edge of the baseline

            - net_length : float
                The length of the net, from post to post, in the court's
                specified units

            - line_thickness : float
                The thickness of the lines of the court in the court's
                specified units

            - backstop_distance : float
                The distance from the back edge of the baseline to the barrier
                behind it in the court's specified units

            - sidestop_distance : float
                The distance from the outer edge of the sideline to the barrier
                that runs parallel to it in the court's specified units
    """

    def __init__(self, league_code = "", court_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a TennisCourt class.

        Parameters
        ----------
        league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "International
        Tennis Federation" should be either "ITF" or "itf"). The default is an
        empty string

        rotation : float
            The angle (in degrees) through which to rotate the final plot. The
            default is ``0.0``

        x_trans : float
            The amount that the ``x`` coordinates are to be shifted. By
            convention, the +``x`` axis extends from the center of the surface
            towards the right-hand baseline when viewing the court in TV view.
            The default is ``0.0``

        y_trans : float
            The amount that the ``y`` coordinates are to be shifted. By
            convention, the +``y`` axis extends from the center of the surface
            towards the top of the court when viewing the court in TV view. The
            default is ``0.0``

        court_updates : dict
            A dictionary of updated parameters to use to create the tennis
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
        self._load_preset_dimensions(sport = "tennis")

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
            "plot_background": "#395d3300",
            "baseline": "#ffffff",
            "singles_sideline": "#ffffff",
            "doubles_sideline": "#ffffff",
            "serviceline": "#ffffff",
            "center_serviceline": "#ffffff",
            "center_mark": "#ffffff",
            "ad_court": "#395d33",
            "deuce_court": "#395d33",
            "backcourt": "#395d33",
            "doubles_alley": "#395d33",
            "court_apron": "#395d33",
            "net": "#d3d3d3"
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
        # it's created by the tennis.court class)
        court_constraint_params = {
            "class": tennis_features.CourtConstraint,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "visible": False
        }
        self._initialize_feature(court_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the ad court
        ad_court_lower_params = {
            "class": tennis_features.FrontcourtHalf,
            "x_anchor": -self.court_params.get("serviceline_distance", 0.0),
            "y_anchor": -self.court_params.get("singles_width", 0.0) / 4.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "singles_width": self.court_params.get("singles_width", 0.0),
            "serviceline_distance": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["ad_court"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(ad_court_lower_params)

        ad_court_upper_params = {
            "class": tennis_features.FrontcourtHalf,
            "x_anchor": 0.0,
            "y_anchor": self.court_params.get("singles_width", 0.0) / 4.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "singles_width": self.court_params.get("singles_width", 0.0),
            "serviceline_distance": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["ad_court"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(ad_court_upper_params)

        # Initialize the deuce court
        deuce_court_lower_params = {
            "class": tennis_features.FrontcourtHalf,
            "x_anchor": -self.court_params.get("serviceline_distance", 0.0),
            "y_anchor": self.court_params.get("singles_width", 0.0) / 4.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "singles_width": self.court_params.get("singles_width", 0.0),
            "serviceline_distance": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["deuce_court"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(deuce_court_lower_params)

        deuce_court_upper_params = {
            "class": tennis_features.FrontcourtHalf,
            "x_anchor": 0.0,
            "y_anchor": -self.court_params.get("singles_width", 0.0) / 4.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "singles_width": self.court_params.get("singles_width", 0.0),
            "serviceline_distance": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["deuce_court"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(deuce_court_upper_params)

        # Initialize the backcourt
        backcourt_params = {
            "class": tennis_features.Backcourt,
            "x_anchor": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "singles_width": self.court_params.get("singles_width", 0.0),
            "serviceline_distance": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["backcourt"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(backcourt_params)

        # Initialize the doubles alley
        doubles_alley_params = {
            "class": tennis_features.DoublesAlley,
            "x_anchor": 0.0,
            "y_anchor": self.court_params.get("singles_width", 0.0) / 2.0,
            "reflect_x": False,
            "reflect_y": True,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": (
                self.court_params.get("doubles_width", 0.0) -
                self.court_params.get("singles_width", 0.0)
            ) / 2.0,
            "facecolor": self.feature_colors["doubles_alley"],
            "edgecolor": None,
            "zorder": 5
        }
        self._initialize_feature(doubles_alley_params)

        # Initialize the baselines
        baseline_params = {
            "class": tennis_features.Baseline,
            "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["baseline"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(baseline_params)

        # Initialize the singles sideline
        singles_sideline_params = {
            "class": tennis_features.Sideline,
            "x_anchor": 0.0,
            "y_anchor": self.court_params.get("singles_width", 0.0) / 2.0,
            "reflect_x": True,
            "reflect_y": True,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["singles_sideline"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(singles_sideline_params)

        # Initialize the doubles sideline
        doubles_sideline_params = {
            "class": tennis_features.Sideline,
            "x_anchor": 0.0,
            "y_anchor": self.court_params.get("doubles_width", 0.0) / 2.0,
            "reflect_x": True,
            "reflect_y": True,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "facecolor": self.feature_colors["doubles_sideline"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(doubles_sideline_params)

        # Initialize the serviceline
        serviceline_params = {
            "class": tennis_features.ServiceLine,
            "x_anchor": self.court_params.get("serviceline_distance", 0.0),
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "singles_width": self.court_params.get("singles_width", 0.0),
            "facecolor": self.feature_colors["serviceline"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(serviceline_params)

        # Initialize the center serviceline
        center_serviceline_params = {
            "class": tennis_features.CenterServiceline,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "center_serviceline_length": self.court_params.get(
                "serviceline_distance",
                0.0
            ),
            "facecolor": self.feature_colors["center_serviceline"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(center_serviceline_params)

        # Initialize the center mark
        center_mark_params = {
            "class": tennis_features.CenterMark,
            "x_anchor": self.court_params.get("court_length", 0.0) / 2.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "center_mark_length": self.court_params.get(
                "center_mark_length",
                0.0
            ),
            "facecolor": self.feature_colors["center_mark"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(center_mark_params)

        # Initialize the court apron
        court_apron_params = {
            "class": tennis_features.CourtApron,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": True,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "backstop_distance": self.court_params.get(
                "backstop_distance",
                0.0
            ),
            "is_constrained": False,
            "sidestop_distance": self.court_params.get(
                "sidestop_distance",
                0.0
            ),
            "facecolor": self.feature_colors["court_apron"],
            "edgecolor": None,
            "zorder": 15
        }
        self._initialize_feature(court_apron_params)

        # Initialize the net
        net_params = {
            "class": tennis_features.Net,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "court_length": self.court_params.get("court_length", 0.0),
            "court_width": self.court_params.get("doubles_width", 0.0),
            "is_constrained": False,
            "feature_thickness": self.court_params.get("line_thickness", 0.0),
            "net_length": self.court_params.get("net_length", 0.0),
            "facecolor": self.feature_colors["net"],
            "edgecolor": None,
            "zorder": 16
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
            An axes object onto which the plot can be drawn. If ``None`` is
            supplied, then the currently-active Axes object will be used

        display_range : str
            The portion of the surface to display. The entire surface
            will always be drawn under the hood, however this parameter
            limits what is shown in the final plot. The following explain what
            each display range corresponds to:

                - ``"full"``: The entire court
                - ``"serve"``: The serving half of the court
                - ``"serving"``: The serving half of the court
                - ``"servinghalf"``: The serving half of the court
                - ``"servicehalf"``: The serving half of the court
                - ``"serving_half"``: The serving half of the court
                - ``"service_half"``: The serving half of the court
                - ``"service half"``: The serving half of the court
                - ``"receive"``: The receiving half of the court
                - ``"receiving"``: The receiving half of the court
                - ``"receivinghalf"``: The receiving half of the court
                - ``"receiving_half"``: The receiving half of the court
                - ``"receiving half"``: The receiving half of the court

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
            float is provided, this will be used as the lower bound of
            the ``y`` coordinates to display and the upper bound will be the
            +``y`` upper touchline. If a tuple, the two values will be used
            to determine the bounds. If ``None``, then the display_range
            ``will`` be used instead to set the bounds. The default is ``None``

        rotation : float or None
            Angle (in degrees) through which to rotate the court when
            drawing. If used, this will set the class attribute of
            ``_rotation``. A value of ``0.0`` will correspond to a TV view of
            the court, where +``x`` is to the right and +``y`` is on top. The
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

                # Assuming the feature is visible (and is not the court
                # constraint), get the feature's x and y limits to ensure it
                # lies within the bounds of the court
                if visible and not isinstance(
                    feature,
                    tennis_features.CourtConstraint
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
            print("The following tennis leagues are available with "
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
            "plot_background": "#395d3300",
            "baseline": "#ffffff",
            "singles_sideline": "#ffffff",
            "doubles_sideline": "#ffffff",
            "serviceline": "#ffffff",
            "center_serviceline": "#ffffff",
            "center_mark": "#ffffff",
            "ad_court": "#395d33",
            "deuce_court": "#395d33",
            "backcourt": "#395d33",
            "doubles_alley": "#395d33",
            "court_apron": "#395d33",
            "net": "#d3d3d3"
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

                - court_length : float
                The length of the court in the court's specified units

            - singles_width : float
                The width of a singles court in the court's specified units

            - doubles_width : float
                The width of a doubles court in the court's specified units

            - serviceline_distance : float
                The distance from the net to the outer edge of the serviceline
                (the line in front of which a serve must land)

            - center_mark_length : float
                The distance that the center mark on the baseline protrudes
                forward from its anchor point at the back edge of the baseline

            - net_length : float
                The length of the net, from post to post, in the court's
                specified units

            - line_thickness : float
                The thickness of the lines of the court in the court's
                specified units

            - backstop_distance : float
                The distance from the back edge of the baseline to the barrier
                behind it in the court's specified units

            - sidestop_distance : float
                The distance from the outer edge of the sideline to the barrier
                that runs parallel to it in the court's specified units

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
            half_court_length = (
                (self.court_params.get("court_length", 0.0) / 2.0) +
                # Add in backstop distance since many shots are taken beyond
                # baseline
                (self.court_params.get("backstop_distance", 20.0))
            )

            half_court_width = (
                (self.court_params.get("doubles_width", 0.0) / 2.0) +
                # Add in sidestop distance since many shots are taken outside
                # of the doubles boundary but are still considered legal
                (self.court_params.get("sidestop_distance", 10.0))
            )

        # If it's for display (e.g. the draw() method), add in the necessary
        # thicknesses of external features (e.g. constraining features)
        if for_display:
            half_court_length = (
                (self.court_params.get("court_length", 0.0) / 2.0) +
                self.court_params.get("backstop_distance", 20.0) +
                5.0
            )

            half_court_width = (
                (self.court_params.get("doubles_width", 0.0) / 2.0) +
                self.court_params.get("sidestop_distance", 10.0) +
                5.0
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (-half_court_length, half_court_length),

                # Serving
                "serve": (-half_court_length, 1.5),
                "serving": (-half_court_length, 1.5),
                "servinghalf": (-half_court_length, 1.5),
                "servicehalf": (-half_court_length, 1.5),
                "serving_half": (-half_court_length, 1.5),
                "service_half": (-half_court_length, 1.5),
                "service half": (-half_court_length, 1.5),
                "serving half": (-half_court_length, 1.5),

                # Receiving
                "receive": (-1.5, half_court_length),
                "receiving": (-1.5, half_court_length),
                "receivinghalf": (-1.5, half_court_length),
                "receiving_half": (-1.5, half_court_length),
                "receiving half": (-1.5, half_court_length)
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
                "full": (-half_court_width, half_court_width),

                # Serving
                "serve": (-half_court_width, half_court_width),
                "serving": (-half_court_width, half_court_width),
                "servinghalf": (-half_court_width, half_court_width),
                "servicehalf": (-half_court_width, half_court_width),
                "serving_half": (-half_court_width, half_court_width),
                "service_half": (-half_court_width, half_court_width),
                "service half": (-half_court_width, half_court_width),
                "serving half": (-half_court_width, half_court_width),

                # Receiving
                "receive": (-half_court_width, half_court_width),
                "receiving": (-half_court_width, half_court_width),
                "receivinghalf": (-half_court_width, half_court_width),
                "receiving_half": (-half_court_width, half_court_width),
                "receiving half": (-half_court_width, half_court_width),
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


class ATPCourt(TennisCourt):
    """A subclass of ``TennisCourt`` specific to the ATP.

    See ``TennisCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the TennisCourt class with the relevant parameters
        super().__init__(
            league_code = "atp",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class ITACourt(TennisCourt):
    """A subclass of ``TennisCourt`` specific to the ITA.

    See ``TennisCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the TennisCourt class with the relevant parameters
        super().__init__(
            league_code = "ita",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class ITFCourt(TennisCourt):
    """A subclass of ``TennisCourt`` specific to the ITF.

    See ``TennisCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the TennisCourt class with the relevant parameters
        super().__init__(
            league_code = "itf",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class NCAACourt(TennisCourt):
    """A subclass of ``TennisCourt`` specific to the NCAA.

    See ``TennisCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the TennisCourt class with the relevant parameters
        super().__init__(
            league_code = "ncaa",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class USTACourt(TennisCourt):
    """A subclass of ``TennisCourt`` specific to the USTA.

    See ``TennisCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the TennisCourt class with the relevant parameters
        super().__init__(
            league_code = "usta",
            court_updates = court_updates,
            *args,
            **kwargs
        )


class WTACourt(TennisCourt):
    """A subclass of ``TennisCourt`` specific to the WTA.

    See ``TennisCourt`` class documentation for full description.
    """

    def __init__(self, court_updates = {}, *args, **kwargs):
        # Initialize the TennisCourt class with the relevant parameters
        super().__init__(
            league_code = "wta",
            court_updates = court_updates,
            *args,
            **kwargs
        )
