#!/usr/bin/env python3
"""Plot dose-response of MEDRAS smoke: initial vs misrepaired DSBs for Z=0 (β surrogate)
and Z=2 (α chain surrogate). Output: figures/smoke_doseresponse.png
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
csv_path = HERE.parent / "results" / "medras_smoke_summary.csv"
out_png = HERE.parent / "figures" / "smoke_doseresponse.png"

doses = {0: [], 2: []}
init = {0: [], 2: []}
misrep = {0: [], 2: []}
with csv_path.open() as f:
    rdr = csv.DictReader(f)
    for row in rdr:
        Z = int(row["Z"])
        d = float(row["dose_Gy"])
        doses[Z].append(d)
        init[Z].append(float(row["mean_init_DSB"]))
        misrep[Z].append(float(row["mean_misrep_DSB"]))

fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
for Z, label, color in [(0, "Z=0 (¹⁷⁷Lu β⁻ surrogate)", "tab:blue"),
                         (2, "Z=2 (²²⁵Ac α chain proxy)", "tab:red")]:
    d = np.array(doses[Z]); i = np.array(init[Z]); m = np.array(misrep[Z])
    order = np.argsort(d)
    ax[0].plot(d[order], i[order], "o-", color=color, label=label)
    ax[1].plot(d[order], m[order], "o-", color=color, label=label)
    # fit through origin
    b_init = float(np.dot(d, i) / np.dot(d, d))
    b_mis  = float(np.dot(d, m) / np.dot(d, d))
    ax[0].plot(d[order], b_init * d[order], "--", color=color, alpha=0.5,
               label=f"  slope = {b_init:.1f} DSB/Gy")
    ax[1].plot(d[order], b_mis * d[order], "--", color=color, alpha=0.5,
               label=f"  slope = {b_mis:.2f} DSB/Gy")

ax[0].set_xlabel("Dose to nucleus [Gy]"); ax[0].set_ylabel("Mean initial DSBs")
ax[0].set_title("Initial DSB yield (MEDRAS smoke)")
ax[1].set_xlabel("Dose to nucleus [Gy]"); ax[1].set_ylabel("Mean misrepaired DSBs (24 h)")
ax[1].set_title("Misrepaired DSBs after MEDRAS Fidelity 24h")
for a in ax:
    a.grid(alpha=0.3); a.legend(fontsize=8, loc="upper left")
fig.suptitle("MEDRAS-MC smoke replication — α (Z=2) vs β⁻ (Z=0) for Rumiantcev 2023", fontsize=11)
fig.tight_layout()
fig.savefig(out_png, dpi=130)
print(f"wrote {out_png}")
