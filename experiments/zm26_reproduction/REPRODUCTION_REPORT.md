# Reproduction report

Paper version: arXiv:2601.22497 (accepted IEEE TEVC), Zhao, Xu & Luo.
Benchmark package commit frozen in `ENVIRONMENT.md`: `0a46ba82f56b13c269ee763b717507c7c4c5f175`
Independent optimizer runs: **3180**
Raw evaluation rows: **8580**
Seeds: 1–30
Reproduction tests: 20 passed (`pytest experiments/zm26_reproduction/tests`)

`src/fairmoo_benchmarks/` was **not** modified.

---

## Core scientific question

> Does the Python reproduction reproduce the core empirical message of ZM26 that average convergence metrics such as meanIGD may fail to reflect fairness between decision makers, while a concession-aware Nash-product evaluation better captures balanced multi-party compromises?

**MOSTLY YES**

Evidence that carries the message:

1. Party IGD ratios up to **5×** on MPMOP15/17 while meanIGD stays moderate (Claims 1–2).
2. Table II **Nash ranking matches 9/11** MPMOP1–11 problems, including the paper’s OptAll-vs-OptMPNDS swaps on MPMOP1 and MPMOP2 (Claims 4 and 7).
3. 25/35 benchmarks change winner between meanIGD and Nash in the Python data (Claim 7).

What does **not** carry Table III:

- On MPDMP1–12, Python **OptAll has the best meanIGD** on every problem. The paper reports the opposite (OptMPNDS/2/3 much closer to each party PF). Absolute meanIGD for MPNDS-family methods is often 100–1000× worse than Table III. Parameters were **not** retuned to hide this.

---

## Experiment summary

| Experiment | Numerical agreement | Ranking agreement | Qualitative agreement | Verdict |
|---|---|---|---|---|
| MPMOP1–11 | meanIGD smaller than Table II (typical rel. diff 0.4–0.98); Nash magnitudes incomparable (C unpublished) | Nash 9/11; meanIGD 7/11 | meanIGD-vs-Nash swaps recovered on MPMOP1/2/4/9 | PARTIAL REPRODUCTION |
| MPMOP12–17 | paper has no numeric table | OptAll wins both metrics here | party disparity and weak concession trend | QUALITATIVE REPRODUCTION ONLY |
| MPMOP12/13 Jain-Gini | no optimizer table in the paper | OptMPNDS has higher Jain / lower Gini than OptAll | relative fairness direction matches the intended story | QUALITATIVE REPRODUCTION ONLY |
| MPDMP1–12 | meanIGD **MISMATCH** for all 12 problems; log-Nash 4 CLOSE / 4 QUALITATIVE / 40 MISMATCH cells | meanIGD ranking 0/12; log-Nash ranking 2/12 (MPDMP1 OptMPNDS3, MPDMP3 OptMPNDS) | OptAll is **not** the worst meanIGD method in Python | FAILED REPRODUCTION |
| MPDMP13–18 | figures only in the paper | concession monotonicity 16/36 pairs | Nash still differs from meanIGD | QUALITATIVE REPRODUCTION ONLY |

---

## What was executed

| Family | Problems | Algorithms | N | FE | Runs |
|---|---|---|---:|---:|---:|
| MPMOP | MPMOP1–17 | OptAll, OptMPNDS | 100 | 10 000 | 30 |
| MPDMP | MPDMP1–18 | OptAll, OptMPNDS, OptMPNDS2, OptMPNDS3 | 200 | 80 000 | 30 |

MPMOP1–11 used **D=2** (Table II caption). MPMOP12–17 used MATLAB default **D=10**. Concession cases are evaluation-only (Table S-IV).

---

## Largest discrepancies vs Tables II–III

Nash absolute values are dominated by unpublished `C` and should not be compared as numbers. The scientifically serious mismatches are **meanIGD on MPDMP**:

