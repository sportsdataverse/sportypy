"""Tests for the curling sheet classes of the module.

@author: Ross Drucker
"""

import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import sportypy.surfaces.curling as curling_sheets
import sportypy._feature_classes.curling as curling_features


def test_base_class_no_league():
    """Test that the base class, CurlingSheet, can be instantiated.

    This test should pass so long as the CurlingSheet class can be successfully
    instantiated without a league passed to it. This should create an instance
    of CurlingSheet with the sheet_params attribute as an empty dictionary
    """
    test_sheet = curling_sheets.CurlingSheet()

    assert test_sheet.sheet_params == {}


def test_wcf_params():
    """Test that the WCFSheet class can be instantiated.

    This test should pass so long as the WCFSheet class can be successfully
    instantiated with the correct parameters.
    """
    wcf_params = {
        "sheet_units": "ft",
        "sheet_length": 150.0,
        "sheet_width": 15.5833,

        "apron_behind_back": 1.5,
        "apron_along_side": 1.5,

        "tee_line_to_center": 57.0,
        "tee_line_thickness": 0.0417,

        "back_line_thickness": 0.0417,
        "back_line_to_tee_line": 6.0,

        "hack_line_thickness": 0.0417,
        "hack_foothold_width": 0.5,
        "hack_foothold_gap": 0.5,
        "hack_foothold_depth": 0.6667,

        "hog_line_to_tee_line": 21.0,
        "hog_line_thickness": 0.3333,

        "centre_line_extension": 12.0,
        "centre_line_thickness": 0.0417,

        "house_ring_radii": [6.0, 4.0, 2.0],
        "button_radius": 0.5,

        "courtesy_line_thickness": 0.0417,
        "courtesy_line_length": 0.5,
        "courtesy_line_to_hog_line": 4.0
    }

    test_params = curling_sheets.WCFSheet().sheet_params

    assert wcf_params == test_params


def test_cani_plot_leagues_no_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    With no league code provided, this method should produce a list of all
    available league codes
    """
    # Create a CurlingSheet() object to use for testing
    test_sheet = curling_sheets.CurlingSheet()

    # Get the available league codes
    available_league_codes = [k for k in test_sheet.league_dimensions.keys()]
    available_league_codes.sort()

    # Generate the expected output for cani_plot_leagues() with no league code
    exp_pl_empty_league_code = ""

    exp_pl_empty_league_code = (
        "The following curling leagues are available with sportypy:\n"
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
    test_sheet.cani_plot_leagues()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_empty_league_code.getvalue() == exp_pl_empty_league_code


def test_cani_plot_leagues_wcf():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed either "wcf", "WCF", or any combination of capitalized and
    lower-case letters of "W", "C", and "F", this should return the same
    message
    """
    # Create a CurlingSheet() object to use for testing
    test_sheet = curling_sheets.CurlingSheet()

    # Generate the expected output for cani_plot_leagues() with a league code
    # (this will use WCF as a test)
    exp_pl_wcf_league_code = "WCF comes with sportypy and is ready to use!\n"

    # Initialize the output-captures
    pl_wcf_league_code_lower = io.StringIO()
    pl_wcf_league_code_upper = io.StringIO()
    pl_wcf_league_code_mixed = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = pl_wcf_league_code_lower
    test_sheet.cani_plot_leagues("wcf")

    sys.stdout = pl_wcf_league_code_upper
    test_sheet.cani_plot_leagues("WCF")

    sys.stdout = pl_wcf_league_code_mixed
    test_sheet.cani_plot_leagues("wCf")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_wcf_league_code_lower.getvalue() == exp_pl_wcf_league_code
    assert pl_wcf_league_code_upper.getvalue() == exp_pl_wcf_league_code
    assert pl_wcf_league_code_mixed.getvalue() == exp_pl_wcf_league_code


def test_cani_plot_leagues_bad_league_code():
    """Test cani_plot_leagues() method will return appropriate message.

    When passed a bad/unsupported league, the cani_plot_leagues() method should
    return a message that the league is unsupported
    """
    # Create a CurlingSheet() object to use for testing
    test_sheet = curling_sheets.CurlingSheet()

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
    test_sheet.cani_plot_leagues("test_league")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert pl_bad_league_code.getvalue() == exp_pl_bad_league_code


