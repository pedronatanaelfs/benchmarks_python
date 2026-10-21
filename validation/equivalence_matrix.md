# Post-fix equivalence matrix

MATLAB objective outputs were generated for all 35 benchmarks and compared
with `rtol=1e-9`, `atol=1e-10`. All objective evaluations pass. Safely
executable PS/PF exports also pass; only MPMOP4/9 remain unexecuted.

| Problem | Structure | D/M/DM | Bounds | Objective function | PS/PF | MATLAB numerical test | Overall |
|---|---|---|---|---|---|---|---|
| MPMOP1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP3 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP4 | PASS | PASS | PASS | PASS | PARTIAL | PASS | PARTIAL |
| MPMOP5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP9 | PASS | PASS | PASS | PASS | PARTIAL | PASS | PARTIAL |
| MPMOP10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP12 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP13 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP14 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP15 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP16 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPMOP17 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP3 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP5 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP6 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP8 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP9 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP10 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP12 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP13 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP14 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP15 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP16 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP17 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| MPDMP18 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## Current totals

- PASS: 33
- PARTIAL: 2
- FAIL: 0
- NEEDS_MANUAL_REVIEW: 0

Objective-function equivalence passes for all 35 problems. PS/PF comparisons
pass for all 33 safely executable MATLAB references. MPMOP4/9 remain PARTIAL
only because their supplied `true_PS.m` attempts a 20000×20000 mesh and
cannot be safely executed; their objective functions pass.

## DM/objective partitions

- MPMOP1–3: DM1 → f1–f2; DM2 → f3–f4.
- MPMOP4–6: DM1 → f1–f3; DM2 → f4–f6.
- MPMOP7–8: DM1 → f1–f2; DM2 → f3–f4; DM3 → f5–f6.
- MPMOP9–11: DM1 → f1–f3; DM2 → f4–f6; DM3 → f7–f9.
- MATLAB MPMOP12–13: DM1 → f1–f2; DM2 → f3–f4.
- MATLAB MPMOP14: DM1 → f1–f3; DM2 → f4–f6.
- MATLAB MPMOP15 and MPMOP17: three two-objective blocks (Python matches;
  MATLAB MPMOP15 calls the MPMOP17 kernel).
- MATLAB MPMOP16: two two-objective blocks (Python matches).
- MPDMP1–2 and 13: two two-objective blocks.
- MPDMP3: f1–f2 and f3–f5.
- MPDMP4–5 and 14: two three-objective blocks.
- MPDMP6–7 and 15: two four-objective blocks.
- MPDMP8 and 16: two five-objective blocks.
- MPDMP9 and 17: three two-objective blocks.
- MPDMP10: f1–f2, f3–f4, f5–f8.
- MPDMP11 and 18: three three-objective blocks.
- MPDMP12: three four-objective blocks.
