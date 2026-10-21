"""Write markdown tables used by REPRODUCTION_REPORT.md."""

from __future__ import annotations

import pandas as pd

from .. import ROOT

SUM = ROOT / "results" / "aggregated" / "summary.csv"
CMP = ROOT / "results" / "paper_comparison" / "paper_vs_python.csv"
OUT = ROOT / "results" / "paper_comparison" / "tables.md"


def main() -> None:
    summary = pd.read_csv(SUM)
    cmp = pd.read_csv(CMP)
    lines = ["# Reproduced tables", ""]
    sub = summary[summary.condition == "case1_no_concession"]
    lines.append("## meanIGD / Nash (case 1)")
    lines.append("")
    lines.append(sub[sub.metric.isin(["meanIGD", "nash_score", "log_nash"])].head(80).to_csv(index=False))
    lines.append("")
    lines.append("## Paper vs Python")
    lines.append("")
    lines.append(cmp.to_csv(index=False))
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
