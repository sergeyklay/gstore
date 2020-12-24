Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

v0.0.5
------

Packaging changes
~~~~~~~~~~~~~~~~~

* Bump GitPython version to fix a crash for users with ``gitpython>=3.0.0, <3.0.6``.
  For more see: https://github.com/gitpython-developers/GitPython/issues/983

v0.0.4
------

* Rename ``GHS_DIR`` environment variable to ``GSTORE_DIR``.

Packaging changes
~~~~~~~~~~~~~~~~~

* Rename package name from ``ghs`` to ``gstore`` to avoid collision with the
  existing package with the same name.

v0.0.3
------

New features
~~~~~~~~~~~~

* Add ability to use ``GHS_DIR`` as a sync base directory.
* Add ability to omit target directory and use current working directory.
* Add ability to fetch objects and refs from an existent repository.

v0.0.2
------

Packaging changes
~~~~~~~~~~~~~~~~~

* Rename package name from ``ghsync`` to ``ghs`` to avoid collision with the
  existing package with the same name.

v0.0.1
------

* Initial release
