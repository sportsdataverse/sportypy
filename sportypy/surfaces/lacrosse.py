"""Extension of the ``BaseSurfacePlot`` class to create a lacrosse field.

Ported from sportyR's ``R/geom-lacrosse.R`` (dimensions from sportyR's
``surface-dimensions.json``): the features, their anchors, reflections,
colours and drawing order are sportyR's. Seven leagues ship: NCAA men's and
women's, NLL (box lacrosse), PLL, USA Lacrosse men's and women's, and World
Lacrosse (box).
"""

import math

import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D

import sportypy._feature_classes.lacrosse as lacrosse_features
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot

# sportyR's lacrosse_features_set_colors(); sportyR leaves the background
# blank, which is transparent here
DEFAULT_COLORS = {
    "plot_background": "#ffffff00",
    "field_apron": "#195f0c",
    "defensive_zone": "#195f0c",
    "neutral_zone": "#195f0c",
    "offensive_zone": "#195f0c",
    "team_a_bench": "#a5acaf4d",
    "team_b_bench": "#a5acaf4d",
    "team_a_penalty_box": "#a5acaf4d",
    "team_b_penalty_box": "#a5acaf4d",
    "off_field_officials_box": "#a5acaf",
    "boards": "#ffa500",
    "end_line": "#ffffff",
    "sideline": "#ffffff",
    "center_line": "#ffffff",
    "wing_line": "#ffffff",
    "restraining_line": "#ffffff",
    "defensive_area_line": "#ffffff",
    "goal_line": "#ffffff",
    "referee_crease": "#ffffff",
    "referee_crease_fill": "#195f0c",
    "goal_circle": "#ffffff",
    "goal_circle_fill": "#195f0c",
    "goal_arc": "#ffffff",
    "goal_fan": "#ffffff",
    "goal_fan_hash_mark": "#ffffff",
    "goal_mouth_hash_mark": "#ffffff",
    "goal_mouth": "#ffffff",
    "below_goal_marking": "#ffffff",
    "goal_frame": "#ffa500",
    "goal_net": "#a5acaf4d",
    "center_circle": "#ffffff",
    "center_face_off_marker": "#ffffff",
    "corner_face_off_marker": "#ffffff",
    "change_area_outline": "#ffffff",
    "change_area_fill": "#195f0c",
}
CONTRASTING_CENTER_FACE_OFF_MARKER = "#ffcb05"
TRANSPARENT = "#ffffff00"

# display_range aliases, as sportyR's geom_lacrosse()
_HALVES = {
    "offense": 1,
    "offence": 1,
    "offensivehalffield": 1,
    "offensive_half_field": 1,
    "offensive half field": 1,
    "defense": -1,
    "defence": -1,
    "defensivehalffield": -1,
    "defensive_half_field": -1,
    "defensive half field": -1,
}


