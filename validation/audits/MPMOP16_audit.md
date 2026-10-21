# MPMOP16 Audit

## Source
- Executable MATLAB: `2026ZhaoNash-main/MPMOP/MPMOP16.m` and `MPMOP_Value.m`
- MATLAB: `M=4`, `DM=2`, `D=10`, unit bounds

## Python current
- `src/fairmoo_benchmarks/mpmop/mpmop16.py`
- `n_obj_per_dm=[2, 2]`, default `n_var=10`

## Decision
**ALIGN** to MATLAB classdef (`M=4`, two parties), not Appendix Table S-VI.

## Validation
- Licensed-MATLAB objectives: PASS
- Licensed-MATLAB PS/PF: PASS
- Final status: **PASS**
