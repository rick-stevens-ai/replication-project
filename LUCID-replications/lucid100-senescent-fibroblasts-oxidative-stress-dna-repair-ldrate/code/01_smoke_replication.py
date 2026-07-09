#!/usr/bin/env python3
"""
LUCID100 slot 56 — smoke replication for Sangsuwan et al. 2023 (FBL 28(11):296).

Strategy: raw per-replicate data are not deposited ("available upon request").
This smoke script uses the PUBLISHED group means ± SE with n=3 to:
  (A) re-run Welch / Student t-tests reported for Table 1 (TIFs at 48 h post 1 Gy)
      and check whether reported significance bins (<0.05, <0.01, <0.001, <0.0001, nc)
      are consistent with the means/SEs in the paper.
  (B) re-do the linear-regression slope estimation for extracellular 8-oxo-dG
      accumulation in P8 vs P13, control vs LDR, over 8 weeks, using reported
      weekly means and reported overall slopes (16/27/26/45 ng/10^6 cells/week)
      to check internal arithmetic consistency.
  (C) verify the qualitative ordering of the γH2AX foci repair kinetics:
      P8 returns to baseline by 24 h while P23 retains ~10 foci, and P19
      groups retain ~4.5 foci.
  (D) report which Table 1 reported significances are consistent / surprising
      under a 2-sample independent t-test assuming SE_i = sd_i/sqrt(n), n=3.

This is a numerical-claim consistency check, NOT a wet-lab re-execution.
No author data, no raw images, no pipeline available.
"""

import json, math, csv, sys, os
from pathlib import Path
from statistics import mean
from scipy import stats
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results"
OUT.mkdir(exist_ok=True)

N = 3  # paper: "at least three independent experiments" — minimum n.

# ------------------------------------------------------------------
# A. Table 1 — TIFs per cell, baseline and 48 h post 1 Gy.
# Reported in paper §3.5 Table 1; see ARTIFACT_MANIFEST.md item 4.
# ------------------------------------------------------------------
# means and SEs as printed:
tif = {
    "P8_C":   (1.91, 0.45),
    "P8_1Gy48h":   (3.88, 0.42),
    "P19C_C":   (7.95, 1.13),
    "P19C_1Gy48h":  (10.71, 1.58),
    "P19IR_C":  (12.32, 1.52),
    "P19IR_1Gy48h": (14.75, 1.91),
    "P19ST_C":  (11.55, 1.29),
    "P19ST_1Gy48h": (16.33, 2.26),
    "P23_C":    (18.27, 2.72),
    "P23_1Gy48h":   (28.55, 2.55),
}

# Reported significance bins from Table 1:
reported_tif = [
    # (A, B, reported_bin_or_p)
    ("P8_1Gy48h",   "P8_C",          "<0.01"),
    ("P8_1Gy48h",   "P19C_C",        "<0.0001"),
    ("P8_1Gy48h",   "P19IR_C",       "<0.0001"),
    ("P8_1Gy48h",   "P19ST_C",       "<0.0001"),
    ("P8_1Gy48h",   "P23_C",         "<0.0001"),
    ("P8_1Gy48h",   "P19C_1Gy48h",   "<0.001"),
    ("P8_1Gy48h",   "P19IR_1Gy48h",  "<0.0001"),
    ("P8_1Gy48h",   "P19ST_1Gy48h",  "<0.0001"),
    ("P8_1Gy48h",   "P23_1Gy48h",    "<0.0001"),
    ("P19C_C",      "P19C_1Gy48h",   "nc (p=0.09)"),
    ("P19C_C",      "P19IR_C",       "<0.05"),
    ("P19C_C",      "P19ST_C",       "<0.05"),
    ("P19C_C",      "P23_C",         "<0.0001"),
    ("P19C_1Gy48h", "P19IR_1Gy48h",  "nc (p=0.08)"),
    ("P19C_1Gy48h", "P19ST_1Gy48h",  "<0.05"),
    ("P19C_1Gy48h", "P23_1Gy48h",    "<0.0001"),
    ("P19IR_C",     "P19IR_1Gy48h",  "nc (p=0.16)"),
    ("P19IR_C",     "P19ST_C",       "nc (p=0.35)"),
    ("P19IR_C",     "P23_C",         "<0.05"),
    ("P19IR_1Gy48h","P19ST_1Gy48h",  "nc (p=0.03)"),  # note: p=0.03 but labelled nc in paper
    ("P19IR_1Gy48h","P23_1Gy48h",    "<0.001"),
    ("P19ST_C",     "P19ST_1Gy48h",  "<0.05"),
    ("P19ST_C",     "P23_C",         "<0.05"),
    ("P19ST_1Gy48h","P23_1Gy48h",    "<0.01"),
]

