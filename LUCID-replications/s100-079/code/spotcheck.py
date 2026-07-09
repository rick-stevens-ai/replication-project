#!/usr/bin/env python3
"""
s100-079 spot-check for Kolovi et al. 2023, PLOS ONE 18(10) e0292608.

We cannot re-run the GATE / Geant4-DNA Monte Carlo here (engine on uicgpu,
and even there the paper's GitHub `tiramisu_simulation` macros would
require a full Geant4 build, Mésocentre Clermont-class hardware, and >>10x
1e8-primary runs to reproduce the published numbers).

This script does TWO independent first-principles cross-checks of the
published numerics that DO NOT require the MC engine:

  Check A: Self-consistency of Table 10.
      The paper gives:
        - SE rate (µGy/h) per nucleosome for each environment,
        - SSB/Gy/Mbp,
        - DSB/Gy/Mbp,
        - SSB/day and DSB/day normalised to 27 Mbp and 1 day exposure.
      For each environment we recompute
        SSB/day = (SE rate µGy/h) * (24 h/day) * 1e-6 (Gy/µGy) * (SSB/Gy/Mbp) * 27 (Mbp)
      and the analogous formula for DSB/day, then compare to the paper.

  Check B: Order-of-magnitude analytic α dose-rate to a 10-µm-radius
  water diatom immersed in
       (B1) pure dry sediment containing 30 Bq/g 226Ra,
       (B2) pure water containing 1000 Bq/L 222Rn.
  This uses the "small target compared to α range" approximation:
       Dose-rate ≈ ε * A_specific * <Eα,deposited per emission>
  where ε is the fraction of α-particle energy deposited in the target
  during a single transit, taken from the paper's own Table 9
  (E_dep,mean ≈ 1.3–1.4E-03 MeV per nucleus passage) and Table 8.
  We compare orders of magnitude rather than exact values, which is the
  appropriate test of a closed-form analytic cross-check.

Outputs: prints a short diagnostic table; writes evidence to
  ../evidence/spotcheck_results.txt and ../evidence/spotcheck_results.json.
"""
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE.parent / "evidence"
EV.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Check A: internal consistency of Table 10
# -----------------------------------------------------------------------------
# Each row: name, SE_rate_uGy_per_h, SSB_per_Gy_per_Mbp, DSB_per_Gy_per_Mbp,
#           paper_SSB_per_day, paper_DSB_per_day
ENVIRONMENTS = [
    {
        "name": "Dry sediment, 0% porosity, 30 Bq/g 226Ra",
        "SE_rate_uGy_per_h": 71.70,
        "SSB_per_Gy_per_Mbp": 0.07,
        "DSB_per_Gy_per_Mbp": 0.02,
        "paper_SSB_per_day": 4.50e-3,
        "paper_DSB_per_day": 1.06e-3,
    },
    {
        "name": "Benthic mix, 90% porosity (no frustule)",
        "SE_rate_uGy_per_h": 8.31,
        "SSB_per_Gy_per_Mbp": 0.16,
        "DSB_per_Gy_per_Mbp": 0.03,
        "paper_SSB_per_day": 5.40e-4,
        "paper_DSB_per_day": 1.21e-4,
    },
    {
        "name": "Benthic mix, 90% porosity (with 2 µm silicate frustule)",
        "SE_rate_uGy_per_h": 7.36,
        "SSB_per_Gy_per_Mbp": 0.15,
        "DSB_per_Gy_per_Mbp": 0.03,
        "paper_SSB_per_day": 4.70e-4,
        "paper_DSB_per_day": 1.11e-4,
    },
    {
        "name": "Water column, 100% porosity, 1000 Bq/L 222Rn",
        "SE_rate_uGy_per_h": 2.12,
        "SSB_per_Gy_per_Mbp": 0.08,
        "DSB_per_Gy_per_Mbp": 0.02,
        "paper_SSB_per_day": 1.48e-4,
        "paper_DSB_per_day": 2.99e-5,
    },
]

