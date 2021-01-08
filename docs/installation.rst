============
Installation
============

Requirements
============

* `Python <https://www.python.org/>`_ >= 3.7
* `Git <https://git-scm.com/>`_ >= 1.7.0

Installing Gstore
=================

Gstore is a Python-only package `hosted on PyPI <https://pypi.org/project/gstore/>`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a virtualenv:

.. code-block:: console

   $ python -m pip install gstore

The command ``gstore`` will be available to you from the command line.

Unstable version
================

The master of all the material is the Git repository at https://github.com/sergeyklay/gstore.
So, can also install the latest unreleased development version directly from the ``master`` branch on GitHub.
It is a work-in-progress of a future stable release so the experience might be not as smooth.:

.. code-block:: bash

   $ pip install -e git://github.com/sergeyklay/gstore.git#egg=gstore
   # OR
   $ pip install --upgrade https://github.com/sergeyklay/gstore.git/archive/master.tar.gz

This command will download the latest version of Gstore from the
`Python Package Index <https://pypi.org/project/gstore/>`_ and install it to your system.

.. note::
   The ``master`` branch will always contain the latest unstable version, so the experience
   might be not as smooth. If you wish to check older versions or formal, tagged release,
   please switch to the relevant `tag <https://github.com/sergeyklay/gstore/tags>`_.

Verify that now we have the current development version identifier with the ``.dev`` suffix,
for example:

.. code-block:: bash

   $ gstore --version
   # gstore 0.3.1.dev1
   # Copyright (C) 2020, 2021 Serghei Iakovlev.
   # This is free software; see the source for copying conditions. There is NO
   # warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

More information about ``pip`` and PyPI can be found here:

* `Install pip <https://pip.pypa.io/en/latest/installing/>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_

Alternatively, you can install from the source as follows:

#. Clone `Gstore repository <https://github.com/sergeyklay/gstore>`_
#. Run ``pip install -r requirements.txt``
#. Run the ``gstore`` module (directory) as follows:

.. code-block:: bash

   $ python -m gstore --version
