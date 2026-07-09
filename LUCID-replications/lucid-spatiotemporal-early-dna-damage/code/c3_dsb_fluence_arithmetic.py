"""
Claim A3 / c3: File S1 arithmetic for DSBs per ion track.

Paper File S1 text:
  "The linear parameter for the number of DSBs was determined from the ion
   fluence (in our experiments 3·10^6 1/cm^2), the LET, and the assumption
   that there are on average 35 DSBs per Gray [Prise 1998], resulting in
   28 DSBs at an LET of 170 keV/um."

Test: from (LET, fluence, 35 DSB/Gy), can we recover ~28 DSBs/track at LET=170?

Method:
  Dose [Gy] = LET [keV/um] * fluence [/cm^2] * unit-conversion
  1 Gy = 1 J/kg = 6.242e15 keV/kg
  fluence in /cm^2; depth/path through a cell layer is implicit, so the
  authors are effectively computing local dose along an ion track within a
  thin nuclear layer of mass density ~1 g/cm^3.

  LET * fluence = energy deposited per unit area per unit length-along-track
    = keV/um * 1/cm^2
  Convert to J/(m^3): keV/um -> J/m = 1.602e-16 J / 1e-6 m = 1.602e-10 J/m
                     /cm^2 -> /m^2 = 1e4 /m^2
   product:  1.602e-10 * 1e4 = 1.602e-6 J/(m^3) per (keV/um * 1/cm^2)
  Density water = 1000 kg/m^3, so dose (Gy=J/kg) = J/m^3 / 1000
                                                = 1.602e-9 Gy per (keV/um * /cm^2)

For LET=170 keV/um, fluence=3e6 /cm^2:
  Dose = 170 * 3e6 * 1.602e-9 = 0.817 Gy
  DSBs = 35 DSBs/Gy * 0.817 Gy = 28.6 DSBs

Matches paper's "28 DSBs at LET=170 keV/um".
"""
import json
import os

LET = 170.0                  # keV/um
FLUENCE = 3.0e6              # /cm^2 (3*10^6 ions per cm^2)
DSB_PER_GY = 35.0            # paper assumption [Prise 1998]
DENSITY = 1000.0             # kg/m^3 (water)

# Unit conversion: (keV/um) * (1/cm^2) -> J/m^3
# 1 keV = 1.602176634e-16 J
# 1/um = 1e6 /m
# (keV/um) -> J/m = 1.602176634e-16 * 1e6 = 1.602176634e-10 J/m
# 1/cm^2 = 1e4 /m^2
# product: J/m^3 = 1.602176634e-10 * 1e4 = 1.602176634e-6
J_PER_M3_PER_UNIT = 1.602176634e-10 * 1e4

energy_density_J_per_m3 = LET * FLUENCE * J_PER_M3_PER_UNIT  # J/m^3
dose_Gy = energy_density_J_per_m3 / DENSITY                  # Gy = J/kg
dsbs_per_track_estimate = DSB_PER_GY * dose_Gy

PAPER_VALUE = 28.0
abs_err = dsbs_per_track_estimate - PAPER_VALUE
rel_err = abs_err / PAPER_VALUE

print(f"LET            = {LET} keV/um")
print(f"Fluence        = {FLUENCE:.2e} /cm^2")
print(f"DSB/Gy         = {DSB_PER_GY}")
print(f"Energy density = {energy_density_J_per_m3:.4e} J/m^3")
print(f"Dose           = {dose_Gy:.4f} Gy")
print(f"DSBs computed  = {dsbs_per_track_estimate:.2f}")
print(f"Paper value    = {PAPER_VALUE}")
print(f"Abs error      = {abs_err:+.3f}")
print(f"Rel error      = {rel_err:+.2%}")

out = {
    "claim": "A3_DSB_fluence_arithmetic",
    "LET_keV_per_um": LET,
    "fluence_per_cm2": FLUENCE,
    "DSB_per_Gy": DSB_PER_GY,
    "density_kg_per_m3": DENSITY,
    "energy_density_J_per_m3": energy_density_J_per_m3,
    "dose_Gy": dose_Gy,
    "DSBs_per_track_computed": dsbs_per_track_estimate,
    "paper_value": PAPER_VALUE,
    "abs_error": abs_err,
    "rel_error": rel_err,
    "verdict": "REPRODUCED" if abs(rel_err) < 0.05 else "MISMATCH",
}
out_path = os.path.join(os.path.dirname(__file__), "..", "results", "c3_dsb_fluence.json")
out_path = os.path.normpath(out_path)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved -> {out_path}")
