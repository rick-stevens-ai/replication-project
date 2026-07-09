"""
GLOBLE (Giant LOop Binary LEsion) cell-survival model
=====================================================
Replicates the *instantaneous* (high-dose-rate) photon-irradiation
GLOBLE model from Friedrich, Durante, Scholz, Radiat Res 178:385-394 (2012).

Original paper DOI: 10.1667/RR2964.1  (CLOSED ACCESS)

Equations sourced from the open-access follow-up:
  Herr L, Friedrich T, Durante M, Scholz M. (2014)
  "A Model of Photon Cell Killing Based on the Spatio-Temporal
   Clustering of DNA Damage in Higher Order Chromatin Structures."
  PLoS ONE 9(1): e83923. doi:10.1371/journal.pone.0083923 (PMC3879277)
  - Eqs. (1) survival, (2) λ, (3-5) Poisson, (6-7) n_i/n_c,
    (8-9) LQ <-> GLOBLE correspondence.
  Tommasino et al. (2015), PLoS ONE 10(6): e0129416 (PMC4465900)
  - Cross-checks N_L=3000, α_DSB=30/Gy, 2-Mbp loops.

Static (single-dose) GLOBLE formulas
------------------------------------
  λ(D)  = α_DSB · D / N_L                                      (avg DSBs / loop)
  n_i(D) = N_L · λ · exp(-λ)                                   (eq 6)
  n_c(D) = N_L · (1 - exp(-λ) - λ·exp(-λ))                     (eq 7)
  S(D)  = exp(-ε_i · n_i(D) - ε_c · n_c(D))                    (eq 1)

LQ correspondence at D -> 0
---------------------------
  α = ε_i · α_DSB                                              (eq 8)
  β = (ε_c/2 - ε_i) · α_DSB² / N_L
    => ε_c = 2 · (N_L·β / α_DSB² + α/α_DSB)
    => ε_c = 2·(N_L·β + α_DSB·α) / α_DSB²                      (eq 9)

Standard parameters (paper):
  α_DSB = 30 DSBs / Gy / cell
  N_L   = 3000 loops / nucleus (≈6000 Mbp genome / 2-Mbp loops)
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Default parameters used throughout the GLOBLE papers (Friedrich 2012,
# Herr 2014, Tommasino 2015 supplement). Override when needed.
# ---------------------------------------------------------------------------
ALPHA_DSB_DEFAULT = 30.0   # DSB/Gy/cell
N_L_DEFAULT       = 3000   # giant loops/domains per nucleus


@dataclass
class GLOBLEParams:
    """Cell-line-specific GLOBLE parameters."""
    eps_i: float                          # ε_i : lethality per isolated DSB
    eps_c: float                          # ε_c : lethality per clustered DSB
    alpha_dsb: float = ALPHA_DSB_DEFAULT  # DSBs / Gy / cell
    n_l:       int   = N_L_DEFAULT        # number of giant loops / nucleus


# ---------------------------------------------------------------------------
# Core GLOBLE functions
# ---------------------------------------------------------------------------
def lambda_per_domain(dose: np.ndarray, p: GLOBLEParams) -> np.ndarray:
    """Average DSBs per domain (eq. 2 in Herr 2014)."""
    return p.alpha_dsb * np.asarray(dose) / p.n_l


def hit_domains(dose: np.ndarray, p: GLOBLEParams) -> tuple[np.ndarray, np.ndarray]:
    """Return (n_i, n_c): mean numbers of isolated- and clustered-DSB loops.
    Eqs. (6)-(7).
    """
    lam = lambda_per_domain(dose, p)
    e   = np.exp(-lam)
    n_i = p.n_l * lam * e
    n_c = p.n_l * (1.0 - e - lam * e)
    return n_i, n_c


def survival(dose: np.ndarray, p: GLOBLEParams) -> np.ndarray:
    """Cell-survival probability S(D) (eq. 1).

    S = exp(-L_i - L_c) with  L_i = ε_i·n_i,  L_c = ε_c·n_c.
    """
    n_i, n_c = hit_domains(dose, p)
    return np.exp(-(p.eps_i * n_i + p.eps_c * n_c))


def neg_log_survival(dose: np.ndarray, p: GLOBLEParams) -> np.ndarray:
    """-ln S(D). Useful for plotting alongside α D + β D²."""
    n_i, n_c = hit_domains(dose, p)
    return p.eps_i * n_i + p.eps_c * n_c


# ---------------------------------------------------------------------------
# LQ <-> GLOBLE correspondence (eqs. 8, 9)
# ---------------------------------------------------------------------------
def lq_from_globle(p: GLOBLEParams) -> tuple[float, float]:
    """Return (α, β) of the small-dose Taylor expansion of -ln S in D.

    From the second-order Taylor expansion of -ln S(D) at D=0:
        α = ε_i · α_DSB                                            (eq. 8)
        β = (ε_c / 2 - ε_i) · α_DSB² / N_L                         (rearranged 9)
    """
    a = p.eps_i * p.alpha_dsb
    b = (p.eps_c / 2.0 - p.eps_i) * p.alpha_dsb ** 2 / p.n_l
    return a, b


def globle_from_lq(alpha_lq: float,
                   beta_lq:  float,
                   alpha_dsb: float = ALPHA_DSB_DEFAULT,
                   n_l:       int   = N_L_DEFAULT) -> GLOBLEParams:
    """Invert (α,β) -> (ε_i, ε_c) using eqs. (8)-(9)."""
    eps_i = alpha_lq / alpha_dsb
    eps_c = 2.0 * (n_l * beta_lq + alpha_dsb * alpha_lq) / alpha_dsb ** 2
    return GLOBLEParams(eps_i=eps_i, eps_c=eps_c,
                        alpha_dsb=alpha_dsb, n_l=n_l)


# ---------------------------------------------------------------------------
# High-dose linear asymptote
# ---------------------------------------------------------------------------
def high_dose_intermediate_slope(p: GLOBLEParams,
                                  d_lo: float = 10.0,
                                  d_hi: float = 40.0) -> float:
    """
    Slope of -ln S(D) in the intermediate-to-high regime where the curve
    is *approximately* linear (the 'transition to straight dose-response'
    described in the Friedrich 2012 abstract).

    In the *basic static* GLOBLE the curve eventually saturates at
    -ln S = eps_c * N_L because every loop becomes clustered and additional
    DSBs no longer change the lethal-event count.  Before that saturation,
    however, the curve passes through a quasi-linear regime characterised
    by the local slope between e.g. 10 and 40 Gy.  That is the regime
    relevant to the abstract's qualitative claim.
    """
    Dpair = np.asarray([d_lo, d_hi], float)
    nlnS  = neg_log_survival(Dpair, p)
    return float((nlnS[1] - nlnS[0]) / (d_hi - d_lo))


def saturation_value(p: GLOBLEParams) -> float:
    """
    Strict D -> infinity limit of -ln S in the basic *static* GLOBLE.
    Every loop becomes clustered so n_c -> N_L, n_i -> 0:
        -ln S  ->  eps_c * N_L
    """
    return p.eps_c * p.n_l


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------
def lq_curve(dose: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """Standard LQ S(D) = exp(-αD - βD²)."""
    d = np.asarray(dose, float)
    return np.exp(-(alpha * d + beta * d ** 2))


if __name__ == "__main__":
    # Quick self-test
    p = GLOBLEParams(eps_i=0.005, eps_c=0.4)
    a, b = lq_from_globle(p)
    print(f"GLOBLE ε_i={p.eps_i} ε_c={p.eps_c}  =>  LQ α={a:.5f}  β={b:.5f}")
    p2 = globle_from_lq(a, b)
    print(f"Inversion:  ε_i={p2.eps_i:.6f}  ε_c={p2.eps_c:.6f}   (should match)")
    print(f"S(2 Gy)  = {survival(np.array([2.0]), p)[0]:.4f}")
    print(f"S(6 Gy)  = {survival(np.array([6.0]), p)[0]:.4f}")
    print(f"S(20 Gy) = {survival(np.array([20.0]), p)[0]:.4e}")
