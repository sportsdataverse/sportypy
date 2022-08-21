"""Tests for the hockey rink classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.hockey as hockey_rinks
import sportypy._feature_classes.hockey as hockey_features


def test_base_class_no_league():
    """Test that the base class, HockeyRink, can be instantiated.

    This test should pass so long as the HockeyRink class can be successfully
    instantiated without a league passed to it. This should create an instance
    of HockeyRink with the rink_params attribute as an empty dictionary
    """
    test_rink = hockey_rinks.HockeyRink()

    assert test_rink.rink_params == {}


def test_nhl_params():
    """Test that the NHLRink class can be instantiated.

    This test should pass so long as the NHLRink class can be successfully
    instantiated with the correct parameters.
    """
    nhl_params = {
        "rink_length": 200.0,
        "rink_width": 85.0,
        "rink_units": "ft",
        "corner_radius": 28.0,
        "board_thickness": 0.4167,
        "referee_crease_radius": 10.0,

        "nzone_length": 50.0,
        "goal_line_to_boards": 11.0,

        "minor_line_thickness": 0.1666,
        "major_line_thickness": 1.0,

        "faceoff_circle_radius": 15.0,
        "center_faceoff_spot_radius": 0.5,
        "noncenter_faceoff_spot_radius": 1.0,
        "nzone_faceoff_spot_to_zone_line": 5.0,
        "odzone_faceoff_spot_to_boards": 31.0,
        "noncenter_faceoff_spot_y": 22.0,
        "noncenter_faceoff_spot_gap_width": 0.25,
        "hashmark_width": 2.0,
        "hashmark_ext_spacing": 5.9166,

        "faceoff_line_dist_x": 2.0,
        "faceoff_line_dist_y": 0.75,
        "faceoff_line_length": 4.0,
        "faceoff_line_width": 3.0,

        "has_trapezoid": True,
        "short_base_width": 22.0,
        "long_base_width": 28.0,

        "goal_crease_style": "nhl98",
        "goal_crease_radius": 6.0,
        "goal_crease_length": 4.5,
        "goal_crease_width": 8.0,
        "goal_crease_notch_dist_x": 4.0,
        "goal_crease_notch_width": 0.4167,

        "goal_mouth_width": 6.0,
        "goal_back_width": 7.3333,
        "goal_depth": 3.3333,
        "goal_post_diameter": 0.1979,
        "goal_radius": 1.6666,

        "bench_length": 30.0,
        "bench_depth": 5.5,
        "bench_separation": 3.3333,

        "penalty_box_length": 8.0,
        "penalty_box_depth": 5.0,
        "penalty_box_separation": 8.0
    }

    test_params = hockey_rinks.NHLRink().rink_params

    assert nhl_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a HockeyRink() object to use for testing
    test_rink = hockey_rinks.HockeyRink()

    # Get the available league codes
    available_league_codes = [k for k in test_rink.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following hockey leagues are available with sportypy:\n"
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
    test_rink.cani_plot_leagues()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_empty_league_code.getvalue() == exp_pl_empty_league_code


def test_cani_plot_leagues_nhl():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "nhl", "NHL", or any combination of capitalized and
    lower-case letters of "N", "H", and "L", this should return the same
    message
    """
    # Create a HockeyRink() object to use for testing
    test_rink = hockey_rinks.HockeyRink()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use NHL as a test)
    exp_pl_nhl_league_code = "NHL comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_nhl_league_code_lower = io.StringIO()
    pl_nhl_league_code_upper = io.StringIO()
    pl_nhl_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_nhl_league_code_lower
    test_rink.cani_plot_leagues("nhl")

    sys.stdout = pl_nhl_league_code_upper
    test_rink.cani_plot_leagues("NHL")

    sys.stdout = pl_nhl_league_code_mixed
    test_rink.cani_plot_leagues("NhL")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_nhl_league_code_lower.getvalue() == exp_pl_nhl_league_code
    assert pl_nhl_league_code_upper.getvalue() == exp_pl_nhl_league_code
    assert pl_nhl_league_code_mixed.getvalue() == exp_pl_nhl_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a HockeyRink() object to use for testing
    test_rink = hockey_rinks.HockeyRink()

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
    test_rink.cani_plot_leagues("test_league")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_bad_league_code.getvalue() == exp_pl_bad_league_code


