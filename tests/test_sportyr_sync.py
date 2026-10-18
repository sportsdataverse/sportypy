"""Tests for the sportyR-synced surfaces (PWHL rink, Curling Canada sheet,
volleyball export) and tools/sync_dimensions.py.

tests/data/sportyr_surface_dimensions.json holds verbatim sportyR entries
(see its ``_provenance`` key); no sibling checkout is needed.
"""

import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

import sportypy.surfaces as surfaces
from sportypy.surfaces.curling import CurlingCanadaSheet
from sportypy.surfaces.hockey import PWHLRink

HERE = Path(__file__).parent
SPORTYR = json.loads((HERE / "data/sportyr_surface_dimensions.json").read_text())


def _drawn_patches(obj):
    ax = obj.draw()
    n = len(ax.patches) + len(ax.collections) + len(ax.lines)
    plt.close("all")
    return n


def test_volleyball_exported_from_surfaces():
    assert surfaces.FIVBCourt and surfaces.NCAACourt and surfaces.USAVolleyballCourt


def test_pwhl_rink_matches_sportyr():
    rink = PWHLRink()
    assert rink.league_code == "pwhl"
    for key, value in SPORTYR["hockey"]["pwhl"].items():
        assert rink.rink_params[key] == value, key
    assert _drawn_patches(rink) > 0


def test_curling_canada_sheet_matches_sportyr():
    sheet = CurlingCanadaSheet()
    assert sheet.league_code == "curling canada"
    for key, value in SPORTYR["curling"]["curling canada"].items():
        assert sheet.sheet_params[key] == value, key
    assert _drawn_patches(sheet) > 0


def _sync_module():
    spec = importlib.util.spec_from_file_location(
        "sync_dimensions", HERE.parent / "tools/sync_dimensions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_sync_check_is_clean_against_vendored_entries(tmp_path):
    src = tmp_path / "dims.json"
    src.write_text(json.dumps({k: v for k, v in SPORTYR.items() if k != "_provenance"}))
    assert _sync_module().main([str(src), "--check"]) == 0


def test_sync_check_detects_missing_league(tmp_path):
    src = tmp_path / "dims.json"
    src.write_text(json.dumps({"hockey": {"newleague": {"rink_units": "ft"}}}))
    assert _sync_module().main([str(src), "--check"]) == 1
