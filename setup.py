import setuptools

setuptools.setup(
    name = "sportypy",
    version = "1.0.0",
    description = "Draw sports surfaces according to rulebook specifications",
    long_description = open("README.md").read(),
    url = "https://github.com/sportsdataverse/sportypy",
    author = "Ross Drucker",
    author_email = "ross.a.drucker@gmail.com",
    license = "GPL 3.0",
    packages = setuptools.find_packages(),
    install_requires = [],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
