=================================================
Gstore: Synchronize GitHub repositories made easy
=================================================

Release v\ |release| (`What's new? <changelog>`).

.. include:: ../README.rst
   :start-after: teaser-begin
   :end-before: teaser-end

Getting Started
===============

Requirements
~~~~~~~~~~~~

* `Python <https://www.python.org/>`_ >= 3.7
* `Git <https://git-scm.com/>`_ >= 1.7.0

Installing Gstore
~~~~~~~~~~~~~~~~~

Gstore is a Python-only package `hosted on PyPI <https://pypi.org/project/gstore/>`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a virtualenv:

.. code-block:: console

   $ python -m pip install gstore

The command ``gstore`` will be available to you from the command line.

The master of all the material is the Git repository at
https://github.com/sergeyklay/gstore. So, you can install development version from the repo as follows:

.. code-block:: bash

   $ pip install -e git://github.com/sergeyklay/gstore.git#egg=gstore

This command will download the latest version of Gstore from the
`Python Package Index <https://pypi.org/project/gstore/>`_ and install it to your system.

.. note::
   The ``master`` branch will always contain the latest unstable version. If you
   wish to check older versions or formal, tagged release, please switch to the
   relevant `tag <https://github.com/sergeyklay/gstore/tags>`_.

More information about ``pip`` and PyPI can be found here:

* `Install pip <https://pip.pypa.io/en/latest/installing/>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_

Alternatively, you can install from the source as follows:

#. Clone `Gstore repository <https://github.com/sergeyklay/gstore>`_
#. Run ``pip install -r requirements.txt``
#. Run the ``gstore`` module (directory) as follows:

.. code-block:: bash

   $ python -m gstore --help


.. include:: ../README.rst
   :start-after: -support-
   :end-before: -project-information-

.. include:: ../README.rst
   :start-after: -similar-projects-

----


Full Table of Contents
======================

.. toctree::
   :maxdepth: 2

   overview
   usage
   logging

.. include:: ../README.rst
   :start-after: -project-information-
   :end-before: -similar-projects-

.. toctree::
   :maxdepth: 1

   license
   changelog


Indices and tables
==================

* `genindex`
* `search`
