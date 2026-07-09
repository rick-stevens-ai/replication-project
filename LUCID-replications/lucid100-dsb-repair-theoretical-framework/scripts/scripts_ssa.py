"""Stochastic simulation of master equation (2.1), vectorized tau-leaping.

For the rate constants in Table 1 of Murray et al. 2016, exact Gillespie
SSA executes ~10^5-10^8 events per simulated hour per trajectory, which is
too slow in pure Python.  We use a fixed-step Poisson tau-leap with
tau small enough that propensities are quasi-constant inside the step.

Reactions per DSB site (X in {0,1}, Y, Z >= 0):
  1. repair:                     X 1->0       rate k1 * Y         (if X==1)
  2. pATM recruit from DSB:      Y += 1       rate k2 * X         (if Y<Ymax)
  3. pATM recruit from gH2AX:    Y += 1       rate k3 * Z         (if Y<Ymax)
  4. pATM dissociation:          Y -= 1       rate k4 * Y         (if Y>0)
  5. H2AX phosphorylation:       Z += 1       rate k5 * Y         (if Z<Zmax)
  6. gH2AX dephosphorylation:    Z -= 1       rate k6 * Z         (if Z>0)
"""
from __future__ import annotations
import numpy as np


def tauleap_ensemble(p, y_max, z_max, z_star, t_grid, n_runs=200, tau=0.001, seed=0):
    """Tau-leap vectorized over n_runs trajectories. Returns (detectable_fraction, mean_Z) on t_grid."""
    rng = np.random.default_rng(seed)
    n_grid = len(t_grid)
    X = np.ones(n_runs, dtype=np.int32)
    Y = np.zeros(n_runs, dtype=np.int32)
    Z = np.zeros(n_runs, dtype=np.int32)
    t = 0.0
    t_end = float(t_grid[-1])
    detectable = np.zeros(n_grid)
    mean_Z = np.zeros(n_grid)
    grid_idx = 0
    # Record initial
    detectable[0] = (Z >= z_star).mean()
    mean_Z[0] = Z.mean()
    grid_idx = 1
    k1, k2, k3, k4, k5, k6 = p["k1"], p["k2"], p["k3"], p["k4"], p["k5"], p["k6"]
    while t < t_end and grid_idx < n_grid:
        r1 = k1 * Y * X                          # repair (only when X==1)
        r2 = k2 * X * (Y < y_max).astype(np.int32)
        r3 = k3 * Z * (Y < y_max).astype(np.int32)
        r4 = k4 * Y
        r5 = k5 * Y * (Z < z_max).astype(np.int32)
        r6 = k6 * Z
        # Draw Poisson events; cap to keep populations sane
        n1 = rng.poisson(r1 * tau)
        n2 = rng.poisson(r2 * tau)
        n3 = rng.poisson(r3 * tau)
        n4 = rng.poisson(r4 * tau)
        n5 = rng.poisson(r5 * tau)
        n6 = rng.poisson(r6 * tau)
        # Apply updates (and clamp)
        X = np.where(n1 > 0, 0, X)  # any repair zeroes X
        Y = Y + n2 + n3 - n4
        Z = Z + n5 - n6
        np.clip(Y, 0, y_max, out=Y)
        np.clip(Z, 0, z_max, out=Z)
        t += tau
        # Record samples whose grid time has been reached
        while grid_idx < n_grid and t >= t_grid[grid_idx]:
            detectable[grid_idx] = (Z >= z_star).mean()
            mean_Z[grid_idx] = Z.mean()
            grid_idx += 1
    return detectable, mean_Z


# Backwards-compatible name used by smoke_model.py
gillespie_ensemble = tauleap_ensemble
