# Diagnostics

## MPDMP meanIGD reversal

On every MPDMP1–12 instance, Python OptAll has a **lower** meanIGD than OptMPNDS / OptMPNDS2 / OptMPNDS3. ZM26 Table III reports the opposite (MPNDS-family near 1e-2–1e-1, OptAll several units).

This folder is for later investigation. Do not retune operators just to chase Table III.

Hypotheses, in order of likelihood:

1. OptMPNDS / PLNDS / JADE2 Python port differences vs She MATLAB (selection, unique-row filter, crowding entropy truncation, archive).
2. Party-wise IGD reference fronts (sample size 2000, MPDMP3/10 unequal objective counts).
3. Evaluation budget / FEI counting during OptMPNDS3 PFt initialization.
4. Paper-version or unpublished extra settings.

Useful columns in `../raw/results.csv`: `IGD_DM1`, `IGD_DM2`, `IGD_DM3`, `meanIGD`, `nash_score`, `log_nash`.
Figure-problem populations: `../raw/populations/MPDMP6_*.npz`, `MPDMP8_*.npz`.

## Nash C scale

`C` is estimated per problem as `max L + 1` on a 40-point random population. Table II Ψ values are O(10)–O(10^13); Python `nash_score` is often O(10^28)–O(10^44). Rankings, not magnitudes, are comparable.

## Stale failure logs

`logs/failures/` held MPDMP3 crashes from the first collector pass (`np.vstack` of 2-obj and 3-obj PFs). The Nash code now skips mismatched PF dimensions. Those jobs were rerun successfully; the stale failure texts were removed.
