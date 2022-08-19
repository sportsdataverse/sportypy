"""Tests for the shape-drawing capabilities of the module.

@author: Ross Drucker
"""

import numpy as np
import pandas as pd
import pandas.testing as pdtest
import sportypy._base_functions._base_shapes as shapes


def test_circle():
    """Test the circle-drawing function.

    This test should pass so long as the circle() function draws the unit
    circle. This is checked by looking at the radius of each point in the
    resulting data frame, which should be 1.0.
    """
    test_circle = shapes.circle()
    test_circle["radius"] = np.sqrt(
        (test_circle["x"] ** 2) + (test_circle["y"] ** 2)
    )

    n_bad = test_circle[
        (test_circle["radius"] < .999) & (test_circle["radius"] > 1)
    ]["radius"].sum()

    assert n_bad == 0.0


def test_rectangle():
    """Test the rectangle-drawing function.

    This test should pass so long as the rectangle() function draws a rectangle
    with length 2 and height 1 (i.e. stretching from -1 to +1 along x and -0.5
    to 0.5 along y)
    """
    expected_rectangle = pd.DataFrame({
        "x": [
            -1.0,
            1.0,
            1.0,
            -1.0,
            -1.0
        ],

        "y": [
            -0.5,
            -0.5,
            0.5,
            0.5,
            -0.5
        ]
    })

    test_rectangle = shapes.rectangle(
        x_min = -1.0,
        x_max = 1.0,
        y_min = -0.5,
        y_max = 0.5
    )

    pdtest.assert_frame_equal(test_rectangle, expected_rectangle)


def test_square():
    """Test the square-drawing function.

    This test should pass so long as the square() function draws a unit square
    centered at (0.0, 0.0)
    """
    expected_square = pd.DataFrame({
        "x": [
            -0.5,
            0.5,
            0.5,
            -0.5,
            -0.5
        ],

        "y": [
            -0.5,
            -0.5,
            0.5,
            0.5,
            -0.5
        ]
    })

    test_square = shapes.square(
        side_length = 1.0
    )

    pdtest.assert_frame_equal(test_square, expected_square)


def test_diamond():
    """Test the diamond-drawing function.

    This test should pass so long as the diamond() function draws a diamond
    with height 1 and width 1 (i.e. with a vertex at 1 on each axis around
    the origin).
    """
    expected_diamond = pd.DataFrame({
        "x": [
            -0.5,
            0.0,
            0.5,
            0.0,
            -0.5
        ],

        "y": [
            0.0,
            -0.5,
            0.0,
            0.5,
            0.0
        ]
    })

    test_diamond = shapes.diamond(
        height = 1.0,
        width = 1.0
    )

    pdtest.assert_frame_equal(test_diamond, expected_diamond)


def test_triangle():
    """Test the triangle-drawing function.

    This test should pass so long as the triangle() function draws a triangle
    with base 1 and height 1.
    """
    expected_triangle = pd.DataFrame({
        "x": [
            0.0,
            0.5,
            1.0,
            0.0
        ],

        "y": [
            0.0,
            1.0,
            0.0,
            0.0
        ]
    })

    test_triangle = shapes.triangle(
        base = 1.0,
        height = 1.0
    )

    pdtest.assert_frame_equal(test_triangle, expected_triangle)
