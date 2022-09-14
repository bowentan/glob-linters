#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [""]  # TODO: add requirements

test_requirements = [
    "pytest>=3",
]

setup(
    author="Bowen Tan",
    author_email="bowentan78@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",  # TODO: modify this
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="GitHub action for multi-language linters",
    entry_points={
        "console_scripts": [
            "glob_linters=glob_linters.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="glob_linters",
    name="glob_linters",
    packages=find_packages(include=["glob_linters", "glob_linters.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/bowentan/glob_linters",
    version="0.1.0",
    zip_safe=False,
)