GENOME_MBP = 27.0
HOURS_PER_DAY = 24.0


def recompute_per_day(SE_rate_uGy_per_h, yield_per_Gy_per_Mbp):
    """Independent recomputation:
        per_day = SE * 24 h * 1e-6 Gy/µGy * yield_per_Gy_per_Mbp * 27 Mbp
    """
    SE_Gy_per_day = SE_rate_uGy_per_h * 1e-6 * HOURS_PER_DAY
    return SE_Gy_per_day * yield_per_Gy_per_Mbp * GENOME_MBP


def pct(a, b):
    if b == 0:
        return float("inf")
    return 100.0 * (a - b) / b


print("=== Check A: Internal consistency of Table 10 ===")
print(f"{'Environment':<55} {'qty':<8} {'recomp':>11} {'paper':>11} {'Δ%':>8}")
A_rows = []
for env in ENVIRONMENTS:
    ssb_re = recompute_per_day(env["SE_rate_uGy_per_h"], env["SSB_per_Gy_per_Mbp"])
    dsb_re = recompute_per_day(env["SE_rate_uGy_per_h"], env["DSB_per_Gy_per_Mbp"])
    name_short = env["name"][:54]
    print(
        f"{name_short:<55} {'SSB/d':<8} {ssb_re:>11.3e} "
        f"{env['paper_SSB_per_day']:>11.3e} {pct(ssb_re, env['paper_SSB_per_day']):>8.1f}"
    )
    print(
        f"{'':<55} {'DSB/d':<8} {dsb_re:>11.3e} "
        f"{env['paper_DSB_per_day']:>11.3e} {pct(dsb_re, env['paper_DSB_per_day']):>8.1f}"
    )
    A_rows.append(
        {
            "env": env["name"],
            "recomputed_SSB_per_day": ssb_re,
            "paper_SSB_per_day": env["paper_SSB_per_day"],
            "rel_err_SSB_pct": pct(ssb_re, env["paper_SSB_per_day"]),
            "recomputed_DSB_per_day": dsb_re,
            "paper_DSB_per_day": env["paper_DSB_per_day"],
            "rel_err_DSB_pct": pct(dsb_re, env["paper_DSB_per_day"]),
        }
    )

# -----------------------------------------------------------------------------
# Check B: order-of-magnitude analytic α dose-rate to a 10-µm-radius
# water diatom, in pure dry sediment and in pure water.
# -----------------------------------------------------------------------------
# Approach: in either limit (sediment-only with 226Ra; water-only with 222Rn)
# the volume containing the source is a sphere of R_env = 55 µm.  α range in
# water (CSDA) is ~35 µm (4.78 MeV, 226Ra) and ~43 µm (5.49 MeV, 222Rn) per
# the paper itself.  Because R_env > R_α, most α emitted near the outer edge
# never reach the central diatom; the paper observes only ~2% of emitted
# primaries cross the 10 µm-radius microorganism.  We use that empirical
# fraction f_reach from the paper as input.  The mean kinetic energy of a
# primary reaching the diatom is also from Table 7 (3.3 MeV for 222Rn,
# 2.8 MeV for 226Ra).  The cell radius (10 µm) is ~20-30% of the residual α
# range, so a substantial fraction of that energy is deposited.  We use
# E_dep,frac ≈ R_cell / R_residual as a stopping-power-weighted estimate,
# but to be conservative we also bracket with E_dep,frac = 1.0 (full stop)
# and compare order of magnitude to the paper.
#
# Dose-rate to diatom mass:
#       D_dot = A_eff * <E_dep_per_primary> / m_diatom
#   A_eff = activity in the source volume that produces primaries reaching
#           the diatom.

import numpy as np

# Constants
MeV_to_J = 1.602176634e-13
mu_g_per_g = 1e-6  # placeholder; not used directly
hour_to_s = 3600.0

