"""Tests for the soccer pitch classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.soccer as soccer_pitches
import sportypy._feature_classes.soccer as soccer_features


def test_base_class_no_league():
    """Test that the base class, SoccerPitch, can be instantiated.

    This test should pass so long as the SoccerPitch class can be
    successfully instantiated without a league passed to it. This should create
    an instance of SoccerPitch with the pitch_params attribute as an empty
    dictionary
    """
    test_pitch = soccer_pitches.SoccerPitch()

    assert test_pitch.pitch_params == {}


def test_epl_params():
    """Test that the EPLPitch class can be instantiated.

    This test should pass so long as the EPLPitch class can be successfully
    instantiated with the correct parameters.
    """
    epl_params = {
        "pitch_units": "m",
        "pitch_length": 120.0,
        "pitch_width": 90.0,
        "line_thickness": 0.12,

        "pitch_apron_touchline": 1.0,
        "pitch_apron_goal_line": 1.0,

        "center_circle_radius": 9.15,
        "center_mark_radius": 0.3048,

        "corner_arc_radius": 1.0,
        "goal_line_defensive_mark_visible": True,
        "touchline_defensive_mark_visible": True,
        "defensive_mark_depth": 0.5,
        "defensive_mark_distance": 9.15,

        "penalty_box_length": 16.5,
        "penalty_circle_radius": 9.15,
        "penalty_mark_dist": 11.0,
        "interior_of_goal_post_to_penalty_box": 16.5,
        "interior_of_goal_post_to_goal_box": 5.5,
        "goal_box_length": 5.5,
        "penalty_mark_radius": 0.1524,

        "goal_width": 7.32,
        "goal_depth": 1.7
    }

    test_params = soccer_pitches.EPLPitch().pitch_params

    assert epl_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a SoccerPitch() object to use for testing
    test_pitch = soccer_pitches.SoccerPitch()

    # Get the available league codes
    available_league_codes = [k for k in test_pitch.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following soccer leagues are available with sportypy:\n"
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
    test_pitch.cani_plot_leagues()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_empty_league_code.getvalue() == exp_pl_empty_league_code


def test_cani_plot_leagues_epl():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "epl", "EPL", or any combination of capitalized and
    lower-case letters of "E", "P", and "L", this should return the same
    message
    """
    # Create a SoccerPitch() object to use for testing
    test_pitch = soccer_pitches.SoccerPitch()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use EPL as a test)
    exp_pl_epl_league_code = "EPL comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_epl_league_code_lower = io.StringIO()
    pl_epl_league_code_upper = io.StringIO()
    pl_epl_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_epl_league_code_lower
    test_pitch.cani_plot_leagues("epl")

    sys.stdout = pl_epl_league_code_upper
    test_pitch.cani_plot_leagues("EPL")

    sys.stdout = pl_epl_league_code_mixed
    test_pitch.cani_plot_leagues("EpL")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_epl_league_code_lower.getvalue() == exp_pl_epl_league_code
    assert pl_epl_league_code_upper.getvalue() == exp_pl_epl_league_code
    assert pl_epl_league_code_mixed.getvalue() == exp_pl_epl_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a SoccerPitch() object to use for testing
    test_pitch = soccer_pitches.SoccerPitch()

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
    test_pitch.cani_plot_leagues("test_league")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_bad_league_code.getvalue() == exp_pl_bad_league_code


def test_cani_change_dimensions():
    """Test cani_change_dimensions() method will return appropriate message.

    When called, this should return a list of the parameterizations of the
    pitch that may be changed by a user
    """
    # Create a SoccerPitch() object to use for testing
    test_pitch = soccer_pitches.EPLPitch()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the pitch_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- pitch_units (m)\n"
        "- pitch_length (120.0)\n"
        "- pitch_width (90.0)\n"
        "- line_thickness (0.12)\n"
        "- pitch_apron_touchline (1.0)\n"
        "- pitch_apron_goal_line (1.0)\n"
        "- center_circle_radius (9.15)\n"
        "- center_mark_radius (0.3048)\n"
        "- corner_arc_radius (1.0)\n"
        "- goal_line_defensive_mark_visible (True)\n"
        "- touchline_defensive_mark_visible (True)\n"
        "- defensive_mark_depth (0.5)\n"
        "- defensive_mark_distance (9.15)\n"
        "- penalty_box_length (16.5)\n"
        "- penalty_circle_radius (9.15)\n"
        "- penalty_mark_dist (11.0)\n"
        "- interior_of_goal_post_to_penalty_box (16.5)\n"
        "- interior_of_goal_post_to_goal_box (5.5)\n"
        "- goal_box_length (5.5)\n"
        "- penalty_mark_radius (0.1524)\n"
        "- goal_width (7.32)\n"
        "- goal_depth (1.7)\n"
        "\n"
        "These parameters may be updated with the update_pitch_params() "
        "method\n"
    )

    # Initialize the output-capture
    change_dimensions = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = change_dimensions
    test_pitch.cani_change_dimensions()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert change_dimensions.getvalue() == exp_change_dimensions


