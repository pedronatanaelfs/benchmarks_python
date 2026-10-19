# MATLAB ↔ Python equivalence audit

This directory is an external validation harness. It does not modify either
MATLAB source repository or the Python benchmark implementations.

## Repository architecture

- `OptMPNDS-master/Problems/MPMOP`: original MPMOP1–11 classdefs.
  Objective equations are centralized in `MPMOP_Value.m`; approximate common
  PS/PF generation is centralized in `true_PS.m`.
- `2026ZhaoNash-main/MPMOP`: MPMOP1–17 classdefs, a larger
  `MPMOP_Value.m`, and `true_PS.m`. The classes inherit `PROBLEM`, supplied
  by `OptMPNDS-master/Public`. MPMOP1–11 class files are byte-identical
  between the two repositories; Zhao extends the shared helpers and adds
  classes 12–17.
- `2026ZhaoNash-main/MPDMP`: MPDMP1–18 classdefs inheriting `MPDMP`.
  `MPDMP.CalObj` delegates to geometry objects such as `square`, `polygon`,
  `ParallelLines1`, `ThreeCorners`, and `ThreeDiagonals`.
- `src/fairmoo_benchmarks`: Python package. Registry entries for MPMOP1–11
  resolve to `mpmop/liu2020.py`; MPDMP1–12 resolve to `mpdmp/she2023.py`.
  The numbered modules for those ranges are wrappers. MPMOP12–17 and
  MPDMP13–18 have numbered implementations.

The complete file-level map is in `benchmark_mapping.csv`.

## Validation layout

```text
validation/
├── benchmark_mapping.csv
├── discrepancy_report.md
├── equivalence_matrix.md
├── generate_reference_inputs.py
├── test_inputs/                         # generated shared X matrices
├── matlab/
│   ├── run_all_matlab_reference_tests.m
│   └── results/                         # generated externally in MATLAB
├── python/
│   ├── run_python_reference_tests.py
│   └── results/                         # generated locally
├── compare/
│   └── compare_matlab_python.py
├── reports/                             # generated numerical reports
└── tests/
    └── test_benchmark_structure.py
```

## Deterministic procedure

From `benchmarks_python`:

```bash
python validation/generate_reference_inputs.py
python validation/python/run_python_reference_tests.py
pytest -q validation/tests
```

Then, in MATLAB:

```matlab
% Open benchmarks_python/validation/matlab as the Current Folder, then:
RUN_ME_IN_MATLAB
```

The MATLAB runner uses `GLOBAL`/`PROBLEM` from OptMPNDS and the benchmark
classes/helpers from `2026ZhaoNash-main`. For each benchmark it writes a CSV
containing `test_id`, the exact shared decision vector, and all objective
values, plus JSON metadata.

After MATLAB completes:

```bash
python validation/compare/compare_matlab_python.py
```

The comparator uses `rtol=1e-9`, `atol=1e-10` and reports maximum absolute
error, maximum safe relative error, MAE, the worst test/objective, both
values, and the corresponding input.

## Final audit status

All 35 MATLAB reference CSVs were generated and compared. After correcting
the Python implementation, objective evaluation passes for all 35
benchmarks at `rtol=1e-9`, `atol=1e-10`. Licensed-MATLAB regression fixtures
are exercised by `tests/test_matlab_reference_regression.py`.
See `equivalence_matrix.md`, `discrepancy_report.md`, and
`reports/numerical_comparison.csv`.

The port now follows the executable MATLAB repository where it conflicts
with the publication-derived implementation. Consequently MATLAB MPMOP15
calls MPMOP17 behavior and is a duplicate of MPMOP17. MATLAB-confirmed
geometry and objective ordering are used for MPDMP3–8 and MPDMP10–12.

The separate PS/PF audit passes all 33 safely executable references. MPMOP4
and MPMOP9 are intentionally excluded because the supplied MATLAB
`true_PS.m` attempts an unsafe 20000×20000 mesh. Final classification:
33 PASS, 2 PARTIAL, 0 FAIL.
