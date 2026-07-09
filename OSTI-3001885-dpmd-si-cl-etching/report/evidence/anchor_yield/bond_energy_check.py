#!/usr/bin/env python3
"""
Sanity check: reference Si-Cl and SiCl4 energetics from public NIST/JANAF-derived values.

The paper C11 (method viability) implies the DeepMD potential should reproduce
DFT-comparable energetics. We do NOT run DeepMD here — but we DO look at the
canonical Si-Cl gas-phase dissociation energies which the paper's PBE reference
must reproduce (else the etch chemistry is broken).

Reference data (public, textbook / JANAF):
    Si-Cl single bond enthalpy   : ~380-400 kJ/mol  = 3.94-4.14 eV
    Si-H single bond enthalpy    : ~318 kJ/mol      = 3.30 eV
    Cl-Cl single bond enthalpy   : ~242 kJ/mol      = 2.51 eV
    SiCl4 atomization enthalpy   : ~1568 kJ/mol / 4 = 4.06 eV/bond
    SiCl4 -> SiCl3 + Cl  BDE     : ~381 kJ/mol      = 3.95 eV

These serve as a physical "reasonability window" for any PBE-trained potential
of Si-Cl. The paper reports its training uses PBE with 110/440 Ry cutoffs and
PSLibrary 1.0.0 ultrasoft PPs at Quantum ESPRESSO v6.4.1 — a level of theory
that consistently reproduces Si-Cl gas-phase bond energies to within ~0.1 eV.

We record these accepted values and check the paper's stated etch products
(SiCl, SiCl2, SiCl3, SiCl4) are energetically consistent with the well-known
bond-strength ordering.
"""

import json

# eV per bond (from NIST WebBook / JANAF / Luo Comprehensive Handbook of Chemical Bond Energies)
KJMOL_PER_EV = 96.485
bond_data = {
    "Si-Cl_gas_phase_BDE_eV":         380.0 / KJMOL_PER_EV,
    "Si-Cl_gas_phase_BDE_kJmol":      380.0,
    "Si-H_BDE_eV":                    318.0 / KJMOL_PER_EV,
    "Cl-Cl_BDE_eV":                   242.0 / KJMOL_PER_EV,
    "SiCl4_atomization_per_bond_eV":  1568.0 / 4.0 / KJMOL_PER_EV,
    "SiCl4_->_SiCl3+Cl_BDE_eV":       381.0 / KJMOL_PER_EV,
    "Si-Si_diamond_cohesion_eV":      4.63,          # experimental cohesive
    "expected_PBE_error_eV":          0.10,          # PBE for Si-Cl typically <0.1 eV MAE
}

# Physical sanity: paper claims SiCl4 is the dominant volatile product at low
# ion energy. This requires Si-Cl bond to be strong enough that 4 Si-Cl bonds
# outweigh 1 Si-Si + 1 Cl-Cl for the etch reaction:
#    Si(s) + 2 Cl2(g) -> SiCl4(g)     dH ~ -662 kJ/mol   (exothermic)
# Check:
dH_atomize_SiCl4  = 1568.0                    # kJ/mol
dH_atomize_Si     = 446.0                     # Si(s)->Si(g), kJ/mol
dH_2Cl2_atomize   = 2 * 242.0                 # 2 Cl2 -> 4 Cl
dH_reaction = dH_atomize_SiCl4 - dH_atomize_Si - dH_2Cl2_atomize
# note this is -formation enthalpy of SiCl4 from atoms; sign convention: negative = exothermic
bond_data["Si+2Cl2->SiCl4_dH_kJmol_estimate"] = -dH_reaction
bond_data["exothermic_check"] = (dH_reaction > 0)

# All 4 Si-Cl bonds combined (4*3.94 = 15.76 eV) vs Si-Si (4.63) + 2 Cl-Cl (2*2.51 = 5.02) = 9.65 eV
lhs = 4 * bond_data["Si-Cl_gas_phase_BDE_eV"]
rhs = 4.63 + 2 * bond_data["Cl-Cl_BDE_eV"]
bond_data["4SiCl_vs_Si+2ClCl_eV"] = {
    "lhs_4SiCl_bonds_eV": lhs,
    "rhs_SiSi_2ClCl_eV":  rhs,
    "energy_gain_per_Si_etched_eV": lhs - rhs,
    "consistent_with_SiCl4_dominant_low_E_paper_claim_C10": (lhs > rhs),
}

# Ion energy vs Si-Si cohesion: for pure sputter, Eth ~ 2-4 x cohesion.
# Si cohesion 4.63 eV -> Eth ~ 10-19 eV. Chang exp Eth ~ 16-28 eV (our fit gave 28 eV).
# Paper DP at 35 eV badly over-predicts (its effective Eth fits <0).
bond_data["expected_physical_Eth_ClAr_range_eV"] = {
    "lower_from_Si_cohesion_2x": 2*4.63,
    "upper_from_Si_cohesion_4x": 4*4.63,
    "chang_experimental_fit_Eth": 28.0,
    "steinbruechel_1989_report": 16.0,
    "paper_DP_fit_Eth":  -2.3,   # nonphysical -> paper is missing/wrong threshold
    "interpretation": "Paper DP has NO effective threshold — over-predicts at 35 eV by 4x. Physically expected Eth ~ 10-30 eV.",
}

print(json.dumps(bond_data, indent=2))
with open("bond_energy_check.json","w") as fh:
    json.dump(bond_data, fh, indent=2)
print("\nSaved bond_energy_check.json")
