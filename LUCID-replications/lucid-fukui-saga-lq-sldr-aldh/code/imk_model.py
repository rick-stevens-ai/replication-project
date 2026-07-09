"""
IMK (Integrated Microdosimetric-Kinetic) model replication for
Fukui et al., Sci Rep 12:1056 (2022), DOI 10.1038/s41598-022-05172-4.

Equations 1-15 from Methods, parameters from Table 1.

Convention from paper:
    -ln S = alpha0 * D + (y_D/(rho*pi*rd^2)) * beta0 * D + F * beta0 * D^2     (Eq 1)

  where F is the Lea-Catcheside time factor (Eq 2):
    F = 2 / ((a+c)^2 * T^2) * [ (a+c)*T + exp(-(a+c)*T) - 1 ]

  When T -> 0 (acute), F -> 1; when T -> infinity, F -> 0.

Microdosimetric prefactor gamma = y_D / (rho * pi * r_d^2)
  rho = 1.0 g/cm^3 = 1.0e-12 g/um^3  ->  in mass per um^3
  Paper writes "Microdosimetry gamma = 0.954 Gy" in Table 1, so we
  treat the prefactor entering Eq 1 effectively as a known constant.

  The combined first-order term is:
      alpha0_eff * D = alpha0 * D + gamma * beta0 * D
  i.e. alpha_LQ = alpha0 + gamma * beta0 .
  For T->0 (acute), beta_LQ = beta0.

Two-cell-population model:
    S(D) = f_p * S_p(D) + f_s * S_s(D),  f_p + f_s = 1   (Eq 14)

For radioresistant lines, the progeny SLDR rate is boosted:
    (a+c)_p* = w_SLDR * (a+c)_p                            (Eq 9)
    alpha0_p* = alpha0_p / w_SLDR                          (Eq 10)
    beta0_p*  = beta0_p  / w_SLDR                          (Eq 11)
And stem cells use (a+c)_H = (a+c)_p* (radioresistant) per Eq 8.

For NON-resistant cells, w_SLDR = 1, (a+c)_p* = (a+c)_p,
    parameters are simply (alpha0_p, beta0_p, (a+c)_p) and
    (alpha0_s, beta0_s, (a+c)_H).

In Table 1, the entries for SAS and HSC2 (non-resistant) are
    alpha0_p* = alpha0_p,  beta0_p* = beta0_p,  (a+c)_p* = (a+c)_p,
    (a+c)_H is the SLDR rate for stem cells.
For SAS-R and HSC2-R (resistant), Table 1 only lists the
*resistant-cell progeny set* [alpha0_p*, beta0_p*, (a+c)_p*]
and w_SLDR with respect to the parental rate; stem cell set is
shared with the parental (same alpha0_s, beta0_s, (a+c)_H).
"""

from __future__ import annotations
import math
import numpy as np

# ----------------------------------------------------------------------
# Paper-reported constants
# ----------------------------------------------------------------------
# Acute dose-rate used in the single-dose experiment: 1.0 Gy/min => 60 Gy/h
DOSE_RATE_ACUTE_GY_PER_H = 60.0

# Microdosimetric prefactor gamma = y_D / (rho * pi * r_d^2).  Table 1 lists
# "gamma = 0.954 Gy" for both SAS and HSC2 families.  We use it as-is.
GAMMA_PREFACTOR = 0.954  # Gy

# ----------------------------------------------------------------------
# Lea-Catcheside time factor F (Eq 2)
# ----------------------------------------------------------------------
def lea_catcheside_F(T_h: float, apc: float) -> float:
    """T_h: dose-delivery time in hours; apc: (a+c) in h^-1.

    F -> 1 as T -> 0, F -> 0 as T -> infinity."""
    if T_h <= 0:
        return 1.0
    x = apc * T_h
    if x < 1e-9:
        # Taylor expand to avoid catastrophic cancellation: F ~= 1 - x/3
        return 1.0 - x / 3.0
    return 2.0 / (x * x) * (x + math.exp(-x) - 1.0)


