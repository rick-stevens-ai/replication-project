#!/usr/bin/env python3
"""Exact Gillespie SSA cross-check for the master equation (2.1).

Used to verify whether the tau-leap in scripts_ssa.py is biased relative to
exact SSA, and whether SSA-vs-ODE deviation is a real model property
(closure inaccuracy) or a tau-leap artifact.

Run only on a small horizon (e.g. 1.5 h MDA-MB-468) -- a single MCF7 hour
involves ~1e6 reactions per trajectory.
"""
from __future__ import annotations
import numpy as np
import json
from pathlib import Path

PARAMS = {
    "MDA-MB-468": dict(k1=0.0032, k2=159.0, k3=14.0, k4=71.0, k5=1056.0, k6=211.0),
    "MCF7":       dict(k1=0.02,   k2=1236.0, k3=220.0, k4=687.0, k5=1765.0, k6=565.0),
}
Y_MAX, Z_MAX = 300, 1000


def ssa_one(p, t_end, rng):
    """Exact Gillespie; returns event-time arrays for X, Y, Z."""
    X, Y, Z = 1, 0, 0
    t = 0.0
    ts = [0.0]; Xs = [X]; Ys = [Y]; Zs = [Z]
    k1, k2, k3, k4, k5, k6 = (p[k] for k in ("k1","k2","k3","k4","k5","k6"))
    while t < t_end:
        r1 = k1 * Y * X
        r2 = k2 * X if Y < Y_MAX else 0
        r3 = k3 * Z if Y < Y_MAX else 0
        r4 = k4 * Y
        r5 = k5 * Y if Z < Z_MAX else 0
        r6 = k6 * Z
        rtot = r1 + r2 + r3 + r4 + r5 + r6
        if rtot <= 0:
            break
        dt = rng.exponential(1.0 / rtot)
        t += dt
        if t > t_end:
            break
        u = rng.random() * rtot
        cum = 0.0
        for idx, r in enumerate((r1, r2, r3, r4, r5, r6)):
            cum += r
            if u <= cum:
                rxn = idx; break
        if   rxn == 0: X = 0
        elif rxn == 1: Y += 1
        elif rxn == 2: Y += 1
        elif rxn == 3: Y -= 1
        elif rxn == 4: Z += 1
        else:          Z -= 1
        ts.append(t); Xs.append(X); Ys.append(Y); Zs.append(Z)
    return np.array(ts), np.array(Xs), np.array(Ys), np.array(Zs)


def sample_grid(ts, ys, grid):
    """Right-continuous step function sampled on grid."""
    idx = np.searchsorted(ts, grid, side="right") - 1
    idx = np.clip(idx, 0, len(ys) - 1)
    return ys[idx]


def ensemble_mean(p, t_end, n_runs, grid, seed=0):
    rng = np.random.default_rng(seed)
    sumX = np.zeros_like(grid)
    sumY = np.zeros_like(grid)
    sumZ = np.zeros_like(grid)
    for _ in range(n_runs):
        ts, Xs, Ys, Zs = ssa_one(p, t_end, rng)
        sumX += sample_grid(ts, Xs, grid)
        sumY += sample_grid(ts, Ys, grid)
        sumZ += sample_grid(ts, Zs, grid)
    return sumX / n_runs, sumY / n_runs, sumZ / n_runs


def main():
    line = "MDA-MB-468"
    p = PARAMS[line]
    t_end = 1.0
    grid = np.linspace(0.0, t_end, 21)
    n_runs = 100
    mX, mY, mZ = ensemble_mean(p, t_end, n_runs, grid, seed=7)
    out = {
        "line": line,
        "t_end_h": t_end,
        "n_runs": n_runs,
        "method": "exact_gillespie",
        "t_h": grid.tolist(),
        "mean_X": mX.tolist(),
        "mean_Y": mY.tolist(),
        "mean_Z": mZ.tolist(),
    }
    out_path = Path(__file__).resolve().parent.parent / "artifacts" / "ssa_exact_mda468.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Exact SSA mean at t={t_end}h: <X>={mX[-1]:.3f}, <Y>={mY[-1]:.2f}, <Z>={mZ[-1]:.2f}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
