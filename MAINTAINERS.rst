==================
Maintainers' Guide
==================

This document outlines essential guidelines for maintaining the ``gstore`` project. It provides instructions for testing, building, and deploying the package, as well as managing CI workflows.

Overview
========

This is managed via uv and adheres to modern Python packaging standards. This guide assumes familiarity with GitHub Actions, ``uv``, and common Python development workflows.

Key configurations:

- **Python Versions Supported:** >= 3.10
- **Build Tool:** ``uv``
- **Primary Dependencies:** ``pygithub``, ``gitpython``
- **Documentation Tool:** ``sphinx``
- **Testing Tools:** ``pytest``, ``coverage``
- **Linting Tools:** ``ruff``

Testing the Project
===================

Unit tests and coverage reporting are managed using ``pytest`` and ``coverage``.

Running Tests Locally
---------------------

Install dependencies:

.. code-block:: bash

   $ uv sync --group dev

Execute tests:

.. code-block:: bash

   $ uv run coverage run -m pytest ./gstore ./tests
   $ uv run coverage combine
   $ uv run coverage report

CI Workflow
-----------

Tests are executed automatically on supported platforms and Python versions. See the configuration in ``.github/workflows/ci.yml`` (`ci <https://github.com/sergeyklay/gstore/blob/main/.github/workflows/ci.yml>`_).

Building the Package
====================


The ``gstore`` package is distributed in ``wheel`` and ``sdist`` formats.

Local Build
-----------

Install build dependencies:

.. code-block:: bash

   $ uv sync --group dev

Build the package:

.. code-block:: bash

   $ uv build
   $ uv run twine check dist/*

CI Workflow
-----------

The build workflow in ``.github/workflows/build.yml`` ensures the package is built and verified across multiple Python versions​ (`build <https://github.com/sergeyklay/gstore/blob/main/.github/workflows/build.yml>`_).

Documentation Management
========================

Documentation is written using ``sphinx`` and built into HTML and other formats.

Building Documentation Locally
------------------------------

Install documentation dependencies:

.. code-block:: bash

   $ uv sync --group dev

Build the documentation:

.. code-block:: bash

   $ uv run sphinx-build --nitpicky --show-traceback --fail-on-warning --builder html docs docs/_build/html

Validate doctests:

.. code-block:: bash

   $ uv run sphinx-build --builder doctest docs docs/_build/doctest
   $ uv run python -m doctest README.rst

CI Workflow
-----------

The docs workflow automatically builds and validates documentation on pushes and pull requests. See ``.github/workflows/docs.yml​`` (`docs <https://github.com/sergeyklay/gstore/blob/main/.github/workflows/docs.yml>`_).

Linting and Code Quality Checks
===============================

Code quality is enforced using ``ruff``.

Running Locally
---------------

Install linting dependencies:

.. code-block:: bash

   $ uv sync --group dev

Execute linting:

.. code-block:: bash

   $ uv run ruff check .

CI Workflow
-----------

The lint workflow in ``.github/workflows/lint.yml`` ensures all pushes and pull requests meet quality standards​ (`lint <https://github.com/sergeyklay/gstore/blob/main/.github/workflows/lint.yml>`_).

Release Process
===============

The release process involves version tagging and package publishing to PyPI.

Steps for Release
-----------------

1. Update the version in ``pyproject.toml`` according to semantic versioning.
2. Update ``CHANGELOG.rst``.
3. Update the version in ``gstore/__init__.py``.
4. Tag the version using git and push tag to GitHub.
5. Build and publish the package:

.. code-block:: bash

   $ uv build
   $ uv publish

CI Workflow
-----------

The build workflow ensures the package is valid before publishing. Tags matching the pattern ``vX.Y.Z`` trigger additional checks​ (`build <https://github.com/sergeyklay/gstore/blob/main/.github/workflows/build.yml>`_).


Continuous Integration and Deployment
=====================================

CI/CD is managed via GitHub Actions, with workflows for:

- **Testing:** Ensures functionality and compatibility across platforms.
- **Linting:** Maintains code quality.
- **Documentation:** Validates and builds project documentation.
- **Building:** Verifies the package's integrity.

Useful CI Commands
------------------

Validate the ``uv.lock`` file:

.. code-block:: bash

   $ uv lock --check

Test installation of the built package:

.. code-block:: bash

   $ pip install dist/*.whl
   $ gstore --version
