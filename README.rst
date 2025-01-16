=============
ZPRP FFmpeg 2
=============

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |github-actions| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/zprp-ffmpeg2/badge/?style=flat
    :target: https://readthedocs.org/projects/zprp-ffmpeg2/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/kraskoa/zprp-ffmpeg2/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/kraskoa/zprp-ffmpeg2/actions

.. |codecov| image:: https://codecov.io/gh/ffmpeg-zprp/zprp-ffmpeg/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/gh/kraskoa/zprp-ffmpeg2

.. |version| image:: https://img.shields.io/pypi/v/zprp-ffmpeg2.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/zprp-ffmpeg2

.. |wheel| image:: https://img.shields.io/pypi/wheel/zprp-ffmpeg2.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/zprp-ffmpeg2

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/zprp-ffmpeg2.svg
    :alt: Supported versions
    :target: https://pypi.org/project/zprp-ffmpeg2

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/zprp-ffmpeg2.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/zprp-ffmpeg2

.. |commits-since| image:: https://img.shields.io/github/commits-since/kraskoa/zprp-ffmpeg2/v1.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/kraskoa/zprp-ffmpeg2/compare/v1.0.0...main



.. end-badges

Implementation of the successor to the ffmpeg-python library

* Free software: MIT license

============
Installation
============

The package is available on pip::

    pip install zprp_ffmpeg2

===============
Getting started
===============

A minimal example showing basic usage of the library:

.. code-block:: python

    import zprp_ffmpeg2 as ffmpeg
    stream = ffmpeg.input("input.mp4")
    stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, "output.mp4")
    ffmpeg.run(stream)

Check out more `examples <https://github.com/kraskoa/zprp-ffmpeg2/tree/main/examples>`_

Further documentation is available `here <https://zprp-ffmpeg2.readthedocs.io/en/latest/>`_

===========
Development
===========

Project uses poetry for package management. Check out their `docs <https://python-poetry.org/docs/>`_ for installation steps.
Tests are managed by tox, which uses pytest under the hood.


To install package in development mode, enter the virtual environment managed by poetry, then use `install` command:

.. code-block:: bash

    poetry shell
    poetry install --with="typecheck"

To run tests on multiple python interpreters, build documentation, check for linting issues, run:

.. code-block:: bash

    tox

However, this might be cumbersome, since it requires having all supported python interpreters available.
To run only selected interpreters, use :code:`-e` option, for example:

.. code-block:: bash

    tox -e py312-lin,check #python 3.12 on linux, and linter checks

You can view all defined interpreters with :code:`tox -l`

To check for typing and linting issues manually, run:

.. code-block:: bash

    mypy src
    pre-commit run --all-files
