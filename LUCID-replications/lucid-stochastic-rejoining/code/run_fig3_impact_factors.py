"""
Reproduce key trends from Fig 3 of Li et al. 2012:

  (a) Mean rejoining time vs nuclear volume V (larger V => longer time, since
      second-order reactions are diluted).
  (b) Mean rejoining time vs initial number of fragments (more fragments =>
      longer time).
  (c) Mean rejoining time vs mean fragment length (jump at L* = 45 bp: shorter
      mean length needs release step => much longer time).

Output:
  - results/fig3_impact.npz
  - figures/fig3_volume.png, fig3_count.png, fig3_meanlen.png
  - logs/fig3_impact.log
"""

from __future__ import annotations
import os, sys, time, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gillespie_rejoining import (
    SimParams, run_ensemble, initial_uniform_same_length,
)


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.makedirs(os.path.join(root, "results"), exist_ok=True)
    os.makedirs(os.path.join(root, "figures"), exist_ok=True)
    os.makedirs(os.path.join(root, "logs"), exist_ok=True)
    log = open(os.path.join(root, "logs", "fig3_impact.log"), "w")

    def L(*a):
        msg = " ".join(str(x) for x in a)
        print(msg); log.write(msg + "\n"); log.flush()

    P_base = dict(
        Lm=15, Lstar=45,
        k1=0.05, k2=0.25, k3=0.02,
        E=10.0, V=1.0, t_max=5e5,
    )

    n_runs = 60   # smaller ensemble for parameter sweeps
    L(f"=== Fig 3 trends: {n_runs} runs per point ===")
    L(f"Base params: {P_base}")

    t0 = time.time()

    # ---- (a) Volume sweep, fixed initial: uniform length 30 bp (< L*), 30 frags
    L("\n(a) Volume sweep")
    volumes = [0.25, 0.5, 1.0, 2.0, 4.0]
    n_frags_a = 30
    n_len_a = 30  # < L* -> includes release step
    mean_times_vol = []
    std_times_vol = []
    for V in volumes:
        P = SimParams(**{**P_base, "V": float(V), "rng_seed": 11})
        times, _ = run_ensemble(
            lambda rng: initial_uniform_same_length(n_len_a, n_frags_a),
            P, n_runs=n_runs,
        )
        mt, st = float(times.mean()), float(times.std())
        mean_times_vol.append(mt); std_times_vol.append(st)
        L(f"  V={V:>5.2f}  mean rejoin time = {mt:8.2f}  std={st:6.2f}")

    # ---- (b) Initial fragment count sweep, V=1, length 30 bp
    L("\n(b) Fragment count sweep")
    counts = [10, 20, 30, 40, 50]
    n_len_b = 30
    mean_times_count = []
    std_times_count = []
    for c in counts:
        P = SimParams(**{**P_base, "rng_seed": 22})
        times, _ = run_ensemble(
            lambda rng: initial_uniform_same_length(n_len_b, c),
            P, n_runs=n_runs,
        )
        mt, st = float(times.mean()), float(times.std())
        mean_times_count.append(mt); std_times_count.append(st)
        L(f"  count={c:>3}  mean rejoin time = {mt:8.2f}  std={st:6.2f}")

    # ---- (c) Mean length sweep — show jump at L* = 45 bp
    L("\n(c) Mean length sweep")
    lengths = [20, 25, 30, 35, 40, 44, 46, 50, 60, 80, 100]
    n_frags_c = 25
    mean_times_len = []
    std_times_len = []
    for n_len in lengths:
        P = SimParams(**{**P_base, "rng_seed": 33})
        times, _ = run_ensemble(
            lambda rng: initial_uniform_same_length(n_len, n_frags_c),
            P, n_runs=n_runs,
        )
        mt, st = float(times.mean()), float(times.std())
        mean_times_len.append(mt); std_times_len.append(st)
        L(f"  mean_len={n_len:>3}  mean rejoin time = {mt:8.2f}  std={st:6.2f}")

    elapsed = time.time() - t0
    L(f"\nTotal wallclock: {elapsed:.1f} s")

    np.savez(os.path.join(root, "results", "fig3_impact.npz"),
             volumes=volumes, mean_times_vol=mean_times_vol, std_times_vol=std_times_vol,
             counts=counts, mean_times_count=mean_times_count, std_times_count=std_times_count,
             lengths=lengths, mean_times_len=mean_times_len, std_times_len=std_times_len,
             params=json.dumps(P_base))

    # Plots
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.errorbar(volumes, mean_times_vol, yerr=std_times_vol, fmt="o-", capsize=4, color="C0")
    ax.set_xlabel("Nuclear volume V (arb. units)")
    ax.set_ylabel("Mean rejoining time (arb. units)")
    ax.set_title("Fig 3(a): rejoining time vs nuclear volume\n(uniform L=30 bp, 30 fragments)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(root, "figures", "fig3_volume.png"), dpi=130)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.errorbar(counts, mean_times_count, yerr=std_times_count, fmt="s-", capsize=4, color="C2")
    ax.set_xlabel("Initial number of fragments M_T")
    ax.set_ylabel("Mean rejoining time (arb. units)")
    ax.set_title("Fig 3(c): rejoining time vs fragment count\n(uniform L=30 bp, V=1)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(root, "figures", "fig3_count.png"), dpi=130)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.errorbar(lengths, mean_times_len, yerr=std_times_len, fmt="d-", capsize=4, color="C3")
    ax.axvline(45, color="k", ls="--", alpha=0.6, label="L* = 45 bp")
    ax.set_xlabel("Mean fragment length (bp)")
    ax.set_ylabel("Mean rejoining time (arb. units)")
    ax.set_title("Fig 3(b/2b): rejoining time vs mean length\n(uniform length, 25 fragments)")
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(root, "figures", "fig3_meanlen.png"), dpi=130)

    L("Saved figures.")
    log.close()


if __name__ == "__main__":
    main()