def test_cani_change_dimensions():
    """Test cani_change_dimensions() method will return appropriate message.

    When called, this should return a list of the parameterizations of the rink
    that may be changed by a user
    """
    # Create a HockeyRink() object to use for testing
    test_rink = hockey_rinks.NHLRink()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the rink_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- rink_length (200.0)\n"
        "- rink_width (85.0)\n"
        "- rink_units (ft)\n"
        "- corner_radius (28.0)\n"
        "- board_thickness (0.4167)\n"
        "- referee_crease_radius (10.0)\n"
        "- nzone_length (50.0)\n"
        "- goal_line_to_boards (11.0)\n"
        "- minor_line_thickness (0.1666)\n"
        "- major_line_thickness (1.0)\n"
        "- faceoff_circle_radius (15.0)\n"
        "- center_faceoff_spot_radius (0.5)\n"
        "- noncenter_faceoff_spot_radius (1.0)\n"
        "- nzone_faceoff_spot_to_zone_line (5.0)\n"
        "- odzone_faceoff_spot_to_boards (31.0)\n"
        "- noncenter_faceoff_spot_y (22.0)\n"
        "- noncenter_faceoff_spot_gap_width (0.25)\n"
        "- hashmark_width (2.0)\n"
        "- hashmark_ext_spacing (5.9166)\n"
        "- faceoff_line_dist_x (2.0)\n"
        "- faceoff_line_dist_y (0.75)\n"
        "- faceoff_line_length (4.0)\n"
        "- faceoff_line_width (3.0)\n"
        "- has_trapezoid (True)\n"
        "- short_base_width (22.0)\n"
        "- long_base_width (28.0)\n"
        "- goal_crease_style (nhl98)\n"
        "- goal_crease_radius (6.0)\n"
        "- goal_crease_length (4.5)\n"
        "- goal_crease_width (8.0)\n"
        "- goal_crease_notch_dist_x (4.0)\n"
        "- goal_crease_notch_width (0.4167)\n"
        "- goal_mouth_width (6.0)\n"
        "- goal_back_width (7.3333)\n"
        "- goal_depth (3.3333)\n"
        "- goal_post_diameter (0.1979)\n"
        "- goal_radius (1.6666)\n"
        "- bench_length (30.0)\n"
        "- bench_depth (5.5)\n"
        "- bench_separation (3.3333)\n"
        "- penalty_box_length (8.0)\n"
        "- penalty_box_depth (5.0)\n"
        "- penalty_box_separation (8.0)\n"
        "\n"
        "These parameters may be updated with the update_rink_params() "
        "method\n"
    )

    # Initialize the output-capture
    change_dimensions = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = change_dimensions
    test_rink.cani_change_dimensions()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert change_dimensions.getvalue() == exp_change_dimensions


def test_cani_color_features():
    """Test cani_color_features() method will return appropriate message.

    When called, this should return a list of the ice rink's features and their
    default/standard colors
    """
    # Create a HockeyRink() object to use for testing
    test_rink = hockey_rinks.HockeyRink()

    # Generate the expected output for cani_color_features()
    exp_color_features = (
        "The following features can be colored via the color_updates "
        "parameter, with the current value in parenthesis:\n"
    )

    for k, v in test_rink.feature_colors.items():
        exp_color_features = f"{exp_color_features}\n- {k} ({v})"

    exp_color_features = (
        f"{exp_color_features}\n\nThese colors may be updated with the "
        "update_colors() method\n"
    )

    # Initialize the output-capture
    color_features = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = color_features
    test_rink.cani_color_features()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert color_features.getvalue() == exp_color_features


