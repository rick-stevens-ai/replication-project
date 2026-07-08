#!/usr/bin/env python3
"""Plot Fig-1 replica: H2 dissociation curve (VQE-compact vs FCI + inset error)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RES = REPO / "results"
data = json.loads((RES / "h2_curve.json").read_text())
curve = data["curve"]

R = np.array([p["R_angstrom"] for p in curve])
E_fci = np.array([p["fci_energy_pyscf"] for p in curve])
E_vqe = np.array([p["vqe_compact_energy"] for p in curve])
E_hf = np.array([p["hf_energy"] for p in curve])
err_mha = np.array([p["err_vs_fci_mha"] for p in curve])

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=150)
ax.plot(R, E_hf, "k--", label="Hartree-Fock", lw=1)
ax.plot(R, E_fci, "b-", label="FCI (PySCF)", lw=1.8)
ax.plot(R, E_vqe, "ro", label="VQE — compact 2e ansatz (this work)",
        ms=5, mfc="none", mew=1.5)
ax.set_xlabel("H-H distance (Å)")
ax.set_ylabel("Energy (hartree)")
ax.set_title("H$_2$ / STO-3G dissociation curve — replication of Smart & Mazziotti (2020)")
ax.grid(alpha=0.3)
ax.legend(loc="lower right", frameon=True)

# Inset with |error| (mHa) vs R, log scale, and a chemical-accuracy line
axi = ax.inset_axes([0.14, 0.52, 0.35, 0.36])
axi.semilogy(R, np.abs(err_mha) + 1e-15, "ro-", ms=3)
axi.axhline(1.6, color="k", ls=":", lw=1)
axi.text(1.5, 2.5, "chem. acc. 1.6 mHa", fontsize=7)
axi.set_xlabel("R (Å)", fontsize=8)
axi.set_ylabel("|E$_{VQE}$−E$_{FCI}$| (mHa)", fontsize=8)
axi.tick_params(labelsize=7)
axi.grid(alpha=0.3, which="both")

plt.tight_layout()
outpath = RES / "h2_dissociation_curve.png"
plt.savefig(outpath, bbox_inches="tight")
print("Wrote", outpath)
