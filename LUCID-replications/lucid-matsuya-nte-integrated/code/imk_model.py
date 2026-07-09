"""
Independent replication of the Integrated Microdosimetric-Kinetic (IMK) model
from Matsuya, Y. et al. (2018) "Integrated Modelling of Cell Responses after
Irradiation for DNA-Targeted Effects and Non-Targeted Effects."
Scientific Reports 8: 4849. DOI: 10.1038/s41598-018-23202-y

This is a fresh, independent implementation written from the paper equations
(no author code consulted). Goal is qualitative + ~10% quantitative agreement
with the paper's reported Tables 1 & 2 parameters and Figures 2-5.

Equations referenced in comments use the paper's numbering (Eqs. 4-26)
and the supplement (SI-x).
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Sequence


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------

def lea_catcheside_F(T: float, a_plus_c: float) -> float:
    """Eq. 4b. Lea-Catcheside time factor for continuous irradiation."""
    if T <= 0.0:
        return 1.0
    x = a_plus_c * T
    return 2.0 / (x * x) * (x + np.exp(-x) - 1.0)


# ---------------------------------------------------------------------------
# Targeted Effects (TE) - MK-style cell survival
# ---------------------------------------------------------------------------

def w_T(D: np.ndarray | float,
        alpha0: float,
        beta0: float,
        gamma: float,
        a_plus_c: float = None,
        T: float = 0.0) -> np.ndarray | float:
    """
    Average number of LLs per nucleus from TEs (Eq. 4a).
    For acute irradiation (T~0) reduces to (alpha0+gamma*beta0)*D + beta0*D^2.
    """
    D = np.asarray(D, dtype=float)
    if T <= 0.0 or a_plus_c is None:
        F = 1.0
    else:
        F = lea_catcheside_F(T, a_plus_c)
    return (alpha0 + gamma * beta0) * D + F * beta0 * D * D


def S_T(D, alpha0, beta0, gamma, a_plus_c=None, T=0.0):
    """TE-only surviving fraction (Eq. 4a)."""
    return np.exp(-w_T(D, alpha0, beta0, gamma, a_plus_c, T))


# ---------------------------------------------------------------------------
# Non-Targeted Effects (NTE) - signals and signal-induced DNA damage
# ---------------------------------------------------------------------------

def hit_probability(D: np.ndarray | float,
                    alpha_b: float,
                    beta_b: float,
                    gamma: float) -> np.ndarray | float:
    """Fraction of hit cells f_h(D) (Eq. 8).  f_b = 1 - f_h."""
    D = np.asarray(D, dtype=float)
    Nh = (alpha_b + gamma * beta_b) * D + beta_b * D * D
    return 1.0 - np.exp(-Nh)


def signal_concentration(t: np.ndarray, mu_s: float, lam_plus_R: float,
                         A: float = 1.0) -> np.ndarray:
    """
    Cell-killing signal concentration as a function of t (Eq. 9), normalised
    to a representative amplitude A = r_s * mu_s * <s_d(r)> / (mu_s-(lam+R)).
    The shape is what is compared to Lyng (calcium) and Han (NO) data.
    """
    t = np.asarray(t, dtype=float)
    denom = (mu_s - lam_plus_R)
    if abs(denom) < 1e-12:
        # degenerate -> limiting form (just use exponential decay shape)
        return A * mu_s * t * np.exp(-lam_plus_R * t)
    return A * (1.0 - np.exp(-denom * t)) * np.exp(-lam_plus_R * t)


def signal_concentration_normalized(t, mu_s, lam_plus_R):
    """Normalised so the peak = 1 -- useful for fitting relative concentration
    data (Lyng calcium, Han NO)."""
    rho = signal_concentration(t, mu_s, lam_plus_R, A=1.0)
    pk = rho.max() if np.isfinite(rho).any() else 1.0
    return rho / pk if pk > 0 else rho


# ---------- NTE DNA damage (Eq. 12) ---------- #

def x_b_NTE(t: np.ndarray, D: float, params: dict) -> np.ndarray:
    """
    Average number of signal-induced PLLs per nucleus as a function of time t
    after acute irradiation (Eq. 12, summed over domains).

    params expects:
        a, c_b, mu_s, lam_plus_R, alpha_b, beta_b, gamma, K_amp
    where K_amp = R * mu_s * r_s * K_b * s_P  (lumped amplitude).
    """
    t = np.asarray(t, dtype=float)
    a = params['a']
    c_b = params['c_b']
    mu_s = params['mu_s']
    lpR = params['lam_plus_R']
    K_amp = params['K_amp']
    alpha_b = params['alpha_b']
    beta_b = params['beta_b']
    gamma = params['gamma']

    fh = hit_probability(D, alpha_b, beta_b, gamma)
    fb = 1.0 - fh
    Nh_total = (alpha_b + gamma * beta_b) * D + beta_b * D * D
    # f_h * f_b -- dose envelope from Eq. 12
    env = fh * fb
    # K_amp absorbs R*mu_s*r_s*K_b*s_P
    amp = K_amp * env / max(mu_s - lpR, 1e-12)

    apb = a + c_b
    t1 = (1.0 - np.exp(-(mu_s - apb) * t)) / max(mu_s - apb, 1e-12)
    t2 = (1.0 - np.exp(-(lpR - apb) * t)) / max(lpR - apb, 1e-12)
    decay = np.exp(-apb * t)
    return amp * (t1 - t2) * decay


def w_b_total_NTE(D, params):
    """Eq. 14-15 (steady accumulated LLs per nucleus from NTE pathway).
    Integrated form (after t -> long enough to integrate signal pulse but
    short enough that LLs persist) used as the cell-survival contribution.
    """
    a = params['a']
    c_b = params['c_b']
    mu_s = params['mu_s']
    lpR = params['lam_plus_R']
    K_amp = params['K_amp']            # = a*R*r_s*K_b*s_P
    alpha_b = params['alpha_b']
    beta_b = params['beta_b']
    gamma = params['gamma']

    delta = K_amp / (lpR * max(a + c_b, 1e-12))  # paper's delta (Eq. 16)
    Nh = (alpha_b + gamma * beta_b) * D + beta_b * D * D
    fh = 1.0 - np.exp(-Nh)
    fb = 1.0 - fh
    return delta * fh * fb  # Eq. 15 form: delta * (1-e^-Nh)*e^-Nh


def w_b_direct(D, delta, alpha_b, beta_b, gamma):
    """Closed-form NTE LLs per nucleus parameterised by delta directly
    (Eq. 15)."""
    D = np.asarray(D, dtype=float)
    Nh = (alpha_b + gamma * beta_b) * D + beta_b * D * D
    return delta * (1.0 - np.exp(-Nh)) * np.exp(-Nh)


def S_NTE(D, delta, alpha_b, beta_b, gamma):
    """NTE surviving fraction from direct irradiation (Eq. 17)."""
    return np.exp(-w_b_direct(D, delta, alpha_b, beta_b, gamma))


def S_NTE_MTBE(D, delta_m, alpha_b, beta_b, gamma):
    """NTE surviving fraction in MTBE assay (Eq. 25):
       -ln S_NTE = delta_m * [1 - exp(-Nh)]^2   ... but the paper writes
       (Eq. 25) as delta_m * (1 - e^-Nh), single power.  Re-read carefully:
       In Eq. 25 it's delta_mt*(1 - e^(-...))  (cf. Eq. 24 -> Eq. 25).
       (Only the donor-cell hit fraction f_h(D) enters; recipient cells are
       fully non-hit, so f_b=1.)
    """
    D = np.asarray(D, dtype=float)
    Nh = (alpha_b + gamma * beta_b) * D + beta_b * D * D
    return np.exp(-delta_m * (1.0 - np.exp(-Nh)))


# ---------------------------------------------------------------------------
# Integrated survival
# ---------------------------------------------------------------------------

def S_total(D, alpha0, beta0, gamma, delta, alpha_b, beta_b, a_plus_c=None, T=0.0):
    """Integrated cell survival (Eq. 19): S = S_T * S_NTE."""
    return S_T(D, alpha0, beta0, gamma, a_plus_c, T) * \
           S_NTE(D, delta, alpha_b, beta_b, gamma)


# ---------------------------------------------------------------------------
# Convenience: dataclasses for parameter sets reported in the paper
# ---------------------------------------------------------------------------

@dataclass
class CellParams:
    name: str
    alpha0: float
    beta0: float
    a_plus_c: float
    alpha_b: float
    beta_b: float
    delta: float
    gamma: float = 0.924  # ~250 kVp X-rays (paper's default for V79 etc.)


# Table 2 values from the paper
PAPER_PARAMS = {
    'V79-379A': CellParams(
        name='V79-379A',
        alpha0=1.60e-2, beta0=6.00e-1, a_plus_c=6.29,
        alpha_b=1.46, beta_b=3.96e-1, delta=2.57e-1, gamma=0.924,
    ),
    'T-47D': CellParams(
        name='T-47D',
        alpha0=1.29e-1, beta0=2.90e-2, a_plus_c=1.60,
        alpha_b=1.80, beta_b=3.00e-2, delta=1.72e-1, gamma=0.480,
    ),
    'HPV-G': CellParams(
        name='HPV-G',
        alpha0=np.nan, beta0=np.nan, a_plus_c=np.nan,
        alpha_b=3.09e1, beta_b=2.38e-2, delta=9.02e-1, gamma=0.480,
    ),
    'E48': CellParams(
        name='E48',
        alpha0=np.nan, beta0=np.nan, a_plus_c=np.nan,
        alpha_b=1.00e-3, beta_b=5.29e-1, delta=5.79e-1, gamma=0.480,
    ),
    'CHO-K1-sham': CellParams(
        name='CHO-K1-sham',
        alpha0=1.15e-1, beta0=2.20e-2, a_plus_c=0.706,  # a+c~0.706 from text
        alpha_b=9.28, beta_b=1.21, delta=2.79e-2, gamma=0.924,
    ),
    'CHO-K1-repair-inhibited': CellParams(
        name='CHO-K1-repair-inhibited',
        # Eq. (Fig. 4 caption): TE params multiplied by 3.52e-1; delta by 1.60e-2 to invert
        # repair (a/(a+c) increases by 3.52e-1 ratio of sham to inhibited).
        # Per paper: ratio sham/inhibited = 3.52e-1 for (alpha0,beta0), 1.60e-2 for delta.
        # So inhibited = sham / ratio:
        alpha0=1.15e-1 / 3.52e-1,
        beta0=2.20e-2 / 3.52e-1,
        a_plus_c=0.706,  # rate not given separately
        alpha_b=9.28, beta_b=1.21,
        delta=2.79e-2 / 1.60e-2,
        gamma=0.924,
    ),
}


# Signal parameters (Table 1)
SIGNAL_PARAMS_CALCIUM = {'mu_s': 80.4, 'lam_plus_R': 79.3}  # h^-1
SIGNAL_PARAMS_NO = {'mu_s': 11.0, 'lam_plus_R': 0.192}     # h^-1


# Damage kinetics (Table 1, MRC-5 calcium)
DAMAGE_PARAMS_MRC5 = {
    'a': 9.37e-3,         # h^-1
    'b_d': 1.15e-1,       # h^-1
    'a_plus_c': 7.04e-1,  # h^-1
    'p': 9.55e2,          # domains per nucleus
    'kd_g': 2.83e-2,      # Gy^-1
    'phi': 1.04,          # dimensionless
    'a_plus_cb': 1.09e-2, # h^-1  -> c_b ~ 1.09e-2 - 9.37e-3 = 1.53e-3 h^-1
    'K_amp_calcium': 4.61e-1,  # R*r_s*k_b*s_P  (h^-1)
    'alpha_b': 5.38,
    'beta_b': 5.41,
    'gamma': 0.923,
}


if __name__ == '__main__':
    # Quick sanity check
    D = np.linspace(0, 5, 21)
    cp = PAPER_PARAMS['V79-379A']
    s = S_total(D, cp.alpha0, cp.beta0, cp.gamma, cp.delta, cp.alpha_b,
                cp.beta_b)
    print(f"V79-379A sanity check S(0)={s[0]:.3f}  S(2 Gy)={s[8]:.3f}  "
          f"S(5 Gy)={s[-1]:.3f}")
