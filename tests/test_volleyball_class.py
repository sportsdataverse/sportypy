"""Tests for the volleyball court classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.volleyball as volleyball_courts
import sportypy._feature_classes.volleyball as volleyball_features


def test_base_class_no_league():
    """Test that the base class, VolleyballCourt, can be instantiated.

    This test should pass so long as the VolleyballCourt class can be
    successfully instantiated without a league passed to it. This should create
    an instance of VolleyballCourt with the court_params attribute as an empty
    dictionary
    """
    test_court = volleyball_courts.VolleyballCourt()

    assert test_court.court_params == {}


def test_ncaa_params():
    """Test that the NCAACourt class can be instantiated.

    This test should pass so long as the NCAACourt class can be successfully
    instantiated with the correct parameters.
    """
    ncaa_params = {
        "court_length": 18.0,
        "court_width": 9.0,
        "court_units": "m",

        "free_zone_end_line": 4.5,
        "free_zone_sideline": 3.0,

        "court_apron_end_line": 2.0,
        "court_apron_sideline": 1.5,

        "line_thickness": 0.05,
        "attack_line_edge_to_center_line": 3.0,

        "substitution_zone_dash_length": 0.15,
        "substitution_zone_dash_breaks": 0.20,
        "substitution_zone_rep_pattern": "5",

        "service_zone_mark_length": 0.15,
        "service_zone_mark_to_end_line": 0.20
    }

    test_params = volleyball_courts.NCAACourt().court_params

    assert ncaa_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a VolleyballCourt() object to use for testing
    test_court = volleyball_courts.VolleyballCourt()

    # Get the available league codes
    available_league_codes = [k for k in test_court.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following volleyball leagues are available with sportypy:\n"
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
    test_court.cani_plot_leagues()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_empty_league_code.getvalue() == exp_pl_empty_league_code


def test_cani_plot_leagues_ncaa():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "ncaa", "NCAA", or any combination of capitalized and
    lower-case letters of "N", "C", and "A", this should return the same
    message
    """
    # Create a VolleyballCourt() object to use for testing
    test_court = volleyball_courts.VolleyballCourt()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use NCAA as a test)
    exp_pl_ncaa_league_code = "NCAA comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_ncaa_league_code_lower = io.StringIO()
    pl_ncaa_league_code_upper = io.StringIO()
    pl_ncaa_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_ncaa_league_code_lower
    test_court.cani_plot_leagues("ncaa")

    sys.stdout = pl_ncaa_league_code_upper
    test_court.cani_plot_leagues("NCAA")

    sys.stdout = pl_ncaa_league_code_mixed
    test_court.cani_plot_leagues("nCaA")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_ncaa_league_code_lower.getvalue() == exp_pl_ncaa_league_code
    assert pl_ncaa_league_code_upper.getvalue() == exp_pl_ncaa_league_code
    assert pl_ncaa_league_code_mixed.getvalue() == exp_pl_ncaa_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a VolleyballCourt() object to use for testing
    test_court = volleyball_courts.VolleyballCourt()

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
    test_court.cani_plot_leagues("test_league")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_bad_league_code.getvalue() == exp_pl_bad_league_code


def test_cani_change_dimensions():
    """Test cani_change_dimensions() method will return appropriate message.

    When called, this should return a list of the parameterizations of the
    court that may be changed by a user
    """
    # Create a VolleyballCourt() object to use for testing
    test_court = volleyball_courts.NCAACourt()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the court_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- court_length (18.0)\n"
        "- court_width (9.0)\n"
        "- court_units (m)\n"
        "- free_zone_end_line (4.5)\n"
        "- free_zone_sideline (3.0)\n"
        "- court_apron_end_line (2.0)\n"
        "- court_apron_sideline (1.5)\n"
        "- line_thickness (0.05)\n"
        "- attack_line_edge_to_center_line (3.0)\n"
        "- substitution_zone_dash_length (0.15)\n"
        "- substitution_zone_dash_breaks (0.2)\n"
        "- substitution_zone_rep_pattern (5)\n"
        "- service_zone_mark_length (0.15)\n"
        "- service_zone_mark_to_end_line (0.2)\n"
        "\n"
        "These parameters may be updated with the update_court_params() "
        "method\n"
    )

    # Initialize the output-capture
    change_dimensions = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = change_dimensions
    test_court.cani_change_dimensions()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert change_dimensions.getvalue() == exp_change_dimensions


