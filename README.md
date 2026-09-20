# default_simkit_project

A template research project built on [SimKit](https://github.com/otmanon/simkit), a
physics-based animation library. SimKit is vendored as a **submodule** rather than a
pip dependency so that library changes needed by an experiment can be made in place,
on a branch owned by this project.

## Layout

| Path           | Holds                                                                  |
| -------------- | ---------------------------------------------------------------------- |
| `data/`        | Meshes, images and other assets used by this project (`2d/`, `3d/`)     |
| `deps/simkit/` | SimKit, as a recursive submodule tracking the `default_simkit_project` branch |
| `experiments/` | Experiment scripts, one file per experiment                            |
| `lib/`         | Project utility code and classes shared across experiments             |
| `results/`     | Default output root — everything written here is gitignored            |

## Setup

Clone with submodules — SimKit itself vendors `simkit-data`, so `--recursive` matters:

```bash
git clone --recursive https://github.com/otmanon/default_simkit_project.git
cd default_simkit_project
```

Already cloned without it:

```bash
git submodule update --init --recursive
```

Then install SimKit in editable mode, so edits under `deps/simkit/` take effect
immediately:

```bash
conda create -n default_simkit_project python=3.11
conda activate default_simkit_project
pip install -e "deps/simkit[all]"
```

SimKit's base install needs only `numpy` and `scipy`; `[all]` adds meshing, viz
(`libigl`, `matplotlib`, `polyscope`), solvers, video and CMA-ES. Swap in narrower
extras (`[mesh,viz]`) if you don't need everything — see
[`deps/simkit/README.md`](deps/simkit/README.md) for the full table.

## Editing SimKit from here

`deps/simkit` is checked out on the `default_simkit_project` branch, not `main`, so
library changes made for this project stay separated from upstream:

```bash
cd deps/simkit
# ... edit ...
git commit -am "Describe the library change"
git push origin default_simkit_project
```

Then record the new submodule pointer in this repo:

```bash
cd ../..
git add deps/simkit
git commit -m "Bump simkit"
```

A change that isn't specific to this project belongs upstream on `main` instead —
prefer that when the experiment doesn't depend on it.

## Running an experiment

`experiments/` is a plain folder of scripts — one file per experiment, no package.
Run them from the repository root with the root on `PYTHONPATH`, so `import lib`
resolves:

```bash
PYTHONPATH=. python experiments/my_experiment.py
```

Shared helpers go in `lib/`, which resolves paths relative to the repo root
regardless of where a script is run from:

```python
from lib import data_path, results_path

mesh = data_path("3d", "bunny.obj")              # <repo>/data/3d/bunny.obj
out  = results_path("my_experiment", "energy.png")  # <repo>/results/my_experiment/...
```

Write outputs to `results/`, by default under a subfolder named after the script;
`results_path()` creates that subfolder for you. The whole tree is gitignored —
commit the script and the conclusions, not the artifacts.

Keep `lib/` types flat — plain functions and shallow dataclasses, not deep
hierarchies.
