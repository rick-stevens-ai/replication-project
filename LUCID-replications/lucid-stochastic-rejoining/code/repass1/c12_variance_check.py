"""
REPASS-1 / C12 — Variance discontinuity at L* (Fig 2(b)).

Paper Fig 2(b) caption / page 4 text: "the rejoining time varies over a
large range when the initial mean length is less than the critical length
(L̄ ≤ L*), compared to that as L̄ > L*."

Pass-1 reported only means.  Here we explicitly compute std and (max-min)
spread on a fine length grid and look for a discontinuity at L* = 45 bp.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from gillespie_rejoining import SimParams, simulate

OUT_RESULTS = ROOT / "results" / "repass1"
OUT_LOGS = ROOT / "logs" / "repass1"
OUT_FIGS = ROOT / "figures" / "repass1"
for d in (OUT_RESULTS, OUT_LOGS, OUT_FIGS):
    d.mkdir(parents=True, exist_ok=True)


def main():
    rng_master = np.random.default_rng(57239)
    M_T = 40  # paper Fig 2(b) uses M_T = 40
    n_runs = 150  # paper says 150 samples
    grid = [20, 25, 30, 35, 40, 44, 45, 46, 50, 60, 80, 100]

    means, stds, mins, maxs, spreads = {}, {}, {}, {}, {}
    t0 = time.time()
    for L_bar in grid:
        ts = np.zeros(n_runs)
        for k in range(n_runs):
            seed = int(rng_master.integers(0, 2**31 - 1))
            P = SimParams(k1=1.0, k2=0.5, k3=0.1, E=1.0, V=1.0, rng_seed=seed)
            t_end, _ = simulate([L_bar] * M_T, P)
            ts[k] = t_end
        means[L_bar] = float(ts.mean())
        stds[L_bar] = float(ts.std())
        mins[L_bar] = float(ts.min())
        maxs[L_bar] = float(ts.max())
        spreads[L_bar] = float(ts.max() - ts.min())
        print(f"  L̄={L_bar:3d}  mean={ts.mean():7.2f}  std={ts.std():6.2f}  "
              f"min={ts.min():6.2f}  max={ts.max():6.2f}  spread={ts.max()-ts.min():6.2f}")
    elapsed = time.time() - t0

    # Discontinuity check at L* = 45
    below = [L for L in grid if L <= 45]
    above = [L for L in grid if L > 45]
    std_below = np.mean([stds[L] for L in below])
    std_above = np.mean([stds[L] for L in above])
    spread_below = np.mean([spreads[L] for L in below])
    spread_above = np.mean([spreads[L] for L in above])
    ratio_std = float(std_below / max(std_above, 1e-6))
    ratio_spread = float(spread_below / max(spread_above, 1e-6))

    summary = {
        "claim": "C12: variance / spread of rejoining time is much larger for L̄ ≤ L* than for L̄ > L*",
        "M_T": M_T,
        "n_runs_per_length": n_runs,
        "lengths_grid": grid,
        "per_length_std": stds,
        "per_length_spread_max_minus_min": spreads,
        "mean_std_for_L_leq_Lstar": float(std_below),
        "mean_std_for_L_gt_Lstar": float(std_above),
        "mean_spread_for_L_leq_Lstar": float(spread_below),
        "mean_spread_for_L_gt_Lstar": float(spread_above),
        "std_ratio_below_over_above": ratio_std,
        "spread_ratio_below_over_above": ratio_spread,
        "verdict": (
            "STRONG" if ratio_std > 3 and ratio_spread > 3 else
            "PARTIAL" if ratio_std > 1.5 else
            "WEAK"
        ),
        "elapsed_s": elapsed,
    }
    (OUT_LOGS / "c12_variance.json").write_text(json.dumps(summary, indent=2))
    np.savez(OUT_RESULTS / "c12_variance.npz",
             grid=np.array(grid),
             means=np.array([means[L] for L in grid]),
             stds=np.array([stds[L] for L in grid]),
             mins=np.array([mins[L] for L in grid]),
             maxs=np.array([maxs[L] for L in grid]))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        L_arr = np.array(grid)
        m = np.array([means[L] for L in grid])
        lo = np.array([mins[L] for L in grid])
        hi = np.array([maxs[L] for L in grid])
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.errorbar(L_arr, m, yerr=[m - lo, hi - m], fmt="o", capsize=4,
                    color="C0", label="mean ± (max, min)")
        ax.set_yscale("log")
        ax.axvline(45, color="red", lw=1, ls="--", label="L* = 45")
        ax.set_xlabel("Initial mean length L̄ (bp)")
        ax.set_ylabel("Rejoining time (log)")
        ax.set_title("C12: error-bar discontinuity at L*  (Fig 2(b) replica)")
        ax.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGS / "c12_variance.png", dpi=120)
        plt.close(fig)
    except Exception as e:
        print(f"  (plot skipped: {e})")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
