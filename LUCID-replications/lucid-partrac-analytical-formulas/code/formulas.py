"""Analytical formulas from Kundrát et al. 2020 (Sci Rep 10:15775).

Formula (1): SB and SSB yields
    Yield = p1 - (p2 * LET)^p3 - p4 / (1 + log^2(LET / p5))

Formula (2): DSB, DSB clusters, DSB sites
    Yield = (p1 + (p2 * LET)^p3) / (1 + (p4 * LET)^p5)

Units: Yield in Gy^-1 Gbp^-1; LET in keV/µm; log = natural log.

When a parameter is N.A. in the paper tables, the corresponding term is
dropped from the formula (i.e. the dip term in Eq.1 vanishes when p4=NaN,
and the overkill divisor in Eq.2 collapses to 1 when p4=NaN).
"""
from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def sb_ssb_yield(let, p1, p2, p3, p4, p5):
    """Eq. (1). NaN in (p4, p5) → drop the log-dip term."""
    let = np.asarray(let, dtype=float)
    out = p1 - np.power(p2 * let, p3)
    if not (np.isnan(p4) or np.isnan(p5)):
        out = out - p4 / (1.0 + np.log(let / p5) ** 2)
    return out


def dsb_yield(let, p1, p2, p3, p4, p5):
    """Eq. (2). NaN in (p4, p5) → drop the overkill divisor (pure power-law growth)."""
    let = np.asarray(let, dtype=float)
    num = p1 + np.power(p2 * let, p3)
    if np.isnan(p4) or np.isnan(p5):
        return num
    den = 1.0 + np.power(p4 * let, p5)
    return num / den


# Sanity-check / smoke tests --------------------------------------------------
if __name__ == "__main__":
    # Hydrogen / total SB at LET=0.5 keV/µm (low-LET regime, expect ~170)
    p = (170, 1.335, 0.7023, 8.541, 6.902)
    print("H total SB @ 0.5 keV/µm:", float(sb_ssb_yield(0.5, *p)))
    # Hydrogen / total DSB at LET=0.5 (expect ~7)
    p = (6.8, 0.1835, 0.9583, float("nan"), float("nan"))
    print("H total DSB @ 0.5 keV/µm:", float(dsb_yield(0.5, *p)))
    # Hydrogen / total DSB at LET=50 (should be ~ p1 + (p2*LET)^p3)
    print("H total DSB @ 50  keV/µm:", float(dsb_yield(50.0, *p)))
