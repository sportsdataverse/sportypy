"""Shared-base behaviour every surface inherits.

- ``update_*`` / ``reset_*`` keep rotation, translation, league and units.
- display padding is 5 rule-book units, converted to the surface's units.
- the baseball full-field range matches sportyR's ``geom_baseball()``.
"""

import json
import math
from pathlib import Path
from numbers import Number

import numpy as np
import pytest

from sportypy.surfaces.baseball import BaseballField, MLBField
from sportypy.surfaces.basketball import BasketballCourt, NBACourt
from sportypy.surfaces.curling import CurlingSheet
from sportypy.surfaces.football import FootballField, NFHSField
from sportypy.surfaces.hockey import HockeyRink
from sportypy.surfaces.lacrosse import LacrosseField, NCAAWLacrosseField, NLLField
from sportypy.surfaces.soccer import SoccerPitch
from sportypy.surfaces.softball import NCAASoftballField, SoftballField
from sportypy.surfaces.tennis import TennisCourt
from sportypy.surfaces.volleyball import VolleyballCourt

CONV = json.loads(
    (Path(__file__).parents[1] / "sportypy/data/unit_conversions.json").read_text()
)

# (class, constructor kwargs, params prefix: field/court/rink/sheet/pitch)
CASES = [
    (BaseballField, {"league_code": "mlb"}, "field"),
    (MLBField, {}, "field"),
    (SoftballField, {"league_code": "ncaa"}, "field"),
    (NCAASoftballField, {}, "field"),
    (BasketballCourt, {"league_code": "nba"}, "court"),
    (NBACourt, {}, "court"),
    (CurlingSheet, {"league_code": "wcf"}, "sheet"),
    (FootballField, {"league_code": "nfl"}, "field"),
    (NFHSField, {"n_players": 8}, "field"),
    (HockeyRink, {"league_code": "nhl"}, "rink"),
    (SoccerPitch, {"league_code": "epl"}, "pitch"),
    (TennisCourt, {"league_code": "atp"}, "court"),
    (VolleyballCourt, {"league_code": "fivb"}, "court"),
    (LacrosseField, {"league_code": "nll"}, "field"),
    (NLLField, {}, "field"),
    (NCAAWLacrosseField, {}, "field"),
]
IDS = [c[0].__module__.split(".")[-1] + "." + c[0].__name__ for c in CASES]
STATE = {"rotation": 90.0, "x_trans": 10.0, "y_trans": -5.0, "units": "in"}


def _same_params(a, b):
    assert a.keys() == b.keys()
    for k in a:
        if isinstance(a[k], Number) and not isinstance(a[k], bool):
            assert a[k] == pytest.approx(b[k], rel=1e-12), k
        else:
            assert a[k] == b[k], k


@pytest.mark.parametrize("cls, kwargs, prefix", CASES, ids=IDS)
@pytest.mark.parametrize(
    "op", ["update_colors", "update_params", "reset_colors", "reset_params"]
)
def test_update_and_reset_keep_state(cls, kwargs, prefix, op):
    surface = cls(**kwargs, **STATE)
    fresh = cls(**kwargs, **STATE)
    if op == "update_colors":
        surface.update_colors({})
    elif op == "update_params":
        getattr(surface, f"update_{prefix}_params")({})
    elif op == "reset_colors":
        surface.reset_colors()
    else:
        getattr(surface, f"reset_{prefix}_params")()

    assert np.allclose(surface._rotation.get_matrix(), fresh._rotation.get_matrix())
    assert (surface.x_trans, surface.y_trans) == (10.0, -5.0)
    assert surface.league_code == fresh.league_code
    params = getattr(surface, f"{prefix}_params")
    assert params[f"{prefix}_units"] == "in"
    _same_params(params, getattr(fresh, f"{prefix}_params"))


def test_reset_after_update_keeps_league():
    """sportyR-style base class with a league: reset must find the league again."""
    field = SoftballField(league_code="ncaa", rotation=90.0)
    field.update_colors({"base": "#000000"})
    field.reset_field_params()
    assert field.league_code == "ncaa"
    assert field.field_params == SoftballField(league_code="ncaa").field_params


UNIT_CASES = list(zip(CASES, IDS))


