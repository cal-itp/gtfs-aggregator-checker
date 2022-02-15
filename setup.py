#!/usr/bin/env python

import re
from pathlib import Path
import pkg_resources
from setuptools import setup, find_namespace_packages

_version_re = re.compile(r"__version__\s+=\s+(.*)")


with open("feed_checker/__init__.py", "r") as f:
    version = _version_re.search(f.read()).group(1).strip("'\"")

with Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]


long_description = Path("README.md").read_text()

setup(
    name="calitp_feed_checker",
    version=version,
    packages=find_namespace_packages(),
    install_requires=install_requires,
    description="Tool for checking if transit urls are on aggregator websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="https://github.com/cal-itp/feed_checker",
)
