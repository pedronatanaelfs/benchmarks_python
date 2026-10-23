from __future__ import annotations

from pathlib import Path

DIAG_ROOT = Path(__file__).resolve().parents[1]
SHARED = DIAG_ROOT / "shared_inputs"
MATLAB_OUT = DIAG_ROOT / "matlab_outputs"
PYTHON_OUT = DIAG_ROOT / "python_outputs"
COMPARISONS = DIAG_ROOT / "comparisons"
REPO_ROOT = DIAG_ROOT.parents[2]
SHE_SRC = REPO_ROOT / "sources" / "mpdmp_2023" / "2022SheOptMPNDS3"


def ensure_dirs() -> None:
    for p in (SHARED, MATLAB_OUT, PYTHON_OUT, COMPARISONS):
        p.mkdir(parents=True, exist_ok=True)
