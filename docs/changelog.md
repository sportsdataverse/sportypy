# Changelog

## `sportypy` 1.2.0

Brings `sportypy` in line with `sportyR` 2.3.0 and the geometry fixes in `sportyR` PR #68 (issues #60-#67).

### New surfaces (ported from `sportyR`)

- Lacrosse: `LacrosseField`, with `NCAAMLacrosseField`, `NCAAWLacrosseField`, `NLLField` (box lacrosse), `PLLField`, `USAMLacrosseField`, `USAWLacrosseField` and `WorldLacrosseField` (box). Every polygon matches what `sportyR`'s `geom_lacrosse()` draws, including the lacrosse fixes in `sportyR` PR #68:
  - NLL and World Lacrosse: the neutral zone spans the 85 ft between the restraining lines (it was 0 long; sportyR #60), and the penalty box fills start at the inside edge of the boards (sportyR #61).
  - NCAA and USA Lacrosse women's: each goal-fan hash mark is placed on the fan arc at the angle it is rotated by, at its stated distance along the arc (sportyR #62).
  - The `"full"`, `"offense"` and `"defense"` display ranges take in the NLL and World Lacrosse player benches, penalty boxes and off-field officials' box (sportyR #63).
  - `goal_arc_line_thickness` defaults to 0, so a goal arc added through `field_updates` without a thickness is a line, not a solid block (sportyR #64).
  - A `center_face_off_marker` colour you pass is kept; the contrasting `#ffcb05` default (NCAA men's) applies only when you pass no marker colour and the marker would match the centre line, so recolouring only `center_line` leaves the marker white (sportyR #65).
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
- Football (NCAA, NFHS, NFL): `field_bordered` stays `True`, so these fields still draw the field border and its white outline, as `sportyR` does after sportyR #67. A colour you pass for the border or its outline is used on these fields. CFL draws no border outline. No visual change.
- Volleyball: `substitution_zone_rep_pattern` is a number (was the string `"5"`). No visual change.
- Baseball, catcher's box: `catchers_box_shape` is now listed as `"rectangle"`, which was already the default. No visual change.

Display ranges:

- Baseball: the full-field view spans the foul poles in `x` with no padding, as `sportyR`'s `geom_baseball()`. Before, both foul-pole limits were shifted 5 ft to the right, cutting 5 ft off the left-field edge.
- The 5-unit padding around a displayed surface is now 5 of the rule book's units, converted to the surface's units (baseball, softball, curling, hockey, tennis). Before, a field drawn in metres was padded by 5 m instead of 5 ft. Plots in the rule book's units are unchanged.

### Fixes

- `update_colors()`, `update_*_params()`, `reset_colors()` and `reset_*_params()` keep the surface's rotation, `x`/`y` translation, league and units. Before, they reset the rotation and translation to 0, went back to the rule book's units, and a base class created with `league_code` (e.g. `SoftballField(league_code = "ncaa")`) raised a `KeyError` on `reset_*_params()`.
- `contour()` and `contourf()` work on matplotlib 3.8 and newer (`QuadContourSet.collections` was removed in matplotlib 3.10).

## `sportypy` 1.1.0

- Added volleyball support

## `sportypy` 1.0.0

Initial release! Ability to plot baseball, basketball, curling, football, hockey, soccer, and tennis is included, with the ability to customize outputs in specific colors and supply custom dimensions.
