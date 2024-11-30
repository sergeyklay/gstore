=========================================
Maintainers' Guide for the gstore Project
=========================================

This document outlines essential guidelines for maintaining the ``gstore`` project. It provides instructions for testing, building, and deploying the package, as well as managing CI workflows.

Overview
========

The ``gstore`` project is a CLI tool for synchronizing GitHub repositories. It is managed via poetry and adheres to modern Python packaging standards. This guide assumes familiarity with GitHub Actions, ``poetry``, and common Python development workflows.

Key configurations:

- ***Python Versions Supported:*** 3.9, 3.10, 3.11, 3.12
- **Build Tool:** ``poetry``
- **Primary Dependencies:** ``pygithub``, ``gitpython``
- **Documentation Tool:** ``sphinx``
- **Linting Tools:** flake8, pylint

Testing the Project
===================

Unit tests and coverage reporting are managed using ``pytest`` and ``coverage``.

Running Tests Locally
---------------------

Install dependencies:

.. code-block:: bash

   $ poetry install --with=testing

Execute tests:

.. code-block:: bash

   $ coverage run -m pytest ./gstore ./tests
   $ coverage combine
   $ coverage report

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

   $ poetry install --only=build

Build the package:

.. code-block:: bash

   $ poetry build

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

   $ poetry install --only=docs

Build the documentation:

.. code-block:: bash

   $ sphinx-build --nitpicky --show-traceback --fail-on-warning --builder html docs docs/_build/html

Validate doctests:

.. code-block:: bash

   $ sphinx-build --builder doctest docs docs/_build/doctest
   $ python -m doctest README.rst

CI Workflow
-----------

The docs workflow automatically builds and validates documentation on pushes and pull requests. See ``.github/workflows/docs.yml​`` (`docs <https://github.com/sergeyklay/gstore/blob/main/.github/workflows/docs.yml>`_).

Linting and Code Quality Checks
===============================

Code quality is enforced using ``flake8`` and ``pylint``.

Running Locally
---------------

Install linting dependencies:

.. code-block:: bash

   $ poetry install --with=testing

Execute linting:

.. code-block:: bash

   $ flake8 ./
   $ pylint ./gstore

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

   $ poetry build
   $ poetry publish

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

Validate the ``pyproject.toml`` file:

.. code-block:: bash

   $ poetry check

Test installation of the built package:

.. code-block:: bash

   $ pip install dist/*.whl
   $ gstore --version
