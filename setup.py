#!/usr/bin/env python

import re
from setuptools import setup, find_namespace_packages

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("gtfs_aggregator_checker/__init__.py", "r") as f:
    version = _version_re.search(f.read()).group(1).strip("'\"")

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="gtfs_aggregator_checker",
    version=version,
    packages=find_namespace_packages(),
    install_requires=[
        "beautifulsoup4",
        "python-dotenv",
        "PyYAML",
        "requests",
        "typer",
    ],
    description="Tool for checking if transit urls are on aggregator websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="https://github.com/cal-itp/gtfs-aggregator-checker",
)
