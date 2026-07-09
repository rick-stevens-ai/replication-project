"""Convergence plot: log-log err vs tau, with reference slope-2 line."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open(os.path.join(os.path.dirname(__file__), "convergence_results.json")) as f:
    R = json.load(f)

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
# left: L2 for all four problems
for key, marker, label in [
    ("cubic_NLS_defocusing", "o", "cubic NLS (defoc.)"),
    ("cubic_NLS_focusing",   "s", "cubic NLS (foc.)"),
    ("SP_plus",              "^", "SP (+|psi|^2)"),
    ("SP_minus",             "v", "SP (-|psi|^2)"),
]:
    d = R[key]
    axs[0].loglog(d["taus"], d["err_L2"], marker + "-", label=label)
axs[0].loglog([0.02, 0.00125], [1e-5 * (0.02/0.02)**2, 1e-5 * (0.00125/0.02)**2],
              "k--", lw=1.0, label="slope 2 (reference)")
axs[0].set_xlabel(r"step size $\tau$")
axs[0].set_ylabel(r"$\|\psi_n - \psi_{\mathrm{ref}}\|_{L^2}$")
axs[0].set_title(r"$L^2$ convergence (Theorems 2.1 & 7.1: expect $O(\tau^2)$)")
axs[0].grid(True, which="both", ls=":", alpha=0.5)
axs[0].legend(fontsize=9)

# right: Hm for all four
for key, marker, label in [
    ("cubic_NLS_defocusing", "o", "cubic NLS (defoc.), H^2"),
    ("cubic_NLS_focusing",   "s", "cubic NLS (foc.), H^2"),
    ("SP_plus",              "^", "SP (+|psi|^2), H^1"),
    ("SP_minus",             "v", "SP (-|psi|^2), H^1"),
]:
    d = R[key]
    axs[1].loglog(d["taus"], d["err_Hm"], marker + "-", label=label)
axs[1].loglog([0.02, 0.00125], [1e-4 * (0.02/0.02)**1, 1e-4 * (0.00125/0.02)**1],
              "k:",  lw=1.0, label="slope 1 (theorem bound)")
axs[1].loglog([0.02, 0.00125], [1e-4 * (0.02/0.02)**2, 1e-4 * (0.00125/0.02)**2],
              "k--", lw=1.0, label="slope 2 (observed)")
axs[1].set_xlabel(r"step size $\tau$")
axs[1].set_ylabel(r"$\|\psi_n - \psi_{\mathrm{ref}}\|_{H^m}$")
axs[1].set_title(r"$H^m$ convergence (theorem: $O(\tau)$; observed: $O(\tau^2)$)")
axs[1].grid(True, which="both", ls=":", alpha=0.5)
axs[1].legend(fontsize=9)

fig.suptitle("Lubich (2008) — Strang splitting for NLS / Schrödinger-Poisson: numerical verification",
             fontsize=13)
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "convergence_plot.png")
fig.savefig(out, dpi=120)
print(f"wrote {out}")
