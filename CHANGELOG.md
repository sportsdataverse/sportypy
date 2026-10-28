# Changelog

## [1.2.3](https://github.com/sportsdataverse/sportypy/compare/v1.2.2...v1.2.3) (2026-10-28)

### Bug Fixes

* **base:** read the bundled data with importlib.resources.files instead of the deprecated open_text ([#32](https://github.com/sportsdataverse/sportypy/issues/32)) ([a558f94](https://github.com/sportsdataverse/sportypy/commit/a558f94aea7f789bb8d2cef630962d04fbd320f6))

## [1.2.2](https://github.com/sportsdataverse/sportypy/compare/v1.2.1...v1.2.2) (2026-10-28)

### Performance Improvements

* **base:** draw circles with 1000 points, as sportyR does, instead of 10000 ([#31](https://github.com/sportsdataverse/sportypy/issues/31)) ([ea9b31e](https://github.com/sportsdataverse/sportypy/commit/ea9b31e101388eb9ded5359a7393560072002491))

## [1.2.1](https://github.com/sportsdataverse/sportypy/compare/v1.2.0...v1.2.1) (2026-10-28)

### Bug Fixes

* **plot:** support matplotlib 3.8+ contour sets and axes types ([e0d214a](https://github.com/sportsdataverse/sportypy/commit/e0d214a17c54b6a5e2ad57992054f935695955aa))

## `sportypy` 1.2.0

Brings `sportypy` in line with `sportyR` 2.3.0 and its geometry fixes.

### New surfaces (ported from `sportyR`)

- Lacrosse: `LacrosseField`, with `NCAAMLacrosseField`, `NCAAWLacrosseField`, `NLLField` (box lacrosse), `PLLField`, `USAMLacrosseField`, `USAWLacrosseField` and `WorldLacrosseField` (box). Every polygon matches what `sportyR`'s `geom_lacrosse()` draws, including these lacrosse fixes:
  - NLL and World Lacrosse: the neutral zone spans the 85 ft between the restraining lines (it was 0 long), and the penalty box fills start at the inside edge of the boards.
  - NCAA and USA Lacrosse women's: each goal-fan hash mark is placed on the fan arc at the angle it is rotated by, at its stated distance along the arc.
  - The `"full"`, `"offense"` and `"defense"` display ranges take in the NLL and World Lacrosse player benches, penalty boxes and off-field officials' box.
  - `goal_arc_line_thickness` defaults to 0, so a goal arc added through `field_updates` without a thickness is a line, not a solid block.
  - A `center_face_off_marker` colour you pass is kept; the contrasting `#ffcb05` default (NCAA men's) applies only when you pass no marker colour and the marker would match the centre line, so recolouring only `center_line` leaves the marker white.
  - NCAA and USA Lacrosse women's: the 8 m arc follows the NCAA rule: two lines at 45 degrees from where the goal line extended crosses the goal circle, joined by a 10.6 m arc about the centre of the goal line; the hash marks sit on that circle, and the goal-line-extended marks are 0.305 m long.
  - PLL: the two-point arc runs parallel to the sidelines 13 yd from the centre of the goal line (new parameter `goal_arc_parallel_line_to_center`), then becomes a 15 yd arc (2024 PLL Rulebook). Without that parameter the arc is a semicircle.
  - NLL and World Lacrosse: each penalty box is `penalty_box_length` (8 ft) inside its walls; the outer wall moved out 0.25 ft.
  - Leagues without a goal fan draw no fan polygon (it was a hidden zero-size shape).
  - NCAA and USA Lacrosse women's: the 8 m arc's hash marks are centred on the middle of the arc's line (10.5495 m from the centre of the goal line), since they bisect it.
- Softball: `SoftballField` and `NCAASoftballField`.
- Hockey: `PWHLRink`, the PWHL's own rink dimensions.
- Curling: `CurlingCanadaSheet`.
- Volleyball courts are now importable from `sportypy.surfaces`: `FIVBCourt`, `USAVolleyballCourt` and `VolleyballCourt`. `sportypy.surfaces.NCAACourt` is still the tennis court; import the volleyball one with `from sportypy.surfaces.volleyball import NCAACourt`.

### Changed output for existing leagues

League dimensions now equal `sportyR` 2.3.0's, with its corrections (`tools/sync_dimensions.py --align`):

- Baseball (MLB, MiLB): bases are 1.5 ft square (were 1.25 ft).
- Basketball (NFHS): the restricted arc is drawn as `sportyR` draws it. NFHS has no restricted-arc radius, so this is a small mark under the basket; it was hidden before.
- Basketball (NBA, NBA G League, WNBA): the second, 12 ft lane is hidden (`[True, False]` visibility, as in `sportyR`). It was drawn fully transparent before, so plots look the same.
- Football (NCAA): the restricted area is 1.8889 yd wide (was 2 yd), so the coaching line sits 6 ft outside the sideline, measured from its inside edge (NCAA Football Rules 1-2-4-a; `sportyR` 2.3.0 has 1.3333 yd), and the team benches are 60 yd long (were 50 yd).
- Football: the field border, its outline and the red-zone border and outline are always drawn, as in `sportyR`. `field_bordered` only picks the default outline colour: white on NCAA, NFHS and NFL (`field_bordered` is `True`), transparent on CFL. A colour you pass always wins, so a CFL outline colour is now drawn (it was ignored). Default output is unchanged.
- Football (NFHS): the field border and its outline wrap the team areas from the centre line, as `sportyR` draws them (11-player: x 0 to 62.1 yd, y ±36.9 yd); they used to cover only the ends of the field beyond the team areas (x 25.1 to 62.1 yd, y ±28.8 yd).
- Football (NCAA): the outer bench corners of the apron, field border and outline sit where `sportyR` puts them, straight above the bench's field-side corner (31.44 yd from the centre line, was 30.78 yd). NFL's corner still follows the bench's slanted side (19.15 yd), as in `sportyR`.
- Football (NCAA, NFHS, CFL): the coaching-box line is `#ffcb05`, as in `sportyR` (and as `NFLField` already drew it); it was white.
- Football: the endzones span the field's width; they used to extend under the sidelines, so plots look the same.
- Football polygons now match `sportyR`'s `geom_football()` point for point for NCAA, NFL, NFHS (11, 9, 8, 6) and CFL (tests/test_football_parity.py).
- Volleyball: `substitution_zone_rep_pattern` is a number (was the string `"5"`). No visual change.
- Baseball, catcher's box: `catchers_box_shape` is now listed as `"rectangle"`, which was already the default. No visual change.

Display ranges:

- Baseball: the full-field view spans the foul poles in `x` with no padding, as `sportyR`'s `geom_baseball()`. Before, both foul-pole limits were shifted 5 ft to the right, cutting 5 ft off the left-field edge.
- The 5-unit padding around a displayed surface is now 5 of the rule book's units, converted to the surface's units (baseball, softball, curling, hockey, tennis). Before, a field drawn in metres was padded by 5 m instead of 5 ft. Plots in the rule book's units are unchanged.

### Fixes

- `update_colors()`, `update_*_params()`, `reset_colors()` and `reset_*_params()` keep the surface's rotation, `x`/`y` translation, league and units. Before, they reset the rotation and translation to 0, went back to the rule book's units, and a base class created with `league_code` (e.g. `SoftballField(league_code = "ncaa")`) raised a `KeyError` on `reset_*_params()`.
- `contour()` and `contourf()` work on matplotlib 3.8 and newer (`QuadContourSet.collections` was removed in matplotlib 3.10).
- `USAVolleyballCourt` draws the USA Volleyball court (3 m side and 4.5 m end free zones). It drew the FIVB court before (5 m and 6.5 m).
- `NWHLRink()` no longer prints a message when it is created (as `sportyR`'s `"nwhl"` rink); the NWHL-to-PHF rename note is in its docstring.
- Thin lines no longer vanish: every feature is drawn with matplotlib's pixel snapping off, which snapped lines thinner than a pixel (volleyball and tennis lines at screen size) to zero width.
- Football display ranges match `sportyR`'s `geom_football()`: the padding is the league's `extra_apron_padding` (2 yd for NCAA, NFL and CFL; was always 5 yd), the width includes the team-bench border, and the red-zone views start at the 20 (were the 22).
- `FootballField` honours `units` (it ignored them): the field is built in yards and converted, so it looks the same in any units.
- Unit conversions: `"mm"` is 304.8 per foot (was 340.8) and the feet-to-yards factor is exactly 1/3 (was 0.3333).
- Lacrosse: `update_colors()` and the other update/reset methods re-derive the NCAA men's contrasting centre face-off colour from the colours you chose, as `sportyR` does (it was fixed at creation).
- A units key in an update (`update_field_params({"field_units": "ft"})`, and the `court_`, `rink_`, `sheet_` and `pitch_` equivalents) converts the surface to those units; the saved lengths were relabelled as the new unit instead. An unknown unit raises `ValueError`.
- Football: after `update_field_params({"field_bordered": ...})` the default outline colours follow the new `field_bordered`; an outline colour you chose is kept.
- Lacrosse: a single `xlim`/`ylim` value is the lower bound of the display range (it raised `TypeError`), and a NumPy array works as a tuple does.
- Football no longer uses pandas' deprecated `inplace` keyword (a `Pandas4Warning` on pandas 3.1).
- Supported Python versions are 3.10 to 3.14 (Python 3.9 reached end of life); CI tests 3.10 and 3.14.
- Packaging moved to `pyproject.toml` with the `uv_build` backend (`setup.py`, `requirements.txt` and `tox.ini` are gone), and matplotlib 3.8 or newer is required.
- Volleyball and basketball in other units: the substitution-zone repetitions and free-throw-circle dashes are counts and are no longer scaled like lengths (a FIVB court in inches drew 196 dashes instead of 5).
- Football in other units: the nudge of a top "1" in the Clarendon font is converted from yards; sizing the yard numbers no longer leaves an extra tiny text on the axes.
- Surfaces in other units and shifted match `sportyR`'s for lacrosse, football and volleyball (tests/test_unit_parity.py).

### Documentation

- The docs site (sportypy.sportsdataverse.org) is rebuilt with Docusaurus in the SportsDataverse docs family, and its API reference is generated from the docstrings on every build. It adds two cookbooks (NBA shot quality, NHL expected goals) with sportsdataverse-py data and sdvplot colours. The Sphinx site is retired; its old addresses (`/surfaces/hockey/nhl.html` and so on) redirect to the matching reference page.

## `sportypy` 1.1.0

- Added volleyball support

## `sportypy` 1.0.0

Initial release! Ability to plot baseball, basketball, curling, football, hockey, soccer, and tennis is included, with the ability to customize outputs in specific colors and supply custom dimensions.
