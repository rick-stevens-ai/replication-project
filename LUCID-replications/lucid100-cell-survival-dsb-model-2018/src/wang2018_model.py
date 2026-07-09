"""
Replication of:
  Wang W., Li C., Qiu R., Chen Y., Wu Z., Zhang H., Li J. (2018)
  "Modelling of Cellular Survival Following Radiation-Induced DNA Double-Strand Breaks"
  Sci. Rep. 8:16202. DOI:10.1038/s41598-018-34159-3

Implements equations (1)–(20) of the paper.

The model has:
  - 2 input parameters per radiation quality:
      n_p  : avg # primary particles that cause a DSB per cell per Gy
      lam_p: avg # DSBs per primary particle that causes DSB
    Both are derived from MCDS-computed Y (DSB/cell/Gy) and lambda (DSB/track).
  - 6 fitting parameters per cell line:
      mu_x          : avg probability of correct end-joining within one DSB
                       (fidelity of NHEJ); 0 < mu_x < 1
      mu_y          : sensitivity of error repair (lethal fraction); 0 < mu_y < 1
      zeta          : overkill / clustered damage parameter (eq 11)
      xi            : intra-track DSB-pair joining parameter (eq 9)
      eta_lp_to_1   : eta(lambda_p->1)    - limit of eta(lambda_p) as lam_p -> 1
      eta_lp_to_inf : eta(lambda_p->inf)  - limit as lam_p -> inf
"""

import numpy as np
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Eq (8): functional form of eta(lambda_p)
#   eta(lam_p) = eta_inf - (eta_inf - eta_1) / lam_p
#   limits: lam_p -> 1   gives eta_1
#           lam_p -> inf gives eta_inf
# ---------------------------------------------------------------------------
def eta_of_lambda_p(lam_p, eta_1, eta_inf):
    lam_p = np.asarray(lam_p, dtype=float)
    return eta_inf - (eta_inf - eta_1) / lam_p


# ---------------------------------------------------------------------------
# Eq (7): probability a DSB end is NOT joined with an end from a different
# primary particle
# ---------------------------------------------------------------------------
def P_interaction(lam_p, n_p, eta_1, eta_inf):
    eta = eta_of_lambda_p(lam_p, eta_1, eta_inf)
    x = eta * n_p
    # Numerically safe (1 - exp(-x))/x
    out = np.where(np.abs(x) < 1e-8, 1.0 - 0.5 * x, (1.0 - np.exp(-x)) / np.where(x == 0, 1, x))
    return out


# Eq (9): probability that a DSB end is NOT joined with another DSB end from
# the same primary particle (clustered-damage handling)
def P_track(lam_p, xi):
    x = xi * np.asarray(lam_p, dtype=float)
    out = np.where(np.abs(x) < 1e-8, 1.0 - 0.5 * x, (1.0 - np.exp(-x)) / np.where(x == 0, 1, x))
    return out


# Eq (10): probability a DSB is correctly repaired
def P_correct(lam_p, n_p, mu_x, xi, eta_1, eta_inf):
    return mu_x * P_track(lam_p, xi) * P_interaction(lam_p, n_p, eta_1, eta_inf)


# Eq (11): probability a DSB has contributed to cell death (overkill)
def P_contribution(lam_p, zeta):
    x = zeta * np.asarray(lam_p, dtype=float)
    out = np.where(np.abs(x) < 1e-8, 1.0 - 0.5 * x, (1.0 - np.exp(-x)) / np.where(x == 0, 1, x))
    return out


