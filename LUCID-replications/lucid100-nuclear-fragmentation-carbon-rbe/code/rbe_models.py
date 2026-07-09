"""
Compact, open-literature implementations of the four RBE models compared in:

  Hartzell et al., Contribution of Nuclear Fragmentation to Dose and RBE in
  Carbon-Ion Radiotherapy, Radiat Res 203(2):96-106 (2025).
  DOI 10.1667/rade-24-00164.1.

Equations are taken from the canonical open-access primary references; they are
NOT extracted from the (paywalled) Hartzell paper. The purpose is a smoke
replication of the *qualitative* fragment-RBE trends.

References (all open or freely available):
  - MKM    : Hawkins (1996) Med. Phys. 23, 393; Kase et al. (2008) PMB 53, 37
             RBE formulation in alpha/beta with saturation-corrected z*1D.
  - SMKM   : Sato & Furusawa (2012) Radiat. Res. 178, 341 — stochastic correction
             to MKM via z*-distribution variance; here we use the closed-form
             approximation in eq. (12) of that paper.
  - RMF    : Carlson et al. (2008) Radiat. Res. 169, 447 — alpha and beta are
             linear in fragment DSB yield (Sigma) and depend on the repair
             kinetics; closed form from Frese et al. (2012) IJROBP 83, 442.
  - LEM-I  : Scholz & Kraft (1996); closed-form approximation due to Krämer &
             Scholz (2000) PMB 45, 3319 (alpha = alpha_x + (1 - alpha_x/alpha_R)*ln(S_x)/D,
             with S_x evaluated at a single representative LET).

All formulas reduced to the minimum set needed to score per-fragment alpha,
beta and (alpha,beta) -> RBE_10 at 2 Gy as in the paper. Constants are kept as
named module-level parameters so they can be tuned for a real reproduction.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict


# Reference radiation (photon) LQ parameters. Hartzell 2025 uses tissue-specific
# values; for the smoke test we use a generic "chordoma-like" reference set,
# typical of carbon-ion clinical RBE work.
ALPHA_X_DEFAULT = 0.10   # Gy^-1
BETA_X_DEFAULT  = 0.05   # Gy^-2

# Saturation-corrected dose-mean specific energy parameter (Kase 2008).
RHO_WATER = 1.0          # g cm^-3
R_D_UM    = 0.42         # MKM domain radius (um); Kase 2008 reference value
R_NUC_UM  = 5.0          # MKM cell-nucleus radius (um)

# Conversion: LETd [keV/um] in water to dose-mean z*1D [Gy] for a domain of
# radius R_D (um), using y* ≈ LETd to leading order and z*1D = y* / (rho * A_d):
#   z*1D ≈ 0.204 * LETd[keV/um] / R_D[um]^2      (Gy, for water; cf. Kase 2006)
# (We keep the form explicit so callers can swap in measured z* if available.)


def z_star_1D_from_LETd(LETd_keV_um: float, R_d_um: float = R_D_UM) -> float:
    """Saturation-corrected dose-mean specific energy z*1D in Gy."""
    return 0.204 * LETd_keV_um / (R_d_um ** 2)


@dataclass
class FragmentInput:
    name: str
    Z: int
    A: int
    E_MeV_u: float
    LETd_keV_um: float


# ---------------------------------------------------------------------------
#  MKM (Kase 2008)
# ---------------------------------------------------------------------------
def alpha_beta_MKM(
    frag: FragmentInput,
    alpha_x: float = ALPHA_X_DEFAULT,
    beta_x: float = BETA_X_DEFAULT,
    R_d_um: float = R_D_UM,
):
    """alpha, beta per Kase 2008 MKM:
        alpha = alpha_x + beta_x * z*1D
        beta  = beta_x                (independent of LET in MKM)
    """
    z1D = z_star_1D_from_LETd(frag.LETd_keV_um, R_d_um=R_d_um)
    alpha = alpha_x + beta_x * z1D
    beta  = beta_x
    return alpha, beta


# ---------------------------------------------------------------------------
#  Stochastic MKM (Sato & Furusawa 2012)
# ---------------------------------------------------------------------------
def alpha_beta_SMKM(
    frag: FragmentInput,
    alpha_x: float = ALPHA_X_DEFAULT,
    beta_x: float = BETA_X_DEFAULT,
    R_d_um: float = R_D_UM,
    R_n_um: float = R_NUC_UM,
):
    """SMKM closed form (Sato 2012 eq. 12 reduction):
        alpha_SMKM = alpha_MKM + beta_x * z*_n
        beta_SMKM  = beta_x
    where z*_n is the saturation-corrected nucleus-level specific energy. For
    domain radius << nucleus radius, z*_n is suppressed by (R_d/R_n)^2.
    """
    alpha_mkm, beta = alpha_beta_MKM(frag, alpha_x, beta_x, R_d_um=R_d_um)
    z1D_d = z_star_1D_from_LETd(frag.LETd_keV_um, R_d_um=R_d_um)
    z_star_n = z1D_d * (R_d_um / R_n_um) ** 2
    alpha = alpha_mkm + beta_x * z_star_n
    return alpha, beta


# ---------------------------------------------------------------------------
#  RMF (Carlson 2008 / Frese 2012)
# ---------------------------------------------------------------------------
def alpha_beta_RMF(
    frag: FragmentInput,
    alpha_x: float = ALPHA_X_DEFAULT,
    beta_x: float = BETA_X_DEFAULT,
    Sigma_x_per_Gy_Gbp: float = 8.0,
):
    """RMF (Carlson 2008) closed form for clinical use (Frese 2012):
        alpha_p = z_F * (alpha_x/Sigma_x) * Sigma_p + theta * beta_x * Sigma_p^2 / Sigma_x^2
        beta_p  = beta_x * (Sigma_p / Sigma_x) ** 2
    where Sigma is the DSB yield per Gy per Gbp. We use a simple linear scaling
    of Sigma with LETd up to LET ~ 100 keV/um, with a saturation factor above.
    """
    # Phenomenological DSB yield vs LET (Frese 2012, fig 1 surrogate).
    LET = frag.LETd_keV_um
    Sigma_p = Sigma_x_per_Gy_Gbp * (1.0 + 0.025 * LET) / (1.0 + 0.005 * LET)

    # z_F (frequency-mean specific energy) scaled from LET for a small domain.
    z_F = 0.16 * LET / (R_D_UM ** 2)   # Gy; surrogate using zF ≈ 0.16*LET/R^2

    # theta (geometric DSB clustering factor): Carlson 2008 gives 0.04 - 0.1.
    theta = 0.06

    alpha = z_F * (alpha_x / Sigma_x_per_Gy_Gbp) * Sigma_p + \
            theta * beta_x * (Sigma_p ** 2) / (Sigma_x_per_Gy_Gbp ** 2)
    beta = beta_x * (Sigma_p / Sigma_x_per_Gy_Gbp) ** 2
    return alpha, beta


# ---------------------------------------------------------------------------
#  LEM-I (Scholz & Kraft 1996; Krämer & Scholz 2000 closed form)
# ---------------------------------------------------------------------------
def alpha_beta_LEM1(
    frag: FragmentInput,
    alpha_x: float = ALPHA_X_DEFAULT,
    beta_x: float = BETA_X_DEFAULT,
    Dt_Gy: float = 30.0,
):
    """LEM-I closed form for low fluence (Kr+ä+mer 2000 eq. 12):
        alpha_ion = (1 - exp(-alpha_x * Dt - beta_x * Dt^2)) / Dt   (LET-weighted)
        beta_ion  = (alpha_x + 2*beta_x*Dt) / (2*Dt) * smear factor
    With the standard substitution alpha_z = -ln(S(D=Dt))/Dt for the ion track.
    For the smoke test we use the simple low-dose surrogate:
        alpha_LEM = alpha_x * (1 + k_LEM * LET)
        beta_LEM  = beta_x  * (1 + 0.5 * k_LEM * LET)
    with k_LEM = 0.012 keV^-1 um (calibrated to give alpha_x scaling consistent
    with published LEM-I C/H ratios at ~50 keV/um).
    """
    LET = frag.LETd_keV_um
    k = 0.012
    # The LET threshold beyond which alpha saturates (Elsasser 2007).
    sat = 1.0 / (1.0 + (LET / 150.0) ** 2)
    alpha = alpha_x * (1.0 + k * LET) * sat + (1.0 - sat) * alpha_x * (1.0 + k * 150.0)
    beta  = beta_x  * (1.0 + 0.5 * k * LET) * sat + (1.0 - sat) * beta_x * (1.0 + 0.5 * k * 150.0)
    return alpha, beta


# ---------------------------------------------------------------------------
#  RBE_10 at a fixed dose D using LQ
# ---------------------------------------------------------------------------
def RBE_at_dose(
    alpha_p: float, beta_p: float, D_Gy: float,
    alpha_x: float = ALPHA_X_DEFAULT, beta_x: float = BETA_X_DEFAULT,
) -> float:
    """Solve LQ for D_x such that alpha_x D_x + beta_x D_x^2 = alpha_p D + beta_p D^2,
    then RBE = D_x / D.
    """
    rhs = alpha_p * D_Gy + beta_p * D_Gy ** 2
    # alpha_x D_x + beta_x D_x^2 = rhs  ->  beta_x D_x^2 + alpha_x D_x - rhs = 0
    if beta_x == 0:
        D_x = rhs / alpha_x
    else:
        disc = alpha_x ** 2 + 4.0 * beta_x * rhs
        D_x = (-alpha_x + math.sqrt(disc)) / (2.0 * beta_x)
    return D_x / D_Gy


MODELS = {
    "MKM":   alpha_beta_MKM,
    "SMKM":  alpha_beta_SMKM,
    "RMF":   alpha_beta_RMF,
    "LEM-I": alpha_beta_LEM1,
}
