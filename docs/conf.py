# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import re
import sys
from importlib.metadata import PackageNotFoundError, version as package_version
import sphinx_bootstrap_theme
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "sportypy")))

project = "sportypy"
# Read the version from the installed package so it matches pyproject.toml;
# a source checkout without sportypy installed reads pyproject.toml itself
try:
    version = package_version("sportypy")
except PackageNotFoundError:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pyproject.toml"), encoding="utf-8") as f:
        version = re.search(r'^version = "([^"]+)"', f.read(), re.M).group(1)
copyright = "2022, Ross Drucker"
author = "Ross Drucker"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "tests/",
    "setup.py"
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_static_path = ["_static"]
html_css_files = ["sportypy.css"]
# Plausible analytics: site-specific script plus its init stub
html_js_files = [
    ("https://plausible.io/js/pa-lI8N5cCc-JaTGLO7Mhsgb.js", {"async": "async"}),
    (None, {"body": "window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};plausible.init()"}),
]
html_permalinks_icon = "#"
html_theme_options = {
    "bootswatch_theme": "cosmo"
}

auto_module_names = False

# (Optional) Logo. Should be small enough to fit the navbar (ideally 24x24).
# Path should be relative to the ``_static`` files directory.
html_logo = os.path.join("..", "logos", "sportypy-logo-1500.png")
html_favicon = os.path.join("..", "logos", "sportypy-logo-32.png")