def test_cani_change_dimensions():
    """Test cani_change_dimensions() method will return appropriate message.

    When called, this should return a list of the parameterizations of the
    sheet that may be changed by a user
    """
    # Create a CurlingSheet() object to use for testing
    test_sheet = curling_sheets.WCFSheet()

    # Generate the expected output for cani_change_dimensions()
    exp_change_dimensions = (
        "The following features can be reparameterized via the sheet_updates "
        "parameter, with the current value in parenthesis:\n\n"
        "- sheet_units (ft)\n"
        "- sheet_length (150.0)\n"
        "- sheet_width (15.5833)\n"
        "- apron_behind_back (1.5)\n"
        "- apron_along_side (1.5)\n"
        "- tee_line_to_center (57.0)\n"
        "- tee_line_thickness (0.0417)\n"
        "- back_line_thickness (0.0417)\n"
        "- back_line_to_tee_line (6.0)\n"
        "- hack_line_thickness (0.0417)\n"
        "- hack_foothold_width (0.5)\n"
        "- hack_foothold_gap (0.5)\n"
        "- hack_foothold_depth (0.6667)\n"
        "- hog_line_to_tee_line (21.0)\n"
        "- hog_line_thickness (0.3333)\n"
        "- centre_line_extension (12.0)\n"
        "- centre_line_thickness (0.0417)\n"
        "- house_ring_radii ([6.0, 4.0, 2.0])\n"
        "- button_radius (0.5)\n"
        "- courtesy_line_thickness (0.0417)\n"
        "- courtesy_line_length (0.5)\n"
        "- courtesy_line_to_hog_line (4.0)\n"
        "\n"
        "These parameters may be updated with the update_sheet_params() "
        "method\n"
    )

    # Initialize the output-capture
    change_dimensions = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = change_dimensions
    test_sheet.cani_change_dimensions()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert change_dimensions.getvalue() == exp_change_dimensions


def test_cani_color_features():
    """Test cani_color_features() method will return appropriate message.

    When called, this should return a list of the ice sheet's features and
    their default/standard colors
    """
    # Create a CurlingSheet() object to use for testing
    test_sheet = curling_sheets.CurlingSheet()

    # Generate the expected output for cani_color_features()
    exp_color_features = (
        "The following features can be colored via the color_updates "
        "parameter, with the current value in parenthesis:\n"
    )

    for k, v in test_sheet.feature_colors.items():
        exp_color_features = f"{exp_color_features}\n- {k} ({v})"

    exp_color_features = (
        f"{exp_color_features}\n\nThese colors may be updated with the "
        "update_colors() method\n"
    )

    # Initialize the output-capture
    color_features = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = color_features
    test_sheet.cani_color_features()

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert color_features.getvalue() == exp_color_features


def test_update_colors():
    """Test that update_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called
    """
    # Create a sample WCF sheet to operate on
    test_wcf = curling_sheets.WCFSheet()

    # Get the standard colors for an WCF sheet. These will be used for
    # comparison
    standard_colors = test_wcf.feature_colors

    # Update a color. The top end of the sheet color is what's updated here as
    # a means of demonstration, but this could work for any parameter. It will
    # be changed from white to dark blue
    test_wcf.update_colors({"end_1": "#13294b"})

    # Get the updated colors
    updated_colors = test_wcf.feature_colors

    # So long as the updated colors dictionary isn't identical to the standard
    # colors dictionary, this method is working

    assert standard_colors != updated_colors


