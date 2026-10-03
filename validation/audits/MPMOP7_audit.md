# MPMOP7 Audit

## Source MATLAB
- `sources/OptMPNDS/Problems/MPMOP/MPMOP7.m`
- Objectives via `MPMOP_Value.m`
- Default `Global.D = 10` in classdef (ZM26 experiments used D=2 for MPMOP1–11 table)

## Python current
- `src/fairmoo_benchmarks/mpmop/liu2020.py` (`MPMOP7`)
- `mpmop_value` port of `MPMOP_Value.m`

## Difference
- None in objective formulas (Octave equivalence PASS, rtol=1e-8, atol=1e-10).
- Common-PS densification is simplified vs full `true_PS.m` mesh search.

## Decision
**KEEP** objectives. Common-PS sampler remains a documented approximation helper (not required for evaluate()).

## Validation
- Octave `MPMOP_Value`: PASS (`validation/equivalence/MPMOP7.md`)
- Final status: **PASS**
