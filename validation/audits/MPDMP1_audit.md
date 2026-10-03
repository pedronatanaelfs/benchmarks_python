# MPDMP1 Audit

## Source
- She et al. 2023 + `sources/mpdmp_2023/2022SheOptMPNDS3/Problems/MPDMP/`
- Detail: square.m explicit points

## Python current
- `src/fairmoo_benchmarks/mpdmp/she2023.py` (`MPDMP1`)

## Difference
- Full PlatEMO classdefs are OCTAVE_INCOMPATIBLE.
- Geometry reproduced from author `.m` constructors + MathWorks `nsidedpoly` docs where used.

## Decision
**KEEP**

## Validation
- Analytical zero-at-reference tests
- Geometry unit tests for nsidedpoly convention
- Final status: **PASS**