def test_cani_color_features():
    """Test cani_color_features() method will return appropriate message.

    When called, this should return a list of the ice court's features and
    their default/standard colors
    """
    # Create a VolleyballCourt() object to use for testing
    test_court = volleyball_courts.VolleyballCourt()

    # Generate the expected output for cani_color_features()
    exp_color_features = (
        "The following features can be colored via the color_updates "
        "parameter, with the current value in parenthesis:\n"
    )

    for k, v in test_court.feature_colors.items():
        exp_color_features = f"{exp_color_features}\n- {k} ({v})"

    exp_color_features = (
        f"{exp_color_features}\n\nThese colors may be updated with the "
        "update_colors() method\n"
    )

    # Initialize the output-capture
    color_features = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = color_features
    test_court.cani_color_features()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert color_features.getvalue() == exp_color_features


def test_update_colors():
    """Test that update_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called
    """
    # Create a sample NCAA court to operate on
    test_ncaa = volleyball_courts.NCAACourt()

    # Get the standard colors for an NCAA court. These will be used for
    # comparison
    standard_colors = test_ncaa.feature_colors

    # Update a color. The center line of the court color is what's updated here
    # as a means of demonstration, but this could work for any parameter. It
    # will be changed from white to dark blue
    test_ncaa.update_colors({"center_line": "#13294b"})

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
    # Create a sample NCAA court to operate on
    test_ncaa = volleyball_courts.NCAACourt()

    # Get the standard colors for an NCAA court. These will be used for
    # comparison
    standard_colors = test_ncaa.feature_colors

    # Update a color. The center line of the court color is what's updated here
    # as a means of demonstration, but this could work for any parameter. It
    # will be changed from white to dark blue
    test_ncaa.update_colors({"center_line": "#13294b"})

    # Get the updated colors
    updated_colors = test_ncaa.feature_colors

    # Now, change the colors back to the original
    test_ncaa.reset_colors()

    # Get the final colors
    final_colors = test_ncaa.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_court_params():
    """Test that update_court_params() method operates as expected.

    This should work as long as the internal court parameters dictionary is
    updated when this method is called
    """
    # Create a sample NCAA court to operate on
    test_ncaa = volleyball_courts.NCAACourt()

    # Get the standard dimensions for an NCAA court. These will be used for
    # comparison
    standard_dimensions = test_ncaa.court_params

    # Update a dimension. The court apron behind the end line is what's updated
    # here as a means of demonstration, but this could work for any parameter.
    # It will be changed from 2.0 meters to 5.0 feet
    test_ncaa.update_court_params({"court_apron_end_line": 5.0})

    # Get the updated dimensions
    updated_dimensions = test_ncaa.court_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_court_params():
    """Test that reset_court_params() method operates as expected.

    This should work as long as the internal court parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample NCAA court to operate on
    test_ncaa = volleyball_courts.NCAACourt()

    # Get the standard dimensions for an NCAA court. These will be used for
    # comparison
    standard_dimensions = test_ncaa.court_params

    # Update a dimension. The court apron behind the end line is what's updated
    # here as a means of demonstration, but this could work for any parameter.
    # It will be changed from 2.0 meters to 5.0 feet
    test_ncaa.update_court_params({"court_apron_end_line": 5.0})

    # Get the updated dimensions
    updated_dimensions = test_ncaa.court_params

    # Now, change the dimensions back to the original
    test_ncaa.reset_court_params()

    # Get the final dimensions
    final_dimensions = test_ncaa.court_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the courts' coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation NCAA court. This should work for any of
    # the leagues supported by sportypy, but NCAA is chosen out of convenience
    test_court_to_convert = volleyball_courts.NCAACourt()

    # Generate a court originating in feet
    ncaa_court_m = volleyball_courts.NCAACourt(units = "ft")

    # Convert the court dimensions from feet to meters
    court_params_to_convert = test_court_to_convert.court_params

    for k, v in court_params_to_convert.items():
        court_params_to_convert[k] = test_court_to_convert._convert_units(
            v,
            "m",
            "ft"
        )

    court_params_to_convert["court_units"] = "ft"

    assert court_params_to_convert == ncaa_court_m.court_params


def test_unsupported_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the courts' coordinates do not change when
    a user wishes to use an unsupported unit
    """
    # There are 13 parameters in an NCAA court
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
    )

    # Initialize the output-capture
    unit_error_string = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = unit_error_string
    volleyball_courts.NCAACourt(units = "foots")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert unit_error_string.getvalue() == exp_unit_error_string


