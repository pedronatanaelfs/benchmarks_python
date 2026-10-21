"""Runtime experimental settings. YAML mirrors live under this folder."""

from __future__ import annotations

from copy import deepcopy

PAPER = {
    "title": "Fairness-Aware Performance Evaluation for Multi-Party Multi-Objective Optimization",
    "authors": "Zhao, Xu & Luo",
    "year": 2026,
    "arxiv": "https://arxiv.org/abs/2601.22497",
    "version": "arXiv:2601.22497 (accepted IEEE TEVC)",
}

RUNS = 30
SEEDS = list(range(1, RUNS + 1))
PF_SAMPLE_SIZE = 2000
OFFSET_PF_SAMPLE = 5000

MPMOP = {
    "problems": [f"MPMOP{i}" for i in range(1, 18)],
    "algorithms": ["OptAll", "OptMPNDS"],
    "n_var": 2,  # ZM26 Table II caption
    "population_size": 100,
    "evaluation_budget": 10000,
    "pro_c": 1.0,
    "dis_c": 20.0,
    "pro_m": 1.0,
    "dis_m": 20.0,
    "mutation_as_expectation": True,
}

MPDMP = {
    "problems": [f"MPDMP{i}" for i in range(1, 19)],
    "algorithms": ["OptAll", "OptMPNDS", "OptMPNDS2", "OptMPNDS3"],
    "n_var": 2,
    "population_size": 200,
    "evaluation_budget": 80000,
    "pro_c": 1.0,
    "dis_c": 15.0,
    "pro_m": 0.5,
    "dis_m": 20.0,
    "mutation_as_expectation": False,
    "optmpnds3_fei": 10000,
    "optmpnds3_p": 0.05,
    "optmpnds3_c": 0.05,
}

# Table S-IV
CONCESSION_CASES = {
    "case1_no_concession": {"2": [0.0, 0.0], "3": [0.0, 0.0, 0.0]},
    "case2_partial": {"2": [0.3, 0.0], "3": [0.3, 0.0, 0.0]},
    "case3_equal_partial": {"2": [0.3, 0.3], "3": [0.3, 0.3, 0.3]},
    "case4_asymmetric": {"2": [0.3, 0.7], "3": [0.3, 0.1, 0.6]},
    "case5_equal_moderate": {"2": [0.5, 0.5], "3": [0.5, 0.5, 0.5]},
    "case6_equal_high": {"2": [0.7, 0.7], "3": [0.7, 0.7, 0.7]},
}

ORIGINAL_BENCHMARKS = [f"MPMOP{i}" for i in range(1, 12)] + [
    f"MPDMP{i}" for i in range(1, 13)
]
NONCONSENSUS_BENCHMARKS = [f"MPMOP{i}" for i in range(12, 18)] + [
    f"MPDMP{i}" for i in range(13, 19)
]

FIGURE_PROBLEMS = ["MPMOP12", "MPMOP13", "MPDMP6", "MPDMP8", "MPDMP13", "MPDMP15"]
JAIN_GINI_PROBLEMS = ["MPMOP12", "MPMOP13"]


def concession_vector(problem_name: str, n_dm: int, case: str) -> list[float]:
    key = "3" if n_dm >= 3 else "2"
    vec = CONCESSION_CASES[case][key]
    if n_dm > len(vec):
        extra = [vec[-1]] * (n_dm - len(vec))
        return list(vec) + extra
    return list(vec[:n_dm])


def cases_for(problem_name: str) -> list[str]:
    if problem_name in NONCONSENSUS_BENCHMARKS:
        return list(CONCESSION_CASES)
    return ["case1_no_concession"]


def algorithm_kwargs(family: str, name: str) -> dict:
    cfg = deepcopy(MPMOP if family == "MPMOP" else MPDMP)
    kw = {
        "population_size": cfg["population_size"],
        "evaluation_budget": cfg["evaluation_budget"],
    }
    if name != "OptMPNDS3":
        kw.update(
            {
                "pro_c": cfg["pro_c"],
                "dis_c": cfg["dis_c"],
                "pro_m": cfg["pro_m"],
                "dis_m": cfg["dis_m"],
                "mutation_as_expectation": cfg["mutation_as_expectation"],
            }
        )
    else:
        kw.update({"fei": cfg["optmpnds3_fei"], "p": cfg["optmpnds3_p"], "c": cfg["optmpnds3_c"]})
    return kw
