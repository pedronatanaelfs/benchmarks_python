# ZM26 reproduction

Pure baseline reproduction of Zhao, Xu & Luo (2026), arXiv:2601.22497,
using the validated `fairmoo_benchmarks` package. Benchmark equations are
not modified.

## Commands

From the repository root, with `fairmoo-benchmarks` activated:

```bash
conda activate fairmoo-benchmarks
pip install -e .

# smoke tests
pytest experiments/zm26_reproduction/tests -q

# full 30-run optimization + evaluation
python -m experiments.zm26_reproduction.runners.run_all

# or by family
python -m experiments.zm26_reproduction.runners.run_mpmop
python -m experiments.zm26_reproduction.runners.run_mpdmp

# post-processing
python -m experiments.zm26_reproduction.scripts.aggregate_results
python -m experiments.zm26_reproduction.scripts.compare_with_paper
python -m experiments.zm26_reproduction.scripts.reproduce_tables
python -m experiments.zm26_reproduction.scripts.reproduce_figures
python -m experiments.zm26_reproduction.runners.run_sensitivity
python -m experiments.zm26_reproduction.scripts.write_reports
```

`write_reports` refreshes CSV/JSON summaries and draft markdown under
`results/paper_comparison/`. The scientific reports `CLAIM_VALIDATION.md`
and `REPRODUCTION_REPORT.md` are maintained after inspecting those CSVs.

Resume is the default. Completed jobs are detected from
`results/raw/job_rows/*.json` and `results/raw/results.csv`.
The CSV is rebuilt from per-job JSON at the end of each run.

```bash
# after a crash, just rerun:
python -m experiments.zm26_reproduction.runners.run_all --workers 16
```

## What to read first

1. `PAPER_PARAMETER_AUDIT.md`
2. `REPRODUCTION_REPORT.md`
3. `CLAIM_VALIDATION.md`
4. `results/reproduction_summary.json`
5. `results/paper_comparison/paper_vs_python.csv`

## Design notes

- Concession thresholds are **evaluation** parameters. Each optimizer run is
  stored once and scored under every Table S-IV case that applies.
- Rankings, not absolute Nash magnitudes, are the comparable quantity: the
  paper never publishes the numerical constant `C`.
