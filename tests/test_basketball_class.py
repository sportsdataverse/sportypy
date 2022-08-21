"""Tests for the basketball court classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.basketball as basketball_courts
import sportypy._feature_classes.basketball as basketball_features


def test_base_class_no_league():
    """Test that the base class, BasketballCourt, can be instantiated.

    This test should pass so long as the BasketballCourt class can be
    successfully instantiated without a league passed to it. This should create
    an instance of BasketballCourt with the court_params attribute as an empty
    dictionary
    """
    test_court = basketball_courts.BasketballCourt()

    assert test_court.court_params == {}


def test_nba_params():
    """Test that the NBACourt class can be instantiated.

    This test should pass so long as the NBACourt class can be successfully
    instantiated with the correct parameters.
    """
    nba_params = {
        "court_length": 94.0,
        "court_width": 50.0,
        "court_units": "ft",
        "line_thickness": 0.1667,
        "bench_side": "top",

        "court_apron_endline": 8.0,
        "court_apron_sideline": 5.0,
        "court_apron_to_boundary": 0.0,
        
        "center_circle_radius": [6.0, 2.1667],

        "basket_center_to_baseline": 5.25,
        "basket_center_to_three_point_arc": 23.75,
        "basket_center_to_corner_three": 22.0,
        "backboard_face_to_baseline": 4.0,

        "lane_length": [19.0, 19.0],
        "lane_width": [16.0, 12.0],
        "paint_margin": [0.0, 0.0],

        "free_throw_circle_radius": 6.0,
        "free_throw_line_to_backboard": 15.0,
        "free_throw_circle_overhang": 1.024,
        "n_free_throw_circle_dashes": 6.0,
        "free_throw_dash_length": 1.292,
        "free_throw_dash_spacing": 1.292,

        "lane_space_mark_lengths": [
            [0.1667, 0.1667, 0.1667, 0.1667],
            [1.0, 0.1667, 0.1667, 0.1667]
        ],
        "lane_space_mark_widths": [0.5, 0.75],
        "lane_space_mark_separations": [
            [3.0, 0.8333, 3.0, 3.0],
            [3.0, 3.0, 3.0, 3.0]
        ],

        "painted_area_visibility": [True, True],
        "lane_boundary_visibility": [True, True],
        "lane_space_mark_visibility": [True, False],
        "lane_lower_defensive_box_marks_visibility": True,

        "baseline_lower_defensive_box_marks_int_sep": 19.0,
        "baseline_to_lane_lower_defensive_box_marks": 13.0,
        "lane_lower_defensive_box_marks_int_sep": 10.0,
        "lower_defensive_box_mark_extension": 0.5,

        "inbounding_line_to_baseline": 28.0,
        "inbounding_line_anchor_side": 1.0,
        "inbounding_line_in_play_ext": 3.0,
        "inbounding_line_out_of_bounds_ext": 0.0,
        "symmetric_inbounding_line": True,

        "substitution_line_ext_sep": 8.5,
        "substitution_line_width": 4.0,

        "restricted_arc_radius": 4.0,

        "backboard_width": 6.0,
        "backboard_thickness": 0.171875,
        
        "basket_ring_inner_radius": 0.75,
        "basket_ring_connector_width": 0.5833,
        "basket_ring_connector_extension": 0.5,
        "basket_ring_thickness": 0.0656
    }

    test_params = basketball_courts.NBACourt().court_params

    assert nba_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a BasketballCourt() object to use for testing
    test_court = basketball_courts.BasketballCourt()

    # Get the available league codes
    available_league_codes = [k for k in test_court.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following basketball leagues are available with sportypy:\n"
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


def test_cani_plot_leagues_nba():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "nba", "NBA", or any combination of capitalized and
    lower-case letters of "N", "B", and "A", this should return the same
    message
    """
    # Create a BasketballCourt() object to use for testing
    test_court = basketball_courts.BasketballCourt()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use NBA as a test)
    exp_pl_nba_league_code = "NBA comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_nba_league_code_lower = io.StringIO()
    pl_nba_league_code_upper = io.StringIO()
    pl_nba_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_nba_league_code_lower
    test_court.cani_plot_leagues("nba")

    sys.stdout = pl_nba_league_code_upper
    test_court.cani_plot_leagues("NBA")

    sys.stdout = pl_nba_league_code_mixed
    test_court.cani_plot_leagues("NbA")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_nba_league_code_lower.getvalue() == exp_pl_nba_league_code
    assert pl_nba_league_code_upper.getvalue() == exp_pl_nba_league_code
    assert pl_nba_league_code_mixed.getvalue() == exp_pl_nba_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a BasketballCourt() object to use for testing
    test_court = basketball_courts.BasketballCourt()

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
    # Create a BasketballCourt() object to use for testing
    test_court = basketball_courts.NBACourt()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the court_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- court_length (94.0)\n"
        "- court_width (50.0)\n"
        "- court_units (ft)\n"
        "- line_thickness (0.1667)\n"
        "- bench_side (top)\n"
        "- court_apron_endline (8.0)\n"
        "- court_apron_sideline (5.0)\n"
        "- court_apron_to_boundary (0.0)\n"
        "- center_circle_radius ([6.0, 2.1667])\n"
        "- basket_center_to_baseline (5.25)\n"
        "- basket_center_to_three_point_arc (23.75)\n"
        "- basket_center_to_corner_three (22.0)\n"
        "- backboard_face_to_baseline (4.0)\n"
        "- lane_length ([19.0, 19.0])\n"
        "- lane_width ([16.0, 12.0])\n"
        "- paint_margin ([0.0, 0.0])\n"
        "- free_throw_circle_radius (6.0)\n"
        "- free_throw_line_to_backboard (15.0)\n"
        "- free_throw_circle_overhang (1.024)\n"
        "- n_free_throw_circle_dashes (6.0)\n"
        "- free_throw_dash_length (1.292)\n"
        "- free_throw_dash_spacing (1.292)\n"
        "- lane_space_mark_lengths ([[0.1667, 0.1667, 0.1667, 0.1667], "
        "[1.0, 0.1667, 0.1667, 0.1667]])\n"
        "- lane_space_mark_widths ([0.5, 0.75])\n"
        "- lane_space_mark_separations ([[3.0, 0.8333, 3.0, 3.0], "
        "[3.0, 3.0, 3.0, 3.0]])\n"
        "- painted_area_visibility ([True, True])\n"
        "- lane_boundary_visibility ([True, True])\n"
        "- lane_space_mark_visibility ([True, False])\n"
        "- lane_lower_defensive_box_marks_visibility (True)\n"
        "- baseline_lower_defensive_box_marks_int_sep (19.0)\n"
        "- baseline_to_lane_lower_defensive_box_marks (13.0)\n"
        "- lane_lower_defensive_box_marks_int_sep (10.0)\n"
        "- lower_defensive_box_mark_extension (0.5)\n"
        "- inbounding_line_to_baseline (28.0)\n"
        "- inbounding_line_anchor_side (1.0)\n"
        "- inbounding_line_in_play_ext (3.0)\n"
        "- inbounding_line_out_of_bounds_ext (0.0)\n"
        "- symmetric_inbounding_line (True)\n"
        "- substitution_line_ext_sep (8.5)\n"
        "- substitution_line_width (4.0)\n"
        "- restricted_arc_radius (4.0)\n"
        "- backboard_width (6.0)\n"
        "- backboard_thickness (0.171875)\n"
        "- basket_ring_inner_radius (0.75)\n"
        "- basket_ring_connector_width (0.5833)\n"
        "- basket_ring_connector_extension (0.5)\n"
        "- basket_ring_thickness (0.0656)\n"
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
    # Create a BasketballCourt() object to use for testing
    test_court = basketball_courts.BasketballCourt()

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
    # Create a sample NBA court to operate on
    test_nba = basketball_courts.NBACourt()

    # Get the standard colors for an NBA court. These will be used for
    # comparison
    standard_colors = test_nba.feature_colors

    # Update a color. The division line is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from black to white
    test_nba.update_colors({"division_line": "#ffffff"})

    # Get the updated colors
    updated_colors = test_nba.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working
    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample NBA court to operate on
    test_nba = basketball_courts.NBACourt()

    # Get the standard colors for an NBA court. These will be used for
    # comparison
    standard_colors = test_nba.feature_colors

    # Update a color. The division line is what's updated here as a means of
    # demonstration, but this could work for any parameter. It will be changed
    # from black to white
    test_nba.update_colors({"division_line": "#ffffff"})

    # Get the updated colors
    updated_colors = test_nba.feature_colors

    # Now, change the colors back to the original
    test_nba.reset_colors()

    # Get the final colors
    final_colors = test_nba.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_court_params():
    """Test that update_court_params() method operates as expected.

    This should work as long as the internal court parameters dictionary is
    updated when this method is called
    """
    # Create a sample NBA court to operate on
    test_nba = basketball_courts.NBACourt()

    # Get the standard dimensions for an NBA court. These will be used for
    # comparison
    standard_dimensions = test_nba.court_params

    # Update a dimension. The full-court length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 94 feet to 200 feet
    test_nba.update_court_params({"court_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_nba.court_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_court_params():
    """Test that reset_court_params() method operates as expected.

    This should work as long as the internal court parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample NBA court to operate on
    test_nba = basketball_courts.NBACourt()

    # Get the standard dimensions for an NBA court. These will be used for
    # comparison
    standard_dimensions = test_nba.court_params

    # Update a dimension. The full-court length is what's updated here as a
    # means of demonstration, but this could work for any parameter. It will be
    # changed from 94 feet to 200 feet
    test_nba.update_court_params({"court_length": 200.0})

    # Get the updated dimensions
    updated_dimensions = test_nba.court_params

    # Now, change the dimensions back to the original
    test_nba.reset_court_params()

    # Get the final dimensions
    final_dimensions = test_nba.court_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the courts' coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation NBA court. This should work for any of the
    # leagues supported by sportypy, but NBA is chosen out of convenience
    test_court_to_convert = basketball_courts.NBACourt()

    # Generate a court originating in meters
    nba_court_m = basketball_courts.NBACourt(units = "m")

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

    assert court_params_to_convert == nba_court_m.court_params


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "fiba": basketball_courts.FIBACourt(),
        "nba": basketball_courts.NBACourt(),
        "nba g league": basketball_courts.NBAGLeagueCourt(),
        "ncaa": basketball_courts.NCAACourt(),
        "nfhs": basketball_courts.NFHSCourt(),
        "wnba": basketball_courts.WNBACourt()
    }

    court = basketball_courts.BasketballCourt()

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
            test_court_plot = test_court.draw()

            assert isinstance(test_court, basketball_courts.BasketballCourt)
            assert isinstance(test_court_plot, matplotlib.axes.SubplotBase)


def test_custom_court_params():
    """Test that custom courts are able to be created.

    This test should pass so long as the courts' parameters are valid
    """
    # Start by defining the customized court parameters. These are a blending
    # of NCAA and NBA court parameters
    court_1_parameters = {
        "court_length": 94.0,
        "court_width": 50.0,
        "court_units": "ft",
        "line_thickness": 0.1667,
        "bench_side": "top",

        "court_apron_endline": 8.0,
        "court_apron_sideline": 5.0,
        "court_apron_to_boundary": 0.0,

        "center_circle_radius": [6.0, 2.1667, 5.0, 5.0],

        "basket_center_to_baseline": 5.25,
        "basket_center_to_three_point_arc": [23.75, 20.75],
        "basket_center_to_corner_three": 22.0,
        "backboard_face_to_baseline": 4.0,

        "lane_length": [19.0, 19.0, 19.0],
        "lane_width": 16.0,
        "paint_margin": [0.0, 0.0],

        "free_throw_circle_radius": 0.0,
        "free_throw_line_to_backboard": 15.0,
        "free_throw_circle_overhang": 1.024,
        "n_free_throw_circle_dashes": 6.0,
        "free_throw_dash_length": 1.292,
        "free_throw_dash_spacing": 1.292,

        "lane_space_mark_lengths": [
            [0.1667, 0.1667, 0.1667, 0.1667]
        ],
        "lane_space_mark_widths": 0.5,
        "lane_space_mark_separations": [
            [3.0, 0.8333, 3.0, 3.0]
        ],

        "painted_area_visibility": True,
        "lane_boundary_visibility": True,
        "lane_space_mark_visibility": True,
        "lane_lower_defensive_box_marks_visibility": True,

        "baseline_lower_defensive_box_marks_int_sep": 19.0,
        "baseline_to_lane_lower_defensive_box_marks": 13.0,
        "lane_lower_defensive_box_marks_int_sep": 10.0,
        "lower_defensive_box_mark_extension": 0.5,

        "inbounding_line_to_baseline": [28.0, 38.0],
        "inbounding_line_anchor_side": 1.0,
        "inbounding_line_in_play_ext": 3.0,
        "inbounding_line_out_of_bounds_ext": 0.0,
        "symmetric_inbounding_line": True,

        "substitution_line_ext_sep": 8.5,
        "substitution_line_width": 4.0,

        "restricted_arc_radius": 4.0,

        "backboard_width": 6.0,
        "backboard_thickness": 0.171875,

        "basket_ring_inner_radius": 0.75,
        "basket_ring_connector_width": 0.5833,
        "basket_ring_connector_extension": 0.5,
        "basket_ring_thickness": 0.0656
    }

    color_updates_1 = {
        "plot_background": "#d2ab6f",
        "defensive_half_court": "#d2ab6f",
        "offensive_half_court": "#d2ab6f",
        "court_apron": "#d2ab6f",
        "center_circle_outline": ["#000000", "#13294b"],
        "center_circle_fill": "#d2ab6f",
        "division_line": "#000000",
        "endline": "#000000",
        "sideline": "#000000",
        "two_point_range": ["#d2ab6f", "#e84a27"],
        "three_point_line": "#000000",
        "painted_area": "#d2ab6f",
        "lane_boundary": "#000000",
        "free_throw_circle_outline": "#000000",
        "free_throw_circle_fill": "#d2ab6f",
        "free_throw_circle_dash": "#000000",
        "lane_space_mark": "#000000",
        "inbounding_line": "#000000",
        "substitution_line": "#000000",
        "baseline_lower_defensive_box": "#000000",
        "lane_lower_defensive_box": "#000000",
        "team_bench_line": "#000000",
        "restricted_arc": "#000000",
        "backboard": "#000000",
        "basket_ring": "#f55b33",
        "net": "#ffffff"
    }

    test_court_1 = basketball_courts.BasketballCourt(
        court_updates = court_1_parameters,
        color_updates = color_updates_1
    )

    court_2_parameters = {
        "court_length": 94.0,
        "court_width": 50.0,
        "court_units": "ft",
        "line_thickness": 0.1667,
        "bench_side": "top",

        "court_apron_endline": 8.0,
        "court_apron_sideline": 5.0,
        "court_apron_to_boundary": 0.0,

        "center_circle_radius": 6.0,

        "basket_center_to_baseline": 5.25,
        "basket_center_to_three_point_arc": 0.0,
        "basket_center_to_corner_three": [21.6563, 20.75],
        "backboard_face_to_baseline": 4.0,

        "lane_length": 19.0,
        "lane_width": [16.0, 12.0],
        "paint_margin": 0.0,

        "free_throw_circle_radius": 0.0,
        "free_throw_line_to_backboard": 15.0,
        "free_throw_circle_overhang": 1.024,
        "n_free_throw_circle_dashes": 6.0,
        "free_throw_dash_length": 1.292,
        "free_throw_dash_spacing": 1.292,

        "lane_space_mark_lengths": 0.1667,
        "lane_space_mark_widths": 0.5,
        "lane_space_mark_separations": 1.5,

        "painted_area_visibility": True,
        "lane_boundary_visibility": True,
        "lane_space_mark_visibility": True,
        "lane_lower_defensive_box_marks_visibility": True,

        "baseline_lower_defensive_box_marks_int_sep": 19.0,
        "baseline_to_lane_lower_defensive_box_marks": 13.0,
        "lane_lower_defensive_box_marks_int_sep": 10.0,
        "lower_defensive_box_mark_extension": 0.5,

        "inbounding_line_to_baseline": 28.0,
        "inbounding_line_anchor_side": [1.0, -1.0],
        "inbounding_line_in_play_ext": 3.0,
        "inbounding_line_out_of_bounds_ext": 0.0,
        "symmetric_inbounding_line": False,

        "substitution_line_ext_sep": 8.5,
        "substitution_line_width": 4.0,

        "restricted_arc_radius": 4.0,

        "backboard_width": 6.0,
        "backboard_thickness": 0.171875,

        "basket_ring_inner_radius": 0.0,
        "basket_ring_connector_width": 0.5833,
        "basket_ring_connector_extension": 0.5,
        "basket_ring_thickness": 0.0656
    }

    color_updates_2 = {
        "plot_background": "#d2ab6f",
        "defensive_half_court": "#d2ab6f",
        "offensive_half_court": "#d2ab6f",
        "court_apron": "#d2ab6f",
        "center_circle_outline": "#000000",
        "center_circle_fill": ["#d2ab6f", "#e04e39"],
        "division_line": "#000000",
        "endline": "#000000",
        "sideline": "#000000",
        "two_point_range": "#d2ab6f",
        "three_point_line": ["#000000"],
        "painted_area": "#d2ab6f",
        "lane_boundary": "#000000",
        "free_throw_circle_outline": "#000000",
        "free_throw_circle_fill": "#d2ab6f",
        "free_throw_circle_dash": "#000000",
        "lane_space_mark": "#000000",
        "inbounding_line": "#000000",
        "substitution_line": "#000000",
        "baseline_lower_defensive_box": "#000000",
        "lane_lower_defensive_box": "#000000",
        "team_bench_line": "#000000",
        "restricted_arc": "#000000",
        "backboard": "#000000",
        "basket_ring": "#f55b33",
        "net": "#ffffff"
    }

    test_court_2 = basketball_courts.BasketballCourt(
        court_updates = court_2_parameters,
        color_updates = color_updates_2
    )

    assert isinstance(test_court_1, basketball_courts.BasketballCourt)
    assert isinstance(test_court_2, basketball_courts.BasketballCourt)


def test_court_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the courts' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = basketball_courts.NBACourt().draw(ax = ax, rotation = 90.0)

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_court_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the courts' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_court = basketball_courts.FIBACourt()
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
    test_court = basketball_courts.NBACourt()
    ax1 = test_court.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_court.draw(xlim = 150.0, ylim = 50.0)

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the court.

    This test should pass so long as an additional feature may be added to the
    court plot. The additional feature tested here is arbitrarily selected to
    be a division line shifted to either side of the court
    """
    new_division_line_1 = {
        "class": basketball_features.DivisionLine,
        "x_anchor": 23.5,
        "y_anchor": 0.0,
        "court_length": 94.0,
        "court_width": 50.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#000000",
        "edgecolor": None,
        "zorder": 1
    }

    new_division_line_2 = {
        "class": basketball_features.DivisionLine,
        "x_anchor": -23.5,
        "y_anchor": 0.0,
        "court_length": 94.0,
        "court_width": 50.0,
        "feature_thickness": 25.0,
        "visible": True,
        "facecolor": "#000000",
        "edgecolor": None,
        "zorder": 1
    }

    ax = basketball_courts.NBACourt(
        new_feature_1 = new_division_line_1,
        new_feature_2 = new_division_line_2
    ).draw()

    plt.close("all")

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_zero_radii():
    """Test that court features work even with a radius of 0.0.

    This test should pass so long as the errors are handled correctly when a
    curved feature is created but the radius is 0.0
    """
    court_1_updates = {
        "basket_center_to_three_point_arc": 0.1667,
        "free_throw_circle_radius": 0.0,
        "symmetric_inbounding_line": False,
        "basket_ring_inner_radius": 0.0
    }

    court_2_updates = {
        "basket_center_to_three_point_arc": 0.0,
        "basket_ring_inner_radius": -0.0656
    }

    ax1 = basketball_courts.NBACourt(
        court_updates = court_1_updates
    ).draw()

    ax2 = basketball_courts.NCAACourt(
        court_updates = court_2_updates
    ).draw()

    plt.close("all")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_court_plot_with_xlim_ylim():
    """Test that court sections can be drawn (e.g. offensive half-court).

    This test should pass so long as there are no errors when drawing a section
    of the court
    """
    ax1 = basketball_courts.NCAACourt().draw(
        display_range = "offensive half court"
    )

    assert isinstance(ax1, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = basketball_courts.NBACourt(rotation = 90).draw(
        display_range = "offense"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)
