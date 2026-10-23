"""Create deterministic shared CSV inputs for MATLAB and Python diagnostics."""

from __future__ import annotations

import numpy as np

from .paths import SHARED, ensure_dirs


def _save(name: str, arr: np.ndarray) -> None:
    path = SHARED / name
    np.savetxt(path, np.atleast_2d(arr), delimiter=",", fmt="%.16g")


def main() -> None:
    ensure_dirs()
    rng = np.random.default_rng(20261021)

    # --- Test 1: MPDMP4 decision vectors ---
    X = np.array(
        [
            [0.0, 0.0],
            [100.0, 100.0],
            [50.0, 50.0],
            [50.0, 40.0],  # common PS
            [50.0, 70.0],  # DM1 vertex
            [30.0, 40.0],  # DM1 vertex
            [70.0, 40.0],  # DM1 vertex
            [50.0, 10.0],  # DM2 vertex
            [30.0, 10.0],
            [70.0, 10.0],
            [40.0, 50.0],  # inside/near DM1
            [60.0, 25.0],  # inside/near DM2
            [10.0, 90.0],
            [90.0, 5.0],
            [0.0, 100.0],
            [100.0, 0.0],
            [33.3, 55.5],
            [71.2, 18.4],
            [12.5, 12.5],
            [87.5, 62.5],
        ],
        dtype=float,
    )
    _save("mpdmp4_X.csv", X)

    # --- Test 2: synthetic 6-objective matrix (MPDMP4 DM1=1:3, DM2=4:6) ---
    F = np.array(
        [
            [0.0, 0.0, 0.0, 5.0, 5.0, 5.0],  # good DM1, bad DM2
            [5.0, 5.0, 5.0, 0.0, 0.0, 0.0],  # bad DM1, good DM2
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # dominates both (ideal)
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # dominated by ideal
            [2.0, 0.0, 2.0, 2.0, 0.0, 2.0],
            [0.0, 2.0, 2.0, 0.0, 2.0, 2.0],
            [3.0, 3.0, 0.0, 3.0, 3.0, 0.0],
            [0.1, 0.2, 0.3, 4.0, 4.0, 4.0],
            [4.0, 4.0, 4.0, 0.1, 0.2, 0.3],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # duplicate of row 4
            [0.0, 0.0, 0.0, 5.0, 5.0, 5.0],  # duplicate of row 1
            [10.0, 10.0, 10.0, 10.0, 10.0, 10.0],  # worst
            [0.0, 1.0, 2.0, 2.0, 1.0, 0.0],
            [2.0, 1.0, 0.0, 0.0, 1.0, 2.0],
            [0.5, 0.5, 5.0, 0.5, 0.5, 5.0],
            [5.0, 0.5, 0.5, 5.0, 0.5, 0.5],
            [0.0, 0.0, 1.0, 8.0, 8.0, 8.0],
            [8.0, 8.0, 8.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    _save("mpnds_F.csv", F)

    # --- Test 3: crowding matrix (one front + duplicates + zero-span) ---
    Fc = np.array(
        [
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
            [5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [2.0, 2.0, 0.0, 2.0, 2.0, 0.0],
            [0.0, 3.0, 3.0, 0.0, 3.0, 3.0],
            [4.0, 0.0, 4.0, 4.0, 0.0, 4.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # duplicate
            [2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],  # duplicate of first
            [3.0, 3.0, 3.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    _save("crowding_F.csv", Fc)
    front = np.ones(Fc.shape[0])
    _save("crowding_front.csv", front)

    # --- Test 4: 200 candidates for environmental selection ---
    Xc = rng.uniform(0.0, 100.0, size=(200, 2))
    _save("envsel_X.csv", Xc)

    # --- Test 5 / unique: duplicates ---
    Xu = np.vstack(
        [
            [10.0, 10.0],
            [20.0, 20.0],
            [10.0, 10.0],
            [30.0, 40.0],
            [20.0, 20.0],
            [20.0, 20.0],
            [50.0, 40.0],
        ]
    )
    _save("unique_X.csv", Xu)

    # --- Test 6: parents for variation (20 parents -> 20 offspring via 10 pairs) ---
    parents = rng.uniform(0.0, 100.0, size=(20, 2))
    # also extreme parents that will go out of bounds before repair
    parents[0] = [0.0, 0.0]
    parents[1] = [100.0, 100.0]
    parents[2] = [0.0, 100.0]
    parents[3] = [100.0, 0.0]
    _save("variation_parents.csv", parents)

    n, d = 10, 2
    _save("ga_mu_sbx.csv", rng.random((n, d)))
    _save("ga_sign_sbx.csv", rng.integers(0, 2, size=(n, d)))
    _save("ga_beta_skip.csv", rng.random((n, d)))
    _save("ga_proc.csv", rng.random((n, 1)))
    _save("ga_site.csv", rng.random((2 * n, d)))
    _save("ga_mu_mut.csv", rng.random((2 * n, d)))

    # --- Test 7 short run: N=20 initial X and per-generation random streams ---
    n_short = 20
    n_gen = 5
    _save("short_X0.csv", rng.uniform(0.0, 100.0, size=(n_short, 2)))
    # tournament: K=2, N=20 parents each gen -> 2*20 integers in 0..N-1
    for g in range(n_gen):
        _save(f"short_tour_g{g}.csv", rng.integers(0, n_short, size=(2, n_short)))
        _save(f"short_ga_mu_sbx_g{g}.csv", rng.random((n_short // 2, 2)))
        _save(f"short_ga_sign_g{g}.csv", rng.integers(0, 2, size=(n_short // 2, 2)))
        _save(f"short_ga_beta_skip_g{g}.csv", rng.random((n_short // 2, 2)))
        _save(f"short_ga_proc_g{g}.csv", rng.random((n_short // 2, 1)))
        _save(f"short_ga_site_g{g}.csv", rng.random((n_short, 2)))
        _save(f"short_ga_mu_mut_g{g}.csv", rng.random((n_short, 2)))

    # --- one-by-one last front: 12 points, keep 5 ---
    Flast = rng.uniform(0.0, 5.0, size=(12, 6))
    Flast[0] = 0.0
    Flast[-1] = 5.0
    _save("lastfront_F.csv", Flast)

    # --- OptMPNDS3 JADE2 one-step (documented, not compared until OptMPNDS is done) ---
    _save("jade_X.csv", rng.uniform(0.0, 100.0, size=(8, 2)))
    _save("jade_cr.csv", np.clip(rng.normal(0.5, 0.1, size=(8, 1)), 0, 1))
    _save("jade_F.csv", np.clip(np.abs(rng.standard_cauchy(size=(8, 1)) * 0.1 + 0.5), 0, 1))
    _save("jade_pbest_idx.csv", rng.integers(0, 8, size=(8, 1)))
    _save("jade_i1.csv", rng.integers(0, 8, size=(8, 1)))
    _save("jade_i2.csv", rng.integers(0, 8, size=(8, 1)))
    _save("jade_jrand.csv", rng.integers(0, 2, size=(8, 1)))
    _save("jade_mask.csv", rng.random((8, 2)))

    meta = SHARED / "README.txt"
    meta.write_text(
        "Deterministic shared inputs for MPDMP4 / OptMPNDS diagnostics.\n"
        "Do not edit. Regenerated by python/generate_shared_inputs.py.\n"
        "MPDMP4 DM ownership (MATLAB 1-based): DM1=1:3, DM2=4:6.\n"
        "Bounds: [0,100]^2. Common PS: (50,40).\n"
    )
    print(f"wrote shared inputs in {SHARED}")


if __name__ == "__main__":
    main()
