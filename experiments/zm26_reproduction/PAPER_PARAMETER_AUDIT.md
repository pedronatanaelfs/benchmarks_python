# Paper parameter audit

Primary paper: Zhao, Xu & Luo, *Fairness-Aware Performance Evaluation for Multi-Party Multi-Objective Optimization*, arXiv:2601.22497, accepted IEEE TEVC.

Official MATLAB metric: `2026ZhaoNash-main/nash-score/nash_score.m`.
Official algorithms: OptMPNDS-master (Liu 2020) and `sources/mpdmp_2023/2022SheOptMPNDS3` (She 2023).

| Parameter | Value used | Source | Exact location | Status |
|---|---:|---|---|---|
| independent runs | 30 | ZM26 | Section V-A1 | CONFIRMED |
| MPMOP D | 2 | ZM26 | Table II caption | CONFIRMED |
| MPMOP12–17 D | 10 | MATLAB classdef `Global.D=10` | `2026ZhaoNash-main/MPMOP/MPMOP12.m` | CONFIRMED |
| MPDMP D | 2 | problem definition | MPDMP classdefs | CONFIRMED |
| MPMOP population size | 100 | Liu/PlatEMO GLOBAL default and `Multi_conclude.m` | `GLOBAL.N=100` | INFERRED_FROM_ORIGINAL_CODE |
| MPDMP population size | 200 | She 2023 | Section 5.1 | CONFIRMED |
| MPMOP evaluation budget | 10000 | PlatEMO `GLOBAL.evaluation` | `OptMPNDS-master/Public/GLOBAL.m` | INFERRED_FROM_ORIGINAL_CODE |
| MPDMP evaluation budget | 80000 | She 2023 | Section 5.1 | CONFIRMED |
| MPMOP crossover | SBX pc=1, ηc=20 | PlatEMO `GA.m` defaults | `Public/GA.m` | INFERRED_FROM_ORIGINAL_CODE |
| MPMOP mutation | PM, E[mutated bits]=1, ηm=20 | PlatEMO `GA.m` | `Public/GA.m` | INFERRED_FROM_ORIGINAL_CODE |
| MPDMP crossover | SBX pc=1, ηc=15 | She 2023 | Section 5.1 | CONFIRMED |
| MPDMP mutation | PM, pm=0.5, ηm=20 | She 2023 | Section 5.1 | CONFIRMED |
| OptMPNDS3 FEI | 10000 / party (first two DMs) | She 2023 + `getPF.m` | Section 5.1; `getPF.m` | CONFIRMED |
| OptMPNDS3 JADE p, c | 0.05, 0.05 | She 2023 | Section 5.1 | CONFIRMED |
| concession original suites | all zeros | ZM26 | Section V-A4 | CONFIRMED |
| concession non-consensus cases | Table S-IV six cases | ZM26 appendix | Table S-IV | CONFIRMED |
| PF sample size | 2000 | official MATLAB | `nash_score.m` `'PFSampleSize'` | INFERRED_FROM_ORIGINAL_CODE |
| Offset PF sample | 5000 | official MATLAB | `compute_offset_to_pf.m` | INFERRED_FROM_ORIGINAL_CODE |
| IGD | Euclidean mean min distance, party-wise | PlatEMO/She IGD | `IGD_GD.m`, `Metrics/IGD.m` | CONFIRMED |
| meanIGD | arithmetic mean of party IGD | ZM26 | Section V-A3 | CONFIRMED |
| Nash log for MPDMP | natural log `ln` | inferred from Table III magnitudes vs Appendix S-I C | Table III + S-I | INFERRED_FROM_ORIGINAL_CODE |
| Nash utility | paper `C - L_m` for reported Ψ; MATLAB `exp(-L_m)` also stored | Theorem 1 vs `nash_score.m` | paper Eq. after Lemma 4; MATLAB line `exp(-L_m)` | see discrepancy below |
| Nash constant C | estimated as `max L + 1` from a random population on each problem | Appendix S-I | Appendix S-I | INFERRED_FROM_ORIGINAL_CODE |
| lambda | Appendix S-II formula on other DMs' PF points | Appendix S-II | Appendix S-II | INFERRED_FROM_ORIGINAL_CODE |
| Wilcoxon / Holm / Friedman | implemented on 30-run vectors | not named in ZM26 main text | — | UNRESOLVED whether ZM26 used Holm; implemented as requested |

## Unresolved items (not silently invented)

1. **Exact C used in Tables II–III.** Appendix S-I describes NSGA-II, 10 runs, `C = max_m L̂_m + δ`. No numerical C or δ is published. Absolute Ψ values are therefore **not expected to match**. Rankings within a problem are the comparable quantity.
2. **MATLAB `nash_score.m` uses `u=exp(-L)`**, which equals `exp(-sum L_m)` and **does not implement Balance Preference (Axiom 3)**. The paper Theorem 1 uses `u=C-L`. Reproduction stores both; claim analysis uses the paper formula.
3. **ZM26 MPMOP evaluation budget** is not stated. Liu's `Multi_conclude.m` used `1000*D*n_dm` at D=10. We used GLOBAL default 10000 at D=2.
4. **ZM26 does not name Wilcoxon/Holm/Friedman** in the main experimental section. Tests were still run as requested.
5. **Jain/Gini** appear in Appendix Table S-III as axiom comparisons, not as optimizer-result tables for MPMOP12/13. We still compute them on party IGD / utilities for those problems.
6. **Party-wise PF API for MPMOP3/6/11** returns `None`; the reproduction evaluates the **common PS** (`get_pareto_set(dm=None)`) per DM. **MPMOP4/9** have no executable MATLAB `true_PS` mesh (20000×20000). The reproduction samples the equivalent manifold `sin(2π(x1+x2))=0` in the experimental `D`. Objective equations in `src/fairmoo_benchmarks/` were not modified.
7. **Unequal objectives per DM (MPDMP3, MPDMP10).** Official `nash_score.m` requires `M % dm_num == 0`. ZM26 Table III still reports these problems. Python Nash uses party slices; cross-DM PF geometry is skipped when objective dimensions differ. `λ=1` in that case.

## Algorithm source map

| Python | MATLAB |
|---|---|
| `algorithms/optall.py` | `OptMPNDS-master/Algorithms/OptAll/OptAll.m` |
| `algorithms/optmpnds.py` | `OptMPNDS-master/Algorithms/OptMPNDS/OptMPNDS.m` + She `MPNDS.m` cell-DM slices |
| `algorithms/optmpnds2.py` | `2022SheOptMPNDS3/Algorithms/OptMPNDS2/OptMPNDS2.m` + `PLNDS.m` |
| `algorithms/optmpnds3.py` | `2022SheOptMPNDS3/Algorithms/OptMPNDS3/OptMPNDS3.m` |
| `algorithms/operators.py` | `GA.m`, `NDSort.m`, `CrowdingDistance.m`, `CrowdingEntropy.m`, `TournamentSelection.m` |
| `metrics/nash_score.py` | `nash-score/nash_score.m`, `compute_offset_to_pf.m` |