def test_court_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the courts' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = volleyball_courts.NCAACourt().draw(ax = ax, rotation = 90.0)

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_court_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the courts' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_court = volleyball_courts.NCAACourt()
    ax1 = test_court.draw(xlim = (-25.0, 15.0), ylim = (-25.0, 25.0))
    ax2 = test_court.draw(xlim = (25.0, -15.0), ylim = (25.0, -25.0))
    ax3 = test_court.draw(xlim = (0.0, 0.0), ylim = (0.0, 0.0))

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
    assert isinstance(ax3, matplotlib.axes.SubplotBase)


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "fivb": volleyball_courts.FIVBCourt(),
        "ncaa": volleyball_courts.NCAACourt(),
        "usa volleyball": volleyball_courts.USAVolleyballCourt()
    }

    leagues = [
        k.lower()
        for k
        in volleyball_courts.VolleyballCourt().league_dimensions.keys()
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
            test_court = league_class_dict[league]

            assert isinstance(test_court, volleyball_courts.VolleyballCourt)


def test_court_plot_singular_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the courts' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_court = volleyball_courts.NCAACourt()
    ax1 = test_court.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_court.draw(xlim = 150.0, ylim = 150.0)

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_court_plot_no_parameters():
    """Test that round features with no radius provided will still work.

    This is to ensure that the class can always be instantiated, but the
    feature may not be perfectly plotted
    """
    # Create the test plots
    test_zero_house_ring_rad = volleyball_courts.NCAACourt(
        court_updates = {
            "house_ring_radii": [0.0, 0.0, 0.0]
        }
    ).draw()

    assert isinstance(test_zero_house_ring_rad, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the court.

    This test should pass so long as an additional feature may be added to the
    court plot. The additional feature tested here is arbitrarily selected to
    be the center line shifted in either direction
    """
    new_center_line_1 = {
        "class": volleyball_features.CenterLine,
        "x_anchor": 0.0,
        "y_anchor": 25.0,
        "court_length": 18.0,
        "court_width": 9.0,
        "feature_thickness": 0.05,
        "visible": True,
        "facecolor": "#13294b",
        "edgecolor": "#e04e39",
        "zorder": 1
    }

    new_center_line_2 = {
        "class": volleyball_features.CenterLine,
        "x_anchor": 0.0,
        "y_anchor": -25.0,
        "court_length": 18.0,
        "court_width": 9.0,
        "feature_thickness": 0.05,
        "visible": True,
        "facecolor": "#13294b",
        "edgecolor": "#e04e39",
        "zorder": 1
    }

    ax = volleyball_courts.NCAACourt(
        new_feature_1 = new_center_line_1,
        new_feature_2 = new_center_line_2
    ).draw()

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = volleyball_courts.NCAACourt(rotation = 90).draw(
        display_range = "offense"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the court defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a court
    with no specified display range
    """
    ax1 = volleyball_courts.NCAACourt().draw(display_range = None)
    ax2 = volleyball_courts.NCAACourt().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
