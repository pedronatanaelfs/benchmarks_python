# MPMOP15 Audit

## Source
- ZM26 Appendix Table S-VI
- Equations verified via pdftotext of Appendix.pdf

## Python current
- `src/fairmoo_benchmarks/mpmop/mpmop15.py`
- Default `n_var=10` with metadata `dimension_status=ASSUMED_DEFAULT`

## Difference
- Numeric D not fixed in Table S-VI.
- ZM26 D=2 caption applies to MPMOP1–11 experiments only.

## Decision
**KEEP** formulas; dimension remains ASSUMED_DEFAULT=10.

## Validation
- Analytical g=1 on party PS (where applicable)
- Final status: **PARTIAL** (dimension assumption)
