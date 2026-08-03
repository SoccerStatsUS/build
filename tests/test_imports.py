"""Every stage module must import cleanly.

Cheap insurance for the wiring rather than the behaviour. make/ modules import
each other flat because the build runs as `python make/`, which is easy to break
from outside: a stale `import main` in make/__init__.py once made the whole
package unimportable while the build itself kept working.
"""

import importlib

import pytest

# The build order from README.md, plus what those stages pull in.
STAGES = ['load', 'normalize', 'lift', 'transform', 'merge', 'generate', 'denormalize']
SUPPORT = ['check', 'main', 'separate', 'helpers']


@pytest.mark.parametrize('name', STAGES + SUPPORT)
def test_module_imports(name):
    assert importlib.import_module(name)


def test_stages_import_in_build_order():
    # Importing them in sequence catches a circular import that importing a
    # single module in isolation can hide.
    for name in STAGES:
        importlib.import_module(name)


def test_make_is_importable_as_a_package():
    assert importlib.import_module('make')


def test_build_entry_point_exists():
    # What make/__main__.py does: `from main import build; build()`.
    main = importlib.import_module('main')
    assert callable(main.build)
