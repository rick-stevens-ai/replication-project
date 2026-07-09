"""
Hand-digitised experimental data points from Qi et al. 2021 figures.

Each entry: list of (time_hours, normalised_residual_DSB_fraction) tuples.
Normalised so that 1.0 = number of foci at t~0 (i.e. peak DSB).

These are approximate digitisations from inspecting the published figures
and are intended for qualitative trend comparison only. Citations refer to
the original experimental papers cited by Qi et al.
"""

# Figure 3a — 4 Gy photon irradiation, NHLF wild-type fibroblasts,
# gamma-H2AX foci, Riballo / Beucher / Kuhne datasets pooled.
# Fraction of peak foci vs time (h).
FIG3A_4GY_PHOTON_WT = [
    (0.25, 0.95),
    (0.5,  0.78),
    (1.0,  0.58),
    (2.0,  0.38),
    (4.0,  0.22),
    (6.0,  0.16),
    (8.0,  0.12),
    (24.0, 0.06),
]

# Figure 3b — 2 Gy photon irradiation, multiple wild-type lines
FIG3B_2GY_PHOTON_WT = [
    (0.25, 0.95),
    (0.5,  0.72),
    (1.0,  0.55),
    (2.0,  0.32),
    (4.0,  0.18),
    (8.0,  0.10),
    (24.0, 0.05),
]

# Figure 4a — 4 Gy proton irradiation, wild-type lines
FIG4A_4GY_PROTON_WT = [
    (0.25, 0.93),
    (0.5,  0.72),
    (1.0,  0.52),
    (2.0,  0.30),
    (4.0,  0.18),
    (6.0,  0.13),
    (24.0, 0.05),
]

# Figure 7a — 2 Gy X-rays, Artemis-deficient (CJ179)
FIG7A_2GY_ARTEMIS_DEF = [
    (0.5, 0.78),
    (1.0, 0.62),
    (2.0, 0.48),
    (4.0, 0.30),
    (8.0, 0.22),
    (24.0, 0.18),
]

# Figure 7c — 2 Gy X-rays, XLF-deficient (2BN)
FIG7C_2GY_XLF_DEF = [
    (0.5, 0.82),
    (1.0, 0.70),
    (2.0, 0.50),
    (4.0, 0.32),
    (8.0, 0.20),
    (24.0, 0.10),
]
