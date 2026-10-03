# Contributing

Contributions that improve scientific fidelity, documentation, or validation
are welcome.

## Guidelines

1. Prefer primary sources (papers / author MATLAB) over third-party ports.
2. Do not invent missing bounds, Pareto sets, fronts, or parameters.
3. Mark unresolved ambiguities as `NEEDS_MANUAL_VERIFICATION`.
4. Keep the public API and documentation in **English**.
5. Add or update tests for any behavioral change.
6. Do not modify vendored MATLAB sources under `sources/` solely to force
   Octave compatibility; record `OCTAVE_INCOMPATIBLE` instead.

## Development setup

```bash
conda env create -f environment.yml
conda activate fairmoo-benchmarks
pytest -q
```

## Pull requests

Please include:

- a short summary of the scientific motivation
- source references (paper section / MATLAB file)
- validation status (`PASS` / `PARTIAL` / `NEEDS_MANUAL_VERIFICATION`)
- test output (at least the affected suite)
