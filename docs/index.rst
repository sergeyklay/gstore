=========================================
Synchronize GitHub repositories made easy
=========================================

Release v\ |release| (`What's new? <changelog>`).

``gstore`` is a simple tool to synchronize GitHub repositories of your organizations.

Its main goal is to help you make backups and sync your projects automatically
and easily.


Overview
========

``gstore`` uses the GitHub API to get a list of all forked, mirrored, public,
and private repos owned by your organizations. If the repo already exists
locally, it will update it via git-pull. Otherwise, it will properly clone the
repo.

``gstore`` will organize your repos into the following directory structure:

.. code-block:: bash

   + sync-dir
   ├── organization_1
   │   ├── repo_1
   │   ├── repo_2
   │   ├── ...
   │   └── repo_n
   ├── organization_2
   │   ├── repo_1
   │   ├── repo_2
   │   ├── ...
   │   └── repo_n
   └── organization_n
       ├── repo_1
       ├── repo_2
       ├── ...
       └── repo_n


Quick Start
===========

#. Generate a GitHub `Personal Access Token <https://github.com/settings/tokens>`_ with the following permissions:

   * ``repo``: Full control of private repositories

   * ``user:read``: Read all user profile data

#. Save the token in a safe place; you'll need it when use ``gstore``

#. Sync your repos:

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup


Support
=======

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the ``gstore``, please
`open an issue <https://github.com/sergeyklay/gstore/issues>`_.


Similar projects
================

There are some projects similar to ``gstore`` you may be interested in:

* https://github.com/kennethreitz42/ghsync
* https://github.com/lgg/simple-git-mirror-sync

----


Full Table of Contents
======================

.. toctree::
   :maxdepth: 2

   installation
   usage
   logging

Project Information
===================

``gstore`` is released under the `GNU General Public Licence version 3 <https://choosealicense.com/licenses/gpl-3.0/>`_, its documentation lives at `Read the Docs <https://gstore.readthedocs.io/>`_, the code on `GitHub <https://github.com/sergeyklay/gstore>`_, and the latest release on `PyPI <https://pypi.org/project/gstore/>`_. It’s rigorously tested on Python 3.8+.

If you'd like to contribute to ``gstore`` you're most welcome!

.. toctree::
   :maxdepth: 1

   maintainers
   license
   changelog


Indices and tables
==================

* `genindex`
* `search`
