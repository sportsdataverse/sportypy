"""Extensions of the BaseFeature class to be specific to volleyball courts.

The features are all parameterized by the basic characteristics of a volleyball
court. A user can manually specify their own court parameters in the
``VolleyballCourt`` class that will adjust the placement of these features,
however the features themselves will be consistent across all volleyball
surfaces.

@author: Ross Drucker
"""
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseVolleyballFeature(BaseFeature):
    """An extension of the ``BaseFeature`` class for volleyball features.

    The following attributes are specific to volleyball features only. For more
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


class CourtConstraint(BaseVolleyballFeature):
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


class FreeZone(BaseVolleyballFeature):
    """The free zone of a volleyball court.

    This is similar to the court apron of a basketball court in that it is the
    area outside of the court. It may be the same color as the interior of the
    court, but isn't necessarily. Unlike a basketball court's apron, however,
    the boundary line thickness doesn't matter since the lines are considered
    in-play and therefore are included in the court's length and width.

    Attributes
    ----------
    free_zone_end_line : float
        The distance the free zone extends beyond the outer edge of the end
        line

    free_zone_sideline : float
        The distance the free zone extends beyond the outer edge of the
        sideline
    """
    def __init__(self, free_zone_end_line = 0.0, free_zone_sideline = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.free_zone_end_line = free_zone_end_line
        self.free_zone_sideline = free_zone_sideline
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the free zone.

        This is not the same as the court apron of the volleyball court, as
        this is the entire area outside of the court's lines, while the court
        apron corresponds to a colored apron inside the free zone.
        """
        free_zone_df = pd.DataFrame({
            "x": [
                0.0,
                self.court_length / 2.0,
                self.court_length / 2.0,
                0.0,
                0.0,
                (self.court_length / 2.0) + self.free_zone_end_line,
                (self.court_length / 2.0) + self.free_zone_end_line,
                0.0,
                0.0
            ],

            "y": [
                self.court_width / 2.0,
                self.court_width / 2.0,
                -self.court_width / 2.0,
                -self.court_width / 2.0,
                (-self.court_width / 2.0) - self.free_zone_sideline,
                (-self.court_width / 2.0) - self.free_zone_sideline,
                (self.court_width / 2.0) + self.free_zone_sideline,
                (self.court_width / 2.0) + self.free_zone_sideline,
                self.court_width / 2.0
            ]
        })

        return free_zone_df


