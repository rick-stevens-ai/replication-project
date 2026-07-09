"""Run Landau damping benchmark.

Linear Landau damping for k=0.5, v_t=1.0:
  γ ≈ -0.1533 (decay rate)
  ω ≈ 1.4156 (oscillation freq)
"""
import os
import json
import numpy as np
import argparse

from vp_hermite import VPHermite, landau_ic, project_initial


def fit_decay(t, e_amp, t_min, t_max):
    """Fit y = A exp(γ t) to the envelope of e_amp (positive amplitude)."""
    mask = (t >= t_min) & (t <= t_max)
    tt = t[mask]
    yy = e_amp[mask]
    # Use peaks of |E|_∞ envelope: local maxima
    peaks_idx = []
    for i in range(1, len(yy) - 1):
        if yy[i] > yy[i - 1] and yy[i] > yy[i + 1]:
            peaks_idx.append(i)
    if len(peaks_idx) < 3:
        # fallback: log-fit raw
        coef = np.polyfit(tt, np.log(yy + 1e-300), 1)
        return coef[0], np.exp(coef[1]), tt, yy
    tp = tt[peaks_idx]
    yp = yy[peaks_idx]
    coef = np.polyfit(tp, np.log(yp), 1)
    return coef[0], np.exp(coef[1]), tp, yp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Nx", type=int, default=64)
    parser.add_argument("--N", type=int, default=64, help="Hermite modes")
    parser.add_argument("--T", type=float, default=30.0)
    parser.add_argument("--dt", type=float, default=0.025)
    parser.add_argument("--alpha", type=float, default=0.01)
    parser.add_argument("--k", type=float, default=0.5)
    parser.add_argument("--v_t", type=float, default=1.0)
    parser.add_argument("--diag_every", type=int, default=2)
    parser.add_argument("--nu", type=float, default=0.0)
    parser.add_argument("--out", type=str, default="../results/landau.npz")
    args = parser.parse_args()

    f0, L = landau_ic(alpha=args.alpha, k=args.k, v_t=args.v_t)
    solver = VPHermite(Nx=args.Nx, N=args.N, L=L, v_t=args.v_t, nu=args.nu)

    # Project initial condition
    C0 = project_initial(f0, solver.x, solver.v_grid, solver.psi)

    print(f"[landau] L={L:.4f}  Nx={args.Nx}  N_H={args.N}  T={args.T}  dt={args.dt}")
    print(f"[landau] initial mass = {solver.total_mass(C0):.6e}")
    rho0 = solver.density(C0)
    E0 = solver.poisson(rho0)
    print(f"[landau] initial |E|_∞ = {np.max(np.abs(E0)):.6e}")

    C, diag = solver.run(C0, T=args.T, dt=args.dt, diag_every=args.diag_every)

    # Fit decay rate from peaks of E_max envelope
    gamma, A, tp, yp = fit_decay(diag["t"], diag["E_max"], t_min=1.0, t_max=min(args.T, 20.0))
    print(f"[landau] fitted γ = {gamma:.5f}  (analytical ≈ -0.1533)")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.savez(args.out, **{k: v for k, v in diag.items()},
             Nx=args.Nx, N=args.N, L=L, dt=args.dt, alpha=args.alpha, k=args.k, v_t=args.v_t,
             gamma_fit=gamma, peaks_t=tp, peaks_y=yp)
    print(f"[landau] saved -> {args.out}")

    # also dump JSON summary
    summ = {
        "Nx": args.Nx, "N_H": args.N, "T": args.T, "dt": args.dt,
        "alpha": args.alpha, "k": args.k, "v_t": args.v_t,
        "gamma_fit": float(gamma),
        "gamma_ref": -0.1533,
        "rel_err_gamma": float(abs(gamma - (-0.1533)) / 0.1533),
        "mass_drift_rel": float((diag["mass"][-1] - diag["mass"][0]) / diag["mass"][0]),
        "energy_drift_rel": float((diag["total_energy"][-1] - diag["total_energy"][0])
                                  / abs(diag["total_energy"][0]) if abs(diag["total_energy"][0]) > 0 else 0.0),
        "momentum_drift_abs": float(abs(diag["momentum"][-1] - diag["momentum"][0])),
        "l2_drift_rel": float((diag["l2"][-1] - diag["l2"][0]) / diag["l2"][0]),
    }
    with open(args.out.replace(".npz", "_summary.json"), "w") as fh:
        json.dump(summ, fh, indent=2)
    print(json.dumps(summ, indent=2))


if __name__ == "__main__":
    main()
