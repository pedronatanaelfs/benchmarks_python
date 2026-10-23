# Reproduction report

Paper version: arXiv:2601.22497 (accepted IEEE TEVC), Zhao, Xu & Luo.
Benchmark package commit frozen in `ENVIRONMENT.md`: `0a46ba82f56b13c269ee763b717507c7c4c5f175`
Independent optimizer runs: **3180**
Raw evaluation rows: **8580**
Seeds: 1–30
Reproduction tests: **27 passed** (`pytest experiments/zm26_reproduction/tests`, including OptMPNDS3 last-generation)
5-seed validation (corrected mutation, MPDMP1/4 × 4 algorithms): **40** additional runs
OptMPNDS3 last-generation 5-seed (MPDMP1/4 then MPDMP6/8): **20** additional runs

`src/fairmoo_benchmarks/` was **not** modified.

---

## Core scientific question

> Does the Python reproduction reproduce the core empirical message of ZM26 that average convergence metrics such as meanIGD may fail to reflect fairness between decision makers, while a concession-aware Nash-product evaluation better captures balanced multi-party compromises?

**MOSTLY YES**

Evidence that carries the message:

1. Party IGD ratios up to **5×** on MPMOP15/17 while meanIGD stays moderate (Claims 1–2).
2. Table II **Nash ranking matches 9/11** MPMOP1–11 problems, including the paper’s OptAll-vs-OptMPNDS swaps on MPMOP1 and MPMOP2 (Claims 4 and 7).
3. 25/35 benchmarks change winner between historical `party_pf_meanIGD` and Nash in the Python data (Claim 7).
4. After correcting the MPDMP IGD reference, OptMPNDS/2 `zm26_meanIGD` matches Table III **order of magnitude** (and often the number itself) on every problem for which final populations exist.

---

## Previous MPDMP mismatch (do not erase)

The first 30-run campaign classified **MPDMP1–12 as `FAILED_REPRODUCTION`**.

That classification was based on the Python column then called `meanIGD`, which is the arithmetic mean of **party-wise geometric IGD** against sampled per-DM PF regions (triangles, squares, pentagons). Typical numbers:

| benchmark | algorithm | paper meanIGD | old Python `party_pf_meanIGD` |
|---|---|---:|---:|
| MPDMP4 | OptMPNDS | 9.58e-4 | 19.21 |
| MPDMP4 | OptMPNDS2 | 1.05e-3 | 19.30 |
| MPDMP1 | OptMPNDS | 0.0545 | 15.47 |
| MPDMP1 | OptAll | 4.04 | 0.89 |

Python **OptAll had the best `meanIGD` on every MPDMP1–12 problem**. The paper reports the opposite. Parameters were **not** retuned.

### Diagnostic evidence (MATLAB ↔ Python, MPDMP4 / OptMPNDS)

Documented in `debug_matlab_python/DIAGNOSTIC_REPORT.md`. The benchmark evaluation and the OptMPNDS loop **matched** MATLAB on the deterministic tests:

- MPDMP4 `CalObj` / Python `evaluate`: PASS
- crowding distance, environmental selection, unique rows, bound clip: PASS
- SBX + PM at MATLAB `proM/D`: PASS
- five-generation shared-stream `X`: PASS at g = 0..5
- JADE2 one-step: PASS

A population sitting on the common PS `(50,40)` has She-style IGD ~`1e-3` against MATLAB `MPDMP4.PF() = CalObj([50,40])`, and party-triangle IGD ~`19`. The table gap was therefore **primarily a different IGD reference**, not a failed optimizer.

Confirmed implementation bugs that were still real (and were fixed in the reproduction layer, not the benchmark package):

1. `nd_sort` stopped on unique-row count and left later duplicates `inf`; `mpnds` dumped leftovers onto an artificial front.
2. Production mutation used `pro_m` as a per-variable probability (~0.5) instead of MATLAB `proM/D`.
3. Crowding entropy guarded NaN/Inf instead of following `CrowdingEntropy.m`.

---

## Corrected evaluation

Two metrics are now stored and must not be conflated:

| Name | Definition | Role |
|---|---|---|
| `zm26_meanIGD` | She `Metrics/IGD.m` on MATLAB `problem.PF()` (sum party `pdist2`, then `min`, then `mean`) | **Official MPDMP Table III reproduction score** |
| `party_pf_meanIGD` | mean of party-wise Euclidean IGD to sampled per-DM PF regions | research / fairness diagnostic (Claims 1–2) |
| `meanIGD` | alias of `party_pf_meanIGD` in `results/raw/results.csv` | backward compatibility only |

Audit: `MPDMP_IGD_REFERENCE_AUDIT.md`.

Existing final populations were rescored **before** any 18×4×30 rerun. Saved `F` exists for MPDMP6 and MPDMP8 (original 30-run figure problems) plus MPDMP1 and MPDMP4 (5-seed validation). Other MPDMP1–12 problems cannot be converted from the old scalar.

### Corrected vs paper (official metric)

| Problem | n | Alg | Paper | Old party-PF | Corrected zm26 | rel. diff | Level |
|---|---:|---|---:|---:|---:|---:|---|
| MPDMP1 | 5 | OptAll | 4.04 | 0.890 | 4.88 | 0.21 | CLOSE |
| MPDMP1 | 5 | OptMPNDS | 0.0545 | 15.47 | **0.0515** | 0.055 | CLOSE |
| MPDMP1 | 5 | OptMPNDS2 | 0.0476 | 15.35 | **0.0311** | 0.35 | CLOSE |
| MPDMP1 | 5 | OptMPNDS3 | 0.0447 | 12.26 | **0.0366** | 0.18 | CLOSE (last-gen fix) |
| MPDMP4 | 5 | OptAll | 0.0178 | 2.45 | 0.0102 | 0.43 | CLOSE |
| MPDMP4 | 5 | OptMPNDS | 9.58e-4 | 19.21 | **3.67e-4** | 0.62 | QUALITATIVE (inside paper ±2.11e-3) |
| MPDMP4 | 5 | OptMPNDS2 | 1.05e-3 | 19.30 | **8.35e-4** | 0.20 | CLOSE |
| MPDMP4 | 5 | OptMPNDS3 | 0.0133 | 17.95 | **0.00989** | 0.26 | CLOSE (last-gen fix) |
| MPDMP6 | 30 | OptAll | 3.23 | 2.04 | 2.98 | 0.077 | CLOSE |
| MPDMP6 | 30 | OptMPNDS | 0.132 | 14.17 | **0.165** | 0.25 | CLOSE |
| MPDMP6 | 30 | OptMPNDS2 | 0.130 | 14.16 | **0.167** | 0.29 | CLOSE |
| MPDMP6 | 5 | OptMPNDS3 | 0.0838 | 14.33 | **0.0869** | 0.037 | CLOSE (last-gen fix; pre-fix 30-run was 1.62) |
| MPDMP8 | 30 | OptAll | 6.23 | 2.95 | **6.12** | 0.017 | CLOSE |
| MPDMP8 | 30 | OptMPNDS | 2.46 | 9.23 | **2.43** | 0.013 | CLOSE |
| MPDMP8 | 30 | OptMPNDS2 | 2.46 | 9.26 | **2.43** | 0.014 | CLOSE |
| MPDMP8 | 5 | OptMPNDS3 | 2.25 | 15.17 | **2.254** | 0.002 | CLOSE (last-gen fix; pre-fix 30-run was 16.71) |
| MPDMP2,3,5,7,9–12 | 0 | all | Table III | party-PF archive | — | — | INCONCLUSIVE (no saved `F`) |

On every problem with `F`, **OptMPNDS and OptMPNDS2 beat OptAll** on `zm26_meanIGD`, matching the paper’s qualitative ranking. After the last-generation fix, 5-seed **OptMPNDS3** is CLOSE to Table III on MPDMP1/4/6/8 (was the ranking outlier because `n` collapsed to ~16). Pre-fix 30-run OptMPNDS3 on MPDMP6/8 (`1.62` / `16.71`) is the same collapse artifact and must not be quoted.