class FrontZone(BaseVolleyballFeature):
    """The front zone of a volleyball court.

    The front zone is the area between the attack line and the line running
    along ``x = 0``. If considering the entirety of the volleyball court as
    being divided into thirds, this is _half_ of the middle third of the court

    Attributes
    ----------
    attack_line_edge_to_center_line : float
        The distance from the edge furthest from the attack line to the center
        of the line running along ``x = 0``
    """
    def __init__(self, attack_line_edge_to_center_line = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.attack_line_edge_to_center_line = attack_line_edge_to_center_line
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the bounding box of the front zone.

        The front zone is the center \"third\" of the court.
        """
        front_zone_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.attack_line_edge_to_center_line,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return front_zone_df


class Backcourt(BaseVolleyballFeature):
    """The backcourt area of the volleyball court.

    This is the area between the attack line and the end line. Players playing
    in the back row of the rotation must take off from this area before
    attacking the ball

    Attributes
    ----------
    attack_line_edge_to_center_line : float
        The distance from the edge furthest from the attack line to the center
        of the line running along ``x = 0``
    """
    def __init__(self, attack_line_edge_to_center_line = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.attack_line_edge_to_center_line = attack_line_edge_to_center_line
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the backcourt.

        If considering the entirety of the volleyball court as
        being divided into thirds, this is _either_ of the otuer thirds of the
        court
        """
        backcourt_length = (
            (self.court_length / 2.0) -
            self.attack_line_edge_to_center_line
        )

        backcourt_df = self.create_rectangle(
            x_min = -backcourt_length / 2.0,
            x_max = backcourt_length / 2.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return backcourt_df


class CourtApron(BaseVolleyballFeature):
    """The apron of the volleyball court.

    The court apron is similar to the court apron of a basketball court in that
    it is the area outside of the court, but this is different than the
    ``FreeZone`` as it is fully contained within the free zone.

    Attributes
    ----------
    court_apron_end_line : float
        The distance the free zone extends beyond the outer edge of the end
        line

    court_apron_sideline : float
        The distance the free zone extends beyond the outer edge of the
        sideline
    """
    def __init__(self, court_apron_end_line = 0.0, court_apron_sideline = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.court_apron_end_line = court_apron_end_line
        self.court_apron_sideline = court_apron_sideline
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising the court apron.

        This is not the same as the free zone of the volleyball court, as this
        is the entire area outside of the court's lines, while the court apron
        corresponds to a colored apron inside the free zone.
        """
        court_apron_df = pd.DataFrame({
            "x": [
                0.0,
                self.court_length / 2.0,
                self.court_length / 2.0,
                0.0,
                0.0,
                (self.court_length / 2.0) + self.court_apron_end_line,
                (self.court_length / 2.0) + self.court_apron_end_line,
                0.0,
                0.0
            ],

            "y": [
                self.court_width / 2.0,
                self.court_width / 2.0,
                -self.court_width / 2.0,
                -self.court_width / 2.0,
                (-self.court_width / 2.0) - self.court_apron_sideline,
                (-self.court_width / 2.0) - self.court_apron_sideline,
                (self.court_width / 2.0) + self.court_apron_sideline,
                (self.court_width / 2.0) + self.court_apron_sideline,
                self.court_width / 2.0
            ]
        })

        return court_apron_df


class EndLine(BaseVolleyballFeature):
    """The end lines.

    These are the lines that run the full width of the court, and their entire
    thickness is considered in bounds during play
    """

    def _get_centered_feature(self):
        """Generate the points comprising the bounding box of the end line.

        The end line's thickness is fully contained inside the court's in-bound
        area
        """
        end_line_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return end_line_df


class Sideline(BaseVolleyballFeature):
    """The sidelines.

    These are the lines that run the full length of the court, and their entire
    thickness is considered in bounds during play
    """

    def _get_centered_feature(self):
        """Generate the points comprising the bounding box of the sideline.

        The sideline's thickness is fully contained inside the court's in-bound
        area
        """
        sideline_df = self.create_rectangle(
            x_min = -self.court_length / 2.0,
            x_max = self.court_length / 2.0,
            y_min = -self.feature_thickness,
            y_max = 0.0
        )

        return sideline_df


class AttackLine(BaseVolleyballFeature):
    """The attack line.

    This is the line that runs from sideline to sideline, separating the
    backcourt from the front zone. Players in the front row may attack from
    either side of this line, while players in the back row must begin their
    attack from the backcourt side of this line. The anchor point of this
    feature should be its outer edge
    """

    def _get_centered_feature(self):
        """Generate the points comprising the attack line.

        This is a solid line. The dashed component that extends this line will
        be handled by the ``SubstitutionZone`` class
        """
        attack_line_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return attack_line_df


class CenterLine(BaseVolleyballFeature):
    """The center line.

    This line runs along the line ``x = 0`` when viewing the court in TV view,
    dividing the court into two equal halves
    """

    def _get_centered_feature(self):
        """Generate the points comprising the center line.

        The center line is a solid line
        """
        center_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.court_width / 2.0,
            y_max = self.court_width / 2.0
        )

        return center_line_df


class ServiceZoneMark(BaseVolleyballFeature):
    """A single service zone mark.

    These marks lie beyond the end lines and denote where a legal serve must
    take place. It appears as a hash mark that is out of bounds of the court,
    but contained within the free zone

    Attributes
    ----------
    service_zone_mark_length : float
        The length of the service zone mark
    """

    def __init__(self, service_zone_mark_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.service_zone_mark_length = service_zone_mark_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising a single service zone mark.

        Use ``reflect_x`` and ``reflect_y`` when instantiating this feature to
        generate all four marks
        """
        service_zone_mark_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.service_zone_mark_length,
            y_min = -self.feature_thickness,
            y_max = 0.0
        )

        return service_zone_mark_df


class SubstitutionZoneDash(BaseVolleyballFeature):
    """A single dash of the substitution zone.

    The substitution zone is typically marked by a dashed line extending from
    the attack lines. This creates a single dash, and the dashes should be
    added to the plot accordingly

    Attributes
    ----------
    dash_length : float
        The length of a single dash of the service line
    """

    def __init__(self, dash_length = 0.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.dash_length = dash_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points comprising a single substitution zone dash.

        The dashes should be iteratively created in the ``VolleyballCourt``
        class
        """
        substitution_zone_dash_df = self.create_rectangle(
            x_min = -self.feature_thickness,
            x_max = 0.0,
            y_min = 0.0,
            y_max = self.dash_length
        )

        return substitution_zone_dash_df
