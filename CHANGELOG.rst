Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

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

* Change the way to communicate with GitHub API. ```requests`` library no
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
