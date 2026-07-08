#!/usr/bin/env python3
"""Verify that the MPF error scales as ~1/lambda^4 (i.e., 1/k^{p+2} for p=2)
while the base 2nd-order Trotter error scales as ~1/lambda^2 (=1/k^2)."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpf_replication import (
    hamiltonian_terms, s2_step, rho_k, rho_exact, trace_norm,
    mpf_state, neel_state
)

def scan(n=3, t=1.0, seed=1, lambdas=(1,2,3,4,5,6)):
    rng = np.random.default_rng(seed)
    h = rng.uniform(-1.0, 1.0, size=n)
    H_full, F_mats = hamiltonian_terms(n, h)
    psi_in = neel_state(n)
    rho_ex = rho_exact(H_full, t, psi_in)

    cs = np.array([0.016088, -1.794934, 2.778846])
    base_ks = np.array([4, 13, 17])

    rows = []
    for lam in lambdas:
        ks = base_ks * lam
        k_max = int(ks[-1])
        rk = rho_k(F_mats, t, k_max, psi_in)
        trot_err = trace_norm(rho_ex - rk)
        mu = mpf_state(F_mats, t, ks, cs, psi_in)
        mpf_err = trace_norm(rho_ex - mu)
        rows.append((lam, k_max, trot_err, mpf_err))
        print(f"lambda={lam:2d} k_max={k_max:3d}  "
              f"trot={trot_err:.4e}  mpf={mpf_err:.4e}", flush=True)

    lam_arr = np.array([r[0] for r in rows], dtype=float)
    trot_arr = np.array([r[2] for r in rows], dtype=float)
    mpf_arr  = np.array([r[3] for r in rows], dtype=float)

    trot_slope = np.polyfit(np.log(lam_arr), np.log(trot_arr), 1)[0]
    mpf_slope  = np.polyfit(np.log(lam_arr), np.log(mpf_arr), 1)[0]
    print(f"\n[n={n} t={t}] fitted slope log(err) vs log(lambda):")
    print(f"  Trotter S_2 slope = {trot_slope:.3f}  (expect -2)")
    print(f"  MPF (p=2)   slope = {mpf_slope:.3f}   (expect -4)")

    return {
        "n": n, "t": t,
        "lambdas": [r[0] for r in rows],
        "k_max": [r[1] for r in rows],
        "trotter_err": trot_arr.tolist(),
        "mpf_err": mpf_arr.tolist(),
        "trotter_slope_measured": trot_slope,
        "mpf_slope_measured": mpf_slope,
        "trotter_slope_expected": -2.0,
        "mpf_slope_expected": -4.0,
    }

if __name__ == "__main__":
    out = {}
    for n in (3, 4):
        out[f"n{n}"] = scan(n=n, t=1.0)
    outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "report", "evidence"))
    with open(os.path.join(outdir, "scaling_check.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote scaling_check.json")