Files: `results/paper_comparison/mpdmp_igd_rescored.csv`, `mpdmp_igd_rescored_summary.csv`, `mpdmp_table_iii_corrected.md`.

Historical party-PF comparison remains in `results/paper_comparison/paper_vs_python.csv` and must not be quoted as the official Table III result.

---

## Experiment summary

| Experiment | Numerical agreement | Ranking agreement | Qualitative agreement | Verdict |
|---|---|---|---|---|
| MPMOP1–11 | meanIGD smaller than Table II (typical rel. diff 0.4–0.98); Nash magnitudes incomparable (C unpublished) | Nash 9/11; meanIGD 7/11 | meanIGD-vs-Nash swaps recovered on MPMOP1/2/4/9 | PARTIAL REPRODUCTION |
| MPMOP12–17 | paper has no numeric table | OptAll wins both metrics here | party disparity and weak concession trend | QUALITATIVE REPRODUCTION ONLY |
| MPMOP12/13 Jain-Gini | no optimizer table in the paper | OptMPNDS has higher Jain / lower Gini than OptAll | relative fairness direction matches the intended story | QUALITATIVE REPRODUCTION ONLY |
| MPDMP1–12 (previous, party-PF) | meanIGD mismatch 12/12; OptAll always best | 0/12 | opposite to Table III | FAILED REPRODUCTION (historical) |
| MPDMP1–12 (corrected zm26) | OptMPNDS/2/All CLOSE where `F` exists; OptMPNDS3 30-seed CLOSE on 11/12 (MPDMP9 QUALITATIVE, Python better); other algorithms still INCONCLUSIVE on 8 problems without `F` | OptAll worse than OptMPNDS/2 on 4/4; OptMPNDS3 first on MPDMP6/8 as in the paper | MPNDS family recovers the common-PS image | **PARTIAL REPRODUCTION** |
| MPDMP13–18 | figures only in the paper | concession monotonicity 16/36 pairs | Nash still differs from meanIGD | QUALITATIVE REPRODUCTION ONLY |

---

## What was executed

| Family | Problems | Algorithms | N | FE | Runs |
|---|---|---|---:|---:|---:|
| MPMOP | MPMOP1–17 | OptAll, OptMPNDS | 100 | 10 000 | 30 |
| MPDMP | MPDMP1–18 | OptAll, OptMPNDS, OptMPNDS2, OptMPNDS3 | 200 | 80 000 | 30 |
| MPDMP validation | MPDMP1, MPDMP4 | same four | 200 | 80 000 | 5 (MATLAB `proM/D`) |
| OptMPNDS3 last-gen | MPDMP1,4,6,8 | OptMPNDS3 | 200 | 80 000 | 5 |

MPMOP1–11 used **D=2** (Table II caption). MPMOP12–17 used MATLAB default **D=10**. Concession cases are evaluation-only (Table S-IV).

---

## Whether a full 30-seed rerun is required

**No full 18 × 4 × 30 rerun.**

| Algorithm | Decision | Reason |
|---|---|---|
| OptMPNDS | **Do not rerun** | Deterministic MPDMP4 loop matched MATLAB. 5-seed MPDMP1/4 with `proM/D` already at Table III scale (`0.0515` vs `0.0545`; `3.67e-4` vs `9.58e-4`). Mutation-rate change is not material relative to the old ~19 party-PF gap. |
| OptMPNDS2 | **Do not rerun** | PLNDS now matches Test 02 integers. 5-seed / 30-run `zm26_meanIGD` at Table III scale. |
| OptAll | **Do not rerun** | Rescored MPDMP6/8 30-run `F` already CLOSE to Table III (`2.98` vs `3.23`; `6.12` vs `6.23`). |
| OptMPNDS3 | **30-seed complete (540/540)** | Last-generation truncation fixed. Post-fix `zm26` is CLOSE on 11/12 Table III problems (MPDMP9 QUALITATIVE: Python 0.037 vs paper 0.203, matching OptMPNDS scale). MPDMP13–18 saved with `n=200` and `zm26=NaN` (no common MATLAB PF). Do not rerun OptAll/OptMPNDS/OptMPNDS2. |

