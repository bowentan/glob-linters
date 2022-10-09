=====
Usage
=====

When using glob-linters as a command line tool, you can use both command line options
and configuration file to control the parameters for linting.

Command options
---------------

.. note::
        The command line options will be overwritten by
        :ref:`configuration file <configuration-file>` . All given
        arguments will ignored if you use configuration file.

You can use :program:`glob_linters` as a command line tool if you want to lint your
codes or test your GitHub action workflow in local terminals.

.. program:: glob_linters

.. option:: -d [TARGET_DIR], --target-dir [TARGET_DIR]

        Specify the directory to be scanned for files to be linted.

        Default: :file:`.`, the current working directory when :program:`glob_linters` is
        called.

        Keyword in configuration file: :code:`target_dir`.

.. option:: -s [TARGET_SUFFIX ...], --file-suffix [TARGET_SUFFIX ...]

        Extensions of files to be linted, e.g., :file:`.cpp`, :file:`.py`, and can be
        given more than one, separated by comma or space. For example,
        :samp:`--file-suffix .cpp .py`

        Default: all supported language extensions.

        Keyword in configuration file: :code:`target_suffix`.

.. option:: -g, --enable-debug

        Enable debug mode. Debugging information will be outputed.

        Default: disabled.

        Keyword in configuration file: :code:`debug`.

.. option:: -c [CONFIGS ...], --configs [CONFIGS ...]

        Set configuration, use ``key=value`` format and separate multiple pairs by
        comma or space.

        Default: :code:`None`, i.e., use default values for all settings.

        Keyword in configuration file: different key for different setting variables.
        See :ref:`executable settings <excutable-config>`.

.. option:: -C [CONFIG_FILE], --config-file [CONFIG_FILE]

        :program:`glob_linters` configuration file (:file:`glob-linters.ini`) path.

        Default: :file:`.github/glob-linters.ini`.

        No keyword for this in configuration file.

Examples
~~~~~~~~

By issuing :program:`glob_linters` in a directory like following:

.. code-block:: console

        $ glob_linters

without any options, :program:`glob_linters` will recursively scan the
directory to find files with all supported extensions using all default linters.

To change the target directory to :file:`src/` and only lint :file:`.py` files,
add options:

.. code-block:: console

        $ glob_linters --target-dir src --target-suffix .py

and if you also want to diasble :code:`flake8` and :code:`mypy` linters with debugging
information, do this:

.. code-block:: console

        $ glob_linters --target-dir src --target-suffix .py --configs .py.disable_linters=flake8,mypy


.. _configuration-file:

Configuration file
------------------

The configuration file format follows configparse_ structure. The configuration file
is generally used in GitHub actions. You can also use it to test your workflow in
local terminals.

.. _configparse: https://docs.python.org/3/library/configparser.html

:code:`[target]`
~~~~~~~~~~~~~~~~

:code:`target_dir = <TARGET_DIR>`
        Work as the same with :option:`glob_linters --target-dir`.

:code:`target_suffix = <TARGET_SUFFIX ...>`
        Work as the same with :option:`glob_linters --file-suffix`.


.. _excutable-config:

:code:`[excutable]`
~~~~~~~~~~~~~~~~~~~

.. note::
        The configuration file for each linter will overwrite the corresponding
        :code:`.options`.

:code:`cpplint = <exec>`
        Specify the executable path of :program:`cpplint`. Can simply be
        :code:`cpplint = cpplint` if it is included in :envvar:`PATH`.

        Default: :code:`cpplint`.

:code:`cpplint.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g.,

        .. code-block:: ini

                cpplint.options = --filter=-whitespace,+whitespace/braces --root=..

        Default configuration file location: :file:`.github/linter-configs/CPPLINT.cfg`.

:code:`clang_format = <exec>`
        Specify the executable path of :program:`clang-format`. Can simply be
        :code:`clang_format = clang-format` if it is included in :envvar:`PATH`.

:code:`clang_format.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g,

        .. code-block:: ini

                clang_format.options = --Werror --style=google

        Default configuration file location: :file:`.github/linter-configs/.clang-format`.

:code:`pylint = <exec>`
        Specify the executable path of :program:`pylint`. Can simply be
        :code:`pylint = pylint` if it is included in :envvar:`PATH`.

:code:`pylint.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g,

        .. code-block:: ini

                pylint.options = --output-format=parseable

        Default configuration file location: :file:`.github/linter-configs/.pylintrc`.

:code:`flake8 = <exec>`
        Specify the executable path of :program:`flake8`. Can simply be
        :code:`flake8 = flake8` if it is included in :envvar:`PATH`.

:code:`flake8.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g.,

        .. code-block:: ini

                flake8.options = --max-line-length 88

        Default configuration file location: :file:`.github/linter-configs/.flake8`.

:code:`black = <exec>`
        Specify the executable path of :program:`black`. Can simply be
        :code:`black = black` if it is included in :envvar:`PATH`.

:code:`black.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g.,

        .. code-block:: ini

                black.options = --diff --check

        Default configuration file location: :file:`.github/linter-configs/.black`.

:code:`isort = <exec>`
        Specify the executable path of :program:`isort`. Can simply be
        :code:`isort = isort` if it is included in :envvar:`PATH`.

:code:`isort.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g.,

        .. code-block:: ini

                isort.options = --line-length 88 --color

        Default configuration file location: :file:`.github/linter-configs/.isort.cfg`.

:code:`mypy = <exec>`
        Specify the executable path of :program:`mypy`. Can simply be
        :code:`mypy = mypy` if it is included in :envvar:`PATH`.

:code:`mypy.options = <...>`
        Specify the options that will passed to the executable. Format is the same as
        given in command line, e.g.,

        .. code-block:: ini

                mypy.options = --cache-dir .

        Default configuration file location: :file:`.github/linter-configs/.mypy.ini`.

:code:`[env]`
~~~~~~~~~~~~~

:code:`debug = <True | False>`
        Set :program:`glob_linters` to debugging mode.

        Default: :code:`False`.

:code:`.cpp.linters = <...>`
        Specify linters used for :file:`.cpp` files.

        Default: :code:`.cpp.linters = cpplint clang_format`.

:code:`.cpp.disable_linters = <...>`
        Disable linters used for :file:`.cpp` files. Should be a list from the default
        linters with the same format as :code:`.cpp.linters`.

:code:`.py.linters = <...>`
        Specify linters used for :file:`.py` files.

        Default: :code:`.py.linters = pylint`.

:code:`.py.disable_linters = <...>`
        Disable linters used for :file:`.py` files. Should be a list from the default
        linters with the same format as :code:`.py.linters`.

Example
~~~~~~~

A direct example is given as:

.. code-block:: ini

        [target]
        target_dir = .
        target_suffix = .py

        [executable]
        pylint = pylint
        black = black
        isort = isort

        [env]
        debug = True
        .py.disable_linters = flake8 mypy

The above example will only lint :file:`.py` files in the current working directory
with only :code:`pylint`, :code:`black` and :code:`isort` linters as well as debugging
mode enabled.

Linter configurations
---------------------

Configuration files for linters are given in :file:`LINTER_CONFIGS` of GitHub_ repository
as templates. You can modify them as you need.

.. _GitHub: https://github.com/bowentan/glob-linters

.. note::

        If you use :program:`glob_linters` in GitHub action, please place configurations
        in :file:`.github/linter-configs/` and do *NOT* change the name of the
        configuration files.