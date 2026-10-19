# Audit Summary (Final)

> **Superseded by the licensed-MATLAB equivalence audit (2026-10-19).**
> Current authoritative status: 35/35 objective PASS; 33/33 safely executable
> PS/PF PASS; overall 33 PASS, 2 PARTIAL (MPMOP4/9 unsafe reference meshes),
> 0 FAIL. See `equivalence_matrix.md`, `discrepancy_report.md`, and
> `reports/`.

Branch: `audit-validation`  
Date: 2026-10-03

## Before

| Status | Count |
|---|---|
| PASS | 23 |
| PARTIAL | 12 |
| NEEDS_MANUAL_VERIFICATION | 0 |
| FAIL | 0 |

Tests: 128 passed, 3 skipped  
Octave: not installed

## After

| Status | Count |
|---|---|
| PASS | 29 |
| PARTIAL | 6 |
| NEEDS_MANUAL_VERIFICATION | 0 |
| FAIL | 0 |

Tests: **146 passed, 1 skipped, 0 failed**  
Octave: **10.3.0** (conda-forge)

PARTIAL remaining: **MPMOP12–MPMOP17** (decision dimension `D` not fixed in ZM26 Table S-VI; default `n_var=10` is `ASSUMED_DEFAULT`).

## Changes Made

| Problem / Area | Issue | Source | Change | Validation | Final Status |
|---|---|---|---|---|---|
| API | `common_ps_exists` as unsafe strings | — | `CommonPSStatus` enum | unit tests vs `bool("False")` pitfall | — |
| MPMOP1–11 | No Octave equivalence | OptMPNDS `MPMOP_Value.m` | Octave runner + CSVs | allclose PASS | PASS |
| MPMOP12–17 | Hidden D=10 assumption | ZM26 Table S-VI; caption D=2 is for MPMOP1–11 only | metadata `ASSUMED_DEFAULT`, docs | analytical PS tests | PARTIAL |
| MPDMP3,5,7,8,11,12 | nsidedpoly orientation PARTIAL | Author `.m` + MathWorks nsidedpoly docs + MPDMP6 PS hardcode | geometry tests; keep formulas | analytical + geometry | PASS |
| MPDMP13–18 | — | ZM26 Table S-V | **no change** | revalidated | PASS |
| pymoo adapter | missing equality tests | — | tests for MPMOP1/15, MPDMP13/17 | PASS | — |
| Docs/README/CITATION | overstated “verified”; missing CFF URL | — | honest status table; CITATION.cff | — | — |

## Remaining Risks

1. **MPMOP12–17 dimension**: experiments may have used a D other than 10; constructors accept `n_var=` override.
2. **MPDMP `nsidedpoly`**: Octave lacks MATLAB Mapping Toolbox; orientation follows MathWorks documentation + author PS hardcodes, not a live MATLAB vertex dump.
3. **Common PS samplers** for some MPMOP1–11 / polygon-intersection MPDMPs are densified helpers, not full `true_PS.m` reproductions. `evaluate()` does not depend on them.
4. **MPDMP classdefs**: full Octave execution of PlatEMO-style problems remains `OCTAVE_INCOMPATIBLE`.

## Scientific Assumptions

- `DEFAULT_N_VAR = 10` for MPMOP12–17 (`dimension_status=ASSUMED_DEFAULT`).
- OptMPNDS default `Global.D=10` for MPMOP1–11 constructors; ZM26 reported D=2 for MPMOP1–11 experiments.
- `nsidedpoly` Radius: first vertex to the right, CCW (MathWorks).
- `nsidedpoly` SideLength with even `n`: axis-aligned (matches MPDMP6 hardcoded PS).
- No fabricated analytical PFs; empty common PS uses `CommonPSStatus.EMPTY` → shape `(0, n_var)`.

## Octave equivalence

| Suite | Result |
|---|---|
| MPMOP1–11 (`MPMOP_Value.m`) | **PASS 11/11** |
| MPDMP1–12 (classdefs) | **OCTAVE_INCOMPATIBLE** |
| MPDMP13–18 / MPMOP12–17 | N/A (no author MATLAB evaluator in-repo) |
