#!/usr/bin/env python3
"""Plot F and chi vs epsN for each N, and log-ratio |chi/F| vs epsN,
to visualize the XEB->fidelity discrepancy that grows at large epsN
(the sharp phase transition of Ware et al 2305.04954, in its finite-size manifestation)."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results" / "xeb_sweep.json"
OUT_DIR = RESULTS.parent
data = json.loads(RESULTS.read_text())
recs = data["records"]

by_n = {}
for r in recs:
    by_n.setdefault(r["n"], []).append(r)
for n in by_n:
    by_n[n].sort(key=lambda r: r["eps"])

# --- Plot 1: F and chi vs epsN, per N ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
colors = plt.get_cmap("viridis")(np.linspace(0.15, 0.85, len(by_n)))
for c, (n, rows) in zip(colors, sorted(by_n.items())):
    x = np.array([r["epsN"] for r in rows])
    F = np.array([r["F_mean"] for r in rows])
    chi = np.array([r["chi_mean"] for r in rows])
    axes[0].plot(x, F, "o-", color=c, label=f"F, N={n}")
    axes[0].plot(x, chi, "s--", color=c, alpha=0.7, label=f"chi, N={n}")
    axes[1].plot(x, chi / np.clip(F, 1e-12, None), "o-", color=c, label=f"N={n}")
axes[0].axvline(np.log(5 / 2), color="red", ls=":", label=r"$\varepsilon N_c=\ln(5/2)\approx 0.916$")
axes[0].set_xlabel(r"$\varepsilon N$")
axes[0].set_ylabel("value")
axes[0].set_yscale("log")
axes[0].set_title("Fidelity F (o) and Linear XEB chi (s) vs epsN, d=8")
axes[0].legend(fontsize=8, ncol=2)
axes[0].grid(True, which="both", alpha=0.3)
axes[1].axvline(np.log(5 / 2), color="red", ls=":", label=r"$\varepsilon N_c=\ln(5/2)$")
axes[1].axhline(1.0, color="gray", ls="-", alpha=0.5, label="chi=F")
axes[1].set_xlabel(r"$\varepsilon N$")
axes[1].set_ylabel(r"$\chi / F$")
axes[1].set_yscale("log")
axes[1].set_title("XEB / Fidelity ratio (deviation from 1 = breakdown)")
axes[1].legend(fontsize=9)
axes[1].grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT_DIR / "fig_F_and_chi_vs_epsN.png", dpi=140)
plt.close(fig)

# --- Plot 2: log(chi) vs epsN with GWN prediction ---
fig, ax = plt.subplots(figsize=(7, 5))
for c, (n, rows) in zip(colors, sorted(by_n.items())):
    x = np.array([r["epsN"] for r in rows])
    chi = np.array([r["chi_mean"] for r in rows])
    F = np.array([r["F_mean"] for r in rows])
    ax.plot(x, np.log(np.clip(chi, 1e-6, None)), "s-", color=c, label=f"log chi, N={n}")
    ax.plot(x, np.log(np.clip(F, 1e-6, None)), "o:", color=c, alpha=0.6, label=f"log F, N={n}")
ax.axvline(np.log(5 / 2), color="red", ls=":", label=r"$\ln(5/2)\approx 0.916$")
ax.set_xlabel(r"$\varepsilon N$")
ax.set_ylabel(r"$\ln$ value")
ax.set_title("Log-XEB and log-F vs epsN; XEB flattens above transition")
ax.legend(fontsize=8, ncol=2)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT_DIR / "fig_log_chi_vs_epsN.png", dpi=140)
plt.close(fig)

print("Wrote:")
for f in sorted(OUT_DIR.glob("*.png")):
    print(f" - {f}")
