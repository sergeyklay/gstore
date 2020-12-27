Gstore
======

Gstore is a simple tool to synchronize GitHub repositories of your organizations.

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

Typical use case
~~~~~~~~~~~~~~~~

Install
-------

Requirements
~~~~~~~~~~~~

* Python_ >= 3.6.7
* Git_ >= 1.7.0

Installing Gstore
~~~~~~~~~~~~~~~~~

Installing Gstore is easily done using pip_. Assuming it is installed, just run
the following from the command-line:

.. code-block:: bash

   $ pip install gstore

The master of all the material is the Git repository at
https://github.com/sergeyklay/gstore . So, you can install development version
from the repo as follows:

.. code-block:: bash

   $ pip install -e git://github.com/sergeyklay/gstore.git#egg=gstore

This command will download the latest version of Gstore from the
`Python Package Index`_ and install it to your system. The command ``gstore``
will be available to you from the command line.

.. note::
   The master branch will always contain the latest unstable version. If you
   wish to check older versions or formal, tagged release, please switch to the
   relevant tag_.

More information about ``pip`` and PyPI can be found here:

* `Install pip`_
* `Python Packaging User Guide`_

Alternatively, you can install from the source as follows:

#. Clone `Gstore repository`_
#. Run ``pip install -r requirements.txt``
#. Run the ``gstore`` module (directory) as follows:

.. code-block:: bash

   $ python -m gstore --help

Quick Start
---------------

#. Generate a GitHub `Personal Access Token`_ with the following permissions:

   * ``repo``: Full control of private repositories

   * ``user:read``: Read all user profile data

#. Save the token in a safe place; you'll need it when use Gstore

#. Sync your repos:

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup

Usage
-----

::

   gstore [<options>] [[--] target]

**Options:**

``-h``, ``--help``
  Show help message and exit.

``--token TOKEN``
  An authentication token for GitHub API requests. If not provided via CLI
  argument, then environment variable will be used. The order of searching for
  a token in environment variables as follows (in order of precedence):

  #. ``GH_TOKEN``, ``GITHUB_TOKEN``
  #. ``GH_ENTERPRISE_TOKEN``, ``GITHUB_ENTERPRISE_TOKEN``

  Setting these variables allows you not to not pass token directly via CLI
  argument and avoids storing it in the Shell history.

``--host HOST``
  The GitHub API hostname. If not provided via CLI argument, then ``GH_HOST``
  environment variable will be used. If environment variable is not set,
  ``api.github.com`` will be used.

``--org ORG [ORG ...]``
  Organizations you have access to (by default all).

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
  Base target to sync repos (e.g. folder on disk). If not provided via argument
  environment variable ``GSTORE_DIR`` will be used. If there is not environment
  variable current working directory will be used.

Examples
~~~~~~~~

**Sync all repos from all organizations**

The example below will perform 2 API requests. The first is to obtain GitHub
username, and the second one to get a list of user's organizations. At the end
Gstore will sync repositories of organizations via Git.

.. code-block:: bash

   $ gstore --token "$TOKEN" ~/backup

Unless you set the ``GSTORE_DIR`` environment variable and don't provide
*target directory*, Gstore will sync all the repositories to current working
directory.:

.. code-block:: bash

   # Will sync all the repositories to current working directory
   $ gstore --token "$TOKEN"

   # Will sync all the repositories to ~/work directory
   $ export GSTORE_DIR=~/work
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

To specify a *target directory* right after organization list use double dash
to signify the end of ``--org`` option.:

.. code-block:: bash

   $ gstore --token "$TOKEN" --org Acme -- ~/backup

**Sync all repos from Foo, Bar and Baz organizations**

To get all repositories of the listed organizations, specify them separated by
a space:

.. code-block:: bash

   $ gstore --token "$TOKEN" --org Foo Bar Baz -- ~/backup

Using Github Enterprise
~~~~~~~~~~~~~~~~~~~~~~~

There is nothing special when working with the Github Enterprise, except for
the host and possible environment variables.:

.. code-block:: bash

   # Using CLI arguments to configure Gstore
   $ gstore --token "secret" --host "example.com/api/v3" ~/backup

   # Using environment variables to configure Gstore
   $ export GH_ENTERPRISE_TOKEN="secret"
   $ export GH_HOST="example.com/api/v3"
   $ gstore ~/backup

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
   $ gstore ~/work

   # Only informational message are visible
   $ gstore ~/work 2>/dev/null

   # Only error messages and warnings are visible
   $ gstore ~/work 1>/dev/null

   # Store logs separately
   $ gstore ~/work > info.log 2> err.log

   # Store all the logs in the same file
   $ gstore ~/work > gstore.log 2>&1

You can control the logging level using the following arguments:

``-v``, ``--verbose``
  Enable verbose mode. Causes Gstore to print debugging messages about its
  progress in some cases.

``-q``, ``--quiet``
  Silence any informational messages except error ones.

Similar projects
----------------

There are some projects similar to Gstore you may be interested in:

* https://github.com/kennethreitz42/ghsync
* https://github.com/adw0rd/github-sync

Support
-------

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the Gstore, please `open an issue`_.

Changes
-------

To see what has changed in recent versions of Gstore see `CHANGELOG.rst`_.

License
-------

This project is open source software licensed under the
`GNU General Public Licence version 3`_.  © 2020 `Serghei Iakovlev`_

.. _tag: https://github.com/sergeyklay/gstore/tags
.. _Python: https://www.python.org/
.. _Git: https://git-scm.com/
.. _pip: https://pip.pypa.io/en/latest/installing.html
.. _Python Package Index: http://pypi.python.org/pypi/GitPython
.. _Install pip: https://pip.pypa.io/en/latest/installing/
.. _Python Packaging User Guide: https://packaging.python.org/
.. _Personal Access Token: https://github.com/settings/tokens
.. _gstore repository: https://github.com/sergeyklay/gstore
.. _CHANGELOG.rst: https://github.com/sergeyklay/gstore/blob/master/CHANGELOG.rst
.. _open an issue: https://github.com/sergeyklay/gstore/issues
.. _`Serghei Iakovlev`: https://github.com/sergeyklay
.. _GNU General Public Licence version 3: https://github.com/sergeyklay/gstore/blob/master/LICENSE
