# Security policy

## Supported versions

Security fixes go into the latest release of `sportypy` on PyPI.

## Reporting a vulnerability

Please report a vulnerability privately through a
[GitHub security advisory](https://github.com/sportsdataverse/sportypy/security/advisories/new),
not a public issue. Include what is affected, how to reproduce it and the
impact you expect. You should hear back within a week.

`sportypy` reads only its bundled JSON data and makes no network requests, so
most reports will concern a dependency (matplotlib, numpy, pandas, scipy) or
the release workflow; those are welcome too.
