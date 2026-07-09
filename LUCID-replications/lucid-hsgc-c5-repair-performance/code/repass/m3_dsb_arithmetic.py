"""M3+M5+M7+M11: Verify several arithmetic claims about DSB yields & lethality.

Paper claims (verbatim from Marker text):
  - Sec 3.2: simple-DSB = 4.11 / complex-DSB = 0.74 (0 mm), 4.69 / 1.04 (32 mm) Gy^-1 Gbp^-1
  - Sec 4 Discussion: "considering only complex DSBs, the number of DSBs was
    increased by 43% when a PMMA block was inserted"
  - Sec 4 Discussion: "yield ratio of DSB+/DSB++ is approximately 1.44 at 0 mm,
    while the yield ratio approximately 1.13 at 32 mm"
  - Sec 4 Discussion: "binary repair lethality ... ~40%" (paper Table 1 gamma=0.39)
  - Sec 4 Discussion: "lethality of residual complex DSBs ... ~3%" (paper Table 1 beta2=2.75e-2)
  - Sec 4 Discussion: "HR can repair ~97% of complex DSBs" (1 - 0.03 = 0.97)

We compute each from Table 1 / reported yields and compare to the paper's
prose. These are pure arithmetic checks (no model fit), but they exercise
the consistency of the paper's own narrative and Table 1.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent.parent / "results" / "repass" / "m3_dsb_arithmetic.json"

# From Sec 3.2
dsb_simple_0  = 4.11
dsb_simple_32 = 4.69
dsb_complex_0  = 0.74
dsb_complex_32 = 1.04

# Discussion: DSB+/DSB++ ratios
ratio_0 = 1.44   # at 0 mm
ratio_32 = 1.13  # at 32 mm

# Table 1
beta2  = 2.75e-2
gamma  = 0.39

# --- M5: 43% increase in complex DSBs from 0 mm -> 32 mm ---
delta_complex = (dsb_complex_32 - dsb_complex_0) / dsb_complex_0 * 100.0
# Paper: ~43%

# --- M3 simple: increase in simple DSBs ---
delta_simple = (dsb_simple_32 - dsb_simple_0) / dsb_simple_0 * 100.0

# --- M6: DSB+ and DSB++ split given the reported ratios ---
def split(complex_total, ratio):
    # DSB+ + DSB++ = complex_total; DSB+/DSB++ = ratio
    dsbpp = complex_total / (1.0 + ratio)
    dsbp = ratio * dsbpp
    sigma2 = dsbp + 2.0 * dsbpp
    return dsbp, dsbpp, sigma2

dp_0, dpp_0, sigma2_0   = split(dsb_complex_0,  ratio_0)
dp_32, dpp_32, sigma2_32 = split(dsb_complex_32, ratio_32)

# --- M7+M11: Lethality interpretation arithmetic ---
binary_lethality_pct = gamma * 100.0           # ~39% ~ 40% in paper
complex_lethality_pct = beta2 * 100.0          # ~2.75% ~ "3%" in paper
hr_repair_success_pct = (1.0 - beta2) * 100.0  # ~97.25%

out = {
    "claim_M5_complex_dsb_increase_pct": {
        "computed_pct": delta_complex,
        "paper_claim_pct": 43.0,
        "abs_delta_pct_points": abs(delta_complex - 43.0),
        "agrees_within_2_pct_pts": abs(delta_complex - 43.0) < 2.0,
    },
    "claim_M5b_simple_dsb_increase_pct": {
        "computed_pct": delta_simple,
        "paper_qualitative": "slightly larger",
        "qualitative_ok": delta_simple > 0,
    },
    "claim_M6_DSBp_DSBpp_split": {
        "PMMA_0mm":  {"DSBp": dp_0,  "DSBpp": dpp_0,  "Sigma2": sigma2_0,
                      "ratio_used": ratio_0,  "complex_total": dsb_complex_0},
        "PMMA_32mm": {"DSBp": dp_32, "DSBpp": dpp_32, "Sigma2": sigma2_32,
                      "ratio_used": ratio_32, "complex_total": dsb_complex_32},
        "note": "Sigma2 used as TLK slow-repair source = DSBp + 2*DSBpp.",
    },
    "claim_M7_binary_lethality": {
        "gamma_Table1": gamma,
        "pct_lethal": binary_lethality_pct,
        "paper_quote_pct": 40.0,
        "abs_delta_pct_pts": abs(binary_lethality_pct - 40.0),
        "agrees_within_2_pct_pts": abs(binary_lethality_pct - 40.0) < 2.0,
    },
    "claim_M7b_complex_DSB_lethality": {
        "beta2_Table1": beta2,
        "pct_lethal": complex_lethality_pct,
        "paper_quote_pct": 3.0,
        "abs_delta_pct_pts": abs(complex_lethality_pct - 3.0),
        "agrees_within_1_pct_pt": abs(complex_lethality_pct - 3.0) < 1.0,
    },
    "claim_M11_HR_repair_success": {
        "computed_pct": hr_repair_success_pct,
        "paper_quote_pct": 97.0,
        "agrees_within_1_pct_pt": abs(hr_repair_success_pct - 97.0) < 1.0,
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
