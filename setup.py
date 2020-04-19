"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# This call to setup() does all the work
setup(
    name="hangman",
    version="1.0.0",
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["Hangman"],
    include_package_data=True,
    install_requires=[
        "os", "random", "stdiomask"
    ],
    entry_points={"console_scripts": ["hangman=Hangman.__main__:driver"]},
)