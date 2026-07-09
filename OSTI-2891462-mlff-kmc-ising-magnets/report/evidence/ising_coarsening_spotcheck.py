#!/usr/bin/env python3
"""
Spot-check for OSTI 2891462 / arXiv 2411.19780 (Tyberg, Fan, Chern 2024).

The paper claims: after a thermal quench of a square-lattice double-exchange
Ising model to a temperature well below Tc but not too low, the domain
coarsening follows the Allen-Cahn power law  L(t) ~ t^{1/2}  (their T=0.1
case, growth exponent alpha = 1/2).

We CANNOT feasibly reproduce their CNN-based ML force field for the electron-
mediated Ising-DE Hamiltonian in a subagent budget. What we CAN do is verify
the well-established physics benchmark they lean on: the standard 2D
nearest-neighbor Ising model on a square lattice, quenched to T well below
Tc = 2.269 J, using Glauber dynamics, should exhibit L(t) ~ t^{1/2} at
higher quench temperatures (Allen-Cahn universality class).

This spot-check does exactly that: standard 2D NN Ising, Glauber dynamics
(same dynamics as the paper), thermal quench from T=infinity, characteristic
length from the correlation function using the same formula as Eq. (10) in
the paper, and fit L(t) ~ t^alpha on the coarsening window.

If we recover alpha ~ 0.5, that supports Allen-Cahn universality is
correctly identified as the reference class the paper compares against.
It does NOT verify their ML model or the anomalous alpha=1/4 at T=0.01.
"""

from __future__ import annotations
import json
import time
import numpy as np


def glauber_sweep(spins: np.ndarray, beta: float, rng: np.random.Generator) -> None:
    """One Glauber sweep in-place; N random single-spin updates on an LxL lattice."""
    L = spins.shape[0]
    N = L * L
    # Vectorize by picking N random sites (with replacement, that's OK for Glauber)
    xs = rng.integers(0, L, size=N)
    ys = rng.integers(0, L, size=N)
    us = rng.random(N)
    for k in range(N):
        i, j = xs[k], ys[k]
        s = spins[i, j]
        # NN sum with periodic BCs
        nb = (
            spins[(i + 1) % L, j]
            + spins[(i - 1) % L, j]
            + spins[i, (j + 1) % L]
            + spins[i, (j - 1) % L]
        )
        # Glauber: flip probability = 1 / (1 + exp(beta * dE)), where dE = 2*s*J*nb (J=1)
        dE = 2.0 * s * nb
        p_flip = 1.0 / (1.0 + np.exp(beta * dE))
        if us[k] < p_flip:
            spins[i, j] = -s


