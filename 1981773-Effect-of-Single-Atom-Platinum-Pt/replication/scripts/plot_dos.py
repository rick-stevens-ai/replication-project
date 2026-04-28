#!/usr/bin/env python3
"""Plot total DOS and PDOS for clean and Pt-doped slabs."""
import os, sys, glob
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(os.path.expanduser("~/projects/replicate-1981773"))
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

def load_dos(path):
    # Format: E DOS IntegratedDOS (3 columns, header starts with #)
    data = np.loadtxt(path, comments="#")
    return data[:,0], data[:,1]

def plot_tdos():
    fig, ax = plt.subplots(1,1,figsize=(7,4))
    for tag, color, label in [("slab_001","C0","(001) clean"),
                              ("slab_001_Pt","C3","(001) Pt-doped")]:
        dos_file = ROOT / tag / "lto.dos"
        if not dos_file.exists():
            # try alternate name
            dos_files = list((ROOT/tag).glob("*.dos"))
            if dos_files: dos_file = dos_files[0]
            else: print(f"no dos in {tag}"); continue
        E, D = load_dos(dos_file)
        # Find Fermi from scf output
        scf_out = ROOT / tag / ("slab_scf.out" if tag=="slab_001" else "slab_Pt_scf.out")
        Ef = 0.0
        if scf_out.exists():
            for line in open(scf_out):
                if "Fermi energy" in line:
                    try: Ef = float(line.split()[-2])
                    except: pass
        ax.plot(E-Ef, D, color=color, label=label, lw=1.0)
    ax.set_xlabel(r"$E - E_F$ (eV)")
    ax.set_ylabel("DOS (states/eV)")
    ax.set_xlim(-8, 6)
    ax.axvline(0, color="k", lw=0.5, ls="--")
    ax.legend()
    ax.set_title("La$_2$Ti$_2$O$_7$ (001) — Total DOS: clean vs Pt-doped")
    fig.tight_layout()
    fig.savefig(FIG/"dos_comparison.pdf")
    fig.savefig(FIG/"dos_comparison.png", dpi=150)
    print(f"saved {FIG}/dos_comparison.pdf")

def plot_pdos():
    """Plot PDOS for each species, for both slabs."""
    fig, axes = plt.subplots(2,1,figsize=(8,7),sharex=True)
    for ax, tag, title in zip(axes, ("slab_001","slab_001_Pt"),
                               ("(001) clean","(001) Pt-doped")):
        # Find PDOS files from projwfc: lto.pdos_atm#*(Xx)*
        pdos_files = sorted((ROOT/tag).glob("lto.pdos_atm*"))
        if not pdos_files:
            ax.text(0.5, 0.5, "No PDOS available", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(title); continue
        
        # Get Fermi
        scf_out = ROOT / tag / ("slab_scf.out" if tag=="slab_001" else "slab_Pt_scf.out")
        Ef = 0.0
        if scf_out.exists():
            for line in open(scf_out):
                if "Fermi energy" in line:
                    try: Ef = float(line.split()[-2])
                    except: pass
        
        # Sum by species
        sums = {}
        for f in pdos_files:
            # parse species from filename: lto.pdos_atm#1(La)_wfc#1(s)
            name = f.name
            import re
            m = re.search(r"\(([A-Z][a-z]?)\)_wfc", name)
            if not m: continue
            species = m.group(1)
            data = np.loadtxt(str(f), comments="#")
            if data.ndim == 1: continue
            E = data[:,0]
            # columns: E, pdos_tot, pdos_l=0... — use column 2 (total per wfc)
            tot = data[:,1] if data.shape[1] >= 2 else None
            if species not in sums:
                sums[species] = [E, np.zeros_like(tot)]
            sums[species][1] += tot
        
        colors = {"La":"C2","Ti":"C1","O":"C0","Pt":"C3"}
        for sp, (E, D) in sums.items():
            ax.plot(E-Ef, D, color=colors.get(sp,"k"), label=sp, lw=1.0)
        ax.set_title(title)
        ax.set_ylabel("PDOS (states/eV)")
        ax.axvline(0, color="k", lw=0.5, ls="--")
        ax.legend()
    axes[-1].set_xlabel(r"$E - E_F$ (eV)")
    axes[-1].set_xlim(-8, 6)
    fig.tight_layout()
    fig.savefig(FIG/"pdos_comparison.pdf")
    fig.savefig(FIG/"pdos_comparison.png", dpi=150)
    print(f"saved {FIG}/pdos_comparison.pdf")

if __name__ == "__main__":
    plot_tdos()
    plot_pdos()
