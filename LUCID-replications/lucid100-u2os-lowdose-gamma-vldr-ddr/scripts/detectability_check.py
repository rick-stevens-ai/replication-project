"""
detectability_check.py — Plodowska 2025 (U2OS VLDR gamma DDR)

Question: under the standard Lengert/Mirsch chronic-induction model
(N_ss = Y * dose_rate / k_repair), is the AD-only signal even
*detectable* by 53BP1 IF microscopy?

Background numbers we have:
  Y_per_Gy = 35 foci/cell (consensus 53BP1 acute reference)
  k_repair = 0.45 /h (consensus short component)
  AD-low: 31 uGy/h ->  N_ss = 35 * 31e-6 / 0.45 = 0.00241 foci/cell
  AD-high: 55 uGy/h -> N_ss = 35 * 55e-6 / 0.45 = 0.00428 foci/cell

Background spontaneous 53BP1 foci in unirradiated U2OS:
  literature range 0.1 - 0.5 foci/cell (Rothkamm 2003; Lobrich 2010 review)

Conclusion under the standard model:
  AD-only signal is *50-200x* below the spontaneous background, so the
  abstract's claim of a "significant" induction cannot be due to the
  steady-state of newly-formed DSB foci alone. Possible reconciliations:
    (a) Cumulative damage assayed at a TRANSIENT time-point (not steady
        state) - but the chronic equation gives the time-averaged value;
        and at equilibrium the standing pool is exactly N_ss.
    (b) An ATM-independent persistent fraction of foci (slow component
        with k_slow ~ 0.01-0.02 /h) - this would shift N_ss up ~20-45x
        and bring AD-low into the 0.05-0.10 foci/cell range (borderline).
    (c) An AD-induced upregulation of foci formation per dose (radio-
        adaptive priming) - the paper's actual claim.
    (d) The authors are measuring a *fraction of cells with >=1 focus*
        (foci-positive cells), which is far more sensitive than mean
        foci/cell at low N.
  The paper's KU-55933 result (KU does NOT block AD-only induction) is
  ALSO consistent with interpretation (b) or (d): a slow-resolution
  non-ATM repair component would not be reduced by KU.

This script writes results/detectability_check.csv with one row per
candidate slow-component model, and a results/detectability.json with
the recommended digitization tolerance: any AD-only foci/cell value in
Fig 1 that exceeds 0.05 should be cross-checked against (a) reporter
intensity threshold; (b) % foci-positive cells; (c) AD dose accumulated.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

Y = 35.0          # foci/cell/Gy
RATES = {"AD_low_31uGy_per_h": 31e-6, "AD_high_55uGy_per_h": 55e-6}

# Candidate slow-component repair rates (1/h) to bracket the
# spontaneous-vs-induced detectability gap.
K_RATES = {
    "fast_only_default": 0.45,
    "fast+slow_mix_lobrich_2010_avg": 0.10,
    "slow_only_persistent_4h_halflife": 0.17,
    "slow_only_persistent_24h_halflife": 0.0289,
    "slow_only_persistent_48h_halflife": 0.01443,
}

BG_FOCI = {
    "U2OS_low_estimate": 0.10,
    "U2OS_mid_estimate": 0.30,
    "U2OS_high_estimate": 0.50,
}

rows = []
for rate_name, rate in RATES.items():
    for k_name, k in K_RATES.items():
        N_ss = Y * rate / k
        for bg_name, bg in BG_FOCI.items():
            rows.append({
                "AD_arm": rate_name,
                "AD_rate_Gy_per_h": rate,
                "repair_model": k_name,
                "k_repair_per_h": k,
                "predicted_steady_state_foci_per_cell": round(N_ss, 5),
                "spontaneous_bg_scenario": bg_name,
                "spontaneous_bg_foci_per_cell": bg,
                "induced_over_background_ratio": round(N_ss / bg, 4),
                "detectable_at_mean_focal_level": "yes" if N_ss > 0.10 * bg else "no",
            })

with open(OUT / "detectability_check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

summary = {
    "punchline": (
        "Under the consensus fast-component model (k=0.45/h), the AD-only "
        "predicted steady-state is 50-200x below spontaneous background — "
        "i.e. invisible at the mean-foci/cell level. Reconciling the "
        "paper's 'significant' AD-only induction with the model requires "
        "either (a) a slow-component PIKK-independent fraction (k ~ "
        "0.01-0.03 /h) lifting N_ss into the 0.03-0.30 foci/cell range, "
        "or (b) reporting % foci-positive cells (more sensitive than "
        "mean N), or (c) a cumulative-foci assay over the 8-day window. "
        "The KU-55933-resistant AD signal is consistent with (a) being a "
        "DNA-PKcs/ATR-mediated slow process."
    ),
    "fast_only_default_N_ss": {
        "AD_low_31uGy_per_h": Y * 31e-6 / 0.45,
        "AD_high_55uGy_per_h": Y * 55e-6 / 0.45,
    },
    "slow_only_24h_halflife_N_ss": {
        "AD_low_31uGy_per_h": Y * 31e-6 / 0.0289,
        "AD_high_55uGy_per_h": Y * 55e-6 / 0.0289,
    },
    "tolerance_recommendations_for_fig1_digitization": {
        "AD_only_foci_per_cell": (
            "If the Fig 1 AD-only point exceeds ~0.1 foci/cell, the simple "
            "fast-component model is rejected and a multi-component fit "
            "with k_slow ~ 0.01-0.05 /h must be substituted before computing "
            "agreement metrics."
        ),
        "CD_only_foci_per_cell": "Expect peak ~25-40 foci/cell at 0.5-1 h post-CD; consistent w/ Y_per_Gy=30-40.",
        "AD+CD_vs_CD_ratio": "Pure linear superposition predicts ratio ~ 1.000. Any large deviation = adaptive modulation (paper's claim).",
    },
}

with open(OUT / "detectability.json", "w") as fh:
    json.dump(summary, fh, indent=2)

print(f"wrote {OUT/'detectability_check.csv'} ({len(rows)} rows)")
print(f"wrote {OUT/'detectability.json'}")
print()
print(summary["punchline"])
