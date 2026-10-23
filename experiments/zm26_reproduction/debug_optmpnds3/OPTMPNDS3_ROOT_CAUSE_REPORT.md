# OptMPNDS3 root-cause report

Primary problem: **MPDMP1**. Confirm: **MPDMP4**, then **MPDMP6 / MPDMP8**.
Production change applied: **one** (last-generation truncation). JADE2 mutation formula was not rewritten.

---

## PRIMARY ROOT CAUSE

**Python truncated the last JADE generation to the leftover evaluation budget, then environmental-selection replaced the whole population with that tiny set.**

Production snapshots (`python_outputs/test_11_production_snapshots.csv`), MPDMP1, **before** the fix:

| seed | eval | n | zm26_meanIGD | mean dist to (50,50) |
|---:|---:|---:|---:|---:|
| 1 | 20000 (after PFt) | 192 | 2.11 | 15.1 |
| 1 | 25192 | 200 | **0.023** | 0.84 |
| 1 | 65192 | 200 | 0.081 | 0.95 |
| 1 | **80000 (final)** | **16** | **0.319** | 6.04 |
| 2 | 20000 | 190 | 0.082 | 14.5 |
| 2 | 65190 | 200 | 0.043 | 1.02 |
| 2 | **80000 (final)** | **19** | **5.11** | 4.79 |

Mid-run IGD is already at Table III scale (`0.02–0.08` vs paper `0.0447`). The returned population is the collapsed last generation. Those finals match the previous 5-seed OptMPNDS3 MPDMP1 numbers (`0.319` and `5.112`).

MATLAB `OptMPNDS3.m` generates one offspring per current individual in a `for i = Population` loop. `INDIVIDUAL()` may **overshoot** `Global.evaluation`. `GLOBAL.NotTermination` runs only at the **next** while-header, saves that **full** generation, then throws `GLOBAL:Termination`. It never envsel-replaces the search population with a 8–20-row leftover batch.

Classification: **ROOT_CAUSE_CANDIDATE → confirmed on the production trajectory.**

Minimal fix in `algorithms/optmpnds3.py`: do not slice `off_x` to `remaining` before evaluating / envsel. Check the budget at generation start only (MATLAB while-header). Slight FE overshoot (at most one generation) matches MATLAB.

Regression: `tests/test_optmpnds3_last_generation.py` (passed).

The PFt / archive / PF-seeding hypothesis is **rejected** as the Table III collapse. Python already sits on the common PS well before the last generation.

---

## Fix verification (5 seeds, N=200, FE=80000)

| Problem | Paper | Pre-fix Python | Post-fix mean (5 seeds) | n_final | Level |
|---|---:|---:|---:|---:|---|
| MPDMP1 | 0.0447 | 2.961 | **0.03663** | 200 | CLOSE |
| MPDMP4 | 0.0133 | 0.0644 | **0.00989** | 200 | CLOSE |
| MPDMP6 | 0.0838 | 1.616 | **0.08686** | 200 | CLOSE |
| MPDMP8 | 2.25 | 16.71 | **2.254** | 200 | CLOSE |

Sources:

- MPDMP1/4: `results/validation/optmpnds3_5seed_after_lastgen_fix.csv`
- MPDMP6/8: `results/validation/optmpnds3_5seed_mpdmp68.csv`

Populations sit on the common PS (MPDMP1/6 ≈ `(50,50)`; MPDMP4 ≈ `(50,40)`; MPDMP8 ≈ `(50,47)`). Relative error vs Table III is 0.18, 0.26, 0.037, and 0.002.

---

## PFt initialization — NOT the primary cause

Python native `getPF` (3 seeds):

| Problem | seed | \|PF1\| | \|PF2\| | n after envsel | zm26 | mean dist to common PS |
|---|---:|---:|---:|---:|---:|---:|
| MPDMP1 | 1 | 100 | 100 | 192 | 2.11 | 15.1 |
| MPDMP1 | 2 | 100 | 100 | 190 | **0.082** | 14.5 |
| MPDMP1 | 3 | 100 | 100 | 191 | 2.24 | 14.5 |
| MPDMP4 | 1 | 100 | 100 | 198 | **0.0073** | 19.5 |
| MPDMP4 | 2 | 100 | 100 | 199 | 0.24 | 18.8 |
| MPDMP4 | 3 | 100 | 100 | 200 | 0.11 | 19.5 |

