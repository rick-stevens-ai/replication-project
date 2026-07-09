#!/usr/bin/env python3
"""
Reduced analytic smoke check for Yu, Geng, Tang (Med Phys 2024) — BNCT via MEDRAS.

What this does (CPU-only, no Geant4 / TOPAS / Monte Carlo):
  1) Use the public analytic MEDRAS (sjmcmahon/MEDRAS) to compute survival curves
     for the BNCT-relevant radiation components:
        - photon  (reference)
        - low-LET proton (~5 keV/um, recoil protons high-energy tail)
        - mid-LET proton (~17 keV/um, 0.58 MeV proton from 14N(n,p)14C)
        - high-LET helium track (~150 keV/um, surrogate for alpha+7Li 'boron dose')
  2) Fit each curve to LQ (-ln S = a*D + b*D^2) over 0-10 Gy.
  3) Compute RBE at SF = 0.5, 0.1, 0.01 vs the photon reference.
  4) Build a 'BNCT total' survival via the paper's accumulation formula (Eq. 6):
        -ln S(D_mix) = sum_i (alpha_i D_i + beta_i D_i^2)
     for a representative BPA-style dose split (boron 65%, proton 17%, photon 18%).
  5) Print a table comparable in spirit to Table 1 of Yu et al. 2024.

Caveats vs the paper:
  - The paper's Monte Carlo MEDRAS version uses Geant4-DNA-derived radial energy
    deposition for BNCT-specific alpha (0.2-1.78 MeV) and 7Li (0.2-1.02 MeV)
    secondaries, plus TOPAS-nBio dose factors F and W tied to BPA/BSH microdistributions.
    None of those microdistribution probability files are provided as supplements.
  - The analytic MEDRAS shipped on GitHub only carries pre-computed tracks for
    protons, helium, carbon, nitrogen. We use Helium @ LET=150 keV/um as a surrogate
    for the combined alpha+7Li boron dose (avg LET ~150-200 keV/um in this regime).
  - Therefore exact numerical reproduction of Table 1 is NOT expected; we reproduce
    the methodology (LQ fits + RBE at fixed SF + Eq.6 accumulation) and the
    qualitative trends.
"""

import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MEDRAS = os.path.join(HERE, "..", "artifacts", "medras_analytic")
sys.path.insert(0, MEDRAS)
from medras import medrascell  # noqa: E402


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def survival_curve(exposure_template, doses):
    cell = medrascell.singleCell()
    return [cell.survival({**exposure_template, "dose": d}) for d in doses]


def fit_lq(doses, sfs):
    d = np.array(doses[1:], dtype=float)
    y = -np.log(np.array(sfs[1:], dtype=float))
    X = np.vstack([d, d * d]).T
    (a, b), *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(a), float(b)


def dose_at_sf(target_sf, alpha, beta):
    rhs = -math.log(target_sf)
    if beta <= 1e-9:
        return rhs / alpha
    return (-alpha + math.sqrt(alpha * alpha + 4.0 * beta * rhs)) / (2.0 * beta)


# ----------------------------------------------------------------------
# 1) build component curves
# ----------------------------------------------------------------------
DOSES = [0, 0.5, 1, 2, 3, 4, 6, 8, 10]

components = {
    "photon":  ({"time": 0},                                 "reference (default X-ray track)"),
    "p_low":   ({"time": 0, "LET": 5,   "particle": 1},      "recoil proton (high-energy tail)"),
    "p_mid":   ({"time": 0, "LET": 17,  "particle": 1},      "0.58 MeV proton from 14N(n,p)14C"),
    "boron":   ({"time": 0, "LET": 150, "particle": 2},      "helium track @150 keV/um (alpha+7Li surrogate)"),
}

fits = {}
print(f"{'component':<10} {'alpha [/Gy]':>12} {'beta [/Gy^2]':>13}   description")
print("-" * 78)
for name, (exp, desc) in components.items():
    sf = survival_curve(exp, DOSES)
    a, b = fit_lq(DOSES, sf)
    fits[name] = (a, b)
    print(f"{name:<10} {a:12.3f} {b:13.4f}   {desc}")


# ----------------------------------------------------------------------
# 2) RBE table (vs photon)
# ----------------------------------------------------------------------
a_ref, b_ref = fits["photon"]
print("\nRBE at fixed survival fractions (vs photon reference):")
print(f"{'component':<10} {'D@SF=0.5':>10} {'RBE50':>7} {'D@SF=0.1':>10} {'RBE10':>7} {'D@SF=0.01':>11} {'RBE1':>7}")
for name, (a, b) in fits.items():
    row = [name]
    for sf_target in (0.5, 0.1, 0.01):
        D_ref = dose_at_sf(sf_target, a_ref, b_ref)
        D = dose_at_sf(sf_target, a, b)
        rbe = D_ref / D
        row.append(f"{D:10.2f}")
        row.append(f"{rbe:7.2f}")
    print(f"{row[0]:<10} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}")


# ----------------------------------------------------------------------
# 3) Eq. 6 accumulation for a BPA-like dose split
#    paper says: high boron concentration -> boron 65%, proton 17%, photon 18%
# ----------------------------------------------------------------------
print("\nEq. 6 accumulation (paper Section 2.4) for a BPA-like high-boron split:")
share = {"boron": 0.65, "p_mid": 0.17, "photon": 0.18}
print(f"  share: {share}")
mix_doses = np.linspace(0, 10, 21)
mix_sf = []
for Dmix in mix_doses:
    log_acc = 0.0
    for comp, frac in share.items():
        a, b = fits[comp]
        Di = frac * Dmix
        log_acc += a * Di + b * Di * Di
    mix_sf.append(math.exp(-log_acc))

print(f"{'Dmix [Gy]':>10} {'S(Dmix)':>10}")
for D, S in zip(mix_doses, mix_sf):
    print(f"{D:10.2f} {S:10.4f}")

# Quick RBE of the BPA-like mix at SF=0.01
a_mix, b_mix = fit_lq(mix_doses.tolist(), mix_sf)
D_mix_1pct = dose_at_sf(0.01, a_mix, b_mix)
D_ref_1pct = dose_at_sf(0.01, a_ref, b_ref)
print(f"\nMix LQ fit: alpha={a_mix:.3f} beta={b_mix:.4f}")
print(f"D_mix@SF=0.01 = {D_mix_1pct:.2f} Gy  vs  D_photon@SF=0.01 = {D_ref_1pct:.2f} Gy")
print(f"Mix RBE_0.01 (this smoke run) = {D_ref_1pct / D_mix_1pct:.2f}")
print("Paper Table 1: BPA total RBE_1 = 2.50 (experimental refs: 2.52, 2.81)")
print("Order-of-magnitude agreement is the success criterion for this analytic smoke check.")
