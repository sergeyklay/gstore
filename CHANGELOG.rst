Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

Versions follow `Semantic Versioning`_ (``<major>.<minor>.<patch>``).

.. note::

   Backward incompatible (breaking) changes will only be introduced in major
   versions with advance notice in the **Deprecations** section of releases.

0.3.1 (2021-01-03)
------------------

Improvements
^^^^^^^^^^^^

* Gstore will exit with a status of one if there are critical errors during
  synchronization.
* Gstore will handle situations with invalid API token or organization name.


Improved Documentation
^^^^^^^^^^^^^^^^^^^^^^

* Move all the documentation to `readthedocs <https://gstore.readthedocs.io>`_.


Bug Fixes
^^^^^^^^^

* Fix ``args.get_token_from_env()`` to properly get a token from environment
  variables or None if variables are not set.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* ``Client.__init__()``, as well as ``Client.resolve_orgs()`` will raise now
  ``gstore.exceptions.InvalidCredentialsError`` in case of incorrect
  credentials usage.
* ``gstore.models.Repository`` now holds ``gstore.models.Organization``.
* Starting with v0.3.1 tests will be included in the PyPI package.


----


0.3.0 (2021-01-03)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Python < 3.7 is no longer supported.
* Changed the way to get repositories from specific organizations.
  From now, to get repositories from specific organizations, list each of them
  on the command line using the argument ``--org``.


Features
^^^^^^^^

* Added ``-o`` as a short form of ``--org`` argument.
* Added ability to limit sync to the specified repositories using ``-r``,
  ``--repo`` option.


Improvements
^^^^^^^^^^^^

* Improved logging and error reporting.
* Improved local repo handling by checking the directory contents.


Bug Fixes
^^^^^^^^^

* Corrected log level on ``--quiet`` mode.
* Fixed invalid local repo handling.


----


0.2.0 (2020-12-27)
------------------

Features
^^^^^^^^

* Added ability to specify host for Github Enterprise.


Improvements
^^^^^^^^^^^^

* Show help message and exit when Gstore is called without any argument and
  there are not enough environment variables for normal operation.


----


0.1.1 (2020-12-27)
------------------

Features
^^^^^^^^

* Added ``-V``, ``--version`` arguments to print program's version information.
* Added ``-dumpversion`` argument to print the version of the program and don't
  do anything else.
* Added ``-q``, ``--quiet`` arguments to silence any informational messages
  except error ones


Improvements
^^^^^^^^^^^^

* Handling situations when the target for sync is a regular file or readonly.


----


0.1.0 (2020-12-26)
------------------

Features
^^^^^^^^

* Provided ability to pass authentication token for github.com API requests via
  environment variables.
* Added ``-v`` argument support to enable verbose mode.


Breaking Changes
^^^^^^^^^^^^^^^^

* The GitHub username is no longer used upon obtaining organizations list.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Changed the way to communicate with GitHub API. ``requests`` library no
  longer used thanks to ``PyGithub``.


----


0.0.5 (2020-12-25)
------------------

Features
^^^^^^^^

* Added better logging subsystem


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Bump GitPython version to fix a crash for users with
  ``gitpython>=3.0.0, <3.0.6``. For more see:
  https://github.com/gitpython-developers/GitPython/issues/983 .


----


0.0.4 (2020-12-24)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Renamed ``GHS_DIR`` environment variable to ``GSTORE_DIR``.
* Renamed package name from ``ghs`` to ``gstore`` to avoid collision with the
  existing package with the same name.


----


0.0.3 (2020-12-24)
------------------

Features
^^^^^^^^

* Added ability to use ``GHS_DIR`` as a sync base directory.
* Added ability to omit target directory and use current working directory.
* Added ability to fetch objects and refs from an existent repository.


----


0.0.2 (2020-12-24)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Renamed package name from ``ghsync`` to ``ghs`` to avoid collision with the
  existing package with the same name.


----


0.0.1 (2020-12-23)
------------------

* Initial release.

.. _Semantic Versioning: https://semver.org/

