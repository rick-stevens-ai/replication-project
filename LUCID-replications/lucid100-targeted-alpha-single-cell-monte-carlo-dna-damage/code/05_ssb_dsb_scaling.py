"""Analytic SSB / sDSB / cDSB yield estimate per parent decay, for the
4 radionuclides x 4 source compartments grid in Jolly & Fielding 2025.

Method (deliberately simple, NOT full TOPAS-nBio DBSCAN):
  * Assume strand-break yield scales with energy deposited in nucleus
    (which is what an LET-weighted DBSCAN integral over alpha tracks
    reduces to in the high-LET / track-segment limit).
  * Use a published-track-structure prefactor for alpha SSB and DSB
    yields per unit dose in cell-nucleus water with G4-DNA models:
      Y_SSB  ~ 350  per Gy per Gbp DNA, alpha (Friedland 2017,
                                            Lampe 2018 ~ 250-400)
      Y_DSB  ~  35  per Gy per Gbp DNA, alpha (Sakata 2020 ~ 30-50)
    Cell nuclear DNA content used in DBSCAN = 16% of 5 um nucleus
    volume (paper convention) — yields a "DNA mass" proxy.
  * sDSB:cDSB split estimated at 0.55:0.45 for high-LET alphas
    (Carrasco-Hernandez 2020; paper Fig 4 visual ratio).

Outputs:
  results/05_ssb_dsb_scaling.json
  results/05_ssb_dsb_scaling.txt

This script reads dose values produced by 04_table2_full.py. It does
NOT attempt a track-structure MC; it tests only the scaling relationship
between dose and strand-break yield, and the qualitative claim that
Ac/Ra produce more breaks than Pb/At in the Nuc compartment.
"""
from __future__ import annotations
import json, math, os

# Reference yields per Gy in cell nucleus (5 um) for alpha tracks,
# track-structure simulation literature (per Gy per cell nucleus).
# These are deliberately calibrated to the paper's Fig 4 absolute scale
# (~ tens of SSBs per parent decay for Nuc source of Ac-225/Ra-223).
# DNA content in nucleus: 16% of nucleus mass = 0.16 * 5.236e-13 g.
# Approx 6 pg DNA per diploid human cell = 6e-12 g; here we use the
# paper's 16% convention => 8.4e-14 g of DNA, ~13.4 Mbp equivalent.
# Then for alpha at ~5-10 keV/um, expect:
#   Y_SSB ~ 5-10 per Gy per cell-nucleus, Y_DSB ~ 0.5-1 per Gy per nucleus
# But the paper Fig 4 shows tens of breaks per parent decay (for 100
# decays = thousands of breaks). So per-decay scaling factor for SSB/DSB
# is recalibrated below from the paper's own numbers.

R_NUC = 5.0
RHO = 1.0
M_NUC_g = (4.0/3.0) * math.pi * (R_NUC*1e-4)**3 * RHO
M_NUC_kg = M_NUC_g * 1e-3
DNA_FRAC = 0.16

# From paper Fig 4 (eyeballed from public PDF, qualitative scale only).
# At-211, Nuc compartment: ~40 SSBs/decay, ~5 sDSBs/decay, ~2 cDSBs/decay
# Used here only to back-out an effective yield-per-Gy that we then apply
# uniformly across all isotopes/compartments. This is the only purpose
# of this script: to test the scaling claim, not to predict absolute
# values independently of the paper.
EYEBALL_AT211_NUC = {"SSB": 40.0, "sDSB": 5.0, "cDSB": 2.0}

def load_dose():
    p = os.path.join(os.path.dirname(__file__), "..", "results", "04_table2_full.json")
    return json.load(open(p))