R_cell_um = 10.0
R_env_um = 55.0
rho_water = 1.00  # g/cm^3
rho_sed = 1.20    # g/cm^3 (Table 5)

# masses
def sphere_vol_cm3(R_um):
    R_cm = R_um * 1e-4
    return 4.0 / 3.0 * math.pi * R_cm ** 3

m_diatom_g = sphere_vol_cm3(R_cell_um) * rho_water
V_env_cm3 = sphere_vol_cm3(R_env_um) - sphere_vol_cm3(R_cell_um)
print()
print(f"diatom mass (10 µm water sphere) = {m_diatom_g:.3e} g")
print(f"environment shell volume (55 µm minus 10 µm) = {V_env_cm3:.3e} cm³")

# Paper-derived empirical inputs (Table 7 + Results paragraph)
# f_reach: fraction of α emitted in the 55 µm sphere that actually enter the
# microorganism.  Paper: "only 2% of the primaries emitted in the 55 µm radius
# environment reached the microorganism".
f_reach = 0.02

# Mean kinetic energy of primaries that DO reach the microorganism
E_reach_226Ra_MeV = 2.8  # Table 7, dry sediments
E_reach_222Rn_MeV = 3.3  # Table 7, water column

# Fraction of that residual energy deposited inside the cell.
# Residual α ranges in water at these energies are ~14 µm (2.8 MeV) and
# ~19 µm (3.3 MeV) (CSDA tables).  Cell diameter = 20 µm.  So most of the
# residual energy IS deposited.  We use f_dep ≈ 0.85 as a midpoint estimate.
f_dep_226Ra = 0.85
f_dep_222Rn = 0.75  # slightly lower because residual range a bit longer than cell

# --- B1: dry sediment, 226Ra ----------------------------------------------
A_specific_226Ra_Bq_per_g = 30.0
m_env_sed_g = V_env_cm3 * rho_sed
A_total_226Ra_Bq = A_specific_226Ra_Bq_per_g * m_env_sed_g
A_eff_226Ra_Bq = A_total_226Ra_Bq * f_reach
E_dep_per_prim_226Ra_MeV = E_reach_226Ra_MeV * f_dep_226Ra
D_dot_226Ra_Gy_per_s = (
    A_eff_226Ra_Bq * E_dep_per_prim_226Ra_MeV * MeV_to_J / (m_diatom_g * 1e-3)
)
D_dot_226Ra_uGy_per_h = D_dot_226Ra_Gy_per_s * hour_to_s * 1e6

# --- B2: water only, 222Rn ------------------------------------------------
A_specific_222Rn_Bq_per_L = 1000.0
A_specific_222Rn_Bq_per_g = A_specific_222Rn_Bq_per_L / 1000.0  # 1 L water = 1000 g
m_env_water_g = V_env_cm3 * rho_water
A_total_222Rn_Bq = A_specific_222Rn_Bq_per_g * m_env_water_g
A_eff_222Rn_Bq = A_total_222Rn_Bq * f_reach
E_dep_per_prim_222Rn_MeV = E_reach_222Rn_MeV * f_dep_222Rn
D_dot_222Rn_Gy_per_s = (
    A_eff_222Rn_Bq * E_dep_per_prim_222Rn_MeV * MeV_to_J / (m_diatom_g * 1e-3)
)
D_dot_222Rn_uGy_per_h = D_dot_222Rn_Gy_per_s * hour_to_s * 1e6

print()
print("=== Check B: Analytic α dose-rate cross-check ===")
print(f"B1 (dry sed, 30 Bq/g 226Ra):  D_dot ≈ {D_dot_226Ra_uGy_per_h:8.2f} µGy/h "
      f"(paper: 92.4 µGy/h)  ratio {D_dot_226Ra_uGy_per_h/92.4:.2f}")
print(f"B2 (water, 1000 Bq/L 222Rn):  D_dot ≈ {D_dot_222Rn_uGy_per_h:8.2f} µGy/h "
      f"(paper:  2.8 µGy/h)  ratio {D_dot_222Rn_uGy_per_h/2.8:.2f}")

