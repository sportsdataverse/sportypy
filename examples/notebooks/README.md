# Cookbooks

Worked analyses with sportypy on real data, loaded with
[sportsdataverse-py](https://py.sportsdataverse.org) and colored with
[sdvplot](https://sdvplot.sportsdataverse.org). Each notebook is committed with
the outputs of its last run, and the docs site turns it into a page under
[Cookbooks](https://sportypy.sportsdataverse.org/docs/cookbooks) on every build
(`tools/gen_docs.py`), so the page shows exactly what the notebook printed and
drew.

To change one, edit it, then run it top to bottom in a fresh kernel and commit
it with its outputs (the site build fails on a notebook that was not):

```bash
uv run --group cookbook jupyter nbconvert --to notebook --execute --inplace examples/notebooks/nba-shot-quality.ipynb
```

Or open it with `uv run --group cookbook jupyter lab`, restart the kernel and
run all cells. A notebook's `metadata.sportypy` holds its sidebar `label`,
`position` and `description`; tag a figure's cell `gallery` to put that figure
on the cookbooks overview and the homepage.
