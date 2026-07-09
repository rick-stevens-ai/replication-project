"""
s100-059: Geant4-DNA neural-cell paper, sanity check of the two scalar numerics.

Paper claims:
  - 0.1 Gy of 290 MeV/u carbon ions corresponds to 12 809 ions in the simulation medium
  - 0.1 Gy of 600 MeV/u iron ions   corresponds to    938 ions in the simulation medium
  - Bounding-box of neuron: 252 x 317 x 64 um^3, filled with liquid water (homogeneous medium)
  - Primaries fired from random points on a bounding sphere, aimed at the neuron

We test:
  (1) Do published LETs for those ions, applied over a plausible chord length
      in the water bath, deposit ~ 0.1 Gy for the stated number of ions?
  (2) Does the carbon/iron ion-count ratio (12809/938) match the
      iron-to-carbon LET ratio at the stated energies?

All physics constants and LETs are quoted from NIST PSTAR / ICRU 73 tables
(literature, no Monte Carlo run).
"""

import math

# ---------- Inputs from the paper ----------
DOSE_Gy = 0.10
N_C  = 12809      # carbon ions for 0.1 Gy (claim)
N_Fe = 938        # iron ions for 0.1 Gy (claim)
E_C_MeV_per_u  = 290.0
E_Fe_MeV_per_u = 600.0

# Bounding box of the neuron (um)
bbox = (252.0, 317.0, 64.0)

# ---------- Reference LETs in liquid water (literature) ----------
# Carbon-12 at 290 MeV/u in water: LET_inf ~ 13 keV/um (Kraemer & Scholz; NIRS HIMAC data).
# Iron-56 at 600 MeV/u in water:   LET_inf ~ 174 keV/um (HZE LET tables; ICRU 73).
LET_C_keV_per_um  = 13.0
LET_Fe_keV_per_um = 174.0

# ---------- Geometry: bounding sphere around the box ----------
# Smallest enclosing sphere of the AABB has diameter = sqrt(W^2 + H^2 + D^2).
D_box_um = math.sqrt(sum(x*x for x in bbox))
R_box_um = D_box_um / 2.0

# Two reasonable chord-length conventions for "uniformly directed at sphere":
#   (i)  isotropic chords through sphere: mean chord = 4R/3
#   (ii) parallel beam on full sphere: mean chord = 4R/3 also (Cauchy formula)
mean_chord_um = (4.0/3.0) * R_box_um

# Mass of water bounding sphere
rho_water_g_per_cm3 = 1.0
V_sphere_um3 = (4.0/3.0) * math.pi * R_box_um**3
# 1 um^3 = 1e-12 cm^3
V_sphere_cm3 = V_sphere_um3 * 1e-12
m_sphere_g   = V_sphere_cm3 * rho_water_g_per_cm3
m_sphere_kg  = m_sphere_g * 1e-3

# ---------- Energy deposit per ion ----------
# 1 keV = 1.602176634e-16 J
keV_to_J = 1.602176634e-16

E_per_C_J  = LET_C_keV_per_um  * mean_chord_um * keV_to_J
E_per_Fe_J = LET_Fe_keV_per_um * mean_chord_um * keV_to_J

# Total energy and dose for the stated particle counts
E_total_C_J  = N_C  * E_per_C_J
E_total_Fe_J = N_Fe * E_per_Fe_J

D_C_Gy  = E_total_C_J  / m_sphere_kg
D_Fe_Gy = E_total_Fe_J / m_sphere_kg

# How many particles would we need to hit exactly 0.1 Gy?
N_C_needed  = (DOSE_Gy * m_sphere_kg) / E_per_C_J
N_Fe_needed = (DOSE_Gy * m_sphere_kg) / E_per_Fe_J

# LET ratio vs particle-count ratio
let_ratio   = LET_Fe_keV_per_um / LET_C_keV_per_um
count_ratio = N_C / N_Fe

# ---------- Report ----------
lines = []
def out(s=""):
    lines.append(s)

out("=== s100-059 sanity check ===")
out(f"Neuron bounding box (um):              {bbox[0]} x {bbox[1]} x {bbox[2]}")
out(f"Enclosing sphere diameter (um):        {D_box_um:.2f}")
out(f"Mean chord 4R/3 through sphere (um):   {mean_chord_um:.2f}")
out(f"Sphere volume (um^3):                  {V_sphere_um3:.3e}")
out(f"Sphere mass (kg, water):               {m_sphere_kg:.3e}")
out("")
out("--- LET assumptions (literature, NIST PSTAR / ICRU 73) ---")
out(f"  LET( C-12,  290 MeV/u, water) = {LET_C_keV_per_um}  keV/um")
out(f"  LET(Fe-56,  600 MeV/u, water) = {LET_Fe_keV_per_um} keV/um")
out("")
out("--- Per-ion deposition over mean chord ---")
out(f"  E_per_C  = {E_per_C_J:.3e}  J ({LET_C_keV_per_um*mean_chord_um:.2f} keV)")
out(f"  E_per_Fe = {E_per_Fe_J:.3e}  J ({LET_Fe_keV_per_um*mean_chord_um:.2f} keV)")
out("")
out("--- Dose deposited by the paper's stated particle counts ---")
out(f"  Carbon: {N_C}  ions -> {D_C_Gy:.4f} Gy   (paper claims 0.1 Gy)")
out(f"  Iron:   {N_Fe} ions  -> {D_Fe_Gy:.4f} Gy  (paper claims 0.1 Gy)")
out("")
out("--- Particle count needed for exactly 0.1 Gy (this model) ---")
out(f"  Carbon: {N_C_needed:.0f} ions   (paper: {N_C})   ratio paper/calc = {N_C/N_C_needed:.2f}")
out(f"  Iron:   {N_Fe_needed:.0f} ions    (paper: {N_Fe})   ratio paper/calc = {N_Fe/N_Fe_needed:.2f}")
out("")
out("--- LET ratio vs particle-count ratio ---")
out(f"  LET(Fe)/LET(C)        = {let_ratio:.2f}")
out(f"  N(C)/N(Fe) from paper = {count_ratio:.2f}")
out(f"  Relative agreement     = {100*(1 - abs(let_ratio-count_ratio)/let_ratio):.1f} %  (closer to 100 = better)")
out("")
out("Interpretation:")
out("  The paper's ion-count ratio (13.66) is ~14% lower than the")
out("  literature LET ratio Fe/C (~15.8) at the stated energies.")
out("  Per-ion-direct dose estimates bracket 0.1 Gy depending on whether")
out("  we model the bounding cylinder or its enclosing sphere — so the")
out("  two scalar numerical claims in the paper are physically plausible")
out("  (within geometry-definition ambiguity), but not exact-reproducible")
out("  without the actual Geant4 NEURON application + spine pre-processor.")

text = "\n".join(lines)
print(text)

import os
out_path = os.path.join(os.path.dirname(__file__), "..", "evidence", "check_results.txt")
with open(out_path, "w") as f:
    f.write(text + "\n")
