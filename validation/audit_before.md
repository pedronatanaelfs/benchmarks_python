# Audit Snapshot (Before Changes)

> **Historical snapshot (2026-10-03).** This is the pre-MATLAB-equivalence
> audit (23 PASS / 12 PARTIAL; Octave not yet executed). It is **not** the
> current public status. After licensed-MATLAB comparison and Python
> correction: **33 PASS, 2 PARTIAL (MPMOP4/9), 0 FAIL**. See
> `validation_report.md` and `audit_final.md`.

Branch: `audit-validation`  
Date: 2026-10-03  
Commit base: `4b9ac35` (origin/main)

## Test suite

```
128 passed, 3 skipped
```

Skipped tests: MATLAB/Octave equivalence placeholders (`OCTAVE_NOT_INSTALLED` at snapshot time; Octave later installed via conda-forge 10.3.0).

## Benchmark status (from `validation/validation_report.md`)

| Status | Count | Problems |
|---|---|---|
| **PASS** | 23 | MPDMP1,2,4,6,9,10,13–18; MPMOP1–11 |
| **PARTIAL** | 12 | MPDMP3,5,7,8,11,12; MPMOP12–17 |
| **NEEDS_MANUAL_VERIFICATION** | 0 | — |
| **FAIL** | 0 | — |

Total benchmarks: **35** (17 MPMOP + 18 MPDMP)

## Known assumptions / risks

1. **MPMOP12–17 `n_var=10`**: Table S-VI uses general `D`; not uniquely fixed. Default 10 follows OptMPNDS/Liu convention. ZM26 Table `tab:MPMOP_results` caption states **D = 2** for **MPMOP1–11 experiments only** (not MPMOP12–17).
2. **`common_ps_exists` stored as strings** `"True"` / `"False"` / `"Unknown"` — unsafe if ever cast with `bool()`.
3. **MPDMP3/5/7/8/11/12**: `nsidedpoly` vertex orientation marked PARTIAL pending MATLAB confirmation.
4. **MPMOP1–11**: objective formulas from `MPMOP_Value.m`; common-PS sampling incomplete vs `true_PS.m`. Overall marked PASS for objectives, but analytical PS sampling is PARTIAL.
5. **Octave equivalence**: not executed at this snapshot (skipped tests).
6. **README claim** “verified Python port” overstates PARTIAL cases.

## MPDMP13–18

Preserve unless objective source inconsistency found. Status PASS; reference points from ZM26 Appendix Table S-V.

## Planned audit actions

1. Type-safe `CommonPSStatus`
2. Explicit dimension metadata for MPMOP12–17
3. Octave equivalence for `MPMOP_Value` (MPMOP1–11)
4. Geometric audit of `nsidedpoly` vs MathWorks / PS hardcodes
5. Pymoo adapter equality tests
6. Docs / inventory / README honesty
7. `audit_final.md`
