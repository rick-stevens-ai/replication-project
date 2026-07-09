"""M2: Verify the Bragg-peak location claim from DepthDose.csv supplement.

Paper (Sec 3.1): "The Bragg peak occurred between 32 mm and 33 mm. Thus, in
this study, we selected a PMMA thickness of 32 mm to downscale the energy of
the incident protons."

The MDPI supplement DepthDose.csv lists relative dose vs PMMA thickness for
70 MeV protons. We locate the depth of maximum relative dose and verify it
falls in [32, 33] mm. We also reproduce a depth-dose plot using only the
supplement.
"""
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "data" / "supplement" / "DepthDose.csv"
OUT_JSON = ROOT / "results" / "repass" / "m2_bragg_peak.json"
OUT_FIG = ROOT / "figures" / "repass" / "m2_depth_dose.png"

depths, doses, stds = [], [], []
with SRC.open() as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if not row or not row[0].strip():
            continue
        depths.append(float(row[0]))
        doses.append(float(row[1]))
        stds.append(float(row[2]) if row[2].strip() else 0.0)

depths = np.array(depths)
doses = np.array(doses)
stds = np.array(stds)

idx_peak = int(np.argmax(doses))
peak_depth = float(depths[idx_peak])

# Window of peak: depth where dose >= 95% of max
peak_dose = float(doses[idx_peak])
mask = doses >= 0.95 * peak_dose
window_lo = float(depths[mask].min())
window_hi = float(depths[mask].max())

# Paper's range
in_paper_range = 32.0 <= peak_depth <= 33.0

# Plot
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.errorbar(depths, doses, yerr=stds, fmt="o-", color="C0",
            ms=4, lw=1.2, capsize=2, label="MDPI supplement (measured)")
ax.axvline(32.0, ls="--", color="C3", alpha=0.6, label="32 mm (paper's choice)")
ax.axvline(33.0, ls=":", color="C3", alpha=0.6, label="33 mm (paper's upper bound)")
ax.axvline(peak_depth, ls="-.", color="C2", alpha=0.7,
           label=f"Argmax @ {peak_depth:g} mm")
ax.set_xlabel("PMMA thickness [mm]")
ax.set_ylabel("Relative dose (scaled at 0 mm)")
ax.set_title("70 MeV proton depth-dose in PMMA (paper's Fig 2)")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_FIG, dpi=150)
plt.close(fig)

out = {
    "claim_M2_bragg_peak_in_32_33_mm": {
        "argmax_depth_mm": peak_depth,
        "peak_relative_dose": peak_dose,
        "ninety_five_percent_window_mm": [window_lo, window_hi],
        "paper_claim_range_mm": [32.0, 33.0],
        "argmax_in_paper_range": in_paper_range,
        "n_depth_points": int(len(depths)),
        "source_csv": str(SRC.relative_to(ROOT)),
        "figure": str(OUT_FIG.relative_to(ROOT)),
    }
}
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
