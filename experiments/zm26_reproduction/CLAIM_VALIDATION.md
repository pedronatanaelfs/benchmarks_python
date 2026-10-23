# Claim validation

Paper: Fairness-Aware Performance Evaluation for Multi-Party Multi-Objective Optimization ([arXiv:2601.22497](https://arxiv.org/abs/2601.22497))
Baseline git commit of the benchmark package: `0a46ba82f56b13c269ee763b717507c7c4c5f175`
Optimizer runs in `results/raw/results.csv`: **3180** (30 seeds × 17 MPMOP × 2 algorithms + 18 MPDMP × 4 algorithms)
Evaluation rows: **8580** (non-consensus problems scored under all six Table S-IV concession cases)
MPDMP metric correction (2026-10-22): official Table III score is `zm26_meanIGD`; historical `meanIGD` is `party_pf_meanIGD`.

Statuses used below: `SUPPORTED` / `PARTIALLY SUPPORTED` / `NOT SUPPORTED` / `INCONCLUSIVE`.

---

## Before / after the MPDMP metric correction

| Claim | Previous status | Corrected status | Reason |
|---|---|---|---|
| 1 | SUPPORTED | **SUPPORTED** | Party-IGD hiding effect is independent of the She `IGD.m` reference. MPMOP15/17 examples unchanged. |
| 2 | SUPPORTED | **SUPPORTED** | Same party-wise columns as Claim 1. `party_pf_meanIGD` is kept for this diagnostic. |
| 3 | SUPPORTED | **SUPPORTED** | Nash still uses party IGD + concession in \(C-L\). MPMOP1/15 examples unchanged. |
| 4 | SUPPORTED (MPMOP1–11 only; MPDMP search written off) | **SUPPORTED** | MPMOP Nash ranking still 9/11. Corrected MPDMP `zm26_meanIGD` now shows OptMPNDS/2 much closer to the common-PS image than OptAll, which is the Table III common-region story. |
| 5 | PARTIALLY SUPPORTED | **PARTIALLY SUPPORTED** | Concession cases were evaluation-only; not affected by the IGD-reference fix. 16/36 pairs still increase along the equal-threshold sequence. |
| 6 | PARTIALLY SUPPORTED | **PARTIALLY SUPPORTED** | Same unpublished-`C` and clipping caveats. |
| 7 | SUPPORTED (MPDMP swap was Python-only and opposite to Table III) | **SUPPORTED** | MPMOP1/2/4/7/8/9 ranking swaps remain. The MPDMP “OptAll best meanIGD / MPNDS best Nash” swap was an artifact of `party_pf_meanIGD`. Under `zm26_meanIGD`, OptMPNDS/2 beat OptAll, agreeing with Table III on that qualitative ranking. |

---

## Claim 1 — meanIGD can hide disparities between DMs

**SUPPORTED**

Party IGD ratio \( \max(IGD_1,IGD_2)/\min(IGD_1,IGD_2) > 2 \) (mean of 30 runs):

| Benchmark | Algorithm | IGD_DM1 | IGD_DM2 | meanIGD | ratio |
|---|---|---:|---:|---:|---:|
| MPMOP15 | OptAll | 0.1403 | 0.7016 | 0.3243 | 5.00 |
| MPMOP17 | OptAll | 0.1403 | 0.7016 | 0.3243 | 5.00 |
| MPMOP15 | OptMPNDS | 0.1773 | 0.801 | 0.3966 | 4.52 |
| MPMOP17 | OptMPNDS | 0.1773 | 0.801 | 0.3966 | 4.52 |
| MPDMP3 | OptMPNDS3 | 2.929 | 10.85 | 6.889 | 3.70 |

On MPMOP15 OptAll the average (0.32) looks “moderate” while DM2 is five times farther from its PF than DM1. That is exactly the hiding effect ZM26 describes.

The MPDMP Table III official score (`zm26_meanIGD`) is a different quantity: She `IGD.m` on a common `problem.PF()`. It can be tiny while `party_pf_meanIGD` stays large (MPDMP4 OptMPNDS: `3.7e-4` vs `~19`). That is further evidence that an average / single-reference IGD can hide party geometry — Claims 1–2 are about *party-wise* IGD, so they continue to use `party_pf_meanIGD`.

---

## Claim 2 — Party-wise IGD reveals disparities hidden by meanIGD

**SUPPORTED**

Same numbers as Claim 1. The party-wise columns, not the average, identify which DM is left behind. See `figures/party_igd_disparity.png`.

---

## Claim 3 — Nash score penalizes populations that heavily disadvantage one DM

**SUPPORTED**

Utility is the paper formula \( u_m = C - L_m \) with \( L_m = \mu_m + \lambda_m L_{\mathrm{pen}} \). A large party IGD or concession penalty shrinks that factor in the product.

Concrete example (means over 30 runs, case 1):

- **MPMOP1 OptAll**: meanIGD **0.025** (better than OptMPNDS **0.199**), but Nash is **lower** (OptAll loses the product ranking to OptMPNDS). Paper Table II shows the same ranking swap.
- **MPMOP15 OptAll**: IGD_DM2 / IGD_DM1 ≈ 5. The product is pulled down by the weak party even though meanIGD remains finite.

The MATLAB `nash_score.m` formula \( u_m=\exp(-L_m) \) is also stored (`nash_score_exp`) and does **not** implement Axiom 3; claim analysis uses the paper \( C-L \) product.

---

## Claim 4 — With a common Pareto-optimal region, Nash rewards mutually good solutions

**SUPPORTED**

On MPMOP1–11 (common PS exists; ZM26 Table II, D=2):

| Benchmark | Paper best meanIGD | Python best meanIGD | Paper best Nash | Python best Nash | Nash ranking match |
|---|---|---|---|---|---|
| MPMOP1 | OptAll | OptAll | OptMPNDS | OptMPNDS | yes |
| MPMOP2 | OptAll | OptAll | OptMPNDS | OptMPNDS | yes |
| MPMOP3 | OptMPNDS | OptMPNDS | OptMPNDS | OptMPNDS | yes |
| MPMOP4 | OptMPNDS | OptMPNDS | OptAll | OptAll | yes |
| MPMOP5 | OptMPNDS | OptAll | OptAll | OptMPNDS | no |
| MPMOP6 | OptMPNDS | OptMPNDS | OptMPNDS | OptAll | no |
| MPMOP7 | OptMPNDS | OptAll | OptMPNDS | OptMPNDS | yes |
| MPMOP8 | OptMPNDS | OptAll | OptMPNDS | OptMPNDS | yes |
| MPMOP9 | tie | OptMPNDS | OptAll | OptAll | yes |
| MPMOP10 | OptAll | OptMPNDS | OptMPNDS | OptMPNDS | yes |
| MPMOP11 | OptMPNDS | OptMPNDS | OptMPNDS | OptMPNDS | yes |

**Nash ranking matches Table II on 9/11 problems.** Absolute Ψ magnitudes do not match (unpublished C). meanIGD ranking matches 7/11; Python meanIGD values are systematically smaller than Table II, so this is qualitative/partial numerical agreement, not EXACT.

MPDMP1–12 also have a common PS. After switching the official score to `zm26_meanIGD` (MATLAB `problem.PF()` + She `IGD.m`):

| Problem | n | Paper OptMPNDS | Python zm26 OptMPNDS | Paper OptAll | Python zm26 OptAll | OptMPNDS/2 beat OptAll? |
|---|---:|---:|---:|---:|---:|---|
| MPDMP1 | 5 | 0.0545 | 0.0515 | 4.04 | 4.88 | yes |
| MPDMP4 | 5 | 9.58e-4 | 3.67e-4 | 0.0178 | 0.0102 | yes |
| MPDMP6 | 30 | 0.132 | 0.165 | 3.23 | 2.98 | yes |
| MPDMP8 | 30 | 2.46 | 2.43 | 6.23 | 6.12 | yes |

The previous report treated MPDMP search as failed because party-triangle IGD was ~19. That was the wrong reference. After fixing last-generation truncation, 5-seed OptMPNDS3 is CLOSE to Table III on the four problems with saved `F`:

| Problem | n | Paper OptMPNDS3 | Python zm26 | n_final |
|---|---:|---:|---:|---:|
| MPDMP1 | 5 | 0.0447 | 0.0366 | 200 |
| MPDMP4 | 5 | 0.0133 | 0.00989 | 200 |
| MPDMP6 | 5 | 0.0838 | 0.0869 | 200 |
| MPDMP8 | 5 | 2.25 | 2.254 | 200 |

That is additional support for Claim 4. Pre-fix 30-run OptMPNDS3 (`1.62` / `16.71` on MPDMP6/8) was the leftover-FE collapse and must not be quoted.

---

## Claim 5 — Without a common PS, concession-based evaluation identifies compromises

**PARTIALLY SUPPORTED**

MPMOP12–17 and MPDMP13–18 were scored under all six Table S-IV cases on the **same** 30 populations (evaluation-only, not search).

- Along the equal-threshold sequence (case1 → case3 → case5 → case6) Nash increased for **16/36** algorithm–problem pairs.
- On MPMOP12/13 the increase is real but tiny, because estimated `C` is huge relative to \( L_{\mathrm{pen}} \), so \( \prod (C-L_m) \) barely moves.
- On MPDMP15 some mid-threshold cases clip to **Nash = 0** (`C - L_m ≤ 0` for a party). That is interpretable as “penalty exceeded the unpublished scale C”, but it is not a smooth concession ranking of compromises.

Figures: `figures/concession_sensitivity_mpmop.png`, `figures/concession_sensitivity_mpdmp.png`.

---

## Claim 6 — Changing concession thresholds changes Nash scores interpretably

**PARTIALLY SUPPORTED**

Direction is usually “more equal concession → higher or equal Nash” when utilities stay positive. The effect is **not** always large or monotone, because:

1. `C` is estimated as `max L + 1` on a random population (Appendix S-I; paper C unpublished).
2. `λ` depends on `ε` (Appendix S-II), so raising `ε` can change the penalty scale, not only the indicator \( \phi \).
3. Clipping at `u_m ≤ 0` produces zeros (MPDMP15 case3).

So the mechanism is visible, but it is not a clean table-ready monotonicity result under our C.

---

## Claim 7 — meanIGD and Nash can rank algorithms differently

**SUPPORTED**

**25 of 35** benchmarks have a different winner for historical `meanIGD` (`party_pf_meanIGD`) vs Nash in the Python 30-run archive.

Paper-reproduced ranking swaps that still hold:

| Benchmark | Best meanIGD | Best Nash | Ranking differs? | Why |
|---|---|---|---|---|
| MPMOP1 | OptAll | OptMPNDS | yes | Matches Table II: OptAll closer on average, OptMPNDS wins the product |
| MPMOP2 | OptAll | OptMPNDS | yes | Same Table II swap |
| MPMOP4 | OptMPNDS | OptAll | yes | Matches Table II (Nash slightly prefers OptAll) |
| MPMOP7 | OptAll | OptMPNDS | yes | Nash agrees with Table II; meanIGD winner differs from the paper |
| MPMOP8 | OptAll | OptMPNDS | yes | Same pattern as MPMOP7 |
| MPMOP9 | OptMPNDS | OptAll | yes | Matches Table II Nash winner |
| MPMOP3 | OptMPNDS | OptMPNDS | no | Same winner |
| MPMOP11 | OptMPNDS | OptMPNDS | no | Same winner |
| MPMOP12–17 | OptAll | OptAll | no | No common PS; OptAll also wins Nash in this reproduction |

**MPDMP1–12 after the metric correction.** Table III reports the MPNDS family best on **both** meanIGD and log-Nash. Python `party_pf_meanIGD` had OptAll best IGD (the old FAILED table). Python `zm26_meanIGD` has OptMPNDS/2 better than OptAll wherever `F` exists, so the official reproduction metric **no longer disagrees** with Nash on “OptAll vs MPNDS/2”. That agrees with the paper’s Table III qualitative ranking. After the last-generation fix, OptMPNDS3 is first on MPDMP6/8 (as in the paper) and third on MPDMP4 (as in the paper). Pre-fix OptMPNDS3 30-run numbers were the leftover-FE collapse.

Do not cite the old party-triangle MPDMP swap as a reproduction of Table III. It remains a valid illustration that **a different IGD definition** can reverse algorithm ranking — which is itself a Claim 1/7-style warning.

Full historical table: `results/paper_comparison/paper_vs_python.csv`.
Corrected MPDMP IGD: `results/paper_comparison/mpdmp_table_iii_corrected.md`.

---

## Core scientific question

> Does our Python reproduction reproduce the core empirical message of ZM26 that average convergence metrics such as meanIGD may fail to reflect fairness between decision makers, while a concession-aware Nash-product evaluation better captures balanced multi-party compromises?

**MOSTLY YES**

- The hiding of party disparity by meanIGD is recovered (Claims 1–2), with large examples on MPMOP15/17, and independently by the MPDMP4 pair (`zm26_meanIGD ~ 1e-4` vs `party_pf_meanIGD ~ 19`).
- Table II Nash rankings are largely recovered (9/11), including the OptAll vs OptMPNDS swaps on MPMOP1/2.
- Table III MPDMP meanIGD **scale and OptMPNDS/2 vs OptAll ranking** are recovered where final populations exist. This was previously reported as FAILED because the Python column used a different reference set.
- OptMPNDS3 on MPDMP1/4/6/8 is now CLOSE to Table III after the last-generation truncation fix. Pre-fix OptMPNDS3 30-run numbers remain invalid.
- Concession sensitivity is present but weak/partial under our estimated C.
- Eight of twelve Table III problems still lack saved `F`, so those cells stay INCONCLUSIVE rather than claimed as numerical matches.
