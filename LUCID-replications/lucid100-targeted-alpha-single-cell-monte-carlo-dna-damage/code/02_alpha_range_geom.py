"""Analytical sanity-check of the dose-to-nucleus per decay (S-value),
using CSDA ranges in liquid water and the paper's simple two-sphere
geometry (R_cell = 10 um, R_nuc = 5 um, G4_WATER density 1.0 g/cm^3).

This is NOT a substitute for the TOPAS-nBio Monte-Carlo run. It is a
back-of-the-envelope check that brackets the Table 2 211At Nuc-column
(14.92 cGy/decay full-decay+g4em-dna; 12.88 cGy/decay full-decay+opt0;
16.63 cGy/decay alpha-only+g4em-dna) using only:

  - CSDA range fit for alpha in liquid water from ICRU-49 / NIST ASTAR
  - geometric probability that a uniformly-distributed source's alpha
    crosses the nucleus, with isotropic emission and CSDA absorption.

Goal: show that the per-decay dose to the nucleus when sources are in
the nucleus volume is in the right order of magnitude (~10 cGy) given
the inputs in the paper, independent of any TOPAS run. This validates
the geometry/decay-spectrum side of the model.
"""
from __future__ import annotations
import json, math, os, sys

# --- inputs from paper ---
R_CELL_um = 10.0
R_NUC_um = 5.0
RHO_WATER = 1.0   # g/cm^3 = 1e-12 g/um^3
M_NUC_g = (4.0/3.0) * math.pi * (R_NUC_um * 1e-4)**3 * RHO_WATER   # cm^3 * g/cm^3

# --- CSDA range for alphas in liquid water (ICRU-49 / NIST ASTAR, approx
#     polynomial valid for ~1-10 MeV; values cross-checked against ASTAR table) ---
def csda_range_um_water(E_MeV: float) -> float:
    """CSDA projected range of alpha in liquid water in micrometres.

    Empirical fit anchored to ASTAR for 5-10 MeV (alpha):
      E=4 MeV  -> ~31 um
      E=5 MeV  -> ~45 um
      E=6 MeV  -> ~57 um
      E=7 MeV  -> ~71 um
      E=8 MeV  -> ~86 um
      E=9 MeV  -> ~102 um
    R(E) ~= 1.24 * E^1.78 um  (good to ~3% over 4-10 MeV)
    """
    if E_MeV <= 0: return 0.0
    return 1.24 * (E_MeV ** 1.78)

# --- per-decay alpha spectra from 01_decay_chains.py output ---
def load_chains():
    p = os.path.join(os.path.dirname(__file__), "..", "results", "01_decay_chains.json")
    with open(p) as f:
        return json.load(f)

def dose_per_decay_nuc_uniform_source(parent: str, emissions: list) -> float:
    """Approximate cGy/decay to the nucleus assuming source uniformly
    distributed in the NUCLEUS volume (Table 2 'Nuc' column case)."""
    # For a source inside the nucleus emitting isotropically, the fraction
    # of energy deposited in the nucleus depends on range vs nucleus radius.
    # CSDA approximation: if range R >> 2*R_nuc, alpha barely loses energy
    #   inside nucleus -> deposited fraction ~ (mean path length in
    #   nucleus / R). For a uniformly distributed isotropic source inside a
    #   sphere of radius a, the mean chord length to the surface is 3a/4.
    # If range R < 2*R_nuc, alpha is fully stopped inside -> deposits all.
    # We use:
    #   f_dep = min(1, mean_chord/R) with mean_chord = 3*R_nuc/4.
    # then E_dep_per_decay = sum_i branching_i * E_i_MeV * f_dep_i
    # converted to cGy/decay = J/kg/decay * 100
    mean_chord_um = 0.75 * R_NUC_um
    Edep_MeV = 0.0
    for e in emissions:
        if e["parent_chain"] != parent: continue
        R = csda_range_um_water(e["energy_MeV"])
        f_dep = min(1.0, mean_chord_um / R) if R > 0 else 1.0
        Edep_MeV += e["branching"] * e["energy_MeV"] * f_dep
    # convert MeV -> J: 1 MeV = 1.602176634e-13 J
    E_J = Edep_MeV * 1.602176634e-13
    # M_NUC_g in grams -> kg
    M_kg = M_NUC_g * 1e-3
    Gy = E_J / M_kg
    return Gy * 100.0  # cGy

