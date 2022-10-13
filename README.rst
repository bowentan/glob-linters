============
glob-linters
============


.. image:: https://img.shields.io/pypi/v/glob_linters.svg
        :target: https://pypi.python.org/pypi/glob_linters

.. image:: https://readthedocs.org/projects/glob-linters/badge/?version=latest
        :target: https://glob-linters.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://github.com/bowentan/glob-linters/actions/workflows/build-publish.yml/badge.svg
        :target: https://github.com/bowentan/glob-linters/actions/workflows/build-publish.yml
        :alt: Build and publish


glob-linters is an integtated tool to lint multiple programming and scripting languages
and can be used as a normal command line in terminals as well as a workflow in GtiHub
actions.


* Free software: MIT license
* Documentation: https://glob-linters.readthedocs.io/.


Features
--------

* Linting multiple languages.
* Fully supporting configuration for each linter via configuration files or command
  options

Supported linters
~~~~~~~~~~~~~~~~~

+----------+----------------+------------------------------------+
| Language | File extension | Linters                            |
+----------+----------------+------------------------------------+
| c++      | .cpp           | cpplint, clang-format              |
+----------+----------------+------------------------------------+
| Python   | .py            | pylint, black, flake8, isort, mypy |
+----------+----------------+------------------------------------+

Quick start
-----------

You can use glob-linters as a command line tool in a terminal or a workflow in GitHub
action. Choose the appropriate one as a quick start.

Command line
~~~~~~~~~~~~

To use as a command line tool, install the latest package by ``pip`` using the
following command:

.. code-block:: console

        $ pip install glob-linters

After successful installation, you can use glob-linters as a command tool by issuing the
following to see the command line options.

.. code-block:: console

        $ glob_linters -h

Then run :code:`glob_linters` to lint all supported languages in the *current directory*,
which will scan all corresponding files recursively and then perform linting. If you
want to lint particular files, please visit the documentation for more advanced usages.

GitHub action
~~~~~~~~~~~~~

To use glob-linters in GitHub action, create a workflow file such as
``.github/workflows/glob-linters.yml`` in your own repository with the example
contents:

.. code-block:: yaml

        name: Code linting

        on:
          push:
            branches: ["main"]
          pull_request:
            branches: ["main"]

        jobs:
          glob-linters:
            runs-on: ubuntu-latest
            steps:
              - name: Checkout code
                uses: actions/checkout@v3
                with:
                  fetch-depth: 0

              - name: Linting
                uses: bowentan/glob-linters@v0
                env:
                  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

You can control the workflow by creating a configuration file named as
``.github/glob-linters.ini`` and a sample configuration is given below:

.. code-block:: ini

        [target]
        target_dir = .
        target_suffix = .py

        [executable]
        cpplint = cpplint
        clang_format = clang-format
        pylint = pylint
        flake8 = flake8
        black = black
        isort = isort

        [env]
        debug = True

This configuration will enable ``debug`` mode with additional information when running
and set the directory that will be searched for linting ``.py`` files to be the
root of your repository.

For more details about usage, please refer to the documentation.

Contributing
------------

If you are interested in this project and would like to make some contributions, please
refer to the contributing_ for the contributing guide.

.. _contributing: https://github.com/bowentan/glob-linters/blob/main/CONTRIBUTING.rst

Credits
-------

This package was created with Cookiecutter_ and
the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
