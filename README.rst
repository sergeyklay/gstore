.. raw:: html

    <h1 align="center">Gstore</h1>
    <p align="center">
        <a href="https://gstore.readthedocs.io/en/latest/?badge=latest">
            <img src="https://readthedocs.org/projects/gstore/badge/?version=latest" alt="Documentation Status" />
        </a>
        <a href="https://github.com/sergeyklay/gstore/actions?workflow=CI">
            <img src="https://github.com/sergeyklay/gstore/workflows/CI/badge.svg?branch=master" alt="CI Status" />
        </a>
        <a href="https://codecov.io/github/sergeyklay/gstore">
            <img src="https://codecov.io/github/sergeyklay/gstore/branch/master/graph/badge.svg" alt="Test Coverage" />
        </a>
    </p>

.. teaser-begin

Gstore is a simple tool to synchronize GitHub repositories of your organizations.

Its main goal is to help you make backups and sync your projects automatically
and easily.

.. teaser-end

Overview
--------

This tool uses the GitHub API to get a list of all forked, mirrored, public,
and private repos owned by your organizations. If the repo already exists
locally, it will update it via git-pull. Otherwise, it will properly clone the
repo.

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

Quick Start
---------------

#. Generate a GitHub `Personal Access Token <https://github.com/settings/tokens>`_ with the following permissions:

   * ``repo``: Full control of private repositories

   * ``user:read``: Read all user profile data

#. Save the token in a safe place; you'll need it when use Gstore

#. Sync your repos:

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup

Usage
-----

::

   gstore [options] [[--] target]

**Options:**
  ``-h``, ``--help``
    Print help message and quit.

  ``--token TOKEN``
    An authentication token for GitHub API requests. If not provided via this
    option, then environment variable will be used. The order of searching
    for a token in environment variables as follows (in order of precedence):

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
~~~~~~~~

**Sync all repos from all organizations**

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

**Sync all repos from Acme organization**

To get all repositories of a specific organization, just specify it as follows:

.. code-block:: bash

   $ gstore --org Acme --token "$TOKEN" ~/backup

**Sync specified repos from Acme organization**

To get only specified repos for a particular organization use ``--repo``
option. This option is additive, and can be used multiple times.:

.. code-block:: bash

   $ gstore --org Acme --repo Acme:foo --repo Acme:bar \
       --token "$TOKEN" ~/backup

**Sync all repos from Foo, Bar and Baz organizations**

To get repositories from specific organizations, list each of them on the
command line using the option ``--org`` as follows:

.. code-block:: bash

   $ gstore --token "$TOKEN" --org Foo --org Bar --org Baz ~/backup

Option ``--org`` is additive, and can be used multiple times.

Logging
-------

All informational and error messages produced by Gstore are sent directly to
the standard OS streams. Gstore doesn't have any special tools/options to setup
logging to files. Such design was chosen deliberately to not increase Gstore
complexity in those aspects where this is not clearly necessary, and also to
simplify its administration by end users.

So, informational and error messages produced by Gstore are sent to two
separate streams:

* The regular output is sent to standard output stream (``STDOUT``)
* The error messages and the warning ones are sent to standard error stream
  (``STDERR``)

The format of the messages generated by Gstore was chosen in such a way as to
preserve human readability, but at the same time to allow specialized tools to
parse message entries according to a single template.

Let's look at a few examples to demonstrate the above:

.. code-block:: bash

   # All messages are visible
   $ gstore ~/backup

   # Only informational message are visible
   $ gstore ~/backup 2>/dev/null

   # Only error messages and warnings are visible
   $ gstore ~/backup 1>/dev/null

   # Store logs separately
   $ gstore ~/backup > info.log 2> err.log

   # Store all the logs in the same file
   $ gstore ~/backup > gstore.log 2>&1

You can control the logging level using the following options:

``-v``, ``--verbose``
  Enable verbose mode. Causes Gstore to print debugging messages about its
  progress in some cases.

``-q``, ``--quiet``
  Silence any informational messages except error ones.

Using Github Enterprise
~~~~~~~~~~~~~~~~~~~~~~~

There is nothing special when working with the Github Enterprise, except for
the host and possible environment variables.:

.. code-block:: bash

   # Using command line options to configure Gstore
   $ gstore --token "secret" --host "github.example.com" ~/backup

   # Using environment variables to configure Gstore
   $ export GH_ENTERPRISE_TOKEN="secret"
   $ export GH_HOST="github.example.com"
   $ gstore ~/backup


.. -support-

Support
-------

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the Gstore, please
`open an issue <https://github.com/sergeyklay/gstore/issues>`_.


.. -project-information-

Project Information
-------------------

Gstore is released under the `GNU General Public Licence version 3 <https://choosealicense.com/licenses/gpl-3.0/>`_,
its documentation lives at `Read the Docs <https://gstore.readthedocs.io/>`_,
the code on `GitHub <https://github.com/sergeyklay/gstore>`_,
and the latest release on `PyPI <https://pypi.org/project/gstore/>`_.
It’s rigorously tested on Python 3.7+.

If you'd like to contribute to Gstore you're most welcome!

.. -similar-projects-

Similar projects
----------------

There are some projects similar to Gstore you may be interested in:

* https://github.com/kennethreitz42/ghsync
* https://github.com/lgg/simple-git-mirror-sync
