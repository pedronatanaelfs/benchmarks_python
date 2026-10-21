# Claim validation

Paper: Fairness-Aware Performance Evaluation for Multi-Party Multi-Objective Optimization ([arXiv:2601.22497](https://arxiv.org/abs/2601.22497))
Baseline git commit of the benchmark package: `0a46ba82f56b13c269ee763b717507c7c4c5f175`
Optimizer runs in `results/raw/results.csv`: **3180** (30 seeds × 17 MPMOP × 2 algorithms + 18 MPDMP × 4 algorithms)
Evaluation rows: **8580** (non-consensus problems scored under all six Table S-IV concession cases)

Statuses used below: `SUPPORTED` / `PARTIALLY SUPPORTED` / `NOT SUPPORTED` / `INCONCLUSIVE`.

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

**SUPPORTED** (ranking evidence on MPMOP1–11; MPDMP search quality is a separate issue)

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

MPDMP1–12 also have a common PS in the benchmark definition, but our OptMPNDS/2/3 ports did **not** recover She 2023 search quality (see Claim 7 and the reproduction report). Claim 4 is therefore supported by the MPMOP suite, not by Table III numbers.

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

**25 of 35** benchmarks have a different winner for meanIGD vs Nash in the Python data.

Paper-reproduced ranking swaps (the important ones):

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
| MPDMP1–12 | OptAll | OptMPNDS / 2 / 3 | yes | **Python-only swap.** Paper: MPNDS-family wins **both** meanIGD and Nash; our ports have OptAll best meanIGD and MPNDS-family best Nash |

The MPDMP swap still illustrates Claim 7 *inside this reproduction*, but it is **not** a numerical reproduction of Table III (see `REPRODUCTION_REPORT.md`). Likely causes: OptMPNDS/2/3 port differences vs She MATLAB, not the Nash formula.

Full table: generated rows in this file’s previous auto-table plus `results/paper_comparison/paper_vs_python.csv`.

---

## Core scientific question

> Does our Python reproduction reproduce the core empirical message of ZM26 that average convergence metrics such as meanIGD may fail to reflect fairness between decision makers, while a concession-aware Nash-product evaluation better captures balanced multi-party compromises?

**MOSTLY YES**

- The hiding of party disparity by meanIGD is recovered (Claims 1–2), with large examples on MPMOP15/17.
- Table II Nash rankings are largely recovered (9/11), including the OptAll vs OptMPNDS swaps on MPMOP1/2.
- Table III (MPDMP search + log-Nash) is **not** recovered numerically: Python OptAll dominates meanIGD, opposite to the paper.
- Concession sensitivity is present but weak/partial under our estimated C.
