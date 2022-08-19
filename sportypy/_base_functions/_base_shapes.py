"""Functions to generate data frames of points that form geometric shapes.

@author: Ross Drucker
"""
import numpy as np
import pandas as pd


def circle(center = (0.0, 0.0), npoints = 1000, d = 2.0, start = 0.0,
           end = 2.0):
    """Create a set of x and y coordinates that form a circle or arc.

    Parameters
    ----------
    center : tuple (default: (0.0, 0.0)
        The (x, y) coordinates of the center of the circle

    npoints : int (default: 1000)
        The number of points with which to create the circle. This will also be
        the length of the resulting data frame

    d : float (default: 2.0; a unit circle)
        Diameter of the circle IN THE UNITS OF THE PLOT. This default unit will
        be feet

    start : float (default: 0.0)
        The angle (in radians) at which to start drawing the circle, where zero
        runs along the +x axis

    end : float (default: 2.0)
        The angle (in radians) at which to stop drawing the circle, where zero
        runs along the +x axis

    Returns
    -------
    circle_df : pandas.DataFrame
        The circle's coordinate points
    """
    # Create a vector of numbers that are evenly spaced apart between the
    # starting and ending angles. They should be multiplied by pi to be in
    # radians. This vector represents the angle through which the circle is
    # traced
    pts = np.linspace(start * np.pi, end * np.pi, npoints)

    # Create the vectors x and y that represent the circle (or arc of a circle)
    # to be created. This is a translation away from the center across (d/2),
    # then rotated by cos(angle) and sin(angle) for x and y respectively.
    x = center[0] + ((d / 2.0) * np.cos(pts))
    y = center[1] + ((d / 2.0) * np.sin(pts))

    # Combine points into data frame for output
    circle_df = pd.DataFrame({
        "x": x,
        "y": y
    })

    return circle_df


def rectangle(x_min, x_max, y_min, y_max):
    """Generate a bounding box for a rectangle.

    Parameters
    ----------
    x_min : float
        The lower of the two x coordinates

    x_max : float
        The higher of the two x coordinates

    y_min : float
        The lower of the two y coordinates

    y_max : float
        The higher of the two y coordinates

    Returns
    -------
    rect_pts : pandas.DataFrame
        The rectangle's bounding box coordinates
    """
    # A rectangle's bounding box is described by going along the following path
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


def square(side_length, center = (0.0, 0.0)):
    """Generate a bound box for a square.

    Parameters
    ----------
    side_length : float
        The length of the side of the square

    center : tuple (default: (0.0, 0.0))
        Where to center the square

    Returns
    -------
    square_pts : pandas.DataFrame
        The square's bounding box coordinates
    """
    # A square's bounding box is described by going along the following path
    square_pts = pd.DataFrame({
        "x": [
            center[0] - side_length / 2.0,
            center[0] + side_length / 2.0,
            center[0] + side_length / 2.0,
            center[0] - side_length / 2.0,
            center[0] - side_length / 2.0
        ],

        "y": [
            center[1] - side_length / 2.0,
            center[1] - side_length / 2.0,
            center[1] + side_length / 2.0,
            center[1] + side_length / 2.0,
            center[1] - side_length / 2.0,
        ]
    })

    return square_pts


def diamond(height, width, center = (0.0, 0.0)):
    """Generate a bound box for a diamond.

    Parameters
    ----------
    height : float
        The vertical height of the diamond

    width : float
        The horizontal width of the diamond

    center : tuple (default: (0.0, 0.0))
        Where to center the diamond

    Returns
    -------
    diamond_pts : pandas.DataFrame
        The diamond's bounding box coordinates
    """
    # A diamond's bounding box is described by going along the following path
    diamond_pts = pd.DataFrame({
        "x": [
            center[0] - width / 2.0,
            center[0],
            center[0] + width / 2.0,
            center[0],
            center[0] - width / 2.0
        ],

        "y": [
            center[1],
            center[1] - height / 2.0,
            center[1],
            center[1] + height / 2.0,
            center[1]
        ]
    })

    return diamond_pts


def triangle(base = 1.0, height = 1.0):
    """Generate the boundary of a triangle.

    Parameters
    ----------
    base : float (default: 1.0)
        When the tip of the triangle is pointing upwards, this is the length of
        the flat side (opposite the upward-pointing side)

    height : float (default: 1.0)
        When the tip of the triangle is pointing upwards, this is the distance
        from the tip of the upward-pointing corner to the base

    Returns
    -------
    triangle_pts : pandas.DataFrame
        The triangle's bounding coordinates
    """
    # A triangle's bounding coordinates are described by going along the
    # following path
    triangle_pts = pd.DataFrame({
        "x": [
            0.0,
            0.5 * base,
            base,
            0.0
        ],

        "y": [
            0.0,
            height,
            0.0,
            0.0
        ]
    })

    return triangle_pts
