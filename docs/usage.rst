=====
Usage
=====

When using glob-linters as a command line tool, you can use both command line options
and configuration file to control the parameters for linting.

Command line options
--------------------

.. note::
        The command line options will be overwritten by
        :ref:`configuration file <configuration-file>` . All given
        arguments will ignored if you use configuration file.

You can use :program:`glob-linters` as a command line tool if you want to lint your
codes or test your GitHub action workflow in local terminals.

.. program:: glob-linters

.. option:: -d [TARGET_DIR], --target-dirs [TARGET_DIR ...]

        Specify the directory to be scanned for files to be linted, could be multiple
        values separated by space.

        Default: :file:`.`, the current working directory when :program:`glob-linters` is
        called.

        Keyword in configuration file: :code:`target.dirs`.

.. option:: -s [TARGET_SUFFIX ...], --target-suffixes [TARGET_SUFFIX ...]

        Extensions of files to be linted, e.g., :file:`.cpp`, :file:`.py`, and can be
        given more than one, separated by comma or space.

        Default: all supported language extensions.

        Keyword in configuration file: :code:`target.suffixes`.

.. option:: -E [ENABLED_LINTER ...], --enable-linters [ENABLED_LINTER ...]

        Enable specified linters to run. Only enabled linters will be run. The format of
        the argument is :code:`{suffix}:{linter_name}`, e.g., :code:`.cpp:clang_format` and
        :code:`.py:mypy`. Multiple arguments can be given.

        Default: :code:`None`

        Keyword in configuration: :code:`{suffix}.enabled_linters` such as
        :code:`.cpp.enabled_linters`.

.. option:: -D [DISABLED_LINTER ...], --disable-linters [DISABLED_LINTER ...]

        Disable specified linters to run. Only enabled linters will be run. The format of
        the argument is the same as :option:`glob-linters --enable-linters`

        Default: :code:`None`

        Keyword in configuration: :code:`{suffix}.disabled_linters` such as
        :code:`.cpp.disabled_linters`.

.. option:: -c [LINTER_SETTING ...], --linter-settings [LINTER_SETTING ...]
        
        Configure linters via command line arguments. Format is
        :code:`{suffix}:{linter_name}.{arg}={value}` where :code:`arg` can be one of the following

        * :code:`executable`, the path of linter executable
        * :code:`config_file`, the path of linter configuration file
        * :code:`options`, additional arguments feeded to linter

        For example, :code:`.cpp:cpplint.executable=/home/bowentan/.local/bin/cpplint`.

        Default: :code:`None`.

        Keyword in configuration file: :code:`{suffix}:{linter_name}.{arg}`.

.. option:: -x [EXTRA_PYTHON_PACKAGE_REQUIREMENTS ...], --extra-python-package-requirements [EXTRA_PYTHON_PACKAGE_REQUIREMENTS ...]
        
        Specify extra python packages which may be used in linting such as as Numpy
        extension. The same format of general :file:`requirements.txt`. Multiple files
        supported.

        Default: :code:`None`

        Keyword in configuration: :code:`env.extra_python_package_requirements`.

.. option:: -C [CONFIG_FILE], --config-file [CONFIG_FILE]

        :program:`glob-linters` configuration file (:file:`glob-linters.ini`) path.

        Default: :file:`.github/glob-linters.ini`.

        No keyword for this in configuration file.

.. option:: -g, --enable-debug

        Enable debug mode. Debugging information will be outputed.

        Default: disabled.

        Keyword in configuration file: :code:`env.debug`.

Examples
~~~~~~~~

By issuing :program:`glob-linters` in a directory like following:

.. code-block:: console

        $ glob-linters

without any options, :program:`glob-linters` will recursively scan the
directory to find files with all supported extensions using all default linters.

To change the target directory to :file:`src/` and only lint :file:`.py` files,
add options:

.. code-block:: console

        $ glob-linters --target-dirs src --target-suffixes .py

and if you also want to diasble :code:`flake8` and :code:`mypy` linters with debugging
information, do this:

.. code-block:: console

        $ glob-linters --target-dir src --target-suffix .py --disable-linters flake8 mypy


.. _configuration-file:

Configuration file
------------------

The configuration file format follows configparse_ structure. The configuration file
is generally used in GitHub actions. You can also use it to test your workflow in
local terminals.

.. _configparse: https://docs.python.org/3/library/configparser.html

:code:`[target]`
~~~~~~~~~~~~~~~~

:code:`dirs = <TARGET_DIR>`
        Work as the same with :option:`glob-linters --target-dirs`. Directories to be
        scanned.

        Default: :file:`.`

:code:`suffixes = <TARGET_SUFFIX ...>`
        Work as the same with :option:`glob-linters --target-suffixes`. File suffixes to
        be scanned.

        Default: all supported file suffixes.

:code:`[{suffix}]`
~~~~~~~~~~~~~~~~~~

:code:`enabled_linters = <...>`
        Specify the linters to be run for files with :code:`{suffix}` suffix. Separate
        multiple values by comma or space.

        Default: all supported linters.

:code:`disabled_linters = <...>`
        Disable the linters that will not be run for files with :code:`{suffix}` suffix.
        Separate multiple values by comma or space.

        Default: :code:`None`.

:code:`[{suffix}:{linter_name}]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:code:`executable = <path>`
        Specify the path of executable of the linter :code:`{suffix}:linter_name`.

        Default: the basename of the linter.

:code:`config_file = <path>`
        Specify the path of configuration file of the linter :code:`{suffix}:linter_name`.

        Default: :code:`None`.

:code:`[env]`
~~~~~~~~~~~~~

:code:`debug = <True | False>`
        Set :program:`glob-linters` to debugging mode.

        Default: :code:`False`.

:code:`extra_python_package_requirements`
        Specify additional Python package requirements. Separate multiple files by comma
        or space.

        Default: :code:`None`.

Example
~~~~~~~

A direct example is given as:

.. code-block:: ini

        [target]
        dirs = src scripts
        suffixes = .cpp .py

        [.cpp]
        enabled_linters = cpplint clang_format
        
        [.cpp:cpplint]
        config_file = .github/linter-configs/CPPLINT.cfg

        [.cpp.clang_format]
        config_file = .github/linter-configs/.clang-format

        [.py]
        disabled_linters = flake8 mypy

        [.py:pylint]
        config_file = .github/linter-configs/.pylintrc

        [.py:black]
        config_file = .github/linter-configs/.black

        [.py:isort]
        config_file = .github/linter-configs/.isort.cfg

        [env]
        debug = True

The above example will lint :file:`.cpp` and :file:`.py` files in the :file:`src` and
:file:`scripts` directories with :code:`cpplint` and :code:`clang_format` for
:code:`.cpp` files, :code:`pylint`, :code:`black` and :code:`isort` linters for 
:code:`.py` files as well as degugging mode enabled. Also custom configuration files for
all enabled linters are given, which are generally cases when used in GitHub Action.

Linter configurations
---------------------

Example configuration files for linters are given in :file:`LINTER_CONFIGS` of GitHub_ repository
as templates. You can modify them as you need.

.. _GitHub: https://github.com/bowentan/glob-linters