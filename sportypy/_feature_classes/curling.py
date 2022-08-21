import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseCurlingFeature(BaseFeature):
    """An extension of the BaseFeature class specifically for curling features.

    The following attributes are specific to curling features only. For more
    information on inherited attributes, please see the BaseFeature class
    definition. The default values are provided to ensure that the feature can
    at least be created.

    Attributes
    ----------
    sheet_length : float (default: 0.0)
        The length of the sheet in TV view

    sheet_width : float (default: 0.0)
        The width of the sheet in TV view

    feature_radius : float (default: 0.0)
        The radius needed to draw the feature. This may not be needed for all
        features

    feature_thickness : float (default: 0.0)
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed
    """

    def __init__(self, sheet_length = 0.0, sheet_width = 0.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = "ft", *args, **kwargs):

        # Set the full-sized dimensions of the sheet
        self.sheet_length = sheet_length
        self.sheet_width = sheet_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class Boundary(BaseCurlingFeature):
    """The constraint around the interior edge of the sheet's boundary lines.

    This confines all interior features to be constrained inside the sheet, as
    well as any interior plots.
    """

    def _get_centered_feature(self):
        """Generate the points comprising the inner boundary of the sheet.

        This is done to constrain any features from extending needlessly beyond
        the edge of the sheet. Lines are considered out, so this should only
        trace the interior
        """
        # Define the length and width of the sheet as length and width
        # attributes. These will be used to constrain plotted points to be
        # defined inside the surface
        self.length = self.sheet_length
        self.width = self.sheet_width

        sheet_constraint_df = self.create_rectangle(
            x_min = -self.sheet_width / 2.0,
            x_max = self.sheet_width / 2.0,
            y_min = -self.sheet_length / 2.0,
            y_max = self.sheet_length / 2.0
        )

        return sheet_constraint_df


class End(BaseCurlingFeature):
    """A parameterization of an end of the curling sheet.

    The end is the area between the center-side edge of the hog line and the
    back board behind the nearest house
    """

    def __init__(self, tee_line_to_center = 0.0, hog_line_to_tee_line = 0.0,
                 drawn_direction = "upward", *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.tee_line_to_center = tee_line_to_center
        self.hog_line_to_tee_line = hog_line_to_tee_line
        self.drawn_direction = drawn_direction
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the coordinates of the end's boundary.

        The end is defined by the interior edges of the sheet's boundaries
        """
        # Define the length of each end
        end_length = (
            (self.sheet_length / 2.0) -
            self.tee_line_to_center +
            self.hog_line_to_tee_line
        )

        if self.drawn_direction.lower() == "upward":
            end_df = self.create_rectangle(
                x_min = -self.sheet_width / 2.0,
                x_max = self.sheet_width / 2.0,
                y_min = 0.0,
                y_max = end_length
            )
        else:
            end_df = self.create_rectangle(
                x_min = -self.sheet_width / 2.0,
                x_max = self.sheet_width / 2.0,
                y_min = -end_length,
                y_max = 0.0
            )

        return end_df


class CentreZone(BaseCurlingFeature):
    """A parameterization of the centre zone of the curling sheet.

    This is the area located between the hog lines
    """

    def __init__(self, tee_line_to_center = 0.0, hog_line_to_tee_line = 0.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.tee_line_to_center = tee_line_to_center
        self.hog_line_to_tee_line = hog_line_to_tee_line
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the coordinates that define the centre zone.

        The interior edges of the hog lines should be used to define this
        """
        # Define the half-length of the centre zone
        half_centre_zone_length = (
            self.tee_line_to_center - self.hog_line_to_tee_line
        )

        centre_zone_df = self.create_rectangle(
            x_min = -self.sheet_width / 2.0,
            x_max = self.sheet_width / 2.0,
            y_min = -half_centre_zone_length,
            y_max = half_centre_zone_length
        )

        return centre_zone_df


class SheetApron(BaseCurlingFeature):
    """A parameterization of the boundary of the sheet.

    This feature may be negligible in thickness, but it does help provide more
    definition to the sheet itself
    """

    def __init__(self, apron_behind_back = 0.0, apron_along_side = 0.0, *args,
                 **kwargs):
        # Initialize the attributes unique to this feature
        self.apron_behind_back = apron_behind_back
        self.apron_along_side = apron_along_side
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the coordinates that define the sheet's apron.

        The interior edges of the sheet are to be used as its minimal
        coordinates
        """
        sheet_apron_df = pd.DataFrame({
            "x": [
                0.0,
                self.sheet_width / 2.0,
                self.sheet_width / 2.0,
                (self.sheet_width / 2.0) + self.apron_along_side,
                (self.sheet_width / 2.0) + self.apron_along_side,
                -(self.sheet_width / 2.0) - self.apron_along_side,
                -(self.sheet_width / 2.0) - self.apron_along_side,
                -self.sheet_width / 2.0,
                -self.sheet_width / 2.0,
                0.0
            ],

            "y": [
                self.sheet_length / 2.0,
                self.sheet_length / 2.0,
                0.0,
                0.0,
                (self.sheet_length / 2.0) + self.apron_behind_back,
                (self.sheet_length / 2.0) + self.apron_behind_back,
                0.0,
                0.0,
                self.sheet_length / 2.0,
                self.sheet_length / 2.0
            ]
        })

        return sheet_apron_df


class CentreLine(BaseCurlingFeature):
    """A parameterization of the centre line.

    This is the line that runs the full length (from hack to hack) on the sheet
    """

    def __init__(self, tee_line_to_center = 0.0, centre_line_extension = 0.0,
                 *args, **kwargs):
        # Define the attributes that are unique to this feature
        self.tee_line_to_center = tee_line_to_center
        self.centre_line_extension = centre_line_extension
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the centre line.

        The centre line is typically black in color
        """
        centre_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.tee_line_to_center - self.centre_line_extension,
            y_max = self.tee_line_to_center + self.centre_line_extension
        )

        return centre_line_df


