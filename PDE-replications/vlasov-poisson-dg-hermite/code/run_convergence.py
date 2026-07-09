"""Convergence sweep: Landau damping decay rate vs Hermite mode count N_H,
and vs spatial resolution Nx."""
import os
import json
import numpy as np
from vp_hermite import VPHermite, landau_ic, project_initial


def fit_decay(t, e_amp, t_min, t_max):
    mask = (t >= t_min) & (t <= t_max)
    tt = t[mask]
    yy = e_amp[mask]
    peaks_idx = [i for i in range(1, len(yy) - 1) if yy[i] > yy[i - 1] and yy[i] > yy[i + 1]]
    if len(peaks_idx) < 3:
        coef = np.polyfit(tt, np.log(yy + 1e-300), 1)
        return coef[0]
    tp = tt[peaks_idx]
    yp = yy[peaks_idx]
    coef = np.polyfit(tp, np.log(yp), 1)
    return coef[0]


def run_one(Nx, NH, T=25.0, dt=0.005):
    f0, L = landau_ic(alpha=0.01, k=0.5, v_t=1.0)
    solver = VPHermite(Nx=Nx, N=NH, L=L, v_t=1.0)
    C0 = project_initial(f0, solver.x, solver.v_grid, solver.psi)
    C, diag = solver.run(C0, T=T, dt=dt, diag_every=4)
    gamma = fit_decay(diag["t"], diag["E_max"], 1.0, min(T, 18.0))
    energy_drift = abs(diag["total_energy"][-1] - diag["total_energy"][0]) / abs(diag["total_energy"][0])
    mass_drift = abs(diag["mass"][-1] - diag["mass"][0]) / diag["mass"][0]
    return {
        "Nx": Nx, "N_H": NH, "T": T, "dt": dt,
        "gamma_fit": float(gamma),
        "rel_err_gamma": float(abs(gamma - (-0.1533)) / 0.1533),
        "energy_drift_rel": float(energy_drift),
        "mass_drift_rel": float(mass_drift),
    }


def main():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
    os.makedirs(out_dir, exist_ok=True)

    # Sweep N_H at fixed Nx=64
    results_NH = []
    for NH in [8, 16, 24, 32, 48, 64, 96]:
        r = run_one(Nx=64, NH=NH, T=25.0, dt=0.005)
        print(f"[NH-sweep] Nx=64  N_H={NH:3d}  gamma={r['gamma_fit']:.5f}  rel_err={r['rel_err_gamma']:.3e}  e_drift={r['energy_drift_rel']:.2e}")
        results_NH.append(r)

    # Sweep Nx at fixed N_H=48
    results_Nx = []
    for Nx in [16, 32, 64, 128]:
        r = run_one(Nx=Nx, NH=48, T=25.0, dt=0.005)
        print(f"[Nx-sweep] N_H=48  Nx={Nx:3d}  gamma={r['gamma_fit']:.5f}  rel_err={r['rel_err_gamma']:.3e}  e_drift={r['energy_drift_rel']:.2e}")
        results_Nx.append(r)

    with open(os.path.join(out_dir, "convergence.json"), "w") as fh:
        json.dump({"NH_sweep": results_NH, "Nx_sweep": results_Nx,
                   "gamma_ref": -0.1533, "omega_ref": 1.4156}, fh, indent=2)
    print("Saved convergence.json")


if __name__ == "__main__":
    main()
