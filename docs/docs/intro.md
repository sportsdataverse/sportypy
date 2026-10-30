---
sidebar_position: 1
sidebar_label: Introduction
description: "sportypy draws regulation, to-scale playing surfaces for ten sports with matplotlib, so tracking and play-by-play data can be plotted on the field, court, rink or sheet it came from."
---

# sportypy

`sportypy` draws regulation, to-scale playing surfaces with matplotlib, so
tracking and play-by-play data can be plotted on the field, court, rink or
sheet it came from. It covers baseball, basketball, curling, football, hockey,
lacrosse, soccer, softball, tennis and volleyball, with a class for each
league's rule-book dimensions.

It is the Python counterpart of [`sportyR`](https://sportyR.sportsdataverse.org)
and keeps parity with it: the same leagues, dimensions, colors and display
ranges. For JavaScript and TypeScript, [`@sportsdataverse/sporty`](https://www.npmjs.com/package/@sportsdataverse/sporty)
is the port of both.

## Installation

`sportypy` supports Python 3.10 and newer.

```bash
pip install sportypy
```

or, in a [`uv`](https://docs.astral.sh/uv/) project,

```bash
uv add sportypy
```

## Draw a surface

```python
import matplotlib.pyplot as plt
from sportypy.surfaces.hockey import NHLRink

NHLRink().draw()
plt.show()
```

## Where to next

- [Getting started](./getting-started.md): display ranges, units, rotation,
  colors, and plotting data on a surface.
- [API reference](./reference/index.md): every sport's base class, its league
  classes and their methods, generated from the docstrings.
- [Plotting and display](./reference/plotting.md): the plotting helpers
  (`scatter`, `heatmap`, `contour`, `hexbin`, `arrow`, ...) every surface has.
- [News](pathname:///CHANGELOG): what changed in each release.