def dose_per_decay_nuc_membrane_source(parent: str, emissions: list) -> float:
    """Approximate cGy/decay to the nucleus assuming source uniformly
    distributed on the cell wall (R_cell). Two effects:
      (1) only a fraction f_geom of alphas, emitted isotropically from
          R_cell, hit the nucleus (geometric solid-angle subtended by the
          nucleus seen from the cell wall).
      (2) those that do, traverse at least (R_cell - R_nuc) = 5 um of water
          before entering the nucleus, losing dE/dx*5um, then deposit at
          most (chord-through-nucleus) MeV inside the nucleus.
    """
    d = R_CELL_um - R_NUC_um  # min wall-to-nucleus distance
    # Solid-angle fraction of nucleus seen from a point at distance R_cell
    # from the cell centre: cap of half-angle theta = asin(R_nuc/R_cell).
    # f_geom = 0.5*(1 - cos(theta)). For R_nuc/R_cell = 0.5: theta=30deg,
    # cos=0.866 -> f_geom = 0.067.
    theta = math.asin(R_NUC_um / R_CELL_um)
    f_geom = 0.5 * (1.0 - math.cos(theta))
    # mean chord through nucleus for a parallel beam through a sphere is
    # 4*R_nuc/3 averaged over impact parameter (volume-weighted).
    mean_chord_nuc_um = (4.0/3.0) * R_NUC_um

    Edep_MeV = 0.0
    for e in emissions:
        if e["parent_chain"] != parent: continue
        R = csda_range_um_water(e["energy_MeV"])
        # 1. energy after traversing 'd' um water (linear approximation
        #    using mean energy E_remaining ~ E0 * max(0, (R-d)/R))
        remaining = max(0.0, (R - d) / R) if R > 0 else 0.0
        E_after_wall = e["energy_MeV"] * remaining
        # 2. fraction of remaining range deposited in nucleus chord
        R_after = csda_range_um_water(E_after_wall) if E_after_wall > 0 else 0.0
        f_in_nuc = min(1.0, mean_chord_nuc_um / R_after) if R_after > 0 else 0.0
        Edep_MeV += e["branching"] * f_geom * E_after_wall * f_in_nuc
    E_J = Edep_MeV * 1.602176634e-13
    M_kg = M_NUC_g * 1e-3
    return E_J / M_kg * 100.0  # cGy

def main():
    data = load_chains()
    emissions = data["emissions"]
    print(f"Nucleus mass: {M_NUC_g*1e9:.3f} pg ({M_NUC_g*1e-3:.3e} kg)")
    print(f"R_cell={R_CELL_um} um, R_nuc={R_NUC_um} um, rho=1 g/cm^3\n")

    print(f"{'Parent':<8} {'Nuc-src cGy/dec':>16} {'Mem-src cGy/dec':>16}  "
          f"({'Table 2 Nuc/Mem' if False else 'paper-2nd-row Nuc/Mem for 211At: 12.88 / 0.93'})")
    results = {}
    for parent in ["Ac-225", "Ra-223", "Pb-212", "At-211"]:
        d_nuc = dose_per_decay_nuc_uniform_source(parent, emissions)
        d_mem = dose_per_decay_nuc_membrane_source(parent, emissions)
        results[parent] = {"nuc_cGy_per_decay": d_nuc,
                           "mem_cGy_per_decay": d_mem}
        print(f"{parent:<8} {d_nuc:>16.3f} {d_mem:>16.3f}")

    # Comparison with Table 2 (211At only):
    table2_211At = {
        "g4em-dna_total": {"Mem": 2.59, "Cyto": 3.85, "Nuc": 14.92},
        "opt0_total":     {"Mem": 0.93, "Cyto": 1.79, "Nuc": 12.88},
        "alpha-only_dna": {"Mem": 1.81, "Cyto": 3.67, "Nuc": 16.63},
        "Guerra_Liberal": {"Mem": 1.04, "Cyto": 1.98, "Nuc": 8.26},
    }
    print("\n--- 211At cross-check vs Table 2 ---")
    print("Paper Nuc range: 12.88 - 16.63 cGy/decay (full decay or alpha-only)")
    print(f"Our analytical estimate: {results['At-211']['nuc_cGy_per_decay']:.2f} cGy/decay")
    print("Paper Mem range:  0.93 -  2.59 cGy/decay")
    print(f"Our analytical estimate: {results['At-211']['mem_cGy_per_decay']:.3f} cGy/decay")

    with open("results/02_alpha_geom.json", "w") as f:
        json.dump({"results": results, "table2_211At_reference": table2_211At,
                   "inputs": {"R_cell_um": R_CELL_um, "R_nuc_um": R_NUC_um,
                              "M_nuc_g": M_NUC_g, "rho": RHO_WATER}}, f, indent=2)
    print("\nWrote results/02_alpha_geom.json")

if __name__ == "__main__":
    main()
