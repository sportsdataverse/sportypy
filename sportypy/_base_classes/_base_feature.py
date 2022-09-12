"""Base classes for features of any sports surface.

The ``BaseFeature`` class is flexible to accomodate a wide variety of different
types of features, with methods to add the feature to the plot as well as
combine different shapes to create a feature. These classes serve as the
building blocks of each surface's features.

@author: Ross Drucker
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class BaseFeature(ABC):
    """A base class for features on any surface.

    This class is for all features of a surface, regardless of the sport it is
    used for.

    Attributes
    ----------
    feature_df : pandas.DataFrame
        The data frame containing the coordinates necessary to draw the feature

    x_anchor : float
        The ``x`` coordinate corresponding to the feature's anchored position
        in the surface's coordinate system. The default is ``0.0``

    y_anchor : float
        The ``y`` coordinate corresponding to the feature's anchored position
        in the surface's coordinate system. The default is ``0.0``

    reflected_over_x : bool
        Whether or not the feature should be reflected over the ``x`` axis. The
        default is ``False``

    reflect_over_y : bool
        Whether or not the feature should be reflected over the ``y`` axis. The
        default is ``True``

    visible : bool
        Whether or not the feature should be visible on the final plot. The
        default is ``False``

    plot_kwargs : dict
        Additional arguments the feature requires to be plotted. These may
        include things such as ``zorder``, ``facecolor``, ``edgecolor``, etc.
    """

    def __init__(self, feature_df = pd.DataFrame(), x_anchor = 0.0,
                 y_anchor = 0.0, reflect_x = False, reflect_y = True,
                 is_constrained = True, visible = True, **plot_kwargs):
        """Initialize the attributes of the class.

        The attributes for features will be provided in the feature's
        construction parameter dictionary
        """
        # Set the x and y anchors as well as the anchor's position
        self.x_anchor = x_anchor
        self.y_anchor = y_anchor

        # If the feature is to be reflected over the x axis, set the reflection
        # factor to be -1
        if reflect_x:
            self.x_reflection = -1
        else:
            self.x_reflection = 1

        # If the feature is to be reflected over the y axis, set the reflection
        # factor to be -1
        if reflect_y:
            self.y_reflection = -1
        else:
            self.y_reflection = 1

        # Set the feature's visibility
        self.visible = visible

        # Set each feature to be constrained
        self.is_constrained = is_constrained

        # Set the rest of the arguments that will be passed to the matplotlib
        # plotting functions
        self.plot_kwargs = plot_kwargs

    @abstractmethod
    def _get_centered_feature(self):
        """Determine the feature's position if it were centered at (0, 0).

        Abstract method that returns the x and y coordinates that are needed
        to create a Polygon for a specific feature if it were to be centered at
        (0, 0) in the coordinate system. This method is created individually
        for each feature in its constructor.

        Returns
        -------
        feature_df : pandas.DataFrame
            The data frame containing the feature's x and y coordinates if they
            were to be drawn at ``(0.0, 0.0)``
        """
        pass

    def _translate_feature(self):
        """Translate the feature to the proper (x, y) location on the surface.

        Return a pandas data frame of the x and y coordinates necessary for
        plotting the feature in the correct location on the surface.

        Parameters
        ----------
        None passed, but utilizes the data frame returned by the
        ``_get_centered_feature()`` method

        Returns
        -------
        feature_df: pandas.DataFrame
            The data frame containing the feature's ``x`` and ``y`` coordinates
            in the correct location on the surface
        """
        # Start by getting the coordinates of the feature as if it were
        # centered around the point (0, 0) through using the
        # _get_centered_feature() method
        feature_df = self._get_centered_feature()

        # Then, reflect and shift all values as appropriate
        feature_df["x"] = feature_df["x"] * self.x_reflection + self.x_anchor
        feature_df["y"] = feature_df["y"] * self.y_reflection + self.y_anchor

        return feature_df

    def create_feature_mpl_polygon(self):
        """Generate a matplotlib.Polygon object that will display the feature.

        Parameters
        ----------
        None passed, but uses the numpy ndarrays returned by the
        ``_translate_feature()`` method

        Returns
        -------
        feature_polygon : matplotlib Polygon
            An object from matplotlib's Polygon class that contains the polygon
            that represents the desired feature
        """
        # Get the polygon's data frame
        feature_df = self._translate_feature()

        # Create a matplotlib.Polygon object that composes the feature
        feature_polygon = plt.Polygon(
            feature_df,
            visible = self.visible,
            **self.plot_kwargs
        )

        return feature_polygon

    @staticmethod
    def create_circle(center = (0.0, 0.0), npoints = 10000, r = 1.0,
                      start = 0.0, end = 2.0):
        """Generate a data frame that contains the points that form a circle.

        This function generates a set of ``x`` and ``y`` coordinates that form
        a circle (or the arc of a circle)

        Parameters
        ----------
        center : tuple
            The ``(x, y)`` coordinates of the center of the circle. The default
            is ``(0.0, 0.0)``

        npoints : int
            The number of points with which to create the circle. This will
            also be the length of the resulting data frame. The default is
            ``1000``

        r : float
            Radius of the circle **in the units of the surface**. The default
            is ``1.0``

        start : float
            The angle (in radians) at which to start drawing the circle, where
            zero runs along the +x axis. The default is ``0.0``

        end : float
            The angle (in radians) at which to stop drawing the circle, where
            zero runs along the +x axis. The default is ``0.0``

        Returns
        -------
        circle_pts : pandas.DataFrame
            A pandas data frame containing the necessary ``x`` and ``y``
            coordinates for a circle
        """
        # Create a vector of numbers that are evenly spaced apart between the
        # starting and ending angles. They should be multiplied by pi to be in
        # radians. This vector represents the angle through which the circle is
        # traced
        theta = np.linspace(start * np.pi, end * np.pi, npoints)

        # Create the vectors x and y that represent the circle (or arc of a
        # circle) to be created. This is a translation away from the center
        # across r, then rotated by cos(angle) and sin(angle) for x and y
        # respectively.
        x = center[0] + (r * np.cos(theta))
        y = center[1] + (r * np.sin(theta))

        circle_pts = pd.DataFrame({
            "x": x,
            "y": y
        })

        return circle_pts

    @staticmethod
    def create_rectangle(x_min = 0.0, x_max = 0.0, y_min = 0.0, y_max = 0.0):
        """Generate a bounding box for a rectangle.

        This method generates a data frame that contains the coordinates
        forming the bounding box of a rectangle

        Parameters
        ----------
        x_min : float
            The lower of the two ``x`` coordinates. The default is ``0.0``

        x_max : float
            The higher of the two ``x`` coordinates. The default is ``0.0``

        y_min : float
            The lower of the two ``y`` coordinates. The default is ``0.0``

        y_max : float
            The higher of the two ``y`` coordinates. The default is ``0.0``

        Returns
        -------
        rect_pts : pandas.DataFrame
            A pandas data frame containing the necessary ``x`` and ``y``
            coordinates for a rectangle
        """
        # A rectangle's bounding box is described by going along the following
        # path:
        # (x_min, y_min)
        # (x_max, y_min)
        # (x_max, y_max)
        # (x_min, y_max)
        # (x_min, y_min)
        #
        # This is the same path that a rectangle will follow
        rect_pts = pd.DataFrame({
            "x": [
                x_min,
                x_max,
                x_max,
                x_min,
                x_min
            ],

            "y": [
                y_min,
                y_min,
                y_max,
                y_max,
                y_min
            ]
        })

        return rect_pts

    @staticmethod
    def create_square(side_length = 1.0, center = (0, 0)):
        """Generate a bound box for a square.

        This function generates a data frame that contains the coordinates
        forming the bounding box of a square

        Parameters
        ----------
        side_length : float
            The length of the side of the square. The default is ``1.0``

        center : tuple
            Where to center the square. The default is ``(0.0, 0.0)``

        Returns
        -------
        square_pts : pandas.DataFrame
            A pandas data frame containing the necessary ``x`` and ``y``
            coordinates for a square
        """
        # A unit square centered at (0, 0) can have its boundary described as
        # the path traced by the following:
        # (-0.5, -0.5)
        # ( 0.5, -0.5)
        # ( 0.5,  0.5)
        # (-0.5,  0.5)
        # (-0.5, -0.5)
        #
        # This is the same path that a generated square will follow, with the
        # side lengths variable
        square_pts = pd.DataFrame({
            "x": [
                center[0] - side_length / 2,
                center[0] + side_length / 2,
                center[0] + side_length / 2,
                center[0] - side_length / 2,
                center[0] - side_length / 2
            ],

            "y": [
                center[1] - side_length / 2,
                center[1] - side_length / 2,
                center[1] + side_length / 2,
                center[1] + side_length / 2,
                center[1] - side_length / 2,
            ]
        })

        return square_pts

    @staticmethod
    def create_diamond(height = 0.0, width = 0.0, center = (0.0, 0.0)):
        """Generate a bound box for a diamond.

        This function generates a data frame that contains the coordinates
        forming the bounding box of a diamond

        Parameters
        ----------
        height : float
            The vertical height of the diamond. The default is ``0.0``

        width : float
            The horizontal width of the diamond. The default is ``0.0``

        center : tuple
            Where to center the diamond. The default is ``(0.0, 0.0)``

        Returns
        -------
        diamond_pts : pandas.DataFrame
            A pandas data frame containing the necessary ``x`` and ``y``
            coordinates for a diamond
        """
        # A unit diamond's bounding box is described by going along the
        # following path:
        # (-0.5,  0.0)
        # ( 0.0, -0.5)
        # ( 0.5,  0.0)
        # ( 0.0,  0.5)
        # (-0.5,  0.0)
        #
        # This is the path that a diamond feature will also trace, with the
        # appropriate height and width
        diamond_pts = pd.DataFrame({
            "x": [
                center[0] - (width / 2.0),
                center[0],
                center[0] + (width / 2.0),
                center[0],
                center[0] - (width / 2.0)
            ],

            "y": [
                center[1],
                center[1] - (height / 2.0),
                center[1],
                center[1] + (height / 2.0),
                center[1]
            ]
        })

        return diamond_pts

    def draw(self, ax, transform = None):
        """Draw the feature.

        Parameters
        ----------
        ax : matplotlib.Axes
            Axes onto which the feature should be drawn

        transform : matplotlib.Transform, optional
            The matplotlib.Transform to apply to the plot. The default is
            ``None``

        Returns
        -------
        patch : matplotlib.patches.Patch
            The patch object that contains the feature. The patch is added to
            the Axes object
        """
        # Set the transformation to be data coordinates if none is passed
        if not transform:
            transform = ax.transData  # pragma: no cover

        # Get the feature's matplotlib.Polygon
        patch = self.create_feature_mpl_polygon()

        # Add the patch to the Axes object
        patch = ax.add_patch(patch)

        # Set the transformation of the patch
        patch.set_transform(transform)

        return patch

    def _reflect(self, df, over_x = False, over_y = True):
        """Reflect a data frame's coordinates over the desired axes.

        Parameters
        ----------
        df : pandas.DataFrame
            A data frame with points to reflect

        over_x : bool False
            Whether or not to reflect the points over the ``x`` axis. The
            default is ``False``

        over_y : bool False
            Whether or not to reflect the points over the ``y`` axis. The
            default is ``False``

        Returns
        -------
        out_df : pandas.DataFrame
            The data frame with the appropriate reflections
        """
        out_df = df.copy()
        if over_x:
            out_df["y"] = -1 * df["y"]
        if over_y:
            out_df["x"] = -1 * df["x"]

        return out_df

    def _rotate(self, df, angle = 0.25):
        """Mathematical rotation about ``(0.0, 0.0)``.

        This rotation is given as::

            x' = x * cos(theta) - y * sin(theta)
            y' = x * sin(theta) + y * cos(theta)

        Parameters
        ----------
        df : pandas.DataFrame
            A data frame with points to rotate

        angle : float
            The angle (in radians) by which to rotate the coordinates, divided
            by pi. The default is ``0.5``

        Returns
        -------
        rotated : pandas.DataFrame
            The data frame rotated around the origin
        """
        # Set theta to be the angle of rotation
        theta = angle * np.pi

        rotated = df.copy()
        rotated["x"] = (
            (df["x"] * math.cos(theta)) -
            (df["y"] * math.sin(theta))
        )
        rotated["y"] = (
            (df["x"] * math.sin(theta)) +
            (df["y"] * math.cos(theta))
        )

        return rotated
