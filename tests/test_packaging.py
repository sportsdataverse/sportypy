"""The Python versions sportypy claims agree with what CI tests."""

import configparser
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
SUPPORTED = ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]


def test_classifiers_list_the_supported_versions():
    setup = (ROOT / "setup.py").read_text(encoding="utf-8")
    listed = re.findall(r'"Programming Language :: Python :: (3\.\d+)"', setup)
    assert listed == SUPPORTED
    assert 'python_requires = ">=3.9"' in setup


def test_tox_envlist_matches_the_classifiers():
    tox = configparser.ConfigParser()
    tox.read(ROOT / "tox.ini", encoding="utf-8")
    envs = [e.strip() for e in tox["tox"]["envlist"].split(",")]
    assert envs == ["py" + v.replace(".", "") for v in SUPPORTED]


def test_ci_tests_the_oldest_and_newest_versions():
    workflow = (ROOT / ".github/workflows/package-coverage.yml").read_text(
        encoding="utf-8"
    )
    matrix = re.search(r"python-version: \[([^\]]*)\]", workflow)
    assert matrix is not None
    versions = re.findall(r"'(3\.\d+)'", matrix.group(1))
    assert versions == [SUPPORTED[0], SUPPORTED[-1]]