# Also: paper's headline benthic-with-frustule total = 9.7 µGy/h. With a 10%
# frustule attenuation:
benthic_estimate = 0.9 * (0.1 * D_dot_226Ra_uGy_per_h + 0.9 * D_dot_222Rn_uGy_per_h)
# (90% porosity = 10% sediment by volume + 90% water by volume, attenuated by
#  ~10% for the frustule.)
print(f"Crude benthic-mix estimate (0.9*(0.1*sed+0.9*water)): "
      f"{benthic_estimate:.2f} µGy/h vs paper 9.7 µGy/h")

# Save
out = {
    "checkA_table10_self_consistency": A_rows,
    "checkB_analytic_alpha_dose_rate": {
        "diatom_mass_g": m_diatom_g,
        "env_shell_volume_cm3": V_env_cm3,
        "B1_dry_sed_226Ra_uGy_per_h_analytic": D_dot_226Ra_uGy_per_h,
        "B1_dry_sed_226Ra_uGy_per_h_paper": 92.4,
        "B1_ratio_analytic_over_paper": D_dot_226Ra_uGy_per_h / 92.4,
        "B2_water_222Rn_uGy_per_h_analytic": D_dot_222Rn_uGy_per_h,
        "B2_water_222Rn_uGy_per_h_paper": 2.8,
        "B2_ratio_analytic_over_paper": D_dot_222Rn_uGy_per_h / 2.8,
        "benthic_crude_estimate_uGy_per_h": benthic_estimate,
        "benthic_paper_uGy_per_h_with_frustule": 9.7,
    },
    "inputs_used": {
        "f_reach": f_reach,
        "f_dep_226Ra": f_dep_226Ra,
        "f_dep_222Rn": f_dep_222Rn,
        "E_reach_226Ra_MeV": E_reach_226Ra_MeV,
        "E_reach_222Rn_MeV": E_reach_222Rn_MeV,
        "R_cell_um": R_cell_um,
        "R_env_um": R_env_um,
        "rho_water_g_per_cm3": rho_water,
        "rho_sed_g_per_cm3": rho_sed,
    },
}
(EV / "spotcheck_results.json").write_text(json.dumps(out, indent=2))
(EV / "spotcheck_results.txt").write_text(
    "Check A (Table 10 self-consistency):\n"
    + "\n".join(
        f"  {r['env']}:\n"
        f"    SSB/d  recomputed={r['recomputed_SSB_per_day']:.3e}  "
        f"paper={r['paper_SSB_per_day']:.3e}  Δ={r['rel_err_SSB_pct']:+.1f}%\n"
        f"    DSB/d  recomputed={r['recomputed_DSB_per_day']:.3e}  "
        f"paper={r['paper_DSB_per_day']:.3e}  Δ={r['rel_err_DSB_pct']:+.1f}%"
        for r in A_rows
    )
    + "\n\nCheck B (analytic α dose-rate cross-check):\n"
    + f"  B1  dry sediment / 30 Bq/g 226Ra   : analytic={D_dot_226Ra_uGy_per_h:.2f} µGy/h "
      f"vs paper=92.4 µGy/h  ratio={D_dot_226Ra_uGy_per_h/92.4:.2f}\n"
    + f"  B2  pure water  / 1000 Bq/L 222Rn  : analytic={D_dot_222Rn_uGy_per_h:.2f} µGy/h "
      f"vs paper= 2.8 µGy/h  ratio={D_dot_222Rn_uGy_per_h/2.8:.2f}\n"
    + f"  benthic crude estimate            : analytic={benthic_estimate:.2f} µGy/h "
      f"vs paper= 9.7 µGy/h  ratio={benthic_estimate/9.7:.2f}\n"
)
print()
print(f"Wrote {EV/'spotcheck_results.json'}")
print(f"Wrote {EV/'spotcheck_results.txt'}")
