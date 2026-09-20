"""Project-local utility library.

Everything reusable across ``experiments/`` lives here: loaders, subspace
builders, plotting helpers, small dataclasses holding run configuration.

Convention
----------
Types are kept *flat*. A module exposes plain functions and shallow
dataclasses rather than deep inheritance hierarchies -- if a helper needs a
variant, prefer another function or an extra field over a subclass.

Usage
-----
Experiments import from the package root::

    from lib import data_path

so re-export the public surface of each new module here.
"""

from pathlib import Path

__all__ = ["ROOT", "DATA_DIR", "DEPS_DIR", "EXPERIMENTS_DIR", "data_path"]

#: Repository root, resolved from this file so it works from any cwd.
ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
DEPS_DIR = ROOT / "deps"
EXPERIMENTS_DIR = ROOT / "experiments"


def data_path(*parts: str) -> Path:
    """Return an absolute path inside ``data/``.

    ``data_path("3d", "bunny.obj")`` -> ``<repo>/data/3d/bunny.obj``.
    """
    return DATA_DIR.joinpath(*parts)
