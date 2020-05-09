#! /usr/bin/env python3

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    return open(os.path.join(here, fname)).read()


with open(os.path.join(here, "yaqd_newport", "VERSION")) as version_file:
    version = version_file.read().strip()

extra_files = {"yaqd_newport": ["VERSION"]}

setup(
    name="yaqd-newport",
    packages=find_packages(exclude=("tests", "tests.*")),
    package_data=extra_files,
    python_requires=">=3.7",
    install_requires=["yaqd-core[aserial]"],
    extras_require={"dev": ["black", "pre-commit", "pydocstyle"],},
    version=version,
    description="yaq daemons for Newport hardware",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="yaq Developers",
    license="LGPL v3",
    url="http://gitlab.com/yaq/yaqd-newport",
    project_urls={
        "Source": "https://gitlab.com/yaq/yaqd-newport",
        "Issue Tracker": "https://gitlab.com/yaq/yaqd-newport/issues",
    },
    entry_points={
        "console_scripts": [
            "yaqd-newport-smc100=yaqd_newport._newport_smc100:NewportSMC100.main",
            "yaqd-newport-conex-agp=yaqd_newport._newport_conex_agp:NewportConexAGP.main",
        ]
    },
    keywords="spectroscopy science multidimensional hardware",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
)
