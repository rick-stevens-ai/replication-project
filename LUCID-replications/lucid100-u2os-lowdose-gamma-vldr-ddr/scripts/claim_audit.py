"""
claim_audit.py — Quantitative claim audit for Plodowska et al. 2025
(DNA Repair 152:103875; U2OS very-low-dose-rate gamma DDR).

Because the main text + figures + supplements remain Cloudflare-blocked
(see notes/data_availability_check.md), this driver does NOT fit author
data. Instead it does the only honest computational replication available
without the figures:

  1. Computes the steady-state and peak 53BP1 foci predictions of the
     standard Lengert/Mirsch (Sci Rep 2018) chronic+impulse kinetic model
     for the EXACT exposure parameters the paper specifies in its abstract.
  2. Computes the predicted ratios across the paper's five named
     conditions (AD-low, AD-high, CD, AD-low+CD, AD-high+CD), with and
     without a KU-55933 ATM-inhibition factor.
  3. Reports which of the paper's *qualitative* abstract claims are
     consistent with the standard kinetic model and which require an
     additional mechanism (e.g. non-ATM PIKK induction at VLDR).
  4. Does NOT compute author-reported numerical foci counts because no
     such numbers exist in any artifact we can fetch — every Result-figure
     quantitative value is locked behind ScienceDirect Cloudflare.

Outputs:
  results/claim_audit.csv     — one row per abstract claim with status
  results/predictions.csv     — model predictions for every condition
  results/predictions.json    — same in machine-readable form
  results/sensitivity.csv     — Y_per_Gy x k_repair sensitivity sweep

Usage:
  python3 scripts/claim_audit.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from foci_kinetics import (  # noqa: E402
    FociParams,
    ad_curve,
    ad_then_cd_curve,
    cd_curve,
    chronic_N,
)

# --------------------------------------------------------------------------
# Exposure conditions as specified by the paper's abstract
# --------------------------------------------------------------------------
# Abstract verbatim:
#   "U2OS cells (with wild type p53) were exposed to gamma radiation AD of
#    5.9 mGy at 31 microGy/h and of 10.5 mGy at 55 microGy/h.
#    ATM was inhibited by addition of KU-55933.
#    Adapted cells were exposed to a CD of 1 Gy photon radiation at 1 Gy/min."

AD_LOW_DOSE_Gy = 5.9e-3
AD_LOW_RATE_Gy_per_h = 31e-6
AD_HIGH_DOSE_Gy = 10.5e-3
AD_HIGH_RATE_Gy_per_h = 55e-6
CD_DOSE_Gy = 1.0
CD_RATE_Gy_per_min = 1.0

T_AD_LOW_h = AD_LOW_DOSE_Gy / AD_LOW_RATE_Gy_per_h   # 190.32 h
T_AD_HIGH_h = AD_HIGH_DOSE_Gy / AD_HIGH_RATE_Gy_per_h  # 190.91 h
T_CD_min = CD_DOSE_Gy / CD_RATE_Gy_per_min            # 1.0 min

# Literature defaults for 53BP1 foci in human cells.
# These are NOT author values; they are the consensus from
# Rothkamm/Lobrich 2003 + Lengert/Mirsch 2018 + the LUCID Mariotti slot.
Y_PER_GY_53BP1 = 35.0   # foci/cell/Gy at acute reference rate (consensus 30-40)
K_REPAIR_53BP1 = 0.45   # 1/h short component (consensus 0.3-0.7)

# KU-55933 modifier — qualitative pattern from the paper's abstract:
#   "KU-55933 failed to inhibit the induction of foci by AD and AD+CD,
#    while foci induction by CD alone was inhibited."
# Modelled here as a SCENARIO, not a fit, with parameter sweep below.
KU_AD_FACTOR_DEFAULT = 1.00          # KU does not block AD-only signal
KU_CD_FACTOR_DEFAULT = 0.40          # KU reduces acute CD signal ~60%
KU_AD_PLUS_CD_FACTOR_DEFAULT = 1.00  # AD+CD signal not abolished

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def make_params(rate_Gy_per_h: float, dose_Gy: float) -> FociParams:
    return FociParams(
        Y_per_Gy=Y_PER_GY_53BP1,
        k_repair=K_REPAIR_53BP1,
        dose_rate_AD_Gy_per_h=rate_Gy_per_h,
        T_ad_h=dose_Gy / rate_Gy_per_h,
        CD_dose_Gy=CD_DOSE_Gy,
        gap_h=0.0,
    )


def steady_state_foci(rate_Gy_per_h: float,
                      Y_per_Gy: float = Y_PER_GY_53BP1,
                      k: float = K_REPAIR_53BP1) -> float:
    """Closed-form steady-state mean foci/cell under chronic exposure."""
    R_foci_per_h = Y_per_Gy * rate_Gy_per_h
    return R_foci_per_h / k


def equilibrium_fraction_at_end(rate_Gy_per_h: float, dose_Gy: float,
                                k: float = K_REPAIR_53BP1) -> float:
    """How close N reaches steady state at the end of the exposure window.
    Returns 1 - exp(-k*T)."""
    T = dose_Gy / rate_Gy_per_h
    return 1.0 - math.exp(-k * T)


# --------------------------------------------------------------------------
# Predictions per condition
# --------------------------------------------------------------------------

def compute_predictions() -> dict:
    p_low = make_params(AD_LOW_RATE_Gy_per_h, AD_LOW_DOSE_Gy)
    p_high = make_params(AD_HIGH_RATE_Gy_per_h, AD_HIGH_DOSE_Gy)

    # Steady-state values (foci/cell during chronic exposure)
    ss_low = steady_state_foci(AD_LOW_RATE_Gy_per_h)
    ss_high = steady_state_foci(AD_HIGH_RATE_Gy_per_h)
    eq_low = equilibrium_fraction_at_end(AD_LOW_RATE_Gy_per_h, AD_LOW_DOSE_Gy)
    eq_high = equilibrium_fraction_at_end(AD_HIGH_RATE_Gy_per_h, AD_HIGH_DOSE_Gy)
    n_end_low = ss_low * eq_low       # foci/cell at end of low-rate AD
    n_end_high = ss_high * eq_high    # foci/cell at end of high-rate AD

    # Acute CD impulse peak
    cd_peak = Y_PER_GY_53BP1 * CD_DOSE_Gy   # 35 foci/cell

    # CD peak with KU
    cd_peak_ku = KU_CD_FACTOR_DEFAULT * cd_peak

    # AD+CD: with chronic gap=0, the CD lands the moment AD ends.
    # At that instant N ≈ n_end + cd_peak (linear superposition).
    ad_low_cd_peak = n_end_low + cd_peak
    ad_high_cd_peak = n_end_high + cd_peak
    ad_low_cd_peak_ku = n_end_low * KU_AD_FACTOR_DEFAULT + cd_peak * KU_CD_FACTOR_DEFAULT
    ad_high_cd_peak_ku = n_end_high * KU_AD_FACTOR_DEFAULT + cd_peak * KU_CD_FACTOR_DEFAULT

    # Time-to-half-decay after CD (post-CD)
    t_half_h = math.log(2.0) / K_REPAIR_53BP1

    return {
        "exposure": {
            "AD_low_dose_Gy": AD_LOW_DOSE_Gy,
            "AD_low_rate_Gy_per_h": AD_LOW_RATE_Gy_per_h,
            "AD_low_duration_h": round(T_AD_LOW_h, 3),
            "AD_low_duration_days": round(T_AD_LOW_h / 24.0, 3),
            "AD_high_dose_Gy": AD_HIGH_DOSE_Gy,
            "AD_high_rate_Gy_per_h": AD_HIGH_RATE_Gy_per_h,
            "AD_high_duration_h": round(T_AD_HIGH_h, 3),
            "AD_high_duration_days": round(T_AD_HIGH_h / 24.0, 3),
            "CD_dose_Gy": CD_DOSE_Gy,
            "CD_rate_Gy_per_min": CD_RATE_Gy_per_min,
            "CD_duration_min": T_CD_min,
        },
        "model_constants": {
            "Y_per_Gy_53BP1": Y_PER_GY_53BP1,
            "k_repair_per_h": K_REPAIR_53BP1,
            "t_half_decay_h": round(t_half_h, 3),
        },
        "steady_state_foci_per_cell": {
            "AD_low_VLDR_steady_state": round(ss_low, 6),
            "AD_high_VLDR_steady_state": round(ss_high, 6),
            "AD_low_equilibration_fraction": round(eq_low, 6),
            "AD_high_equilibration_fraction": round(eq_high, 6),
            "AD_low_foci_at_end_of_AD": round(n_end_low, 6),
            "AD_high_foci_at_end_of_AD": round(n_end_high, 6),
        },
        "peak_foci_per_cell": {
            "CD_only_peak": round(cd_peak, 3),
            "CD_only_KU_peak": round(cd_peak_ku, 3),
            "AD_low_plus_CD_peak": round(ad_low_cd_peak, 3),
            "AD_high_plus_CD_peak": round(ad_high_cd_peak, 3),
            "AD_low_plus_CD_KU_peak": round(ad_low_cd_peak_ku, 3),
            "AD_high_plus_CD_KU_peak": round(ad_high_cd_peak_ku, 3),
        },
        "KU_modifier_scenario": {
            "AD_yield_factor": KU_AD_FACTOR_DEFAULT,
            "CD_yield_factor": KU_CD_FACTOR_DEFAULT,
            "AD_plus_CD_factor": KU_AD_PLUS_CD_FACTOR_DEFAULT,
        },
    }


# --------------------------------------------------------------------------
# Claim audit
# --------------------------------------------------------------------------

CLAIMS = [
    {
        "id": "C1",
        "claim": "AD alone produces a significant 53BP1 foci induction.",
        "type": "qualitative",
        "tested_via": "model prediction of steady-state N during AD",
        "verdict": None,
    },
    {
        "id": "C2",
        "claim": "KU-55933 fails to inhibit 53BP1 foci induction by AD alone.",
        "type": "qualitative",
        "tested_via": "ratio (AD+KU)/(AD) predicted ~1.0 under the modelled scenario; "
                      "consistent with non-ATM (DNA-PKcs/ATR) handling of VLDR damage",
        "verdict": None,
    },
    {
        "id": "C3",
        "claim": "KU-55933 inhibits foci induction by CD alone.",
        "type": "qualitative",
        "tested_via": "ratio (CD+KU)/(CD) predicted ~0.40 in standard ATM-dominant acute scenario",
        "verdict": None,
    },
    {
        "id": "C4",
        "claim": "KU-55933 fails to inhibit foci induction by AD+CD.",
        "type": "qualitative",
        "tested_via": "ratio (AD+CD+KU)/(AD+CD) predicted ~1.0 if combined response uses non-ATM kinases",
        "verdict": None,
    },
    {
        "id": "C5",
        "claim": "AD modulates the response to a subsequent CD.",
        "type": "qualitative",
        "tested_via": "ad_then_cd_curve permits a cross-talk factor ad_plus_cd_factor; "
                      "linear-superposition model is the *null hypothesis*; deviation = adaptive response",
        "verdict": None,
    },
    {
        "id": "C6",
        "claim": "KU-55933 potentiates the G2 block in AD+CD-exposed cells.",
        "type": "qualitative",
        "tested_via": "outside foci-kinetics model; G2 block requires cell-cycle compartment fits",
        "verdict": None,
    },
    {
        "id": "C7",
        "claim": "Gene expression is modulated by AD.",
        "type": "qualitative",
        "tested_via": "qPCR / panel data; requires supplementary table",
        "verdict": None,
    },
    {
        "id": "C8",
        "claim": "AD exposure dose rates were 31 microGy/h (5.9 mGy total) and 55 microGy/h (10.5 mGy total).",
        "type": "quantitative",
        "tested_via": "exposure-duration cross-check: 5.9/31e-6 = 190.32 h; 10.5/55e-6 = 190.91 h",
        "verdict": None,
    },
    {
        "id": "C9",
        "claim": "CD was 1 Gy delivered at 1 Gy/min.",
        "type": "quantitative",
        "tested_via": "duration cross-check: 1.0/1.0 = 1.0 min",
        "verdict": None,
    },
]


def evaluate_claims(pred: dict) -> list[dict]:
    rows = []
    p = pred["peak_foci_per_cell"]
    ss = pred["steady_state_foci_per_cell"]
    ku = pred["KU_modifier_scenario"]

    # C1 — AD-only "significant" induction.
    # Predicted steady-state foci are ~2e-3 to ~4e-3 per cell — well below 1
    # foci/cell. "Significant" in the paper is almost certainly statistical
    # (vs sham) given typical microscopy fields of ~10^3-10^4 cells per
    # condition. Model is CONSISTENT with the headline (some signal exists),
    # but a quantitative test requires per-cell counts from Fig 1.
    c1 = (
        "CONSISTENT (model gives sub-foci/cell steady-state ~%g (low) / %g (high); the paper's "
        "'significant' is statistical, not large-N)" % (
            ss["AD_low_VLDR_steady_state"], ss["AD_high_VLDR_steady_state"])
    )

    # C2 — KU does not affect AD-only.
    # Standard ATM-dominant model would PREDICT a drop. Paper observes ~no drop.
    # That contradicts an ATM-only model and supports a non-ATM PIKK at VLDR.
    c2 = (
        "REQUIRES non-ATM PIKK (DNA-PKcs/ATR) hypothesis at VLDR. Model captures via "
        "KU_AD_FACTOR=1.0 scenario; not testable without Fig 1 per-cell counts."
    )

    # C3 — KU inhibits CD-only.
    # Standard scenario: CD impulse foci = 35 foci/cell at peak; KU brings to ~14.
    # The CD/CD+KU ratio is 1/0.40 = 2.5. Consistent with broad literature on
    # KU-55933 (Hickson 2004; Bakkenist & Kastan 2003) reducing IRIF intensity ~50-70%.
    c3 = (
        "CONSISTENT with ATM literature (~50-70%% IRIF reduction). Model peak CD=%g, "
        "CD+KU=%g (ratio %.2fx)." % (p["CD_only_peak"], p["CD_only_KU_peak"],
                                     p["CD_only_peak"] / max(p["CD_only_KU_peak"], 1e-9))
    )

    # C4 — KU does not block AD+CD.
    # Under linear superposition this WOULD predict a drop (since CD dominates).
    # Paper observes no drop => "AD pre-exposure rewires kinase usage so CD
    # response becomes ATM-independent in adapted cells".
    # That cannot be captured by the linear superposition model alone — it
    # requires an extra cross-talk modifier (ad_plus_cd_factor).
    c4 = (
        "REQUIRES adaptive cross-talk (AD switches CD-response kinase profile). Pure linear "
        "superposition predicts (AD+CD+KU)/(AD+CD) ~ %.2f (not 1.0). Model "
        "scaffold has the ad_plus_cd_factor handle to capture this; testing requires Fig 2."
        % (
            ((ss["AD_low_foci_at_end_of_AD"] * ku["AD_yield_factor"]
              + p["CD_only_KU_peak"])
             / max(p["AD_low_plus_CD_peak"], 1e-9))
        )
    )

    # C5 — AD modulates CD response.
    # Same model handle (ad_plus_cd_factor). Null = 1.0 (no modulation).
    # Paper observation: non-null. Without Fig 2 we can only state the test we would run.
    c5 = (
        "TESTABLE-ONCE-DIGITIZED. Model predicts (AD_low+CD)/(CD)=%.3f and "
        "(AD_high+CD)/(CD)=%.3f under pure linear superposition (modulation factor=1). "
        "Author's finding of modulation = digitized ratio significantly != these."
        % (
            p["AD_low_plus_CD_peak"] / p["CD_only_peak"],
            p["AD_high_plus_CD_peak"] / p["CD_only_peak"],
        )
    )

    # C6 — G2 block potentiation by KU in AD+CD.
    c6 = "OUT-OF-SCOPE for foci-kinetics model. Requires cell-cycle compartment fit on Fig 3."

    # C7 — gene expression modulation by AD.
    c7 = "DATA-BLOCKED. Requires supplementary table (mmc*.xlsx) not yet retrievable."

    # C8 — exposure duration cross-check.
    e = pred["exposure"]
    c8 = (
        "VERIFIED arithmetic: AD-low duration = %.3f h (~%.2f days); "
        "AD-high duration = %.3f h (~%.2f days). Both ~7.9 days of chronic VLDR exposure." %
        (e["AD_low_duration_h"], e["AD_low_duration_days"],
         e["AD_high_duration_h"], e["AD_high_duration_days"])
    )

    # C9 — CD duration cross-check.
    c9 = "VERIFIED arithmetic: 1 Gy at 1 Gy/min = 1.0 min impulse — well-approximated as delta."

    verdicts = [c1, c2, c3, c4, c5, c6, c7, c8, c9]
    for claim, verdict in zip(CLAIMS, verdicts):
        rows.append({
            "id": claim["id"],
            "type": claim["type"],
            "claim": claim["claim"],
            "tested_via": claim["tested_via"],
            "verdict": verdict,
        })
    return rows


# --------------------------------------------------------------------------
# Sensitivity sweep
# --------------------------------------------------------------------------

def sensitivity_sweep() -> list[dict]:
    """Sweep Y_per_Gy in {25, 30, 35, 40, 45} and k_repair in {0.30, 0.45, 0.60}.
    Report steady-state AD-low/high and CD peak for each."""
    rows = []
    for Y in [25.0, 30.0, 35.0, 40.0, 45.0]:
        for k in [0.30, 0.45, 0.60]:
            ss_low = Y * AD_LOW_RATE_Gy_per_h / k
            ss_high = Y * AD_HIGH_RATE_Gy_per_h / k
            cd_peak = Y * CD_DOSE_Gy
            rows.append({
                "Y_per_Gy": Y,
                "k_repair_per_h": k,
                "AD_low_steady_state_foci_per_cell": round(ss_low, 6),
                "AD_high_steady_state_foci_per_cell": round(ss_high, 6),
                "CD_peak_foci_per_cell": round(cd_peak, 3),
                "high_over_low_ratio": round(ss_high / ss_low, 3),
            })
    return rows


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    pred = compute_predictions()
    rows = evaluate_claims(pred)
    sens = sensitivity_sweep()

    results_dir = ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    with open(results_dir / "predictions.json", "w") as fh:
        json.dump(pred, fh, indent=2)

    # CSV — predictions flat
    flat = []
    for section, vals in pred.items():
        for k, v in vals.items():
            flat.append({"section": section, "key": k, "value": v})
    with open(results_dir / "predictions.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["section", "key", "value"])
        w.writeheader()
        w.writerows(flat)

    # CSV — claim audit
    with open(results_dir / "claim_audit.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "type", "claim", "tested_via", "verdict"])
        w.writeheader()
        w.writerows(rows)

    # CSV — sensitivity
    with open(results_dir / "sensitivity.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(sens[0].keys()))
        w.writeheader()
        w.writerows(sens)

    # Print human summary
    print("=" * 78)
    print("Plodowska 2025 — claim audit (data-blocked, model-only)")
    print("=" * 78)
    print(f"\nExposure constants (from abstract):")
    for k, v in pred["exposure"].items():
        print(f"  {k:36s} {v}")
    print(f"\nModel constants (literature defaults; NOT author values):")
    for k, v in pred["model_constants"].items():
        print(f"  {k:36s} {v}")
    print(f"\nKey predictions:")
    for k, v in pred["steady_state_foci_per_cell"].items():
        print(f"  {k:36s} {v}")
    for k, v in pred["peak_foci_per_cell"].items():
        print(f"  {k:36s} {v}")
    print(f"\nClaim verdicts:")
    for r in rows:
        print(f"  [{r['id']}] {r['claim']}")
        print(f"       -> {r['verdict']}")
    print(f"\nArtifacts written to {results_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
