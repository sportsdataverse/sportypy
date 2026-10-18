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
    # FootballField does not support ``units`` (its features assume yards)
    assert params[f"{prefix}_units"] == ("yd" if issubclass(cls, FootballField) else "in")
    _same_params(params, getattr(fresh, f"{prefix}_params"))


def test_reset_after_update_keeps_league():
    """sportyR-style base class with a league: reset must find the league again."""
    field = SoftballField(league_code="ncaa", rotation=90.0)
    field.update_colors({"base": "#000000"})
    field.reset_field_params()
    assert field.league_code == "ncaa"
    assert field.field_params == SoftballField(league_code="ncaa").field_params


# FootballField does not support ``units`` (its features assume yards)
UNIT_CASES = [(c, i) for c, i in zip(CASES, IDS) if not issubclass(c[0], FootballField)]


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
