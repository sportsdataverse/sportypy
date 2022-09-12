def autoset_font_size(ax, txt, xy, width, height, *, transform = None,
                      **kwargs):
    """Automatically set the size of text based on a specified height.

    This is useful when plotting the yardage marking numbers on a football
    field

    Parameters
    ----------
    ax : matplotlib.Axes
        An axes object to use to set the font size

    txt : str
        The string to use to set the font size

    xy : tuple
        The ``(x, y)`` coordinates where the text should be anchored. This
        should be passed as a tuple of floats

    width : float
        The width of the bounding box of the text in the units of the surface

    height : float
        The height of the bounding box of the text in the units of the surface

    transform : matplotlib.Transform, optional
        A transform to apply to the data

    Returns
    -------
    adjusted_size : float
        The adjusted font size
    """
    if transform is None:
        transform = ax.transData

    #  Different alignments give different bottom left and top right anchors.
    x, y = xy
    xa0, xa1 = (x - width / 2, x + width / 2)
    ya0, ya1 = (y - height / 2, y + height / 2)
    a0 = xa0, ya0
    a1 = xa1, ya1

    x0, y0 = transform.transform(a0)
    x1, y1 = transform.transform(a1)
    # rectangle region size to constrain the text in pixel
    rect_height = y1 - y0

    fig = ax.get_figure()
    dpi = fig.dpi
    rect_height_inch = rect_height / dpi
    # Initial fontsize according to the height of boxes
    fontsize = rect_height_inch / 72

    text = ax.annotate(
        txt,
        xy,
        ha = "center",
        va = "center",
        xycoords = transform,
        **kwargs
    )

    # Adjust the fontsize according to the box size.
    text.set_fontsize(fontsize)
    bbox = text.get_window_extent(fig.canvas.get_renderer())
    adjusted_size = (30 * fontsize) / bbox.width

    return adjusted_size
