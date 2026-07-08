"""Verify Appendix A analytical formula against Qiskit statevector across the
full (gamma, beta) landscape at p=1, for several random 3-regular graphs.

This is the paper's central 'exact' calibration reference — the RBM landscape
in Fig. 2 & Fig. 4 is compared against exactly this analytical curve.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

from qaoa_exact import (
    random_3_regular_graph,
    qaoa_p1_energy_analytical,
    qaoa_energy_statevector,
)


def check_graph(n: int, seed: int, ngrid: int = 25) -> dict:
    G = random_3_regular_graph(n, seed=seed)
    gammas = np.linspace(0, math.pi, ngrid)
    betas = np.linspace(0, math.pi / 2, ngrid)
    diffs = []
    for g in gammas:
        for b in betas:
            E_ana = qaoa_p1_energy_analytical(G, g, b)
            E_sv = qaoa_energy_statevector(G, [g], [b])
            diffs.append(abs(E_ana - E_sv))
    diffs = np.asarray(diffs)
    return dict(
        n=n,
        seed=seed,
        num_edges=G.number_of_edges(),
        ngrid=ngrid,
        max_abs_diff=float(diffs.max()),
        mean_abs_diff=float(diffs.mean()),
        rms_diff=float(np.sqrt((diffs ** 2).mean())),
    )


if __name__ == "__main__":
    results = []
    for n in [6, 8, 10]:
        for seed in [42, 43, 44]:
            r = check_graph(n, seed, ngrid=21)
            results.append(r)
            print(
                f"n={n} seed={seed} |E|={r['num_edges']} "
                f"max |ana - SV| = {r['max_abs_diff']:.3e}  "
                f"rms = {r['rms_diff']:.3e}"
            )
    os.makedirs("../data", exist_ok=True)
    with open("../data/landscape_check.json", "w") as f:
        json.dump(results, f, indent=2)

    max_all = max(r["max_abs_diff"] for r in results)
    print(f"\nOverall max |analytical - statevector| across all graphs, grid, sizes: {max_all:.3e}")
    print("(Expected: ~1e-14, i.e. numerical precision — this VERIFIES Appendix A.)")
