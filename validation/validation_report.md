# Validation Report

GNU Octave: **10.3.0** (conda-forge) for `MPMOP_Value.m` equivalence.
MATLAB proprietary license not used. MPDMP PlatEMO classdefs: `OCTAVE_INCOMPATIBLE`.

Reference evaluations: `validation/reference_values/*` (seed 42 inputs + Octave/Python CSVs for MPMOP1–11).

| Problem | Python Runs | Shape | Bounds | Analytical | MATLAB/Octave | Overall |
|---|---|---|---|---|---|---|
| MPDMP1 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP2 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP3 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP4 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP5 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP6 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP7 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP8 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP9 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP10 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP11 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP12 | PASS | PASS | PASS | PASS | OCTAVE_INCOMPATIBLE | PASS |
| MPDMP13 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP14 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP15 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP16 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP17 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP18 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPMOP1 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP2 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP3 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP4 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP5 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP6 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP7 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP8 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP9 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP10 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP11 | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP12 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP13 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP14 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP15 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP16 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP17 | PASS | PASS | PASS | PASS | N/A | PARTIAL |

## Summary counts

- **PASS**: 29
- **PARTIAL**: 6
- **NEEDS_MANUAL_VERIFICATION**: 0
- **FAIL**: 0

## Notes

- MPDMP13–18 unchanged; Table S-V reference points preserved.
- MPMOP1–11: objective formulas match Octave `MPMOP_Value.m` (rtol=1e-8, atol=1e-10).
- MPMOP12–17: formulas from Table S-VI; `n_var` default=10 is `ASSUMED_DEFAULT` (PARTIAL).
- MPDMP polygon problems: vertices follow MathWorks `nsidedpoly` documentation + author hardcodes (MPDMP6 PS).
- `common_ps_exists` is now type-safe `CommonPSStatus` enum.
