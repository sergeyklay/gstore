============
Installation
============

Requirements
============

* `Python <https://www.python.org/>`_ >= 3.8
* `Git <https://git-scm.com/>`_ >= 1.7.0

Installing gstore
=================

``gstore`` is a Python-only package `hosted on PyPI <https://pypi.org/project/gstore/>`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a virtualenv:

.. code-block:: console

   $ python -m pip install gstore

The command ``gstore`` will be available to you from the command line.

Unstable version
================

The master of all the material is the Git repository at https://github.com/sergeyklay/gstore.
So, can also install the latest unreleased development version directly from the ``main`` branch on GitHub.
It is a work-in-progress of a future stable release so the experience might be not as smooth.:

.. code-block:: bash

   $ python -m pip install -e git+ssh://git@github.com/sergeyklay/gstore.git#egg=gstore

This command will download the latest version of ``gstore`` from the
`Python Package Index <https://pypi.org/project/gstore/>`_ and install it to your system.

.. note::
   The ``main`` branch will always contain the latest unstable version, so the experience
   might be not as smooth. If you wish to check older versions or formal, tagged release,
   please switch to the relevant `tag <https://github.com/sergeyklay/gstore/tags>`_.

Verify that now we have the current development version, for example:

.. code-block:: bash

   $ gstore --version
   # gstore 0.7.0
   # Copyright (C) 2020-2024 Serghei Iakovlev.
   # This is free software; see the source for copying conditions. There is NO
   # warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

More information about ``pip`` and PyPI can be found here:

* `Install pip <https://pip.pypa.io/en/latest/installation/>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_
