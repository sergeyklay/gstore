ghsync
======

Ghsync is a simple cli tool to synchronize organizations' repositories from GitHub.

Usage
-----

Examples
~~~~~~~~

**Sync all repos from all organizations**

.. code-block:: bash

   ghsync --token "$TOKEN" --user "$USER" -- ~/backup

**Sync all repos from Acme organization**

.. code-block:: bash

   ghsync --token "$TOKEN" --org Acme -- ~/backup

**Sync all repos from Foo, Bar and Baz organizations**

.. code-block:: bash

   ghsync --token "$TOKEN" --org Foo Bar Baz -- ~/backup

License
------

This project is open source software licensed under the GNU General Public
Licence version 3.  © 2020 Serghei Iakovlev