| benchmark | algorithm | metric | paper_mean | python_mean | rel_diff | level |
|---|---|---|---:|---:|---:|---|
| MPDMP4 | OptMPNDS | meanIGD | 9.58e-4 | 19.21 | ~2e4 | MISMATCH |
| MPDMP4 | OptMPNDS2 | meanIGD | 1.05e-3 | 19.30 | ~1.8e4 | MISMATCH |
| MPDMP9 | OptMPNDS2 | meanIGD | 0.0215 | 13.26 | ~616 | MISMATCH |
| MPDMP1 | OptMPNDS | meanIGD | 0.0545 | 15.47 | ~283 | MISMATCH |
| MPDMP1 | OptAll | meanIGD | 4.04 | 0.89 | 0.78 | ranking reversed |
| MPMOP8 | OptAll | nash_score | 3.68e3 | 1.33e43 | C-scale | QUALITATIVE (ranking matches) |
| MPMOP6 | both | nash_score | ~6–7 | ~6e29 | C-scale | MISMATCH (Nash winner also differs) |

Full cell-level comparison: `results/paper_comparison/paper_vs_python.csv`.

---

## Diagnosed causes (not tuned away)

Documented in `PAPER_PARAMETER_AUDIT.md`. Short list:

1. **Unpublished C** — Appendix S-I; we used `max L + 1` on a random population. Absolute Ψ cannot match Tables II–III.
2. **Paper vs MATLAB Nash formula** — Theorem 1 uses \( C-L \); `nash_score.m` uses \( \exp(-L) \). Both stored; claims use the paper formula.
3. **MPMOP budget/operators inferred** from PlatEMO GLOBAL / `GA.m`, not stated in ZM26.
4. **MPDMP OptMPNDS/2/3 search quality** — Python ports follow She MATLAB structure (MPNDS, PLNDS, PFt+JADE2, crowding entropy) but produce much worse party IGD than Table III. Possible remaining port gaps: JADE2 archive, `getPF` init, unique-row truncation, crowding-entropy one-by-one removal vs numerical differences, IGD reference discretization. **Not adjusted to chase Table III.**
5. **MPDMP3/10 unequal n_obj_per_dm** — MATLAB `nash_score.m` cannot run these; Python skips cross-space PF geometry and sets `λ=1` when dimensions differ.
6. **MPMOP4/9 PF** — MATLAB `true_PS` 20000² mesh is unsafe; reproduction samples the equivalent manifold `sin(2π(x1+x2))=0`.
7. **PF/IGD scale** — Python meanIGD on MPMOP is consistently smaller than Table II (better apparent convergence, or a different PF sample). Rankings remain the comparable quantity.

---

## Statistical tests

Wilcoxon rank-sum (Mann–Whitney U) with Holm correction and Friedman average ranks:

- `results/statistical_tests/wilcoxon_holm.csv` (raw and Holm p-values)
- `results/statistical_tests/friedman.csv`

ZM26 does not name this protocol in the main text (`UNRESOLVED` in the parameter audit). Tests were still computed as requested.

---

## Figures

All PNG+PDF under `figures/`:

- `paper_vs_python_meanIGD`
- `paper_vs_python_nash`
- `ranking_comparison`
- `party_igd_disparity`
- `concession_sensitivity_mpmop`
- `concession_sensitivity_mpdmp`
- decision-space snapshots: MPMOP12, MPMOP13, MPDMP6, MPDMP8, MPDMP13, MPDMP15

Axes were not adjusted to imitate the paper.

---

## Raw data

- Run-level metrics: `results/raw/results.csv` (one row per run × concession case)
- Final populations for figure problems: `results/raw/populations/*.npz` (`X`, `F`, `seed`, `problem`, `algorithm`)
- Per-job JSON (optional, not required to inspect conclusions): `results/raw/job_rows/`
- Aggregates: `results/aggregated/summary.csv`

Populations for non-figure problems can be regenerated with the same seeds via `python -m experiments.zm26_reproduction.runners.run_all`.

---

## Files to read first

1. `PAPER_PARAMETER_AUDIT.md`
2. `CLAIM_VALIDATION.md`
3. `results/reproduction_summary.json`
4. `results/paper_comparison/paper_vs_python.csv`
5. this file
