=====
Usage
=====

Command Line Options
====================

**Quick Start:**

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup

**Synopsis:**

::

   gstore [options] [[--] target]

**Options:**
  ``-h``, ``--help``
    Print help message and quit.

  ``--token TOKEN``
    A `Personal Access Token <https://github.com/settings/tokens>`_ for GitHub
    API requests. If not provided via this option, then environment variable
    will be used. The order of searching for a token in environment variables
    as follows (in order of precedence):

    #. ``GH_TOKEN``, ``GITHUB_TOKEN``
    #. ``GH_ENTERPRISE_TOKEN``, ``GITHUB_ENTERPRISE_TOKEN``

    Setting these variables allows you not to not pass token directly via CLI
    and avoids storing it in the Shell history.

  ``--host HOST``
    The GitHub API hostname. If not provided via this options, then ``GH_HOST``
    environment variable will be used. If environment variable is not set,
    ``api.github.com`` will be used.

  ``-o ORG``, ``--org ORG``
    Organization to sync (all if not provided). Option is additive, and can be
    used multiple times.

  ``-r REPO``, ``--repo REPO``
    Limit sync to the specified repository, otherwise sync all repositories
    (format *org:repo*). Option is additive, and can be used multiple times.

  ``-v``, ``--verbose``
    Enable verbose mode. Causes Gstore to print debugging messages about its
    progress in some cases.

  ``-q``, ``--quiet``
    Silence any informational messages, but not error ones.

  ``-V``, ``--version``
    Print program's version information and quit.

  ``-dumpversion``
    Print the version of the program and don't do anything else.

  ``[--] target``
    Base target to sync repos (e.g. folder on disk). If not provided
    environment variable ``GSTORE_DIR`` will be used. If there is not
    environment variable, then current working directory will be used.

Examples
========

Sync all repos from all organizations
-------------------------------------

The example below will perform HTTP requests to GitHub API. In general, we'll
need to obtain GitHub username, and to get a list of user's organizations.
At the end Gstore will sync repositories of organizations via Git.

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup

Unless you set the ``GSTORE_DIR`` environment variable and don't provide
target directory, Gstore will sync all the repositories to current working
directory.:

.. code-block:: bash

   # Will sync all the repositories to current working directory
   $ gstore --token "$TOKEN"

   # Will sync all the repositories to ~/backup directory
   $ export GSTORE_DIR=~/backup
   $ export GH_TOKEN="secret"
   $ gstore

   # Will sync all the repositories to ~/backup directory
   $ gstore --token "$TOKEN" ~/backup

.. note::

   Gstore will show help message and exit when it is called without any
   argument and there are not enough environment variables for normal
   operation.

Sync all repos from an organization
-----------------------------------

To get all repositories of a specific organization, just specify it as follows:

.. code-block:: bash

   $ gstore --org Acme --token "$TOKEN" ~/backup

Sync specified repos from an organization
-----------------------------------------

To get only specified repos for a particular organization use ``--repo``
option. This option is additive, and can be used multiple times.:

.. code-block:: bash

   $ gstore --org Acme --repo Acme:foo --repo Acme:bar \
       --token "$TOKEN" ~/backup

Sync all repos from many organizations
--------------------------------------

To get repositories from specific organizations, list each of them on the
command line using the option ``--org`` as follows:

.. code-block:: bash

   $ gstore --token "$TOKEN" --org Foo --org Bar --org Baz ~/backup

Option ``--org`` is additive, and can be used multiple times.

Using Github Enterprise
=======================

There is nothing special when working with the Github Enterprise, except for
the host and possible environment variables.:

.. code-block:: bash

   # Using command line options to configure Gstore
   $ gstore --token "secret" --host "github.example.com" ~/backup

   # Using environment variables to configure Gstore
   $ export GH_ENTERPRISE_TOKEN="secret"
   $ export GH_HOST="github.example.com"
   $ gstore ~/backup
