"""Experiments.

Each experiment is a self-contained subfolder, e.g.::

    experiments/
        my_experiment/
            __init__.py
            run.py       # entry point: `python -m experiments.my_experiment.run`
            README.md    # what it asks, how to run it, what it produced

Shared code does not belong here -- it belongs in ``lib/``. Outputs
(``results/``, renders, ``.npz`` caches) are gitignored; commit the script and
the conclusions, not the artifacts.
"""
