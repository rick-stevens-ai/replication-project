"""
Mariotti et al. 2013 (PLOS ONE 8:e79541) γ-H2AX foci kinetics model.

Implements eq.(1), eq.(2), eq.(3), eq.(4) from the paper, exactly as written:

  (1) N(t) = A * (1 - exp(-B*t))
  (2) N(t) = C*exp(-D*t) + (1-C)*exp(-E*t)
  (3) N(t) = A * (1 - exp(-B*t)) * [C*exp(-D*t) + (1-C)*exp(-E*t)]       # acute dose
  (4) Split: N_total(t) = N_acute(t; A1,B1,C1,D1,E1)
                       + Heaviside(t-Δt) * N_acute(t-Δt; A2,B2,C2,D2,E2)

In the paper text the symbols for the two terms of (4) are (α,β,γ,δ,ε)
for the FIRST (fixed) exposure and (A,B,C,D,E) for the SECOND (free).
Table S1 reports the second-exposure parameters under the Greek headers
(consistent with the table caption "Second exposure fitting parameters")
— here we just store both sets as 5-tuples and label them by role
(first / second), independent of which alphabet the paper used.
Time unit throughout is HOURS.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass


# ---------- Equations -----------------------------------------------------

def induction(t, A, B):
    """Eq.(1): saturating induction."""
    t = np.asarray(t, dtype=float)
    return A * (1.0 - np.exp(-B * t))


def biexp_decay(t, C, D, E):
    """Eq.(2): two-phase decay (fast fraction C, rate D; slow fraction (1-C), rate E)."""
    t = np.asarray(t, dtype=float)
    return C * np.exp(-D * t) + (1.0 - C) * np.exp(-E * t)


def acute(t, A, B, C, D, E):
    """Eq.(3): product of induction and biexp decay. t in HOURS."""
    t = np.asarray(t, dtype=float)
    # Suppress negative times -> N=0 (model meaningless before exposure)
    out = np.where(t > 0,
                   A * (1.0 - np.exp(-B * np.where(t > 0, t, 0.0)))
                     * (C * np.exp(-D * np.where(t > 0, t, 0.0))
                        + (1.0 - C) * np.exp(-E * np.where(t > 0, t, 0.0))),
                   0.0)
    return out


def split_dose(t, p_first, p_second, delta_t):
    """
    Eq.(4): independent sum of two acute exposures, the second offset by Δt.

    p_first  = (A1,B1,C1,D1,E1) for first exposure (fixed)
    p_second = (A2,B2,C2,D2,E2) for second exposure (free)
    delta_t  = gap in hours between first and second exposure
    """
    t = np.asarray(t, dtype=float)
    first = acute(t, *p_first)
    second = acute(t - delta_t, *p_second)
    return first + second


# ---------- Reported Table S1 parameter set --------------------------------

@dataclass(frozen=True)
class AcuteParams:
    A: float
    B: float
    C: float
    D: float
    E: float

    def as_tuple(self):
        return (self.A, self.B, self.C, self.D, self.E)


# From Table S1 (Mariotti 2013 supplementary DOCX) — single acute fits.
SINGLE_ACUTE = {
    "1Gy_225kVp": AcuteParams(A=24.63, B=8.011, C=0.91, D=0.23, E=3.32e-12),
    "2Gy_225kVp": AcuteParams(A=41.67, B=9.55,  C=0.41, D=0.50, E=0.06),
}

# Second-exposure parameters for split-dose (1+1 Gy, 225 kVp), Table S1.
# Indexed by the gap (Δt) between the two 1-Gy exposures.
SECOND_EXPOSURE = {
    20/60.0: AcuteParams(A=100.9,  B=0.69, C=0.15, D=2.55, E=0.15),    # 20 min
    1.0:     AcuteParams(A=27.7,   B=3.93, C=0.73, D=2.74, E=0.11),    # 1 h
    2.0:     AcuteParams(A=30.74,  B=3.22, C=0.79, D=1.84, E=0.05),    # 2 h
    5.0:     AcuteParams(A=30.4,   B=2.81, C=0.83, D=1.14, E=0.19),    # 5 h
    12.0:    AcuteParams(A=24.07,  B=6.52, C=0.93, D=0.24, E=2.4e-6),  # 12 h
}


# The first (fixed) exposure in a split-dose is 1 Gy 225 kVp, so its
# parameters are the SINGLE_ACUTE["1Gy_225kVp"] set.
FIRST_FIXED = SINGLE_ACUTE["1Gy_225kVp"]


if __name__ == "__main__":
    # Sanity check
    t = np.array([0.0, 0.5, 1.0, 6.0, 24.0])
    for label, p in SINGLE_ACUTE.items():
        print(label, "N(t) =", acute(t, *p.as_tuple()))