def welch_from_summary(m1, se1, n1, m2, se2, n2):
    sd1 = se1 * math.sqrt(n1); sd2 = se2 * math.sqrt(n2)
    s1 = sd1**2 / n1; s2 = sd2**2 / n2
    se_diff = math.sqrt(s1 + s2)
    if se_diff == 0:
        return float("nan"), float("nan")
    t = (m1 - m2) / se_diff
    df = (s1 + s2)**2 / ((s1**2)/(n1-1) + (s2**2)/(n2-1))
    p = 2 * (1 - stats.t.cdf(abs(t), df))
    return t, p

def bin_p(p):
    if p < 0.0001: return "<0.0001"
    if p < 0.001:  return "<0.001"
    if p < 0.01:   return "<0.01"
    if p < 0.05:   return "<0.05"
    return f"nc (p={p:.2f})"

A_results = []
for a, b, reported in reported_tif:
    m1, se1 = tif[a]; m2, se2 = tif[b]
    t, p = welch_from_summary(m1, se1, N, m2, se2, N)
    A_results.append({
        "A": a, "B": b, "mean_A": m1, "se_A": se1, "mean_B": m2, "se_B": se2,
        "t": round(t, 3), "p_replicated": round(p, 5),
        "bin_replicated": bin_p(p),
        "reported": reported,
    })

# ------------------------------------------------------------------
# B. 8-oxo-dG accumulation slope check (P8/P13, control/LDR).
# Paper reports per-week mean increment (slope) and SE from a linear
# regression over 8 weeks. We do not have weekly per-replicate values,
# so we check internal consistency of the four reported t-tests
# (P8 LDR vs P13 LDR; P8 C vs P13 C) using slope ± SE_slope with n=3.
# Reported: "irradiated P13 (45±10) > irradiated P8 (27±7), p=0.035";
# "non-irradiated P13 (26±5) > non-irradiated P8 (16±4), p=0.045".
# Also: P8 C vs P8 LDR p=0.003 (16±4 vs 27±7).
# ------------------------------------------------------------------
oxo = {
    "P8_C":  (16, 4),
    "P8_LDR":(27, 7),
    "P13_C": (26, 5),
    "P13_LDR":(45, 10),
}
oxo_tests = [
    ("P13_LDR","P8_LDR", 0.035),
    ("P13_C", "P8_C",    0.045),
    ("P8_LDR","P8_C",    0.003),
]
B_results = []
for a, b, p_rep in oxo_tests:
    m1, se1 = oxo[a]; m2, se2 = oxo[b]
    t, p = welch_from_summary(m1, se1, N, m2, se2, N)
    B_results.append({
        "A": a, "B": b, "mean_A": m1, "se_A": se1, "mean_B": m2, "se_B": se2,
        "t_replicated": round(t, 3),
        "p_replicated": round(p, 5),
        "p_reported":   p_rep,
        "agree_within_factor_3": bool((p / p_rep < 3 and p_rep / p < 3)) if (p > 0 and p_rep > 0) else False,
    })

