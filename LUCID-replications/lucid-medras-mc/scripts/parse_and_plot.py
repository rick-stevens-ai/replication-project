"""
Step 3: Parse the Medras-MC Fidelity log and produce three plots that map
onto specific claims in McMahon & Prise (2021):

  (1) Misrepair fraction vs LET           — main mechanism behind RBE (Fig 5 context)
  (2) Residual-DSB kinetics vs time        — DNA repair kinetics (Fig 2 context)
  (3) Misrepair vs delivered dose (X-ray)  — Fig 3A context (DSB misrejoining vs dose)

We also dump a tidy CSV for downstream use and print summary stats.
"""

import os
import re
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.normpath(os.path.join(HERE, "..", "logs", "02_repair_fidelity.log"))
OUT = os.path.normpath(os.path.join(HERE, "..", "results"))
FIG = os.path.normpath(os.path.join(HERE, "..", "figures"))
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

# Match: filename, Z=N, energy MeV, dose Gy
FN_RX = re.compile(r"DNA Damage Z=(\d+) ([0-9.]+) MeV ([0-9.]+) Gy")

# Map (Z, energy_MeV) -> (LET keV/um, label, particle) for the conditions used
# in damagegenerator.damageModel.basicXandIon(). For photons, LET is set to ~0.
COND = {
    # photons: vary dose only, LET ≈ 2 keV/um (200 kVp/Co-60 surrogate; not used by code)
    (0, "1.0"): {"LET": 2.0, "particle": "Photon (Z=0)"},
    # protons: from damageModel.basicXandIon()
    (1, "0.975"): {"LET": 29.78, "particle": "Proton (Z=1)"},
    (1, "1.175"): {"LET": 25.27, "particle": "Proton (Z=1)"},
    (1, "1.5"):   {"LET": 20.59, "particle": "Proton (Z=1)"},
    (1, "1.8"):   {"LET": 17.78, "particle": "Proton (Z=1)"},
    (1, "2.2"):   {"LET": 15.19, "particle": "Proton (Z=1)"},
    (1, "2.5"):   {"LET": 13.72, "particle": "Proton (Z=1)"},
    (1, "3.5"):   {"LET": 10.60, "particle": "Proton (Z=1)"},
    (1, "5.5"):   {"LET":  7.42, "particle": "Proton (Z=1)"},
    (1, "8.5"):   {"LET":  5.25, "particle": "Proton (Z=1)"},
    (1, "34"):    {"LET":  1.77, "particle": "Proton (Z=1)"},
    # carbon ions
    (6, "24"):   {"LET": 512.0,  "particle": "Carbon (Z=6)"},
    (6, "60"):   {"LET": 265.0,  "particle": "Carbon (Z=6)"},
    (6, "120"):  {"LET": 151.95, "particle": "Carbon (Z=6)"},
    (6, "185"):  {"LET": 100.0,  "particle": "Carbon (Z=6)"},
    (6, "360"):  {"LET":  60.0,  "particle": "Carbon (Z=6)"},
    (6, "960"):  {"LET":  26.0,  "particle": "Carbon (Z=6)"},
    (6, "1200"): {"LET":  20.29, "particle": "Carbon (Z=6)"},
}

