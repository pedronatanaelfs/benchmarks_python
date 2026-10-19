# MATLAB execution status

Local MATLAB execution was initially attempted on 2026-10-19 with:

```text
matlab -batch "disp(version)"
```

The runtime stopped before executing MATLAB code with **MathWorks Licensing
Error 9**: the host ID in the installed license does not match this computer.
This is a definitive local license blocker, not a benchmark or harness error.

The harness was subsequently run by the user in a licensed MATLAB
environment. All 35 objective CSVs and all 35 metadata JSON files were
generated successfully, with no `failures.txt`. These outputs are now the
reference used by `numerical_comparison.csv`.

No Octave result was used as proof of final MATLAB equivalence.