class TeeLine(BaseCurlingFeature):
    """A parameterization of the tee line.

    This is the line that runs through the center of the house, from side wall
    to side wall
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the tee line.

        The tee line is typically black in color
        """
        tee_line_df = self.create_rectangle(
            x_min = -self.sheet_width / 2.0,
            x_max = self.sheet_width / 2.0,
            y_min = -self.feature_thickness / 2.0,
            y_max = self.feature_thickness / 2.0
        )

        return tee_line_df


class BackLine(BaseCurlingFeature):
    """A parameterization of the back line.

    This is the line that runs through the back of the house, from side wall to
    side wall
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the back line.

        The back line is typically black in color
        """
        back_line_df = self.create_rectangle(
            x_min = -self.sheet_width / 2.0,
            x_max = self.sheet_width / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return back_line_df


class HogLine(BaseCurlingFeature):
    """A parameterization of the hog line.

    This is the line at the start of each end of the ice
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the hog line.

        The hog line is typically red in color
        """
        hog_line_df = self.create_rectangle(
            x_min = -self.sheet_width / 2.0,
            x_max = self.sheet_width / 2.0,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return hog_line_df


class HackLine(BaseCurlingFeature):
    """A parameterization of the hack line.

    This is the line that runs between each foothold in the hack
    """

    def __init__(self, hack_width = 0.0, *args, **kwargs):
        # Define the attributes that are unique to this feature
        self.hack_width = hack_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the hack line.

        The hack line is typically black in color
        """
        hack_line_df = self.create_rectangle(
            x_min = -self.hack_width / 2.0,
            x_max = self.hack_width / 2.0,
            y_min = -self.feature_thickness,
            y_max = 0.0
        )

        return hack_line_df


class CourtesyLine(BaseCurlingFeature):
    """A parameterization of the courtesy line.

    These lines are where players stand during the delivery process of each
    stone when the opposing team is throwing
    """

    def __init__(self, courtesy_line_length = 0.0, *args, **kwargs):
        # Define the attributes that are unique to this feature
        self.courtesy_line_length = courtesy_line_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the courtesy line.

        The courtesy line is typically black in color
        """
        courtesy_line_df = self.create_rectangle(
            x_min = -self.courtesy_line_length,
            x_max = 0.0,
            y_min = -self.feature_thickness,
            y_max = 0.0
        )

        return courtesy_line_df


class HackFoothold(BaseCurlingFeature):
    """A parameterization of a single foothold in the hack.

    There are two footholds in each hack. This feature only plots one of the
    footholds
    """

    def __init__(self, foothold_depth = 0.0, foothold_width = 0.0, *args,
                 **kwargs):
        # Define the attributes unique to this feature
        self.foothold_depth = foothold_depth
        self.foothold_width = foothold_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of a hack foothold.

        These are usually black in color
        """
        foothold_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.foothold_width,
            y_min = -self.foothold_depth,
            y_max = 0.0
        )

        return foothold_df


class Button(BaseCurlingFeature):
    """A parameterization of the button in each house on the curling sheet.

    The button is the center ring of the house, with its center located at the
    intersection of the tee line and centre line
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of the button.

        The button is a circle with no thickness
        """
        button_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return button_df


class HouseRing(BaseCurlingFeature):
    """A parameterization of a single ring in the house.

    The rings are concentric, centered at the intersection of the tee line and
    centre line
    """

    def _get_centered_feature(self):
        """Generate the points that comprise the boundary of a house ring.

        Because the rings are concentric, with each ring having no border
        against the next, these rings are created as full circles rather than
        as half circles with a thickness
        """
        ring_df = self.create_circle(
            center = (0.0, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return ring_df
