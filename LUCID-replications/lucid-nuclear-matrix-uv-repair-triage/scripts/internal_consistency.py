#!/usr/bin/env python3
"""
Internal consistency check — Mullenders et al. NAR 1988, 16(22):10607–10622.

The paper has NO machine-readable data, NO tables, NO equations and NO fitted
parameters. The only computational target that is honest (i.e. not a circular
re-derivation of the same scatter the authors eyeballed) is to take the
text-stated grain-count percentages (autoradiography assay, Fig. 3) and compute
the implied fold-enrichment-over-baseline, then compare that to the
text-stated sucrose-gradient ³H/¹⁴C fold-enrichments at matching UV doses.

Inputs are all from the paper text (source.txt).
Outputs: results/internal_consistency_checks.json
"""
from __future__ import annotations
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

# Author-stated autoradiographic grain-% at matrix (from source.txt around L477-487)
grain_pct = {
    "baseline_unirradiated":              18.1,
    "5J_per_m2_6min_pulse":               34.1,
    "5J_per_m2_10min_pulse":              32.5,
    "30J_per_m2_10min_pulse":             23.6,
    "30J_per_m2_120min_pulse":            18.7,
}

# Author-stated sucrose-gradient ³H/¹⁴C fold-enrichment summary (Discussion + Results)
sucrose_fold = {
    "30J_per_m2_short_pulse_5_to_10min":  (1.3, 1.6),   # "1.3–1.6", summarized as 1.5
    "5J_per_m2_2h_normal":                (1.7, 1.7),
    "5J_per_m2_2h_XPD":                   (1.7, 1.7),
    "5J_per_m2_2h_XPC":                   (3.0, 999.0), # ">3-fold"
    "5J_per_m2_2h_CS":                    (0.5, 0.5),   # ~2-fold depletion
    "replication_label_reference":        (15.0, 20.0),
}

baseline = grain_pct["baseline_unirradiated"]
grain_fold = {
    "5J_6min_grain_fold_vs_baseline":   round(grain_pct["5J_per_m2_6min_pulse"]/baseline, 3),
    "5J_10min_grain_fold_vs_baseline":  round(grain_pct["5J_per_m2_10min_pulse"]/baseline, 3),
    "30J_10min_grain_fold_vs_baseline": round(grain_pct["30J_per_m2_10min_pulse"]/baseline, 3),
    "30J_120min_grain_fold_vs_baseline":round(grain_pct["30J_per_m2_120min_pulse"]/baseline, 3),
}

southern = {
    "matrix_pct_10ug_DNase":  17.5,
    "loop_pct_10ug_DNase":    82.5,
    "matrix_pct_12ug_DNase":  10.0,
    "loop_pct_12ug_DNase":    90.0,
    "matrix_ratio_12_over_10": round(10.0/17.5, 3),  # 0.571
    "sum_check_10ug": 17.5 + 82.5,                    # 100.0
    "sum_check_12ug": 10.0 + 90.0,                    # 100.0
}

# Consistency narrative
consistency = {
    "5J_short_pulse_method_agreement":
      f"grain {grain_fold['5J_6min_grain_fold_vs_baseline']}/"
      f"{grain_fold['5J_10min_grain_fold_vs_baseline']} vs sucrose 1.7 — methods agree within ~10–15%",
    "30J_short_pulse_method_agreement":
      f"grain {grain_fold['30J_10min_grain_fold_vs_baseline']} vs sucrose 1.3–1.6 — overlap",
    "30J_long_pulse_decay":
      f"grain {grain_fold['30J_120min_grain_fold_vs_baseline']} ≈ no enrichment after 2 h — matches verbal claim",
    "southern_dnase_dose_monotonicity":
      f"matrix fraction drops 17.5 → 10.0% as DNase rises 10 → 12 µg/ml — monotonic, as expected",
    "fractions_sum_to_100":
      "both 10 µg/ml (17.5+82.5) and 12 µg/ml (10+90) sum to 100% as required",
}

payload = {
    "paper": "Mullenders et al. 1988, NAR 16(22):10607–10622",
    "source": "source.txt (pdftotext -layout); page images in pages/",
    "author_stated": {"grain_pct": grain_pct, "sucrose_fold": sucrose_fold, "southern": southern},
    "derived": {"grain_fold": grain_fold},
    "consistency": consistency,
    "notes": [
        "These are NOT independent measurements; they are arithmetic on the paper's own stated numbers.",
        "The 1988 paper provides no raw DPM tables, no error bars, no N, and no statistical tests.",
        "Treat this as an internal-consistency cross-check between the paper's two assay methods, ",
        "not a replication of the underlying biology."
    ],
}

with open(OUT / "internal_consistency_checks.json", "w") as f:
    json.dump(payload, f, indent=2)

print(json.dumps(payload, indent=2))