`getPF` returns each party’s front 1 (MPDMP1: the two diagonals). Official `zm26_meanIGD` for a 1-row MATLAB `PF()` is essentially the **nearest** individual to the intersection image, so gen-0 IGD is noisy. Seed 2 is already near the paper final. After ~5000 JADE evals the search is on `(50,50)` with zm26 ~ `1e-2`. **PFt is not why finals were ~3.**

MATLAB `mpdmp1_initialization.csv` is still **WAITING** for a native `getPF` dump (independent RNG; compare region/scale only).

Scatter: `figures/mpdmp1_python_pft.png`, `figures/mpdmp4_python_pft.png`.

---

## SECONDARY DIFFERENCES (not the Table III collapse)

Source mapping: `OPTMPNDS3_SOURCE_MAPPING.md`. Still unconfirmed vs MATLAB CSVs:

1. No `updateArchive(..., setdiff(Offsprings, Population), 2N)` after envsel.
2. μCR/μF from dominance-event CR/F, not surviving `INDIVIDUAL.add` (zeros dropped).
3. No `while Parent2 == Parent1` retry.
4. Shared-stream toy N=20 replica first X difference at **g2** (archive size already differs at g1). That replica is **not** why n→16 at FE=80000.

These may affect path quality slightly (30-gen replica: production 0.071 vs faithful 0.049 on MPDMP1). They are **not** the order-of-magnitude gap and were **not** rewritten.

---

## CONFIRMED NON-CAUSES

| Component | Status |
|---|---|
| MPDMP evaluation | PASS |
| `nd_sort` / PLNDS | PASS |
| Crowding entropy NaN/Inf | PASS |
| Unique-row + one-by-one envsel | PASS |
| JADE2 mutation on shared indices | PASS |
| `proM/D` in party NSGA-II | PASS |
| Archive empty at generation 0 | PASS |
| p-best: lexsort vs `getBestIndividual.m` replica | PASS (0/20 shared, 0/200 random) |
| μF Lehmer / μCR mean **formula** on a shared S | PASS pending MATLAB CSV |
| PFt “wrong region” as explanation of mean 2.96 | **rejected** by test_11 mid-run |
| Last-generation leftover-FE truncation | **ROOT CAUSE** (fixed) |

---

## MATLAB outputs

Still needed for exact operator CSVs (tests 01–08, optional 09):

```matlab
cd experiments/zm26_reproduction/debug_optmpnds3/matlab
run_all_optmpnds3_diagnostics
```

Then `python compare_optmpnds3_outputs.py`.

Native 5-run MATLAB OptMPNDS3 is optional (`run_all_optmpnds3_diagnostics(true)`).

These CSVs would confirm secondary operator diffs. They are **not** required to explain the Table III collapse.

---

## Full 30-seed OptMPNDS3 rerun gate (§26)

| Condition | Result |
|---|---|
| 1. Concrete implementation mismatch | **yes** — last-generation `off_x[:remaining]` |
| 2. Fix validated against MATLAB semantics | **yes** — generation-boundary `NotTermination`; unit test; 5-seed scale |
| 3. 5-seed MPDMP1/4 improve materially | **yes** — 2.96→0.037 and 0.064→0.0099 |
| 4. MPDMP6/8 confirmation also improves | **yes** — 1.62→0.087 and 16.71→2.25 |

All four conditions hold. OptAll / OptMPNDS / OptMPNDS2 are **not** rerun. OptMPNDS3 30-seed writes to `results/validation/optmpnds3_30seed/`.

30-seed OptMPNDS3 is complete: **540/540**, all `n_final=200`. Table III is CLOSE on 11/12; MPDMP9 is QUALITATIVE (Python 0.037 vs paper 0.203). MPDMP13–18 have no common MATLAB PF, so `zm26=NaN`; populations are still saved.
