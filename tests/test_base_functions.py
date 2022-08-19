"""Tests for the coordinate transformation capabilities of the module.

@author: Ross Drucker
"""

import pandas as pd
import pandas.testing as pdtest
import sportypy._base_functions._coordinate_transformations as transform


def test_reflect():
    """Test the mathematical reflection function.

    This test should pass so long as the reflect() function performs a
    mathematical reflection of a data frame over a specified axis. This will be
    tested by reflecting points over the x axis, the y axis, and both axes
    simultaneously.
    """
    test_data = pd.DataFrame({
        "x": [
            1.0,
            2.0,
            3.0
        ],

        "y": [
            1.0,
            2.0,
            3.0
        ]
    })

    expected_x_only = pd.DataFrame({
        "x": [
            1.0,
            2.0,
            3.0
        ],

        "y": [
            -1.0,
            -2.0,
            -3.0
        ]
    })

    expected_y_only = pd.DataFrame({
        "x": [
            -1.0,
            -2.0,
            -3.0
        ],

        "y": [
            1.0,
            2.0,
            3.0
        ]
    })

    expected_x_and_y = pd.DataFrame({
        "x": [
            -1.0,
            -2.0,
            -3.0
        ],

        "y": [
            -1.0,
            -2.0,
            -3.0
        ]
    })

    test_x_only = transform.reflect(test_data, over_x = True, over_y = False)
    test_y_only = transform.reflect(test_data, over_x = False, over_y = True)
    test_x_and_y = transform.reflect(test_data, over_x = True, over_y = True)

    pdtest.assert_frame_equal(test_x_only, expected_x_only)
    pdtest.assert_frame_equal(test_y_only, expected_y_only)
    pdtest.assert_frame_equal(test_x_and_y, expected_x_and_y)


def test_rotate():
    """Test the mathematical rotation function.

    This test should pass so long as the rotate() function performs a
    mathematical rotation of a data frame about a specified point. This will be
    tested by rotating the point (1.0, 1.0) about the coordinate axis origin.
    """
    test_data = pd.DataFrame({
        "x": [
            1.0
        ],

        "y": [
            0.0
        ]
    })

    expected_ccw = pd.DataFrame({
        "x": [
            0.0
        ],

        "y": [
            1.0
        ]
    })

    expected_cw = pd.DataFrame({
        "x": [
            0.0
        ],

        "y": [
            -1.0
        ]
    })

    test_ccw = transform.rotate(test_data, rotation_dir = "ccw", angle = 0.5)
    test_cw = transform.rotate(test_data, rotation_dir = "cw", angle = 0.5)

    pdtest.assert_frame_equal(test_ccw, expected_ccw)
    pdtest.assert_frame_equal(test_cw, expected_cw)


def test_translate():
    """Test the mathematical translation function.

    This test should pass so long as the translate() function performs a
    mathematical translation of the points in a data frame. This will be tested
    by translating points over the x axis, the y axis, and both axes
    simultaneously.
    """
    test_data = pd.DataFrame({
        "x": [
            1.0,
            2.0,
            3.0
        ],

        "y": [
            1.0,
            2.0,
            3.0
        ]
    })

    expected_x_only = pd.DataFrame({
        "x": [
            2.0,
            3.0,
            4.0
        ],

        "y": [
            1.0,
            2.0,
            3.0
        ]
    })

    expected_y_only = pd.DataFrame({
        "x": [
            1.0,
            2.0,
            3.0
        ],

        "y": [
            2.0,
            3.0,
            4.0
        ]
    })

    expected_x_and_y = pd.DataFrame({
        "x": [
            2.0,
            3.0,
            4.0
        ],

        "y": [
            2.0,
            3.0,
            4.0
        ]
    })

    test_x_only = transform.translate(
        test_data,
        translate_x = 1.0,
        translate_y = 0.0
    )

    test_y_only = transform.translate(
        test_data,
        translate_x = 0.0,
        translate_y = 1.0
    )

    test_x_and_y = transform.translate(
        test_data,
        translate_x = 1.0,
        translate_y = 1.0
    )

    pdtest.assert_frame_equal(test_x_only, expected_x_only)
    pdtest.assert_frame_equal(test_y_only, expected_y_only)
    pdtest.assert_frame_equal(test_x_and_y, expected_x_and_y)


def test_scale():
    """Test the mathematical scaling function.

    This test should pass so long as the scale() function performs a
    mathematical scaling of the points in a data frame. This will be tested by
    translating points over the x axis, the y axis, and both axes
    simultaneously.
    """
    test_data = pd.DataFrame({
        "x": [
            1.0,
            2.0,
            3.0
        ],

        "y": [
            1.0,
            2.0,
            3.0
        ]
    })

    expected_scale = pd.DataFrame({
        "x": [
            2.0,
            4.0,
            6.0
        ],

        "y": [
            2.0,
            4.0,
            6.0
        ]
    })

    test_scale = transform.scale(
        test_data,
        scale_factor = 2.0
    )

    pdtest.assert_frame_equal(test_scale, expected_scale)
