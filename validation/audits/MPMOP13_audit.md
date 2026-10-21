# MPMOP13 Audit

## Source
- Executable MATLAB: `2026ZhaoNash-main/MPMOP/MPMOP13.m` and `MPMOP_Value.m`
- Publication Table S-VI is **not** used where it conflicts with MATLAB

## Python current
- `src/fairmoo_benchmarks/mpmop/mpmop13.py`
- Default `n_var=10` from MATLAB `obj.Global.D = 10`
- Unit bounds `[0,1]^D`, `M=4`, `DM=2`

## Decision
**ALIGN** to MATLAB classdef, not Appendix Table S-VI.

## Validation
- Licensed-MATLAB objectives: PASS
- Licensed-MATLAB PS/PF: PASS
- Final status: **PASS**
