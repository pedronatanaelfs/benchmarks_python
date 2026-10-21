# fairmoo_benchmarks

Python / NumPy / [pymoo](https://pymoo.org) implementations of **multi-party multi-objective optimization (MPMOP)** benchmarks for research on fairness, consensus, and preference-aware search among multiple decision makers (DMs).

## What this repository is

In standard multi-objective optimization, one decision maker faces several conflicting objectives. In **multi-party** problems, several DMs share the same decision variables, but each DM has their own objective vector and (often) their own Pareto set. Algorithms and metrics must therefore reason about:

- per-DM objective ownership,
- common vs. disjoint Pareto sets,
- compromise / concession among parties,
- fair evaluation of approximation quality across DMs.

This repository provides a **source-traced Python port** of the main synthetic suites used in that literature, with numerical and analytical validation reported **benchmark-by-benchmark**:

| Family | Problems | Origin |
|---|---|---|
| MPMOP | MPMOP1–MPMOP17 | Liu et al. (CEC 2020) + Zhao et al. (2026) extensions |
| MPDMP | MPDMP1–MPDMP18 | She et al. (2023) + Zhao et al. (2026) extensions |

### Validation status (current)

| Status | Count | Notes |
|---|---|---|
| **PASS** | 33 | Objectives and safely executable PS/PF outputs match licensed MATLAB |
| **PARTIAL** | 2 | MPMOP4/9 objectives pass; original `true_PS.m` uses an unsafe 20000×20000 mesh |
| **NEEDS_MANUAL_VERIFICATION** | 0 | — |
| **FAIL** | 0 | — |

Objective equivalence is **PASS 35/35**. PS/PF equivalence is **PASS 33/33**
for every safely executable MATLAB reference. See
`validation/equivalence_matrix.md` and `validation/reports/`.

## What it does

- Implements all **35** benchmarks with vectorized NumPy evaluation
- Exposes a uniform API (`get_problem`, `evaluate`, `evaluate_dm`, Pareto set / reference points when known)
- Preserves **which objectives belong to which DM** (essential for fairness research) via `CommonPSStatus` and DM objective slices
- Provides a **pymoo adapter** that concatenates objectives for standard MOEAs (NSGA-II/III, etc.), while keeping the multi-DM view on the base problem
- Ships unit tests, analytical checks, optional Octave equivalence, source mapping, and validation artifacts under `docs/` and `validation/`

Example workflow:

```python
problem = get_problem("MPDMP17")
F = problem.evaluate(X)           # all objectives concatenated
F_dm1 = problem.evaluate_dm(X, 0) # only DM1's objectives
```

## What it does not do (yet)

This release focuses on **correct benchmarks**, not on fairness metrics or
solvers. It includes the MPDMP reference concession-case table, but does
**not** implement satisfaction/ROI models, Nash-product indicators,
preference elicitation, or optimization algorithms.

Scientific correctness is prioritized over completeness. Ambiguous details are marked `NEEDS_MANUAL_VERIFICATION` or `PARTIAL` in the documentation — they are never invented silently.

## Installation (Conda / Miniconda)

Conda is the recommended environment manager for this project.

```bash
cd benchmarks_python   # repository root

conda env create -f environment.yml
conda activate fairmoo-benchmarks
```

Refresh an existing environment:

```bash
conda env update -f environment.yml --prune
```

Verify the install:

```bash
python -c "from fairmoo_benchmarks import get_problem; print(get_problem('MPDMP13').n_dm)"
pytest -q
```

### Windows

In **Anaconda Prompt** or PowerShell (with conda initialized):

```powershell
cd path\to\benchmarks_python
conda env create -f environment.yml
conda activate fairmoo-benchmarks
```

### Linux / macOS (if `conda` is not on `PATH`)

```bash
source "$HOME/miniconda3/etc/profile.d/conda.sh"
# or: eval "$("$HOME/miniconda3/bin/conda" shell.bash hook)"

conda activate fairmoo-benchmarks
```

Initialize conda for new shells:

```bash
conda init bash   # or: conda init zsh
```

## Quick start

```python
from fairmoo_benchmarks import get_problem
import numpy as np

problem = get_problem("MPDMP17")
print(problem.n_dm, problem.n_obj_per_dm)

rng = np.random.default_rng(42)
X = rng.uniform(problem.xl, problem.xu, size=(32, problem.n_var))
F = problem.evaluate(X)            # shape (32, sum(n_obj_per_dm))
F_dm1 = problem.evaluate_dm(X, 0)  # DM1 objectives only

for dm in range(problem.n_dm):
    Fm = problem.evaluate_dm(X, dm)
    print(dm, Fm.shape)
```

## pymoo integration

`PymooMultiPartyAdapter` concatenates all party-wise objectives into a single
pymoo `Problem` (required by standard MOEAs). Multi-DM ownership remains
available on the base object:

```python
from fairmoo_benchmarks import get_problem
from fairmoo_benchmarks.pymoo import PymooMultiPartyAdapter

base = get_problem("MPDMP13")
pymoo_problem = PymooMultiPartyAdapter(base)

# still available:
base.evaluate_dm(X, dm=1)
pymoo_problem.base.evaluate_dm(X, dm=1)
```

Examples:

- `examples/run_nsga2.py`
- `examples/run_nsga3.py`
- `examples/visualize_mpdmp.py`
- `examples/evaluate_by_dm.py`

## Registry

```python
from fairmoo_benchmarks import list_problems, describe_problem, get_problem

list_problems()
describe_problem("MPDMP17")
```

## Benchmark sources

Vendored under `sources/`:

| Suite | Primary source |
|---|---|
| MPMOP1–11 | Liu et al., IEEE CEC 2020 + [OptMPNDS](https://github.com/lwjie595/OptMPNDS) |
| MPDMP1–12 | She et al., 2023 + [2022SheOptMPNDS3](https://github.com/MiLabHITSZ/2022SheOptMPNDS3) |
| MPMOP12–17, MPDMP13–18 | Zhao et al., 2026 ([arXiv:2601.22497](https://arxiv.org/abs/2601.22497)) plus supplied executable MATLAB repository |

Traceability: `docs/source_mapping.md`, `docs/mathematical_validation.md`,
and the generated artifacts under `validation/`.

## Tests and validation

```bash
conda activate fairmoo-benchmarks
pytest -q
```

Artifacts:

- `validation/validation_report.md` (current MATLAB equivalence report)
- `validation/audit_final.md` (current 33 PASS / 2 PARTIAL)
- `validation/audit_before.md` (historical 2026-10-03 snapshot only)
- `validation/equivalence/` (MPMOP1–11 vs Octave)
- `validation/audits/` (per-benchmark KEEP/FIX decisions)
- `validation/reference_values/`
- `validation/matlab/results/` (licensed-MATLAB objective references)
- `validation/matlab/pareto_results/` (licensed-MATLAB PS/PF references)
- `validation/reports/numerical_comparison.csv`
- `validation/reports/pareto_comparison.csv`
- `validation/test_summary.txt`

GNU Octave is **optional** for normal use. When installed, MPMOP1–11 can be
cross-checked against author `MPMOP_Value.m` via
`validation/matlab_octave/run_mpmop_equivalence.py`.
MPDMP PlatEMO classdefs are `OCTAVE_INCOMPATIBLE` (no `nsidedpoly` / PROBLEM base).

## Citation

If you use this package, please cite the **original benchmark papers** listed
above (Liu/She/Zhao et al.) and this Python port repository.

Machine-readable citation metadata: [`CITATION.cff`](CITATION.cff).

## License

MIT — see `LICENSE`.
