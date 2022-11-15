#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()


setup(
    name="shyysh",
    author="Viktor Tereshchenko",
    version="0.0.2",
    url="https://github.com/m0nochr0me/shyysh",
    description="TUI SSH Connection manager",
    long_description=long_description,
    packages=find_packages("."),
    include_package_data=True,
    package_data={"shyysh": ["config.default.yaml"]},
    install_requires=[
        "tinydb>=4.7.0",
        "libtmux>=0.15.0",
        "asciimatics>=1.14.0",
        "PyYAML>=6.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": [
            "shyysh = shyysh.shyysh_main:main",
            "shyysh_manager = shyysh.shyysh_manager:main",
        ]
    }
)