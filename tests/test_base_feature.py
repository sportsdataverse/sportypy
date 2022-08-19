"""Tests for the BaseFeature class of the module.

@author: Ross Drucker
"""
import pandas as pd
import pandas.testing as pdtest
from sportypy._base_classes._base_feature import BaseFeature

def test_diamond_points():
    class DiamondFeature(BaseFeature):
        def _get_centered_feature(self):
            diamond_df = self.create_diamond(
                height = 1.0,
                width = 1.0
            )

            return diamond_df
    
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

    test_diamond = DiamondFeature()._get_centered_feature()

    pdtest.assert_frame_equal(test_diamond, expected_diamond)
