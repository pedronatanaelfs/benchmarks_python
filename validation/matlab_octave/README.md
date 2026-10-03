# MATLAB / Octave equivalence harness

GNU Octave was **not installed** when this package was built (`octave --version` failed).

When Octave becomes available:

1. Export `X` from Python to CSV under this folder.
2. Call the original `.m` evaluators from `sources/OptMPNDS` / `sources/mpdmp_2023/2022SheOptMPNDS3`.
3. Compare with Python via `np.allclose(..., rtol=1e-8, atol=1e-10)`.

Do **not** modify the vendored MATLAB sources only to force Octave compatibility; record `OCTAVE_INCOMPATIBLE` instead.
