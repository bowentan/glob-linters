.. highlight:: shell

============
Contributing
============

Contributions are welcome, and are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/bowentan/glob-linters/issues.

If you are reporting a bug, please follow the template to give as many details as
you can.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

glob-linters could always use more documentation, whether as part of the
official glob-linters docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/bowentan/glob-linters/issues.

Get Started!
------------

Ready to contribute? Here's how to set up `glob-linters` for local development.

1. Fork the `glob-linters` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:bowentan/glob-linters.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv glob-linters
    $ cd glob-linters/
    $ python setup.py develop

   Additionally, you can install the required Python packages for development::

    $ pip install -r requirements_dev.txt

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the following checks:

   * :program:`pylint`
   * :program:`flake8`
   * :program:`black`
   * :program:`isort`
   * :program:`mypy`

   All these linters have corresponding extensions in VSCode. You should also test
   the changes to guarantee that they work before you commit changes.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should pass local tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.