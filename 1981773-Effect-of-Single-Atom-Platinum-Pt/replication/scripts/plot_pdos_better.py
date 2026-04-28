#!/usr/bin/env python3
"""Better PDOS plots: zoomed gap region, orbital resolution."""
import os, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(os.path.expanduser("~/projects/replicate-1981773"))
FIG = ROOT / "figures"

def fermi(path):
    Ef = 0.0
    if Path(path).exists():
        for line in open(path):
            if "the Fermi energy is" in line:
                try: Ef = float(line.split()[-2])
                except: pass
    return Ef

def load_pdos_by_species_orbital(dirpath):
    """Return dict[species][l] = (E, D) summed across all atoms/wfcs of that species-orbital."""
    files = sorted(Path(dirpath).glob("lto.pdos_atm*"))
    L_MAP = {"s":"s", "p":"p", "d":"d", "f":"f"}
    result = {}
    for f in files:
        m = re.search(r"\(([A-Z][a-z]?)\)_wfc#\d+\(([spdf])\)", f.name)
        if not m: continue
        sp, l = m.group(1), m.group(2)
        try:
            d = np.loadtxt(str(f), comments="#")
        except: continue
        if d.ndim != 2: continue
        E = d[:,0]
        tot = d[:,1]  # total ldos for this wfc
        key = (sp, l)
        if key not in result:
            result[key] = [E, np.zeros_like(tot)]
        else:
            # Energy grid should match
            pass
        result[key][1] += tot
    return result

def plot_comparison():
    # Two-panel: clean top, doped bottom; zoomed -6 to +3 eV
    fig, axes = plt.subplots(2,1,figsize=(9,7),sharex=True)
    
    scf_name_map = {"slab_001":"lto_scf_final.out", "slab_001_Pt":"lto_scf_final.out"}
    colors = {"La":"#2ca02c", "Ti":"#ff7f0e", "O":"#1f77b4", "Pt":"#d62728"}
    linestyles = {"s":"-", "p":"-", "d":"-", "f":"--"}
    
    for ax, tag, title in [
        (axes[0], "slab_001", "(001) Clean La$_2$Ti$_2$O$_7$"),
        (axes[1], "slab_001_Pt", "(001) Pt-doped (Ti $\\to$ Pt surface substitution)"),
    ]:
        d = ROOT / tag
        data = load_pdos_by_species_orbital(d)
        Ef = fermi(d / scf_name_map[tag])
        if not data:
            ax.text(0.5,0.5,"no PDOS", ha="center", transform=ax.transAxes); continue
        # Reference energy grid
        ref_E = next(iter(data.values()))[0]
        
        # Total DOS overlay (light gray)
        try:
            dos_data = np.loadtxt(str(d/"lto.dos"), comments="#")
            ax.fill_between(dos_data[:,0]-Ef, 0, dos_data[:,1], color="gray", alpha=0.15, label="total DOS")
        except: pass
        
        # Per species, summing across orbitals
        for sp in ["La","Ti","O","Pt"]:
            # Sum all orbitals for this species
            combined = np.zeros_like(ref_E)
            E = ref_E
            for l in ["s","p","d","f"]:
                k = (sp, l)
                if k in data:
                    E = data[k][0]
                    combined = combined + data[k][1]
            if combined.sum() > 0:
                # Pt signal is small — scale it up if needed
                scale = 1.0
                lbl = sp
                if sp == "Pt":
                    # Scale Pt up for visibility
                    scale = 5.0
                    lbl = f"Pt (×{int(scale)})"
                ax.plot(E - Ef, combined * scale, color=colors.get(sp,"k"),
                        lw=1.4, label=lbl)
        
        ax.axvline(0, color="k", lw=0.7, ls="--", alpha=0.7)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("PDOS (states/eV)")
        ax.set_xlim(-6, 3)
        ax.set_ylim(0, 15)
        ax.legend(loc="upper right", ncol=2, fontsize=9)
    
    axes[-1].set_xlabel(r"$E - E_F$ (eV)")
    fig.suptitle("Species-resolved PDOS (PBE/SSSP; Gaussian $\\sigma$=0.02 eV)", fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG/"pdos_species.pdf")
    fig.savefig(FIG/"pdos_species.png", dpi=150)
    print(f"saved {FIG}/pdos_species.pdf")

    # Gap-region zoom: compare Pt contribution directly
    fig2, ax = plt.subplots(figsize=(8,4.5))
    for tag, label, color in [
        ("slab_001","clean (001)","#1f77b4"),
        ("slab_001_Pt","Pt-doped (001)","#d62728"),
    ]:
        d = ROOT/tag
        dos_data = np.loadtxt(str(d/"lto.dos"), comments="#")
        Ef = fermi(d/scf_name_map[tag])
        ax.plot(dos_data[:,0]-Ef, dos_data[:,1], color=color, lw=1.2, label=f"Total — {label}")
    # Pt contribution alone (doped)
    d = ROOT/"slab_001_Pt"
    data = load_pdos_by_species_orbital(d)
    Ef = fermi(d/scf_name_map["slab_001_Pt"])
    ref_E = next(iter(data.values()))[0]
    pt_tot = np.zeros_like(ref_E)
    pt_d = np.zeros_like(ref_E)
    for l in ["s","p","d","f"]:
        if ("Pt", l) in data:
            pt_tot = pt_tot + data[("Pt", l)][1]
            if l == "d":
                pt_d = data[("Pt", l)][1]
    ax.fill_between(ref_E-Ef, 0, pt_tot*20, color="darkred", alpha=0.6, label=r"Pt total $\times 20$")
    ax.plot(ref_E-Ef, pt_d*20, color="black", lw=1.0, ls=":", label=r"Pt 5$d$ $\times 20$")
    ax.axvline(0, color="k", lw=0.7, ls="--")
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 60)
    ax.set_xlabel(r"$E - E_F$ (eV)")
    ax.set_ylabel("DOS (states/eV)")
    ax.set_title("Gap region zoom: clean vs.\\ Pt-doped with Pt PDOS")
    ax.legend(loc="upper left", fontsize=9)
    fig2.tight_layout()
    fig2.savefig(FIG/"pdos_gap_zoom.pdf")
    fig2.savefig(FIG/"pdos_gap_zoom.png", dpi=150)
    print(f"saved {FIG}/pdos_gap_zoom.pdf")

if __name__ == "__main__":
    plot_comparison()
