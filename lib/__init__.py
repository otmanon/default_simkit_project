"""Project-local utility library.

Everything reusable across ``experiments/`` and ``demos/`` lives here: loaders,
subspace builders, plotting helpers, small dataclasses holding run
configuration.

Convention
----------
Types are kept *flat*. A module exposes plain functions and shallow
dataclasses rather than deep inheritance hierarchies -- if a helper needs a
variant, prefer another function or an extra field over a subclass.

Usage
-----
Scripts import from the package root::

    from lib import data_path, results_path

so re-export the public surface of each new module here. ``pip install -e .``
puts this package on ``sys.path``, so scripts run directly, from any cwd::

    python experiments/my_experiment.py
"""

from pathlib import Path

__all__ = [
    "ROOT",
    "DATA_DIR",
    "DEPS_DIR",
    "EXPERIMENTS_DIR",
    "DEMOS_DIR",
    "RESULTS_DIR",
    "data_path",
    "results_path",
]

#: Repository root, resolved from this file so it works from any cwd.
ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
DEPS_DIR = ROOT / "deps"
EXPERIMENTS_DIR = ROOT / "experiments"
DEMOS_DIR = ROOT / "demos"

#: Default output root for experiments. Everything written here is gitignored.
RESULTS_DIR = ROOT / "results"


def data_path(*parts: str) -> Path:
    """Return an absolute path inside ``data/``.

    ``data_path("3d", "bunny.obj")`` -> ``<repo>/data/3d/bunny.obj``.
    """
    return DATA_DIR.joinpath(*parts)


def results_path(*parts: str) -> Path:
    """Return an absolute path inside ``results/``, creating parent dirs.

    ``results_path("my_experiment", "energy.png")`` ->
    ``<repo>/results/my_experiment/energy.png``, with ``results/my_experiment/``
    created if it does not exist yet.
    """
    path = RESULTS_DIR.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
