"""
Reproduce Fig 4 trend: mean kinetics of remaining DNA fragments fraction vs time,
comparing low-LET (gamma, 3% short) and high-LET (Fe ion, 30% short).

Output:
  - results/fig4_kinetics.npz  (time grid + curves)
  - figures/fig4_kinetics.png
  - logs/fig4_kinetics.log
"""

from __future__ import annotations
import os, sys, time, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gillespie_rejoining import (
    SimParams, run_ensemble,
    initial_high_LET_Fe_1Gy, initial_low_LET_gamma_1Gy,
    mean_remaining_fraction_curve,
)


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.makedirs(os.path.join(root, "results"), exist_ok=True)
    os.makedirs(os.path.join(root, "figures"), exist_ok=True)
    os.makedirs(os.path.join(root, "logs"), exist_ok=True)
    log = open(os.path.join(root, "logs", "fig4_kinetics.log"), "w")

    def L(*a):
        msg = " ".join(str(x) for x in a)
        print(msg); log.write(msg + "\n"); log.flush()

    # Parameters (paper does not give numeric rates; choose unit-consistent values
    # that produce the same biphasic shape. Volume = 1; rates set to give
    # rejoining on time scales of ~1-100 in arbitrary units. Convert to "min"
    # by matching characteristic time for low-LET curve.
    # k1 (recruitment), k2 (joining), k3 (residue release).
    P_base = dict(
        Lm=15, Lstar=45,
        k1=0.05,   # Ku-end binding rate
        k2=0.25,   # fragment joining rate per pair / V
        k3=0.02,   # residue release rate (slow -> drives biphasic)
        E=10.0,    # Ku pool (treated abundant)
        V=1.0,
        t_max=5e5,
    )

    n_runs = 200
    n_dsb = 30  # 1 Gy => ~25-35 DSBs

    L(f"=== Fig 4 replication: {n_runs} stochastic runs per condition ===")
    L(f"Params: {P_base}")
    L(f"n_dsb per 1 Gy: {n_dsb}")

    t0 = time.time()

    # Low-LET gamma: 3% short
    L("Running low-LET gamma (3% short)...")
    P_low = SimParams(**{**P_base, "rng_seed": 12345})
    times_low, traj_low = run_ensemble(
        lambda rng: initial_low_LET_gamma_1Gy(rng, n_dsb=n_dsb, frac_short=0.03),
        P_low, n_runs=n_runs,
    )
    L(f"  Mean rejoining time (low-LET): {times_low.mean():.2f}  std: {times_low.std():.2f}")
    L(f"  Median: {np.median(times_low):.2f}  min/max: {times_low.min():.2f}/{times_low.max():.2f}")

    # High-LET Fe: 30% short
    L("Running high-LET Fe (30% short)...")
    P_high = SimParams(**{**P_base, "rng_seed": 67890})
    times_high, traj_high = run_ensemble(
        lambda rng: initial_high_LET_Fe_1Gy(rng, n_dsb=n_dsb, frac_short=0.30),
        P_high, n_runs=n_runs,
    )
    L(f"  Mean rejoining time (high-LET): {times_high.mean():.2f}  std: {times_high.std():.2f}")
    L(f"  Median: {np.median(times_high):.2f}  min/max: {times_high.min():.2f}/{times_high.max():.2f}")

    elapsed = time.time() - t0
    L(f"Total simulation wallclock: {elapsed:.1f} s")

    # Build time grid
    t_max_plot = float(min(P_base["t_max"], 1.2 * max(times_high.max(), times_low.max())))
    t_grid = np.linspace(0, t_max_plot, 400)

    curve_low = mean_remaining_fraction_curve(traj_low, t_grid)
    curve_high = mean_remaining_fraction_curve(traj_high, t_grid)

    # Save results
    out = os.path.join(root, "results", "fig4_kinetics.npz")
    np.savez(out,
             t_grid=t_grid,
             curve_low_LET=curve_low,
             curve_high_LET=curve_high,
             times_low=times_low,
             times_high=times_high,
             params=json.dumps(P_base))
    L(f"Saved: {out}")

    # Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(t_grid, 100 * curve_low, "g-.", lw=2,
            label="Low LET (γ-ray, 3% short) — model")
    ax.plot(t_grid, 100 * curve_high, "r-", lw=2,
            label="High LET (Fe ion, 30% short) — model")
    ax.set_xlabel("Time (arbitrary units)")
    ax.set_ylabel("Remaining fragments  (M(t)−1)/(M(0)−1)   [%]")
    ax.set_title("Replicated Fig 4: Mean kinetics of DNA fragment rejoining\n"
                 "(Li et al. 2012, PLoS ONE; independent open replication)")
    ax.set_ylim(-2, 102)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")
    fig.tight_layout()
    figpath = os.path.join(root, "figures", "fig4_kinetics.png")
    fig.savefig(figpath, dpi=130)
    L(f"Saved: {figpath}")

    # Log-time plot for biphasic visibility
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    pos = t_grid > 0
    ax2.semilogx(t_grid[pos], 100 * curve_low[pos], "g-.", lw=2,
                 label="Low LET (γ-ray, 3% short)")
    ax2.semilogx(t_grid[pos], 100 * curve_high[pos], "r-", lw=2,
                 label="High LET (Fe ion, 30% short)")
    ax2.set_xlabel("Time (arbitrary units, log scale)")
    ax2.set_ylabel("Remaining fragments [%]")
    ax2.set_title("Fig 4 (log time) — biphasic kinetics")
    ax2.set_ylim(-2, 102)
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend()
    fig2.tight_layout()
    figpath2 = os.path.join(root, "figures", "fig4_kinetics_logtime.png")
    fig2.savefig(figpath2, dpi=130)
    L(f"Saved: {figpath2}")

    log.close()


if __name__ == "__main__":
    main()
