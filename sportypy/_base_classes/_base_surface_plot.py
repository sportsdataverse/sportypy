"""Base surface plot class to extend scipy to sportypy.

The ``BaseSurfacePlot`` class is an extension of the BaseSurface class that
enables a user to seamlessly create an analytic plot on top of any surface. Any
league or sport surface will be an inherit this class.

@author: Ross Drucker
"""
import numpy as np
from functools import wraps
import matplotlib.pyplot as plt
from sportypy._base_classes._base_surface import BaseSurface
from scipy.stats import binned_statistic_2d


class BaseSurfacePlot(BaseSurface):
    """A plot of a sport's/league's surface.

    Class that extends a basic surface to include the necessary methods for
    plotting its features, user-supplied data, heatmaps, hexbin plots, etc.
    """

    def _validate_values(plot_function):
        """Ensure values passed to the plotting function are constrained.

        A point is considered "valid" if the point lies within the boundaries
        of the surface or constraint. Those points that do not are not plotted
        and are instead converted to be np.nan

        This is a decorator which will be used with plotting methods of this
        class.

        This expects that ``x`` and ``y`` have already been converted to the
        right units and shifted appropriately to be plotted
        """

        @wraps(plot_function)
        def wrapper(self, x, y, *, values = None, plot_range = None,
                    plot_xlim = None, plot_ylim = None, for_plot = False,
                    for_display = True, **kwargs):
            # Get the values to use for a hexbin plot. This controls how the
            # hexagons are defined in a hexbin
            C = kwargs.pop("C", None)

            # If no values are supplied, use the binning parameter C described
            # above
            values = C if values is None else values

            # Make a copy of the values so as not to overwrite the original
            # values
            values = self.copy_(values)

            # If there are no values, make a series of 1s to serve as
            # placeholders that is the same shape as the x and y values
            if values is None:
                values = np.ones_like(x)

            # Otherwise, use the actual values and flatten them (if necessary)
            # to a one-dimensional array
            else:
                values = np.ravel(values)

                # Force the x and y values to be symmetric
                if kwargs.get("symmetrize", False):
                    values = np.concatenate((values, values))

            # If x, y, and values are not symmetric in length, raise an error
            if len(x) != len(y) or len(x) != len(values):
                raise Exception("x, y, and values must all be of same length")

            # Initialize the mask to be be false. The mask will indicate
            # whether a point lies within the defined limits for the plot
            mask = False

            # If no plot_range is specified, and no x or y limitations are
            # imposed, set the plot limits to that of a full-surface plot
            if plot_range is None and plot_xlim is None and plot_ylim is None:
                plot_xlim, plot_ylim = self._get_plot_range_limits(
                    for_plot = True,
                    for_display = False
                )

            # Otherwise, get the limits of the plot based on the supplied
            # values and set the mask to identify points who are outside of its
            # bounds
            else:
                plot_xlim, plot_ylim = self._get_plot_range_limits(
                    plot_range,
                    plot_xlim,
                    plot_ylim,
                    for_plot = True,
                    for_display = False
                )

                # The mask finds points that are below the minimum allowable x
                # and y values or above the maximum allowable x and y values
                mask = (
                    (x < plot_xlim[0]) | (x > plot_xlim[1]) |
                    (y < plot_ylim[0]) | (y > plot_ylim[1])
                )

            # If the plot is constrained to exclude values outside its bounds,
            # then values outside of the boundaries of the surface should be
            # set to be nan
            is_constrained = kwargs.get("is_constrained", True)
            if is_constrained:
                values = self._outside_surface_to_nan(x, y, values)

            # Create the final mask to exclude points that are outside the
            # boundary of the surface or are non-existent (nan)
            mask = mask | np.isnan(x) | np.isnan(y) | np.isnan(values)

            # Apply the mask to both the x and y coordinates as well as the
            # values
            x = x[~mask]
            y = y[~mask]
            values = values[~mask]

            if not is_constrained:
                plot_xlim = [min([*plot_xlim, *x]), max([*plot_xlim, *x])]
                plot_ylim = [min([*plot_ylim, *y]), max([*plot_ylim, *y])]

            return plot_function(
                self,
                x,
                y,
                values = values,
                plot_range = plot_range,
                plot_xlim = plot_xlim,
                plot_ylim = plot_ylim,
                **kwargs
            )

        return wrapper

    def _validate_plot(plot_function):
        """Ensure correct form for all parameters necessary to draw the plot.

        This is a decorator which will be used with plotting methods of this
        class.
        """

        @wraps(plot_function)
        def wrapper(self, *args, **kwargs):
            # If no Axes object is passed as a keyword argument, create one to
            # use for the plot
            if "ax" not in kwargs:
                kwargs["ax"] = plt.gca()

            # Convert the non-keyword arguments to a list
            args = list(args)

            # Check if any of the following are passed as keyword arguments to
            # the plot function
            for coord in ("x", "y", "x1", "y1", "x2", "y2"):
                # If they are, then append it to the list of arguments
                if coord in kwargs:
                    args.append(kwargs.pop(coord))

            for i in range(len(args)):
                args[i] = self.copy_(args[i])
                args[i] = np.ravel(args[i])

                is_y = i % 2

                if kwargs.get("symmetrize", False):
                    args[i] = np.concatenate((
                        args[i],
                        args[i] * (-1 if is_y else 1)
                    ))

                args[i] = args[i] - (self.y_trans if is_y else self.x_trans)

            kwargs["transform"] = self._get_transform(kwargs["ax"])
            kwargs["clip_on"] = kwargs.get(
                "clip_on",
                kwargs.get(
                    "is_constrained",
                    True
                )
            )

            args = tuple(args)

            return plot_function(self, *args, **kwargs)

        return wrapper

    def _constrain_plot(self, plot_features, ax, transform):
        """Constrain the features of the plot.

        Plot features should be contained fully inside of the boundaries of the
        surface (e.g. the goal line of a hockey rink should not extend past the
        boards in the corner).

        Parameters
        ----------
        plot_features: list
            The list of features to add to the plot

        ax : matplotlib.Axes
            The axes object onto which the features should be added

        transform : matplotlib.Transform
            The relevant coordinate transform to apply to the features of the
            surface

        Returns
        -------
        Nothing, but the features will be "clipped" to be within the boundary
        of the surface
        """
        # If the plot features passed are an iterable, use them. If not,
        # convert them to a list and then use them
        try:
            iter(plot_features)
        except TypeError:
            plot_features = [plot_features]

        # Set the constraint of the surface
        constraint = self._add_surface_constraint(ax, transform)

        # Iterate over the features and remove any parts of them that extend
        # beyond the surface's boundary
        for plot_feature in plot_features:
            plot_feature.set_clip_path(constraint)

    def _outside_surface_to_nan(self, x, y, values):
        """Remove coordinates that are outside the surface boundary.

        Set any value of passed-in data from outside the boundary of the
        surface to be nan.

        Parameters
        ----------
        x : numpy.ndarray
            The ``x`` values of the coordinates to mask if outside the plot

        y: numpy.ndarray
            The ``y`` values of the coordinates to mask if outside the plot

        values : numpy.ndarray
            The values over which to mask if outside the plot

        corner_radius : float
            The radius of the corner of the surface, in the units of the plot.
            The default is 0.0, which corresponds to the corners" center points
            being located at the actual corner. The default is ``0.0``

            NOTE: This is passed from the constraint's definition

        Returns
        -------
        values : numpy.ndarray
            The masked set of values
        """
        # Convert the x and y values of the coordinates to be floats
        x = np.abs(x).astype("float32")
        y = np.abs(y).astype("float32")

        # Convert the values array to also be floats
        values = values.astype("float32")

        # Get the center of the corners
        center_x = (self._surface_constraint.length / 2.0) - \
            self._surface_constraint.feature_radius

        center_y = (self._surface_constraint.width / 2.0) - \
            self._surface_constraint.feature_radius

        # Create a mask to change the proper values of x and y to be nan. This
        # will be for coordinates where x is more than half way across the
        # length of the surface (e.g. beyond the endline of a basketball court)
        # or more than half way across the width of a surface (e.g. outside
        # the benches of an NHL rink)
        mask = (
            ((x > center_x) & (y > center_y) &
             ((center_x - x) ** 2 + (center_y - y) ** 2 >
             self._surface_constraint.feature_radius ** 2))
        )

        # Apply the mask
        values[mask] = np.nan

        # Return the values with the mask applied
        return values

    def _update_display_range(self, x, y, ax):
        """Update ``xlim`` and ``ylim`` for non-constrained features.

        Parameters
        ----------
        x : numpy.ndarray
            The ``x`` values of the coordinates to be plotted onto the surface

        y: numpy.ndarray
            The ``y`` values of the coordinates to be plotted onto the surface

        ax : matplotlib.Axes
            The axes object onto which the features should be added

        Returns
        -------
        Nothing, but updates the ``x`` and ``y`` limits appropriately
        """
        # Perform a rotation of the coordinates as necessary
        x, y = self._rotate_xy(x, y)

        # Get the current limits
        current_xlim = ax.get_xlim()
        current_ylim = ax.get_ylim()

        # Get the full limits of x and y
        full_xlim = [*current_xlim, *x]
        full_ylim = [*current_ylim, *y]

        # Update appropriately
        ax.set_xlim(min(full_xlim), max(full_xlim))
        ax.set_ylim(min(full_ylim), max(full_ylim))

    def _bound_surface(self, x, y, plot_features, ax, transform,
                       is_constrained, update_display_range):
        """Update the constraints and bounding limits of the resulting plot.

        Parameters
        ----------
        x : numpy.ndarray
            The ``x`` values of the coordinates to be plotted onto the surface

        y: numpy.ndarray
            The ``y`` values of the coordinates to be plotted onto the surface

        plot_features: list
            The list of features to add to the plot

        ax : matplotlib.Axes
            The axes object onto which the features should be added

        transform : matplotlib.Transform
            The relevant coordinate transform to apply to the features of the
            surface

        is_constrained : boolean
            Whether or not the surface is constrained

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot
        """
        # If the surface is constrained, enforce the constraint
        if is_constrained:
            self._constrain_plot(plot_features, ax, transform)

        # Otherwise, if a coordinate should be allowed to be plotted outside
        # of the boundary of the surface (e.g. a home run's landing spot in
        # a baseball plot), update the display correctly
        else:
            if update_display_range:
                self._update_display_range(x, y, ax)

    @staticmethod
    def binned_stat_2d(x, y, values, statistic = "sum", xlim = None,
                       ylim = None, binsize = 1, bins = None):
        """Create a two-dimensional binned statistic via scipy.

        Parameters
        ----------
        x : numpy.ndarray
            A sequence of values to be binned along in the first dimension

        y: numpy.ndarray
            A sequence of values to be binned along in the second dimension

        values : numpy.ndarray
            The data on which the statistic will be computed. This must have
            the same shape as ``x``, or a list of sequences that each have the
            same shape as ``x``

        statistic : str or callable
            The statistic to compute via scipy. Per scipy, the following are
            available:
                - ``"count"``: the number of points inside each bin
                - ``"max"``: the maximum for points inside each bin
                - ``"mean"``: the mean of values for points inside each bin
                - ``"median"``: the median for points inside each bin
                - ``"min"``: the minimum for points inside each bin
                - ``"std"``: the standard deviation for points inside each bin
                - ``"sum"``: the sum of the values for points inside each bin
                - {function}: a user-defined function that utilizes a
                    1-dimensional array of values and outputs a single
                    numerical statistic
            The default is ``"sum"``

        xlim : tuple of float or tuple of int, optional
            The lower and upper bounds of the ``x`` coordinates that should be
            included. This is only used if the bins argument is ``None``

        ylim : tuple of float or tuple of int, optional
            The lower and upper bounds of the ``y`` coordinates that should be
            included. This is only used if the bins argument is ``None``

        binsize : float or tuple of float, optional
            The size of the bins for any given portion of the surface:
            - a single float: the size of the bins for both dimension
            - a tuple of floats: the size of the bins in each dimension

        bins : int or tuple of ints or numpy.ndarray or tuple of numpy.ndarray,
            optional
            The specifications of each bin:
                - a single int: the number of bins for both dimensions
                - a tuple of ints: the number of bins in each dimension
                - a numpy.ndarray: the bin edges for both dimensions
                - a tuple of numpy.ndarrays: the bin edges in each dimension

        Returns
        -------
            stat: (nx, ny) numpy.ndarray
                The values of the selected statistic in each of the
                two-dimensional bins

            x_edge: (nx + 1) numpy.ndarray
                The bin edges along the first dimension

            y_edge: (ny + 1) numpy.ndarray
                The bin edges along the second dimension
        """
        # If no bins are provided, try to iterate through the binsizes
        if bins is None:
            try:
                iter(binsize)
            except TypeError:
                binsize = (binsize, binsize)

            # Get the coordinates of the center of each bin
            x_edge = np.arange(
                xlim[0] - binsize[0] / 2.0,
                xlim[1] + binsize[0],
                binsize[0]
            )
            y_edge = np.arange(
                ylim[0] - binsize[1] / 2.0,
                ylim[1] + binsize[1],
                binsize[1]
            )

            # Define the bins
            bins = [x_edge, y_edge]

        # Compute the statistic
        stat, x_edge, y_edge, _ = binned_statistic_2d(
            x,
            y,
            values,
            statistic = statistic,
            bins = bins
        )

        # Get the transpose of each statistic
        stat = stat.T

        return stat, x_edge, y_edge

    @_validate_plot
    def plot(self, x, y, *, is_constrained = True,
             update_display_range = True, zorder = 100, ax = None, **kwargs):
        """Wrapper for all matplotlib plot functions sportypy supports.

        This will plot to areas out of view when the full surface isn't
        displayed, but the ``xlim`` and ``ylim`` arguments will constrain the
        plot's display.

        All parameters other than ``x`` and ``y`` require keywords

        Parameters
        ----------
        x : numpy.ndarray
            The ``x`` values used in the plot

        y: numpy.ndarray
            The ``y`` values used in the plot

        is_constrained : boolean
            Whether or not the plot should be constrained by the surface's
            boundary. The default is ``True``

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot. This is only used when
            ``is_constrained == False``. The default is ``False``

        zorder : float
            Determine the layer onto which the plot will be drawn. It's
            recommended that this value not be lower than 100. The default is
            ``100``

        ax : matplotlib.Axes
            The axes object onto which the plot should be added. If not
            provided, it will use the currently active axes

        Returns
        -------
        A list of matplotlib.Line2D objects
        """
        # Plot the data onto the Axes object
        img = ax.plot(x, y, zorder = zorder, **kwargs)

        # Bound the plot to be contained inside the surface
        self._bound_surface(
            x,
            y,
            img,
            ax,
            kwargs["transform"],
            is_constrained,
            update_display_range
        )

        return img

    @_validate_plot
    def scatter(self, x, y, *, is_constrained = True,
                update_display_range = True, symmetrize = False, zorder = 21,
                ax = None, **kwargs):
        """Wrapper for matplotlib's scatter function.

        This will create a scatterplot on top of the displayed surface.

        Parameters
        ----------
        x : numpy.ndarray
            The ``x`` values used in the plot

        y: numpy.ndarray
            The ``y`` values used in the plot

        is_constrained : boolean
            Whether or not the plot should be constrained by the surface's
            boundary. The default is ``True``

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot. This is only used when
            ``is_constrained == False``. The default is ``False``

        symmetrize : boolean
            Whether or not to reflect coordinates across the ``y`` axis. The
            default is ``False``

        zorder : int
            Determine the layer onto which the plot will be drawn. It's
            recommended that this value not be lower than 21. The default is
            ``21``

        ax : matplotlib.Axes
            The axes object onto which the plot should be added. If not
            provided, it will use the currently active axes

        Returns
        -------
        A scatterplot of the data
        """
        scatter_plot = ax.scatter(x, y, zorder = zorder, **kwargs)
        self._bound_surface(
            x,
            y,
            scatter_plot,
            ax,
            kwargs["transform"],
            is_constrained,
            update_display_range
        )
        return scatter_plot

    @_validate_plot
    def arrow(self, x1, y1, x2, y2, *, is_constrained = True,
              update_display_range = True, length_includes_head = True,
              head_width = 1, zorder = 21, ax = None, **kwargs):
        """Wrapper for arrow function from matplotlib.

        This will plot to areas out of view when the full surface isn't
        displayed, but the ``xlim`` and ``ylim`` arguments will constrain the
        plot's display.

        All parameters other than ``x1``, ``y1``, ``x2``, and ``y2`` require
        keywords

        Parameters
        ----------
        x1 : numpy.ndarray
            The starting x-coordinates of the arrows

        y1 : numpy.ndarray
            The starting y-coordinates of the arrows

        x2 : numpy.ndarray
            The ending x-coordinates of the arrows

        y2 : numpy.ndarray
            The ending y-coordinates of the arrows

        is_constrained : boolean
            Whether or not the plot should be constrained by the surface's
            boundary. The default is ``True``

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot. This is only used when
            ``is_constrained == False``. The default is ``False``

        length_includes_head : boolean
            Whether or not the head of the arrow is to be included in
            calculating the length of the arrow. The default is True

        head_width : int
            Total width of the full head of the arrow. The default is ``1``

        zorder : int
            Determine the layer onto which the plot will be drawn. It's
            recommended that this value not be lower than 21. The default is
            ``21``

        ax : matplotlib.Axes
            The axes object onto which the plot should be added. If not
            provided, it will use the currently active axes

        **kwargs : dict, optional
            Any other matplotlib arrow properties

        Returns
        -------
        A list of matplotlib.FancyArrow objects
        """
        # Compute the distance between the ending and starting points
        dx = x2 - x1
        dy = y2 - y1

        # Define a container for the arrows
        arrows = []

        # Create the arrows
        for i in range(len(x1)):
            arrows.append(
                ax.arrow(
                    x1[i],
                    y1[i],
                    dx[i],
                    dy[i],
                    zorder = zorder,
                    head_width = head_width,
                    length_includes_head = length_includes_head,
                    **kwargs
                )
            )

        # Bound the resulting plot to be inside the surface
        self._bound_surface(
            [*x1, *x2],
            [*y1, *y2],
            arrows,
            ax,
            kwargs["transform"],
            is_constrained,
            update_display_range
        )

        return arrows

    @_validate_plot
    @_validate_values
    def hexbin(self, x, y, *, values = None, is_constrained = True,
                update_display_range = True, symmetrize = False,
                plot_range = None, plot_xlim = None, plot_ylim = None,
                gridsize = None, binsize = 1, zorder = 11, clip_on = True,
                ax = None, **kwargs):
        """Wrapper for hexbin function from matplotlib.

        This will plot to areas out of view when the full surface isn't
        displayed, but the ``xlim`` and ``ylim`` arguments will constrain the
        plot's display.

        All parameters other than ``x`` and ``y`` require keywords

        Parameters
        ----------
        x : numpy.ndarray
            A sequence of values to be binned along in the first dimension

        y: numpy.ndarray
            A sequence of values to be binned along in the second dimension

        values : numpy.ndarray
            The data to use for each hexbin. If ``None``, then values of 1 will
            be assigned to each ``(x, y)`` coordinate

        is_constrained : boolean
            Whether or not the plot should be constrained by the surface's
            boundary. The default is ``True``

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot. This is only used when
            ``is_constrained == False``. The default is ``False``

        symmetrize : boolean
            Whether or not to reflect coordinates and values across the ``y``
            axis. The default is ``False``

        plot_range : str, optional
            Restrict the portion of the surface that can be plotted to.

            This is achieved by removing values outside of the given range in
            each surface's ``draw()`` method. See the surface ``draw()`` method
            for viable options. This will only affect the x-coordinates and can
            be used in conjunction with ``ylim``, but will be superceded so
            long as ``xlim`` is provided

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        plot_xlim : float or tuple of floats, optional
            The range of ``x`` coordinates to include in the plot:
                - a single float: the lower bound of the ``x`` coordinates
                - a tuple of floats: the lower and upper bounds of the ``x``
                  coordinates

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        plot_ylim : float or tuple of floats, optional
            The range of ``y`` coordinates to include in the plot:
                - a single float: the lower bound of the ``y`` coordinates
                - a tuple of floats: the lower and upper bounds of the ``y``
                  coordinates

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        gridsize : int or tuple of ints, optional
            The grid specification. If passed as a single integer, this is the
            number of hexagons in the ``x`` direction. The number of hexagons
            in the ``y`` direction is then chosen such that each hexagon is
            approximately regular. If passed as a tuple, the first integer will
            be the number of hexagons in the ``x`` direction, and the second
            will be the number of hexagons in the ``y`` direction

        binsize : float or tuple of floats, optional
            The size of the bins for any given portion of the surface:
            - a single float: the size of the bins for both dimension
            - a tuple of floats: the size of the bins in each dimension

        zorder : float
            Determine the layer onto which the plot will be drawn. It's
            recommended that this value be between 11 and 15. The default is
            ``11``


        clip_on : boolean
            Whether or not the matplotlib artist uses clipping. Other plotting
            features will automatically be set to the same value as
            ``is_constrained``, but this may result in oddities specific to
            hexbin. The default is ``True``

        ax : matplotlib.Axes
            The axes object onto which the plot should be added. If not
            provided, it will use the currently active axes

        **kwargs : dict, optional
            Any other matplotlib hexbin properties

        Returns
        -------
        A matplotlib.PolyCollection object of the hexbins
        """
        # Set the value of clip_on, defaulting to True if not passed
        kwargs["clip_on"] = kwargs.get("clip_on", True)

        # Try to determine the binsize
        try:
            iter(binsize)
        except TypeError:
            binsize = (binsize, binsize)

        # Set the default grid size to be uniform in both the x and y
        # directions. If a gridsize is passed, it will be used
        if not gridsize:
            gridsize = (
                int((plot_xlim[1] - plot_xlim[0]) / binsize[0]),
                int((plot_ylim[1] - plot_ylim[0]) / binsize[1])
            )

        # Reduce function needs to change since hexbin uses count when C is
        # None and np.mean when values are included
        if np.all(values == 1):
            kwargs["reduce_C_function"] = kwargs.get(
                "reduce_C_function",
                np.sum
            )

        # The transformation should be applied to the hexagons only *after* the
        # hexbin is drawn
        transform = kwargs.pop("transform")
        hexagon_transform = transform - ax.transData

        # Add the hexagons to the plot
        hexbin_plot = ax.hexbin(
            x,
            y,
            C = values,
            gridsize = gridsize,
            zorder = zorder,
            **kwargs
        )

        # Correct the rotation of the hexbins
        hexes = hexbin_plot.get_paths()[0]
        hexes.vertices = hexagon_transform.transform(hexes.vertices)
        hexbin_plot.set_offsets(
            hexagon_transform.transform(
                hexbin_plot.get_offsets()
            )
        )

        # Bound the resulting plot to be inside the surface
        self._bound_surface(
            x,
            y,
            hexbin_plot,
            ax,
            transform,
            is_constrained,
            update_display_range
        )

        return hexbin_plot

    @_validate_plot
    @_validate_values
    def heatmap(self, x, y, *, values = None, is_constrained = True,
                update_display_range = True, symmetrize = False,
                plot_range = None, plot_xlim = None, plot_ylim = None,
                statistic = "sum", binsize = 1, bins = None, zorder = 11,
                ax = None, **kwargs):
        """Wrapper for pcolormesh function from matplotlib.

        This will plot to areas out of view when the full surface isn't
        displayed, but the ``xlim`` and ``ylim`` arguments will constrain the
        plot's display.

        All parameters other than ``x`` and ``y`` require keywords

        Parameters
        ----------
        x : numpy.ndarray
            A sequence of values to be binned along in the first dimension

        y: numpy.ndarray
            A sequence of values to be binned along in the second dimension

        values : numpy.ndarray
            The data to use for color-mapping. If ``None``, then values of 1
            will be assigned to each ``(x, y)`` coordinate

        is_constrained : boolean
            Whether or not the plot should be constrained by the surface's
            boundary. The default is ``True``

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot. This is only used when
            ``is_constrained == False``. The default is ``False``

        symmetrize : boolean
            Whether or not to reflect coordinates and values across the ``y``
            axis. The default is ``False``

        plot_range : str, optional
            Restrict the portion of the surface that can be plotted to.

            This is achieved by removing values outside of the given range in
            each surface's ``draw()`` method. See the surface ``draw()`` method
            for viable options. This will only affect the x-coordinates and can
            be used in conjunction with ``ylim``, but will be superceded so
            long as ``xlim`` is provided

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        plot_xlim : float or tuple of floats, optional
            The range of ``x`` coordinates to include in the plot:
                - a single float: the lower bound of the ``x`` coordinates
                - a tuple of floats: the lower and upper bounds of the ``x``
                  coordinates

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        plot_ylim : float or tuple of floats, optional
            The range of ``y`` coordinates to include in the plot:
                - a single float: the lower bound of the ``y`` coordinates
                - a tuple of floats: the lower and upper bounds of the ``y``
                  coordinates

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        statistic : str or callable
            The statistic to compute via scipy. Per scipy, the following are
            available:
                - ``"count"``: the number of points inside each bin
                - ``"max"``: the maximum for points inside each bin
                - ``"mean"``: the mean of values for points inside each bin
                - ``"median"``: the median for points inside each bin
                - ``"min"``: the minimum for points inside each bin
                - ``"std"``: the standard deviation for points inside each bin
                - ``"sum"``: the sum of the values for points inside each bin
                - {function}: a user-defined function that utilizes a
                    1-dimensional array of values and outputs a single
                    numerical statistic
            The default is ``"sum"``

        binsize : float or tuple of floats, optional
            The size of the bins for any given portion of the surface:
            - a single float: the size of the bins for both dimension
            - a tuple of floats: the size of the bins in each dimension

        bins : int or tuple of ints or numpy.ndarray or tuple of numpy.ndarray,
            optional
            The specifications of each bin:
                - a single int: the number of bins for both dimensions
                - a tuple of ints: the number of bins in each dimension
                - a numpy.ndarray: the bin edges for both dimensions
                - a tuple of numpy.ndarrays: the bin edges in each dimension

        zorder : float
            Determine the layer onto which the heatmap will be drawn. It's
            recommended that this value be between 11 and 15. The default is
            ``11``

        ax : matplotlib.Axes
            The axes object onto which the heatmap should be added. If not
            provided, it will use the currently active axes

        **kwargs : dict, optional
            Any other matplotlib heatmap properties

        Returns
        -------
        A matplotlib.QuadMesh object of the heat map
        """
        # Compute the statistic for the heatmap
        stat, x_edge, y_edge = self.binned_stat_2d(
            x,
            y,
            values,
            statistic,
            plot_xlim,
            plot_ylim,
            binsize,
            bins
        )

        # Add the heatmap to the the plot
        heatmap_plot = ax.pcolormesh(
            x_edge,
            y_edge,
            stat,
            zorder = zorder,
            **kwargs
        )

        # Bound the resulting plot to be inside the surface
        self._bound_surface(
            x,
            y,
            heatmap_plot,
            ax,
            kwargs["transform"],
            is_constrained,
            update_display_range
        )

        return heatmap_plot

    @_validate_plot
    @_validate_values
    def contour(self, x, y, *, values = None, fill = True,
                is_constrained = True, update_display_range = True,
                symmetrize = False, plot_range = None, plot_xlim = None,
                plot_ylim = None, statistic = "sum", binsize = 1, bins = None,
                zorder = 11, ax = None, **kwargs):
        """Wrapper for matplotlib contour and contourf functions.

        This will plot to areas out of view when the full surface isn't
        displayed, but the ``xlim`` and ``ylim`` arguments will constrain the
        plot's display.

        All parameters other than ``x`` and ``y`` require keywords

        Parameters
        ----------
        x : numpy.ndarray
            A sequence of values to be binned along in the first dimension

        y: numpy.ndarray
            A sequence of values to be binned along in the second dimension

        values : numpy.ndarray
            The data to use for color-mapping. If ``None``, then values of 1
            will be assigned to each ``(x, y)`` coordinate

        fill : boolean
            Whether or not to fill in the contours. The default is ``True``

        is_constrained : boolean
            Whether or not the plot should be constrained by the surface's
            boundary. The default is ``True``

        update_display_range : boolean
            Whether or not to allow the plotted points to update the ``x`` and
            ``y`` limits of the plot. This is only used when
            ``is_constrained == False``. The default is ``False``

        symmetrize : boolean
            Whether or not to reflect coordinates and values across the ``y``
            axis. The default is ``False``

        plot_range : str, optional
            Restrict the portion of the surface that can be plotted to.

            This is achieved by removing values outside of the given range in
            each surface's ``draw()`` method. See the surface ``draw()`` method
            for viable options. This will only affect the x-coordinates and can
            be used in conjunction with ``ylim``, but will be superceded so
            long as ``xlim`` is provided

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        plot_xlim : float or tuple of floats, optional
            The range of ``x`` coordinates to include in the plot:
                - a single float: the lower bound of the ``x`` coordinates
                - a tuple of floats: the lower and upper bounds of the ``x``
                  coordinates

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        plot_ylim : float or tuple of floats, optional
            The range of ``y`` coordinates to include in the plot:
                - a single float: the lower bound of the ``y`` coordinates
                - a tuple of floats: the lower and upper bounds of the ``y``
                  coordinates

            If no values are passed for ``plot_range``, ``plot_xlim``, and
            ``plot_ylim``, all coordinate values will be used

        statistic : str or callable
            The statistic to compute via scipy. Per scipy, the following are
            available:
                - ``"count"``: the number of points inside each bin
                - ``"max"``: the maximum for points inside each bin
                - ``"mean"``: the mean of values for points inside each bin
                - ``"median"``: the median for points inside each bin
                - ``"min"``: the minimum for points inside each bin
                - ``"std"``: the standard deviation for points inside each bin
                - ``"sum"``: the sum of the values for points inside each bin
                - {function}: a user-defined function that utilizes a
                    1-dimensional array of values and outputs a single
                    numerical statistic
            The default is ``"sum"``

        binsize : float or tuple of floats, optional
            The size of the bins for any given portion of the surface:
            - a single float: the size of the bins for both dimension
            - a tuple of floats: the size of the bins in each dimension

        bins : int or tuple of ints or numpy.ndarray or tuple of numpy.ndarray,
            optional
            The specifications of each bin:
                - a single int: the number of bins for both dimensions
                - a tuple of ints: the number of bins in each dimension
                - a numpy.ndarray: the bin edges for both dimensions
                - a tuple of numpy.ndarrays: the bin edges in each dimension

        zorder : float
            Determine the layer onto which the plot will be drawn. It's
            recommended that this value be between 11 and 15. The default is
            ``11``

        ax : matplotlib.Axes
            The axes object onto which the plot should be added. If not
            provided, it will use the currently active axes

        **kwargs : dict, optional
            Any other matplotlib contour properties

        Returns
        -------
        A matplotlib.QuadContourSet object of the contour plot
        """
        # Compute the statistic for the heatmap
        stat, x_edge, y_edge = self.binned_stat_2d(
            x,
            y,
            values,
            statistic,
            plot_xlim,
            plot_ylim,
            binsize,
            bins
        )

        # Define the centers of the x and y edges
        x_centers = (x_edge[:-1] + x_edge[1:]) / 2.0
        y_centers = (y_edge[:-1] + y_edge[1:]) / 2.0

        # Enforce the plot limits
        if plot_xlim is not None:
            x_centers[-1] = max(x_centers[-1], plot_xlim[1])
        if plot_ylim is not None:
            y_centers[-1] = max(y_centers[-1], plot_ylim[1])

        # Remove the clip_on argument if it's not used in the function
        kwargs.pop("clip_on", None)

        # Create the contour plot
        contour_function = ax.contourf if fill else ax.contour
        contour_plot = contour_function(
            x_centers,
            y_centers,
            stat,
            zorder = zorder,
            **kwargs
        )

        # Bound the resulting plot to be inside the surface
        self._bound_surface(
            x,
            y,
            contour_plot.collections,
            ax,
            kwargs["transform"],
            is_constrained,
            update_display_range
        )

        return contour_plot

    # Define the alias for contour
    contourf = contour
