"""
REPASS-1 / C9 — Test the paper's prediction of a secondary jump at L*/m.

Paper quote (page 4): "Interestingly, another jump occurs at L̄ ≈ L*/2 ...
we may expect a jump occurring at the mean length given at L*/m for any
positive integer m, if fragment X_{L*/m} can recruit repair protein."

For L* = 45 bp, L*/2 = 22.5 bp.  Fragments of length 22 bp are >= Lm=15
so they DO recruit Ku, so the prediction applies.

We sweep mean length L̄ ∈ {15, 16, ..., 50} with M_T = 25, 80 runs each,
and look for a discontinuity near 22-23 bp.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from gillespie_rejoining import (
    SimParams,
    simulate,
)

OUT_RESULTS = ROOT / "results" / "repass1"
OUT_LOGS = ROOT / "logs" / "repass1"
OUT_FIGS = ROOT / "figures" / "repass1"
for d in (OUT_RESULTS, OUT_LOGS, OUT_FIGS):
    d.mkdir(parents=True, exist_ok=True)


def main():
    rng_master = np.random.default_rng(424242)
    lengths_grid = list(range(15, 51))  # 15..50 bp
    n_runs = 80
    M_T = 25

    means = []
    stds = []
    medians = []

    t0 = time.time()
    for L_bar in lengths_grid:
        ts = np.zeros(n_runs)
        for k in range(n_runs):
            seed = int(rng_master.integers(0, 2**31 - 1))
            P = SimParams(
                k1=1.0, k2=0.5, k3=0.1, E=1.0, V=1.0,
                rng_seed=seed,
            )
            init = [L_bar] * M_T  # all same length, as paper does
            t_end, _ = simulate(init, P)
            ts[k] = t_end
        means.append(float(ts.mean()))
        stds.append(float(ts.std()))
        medians.append(float(np.median(ts)))
        print(f"  L̄={L_bar:3d}  mean={ts.mean():8.2f}  std={ts.std():7.2f}  med={np.median(ts):7.2f}")

    elapsed = time.time() - t0

    arr = {
        "lengths": np.array(lengths_grid),
        "mean_t": np.array(means),
        "std_t": np.array(stds),
        "median_t": np.array(medians),
    }
    np.savez(OUT_RESULTS / "c9_secondary_jump.npz", **arr)

    # Search for sub-threshold discontinuity:
    # Compute first-difference of mean within [Lm+2, L*-1].
    L = np.array(lengths_grid)
    M = np.array(means)
    dM = np.diff(M)
    # Region of interest: below L* (skip exact threshold).
    below_idx = np.where(L[1:] < 45)[0]
    # Find max-|jump| in that region.
    rel_idx = below_idx[np.argmax(np.abs(dM[below_idx]))]
    jump_at_L = int(L[rel_idx + 1])
    jump_dM = float(dM[rel_idx])
    typical_dM = float(np.median(np.abs(dM[below_idx])))

    # Specifically look at L*/2 = 22.5 -> compare L=22 vs L=23.
    try:
        idx22 = lengths_grid.index(22)
        idx23 = lengths_grid.index(23)
        jump_at_22_to_23 = float(means[idx23] - means[idx22])
    except ValueError:
        jump_at_22_to_23 = None

    # Try plot (matplotlib optional)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.errorbar(L, M, yerr=np.array(stds), fmt="o-", capsize=3, lw=1)
        ax.axvline(45, color="red", lw=1, alpha=0.7, label="L* = 45")
        ax.axvline(22.5, color="orange", lw=1, alpha=0.7, ls="--",
                   label="predicted secondary jump at L*/2 = 22.5")
        ax.set_xlabel("Initial mean length L̄ (bp)")
        ax.set_ylabel(f"Mean rejoining time (M_T={M_T}, {n_runs} runs)")
        ax.set_title("C9: looking for a secondary jump at L*/2")
        ax.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGS / "c9_secondary_jump.png", dpi=120)
        plt.close(fig)
    except Exception as e:
        print(f"  (matplotlib skipped: {e})")

    summary = {
        "claim": "C9: secondary jump at L*/m, specifically L*/2 = 22.5 bp",
        "M_T": M_T,
        "n_runs_per_length": n_runs,
        "lengths_grid": lengths_grid,
        "primary_threshold_jump_45_vs_44": float(means[lengths_grid.index(45)] - means[lengths_grid.index(44)]),
        "step_22_to_23_mean_delta": jump_at_22_to_23,
        "max_abs_subthreshold_step": {"at_L": jump_at_L, "delta_mean": jump_dM},
        "median_abs_subthreshold_step": typical_dM,
        "verdict": (
            "STRONG" if jump_at_22_to_23 is not None
            and abs(jump_at_22_to_23) > 3 * typical_dM else
            "WEAK / not visible"
        ),
        "elapsed_s": elapsed,
    }
    (OUT_LOGS / "c9_secondary_jump.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
