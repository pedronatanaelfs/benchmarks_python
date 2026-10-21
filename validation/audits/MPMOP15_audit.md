# MPMOP15 Audit

## Source
- Executable MATLAB: `2026ZhaoNash-main/MPMOP/MPMOP15.m`
- MATLAB `CalObj` calls the MPMOP17 kernel (intentional duplicate)

## Python current
- `src/fairmoo_benchmarks/mpmop/mpmop15.py`
- Default `n_var=10` from MATLAB `obj.Global.D = 10`
- Unit bounds `[0,1]^D`, `M=6`, `DM=3`

## Decision
**ALIGN** to MATLAB, including the MPMOP15→MPMOP17 kernel duplication.

## Validation
- Licensed-MATLAB objectives: PASS
- Licensed-MATLAB PS/PF: PASS
- Final status: **PASS**
