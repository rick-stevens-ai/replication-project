"""
REPASS-1 / C13 — k3 (release-rate) dose-response.

Paper Fig 3(b), text page 4: "Fig. 3(b) shows that the rejoining time is
increased markedly as release rate is reduced by half when L̄ ≤ L*" and
"if all the DNA fragments have length larger than L*, then the release
step is not necessary and hence varying k3 has no effect on the rejoining
in this case, as shown in Fig. 3(b) for L̄ > L*."

Pass-1 dispatched this as "structural / guaranteed by construction".  We
now test it numerically with k3 ∈ {0.025, 0.05, 0.1, 0.2, 0.4} at two
length regimes: L̄ = 30 bp (short, in I2) and L̄ = 80 bp (long, in I3).
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


def sweep(L_bar, n_runs, k3_grid, M_T, rng_master):
    means, stds = [], []
    for k3 in k3_grid:
        ts = np.zeros(n_runs)
        for k in range(n_runs):
            seed = int(rng_master.integers(0, 2**31 - 1))
            P = SimParams(k1=1.0, k2=0.5, k3=k3, E=1.0, V=1.0, rng_seed=seed)
            t_end, _ = simulate([L_bar] * M_T, P)
            ts[k] = t_end
        means.append(float(ts.mean()))
        stds.append(float(ts.std()))
        print(f"   L̄={L_bar}  k3={k3:6.3f}  mean={ts.mean():7.2f}  std={ts.std():6.2f}")
    return means, stds


def main():
    rng_master = np.random.default_rng(99001)
    M_T = 25
    n_runs = 80
    k3_grid = [0.025, 0.05, 0.1, 0.2, 0.4]

    t0 = time.time()
    print("\n=== C13a SHORT-only regime, L̄ = 30 bp ===")
    short_means, short_stds = sweep(30, n_runs, k3_grid, M_T, rng_master)
    print("\n=== C13b LONG-only regime, L̄ = 80 bp ===")
    long_means, long_stds = sweep(80, n_runs, k3_grid, M_T, rng_master)
    elapsed = time.time() - t0

    # Short regime: rejoining time should INCREASE as k3 decreases.
    # Order: rev sort by k3 (smallest first) -> means should decrease as k3 grows.
    k3_arr = np.array(k3_grid, dtype=float)
    sm = np.array(short_means)
    lm = np.array(long_means)
    # spearman-style monotonicity check
    diffs_short = np.diff(sm)  # should be NEGATIVE (smaller k3 = larger time)
    diffs_long = np.diff(lm)  # should be ~0
    short_mono_decreasing = float((diffs_short < 0).mean())
    long_flat_frac = float((np.abs(diffs_long) < 0.05 * np.mean(lm)).mean())

    # Ratio of mean(k3=0.05) / mean(k3=0.1) — "halving k3" effect.
    halve_ratio_short = float(sm[k3_grid.index(0.05)] / sm[k3_grid.index(0.1)])
    halve_ratio_long = float(lm[k3_grid.index(0.05)] / lm[k3_grid.index(0.1)])

    summary = {
        "claim": ("C13: rejoining time strongly increases as k3 decreases "
                  "for L̄ ≤ L*, but is ~independent of k3 for L̄ > L*"),
        "M_T": M_T,
        "n_runs_per_k3": n_runs,
        "k3_grid": k3_grid,
        "L_bar_short_30bp": {
            "means": short_means,
            "stds": short_stds,
            "monotone_decreasing_frac": short_mono_decreasing,
            "ratio_halve_k3_0p05_over_0p1": halve_ratio_short,
        },
        "L_bar_long_80bp": {
            "means": long_means,
            "stds": long_stds,
            "flat_within_5pct_frac": long_flat_frac,
            "ratio_halve_k3_0p05_over_0p1": halve_ratio_long,
        },
        "elapsed_s": elapsed,
        "verdict": (
            "STRONG" if halve_ratio_short > 1.5 and abs(halve_ratio_long - 1.0) < 0.05
            else "PARTIAL"
        ),
    }
    (OUT_LOGS / "c13_k3_sweep.json").write_text(json.dumps(summary, indent=2))
    np.savez(OUT_RESULTS / "c13_k3_sweep.npz",
             k3_grid=k3_arr, short_means=sm, long_means=lm,
             short_stds=np.array(short_stds), long_stds=np.array(long_stds))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.errorbar(k3_arr, sm, yerr=short_stds, fmt="o-", label="L̄ = 30 bp (short, in I2)")
        ax.errorbar(k3_arr, lm, yerr=long_stds, fmt="s-", label="L̄ = 80 bp (long, in I3)")
        ax.set_xscale("log")
        ax.set_xlabel("k3 (release rate)")
        ax.set_ylabel("Mean rejoining time")
        ax.set_title("C13: k3 sweep — release rate matters only when L̄ ≤ L*")
        ax.legend()
        plt.tight_layout()
        plt.savefig(OUT_FIGS / "c13_k3_sweep.png", dpi=120)
        plt.close(fig)
    except Exception as e:
        print(f"  (plot skipped: {e})")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
