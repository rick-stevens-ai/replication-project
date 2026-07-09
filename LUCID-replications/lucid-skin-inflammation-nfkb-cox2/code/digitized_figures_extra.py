"""
Additional digitizations for Acheva et al. 2017 (NF-kB / COX-2 / 3D skin).
Covers the wet-lab summary bar charts that were NOT in the original
digitized_figures.py: Fig 3C, 3E, 4B, 5B, 5C, 6D, 6E, 6F, 7B.

All values are visual reads of the published PDF bar charts via a
multimodal LLM (Argo Claude Sonnet 4.6) cross-checked against figure
captions. These are NOT raw data — the authors deposited no raw
densitometry, IHC ROI stacks, or ELISA OD plate reads. These
digitizations are explicitly intended only for the statistical-
consistency audit (do the printed asterisks survive a recomputed
Tukey HSD on the printed means/SEMs?), not as a re-analysis of
the underlying biology.

Captions consulted (verbatim):
 - Fig 3: "Error bars—SEM; **p < 0.01; ***p < 0.001, one-way ANOVA, Tukey posttest."
   (No explicit n; the paper's other 3D culture experiments are n=2.)
 - Fig 4: "Results are arithmetical mean from two independent experiments.
   Each condition in these experiments had two replicate samples;
   error bars—SEM." (NO asterisks marked in caption — descriptive only.)
 - Fig 5: "Results are arithmetical mean from two independent experiments.
   Each condition in these experiments had two replicate samples;
   error bars—SEM." (NO asterisks marked in caption — descriptive only.)
 - Fig 6: "Results are arithmetical mean from two independent experiments.
   *p < 0.05; **p < 0.01; ***p < 0.001, one-way ANOVA, Tukey posttest."
 - Fig 7: "***p < 0.001, one-way ANOVA, Tukey posttest." (n implicit, n=2)
"""
from __future__ import annotations
from digitized_figures import Bar

# -----------------------------------------------------------------
# Figure 3C — K1 immunofluorescence quantification
# Y-axis: "% K1 positive area of the raft culture" (best-read label)
# n = 2 (assumed from elsewhere in paper; Fig3 caption omits explicit n)
# -----------------------------------------------------------------
FIG3C_K1 = [
    Bar("CTRL",                12.0, 1.5, 2),
    Bar("2 Gy",                 8.0, 1.5, 2),
    Bar("2 Gy Shielded",       17.0, 2.5, 2),
    Bar("sc-236",               6.0, 1.5, 2),
    Bar("2 Gy + sc-236",       10.0, 2.0, 2),
    Bar("2 Gy Shield + sc-236",10.0, 2.0, 2),
]
# Reported asterisks (read from figure):
#   CTRL vs 2 Gy Shielded:           **
#   2 Gy Shielded vs Shield+sc-236:  **
FIG3C_REPORTED_SIG = [
    ("CTRL",         "2 Gy Shielded",          "**"),
    ("2 Gy Shielded","2 Gy Shield + sc-236",   "**"),
]

# -----------------------------------------------------------------
# Figure 3E — FLG immunofluorescence quantification
# -----------------------------------------------------------------
FIG3E_FLG = [
    Bar("CTRL",                11.0, 1.0, 2),
    Bar("2 Gy",                 2.0, 0.5, 2),
    Bar("2 Gy Shielded",        2.5, 0.5, 2),
    Bar("sc-236",               7.0, 1.5, 2),
    Bar("2 Gy + sc-236",        1.5, 0.5, 2),
    Bar("2 Gy Shield + sc-236", 2.0, 0.5, 2),
]
FIG3E_REPORTED_SIG = [
    ("CTRL", "2 Gy",                  "***"),
    ("CTRL", "2 Gy Shielded",         "***"),
    ("CTRL", "sc-236",                "**"),
    ("CTRL", "2 Gy Shield + sc-236",  "*"),
]

# -----------------------------------------------------------------
# Figure 4B — densitometry of p-p65 and p-p38 (Bay 11-7085)
# n = 2 per condition. CAPTION HAS NO ASTERISKS — descriptive only.
# Audit goal: TREND check only (does 2Gy increase p-p65 vs CTRL?
# does Bay 1uM + 2Gy knock it back down? does 2Gy increase p-p38?)
# -----------------------------------------------------------------
FIG4B_PP65 = [
    Bar("CTRL",                 0.01, 0.005, 2),
    Bar("Bay 1 uM",             0.02, 0.005, 2),
    Bar("2 Gy + Bay 1 uM",      0.03, 0.010, 2),
    Bar("2 Gy",                 0.75, 0.20,  2),
]
FIG4B_PP38 = [
    Bar("CTRL",                 0.60, 0.15, 2),
    Bar("Bay 1 uM",             0.55, 0.10, 2),
    Bar("2 Gy + Bay 1 uM",      0.15, 0.05, 2),
    Bar("2 Gy",                 0.30, 0.10, 2),
]

