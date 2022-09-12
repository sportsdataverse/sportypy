"""Base class to plot any sports surface.

@author: Ross Drucker
"""
import json
import numpy as np
import importlib.resources
from abc import ABC, abstractmethod


class BaseSurface(ABC):
    """Abstract base class for plotting any sports surface.

    This class is not meant to be used directly, as it will be extended by each
    sport.

    Attributes
    ----------
    x_trans : float
        The amount by which to shift the surface from having its center be
        located at ``(0, 0)``. As an example, an NFL football field may set its
        ``x_trans`` value to be ``-60.0`` so that the line ``x = 0``
        corresponds to the inner edge of the back of the left endzone. The
        default is ``0.0``

    y_trans : float
        The amount by which to shift the surface from having its center be
        located at ``(0, 0)``. As an example, an NFL football field may set its
        ``y_trans`` value to be ``-26.333`` so that the line y = 0 corresponds
        to the inner edge of the back of the left endzone. The default is
        ``0.0``

    rulebook_unit : str
        The units provided in the rule book. These serve as the base unit for
        the plot, however this behavior may be overridden by a user supplying
        their own units. The default is ``"ft"``

    _rotation : float or None
        The angle through which the plot will be rotated. This should be passed
        in degrees, not radians. THe default is ``None``

    _feature_xlim : float or None
        The minimum or maximum ``x`` coordinate that should be allowed by the
        surface. This constrains all interior features to be contained by the
        surface. This is written to by each surface's ``draw()`` method. The
        default is ``None``

    _feature_ylim : float or None
        The minimum or maximum ``y`` coordinate that should be allowed by the
        surface. This constrains all interior features to be contained by the
        surface. This is written to by each surface's ``draw()`` method. The
        default is ``None``

    _features : list
        The instantiated feature objects that comprise the surface. These are
        the features that get plotted

    _surface_constraint : object or None
        A class object that constrains the plotting region to be inside of the
        playing surface. The default is ``None``

    _display_ranges : dict or None
        A dictionary that stores the display ranges that are available for a
        given surface's plot. The dictionary will have keys corresponding to
        the range to display (i.e. "full" being the full surface), and values
        that are themselves a dictionary of x limits, y limits, and a brief
        description of what each display range corresponds to. This will be
        created by the surface class' ``_get_display_ranges_dict()`` method.
        The default is ``None``
    """

    def __init__(self):
        # Initialize the values needed to shift the surface from having its
        # center at (0, 0)
        self.x_trans = 0.0
        self.y_trans = 0.0

        # Initialize the angle through which the final plot will be rotated. A
        # value of 0 will correspond to "TV View," or how the surface would
        # ordinarily look if watching the sport on TV. Usually, this results in
        # a surface that is wider than it is tall
        self._rotation = None

        # Initialize the display limits of the final plot. These will be
        # written to by the set_plot_display_range() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize an empty list to contain a surface's features. This list
        # will be appended to by the _initialize_feature() method below
        self._features = []

        # Initialize a constraint on the surface. For example, don't allow any
        # plots or features to extend beyond the boards in a hockey rink
        self._surface_constraint = None

        # Initialize a possible set of display ranges for the plot. This will
        # be set by each surface's _get_display_range_dict() method
        self._display_ranges = None

        # Initialize the unit conversions
        self._load_unit_conversions()

    @staticmethod
    def copy_(param):
        """Copy what's passed in (if possible).

        Most of the plotting functions require an iterable object to be passed
        in as coordinates. This allows for an iterable array to be copied while
        also handling the case where a single point may be passed to it.

        Parameters
        ----------
        param : iterable
            Any iterable that should be copied. Ususally, these are pandas data
            frames. However, if a float or int is passed in, this will also
            work

        Returns
        -------
        param : iterable or float or int
            The copied array, or the passed-in float or int
        """
        try:
            param = param.copy()

        except AttributeError:
            pass

        return param

    def _initialize_feature(self, params):
        """Initialize a feature on the surface at its required coordinates.

        Each feature is parameterized in its own class method, but is
        instantiated by this method in the surface's ``__init__()`` method.
        This method appends the instance of the feature to the surface class'
        ``_features`` attribute

        Parameters
        ----------
        params : dict
            The required parameters for instantiation of a feature, as well as
            for formatting in the resulting plots

        Returns
        -------
        Nothing, but it does instantiate a feature and append it to the
        surface class' ``_features`` attribute
        """
        # Get the feature's class. This will be instantiated later, but removed
        # from the feature's parameter dictionary now
        feature_class = params.pop("class")

        # Get the coordinates of the feature's center in the final plot. If
        # none exist, set the default to be 0. These will be numpy ndarrays
        center_of_feature_x = np.ravel(params.get("x_anchor", [0]))
        center_of_feature_y = np.ravel(params.get("y_anchor", [0]))

        # Determine whether or not to reflect the x and y coordinates over the
        # respective axes
        if params.pop("reflect_x", False):
            x_reflections = [False, True]

        else:
            x_reflections = [False]

        if params.pop("reflect_y", False):
            y_reflections = [False, True]

        else:
            y_reflections = [False]

        # Iterate over the x and y centers of the features
        for x in center_of_feature_x:
            for y in center_of_feature_y:
                for x_reflection in x_reflections:
                    for y_reflection in y_reflections:
                        # Copy the feature's parameters as a dictionary. This
                        # is the dictionary that will be used to instantiate
                        # the feature
                        feature_params = dict(params)

                        # If necessary, reflect the feature over the
                        # appropriate axes
                        if x_reflection:
                            feature_params["x_anchor"] = -1 * x
                        else:
                            feature_params["x_anchor"] = x

                        if y_reflection:
                            feature_params["y_anchor"] = -1 * y
                        else:
                            feature_params["y_anchor"] = y

                        # Add the relevant information to the feature's class
                        # construction dictionary. This will be used by the
                        # feature's instantiation methods
                        feature_params["reflect_x"] = x_reflection
                        feature_params["reflect_y"] = y_reflection

                        # Instantiate the feature and append it to the
                        # surface's self._features attribute
                        self._features.append(feature_class(**feature_params))

    def _add_surface_constraint(self, ax, transform = None):
        """Constrains features from extending beyond surface boundaries.

        Parameters
        ----------
        ax : matplotlib.Axes
            Axes in which to add the constraint. This will contain the surface
            plot

        transform: matplotlib.Transform, optional
            Transform to apply to the constraint

        Returns
        -------
        matplotlib Polygon
        """
        # Set the transform (if applicable) to the surface
        if transform:
            transform = transform
        else:
            transform = ax.transData  # pragma: no cover

        # Set the constraining polygon
        constraint = self._surface_constraint.create_feature_mpl_polygon()
        constraint.set_transform(transform)

        # Add the constraint to the Axes object
        ax.add_patch(constraint)

        # Return the constraint's polygon
        return constraint

    def _get_transform(self, ax):
        """Get a matplotlib.Transform to apply to the features of the surface.

        Rather than having to rotate every point, it's much more
        straightforward to rotate the final plot. This transformation goes
        between the data's units and the graphic device's units

        Parameters
        ----------
        ax : matplotlib.Axes
            The axes onto which the transform should be applied

        transform : matplotlib.Transform or None
            The ``matplotlib.Transform to apply``. The default is ``None``

        Returns
        -------
        transform : matplotlib.Transform
            The applied transformation
        """
        # Determine the transform to use
        transform = self._rotation + ax.transData

        return transform

    def _rotate_xy(self, x, y):
        """Rotate the ``x`` and ``y`` coordinates with surface rotation.

        Parameters
        ----------
        x : float
            The ``x`` coordinate(s)

        y : float
            The ``y`` coordinate(s)

        Returns
        -------
        The rotated ``x`` and ``y`` coordinates
        """
        if self._rotation:
            xy = self._rotation.transform(tuple(zip(x, y)))
            x, y = xy[:, 0], xy[:, 1]
        return x, y

    def convert_xy(self, x, y):
        """Reposition and scale the ``x`` and ``y`` coordinates.

        The ``x`` and ``y`` coordinates must be moved to the proper position
        and rescaled to the size used for the final surface plot.

        Parameters
        ----------
        x : float
            The ``x`` coordinate(s)

        y : float
            The ``y`` coordinate(s)

        Returns
        -------
        x : float
            The ``x`` coordinate(s) adjusted to the proper position and scale

        y : float
            The ``y`` coordinate(s) adjusted to the proper position and scale
        """
        # Copy the features' x and y coordinates so as not to overwrite them
        x = self.copy_(x)
        y = self.copy_(y)

        # Flatten and shift them according to how the final plot should be
        # rendered
        x = np.ravel(x) - self.x_trans
        y = np.ravel(y) - self.y_trans

        # If the surface's plot needs to be rotated, perform the rotation
        return self._rotate_xy(x, y)

    @abstractmethod
    def _get_plot_range_limits(self):
        """Set the displayable range of the resulting plot.

        This is an abstract method that sets the displayable range of the
        resulting plot. This method is created individually for each sport in
        its respective surface class

        Returns
        -------
        xlim : tuple of ints or tuple of floats
            The lower and upper limits on the ``x`` display range

        ylim : tuple of ints or tuple of floats
            The lower and upper limits on the ``y`` display range
        """
        pass

    def set_plot_display_range(self, ax = None, display_range = "full",
                               xlim = None, ylim = None, for_plot = False,
                               for_display = True):
        """Set the ``x`` and ``y`` limits for the plot.

        Parameters
        ----------
        ax : matplotlib.Axes or None
            The Axes object onto which ``xlim`` and ``ylim`` will be set. The
            default is ``None``

        display_range : str
            The portion of the surface to display. The entire surface is
            drawn regardless, however this reduces the displayed range to be
            what is desired. This is passed to each surface's
            ``_get_plot_range_limits()`` method to determine the ``xlim`` and
            ``ylim`` to be shown. If an invalid value is passed to this method,
            the full surface will be shown by default. The default is
            ``"full"``

        xlim : float or tuple of floats or None
            If a single float is passed, this will be the lower bound of ``x``
            to display. If a tuple is passed, it will be the lower and upper
            bounds of ``x`` to display. If ``None``, then the value will be set
            by the surface's ``_get_plot_range_limits()`` method. The default
            is ``None``

        ylim : float or tuple of floats or None
            If a single float is passed, this will be the lower bound of ``y``
            to display. If a tuple is passed, it will be the lower and upper
            bounds of ``y`` to display. If ``None``, then the value will be set
            by the surface's ``_get_plot_range_limits()`` method. The default
            is ``None``

        Returns
        -------
        ax : matplotlib.Axes
            A matplotlib Axes object with the surface drawn on it
        """
        # Set the display limits
        xlim, ylim = self._get_plot_range_limits(
            display_range,
            xlim,
            ylim,
            for_plot = for_plot,
            for_display = for_display
        )

        # Get the constraining feature's polygon's x and y coordinates
        constraint_df = self._surface_constraint._get_centered_feature()
        mask = (constraint_df["x"] >= xlim[0]) & \
               (constraint_df["x"] <= xlim[1]) & \
               (constraint_df["y"] >= ylim[0]) & \
               (constraint_df["y"] <= ylim[1])

        x = np.concatenate((constraint_df["x"][mask], xlim, xlim))
        y = np.concatenate((constraint_df["y"][mask], ylim, ylim[::-1]))

        # If the full display range is desired, set the x and y limit
        # attributes
        if display_range == "full":
            if self._feature_xlim:
                x = np.concatenate((x, self._feature_xlim))
            if self._feature_ylim:
                y = np.concatenate((y, self._feature_ylim))

        # Shift the x and y limits so that convert_xy can undo the shift
        # correctly
        xs, ys = self.convert_xy(x + self.x_trans, y + self.y_trans)

        # Set the x and y limits of the plot. User-supplied x and y limits will
        # take precedence over the display_range parameter
        ax.set_xlim(np.min(xs), np.max(xs))
        ax.set_ylim(np.min(ys), np.max(ys))

        return ax

    def _load_unit_conversions(self):
        """Load in the unit-conversions file.

        A user's desired units may not always be what is defined in the rule
        book, and having pre-defined unit conversions (with feet as the base)
        allows this conversion to occur for any surface
        """
        # Load in the units that are convertable
        with importlib.resources.open_text(
            "sportypy.data", "unit_conversions.json"
        ) as f:
            self.unit_conversions = json.load(f)

    def _load_preset_dimensions(self, sport):
        """Load in pre-defined dimensions for various leagues of a sport.

        Several leagues come published with this package, and this function
        serves to load in the dimensions specific to these leagues.

        Parameters
        ----------
        sport : str
            The name of the sport whose leagues are to be loaded

        Returns
        -------
        Nothing, but sets the league_dimensions attribute of the class that can
        be called in the child classes to set league-defined parameters
        """
        # Load the pre-defined dimensions from the JSON file
        with importlib.resources.open_text(
                "sportypy.data", "surface_dimensions.json"
        ) as f:
            dimensions = json.load(f)

        # Retain only leagues in the desired sport
        self.league_dimensions = dimensions[sport.lower()]

    def _convert_units(self, value, start_unit, desired_unit):
        """Convert the units of the surface as required by the user.

        Units of the surface for pre-defined leagues are provided in the
        surface_dimensions.json file of the module. Should a user want to
        create the plot with different units to more easily align with the data
        they wish to display, this method allows for the units to be easily
        converted. This should NOT change the visual display of the plot, but
        instead just change the underlying coordinate system

        Parameters
        ----------
        value : float
            The value whose units are to be converted. These correspond to
            parameters of the surface

        start_unit : str
            The units that the parameterization is originally given in

        desired_unit : str
            The units that the parameterization should be converted to

        Returns
        -------
        value : float
            The parameter given in the desired unit
        """
        if type(value) == bool:
            return value

        try:
            value /= self.unit_conversions[start_unit]
            value *= self.unit_conversions[desired_unit]

        except TypeError:
            pass

        except KeyError:
            print(f"{desired_unit} is not currently a supported unit")

        return value