# Eq (13)/(14)/(15): Cell survival
def survival(D, Y, lam_p, n_p, mu_x, mu_y, zeta, xi, eta_1, eta_inf):
    """
    D        : dose (Gy) — array
    Y        : DSB yield per cell per Gy (scalar, for this radiation quality)
    lam_p    : avg DSBs per primary particle that caused DSB (scalar)
    n_p      : np per Gy — when multiplied by D gives total np for that dose
                (we follow paper eq 5: np_total = (Y*D/lam_p)*(1 - exp(-lam))
                 = (Y*D)/lam_p_eff. Here we accept n_p already as the per-Gy
                 quantity n_p_perGy and total np = n_p_perGy * D )
    """
    D = np.asarray(D, dtype=float)
    N = Y * D                              # eq (1)
    np_total = n_p * D                     # total primary particles causing DSB
    Pc = P_correct(lam_p, np_total, mu_x, xi, eta_1, eta_inf)
    Pco = P_contribution(lam_p, zeta)
    Ndeath = mu_y * N * Pco * (1.0 - Pc)   # eq (13)
    return np.exp(-Ndeath)                 # eq (14)/(15)


# Eqs (18)/(19): closed-form alpha, beta in LQ limit (np small)
def alpha_beta(Y, lam_p, mu_x, mu_y, zeta, xi, eta_1, eta_inf):
    """
    Eq (18):  alpha = Y * (1 - exp(-zeta*lam_p))/(zeta*lam_p)
                     * (1 - mu_x * (1 - exp(-xi*lam_p))/(xi*lam_p)) * mu_y

    Eq (19):  beta  = (1/2) * eta(lam_p) * (Y / lam_p) * Y
                       * (1 - exp(-zeta*lam_p))/(zeta*lam_p)
                       * (1 - exp(-xi*lam_p))/(xi*lam_p)
                       * mu_x * mu_y
    """
    a_clust = (1.0 - np.exp(-zeta * lam_p)) / (zeta * lam_p)
    b_clust = (1.0 - np.exp(-xi * lam_p)) / (xi * lam_p)
    alpha = Y * a_clust * (1.0 - mu_x * b_clust) * mu_y
    eta = eta_of_lambda_p(lam_p, eta_1, eta_inf)
    beta = 0.5 * eta * (Y / lam_p) * Y * a_clust * b_clust * mu_x * mu_y
    return alpha, beta


# ---------------------------------------------------------------------------
# Eq (20): alpha/beta ratio (closed form)
# ---------------------------------------------------------------------------
def alpha_over_beta(Y, lam_p, mu_x, mu_y, zeta, xi, eta_1, eta_inf):
    alpha, beta = alpha_beta(Y, lam_p, mu_x, mu_y, zeta, xi, eta_1, eta_inf)
    return alpha / beta


# ---------------------------------------------------------------------------
# Convenience: bundle of cell-line fit parameters
# ---------------------------------------------------------------------------
@dataclass
class CellLineParams:
    name: str
    mu_x: float
    mu_y: float
    zeta: float
    xi: float
    eta_lp_to_1: float
    eta_lp_to_inf: float


# Parameters as reported by Wang 2018, Table 1
HSG_PARAMS = CellLineParams(
    name="HSG",
    mu_x=0.9817,
    mu_y=0.0891,
    zeta=0.1025,
    xi=0.0572,
    eta_lp_to_1=7.26e-4,
    eta_lp_to_inf=0.0022,
)
V79_PARAMS = CellLineParams(
    name="V79",
    mu_x=0.9568,
    mu_y=0.0300,
    zeta=0.0412,
    xi=0.0608,
    eta_lp_to_1=9.78e-4,
    eta_lp_to_inf=0.0065,
)


def cell_survival(D, Y, lam_p, n_p_perGy, cell: CellLineParams):
    return survival(D, Y, lam_p, n_p_perGy,
                    cell.mu_x, cell.mu_y, cell.zeta, cell.xi,
                    cell.eta_lp_to_1, cell.eta_lp_to_inf)


def cell_alpha_beta(Y, lam_p, cell: CellLineParams):
    return alpha_beta(Y, lam_p,
                      cell.mu_x, cell.mu_y, cell.zeta, cell.xi,
                      cell.eta_lp_to_1, cell.eta_lp_to_inf)
