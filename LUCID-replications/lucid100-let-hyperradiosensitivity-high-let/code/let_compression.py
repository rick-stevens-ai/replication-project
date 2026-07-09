#!/usr/bin/env python3
"""
let_compression.py — Exploratory analysis of the paper's central claim:
"progressive compression of hyper-radiosensitivity and induced radioresistance
with increasing LET", where the characteristic HRS-IRR transition (D_c) shifts
toward an initial steep decline without recovery.

We map IR-model parameters (alpha_s/alpha_r ratio, D_c) against approximate
LET (from the irradiation descriptor strings) for high-LET datasets in the
Polgár 2022 STOREDB v2 cohort, plus a "low-LET reference" group of photons
(X-ray/gamma) fitted equivalently.

Outputs:
  figures/let_vs_HRS_shape.png
  results/let_table.csv
"""
from __future__ import annotations
import csv, re
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
FITS = ROOT / "results" / "fits.csv"
OUT_TABLE = ROOT / "results" / "let_table.csv"
FIG = ROOT / "figures" / "let_vs_HRS_shape.png"


def parse_let_keV_per_um(irr: str):
    """Extract LET in keV/um from the irradiation string. Return None if unknown."""
    if not irr:
        return None
    s = irr.replace("μ", "u")
    # Direct 'LET = NNN keV/um'
    m = re.search(r"LET\s*=\s*([0-9]+\.?[0-9]*)\s*keV/?u?m?", s, re.I)
    if m:
        return float(m.group(1))
    # 'NNN keV/um' standalone
    m = re.search(r"([0-9]+\.?[0-9]*)\s*keV/?u?m?", s, re.I)
    if m:
        return float(m.group(1))
    return None


def classify_low_LET(irr: str) -> bool:
    if not irr:
        return False
    s = irr.lower()
    return any(k in s for k in ["x-ray", "kvp", "kev x", "gamma", "γ-ray", "γ ray",
                                "γrays", "6 mv", "60co", "co60", "cobalt"])


def main():
    rows = list(csv.DictReader(FITS.open()))
    out = []
    for r in rows:
        irr = r.get("irradiation", "") or ""
        ar = r.get("ir_alpha_r_fit"); aS = r.get("ir_alpha_s_fit"); dc = r.get("ir_dc_fit")
        if not (ar and aS and dc):
            continue
        try:
            ar = float(ar); aS = float(aS); dc = float(dc)
        except Exception:
            continue
        let = parse_let_keV_per_um(irr)
        low_let = classify_low_LET(irr)
        if not (let is not None or low_let):
            continue
        ratio = aS / ar if ar > 1e-9 else float("inf")
        out.append({
            "id": r["id"],
            "cell_line": r.get("cell_line", ""),
            "irradiation": irr,
            "LET_keV_per_um": let,
            "is_low_LET_photon": low_let,
            "ir_alpha_r": ar,
            "ir_alpha_s": aS,
            "ir_dc": dc,
            "alpha_s_over_r": ratio,
        })

    with OUT_TABLE.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)

    # Build arrays for plotting
    low = [r for r in out if r["is_low_LET_photon"] and r["LET_keV_per_um"] is None]
    high = [r for r in out if r["LET_keV_per_um"] is not None]

    # Assign a nominal LET of ~2 keV/um for photons (median for kV x-rays / MV photons).
    NOMINAL_PHOTON_LET = 2.0
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: D_c vs LET
    if low:
        axL.scatter([NOMINAL_PHOTON_LET] * len(low),
                    [r["ir_dc"] for r in low],
                    s=30, alpha=0.5, color="C0",
                    label=f"low-LET photons (n={len(low)}, plotted @ ~2 keV/μm)")
    if high:
        axL.scatter([r["LET_keV_per_um"] for r in high],
                    [r["ir_dc"] for r in high],
                    s=60, color="C3", marker="^",
                    label=f"high-LET (n={len(high)})")
    axL.set_xscale("log")
    axL.set_xlabel("LET [keV/μm]  (photons placed at nominal 2 keV/μm)")
    axL.set_ylabel(r"IR transition dose $D_c$ [Gy]")
    axL.set_title(r"HRS-IRR transition $D_c$ vs LET")
    axL.legend(fontsize=8)
    axL.grid(True, which="both", alpha=0.3)

    # Right: alpha_s/alpha_r vs LET
    if low:
        axL2 = axR
        ys = [min(r["alpha_s_over_r"], 50) for r in low]
        axL2.scatter([NOMINAL_PHOTON_LET] * len(low), ys, s=30, alpha=0.5, color="C0",
                     label=f"low-LET photons (n={len(low)})")
    if high:
        ys = [min(r["alpha_s_over_r"], 50) for r in high]
        axR.scatter([r["LET_keV_per_um"] for r in high], ys, s=60, color="C3", marker="^",
                    label=f"high-LET (n={len(high)})")
    axR.set_xscale("log")
    axR.set_xlabel("LET [keV/μm]")
    axR.set_ylabel(r"$\alpha_s / \alpha_r$  (HRS amplitude, clipped at 50)")
    axR.set_title("HRS amplitude vs LET")
    axR.legend(fontsize=8)
    axR.grid(True, which="both", alpha=0.3)

    fig.suptitle("Exploratory: how do IR-model HRS signatures change with LET?\n"
                 "(Polgár 2022 STOREDB v2; LET extracted heuristically from irradiation strings)",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(FIG, dpi=140)
    plt.close(fig)

    print(f"low-LET photon rows: {len(low)}")
    print(f"high-LET rows with parsed LET: {len(high)}")
    print(f"Wrote {OUT_TABLE.relative_to(ROOT)} and {FIG.relative_to(ROOT)}")

    # Tiny qualitative summary
    if low and high:
        med_dc_lo = float(np.median([r["ir_dc"] for r in low]))
        med_dc_hi = float(np.median([r["ir_dc"] for r in high]))
        med_ratio_lo = float(np.median([r["alpha_s_over_r"] for r in low]))
        med_ratio_hi = float(np.median([r["alpha_s_over_r"] for r in high]))
        print(f"\nMedian D_c   low-LET={med_dc_lo:.3f} Gy   high-LET={med_dc_hi:.3f} Gy")
        print(f"Median αs/αr low-LET={med_ratio_lo:.2f}     high-LET={med_ratio_hi:.2f}")
        print("(Direction-of-effect only; the curated dataset is heavily photon-skewed,")
        print(" so this is exploratory not statistically definitive.)")


if __name__ == "__main__":
    main()
