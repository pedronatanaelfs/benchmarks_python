# MATLAB ↔ Python Validation Report

Date: 2026-10-19  
Reference: licensed MATLAB running the supplied, unmodified benchmark sources.

## Final status

| Status | Count | Meaning |
|---|---:|---|
| **PASS** | 33 | Objectives, metadata, and safely executable PS/PF outputs match MATLAB |
| **PARTIAL** | 2 | MPMOP4/9 objectives match; original MATLAB PS/PF routine is unsafe to execute |
| **NEEDS_MANUAL_REVIEW** | 0 | — |
| **FAIL** | 0 | — |

Objective-function equivalence is **PASS 35/35** using the same 18
deterministic decision vectors per benchmark:

```text
np.allclose(matlab, python, rtol=1e-9, atol=1e-10)
```

PS/PF equivalence is **PASS 33/33** for every safely executable MATLAB
reference.

## Numerical evidence

- Maximum objective discrepancies among passing benchmarks are floating-point
  roundoff; all satisfy the stated tolerance.
- MATLAB result CSVs: `validation/matlab/results/`
- Python result CSVs: `validation/python/results/`
- Per-problem errors: `validation/reports/numerical_comparison.csv`
- MATLAB PS/PF exports: `validation/matlab/pareto_results/`
- PS/PF comparison: `validation/reports/pareto_comparison.csv`
- Complete matrix: `validation/equivalence_matrix.md`
- Discrepancy and remediation trail: `validation/discrepancy_report.md`

## Corrections validated against MATLAB

- MPMOP12–17 equations, bounds, dimensions, objective counts, DM partitions,
  party PS, and PF generation now follow the executable MATLAB classes.
- MATLAB MPMOP15 intentionally calls the MPMOP17 kernel; Python preserves
  that behavior.
- MPDMP3–8 and MPDMP10–12 now reproduce MATLAB `nsidedpoly` orientation and
  normalized `polyshape.Vertices` objective ordering.
- MPDMP polygon common-PS grids reproduce MATLAB's 1000×1000 sampling and
  ordering.
- MPDMP13–18 reproduce MATLAB conflict PF paths and concession-case tables.
- MPMOP1–3, 5–8, and 10–11 reproduce `true_PS.m` sampling.

## Why MPMOP4 and MPMOP9 are PARTIAL

Their objective functions pass MATLAB numerical comparison. However, the
supplied `true_PS.m` calls:

```matlab
meshgrid(linspace(0,1,20000))
```

which attempts a 20,000×20,000 mesh before several additional arrays and
nested loops. The reference implementation is not safely executable on a
normal workstation, so PS/PF numerical equivalence cannot be established
without modifying the MATLAB ground truth. They are therefore classified
PARTIAL rather than incorrectly declared PASS.

## Automated tests

```text
227 passed, 1 skipped, 0 failed
```

This includes:

- 35 licensed-MATLAB objective regression cases;
- 33 licensed-MATLAB PS/PF regression cases;
- structural, analytical, geometry, registry, and pymoo adapter tests.

GNU Octave remains an optional secondary check for MPMOP1–11, but no Octave
result is used as proof of final MATLAB equivalence.