class LacrosseField(BaseSurfacePlot):
    """A lacrosse field, as sportyR's ``geom_lacrosse()``.

    ``league_code`` is one of ``"ncaam"``, ``"ncaaw"``, ``"nll"``, ``"pll"``,
    ``"usam"``, ``"usaw"`` or ``"world lacrosse"`` (case-insensitive).
    ``field_params`` takes the keys of sportyR's ``lacrosse`` dimensions (see
    ``cani_change_dimensions()``), the colours are listed by
    ``cani_color_features()``, and ``draw()`` accepts a ``display_range`` of
    ``"full"``, ``"in_bounds_only"``, ``"offense"`` or ``"defense"`` (and
    sportyR's other spellings of these).
    """

    def __init__(
        self,
        league_code="",
        field_updates=None,
        color_updates=None,
        rotation=0.0,
        x_trans=0.0,
        y_trans=0.0,
        units="default",
        **added_features,
    ):
        self._load_preset_dimensions(sport="lacrosse")
        self._load_unit_conversions()
        self.league_code = league_code.lower()
        self.field_params = {
            **self.league_dimensions.get(self.league_code, {}),
            **(field_updates or {}),
        }

        if units.lower() != "default":
            start = self.field_params.get("field_units", "ft")
            for k, v in self.field_params.items():
                if isinstance(v, list):
                    self.field_params[k] = [
                        self._convert_units(i, start, units.lower()) for i in v
                    ]
                else:
                    self.field_params[k] = self._convert_units(v, start, units.lower())
            self.field_params["field_units"] = units.lower()

        self.rotation_amt = rotation
        self._rotation = Affine2D().rotate_deg(rotation)
        self.x_trans, self.y_trans = x_trans, y_trans
        self._features = []
        self._feature_xlim = None
        self._feature_ylim = None

        p = self.field_params
        g = lambda key, default=0.0: p.get(key, default)  # noqa: E731

        # The colours the user chose (kept so update/reset methods can re-derive
        # the contrasting default below from them)
        self._color_updates = dict(color_updates or {})
        colors = {**DEFAULT_COLORS, **self._color_updates}
        # The contrasting colour applies only when the user chose no marker
        # colour and the marker would match the (possibly user-set) center line
        # (sportyR #65)
        if (
            g("center_face_off_marker_color_contrasting", False)
            and "center_face_off_marker" not in (color_updates or {})
            and colors["center_face_off_marker"] == colors["center_line"]
        ):
            colors["center_face_off_marker"] = CONTRASTING_CENTER_FACE_OFF_MARKER
        self.feature_colors = colors

        units_ = p.get("field_units", "ft")
        zorder = iter(range(1, 1000))

        def add(
            cls,
            fill,
            x=0.0,
            y=0.0,
            reflect_x=False,
            reflect_y=False,
            outline=None,
            **dims,
        ):
            """One sportyR ``add_feature()`` call (sportyR's drawing order)."""
            edge = outline if outline not in (None, TRANSPARENT) else None
            self._initialize_feature(
                {
                    "class": cls,
                    "dims": dims,
                    "x_anchor": x,
                    "y_anchor": y,
                    "reflect_x": reflect_x,
                    "reflect_y": reflect_y,
                    "is_constrained": False,
                    "feature_units": units_,
                    "facecolor": fill,
                    "edgecolor": edge,
                    "zorder": next(zorder),
                }
            )

        length, width = g("field_length"), g("field_width")
        shape = g("field_shape", "rectangle")
        boards_t = g("boards_thickness")
        zone = {
            "field_length": length,
            "field_width": width,
            "corner_radius": g("corner_radius"),
            "nzone_length": g("neutral_zone_length"),
            "field_shape": shape,
        }
        goal_x = length / 2.0 - g("goal_line_center_to_end_line")
        goal_circle = {
            "goal_circle_radius": g("goal_circle_radius"),
            "line_thickness": g("goal_circle_thickness"),
            "goal_circle_full_360": g("goal_circle_full_360", False),
            "goal_depth": g("goal_depth"),
            "goal_depth_to_circle": g("goal_depth_to_circle"),
        }
        goal_frame = {
            "goal_frame_opening_interior": g("goal_frame_opening_interior"),
            "goal_post_thickness": g("goal_post_thickness"),
            "goal_depth": g("goal_depth"),
        }
        bench = {
            "bench_area_outline_thickness": boards_t,
            "bench_length": g("bench_length"),
            "bench_depth": g("bench_depth"),
        }
        change_area_length = (
            g("bench_separation") / 2.0 + g("bench_length") + g("change_area_extension")
        )
        bench_x = g("bench_separation") / 2.0 + g("bench_length") / 2.0
        penalty_x = (
            g("penalty_box_separation") / 2.0
            + g("boards_thickness")
            + g("penalty_box_length") / 2.0
        )
        penalty_fill = {
            "penalty_box_outline_thickness": boards_t,
            "penalty_box_length": g("penalty_box_length"),
            "penalty_box_depth": g("penalty_box_depth"),
        }
        crease = {
            "referee_crease_radius": g("referee_crease_radius"),
            "line_thickness": g("referee_crease_thickness"),
        }

        # The field's interior constrains plotted data (it is not drawn)
        self._initialize_feature(
            {
                "class": lacrosse_features.FieldConstraint,
                "field_length": length,
                "field_width": width,
                "corner_radius": g("corner_radius"),
                "feature_units": units_,
                "visible": False,
            }
        )
        self._surface_constraint = self._features.pop(-1)

        f = lacrosse_features
        add(
            f.FieldApron,
            colors["field_apron"],
            reflect_x=True,
            outline=colors["field_apron"],
            field_length=length,
            field_width=width,
            field_apron_thickness=g("field_apron_thickness"),
            field_shape=shape,
        )
        add(
            f.DefensiveZone,
            colors["defensive_zone"],
            outline=colors["defensive_zone"],
            **zone,
        )
        add(
            f.NeutralZone,
            colors["neutral_zone"],
            field_width=width,
            nzone_length=g("neutral_zone_length"),
        )
        add(
            f.OffensiveZone,
            colors["offensive_zone"],
            outline=colors["offensive_zone"],
            **zone,
        )
        add(
            f.RefereeCreaseFill,
            colors["referee_crease_fill"],
            y=-width / 2.0,
            reflect_x=True,
            **crease,
        )
        add(
            f.Sideline,
            colors["sideline"] if g("has_sidelines", True) else TRANSPARENT,
            y=width / 2.0,
            reflect_y=True,
            field_length=length,
            line_thickness=g("boundary_thickness"),
        )
        add(
            f.EndLine,
            colors["end_line"] if g("has_endlines", True) else TRANSPARENT,
            x=length / 2.0,
            reflect_x=True,
            field_width=width,
            line_thickness=g("boundary_thickness"),
        )
        add(
            f.ChangeAreaOutline,
            colors["change_area_outline"],
            y=width / 2.0,
            reflect_x=True,
            outline=colors["change_area_outline"],
            change_area_length=change_area_length,
            change_area_width=g("change_area_width"),
            feature_thickness=g("change_area_outline_thickness"),
        )
        add(
            f.ChangeAreaFill,
            colors["change_area_fill"],
            y=width / 2.0,
            reflect_x=True,
            outline=colors["change_area_fill"],
            change_area_length=change_area_length,
            change_area_width=g("change_area_width"),
        )
        add(
            f.CenterLine,
            colors["center_line"],
            reflect_x=True,
            center_line_width=g("center_line_width"),
            line_thickness=g("center_line_thickness"),
        )
        add(
            f.PlayerBenchAreaFill,
            colors["team_a_bench"],
            x=-bench_x,
            y=width / 2.0,
            **bench,
        )
        add(
            f.PlayerBenchAreaFill,
            colors["team_b_bench"],
            x=bench_x,
            y=width / 2.0,
            **bench,
        )
        add(
            f.PlayerBenchOutline,
            colors["boards"],
            x=g("bench_separation") / 2.0,
            y=width / 2.0,
            reflect_x=True,
            **bench,
        )
        add(
            f.PenaltyBoxFill,
            colors["team_a_penalty_box"],
            x=-penalty_x,
            y=-width / 2.0,
            **penalty_fill,
        )
        add(
            f.PenaltyBoxFill,
            colors["team_b_penalty_box"],
            x=penalty_x,
            y=-width / 2.0,
            **penalty_fill,
        )
        add(
            f.PenaltyBoxOutline,
            colors["boards"],
            y=-width / 2.0,
            reflect_x=True,
            penalty_box_outline_thickness=boards_t,
            penalty_box_length=g("penalty_box_length"),
            penalty_box_depth=g("penalty_box_depth"),
            penalty_box_separation=g("penalty_box_separation"),
        )
        add(
            f.OffFieldOfficialsBox,
            colors["off_field_officials_box"],
            y=-width / 2.0,
            officials_box_thickness=boards_t,
            officials_box_length=g("penalty_box_separation"),
            officials_box_depth=g("penalty_box_depth"),
        )
        add(
            f.Boards,
            colors["boards"],
            reflect_x=True,
            outline=colors["boards"] if g("has_boards", False) else TRANSPARENT,
            field_length=length,
            field_width=width,
            corner_radius=g("corner_radius"),
            boundary_thickness=boards_t,
        )
        add(
            f.WingLine,
            colors["wing_line"],
            y=width / 2.0 - g("wing_line_center_to_sideline"),
            reflect_y=True,
            wing_line_length=g("wing_line_length"),
            line_thickness=g("wing_line_thickness"),
        )
        add(
            f.RestrainingLine,
            colors["restraining_line"],
            x=g("restraining_line_outer_edge_to_center"),
            reflect_x=True,
            field_width=width,
            line_thickness=g("restraining_line_thickness"),
        )
        add(
            f.DefensiveAreaLine,
            colors["defensive_area_line"],
            x=length / 2.0 - g("defensive_area_line_length"),
            y=width / 2.0 - g("defensive_area_line_center_to_sideline"),
            reflect_x=True,
            reflect_y=True,
            defensive_area_line_length=g("defensive_area_line_length"),
            line_thickness=g("defensive_area_line_thickness"),
        )
        add(
            f.RefereeCrease,
            colors["referee_crease"],
            y=-width / 2.0,
            reflect_x=True,
            **crease,
        )
        add(
            f.CenterCircle,
            colors["center_circle"],
            reflect_x=True,
            center_circle_radius=g("center_circle_radius"),
            center_circle_thickness=g("center_circle_thickness"),
        )
        add(
            f.GoalCircleFill,
            colors["goal_circle_fill"],
            x=goal_x,
            reflect_x=True,
            reflect_y=True,
            **goal_circle,
        )
        add(
            f.GoalCircle,
            colors["goal_circle"],
            x=goal_x,
            reflect_x=True,
            reflect_y=True,
            **goal_circle,
        )
        add(
            f.GoalArc,
            colors["goal_arc"],
            x=goal_x,
            reflect_x=True,
            goal_arc_extension=g("goal_arc_extension"),
            goal_arc_radius=g("goal_arc_radius"),
            line_thickness=g("goal_arc_line_thickness"),
            goal_arc_parallel_line_to_center=g(
                "goal_arc_parallel_line_to_center", g("goal_arc_radius")
            ),
        )
        add(
            f.GoalFan,
            colors["goal_fan"],
            x=goal_x,
            reflect_x=True,
            goal_fan_radius=g("goal_fan_radius"),
            goal_circle_radius=g("goal_circle_radius"),
            line_thickness=g("goal_fan_line_thickness"),
        )

        # The goal fan's line runs from goal_fan_radius - t to goal_fan_radius
        # about the goal-line centre (see goal_fan(), sportyR #69). The hash
        # marks bisect the arc, so they are centred on the line's middle,
        # R = goal_fan_radius - t / 2 (sportyR #75); a mark at arc distance
        # ``separation`` from the fan's center sits theta = separation / R
        # radians from it, placed there and rotated by -theta, perpendicular to
        # the arc (sportyR #62)
        fan_r, circle_r = g("goal_fan_radius"), g("goal_circle_radius")
        mark_r = g("goal_fan_radius", 1.0) - g("goal_fan_line_thickness") / 2.0
        for separation in g("goal_fan_hash_mark_separation_from_center", []) or []:
            theta = separation / mark_r
            place = theta / math.pi
            add(
                f.GoalFanHashMark,
                colors["goal_fan_hash_mark"],
                x=goal_x + mark_r * math.cos((1.0 - place) * math.pi),
                y=mark_r * math.sin((1.0 - place) * math.pi),
                reflect_x=True,
                reflect_y=True,
                goal_fan_hash_mark_length=g("goal_fan_hash_mark_length"),
                line_thickness=g("goal_fan_hash_mark_line_thickness"),
                rotational_angle=-theta * 180.0 / math.pi,
            )

        add(
            f.GoalMouth,
            colors["goal_mouth"],
            x=goal_x,
            reflect_x=True,
            goal_mouth_radius=g("goal_mouth_radius"),
            line_thickness=g("goal_mouth_line_thickness"),
            goal_mouth_semi_circle_separation=g("goal_mouth_semi_circle_separation"),
        )
        add(
            f.GoalMouthHashMark,
            colors["goal_mouth_hash_mark"],
            x=goal_x,
            y=fan_r,
            reflect_x=True,
            reflect_y=True,
            goal_mouth_hash_mark_length=g("goal_mouth_hash_mark_length"),
            line_thickness=g("goal_mouth_hash_mark_line_thickness"),
        )
        add(
            f.BelowGoalMarking,
            colors["below_goal_marking"],
            x=goal_x + g("below_goal_marking_to_goal_line"),
            y=fan_r / 2.0,
            reflect_x=True,
            reflect_y=True,
            below_goal_marking_radius=g("below_goal_marking_radius"),
        )
        add(f.GoalNet, colors["goal_net"], x=goal_x, reflect_x=True, **goal_frame)
        add(f.GoalFrame, colors["goal_frame"], x=goal_x, reflect_x=True, **goal_frame)
        add(
            f.GoalLine,
            colors["goal_line"],
            x=goal_x,
            reflect_x=True,
            goal_frame_width=g("goal_frame_width"),
            line_thickness=g("goal_line_thickness"),
            goal_line_full_diameter=g("goal_line_full_diameter", False),
            goal_circle_radius=circle_r,
        )
        add(
            f.FaceOffMarker,
            colors["center_face_off_marker"],
            shape=g("center_face_off_marker_shape", "O"),
            feature_thickness=g("center_face_off_marker_side_width"),
            side_length=g("center_face_off_marker_side_length"),
            feature_radius=g("center_face_off_marker_radius"),
        )
        add(
            f.FaceOffMarker,
            colors["corner_face_off_marker"],
            x=(
                g("restraining_line_outer_edge_to_center")
                + g("corner_face_off_marker_to_attack_line_outer") / 2.0
            ),
            y=width / 2.0 - g("corner_face_off_marker_to_boards"),
            reflect_x=True,
            reflect_y=True,
            shape=g("corner_face_off_marker_shape", "O"),
            feature_thickness=g("corner_face_off_marker_bar_width"),
            side_length=g("corner_face_off_marker_bar_length"),
            feature_radius=g("corner_face_off_marker_radius"),
        )

        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax=None, display_range="full", xlim=None, ylim=None, rotation=None):
        """Draw the field.

        Parameters
        ----------
        ax : matplotlib.Axes
            An Axes object onto which the plot can be drawn. If ``None`` is
            supplied, then the currently-active Axes object will be used

        display_range : str
            ``"full"`` (the default), ``"in_bounds_only"``, ``"offense"`` or
            ``"defense"``; see the class documentation

        xlim : tuple or None
            The ``x`` limits to display (overrides ``display_range``)

        ylim : tuple or None
            The ``y`` limits to display (overrides ``display_range``)

        rotation : float or None
            Degrees to rotate the field through (counterclockwise)

        Returns
        -------
        ax : matplotlib.Axes
            An Axes object with the field drawn on it
        """
        if rotation:
            self._rotation = Affine2D().rotate_deg(rotation)

        if ax is None:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor(self.feature_colors["plot_background"])

        ax.set_aspect("equal")
        ax.grid(visible=False, which="both")
        ax.axis("off")

        transform = self._get_transform(ax)
        constraint = self._add_surface_constraint(ax, transform)
        for feature in self._features:
            drawn_feature = feature.draw(ax, transform)
            if feature.is_constrained:
                drawn_feature.set_clip_path(constraint)

        return self.set_plot_display_range(
            ax, display_range, xlim, ylim, for_plot=False, for_display=True
        )

    def cani_plot_leagues(self, league_code=None):
        """Print whether ``league_code`` ships with sportypy, or every league that does."""
        leagues = sorted(self.league_dimensions)
        if league_code is not None:
            if league_code.lower() in leagues:
                print(f"{league_code.upper()} comes with sportypy and is ready to use!")
            else:
                print(
                    f"{league_code.upper()} does not come with sportypy, but may be "
                    "parameterized. Use the cani_change_dimensions() to check what "
                    "parameters are needed."
                )
        else:
            print("The following lacrosse leagues are available with sportypy:\n")
            for league in leagues:
                print(f"- {league.upper()}")

    def cani_color_features(self):
        """Print the features that can be coloured, with their current colours."""
        print(
            "The following features can be colored via the color_updates parameter, "
            "with the current value in parenthesis:\n"
        )
        for k, v in self.feature_colors.items():
            print(f"- {k} ({v})")
        print("\nThese colors may be updated with the update_colors() method")

    def cani_change_dimensions(self):
        """Print the field's parameters, with their current values."""
        print(
            "The following features can be reparameterized via the field_updates "
            "parameter, with the current value in parenthesis:\n"
        )
        for k, v in self.field_params.items():
            print(f"- {k} ({v})")
        print("\nThese parameters may be updated with the update_field_params() method")

    def update_colors(self, color_updates=None, *args, **kwargs):
        """Re-draw the field's features with ``color_updates`` applied."""
        self._reinit(
            field_updates=self.field_params,
            color_updates={**self._color_updates, **(color_updates or {})},
        )

    def update_field_params(self, field_param_updates=None, *args, **kwargs):
        """Re-draw the field with ``field_param_updates`` applied."""
        self._reinit(
            field_updates={**self.field_params, **(field_param_updates or {})},
            color_updates=self._color_updates,
        )

    def reset_colors(self):
        """Go back to the default colours (sportyR's)."""
        self._reinit(field_updates=self.field_params, color_updates={})

    def reset_field_params(self):
        """Go back to the league's dimensions (in the field's current units)."""
        self._reinit(
            field_updates=self.league_dimensions.get(self.league_code, {}),
            color_updates=self._color_updates,
        )

    def _get_plot_range_limits(
        self,
        display_range="full",
        xlim=None,
        ylim=None,
        for_plot=False,
        for_display=True,
    ):
        """Get the ``x`` and ``y`` limits, as sportyR's ``geom_lacrosse()``.

        ``"full"`` (and any unknown range) is the field plus its apron and, on
        surfaces that have them, the player benches, penalty boxes and
        off-field officials' box outside the boards (sportyR #63);
        ``"in_bounds_only"`` the field plus the boards' thickness; the half
        fields run from the center line out to the same extent. With
        ``for_plot`` (limits for plotted data) only the field is used. An
        explicit ``xlim``/``ylim`` tuple replaces the range (less the
        translation).
        """
        p = self.field_params
        g = lambda key: p.get(key, 0.0)  # noqa: E731
        half_length = g("field_length") / 2.0
        half_width = g("field_width") / 2.0
        if for_display and not for_plot:
            boards = g("boards_thickness")
            half_length = max(
                half_length + g("field_apron_thickness"),
                g("bench_separation") / 2.0 + g("bench_length") + boards,
                g("penalty_box_separation") / 2.0 + g("penalty_box_length") + 2.0 * boards,
            )
            half_width += max(
                g("field_apron_thickness"),
                2.0 * boards + max(g("bench_depth"), g("penalty_box_depth")),
            )
        key = str(display_range or "full").lower()

        if key in ("in_bounds_only", "in bounds only"):
            boards = p.get("boards_thickness", 0.0)
            full_x = (
                -(p.get("field_length", 0.0) / 2.0 + boards),
                p.get("field_length", 0.0) / 2.0 + boards,
            )
            full_y = (
                -(p.get("field_width", 0.0) / 2.0 + boards),
                p.get("field_width", 0.0) / 2.0 + boards,
            )
        else:
            side = _HALVES.get(key, 0)
            full_x = {1: (0.0, half_length), -1: (-half_length, 0.0)}.get(
                side, (-half_length, half_length)
            )
            full_y = (-half_width, half_width)

        x = (xlim[0] - self.x_trans, xlim[1] - self.x_trans) if xlim else full_x
        y = (ylim[0] - self.y_trans, ylim[1] - self.y_trans) if ylim else full_y
        return (min(x), max(x)), (min(y), max(y))


class NCAAMLacrosseField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to NCAA men's lacrosse."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="ncaam", field_updates=field_updates, *args, **kwargs
        )


class NCAAWLacrosseField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to NCAA women's lacrosse."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="ncaaw", field_updates=field_updates, *args, **kwargs
        )


class NLLField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to the NLL (box lacrosse)."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="nll", field_updates=field_updates, *args, **kwargs
        )


class PLLField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to the PLL."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="pll", field_updates=field_updates, *args, **kwargs
        )


class USAMLacrosseField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to USA Lacrosse (men's)."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="usam", field_updates=field_updates, *args, **kwargs
        )


class USAWLacrosseField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to USA Lacrosse (women's)."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="usaw", field_updates=field_updates, *args, **kwargs
        )


class WorldLacrosseField(LacrosseField):
    """A subclass of ``LacrosseField`` specific to World Lacrosse (box)."""

    def __init__(self, field_updates=None, *args, **kwargs):
        super().__init__(
            league_code="world lacrosse", field_updates=field_updates, *args, **kwargs
        )
