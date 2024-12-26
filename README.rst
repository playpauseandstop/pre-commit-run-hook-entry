=========================
pre-commit-run-hook-entry
=========================

.. image:: https://github.com/playpauseandstop/pre-commit-run-hook-entry/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/playpauseandstop/pre-commit-run-hook-entry/actions/workflows/ci.yml
    :alt: CI

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

.. image:: https://img.shields.io/pypi/v/pre-commit-run-hook-entry.svg
    :target: https://pypi.org/project/pre-commit-run-hook-entry/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/pre-commit-run-hook-entry.svg
    :target: https://pypi.org/project/pre-commit-run-hook-entry/
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/pre-commit-run-hook-entry.svg
    :target: https://github.com/playpauseandstop/pre-commit-run-hook-entry/blob/main/LICENSE
    :alt: BSD License

.. image:: https://coveralls.io/repos/playpauseandstop/pre-commit-run-hook-entry/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/playpauseandstop/pre-commit-run-hook-entry
    :alt: Coverage

Run `pre-commit`_ hook entry. Allow to run pre-commit hooks for text editor
formatting / linting needs.

.. _`pre-commit`: https://pre-commit.com/

Danger Zone
===========

**IMPORTANT:** This is highly experimental tool as `pre-commit internals does
not intend to be used in other scripts
<https://github.com/pre-commit/pre-commit/issues/1468#issuecomment-640699437>`_.
It might be broken after new pre-commit release.

**TO USE WITH CAUTION!**

Requirements
============

- `Python <https://www.python.org/>`_ 3.9 or later
- `pre-commit`_ 4.0 or later

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

    pre-commit-run-hook-entry HOOK [ARGS]
    pre-commit-which-hook-entry HOOK

Prerequisites
-------------

``pre-commit-run-hook-entry`` only works in directories, where
``pre-commit run --all HOOK`` is executable.

pre-commit Versions Support
---------------------------

================================= ===================
pre-commit-run-hook-entry version pre-commit version
================================= ===================
``1.0.0b0`` or lower              ``3.8.0`` or lower
``1.0.0rc0`` or higher            ``4.0.0`` or higher
================================= ===================

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

isorted
~~~~~~~

.. code-block:: json

    {
        "isorted.isort_command": ["pre-commit-run-hook-entry", "isort"]
    }

sublack
~~~~~~~

From one point `sublack <https://github.com/jgirardet/sublack/>`__ has builtin
pre-commit integration, but it seems do not respect settings from
``pyproject.toml``, to fix this use ``pre-commit-run-black-entry`` as
``sublack.black_command``,

.. code-block:: json

    {
        "sublack.black_command": "pre-commit-run-black-entry"
    }


SublimeLinter-flake8
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "SublimeLinter.linters.flake8.executable": "pre-commit-run-hook-entry",
        "SublimeLinter.linters.flake8.args": ["--", "flake8"]
    }


SublimeLinter-contrib-mypy
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "SublimeLinter.linters.mypy.executable": "pre-commit-run-hook-entry",
        "SublimeLinter.linters.mypy.args": ["--", "mypy"]
    }

SublimeJsPrettier
~~~~~~~~~~~~~~~~~

First, you need to find out path to prettier hook entry with,

.. code-block:: bash

    pre-commit-which-hook-entry prettier

Then, paste command output (``<OUTPUT>``) into plugin config,

.. code-block:: json

    {
        "js_prettier": {
            "prettier_cli_path": "<OUTPUT>"
        }
    }

SublimeLinter-eslint
~~~~~~~~~~~~~~~~~~~~

First, you need to find out path to eslint hook entry with,

.. code-block:: bash

    pre-commit-which-hook-entry eslint

Then, paste command output (``<OUTPUT>``) into plugin config,

.. code-block:: json

    {
        "SublimeLinter.linters.eslint.executable": "<OUTPUT>",
        "SublimeLinter.linters.eslint.env": {
            "NODE_PATH": "<OUTPUT>/../../lib/node_modules"
        }
    }

**IMPORTANT:** If you're using any ``additionalDependencies`` for eslint hook,
you need to configure ``NODE_PATH``, so plugin will be able to find out given
dependencies.

Issues & Feature Requests
=========================

Feel free to submit new issue or feature request `at GitHub
<https://github.com/playpauseandstop/pre-commit-run-hook-entry/issues>`_
