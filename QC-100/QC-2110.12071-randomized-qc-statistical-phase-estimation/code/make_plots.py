#!/usr/bin/env python3
"""Plots for the replication report."""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

evd = Path(__file__).resolve().parent.parent / "report" / "evidence"

# --- Plot 1: CDF - analytic vs. estimated -------------------
run = json.load(open(evd / "spe_run.json"))
x = np.array(run["x_grid"])
Ca = np.array(run["C_analytic_real"])
Ce = np.array(run["C_est_real"])
tau = run["tau"]
Egs = run["true_energies"][0]
true_gs_phase = tau * Egs
overlaps = run["overlaps"]
Es = run["true_energies"]

fig, ax = plt.subplots(1, 1, figsize=(8.0, 4.5))
ax.plot(x, Ca, lw=1.5, label="Analytic $\\tilde C(x)$ (Eq. 6, exact $\\langle U_j\\rangle$)")
ax.plot(x, Ce, lw=0.8, alpha=0.7, label=f"Estimated $\\tilde C(x)$ from {run['cfg']['n_samples']} draws"
                                       f" ({run['cfg']['n_hadamard_tests']} Hadamard tests)")
for k, (E, ov) in enumerate(zip(Es, overlaps)):
    x_jump = tau * E
    if ov > 1e-6:
        ax.axvline(x_jump, ls=":", color="grey", alpha=0.6)
        ax.text(x_jump, 1.05, f"$\\tau E_{k}$\n(overlap {ov:.2f})", ha="center", fontsize=8)
ax.axvline(true_gs_phase, ls="-", color="red", alpha=0.8, lw=0.8, label=f"True $\\tau E_{{gs}}$ = {true_gs_phase:.4f}")
ax.set_xlim(-math.pi/2, math.pi/2)
ax.set_xlabel(r"$x$  (rescaled phase, $x = \tau H$)")
ax.set_ylabel(r"$\tilde C(x)$")
ax.set_title("Statistical phase estimation on 2-qubit TFIM (J=1, h=0.5)\n"
             "Wan-Berta-Campbell 2110.12071 approximate CDF, Fourier truncation d=20")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(evd / "fig_cdf.png", dpi=140)
print("wrote", evd / "fig_cdf.png")

# --- Plot 2: sample-complexity scaling (std of C-estimator) --------
scan = json.load(open(evd / "spe_scaling.json"))
study = scan["study"]
n = np.array([s["n_samples"] for s in study])
std_re = np.array([s["std_C_re"] for s in study])
rms_e = np.array([s["rms_energy_err"] for s in study])

# Fit slope to std_re (Hoeffding shot-noise scaling)
logn = np.log10(n); logs = np.log10(std_re)
slope, intercept = np.polyfit(logn, logs, 1)

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
ax1.loglog(n, std_re, "o-", label=f"observed std$[C_{{est}}(x_0)]$")
ax1.loglog(n, 10**intercept * n**slope, "--", color="C1",
           label=f"fit: slope = {slope:+.3f}")
ax1.loglog(n, std_re[0] * (n[0]/n)**0.5, ":", color="grey",
           label=r"paper prediction $\propto N^{-1/2}$")
ax1.set_xlabel("N_samples (Fourier-index draws; each = 2 Hadamard-test shots)")
ax1.set_ylabel(r"std of $\tilde C(x_0)$ estimator")
ax1.set_title("Sample-complexity scaling (shot-noise, paper Eq. 11)")
ax1.legend(fontsize=8); ax1.grid(True, which="both", alpha=0.3)

# Right panel: energy error
mask = np.isfinite(rms_e) & (rms_e > 0) & (rms_e < 0.5)
ax2.loglog(n[mask], rms_e[mask], "o-", color="C2", label="RMS energy error")
if mask.sum() >= 2:
    slope_e, intercept_e = np.polyfit(np.log10(n[mask]), np.log10(rms_e[mask]), 1)
    ax2.loglog(n[mask], 10**intercept_e * n[mask]**slope_e, "--", color="C1",
               label=f"fit: slope = {slope_e:+.3f}")
ax2.set_xlabel("N_samples")
ax2.set_ylabel("RMS |E_est - E_gs| (Hartree, TFIM units)")
ax2.set_title("Downstream ground-state energy error")
ax2.legend(fontsize=8); ax2.grid(True, which="both", alpha=0.3)
fig2.tight_layout()
fig2.savefig(evd / "fig_scaling.png", dpi=140)
print("wrote", evd / "fig_scaling.png")

print(f"\nFitted slope of std[C_est] vs N_samples: {slope:+.3f}  (paper: -0.500)")
print(f"Deviation from -0.5:                     {abs(slope - (-0.5)):.3f}")
