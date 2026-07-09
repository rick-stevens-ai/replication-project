#!/usr/bin/env python3
"""
Independent reproduction of Eq. 1 (Humm & Charlton 1989) used in
Carrasco-Hernandez et al. 2023, Front. Med. 10:1253746.

    N0 = N_DSB / [ (1 - exp(-lambda*t)) * (f + 35*D) ]

With:
    N_DSB = 194  (DSB produced by 100 decays/cell of 125I, used as reference)
    t     = 24 h (cell cycle G2 -> G1)
    f     = DSB/decay from short-range emissions (= the per-decay DSB yield they tabulate)
    35*D  = damage from long-range emissions (taken to be folded into f for this paper)
    The paper folds (f + 35D) == DSB/decay reported in Table 1 (0.25 nm column).

After computing N0, multiply by 2 to account for the first cell division.

Then initial activity per cell = lambda * N0 * 2.

We compare against Table 2.
"""
from __future__ import annotations
import math

# Half-lives (in hours), per NNDC / Decay Data Evaluation Project
HALF_LIFE_H = {
    "125I":  60.140 * 24,       # 60.14 d -> hours
    "123I":  13.2235,           # h
    "111In": 67.317,            # 2.8047 d -> 67.31 h (NNDC)
    "99mTc":  6.0067,           # h
    "64Cu":  12.7012,           # h
}

# DSB per decay at 0.25 nm off central DNA axis, from Table 1 of the paper
DSB_PER_DECAY_025 = {
    "125I":  1.94,
    "123I":  1.20,
    "111In": 1.09,
    "99mTc": 0.378,
    "64Cu":  0.171,
}

# Statistical uncertainty (1 sigma) on DSB/decay at 0.25 nm
DSB_PER_DECAY_025_SIG = {
    "125I":  0.01,
    "123I":  0.01,
    "111In": 0.01,
    "99mTc": 0.003,
    "64Cu":  0.003,
}

# Paper's reported values from Table 2 (this-work columns) for cross-check
PAPER_N0 = {
    "125I":  (17416, 46),
    "123I":  (451, 2),
    "111In": (1625, 8),
    "99mTc": (1095, 4),
    "64Cu":  (3107, 28),
}
PAPER_BQ = {  # initial activity per cell, Bq * 1e-3
    "125I":  (2.32, 0.01),
    "123I":  (6.58, 0.03),
    "111In": (4.65, 0.02),
    "99mTc": (35.0, 0.1),
    "64Cu":  (47.1, 0.4),
}

N_DSB_REF = 194.0   # DSB from 100 decays/cell of 125I (paper's calibration anchor)
T_HOURS   = 24.0    # cell cycle length used in the paper

print("Independent reproduction of Eq. 1 (Humm & Charlton 1989)\n")
print(f"  Anchor: N_DSB = {N_DSB_REF}  (100 decays of 125I)")
print(f"  Cell cycle t = {T_HOURS} h")
print(f"  Final atom count multiplied by 2 (first cell division)\n")

hdr = f"{'Nuc':<6}{'T1/2(h)':>10}{'lambda(/h)':>14}{'DSB/dec':>10}{'(1-e^-lt)':>12}{'N0 calc':>12}{'N0 paper':>12}{'rel err':>10}{'A_calc(Bq*1e-3)':>18}{'A_paper':>10}"
print(hdr)
print("-" * len(hdr))

results = []
for nuc in ["125I", "123I", "111In", "99mTc", "64Cu"]:
    t12 = HALF_LIFE_H[nuc]
    lam = math.log(2) / t12              # per hour
    f   = DSB_PER_DECAY_025[nuc]
    factor = 1.0 - math.exp(-lam * T_HOURS)
    N0_single = N_DSB_REF / (factor * f)
    N0 = N0_single * 2.0                  # first cell division
    # Initial activity per cell:  A = lambda * N0
    # lambda in s^-1: lam_s = ln2 / (t12 * 3600)
    lam_s = math.log(2) / (t12 * 3600.0)
    A_bq = lam_s * N0
    A_bq_milli = A_bq * 1e3               # Bq * 1e-3 units used in paper
    N0_paper, _ = PAPER_N0[nuc]
    A_paper, _  = PAPER_BQ[nuc]
    rel_n0 = (N0 - N0_paper) / N0_paper * 100.0
    print(f"{nuc:<6}{t12:>10.3f}{lam:>14.6f}{f:>10.3f}{factor:>12.4f}{N0:>12.0f}{N0_paper:>12d}{rel_n0:>9.2f}%{A_bq_milli:>18.3f}{A_paper:>10.3f}")
    results.append((nuc, N0, N0_paper, A_bq_milli, A_paper, rel_n0))

print("\nNotes on the cross-check:")
print(" * If the paper's Eq. 1 is interpreted literally with N_DSB=194 and t=24 h,")
print("   the recovered N0 should equal the paper's reported N0 within ~1% rounding.")
print(" * Discrepancies trace to (a) the per-decay DSB yield rounded for Table 2 vs")
print("   the actual stat-mean used internally, and (b) the half-life database used.")
