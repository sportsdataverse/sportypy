"""Tests for the tennis court classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.tennis as tennis_courts
import sportypy._feature_classes.tennis as tennis_features


def test_base_class_no_league():
    """Test that the base class, TennisCourt, can be instantiated.

    This test should pass so long as the TennisCourt class can be
    successfully instantiated without a league passed to it. This should create
    an instance of TennisCourt with the court_params attribute as an empty
    dictionary
    """
    test_court = tennis_courts.TennisCourt()

    assert test_court.court_params == {}


def test_itf_params():
    """Test that the ITFCourt class can be instantiated.

    This test should pass so long as the ITFCourt class can be successfully
    instantiated with the correct parameters.
    """
    itf_params = {
        "court_length": 78.0,
        "singles_width": 27.0,
        "court_units": "ft",
        "doubles_width": 36.0,
        "serviceline_distance": 21.0,
        "center_mark_length": 0.3333,
        "net_length": 42.0,
        "line_thickness": 0.1667,
        "backstop_distance": 21.0,
        "sidestop_distance": 12.0
    }

    test_params = tennis_courts.ITFCourt().court_params

    assert itf_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a TennisCourt() object to use for testing
    test_court = tennis_courts.TennisCourt()

    # Get the available league codes
    available_league_codes = [k for k in test_court.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following tennis leagues are available with sportypy:\n"
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


def test_cani_plot_leagues_itf():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "itf", "ITF", or any combination of capitalized and
    lower-case letters of "I", "T", and "F", this should return the same
    message
    """
    # Create a TennisCourt() object to use for testing
    test_court = tennis_courts.TennisCourt()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use ITF as a test)
    exp_pl_itf_league_code = "ITF comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_itf_league_code_lower = io.StringIO()
    pl_itf_league_code_upper = io.StringIO()
    pl_itf_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_itf_league_code_lower
    test_court.cani_plot_leagues("itf")

    sys.stdout = pl_itf_league_code_upper
    test_court.cani_plot_leagues("ITF")

    sys.stdout = pl_itf_league_code_mixed
    test_court.cani_plot_leagues("ItF")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_itf_league_code_lower.getvalue() == exp_pl_itf_league_code
    assert pl_itf_league_code_upper.getvalue() == exp_pl_itf_league_code
    assert pl_itf_league_code_mixed.getvalue() == exp_pl_itf_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a TennisCourt() object to use for testing
    test_court = tennis_courts.TennisCourt()

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
    # Create a TennisCourt() object to use for testing
    test_court = tennis_courts.ITFCourt()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the court_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- court_length (78.0)\n"
        "- singles_width (27.0)\n"
        "- court_units (ft)\n"
        "- doubles_width (36.0)\n"
        "- serviceline_distance (21.0)\n"
        "- center_mark_length (0.3333)\n"
        "- net_length (42.0)\n"
        "- line_thickness (0.1667)\n"
        "- backstop_distance (21.0)\n"
        "- sidestop_distance (12.0)\n"
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

    When called, this should return a list of the court's features and their
    default/standard colors
    """
    # Create a TennisCourt() object to use for testing
    test_court = tennis_courts.TennisCourt()

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
    # Create a sample ITF court to operate on
    test_itf = tennis_courts.ITFCourt()

    # Get the standard colors for an ITF court. These will be used for
    # comparison
    standard_colors = test_itf.feature_colors

    # Update a color. The doubles alley is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to orange
    test_itf.update_colors({"doubles_alley": "#e84a27"})

    # Get the updated colors
    updated_colors = test_itf.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working
    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample ITF court to operate on
    test_itf = tennis_courts.ITFCourt()

    # Get the standard colors for an ITF court. These will be used for
    # comparison
    standard_colors = test_itf.feature_colors

    # Update a color. The doubles alley is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from white to orange
    test_itf.update_colors({"doubles_alley": "#e84a27"})

    # Get the updated colors
    updated_colors = test_itf.feature_colors

    # Now, change the colors back to the original
    test_itf.reset_colors()

    # Get the final colors
    final_colors = test_itf.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_court_params():
    """Test that update_court_params() method operates as expected.

    This should work as long as the internal court parameters dictionary is
    updated when this method is called
    """
    # Create a sample ITF court to operate on
    test_itf = tennis_courts.ITFCourt()

    # Get the standard dimensions for an ITF court. These will be used for
    # comparison
    standard_dimensions = test_itf.court_params

    # Update a dimension. The full-court length is what"s updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 78 feet to 200 feet
    test_itf.update_court_params({"court_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_itf.court_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_court_params():
    """Test that reset_court_params() method operates as expected.

    This should work as long as the internal court parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample ITF court to operate on
    test_itf = tennis_courts.ITFCourt()

    # Get the standard dimensions for an ITF court. These will be used for
    # comparison
    standard_dimensions = test_itf.court_params

    # Update a dimension. The full-court length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 78 feet to 200 feet
    test_itf.update_court_params({"court_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_itf.court_params

    # Now, change the dimensions back to the original
    test_itf.reset_court_params()

    # Get the final dimensions
    final_dimensions = test_itf.court_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the courts' coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation ITF court. This should work for any of the
    # leagues supported by sportypy, but ITF is chosen out of convenience
    test_court_to_convert = tennis_courts.ITFCourt()

    # Generate a court originating in meters
    itf_court_m = tennis_courts.ITFCourt(units = "m")

    # Convert the court dimensions from feet to meters
    court_params_to_convert = test_court_to_convert.court_params

    for k, v in court_params_to_convert.items():
        court_params_to_convert[k] = test_court_to_convert._convert_units(
            v,
            "ft",
            "m"
        )

    # Convert the units to be meters
    court_params_to_convert["court_units"] = "m"

    assert court_params_to_convert == itf_court_m.court_params


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "ita": tennis_courts.ITACourt(),
        "itf": tennis_courts.ITFCourt(),
        "ncaa": tennis_courts.NCAACourt(),
        "usta": tennis_courts.USTACourt(),
        "wta": tennis_courts.WTACourt()
    }

    court = tennis_courts.TennisCourt()

    leagues = [k.lower() for k in court.league_dimensions.keys()]

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

            assert isinstance(test_court, tennis_courts.TennisCourt)


def test_custom_court_params():
    """Test that custom courts are able to be created.

    This test should pass so long as the courts' parameters are valid
    """
    # Start by defining the customized court parameters
    court_1_parameters = {
        "court_length": 178.0,
        "singles_width": 20.0,
        "court_units": "ft",
        "doubles_width": 30.0,
        "serviceline_distance": 121.0,
        "center_mark_length": 10.3333,
        "net_length": 52.0,
        "line_thickness": 1.1667,
        "backstop_distance": 51.0,
        "sidestop_distance": 52.0
    }

    color_updates_1 = {
        "baseline": "#0088ce",
        "singles_sideline": "#0088ce",
        "doubles_sideline": "#0088ce",
        "serviceline": "#0088ce",
        "center_serviceline": "#0088ce",
        "center_mark": "#0088ce",
        "ad_court": "#000000",
        "deuce_court": "#000000",
        "backcourt": "#000000",
        "doubles_alley": "#000000",
        "court_apron": "#000000",
        "net": "#0088ce"
    }

    test_court_1 = tennis_courts.TennisCourt(
        court_updates = court_1_parameters,
        color_updates = color_updates_1
    )

    assert isinstance(test_court_1, tennis_courts.TennisCourt)


def test_court_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the courts' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = tennis_courts.ITFCourt().draw(ax = ax, rotation = 90.0)

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_court_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the courts' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_court = tennis_courts.WTACourt()
    ax1 = test_court.draw(xlim = (-15.0, 15.0), ylim = (-15.0, 15.0))
    ax2 = test_court.draw(xlim = (15.0, -15.0), ylim = (15.0, -15.0))
    ax3 = test_court.draw(xlim = (0.0, 0.0), ylim = (0.0, 0.0))

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
    assert isinstance(ax3, matplotlib.axes.SubplotBase)


def test_court_plot_singular_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the courts' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_court = tennis_courts.ITFCourt()
    ax1 = test_court.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_court.draw(xlim = 150.0, ylim = 65.0)

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the court.

    This test should pass so long as an additional feature may be added to the
    court plot. The additional feature tested here is arbitrarily selected to
    be a sideline shifted to either side of the court
    """
    new_sideline = {
        "class": tennis_features.Sideline,
        "x_anchor": 24.0,
        "y_anchor": 0.0,
        "court_length": 78.0,
        "court_width": 27.0,
        "feature_thickness": 0.1667,
        "visible": True,
        "facecolor": "#000000",
        "edgecolor": None,
        "zorder": 1
    }

    ax = tennis_courts.ITFCourt(
        new_feature_1 = new_sideline,
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_court_plot_with_xlim_ylim():
    """Test that court sections can be drawn (e.g. service side of the court).

    This test should pass so long as there are no errors when drawing a section
    of the court
    """
    ax1 = tennis_courts.NCAACourt().draw(
        display_range = "serve"
    )

    assert isinstance(ax1, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the court may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = tennis_courts.NCAACourt(rotation = 90).draw(
        display_range = "serve"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the court defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a court
    with no specified display range
    """
    ax1 = tennis_courts.ITFCourt().draw(display_range = None)
    ax2 = tennis_courts.ITFCourt().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
