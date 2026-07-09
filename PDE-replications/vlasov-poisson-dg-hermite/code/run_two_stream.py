"""Two-stream instability benchmark.

Two counter-propagating Maxwellians, alpha=0.05 perturbation in cos(kx),
k=0.5, v_b=2.0, v_t=1.0. Linear growth rate γ ≈ 0.25 (well-known).
"""
import os
import json
import argparse
import numpy as np

from vp_hermite import VPHermite, two_stream_ic, two_stream_classical_ic, project_initial


def fit_growth(t, e_amp, t_min, t_max):
    mask = (t >= t_min) & (t <= t_max)
    tt = t[mask]
    yy = e_amp[mask]
    coef = np.polyfit(tt, np.log(yy + 1e-300), 1)
    return coef[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Nx", type=int, default=128)
    parser.add_argument("--N", type=int, default=96)
    parser.add_argument("--T", type=float, default=40.0)
    parser.add_argument("--dt", type=float, default=0.005)
    parser.add_argument("--out", type=str, default="../results/two_stream.npz")
    parser.add_argument("--variant", type=str, default="classical",
                        choices=["classical", "symmetric"])
    args = parser.parse_args()

    if args.variant == "classical":
        # Filbet-Sonnendrücker: f0 = 2 v^2 e^{-v^2/2}/sqrt(2π) * (1+α cos kx)
        # Linear growth rate γ ≈ 0.2845 for k=0.5.
        f0, L = two_stream_classical_ic(alpha=0.05, k=0.5)
        gamma_ref = 0.2845
    else:
        f0, L = two_stream_ic(alpha=0.05, k=0.5, v_t=1.0, v_b=2.0)
        gamma_ref = 0.25
    solver = VPHermite(Nx=args.Nx, N=args.N, L=L, v_t=1.0)
    C0 = project_initial(f0, solver.x, solver.v_grid, solver.psi)

    print(f"[two_stream] L={L:.4f}  Nx={args.Nx}  N_H={args.N}  T={args.T}  dt={args.dt}")
    print(f"[two_stream] initial mass = {solver.total_mass(C0):.6e}")

    C, diag = solver.run(C0, T=args.T, dt=args.dt, diag_every=4)

    # Fit linear growth rate in early window from peaks of E_l2 (cleaner than
    # E_max which oscillates with the standing wave).
    t = diag["t"]; e = diag["E_l2"]
    # Look for early linear growth before saturation; use peaks of E_l2
    peaks = [i for i in range(1, len(e) - 1) if e[i] > e[i-1] and e[i] > e[i+1]]
    peaks_arr = np.array(peaks)
    mask_p = (t[peaks_arr] >= 1.0) & (t[peaks_arr] <= 10.0)
    if np.sum(mask_p) >= 3:
        tp = t[peaks_arr][mask_p]; ep = e[peaks_arr][mask_p]
        coef = np.polyfit(tp, np.log(ep), 1)
        gamma = coef[0]
        print(f"[two_stream] linear growth γ = {gamma:.5f} from {np.sum(mask_p)} peaks in [1,10]  (reference ≈ {gamma_ref})")
    else:
        gamma = fit_growth(t, e, 2.0, 9.0)
        print(f"[two_stream] linear growth γ = {gamma:.5f} (fallback log-fit)  (reference ≈ {gamma_ref})")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.savez(args.out, **diag, Nx=args.Nx, N=args.N, L=L, dt=args.dt,
             gamma_fit=gamma)

    summ = {
        "Nx": args.Nx, "N_H": args.N, "T": args.T, "dt": args.dt,
        "variant": args.variant,
        "gamma_fit": float(gamma),
        "gamma_ref": gamma_ref,
        "rel_err_gamma": float(abs(gamma - gamma_ref) / gamma_ref),
        "mass_drift_rel": float((diag["mass"][-1] - diag["mass"][0]) / diag["mass"][0]),
        "energy_drift_rel": float((diag["total_energy"][-1] - diag["total_energy"][0])
                                  / abs(diag["total_energy"][0])),
        "momentum_drift_abs": float(abs(diag["momentum"][-1] - diag["momentum"][0])),
        "E_max_final": float(diag["E_max"][-1]),
        "E_max_initial": float(diag["E_max"][0]),
    }
    with open(args.out.replace(".npz", "_summary.json"), "w") as fh:
        json.dump(summ, fh, indent=2)
    print(json.dumps(summ, indent=2))


if __name__ == "__main__":
    main()
