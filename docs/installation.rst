.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Sqlite3Wrapper, run this command in your terminal:

.. code-block:: console

    $ pip install sqlite3wrapper

This is the preferred method to install Sqlite3Wrapper, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From poetry
--------------

To install Sqlite3Wrapper via poetry, add the following line in pyproject.toml:

.. code-block:: console

    [tool.poetry.dependencies]
    ...
    sqlite3wrapper = {git = "https://github.com/seokwangwoo/sqlite3wrapper"}

Then, you can install it with:

.. code-block:: console

    $ poetry install


From source
-----------

The source for Sqlite3Wrapper can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/seokwangwoo/sqlite3wrapper

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/seokwangwoo/sqlite3wrapper/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .

.. _Github repo: https://github.com/seokwangwoo/sqlite3wrapper
.. _tarball: https://github.com/seokwangwoo/sqlite3wrapper/tarball/master
