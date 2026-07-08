#!/usr/bin/env python3
"""Plot total DOS comparison with annotations."""
import os, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(os.path.expanduser("~/projects/replicate-1981773"))
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

def load_dos(path):
    data = np.loadtxt(path, comments="#")
    return data[:,0], data[:,1]

def get_fermi(scf_out):
    Ef = 0.0
    if scf_out.exists():
        for line in open(scf_out):
            if "the Fermi energy is" in line:
                try: Ef = float(line.split()[-2])
                except: pass
    return Ef

def get_gap(scf_out):
    """Parse highest occupied and lowest unoccupied from scf with tetrahedra."""
    import re
    nelec = None; kblocks = []; current = []
    with open(scf_out) as f:
        for line in f:
            m = re.search(r"number of electrons\s+=\s+(-?\d+\.\d+)", line)
            if m: nelec = float(m.group(1))
            if re.match(r"\s+k\s*=", line):
                if current: kblocks.append(current); current = []
                continue
            parts = line.split()
            if parts and all(re.match(r"^-?\d+\.\d+$", p) for p in parts):
                try: current.extend(float(p) for p in parts)
                except: pass
        if current: kblocks.append(current)
    if nelec is None or not kblocks: return None, None, None
    nocc = int(round(nelec/2))
    try:
        homo = max(b[nocc-1] for b in kblocks if len(b) >= nocc)
        lumo = min(b[nocc] for b in kblocks if len(b) > nocc)
        return homo, lumo, lumo-homo
    except:
        return None, None, None

fig, axes = plt.subplots(2,1,figsize=(8,7),sharex=True)

for ax, tag, scf_name, title, color in [
    (axes[0], "slab_001", "lto_scf_final.out", "(001) Clean slab", "#1f77b4"),
    (axes[1], "slab_001_Pt", "lto_scf_final.out", "(001) Pt-doped slab", "#d62728"),
]:
    d = ROOT / tag
    dos_file = d / "lto.dos"
    E, D = load_dos(dos_file)
    Ef = get_fermi(d/scf_name)
    homo, lumo, gap = get_gap(d/scf_name)
    
    Es = E - Ef
    ax.fill_between(Es, 0, D, where=(Es<=0), color=color, alpha=0.3)
    ax.plot(Es, D, color=color, lw=1.0)
    ax.axvline(0, color="k", lw=0.7, ls="--", alpha=0.7)
    if homo is not None:
        ax.axvline(homo-Ef, color="green", lw=0.8, ls=":", alpha=0.8, label=f"VBM={homo-Ef:.2f}")
        ax.axvline(lumo-Ef, color="orange", lw=0.8, ls=":", alpha=0.8, label=f"CBM={lumo-Ef:.2f}")
        ax.annotate(f"$E_g$ = {gap:.2f} eV", xy=((homo+lumo)/2-Ef, 5), ha="center",
                     bbox=dict(boxstyle="round", facecolor="lightyellow", edgecolor="gray"),
                     fontsize=10)
    ax.set_title(title, fontsize=11)
    ax.set_ylabel("DOS (states/eV)")
    ax.set_xlim(-8, 5)
    ax.set_ylim(0, max(D[(Es>-8)&(Es<5)])*1.1)
    ax.legend(loc="upper right", fontsize=9)

axes[-1].set_xlabel(r"$E - E_F$ (eV)")
fig.suptitle(r"La$_2$Ti$_2$O$_7$ (001) — total DOS (PBE/SSSP)", fontsize=12)
fig.tight_layout()
fig.savefig(FIG/"dos_comparison.pdf")
fig.savefig(FIG/"dos_comparison.png", dpi=150)
print(f"saved {FIG}/dos_comparison.pdf")

# Also combined overlay
fig2, ax2 = plt.subplots(figsize=(7,4))
for tag, scf, label, color in [
    ("slab_001","lto_scf_final.out","clean (001)","#1f77b4"),
    ("slab_001_Pt","lto_scf_final.out","Pt-doped (001)","#d62728"),
]:
    d = ROOT/tag
    E,D = load_dos(d/"lto.dos")
    Ef = get_fermi(d/scf)
    ax2.plot(E-Ef, D, color=color, lw=1.2, label=label)
ax2.axvline(0, color="k", lw=0.5, ls="--")
ax2.set_xlabel(r"$E - E_F$ (eV)")
ax2.set_ylabel("DOS (states/eV)")
ax2.set_xlim(-8, 5)
ax2.legend(frameon=False)
ax2.set_title("Total DOS: clean vs Pt-doped La$_2$Ti$_2$O$_7$(001)")
fig2.tight_layout()
fig2.savefig(FIG/"dos_overlay.pdf")
fig2.savefig(FIG/"dos_overlay.png", dpi=150)
print(f"saved {FIG}/dos_overlay.pdf")
