from __future__ import annotations

from typing import Any

import numpy as np

from ..config.settings import (
    OFFSET_PF_SAMPLE,
    PF_SAMPLE_SIZE,
    cases_for,
    concession_vector,
)
from ..metrics.gini import gini_coefficient
from ..metrics.igd import party_igd
from ..metrics.jain import jain_index
from ..metrics.matlab_mpdmp_pf import matlab_problem_pf
from ..metrics.mean_igd import mean_igd
from ..metrics.nash_score import estimate_lambda, nash_components
from ..metrics.she_igd import zm26_meanIGD


def evaluate_conditions(
    F: np.ndarray,
    problem,
    slices,
    pf_per_dm,
    *,
    C: float,
    rng: np.random.Generator,
    lambdas: dict | None = None,
) -> list[dict[str, Any]]:
    n_dm = problem.n_dm
    rows = []
    igds = party_igd(F, pf_per_dm, slices)
    party_migd = float(np.nanmean(igds))
    zm26 = np.nan
    if str(getattr(problem, "name", "")).startswith("MPDMP"):
        try:
            zm26 = zm26_meanIGD(F, matlab_problem_pf(problem), slices)
        except Exception:
            zm26 = np.nan
    for case in cases_for(problem.name):
        eps = np.asarray(concession_vector(problem.name, n_dm, case), dtype=float)
        if lambdas is not None and case in lambdas:
            lam = lambdas[case]
        else:
            lam = estimate_lambda(pf_per_dm, slices, eps, rng)
        det = nash_components(
            F,
            pf_per_dm,
            slices,
            eps,
            lam,
            C=C,
            pf_sample_size=PF_SAMPLE_SIZE,
            offset_pf_sample=OFFSET_PF_SAMPLE,
            rng=rng,
        )
        row: dict[str, Any] = {
            "condition": case,
            "meanIGD": party_migd,  # alias of party_pf_meanIGD (backward compatible)
            "party_pf_meanIGD": party_migd,
            "zm26_meanIGD": zm26,
            "nash_score": det.nash_C,
            "nash_score_exp": det.nash_exp,
            "log_nash": det.log_nash_C,
            "C": det.C,
            "jain_index": jain_index(1.0 / np.clip(igds, 1e-12, None)),
            "gini_index": gini_coefficient(igds),
            "jain_utility": jain_index(np.clip(det.utility_C, 0, None)),
            "gini_utility": gini_coefficient(np.clip(det.utility_C, 0, None)),
        }
        for i in range(3):
            row[f"IGD_DM{i+1}"] = float(igds[i]) if i < n_dm else np.nan
            row[f"concession_DM{i+1}"] = (
                float(det.concession_mean[i]) if i < n_dm else np.nan
            )
            row[f"penalty_DM{i+1}"] = float(det.penalty_mean[i]) if i < n_dm else np.nan
            row[f"utility_DM{i+1}"] = float(det.utility_C[i]) if i < n_dm else np.nan
            row[f"lambda_DM{i+1}"] = float(det.lambda_[i]) if i < n_dm else np.nan
            row[f"mu_DM{i+1}"] = float(det.mu[i]) if i < n_dm else np.nan
        rows.append(row)
    return rows


def estimate_C(problem, pf_per_dm, slices, rng) -> float:
    """Appendix S-I style upper bound from a random population plus PF-to-PF IGD."""
    from ..algorithms.operators import random_population

    X = random_population(rng, 40, problem.xl, problem.xu)
    F = problem.evaluate(X)
    eps = np.zeros(problem.n_dm)
    lam = estimate_lambda(pf_per_dm, slices, eps, rng)
    det = nash_components(F, pf_per_dm, slices, eps, lam, C=1.0, rng=rng)
    return float(max(det.L) + 1.0)