# Parse log
records = []
with open(LOG) as fh:
    for line in fh:
        if "\tSummary\t" not in line:
            continue
        parts = line.rstrip("\n").split("\t")
        # parts: [filename, 'Summary', totalBreaks, complexity, avgBreaks,
        #         breakStdev, avgMisrep, misrepStdev, avgInterChrom, '', filename,
        #         '1', kin0, kin1, ...]
        fname = parts[0]
        m = FN_RX.search(fname)
        if not m:
            print("skip:", fname)
            continue
        Z = int(m.group(1))
        energy = m.group(2)
        dose_gy = float(m.group(3))

        total_breaks = float(parts[2])
        complexity = float(parts[3])
        avg_breaks = float(parts[4])
        break_stdev = float(parts[5])
        avg_misrep = float(parts[6])
        misrep_stdev = float(parts[7])
        avg_interchrom = float(parts[8])

        # kinetics block: after first 9 cols there's an empty col, then
        # filename, exposure-index '1', then floats at 0.1 h intervals.
        kin_start = None
        for i, v in enumerate(parts[9:], start=9):
            if v == "1" and parts[i - 1].endswith(".txt"):
                kin_start = i + 1
                break
        if kin_start is None:
            kinetics = []
        else:
            kinetics = []
            for v in parts[kin_start:]:
                if v == "":
                    continue
                try:
                    kinetics.append(float(v))
                except ValueError:
                    break

        key = (Z, energy)
        cond = COND.get(key, {"LET": float("nan"), "particle": f"Z={Z}"})
        records.append({
            "file": fname,
            "Z": Z,
            "energy_MeV": float(energy),
            "dose_Gy": dose_gy,
            "LET_keV_per_um": cond["LET"],
            "particle": cond["particle"],
            "total_breaks": total_breaks,
            "complexity_frac": complexity,
            "avg_breaks_per_exposure": avg_breaks,
            "break_stdev": break_stdev,
            "avg_misrepair_frac": avg_misrep,
            "misrep_stdev": misrep_stdev,
            "avg_interchrom_frac": avg_interchrom,
            "kinetics_per_break": kinetics,  # foci/residual breaks normalized to t=0
        })

# Write tidy CSV (summary only)
csv_path = os.path.join(OUT, "fidelity_summary.csv")
with open(csv_path, "w", newline="") as fh:
    cols = ["file", "Z", "energy_MeV", "dose_Gy", "LET_keV_per_um", "particle",
            "total_breaks", "complexity_frac", "avg_breaks_per_exposure",
            "break_stdev", "avg_misrepair_frac", "misrep_stdev",
            "avg_interchrom_frac"]
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in records:
        w.writerow({k: r[k] for k in cols})
print(f"Wrote {csv_path}  ({len(records)} rows)")

# ---------- Plot 1: misrepair fraction vs LET ----------
fig, ax = plt.subplots(figsize=(7, 5))
groups = {}
for r in records:
    groups.setdefault(r["particle"], []).append(r)

markers = {"Photon (Z=0)": ("ko", "X-rays / photons"),
           "Proton (Z=1)": ("bs", "Protons"),
           "Carbon (Z=6)": ("r^", "Carbon ions")}
for ptcl, rows in groups.items():
    if ptcl == "Photon (Z=0)":
        # average across doses to get a single point
        ms = np.mean([r["avg_misrepair_frac"] for r in rows])
        ss = np.std([r["avg_misrepair_frac"] for r in rows])
        ax.errorbar([rows[0]["LET_keV_per_um"]], [ms], yerr=[ss],
                    fmt=markers[ptcl][0], label=markers[ptcl][1], markersize=10)
        continue
    lets = np.array([r["LET_keV_per_um"] for r in rows])
    ms = np.array([r["avg_misrepair_frac"] for r in rows])
    order = np.argsort(lets)
    ax.plot(lets[order], ms[order], markers[ptcl][0] + "-",
            label=markers[ptcl][1], markersize=8, alpha=0.85)

ax.set_xscale("log")
ax.set_xlabel("LET (keV / μm)")
ax.set_ylabel("Mean misrepair fraction per DSB")
ax.set_title("Medras-MC misrepair vs LET (1 Gy, repeats=50, n=20 exposures/condition)\n"
             "Reproducing the central RBE mechanism of McMahon & Prise 2021")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig1_path = os.path.join(FIG, "misrepair_vs_LET.png")
fig.savefig(fig1_path, dpi=140)
print(f"Wrote {fig1_path}")

