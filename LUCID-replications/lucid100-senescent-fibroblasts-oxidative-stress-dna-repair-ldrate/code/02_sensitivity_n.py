#!/usr/bin/env python3
"""
Sensitivity: for the TIF Table 1 and 8-oxo-dG slope tests, search the
minimum effective n (cells/wells/weeks) needed to reproduce each reported
significance bin, given the published mean and SE. This pins down what
the paper's effective sample size MUST have been for the printed p-values
to be internally consistent.
"""
import json, math
from pathlib import Path
from scipy import stats

OUT = Path(__file__).resolve().parent.parent / "results"

def welch_p(m1, se1, n1, m2, se2, n2):
    # Treat se as SE of the mean; sd_i = se_i * sqrt(n_i_pub) but we
    # vary the *effective* n while keeping the *reported sd* constant
    # by inverting se -> sd assuming the original n_pub=3.
    sd1 = se1 * math.sqrt(3); sd2 = se2 * math.sqrt(3)
    s1 = sd1**2 / n1; s2 = sd2**2 / n2
    se_diff = math.sqrt(s1 + s2)
    t = (m1 - m2) / se_diff
    df = (s1 + s2)**2 / ((s1**2)/(n1-1) + (s2**2)/(n2-1))
    return 2 * (1 - stats.t.cdf(abs(t), df))

def bin_p(p):
    if p < 0.0001: return "<0.0001"
    if p < 0.001:  return "<0.001"
    if p < 0.01:   return "<0.01"
    if p < 0.05:   return "<0.05"
    return f"nc(p={p:.3f})"

# Same data as 01_smoke_replication.py — limited subset of strongest claims.
tif = {
    "P8_C":   (1.91, 0.45), "P8_1Gy48h":   (3.88, 0.42),
    "P19C_C": (7.95, 1.13), "P19C_1Gy48h": (10.71, 1.58),
    "P19IR_C":(12.32,1.52), "P19IR_1Gy48h":(14.75, 1.91),
    "P19ST_C":(11.55,1.29), "P19ST_1Gy48h":(16.33, 2.26),
    "P23_C":  (18.27,2.72), "P23_1Gy48h":  (28.55, 2.55),
}
oxo = {
    "P8_C":(16,4),"P8_LDR":(27,7),"P13_C":(26,5),"P13_LDR":(45,10),
}

probes = [
    ("TIF: P8 1Gy 48h vs P19C 1Gy 48h", tif["P8_1Gy48h"], tif["P19C_1Gy48h"], "<0.001"),
    ("TIF: P8 1Gy 48h vs P23 1Gy 48h",  tif["P8_1Gy48h"], tif["P23_1Gy48h"],  "<0.0001"),
    ("TIF: P19C C vs P19IR C",           tif["P19C_C"],    tif["P19IR_C"],     "<0.05"),
    ("TIF: P19ST C vs P19ST 1Gy 48h",    tif["P19ST_C"],   tif["P19ST_1Gy48h"],"<0.05"),
    ("8oxo: P8 C vs P8 LDR",             oxo["P8_C"],      oxo["P8_LDR"],      "<0.01"),  # paper p=0.003 ~ "<0.01"
    ("8oxo: P8 LDR vs P13 LDR",          oxo["P8_LDR"],    oxo["P13_LDR"],     "<0.05"),  # paper p=0.035
    ("8oxo: P8 C vs P13 C",              oxo["P8_C"],      oxo["P13_C"],       "<0.05"),  # paper p=0.045
]

THRESH = {"<0.0001":0.0001, "<0.001":0.001, "<0.01":0.01, "<0.05":0.05}

rows = []
for label, (m1,se1), (m2,se2), reported_bin in probes:
    target = THRESH[reported_bin]
    # find smallest n in [3..200] s.t. p < target
    min_n = None
    for n in range(3, 201):
        p = welch_p(m1, se1, n, m2, se2, n)
        if p < target:
            min_n = n
            break
    rows.append({
        "comparison": label,
        "mean_A": m1, "se_A": se1, "mean_B": m2, "se_B": se2,
        "reported_bin": reported_bin,
        "p_at_n3": round(welch_p(m1, se1, 3, m2, se2, 3), 4),
        "p_at_n10": round(welch_p(m1, se1, 10, m2, se2, 10), 4),
        "p_at_n24": round(welch_p(m1, se1, 24, m2, se2, 24), 4),
        "p_at_n100": round(welch_p(m1, se1, 100, m2, se2, 100), 6),
        "min_effective_n_to_match_reported_bin": min_n,
    })

with open(OUT/"sensitivity_n.json","w") as f:
    json.dump({"note":"effective n required for printed p-values to be reproducible from published mean±SE", "rows": rows}, f, indent=2)
print(json.dumps(rows, indent=2))