@pytest.mark.parametrize(
    "cls, kwargs, prefix", [c for c, _ in UNIT_CASES], ids=[i for _, i in UNIT_CASES]
)
@pytest.mark.parametrize(
    "display_range", ["full", "offense", "ozone", "infield", "house"]
)
def test_display_range_scales_with_units(cls, kwargs, prefix, display_range):
    """Every display limit (padding included) is a length, so it scales by the
    unit factor: 5 rule-book units of padding, not 5 of whatever unit."""

    native = cls(**kwargs)
    rulebook = getattr(native, f"{prefix}_params")[f"{prefix}_units"]
    target = "m" if rulebook != "m" else "ft"
    converted = cls(**kwargs, units=target)
    factor = CONV[target] / CONV[rulebook]
    got = np.array(converted._get_plot_range_limits(display_range))
    want = np.array(native._get_plot_range_limits(display_range)) * factor
    assert np.allclose(got, want, rtol=1e-9, atol=1e-9)


def test_mlb_meters_pad_is_five_feet():
    field = MLBField(units="m")
    _, (_, y_max) = field._get_plot_range_limits("full")
    assert y_max == pytest.approx(
        field.field_params["center_field_distance"] + 5 * 0.3048
    )


def test_baseball_full_range_matches_sportyr():
    """sportyR geom_baseball(): full x spans the foul poles with no padding,
    y runs from 5 ft behind the backstop to 5 ft past center field."""
    p = MLBField().field_params
    xlim, ylim = MLBField()._get_plot_range_limits("full")
    assert xlim == pytest.approx(
        (
            p["left_field_distance"] * math.cos(3 * math.pi / 4),
            p["right_field_distance"] * math.cos(math.pi / 4),
        )
    )
    assert ylim == pytest.approx(
        (-(p["backstop_radius"] + 5), p["center_field_distance"] + 5)
    )


@pytest.mark.parametrize("unit", ["mm", "millimeters", "millimetre"])
def test_feet_to_millimetres(unit):
    """1 ft = 304.8 mm, whichever spelling of millimetres is used."""
    rink = HockeyRink(league_code="nhl")
    assert rink._convert_units(1.0, "ft", unit) == pytest.approx(304.8)
    assert HockeyRink(league_code="nhl", units=unit).rink_params["rink_length"] == pytest.approx(200.0 * 304.8)


@pytest.mark.parametrize("units, factor", [("ft", 3.0), ("m", 0.9144), ("in", 36.0)])
def test_football_field_honours_units(units, factor):
    """Every football polygon (and the yard numbers) scales by the unit factor,
    so the field looks the same in any units."""
    from sportypy.surfaces.football import NFLField

    yd, conv = NFLField(), NFLField(units=units)
    assert conv.field_params["field_units"] == units
    assert conv.field_params["field_length"] == pytest.approx(100.0 * factor)
    assert len(yd._features) == len(conv._features)
    for a, b in zip(yd._features, conv._features):
        da, db = a._translate_feature(), b._translate_feature()
        assert np.allclose(da["x"] * factor, db["x"]) and np.allclose(da["y"] * factor, db["y"])
    assert np.allclose(yd.yardage_markers["marked_line"] * factor, conv.yardage_markers["marked_line"])
    got = np.array(conv._get_plot_range_limits("redzone"))
    assert np.allclose(got, np.array(yd._get_plot_range_limits("redzone")) * factor)


def test_a_yard_is_three_feet():
    """1 yd = 3 ft exactly (sportyR uses 1 / 3); it was 0.3333 (0.01% off)."""
    rink = HockeyRink(league_code="nhl")
    assert rink._convert_units(1.0, "yd", "ft") == pytest.approx(3.0, rel=1e-15)
    assert rink._convert_units(100.0, "yards", "in") == pytest.approx(3600.0, rel=1e-15)


@pytest.mark.parametrize(
    "cls, kwargs, prefix, key",
    [
        (VolleyballCourt, {"league_code": "fivb"}, "court", "substitution_zone_rep_pattern"),
        (BasketballCourt, {"league_code": "nba"}, "court", "n_free_throw_circle_dashes"),
    ],
)
def test_counts_are_not_converted_with_units(cls, kwargs, prefix, key):
    """A count (dashes, repetitions) is not a length: units leave it alone, so
    the surface draws the same number of marks in any units."""
    native = cls(**kwargs)
    for units in ("in", "cm"):
        converted = cls(**kwargs, units=units)
        assert getattr(converted, f"{prefix}_params")[key] == getattr(native, f"{prefix}_params")[key]
        assert len(converted._features) == len(native._features)
