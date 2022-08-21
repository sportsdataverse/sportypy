"""Tests for the baseball field classes of the module.

@author: Ross Drucker
"""

import io
import sys
import math
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import sportypy.surfaces.baseball as baseball_fields
import sportypy._feature_classes.baseball as baseball_features


def test_base_class_no_league():
    """Test that the base class, BaseballField, can be instantiated.

    This test should pass so long as the BaseballField class can be
    successfully instantiated without a league passed to it. This should create
    an instance of BaseballField with the field_params attribute as an empty
    dictionary
    """
    test_field = baseball_fields.BaseballField()

    assert test_field.field_params == {}


def test_mlb_params():
    """Test that the MLBField class can be instantiated.

    This test should pass so long as the MLBField class can be successfully
    instantiated with the correct parameters.
    """
    mlb_params = {
        "field_units": "ft",

        "left_field_distance": 355.0,
        "right_field_distance": 355.0,
        "center_field_distance": 400.0,

        "baseline_distance": 90.0,

        "running_lane_start_distance": 45.0,
        "running_lane_depth": 3.0,
        "running_lane_length": 48.0,

        "pitchers_mound_center_to_home_plate": 59.0,
        "pitchers_mound_radius": 9.0,
        "pitchers_plate_front_to_home_plate": 60.5,
        "pitchers_plate_width": 0.5,
        "pitchers_plate_length": 2.0,

        "base_side_length": 1.25,
        "home_plate_edge_length": 1.4167,

        "infield_arc_radius": 95.0,
        "base_anchor_to_infield_grass_radius": 13.0,

        "line_width": 0.25,
        "foul_line_to_infield_grass": 3.0,
        "foul_line_to_foul_grass": 3.0,

        "batters_box_length": 6.0,
        "batters_box_width": 4.0,
        "batters_box_y_adj": 0.7083,
        "home_plate_side_to_batters_box": 0.5,
        "catchers_box_depth": 8.0,
        "catchers_box_width": 3.5833,

        "backstop_radius": 60.0,
        "home_plate_circle_radius": 13.0
    }

    test_params = baseball_fields.MLBField().field_params

    assert mlb_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a BaseballField() object to use for testing
    test_field = baseball_fields.BaseballField()

    # Get the available league codes
    available_league_codes = [k for k in test_field.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following baseball leagues are available with sportypy:\n"
    )

    for league_code in available_league_codes[:-1]:
        new_league = f"- {league_code.upper()}"
        exp_pl_empty_league_code = f"{exp_pl_empty_league_code}\n{new_league}"

    exp_pl_empty_league_code = (f"{exp_pl_empty_league_code}\n"
                                f"- {available_league_codes[-1].upper()}\n")

    # Initialize the output-capture
    pl_empty_league_code = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_empty_league_code
    test_field.cani_plot_leagues()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_empty_league_code.getvalue() == exp_pl_empty_league_code