def correlation_length(spins: np.ndarray) -> float:
    """Characteristic domain length from the connected pair correlation.

    Following Bray's phase-ordering review and the paper's Eq. (10),
    we compute C(r) = <(s(0)-m)(s(r)-m)> radially, normalize to C(0)=1,
    truncate at the first zero crossing r*, and take
        L = sum_{r=0..r*} r*C(r) / sum_{r=0..r*} C(r).
    Truncating at the first zero avoids the negative-tail artifact that
    corrupts the naive Eq.(10) estimate.
    """
    L = spins.shape[0]
    s = spins.astype(np.float64) - spins.mean()
    F = np.fft.fft2(s)
    C2d = np.real(np.fft.ifft2(F * np.conj(F))) / (L * L)
    C2d = np.fft.fftshift(C2d)
    c0 = C2d[L // 2, L // 2]
    if c0 <= 0:
        return 0.0
    C2d = C2d / c0

    y, x = np.indices((L, L))
    r = np.sqrt((x - L / 2) ** 2 + (y - L / 2) ** 2)
    r_int = r.astype(int)
    max_r = L // 2
    C_r = np.zeros(max_r)
    for rr in range(max_r):
        mask = r_int == rr
        if mask.any():
            C_r[rr] = C2d[mask].mean()

    # Find first zero crossing
    r_star = max_r
    for rr in range(1, max_r):
        if C_r[rr] <= 0:
            r_star = rr
            break
    if r_star < 2:
        return 0.0
    r_arr = np.arange(r_star, dtype=np.float64)
    num = np.sum(r_arr * C_r[:r_star])
    den = np.sum(C_r[:r_star])
    if den <= 0:
        return 0.0
    return float(num / den)


def run_quench(L: int, T: float, n_sweeps: int, sample_every: int, n_runs: int, seed: int) -> dict:
    """Return t (in sweeps) and averaged L(t) across n_runs quenches."""
    beta = 1.0 / T
    n_samples = n_sweeps // sample_every
    t_arr = np.array([(k + 1) * sample_every for k in range(n_samples)], dtype=np.float64)
    L_arr = np.zeros(n_samples, dtype=np.float64)
    for run in range(n_runs):
        rng = np.random.default_rng(seed + run)
        spins = rng.choice(np.array([-1, 1], dtype=np.int8), size=(L, L))
        for k in range(n_samples):
            for _ in range(sample_every):
                glauber_sweep(spins, beta, rng)
            L_arr[k] += correlation_length(spins)
    L_arr /= n_runs
    return {"t": t_arr.tolist(), "L": L_arr.tolist(), "L_lattice": L, "T": T,
            "n_runs": n_runs, "n_sweeps": n_sweeps, "sample_every": sample_every, "seed": seed}


def fit_power_law(t: np.ndarray, L: np.ndarray, t_min: float, t_max: float) -> dict:
    """Fit log L = alpha * log t + c on the window t in [t_min, t_max]."""
    m = (t >= t_min) & (t <= t_max) & (L > 0)
    if m.sum() < 4:
        return {"alpha": None, "intercept": None, "n": int(m.sum())}
    x = np.log(t[m])
    y = np.log(L[m])
    A = np.vstack([x, np.ones_like(x)]).T
    (alpha, c), residuals, rank, sv = np.linalg.lstsq(A, y, rcond=None)
    # crude R^2
    yhat = alpha * x + c
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
    return {"alpha": float(alpha), "intercept": float(c), "R2": float(r2) if r2 is not None else None,
            "n_points": int(m.sum()), "t_min": t_min, "t_max": t_max}


def main() -> None:
    t0 = time.time()
    # 128x128 lattice, quench to T=1.7 (well below Tc=2.269 but above the freezing regime).
    # 800 sweeps, sample every 10, 3 runs. Reference: Bray, Adv. Phys. 43, 357 (1994).
    result = run_quench(L=128, T=1.7, n_sweeps=800, sample_every=10, n_runs=3, seed=20260703)
    t_arr = np.array(result["t"])
    L_arr = np.array(result["L"])
    # Multiple fit windows to check robustness. Reference: pure Allen-Cahn -> alpha=0.5.
    # We report the early-time (well below saturation) window as primary; late-time
    # deviation is a known finite-size saturation effect (L -> L_lattice/2).
    fit_primary = fit_power_law(t_arr, L_arr, t_min=30.0, t_max=300.0)
    fit_secondary = fit_power_law(t_arr, L_arr, t_min=50.0, t_max=400.0)
    fit_full = fit_power_law(t_arr, L_arr, t_min=30.0, t_max=600.0)
    out = {
        "paper": "OSTI 2891462 / arXiv 2411.19780 (Tyberg, Fan, Chern 2024)",
        "spot_check": (
            "Allen-Cahn alpha=1/2 for standard 2D NN Ising, Glauber, T=1.7 (below Tc=2.269), "
            "L=128, 800 sweeps, 3 seed-runs, correlation length by connected-C(r) truncated at first zero."
        ),
        "reference_alpha": 0.5,
        "measured_primary_window": fit_primary,
        "measured_secondary_window": fit_secondary,
        "measured_full_window": fit_full,
        "note_finite_size": (
            "L(t) saturates at ~L_lattice/2 = 64. Late-time deviation from pure alpha=0.5 is finite-size, "
            "not a physics discrepancy. Early-window primary fit is the correct benchmark comparison."
        ),
        "series": result,
        "elapsed_seconds": time.time() - t0,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
