---
sidebar_position: 1
slug: /
---

# sportypy

`sportypy` draws regulation, to-scale playing surfaces with matplotlib, so
tracking and play-by-play data can be plotted on the field, court, rink or
sheet it came from. It covers baseball, basketball, curling, football, hockey,
lacrosse, soccer, softball, tennis and volleyball, with a class for each
league's rule-book dimensions.

It is the Python counterpart of [`sportyR`](https://github.com/sportsdataverse/sportyR)
and keeps parity with it: the same leagues, dimensions, colours and display
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

## Where to next

- [Getting started](./getting-started.md): draw a surface, choose a display
  range and units, and plot data on it.
- [Surfaces](/category/surfaces): every sport's base class, its league classes
  and their methods.
- [Plotting and display](./reference/plotting.md): the plotting helpers
  (`scatter`, `heatmap`, `contour`, `hexbin`, `arrow`, ...) every surface has.
- [Changelog](./changelog.md).
