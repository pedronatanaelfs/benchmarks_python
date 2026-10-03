# Validation Report

GNU Octave: **NOT INSTALLED** (`octave --version` unavailable). MATLAB proprietary license not used.

Reference evaluations stored in `validation/reference_values/*_seed42.npz` (corners + midpoint + 100 random points, seed=42).

| Problem | Python Runs | Shape | Bounds | Analytical | MATLAB/Octave | Overall |
|---|---|---|---|---|---|---|
| MPDMP1 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP2 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP3 | PASS | PASS | PASS | PARTIAL | N/A | PARTIAL |
| MPDMP4 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP5 | PASS | PASS | PASS | PARTIAL | N/A | PARTIAL |
| MPDMP6 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP7 | PASS | PASS | PASS | PARTIAL | N/A | PARTIAL |
| MPDMP8 | PASS | PASS | PASS | PARTIAL | N/A | PARTIAL |
| MPDMP9 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP10 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP11 | PASS | PASS | PASS | PARTIAL | N/A | PARTIAL |
| MPDMP12 | PASS | PASS | PASS | PARTIAL | N/A | PARTIAL |
| MPDMP13 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP14 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP15 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP16 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP17 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPDMP18 | PASS | PASS | PASS | PASS | N/A | PASS |
| MPMOP1 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP2 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP3 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP4 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP5 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP6 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP7 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP8 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP9 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP10 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP11 | PASS | PASS | PASS | PARTIAL | N/A | PASS |
| MPMOP12 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP13 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP14 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP15 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP16 | PASS | PASS | PASS | PASS | N/A | PARTIAL |
| MPMOP17 | PASS | PASS | PASS | PASS | N/A | PARTIAL |

## Summary counts

- **PARTIAL**: 12
- **PASS**: 23

## Notes

- MPDMP13–18 reference points verified against ZM26 Appendix Table S-V (pdftotext).
- MPMOP12–17 equations taken from ZM26 Appendix Table S-VI; default `n_var=10` is conventional and marked PARTIAL where D is unspecified.
- MPDMP1–12 taken from official MATLAB `2022SheOptMPNDS3`; polygon orientation via `nsidedpoly` marked PARTIAL pending Octave/MATLAB vertex dump.
- MPMOP1–11 objective formulas ported from `MPMOP_Value.m`; common-PS sampling is PARTIAL vs full `true_PS.m` procedure.
- No PASS is assigned when a definition was assumed without a primary source.
