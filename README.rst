ghs
===

Ghs is a simple cli tool to synchronize organizations' repositories from GitHub.

Overview
--------

This tool uses the GitHub API to get a list of all forked, mirrored, public, and
private repos owned by you organizations. If the repo already exists locally, it
will update it via git-pull. Otherwise, it will properly clone the repo.

It will organize your repos into the following directory structure:

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

Install
-------

To install ghsync, simply run:

.. code-block:: bash

   $ pip install ghs

The command ``ghs`` will be available to you from the command line.

Usage
-----

.. code-block:: bash

   $ ghs [-h] [--user USER] --token TOKEN [--org [ORG ...]] [target]

   Synchronize organizations' repositories from GitHub.

   positional arguments:
     target           base target to sync repos (e.g. folder on disk)

   optional arguments:
     -h, --help       show this help message and exit
     --user USER      username to use to get organizations list
     --token TOKEN    personal auth token
     --org [ORG ...]  organizations you have access to (by default all)

Examples
~~~~~~~~

**Sync all repos from all organizations**

To be able get organizations list for a user, ghs will need a GitHub
username. Thus we pass it bellow (``--user``).:

.. code-block:: bash

   $ ghs --token "$TOKEN" --user "$GH_USER" ~/backup

Unless you set the ``GHS_DIR`` environment variable and don't provide
``target``, ghs will sync all the repositories to current working directory.:

.. code-block:: bash

   # Will sync all the repositories to current working directory
   $ ghs --token "$TOKEN" --user "$GH_USER"

   # Will sync all the repositories to ~/work directory
   $ export GHS_DIR=~/work
   $ ghs --token "$TOKEN" --user "$GH_USER"

**Sync all repos from Acme organization**

To get all repositories of a specific organization, just specify it:

.. code-block:: bash

   $ ghs --token "$TOKEN" --org Acme -- ~/backup

**Sync all repos from Foo, Bar and Baz organizations**

To get all repositories of the listed organizations, specify them separated by a
space:

.. code-block:: bash

   $ ghs --token "$TOKEN" --org Foo Bar Baz -- ~/backup

License
-------

This project is open source software licensed under the GNU General Public
Licence version 3.  © 2020 Serghei Iakovlev
