"""Extension of the ``BaseSurfacePlot`` class to create a curling sheet.

This is a second-level child class of the ``BaseSurface`` class, and as such
will have access to its attributes and methods. ``sportypy`` will ship with
pre-defined leagues that will have their own subclass, but a user can manually
specify their own sheet parameters to create a totally-customized sheet. The
sheet's features are parameterized by the basic dimensions of the sheet, which
comprise the attributes of the class.

@author: Ross Drucker
"""
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.curling as curling_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class CurlingSheet(BaseSurfacePlot):
    """A subclass of ``BaseSurfacePlot`` to make a generic curling sheet.

    This allows for the creation of the curling sheet in a way that is entirely
    parameterized by the sheet's baseline characteristics.

    All attributes should default to ``0.0`` (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid curling sheet. The attributes needed to instantiate a particular
    league's surface must be specified in the ``sheet_params`` dictionary. For
    many leagues, these will be provided in the surface_dimensions.json file in
    the data/ subdirectory of ``sportypy``.

    See the ``BaseSurfacePlot`` and ``BaseSurface`` class definitions for full
    details.

    Attributes
    ----------
    league_code : str
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "World Curling
        Federation" should be either "WCF" or "wcf"). The default
        is an empty string

    rotation_amt : float
        The angle (in degrees) through which to rotate the final plot. The
        default is ``0.0``

    x_trans : float
        The amount that the ``x`` coordinates are to be shifted. By convention,
        the +``x`` axis extends from the center of the surface towards the
        right-hand side wall when viewing the sheet in TV view. The default is
        ``0.0``

    y_trans : float
        The amount that the ``y`` coordinates are to be shifted. By convention,
        the +``y`` axis extends from the center of the surface towards the
        top house when viewing the sheet in TV view. The default is
        ``0.0``

    feature_colors : dict
        A dictionary of coloring parameters to pass to the plot

    sheet_params : dict
        A dictionary containing the following parameters of the sheet:

            - sheet_length : float
                The full length of the sheet. Length is defined as the distance
                between the inner edge of the boards behind each house

            - sheet_width : float
                The full width of the sheet. Width is defined as the distance
                between the inner edge of the side walls

            - sheet_units : str
                The units with which to draw the sheet

            - apron_behind_back : float
                The dimension of the sheet's apron behind the back board. In TV
                view, this is in the ``y`` direction

            - apron_along_side : float
                The dimension of the sheet's apron beyond the side wall. In TV
                view, this is in the +``x`` direction

            - tee_line_to_center : float
                The distance from the center of the shet to the center of the
                tee line

            - tee_line_thickness : float
                The thickness of the tee line. This is the line that runs
                through the center of the house, from side wall to side wall

            - back_line_thickness : float
                The thickness of the back line. This is the line between the
                house and the hack

            - back_line_to_tee_line : float
                The distance from the center of the tee line to the outside
                edge of the back line (which runs between the house and the
                hack)

            - hack_line_thickness : float
                The thickness of the hack line

            - hack_foothold_width : float
                The width of a foothold of the hack. In TV view, this is the
                dimension of the foothold in the ``x`` direction (parallel to
                the tee line)

            - hack_foothold_gap : float
                The interior separation between the two footholds in the hack

            - hack_foothold_depth : float
                The distance from the house-side to the back wall side of the
                foothold of the hack. The back of the foothold will lie along
                the hack line

            - hog_line_to_tee_line : float
                The distance from the inside edge of the hog line (the edge
                nearest the house) to the tee line

            - hog_line_thickness : float
                The thickness of the hog line

            - centre_line_extension : float
                The distance beyond the center of the tee line that the centre
                line extends towards the back wall

            - centre_line_thickness : float
                The thickness of the centre line

            - house_ring_radii : list of floats
                The radii of the house rings. These will be reordered to be
                descending by default. This should NOT include the button, as
                this will be handled separately

            - button_radius : float
                The radius of the button (the center ring of the house)

            - courtesy_line_thickness : float
                The thickness of the courtesy lines. These are the lines
                marking where players on the non-throwing team should stand
                while awaiting their next throw. This dimension should be in
                the ``y`` direction when viewing the sheet in TV view

            - courtesy_line_length : float
                The distance outward from the inner edge of the side wall that
                the courtesy line extends towards the center of the sheet

            - courtesy_line_to_hog_line : float
                The distance between the outer edges of the hog line and the
                courtesy line
    """

    def __init__(self, league_code = "", sheet_updates = {},
                 color_updates = {}, rotation = 0.0, x_trans = 0.0,
                 y_trans = 0.0, units = "default", **added_features):
        """Initialize an instance of a ``CurlingSheet`` class.

        Parameters
        ----------
        league_code : str
            The league for which the plot should be drawn. This is
            case-insensitive but should be the shortened name of the league
            (e.g. "World Curling Federation" should be either "WCF" or
            "wcf"). The default is an empty string

        rotation : float
            The angle (in degrees) through which to rotate the final plot. The
            default is ``0.0``

        x_trans : float
            The amount that the ``x`` coordinates are to be shifted. By
            convention, the +``x`` axis extends from the center of the surface
            towards the right-hand side wall when viewing the sheet in TV view.
            The default is ``0.0``

        y_trans : float
            The amount that the ``y`` coordinates are to be shifted. By
            convention, the +``y`` axis extends from the center of the surface
            towards the top house when viewing the sheet in TV view. The
            default is ``0.0``

        sheet_updates : dict
            A dictionary of updated parameters to use to create the curling
            sheet. The default is an empty dictionary

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
        # Load all pre-defined sheet dimensions for provided leagues
        self._load_preset_dimensions(sport = "curling")

        # Load all unit conversions
        self._load_unit_conversions()

        # Set the league to be the lower-case version of the supplied value
        self.league_code = league_code.lower()

        # Try to get the league specified from the pre-defined set of leagues
        try:
            sheet_dimensions = self.league_dimensions[self.league_code]

        # If it can't be found, set the sheet_dimensions dictionary to be empty
        except KeyError:
            sheet_dimensions = {}

        # Combine the sheet dimensions (if found from in the pre-defined
        # leagues) with any parameter updates supplied by the user. This will
        # comprise the parameter set with which the sheet is to be drawn
        sheet_params = {
            **sheet_dimensions,
            **sheet_updates
        }

        # Set the passed parameters of the sheet to be the class' sheet_params
        # attribute
        self.sheet_params = sheet_params

        # Convert the sheet's units if needed
        if units.lower() != "default":
            for k, v in sheet_params.items():
                self.sheet_params[k] = self._convert_units(
                    v,
                    self.sheet_params["sheet_units"],
                    units.lower()
                )

            self.sheet_params["sheet_units"] = units.lower()

        # Set the rotation of the plot to be the supplied rotation value
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the sheet's necessary shifts. This will overwrite the default
        # values of x_trans and y_trans inherited from the BaseSurfacePlot
        # class (which is in turn inherited from BaseSurface)
        self.x_trans, self.y_trans = x_trans, y_trans

        # Create a container for the relevant features of an ice sheet
        self._features = []

        # Initialize the x and y limits for the plot be None. These will get
        # set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the default colors of the sheet
        default_colors = {
            "plot_background": "#ffffff00",
            "end_1": "#ffffff",
            "centre_zone": "#ffffff",
            "end_2": "#ffffff",
            "sheet_apron": "#0033a0",
            "centre_line": "#000000",
            "tee_line": "#000000",
            "back_line": "#000000",
            "hog_line": "#c8102e",
            "hack_line": "#000000",
            "courtesy_line": "#000000",
            "hack": "#000000",
            "button": "#ffffff",
            "house_rings": ["#c8102e", "#ffffff", "#0033a0"]
        }

        # Combine the colors with a passed colors dictionary
        if not color_updates:
            color_updates = {}

        # Create the final color set for the features of the sheet
        self.feature_colors = {
            **default_colors,
            **color_updates
        }

        # Initialize the constraint on the sheet to confine all features to be
        # contained within the surface. The feature itself is not visible (as
        # it's created by the curling.SheetApron class)
        sheet_constraint_params = {
            "class": curling_features.Boundary,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "visible": False
        }
        self._initialize_feature(sheet_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the lower end
        end_1_params = {
            "class": curling_features.End,
            "x_anchor": 0.0,
            "y_anchor": (
                (-self.sheet_params.get("tee_line_to_center", 0.0)) +
                self.sheet_params.get("hog_line_to_tee_line", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "drawn_direction": "downward",
            "tee_line_to_center": self.sheet_params.get(
                "tee_line_to_center",
                0.0
            ),
            "hog_line_to_tee_line": self.sheet_params.get(
                "hog_line_to_tee_line",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["end_1"],
            "edgecolor": self.feature_colors["end_1"],
            "zorder": 5
        }
        self._initialize_feature(end_1_params)

        # Initialize the upper end
        end_2_params = {
            "class": curling_features.End,
            "x_anchor": 0.0,
            "y_anchor": (
                (self.sheet_params.get("tee_line_to_center", 0.0)) -
                self.sheet_params.get("hog_line_to_tee_line", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "tee_line_to_center": self.sheet_params.get(
                "tee_line_to_center",
                0.0
            ),
            "hog_line_to_tee_line": self.sheet_params.get(
                "hog_line_to_tee_line",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["end_2"],
            "edgecolor": self.feature_colors["end_2"],
            "zorder": 6
        }
        self._initialize_feature(end_2_params)

        # Initialize the centre zone
        centre_zone_params = {
            "class": curling_features.CentreZone,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "tee_line_to_center": self.sheet_params.get(
                "tee_line_to_center",
                0.0
            ),
            "hog_line_to_tee_line": self.sheet_params.get(
                "hog_line_to_tee_line",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["centre_zone"],
            "edgecolor": self.feature_colors["centre_zone"],
            "zorder": 5
        }
        self._initialize_feature(centre_zone_params)

        # Initialize the hog line
        hog_line_params = {
            "class": curling_features.HogLine,
            "x_anchor": 0.0,
            "y_anchor": (
                self.sheet_params.get("tee_line_to_center", 0.0) -
                self.sheet_params.get("hog_line_to_tee_line", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_thickness": self.sheet_params.get(
                "hog_line_thickness",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["hog_line"],
            "edgecolor": self.feature_colors["hog_line"],
            "zorder": 16
        }
        self._initialize_feature(hog_line_params)

        # Initialize the hack line
        hack_line_params = {
            "class": curling_features.HackLine,
            "x_anchor": 0.0,
            "y_anchor": (
                self.sheet_params.get("tee_line_to_center", 0.0) +
                self.sheet_params.get("centre_line_extension", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_thickness": self.sheet_params.get(
                "hack_line_thickness",
                0.0
            ),
            "hack_width": (
                (2.0 * self.sheet_params.get("hack_foothold_width", 0.0)) +
                self.sheet_params.get("hack_foothold_gap", 0.0)
            ),
            "visible": True,
            "facecolor": self.feature_colors["hack_line"],
            "edgecolor": self.feature_colors["hack_line"],
            "zorder": 16
        }
        self._initialize_feature(hack_line_params)

        # Initialize the courtesy lines
        courtesy_line_params = {
            "class": curling_features.CourtesyLine,
            "x_anchor": self.sheet_params.get("sheet_width", 0.0) / 2.0,
            "y_anchor": (
                self.sheet_params.get("tee_line_to_center", 0.0) -
                self.sheet_params.get("hog_line_to_tee_line", 0.0) -
                self.sheet_params.get("courtesy_line_to_hog_line", 0.0)
            ),
            "reflect_x": True,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_thickness": self.sheet_params.get(
                "courtesy_line_thickness",
                0.0
            ),
            "courtesy_line_length": self.sheet_params.get(
                "courtesy_line_length",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["courtesy_line"],
            "edgecolor": self.feature_colors["courtesy_line"],
            "zorder": 16
        }
        self._initialize_feature(courtesy_line_params)

        # Initialize the hack line
        hack_params = {
            "class": curling_features.HackFoothold,
            "x_anchor": self.sheet_params.get("hack_foothold_gap", 0.0),
            "y_anchor": (
                self.sheet_params.get("tee_line_to_center", 0.0) +
                self.sheet_params.get("centre_line_extension", 0.0)
            ),
            "reflect_x": True,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "foothold_depth": self.sheet_params.get(
                "hack_foothold_depth",
                0.0
            ),
            "foothold_width": self.sheet_params.get(
                "hack_foothold_width",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["hack"],
            "edgecolor": self.feature_colors["hack"],
            "zorder": 17
        }
        self._initialize_feature(hack_params)

        # Initialize the house rings

        # First, they need to be ordered from largest radius to smallest
        house_ring_radii = self.sheet_params.get("house_ring_radii", [0.0])
        house_ring_radii.sort(reverse = True)

        # Iterate over the number of rings
        for i, radius in enumerate(house_ring_radii):
            house_ring_params = {
                "class": curling_features.HouseRing,
                "x_anchor": 0.0,
                "y_anchor": self.sheet_params.get("tee_line_to_center", 0.0),
                "reflect_x": False,
                "reflect_y": True,
                "feature_units": self.sheet_params.get("sheet_units", "ft"),
                "sheet_length": self.sheet_params.get("sheet_length", 0.0),
                "sheet_width": self.sheet_params.get("sheet_width", 0.0),
                "feature_radius": radius,
                "visible": True,
                "facecolor": self.feature_colors["house_rings"][i],
                "edgecolor": self.feature_colors["house_rings"][i],
                "zorder": 16
            }
            self._initialize_feature(house_ring_params)

        # Initialize the button
        button_params = {
            "class": curling_features.Button,
            "x_anchor": 0.0,
            "y_anchor": self.sheet_params.get("tee_line_to_center", 0.0),
            "reflect_x": False,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_radius": self.sheet_params.get("button_radius", 0.0),
            "visible": True,
            "facecolor": self.feature_colors["button"],
            "edgecolor": self.feature_colors["button"],
            "zorder": 16
        }
        self._initialize_feature(button_params)

        # Initialize the centre line
        centre_line_params = {
            "class": curling_features.CentreLine,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": False,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_thickness": self.sheet_params.get(
                "centre_line_thickness",
                0.0
            ),
            "tee_line_to_center": self.sheet_params.get(
                "tee_line_to_center",
                0.0
            ),
            "centre_line_extension": self.sheet_params.get(
                "centre_line_extension",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["centre_line"],
            "edgecolor": self.feature_colors["centre_line"],
            "zorder": 17
        }
        self._initialize_feature(centre_line_params)

        # Initialize the tee line
        tee_line_params = {
            "class": curling_features.TeeLine,
            "x_anchor": 0.0,
            "y_anchor": self.sheet_params.get("tee_line_to_center", 0.0),
            "reflect_x": False,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_thickness": self.sheet_params.get(
                "tee_line_thickness",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["tee_line"],
            "edgecolor": self.feature_colors["tee_line"],
            "zorder": 17
        }
        self._initialize_feature(tee_line_params)

        # Initialize the back line
        back_line_params = {
            "class": curling_features.BackLine,
            "x_anchor": 0.0,
            "y_anchor": (
                self.sheet_params.get("tee_line_to_center", 0.0) +
                self.sheet_params.get("back_line_to_tee_line", 0.0)
            ),
            "reflect_x": False,
            "reflect_y": True,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "feature_thickness": self.sheet_params.get(
                "back_line_thickness",
                0.0
            ),
            "visible": True,
            "facecolor": self.feature_colors["tee_line"],
            "edgecolor": self.feature_colors["tee_line"],
            "zorder": 17
        }
        self._initialize_feature(back_line_params)

        # Initialize the sheet apron
        sheet_apron_params = {
            "class": curling_features.SheetApron,
            "x_anchor": 0.0,
            "y_anchor": 0.0,
            "reflect_x": False,
            "reflect_y": True,
            "is_constrained": False,
            "feature_units": self.sheet_params.get("sheet_units", "ft"),
            "sheet_length": self.sheet_params.get("sheet_length", 0.0),
            "sheet_width": self.sheet_params.get("sheet_width", 0.0),
            "apron_behind_back": self.sheet_params.get(
                "apron_behind_back",
                0.0
            ),
            "apron_along_side": self.sheet_params.get("apron_along_side", 0.0),
            "visible": True,
            "facecolor": self.feature_colors["sheet_apron"],
            "edgecolor": self.feature_colors["sheet_apron"],
            "zorder": 20
        }
        self._initialize_feature(sheet_apron_params)

        # Initialize all other features passed as keyword arguments
        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = "full", xlim = None, ylim = None,
             rotation = None):
        """Draw the sheet.

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
                - ``"house"``: The top house on the surface when viewing the
                    sheet in TV view

            The default is ``"full"``

        xlim : float or tuple of floats or None
            The display range in the ``x`` direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the ``x`` coordinates to display and the upper bound will be the
            +``x`` end of the sheet. If a tuple, the two values will be
            used to determine the bounds. If ``None``, then the
            ``display_range`` will be used instead to set the bounds. The
            default is ``None``

        ylim : float or tuple of floats or None
            The display range in the ``y`` direction to be used. If a single
            float is provided, this will be used as the lower bound of the y
            coordinates to display and the upper bound will be the +``y`` side
            of the sheet. If a tuple, the two values will be used to determine
            the bounds. If ``None``, then the ``display_range`` will be used
            instead to set the bounds.  The default is ``None``

        rotation : float or None
            Angle (in degrees) through which to rotate the sheet when drawing.
            If used, this will set the class attribute of ``_rotation``. A
            value of ``0.0`` will correspond to a TV view of the sheet, where
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

                # Assuming the feature is visible (and is not the boundary),
                # get the feature's x and y limits to ensure it lies within the
                # bounds of the sheet
                if visible and not isinstance(
                    feature,
                    curling_features.Boundary
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
            print("The following curling leagues are available with "
                  "sportypy:\n")

            # Print the current leagues
            for league_code in available_league_codes:
                print(f"- {league_code.upper()}")

    def cani_color_features(self):
        """Determine what features of the sheet can be colored.

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
        """Determine what features of the sheet can be re-parameterized.

        This function is a helper function for the user to aid in customizing
        a sheet's parameters. The printed result of this method will be the
        names of the features that are able to be reparameterized. This method
        is also useful when defining new features and using an existing
        league's sheet dimensions as a starting point

        Returns
        -------
        Nothing, but a message will be printed out
        """
        # Preamble
        print("The following features can be reparameterized via the "
              "sheet_updates parameter, with the current value in "
              "parenthesis:\n")

        # Print the current values of the colors
        for k, v in self.sheet_params.items():
            print(f"- {k} ({v})")

        # Footer
        print("\nThese parameters may be updated with the "
              "update_sheet_params() method")

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
            sheet_updates = self.sheet_params,
            color_updates = updated_colors
        )

    def update_sheet_params(self, sheet_param_updates = {}, *args, **kwargs):
        """Update the sheet's defining parameters.

        This method should primarily be used in cases when plotting a league
        not currently supported by ``sportypy``

        Parameters
        ----------
        sheet_updates : dict
            A dictionary where the keys correspond to the name of the parameter
            of the sheet that is to be updated (see
            ``cani_change_dimensions()`` method for a list of these
            parameters). The default is an empty dictionary

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated parameters
        """
        # Start by getting the currently-used sheet parameters
        current_sheet_params = self.sheet_params

        # Create a new dictionary to hold the updated parameters via dictionary
        # comprehension
        updated_sheet_params = {
            **current_sheet_params,
            **sheet_param_updates
        }

        # Re-instantiate the class with the new parameters
        self.__init__(
            sheet_updates = updated_sheet_params,
            color_updates = self.feature_colors
        )

    def reset_colors(self):
        """Reset the features of the sheet to their default color set.

        The colors can be passed at the initial instantiation of the class via
        the ``color_updates`` parameter, and through the ``update_colors()``
        method, these can be changed. This method allows the colors to be reset
        to their default values after experiencing such a change
        """
        # Re-instantiate the class with the default colors
        default_colors = {
            "plot_background": "#ffffff00",
            "end_1": "#ffffff",
            "centre_zone": "#ffffff",
            "end_2": "#ffffff",
            "sheet_apron": "#0033a0",
            "centre_line": "#000000",
            "tee_line": "#000000",
            "back_line": "#000000",
            "hog_line": "#c8102e",
            "hack_line": "#000000",
            "courtesy_line": "#000000",
            "hack": "#000000",
            "button": "#ffffff",
            "house_rings": ["#c8102e", "#ffffff", "#0033a0"]
        }

        self.__init__(
            sheet_updates = self.sheet_params,
            color_updates = default_colors
        )

    def reset_sheet_params(self):
        """Reset the features of the sheet to their default parameterizations.

        The sheet parameters can be passed at the initial instantiation of the
        class via the ``sheet_updates`` parameter, and through the
        ``update_sheet_params()`` method, these can be changed. This method
        allows the feature parameterization to be reset to their default values
        after experiencing such a change
        """
        # Re-instantiate the class with the default parameters
        default_params = self.league_dimensions[self.league_code]

        self.__init__(
            sheet_updates = default_params,
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
                - ``"house"``: The top house on the surface when viewing the
                    sheet in TV view

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
            half_sheet_length = self.sheet_params.get(
                "sheet_length",
                0.0
            ) / 2.0
            half_sheet_width = self.sheet_params.get("sheet_width", 0.0) / 2.0
            end_length = (
                self.sheet_params.get("tee_line_to_center", 0.0) -
                self.sheet_params.get("hog_line_to_tee_line", 0.0) -
                self.sheet_params.get("courtesy_line_to_hog_line", 0.0)
            )

        # If it's for display (e.g. the draw() method), add in the necessary
        # thicknesses of external features (e.g. sheet apron)
        if for_display:
            half_sheet_length = (
                (self.sheet_params.get("sheet_length", 0.0) / 2.0) +
                self.sheet_params.get("apron_behind_back", 0.0) +
                5.0
            )
            half_sheet_width = (
                (self.sheet_params.get("sheet_width", 0.0) / 2.0) +
                self.sheet_params.get("apron_along_side", 0.0) +
                5.0
            )
            end_length = (
                self.sheet_params.get("tee_line_to_center", 0.0) -
                self.sheet_params.get("hog_line_to_tee_line", 0.0) -
                self.sheet_params.get("courtesy_line_to_hog_line", 0.0) -
                5.0
            )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                "full": (-half_sheet_width, half_sheet_width),

                # House
                "house": (-half_sheet_width, half_sheet_width)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # sheet
            xlim = xlims.get(
                display_range,
                (-half_sheet_width, half_sheet_width)
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

                # If the provided value for the x limit is beyond the side of
                # the sheet, display the entire sheet
                if xlim >= half_sheet_width:
                    xlim = -half_sheet_width

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_sheet_width)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the sheet. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(" ", "")

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                "full": (-(half_sheet_length), half_sheet_length),

                # House
                "house": (end_length, half_sheet_length)
            }

            # Extract the y limit from the dictionary, defaulting to the full
            # sheet
            ylim = ylims.get(
                display_range,
                (-half_sheet_length, half_sheet_length)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= half_sheet_length:
                    ylim = -half_sheet_length

                ylim = (ylim, half_sheet_length)

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

        # Constrain the limits from going beyond the end of the sheet (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_sheet_width),
            min(xlim[1], half_sheet_width)
        )

        ylim = (
            max(ylim[0], -half_sheet_length),
            min(ylim[1], half_sheet_length)
        )

        return xlim, ylim


class WCFSheet(CurlingSheet):
    """A subclass of ``CurlingSheet`` specific to the WCF.

    See ``CurlingSheet`` class documentation for full description.
    """

    def __init__(self, sheet_updates = {}, *args, **kwargs):
        # Initialize the CurlingSheet class with the relevant parameters
        super().__init__(
            league_code = "wcf",
            sheet_updates = sheet_updates,
            *args,
            **kwargs
        )