def test_cani_color_features():
    """Test cani_color_features() method will return appropriate message.

    When called, this should return a list of the pitch's features and their
    default/standard colors
    """
    # Create a SoccerPitch() object to use for testing
    test_pitch = soccer_pitches.SoccerPitch()

    # Generate the expected output for cani_color_features()
    exp_color_features = (
        "The following features can be colored via the color_updates "
        "parameter, with the current value in parenthesis:\n"
    )

    for k, v in test_pitch.feature_colors.items():
        exp_color_features = f"{exp_color_features}\n- {k} ({v})"

    exp_color_features = (
        f"{exp_color_features}\n\nThese colors may be updated with the "
        "update_colors() method\n"
    )

    # Initialize the output-capture
    color_features = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = color_features
    test_pitch.cani_color_features()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert color_features.getvalue() == exp_color_features


def test_update_colors():
    """Test that update_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called
    """
    # Create a sample EPL pitch to operate on
    test_epl = soccer_pitches.EPLPitch()

    # Get the standard colors for an EPL pitch. These will be used for
    # comparison
    standard_colors = test_epl.feature_colors

    # Update a color. The halfway line is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to yellow
    test_epl.update_colors({"halfway_line": "#ffc805"})

    # Get the updated colors
    updated_colors = test_epl.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working

    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample EPL pitch to operate on
    test_epl = soccer_pitches.EPLPitch()

    # Get the standard colors for an EPL pitch. These will be used for
    # comparison
    standard_colors = test_epl.feature_colors

    # Update a color. The halfway line is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to yellow
    test_epl.update_colors({"halfway_line": "#ffc805"})

    # Get the updated colors
    updated_colors = test_epl.feature_colors

    # Now, change the colors back to the original
    test_epl.reset_colors()

    # Get the final colors
    final_colors = test_epl.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_pitch_params():
    """Test that update_pitch_params() method operates as expected.

    This should work as long as the internal pitch parameters dictionary is
    updated when this method is called
    """
    # Create a sample EPL pitch to operate on
    test_epl = soccer_pitches.EPLPitch()

    # Get the standard dimensions for an EPL pitch. These will be used for
    # comparison
    standard_dimensions = test_epl.pitch_params

    # Update a dimension. The full-pitch length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 120 meters to 200 meters
    test_epl.update_pitch_params({"pitch_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_epl.pitch_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_pitch_params():
    """Test that reset_pitch_params() method operates as expected.

    This should work as long as the internal pitch parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample EPL pitch to operate on
    test_epl = soccer_pitches.EPLPitch()

    # Get the standard dimensions for an EPL pitch. These will be used for
    # comparison
    standard_dimensions = test_epl.pitch_params

    # Update a dimension. The full-pitch length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 120 meters to 200 meters
    test_epl.update_pitch_params({"pitch_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_epl.pitch_params

    # Now, change the dimensions back to the original
    test_epl.reset_pitch_params()

    # Get the final dimensions
    final_dimensions = test_epl.pitch_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the pitch's coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation EPL pitch. This should work for any of the
    # leagues supported by sportypy, but EPL is chosen out of convenience
    test_pitch_to_convert = soccer_pitches.EPLPitch()

    # Generate a pitch originating in feet
    epl_pitch_m = soccer_pitches.EPLPitch(units = "ft")

    # Convert the pitch dimensions from meters to feet
    pitch_params_to_convert = test_pitch_to_convert.pitch_params

    for k, v in pitch_params_to_convert.items():
        pitch_params_to_convert[k] = test_pitch_to_convert._convert_units(
            v,
            "m",
            "ft"
        )

    # Convert the units to be meters
    pitch_params_to_convert["pitch_units"] = "ft"

    assert pitch_params_to_convert == epl_pitch_m.pitch_params


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "epl": soccer_pitches.EPLPitch(),
        "fifa": soccer_pitches.FIFAPitch(),
        "mls": soccer_pitches.MLSPitch(),
        "ncaa": soccer_pitches.NCAAPitch(),
        "nwsl": soccer_pitches.NWSLPitch(),
    }

    pitch = soccer_pitches.SoccerPitch()

    leagues = [k.lower() for k in pitch.league_dimensions.keys()]

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

            assert isinstance(test_rink, soccer_pitches.SoccerPitch)


def test_custom_pitch_params():
    """Test that custom pitchs are able to be created.

    This test should pass so long as the pitch's parameters are valid
    """
    # Start by defining the customized pitch parameters
    pitch_parameters = {
        "pitch_units": "m",
        "pitch_length": 120.0,
        "pitch_width": 90.0,
        "line_thickness": 0.12,

        "pitch_apron_touchline": 1.0,
        "pitch_apron_goal_line": 1.0,

        "center_circle_radius": 9.15,
        "center_mark_radius": 0.3048,

        "corner_arc_radius": 1.0,
        "goal_line_defensive_mark_visible": True,
        "touchline_defensive_mark_visible": True,
        "defensive_mark_depth": 0.5,
        "defensive_mark_distance": 9.15,

        "penalty_box_length": 16.5,
        "penalty_circle_radius": 9.15,
        "penalty_mark_dist": 11.0,
        "interior_of_goal_post_to_penalty_box": 16.5,
        "interior_of_goal_post_to_goal_box": 5.5,
        "goal_box_length": 5.5,
        "penalty_mark_radius": 0.1524,

        "goal_width": 7.32,
        "goal_depth": 1.7
    }

    color_updates = {
        "plot_background": "#196f0c",
        "defensive_half_pitch": "#195f0c",
        "offensive_half_pitch": "#195f0c",
        "pitch_apron": "#195f0c",
        "touchline": "#ffffff",
        "goal_line": "#ffffff",
        "corner_arc": "#ffffff",
        "halfway_line": "#ffffff",
        "center_circle": "#ffffff",
        "center_mark": "#ffffff",
        "penalty_box": "#ffffff",
        "goal_box": "#ffffff",
        "penalty_mark": "#ffffff",
        "corner_defensive_mark": "#ffffff",
        "goal": "#ffffff"
    }

    test_pitch = soccer_pitches.SoccerPitch(
        pitch_updates = pitch_parameters,
        color_updates = color_updates
    )

    assert isinstance(test_pitch, soccer_pitches.SoccerPitch)


def test_pitch_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the pitch's plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = soccer_pitches.EPLPitch().draw(ax = ax, rotation = 90.0)

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_pitch_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the pitch's plot may be customized by
    setting the xlim and ylim parameters
    """
    test_pitch = soccer_pitches.EPLPitch()
    ax1 = test_pitch.draw(xlim = (-15.0, 15.0), ylim = (-15.0, 15.0))
    ax2 = test_pitch.draw(xlim = (15.0, -15.0), ylim = (15.0, -15.0))
    ax3 = test_pitch.draw(xlim = (0.0, 0.0), ylim = (0.0, 0.0))

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
    assert isinstance(ax3, matplotlib.axes.SubplotBase)


def test_pitch_plot_singular_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the pitch's plot may be customized by
    setting the xlim and ylim parameters
    """
    test_pitch = soccer_pitches.EPLPitch()
    ax1 = test_pitch.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_pitch.draw(xlim = 150.0, ylim = 50.0)

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the rink.

    This test should pass so long as an additional feature may be added to the
    pitch plot. The additional feature tested here is arbitrarily selected to
    be a halfway line shifted to either side of the pitch
    """
    new_halfway_line_1 = {
        "class": soccer_features.HalfwayLine,
        "x_anchor": 30.0,
        "y_anchor": 0.0,
        "pitch_length": 120.0,
        "pitch_width": 90.0,
        "feature_thickness": 0.12,
        "visible": True,
        "facecolor": "#ffc805",
        "edgecolor": None,
        "zorder": 50
    }

    new_halfway_line_2 = {
        "class": soccer_features.HalfwayLine,
        "x_anchor": -23.5,
        "y_anchor": 0.0,
        "pitch_length": 94.0,
        "pitch_width": 50.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#000000",
        "edgecolor": None,
        "zorder": 50
    }

    ax = soccer_pitches.EPLPitch(
        new_feature_1 = new_halfway_line_1,
        new_feature_2 = new_halfway_line_2
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_zero_radii():
    """Test that pitch features work even with a radius of 0.0.

    This test should pass so long as the errors are handled correctly when a
    curved feature is created but the radius is 0.0
    """
    pitch_updates = {
        "penalty_circle_radius": 0.0
    }

    ax = soccer_pitches.EPLPitch(
        pitch_updates = pitch_updates
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_pitch_plot_with_xlim_ylim():
    """Test that pitch sections can be drawn (e.g. offensive half-pitch).

    This test should pass so long as there are no errors when drawing a section
    of the pitch
    """
    ax1 = soccer_pitches.NCAAPitch().draw(
        display_range = "offensive half pitch"
    )

    assert isinstance(ax1, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = soccer_pitches.EPLPitch(rotation = 90).draw()

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the pitch defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a pitch
    with no specified display range
    """
    ax1 = soccer_pitches.EPLPitch().draw(display_range = None)
    ax2 = soccer_pitches.EPLPitch().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
