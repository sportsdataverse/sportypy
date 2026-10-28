"""Tests for the BaseSurface class of the module.

@author: Ross Drucker
"""
from sportypy._base_classes._base_surface import BaseSurface

def test_base_surface():
    """Test that a generic BaseSurface class instance can be instantiated.

    This test ensures that the BaseSurface class can be instantiated after
    arbitrarily defining a child class, TestSubclass, that calls the __init__
    method of the BaseSurface class
    """
    class TestSubclass(BaseSurface):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def _get_plot_range_limits(self):
            pass

    test_subclass = TestSubclass()

    assert isinstance(test_subclass, TestSubclass)


def test_surface_params_without_a_params_attribute():
    """Test that a surface with no ``*_params`` attribute has empty params.

    The fallback returns an empty dict and the generic ``units`` key
    """
    class TestSubclass(BaseSurface):
        def _get_plot_range_limits(self):
            pass

    assert TestSubclass()._surface_params() == ({}, "units")
