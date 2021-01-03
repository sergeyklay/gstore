Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

v0.3.0
------

* Improved logging and error reporting.
* Improved local repo handling by checking the directory contents.
* Corrected log level on ``--quiet`` mode.
* Changed the way to get repositories from specific organizations.
  From now, to get repositories from specific organizations, list each of them
  on the command line using the argument ``--org``.
* Fixed invalid local repo handling.

New features
~~~~~~~~~~~~

* Added ``-o`` as a short form of ``--org`` argument.
* Added ability to limit sync to the specified repositories using ``--repo``
  option.

Packaging changes
~~~~~~~~~~~~~~~~~

* Python < 3.7 is no longer supported.

v0.2.0
------

* Show help message and exit when Gstore is called without any argument and
  there are not enough environment variables for normal operation.

New features
~~~~~~~~~~~~

* Added ability to specify host for Github Enterprise.

v0.1.1
------

* Handling situations when the target for sync is a regular file or readonly.

New features
~~~~~~~~~~~~

* Added ``-V``, ``--version`` arguments to print program's version information.
* Added ``-dumpversion`` argument to print the version of the program and don't
  do anything else.
* Added ``-q``, ``--quiet`` arguments to silence any informational messages
  except error ones

v0.1.0
------

New features
~~~~~~~~~~~~

* The GitHub username is no longer required upon obtaining organizations list.
* Provided ability to pass authentication token for github.com API requests via
  environment variables.
* Added ``-v`` argument support to enable verbose mode.

Packaging changes
~~~~~~~~~~~~~~~~~

* Changed the way to communicate with GitHub API. ``requests`` library no
  longer used thanks to ``PyGithub``.

v0.0.5
------

New features
~~~~~~~~~~~~

* Added better logging subsystem

Packaging changes
~~~~~~~~~~~~~~~~~

* Bump GitPython version to fix a crash for users with
  ``gitpython>=3.0.0, <3.0.6``. For more see:
  https://github.com/gitpython-developers/GitPython/issues/983 .

v0.0.4
------

* Renamed ``GHS_DIR`` environment variable to ``GSTORE_DIR``.

Packaging changes
~~~~~~~~~~~~~~~~~

* Renamed package name from ``ghs`` to ``gstore`` to avoid collision with the
  existing package with the same name.

v0.0.3
------

New features
~~~~~~~~~~~~

* Added ability to use ``GHS_DIR`` as a sync base directory.
* Added ability to omit target directory and use current working directory.
* Added ability to fetch objects and refs from an existent repository.

v0.0.2
------

Packaging changes
~~~~~~~~~~~~~~~~~

* Renamed package name from ``ghsync`` to ``ghs`` to avoid collision with the
  existing package with the same name.

v0.0.1
------

* Initial release.