def test_update_colors():
    """Test that update_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called
    """
    # Create a sample NHL rink to operate on
    test_nhl = hockey_rinks.NHLRink()

    # Get the standard colors for an NHL rink. These will be used for
    # comparison
    standard_colors = test_nhl.feature_colors

    # Update a color. The neutral zone color is what's updated here as a means
    # of demonstration, but this could work for any parameter. It will be
    # changed from white to dark blue
    test_nhl.update_colors({"nzone_ice": "#13294b"})

    # Get the updated colors
    updated_colors = test_nhl.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working

    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample NHL rink to operate on
    test_nhl = hockey_rinks.NHLRink()

    # Get the standard colors for an NHL rink. These will be used for
    # comparison
    standard_colors = test_nhl.feature_colors

    # Update a color. The neutral zone color is what's updated here as a means
    # of demonstration, but this could work for any parameter. It will be
    # changed from white to dark blue
    test_nhl.update_colors({"nzone_ice": "#13294b"})

    # Get the updated colors
    updated_colors = test_nhl.feature_colors

    # Now, change the colors back to the original
    test_nhl.reset_colors()

    # Get the final colors
    final_colors = test_nhl.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_rink_params():
    """Test that update_rink_params() method operates as expected.

    This should work as long as the internal rink parameters dictionary is
    updated when this method is called
    """
    # Create a sample NHL rink to operate on
    test_nhl = hockey_rinks.NHLRink()

    # Get the standard dimensions for an NHL rink. These will be used for
    # comparison
    standard_dimensions = test_nhl.rink_params

    # Update a dimension. The neutral zone length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 50 feet to 75 feet
    test_nhl.update_rink_params({"nzone_length": 75.0})

    # Get the updated dimensions
    updated_dimensions = test_nhl.rink_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_rink_params():
    """Test that reset_rink_params() method operates as expected.

    This should work as long as the internal rink parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample NHL rink to operate on
    test_nhl = hockey_rinks.NHLRink()

    # Get the standard dimensions for an NHL rink. These will be used for
    # comparison
    standard_dimensions = test_nhl.rink_params

    # Update a dimension. The neutral zone length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 50 feet to 75 feet
    test_nhl.update_rink_params({"nzone_length": 75.0})

    # Get the updated dimensions
    updated_dimensions = test_nhl.rink_params

    # Now, change the dimensions back to the original
    test_nhl.reset_rink_params()

    # Get the final dimensions
    final_dimensions = test_nhl.rink_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the rinks' coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation NHL rink. This should work for any of the
    # leagues supported by sportypy, but NHL is chosen out of convenience
    test_rink_to_convert = hockey_rinks.NHLRink()

    # Generate a rink originating in meters
    nhl_rink_m = hockey_rinks.NHLRink(units = "m")

    # Convert the rink dimensions from feet to meters
    rink_params_to_convert = test_rink_to_convert.rink_params

    for k, v in rink_params_to_convert.items():
        rink_params_to_convert[k] = test_rink_to_convert._convert_units(
            v,
            "ft",
            "m"
        )

    rink_params_to_convert["rink_units"] = "m"

    assert rink_params_to_convert == nhl_rink_m.rink_params


def test_unsupported_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the rinks' coordinates do not change when
    a user wishes to use an unsupported unit
    """
    # There are 43 parameters in an NHL rink, so the error message should be
    # repeated 41 times (since 2 parameters are booleans)
    exp_unit_error_string = (
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
        "foots is not currently a supported unit\n"
    )

    # Initialize the output-capture
    unit_error_string = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = unit_error_string
    hockey_rinks.NHLRink(units = "foots")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert unit_error_string.getvalue() == exp_unit_error_string


def test_rink_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the rinks' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = hockey_rinks.NHLRink().draw(ax = ax, rotation = 90.0)

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_rink_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the rinks' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_rink = hockey_rinks.NHLRink()
    ax1 = test_rink.draw(xlim = (-15.0, 15.0), ylim = (-15.0, 15.0))
    ax2 = test_rink.draw(xlim = (15.0, -15.0), ylim = (15.0, -15.0))
    ax3 = test_rink.draw(xlim = (0.0, 0.0), ylim = (0.0, 0.0))

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
    assert isinstance(ax3, matplotlib.axes.SubplotBase)


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "ahl": hockey_rinks.AHLRink(),
        "echl": hockey_rinks.ECHLRink(),
        "iihf": hockey_rinks.IIHFRink(),
        "phf": hockey_rinks.PHFRink(),
        "ncaa": hockey_rinks.NCAARink(),
        "nhl": hockey_rinks.NHLRink(),
        "ohl": hockey_rinks.OHLRink(),
        "nwhl": hockey_rinks.NWHLRink(),
        "qmjhl": hockey_rinks.QMJHLRink(),
        "ushl": hockey_rinks.USHLRink()
    }

    leagues = [
        k.lower() for k in hockey_rinks.HockeyRink().league_dimensions.keys()
    ]

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
            test_rink = league_class_dict[league]

            assert isinstance(test_rink, hockey_rinks.HockeyRink)


