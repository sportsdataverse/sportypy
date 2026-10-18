"""Extension of the ``BaseballField`` class to create a softball field.

Ported from sportyR's ``R/geom-softball.R`` (dimensions from sportyR's
``surface-dimensions.json``). The field shares the baseball diamond geometry
and the draw/limit/color machinery of ``BaseballField``; it differs in having a
pitcher's circle and lane, coach's boxes, and no pitcher's mound or infield
grass.
"""

import math

import numpy as np
from matplotlib.transforms import Affine2D

import sportypy._feature_classes.softball as softball_features
from sportypy.surfaces.baseball import BaseballField


DEFAULT_COLORS = {
    "plot_background": "#395d33",
    "infield_dirt": "#9b7653",
    "base": "#ffffff",
    "pitchers_plate": "#ffffff",
    "batters_box": "#ffffff",
    "catchers_box": "#ffffff",
    "foul_line": "#ffffff",
    "running_lane": "#ffffff",
    "pitchers_circle": "#ffffff",
    "pitchers_lane": "#ffffff",
    "coaches_box": "#ffffff"
}


class SoftballField(BaseballField):
    """A subclass of ``BaseballField`` that draws a softball field.

    ``field_params`` takes the keys of sportyR's ``softball`` dimensions (see
    ``surface_dimensions.json``). The colors are ``plot_background``,
    ``infield_dirt``, ``base``, ``pitchers_plate``, ``batters_box``,
    ``catchers_box``, ``foul_line``, ``running_lane``, ``pitchers_circle``,
    ``pitchers_lane`` and ``coaches_box``. ``draw()`` accepts
    ``display_range`` of ``"full"`` or ``"infield"``. See ``BaseballField`` for
    the shared parameters and methods.
    """

    def __init__(
        self,
        league_code="",
        field_updates={},
        color_updates={},
        rotation=0.0,
        x_trans=0.0,
        y_trans=0.0,
        units="default",
        **added_features,
    ):
        self._load_preset_dimensions(sport="softball")
        self._load_unit_conversions()
        self.league_code = league_code.lower()

        field_params = {**self.league_dimensions.get(self.league_code, {}), **field_updates}
        self.field_params = field_params

        if units.lower() != "default":
            for k, v in field_params.items():
                self.field_params[k] = self._convert_units(v, self.field_params["field_units"], units.lower())
            self.field_params["field_units"] = units.lower()

        self.rotation_amt = rotation
        self._rotation = Affine2D().rotate_deg(rotation)
        self.x_trans, self.y_trans = x_trans, y_trans
        self._features = []
        self._feature_xlim = None
        self._feature_ylim = None

        self.feature_colors = {**DEFAULT_COLORS, **(color_updates or {})}

        p = self.field_params
        g = lambda key: p.get(key, 0.0)  # noqa: E731
        units_ = p.get("field_units", "ft")
        colors = self.feature_colors
        baseline = g("baseline_distance")
        plate_y = g("pitchers_plate_front_to_home_plate")
        box_dims = {
            "batters_box_length": g("batters_box_length"),
            "batters_box_y_adj": g("batters_box_y_adj"),
        }

        def add(cls, color, zorder, x=0.0, y=0.0, reflect_x=False, **kwargs):
            self._initialize_feature(
                {
                    "class": cls,
                    "x_anchor": x,
                    "y_anchor": y,
                    "reflect_x": reflect_x,
                    "reflect_y": False,
                    "feature_units": units_,
                    "facecolor": colors[color] if color else None,
                    "edgecolor": None,
                    "zorder": zorder,
                    **kwargs,
                }
            )

        # Surface constraint (invisible)
        add(softball_features.FieldConstraint, None, 0, visible=False)
        self._surface_constraint = self._features.pop(-1)

        add(
            softball_features.InfieldDirt,
            "infield_dirt",
            5,
            home_plate_circle_radius=g("home_plate_circle_radius"),
            foul_line_to_foul_grass=g("foul_line_to_foul_grass"),
            infield_arc_radius=g("infield_arc_radius"),
            pitchers_plate_dist=plate_y,
        )
        add(
            softball_features.PitchersCircle,
            "pitchers_circle",
            8,
            y=plate_y,
            is_constrained=False,
            feature_radius=g("pitchers_circle_radius"),
            feature_thickness=g("line_width"),
        )
        add(softball_features.HomePlate, "base", 16, home_plate_edge_length=g("home_plate_edge_length"))
        for x, y, side in [
            (baseline * math.cos(np.pi / 4.0), baseline * math.sin(np.pi / 4.0), {"adjust_x_left": True}),
            (0.0, baseline * math.sqrt(2.0), {}),
            (baseline * math.cos(3.0 * np.pi / 4.0), baseline * math.sin(3.0 * np.pi / 4.0), {"adjust_x_right": True}),
        ]:
            add(softball_features.Base, "base", 16, x=x, y=y, base_side_length=g("base_side_length"), **side)
        add(
            softball_features.PitchersPlate,
            "pitchers_plate",
            16,
            y=plate_y,
            pitchers_plate_length=g("pitchers_plate_length"),
            feature_thickness=g("pitchers_plate_width"),
        )
        add(
            softball_features.BattersBox,
            "batters_box",
            16,
            x=(g("home_plate_edge_length") / 2.0 + g("home_plate_side_to_batters_box") + g("batters_box_width") / 2.0),
            reflect_x=True,
            is_constrained=False,
            feature_thickness=g("line_width"),
            batters_box_width=g("batters_box_width"),
            **box_dims,
        )
        add(
            softball_features.CatchersBox,
            "catchers_box",
            16,
            is_constrained=False,
            feature_thickness=g("line_width"),
            catchers_box_depth=g("catchers_box_depth"),
            catchers_box_width=g("catchers_box_width"),
            **box_dims,
        )
        for is_1b, dist in [(False, "left_field_distance"), (True, "right_field_distance")]:
            add(
                softball_features.FoulLine,
                "foul_line",
                17,
                feature_thickness=g("line_width"),
                is_line_1b=is_1b,
                line_distance=g(dist),
                batters_box_width=g("batters_box_width"),
                home_plate_side_to_batters_box=g("home_plate_side_to_batters_box"),
                home_plate_edge_length=g("home_plate_edge_length"),
                **box_dims,
            )
        add(
            softball_features.RunningLane,
            "running_lane",
            18,
            is_constrained=False,
            feature_thickness=g("line_width"),
            running_lane_start_distance=g("running_lane_start_distance"),
            running_lane_length=g("running_lane_length"),
            running_lane_depth=g("running_lane_depth"),
        )
        add(
            softball_features.PitchersLane,
            "pitchers_lane",
            17,
            y=plate_y,
            reflect_x=True,
            is_constrained=False,
            feature_thickness=g("line_width"),
            pitchers_lane_length=g("pitchers_lane_length"),
            pitchers_plate_length=g("pitchers_plate_length"),
            pitchers_plate_front_to_home_plate=plate_y,
            home_plate_edge_length=g("home_plate_edge_length"),
            home_plate_side_to_batters_box=g("home_plate_side_to_batters_box"),
            **box_dims,
        )
        add(
            softball_features.CoachesBox,
            "coaches_box",
            17,
            reflect_x=True,
            is_constrained=False,
            feature_thickness=g("line_width"),
            baseline_distance=baseline,
            coaches_box_depth=g("coaches_box_depth"),
            coaches_box_length=g("coaches_box_length"),
            coaches_box_width=g("coaches_box_width"),
        )

        for added_feature in added_features.values():
            self._initialize_feature(added_feature)


    def reset_colors(self):
        """Reset the features of the field to the softball default colors."""
        self._reinit(
            field_updates = self.field_params,
            color_updates = dict(DEFAULT_COLORS)
        )

    def _get_plot_range_limits(self, display_range = "full", xlim = None,
                               ylim = None, for_plot = False,
                               for_display = True):
        """Get the ``x`` and ``y`` limits, as sportyR's ``geom_softball()``.

        ``"full"`` spans the foul poles in ``x`` (no padding) and runs from
        the backstop to center field in ``y`` (5 units of padding on both).
        ``"infield"`` is the infield arc radius and the home plate circle,
        padded by 5. With ``for_plot`` the padding is dropped. An explicit
        ``xlim``/``ylim`` tuple replaces the range (less the translation).
        """
        # 5 rule-book units, converted to the surface's units (sportyR leaves its display limits unconverted)
        pad = self._display_pad(5.0) if for_display and not for_plot else 0.0
        g = lambda key: self.field_params.get(key, 0.0)  # noqa: E731
        arc, plate = g("infield_arc_radius"), g(
            "pitchers_plate_front_to_home_plate")
        full_x = (g("left_field_distance") * math.cos(3.0 * np.pi / 4.0),
                  g("right_field_distance") * math.cos(np.pi / 4.0))
        full_y = (-(g("backstop_radius") + pad), g("center_field_distance") + pad)
        infield_x = (-(arc + pad), arc + pad)
        infield_y = (-(g("home_plate_circle_radius") + pad), plate + arc + pad)

        infield = str(display_range or "").lower().replace(" ", "") == "infield"
        x = (xlim[0] - self.x_trans, xlim[1] - self.x_trans) if xlim else (
            infield_x if infield else full_x)
        y = (ylim[0] - self.y_trans, ylim[1] - self.y_trans) if ylim else (
            infield_y if infield else full_y)
        return (min(x), max(x)), (min(y), max(y))


class NCAASoftballField(SoftballField):
    """A subclass of ``SoftballField`` specific to NCAA softball.

    See ``SoftballField`` class documentation for full description.
    """

    def __init__(self, field_updates={}, *args, **kwargs):
        super().__init__(league_code="ncaa", field_updates=field_updates, *args, **kwargs)