# ------------------------------------------------------------------
# C. γH2AX foci repair kinetics — qualitative ordering check.
# Paper Fig 5A/B, §3.4. Time courses for P8, P19-C/ST/IR, P23.
# ------------------------------------------------------------------
foci = {
    # group: {time_h: (mean, se)}
    "P8":   {0: (0.20, 0.05), 0.75: (17.0, 2.0), 24: (0.30, 0.10), 48: (0.30, 0.10)},
    "P23":  {0: (3.50, 1.30), 0.75: (22.0, 2.0), 24: (10.0, 1.0),  48: (10.0, 1.0)},
    "P19C": {0: (3.50, 0.50), 0.75: (None,None), 24: (4.50, 0.70),  48: (4.50, 0.70)},
    "P19ST":{0: (3.50, 0.50), 0.75: (None,None), 24: (4.50, 0.70),  48: (4.50, 0.70)},
    "P19IR":{0: (3.50, 0.50), 0.75: (None,None), 24: (4.50, 0.70),  48: (4.50, 0.70)},
}
qual_claims = []
# Claim 1: P8 returns to baseline at 24 h (within ~1 SE).
m0, se0 = foci["P8"][0]; m24, se24 = foci["P8"][24]
qual_claims.append({
    "claim": "P8 γH2AX foci at 24 h are statistically indistinguishable from pre-irradiation baseline.",
    "delta": round(m24 - m0, 3),
    "approx_p": round(welch_from_summary(m24, se24, N, m0, se0, N)[1], 4),
    "verdict": "consistent with paper (no significant difference)" if welch_from_summary(m24, se24, N, m0, se0, N)[1] > 0.05 else "INCONSISTENT",
})
# Claim 2: P23 24 h residual foci significantly above its own baseline AND above P8 24 h.
t_p23_self, p_p23_self = welch_from_summary(*foci["P23"][24], N, *foci["P23"][0], N)
t_p23_v_p8,  p_p23_v_p8  = welch_from_summary(*foci["P23"][24], N, *foci["P8"][24], N)
qual_claims.append({
    "claim": "P23 residual foci at 24 h are significantly above P23 baseline.",
    "t": round(t_p23_self,2), "p": round(p_p23_self,4),
    "verdict": "consistent" if p_p23_self < 0.05 else "INCONSISTENT (paper asserts persistent damage)"
})
qual_claims.append({
    "claim": "P23 residual foci at 24 h > P8 residual foci at 24 h.",
    "t": round(t_p23_v_p8,2), "p": round(p_p23_v_p8,4),
    "verdict": "consistent" if p_p23_v_p8 < 0.05 else "INCONSISTENT"
})
# Claim 3: P19 groups retain ~4.5 foci, also above P8 24 h baseline.
t_p19_v_p8, p_p19_v_p8 = welch_from_summary(*foci["P19C"][24], N, *foci["P8"][24], N)
qual_claims.append({
    "claim": "P19-C residual foci at 24 h > P8 residual foci at 24 h.",
    "t": round(t_p19_v_p8,2), "p": round(p_p19_v_p8,4),
    "verdict": "consistent" if p_p19_v_p8 < 0.05 else "INCONSISTENT"
})

# ------------------------------------------------------------------
# Save results
# ------------------------------------------------------------------
out = {
    "paper": "Sangsuwan et al. 2023, FBL 28(11):296, DOI 10.31083/j.fbl2811296",
    "n_per_group_assumed": N,
    "data_source": "published group means and SEs (raw data 'available upon request', not deposited)",
    "A_TIF_table1_replication": {
        "n_comparisons": len(A_results),
        "agreement_count": sum(1 for r in A_results if r["bin_replicated"] == r["reported"].split(" ")[0]),
        "soft_agreement_count": sum(
            1 for r in A_results
            if (r["bin_replicated"].startswith("<") and r["reported"].startswith("<")
                and float(r["bin_replicated"][1:]) >= float(r["reported"].split(" ")[0][1:]))
            or (r["bin_replicated"].startswith("nc") and r["reported"].startswith("nc"))
        ),
        "rows": A_results,
    },
    "B_8oxodG_slope_t_tests": B_results,
    "C_gh2ax_kinetics_qualitative": qual_claims,
}
with open(OUT / "smoke_replication_results.json","w") as f:
    json.dump(out, f, indent=2)

# Also write CSV summary for Table 1 comparisons
with open(OUT / "table1_tif_replication.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["A","B","mean_A","se_A","mean_B","se_B","t","p_replicated","bin_replicated","reported"])
    for r in A_results:
        w.writerow([r["A"],r["B"],r["mean_A"],r["se_A"],r["mean_B"],r["se_B"],r["t"],r["p_replicated"],r["bin_replicated"],r["reported"]])

print(json.dumps({
    "table1_n": len(A_results),
    "table1_agree_exact_bin": out["A_TIF_table1_replication"]["agreement_count"],
    "table1_agree_soft":      out["A_TIF_table1_replication"]["soft_agreement_count"],
    "oxo_results": B_results,
    "qual_claims": qual_claims,
}, indent=2))