def test_rectangular_goal_lines():
    """Test to make rectangular goal line if closer to center than corner.

    This test should pass so long as the x-position of the goal line (contolled
    by the goal_line_to_boards parameter in rink_params) is greater than the
    radius of the corner of the rink (controlled by the corner_radius parameter
    in rink_params)
    """
    # Make a test rink with an altered goal_line_to_boards parameter
    test_rink = hockey_rinks.NHLRink(
        rink_updates = {"goal_line_to_boards": 35.0}
    )

    # The goal line is the 13th and 14th (1-indexed) features instantiated in
    # the HockeyRink class
    goal_line_df = test_rink._features[13]._get_centered_feature()

    # If rectangular, this should have beenc reated via the create_rectangle()
    # method of the BaseFeature class, which has exactly five points
    assert len(goal_line_df) == 5


def test_crease_styles():
    """Test to make sure that rinks with various crease styles are plottable.

    This test should pass so long as the various goal crease styles are viable
    for plots. Assuming no errors are raised, these tests should pass
    """
    # A USHL hockey rink will naturally use a "ushl1"-style crease
    ushl = hockey_rinks.USHLRink()

    ushl_plot = ushl.draw()

    # A hockey rink pre-1998 will use the nhl92 style currently supported by
    # sportypy
    nhl92 = hockey_rinks.NHLRink(rink_updates = {"goal_crease_style": "nhl92"})

    nhl92_plot = nhl92.draw()

    # Test a bad style
    bad_crease_style = hockey_rinks.NHLRink(
        rink_updates = {
            "goal_crease_style": "test_style"
        }
    )

    bad_crease_style_plot = bad_crease_style.draw()

    assert isinstance(ushl_plot, matplotlib.axes.SubplotBase)
    assert isinstance(nhl92_plot, matplotlib.axes.SubplotBase)
    assert isinstance(bad_crease_style_plot, matplotlib.axes.SubplotBase)


def test_rink_plot_singular_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the rinks' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_rink = hockey_rinks.NHLRink()
    ax1 = test_rink.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_rink.draw(xlim = 150.0, ylim = 150.0)

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_rink_plot_no_parameters():
    """Test that round features with no radius provided will still work.

    This is to ensure that the class can always be instantiated, but the
    feature may not be perfectly plotted
    """
    # Create the test plots
    test_zero_goal_crease_rad = hockey_rinks.NHLRink(
        rink_updates = {
            "goal_crease_radius": 0.0
        }
    ).draw()

    test_zero_corner_rad = hockey_rinks.NHLRink(
        rink_updates = {
            "corner_radius": 0.0
        }
    ).draw()

    test_zero_faceoff_radii = hockey_rinks.NHLRink(
        rink_updates = {
            "faceoff_circle_radius": 0.0,
            "noncenter_faceoff_spot_radius": .1666
        }
    ).draw()

    assert isinstance(test_zero_goal_crease_rad, matplotlib.axes.SubplotBase)
    assert isinstance(test_zero_corner_rad, matplotlib.axes.SubplotBase)
    assert isinstance(test_zero_faceoff_radii, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the rink.

    This test should pass so long as an additional feature may be added to the
    rink plot. The additional feature tested here is arbitrarily selected to be
    the neutral zone shifted in either direction
    """
    new_nz_1 = {
        "class": hockey_features.NeutralZone,
        "x_anchor": 25.0,
        "y_anchor": 0.0,
        "rink_length": 200.0,
        "rink_width": 85.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#13294b",
        "edgecolor": "#e04e39",
        "zorder": 1
    }

    new_nz_2 = {
        "class": hockey_features.NeutralZone,
        "x_anchor": -25.0,
        "y_anchor": 0.0,
        "rink_length": 200.0,
        "rink_width": 85.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#e04e39",
        "edgecolor": "#13294b",
        "zorder": 1
    }

    ax = hockey_rinks.NHLRink(
        new_feature_1 = new_nz_1,
        new_feature_2 = new_nz_2
    ).draw()

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = hockey_rinks.NHLRink(rotation = 90).draw(
        display_range = "ozone"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the rink defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a rink
    with no specified display range
    """
    ax1 = hockey_rinks.NHLRink().draw(display_range = None)
    ax2 = hockey_rinks.NHLRink().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
