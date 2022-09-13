import setuptools

setuptools.setup(
    name = "sportypy",
    version = "1.0.0",
    description = "Draw sports surfaces according to rulebook specifications",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/sportsdataverse/sportypy",
    project_urls = {
        "Source": "https://github.com/sportsdataverse/sportypy",
        "Docs": "https://sportypy.sportsdataverse.org/",
        "Bug Tracker": "https://github.com/sportsdataverse/sportypy/issues",
    },
    author = "Ross Drucker",
    author_email = "ross.a.drucker@gmail.com",
    maintainer = "Ross Drucker",
    license = "GPL 3.0",
    packages = setuptools.find_packages(exclude = ["tests", "tests.*"]),
    install_requires = [
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
    ],
    extras_require = {
        "test": [
            "flake8",
            "pytest",
            "pydocstyle",
            "pycodestyle",
        ],
        "docs": [
            "sphinx",
            "livereload",
            "myst-parser",
            "sphinx-markdown-builder",
            "sphinx-bootstrap-theme",
        ]
    },
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data = True,
    package_data = {
        "sportypy.data": ["*.json"]
    }
)
