"""Mathematical transformations on geometric shapes/points.

Module to perform basic coordinate transformations to aid in creating a
playing surface

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd


def reflect(df, over_x = False, over_y = True):
    """Mathematical reflection over a specified axis.

    Parameters
    ----------
    df : pandas.DataFrame
        A data frame of coordinates with an "x" column and a "y" column

    over_x : bool
        Whether or not to reflect the coordinates over the x axis

    over_y : bool
        Whether or not to reflect the coordinates over the y axis

    Returns
    -------
    out : pandas.DataFrame
        The reflected pandas data frame
    """
    # Make a copy of the original dataframe on which to operate
    reflected = df.copy()

    # If a reflection over the x axis is required, perform it
    if over_y:
        reflected = pd.DataFrame({
            "x": -1 * reflected["x"],
            "y": reflected["y"]
        })

    # If a reflection over the y axis is required, perform it
    if over_x:
        reflected = pd.DataFrame({
            "x": reflected["x"],
            "y": -1 * reflected["y"]
        })

    return reflected


def rotate(df, rotation_dir = 'ccw', angle = 0.5):
    """Mathematical rotation about (0.0, 0.0).

    This rotation is given as:
        x' = x * cos(theta) - y * sin(theta)
        y' = x * sin(theta) + y * cos(theta)

    Parameters
    ----------
    df : pandas.DataFrame
        A data frame of coordinates with an "x" column and a "y" column

    rotation_dir : str (default: 'ccw')
        The direction of rotation direction. 'ccw' corresponds to
        counterclockwise

    angle : float (default: 0.5)
        The angle (in radians) by which to rotate the coordinates, divided by
        pi

    Returns
    -------
    rotated : pandas.DataFrame
        The rotated pandas data frame
    """
    # If the rotation direction is clockwise, take the negative of the angle
    if rotation_dir.lower() not in ['ccw', 'counter', 'counterclockwise']:
        angle *= -1.0

    # Set theta to be the angle of rotation
    theta = angle * np.pi

    # Make a copy of the original dataframe on which to operate
    rotated = df.copy()
    rotated["x"] = (df["x"] * math.cos(theta)) - (df["y"] * math.sin(theta))
    rotated["y"] = (df["x"] * math.sin(theta)) + (df["y"] * math.cos(theta))

    return rotated


def translate(df, translate_x = 0.0, translate_y = 0.0):
    """Mathematical translation of coordinates.

    Parameters
    ----------
    df : pandas.DataFrame
        A data frame of coordinates with an "x" column and a "y" column

    translate_x : float (default: 0.0)
        How many units (in the input dataframe's units) to translate the points
        in the +x direction

    translate_y: float (default: 0.0)
        How many units (in the input dataframe's units) to translate the points
        in the +y direction

    Returns
    -------
    translated : pandas.DataFrame
        The translated pandas data frame
    """
    # Make a copy of the original dataframe on which to operate
    translated = df.copy()

    # Translate the x and y coordinates
    translated["x"] = translated["x"] + translate_x
    translated["y"] = translated["y"] + translate_y

    return translated


def scale(df, scale_factor = 1.0):
    """Mathematical scaling of coordinates.

    Parameters
    ----------
    df : pandas.DataFrame
        A data frame of coordinates with an "x" column and a "y" column

    scale_factor : float (default: 1.0)
        The factor by which to scale the coordinates

    Returns
    -------
    scaled : pandas.DataFrame
        The scaled pandas data frame
    """
    # Make a copy of the original dataframe on which to operate
    scaled = df.copy()

    # Scale the x and y coordinates
    scaled["x"] = scale_factor * scaled["x"]
    scaled["y"] = scale_factor * scaled["y"]

    return scaled
