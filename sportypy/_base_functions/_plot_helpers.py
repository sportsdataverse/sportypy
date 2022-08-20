from typing import Optional, Literal

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.text import Annotation
from matplotlib.transforms import Transform, Bbox


def text_with_autofit(
    ax: plt.Axes,
    txt: str,
    xy: tuple[float, float],
    width: float, height: float,
    *,
    transform: Optional[Transform] = None,
    ha: Literal['left', 'center', 'right'] = 'center',
    va: Literal['bottom', 'center', 'top'] = 'center',
    show_rect: bool = False,
    **kwargs,
):
    if transform is None:
        transform = ax.transData

    #  Different alignments give different bottom left and top right anchors.
    x, y = xy
    xa0, xa1 = {
        'center': (x - width / 2, x + width / 2),
        'left': (x, x + width),
        'right': (x - width, x),
    }[ha]
    ya0, ya1 = {
        'center': (y - height / 2, y + height / 2),
        'bottom': (y, y + height),
        'top': (y - height, y),
    }[va]
    a0 = xa0, ya0
    a1 = xa1, ya1

    x0, y0 = transform.transform(a0)
    x1, y1 = transform.transform(a1)
    # rectangle region size to constrain the text in pixel
    rect_width = x1 - x0
    rect_height = y1 - y0

    fig: plt.Figure = ax.get_figure()
    dpi = fig.dpi
    rect_height_inch = rect_height / dpi
    # Initial fontsize according to the height of boxes
    fontsize = rect_height_inch / 72

    text: Annotation = ax.annotate(
        txt,
        xy,
        ha=ha,
        va=va,
        xycoords=transform,
        **kwargs
    )

    # Adjust the fontsize according to the box size.
    text.set_fontsize(fontsize)
    bbox: Bbox = text.get_window_extent(fig.canvas.get_renderer())
    adjusted_size = (30 * fontsize) / bbox.width
    text.set_fontsize(adjusted_size)

    return text