# ---------- Plot 2: residual-DSB kinetics ----------
fig, ax = plt.subplots(figsize=(7, 5))
t = None
plotted = 0
for r in records:
    if not r["kinetics_per_break"]:
        continue
    k = np.array(r["kinetics_per_break"])
    t = np.arange(len(k)) * 0.1  # 0.1 h step

    # Plot one representative per particle type, plus all X-ray doses
    if r["particle"] == "Photon (Z=0)":
        ax.plot(t, k, "-", alpha=0.5,
                label=f"X-ray {r['dose_Gy']:.0f} Gy" if r["dose_Gy"] in (1, 4, 8) else None,
                color="black", lw=1.0 + 0.4 * r["dose_Gy"] / 8)
        plotted += 1
    elif r["particle"] == "Proton (Z=1)" and abs(r["LET_keV_per_um"] - 20.59) < 0.1:
        ax.plot(t, k, "b-", label="Proton 20.6 keV/μm, 1 Gy", lw=1.8)
        plotted += 1
    elif r["particle"] == "Carbon (Z=6)" and abs(r["LET_keV_per_um"] - 151.95) < 0.1:
        ax.plot(t, k, "r-", label="Carbon 152 keV/μm, 1 Gy", lw=1.8)
        plotted += 1

ax.set_xlabel("Time after exposure (h)")
ax.set_ylabel("Residual breaks / N$_0$  (foci-equivalent)")
ax.set_title("Medras-MC repair kinetics (γH2AX-like foci with foci-delay on)")
ax.set_yscale("log")
ax.set_ylim(0.03, 1.05)
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig2_path = os.path.join(FIG, "repair_kinetics.png")
fig.savefig(fig2_path, dpi=140)
print(f"Wrote {fig2_path}  (plotted {plotted} curves)")

# ---------- Plot 3: misrepair vs dose (X-ray only) ----------
fig, ax = plt.subplots(figsize=(7, 5))
xray = [r for r in records if r["particle"] == "Photon (Z=0)"]
xray.sort(key=lambda r: r["dose_Gy"])
ds = np.array([r["dose_Gy"] for r in xray])
ms = np.array([r["avg_misrepair_frac"] for r in xray])
ss = np.array([r["misrep_stdev"] for r in xray])
ax.errorbar(ds, ms, yerr=ss, fmt="ko-", capsize=4, label="Medras-MC")
# Linear-like trend (η'·N) reference using N=35 DSB/Gy
ax.set_xlabel("Dose (Gy, X-rays)")
ax.set_ylabel("Mean misrepair fraction per DSB")
ax.set_title("Medras-MC misrepair vs X-ray dose (Fig 3A analog)\n"
             "n=20 exposures × 50 repeats per dose")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig3_path = os.path.join(FIG, "misrepair_vs_dose_xray.png")
fig.savefig(fig3_path, dpi=140)
print(f"Wrote {fig3_path}")

# ---------- Print summary stats ----------
print("\n--- Quantitative summary ---")
print(f"{'Particle':<15} {'LET(keV/μm)':>12} {'Dose(Gy)':>10} "
      f"{'avg DSB':>9} {'complex':>9} {'misrep':>8} {'inter-chrom':>12}")
for r in sorted(records, key=lambda r: (r["Z"], r["LET_keV_per_um"], r["dose_Gy"])):
    print(f"{r['particle']:<15} {r['LET_keV_per_um']:>12.2f} {r['dose_Gy']:>10.1f} "
          f"{r['avg_breaks_per_exposure']:>9.1f} {r['complexity_frac']:>9.3f} "
          f"{r['avg_misrepair_frac']:>8.4f} {r['avg_interchrom_frac']:>12.4f}")

# Quick benchmark vs paper values
xray_1gy = [r for r in records if r["Z"] == 0 and r["dose_Gy"] == 1.0]
if xray_1gy:
    r = xray_1gy[0]
    print(f"\nBenchmark — X-ray 1 Gy:")
    print(f"  Avg DSBs per exposure : {r['avg_breaks_per_exposure']:.1f}   (paper: 35 DSB/Gy)")
    print(f"  Complex fraction       : {r['complexity_frac']:.3f}  (paper: 0.43 ± 0.02)")
    print(f"  Misrepair fraction     : {r['avg_misrepair_frac']:.4f}")
