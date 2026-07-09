"""
MULTISIG1 model — replication of Scott (2011), Dose-Response 9:579-601.
DOI: 10.2203/dose-response.10-039.Scott

Equations implemented:
  Eq 3:  B(D) = B0 + alpha*D                     average induced DSBs/cell, dose D
  Eq 4:  B(D) = BT + alpha*(D - T)               D > T form
  Eq 5:  BPM(D) = BT/m + alpha*(D - T)/m         average breaks per DNA molecule (m=46)
  Eq 6:  phi_1(t) = exp(-t/beta)/beta            repair-time density, 1 DSB on a molecule
  Eq 8:  phi_n(t) = (beta^-n) * t^(n-1)/(n-1)! * exp(-t/beta)   gamma density, n DSBs
  Eq 10: Att_n(D) = 100 * n * P(n, BPM(D)) / BPM(D)            attribution percent
  Eq 11: Psi_n(t) = 1 - sum_{j=0}^{n-1} ((t/beta)^j / j!) * exp(-t/beta)
  Eq 12: Cum(t,D) = sum_n [P(n, BPM(D)) * Psi_n(t)] / Omega(D), Omega = 1 - exp(-BPM(D))
  Eq 13: RB(t,D) = BT + alpha*(D - T) * (1 - Cum(t,D))         residual DSBs per cell
  Eq 14: RBM(t,D) = RB(t,D)/m

Parameter values (text and figure 5 captions, pp. 587, 592):
  BT    = 0.1   foci/cell     (Rothkamm & Lobrich 2003, Fmin)
  alpha = 0.035 /mGy           (Rothkamm & Lobrich 2003 slope)
  T     = 1.4   mGy            (threshold; Scott 2010)
  beta  = 2.5   h              (mean DSB repair time; Scott 2010, fit to R&L 2003)
  m     = 46    DNA molecules per nucleus (page 586)
  B0    = 0.05  foci/cell      (Rothkamm & Lobrich 2003; horizontal control line in Fig 5)
"""

from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass
class MultiSig1Params:
    BT: float = 0.1      # foci/cell (residual after repair)
    alpha: float = 0.035 # foci/cell per mGy
    T: float = 1.4       # mGy (epicellcom threshold)
    beta: float = 2.5    # h (mean DSB repair time)
    m: int = 46          # chromosomes/DNA molecules per nucleus
    B0: float = 0.05     # foci/cell, spontaneous baseline (R&L 2003)


def B_of_D(D: float, p: MultiSig1Params) -> float:
    """Eq 3: average induced DSBs per cell at dose D (high-rate brief exposure)."""
    return p.B0 + p.alpha * D


def BPM(D: float, p: MultiSig1Params) -> float:
    """Eq 5: average breaks per DNA molecule. Defined for D > T; clamped at 0 otherwise."""
    if D <= p.T:
        # Below threshold: no epicellcom repair; per-molecule average is BT/m only
        # (text: below T, DSBs persist; eq 5 form applies for D > T)
        return p.BT / p.m
    return p.BT / p.m + p.alpha * (D - p.T) / p.m


def poisson_pmf(n: int, lam: float) -> float:
    """P(n; lam) = exp(-lam) lam^n / n!"""
    if lam <= 0:
        return 1.0 if n == 0 else 0.0
    return math.exp(-lam) * (lam ** n) / math.factorial(n)


def phi_n(n: int, t: float, p: MultiSig1Params) -> float:
    """Eq 8: gamma density for time to repair n DSBs on the same molecule."""
    if t < 0 or n < 1:
        return 0.0
    return ((p.beta ** -n) * (t ** (n - 1)) / math.factorial(n - 1)) * math.exp(-t / p.beta)


def Psi_n(n: int, t: float, p: MultiSig1Params) -> float:
    """Eq 11: cumulative distribution function for repair of n DSBs."""
    if t < 0:
        return 0.0
    s = 0.0
    x = t / p.beta
    for j in range(n):  # 0..n-1
        s += (x ** j) / math.factorial(j)
    return 1.0 - s * math.exp(-x)


def Cum(t: float, D: float, p: MultiSig1Params, n_max: int = 30) -> float:
    """Eq 12: Poisson-weighted cumulative repair probability across n=1..n_max."""
    lam = BPM(D, p)
    if lam <= 0:
        return 0.0
    omega = 1.0 - math.exp(-lam)
    if omega <= 0:
        return 0.0
    s = 0.0
    for n in range(1, n_max + 1):
        s += poisson_pmf(n, lam) * Psi_n(n, t, p)
    return s / omega


def Att_n(n: int, D: float, p: MultiSig1Params) -> float:
    """Eq 10: percent attribution to overall repair kinetics from n-DSB molecules."""
    lam = BPM(D, p)
    if lam <= 0:
        return 0.0
    return 100.0 * n * poisson_pmf(n, lam) / lam


def RB(t: float, D: float, p: MultiSig1Params, n_max: int = 30) -> float:
    """Eq 13: residual DSBs per cell at time t after dose D."""
    if D <= p.T:
        # Below threshold: no repair; eq 3 (constant in t)
        return B_of_D(D, p)
    return p.BT + p.alpha * (D - p.T) * (1.0 - Cum(t, D, p, n_max=n_max))


def RBM(t: float, D: float, p: MultiSig1Params, n_max: int = 30) -> float:
    """Eq 14: residual DSBs per DNA molecule."""
    return RB(t, D, p, n_max=n_max) / p.m
