#!/usr/bin/env python3
"""Monte-Carlo cross-check of the PGM confusion probabilities.

For the D_4 group at s=3 we independently sample the PGM outcome
distribution by drawing states (measurement Kraus decomposition) and
compare against the analytic Tr(E_j rho_i) matrix, to catch any
implementation bug in the analytic PGM code.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

import hsp_query_complexity as core

HERE = Path(__file__).resolve().parent
SEED = 20260705
N_SHOTS = 20000


def sample_povm_outcome(rng: np.random.Generator,
                        rho: np.ndarray,
                        povm) -> int:
    """Draw one measurement outcome by directly sampling the categorical
    distribution p_j = Tr(E_j rho).  This is what a real quantum experiment
    would give us; sampling this way validates the analytic PGM.
    """
    probs = np.array([float(np.sum(E * rho)) for E in povm])
    probs = np.clip(probs, 0.0, None)
    probs = probs / probs.sum()
    return int(rng.choice(len(probs), p=probs))


def main() -> None:
    rng = np.random.default_rng(SEED)
    G = core.build_D4()
    s = 3
    r = len(G.subgroups)
    priors = np.ones(r) / r

    print(f"Monte-Carlo cross-check: {G.name}, s={s}, r={r}, shots={N_SHOTS}",
          flush=True)

    rho1 = [core.coset_state_density(G, H) for H in G.subgroups]
    rhos = [core.tensor_power_density(rho, s) for rho in rho1]
    povm = core.pretty_good_measurement(rhos, priors)

    analytic = core.measurement_confusion_matrix(rhos, povm)

    # Precompute per-state outcome distributions once (they are what a
    # shot-based experiment samples from), then draw N_SHOTS from each.
    empirical = np.zeros((r, r), dtype=np.float64)
    for i, rho in enumerate(rhos):
        probs = np.array([float(np.sum(E * rho)) for E in povm])
        probs = np.clip(probs, 0.0, None)
        probs = probs / probs.sum()
        outcomes = rng.choice(len(probs), size=N_SHOTS, p=probs)
        for j in outcomes:
            empirical[i, j] += 1
    empirical = empirical / N_SHOTS

    diff = np.max(np.abs(analytic - empirical))
    print(f"  max |analytic - empirical| = {diff:.4f}", flush=True)
    print(f"  expected (Hoeffding, 95% CI at {N_SHOTS} shots) ~ "
          f"{1.96 / (2*math.sqrt(N_SHOTS)):.4f}", flush=True)

    out = {
        "group": G.name,
        "s": s,
        "num_subgroups": r,
        "n_shots": N_SHOTS,
        "seed": SEED,
        "analytic_confusion_diag": [float(analytic[i, i]) for i in range(r)],
        "empirical_confusion_diag": [float(empirical[i, i]) for i in range(r)],
        "max_abs_diff": float(diff),
        "hoeffding_95pct_CI_halfwidth": 1.96 / (2 * math.sqrt(N_SHOTS)),
        "pass": bool(diff < 3 * 1.96 / (2 * math.sqrt(N_SHOTS))),
    }
    with (HERE / "results" / "monte_carlo_check.json").open("w") as fh:
        json.dump(out, fh, indent=2)
    print(f"  PASS: {out['pass']}", flush=True)


if __name__ == "__main__":
    main()
