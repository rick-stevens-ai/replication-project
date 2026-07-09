"""
Shuryak, Brenner, Ullrich (2011) PLoS One 6(12):e28559
Radiation-Induced Carcinogenesis: Mechanistically Based Differences
between Gamma-Rays and Neutrons, and Interactions with DMBA.

Replication of the closed-form ERR model (Eqs. 3-4 of the paper).
Best-fit parameters from Table 1.

Model summary:
  ERR = (Q1*Q2 + Q3)/Q4 - 1
  Q1  = (1 + Yv) / [1 + Yv*(1 - exp(-d*(A - Tx - L)))]
  Q2  = exp(b*(A - Tx - L)) * (exp(b*Tx) - 1 + b*Xv)
  Q3  = exp(b*(A - Tx - L)) - 1
  Q4  = exp(b*(A - L)) - 1
  Xv  = X_DMBA*D_DMBA + X_gamma * D_gamma * G(D_gamma, R_gamma)
  Yv  = Y_n * D_n / (R_n + q)
  G   = 2*[exp(-alpha) - 1 + alpha]/alpha^2,  alpha = K_rep * D_gamma / R_gamma
       (Lea-Catcheside protraction factor)

Time units: days. Dose units: Gy (DMBA in mg).
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass


# -----------------------------------------------------------------------------
# Best-fit parameters, Table 1 of Shuryak et al. 2011
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    b: float = 1.40e-2          # days^-1   pre-malignant niche replication rate
    d: float = 4.00e-4          # days^-1   homeostatic regulation
    X_DMBA: float = 8.42        # days/mg
    X_gamma: float = 969.0      # days/Gy
    K_rep: float = 0.391        # days^-1
    Y_n: float = 2.5e4          # days^-1
    q: float = 123.0            # Gy/day    dose rate at which Pe=0.5
    L: float = 50.0             # days      lag


P_DEFAULT = Params()

# Experimental setup (Methods: mice exposed at 12 weeks = 84 days,
# mammary tumour incidence followed up to ~800 days).
TX_DAYS = 84.0          # age at exposure
A_DAYS_DEFAULT = 800.0  # age at which ERR is reported


def lea_catcheside(D_gamma: float, R_gamma: float, K_rep: float) -> float:
    """Lea-Catcheside / Sachs-Brenner protraction factor for constant dose-rate.
    G = 2*[exp(-alpha) - 1 + alpha] / alpha^2,  alpha = K_rep * D_gamma / R_gamma.

    Limits: G -> 1 as alpha -> 0 (acute), G -> 0 as alpha -> infinity (chronic).
    For D_gamma == 0 or R_gamma == 0, returns 0 (no gamma dose contribution).
    """
    if D_gamma <= 0.0 or R_gamma <= 0.0:
        return 0.0
    alpha = K_rep * D_gamma / R_gamma
    if alpha < 1e-6:
        # Taylor expansion: G = 1 - alpha/3 + alpha^2/12 - ...
        return 1.0 - alpha / 3.0 + (alpha ** 2) / 12.0
    return 2.0 * (np.exp(-alpha) - 1.0 + alpha) / (alpha ** 2)


def Xv(D_DMBA: float, D_gamma: float, R_gamma: float, p: Params = P_DEFAULT) -> float:
    """Initiation term Xv (units: days)."""
    G = lea_catcheside(D_gamma, R_gamma, p.K_rep) if D_gamma > 0 else 0.0
    return p.X_DMBA * D_DMBA + p.X_gamma * D_gamma * G


def Yv(D_n: float, R_n: float, p: Params = P_DEFAULT) -> float:
    """Bystander promotion term Yv (dimensionless)."""
    if D_n <= 0.0:
        return 0.0
    return p.Y_n * D_n / (R_n + p.q)


def ERR(D_DMBA: float = 0.0,
        D_gamma: float = 0.0,
        R_gamma: float = 0.0,
        D_n: float = 0.0,
        R_n: float = 0.0,
        A: float = A_DAYS_DEFAULT,
        Tx: float = TX_DAYS,
        p: Params = P_DEFAULT) -> float:
    """Compute the excess relative risk per Eq. 3.

    Doses are total cumulative doses (Gy for radiations, mg for DMBA).
    Dose rates are in Gy/day. R is ignored if its dose is zero.
    """
    Xv_val = Xv(D_DMBA, D_gamma, R_gamma, p)
    Yv_val = Yv(D_n, R_n, p)
    dt = A - Tx - p.L  # post-tumour-window time
    if dt <= 0.0:
        return 0.0

    Q1 = (1.0 + Yv_val) / (1.0 + Yv_val * (1.0 - np.exp(-p.d * dt)))
    Q2 = np.exp(p.b * dt) * (np.exp(p.b * Tx) - 1.0 + p.b * Xv_val)
    Q3 = np.exp(p.b * dt) - 1.0
    Q4 = np.exp(p.b * (A - p.L)) - 1.0
    return (Q1 * Q2 + Q3) / Q4 - 1.0


def ERR_array(arr_kwargs, **fixed):
    """Vectorised ERR: pass a dict of {kwarg: array} for the swept variables."""
    keys = list(arr_kwargs.keys())
    arrs = [np.atleast_1d(np.asarray(arr_kwargs[k], dtype=float)) for k in keys]
    shape = np.broadcast_shapes(*[a.shape for a in arrs])
    out = np.empty(shape, dtype=float)
    it = np.nditer([*[np.broadcast_to(a, shape) for a in arrs]], flags=['multi_index'])
    for vals in it:
        kw = {k: float(v) for k, v in zip(keys, vals)}
        kw.update(fixed)
        out[it.multi_index] = ERR(**kw)
    return out


if __name__ == "__main__":
    # quick sanity prints reproducing paper claims
    # gamma: 1 Gy HDR (576 Gy/day) at age 800
    e_g_hdr = ERR(D_gamma=1.0, R_gamma=576.0)
    e_g_ldr = ERR(D_gamma=1.0, R_gamma=0.01)
    print(f"gamma 1Gy HDR(576 Gy/d):  ERR = {e_g_hdr:.3f}")
    print(f"gamma 1Gy LDR(0.01 Gy/d): ERR = {e_g_ldr:.3f}")
    print(f"ratio HDR/LDR = {e_g_hdr/e_g_ldr:.2f} (paper claims ~10x)")
    # neutrons at 0.025 Gy LDR/HDR
    for D, R, lbl in [(0.025, 0.01, "n 0.025 Gy LDR"),
                      (0.025, 360.0, "n 0.025 Gy HDR"),
                      (0.05,  0.01, "n 0.05 Gy LDR"),
                      (0.05,  360.0, "n 0.05 Gy HDR"),
                      (0.10,  0.01, "n 0.10 Gy LDR"),
                      (0.10,  360.0, "n 0.10 Gy HDR")]:
        print(f"{lbl}: ERR = {ERR(D_n=D, R_n=R):.2f}")
    # neutron + DMBA combos
    for D, R, lbl in [(0.025, 0.01, "n+DMBA 0.025 Gy LDR"),
                      (0.05,  0.01, "n+DMBA 0.05 Gy LDR"),
                      (0.10,  0.01, "n+DMBA 0.10 Gy LDR"),
                      (0.025, 360.0, "n+DMBA 0.025 Gy HDR"),
                      (0.05,  360.0, "n+DMBA 0.05 Gy HDR"),
                      (0.10,  360.0, "n+DMBA 0.10 Gy HDR")]:
        print(f"{lbl}: ERR = {ERR(D_n=D, R_n=R, D_DMBA=2.5):.2f}")
    # DMBA-only
    for D in [2.5, 25.0, 75.0]:
        print(f"DMBA {D} mg: ERR = {ERR(D_DMBA=D):.2f}")
