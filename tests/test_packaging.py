"""The Python versions sportypy claims agree with what CI tests."""

import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
SUPPORTED = ["3.10", "3.11", "3.12", "3.13", "3.14"]


def test_classifiers_list_the_supported_versions():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    listed = re.findall(r'"Programming Language :: Python :: (3\.\d+)"', pyproject)
    assert listed == SUPPORTED
    assert f'requires-python = ">={SUPPORTED[0]}"' in pyproject


def test_ci_tests_the_oldest_and_newest_versions():
    workflow = (ROOT / ".github/workflows/package-coverage.yml").read_text(
        encoding="utf-8"
    )
    matrix = re.search(r"python-version: \[([^\]]*)\]", workflow)
    assert matrix is not None
    versions = re.findall(r"'(3\.\d+)'", matrix.group(1))
    assert versions == [SUPPORTED[0], SUPPORTED[-1]]
