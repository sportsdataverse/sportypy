"""Extension of the BaseSurfacePlot class to create a hockey rink.

This is a second-level child class of the BaseSurface class, and as such will
have access to its attributes and methods. Sportypy will ship with pre-defined
leagues that will have their own subclass, but a user can manually specify
their own rink parameters to create a totally-customized rink. The rink's
features are parameterized by the basic dimensions of the rink, which comprise
the attributes of the class.

@author: Ross Drucker
"""
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy._feature_classes.hockey as hockey
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class HockeyRink(BaseSurfacePlot):
    """A subclass of the BaseSurfacePlot class to make a generic hockey rink.

    This allows for the creation of the hockey rink in a way that is entirely
    parameterized by the rink's baseline characteristics.

    All attributes should default to 0.0 (if of a numeric type) or an empty
    string (if of a string type). Customized parameters may be specified via a
    child class (see below) or by directly specifying all necessary attributes
    of a valid ice hockey rink. The attributes needed to instantiate a
    particular league's surface must be specified in the rink_params
    dictionary. For many leagues, these will be provided in the hockey.json
    file in the data/ subdirectory of this module.

    See the BaseSurfacePlot and BaseSurface class definitions for full details.

    NOTE: Any attribute below that is prefixed with an asterisk (*) should be
    specified via the rink_updates dictionary as these parameters are specific
    to each league. Attributes prefixed with a hyphen (-) are specified at the
    time that the surface class is created

    Attributes
    ----------
    - league_code : str (default: '')
        The league for which the plot should be drawn. This is case-insensitive
        but should be the shortened name of the league (e.g. "National Hockey
        League" should be either "NHL" or "nhl")

    - rotation : float (default: 0.0)
        The angle (in degrees) through which to rotate the final plot

    - x_trans : float (default: 0.0)
        The amount that the x coordinates are to be shifted. By convention,
        the +x axis extends from the center of the ice surface towards the
        right-hand goal when viewing the rink in TV view

    - y_trans : float (default: 0.0)
        The amount that the y coordinates are to be shifted. By convention,
        the +y axis extends from the center of the ice surface towards the
        top of the rink when viewing the rink in TV view

    - colors_dict : dict
        A dictionary of coloring parameters to pass to the plot. Defaults are
        provided in the class per each rule book, but this allows the plot to
        be more heavily customized/styled

    - units : str (default: 'default')
        The units that the final plot should utilize. The default units are the
        units specified in the rule book of the league

    * rink_length : float
        The full length of the rink. Length is defined as the distance between
        the inner edge of the boards behind each goal at its widest point

    * rink_width : float
        The full width of the rink. Width is defined as the distance between
        the inner edge of the boards between the team bench and the penalty box
        on the other side of the ice

    * rink_units : str
        The units with which to draw the rink

    * corner_radius : float
        The radius of the circle that comprises the rink's corners

    * board_thickness : float
        The thickness of the boards. This is to give the boundary of the rink a
        clearer-to-see definition, although only the inner edge of the boards
        is considered in play and the boundary of the rink

    * referee_crease_radius : float
        The outer radius of the semi-circle that comprises the referee's crease

    * nzone_length : float
        The length of the neutral zone, measured from the interior edges of the
        zone lines (blue lines)

    * goal_line_to_boards : float
        The x position of the center of the right-hand goal line relative to
        the boards behind the right-hand goal when viewing the rink in TV view

    * major_line_thickness : float
        The thickness of the major lines on the ice surface. Major lines are
        considered to be the center line (red line) and zone lines (blue lines)

    * minor_line_thickness : float
        The thickness of the minor lines on the ice surface. Minor lines are
        those such as goal lines, hash marks, faceoff markings, or circle
        thicknesses

    * faceoff_circle_radius : float
        The radius of the faceoff circles, both center and non-center, on the
        ice

    * center_faceoff_spot_radius : float
        The radius of the center faceoff spot on the ice

    * noncenter_faceoff_spot_radius : float
        The radius of the non-centered faceoff spots on the ice. These are in
        the defensive, neutral, and offensive zones

    * nzone_faceoff_spot_to_zone_line : float
        The x position of the right-side faceoff spots in the neutral zone
        relative to the neutral-zone side of the zone (blue) line when viewing
        the rink in TV view

    * odzone_faceoff_spot_to_boards : float
        The distance (in the x direction) from the end of the rink to the
        center of the defensive/offensive zone faceoff spot

    * noncenter_faceoff_spot_y : float
        The y position of the upper faceoff spots in the defensive, neutral,
        and offensive zones on the ice when viewing the rink in TV view

    * noncenter_faceoff_spot_gap_width : float
        The gap between the interior edge of a non-centered faceoff spot ring
        and the stripe running across it

    * hashmark_width : float
        The width of the hashmarks on the exterior of the defensive and
        offensive faceoff circles. Note that width refers to a distance solely
        in the y direction when viewing the rink in TV View

    * hashmark_ext_spacing : float
        The exterior horizontal spacing between the hashmarks on the exterior
        of the defensive and offensive faceoff circles when viewing the rink in
        TV view. Note that this is solely in the x direction

    * faceoff_line_dist_x : float
        The distance from the center of the defensive and offensive faceoff
        spot to the left-most edge of the upper-right faceoff line when viewing
        the rink in TV view

    * faceoff_line_dist_y: float
        The distance from the center of the defensive and offensive faceoff
        spot to the bottom edge of the upper-right faceoff line when viewing
        the rink in TV view

    * faceoff_line_length : float
        The exterior length of the faceoff line when viewing the rink in TV
        view

    * faceoff_line_width : float
        The exterior width of the faceoff line when viewing the rink in TV view

    * has_trapezoid : boolean
        Indicator of whether or not the rink has a goalkeeper's restricted area
        (trapezoid) behind each goal

    * short_base_width : float
        The exterior base-width of the trapezoid (should it exist) that lies
        along the goal line

    * long_base_width : float
        The exterior base-width of the trapezoid (should it exist) that lies
        along the boards

    * goal_crease_style : str
        The style of goal crease to implement. Viable options are:
            nhl98 : the current iteration of the NHL goal crease. This is what
                is used for most professional leagues

            nhl92 : the previous iteration of an NHL goal crease. It is drawn
                as a semi-circle with two L-shaped notches at the edge of the
                crease intersecting the semi-circle

            ushl1 : the current iteration of a USA Hockey goal crease. This is
                what is currently used in the USHL (United States Hockey
                League)

    * goal_crease_radius : float
        The radius of the rounded portion of the goal crease, as taken from the
        center of the goal line

    * goal_crease_length : float
        The distance from the center of the goal line to the start of the arc
        of the goal crease

    * goal_crease_width : float
        The exterior width of the goal crease

    * goal_crease_notch_dist_x : float
        The distance from the center of the goal line to the notch (if one
        exists) in the goal crease

    * goal_crease_notch_width : float
        The width of the notch (if one exists) in the goal crease

    * goal_mouth_width : float
        The interior distance between the goalposts

    * goal_back_width : float
        The exterior distance between the widest part of the goal frame's
        footprint

    * goal_depth : float
        The depth of the goal frame from the center of the goal line to the
        exterior of the back pipe of the goal frame

    * goal_post_diameter : float
        The diameter of the posts of the goal frame

    * goal_radius : float
        The interior radius of the goal frame

    * bench_length : float
        The exterior length of a single team's bench area

    * bench_depth : float
        The interior depth off the boards of a single team's bench area

    * bench_separation : float
        The separation between the two teams' bench areas

    * penalty_box_length : float
        The interior length of a single penalty box

    * penalty_box_depth : float
        The interior depth off of the boards of a single team's penalty box

    * penalty_box_separation : float
        The distance that separates each team's penalty box area. This should
        be equivalent to the length of the off-ice officials' box
    """

    def __init__(self, league_code = '', rink_updates = {}, colors_dict = {},
                 rotation = 0.0, x_trans = 0.0, y_trans = 0.0,
                 units = 'default', **added_features):
        # Load all pre-defined rink dimensions for provided leagues
        self._load_preset_dimensions(sport = 'hockey')

        # Load all unit conversions
        self._load_unit_conversions()

        # Set the league to be the lower-case version of the supplied value
        self.league_code = league_code.lower()

        # Try to get the league specified from the pre-defined set of leagues
        try:
            rink_dimensions = self.league_dimensions[self.league_code]

        # If it can't be found, set the rink_dimensions dictionary to be empty
        except KeyError:
            rink_dimensions = {}

        # Combine the rink dimensions (if found from in the pre-defined
        # leagues) with any parameter updates supplied by the user. This will
        # comprise the parameter set with which the rink is to be drawn
        rink_params = {
            **rink_dimensions,
            **rink_updates
        }

        # Set the passed parameters of the rink to be the class' rink_params
        # attribute
        self.rink_params = rink_params

        # Convert the rink's units if needed
        if units.lower() != 'default':
            for k, v in rink_params.items():
                self.rink_params[k] = self._convert_units(
                    v,
                    self.rink_params['rink_units'],
                    units.lower()
                )

        # Set the rotation of the plot to be the supplied rotation value
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the rink's necessary shifts. This will overwrite the default
        # values of x_trans and y_trans inherited from the BaseSurfacePlot
        # class (which is in turn inherited from BaseSurface)
        self.x_trans, self.y_trans = x_trans, y_trans

        # Create a container for the relevant features of an ice rink
        self._features = []

        # Initialize the x and y limits for the plot be None. These will get
        # set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the default colors of the rink
        default_colors = {
            'plot_background': '#ffffff',
            'boards': '#000000',
            'ozone_ice': '#ffffff',
            'nzone_ice': '#ffffff',
            'dzone_ice': '#ffffff',
            'center_line': '#c8102e',
            'zone_line': '#0033a0',
            'goal_line': '#c8102e',
            'restricted_trapezoid': '#c8102e',
            'goal_crease_outline': '#c8102e',
            'goal_crease_fill': '#41b6e6',
            'referee_crease': '#c8102e',
            'center_faceoff_spot': '#0033a0',
            'faceoff_spot_ring': '#c8102e',
            'faceoff_spot_stripe': '#c8102e',
            'center_faceoff_circle': '#0033a0',
            'odzone_faceoff_circle': '#c8102e',
            'faceoff_line': '#c8102e',
            'goal_frame': '#c8102e',
            'goal_fill': '#a5acaf4d',
            'team_a_bench': '#ffffff',
            'team_b_bench': '#ffffff',
            'team_a_penalty_box': '#ffffff',
            'team_b_penalty_box': '#ffffff',
            'off_ice_officials_box': '#a5acaf'
        }

        # Combine the colors with a passed colors dictionary
        if not colors_dict:
            colors_dict = {}

        # Create the final color set for the features of the rink
        self.feature_colors = {
            **default_colors,
            **colors_dict
        }

        # Initialize the constraint on the rink to confine all features to be
        # contained within the boards. The feature itself is not visible (as
        # it's created by the hockey.Boards class)
        boards_constraint_params = {
            'class': hockey.BoardsConstraint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_radius': self.rink_params.get('corner_radius', 0.0),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'visible': False
        }
        self._initialize_feature(boards_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        #######################################################################
        #                              zorder = 1                             #
        #######################################################################

        # Initialize the defensive zone
        dzone_params = {
            'class': hockey.DefensiveZone,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'nzone_length': self.rink_params.get('nzone_length', 0.0),
            'feature_radius': self.rink_params.get('corner_radius', 0.0),
            'visible': True,
            'facecolor': self.feature_colors['dzone_ice'],
            'edgecolor': self.feature_colors['dzone_ice'],
            'zorder': 1
        }
        self._initialize_feature(dzone_params)

        # Initialize the neutral zone
        nzone_params = {
            'class': hockey.NeutralZone,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_thickness': self.rink_params.get('nzone_length', 0.0),
            'visible': True,
            'facecolor': self.feature_colors['nzone_ice'],
            'edgecolor': self.feature_colors['nzone_ice'],
            'zorder': 1
        }
        self._initialize_feature(nzone_params)

        # Initialize the offensive zone
        ozone_params = {
            'class': hockey.OffensiveZone,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'nzone_length': self.rink_params.get('nzone_length', 0.0),
            'feature_radius': self.rink_params.get('corner_radius', 0.0),
            'visible': True,
            'facecolor': self.feature_colors['ozone_ice'],
            'edgecolor': self.feature_colors['ozone_ice'],
            'zorder': 1
        }
        self._initialize_feature(ozone_params)

        #######################################################################
        #                             zorder = 10                             #
        #######################################################################

        # Initialize the goal crease's filled-in interior
        goal_crease_fill_params = {
            'class': hockey.GoalCreaseFill,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('goal_line_to_boards', 0.0)
            ),
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'crease_length': self.rink_params.get('goal_crease_length', 0.0),
            'crease_width': self.rink_params.get('goal_crease_width', 0.0),
            'notch_dist_x': self.rink_params.get(
                'goal_crease_notch_dist_x',
                0.0
            ),
            'notch_width': self.rink_params.get(
                'goal_crease_notch_width',
                0.0
            ),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'crease_style': self.rink_params.get('goal_crease_style', 'nhl98'),
            'feature_radius': self.rink_params.get('goal_crease_radius', 0.0),
            'facecolor': self.feature_colors['goal_crease_fill'],
            'edgecolor': self.feature_colors['goal_crease_fill'],
            'zorder': 10
        }
        self._initialize_feature(goal_crease_fill_params)

        # Initialize the goal frame
        goal_frame_params = {
            'class': hockey.GoalFrame,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('goal_line_to_boards', 0.0)
            ),
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'goal_mouth_width': self.rink_params.get('goal_mouth_width', 0.0),
            'goal_back_width': self.rink_params.get('goal_back_width', 0.0),
            'goal_depth': self.rink_params.get('goal_depth', 0.0),
            'post_diameter': self.rink_params.get('goal_post_diameter', 0.0),
            'feature_radius': self.rink_params.get('goal_radius', 0.0),
            'facecolor': self.feature_colors['goal_frame'],
            'edgecolor': self.feature_colors['goal_frame'],
            'zorder': 10
        }
        self._initialize_feature(goal_frame_params)

        # Initialize the goal frame's filled-in interior
        goal_frame_fill_params = {
            'class': hockey.GoalFrameFill,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('goal_line_to_boards', 0.0)
            ),
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'goal_mouth_width': self.rink_params.get('goal_mouth_width', 0.0),
            'goal_back_width': self.rink_params.get('goal_back_width', 0.0),
            'goal_depth': self.rink_params.get('goal_depth', 0.0),
            'post_diameter': self.rink_params.get('goal_post_diameter', 0.0),
            'feature_radius': self.rink_params.get('goal_radius', 0.0),
            'facecolor': self.feature_colors['goal_fill'],
            'edgecolor': self.feature_colors['goal_fill'],
            'zorder': 10
        }
        self._initialize_feature(goal_frame_fill_params)

        #######################################################################
        #                             zorder = 15                             #
        #######################################################################

        # Initialize the goalkeeper's restricted area (if it's required)
        if self.rink_params.get('has_trapezoid', False):
            goaltenders_restricted_area_params = {
                'class': hockey.GoaltendersRestrictedArea,
                'x_anchor': (
                    (self.rink_params.get('rink_length', 0.0) / 2.0) -
                    self.rink_params.get('goal_line_to_boards', 0.0)
                ),
                'y_anchor': 0.0,
                'reflect_x': True,
                'reflect_y': False,
                'short_base_width': self.rink_params.get(
                    'short_base_width',
                    0.0
                ),
                'long_base_width': self.rink_params.get(
                    'long_base_width',
                    0.0
                ),
                'rink_length': self.rink_params.get('rink_length', 0.0),
                'rink_width': self.rink_params.get('rink_width', 0.0),
                'feature_thickness': self.rink_params.get(
                    'minor_line_thickness',
                    0.0
                ),
                'facecolor': self.feature_colors['restricted_trapezoid'],
                'edgecolor': self.feature_colors['restricted_trapezoid'],
                'zorder': 15
            }
            self._initialize_feature(goaltenders_restricted_area_params)

        # Initialize the goal crease outlines
        goal_crease_outline_params = {
            'class': hockey.GoalCreaseOutline,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('goal_line_to_boards', 0.0)
            ),
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'crease_length': self.rink_params.get('goal_crease_length', 0.0),
            'crease_width': self.rink_params.get('goal_crease_width', 0.0),
            'notch_dist_x': self.rink_params.get(
                'goal_crease_notch_dist_x',
                0.0
            ),
            'notch_width': self.rink_params.get(
                'goal_crease_notch_width',
                0.0
            ),
            'crease_style': self.rink_params.get('goal_crease_style', 'nhl98'),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get('goal_crease_radius', 0.0),
            'facecolor': self.feature_colors['goal_crease_outline'],
            'edgecolor': self.feature_colors['goal_crease_outline'],
            'zorder': 15
        }
        self._initialize_feature(goal_crease_outline_params)

        # Initialize the center faceoff circle
        center_faceoff_circle_params = {
            'class': hockey.CenterFaceoffCircle,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'faceoff_circle_radius',
                0.0
            ),
            'facecolor': self.feature_colors['center_faceoff_circle'],
            'edgecolor': self.feature_colors['center_faceoff_circle'],
            'zorder': 15
        }
        self._initialize_feature(center_faceoff_circle_params)

        # Initialize the faceoff spots in the neutral zone
        nzone_faceoff_spot_ring_params = {
            'class': hockey.NODZoneFaceoffSpotRing,
            'x_anchor': (
                (self.rink_params.get('nzone_length', 0.0) / 2.0) -
                self.rink_params.get('nzone_faceoff_spot_to_zone_line', 0.0)
            ),
            'y_anchor': self.rink_params.get(
                'noncenter_faceoff_spot_y',
                0.0
            ),
            'reflect_x': True,
            'reflect_y': True,
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'noncenter_faceoff_spot_radius',
                0.0
            ),
            'facecolor': self.feature_colors['faceoff_spot_ring'],
            'edgecolor': self.feature_colors['faceoff_spot_ring'],
            'zorder': 15
        }
        self._initialize_feature(nzone_faceoff_spot_ring_params)

        # Initialize the faceoff spot stripes in the neutral zone
        nzone_faceoff_spot_stripe_params = {
            'class': hockey.NODZoneFaceoffSpotStripe,
            'x_anchor': (
                (self.rink_params.get('nzone_length', 0.0) / 2.0) -
                self.rink_params.get('nzone_faceoff_spot_to_zone_line', 0.0)
            ),
            'y_anchor': self.rink_params.get(
                'noncenter_faceoff_spot_y',
                0.0
            ),
            'reflect_x': True,
            'reflect_y': True,
            'gap_width': self.rink_params.get(
                'noncenter_faceoff_spot_gap_width',
                0.0
            ),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'noncenter_faceoff_spot_radius',
                0.0
            ),
            'facecolor': self.feature_colors['faceoff_spot_stripe'],
            'edgecolor': self.feature_colors['faceoff_spot_stripe'],
            'zorder': 15
        }
        self._initialize_feature(nzone_faceoff_spot_stripe_params)

        # Initialize the faceoff circles in the offensive/defensive zones
        odzone_faceoff_circle_params = {
            'class': hockey.ODZoneFaceoffCircle,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('odzone_faceoff_spot_to_boards', 0.0)
            ),
            'y_anchor': self.rink_params.get('noncenter_faceoff_spot_y', 0.0),
            'reflect_x': True,
            'reflect_y': True,
            'hashmark_width': self.rink_params.get('hashmark_width', 0.0),
            'hashmark_ext_spacing': self.rink_params.get(
                'hashmark_ext_spacing',
                0.0
            ),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'faceoff_circle_radius',
                0.0
            ),
            'facecolor': self.feature_colors['odzone_faceoff_circle'],
            'edgecolor': self.feature_colors['odzone_faceoff_circle'],
            'zorder': 15
        }
        self._initialize_feature(odzone_faceoff_circle_params)

        # Initialize the faceoff spot rings in the offensive/defensive zones
        odzone_faceoff_spot_ring_params = {
            'class': hockey.NODZoneFaceoffSpotRing,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('odzone_faceoff_spot_to_boards', 0.0)
            ),
            'y_anchor': self.rink_params.get(
                'noncenter_faceoff_spot_y',
                0.0
            ),
            'reflect_x': True,
            'reflect_y': True,
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'noncenter_faceoff_spot_radius',
                0.0
            ),
            'facecolor': self.feature_colors['faceoff_spot_ring'],
            'edgecolor': self.feature_colors['faceoff_spot_ring'],
            'zorder': 15
        }
        self._initialize_feature(odzone_faceoff_spot_ring_params)

        # Initialize the faceoff spot stripes in the offensive/defensive zones
        odzone_faceoff_spot_stripe_params = {
            'class': hockey.NODZoneFaceoffSpotStripe,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('odzone_faceoff_spot_to_boards', 0.0)
            ),
            'y_anchor': self.rink_params.get(
                'noncenter_faceoff_spot_y',
                0.0
            ),
            'reflect_x': True,
            'reflect_y': True,
            'gap_width': self.rink_params.get(
                'noncenter_faceoff_spot_gap_width',
                0.0
            ),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'noncenter_faceoff_spot_radius',
                0.0
            ),
            'facecolor': self.feature_colors['faceoff_spot_stripe'],
            'edgecolor': self.feature_colors['faceoff_spot_stripe'],
            'zorder': 15
        }
        self._initialize_feature(odzone_faceoff_spot_stripe_params)

        # Initialize the bench for Team A. This will be located on the TV-left
        # team bench area
        team_a_bench_params = {
            'class': hockey.PlayerBenchFill,
            'x_anchor': -(
                (self.rink_params.get('bench_separation', 0.0) / 2.0) +
                (self.rink_params.get('bench_length', 0.0) / 2.0)
            ),
            'y_anchor': self.rink_params.get('rink_width', 0.0) / 2.0,
            'reflect_x': False,
            'reflect_y': False,
            'bench_length': self.rink_params.get('bench_length', 0.0),
            'bench_depth': self.rink_params.get('bench_depth', 0.0),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['team_a_bench'],
            'edgecolor': self.feature_colors['team_a_bench'],
            'zorder': 15
        }
        self._initialize_feature(team_a_bench_params)

        # Initialize the bench for Team B. This will be located on the TV-right
        # team bench area
        team_b_bench_params = {
            'class': hockey.PlayerBenchFill,
            'x_anchor': (
                (self.rink_params.get('bench_separation', 0.0) / 2.0) +
                (self.rink_params.get('bench_length', 0.0) / 2.0)
            ),
            'y_anchor': self.rink_params.get('rink_width', 0.0) / 2.0,
            'reflect_x': False,
            'reflect_y': False,
            'bench_length': self.rink_params.get('bench_length', 0.0),
            'bench_depth': self.rink_params.get('bench_depth', 0.0),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['team_b_bench'],
            'edgecolor': self.feature_colors['team_b_bench'],
            'zorder': 15
        }
        self._initialize_feature(team_b_bench_params)

        # Initialize the penalty box for Team A. This will be located on the
        # TV-left team bench area
        team_a_penalty_box_params = {
            'class': hockey.PenaltyBoxFill,
            'x_anchor': -(
                (self.rink_params.get('penalty_box_separation', 0.0) / 2.0) +
                self.rink_params.get('board_thickness', 0.0) +
                (self.rink_params.get('penalty_box_length', 0.0) / 2.0)
            ),
            'y_anchor': -(
                (self.rink_params.get('rink_width', 0.0) / 2.0) -
                self.rink_params.get('board_thickness', 0.0)
            ),
            'reflect_x': False,
            'reflect_y': False,
            'penalty_box_length': self.rink_params.get(
                'penalty_box_length',
                0.0
            ),
            'penalty_box_depth': self.rink_params.get(
                'penalty_box_depth',
                0.0
            ),
            'penalty_box_separation': self.rink_params.get(
                'penalty_box_separation',
                0.0
            ),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['team_a_penalty_box'],
            'edgecolor': self.feature_colors['team_a_penalty_box'],
            'zorder': 15
        }
        self._initialize_feature(team_a_penalty_box_params)

        # Initialize the penalty box for Team B. This will be located on the
        # TV-right team bench area
        team_b_penalty_box_params = {
            'class': hockey.PenaltyBoxFill,
            'x_anchor': (
                (self.rink_params.get('penalty_box_separation', 0.0) / 2.0) +
                self.rink_params.get('board_thickness', 0.0) +
                (self.rink_params.get('penalty_box_length', 0.0) / 2.0)
            ),
            'y_anchor': -(
                (self.rink_params.get('rink_width', 0.0) / 2.0) -
                self.rink_params.get('board_thickness', 0.0)
            ),
            'reflect_x': False,
            'reflect_y': False,
            'penalty_box_length': self.rink_params.get(
                'penalty_box_length',
                0.0
            ),
            'penalty_box_depth': self.rink_params.get(
                'penalty_box_depth',
                0.0
            ),
            'penalty_box_separation': self.rink_params.get(
                'penalty_box_separation',
                0.0
            ),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['team_b_penalty_box'],
            'edgecolor': self.feature_colors['team_b_penalty_box'],
            'zorder': 15
        }
        self._initialize_feature(team_b_penalty_box_params)

        # Initialize the off-ice officials' box
        off_ice_officials_box_params = {
            'class': hockey.OffIceOfficialsBox,
            'x_anchor': 0.0,
            'y_anchor': -(
                (self.rink_params.get('rink_width', 0.0) / 2.0) -
                self.rink_params.get('board_thickness', 0.0)
            ),
            'reflect_x': False,
            'reflect_y': False,
            'officials_box_length': self.rink_params.get(
                'penalty_box_separation',
                0.0
            ),
            'officials_box_depth': self.rink_params.get(
                'penalty_box_depth',
                0.0
            ),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['off_ice_officials_box'],
            'edgecolor': self.feature_colors['off_ice_officials_box'],
            'zorder': 15
        }
        self._initialize_feature(off_ice_officials_box_params)

        #######################################################################
        #                             zorder = 20                             #
        #######################################################################

        # Initialize the center (red) line
        center_line_params = {
            'class': hockey.CenterLine,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'reflect_x': False,
            'reflect_y': False,
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_thickness': self.rink_params.get(
                'major_line_thickness',
                0.0
            ),
            'facecolor': self.feature_colors['center_line'],
            'edgecolor': self.feature_colors['center_line'],
            'zorder': 20
        }
        self._initialize_feature(center_line_params)

        # Initialize the zone (blue) lines
        zone_line_params = {
            'class': hockey.ZoneLine,
            'x_anchor': self.rink_params.get('nzone_length', 0.0) / 2.0,
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_thickness': self.rink_params.get(
                'major_line_thickness',
                0.0
            ),
            'facecolor': self.feature_colors['zone_line'],
            'edgecolor': self.feature_colors['zone_line'],
            'zorder': 20
        }
        self._initialize_feature(zone_line_params)

        # Initialize the goal lines
        goal_line_params = {
            'class': hockey.GoalLine,
            'x_anchor': (
                (self.rink_params.get('rink_length', 0.0) / 2.0) -
                self.rink_params.get('goal_line_to_boards', 0.0)
            ),
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get('corner_radius', 0.0),
            'facecolor': self.feature_colors['goal_line'],
            'edgecolor': self.feature_colors['goal_line'],
            'zorder': 20
        }
        self._initialize_feature(goal_line_params)

        # Initialize the referee's crease
        referee_crease_params = {
            'class': hockey.RefereeCrease,
            'x_anchor': 0.0,
            'y_anchor': -self.rink_params.get('rink_width', 0.0) / 2.0,
            'reflect_x': True,
            'reflect_y': False,
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_thickness': self.rink_params.get(
                'minor_line_thickness',
                0.0
            ),
            'feature_radius': self.rink_params.get(
                'referee_crease_radius',
                0.0
            ),
            'facecolor': self.feature_colors['referee_crease'],
            'edgecolor': self.feature_colors['referee_crease'],
            'zorder': 20
        }
        self._initialize_feature(referee_crease_params)

        # Initialize the faceoff lines. These are the L's located around the
        # offensive/defensive zone faceoff spots. Each L is created
        # individually at the center of the plot and then translated to its
        # proper ending location, so each L-shaped piece needs to be reflected
        # over x (but not y), over y (but not x), and over x and y
        # simultaneously. This is controlled by the two for-loops. See the
        # class definition for more details
        for over_x in [False, True]:
            for over_y in [False, True]:
                odzone_faceoff_line_params = {
                    'class': hockey.ODZoneFaceoffLines,
                    'x_anchor': (
                        (self.rink_params.get('rink_length', 0.0) / 2.0) -
                        self.rink_params.get(
                            'odzone_faceoff_spot_to_boards',
                            0.0
                        )
                    ),
                    'y_anchor': self.rink_params.get(
                        'noncenter_faceoff_spot_y',
                        0.0
                    ),
                    'reflect_x': True,
                    'reflect_y': True,
                    'over_x': over_x,
                    'over_y': over_y,
                    'faceoff_line_dist_x': self.rink_params.get(
                        'faceoff_line_dist_x',
                        0.0
                    ),
                    'faceoff_line_dist_y': self.rink_params.get(
                        'faceoff_line_dist_y',
                        0.0
                    ),
                    'faceoff_line_length': self.rink_params.get(
                        'faceoff_line_length',
                        0.0
                    ),
                    'faceoff_line_width': self.rink_params.get(
                        'faceoff_line_width',
                        0.0
                    ),
                    'feature_thickness': self.rink_params.get(
                        'minor_line_thickness',
                        0.0
                    ),
                    'facecolor': self.feature_colors['faceoff_line'],
                    'edgecolor': self.feature_colors['faceoff_line'],
                    'zorder': 20
                }
                self._initialize_feature(odzone_faceoff_line_params)

        #######################################################################
        #                             zorder = 25                             #
        #######################################################################

        # Initialize the center faceoff spot
        center_faceoff_spot_params = {
            'class': hockey.CenterFaceoffSpot,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'feature_radius': self.rink_params.get(
                'center_faceoff_spot_radius',
                0.0
            ),
            'facecolor': self.feature_colors['center_faceoff_spot'],
            'edgecolor': self.feature_colors['center_faceoff_spot'],
            'zorder': 25
        }
        self._initialize_feature(center_faceoff_spot_params)

        #######################################################################
        #                             zorder = 100                            #
        #######################################################################

        # Initialize the boards of the rink. NOTE: the zorder is set to be the
        # highest here to be plotted over any other features that it may
        # overlap
        board_params = {
            'class': hockey.Boards,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'rink_length': self.rink_params.get('rink_length', 0.0),
            'rink_width': self.rink_params.get('rink_width', 0.0),
            'feature_radius': self.rink_params.get('corner_radius', 0.0),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['boards'],
            'edgecolor': self.feature_colors['boards'],
            'zorder': 100
        }
        self._initialize_feature(board_params)

        # Initialize the player benches
        bench_params = {
            'class': hockey.PlayerBenchOutline,
            'x_anchor': self.rink_params.get('bench_separation', 0.0) / 2.0,
            'y_anchor': self.rink_params.get('rink_width', 0.0) / 2.0,
            'reflect_x': True,
            'reflect_y': False,
            'bench_length': self.rink_params.get('bench_length', 0.0),
            'bench_depth': self.rink_params.get('bench_depth', 0.0),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['boards'],
            'edgecolor': self.feature_colors['boards'],
            'zorder': 100
        }
        self._initialize_feature(bench_params)

        # Initialize the penalty boxes
        penalty_box_params = {
            'class': hockey.PenaltyBoxOutline,
            'x_anchor': 0.0,
            'y_anchor': -(
                (self.rink_params.get('rink_width', 0.0) / 2.0) -
                self.rink_params.get('board_thickness', 0.0)
            ),
            'reflect_x': True,
            'reflect_y': False,
            'penalty_box_length': self.rink_params.get(
                'penalty_box_length',
                0.0
            ),
            'penalty_box_depth': self.rink_params.get(
                'penalty_box_depth',
                0.0
            ),
            'penalty_box_separation': self.rink_params.get(
                'penalty_box_separation',
                0.0
            ),
            'feature_thickness': self.rink_params.get('board_thickness', 0.0),
            'facecolor': self.feature_colors['boards'],
            'edgecolor': self.feature_colors['boards'],
            'zorder': 100
        }
        self._initialize_feature(penalty_box_params)

        # Initialize all other features passed as keyword arguments
        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = 'full', xlim = None, ylim = None,
             rotation = None):
        """Draw the rink.

        Parameters
        ----------
        ax : matplotlib.Axes
            An axes object onto which the plot can be drawn. If None is
            supplied, then the currently-active Axes object will be used

        display_range : str; default "full"
            The portion of the surface to display. The entire surface
            will always be drawn under the hood, however this parameter
            limits what is shown in the final plot. The following explain what
            each display range corresponds to:

            'full' : the entire ice surface

            'offense' : the offensive (TV-right) half of the ice surface

            'offence' : the offensive (TV-right) half of the ice surface

            'defense' : the defensive (TV-left) half of the ice surface

            'defence' : the defensive (TV-left) half of the ice surface

            'nzone' : the neutral zone (the area between the zone lines)

            'neutral' : the neutral zone (the area between the zone lines)

            'neutral_zone' : the neutral zone (the area between the zone lines)

            'neutral zone' : the neutral zone (the area between the zone lines)

            'ozone' : the offensive zone. This is the area (TV-right) of the
                neutral zone

            'offensive_zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'offensive zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'attacking_zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'attacking zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'dzone' : the defensive zone. This is the area (TV-left) of the
                neutral zone

            'defensive_zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

            'defensive zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

            'defending_zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

            'defending zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

        xlim : float, tuple (float, float), or None (default: None)
            The display range in the x direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the x coordinates to display and the upper bound will be the
            +x end of the boards. If a tuple, the two values will be
            used to determine the bounds. If None, then the
            display_range will be used instead to set the bounds

        ylim : float, tuple (float, float), or None (default: None)
            The display range in the y direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the y coordinates to display and the upper bound will be the
            +y side of the rink. If a tuple, the two values will be used
            to determine the bounds. If None, then the display_range
            will be used instead to set the bounds

        rotation : float or None (default: None)
            Angle (in degrees) through which to rotate the rink when
            drawing. If used, this will set the class attribute of
            self._rotation. A value of 0.0 will correspond to a TV View
            of the rink, where +x is to the right and +y is on top. The
            rotation occurs counter clockwise
        """
        # If there is a rotation to be applied, apply it first and set it as
        # the class attribute self._rotation
        if rotation:
            self._rotation = Affine2D().rotate_deg(rotation)

        # If an Axes object is not provided, create one to use for plotting
        if ax is None:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor(self.feature_colors['plot_background'])
            fig.set_size_inches(50, 50)
            ax = plt.gca()

        # Set the aspect ratio to be equal and remove the axis to leave only
        # the plot
        ax.set_aspect('equal')
        ax.axis('off')

        # Get the transformation to apply
        transform = self._get_transform(ax)

        # Add each feature
        for feature in self._features:
            # Start by adding the feature to the current Axes object
            feature.draw(ax, transform)

            try:
                # Check the feature's visibility
                visible = feature.visible
            except AttributeError:
                # If the feature doesn't have a visible attribute, set its
                # visibility to be true by default
                visible = True

            # Assuming the feature is visible (and is not the boards), get
            # the feature's x and y limits to ensure it lies within the
            # bounds of the rink
            if visible and not isinstance(feature, hockey.Boards):
                try:
                    feature_df = feature._translate_feature()

                    # If the feature doesn't have a limitation on x, set its
                    # limits to be its minimum and maximum values of x
                    if self._feature_xlim is None:
                        self._feature_xlim = [
                            feature_df['x'].min(),
                            feature_df['x'].max()
                        ]

                    # Otherwise, set the limits to be the smaller of its
                    # specified minimum and smallest x value or the larger
                    # of its specified maximum and largest x value
                    else:
                        self._feature_xlim = [
                            min(self._feature_xlim[0], feature_df['x'].min()),
                            max(self._feature_xlim[0], feature_df['x'].max())
                        ]

                    # If the feature doesn't have a limitation on y, set its
                    # limits to be its minimum and maximum values of y
                    if self._feature_ylim is None:
                        self._feature_ylim = [
                            feature_df['y'].min(),
                            feature_df['y'].max()
                        ]

                    # Otherwise, set the limits to be the smaller of its
                    # specified minimum and smallest y value or the larger
                    # of its specified maximum and largest y value
                    else:
                        self._feature_ylim = [
                            min(self._feature_ylim[0], feature_df['y'].min()),
                            max(self._feature_ylim[0], feature_df['y'].max())
                        ]

                except TypeError:
                    # If there is an error with the above process, do not
                    # set the x and y limits
                    pass

        # Set the plot's display range
        ax = self.set_plot_display_range(ax, display_range, xlim, ylim)

        return ax

    def cani_plot_leagues(self, league_code = None):
        """Show if a league can be plotted, or what leagues are pre-defined.

        A user may wish to know if a specific hockey league can be plotted.
        This method allows a user to check if that specific league code comes
        shipped with sportypy for easier plotting (if they provide the league
        code), or can also show what leagues are available to be plotted

        Parameters
        ----------
        league_code : str or None (default: None)
            A league code that may or may not be shipped with the package. If
            the league code is None, this will display all leagues that do come
            shipped with sportypy

        Returns
        -------
        available_league_codes : list or None
            A list of available league codes. If a user passes a league code
            that doesn't ship with sportypy, then the return will be None
        """
        # Define all available league codes
        available_league_codes = [k for k in self.league_dimensions.keys()]
        available_league_codes.sort()

        # If a user wants to know about a specific league, check if the league
        # comes pre-shipped with the package
        if league_code is not None:
            # Convert the league code to be all lower-case
            league_code = league_code.lower()

            # If the league code exists, return it as a list of length 1 with
            # a printed message
            if league_code in available_league_codes:
                print(f'{league_code.upper()} comes with sportypy and is '
                      'ready to use!')

                available_league_codes = [league_code]

            # Otherwise, alert the user that they will need to manually specify
            # the parameters of the league
            else:
                print(f'{league_code.upper()} does not come with sportypy, '
                      'but may be parameterized. Use the '
                      'cani_change_dimensions() to check what parameters are '
                      'needed.')

                available_league_codes = None

        # If no league code is provided, print out the list of all available
        else:
            # Preamble
            print('The following hockey leagues are available with '
                  'sportypy:\n')

            # Print the current leagues
            for league_code in available_league_codes:
                print(f'- {league_code.upper()}')

        return available_league_codes

    def cani_color_features(self):
        """Determine what features of the rink can be colored.

        This function is a helper function for the user to aid in plot styling
        and customization. The printed result of this method will be the names
        of the features that are able to be colored
        """
        # Preamble
        print('The following features can be colored via the colors_dict '
              'parameter, with the current value in parenthesis:\n')

        # Print the current values of the colors
        for k, v in self.feature_colors.items():
            print(f'- {k} ({v})')

        # Footer
        print('\nThese colors may be updated with the update_colors() method')

    def cani_change_dimension(self):
        """Determine what features of the rink can be re-parameterized.

        This function is a helper function for the user to aid in customizing
        a rink's parameters. The printed result of this method will be the
        names of the features that are able to be reparameterized. This method
        is also useful when defining new features and using an existing
        league's rink dimensions as a starting point
        """
        # Preamble
        print('The following features can be reparameterized via the '
              'rink_updates parameter, with the current value in '
              'parenthesis:\n')

        # Print the current values of the colors
        for k, v in self.rink_params.items():
            print(f'- {k} ({v})')

        # Footer
        print('\nThese parameters may be updated with the '
              'update_rink_params() method')

    def update_colors(self, color_updates = {}, *args, **kwargs):
        """Update the colors currently used in the plot.

        The colors can be passed at the initial instantiation of the class via
        the colors_dict parameter, but this method allows the colors to be
        updated after the initial instantiation and will re-instantiate the
        class with the new colors

        Parameters
        ----------
        color_updates : dict (default: {}; an empty dictionary)
            A dictionary where the keys correspond to the name of the feature
            that's color is to be updated (see cani_color_features() method for
            a list of these names)

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated colors
        """
        # Start by getting the currently-used feature colors
        current_colors = self.feature_colors

        # Create a new dictionary to hold the updated colors via dictionary
        # comprehension
        updated_colors = {
            **current_colors,
            **color_updates
        }

        # Re-instantiate the class with the new colors
        self.__init__(
            rink_updates = self.rink_params,
            colors_dict = updated_colors
        )

    def update_rink_params(self, rink_param_updates = {}, *args, **kwargs):
        """Update the rink's defining parameters.

        This method should primarily be used in cases when plotting a league
        not currently supported by sportypy

        Parameters
        ----------
        rink_updates : dict (default: {}; an empty dictionary)
            A dictionary where the keys correspond to the name of the parameter
            of the rink that is to be updated (see cani_change_dimension()
            method for a list of these parameters)

        Returns
        -------
        Nothing, but the class is re-instantiated with the updated parameters
        """
        # Start by getting the currently-used rink parameters
        current_rink_params = self.rink_params

        # Create a new dictionary to hold the updated parameters via dictionary
        # comprehension
        updated_rink_params = {
            **current_rink_params,
            **rink_param_updates
        }

        # Re-instantiate the class with the new parameters
        self.__init__(
            rink_updates = updated_rink_params,
            colors_dict = self.feature_colors
        )

    def reset_colors(self):
        """Reset the features of the rink to their default color set.

        The colors can be passed at the initial instantiation of the class via
        the colors_dict parameter, and through the update_colors() method,
        these can be changed. This method allows the colors to be reset to
        their default values after experiencing such a change
        """
        # Re-instantiate the class with the default colors
        default_colors = {
            'plot_background': '#ffffff',
            'boards': '#000000',
            'ozone_ice': '#ffffff',
            'nzone_ice': '#ffffff',
            'dzone_ice': '#ffffff',
            'center_line': '#c8102e',
            'zone_line': '#0033a0',
            'goal_line': '#c8102e',
            'restricted_trapezoid': '#c8102e',
            'goal_crease_outline': '#c8102e',
            'goal_crease_fill': '#41b6e6',
            'referee_crease': '#c8102e',
            'center_faceoff_spot': '#0033a0',
            'faceoff_spot_ring': '#c8102e',
            'faceoff_spot_stripe': '#c8102e',
            'center_faceoff_circle': '#0033a0',
            'odzone_faceoff_circle': '#c8102e',
            'faceoff_line': '#c8102e',
            'goal_frame': '#c8102e',
            'goal_fill': '#a5acaf4d',
            'team_a_bench': '#ffffff',
            'team_b_bench': '#ffffff',
            'team_a_penalty_box': '#ffffff',
            'team_b_penalty_box': '#ffffff',
            'off_ice_officials_box': '#a5acaf'
        }

        self.__init__(
            rink_updates = self.rink_params,
            colors_dict = default_colors
        )

    def reset_rink_params(self):
        """Reset the features of the rink to their default parameterizations.

        The rink parameters can be passed at the initial instantiation of the
        class via the rink_updates parameter, and through the
        update_rink_params() method, these can be changed. This method allows
        the feature parameterization to be reset to their default values after
        experiencing such a change
        """
        # Re-instantiate the class with the default parameters
        default_params = self.rink_dimensions[self.league_code]

        self.__init__(
            rink_updates = default_params,
            colors_dict = self.feature_colors
        )

    def _get_plot_range_limits(self, display_range = 'full', xlim = None,
                               ylim = None):
        """Get the x and y limits for the displayed plot.

        Parameters
        ----------
        display_range : str (default: 'full')
            The range of which to display the plot. This is a key that will
            be searched for in the ranges_dict parameter

        xlim : float or None (default: None)
            A specific limit on x for the plot

        ylim : float or None (default: None)
            A specific limit on y for the plot

        Returns
        -------
        xlim : tuple
            The x-directional limits for displaying the plot

        ylim : tuple
            The y-directional limits for displaying the plot
        """
        # Copy the supplied xlim and ylim parameters so as not to overwrite
        # the initial memory
        xlim = self.copy_(xlim)
        ylim = self.copy_(ylim)

        # Determine the length of half of the rink (including the thickness of
        # the boards)
        half_rink_length = (
            (self.rink_params.get('rink_length', 0.0) / 2.0) +
            (self.rink_params.get('board_thickness', 0.0))
        )

        half_rink_width = (
            (self.rink_params.get('rink_width', 0.0) / 2.0) +
            max(
                self.rink_params.get('bench_depth', 0.0),
                self.rink_params.get('penalty_box_depth', 0.0)
            ) +
            self.rink_params.get('board_thickness', 0.0)
        )

        half_nzone_length = (
            self.rink_params.get('nzone_length', 0.0) / 2.0 +
            self.rink_params.get('major_line_thickness', 0.0)
        )

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(' ', '')

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                'full': (-half_rink_length, half_rink_length),

                # Half-rink plots
                'offense': (0.0, half_rink_length),
                'offence': (0.0, half_rink_length),
                'defense': (-half_rink_length, 0.0),
                'defence': (-half_rink_length, 0.0),

                # Neutral zone
                'nzone': (-half_nzone_length, half_nzone_length),
                'neutral': (-half_nzone_length, half_nzone_length),
                'neutral_zone': (-half_nzone_length, half_nzone_length),
                'neutral zone': (-half_nzone_length, half_nzone_length),

                # Offensive zone
                'ozone': (half_nzone_length - 5.0, half_rink_length),
                'offensive_zone': (half_nzone_length - 5.0, half_rink_length),
                'offensive zone': (half_nzone_length - 5.0, half_rink_length),
                'attacking_zone': (half_nzone_length - 5.0, half_rink_length),
                'attacking zone': (half_nzone_length - 5.0, half_rink_length),

                # Defensive zone
                'dzone': (-half_rink_length, -half_nzone_length + 5.0),
                'defensive_zone': (
                    -half_rink_length,
                    -half_nzone_length + 5.0
                ),
                'defensive zone': (
                    -half_rink_length,
                    -half_nzone_length + 5.0
                ),
                'defending_zone': (
                    -half_rink_length,
                    -half_nzone_length + 5.0
                ),
                'defending zone': (
                    -half_rink_length,
                    -half_nzone_length + 5.0
                )
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # rink
            xlim = xlims.get(
                display_range,
                (-half_rink_length, half_rink_length)
            )

        # If an x limit is provided, try to use it
        else:
            try:
                xlim = (xlim[0] - self.x_trans, xlim[1] - self.x_trans)

            # If the limit provided is not a tuple, use the provided value as
            # best as possible. This will set the provided value as the lower
            # limit of x, and display any x values greater than it
            except TypeError:
                # Apply the necessary shift to align the plot limit with the
                # data
                xlim = xlim - self.x_trans

                # If the provided value for the x limit is beyond the end of
                # the boards, display the entire rink
                if xlim >= half_rink_length:
                    xlim = -half_rink_length

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_rink_length)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the rink. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(' ', '')

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                'full': (-(half_rink_width), half_rink_width),

                # Half-rink plots
                'offense': (-half_rink_width, half_rink_width),
                'offence': (-half_rink_width, half_rink_width),
                'defense': (-half_rink_width, half_rink_width),
                'defence': (-half_rink_width, half_rink_width),

                # Neutral zone
                'nzone': (-half_rink_width, half_rink_width),
                'neutral': (-half_rink_width, half_rink_width),
                'neutral_zone': (-half_rink_width, half_rink_width),
                'neutral zone': (-half_rink_width, half_rink_width),

                # Offensive zone
                'ozone': (-half_rink_width, half_rink_width),
                'offensive_zone': (-half_rink_width, half_rink_width),
                'offensive zone': (-half_rink_width, half_rink_width),
                'attacking_zone': (-half_rink_width, half_rink_width),
                'attacking zone': (-half_rink_width, half_rink_width),

                # Defensive zone
                'dzone': (-half_rink_width, half_rink_width),
                'defensive_zone': (-half_rink_width, half_rink_width),
                'defensive zone': (-half_rink_width, half_rink_width),
                'defending_zone': (-half_rink_width, half_rink_width),
                'defending zone': (-half_rink_width, half_rink_width)
            }

            # Extract the y limit from the dictionary, defaulting to the full
            # rink
            ylim = ylims.get(
                display_range,
                (-half_rink_width, half_rink_width)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= half_rink_width:
                    ylim = -half_rink_width

                ylim = (ylim, half_rink_width)

        # Smaller coordinate should always go first
        if xlim[0] > xlim[1]:
            xlim = (xlim[1], xlim[0])
        if ylim[0] > ylim[1]:
            ylim = (ylim[1], ylim[0])

        # Constrain the limits from going beyond the end of the rink (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_rink_length),
            min(xlim[1], half_rink_length)
        )

        ylim = (
            max(ylim[0], -half_rink_width),
            min(ylim[1], half_rink_width)
        )

        return xlim, ylim


class AHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the AHL.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'ahl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class ECHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the ECHL.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'echl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class IIHFRink(HockeyRink):
    """A subclass of HockeyRink specific to the IIHF.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'iihf',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class PHFRink(HockeyRink):
    """A subclass of HockeyRink specific to the PHF.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'phf',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class NCAARink(HockeyRink):
    """A subclass of HockeyRink specific to the NCAA.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'ncaa',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class NHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the NHL.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'nhl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class NWHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the NWHL.

    This class is created for historical reference; as of 2021 the NWHL has
    changed names to the Premier Hockey Federation. Please use PHFRink class
    going forward

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Deprecation notice that NWHL has changed to PHF
        print('As of the 2021-2022 season, the NWHL has changed names to be '
              'the Premier Hockey Federation (PHF). Please use PHFRink() '
              'going forward.')

        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'nwhl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class OHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the OHL.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'ohl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class QMJHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the QMJHL.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'qmjhl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )


class USHLRink(HockeyRink):
    """A subclass of HockeyRink specific to the USHL.

    See HockeyRink class documentation for full description.
    """

    def __init__(self, rink_updates = {}, *args, **kwargs):
        # Initialize the HockeyRink class with the relevant parameters
        super().__init__(
            league_code = 'ushl',
            rink_updates = rink_updates,
            *args,
            **kwargs
        )
