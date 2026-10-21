# MPMOP17 Audit

## Source
- Executable MATLAB: `2026ZhaoNash-main/MPMOP/MPMOP17.m` and `MPMOP_Value.m`
- MATLAB: `M=6`, `DM=3`, `D=10`, unit bounds

## Python current
- `src/fairmoo_benchmarks/mpmop/mpmop17.py`
- `n_obj_per_dm=[2, 2, 2]`, default `n_var=10`

## Decision
**ALIGN** to MATLAB classdef (`M=6`, three two-objective parties), not
Appendix Table S-VI.

## Validation
- Licensed-MATLAB objectives: PASS
- Licensed-MATLAB PS/PF: PASS
- Final status: **PASS**