# ----------------------------------------------------------------------
# Single-population survival, single-dose (Eq 1)
# ----------------------------------------------------------------------
def neglogS_single(D, alpha0, beta0, apc, T_h, gamma=GAMMA_PREFACTOR):
    F = lea_catcheside_F(T_h, apc)
    return alpha0 * D + gamma * beta0 * D + F * beta0 * D * D


def S_single(D, alpha0, beta0, apc, T_h=0.0, gamma=GAMMA_PREFACTOR):
    return np.exp(-np.asarray([neglogS_single(d, alpha0, beta0, apc, T_h, gamma) for d in np.atleast_1d(D)]))


# ----------------------------------------------------------------------
# Two-population survival (Eq 14) for ACUTE single-dose irradiation
# (Eqs 6, 7 with T set by the acute dose rate of 1 Gy/min)
# ----------------------------------------------------------------------
def S_total_single_dose(
    D,
    alpha0_p_star, beta0_p_star, apc_p_star,
    alpha0_s, beta0_s, apc_H,
    f_s,
    dose_rate_gy_per_h: float = DOSE_RATE_ACUTE_GY_PER_H,
    gamma: float = GAMMA_PREFACTOR,
):
    D = np.atleast_1d(np.asarray(D, dtype=float))
    f_p = 1.0 - f_s
    out = np.empty_like(D)
    for i, d in enumerate(D):
        T = d / dose_rate_gy_per_h  # hours
        nlS_p = neglogS_single(d, alpha0_p_star, beta0_p_star, apc_p_star, T, gamma)
        nlS_s = neglogS_single(d, alpha0_s,      beta0_s,      apc_H,      T, gamma)
        Sp = math.exp(-nlS_p)
        Ss = math.exp(-nlS_s)
        out[i] = f_p * Sp + f_s * Ss
    return out


# ----------------------------------------------------------------------
# Split-dose: total dose D in 2 fractions with interval tau (h)
# Per Eqs 4, 12, 13. Each fraction acutely delivered (T->0, F->1).
# ----------------------------------------------------------------------
def neglogS_split_pop(D1, D2, tau, alpha0, beta0, apc, gamma=GAMMA_PREFACTOR):
    # Sum over two acute deliveries plus cross-term
    nl = 0.0
    for D_i in (D1, D2):
        # acute single-dose with T->0  =>  F=1
        nl += alpha0 * D_i + gamma * beta0 * D_i + beta0 * D_i * D_i
    nl += 2.0 * beta0 * math.exp(-apc * tau) * D1 * D2
    return nl


def S_total_split_dose(
    D1, D2, tau_h,
    alpha0_p_star, beta0_p_star, apc_p_star,
    alpha0_s, beta0_s, apc_H,
    f_s,
    gamma: float = GAMMA_PREFACTOR,
):
    nl_p = neglogS_split_pop(D1, D2, tau_h, alpha0_p_star, beta0_p_star, apc_p_star, gamma)
    nl_s = neglogS_split_pop(D1, D2, tau_h, alpha0_s,      beta0_s,      apc_H,      gamma)
    Sp = math.exp(-nl_p)
    Ss = math.exp(-nl_s)
    f_p = 1.0 - f_s
    return f_p * Sp + f_s * Ss


# ----------------------------------------------------------------------
# Coefficient of determination
# ----------------------------------------------------------------------
def r_squared_log(y_obs, y_pred, eps=1e-30):
    """R^2 computed in -ln S space (same as paper: fits -ln S)."""
    y_obs = np.asarray(y_obs, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    nl_obs = -np.log(np.maximum(y_obs, eps))
    nl_pred = -np.log(np.maximum(y_pred, eps))
    ss_res = np.sum((nl_obs - nl_pred) ** 2)
    ss_tot = np.sum((nl_obs - nl_obs.mean()) ** 2)
    if ss_tot <= 0:
        return float("nan")
    return 1.0 - ss_res / ss_tot
