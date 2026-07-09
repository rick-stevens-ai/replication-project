"""
Digitized data points from Figure 5 of Fukui et al. 2022 (Sci Rep).
Y-axis = surviving fraction (log), X-axis = dose (Gy).

These are READ FROM THE PUBLISHED FIGURE BY VISUAL ESTIMATION using a
vision model.  Uncertainties are large (factor of ~1.5 on each point
in log space).  See README for caveats.
"""

# (dose_Gy, surviving_fraction)
FIG5_DATA = {
    # Panel A
    "SAS":    [(0, 1.0), (2, 0.50), (4, 0.20), (6, 0.040),
               (8, 0.012), (10, 0.0022), (12, 0.00030), (15, 0.000018)],
    "SAS-R":  [(0, 1.0), (2, 0.75), (4, 0.28), (6, 0.050),
               (8, 0.018), (10, 0.0042), (12, 0.0014), (15, 0.000070)],

    # Panel B
    "HSC2":   [(0, 1.0), (1, 0.78), (2, 0.50), (3, 0.14),
               (4, 0.035), (6, 0.0015)],
    "HSC2-R": [(0, 1.0), (1, 0.85), (2, 0.50), (3, 0.25),
               (4, 0.12), (6, 0.060), (8, 0.0080),
               (10, 0.0012), (12, 0.00050), (15, 0.00022)],
}

# Paper-reported R^2 for the IMK model vs. these experimental points:
FIG5_REPORTED_R2 = {"A_SAS_family": 0.898, "B_HSC2_family": 0.916}
