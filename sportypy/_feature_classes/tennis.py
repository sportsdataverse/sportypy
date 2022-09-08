"""Extensions of the ``BaseFeature`` class to be specific to tennis courts.

The features are all parameterized by the basic characteristics of a tennis
court. A user can manually specify their own court parameters in the
``TennisCourt`` class that will adjust the placement of these features, however
the features themselves will be consistent across all tennis surfaces.

@author: Ross Drucker
"""
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseTennisFeature(BaseFeature):
    """An extension of the ``BaseFeature`` class for tennis features.

    The following attributes are specific to tennis features only. For more
    information on inherited attributes, please see the ``BaseFeature`` class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
    court_length : float
        The length of the court in TV view. The default is ``0.0``

    court_width : float
        The width of the court in TV view. The default is ``0.0``

    feature_radius : float
        The radius needed to draw the feature. This may not be needed for all
        features. The default is ``0.0``

    feature_thickness : float
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed. The default is ``0.0``

    field_units : str
        The units with which the feature is drawn. The default is ``"ft"``
    """

    def __init__(self, court_length = 0.0, court_width = 0.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = "ft", *args, **kwargs):

        # Set the full-sized dimensions of the court
        self.court_length = court_length
        self.court_width = court_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class CourtConstraint(BaseTennisFeature):
    """The constraint around the interior edge of the court's boundary lines.

    This confines all interior features to be constrained inside the court, as
    well as any interior plots.
    """

    def _get_centered_feature(self):
        """Generate the points comprising the inner boundary of the court.

        This is done to constrain any features from extending needlessly beyond
        the edge of the court. Lines are considered out, so this should only
        trace the interior
        """
        # Define the length and width of the court as length and width
        # attributes. These will be used to constrain plotted points to be
        # defined inside the surface
        self.length = self.court_length
        self.width = self.court_width

        court_constraint_df = self.create_rectangle(
            x_min = -self.court_length / 2.0,
            x_max = self.court_length / 2.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return court_constraint_df


class Baseline(BaseTennisFeature):
    """The baseline of a tennis court.

    These are the lines behind which a player will serve the ball. They span
    the entire width of the court
    """

    def _get_centered_feature(self):
        """Generate the points comprising the baseline of the court.

        Lines are considered in play, so the outer edge of the baseline will
        lie along ``y = {court_length / 2.0}``
        """
        baseline_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return baseline_df


class Sideline(BaseTennisFeature):
    """A sideline on a tennis court.

    This may refer to either the singles or doubles sideline.
    """

    def _get_centered_feature(self):
        """Generate the points comprising a sideline on the court.

        Lines are considered in play, so the outer edge of the sideline will
        lie along ``x = {court_width / 2.0}``
        """
        sideline_df = self.create_rectangle(
            x_min = -self.court_length / 2.0,
            x_max = self.court_length / 2.0,
            y_min = -self.feature_thickness,
            y_max = 0.0
        )

        return sideline_df


class ServiceLine(BaseTennisFeature):
    """The serviceline on the court.

    A serve must land between the net and this line on the proper side of the
    court to be considered legal and in play.

    Attributes
    ----------
    singles_width : float
        The width of a singles court in the court's specified units
    """

    def __init__(self, singles_width = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.singles_width = singles_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the serviceline on the court.

        This line extend completely between the singles sidelines (but not
        extend to the doubles sidelines)
        """
        serviceline_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = -self.singles_width / 2.0,
            y_max = self.singles_width / 2.0
        )

        return serviceline_df


class CenterServiceline(BaseTennisFeature):
    """The center serviceline on the court.

    This line divides the service area into two parts: the ad court (left) and
    the deuce court (right)

    Attributes
    ----------
    center_serviceline_length : float
        The length of the center serviceline
    """

    def __init__(self, center_serviceline_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.center_serviceline_length = center_serviceline_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the center serviceline on the court.

        This line extends from the net to the back edge of the serviceline, and
        is centered on the line x = 0.0
        """
        center_serviceline_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.center_serviceline_length,
            y_min = -self.feature_thickness / 2.0,
            y_max = self.feature_thickness / 2.0
        )

        return center_serviceline_df


class CenterMark(BaseTennisFeature):
    """The center mark on the baseline of the court.

    This line identifies the center point of the baseline.

    Attributes
    ----------
    center_mark_length : float
        The distance that the center mark on the baseline protrudes forward
        from its anchor point at the back edge of the baseline
    """

    def __init__(self, center_mark_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.center_mark_length = center_mark_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the center mark on the court.

        This line should extend towards the net
        """
        center_mark_df = self.create_rectangle(
            x_min = -self.center_mark_length,
            x_max = 0.0,
            y_min = -self.feature_thickness / 2.0,
            y_max = self.feature_thickness / 2.0
        )

        return center_mark_df


class FrontcourtHalf(BaseTennisFeature):
    """One half of the frontcourt (either ad or deuce court).

    The left-hand side of the court when facing the net from the nearest
    baseline is the ad court, and the right-hand side is the deuce court

    Attributes
    ----------
    singles_width : float
        The width of a singles court in the court's specified units

    serviceline_distance : float
        The distance from the net to the outer edge of the serviceline (the
        line in front of which a serve must land)
    """

    def __init__(self, singles_width = 0.0, serviceline_distance = 0.0, *args,
                 **kwargs):
        # Initialize the attributes unique to this feature
        self.singles_width = singles_width
        self.serviceline_distance = serviceline_distance
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the ad court.

        This feature is constrained by the singles sideline and the serviceline
        """
        frontcourt_half_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.serviceline_distance,
            y_min = -self.singles_width / 4.0,
            y_max = self.singles_width / 4.0
        )

        return frontcourt_half_df


class Backcourt(BaseTennisFeature):
    """The backcourt of the tennis court.

    This is the area behind the serviceline on the court, contained within the
    singles sidelines

    Attributes
    ----------
    singles_width : float
        The width of a singles court in the court's specified units

    serviceline_distance : float
        The distance from the net to the outer edge of the serviceline (the
        line in front of which a serve must land)
    """

    def __init__(self, singles_width = 0.0, serviceline_distance = 0.0, *args,
                 **kwargs):
        # Initialize the attributes unique to this feature
        self.singles_width = singles_width
        self.serviceline_distance = serviceline_distance
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the backcourt of the tennis court.

        This feature is constrained by the singles sideline and the serviceline
        """
        backcourt_df = self.create_rectangle(
            x_min = 0.0,
            x_max = (self.court_length / 2.0) - self.serviceline_distance,
            y_min = -self.singles_width / 2.0,
            y_max = self.singles_width / 2.0
        )

        return backcourt_df


class DoublesAlley(BaseTennisFeature):
    """The doubles alley on the tennis court.

    This is the area between the singles and doubles sideline. It should run
    the entire length of the court
    """

    def _get_centered_feature(self):
        doubles_alley_df = self.create_rectangle(
            x_min = -self.court_length / 2.0,
            x_max = self.court_length / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return doubles_alley_df


class CourtApron(BaseTennisFeature):
    """The boundary that surrounds the tennis court.

    This is the backstop and the sidestop

    Attributes
    ----------
    backstop_distance : float
        The distance from the back edge of the baseline to the barrier behind
        it in the court's specified units

    sidestop_distance : float
        The distance from the outer edge of the sideline to the barrier that
        runs parallel to it in the court's specified units
    """

    def __init__(self, backstop_distance = 0.0, sidestop_distance = 0.0, *args,
                 **kwargs):
        # Initialize the attributes unique to this feature
        self.backstop_distance = backstop_distance
        self.sidestop_distance = sidestop_distance
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the court apron.

        This is entirely outside of the playing court, but legal shots made
        here are considered in play
        """
        court_apron_df = pd.DataFrame({
            "x": [
                0.0,
                self.court_length / 2.0,
                self.court_length / 2.0,
                0.0,
                0.0,
                (self.court_length / 2.0) + self.backstop_distance,
                (self.court_length / 2.0) + self.backstop_distance,
                0.0,
                0.0
            ],

            "y": [
                self.court_width / 2.0,
                self.court_width / 2.0,
                -self.court_width / 2.0,
                -self.court_width / 2.0,
                -((self.court_width / 2.0) + self.sidestop_distance),
                -((self.court_width / 2.0) + self.sidestop_distance),
                (self.court_width / 2.0) + self.sidestop_distance,
                (self.court_width / 2.0) + self.sidestop_distance,
                self.court_width / 2.0
            ]
        })

        return court_apron_df


class Net(BaseTennisFeature):
    """The net on the tennis court.

    This divides the court into two halves

    Attributes
    ----------
    net_length : float
        The length of the net, from post to post, in the court's specified
        units
    """

    def __init__(self, net_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.net_length = net_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the net.

        This does not include the net posts
        """
        net_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.net_length / 2.0,
            y_max = self.net_length / 2.0
        )

        return net_df
