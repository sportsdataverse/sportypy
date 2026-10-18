# Changelog

## `sportypy` 1.2.0

Brings `sportypy` in line with `sportyR` 2.3.0.

### New surfaces (ported from `sportyR`)

- Lacrosse: `LacrosseField`, with `NCAAMLacrosseField`, `NCAAWLacrosseField`, `NLLField` (box lacrosse), `PLLField`, `USAMLacrosseField`, `USAWLacrosseField` and `WorldLacrosseField` (box). Every polygon matches what `sportyR`'s `geom_lacrosse()` draws.
- Softball: `SoftballField` and `NCAASoftballField`.
- Hockey: `PWHLRink`, the PWHL's own rink dimensions.
- Curling: `CurlingCanadaSheet`.
- Volleyball courts are now importable from `sportypy.surfaces`: `FIVBCourt`, `USAVolleyballCourt` and `VolleyballCourt`. `sportypy.surfaces.NCAACourt` is still the tennis court; import the volleyball one with `from sportypy.surfaces.volleyball import NCAACourt`.

### Changed output for existing leagues

League dimensions now equal `sportyR` 2.3.0's (`tools/sync_dimensions.py --align`):

- Baseball (MLB, MiLB): bases are 1.5 ft square (were 1.25 ft).
- Basketball (NFHS): the restricted arc is drawn as `sportyR` draws it. NFHS has no restricted-arc radius, so this is a small mark under the basket; it was hidden before.
- Basketball (NBA, NBA G League, WNBA): the second, 12 ft lane is hidden (`[True, False]` visibility, as in `sportyR`). It was drawn fully transparent before, so plots look the same.
- Football (NCAA): the restricted area is 1.3333 yd wide (was 2 yd) and the team benches are 60 yd long (were 50 yd).
- Football (NCAA, NFHS, NFL): `field_bordered` is `False`, so the field border, its white outline and the red-zone border are no longer drawn.
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
