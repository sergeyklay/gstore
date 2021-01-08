=================================================
Gstore: Synchronize GitHub repositories made easy
=================================================

Release v\ |release| (`What's new? <changelog>`).

.. include:: ../README.rst
   :start-after: teaser-begin
   :end-before: teaser-end

Overview
========

Gstore uses the GitHub API to get a list of all forked, mirrored, public,
and private repos owned by your organizations. If the repo already exists
locally, it will update it via git-pull. Otherwise, it will properly clone the
repo.

Gstore will organize your repos into the following directory structure:

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

#. Save the token in a safe place; you'll need it when use Gstore

#. Sync your repos:

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup


.. include:: ../README.rst
   :start-after: -support-
   :end-before: -similar-projects-

.. include:: ../README.rst
   :start-after: -similar-projects-

----


Full Table of Contents
======================

.. toctree::
   :maxdepth: 2

   installation
   usage
   logging

.. include:: ../README.rst
   :start-after: -project-information-
   :end-before: -support-

.. toctree::
   :maxdepth: 1

   license
   changelog


Indices and tables
==================

* `genindex`
* `search`
