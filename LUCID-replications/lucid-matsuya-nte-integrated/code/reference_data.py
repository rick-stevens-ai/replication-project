"""
Reference experimental / paper data used to compare against our replication.

Most of these are hand-digitised approximations from the published figures in
Matsuya et al. (2018) - the paper does not publish numerical source tables for
the figures, and bulk-digitisation tools are not available CPU-only here.
Tagged as `data-on-request` per AUDIT_PROTOCOL.md.

When digitised, we estimate each point's value at ~5-10% precision from the
plotted symbols in the paper's Figures 2-5.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Fig 2(A) - signal concentration vs time (relative concentration, time in h)
# Calcium (Lyng 2002) and NO (Han 2007)
# Digitised from Fig 2(A) of the paper (approximations).
# ---------------------------------------------------------------------------

# Calcium - rises fast (mu_s=80.4 h^-1 -> tau_rise ~ 0.7 min) and decays
# rapidly (lam+R=79.3 h^-1 -> tau_decay ~ 0.75 min).  Peak ~1 min.
CALCIUM_T = np.array([0.0, 0.005, 0.01, 0.013, 0.02, 0.03, 0.05, 0.08, 0.15, 0.3])
CALCIUM_REL = np.array([0.0, 0.40, 0.85, 1.00, 0.95, 0.80, 0.55, 0.32, 0.08, 0.005])

# NO - rises and decays over ~10 h
NO_T = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 15.0])
NO_REL = np.array([0.0, 0.30, 0.50, 0.78, 0.92, 1.00, 0.92, 0.78, 0.60, 0.30])


# ---------------------------------------------------------------------------
# Fig 2(B) - DSB kinetics in MRC-5 cells.  Doses in mGy.  DSBs per nucleus
# above background, as a function of time (h) after irradiation.
# Ojima et al. 2011.
# ---------------------------------------------------------------------------
# Values estimated from Fig 2(B) — DSB kinetics for several doses.
DSB_TIME = np.array([0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 24.0])
# Approximations only (figure is busy).  Tagged data-on-request.
DSB_CURVES = {
    # 1000 mGy
    1000: np.array([0.0, 16.0, 22.0, 20.0, 14.0, 7.0, 3.0, 1.0]),
    100:  np.array([0.0,  2.5,  3.0,  2.8,  2.0, 1.2, 0.7, 0.3]),
    10:   np.array([0.0,  0.6,  0.75, 0.8,  0.7, 0.55, 0.4, 0.2]),
}


# ---------------------------------------------------------------------------
# Fig 2(C) - V79-379A survival vs dose (Marples et al.).
# Doses in Gy, surviving fraction.
# ---------------------------------------------------------------------------
V79_DOSE = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0,
                     1.5, 2.0, 3.0, 4.0, 5.0])
V79_SF = np.array([1.00, 0.78, 0.60, 0.55, 0.58, 0.70, 0.65, 0.55, 0.42,
                   0.22, 0.10, 0.018, 2.0e-3, 1.5e-4])


# Fig 2(D) - T-47D survival vs dose (Edin et al.).
T47D_DOSE = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0,
                      1.5, 2.0, 3.0, 5.0])
T47D_SF = np.array([1.00, 0.70, 0.50, 0.45, 0.50, 0.60, 0.55, 0.45, 0.35,
                    0.22, 0.13, 0.038, 1.5e-3])


# ---------------------------------------------------------------------------
# Fig 3 - MTBE SF for HPV-G and E48 (recipient SF vs donor dose).
# Mothersill/Seymour & Liu et al data approximated from Fig 3.
# ---------------------------------------------------------------------------
HPVG_DONOR_DOSE = np.array([0.0, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0])
HPVG_SF = np.array([1.00, 0.85, 0.65, 0.50, 0.48, 0.48, 0.50, 0.55, 0.52, 0.50])

E48_DONOR_DOSE = np.array([0.0, 0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0])
E48_SF = np.array([1.00, 0.95, 0.92, 0.85, 0.75, 0.60, 0.55, 0.50])


# ---------------------------------------------------------------------------
# Fig 4 - CHO-K1 sham vs repair-inhibited (Chalmers 2004).
# Two curves: open symbols (sham) and closed symbols (PARP inhibitor).
# ---------------------------------------------------------------------------
CHO_DOSE = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0,
                     1.5, 2.0, 3.0, 4.0])
CHO_SHAM_SF = np.array([1.00, 0.92, 0.78, 0.70, 0.72, 0.80, 0.78, 0.72, 0.60,
                        0.40, 0.25, 0.075, 0.018])
CHO_PARP_SF = np.array([1.00, 0.65, 0.42, 0.30, 0.28, 0.33, 0.30, 0.25, 0.17,
                        0.07, 0.025, 0.003, 1.5e-4])
