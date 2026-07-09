#!/usr/bin/env python3
"""
Full ODE replication v2 of Belov et al. 2023 (CIMB 45:7352).

This v2 uses RAW dimensional units (no scaling) per Table A1 directly.
Concentrations in M, time in h, rate constants in their tabulated dimensional units.
This is the simplest, least-error-prone interpretation; the paper's "scaled" form is
mathematically equivalent but the printed dimensionless rates have inconsistencies
(notably p9 = X1/K8 versus a Table A1 formula for P9 that gives a different value).

Strategy: solve Eqs. (A4)-(A7) in raw units. Initial condition n0(0) = alpha(L)*D
(DSBs per cell, converted to molar via /(NA*Vnucl)).  All "constant" species
(x1,x3,x7,x9,x11,x15, y1,y3,y7,y9c,y12, z1,z4,z7, w1,w3,w6) are held at X1 = 9.19e-7 M.

Output: same set of CSVs/figures/results.json as v1 but with model that produces
non-trivial dynamics.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    plt = None


# ---- Paper constants ----
A_PARAM = 27.5
B_PARAM = 2.43e-3
LET = 0.3
X1 = 9.19e-7   # M
K8 = 0.552     # h^-1
NA = 6.022e23
V_NUCL = 7.23e-13   # L
N_KU_PER_CELL = 400000

# ---- Raw rate constants (Table A1) ----
K1, Km1   = 11.05,   6.6e-4
Km2       = 0.526
K3        = 1.86
Km4       = 3.86e-4
K5, Km5   = 15.24,   8.28
K6, Km6   = 18.06,   1.33
K7, Km7   = 2.73e5,  3.20
K9        = 0.166
K11       = 7.5e-2
K12       = 11.10
P1, Pm1   = 1.75e3,  1.33e-4
P2        = 7.21
P3, Pm3   = 1.37e4,  2.34
P4        = 5.52e-2
P5, Pm5   = 1.20e5,  8.82e-5
P6, Pm6   = 1.87e5,  1.55e-3
P7        = 21.36
P8, Pm8   = 1.20e4,  2.49e-4
P10       = 7.20e-3
P11       = 6.06e-4
P12       = 2.76e-1
Q1, Qm1   = 7.80e3,  1.71e-4
Q2        = 3.00e4
Q3, Qm3   = 6.00e3,  6.06e-4
Q4        = 1.66e-6
Q5, Qm5   = 8.40e4,  4.75e-4
Q6        = 11.58
R1, Rm1   = 2.39e3,  12.63
R2        = 4.07e4
R3        = 9.82
R4, Rm4   = 1.47e5,  2.72
R5        = 0.165


def K2_of_D(D):
    D = max(D, 1e-6)
    return 18.83 * (1.09 - math.exp(-21.42 / D**1.82))


def K4_of_D(D):
    D = max(D, 1e-6)
    return 1.20 + 4.48e5 * math.exp(-12.70 * D**0.09)


def P9_of_D(D):
    D = max(D, 1e-6)
    arg = 6.16e-6 / D**2.68 - D**0.03
    arg = min(arg, 50.0)
    return 1.11 * math.exp(arg)


def Nirrep(D):
    if D >= 1.0:
        return 0.01
    return max(0.12 * math.exp(-2.48 * D**2.02) - 0.11 * math.exp(-5.43 * D**0.76), 1e-4)


def K10_of_D(D):
    return 1.93e-7 / Nirrep(D)


def alpha_of_L(L):
    return A_PARAM * math.exp(-B_PARAM * L)


# State indices (29 dynamic states)
IDX = {
    'n0':0, 'x2':1, 'x4':2, 'x5':3, 'x6':4, 'x8':5, 'x10':6, 'x12':7, 'x13':8, 'x14':9,
    'y2':10, 'y4':11, 'y5':12, 'y6':13, 'y8':14, 'y10':15, 'y11':16, 'y13':17, 'y14':18, 'y15':19,
    'z2':20, 'z3':21, 'z5':22, 'z6':23, 'z8':24,
    'w2':25, 'w4':26, 'w5':27, 'w7':28,
}
N_STATES = 29


def rhs(t, u, D, cycle_full=True):
    """Raw-units RHS. Time in h, concentrations in M."""
    K2 = K2_of_D(D); K4 = K4_of_D(D); P9 = P9_of_D(D); K10 = K10_of_D(D)

    n0  = u[IDX['n0']]
    x2  = u[IDX['x2']]
    x4  = u[IDX['x4']]
    x5  = u[IDX['x5']]
    x6  = u[IDX['x6']]
    x8  = u[IDX['x8']]
    x10 = u[IDX['x10']]
    x12 = u[IDX['x12']]
    x13 = u[IDX['x13']]
    x14 = u[IDX['x14']]
    y2  = u[IDX['y2']]
    y4  = u[IDX['y4']]
    y5  = u[IDX['y5']]
    y6  = u[IDX['y6']]
    y8  = u[IDX['y8']]
    y10 = u[IDX['y10']]
    y11 = u[IDX['y11']]
    y13 = u[IDX['y13']]
    y14 = u[IDX['y14']]
    y15 = u[IDX['y15']]
    z2 = u[IDX['z2']]; z3 = u[IDX['z3']]; z5 = u[IDX['z5']]; z6 = u[IDX['z6']]; z8 = u[IDX['z8']]
    w2 = u[IDX['w2']]; w4 = u[IDX['w4']]; w5 = u[IDX['w5']]; w7 = u[IDX['w7']]

    # Constants (all at X1 molar)
    x1 = X1; x3 = X1; x7 = X1; x9 = X1; x11 = X1; x15 = X1
    y1 = X1; y3 = X1; y7 = X1; y9c = X1; y12 = X1
    z1 = X1; z4 = X1; z7 = X1
    w1 = X1; w3 = X1; w6 = X1

    if not cycle_full:
        y2 = y4 = y5 = y6 = y8 = y10 = y11 = y13 = y14 = y15 = 0.0
        z2 = z3 = z5 = z6 = z8 = 0.0

    # NHEJ + gH2AX (Eq A4) -- raw units
    if cycle_full:
        dn0 = -n0 * (K1*x1 + P1*y1) + Km1*x2 + Pm1*y2
    else:
        dn0 = -n0 * (K1*x1) + Km1*x2
    dx2  = K1*n0*x1 - x2*(Km1 + K2*x3) + Km2*x4
    dx4  = K2*x2*x3 - x4*(K3 + Km2)
    dx5  = K3*x4 - K4*x5*x5 + Km4*x6
    dx6  = K4*x5*x5 - x6*(K5*x7 + Km4) + Km5*x8
    dx8  = Km6*x10 + K5*x6*x7 - x8*(Km5 + K6*x9)
    dx10 = Km7*x12 + K6*x8*x9 - x10*(Km6 + K7*x11)
    dx12 = K7*x10*x11 - x12*(K8 + Km7)
    dx13 = K8*x12 + P12*y14 + P11*y15 + Q6*z8 + R5*w7
    sum_active = x5 + x6 + x8 + x10 + x12 + y5
    # Eq 25: V_gH2AX+ = K9*[Sum]*[H2AX] / (K10 + [Sum])
    # Eq 27: V_gH2AX- = K11*[dsDNA] + K12*[gH2AX]
    dx14 = K9 * sum_active * x15 / (K10 + sum_active) - K11*x13 - K12*x14

    # HR (Eq A5)
    Pm2 = 0.0
    dy2  = P1*n0*y1 - y2*(Pm1 + P3*y4) + Pm3*y5
    dy4  = P2*y3 - y4*(Pm2 + P3*y2) + y5*(P4 + Pm3) - P2*y4  # add -P2*y4 self-decay to prevent runaway
    # Without the self-decay term y4 grows linearly forever. The paper does not include
    # a clear decay; we add a phenomenological balance so y4 reaches steady state
    # (it equilibrates between P2 production and consumption via P3*y2).
    # Better: just leave dy4 = P2*y3 - y4*(Pm2 + P3*y2) + y5*(P4 + Pm3) and accept it.
    dy4  = P2*y3 - y4*(Pm2 + P3*y2) + y5*(P4 + Pm3)
    dy5  = P3*y2*y4 - y5*(P4 + Pm3)
    dy6  = P4*y5 - y6*(P5*y7 + R1*w1) + Pm5*y8 + Rm1*w2
    dy8  = Pm6*y10 + P5*y6*y7 - y8*(Pm5 + P6*y9c + Q1*z1) + Qm1*z2
    dy10 = P6*y8*y9c - y10*(P7 + Pm6)
    dy11 = P7*y10 - P8*y11*y12 + Pm8*y13
    dy13 = P8*y11*y12 - y13*(P9 + Pm8)
    dy14 = P9*y13 - y14*(P10 + P12)
    dy15 = P10*y14 - P11*y15

    # SSA (Eq A6)
    dz2  = Q1*y8*z1 - z2*(Qm1 + Q2*z2*z2)
    dz3  = Q2*z2*z2 - Q3*z3*z4 + Qm3*z5
    dz5  = Q3*z3*z4 - z5*(Q4 + Qm3)
    dz6  = Q4*z5 - Q5*z6*z7 + Qm5*z8
    dz8  = Q5*z6*z7 - z8*(Q6 + Qm5)

    # Alt-EJ (Eq A7)
    dw2  = R1*w1*y6 - w2*(R2 + Rm1)
    dw4  = R2*w2*w3 - R3*w4
    dw5  = R3*w4 - R4*w5*w6 + Rm4*w7
    dw7  = R4*w5*w6 - w7*(R5 + Rm4)

    du = np.zeros(N_STATES)
    du[IDX['n0']]  = dn0
    du[IDX['x2']]  = dx2
    du[IDX['x4']]  = dx4
    du[IDX['x5']]  = dx5
    du[IDX['x6']]  = dx6
    du[IDX['x8']]  = dx8
    du[IDX['x10']] = dx10
    du[IDX['x12']] = dx12
    du[IDX['x13']] = dx13
    du[IDX['x14']] = dx14
    du[IDX['y2']]  = dy2
    du[IDX['y4']]  = dy4
    du[IDX['y5']]  = dy5
    du[IDX['y6']]  = dy6
    du[IDX['y8']]  = dy8
    du[IDX['y10']] = dy10
    du[IDX['y11']] = dy11
    du[IDX['y13']] = dy13
    du[IDX['y14']] = dy14
    du[IDX['y15']] = dy15
    du[IDX['z2']]  = dz2
    du[IDX['z3']]  = dz3
    du[IDX['z5']]  = dz5
    du[IDX['z6']]  = dz6
    du[IDX['z8']]  = dz8
    du[IDX['w2']]  = dw2
    du[IDX['w4']]  = dw4
    du[IDX['w5']]  = dw5
    du[IDX['w7']]  = dw7
    return du


def run_one_dose(D_Gy, L=LET, t_max=24.0, n_pts=200, cycle_full=True):
    # Initial n0: convert N0 (DSB/cell count) to molar via /(NA*Vnucl)
    N0_count = alpha_of_L(L) * D_Gy * Nirrep(D_Gy) + alpha_of_L(L) * D_Gy * (1 - Nirrep(D_Gy))
    # Actually per Eq.(1) source: dN0/dt = alpha*dD/dt * Nir. The Nir factor only applies
    # to the irreparable subpopulation. For total initial DSBs we use full alpha*D, and the
    # Nirrep factor governs the long-time residual via dose-dependent K10.
    N0_count = alpha_of_L(L) * D_Gy
    n0_M = N0_count / (NA * V_NUCL)
    u0 = np.zeros(N_STATES)
    u0[IDX['n0']] = n0_M
    t_eval = np.linspace(0.0, t_max, n_pts)
    sol = solve_ivp(
        rhs, (0.0, t_max), u0, t_eval=t_eval, args=(D_Gy, cycle_full),
        method='LSODA', rtol=1e-9, atol=1e-18, max_step=0.5,
    )
    if not sol.success:
        raise RuntimeError(f"ODE failed at D={D_Gy} Gy: {sol.message}")
    return sol.t, sol.y, N0_count, n0_M


def to_foci_per_cell(conc_M):
    """Convert molar concentration to count/cell using NA * V_nucl."""
    return conc_M * NA * V_NUCL


def gamma_h2ax_foci(U):
    return to_foci_per_cell(U[IDX['x14'], :])


def rad51_foci(U):
    # Rad51 foci proxy: total post-Rad51-filament HR intermediates
    s = U[IDX['y11'], :] + U[IDX['y13'], :] + U[IDX['y14'], :] + U[IDX['y15'], :]
    return to_foci_per_cell(s)


def main():
    here = Path(__file__).resolve().parent
    root = here.parent
    res_dir = root / "results"
    fig_dir = root / "figures"
    res_dir.mkdir(exist_ok=True)
    fig_dir.mkdir(exist_ok=True)

    t0 = time.time()
    doses_mGy = np.array([20, 40, 80, 160, 250, 500, 1000])
    doses_Gy = doses_mGy / 1000.0
    T_END = 24.0
    N_PTS = 240

    W_CYCLE = 0.55
    W_NO    = 0.45

    h2ax_all = {}
    rad51_all = {}
    t_grid = None

    print("Time-course solves (raw units, v2)...")
    for D_mGy, D_Gy in zip(doses_mGy, doses_Gy):
        t, U_full, N0, n0_M = run_one_dose(D_Gy, t_max=T_END, n_pts=N_PTS, cycle_full=True)
        _, U_red, _, _      = run_one_dose(D_Gy, t_max=T_END, n_pts=N_PTS, cycle_full=False)
        h2ax = W_CYCLE * gamma_h2ax_foci(U_full) + W_NO * gamma_h2ax_foci(U_red)
        rad51 = W_CYCLE * rad51_foci(U_full)
        h2ax_all[D_mGy] = h2ax
        rad51_all[D_mGy] = rad51
        t_grid = t
        peak_h2ax = float(np.max(h2ax))
        t_peak_h2ax = float(t[np.argmax(h2ax)])
        resid_h2ax = float(h2ax[-1])
        peak_r51 = float(np.max(rad51))
        t_peak_r51 = float(t[np.argmax(rad51)])
        resid_r51 = float(rad51[-1])
        print(f"  D={D_mGy:>4} mGy: N0={N0:5.2f} | gH2AX peak={peak_h2ax:7.3f}@t={t_peak_h2ax:.2f}h, 24h={resid_h2ax:7.3f} "
              f"| Rad51 peak={peak_r51:7.3f}@t={t_peak_r51:.2f}h, 24h={resid_r51:7.3f}")

    import csv
    with open(res_dir / "ode_h2ax_kinetics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_h"] + [f"D_{d}_mGy" for d in doses_mGy])
        for i, t in enumerate(t_grid):
            row = [f"{t:.4f}"] + [f"{h2ax_all[d][i]:.5f}" for d in doses_mGy]
            w.writerow(row)
    with open(res_dir / "ode_rad51_kinetics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_h"] + [f"D_{d}_mGy" for d in doses_mGy])
        for i, t in enumerate(t_grid):
            row = [f"{t:.4f}"] + [f"{rad51_all[d][i]:.5f}" for d in doses_mGy]
            w.writerow(row)
    print(f"Wrote h2ax / rad51 kinetics CSVs")

    print("\nPHR(D) sweep...")
    dose_sweep_mGy = np.array([5, 10, 20, 40, 60, 80, 120, 160, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000])
    PHR_vals = []
    means_h2ax = []
    means_r51 = []
    for D_mGy in dose_sweep_mGy:
        D_Gy = D_mGy / 1000.0
        t, U_full, N0, _ = run_one_dose(D_Gy, t_max=T_END, n_pts=N_PTS, cycle_full=True)
        h2ax_t = gamma_h2ax_foci(U_full)
        rad51_t = rad51_foci(U_full)
        mean_h2ax = float(np.trapezoid(h2ax_t, t) / T_END)
        mean_r51  = float(np.trapezoid(rad51_t, t) / T_END)
        if mean_h2ax > 1e-12:
            phr = 100.0 * mean_r51 / mean_h2ax
        else:
            phr = float('nan')
        PHR_vals.append(phr)
        means_h2ax.append(mean_h2ax)
        means_r51.append(mean_r51)
        print(f"  D={D_mGy:>4} mGy: mean(gH2AX)={mean_h2ax:8.4f} mean(Rad51)={mean_r51:8.4f} PHR={phr:8.2f}%")

    with open(res_dir / "ode_PHR_vs_dose.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dose_mGy", "mean_h2ax", "mean_rad51", "PHR_percent"])
        for d, mh, mr, p in zip(dose_sweep_mGy, means_h2ax, means_r51, PHR_vals):
            w.writerow([d, f"{mh:.6f}", f"{mr:.6f}", f"{p:.4f}"])
    print(f"Wrote ode_PHR_vs_dose.csv")

    PHR_arr = np.array(PHR_vals)
    phr_at_20  = float(PHR_arr[np.where(dose_sweep_mGy == 20)[0][0]])
    phr_at_1000 = float(PHR_arr[np.where(dose_sweep_mGy == 1000)[0][0]])
    decreasing = int(np.sum(np.diff(PHR_arr) < 0))
    monotonic_frac = decreasing / max(len(PHR_arr)-1, 1)
    PHR_ratio = phr_at_20 / max(phr_at_1000, 1e-6)

    peak_times = {int(d): float(t_grid[int(np.argmax(h2ax_all[d]))]) for d in doses_mGy}
    peak_shift = (peak_times[1000] <= peak_times[250]) or (peak_times[500] <= peak_times[250])

    residual_frac = {}
    for d in doses_mGy:
        peak = float(np.max(h2ax_all[d]))
        r24  = float(h2ax_all[d][-1])
        residual_frac[int(d)] = (r24 / peak) if peak > 1e-9 else float('nan')

    results = {
        "doses_mGy": doses_mGy.tolist(),
        "h2ax_peak_per_cell": {int(d): float(np.max(h2ax_all[d])) for d in doses_mGy},
        "h2ax_peak_time_h":   {int(d): float(t_grid[int(np.argmax(h2ax_all[d]))]) for d in doses_mGy},
        "h2ax_residual_24h":  {int(d): float(h2ax_all[d][-1]) for d in doses_mGy},
        "rad51_peak_per_cell":{int(d): float(np.max(rad51_all[d])) for d in doses_mGy},
        "rad51_peak_time_h":  {int(d): float(t_grid[int(np.argmax(rad51_all[d]))]) for d in doses_mGy},
        "rad51_residual_24h": {int(d): float(rad51_all[d][-1]) for d in doses_mGy},
        "residual_h2ax_frac_of_peak": residual_frac,
        "PHR_sweep": {
            "dose_mGy": dose_sweep_mGy.tolist(),
            "PHR_percent": [float(p) for p in PHR_vals],
        },
        "PHR_at_20_mGy": phr_at_20,
        "PHR_at_1000_mGy": phr_at_1000,
        "PHR_decrease_ratio_20_over_1000": PHR_ratio,
        "PHR_monotonic_decreasing_fraction": monotonic_frac,
        "peak_timing_shift_present": bool(peak_shift),
        "wall_clock_s": time.time() - t0,
    }
    with open(root / "results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote results.json")
    print(f"Wall: {time.time()-t0:.1f} s")

    if plt is not None:
        fig, axes = plt.subplots(2, 2, figsize=(12, 9))
        for d in [20, 40, 80]:
            axes[0,0].plot(t_grid, h2ax_all[d], label=f"{d} mGy")
        axes[0,0].set_xlabel("Time (h)")
        axes[0,0].set_ylabel("gH2AX foci / cell")
        axes[0,0].set_title("Fig 5 analog (20-80 mGy)")
        axes[0,0].legend(); axes[0,0].grid(alpha=0.3)

        for d in [160, 250, 500, 1000]:
            axes[0,1].plot(t_grid, h2ax_all[d], label=f"{d} mGy")
        axes[0,1].set_xlabel("Time (h)")
        axes[0,1].set_ylabel("gH2AX foci / cell")
        axes[0,1].set_title("Fig 5 analog (160-1000 mGy)")
        axes[0,1].legend(); axes[0,1].grid(alpha=0.3)

        for d in doses_mGy:
            axes[1,0].plot(t_grid, rad51_all[d], label=f"{d} mGy")
        axes[1,0].set_xlabel("Time (h)")
        axes[1,0].set_ylabel("Rad51 foci / cell")
        axes[1,0].set_title("Fig 6 analog (Rad51)")
        axes[1,0].legend(fontsize=8); axes[1,0].grid(alpha=0.3)

        axes[1,1].plot(dose_sweep_mGy, PHR_vals, 'o-', color='C3')
        axes[1,1].set_xlabel("Dose (mGy)")
        axes[1,1].set_ylabel("PHR (%)")
        axes[1,1].set_title("Fig 7 analog: PHR(D)")
        axes[1,1].grid(alpha=0.3)

        fig.suptitle("Belov 2023 CIMB - full ODE replication v2 (raw units)", fontsize=12)
        fig.tight_layout()
        fig.savefig(fig_dir / "ode_full_model.png", dpi=130)
        print(f"Wrote figures/ode_full_model.png")


if __name__ == "__main__":
    main()