def test_cani_plot_leagues_mlb():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "mlb", "MLB", or any combination of capitalized and
    lower-case letters of "M", "L", and "B", this should return the same
    message
    """
    # Create a BaseballField() object to use for testing
    test_field = baseball_fields.BaseballField()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use MLB as a test)
    exp_pl_mlb_league_code = "MLB comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_mlb_league_code_lower = io.StringIO()
    pl_mlb_league_code_upper = io.StringIO()
    pl_mlb_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_mlb_league_code_lower
    test_field.cani_plot_leagues("mlb")

    sys.stdout = pl_mlb_league_code_upper
    test_field.cani_plot_leagues("MLB")

    sys.stdout = pl_mlb_league_code_mixed
    test_field.cani_plot_leagues("MlB")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_mlb_league_code_lower.getvalue() == exp_pl_mlb_league_code
    assert pl_mlb_league_code_upper.getvalue() == exp_pl_mlb_league_code
    assert pl_mlb_league_code_mixed.getvalue() == exp_pl_mlb_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a BaseballField() object to use for testing
    test_field = baseball_fields.BaseballField()

    # Generate the expected output for cani_plot_leagues() with an invalid
    # league code (this will use test_league as a test)
    exp_pl_bad_league_code = (
        "TEST_LEAGUE does not come with sportypy, but may be parameterized. "
        "Use the cani_change_dimensions() to check what parameters are needed."
        "\n"
    )

    # Initialize the output-capture
    pl_bad_league_code = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_bad_league_code
    test_field.cani_plot_leagues("test_league")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_bad_league_code.getvalue() == exp_pl_bad_league_code


def test_cani_change_dimensions():
    """Test cani_change_dimensions() method will return appropriate message.

    When called, this should return a list of the parameterizations of the
    field that may be changed by a user
    """
    # Create a BaseballField() object to use for testing
    test_field = baseball_fields.MLBField()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the field_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- field_units (ft)\n"
        "- left_field_distance (355.0)\n"
        "- right_field_distance (355.0)\n"
        "- center_field_distance (400.0)\n"
        "- baseline_distance (90.0)\n"
        "- running_lane_start_distance (45.0)\n"
        "- running_lane_depth (3.0)\n"
        "- running_lane_length (48.0)\n"
        "- pitchers_mound_center_to_home_plate (59.0)\n"
        "- pitchers_mound_radius (9.0)\n"
        "- pitchers_plate_front_to_home_plate (60.5)\n"
        "- pitchers_plate_width (0.5)\n"
        "- pitchers_plate_length (2.0)\n"
        "- base_side_length (1.25)\n"
        "- home_plate_edge_length (1.4167)\n"
        "- infield_arc_radius (95.0)\n"
        "- base_anchor_to_infield_grass_radius (13.0)\n"
        "- line_width (0.25)\n"
        "- foul_line_to_infield_grass (3.0)\n"
        "- foul_line_to_foul_grass (3.0)\n"
        "- batters_box_length (6.0)\n"
        "- batters_box_width (4.0)\n"
        "- batters_box_y_adj (0.7083)\n"
        "- home_plate_side_to_batters_box (0.5)\n"
        "- catchers_box_depth (8.0)\n"
        "- catchers_box_width (3.5833)\n"
        "- backstop_radius (60.0)\n"
        "- home_plate_circle_radius (13.0)\n"
        "\n"
        "These parameters may be updated with the update_field_params() "
        "method\n"
    )

    # Initialize the output-capture
    change_dimensions = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = change_dimensions
    test_field.cani_change_dimensions()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert change_dimensions.getvalue() == exp_change_dimensions


def test_cani_color_features():
    """Test cani_color_features() method will return appropriate message.

    When called, this should return a list of the field's features and their
    default/standard colors
    """
    # Create a BaseballField() object to use for testing
    test_field = baseball_fields.BaseballField()

    # Generate the expected output for cani_color_features()
    exp_color_features = (
        "The following features can be colored via the color_updates "
        "parameter, with the current value in parenthesis:\n"
    )

    for k, v in test_field.feature_colors.items():
        exp_color_features = f"{exp_color_features}\n- {k} ({v})"

    exp_color_features = (
        f"{exp_color_features}\n\nThese colors may be updated with the "
        "update_colors() method\n"
    )

    # Initialize the output-capture
    color_features = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = color_features
    test_field.cani_color_features()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert color_features.getvalue() == exp_color_features


def test_update_colors():
    """Test that update_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called
    """
    # Create a sample MLB field to operate on
    test_mlb = baseball_fields.MLBField()

    # Get the standard colors for an MLB field. These will be used for
    # comparison
    standard_colors = test_mlb.feature_colors

    # Update a color. Home plate is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to red
    test_mlb.update_colors({"foul_line": "#c8102e"})

    # Get the updated colors
    updated_colors = test_mlb.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working
    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample MLB field to operate on
    test_mlb = baseball_fields.MLBField()

    # Get the standard colors for an MLB field. These will be used for
    # comparison
    standard_colors = test_mlb.feature_colors

    # Update a color. Home plate is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to red
    test_mlb.update_colors({"foul_line": "#c8102e"})

    # Get the updated colors
    updated_colors = test_mlb.feature_colors

    # Now, change the colors back to the original
    test_mlb.reset_colors()

    # Get the final colors
    final_colors = test_mlb.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_field_params():
    """Test that update_field_params() method operates as expected.

    This should work as long as the internal field parameters dictionary is
    updated when this method is called
    """
    # Create a sample MLB field to operate on
    test_mlb = baseball_fields.MLBField()

    # Get the standard dimensions for an MLB field. These will be used for
    # comparison
    standard_dimensions = test_mlb.field_params

    # Update a dimension. The baseline distances are what are updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 90 feet to 200 feet
    test_mlb.update_field_params({"baseline_distance": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_mlb.field_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_field_params():
    """Test that reset_field_params() method operates as expected.

    This should work as long as the internal field parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample MLB field to operate on
    test_mlb = baseball_fields.MLBField()

    # Get the standard dimensions for an MLB field. These will be used for
    # comparison
    standard_dimensions = test_mlb.field_params

    # Update a dimension. The baseline distances are what are updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 90 feet to 200 feet
    test_mlb.update_field_params({"baseline_distance": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_mlb.field_params

    # Now, change the dimensions back to the original
    test_mlb.reset_field_params()

    # Get the final dimensions
    final_dimensions = test_mlb.field_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the fields' coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation MLB field. This should work for any of the
    # leagues supported by sportypy, but MLB is chosen out of convenience
    test_field_to_convert = baseball_fields.MLBField()

    # Generate a field originating in meters
    mlb_field_m = baseball_fields.MLBField(units = "m")

    # Convert the field dimensions from feet to meters
    field_params_to_convert = test_field_to_convert.field_params

    for k, v in field_params_to_convert.items():
        field_params_to_convert[k] = test_field_to_convert._convert_units(
            v,
            "ft",
            "m"
        )

    # Convert the units to be meters
    field_params_to_convert["field_units"] = "m"

    assert field_params_to_convert == mlb_field_m.field_params


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "little_league": baseball_fields.LittleLeagueField(),
        "milb": baseball_fields.MiLBField(),
        "mlb": baseball_fields.MLBField(),
        "ncaa": baseball_fields.NCAAField(),
        "nfhs": baseball_fields.NFHSField(),
        "pony": baseball_fields.PonyField()
    }

    field = baseball_fields.BaseballField()

    leagues = [k.lower() for k in field.league_dimensions.keys()]

    missing_leagues = [
        league
        for league in leagues
        if league not in league_class_dict.keys()
    ]

    if len(missing_leagues) > 0:
        print("The following leagues are not tested:\n")
        for league in missing_leagues:
            print(f"- {league}")

    else:
        for league in league_class_dict.keys():
            test_field = league_class_dict[league]

            assert isinstance(test_field, baseball_fields.BaseballField)


def test_custom_field_params():
    """Test that custom fields are able to be created.

    This test should pass so long as the fields' parameters are valid
    """
    # Start by defining the customized field parameters. These are a blending
    # of Little League and MLB field parameters
    field_parameters = {
        "field_units": "ft",

        "left_field_distance": 355.0,
        "right_field_distance": 355.0,
        "center_field_distance": 400.0,

        "baseline_distance": 90.0,

        "running_lane_start_distance": 45.0,
        "running_lane_depth": 3.0,
        "running_lane_length": 48.0,

        "pitchers_mound_center_to_home_plate": 46.0,
        "pitchers_mound_radius": 5.0,
        "pitchers_plate_front_to_home_plate": 47.0,
        "pitchers_plate_width": 0.5,
        "pitchers_plate_length": 2.0,

        "base_side_length": 1.25,
        "home_plate_edge_length": 1.4167,

        "infield_arc_radius": 95.0,
        "base_anchor_to_infield_grass_radius": 13.0,

        "line_width": 0.25,
        "foul_line_to_infield_grass": 3.0,
        "foul_line_to_foul_grass": 3.0,

        "batters_box_length": 6.0,
        "batters_box_width": 4.0,
        "batters_box_y_adj": 0.7083,
        "home_plate_side_to_batters_box": 0.5,
        "catchers_box_shape": "trapezoid",
        "catchers_box_depth": 8.0,
        "catchers_box_width": 3.5833,

        "backstop_radius": 60.0,
        "home_plate_circle_radius": 9.0
    }

    color_updates = {
        "plot_background": "#9b7653",
        "infield_dirt": "#395d33",
        "infield_grass": "#9b7653",
        "pitchers_mound": "#395d33",
        "base": "#c8102e",
        "pitchers_plate": "#c8102e",
        "batters_box": "#c8102e",
        "catchers_box": "#c8102e",
        "foul_line": "#c8102e",
        "running_lane": "#c8102e"
    }

    test_field = baseball_fields.BaseballField(
        field_updates = field_parameters,
        color_updates = color_updates
    )

    assert isinstance(test_field, baseball_fields.BaseballField)


def test_field_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the fields' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = baseball_fields.MLBField().draw(ax = ax, rotation = 90.0)

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_field_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the fields' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_field = baseball_fields.MLBField()
    ax1 = test_field.draw(xlim = (-355.0, 355.0), ylim = (-355.0, 355.0))
    ax2 = test_field.draw(xlim = (355.0, -355.0), ylim = (355.0, -355.0))
    ax3 = test_field.draw(xlim = (0.0, 0.0), ylim = (0.0, 0.0))

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
    assert isinstance(ax3, matplotlib.axes.SubplotBase)


def test_field_plot_singular_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the fields' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_field = baseball_fields.MLBField()
    ax1 = test_field.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_field.draw(xlim = -150.0, ylim = 50.0)

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the field.

    This test should pass so long as an additional feature may be added to the
    field plot. The additional feature tested here is arbitrarily selected to
    be a safety base located next to first base
    """
    safety_base = {
        "class": baseball_features.Base,
        "x_anchor": (
            (90.0 * math.cos(np.pi / 4.0)) +
            (1.25 * math.cos(np.pi / 4.0))
        ),
        "y_anchor": (
            (90.0 * math.cos(np.pi / 4.0)) -
            (1.25 * math.cos(np.pi / 4.0))
        ),
        "base_side_length": 1.25,
        "adjust_x_left": True,
        "visible": True,
        "facecolor": "#c8102e",
        "edgecolor": None,
        "zorder": 1
    }

    ax = baseball_fields.MLBField(
        new_feature_1 = safety_base
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_zero_radii():
    """Test that field features work even with a radius of 0.0.

    This test should pass so long as the errors are handled correctly when a
    curved feature is created but the radius is 0.0
    """
    field_updates = {
        "infield_arc_radius": 0.0,
        "pitchers_mound_radius": 0.0,
        "home_plate_circle_radius": 0.0,
        "base_anchor_to_infield_grass_radius": 0.0
    }

    ax = baseball_fields.LittleLeagueField(
        field_updates = field_updates
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_field_plot_with_xlim_ylim():
    """Test that field sections can be drawn (e.g. offensive half-field).

    This test should pass so long as there are no errors when drawing a section
    of the field
    """
    ax1 = baseball_fields.MLBField().draw(
        display_range = "infield"
    )

    ax2 = baseball_fields.MLBField().draw(
        xlim = 350.0,
        ylim = 500.0
    )

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = baseball_fields.MLBField(rotation = 90).draw(
        display_range = "infield"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the field defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a field
    with no specified display range
    """
    ax1 = baseball_fields.MLBField().draw(display_range = None)
    ax2 = baseball_fields.MLBField().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
