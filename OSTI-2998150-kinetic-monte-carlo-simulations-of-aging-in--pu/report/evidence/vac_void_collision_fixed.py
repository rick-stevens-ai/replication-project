#!/usr/bin/env python3
"""
Corrected replication of Eq. (5) from Oppelstrup et al. 2025.

Fix vs work/vac_void_collision.py: rho is the density of ABSORBERS (voids),
not the density of walkers. Since we simulate ONE absorbing sphere in volume
L^3, rho = 1/L^3. tau is the mean per-walker time between absorptions.

Claim:  DRρτ = 0.078 - 0.19*(R/L)   (paper Eq. 5)
        Theoretical intercept: 1/(4π) = 0.07958
"""
import argparse
import json
import math
import time
from pathlib import Path
import numpy as np

FOUR_PI_INV = 1.0 / (4.0 * math.pi)


def segment_hits_sphere(x0, x1, R2):
    d = x1 - x0
    dd = np.einsum("ij,ij->i", d, d)
    dd_safe = np.where(dd > 0, dd, 1.0)
    t_star = -np.einsum("ij,ij->i", x0, d) / dd_safe
    t_star = np.clip(t_star, 0.0, 1.0)
    closest = x0 + t_star[:, None] * d
    return np.einsum("ij,ij->i", closest, closest) < R2


def one_experiment(N, L, R, D=1.0, target_events=2000, seed=0, dt_frac=0.05):
    rng = np.random.default_rng(seed)
    step_rms_per_axis = dt_frac * R
    dt = step_rms_per_axis ** 2 / (2.0 * D)
    sigma_axis = math.sqrt(2.0 * D * dt)
    R2 = R * R
    half_L = L / 2.0

    def sample_positions(n):
        pos = np.empty((n, 3))
        filled = 0
        while filled < n:
            k = n - filled
            trial = rng.uniform(-half_L, half_L, size=(k * 4, 3))
            r2 = np.sum(trial ** 2, axis=1)
            keep = trial[r2 > R2][:k]
            m = keep.shape[0]
            pos[filled:filled + m] = keep
            filled += m
        return pos

    pos = sample_positions(N)
    n_events = 0
    t_now = 0.0
    max_steps = 20_000_000
    step = 0
    while n_events < target_events and step < max_steps:
        step += 1
        jump = rng.normal(0.0, sigma_axis, size=pos.shape)
        new_pos = pos + jump
        hit_mask = segment_hits_sphere(pos, new_pos, R2)
        new_pos -= L * np.round(new_pos / L)
        pos = new_pos
        hit_idx = np.where(hit_mask)[0]
        if hit_idx.size > 0:
            n_events += hit_idx.size
            pos[hit_idx] = sample_positions(hit_idx.size)
        t_now += dt

    # Per-walker mean-wait between absorptions
    tau = t_now * N / n_events
    # DENSITY OF VOIDS = 1 / L^3 (single absorbing sphere in box)
    rho = 1.0 / (L ** 3)
    DRrhotau = D * R * rho * tau
    return dict(L=L, R=R, N=N, D=D, dt=dt, steps_taken=step,
                n_events=n_events, sim_time=t_now, tau_mean=tau,
                rho_voids=rho, DRrhotau=DRrhotau)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--Ls", nargs="+", type=float, default=[15.0, 20.0])
    ap.add_argument("--Rs", nargs="+", type=float, default=[1.0, 1.5, 2.0, 3.0])
    ap.add_argument("--N", type=int, default=200)
    ap.add_argument("--events", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--dt_frac", type=float, default=0.05)
    args = ap.parse_args()

    t0 = time.time()
    results = []
    for L in args.Ls:
        for R in args.Rs:
            r = one_experiment(N=args.N, L=L, R=R,
                               target_events=args.events,
                               seed=args.seed + int(1000 * (L + R)),
                               dt_frac=args.dt_frac)
            r["four_pi_inv"] = FOUR_PI_INV
            print(f"L={L:5.1f} R={R:4.2f} N={args.N:4d} events={r['n_events']:5d} "
                  f"steps={r['steps_taken']:>8d}  "
                  f"DRρτ={r['DRrhotau']:.5f}  (1/4π={FOUR_PI_INV:.5f})",
                  flush=True)
            results.append(r)

    x = np.array([r["R"] / r["L"] for r in results])
    y = np.array([r["DRrhotau"] for r in results])
    A = np.vstack([np.ones_like(x), x]).T
    (a, b), *_ = np.linalg.lstsq(A, y, rcond=None)

    summary = {
        "results": results,
        "fit_intercept_a": float(a),
        "fit_slope_b": float(b),
        "paper_intercept": 0.078,
        "paper_slope": -0.19,
        "theoretical_intercept": FOUR_PI_INV,
        "wallclock_s": time.time() - t0,
        "args": vars(args),
        "python": __import__("sys").version,
        "numpy": np.__version__,
    }
    Path(args.out).write_text(json.dumps(summary, indent=2))
    print(f"\nFit:   DRρτ = {a:.5f} + ({b:.5f})*(R/L)")
    print(f"Paper: DRρτ = 0.078 + (-0.19)*(R/L)")
    print(f"Theory intercept 1/(4π) = {FOUR_PI_INV:.5f}")
    print(f"Wrote {args.out}   ({summary['wallclock_s']:.1f}s wall)")


if __name__ == "__main__":
    main()
