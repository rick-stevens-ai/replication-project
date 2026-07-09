"""
REPASS-1 / C11 — 2D monotonicity of T_M(r1, r2).

Paper Fig 3(d), text page 4: "T_M(r1, r2) is increasing in both r1 and r2,
indicating that more short fragments lead to more time for complete rejoining".

  r1 = fraction of fragments with length in I2 = (L*/2, L*]    = (22.5, 45]
  r2 = fraction of fragments with length in I1 = (Lm, L*/2]    = (15, 22.5]
  1 - r1 - r2 = fraction in I3 = (L*, ∞) = (45, ∞)

We pick M_T = 40, L_T = 2000 bp (paper constraints), and walk a 6×6 grid
in (r1, r2) with r1 + r2 <= 1. For each cell we draw n_runs trajectories
with random per-run initial length draws that respect (r1, r2) bin sizes
and the target L_T (relaxed: we constrain mean length to L_T/M_T = 50 bp
in expectation by drawing uniformly within each bin and renormalizing).

We report T_M(r1, r2) and assess monotonicity along both axes.
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


Lm = 15
Lstar = 45
HALF = Lstar // 2  # = 22 (integer); I1 = (Lm, 22], I2 = (22, 45], I3 = (45, ?]


def build_init(rng, n1, n2, n3, target_total_len):
    """Draw lengths: n1 from I1=(15,22], n2 from I2=(22,45], n3 from I3=(45,200]."""
    lens = []
    if n1 > 0:
        lens.extend(rng.integers(Lm + 1, HALF + 1, size=n1).tolist())
    if n2 > 0:
        lens.extend(rng.integers(HALF + 1, Lstar + 1, size=n2).tolist())
    if n3 > 0:
        # I3 — paper used [15,100] under constraint L_T=2000, M_T=40 -> mean 50.
        # To match target total length, scale I3 draws.
        # Simple: draw uniform [46, 200], then linear-scale if total off-target.
        raw = rng.integers(46, 201, size=n3)
        cur_total = sum(lens) + raw.sum()
        deficit = target_total_len - cur_total
        # Distribute integer deficit across long fragments (clamp each to >=46).
        adj = raw.astype(float) + deficit / n3
        adj = np.maximum(adj, 46.0)
        lens.extend([int(round(x)) for x in adj])
    return lens


def main():
    rng_master = np.random.default_rng(0xA11CE)
    M_T = 40
    L_T = 2000
    n_runs = 30
    # grid of (r1, r2) with r1+r2 <= 1
    grid = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

    results = {}  # (r1, r2) -> mean rejoining time
    raw = {}
    n_cells = 0

    t0 = time.time()
    print(f"\n=== C11: T_M(r1, r2) surface, M_T={M_T}, L_T={L_T}, n_runs/cell={n_runs} ===")
    for r1 in grid:
        for r2 in grid:
            if r1 + r2 > 1.0 + 1e-9:
                continue
            n_cells += 1
            n2 = int(round(r1 * M_T))  # fraction in I2
            n1 = int(round(r2 * M_T))  # fraction in I1
            n3 = M_T - n1 - n2
            if n3 < 0:
                continue
            ts = np.zeros(n_runs)
            for k in range(n_runs):
                seed = int(rng_master.integers(0, 2**31 - 1))
                P = SimParams(k1=1.0, k2=0.5, k3=0.1, E=1.0, V=1.0, rng_seed=seed)
                init = build_init(np.random.default_rng(seed + 7), n1, n2, n3, L_T)
                t_end, _ = simulate(init, P)
                ts[k] = t_end
            key = (round(r1, 2), round(r2, 2))
            results[key] = float(ts.mean())
            raw[key] = ts.tolist()
            print(f"  r1={r1:.1f} r2={r2:.1f}  (n1={n1:2d}, n2={n2:2d}, n3={n3:2d})  "
                  f"mean T={ts.mean():7.2f}  std={ts.std():6.2f}")

    elapsed = time.time() - t0

    # Assess monotonicity along each axis (when other is held).
    def monotone(seq):
        diffs = np.diff(seq)
        return float((diffs >= -1e-3).mean())  # fraction of non-decreasing steps

    mono_r1 = []  # vary r1 holding r2 fixed
    for r2 in grid:
        seq = [results[(round(r1, 2), round(r2, 2))]
               for r1 in grid if (round(r1, 2), round(r2, 2)) in results]
        if len(seq) >= 3:
            mono_r1.append({"r2_fixed": r2, "values": seq, "mono_frac": monotone(seq)})
    mono_r2 = []
    for r1 in grid:
        seq = [results[(round(r1, 2), round(r2, 2))]
               for r2 in grid if (round(r1, 2), round(r2, 2)) in results]
        if len(seq) >= 3:
            mono_r2.append({"r1_fixed": r1, "values": seq, "mono_frac": monotone(seq)})

    # Pearson-like correlation: T vs r1, vs r2
    keys = list(results.keys())
    r1_arr = np.array([k[0] for k in keys])
    r2_arr = np.array([k[1] for k in keys])
    T_arr = np.array([results[k] for k in keys])
    corr_r1 = float(np.corrcoef(r1_arr, T_arr)[0, 1])
    corr_r2 = float(np.corrcoef(r2_arr, T_arr)[0, 1])

    summary = {
        "claim": "C11: T_M(r1, r2) increases in both r1 and r2",
        "grid": grid,
        "n_cells_run": len(results),
        "monotonicity_along_r1_axis_fixed_r2": mono_r1,
        "monotonicity_along_r2_axis_fixed_r1": mono_r2,
        "correlation_T_vs_r1": corr_r1,
        "correlation_T_vs_r2": corr_r2,
        "elapsed_s": elapsed,
        "verdict": (
            "STRONG" if (corr_r1 > 0.4 and corr_r2 > 0.4) else
            "PARTIAL" if (corr_r1 > 0.1 and corr_r2 > 0.1) else
            "WEAK"
        ),
    }
    (OUT_LOGS / "c11_2d_surface.json").write_text(json.dumps(summary, indent=2))
    np.savez(OUT_RESULTS / "c11_2d_surface.npz",
             keys=np.array(keys), means=np.array([results[k] for k in keys]))

    # Plot heatmap
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ng = len(grid)
        grid_arr = np.full((ng, ng), np.nan)
        for i, r1 in enumerate(grid):
            for j, r2 in enumerate(grid):
                k = (round(r1, 2), round(r2, 2))
                if k in results:
                    grid_arr[i, j] = results[k]
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(grid_arr, origin="lower", aspect="auto",
                       extent=[grid[0], grid[-1], grid[0], grid[-1]],
                       cmap="viridis")
        ax.set_xlabel("r2 (fraction in I1=(15,22] bp)")
        ax.set_ylabel("r1 (fraction in I2=(22,45] bp)")
        ax.set_title("C11: T_M(r1, r2) — mean rejoining time")
        plt.colorbar(im, ax=ax, label="mean T")
        plt.tight_layout()
        plt.savefig(OUT_FIGS / "c11_2d_surface.png", dpi=120)
        plt.close(fig)
    except Exception as e:
        print(f"  (plot skipped: {e})")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
