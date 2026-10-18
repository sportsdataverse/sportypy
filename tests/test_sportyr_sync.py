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


def test_package_level_names_not_rebound_by_volleyball():
    assert surfaces.NCAACourt.__module__ == "sportypy.surfaces.tennis"
    assert surfaces.volleyball.NCAACourt.__module__ == "sportypy.surfaces.volleyball"
    assert surfaces.FIVBCourt.__module__ == "sportypy.surfaces.volleyball"


def test_sync_write_mode_adds_entry(tmp_path, monkeypatch, capsys):
    mod = _sync_module()
    target = tmp_path / "target.json"
    target.write_text(json.dumps({"hockey": {"nhl": {"a": 1, "b": 2}}}, indent=4))
    src = tmp_path / "src.json"
    entry = SPORTYR["hockey"]["pwhl"]
    src.write_text(json.dumps({
        "hockey": {"nhl": {"a": 1, "b": 3}, "pwhl": entry}, "lacrosse": {"x": {}}}, indent=2))
    monkeypatch.setattr(mod, "TARGET", target)
    assert mod.main([str(src)]) == 0
    out = capsys.readouterr().out
    assert "drift: hockey/nhl/b: 2 vs 3" in out
    assert "sport 'lacrosse' absent" in out
    assert json.loads(target.read_text())["hockey"]["pwhl"] == entry
    assert mod.main([str(src), "--check"]) == 0


FOUR_SPACE_SRC = """{
    "softball": {
        "custom": {
            "a": 0.0
        },
        "ncaa": {
            "field_units": "ft",

            "a": 1.5,
            "nested": {
                "b": 2
            }
        }
    }
}
"""


def test_entry_text_and_add_sport_keep_four_space_style():
    mod = _sync_module()
    block = mod.entry_text(FOUR_SPACE_SRC, "softball", "ncaa")
    assert block.startswith('        "ncaa": {\n            "field_units": "ft",')
    assert '\n                "b": 2\n' in block
    target = '{\n    "hockey": {\n        "nhl": {\n            "a": 1\n        }\n    }\n}'
    out = mod.add_sport(target, "softball", block)
    assert json.loads(out)["softball"]["ncaa"] == json.loads(FOUR_SPACE_SRC)["softball"]["ncaa"]
    assert json.loads(out)["hockey"] == {"nhl": {"a": 1}}
    assert '\n    "softball": {\n        "ncaa": {\n            "field_units"' in out


def test_add_sport_unknown_to_sportyr_is_a_usage_error(tmp_path, capsys):
    src = tmp_path / "src.json"
    src.write_text(json.dumps({"hockey": {}}))
    with pytest.raises(SystemExit) as e:
        _sync_module().main([str(src), "--add-sport", "curling2"])
    assert e.value.code == 2
    assert "curling2" in capsys.readouterr().err
