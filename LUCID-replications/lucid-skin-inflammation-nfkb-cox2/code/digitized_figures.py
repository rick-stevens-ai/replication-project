"""
Digitized values from Acheva et al. 2017 Frontiers in Immunology
(doi: 10.3389/fimmu.2017.00082) — Figures 1, 2, and 7.

Values were read visually from the published figures (open-access PDF).
Means and SEM are best-effort estimates from gridlines and error-bar heights.
The N (sample size) and statistical test are quoted verbatim from each figure
caption.

These are NOT raw experimental data. They are reconstructions of the published
summary statistics for the purpose of (a) sanity-checking the printed
significance asterisks and (b) computing derived quantities (IC50, fold-change)
that the authors did not state explicitly.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Bar:
    label: str
    mean: float
    sem: float            # standard error of the mean
    n: int                # sample size from caption


# -------------------------------------------------------------------------
# Figure 1: COX-2 mRNA fold-change (qRT-PCR, 2^-ddCT relative to 18S rRNA)
# Caption: "(n = 3) ... one-way ANOVA Tukey posttest; **p < 0.01;
#           ***p < 0.001; *p < 0.05."
# Two grouped conditions: 2 Gy Shielded vs 2 Gy Irradiated
# -------------------------------------------------------------------------
FIG1_SHIELDED: List[Bar] = [
    Bar("CTRL",          1.00, 0.08, 3),
    Bar("2 h",           0.70, 0.15, 3),
    Bar("4 h",           0.40, 0.12, 3),   # downregulation in shielded area
    Bar("4 h + sc-236",  1.00, 0.38, 3),
    Bar("24 h",          0.60, 0.12, 3),
]

FIG1_IRRADIATED: List[Bar] = [
    Bar("CTRL",          1.00, 0.08, 3),
    Bar("2 h",           1.15, 0.20, 3),
    Bar("4 h",           2.40, 0.25, 3),   # peak ~2.5x reported in text
    Bar("4 h + sc-236",  0.50, 0.30, 3),   # <0.5 of control per text
    Bar("24 h",          0.90, 0.18, 3),
]

# Asterisks reported by authors (in irradiated arm):
#   CTRL vs 4h: ***   2h vs 4h: **   4h vs 4h+sc-236: *   4h vs 24h: **
FIG1_REPORTED_SIG = [
    ("irradiated:CTRL",        "irradiated:4 h",          "***"),
    ("irradiated:2 h",         "irradiated:4 h",          "**"),
    ("irradiated:4 h",         "irradiated:4 h + sc-236", "*"),
    ("irradiated:4 h",         "irradiated:24 h",         "**"),
]


# -------------------------------------------------------------------------
# Figure 2: MTT cytotoxicity (n = 2; ANOVA Tukey, SEM error bars)
# Y-axis: % viability relative to control
# Panel A: sc-236   Panel B: Bay 11-7085
# -------------------------------------------------------------------------
FIG2A_SC236: List[Bar] = [
    Bar("0",     100.0, 0.0, 2),
    Bar("DMSO",   92.0, 7.0, 2),
    Bar("5",      93.0, 5.0, 2),
    Bar("10",     74.0, 3.0, 2),
    Bar("15",     54.0, 1.0, 2),
    Bar("25",     10.0, 4.5, 2),
]
# Reported asterisks (all vs control, 0):  10:*  15:**  25:***

FIG2B_BAY: List[Bar] = [
    Bar("0",     100.0, 0.0, 2),
    Bar("DMSO",   92.0, 7.0, 2),
    Bar("1",      74.0, 16.5, 2),
    Bar("5",      35.0, 1.5, 2),
    Bar("10",     12.0, 4.5, 2),
]
# Reported asterisks (all vs control, 0):  5:*  10:**   (1: NS)


# -------------------------------------------------------------------------
# Figure 7: PGE2 ELISA (n = 2; ANOVA Tukey, SEM error bars)
# Y-axis: pg/ml
# Panel A: 0/24/48/72 h, CTRL vs 2 Gy
# Panel B: same time courses with sc-236 5 uM inhibitor
# -------------------------------------------------------------------------
FIG7A_CTRL = [
    Bar("0 h",   250.0, 250.0, 2),  # SEM nearly equals mean — very noisy
    Bar("24 h",  250.0, 100.0, 2),
    Bar("48 h",   80.0,  20.0, 2),
    Bar("72 h",  250.0,  60.0, 2),
]

FIG7A_2GY = [
    Bar("0 h",    15.0,  10.0, 2),
    Bar("24 h",   15.0,  10.0, 2),
    Bar("48 h",   10.0,   5.0, 2),
    Bar("72 h", 1600.0, 100.0, 2),  # *** vs control 72h per caption
]

# Reported quantitative claim (text):
#   "At 72 h ... the COX-2 product's levels were significantly elevated
#    (6.5 times higher than in the initial levels of the non-irradiated
#    3D cultures medium)."
FIG7_CLAIM_FOLD_72H = 6.5


def all_data() -> Dict[str, list]:
    return dict(
        fig1_shielded=FIG1_SHIELDED,
        fig1_irradiated=FIG1_IRRADIATED,
        fig2a_sc236=FIG2A_SC236,
        fig2b_bay=FIG2B_BAY,
        fig7a_ctrl=FIG7A_CTRL,
        fig7a_2gy=FIG7A_2GY,
    )


if __name__ == "__main__":
    import json
    out = {k: [b.__dict__ for b in v] for k, v in all_data().items()}
    out["fig7_claim_fold_72h"] = FIG7_CLAIM_FOLD_72H
    out["fig1_reported_sig"] = FIG1_REPORTED_SIG
    print(json.dumps(out, indent=2))
