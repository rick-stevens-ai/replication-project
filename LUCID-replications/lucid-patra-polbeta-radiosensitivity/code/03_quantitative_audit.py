#!/usr/bin/env python3
"""
Internal-consistency audit of all quantitative claims in Patra et al. 2022.

We extract every numeric assertion from the paper text (verbatim quotes) and:
  1) Check internal arithmetic where possible.
  2) Check internal consistency between text, figures, and supplements.
  3) Flag anything that looks anomalous.

Outputs:
  results/quant_audit.json
  results/quant_audit.txt
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES  = ROOT / "results"; RES.mkdir(exist_ok=True)

audit = {}

# -------- ROS generation (Fig 5) --------
# Paper text:
#  "In the case of PA1 cells, the mean fluorescence was increased over non-treated
#   cells (control) by 169.0% ± 8.2%, and 191.9% ± 11.5% for 5 Gy, and 10 Gy of
#   γ-radiation, respectively."
#  "The PA1PolβΔ cells showed 173.7% ± 13.4% increase in mean fluorescence intensity
#   over respective control cells at 5 Gy and 134.5% ± 9.1% at 10 Gy."
audit["ROS_Fig5"] = {
    "PA1": {"5Gy_pct_over_ctrl": [169.0, 8.2], "10Gy_pct_over_ctrl": [191.9, 11.5]},
    "PA1PolBetaDelta": {"5Gy_pct_over_ctrl": [173.7, 13.4], "10Gy_pct_over_ctrl": [134.5, 9.1]},
    "internal_consistency_note": (
        "Reported PA1PolβΔ ROS at 10 Gy (134.5%) is LOWER than at 5 Gy (173.7%) "
        "for the same line — counter-intuitive given that BER is more compromised. "
        "Paper does not explain this non-monotonic behavior. "
        "Also: PA1 ROS at 10 Gy (191.9%) > PA1PolβΔ at 10 Gy (134.5%), which is the OPPOSITE "
        "of what the BER-failure hypothesis predicts. The authors do not flag this."
    ),
}

# -------- Cell-cycle arrest in G2/M (Fig 6) --------
# Quotes:
#  PA1: control 36.6 ± 0.4 in G2/M; 57.8 ± 1.1 at 10 Gy; 62.0 ± 1.1 at 15 Gy
#  PA1PolβΔ: control 16.2 ± 0.8; 46.2 ± 6.4 at 5 Gy; 56.4 ± 5.0 at 10 Gy; 44.1 ± 2.2 at 15 Gy
audit["CellCycle_G2M_Fig6"] = {
    "PA1": {"control": [36.6, 0.4], "10Gy": [57.8, 1.1], "15Gy": [62.0, 1.1]},
    "PA1PolBetaDelta": {"control": [16.2, 0.8], "5Gy": [46.2, 6.4], "10Gy": [56.4, 5.0], "15Gy": [44.1, 2.2]},
    "internal_consistency_note": (
        "Anomaly: PA1PolβΔ G2/M at 15 Gy (44.1%) is LOWER than at 10 Gy (56.4%). "
        "This is consistent with cells already dying / fragmenting at 15 Gy (so fewer "
        "intact 4N cells are detected), but the paper does not explain it. "
        "Also: untreated PA1PolβΔ G2/M baseline (16.2%) is less than half PA1 baseline "
        "(36.6%) — that is a >2× difference in baseline cell-cycle distribution for "
        "supposedly isogenic lines, which is not discussed."
    ),
}

# -------- Apoptosis (Fig 7) --------
# Quotes at 5 Gy: PA1PolβΔ EA = 20.9 ± 0.9%, PA1 EA = 0.5 ± 0.3%
# At 10 Gy: PA1PolβΔ EA = 31.2 ± 0.2%, LA = 16.5 ± 1.2%; PA1 EA = 0.6 ± 0.1%, LA = 2.1 ± 0.3%
# Live cells at 10 Gy: PA1 58.5 ± 1.9%, PA1PolβΔ 11.3 ± 0.9%
audit["Apoptosis_Fig7"] = {
    "5Gy_EarlyApoptosis_pct": {"PA1": [0.5, 0.3], "PA1PolBetaDelta": [20.9, 0.9]},
    "10Gy_EarlyApoptosis_pct": {"PA1": [0.6, 0.1], "PA1PolBetaDelta": [31.2, 0.2]},
    "10Gy_LateApoptosis_pct":  {"PA1": [2.1, 0.3], "PA1PolBetaDelta": [16.5, 1.2]},
    "10Gy_LiveCells_pct":      {"PA1": [58.5, 1.9], "PA1PolBetaDelta": [11.3, 0.9]},
    "checksum_PA1_10Gy": (
        "Live + EA + LA (PA1@10Gy) = 58.5 + 0.6 + 2.1 = 61.2% — remainder 38.8% is "
        "presumably necrotic / PI-only. Paper does not report the necrotic %."
    ),
    "checksum_PA1del_10Gy": (
        "Live + EA + LA (PA1PolβΔ@10Gy) = 11.3 + 31.2 + 16.5 = 59.0% — "
        "remainder 41.0% necrotic. Paper does not report it."
    ),
    "consistency_with_colony_assay": (
        "At 10 Gy the colony assay says ~4-6% of PA1PolβΔ form colonies (SF~0.05), "
        "and the apoptosis assay says only 11.3% are live at 10 Gy. Roughly consistent: "
        "the ~5% colony-forming fraction is a SUBSET of the ~11% still classified as live."
    ),
}

# -------- HDOCK protein-DNA docking (Results section) --------
# Quotes:
#  Δ-dsDNA: -303.64 kcal/mol vs WT-dsDNA: -245.74 kcal/mol  -> Δ stronger by ~58 kcal/mol
#  Δ-ssDNA: -272.65 kcal/mol vs WT-ssDNA: -285.44 kcal/mol  -> WT stronger by ~12.8 kcal/mol
audit["HDOCK_protein_DNA"] = {
    "WT_dsDNA_kcal_mol": -245.74,
    "DEL_dsDNA_kcal_mol": -303.64,
    "WT_ssDNA_kcal_mol": -285.44,
    "DEL_ssDNA_kcal_mol": -272.65,
    "delta_dsDNA_minus_WT": -303.64 - (-245.74),  # -57.9
    "interpretation_in_paper": "PolβΔ binds dsDNA more strongly than WT — authors argue this is dominant-negative.",
    "critical_caveat": (
        "HDOCK reports DIMENSIONLESS native-like scores (lower = better), NOT a physical "
        "binding free energy in kcal/mol. Reporting HDOCK scores as kcal/mol is a "
        "common but well-documented error in the docking literature. The relative ranking "
        "may still be informative, but the units are wrong. Same applies to ClusPro scores "
        "in Suppl Table S2."
    ),
}

# -------- ClusPro protein-protein scores (Suppl Table S2) --------
audit["ClusPro_protein_protein_Suppl_Table_S2"] = {
    "1EBM_HOGG1":       {"WT": -7.0,  "DEL": -7.2},
    "1TDH_NEIL1":       {"WT": -9.7,  "DEL": -12.4},
    "1WSR_GLDC":        {"WT": -12.4, "DEL": -11.1},
    "1XNA_XRCC1_N":     {"WT": -13.0, "DEL": -13.9},
    "2BRF_PNKP_FHA":    {"WT": -12.9, "DEL": -13.4},
    "2FOZ_ADPRH":       {"WT": -11.9, "DEL": -12.1},
    "2RCW_PARP1":       {"WT": -9.3,  "DEL": -9.2},
    "3Q8K_FEN1":        {"WT": -7.0,  "DEL": -7.2},
    "4ZZY_PARP2":       {"WT": -12.4, "DEL": -11.7},
    "summary": (
        "Only 1 of 9 partners (NEIL1, 1TDH) shows a >2 kcal/mol difference. The paper "
        "draws its main conclusion ('PolβΔ has stronger NEIL1 binding') from this single "
        "outlier. The other 8 are within ±1.3 of WT, well within ClusPro score noise."
    ),
    "unit_caveat": (
        "ClusPro outputs cluster sizes / weighted scores in arbitrary units; reporting "
        "as kcal/mol is incorrect."
    ),
}

# -------- Deletion residue range — text has THREE different versions --------
audit["Deletion_range_internal_inconsistency"] = {
    "Methods_section":     "208-301 (Section 10, Protein structure modelling)",
    "Results_section":     "208-304 (Results paragraph after Fig 8)",
    "Discussion_section":  "211-339 (overlaid structures, after Fig 8 — but this is BEYOND aa 335, the full WT length!)",
    "Sup_Table_S1_cDNA":   "Actual deletion spans WT codons 121-257 (137 aa) with frameshift — does NOT match any of the three text values."
}

# -------- Sequence-level finding (from 01_sequence_check.py) --------
audit["Sequence_check_results_from_script_01"] = json.loads((RES / "sequence_check.json").read_text())

# Write outputs
(RES / "quant_audit.json").write_text(json.dumps(audit, indent=2))
# Pretty-print text
lines = []
def render(obj, depth=0):
    pad = "  " * depth
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                render(v, depth+1)
            else:
                lines.append(f"{pad}{k}: {v}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}[{i}]:")
                render(v, depth+1)
            else:
                lines.append(f"{pad}- {v}")
    else:
        lines.append(f"{pad}{obj}")
render(audit)
(RES / "quant_audit.txt").write_text("\n".join(lines))
print("\n".join(lines[:60]))
print("...")
print(f"\nFull audit: {RES/'quant_audit.txt'}")
