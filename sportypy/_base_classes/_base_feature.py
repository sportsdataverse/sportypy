"""Base classes for features of any sports surface.

The BaseFeature class is flexible to accomodate a wide variety of different
types of features, with methods to add the feature to the plot as well as
combine different shapes to create a feature. These classes serve as the
building blocks of each surface's features.

@author: Ross Drucker
"""

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
    feature_df : pandas.DataFrame (default: empty data frame)
        The dataframe containing the coordinates necessary to draw the feature

    x_anchor : float (default: 0.0)
        The x coordinate corresponding to the feature's anchored position in
        the surface's coordinate system

    y_anchor : float (default: 0.0)
        The y coordinate corresponding to the feature's anchored position in
        the surface's coordinate system

    x_justify : str (default: 'center')
        The position of the x anchor relative to the rest of the feature.
        Viable options are 'center', 'left_edge', or 'right_edge'. This will be
        used to anchor the feature to its given location

    y_justify : str (default: 'center')
        The position of the y anchor relative to the rest of the feature.
        Viable options are 'center', 'top', or 'bottom'. This will be used to
        anchor the feature to its given location

    reflected_over_x : bool (default: False)
        Whether or not the feature should be reflected over the x axis

    reflect_over_y : bool (default: True)
        Whether or not the feature should be reflected over the y axis

    visible : bool (default: False)
        Whether or not the feature should be visible on the final plot

    plot_kwargs : dict
        Additional arguments the feature requires to be plotted
    """

    def __init__(self, feature_df = pd.DataFrame(), x_anchor = 0.0,
                 y_anchor = 0.0, x_justify = 'center', y_justify = 'center',
                 reflect_x = False, reflect_y = True, is_constrained = True,
                 visible = True, **plot_kwargs):
        """Initialize the attributes of the class.

        The attributes for features will be provided in the feature's
        construction parameter dictionary
        """
        # Set the x and y anchors as well as the anchor's position
        self.x_anchor = x_anchor
        self.x_justify = x_justify
        self.y_anchor = y_anchor
        self.y_justify = y_justify

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
            were to be drawn at (0, 0)
        """
        pass

    def _translate_feature(self):
        """Translate the feature to the proper (x, y) location on the surface.

        Return a pandas data frame of the x and y coordinates necessary for
        plotting the feature in the correct location on the surface.

        Parameters
        ----------
        None passed, but utilizes the data frame returned by the
        _get_centered_feature() method

        Returns
        -------
        feature_df: pandas.DataFrame
            The data frame containing the feature's x and y coordinates in the
            correct location on the surface.
        """
        # Start by getting the coordinates of the feature as if it were
        # centered around the point (0, 0) through using the
        # _get_centered_feature() method
        feature_df = self._get_centered_feature()

        # Then, reflect and shift all values as appropriate
        feature_df['x'] = (feature_df['x'] * self.x_reflection) + self.x_anchor
        feature_df['y'] = (feature_df['y'] * self.y_reflection) + self.y_anchor

        return feature_df

    def create_feature_mpl_polygon(self):
        """Generate a matplotlib.Polygon object that will display the feature.

        Parameters
        ----------
        None passed, but uses the numpy ndarrays returned by the
        self._translate_feature() method

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

        This function generates a set of x and y coordinates that form a circle
        (or the arc of a circle)

        Parameters
        ----------
        center : tuple (float, float) (default: (0.0, 0.0))
            The (x, y) coordinates of the center of the circle

        npoints : int (default: 1000)
            The number of points with which to create the circle. This will
            also be the length of the resulting data frame

        r : float (default: 1.0)
            Radius of the circle IN THE UNITS OF THE SURFACE

        start : float (default: 0.0)
            The angle (in radians) at which to start drawing the circle, where
            zero runs along the +x axis

        end : float (default: 0.0)
            The angle (in radians) at which to stop drawing the circle, where
            zero runs along the +x axis

        Returns
        -------
        circle_pts : pandas.DataFrame
            A pandas data frame containing the necessary x and y coordinates
            for a circle
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
            'x': x,
            'y': y
        })

        return circle_pts

    @staticmethod
    def create_rectangle(x_min = 0.0, x_max = 0.0, y_min = 0.0, y_max = 0.0):
        """Generate a bounding box for a rectangle.

        This method generates a data frame that contains the coordinates
        forming the bounding box of a rectangle

        Parameters
        ----------
        x_min : float (default: 0.0)
            The lower of the two x coordinates

        x_max : float (default: 0.0)
            The higher of the two x coordinates

        y_min : float (default: 0.0)
            The lower of the two y coordinates

        y_max : float (default: 0.0)
            The higher of the two y coordinates

        Returns
        -------
        rect_pts : pandas.DataFrame
            A pandas data frame containing the necessary x and y coordinates
            for a rectangle
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
            'x': [
                x_min,
                x_max,
                x_max,
                x_min,
                x_min
            ],

            'y': [
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
        side_length : float (default: 1.0)
            The length of the side of the square

        center : tuple (float, float) (default: (0.0, 0.0))
            Where to center the square

        Returns
        -------
        square_pts : pandas.DataFrame
            A pandas data frame containing the necessary x and y coordinates
            for a square
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
            'x': [
                center[0] - side_length / 2,
                center[0] + side_length / 2,
                center[0] + side_length / 2,
                center[0] - side_length / 2,
                center[0] - side_length / 2
            ],

            'y': [
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
        height : float (default: 0.0)
            The vertical height of the diamond

        width : float (default: 0.0)
            The horizontal width of the diamond

        center : tuple (float, float) (default: (0.0, 0.0))
            Where to center the diamond

        Returns
        -------
        diamond_pts : pandas.DataFrame
            A pandas data frame containing the necessary x and y coordinates
            for a diamond
        """
        # A unit diamond's bounding box is described by going along the
        # following path:
        # (-0.5,  0.0)
        # ( 0.0, -0.5)
        # ( 0.5,  0.0)
        # ( 0.0, -0.5)
        # (-0.5,  0.0)
        #
        # This is the path that a diamond feature will also trace, with the
        # appropriate height and width
        diamond_pts = pd.DataFrame({
            'x': [
                center[0] - width / 2,
                center[0],
                center[0] + width / 2,
                center[0],
                center[0] - width / 2
            ],

            'y': [
                center[1],
                center[1] - height / 2,
                center[1],
                center[1] + height / 2,
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

        transform : matplotlib.Transform or None (default: None)

        Returns
        -------
        patch : matplotlib.patches.Patch
            The patch object that contains the feature. The patch is added to
            the Axes object
        """
        # Set the transformation to be data coordinates if none is passed
        if not transform:
            transform = ax.transData

        # Get the feature's matplotlib.Polygon
        patch = self.create_feature_mpl_polygon()

        # Add the patch to the Axes object
        patch = ax.add_patch(patch)

        # Set the transformation of the patch
        patch.set_transform(transform)

        return patch


class TeamLogo(BaseFeature):
    """A base class for a team's logo.

    Team logos are pulled directly from league sources as SVG files.

    Attributes
    ----------
    logo_path : str
        A path or link to the image to use for the team's logo

    bbox_shape : str (default: 'rect')
        The shape that forms the boundary of the image. This can be either
        'circ', 'circle', or 'round' for circularly-bounded logos, or 'rect' or
        'square' for box-bounded logos

    rotation : float (default: 0.0)
        The amount by which to rotate the logo

    extent : list (default: []; an empty list)
        The margins (in plot coordinates) of the logo's bounding box
    """

    def __init__(self, logo_path, bbox_shape = 'rect', rotation = 0.0,
                 extent = [], **polygon_kwargs):
        self.logo_path = logo_path
        self.rotation = rotation
        self.extent = extent
        self.bbox_shape = bbox_shape.lower()

        super().__init__(**polygon_kwargs)

    def draw(self, ax, transform = None):
        """Draw the logo onto the surface.

        Parameters
        ----------
        ax : matplotlib.Axes
            Axes object onto which the logo should be drawn

        transform : matplotlib.Transform
            The transformation to apply to the logo

        Returns
        -------
        logo : matplotlib.AxesImage
            The logo to be added
        """
        if not self.visible:
            return None

        if transform is None:
            transform = ax.transData

        try:
            # Start by reading in the logo file
            logo_img = plt.imread(self.path)

            x = self.x * self.x_reflection
            y = self.y * self.y_reflection

            # Set the bounding box
            if self.extent == []:
                if self.bbox_shape in ['circ', 'circle', 'round']:
                    extent = [
                        int(x - self.radius),
                        int(x + self.radius),
                        int(y - self.radius),
                        int(y + self.radius)
                    ]

                else:
                    # Default to a 10x10 square
                    extent = [
                        int(x - 10),
                        int(x + 10),
                        int(y - 10),
                        int(y + 10)
                    ]

            # Add the logo to the axes
            logo = ax.imshow(logo_img, extent = extent, **self.polygon_kwargs)

            # Set the clip if it's constrained to be inside a circle
            if self.bbox_shape in ['circ', 'circle', 'round']:
                patch = plt.Circle(
                    (x, y),
                    radius = self.radius,
                    transform = transform
                )

                logo.set_clip_path(patch)

            return logo

        except Exception as e:
            print(e)

            return None
