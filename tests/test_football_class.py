"""Tests for the football field classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.football as football_fields
import sportypy._feature_classes.football as football_features


def test_base_class_no_league():
    """Test that the base class, footballfield, can be instantiated.

    This test should pass so long as the footballfield class can be
    successfully instantiated without a league passed to it. This should create
    an instance of footballfield with the field_params attribute as an empty
    dictionary
    """
    test_field = football_fields.FootballField()

    assert test_field.field_params == {}


def test_nfl_params():
    """Test that the NFLField class can be instantiated.

    This test should pass so long as the NFLField class can be successfully
    instantiated with the correct parameters.
    """
    nfl_params = {
        "field_units": "yd",
        "field_length": 100.0,
        "field_width": 53.3333,
        "endzone_length": 10.0,
        "extra_apron_padding": 2.0,

        "minor_line_thickness": 0.1111,
        "goal_line_thickness": 0.2222,
        "boundary_line_thickness": 2.0,
        "minor_yard_line_height": 0.6667,
        "field_border_thickness": 1.3333,
        "field_border_behind_bench": True,

        "major_yard_line_distance": 5.0,

        "sideline_to_major_yard_line": 0.2222,
        "inbound_cross_hashmark_length": 0.2778,
        "inbound_hashmark_separation": 6.1667,
        "inbound_cross_hashmark_separation": 6.1667,

        "sideline_to_outer_yard_line": 0.2222,

        "sideline_to_bottom_of_numbers": 12.0,
        "number_height": 2.0,

        "try_mark_distance": 2.0,
        "try_mark_width": 1.0,

        "arrow_line_dist": 10.0,
        "yard_line_to_arrow": 1.8333,
        "top_number_to_arrow": 0.4167,
        "arrow_base": 0.5,
        "arrow_length": 0.9682,
        "number_to_yard_line": 0.3333,
        "number_width": 1.3333,

        "numbers_bottom": [
            "1", "0",
            "2", "0",
            "3", "0",
            "4", "0",
            "5", "0",
            "4", "0",
            "3", "0",
            "2", "0",
            "1", "0"
        ],

        "numbers_top": [
            "0", "1",
            "0", "2",
            "0", "3",
            "0", "4",
            "0", "5",
            "0", "4",
            "0", "3",
            "0", "2",
            "0", "1"
        ],

        "number_font": "Clarendon-Regular",

        "restricted_area_width": 2.0,
        "coaching_box_width": 2.0,
        "team_bench_width": 6.0,
        "team_bench_length_field_side": 44.9861,
        "team_bench_length_back_side": 37.2639,
        "team_bench_area_border_thickness": 0.1111,
        "bench_shape": "trapezoid",
        "field_bordered": True
    }

    test_params = football_fields.NFLField().field_params

    assert nfl_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a FootballField() object to use for testing
    test_field = football_fields.FootballField()

    # Get the available league codes
    available_league_codes = [k for k in test_field.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following football leagues are available with sportypy:\n"
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


def test_cani_plot_leagues_nfl():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "nfl", "NFL", or any combination of capitalized and
    lower-case letters of "N", "F", and "L", this should return the same
    message
    """
    # Create a FootballField() object to use for testing
    test_field = football_fields.FootballField()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use NFL as a test)
    exp_pl_nfl_league_code = "NFL comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_nfl_league_code_lower = io.StringIO()
    pl_nfl_league_code_upper = io.StringIO()
    pl_nfl_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_nfl_league_code_lower
    test_field.cani_plot_leagues("nfl")

    sys.stdout = pl_nfl_league_code_upper
    test_field.cani_plot_leagues("NFL")

    sys.stdout = pl_nfl_league_code_mixed
    test_field.cani_plot_leagues("NfL")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_nfl_league_code_lower.getvalue() == exp_pl_nfl_league_code
    assert pl_nfl_league_code_upper.getvalue() == exp_pl_nfl_league_code
    assert pl_nfl_league_code_mixed.getvalue() == exp_pl_nfl_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a FootballField() object to use for testing
    test_field = football_fields.FootballField()

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
    # Create a FootballField() object to use for testing
    test_field = football_fields.NFLField()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the field_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- field_units (yd)\n"
        "- field_length (100.0)\n"
        "- field_width (53.3333)\n"
        "- endzone_length (10.0)\n"
        "- extra_apron_padding (2.0)\n"
        "- minor_line_thickness (0.1111)\n"
        "- goal_line_thickness (0.2222)\n"
        "- boundary_line_thickness (2.0)\n"
        "- minor_yard_line_height (0.6667)\n"
        "- field_border_thickness (1.3333)\n"
        "- field_border_behind_bench (True)\n"
        "- major_yard_line_distance (5.0)\n"
        "- sideline_to_major_yard_line (0.2222)\n"
        "- inbound_cross_hashmark_length (0.2778)\n"
        "- inbound_hashmark_separation (6.1667)\n"
        "- inbound_cross_hashmark_separation (6.1667)\n"
        "- sideline_to_outer_yard_line (0.2222)\n"
        "- sideline_to_bottom_of_numbers (12.0)\n"
        "- number_height (2.0)\n"
        "- try_mark_distance (2.0)\n"
        "- try_mark_width (1.0)\n"
        "- arrow_line_dist (10.0)\n"
        "- yard_line_to_arrow (1.8333)\n"
        "- top_number_to_arrow (0.4167)\n"
        "- arrow_base (0.5)\n"
        "- arrow_length (0.9682)\n"
        "- number_to_yard_line (0.3333)\n"
        "- number_width (1.3333)\n"
        "- numbers_bottom (['1', '0', '2', '0', '3', '0', '4', '0', '5', '0',"
        " '4', '0', '3', '0', '2', '0', '1', '0'])\n"
        "- numbers_top (['0', '1', '0', '2', '0', '3', '0', '4', '0', '5',"
        " '0', '4', '0', '3', '0', '2', '0', '1'])\n"
        "- number_font (Clarendon-Regular)\n"
        "- restricted_area_width (2.0)\n"
        "- coaching_box_width (2.0)\n"
        "- team_bench_width (6.0)\n"
        "- team_bench_length_field_side (44.9861)\n"
        "- team_bench_length_back_side (37.2639)\n"
        "- team_bench_area_border_thickness (0.1111)\n"
        "- bench_shape (trapezoid)\n"
        "- field_bordered (True)\n"
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

    When called, this should return a list of the football field's features and
    their default/standard colors
    """
    # Create a FootballField() object to use for testing
    test_field = football_fields.FootballField()

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
    # Create a sample NCAA field to operate on
    test_ncaa = football_fields.NCAAField()

    # Get the standard colors for an NCAA field. These will be used for
    # comparison
    standard_colors = test_ncaa.feature_colors

    # Update a color. The goal line is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to orange
    test_ncaa.update_colors({"goal_line": "#e84a27"})

    # Get the updated colors
    updated_colors = test_ncaa.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working
    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample NCAA field to operate on
    test_ncaa = football_fields.NCAAField()

    # Get the standard colors for an NCAA field. These will be used for
    # comparison
    standard_colors = test_ncaa.feature_colors

    # Update a color. The goal line is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to orange
    test_ncaa.update_colors({"goal_line": "#e84a27"})

    # Get the updated colors
    updated_colors = test_ncaa.feature_colors

    # Now, change the colors back to the original
    test_ncaa.reset_colors()

    # Get the final colors
    final_colors = test_ncaa.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_field_params():
    """Test that update_field_params() method operates as expected.

    This should work as long as the internal field parameters dictionary is
    updated when this method is called
    """
    # Create a sample NFL field to operate on
    test_nfl = football_fields.NFLField()

    # Get the standard dimensions for an NFL field. These will be used for
    # comparison
    standard_dimensions = test_nfl.field_params

    # Update a dimension. The endzone length is what's updated here as a means
    # of demonstration, but this could work for any parameter. It will be
    # changed from 10 yards to 20 yards
    test_nfl.update_field_params({"endzone_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_nfl.field_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working
    assert standard_dimensions != updated_dimensions


def test_reset_field_params():
    """Test that reset_field_params() method operates as expected.

    This should work as long as the internal field parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample NFL field to operate on
    test_nfl = football_fields.NFLField()

    # Get the standard dimensions for an NFL field. These will be used for
    # comparison
    standard_dimensions = test_nfl.field_params

    # Update a dimension. The endzone length is what's updated here as a means
    # of demonstration, but this could work for any parameter. It will be
    # changed from 10 yards to 20 yards
    test_nfl.update_field_params({"endzone_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_nfl.field_params

    # Now, change the dimensions back to the original
    test_nfl.reset_field_params()

    # Get the final dimensions
    final_dimensions = test_nfl.field_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "cfl": football_fields.CFLField(),
        "ncaa": football_fields.NCAAField(),
        "nfhs11": football_fields.NFHSField(n_players = 11),
        "nfhs9": football_fields.NFHSField(n_players = 9),
        "nfhs8": football_fields.NFHSField(n_players = 8),
        "nfhs6": football_fields.NFHSField(n_players = 6),
        "nfl": football_fields.NFLField()
    }

    field = football_fields.FootballField()

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
            test_field_plot = test_field.draw()

            assert isinstance(test_field, football_fields.FootballField)
            assert isinstance(test_field_plot, matplotlib.axes.SubplotBase)


def test_custom_field_params():
    """Test that custom fields are able to be created.

    This test should pass so long as the fields' parameters are valid
    """
    # Start by defining the customized field parameters. These are a blending
    # of NCAA and CFL field parameters
    field_parameters = {
        "field_units": "yd",
        "field_length": 100.0,
        "field_width": 53.3333,
        "endzone_length": 10.0,
        "field_border_thickness": 1.3333,
        "field_border_behind_bench": True,

        "minor_line_thickness": 0.1111,
        "goal_line_thickness": 0.1111,
        "boundary_line_thickness": 0.1111,
        "minor_yard_line_height": 0.6667,

        "major_yard_line_distance": 5.0,

        "sideline_to_major_yard_line": 0.1111,
        "inbound_cross_hashmark_length": 0.2778,
        "inbound_hashmark_separation": 13.3333,
        "inbound_cross_hashmark_separation": 13.3333,

        "sideline_to_outer_yard_line": 0.1111,

        "sideline_to_bottom_of_numbers": 7.0,
        "number_height": 2.0,

        "try_mark_distance": 3.0,
        "try_mark_width": 1.0,

        "arrow_line_dist": 10.0,
        "yard_line_to_arrow": 1.8333,
        "top_number_to_arrow": 0.4167,
        "arrow_base": 0.5,
        "arrow_length": 0.9682,
        "number_to_yard_line": 0.3333,
        "number_width": 1.3333,

        "numbers_bottom": [
            "1", "0",
            "2", "0",
            "3", "0",
            "4", "0",
            "5", "0",
            "4", "0",
            "3", "0",
            "2", "0",
            "1", "0"
        ],

        "numbers_top": [
            "0", "1",
            "0", "2",
            "0", "3",
            "0", "4",
            "0", "5",
            "0", "4",
            "0", "3",
            "0", "2",
            "0", "1"
        ],

        "number_font": "Deja Vu Sans",

        "restricted_area_width": 2.0,
        "coaching_box_width": 2.0,
        "team_bench_width": 4.0,
        "team_bench_length_field_side": 50.0,
        "team_bench_length_back_side": 50.0,
        "team_bench_area_border_thickness": 0.1111,
        "bench_shape": "rectangular",
        "field_bordered": False,
        "additional_minor_yard_lines": [-2.5, -5.0, -7.5]
    }

    test_field = football_fields.FootballField(
        field_updates = field_parameters
    )

    assert isinstance(test_field, football_fields.FootballField)


def test_field_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the fields' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = football_fields.CFLField().draw(ax = ax, rotation = 90.0)

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_field_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the fields' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_field = football_fields.NFLField()
    ax1 = test_field.draw(xlim = (-15.0, 15.0), ylim = (-15.0, 15.0))
    ax2 = test_field.draw(xlim = (15.0, -15.0), ylim = (15.0, -15.0))
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
    test_field = football_fields.NFLField()
    ax1 = test_field.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_field.draw(xlim = 150.0, ylim = 50.0)

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the field.

    This test should pass so long as an additional feature may be added to the
    field plot. The additional feature tested here is arbitrarily selected to
    be a division line shifted to either side of the field
    """
    new_division_line_1 = {
        "class": football_features.GoalLine,
        "x_anchor": 23.5,
        "y_anchor": 0.0,
        "field_length": 94.0,
        "field_width": 50.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#000000",
        "edgecolor": None,
        "zorder": 1
    }

    new_division_line_2 = {
        "class": football_features.GoalLine,
        "x_anchor": -23.5,
        "y_anchor": 0.0,
        "field_length": 94.0,
        "field_width": 50.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#000000",
        "edgecolor": None,
        "zorder": 1
    }

    ax = football_fields.CFLField(
        new_feature_1 = new_division_line_1,
        new_feature_2 = new_division_line_2
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_non_standard_NFHS():
    """Test that non-standard NFHS fields default to the 11-player dimensions.

    This test should pass so long as a high school football field specified for
    a non-standard number of players will default to the 11-player dimensions.
    For this package, "standard" is defined as being either 11, 9, 8, or 6
    players per team
    """
    nfhs_5 = football_fields.NFHSField(n_players = 5)
    test_field = football_fields.NFHSField(n_players = 11)

    assert nfhs_5.field_params == test_field.field_params


def test_alternate_numeral_font():
    """Test that alternate fonts can be used for field numerals.

    By default, the field will use Clarendon Regular as the font for field
    numbers. Because of how this rotates for the upper numbers in TV view, an
    additional shift is applied. For non-default fonts, this shift should not
    occur
    """
    # Start by defining the customized field parameters. These are a blending
    # of NCAA and CFL field parameters
    field_parameters = {
        "field_units": "yd",
        "field_length": 100.0,
        "field_width": 53.3333,
        "endzone_length": 10.0,
        "field_border_thickness": 1.3333,
        "field_border_behind_bench": False,

        "minor_line_thickness": 0.1111,
        "goal_line_thickness": 0.1111,
        "boundary_line_thickness": 0.1111,
        "minor_yard_line_height": 0.6667,

        "major_yard_line_distance": 5.0,

        "sideline_to_major_yard_line": 0.1111,
        "inbound_cross_hashmark_length": 0.2778,
        "inbound_hashmark_separation": 13.3333,
        "inbound_cross_hashmark_separation": 13.3333,

        "sideline_to_outer_yard_line": 0.1111,

        "sideline_to_bottom_of_numbers": 7.0,
        "number_height": 2.0,

        "try_mark_distance": 3.0,
        "try_mark_width": 1.0,

        "arrow_line_dist": 10.0,
        "yard_line_to_arrow": 1.8333,
        "top_number_to_arrow": 0.4167,
        "arrow_base": 0.5,
        "arrow_length": 0.9682,
        "number_to_yard_line": 0.3333,
        "number_width": 1.3333,

        "numbers_bottom": [
            "1", "0",
            "2", "0",
            "3", "0",
            "4", "0",
            "5", "0",
            "4", "0",
            "3", "0",
            "2", "0",
            "1", "0"
        ],

        "numbers_top": [
            "0", "1",
            "0", "2",
            "0", "3",
            "0", "4",
            "0", "5",
            "0", "4",
            "0", "3",
            "0", "2",
            "0", "1"
        ],

        "number_font": "Deja Vu Sans",

        "restricted_area_width": 2.0,
        "coaching_box_width": 2.0,
        "team_bench_width": 4.0,
        "team_bench_length_field_side": 50.0,
        "team_bench_length_back_side": 50.0,
        "team_bench_area_border_thickness": 0.1111,
        "bench_shape": "rectangular",
        "field_bordered": False,
        "additional_minor_yard_lines": [-2.5, -5.0, -7.5]
    }

    test_field = football_fields.FootballField(
        field_updates = field_parameters
    )

    ax = test_field.draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = football_fields.NFLField(rotation = 90).draw(
        display_range = "offense"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the field defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a field
    with no specified display range
    """
    ax1 = football_fields.NFLField().draw(display_range = None)
    ax2 = football_fields.NFLField().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
