# MPDMP1–12 IGD reference audit

Primary MATLAB path (She 2023, used by ZM26 Table III magnitudes):

1. `GLOBAL.NotTermination` stores `obj.PF = obj.problem.PF()`.
2. `GLOBAL.Metric(@IGD, Population, obj.PF, obj.DM)` calls `Metrics/IGD.m`.
3. `IGD.m` does **not** average party-wise IGDs. It sums party `pdist2` blocks, then `min` over the approximation, then `mean` over PF points.

```matlab
for i = 1:length(DM)
    temp = pdist2(PF(:, DM{i}), obj(:, DM{i}));
    dis = dis + temp;
end
grades = min(dis, [], 2);
score = [mean(grades), min(grades)];
```

ZM26 Section V-A3 *describes* meanIGD as the arithmetic mean of party-wise IGD. The **executable** MPDMP path in the She repository that produced Table-III-scale numbers is `IGD.m` + `problem.PF()`. The MPDMP4 diagnostic matched paper `9.58e-4` only under that definition.

The previous Python column `meanIGD` is therefore renamed conceptually to `party_pf_meanIGD` (sampled per-DM geometric PF). The reproduction metric is `zm26_meanIGD`.

| Problem | MATLAB PF source | IGD reference shape | Per-party mean of IGDs? | Python previous behavior | Match? |
|---|---|---|---|---|---|
| MPDMP1 | `MPDMP1.PF`: `[20√2]*4` (analytical common-PS image) | 1 × 4 | No — She `IGD.m` on that row | party triangle/line PFs, mean of 2 IGDs | **No** |
| MPDMP2 | `trapezoid1.PF` of PS `(130/3, 170/3)` | 1 × 4 | No | party PFs | **No** |
| MPDMP3 | `LinearMap.PF` = `EuclideanDistance` of line ∩ triangle (`linspace` 10000) | N × 5 (N = in-triangle segment) | No | party PFs (line vs triangle), unequal M | **No** |
| MPDMP4 | `MPDMP4.PF` = `CalObj([50,40])` | 1 × 6 | No | party triangle PFs (2000 pts each) | **No** |
| MPDMP5 | `polygon.PF` = grid intersection of two `nsidedpoly` triangles | N × 6 | No | party triangle PFs | **No** |
| MPDMP6 | `MPDMP6.PF` = `EuclideanDistance` of common edge `(50, linspace(40,60,10000))` | 10000 × 8 | No | party square PFs | **No** |
| MPDMP7 | `polygon.PF` grid intersection of two squares | N × 8 | No | party square PFs | **No** |
| MPDMP8 | `polygon.PF` grid intersection of two pentagons | N × 10 | No | party pentagon PFs | **No** |
| MPDMP9 | `MPDMP9.PF` = `fitness([50,50])` | 1 × 6 | No | party PFs (3 DMs) | **No** |
| MPDMP10 | `Map10.PF` = `EuclideanDistance([50,50])` | 1 × 8 | No | party PFs (unequal DM sizes) | **No** |
| MPDMP11 | `polygon.PF` 3-triangle intersection | N × 9 | No | party triangle PFs | **No** |
| MPDMP12 | `polygon.PF` 3-square intersection | N × 12 | No | party square PFs | **No** |

## What `zm26_meanIGD` implements

- Reference = MATLAB `problem.PF()` reconstructed in `metrics/matlab_mpdmp_pf.py` (reproduction layer, not the benchmark package).
- Score = She `IGD.m` (`metrics/she_igd.py`).
- One concatenated PF, DM slices only for the summed `pdist2` blocks.

## What `party_pf_meanIGD` keeps

- `problem.get_pareto_front(dm=…)` / `reference_fronts`.
- Arithmetic mean of party-wise Euclidean IGD.
- Useful for fairness diagnostics (Claims 1–2 style disparities). **Not** the official MPDMP Table III metric.

## Saved populations

The 30-run campaign stored `X,F` only for `FIGURE_PROBLEMS`. Among MPDMP1–12 that is **MPDMP6** and **MPDMP8** (`results/raw/populations/`, 30 seeds × 4 algorithms). Those files **are** in the tree and were rescored to `zm26_meanIGD`.

MPDMP1 and MPDMP4 have 5-seed validation populations under `results/validation/populations/` (corrected `proM/D` mutation). Those are **new** searches, not overlays onto the original 30-run rows.

Without `F`, the old `party_pf_meanIGD` scalar cannot be converted. MPDMP2, 3, 5, 7, 9–12 therefore remain INCONCLUSIVE for the official metric.

Rescore outputs:

- `results/paper_comparison/mpdmp_igd_rescored.csv`
- `results/paper_comparison/mpdmp_igd_rescored_summary.csv`
- `results/paper_comparison/mpdmp_table_iii_corrected.md`
