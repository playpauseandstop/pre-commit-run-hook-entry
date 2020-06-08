=========================
pre-commit-run-hook-entry
=========================

Run `pre-commit`_ hook entry. Allow to run pre-commit hooks for text editor
formatting / linting needs.

.. _`pre-commit`: https://pre-commit.com/

Requirements
============

- `Python <https://www.python.org/>`_ 3.6.1 or later
- `pre-commit`_ 2.4.0 or later

License
=======

``pre-commit-run-hook-entry`` is licensed under the terms of
`BSD-3-Clause </LICENSE>`_ license.

Installation
============

.. code-block:: bash

    pip install pre-commit-run-hook-entry

Usage
=====

.. code-block:: bash

    pre-commit-run-hook-entry <hook>

Prerequisites
-------------

``pre-commit-run-hook-entry`` only works in directories, where
``pre-commit run --all <hook>`` is executable.

VS Code Integration
-------------------

Example below illustrates how to configure VS Code to use black, flake8 &
mypy pre-commit hooks for formatting & linting,

.. code-block:: json

    {
        "python.formatting.provider": "black",
        "python.formatting.blackPath": "pre-commit-run-hook-entry",
        "python.formatting.blackArgs": ["black"],
        "python.linting.enabled": true,
        "python.linting.flake8Enabled": true,
        "python.linting.flake8Path": "pre-commit-run-hook-entry",
        "python.linting.flake8Args": ["flake8"],
        "python.linting.mypyEnabled": true,
        "python.linting.mypyPath": "pre-commit-run-hook-entry",
        "python.linting.mypyArgs": ["mypy"]
    }

Sublime Text 3 Integration
--------------------------

sublack
~~~~~~~

From one point `sublack <https://github.com/jgirardet/sublack/>`_ has builtin
pre-commit integration, but it seems do not respect settings from
``pyproject.toml``, to fix this use ``pre-commit-run-black-entry`` as
``sublack.black_command``,

.. code-block:: json

    {
        "sublack.black_command": "pre-commit-run-black-entry"
    }


SublimeLinter-contrib-flake8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "SublimeLinter.linters.flake8.executable": "pre-commit-run-hook-entry",
        "SublimeLinter.linters.flake8.args": ["--", "flake8"],
    }


SublimeLinter-contrib-mypy
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "SublimeLinter.linters.mypy.executable": "pre-commit-run-hook-entry",
        "SublimeLinter.linters.mypy.args": ["--", "mypy"],
    }

Issues & Feature Requests
=========================

`playpauseandstop/pre-commit-run-hook-entry @ GitHub
<https://github.com/playpauseandstop/pre-commit-run-hook-entry/issues>`_