def test_reset_colors():
    """Test that reset_colors() method operates as expected.

    This should work as long as the internal feature colors dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial colors
    """
    # Create a sample WCF sheet to operate on
    test_wcf = curling_sheets.WCFSheet()

    # Get the standard colors for an WCF sheet. These will be used for
    # comparison
    standard_colors = test_wcf.feature_colors

    # Update a color. The top end of the sheet color is what's updated here as
    # a means of demonstration, but this could work for any parameter. It will
    # be changed from white to dark blue
    test_wcf.update_colors({"end_1": "#13294b"})

    # Get the updated colors
    updated_colors = test_wcf.feature_colors

    # Now, change the colors back to the original
    test_wcf.reset_colors()

    # Get the final colors
    final_colors = test_wcf.feature_colors

    assert standard_colors != updated_colors
    assert updated_colors != final_colors
    assert standard_colors == final_colors


def test_update_sheet_params():
    """Test that update_sheet_params() method operates as expected.

    This should work as long as the internal sheet parameters dictionary is
    updated when this method is called
    """
    # Create a sample WCF sheet to operate on
    test_wcf = curling_sheets.WCFSheet()

    # Get the standard dimensions for an WCF sheet. These will be used for
    # comparison
    standard_dimensions = test_wcf.sheet_params

    # Update a dimension. The hack foothold is what's updated here as a means
    # of demonstration, but this could work for any parameter. It will be
    # changed from 0.5 feet to 0.75 feet
    test_wcf.update_sheet_params({"hack_foothold_width": 0.75})

    # Get the updated dimensions
    updated_dimensions = test_wcf.sheet_params

    # So long as the updated dimensions dictionary isn't identical to the
    # standard dimensions dictionary, this method is working

    assert standard_dimensions != updated_dimensions


def test_reset_sheet_params():
    """Test that reset_sheet_params() method operates as expected.

    This should work as long as the internal sheet parameters dictionary is
    updated when this method is called, and returns an identical dictionary to
    the initial dimensions
    """
    # Create a sample WCF sheet to operate on
    test_wcf = curling_sheets.WCFSheet()

    # Get the standard dimensions for an WCF sheet. These will be used for
    # comparison
    standard_dimensions = test_wcf.sheet_params

    # Update a dimension. The hack foothold is what's updated here as a means
    # of demonstration, but this could work for any parameter. It will be
    # changed from 0.5 feet to 0.75 feet
    test_wcf.update_sheet_params({"hack_foothold_width": 0.75})

    # Get the updated dimensions
    updated_dimensions = test_wcf.sheet_params

    # Now, change the dimensions back to the original
    test_wcf.reset_sheet_params()

    # Get the final dimensions
    final_dimensions = test_wcf.sheet_params

    assert standard_dimensions != updated_dimensions
    assert updated_dimensions != final_dimensions
    assert standard_dimensions == final_dimensions


