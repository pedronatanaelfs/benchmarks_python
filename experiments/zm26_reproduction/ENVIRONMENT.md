# Frozen reproduction environment

Recorded before optimizer runs.

```
Git commit: 0a46ba82f56b13c269ee763b717507c7c4c5f175
Python version: 3.12.14
NumPy version: 2.5.3
SciPy version: 1.18.1
pymoo version: 0.6.2
OS: Linux 7.0.0-38-generic x86_64 (Ubuntu 24.04)
CPU: 20 logical processors (pedro-Nitro-ANV15-52)
Number of repository tests: 227 passed, 1 skipped, 0 failed
Test result: PASS
Benchmark validation status: 33 PASS, 2 PARTIAL (MPMOP4/9 PS/PF mesh), 0 FAIL
  Objectives 35/35 PASS vs licensed MATLAB (rtol=1e-9, atol=1e-10)
```

Conda environment: `fairmoo-benchmarks` from `environment.yml`.

ZM26 reproduction unit tests: 20 passed (metrics, Nash, algorithm smoke, PF fallbacks).

No file under `src/fairmoo_benchmarks/` was modified for this reproduction.
