"""M1: Verify the paper's half-life arithmetic for HSGc-C5 fast/slow repair.

Paper quotes (Sakata et al. 2021, Cancers 13:6046):
  - "The probability of the repair was approximately 3.36 h^-1
     (the half-life time is approximately 12.6 min)" (Results, Sec 3.3)
  - "the fast-repair process was very fast (12.7 min)"  (Discussion, Sec 4)
  - "Through the slow-repair process, the probability of the repair was
     approximately 0.01 h^-1 (the half-life time is approximately 70.0 h)" (Sec 3.3)

Tau = ln(2)/lam (paper's Eq 6 surrounding text: tau = ln 2 / lam if 1st-order
repair is not saturated).
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent.parent / "results" / "repass" / "m1_halflives.json"

LAM1 = 3.36          # h^-1, Table 1
LAM2 = 0.99e-2       # h^-1, Table 1 (paper rounds to "0.01" in prose)

tau1_h = math.log(2.0) / LAM1
tau1_min = tau1_h * 60.0
tau2_h = math.log(2.0) / LAM2

# Paper quotes
paper_tau1_min_results = 12.6
paper_tau1_min_discussion = 12.7
paper_tau2_h = 70.0

out = {
    "claim_M1_fast_halflife": {
        "lam1_h_inv": LAM1,
        "predicted_tau_min": tau1_min,
        "paper_quoted_results_section_min": paper_tau1_min_results,
        "paper_quoted_discussion_section_min": paper_tau1_min_discussion,
        "match_results_abs_delta_min": abs(tau1_min - paper_tau1_min_results),
        "match_discussion_abs_delta_min": abs(tau1_min - paper_tau1_min_discussion),
        "agrees_within_0p1_min": abs(tau1_min - paper_tau1_min_results) < 0.1
                                  or abs(tau1_min - paper_tau1_min_discussion) < 0.1,
    },
    "claim_M1_slow_halflife": {
        "lam2_h_inv": LAM2,
        "predicted_tau_h": tau2_h,
        "paper_quoted_h": paper_tau2_h,
        "abs_delta_h": abs(tau2_h - paper_tau2_h),
        "agrees_within_1_h": abs(tau2_h - paper_tau2_h) < 1.0,
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
