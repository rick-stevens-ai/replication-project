"""GLOBLE — Giant LOop Binary LEsion model, kinetic extension.

Implements the model of Herr, Friedrich, Durante & Scholz, PLoS ONE 9(1) e83923 (2014).

The five level fractions f_0, f_i, f_c, l_i, l_c obey (Eqs. 13–17):

    df_0/dt  = -λ̇·f_0  + r_i·f_i + r_c·f_c
    df_i/dt  =  λ̇·f_0  - (λ̇ + r_i + m_i)·f_i
    df_c/dt  =  λ̇·f_i  - (r_c + m_c)·f_c
    dl_i/dt  =  m_i·f_i
    dl_c/dt  =  m_c·f_c

with rates (Eq. 11–12):

    r_x = (1 - ε_x) · ln(2)/HLT_x
    m_x =      ε_x  · ln(2)/HLT_x

DSB rate per domain (Eq. 10): λ̇ = α_DSB · Ḋ / N_L.

Survival (Eq. 18): S = exp[ -N_L · ( l_i(∞) + l_c(∞) ) ].

Paper-fixed constants: α_DSB = 30 /Gy/cell, N_L = 3000 domains, HLT_c = 5 h.
Per-cell-line: ε_i, ε_c, HLT_i.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np
from scipy.integrate import solve_ivp


# ---------------- paper-fixed constants ---------------- #

ALPHA_DSB = 30.0     # DSB per Gy per cell
N_L       = 3000     # giant-loop domains per nucleus
HLT_C     = 5.0      # h, half-life of clustered DSBs (paper-fixed)
LN2       = math.log(2.0)


# ---------------- parameters ---------------- #

@dataclass(frozen=True)
class GlobleParams:
    eps_i: float          # lethality probability for isolated DSBs (ε_i)
    eps_c: float          # lethality probability for clustered DSBs (ε_c)
    hlt_i: float          # half-life time of isolated DSBs (h)
    hlt_c: float = HLT_C  # half-life time of clustered DSBs (h)
    n_l:   int   = N_L
    alpha_dsb: float = ALPHA_DSB

    @property
    def r_i(self) -> float: return (1.0 - self.eps_i) * LN2 / self.hlt_i
    @property
    def m_i(self) -> float: return self.eps_i        * LN2 / self.hlt_i
    @property
    def r_c(self) -> float: return (1.0 - self.eps_c) * LN2 / self.hlt_c
    @property
    def m_c(self) -> float: return self.eps_c        * LN2 / self.hlt_c

    def lambda_dot(self, dose_rate_gy_per_h: float) -> float:
        """DSB induction rate per domain (per hour). Eq. (10)."""
        return self.alpha_dsb * dose_rate_gy_per_h / self.n_l


# ---------------- ODE system ---------------- #

def _rhs(t: float, y: np.ndarray, ldot: float, ri: float, mi: float, rc: float, mc: float) -> np.ndarray:
    f0, fi, fc, li, lc = y
    df0 = -ldot * f0 + ri * fi + rc * fc
    dfi =  ldot * f0 - (ldot + ri + mi) * fi
    dfc =  ldot * fi - (rc + mc) * fc
    dli = mi * fi
    dlc = mc * fc
    return np.array([df0, dfi, dfc, dli, dlc])


def integrate_single_dose(
    p: GlobleParams,
    dose_gy: float,
    dose_rate_gy_per_h: float,
    *,
    relax_time_h: float = 50.0,
    rtol: float = 1e-9,
    atol: float = 1e-12,
) -> dict:
    """Integrate the ODEs for a single-dose treatment at constant dose rate, then
    relax for `relax_time_h` extra hours of repair to approximate t → ∞.
    Returns dict including l_i_inf, l_c_inf, survival and the trajectory.
    """
    T = dose_gy / dose_rate_gy_per_h  # h
    ldot_on  = p.lambda_dot(dose_rate_gy_per_h)
    ri, mi, rc, mc = p.r_i, p.m_i, p.r_c, p.m_c

    y0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
    sol_on = solve_ivp(_rhs, (0.0, T), y0, args=(ldot_on, ri, mi, rc, mc),
                       method="LSODA", rtol=rtol, atol=atol, dense_output=False)
    y_T = sol_on.y[:, -1]

    # off-beam relaxation (λ̇ = 0)
    sol_off = solve_ivp(_rhs, (0.0, relax_time_h), y_T, args=(0.0, ri, mi, rc, mc),
                        method="LSODA", rtol=rtol, atol=atol, dense_output=False)
    y_end = sol_off.y[:, -1]

    li_inf, lc_inf = y_end[3], y_end[4]
    # closed-form expression for l_i(∞), l_c(∞) using Eqs. (20)–(21) for cross-check
    li_inf_alt = y_T[3] + p.eps_i * y_T[1]
    lc_inf_alt = y_T[4] + p.eps_c * y_T[2]

    surv = math.exp(-p.n_l * (li_inf + lc_inf))
    surv_alt = math.exp(-p.n_l * (li_inf_alt + lc_inf_alt))
    return dict(
        T_h=T, l_i_inf=li_inf, l_c_inf=lc_inf, survival=surv,
        l_i_inf_eq20=li_inf_alt, l_c_inf_eq20=lc_inf_alt, survival_eq20=surv_alt,
        y_T=y_T, y_end=y_end,
    )


def survival_single_dose(p: GlobleParams, dose_gy: float, dose_rate_gy_per_h: float) -> float:
    return integrate_single_dose(p, dose_gy, dose_rate_gy_per_h)["survival"]


def survival_curve(
    p: GlobleParams,
    doses_gy: Sequence[float],
    dose_rate_gy_per_h: float,
) -> np.ndarray:
    return np.array([survival_single_dose(p, d, dose_rate_gy_per_h) for d in doses_gy])


# ---------------- static GLOBLE (instantaneous limit) ---------------- #

def survival_static(p: GlobleParams, dose_gy: float) -> float:
    """Static GLOBLE survival from Eqs. (2)–(7) and (1)."""
    lam = p.alpha_dsb * dose_gy / p.n_l
    p1 = lam * math.exp(-lam)
    pge2 = 1.0 - math.exp(-lam) - p1
    ni = p.n_l * p1
    nc = p.n_l * pge2
    return math.exp(-(p.eps_i * ni + p.eps_c * nc))


# ---------------- split-dose closed form (Eqs. 22–32) ---------------- #

def survival_split_dose(p: GlobleParams, d_gy: float, t1_h: float) -> float:
    """Two equally sized acute doses d separated by t1 (hours)."""
    lam = p.alpha_dsb * d_gy / p.n_l
    p0 = math.exp(-lam)
    p1 = lam * math.exp(-lam)
    pge2 = 1.0 - p0 - p1

    n_i_0p = p.n_l * p1
    n_c_0p = p.n_l * pge2
    # n_0 after first dose, evolving via repair; for L computation we don't need n_0
    decay_i = math.exp(-(p.m_i + p.r_i) * t1_h)
    decay_c = math.exp(-(p.m_c + p.r_c) * t1_h)

    n_i_t1m = n_i_0p * decay_i
    n_c_t1m = n_c_0p * decay_c

    Li_t1m = n_i_0p * (1.0 - decay_i) * p.eps_i
    Lc_t1m = n_c_0p * (1.0 - decay_c) * p.eps_c

    # n_0 at t1- = N_L - n_i(t1-) - n_c(t1-) - L_i/eps_i adjusted lethals removed?
    # Per the paper, l_i and l_c are absorbing, leaving the "alive" domain pool.
    # The non-lethal repaired domains return to f_0. So we conserve total domains:
    #   n_0(t1-) = N_L - n_i(t1-) - n_c(t1-) - L_i(t1-) - L_c(t1-).
    n_0_t1m = p.n_l - n_i_t1m - n_c_t1m - Li_t1m - Lc_t1m

    # second dose (Eqs. 29–30)
    n_i_t1p = n_i_t1m * p0 + n_0_t1m * p1
    n_c_t1p = n_c_t1m + n_i_t1m * (p1 + pge2) + n_0_t1m * pge2

    L_total = Li_t1m + Lc_t1m + p.eps_i * n_i_t1p + p.eps_c * n_c_t1p
    return math.exp(-L_total)


# ---------------- low-dose-rate closed form (Eq. 38) ---------------- #

def survival_low_dose_rate_closed_form(p: GlobleParams, dose_gy: float, dose_rate_gy_per_h: float) -> float:
    """Eq. (38): single dose at very low constant rate. f_c → 0 approximation."""
    T = dose_gy / dose_rate_gy_per_h
    ldot = p.lambda_dot(dose_rate_gy_per_h)
    r = p.m_i + p.r_i
    x_tilde = math.sqrt((r + ldot) ** 2 - 4.0 * ldot * p.m_i)
    y_tilde = r + ldot - x_tilde
    bracket = (
        1.0
        + (p.m_i * ldot / x_tilde)
        * math.exp(-y_tilde * T / 2.0)
        * (
            1.0 / r
            - 2.0 / y_tilde
            - math.exp(-x_tilde * T) * (1.0 / r - 2.0 / (y_tilde + 2.0 * x_tilde))
        )
    )
    return math.exp(-p.n_l * bracket)


# ---------------- LQ + Lea-Catcheside (Eq. 41) ---------------- #

def lea_catcheside_G(r: float, T_h: float) -> float:
    if T_h <= 0:
        return 1.0
    rT = r * T_h
    return 2.0 * (math.exp(-rT) + rT - 1.0) / (rT * rT)


def survival_lq_lc(alpha: float, beta: float, dose_gy: float, dose_rate_gy_per_h: float, r: float) -> float:
    T = dose_gy / dose_rate_gy_per_h
    G = lea_catcheside_G(r, T)
    return math.exp(-(alpha * dose_gy + G * beta * dose_gy * dose_gy))


def lq_params_from_globle(p: GlobleParams) -> tuple[float, float]:
    """Eqs. (8)–(9): α = ε_i · α_DSB ; β = (ε_c · α_DSB² − 2·α·α_DSB) / (2·N_L).
    The paper writes ε_c = 2·(N_L·β + α_DSB·α)/α_DSB² so we invert.
    """
    alpha = p.eps_i * p.alpha_dsb
    beta  = (p.eps_c * p.alpha_dsb * p.alpha_dsb - 2.0 * alpha * p.alpha_dsb) / (2.0 * p.n_l)
    return alpha, beta


def globle_taylor_alpha_beta(p: GlobleParams) -> tuple[float, float]:
    """Numerical (finite-difference) Taylor coefficients of −ln S at D=0.

    Coefficient of D     → α
    Coefficient of D²/2  → 2β (when including the LC factor G evaluated at T)
    For an *instantaneous* (high-rate) treatment, returns the static GLOBLE α and β.
    """
    # Use static GLOBLE (instantaneous) for the analytical baseline; ε_i α_DSB = α.
    h1, h2 = 1e-3, 2e-3
    s1 = survival_static(p, h1)
    s2 = survival_static(p, h2)
    s0 = 1.0
    nl0 = -math.log(s0)
    nl1 = -math.log(s1)
    nl2 = -math.log(s2)
    # forward differences
    alpha_num = (4 * nl1 - nl2) / (2 * h1)  # O(h^2) approx of f'(0)
    beta_num  = (nl2 - 2 * nl1 + nl0) / (h1 * h1) / 2.0  # second derivative / 2
    return alpha_num, beta_num