# -----------------------------------------------------------------
# Figure 5B — COX-2 densitometry vs Bay dose ladder (4h post 2Gy)
# n = 2 per condition. CAPTION HAS NO ASTERISKS — descriptive only.
# Audit goal: dose-response monotonicity (Bay dose ladder under 2Gy
# should monotonically decrease COX-2).
# -----------------------------------------------------------------
FIG5B_COX2 = [
    Bar("Bay 0 (no IR)",        0.80, 0.10, 2),
    Bar("Bay 1 (no IR)",        0.70, 0.15, 2),
    Bar("Bay 0 + 2 Gy",         0.60, 0.10, 2),
    Bar("Bay 1 + 2 Gy",         0.50, 0.10, 2),
    Bar("Bay 5 + 2 Gy",         0.30, 0.05, 2),
    Bar("Bay 10 + 2 Gy",        0.20, 0.05, 2),
]

# -----------------------------------------------------------------
# Figure 5C — p-p65 densitometry vs Bay dose ladder
# n = 2. Descriptive only. Audit: dose-response monotonicity under 2Gy.
# -----------------------------------------------------------------
FIG5C_PP65 = [
    Bar("Bay 0 (no IR)",        0.20, 0.03, 2),
    Bar("Bay 1 (no IR)",        0.10, 0.02, 2),
    Bar("Bay 0 + 2 Gy",         0.30, 0.05, 2),
    Bar("Bay 1 + 2 Gy",         0.25, 0.05, 2),
    Bar("Bay 5 + 2 Gy",         0.20, 0.04, 2),
    Bar("Bay 10 + 2 Gy",        0.15, 0.03, 2),
]

# -----------------------------------------------------------------
# Figure 6D — cornified layer thickness with Bay 11-7085
# Y: thickness (microns). n = 2.
# -----------------------------------------------------------------
FIG6D_THICKNESS = [
    Bar("CTRL",                3.8, 0.4, 2),
    Bar("2 Gy",                2.2, 0.3, 2),
    Bar("2 Gy Shielded",       4.8, 0.3, 2),
    Bar("Bay 11-7085",         1.8, 0.3, 2),
    Bar("2 Gy + Bay",          2.0, 0.3, 2),
    Bar("2 Gy Shield + Bay",   3.2, 0.4, 2),
]
FIG6D_REPORTED_SIG = [
    ("CTRL",        "2 Gy Shielded",       "***"),
    ("2 Gy",        "2 Gy Shielded",       "**"),
    ("2 Gy Shielded","2 Gy Shield + Bay",  "**"),
    ("CTRL",        "2 Gy + Bay",          "**"),
]

# -----------------------------------------------------------------
# Figure 6E — K1 quantification with Bay
# -----------------------------------------------------------------
FIG6E_K1 = [
    Bar("CTRL",                20.0, 1.5, 2),
    Bar("2 Gy",                13.0, 2.0, 2),
    Bar("2 Gy Shielded",       15.0, 1.5, 2),
    Bar("Bay 11-7085",          5.5, 1.0, 2),
    Bar("2 Gy + Bay",           6.5, 1.0, 2),
    Bar("2 Gy Shield + Bay",   16.5, 2.5, 2),
]
FIG6E_REPORTED_SIG = [
    ("CTRL", "Bay 11-7085",       "*"),
    ("CTRL", "2 Gy + Bay",        "***"),  # vision read ambiguous; will recompute both candidates
]

# -----------------------------------------------------------------
# Figure 6F — FLG quantification with Bay
# -----------------------------------------------------------------
FIG6F_FLG = [
    Bar("CTRL",                12.0, 1.5, 2),
    Bar("2 Gy",                 8.0, 1.5, 2),
    Bar("2 Gy Shielded",        7.0, 1.0, 2),
    Bar("Bay 11-7085",          9.5, 1.5, 2),
    Bar("2 Gy + Bay",           6.5, 1.0, 2),
    Bar("2 Gy Shield + Bay",    2.0, 0.5, 2),
]
FIG6F_REPORTED_SIG = [
    ("CTRL",        "2 Gy Shield + Bay", "**"),
    ("Bay 11-7085", "2 Gy Shield + Bay", "*"),
]

# -----------------------------------------------------------------
# Figure 7B — PGE2 with sc-236 across 0/24/48/72h timecourse
# n = 2. Caption mentions only "***p<0.001"; printed *** marks the
# 72h 2Gy bar getting knocked down by sc-236.
# -----------------------------------------------------------------
FIG7B_BARS = [
    Bar("0h CTRL sc0",     50.0,  20.0, 2),
    Bar("0h CTRL sc5",     30.0,  15.0, 2),
    Bar("0h 2Gy sc0",      30.0,  15.0, 2),
    Bar("0h 2Gy sc5",      20.0,  10.0, 2),
    Bar("24h CTRL sc0",    50.0,  20.0, 2),
    Bar("24h CTRL sc5",    30.0,  15.0, 2),
    Bar("24h 2Gy sc0",     50.0,  20.0, 2),
    Bar("24h 2Gy sc5",     30.0,  15.0, 2),
    Bar("48h CTRL sc0",    50.0,  20.0, 2),
    Bar("48h CTRL sc5",    30.0,  15.0, 2),
    Bar("48h 2Gy sc0",     80.0,  30.0, 2),
    Bar("48h 2Gy sc5",     40.0,  15.0, 2),
    Bar("72h CTRL sc0",   100.0,  30.0, 2),
    Bar("72h CTRL sc5",    60.0,  20.0, 2),
    Bar("72h 2Gy sc0",   1500.0, 150.0, 2),
    Bar("72h 2Gy sc5",     50.0,  20.0, 2),
]
FIG7B_REPORTED_SIG = [
    ("72h 2Gy sc0", "72h 2Gy sc5", "***"),
]
