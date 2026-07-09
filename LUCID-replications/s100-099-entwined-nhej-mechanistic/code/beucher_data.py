"""
Beucher et al. 2009 (EMBO J 28:3413-3427) γ-H2AX foci-per-cell kinetics
after 2 Gy Cs-137 in G2-synchronised cells, normalised to the 0.5 h
post-irradiation value (the convention used by Ingram et al. 2019,
Fig. 3, who themselves digitised these points with WebPlotDigitizer).

The exact per-point values are NOT in the replicated paper's source PDF
and have NOT been published in tabular form by Beucher et al.  The
values below are best-effort approximations of the published bar/line
positions in Beucher Fig. 1B and Ingram Fig. 3 (the same panels Ingram
digitised) and are used here as a TEMPLATE reference dataset so that
the goodness-of-fit machinery can be exercised.  They MUST be replaced
by a fresh WebPlotDigitizer pass on the actual Beucher Fig. 1B for any
quantitative agreement claim — see report/REPORT.md "Reproducibility
blockers" section.

Time points are hours post-irradiation.  Values are fraction of the
0.5 h foci count remaining (i.e. 1.0 at t=0.5 h, smaller later).
"""

# Hours post-irradiation
TIMES_H = [0.5, 1.0, 2.0, 4.0, 6.0, 8.0]

# Self-normalised residual γ-H2AX foci  (1.0 at 0.5 h)
# Sources: Beucher 2009 Fig 1B C2886 WT-HF, 2BN XLF-/-, Lig4-/- MEF
# (digitised in Ingram 2019 Fig 3).  These are approximations.
BEUCHER = {
    "HF_WT":   [1.00, 0.78, 0.45, 0.22, 0.13, 0.08],
    "MEF_WT":  [1.00, 0.80, 0.50, 0.27, 0.16, 0.10],
    "XLF":     [1.00, 0.88, 0.66, 0.42, 0.28, 0.20],
    "Lig4":    [1.00, 0.92, 0.78, 0.55, 0.42, 0.34],
}

# Per-point SEM (approximate; ±0.05 typical in literature)
BEUCHER_SEM = {k: [0.05] * len(TIMES_H) for k in BEUCHER}
