# Audit Summary (Final)

Date: 2026-10-19  
Ground truth: supplied executable MATLAB benchmark repositories.

## Result

| Status | Count |
|---|---:|
| PASS | 33 |
| PARTIAL | 2 |
| NEEDS_MANUAL_REVIEW | 0 |
| FAIL | 0 |

- Objective equivalence: **35/35 PASS**
- Safely executable PS/PF equivalence: **33/33 PASS**
- Automated tests: **227 passed, 1 skipped, 0 failed**

The two PARTIAL problems are MPMOP4 and MPMOP9. Their objectives match
MATLAB, but the original `true_PS.m` requests a 20,000×20,000 mesh and is
not safely executable without modifying the reference.

## Resolved discrepancies

1. MPMOP12–17 were aligned to the executable MATLAB classes rather than the
   conflicting publication-derived definitions.
2. MPMOP16/17 objective counts and DM partitions were corrected.
3. MATLAB's MPMOP15→MPMOP17 kernel duplication is preserved.
4. MPDMP `nsidedpoly` orientation and `polyshape.Vertices` order were
   recovered from licensed MATLAB and ported.
5. Polygon-intersection common PS grids, conflict PF paths, and concession
   tables were ported.
6. `true_PS.m` sampling was reproduced for MPMOP1–3, 5–8, and 10–11.

## Evidence

- `equivalence_matrix.md`
- `discrepancy_report.md`
- `reports/numerical_comparison.csv`
- `reports/pareto_comparison.csv`
- `matlab/results/`
- `matlab/pareto_results/`

Octave remains an optional secondary check. Final equivalence claims rely on
licensed MATLAB outputs, not Octave.