def test_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the sheets' coordinates change in
    accordance with a user's wishes
    """
    # Start by creating a regulation WCF sheet. This should work for any of the
    # leagues supported by sportypy, but WCF is chosen out of convenience
    test_sheet_to_convert = curling_sheets.WCFSheet()

    # Generate a sheet originating in meters
    wcf_sheet_m = curling_sheets.WCFSheet(units = "m")

    # Convert the sheet dimensions from feet to meters
    sheet_params_to_convert = test_sheet_to_convert.sheet_params

    for k, v in sheet_params_to_convert.items():
        sheet_params_to_convert[k] = test_sheet_to_convert._convert_units(
            v,
            "ft",
            "m"
        )

    sheet_params_to_convert["sheet_units"] = "m"

    assert sheet_params_to_convert == wcf_sheet_m.sheet_params


def test_unsupported_unit_conversions():
    """Test that unit conversion functionality works as intended.

    This test should pass so long as the sheets' coordinates do not change when
    a user wishes to use an unsupported unit
    """
    # There are 22 parameters in an WCF sheet
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
    )

    # Initialize the output-capture
    unit_error_string = io.StringIO()

    # Change the system output to be capturable and capture each testing output
    sys.stdout = unit_error_string
    curling_sheets.WCFSheet(units = "foots")

    # Change back to standard output
    sys.stdout = sys.__stdout__

    assert unit_error_string.getvalue() == exp_unit_error_string


def test_sheet_plot_rotation():
    """Test that the plot rotation functionality works as expected.

    This test should pass so long as the sheets' plot may be rotated without
    error
    """
    fig, ax = plt.subplots()

    ax = curling_sheets.WCFSheet().draw(ax = ax, rotation = 90.0)

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_sheet_plot_tuple_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the sheets' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_sheet = curling_sheets.WCFSheet()
    ax1 = test_sheet.draw(xlim = (-25.0, 15.0), ylim = (-25.0, 25.0))
    ax2 = test_sheet.draw(xlim = (25.0, -15.0), ylim = (25.0, -25.0))
    ax3 = test_sheet.draw(xlim = (0.0, 0.0), ylim = (0.0, 0.0))

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
    assert isinstance(ax3, matplotlib.axes.SubplotBase)


def test_supported_leagues():
    """Test that the child classes for each league are fully operational.

    This is done by associating a league with its child class in a dictionary
    and attempting to instantiate it, then verifying that no errors are caused
    """

    league_class_dict = {
        "wcf": curling_sheets.WCFSheet(),
    }

    leagues = [
        k.lower()
        for k
        in curling_sheets.CurlingSheet().league_dimensions.keys()
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
            test_sheet = league_class_dict[league]

            assert isinstance(test_sheet, curling_sheets.CurlingSheet)


def test_sheet_plot_singular_xlim_and_ylim():
    """Test that xlim and ylim setting functionality works as intended.

    This test should pass so long as the sheets' plot may be customized by
    setting the xlim and ylim parameters
    """
    test_sheet = curling_sheets.WCFSheet()
    ax1 = test_sheet.draw(xlim = 10.0, ylim = 10.0)
    ax2 = test_sheet.draw(xlim = 150.0, ylim = 150.0)

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)


def test_sheet_plot_no_parameters():
    """Test that round features with no radius provided will still work.

    This is to ensure that the class can always be instantiated, but the
    feature may not be perfectly plotted
    """
    # Create the test plots
    test_zero_house_ring_rad = curling_sheets.WCFSheet(
        sheet_updates = {
            "house_ring_radii": [0.0, 0.0, 0.0]
        }
    ).draw()

    assert isinstance(test_zero_house_ring_rad, matplotlib.axes.SubplotBase)


def test_additional_feature():
    """Test that additional features can be added to the sheet.

    This test should pass so long as an additional feature may be added to the
    sheet plot. The additional feature tested here is arbitrarily selected to
    be the hog lines shifted in either direction
    """
    new_hog_line_1 = {
        "class": curling_features.HogLine,
        "x_anchor": 0.0,
        "y_anchor": 25.0,
        "sheet_length": 150.0,
        "sheet_width": 15.5833,
        "feature_thickness": 0.5,
        "visible": True,
        "facecolor": "#13294b",
        "edgecolor": "#e04e39",
        "zorder": 1
    }

    new_hog_line_2 = {
        "class": curling_features.HogLine,
        "x_anchor": 0.0,
        "y_anchor": -25.0,
        "sheet_length": 150.0,
        "sheet_width": 15.5833,
        "feature_thickness": 0.5,
        "visible": True,
        "facecolor": "#13294b",
        "edgecolor": "#e04e39",
        "zorder": 1
    }

    ax = curling_sheets.WCFSheet(
        new_feature_1 = new_hog_line_1,
        new_feature_2 = new_hog_line_2
    ).draw()

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_rotated_surface_plot():
    """Test that the field may be properly rotated about the origin.

    This test should pass so long as there are no errors when drawing a rotated
    plot of the surface
    """
    ax = curling_sheets.WCFSheet(rotation = 90).draw(
        display_range = "house"
    )

    assert isinstance(ax, matplotlib.axes.SubplotBase)


def test_display_range_none_empty_string():
    """Test that the sheet defaults to display_range == "full" if None passed.

    This test should pass so long as there are no erros when drawing a sheet
    with no specified display range
    """
    ax1 = curling_sheets.WCFSheet().draw(display_range = None)
    ax2 = curling_sheets.WCFSheet().draw(display_range = "")

    assert isinstance(ax1, matplotlib.axes.SubplotBase)
    assert isinstance(ax2, matplotlib.axes.SubplotBase)
