# Changelog

## `sportypy` 1.2.0

Brings `sportypy` in line with `sportyR` 2.3.0 and the geometry fixes in `sportyR` PR #68 (issues #60-#67 and #69-#72; sportyR commit 00e364a).

### New surfaces (ported from `sportyR`)

- Lacrosse: `LacrosseField`, with `NCAAMLacrosseField`, `NCAAWLacrosseField`, `NLLField` (box lacrosse), `PLLField`, `USAMLacrosseField`, `USAWLacrosseField` and `WorldLacrosseField` (box). Every polygon matches what `sportyR`'s `geom_lacrosse()` draws, including the lacrosse fixes in `sportyR` PR #68:
  - NLL and World Lacrosse: the neutral zone spans the 85 ft between the restraining lines (it was 0 long; sportyR #60), and the penalty box fills start at the inside edge of the boards (sportyR #61).
  - NCAA and USA Lacrosse women's: each goal-fan hash mark is placed on the fan arc at the angle it is rotated by, at its stated distance along the arc (sportyR #62).
  - The `"full"`, `"offense"` and `"defense"` display ranges take in the NLL and World Lacrosse player benches, penalty boxes and off-field officials' box (sportyR #63).
  - `goal_arc_line_thickness` defaults to 0, so a goal arc added through `field_updates` without a thickness is a line, not a solid block (sportyR #64).
  - A `center_face_off_marker` colour you pass is kept; the contrasting `#ffcb05` default (NCAA men's) applies only when you pass no marker colour and the marker would match the centre line, so recolouring only `center_line` leaves the marker white (sportyR #65).
  - NCAA and USA Lacrosse women's: the 8 m arc follows the NCAA rule: two lines at 45 degrees from where the goal line extended crosses the goal circle, joined by a 10.6 m arc about the centre of the goal line; the hash marks sit on that circle, and the goal-line-extended marks are 0.305 m long (sportyR #69).
  - PLL: the two-point arc runs parallel to the sidelines 13 yd from the centre of the goal line (new parameter `goal_arc_parallel_line_to_center`), then becomes a 15 yd arc (2024 PLL Rulebook; sportyR #70). Without that parameter the arc is a semicircle.
  - NLL and World Lacrosse: each penalty box is `penalty_box_length` (8 ft) inside its walls; the outer wall moved out 0.25 ft (sportyR #72).
  - Leagues without a goal fan draw no fan polygon (it was a hidden zero-size shape).
- Softball: `SoftballField` and `NCAASoftballField`.
- Hockey: `PWHLRink`, the PWHL's own rink dimensions.
- Curling: `CurlingCanadaSheet`.
- Volleyball courts are now importable from `sportypy.surfaces`: `FIVBCourt`, `USAVolleyballCourt` and `VolleyballCourt`. `sportypy.surfaces.NCAACourt` is still the tennis court; import the volleyball one with `from sportypy.surfaces.volleyball import NCAACourt`.

### Changed output for existing leagues

League dimensions now equal `sportyR` 2.3.0's, with PR #68's corrections (`tools/sync_dimensions.py --align`):

- Baseball (MLB, MiLB): bases are 1.5 ft square (were 1.25 ft).
- Basketball (NFHS): the restricted arc is drawn as `sportyR` draws it. NFHS has no restricted-arc radius, so this is a small mark under the basket; it was hidden before.
- Basketball (NBA, NBA G League, WNBA): the second, 12 ft lane is hidden (`[True, False]` visibility, as in `sportyR`). It was drawn fully transparent before, so plots look the same.
- Football (NCAA): the restricted area is 1.8889 yd wide (was 2 yd), so the coaching line sits 6 ft outside the sideline, measured from its inside edge (NCAA Football Rules 1-2-4-a; `sportyR` 2.3.0 has 1.3333 yd, corrected in sportyR #66), and the team benches are 60 yd long (were 50 yd).
- Football: the field border, its outline and the red-zone border and outline are always drawn, as in `sportyR`. `field_bordered` only picks the default outline colour: white on NCAA, NFHS and NFL (`field_bordered` is `True`, sportyR #67), transparent on CFL. A colour you pass always wins, so a CFL outline colour is now drawn (it was ignored). Default output is unchanged.
- Football (NFHS): the field border and its outline wrap the team areas from the centre line, as `sportyR` draws them (11-player: x 0 to 62.1 yd, y ±36.9 yd); they used to cover only the ends of the field beyond the team areas (x 25.1 to 62.1 yd, y ±28.8 yd).
- Football (NCAA): the outer bench corners of the apron, field border and outline sit where `sportyR` puts them, straight above the bench's field-side corner (31.44 yd from the centre line, was 30.78 yd). NFL's corner still follows the bench's slanted side (19.15 yd), which `sportyR` adopted in sportyR #71.
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

## `sportypy` 1.1.0

- Added volleyball support

## `sportypy` 1.0.0

Initial release! Ability to plot baseball, basketball, curling, football, hockey, soccer, and tennis is included, with the ability to customize outputs in specific colors and supply custom dimensions.