Completing numerical Table III cells for MPDMP2, 3, 5, 7, 9–12 would require saved `F` (evaluation-only if those populations are regenerated with the same seeds). That is optional bookkeeping, not evidence that the previous FAILED verdict was an optimization failure.

No parameter was tuned to chase Table III (`N`, `FE`, mutation, PF sampling, `C`, `λ` unchanged except the MATLAB-documented `proM/D` site probability).

---

## Diagnosed causes (not tuned away)

Documented in `PAPER_PARAMETER_AUDIT.md`. Short list:

1. **Unpublished C** — Appendix S-I; we used `max L + 1` on a random population. Absolute Ψ cannot match Tables II–III.
2. **Paper vs MATLAB Nash formula** — Theorem 1 uses \( C-L \); `nash_score.m` uses \( \exp(-L) \). Both stored; claims use the paper formula.
3. **MPMOP budget/operators inferred** from PlatEMO GLOBAL / `GA.m`, not stated in ZM26.
4. **Historical MPDMP “search failure”** — mostly `party_pf_meanIGD` vs She `IGD.m` + `problem.PF()`. See `MPDMP_IGD_REFERENCE_AUDIT.md`.
5. **OptMPNDS3 last-generation truncation (fixed)** — Python sliced the leftover FE budget so envsel replaced N=200 with ~16 individuals. Mid-run MPDMP1 was already `zm26~0.02–0.08`. After the MATLAB-style generation-boundary stop, 5-seed MPDMP1/4 match Table III scale. Secondary diffs (post-envsel archive, S_CR source) are documented in `debug_optmpnds3/` and were not rewritten.
6. **MPDMP3/10 unequal n_obj_per_dm** — MATLAB `nash_score.m` cannot run these; Python skips cross-space PF geometry and sets `λ=1` when dimensions differ.
7. **MPMOP4/9 PF** — MATLAB `true_PS` 20000² mesh is unsafe; reproduction samples the equivalent manifold `sin(2π(x1+x2))=0`.
8. **PF/IGD scale on MPMOP** — Python meanIGD on MPMOP is consistently smaller than Table II. Rankings remain the comparable quantity.

---

## Statistical tests

Wilcoxon rank-sum (Mann–Whitney U) with Holm correction and Friedman average ranks:

- `results/statistical_tests/wilcoxon_holm.csv` (raw and Holm p-values)
- `results/statistical_tests/friedman.csv`

These tests were computed on the historical `party_pf_meanIGD` 30-run vectors. They are **not** re-interpreted as Table III evidence.

ZM26 does not name this protocol in the main text (`UNRESOLVED` in the parameter audit).

---

## Figures

All PNG+PDF under `figures/`:

- `paper_vs_python_meanIGD` (historical party-PF column)
- `paper_vs_python_nash`
- `ranking_comparison`
- `party_igd_disparity`
- `concession_sensitivity_mpmop`
- `concession_sensitivity_mpdmp`
- decision-space snapshots: MPMOP12, MPMOP13, MPDMP6, MPDMP8, MPDMP13, MPDMP15

Axes were not adjusted to imitate the paper.

---

## Raw data

- Run-level metrics: `results/raw/results.csv` (`meanIGD` = `party_pf_meanIGD`; future rows also store `zm26_meanIGD`)
- Final populations for figure problems: `results/raw/populations/*.npz`
- 5-seed validation: `results/validation/mpdmp_5seed.csv` and `results/validation/populations/`
- OptMPNDS3 last-gen 5-seed: `results/validation/optmpnds3_5seed_after_lastgen_fix.csv`, `optmpnds3_5seed_mpdmp68.csv`
- OptMPNDS3 30-seed (post-fix, 540/540): `results/validation/optmpnds3_30seed/`
- Per-job JSON: `results/raw/job_rows/`
- Aggregates: `results/aggregated/summary.csv`

---

## Files to read first

1. `PAPER_PARAMETER_AUDIT.md`
2. `MPDMP_IGD_REFERENCE_AUDIT.md`
3. `CLAIM_VALIDATION.md`
4. `results/paper_comparison/mpdmp_table_iii_corrected.md`
5. `results/reproduction_summary.json`
6. this file
