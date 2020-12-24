gstore
===

Gstore is a simple tool to synchronize GitHub repositories of your organizations.

Overview
--------

This tool uses the GitHub API to get a list of all forked, mirrored, public, and
private repos owned by your organizations. If the repo already exists locally,
it will update it via git-pull. Otherwise, it will properly clone the repo.

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

To install gstore, simply run:

.. code-block:: bash

   $ pip install gstore

The command ``gstore`` will be available to you from the command line.

Usage
-----

.. code-block:: bash

   $ gstore [-h] [--user USER] --token TOKEN [--org [ORG ...]] [target]

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

To be able get organizations list for a user, gstore will need a GitHub
username. Thus we pass it bellow (``--user``).:

.. code-block:: bash

   $ gstore --token "$TOKEN" --user "$GH_USER" ~/backup

Unless you set the ``GSTORE_DIR`` environment variable and don't provide
*target*, gstore will sync all the repositories to current working directory.:

.. code-block:: bash

   # Will sync all the repositories to current working directory
   $ gstore --token "$TOKEN" --user "$GH_USER"

   # Will sync all the repositories to ~/work directory
   $ export GSTORE_DIR=~/work
   $ gstore --token "$TOKEN" --user "$GH_USER"

   # Will sync all the repositories to ~/backup directory
   $ gstore --token "$TOKEN" --user "$GH_USER" ~/backup

**Sync all repos from Acme organization**

To get all repositories of a specific organization, just specify it as follows:

.. code-block:: bash

   $ gstore --org Acme --token "$TOKEN" ~/backup

To specify a *target* directory right after organization list use double dash
to signify the end of org option.:

.. code-block:: bash

   $ gstore --token "$TOKEN" --org Acme -- ~/backup

**Sync all repos from Foo, Bar and Baz organizations**

To get all repositories of the listed organizations, specify them separated by a
space:

.. code-block:: bash

   $ gstore --token "$TOKEN" --org Foo Bar Baz -- ~/backup

Similar projects
----------------

There are some projects similar to gstore you may interested for:

* https://github.com/kennethreitz42/ghsync
* https://github.com/adw0rd/github-sync

Support
-------

Feel free to ask question or make suggestions in our `issue tracker`_.

Changes
-------

To see what has changed in recent versions of gstore see `CHANGELOG.rst`_.

License
-------

This project is open source software licensed under the
`GNU General Public Licence version 3`_.  © 2020 `Serghei Iakovlev`_

.. _CHANGELOG.rst: https://github.com/sergeyklay/gstore/blob/master/CHANGELOG.rst
.. _issue tracker: https://github.com/sergeyklay/gstore/issues
.. _`Serghei Iakovlev`: https://github.com/sergeyklay
.. _GNU General Public Licence version 3: https://github.com/sergeyklay/gstore/blob/master/LICENSE