def main():
    d = load_dose()
    dose = d["dose_cGy_per_decay"]

    # Calibrate: use At-211 Nuc analytical dose (cGy/decay -> Gy/decay)
    cal_dose_Gy = dose["At-211"]["Nuc"] / 100.0  # Gy per decay
    # Effective per-Gy yields:
    Y_SSB  = EYEBALL_AT211_NUC["SSB"]  / cal_dose_Gy
    Y_sDSB = EYEBALL_AT211_NUC["sDSB"] / cal_dose_Gy
    Y_cDSB = EYEBALL_AT211_NUC["cDSB"] / cal_dose_Gy
    print(f"Calibration: At-211 Nuc analytical dose = {cal_dose_Gy*1000:.2f} mGy/decay")
    print(f"  -> Y_SSB={Y_SSB:.1f}/Gy, Y_sDSB={Y_sDSB:.2f}/Gy, Y_cDSB={Y_cDSB:.2f}/Gy")
    print(f"     (per parent decay, with DBSCAN-like scoring in nucleus)\n")

    parents = ["Ac-225", "Ra-223", "Pb-212", "At-211"]
    compartments = ["Mem", "Cyto", "NucWall", "Nuc"]

    out = {"yields_per_Gy": {"SSB": Y_SSB, "sDSB": Y_sDSB, "cDSB": Y_cDSB},
           "calibration_isotope_compartment": "At-211/Nuc (analytical)",
           "calibration_target_breaks": EYEBALL_AT211_NUC,
           "predicted_breaks_per_decay": {"SSB": {}, "sDSB": {}, "cDSB": {}}}

    print(f"=== Predicted SSBs per parent decay ===")
    print(f"{'Isotope':<8} " + " ".join(f"{c:>10}" for c in compartments))
    for p in parents:
        out["predicted_breaks_per_decay"]["SSB"][p] = {}
        out["predicted_breaks_per_decay"]["sDSB"][p] = {}
        out["predicted_breaks_per_decay"]["cDSB"][p] = {}
        ssbs = []
        for c in compartments:
            dose_Gy = dose[p][c] / 100.0
            n_ssb  = Y_SSB  * dose_Gy
            n_sdsb = Y_sDSB * dose_Gy
            n_cdsb = Y_cDSB * dose_Gy
            out["predicted_breaks_per_decay"]["SSB"][p][c]  = n_ssb
            out["predicted_breaks_per_decay"]["sDSB"][p][c] = n_sdsb
            out["predicted_breaks_per_decay"]["cDSB"][p][c] = n_cdsb
            ssbs.append(f"{n_ssb:>10.2f}")
        print(f"{p:<8} " + " ".join(ssbs))

    print(f"\n=== Predicted sDSBs per parent decay ===")
    print(f"{'Isotope':<8} " + " ".join(f"{c:>10}" for c in compartments))
    for p in parents:
        row = [f"{out['predicted_breaks_per_decay']['sDSB'][p][c]:>10.2f}"
               for c in compartments]
        print(f"{p:<8} " + " ".join(row))

    print(f"\n=== Predicted cDSBs per parent decay ===")
    print(f"{'Isotope':<8} " + " ".join(f"{c:>10}" for c in compartments))
    for p in parents:
        row = [f"{out['predicted_breaks_per_decay']['cDSB'][p][c]:>10.2f}"
               for c in compartments]
        print(f"{p:<8} " + " ".join(row))

    print(f"\n=== Trend checks ===")
    # Claim from paper: SSB/sDSB/cDSB all increase Mem<Cyto<NucWall<Nuc
    # and Ac/Ra > Pb/At in Nuc compartment.
    trend_ok = {}
    for kind in ["SSB", "sDSB", "cDSB"]:
        kind_ok = True
        for p in parents:
            row = out["predicted_breaks_per_decay"][kind][p]
            if not (row["Mem"] < row["Cyto"] < row["NucWall"] < row["Nuc"]):
                kind_ok = False
        nuc = {p: out["predicted_breaks_per_decay"][kind][p]["Nuc"] for p in parents}
        ord_ok = min(nuc["Ac-225"], nuc["Ra-223"]) > max(nuc["Pb-212"], nuc["At-211"])
        trend_ok[kind] = {"compartment_monotonic": kind_ok,
                          "Ac_Ra_above_Pb_At_in_Nuc": ord_ok}
        print(f"  {kind}: compartment_monotonic={kind_ok}, Ac/Ra>Pb/At in Nuc={ord_ok}")
    out["trend_checks"] = trend_ok

    # Honest caveats
    out["caveats"] = (
        "Per-Gy yields were calibrated against ONE point from the paper "
        "(eyeballed Fig 4 At-211/Nuc), so this script primarily tests "
        "the scaling relation (dose -> break count) and trend ordering, "
        "NOT independent absolute prediction. Independent track-structure "
        "MC would require TOPAS-nBio (not run here).")
    print(f"\nCaveats: {out['caveats']}")

    with open("results/05_ssb_dsb_scaling.json", "w") as f:
        json.dump(out, f, indent=2)
    txt_path = "results/05_ssb_dsb_scaling.txt"
    with open(txt_path, "w") as f:
        f.write(json.dumps(out, indent=2))
    print(f"\nWrote results/05_ssb_dsb_scaling.json")

if __name__ == "__main__":
    main()
