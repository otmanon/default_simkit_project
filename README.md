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
| `demos/`       | Interactive demo scripts — they render, they don't write output        |
| `experiments/` | Experiment scripts, one file per experiment                            |
| `lib/`         | Project utility code and classes shared by both                        |
| `results/`     | Default output root for experiments — gitignored                       |

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

Then install SimKit and this project, both editable — so edits under
`deps/simkit/` take effect immediately and `import lib` works from any directory:

```bash
conda create -n default_simkit_project python=3.11
conda activate default_simkit_project
pip install -e "deps/simkit[all]" -e .
```

Order matters only in that SimKit must come from `deps/simkit`, never PyPI; this
project declares no dependency on it precisely so a released copy can't shadow the
submodule.

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

## Experiments and demos

Both are plain folders of scripts — one file each, no packages, nothing to invoke
through `-m`. Because the project is installed editable, they run directly:

```bash
python experiments/my_experiment.py
python demos/my_demo.py
```

**Experiments** measure something and persist it. They write to `results/`, by
default a subfolder named after the script; `results_path()` creates it for you:

```python
from lib import data_path, results_path

mesh = data_path("3d", "bunny.obj")                 # <repo>/data/3d/bunny.obj
out  = results_path("my_experiment", "energy.png")  # <repo>/results/my_experiment/...
```

`results/` is gitignored end to end — commit the script and the conclusions, not
the artifacts.

**Demos** show something. They open an interactive viewer (polyscope) and store
nothing, so a demo script should not import `results_path` at all; if you find
yourself saving frames or arrays from one, it has become an experiment and belongs
in `experiments/`.

```python
from lib import data_path
import polyscope as ps

ps.init()
# ... register geometry, set callbacks ...
ps.show()
```

Shared helpers for either go in `lib/`, whose paths resolve relative to the repo
root regardless of cwd. Keep those types flat — plain functions and shallow
dataclasses, not deep hierarchies.
