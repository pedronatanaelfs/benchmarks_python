# MPDMP1–12 Table III comparison (corrected `zm26_meanIGD`)

Official reproduction metric: She `IGD.m` on MATLAB `problem.PF()`.
Historical `meanIGD` in `results/raw/results.csv` is `party_pf_meanIGD` and is **not** the Table III score.

`n=5` = 5-seed four-algorithm validation (MPDMP1/4).
`n=30` = original 30-run `F` for OptAll / OptMPNDS / OptMPNDS2 on MPDMP6/8, or post-fix OptMPNDS3 in `results/validation/optmpnds3_30seed/`.
`n=0` = no saved `F`; cannot convert the old scalar.
Pre-fix OptMPNDS3 30-run `zm26` on MPDMP6/8 (`1.616` / `16.71`) is invalid (`n` collapsed to ~16) and is not shown.

| Problem | Algorithm | Paper meanIGD | Old party-PF | Corrected zm26 | n | rel. diff | Level |
|---|---|---:|---:|---:|---:|---:|---|
| MPDMP1 | OptAll | 4.04 | 0.8895 | 4.881 | 5 | 0.2081 | CLOSE |
| MPDMP1 | OptMPNDS | 0.0545 | 15.47 | 0.05149 | 5 | 0.05514 | CLOSE |
| MPDMP1 | OptMPNDS2 | 0.0476 | 15.35 | 0.03109 | 5 | 0.3469 | CLOSE |
| MPDMP1 | OptMPNDS3 | 0.0447 | 12.26 | **0.04066** | 30 | 0.0903 | CLOSE (last-gen fix; was 2.961) |
| MPDMP2 | OptAll | 3.94 | 0.7207 | — | 0 | — | INCONCLUSIVE |
| MPDMP2 | OptMPNDS | 0.0649 | 12.09 | — | 0 | — | INCONCLUSIVE |
| MPDMP2 | OptMPNDS2 | 0.0617 | 13.04 | — | 0 | — | INCONCLUSIVE |
| MPDMP2 | OptMPNDS3 | 0.0577 | 7.693 | **0.06752** | 30 | 0.170 | CLOSE |
| MPDMP3 | OptAll | 2.73 | 1.207 | — | 0 | — | INCONCLUSIVE |
| MPDMP3 | OptMPNDS | 0.211 | 7.631 | — | 0 | — | INCONCLUSIVE |
| MPDMP3 | OptMPNDS2 | 0.215 | 7.569 | — | 0 | — | INCONCLUSIVE |
| MPDMP3 | OptMPNDS3 | 0.113 | 6.889 | **0.1478** | 30 | 0.308 | CLOSE |
| MPDMP4 | OptAll | 0.0178 | 2.452 | 0.01019 | 5 | 0.4274 | CLOSE |
| MPDMP4 | OptMPNDS | 0.000958 | 19.21 | 0.0003666 | 5 | 0.6173 | QUALITATIVE |
| MPDMP4 | OptMPNDS2 | 0.00105 | 19.3 | 0.0008353 | 5 | 0.2044 | CLOSE |
| MPDMP4 | OptMPNDS3 | 0.0133 | 17.95 | **0.01270** | 30 | 0.0450 | CLOSE (last-gen fix; was 0.0644) |
| MPDMP5 | OptAll | 6.9 | 3.449 | — | 0 | — | INCONCLUSIVE |
| MPDMP5 | OptMPNDS | 2.97 | 9.181 | — | 0 | — | INCONCLUSIVE |
| MPDMP5 | OptMPNDS2 | 2.94 | 9.189 | — | 0 | — | INCONCLUSIVE |
| MPDMP5 | OptMPNDS3 | 2.66 | 14.49 | **2.664** | 30 | 0.00165 | CLOSE |
| MPDMP6 | OptAll | 3.23 | 2.045 | 2.982 | 30 | 0.07682 | CLOSE |
| MPDMP6 | OptMPNDS | 0.132 | 14.17 | 0.1651 | 30 | 0.2505 | CLOSE |
| MPDMP6 | OptMPNDS2 | 0.13 | 14.16 | 0.1671 | 30 | 0.2857 | CLOSE |
| MPDMP6 | OptMPNDS3 | 0.0838 | 14.33 | **0.08650** | 30 | 0.0322 | CLOSE (last-gen fix; pre-fix 1.616) |
| MPDMP7 | OptAll | 8.93 | 3.804 | — | 0 | — | INCONCLUSIVE |
| MPDMP7 | OptMPNDS | 2.45 | 15.47 | — | 0 | — | INCONCLUSIVE |
| MPDMP7 | OptMPNDS2 | 2.45 | 15.51 | — | 0 | — | INCONCLUSIVE |
| MPDMP7 | OptMPNDS3 | 2.26 | 15.89 | **2.306** | 30 | 0.0205 | CLOSE |
| MPDMP8 | OptAll | 6.23 | 2.953 | 6.124 | 30 | 0.01706 | CLOSE |
| MPDMP8 | OptMPNDS | 2.46 | 9.234 | 2.428 | 30 | 0.01304 | CLOSE |
| MPDMP8 | OptMPNDS2 | 2.46 | 9.26 | 2.425 | 30 | 0.01411 | CLOSE |
| MPDMP8 | OptMPNDS3 | 2.25 | 15.17 | **2.279** | 30 | 0.0129 | CLOSE (last-gen fix; pre-fix 16.71) |
| MPDMP9 | OptAll | 6.71 | 0.9334 | — | 0 | — | INCONCLUSIVE |
| MPDMP9 | OptMPNDS | 0.031 | 13.39 | — | 0 | — | INCONCLUSIVE |
| MPDMP9 | OptMPNDS2 | 0.0215 | 13.26 | — | 0 | — | INCONCLUSIVE |
| MPDMP9 | OptMPNDS3 | 0.203 | 10.5 | **0.03712** | 30 | 0.817 | QUALITATIVE (Python better; paper OptMPNDS3 is ~6× OptMPNDS) |
| MPDMP10 | OptAll | 6.55 | 1.521 | — | 0 | — | INCONCLUSIVE |
| MPDMP10 | OptMPNDS | 0.0964 | 14.13 | — | 0 | — | INCONCLUSIVE |
| MPDMP10 | OptMPNDS2 | 0.0845 | 14.44 | — | 0 | — | INCONCLUSIVE |
| MPDMP10 | OptMPNDS3 | 0.0699 | 12.78 | **0.07218** | 30 | 0.0327 | CLOSE |
| MPDMP11 | OptAll | 1.79 | 1.896 | — | 0 | — | INCONCLUSIVE |
| MPDMP11 | OptMPNDS | 1.39 | 7.744 | — | 0 | — | INCONCLUSIVE |
| MPDMP11 | OptMPNDS2 | 1.38 | 7.872 | — | 0 | — | INCONCLUSIVE |
| MPDMP11 | OptMPNDS3 | 1.19 | 8.362 | **1.192** | 30 | 0.00173 | CLOSE |
| MPDMP12 | OptAll | 10.2 | 2.907 | — | 0 | — | INCONCLUSIVE |
| MPDMP12 | OptMPNDS | 2.74 | 8.736 | — | 0 | — | INCONCLUSIVE |
| MPDMP12 | OptMPNDS2 | 2.78 | 8.698 | — | 0 | — | INCONCLUSIVE |
| MPDMP12 | OptMPNDS3 | 2.79 | 9.209 | **2.611** | 30 | 0.0640 | CLOSE |

## Rankings where `F` exists

| Problem | Paper ranking | Corrected Python ranking | Full match | OptAll worse than OptMPNDS/2 |
|---|---|---|---|---|
| MPDMP1 | OptMPNDS3,OptMPNDS2,OptMPNDS,OptAll | OptMPNDS2,OptMPNDS3,OptMPNDS,OptAll | False | True |
| MPDMP4 | OptMPNDS,OptMPNDS2,OptMPNDS3,OptAll | OptMPNDS,OptMPNDS2,OptMPNDS3,OptAll | True | True |
| MPDMP6 | OptMPNDS3,OptMPNDS2,OptMPNDS,OptAll | OptMPNDS3,OptMPNDS,OptMPNDS2,OptAll | False (2nd/3rd of near-tied OptMPNDS/2) | True |
| MPDMP8 | OptMPNDS3,OptMPNDS,OptMPNDS2,OptAll | OptMPNDS3,OptMPNDS2,OptMPNDS,OptAll | False (2nd/3rd of near-tied OptMPNDS/2) | True |
