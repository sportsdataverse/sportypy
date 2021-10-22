"""Base surface plot class to extend scipy to sportypy.

The BaseSurfacePlot class is an extension of the BaseSurface class that enables
a user to seamlessly create an analytic plot on top of any surface. Any league
or sport surface will be an inherit this class.

@author: Ross Drucker
"""
import numpy as np
from functools import wraps
import matplotlib.pyplot as plt
from sportypy._base_classes._base_surface import BaseSurface


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

        This expects that x and y have already been converted to the right
        units and shifted appropriately to be plotted
        """

        @wraps(plot_function)
        def wrapper(self, x, y, *, values = None, plot_range = None,
                    plot_xlim = None, plot_ylim = None, **kwargs):
            # Get the values to use for a hexbin plot. This controls how the
            # hexagons are defined in a hexbin
            C = kwargs.pop('C', None)

            # If no values are supplied, use the binning parameter C described
            # above
            if not values:
                values = C

            # Make a copy of the values so as not to overwrite the original
            # values
            values = self.copy_(values)

            # If there are no values, make a series of 1s to serve as
            # placeholders that is the same shape as the x and y values
            if not values:
                values = np.ones(x.shape)

            # Otherwise, use the actual values and flatten them (if necessary)
            # to a one-dimensional array
            else:
                values = np.ravel(values)

                # Force the x and y values to be symmetric
                if kwargs.get('symmetrize', False):
                    values = np.concatenate((values, values))

            # If x, y, and values are not symmetric in length, raise an error
            if len(x) != len(y) or len(x) != len(values):
                raise Exception('x, y, and values must all be of same length')

            if plot_range is None and plot_xlim is None and plot_ylim is None:
                plot_xlim, plot_ylim = self._get_limits('full')

            # Initialize the mask to be be false. The mask will indicate
            # whether a point lies within the defined limits for the plot
            mask = False

            # If no plot_range is specified, and no x or y limitations are
            # imposed, set the plot limits to that of a full-surface plot
            if plot_range is None and plot_xlim is None and plot_ylim is None:
                plot_xlim, plot_ylim = self._get_limits('full')

            # Otherwise, get the limits of the plot based on the supplied
            # values and set the mask to identify points who are outside of its
            # bounds
            else:
                plot_xlim, plot_ylim = self.get_limits(
                    plot_range,
                    self.copy_(plot_xlim),
                    self.copy_(plot_ylim)
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
            if kwargs.get('is_constrained', True):
                values = self._outside_surface_to_nan(x, y, values)

            # Create the final mask to exclude points that are outside the
            # boundary of the surface or are non-existent (nan)
            mask = mask | np.isnan(x) | np.isnan(y) | np.isnan(values)

            # Apply the mask to both the x and y coordinates as well as the
            # values
            x = x[~mask]
            y = y[~mask]
            values = values[~mask]

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
            if 'ax' not in kwargs:
                kwargs['ax'] = plt.gca()

            # Convert the non-keyword arguments to a list
            args = list(args)

            # Check if any of the following are passed as keyword arguments to
            # the plot function
            for coord in ('x', 'y', 'x1', 'y1', 'x2', 'y2'):
                # If they are, then append it to the list of arguments
                if coord in kwargs:
                    args.append(kwargs.pop(coord))

            for i in range(len(args)):
                args[i] = self.copy_(args[i])
                args[i] = np.ravel(args[i])

                is_y = i % 2

                if kwargs.get('symmetrize', False):
                    args[i] = np.concatenate((
                        args[i],
                        args[i] * (-1 if is_y else 1)
                    ))

                args[i] = args[i] - (self.y_shift if is_y else self.x_shift)

            kwargs['transform'] = self._get_transform(kwargs['ax'])

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
            The x values of the coordinates to mask if outside the plot

        y: numpy.ndarray
            The y values of the coordinates to mask if outside the plot

        values : numpy.ndarray
            The values over which to mask if outside the plot

        corner_radius : float (default: 0.0)
            The radius of the corner of the surface, in the units of the plot.
            The default is 0.0, which corresponds to the corners' center points
            being located at the actual corner

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
            ((x > center_x)) & (y > center_y) &
            ((center_x - x ** 2)) + ((center_y - y) ** 2) >
            (self._surface_constraint ** 2)
        )

        # Apply the mask
        values[mask] = np.nan

        # Return the values with the mask applied
        return values
