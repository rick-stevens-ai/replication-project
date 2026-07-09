"""Extend the analytical S-value cross-check to ALL 4 radionuclides and
ALL 4 source compartments (Mem / Cyto / NucWall / Nuc) — covers the
core quantitative scaffold of Jolly & Fielding 2025 Figs 1-3 and
Table 2.

This is a closed-form CSDA + geometric solid-angle model. It is NOT
TOPAS-nBio. Goal: reproduce the *trend ordering* (Mem << Cyto < NucWall
< Nuc, Ac/Ra > Pb/At for total dose) and bracket Table 2 211At values
within model tolerance.

Outputs:
  results/04_table2_full.json
  results/04_table2_full.txt
"""
from __future__ import annotations
import json, math, os

R_CELL = 10.0   # um
R_NUC = 5.0     # um
RHO = 1.0       # g/cm^3
M_NUC_g = (4.0/3.0) * math.pi * (R_NUC * 1e-4)**3 * RHO
M_NUC_kg = M_NUC_g * 1e-3

MEV_TO_J = 1.602176634e-13

def csda_range_um(E_MeV: float) -> float:
    """Alpha CSDA range in liquid water, um. R ~= 1.24 E^1.78 (~3% over 4-10 MeV)."""
    if E_MeV <= 0: return 0.0
    return 1.24 * (E_MeV ** 1.78)

def load_chains():
    p = os.path.join(os.path.dirname(__file__), "..", "results", "01_decay_chains.json")
    return json.load(open(p))

# ----- Geometry helpers -----
def f_geom_point_to_sphere(r_src: float) -> float:
    """Solid-angle fraction of nucleus seen from a point at distance r_src
    from cell centre (r_src >= R_nuc means source is outside nucleus)."""
    if r_src <= R_NUC:
        return 1.0  # we're inside the nucleus; handle separately
    theta = math.asin(R_NUC / r_src)
    return 0.5 * (1.0 - math.cos(theta))

def mean_chord_through_nucleus_um() -> float:
    """Mean chord through a sphere for a uniform parallel beam, weighted by
    impact-parameter area: 4R/3."""
    return (4.0/3.0) * R_NUC

def mean_chord_inside_sphere_um(R: float) -> float:
    """Mean distance from a uniformly-distributed isotropic-direction
    starting point inside a sphere of radius R to the surface: 3R/4."""
    return 0.75 * R

# ----- Dose calculators per source compartment -----
def dose_from_external_uniform_shell(parent: str, emissions: list, r_src: float) -> float:
    """Source on a thin shell at radius r_src (outside nucleus), uniform
    on the shell, isotropic emission."""
    f_geom = f_geom_point_to_sphere(r_src)
    d_to_nuc = r_src - R_NUC  # straight-line wall-to-nucleus
    mean_chord_nuc = mean_chord_through_nucleus_um()
    Edep_MeV = 0.0
    for e in emissions:
        if e["parent_chain"] != parent: continue
        R = csda_range_um(e["energy_MeV"])
        if R <= d_to_nuc:
            continue
        # remaining energy fraction after traversing d_to_nuc (linear approx)
        remaining = (R - d_to_nuc) / R
        E_after = e["energy_MeV"] * remaining
        R_after = csda_range_um(E_after)
        f_in_nuc = min(1.0, mean_chord_nuc / R_after) if R_after > 0 else 0.0
        Edep_MeV += e["branching"] * f_geom * E_after * f_in_nuc
    return Edep_MeV * MEV_TO_J / M_NUC_kg * 100.0   # cGy

def dose_from_uniform_cytoplasm(parent: str, emissions: list) -> float:
    """Source uniformly distributed in cytoplasm (between R_nuc and R_cell).
    Average over radial shells weighted by shell volume."""
    Nshells = 50
    rs = []
    vols = []
    for i in range(Nshells):
        r1 = R_NUC + (R_CELL - R_NUC) * i / Nshells
        r2 = R_NUC + (R_CELL - R_NUC) * (i+1) / Nshells
        r_mid = 0.5 * (r1 + r2)
        v_shell = (4.0/3.0)*math.pi*(r2**3 - r1**3)
        rs.append(r_mid)
        vols.append(v_shell)
    total = sum(vols)
    dose = 0.0
    for r, v in zip(rs, vols):
        dose += (v/total) * dose_from_external_uniform_shell(parent, emissions, r)
    return dose

def dose_from_uniform_nucleus(parent: str, emissions: list) -> float:
    """Source uniformly distributed in nucleus volume, isotropic."""
    mean_chord = mean_chord_inside_sphere_um(R_NUC)
    Edep_MeV = 0.0
    for e in emissions:
        if e["parent_chain"] != parent: continue
        R = csda_range_um(e["energy_MeV"])
        f_dep = min(1.0, mean_chord / R) if R > 0 else 1.0
        Edep_MeV += e["branching"] * e["energy_MeV"] * f_dep
    return Edep_MeV * MEV_TO_J / M_NUC_kg * 100.0

# ----- Hits/decay calculator (Figs 1d, 2d, 3d) -----
def hits_per_decay(parent: str, emissions: list, compartment: str) -> float:
    """Mean alpha-particle hits to the nucleus surface per parent decay.

    For sources outside nucleus: f_hit = solid angle fraction averaged
    over source distribution (and assumes alpha range >> distance, which
    is true for >5 MeV alphas through <10 um water for these geometries).

    For sources inside nucleus: every emitted alpha crosses the surface
    (they all eventually exit if range > mean_chord). So hits = total
    alphas/decay.
    """
    alphas = [e for e in emissions if e["parent_chain"] == parent]
    if compartment == "Nuc":
        # all alphas exit if range > mean chord
        return sum(e["branching"] for e in alphas
                   if csda_range_um(e["energy_MeV"]) >= mean_chord_inside_sphere_um(R_NUC))
    elif compartment == "NucWall":
        # half emitted inward (hit), half outward
        return sum(0.5 * e["branching"] for e in alphas)
    elif compartment == "Cyto":
        # average solid-angle fraction over cytoplasm volume
        Nshells = 50
        f_geom_avg = 0.0
        vsum = 0.0
        for i in range(Nshells):
            r1 = R_NUC + (R_CELL - R_NUC) * i / Nshells
            r2 = R_NUC + (R_CELL - R_NUC) * (i+1) / Nshells
            r_mid = 0.5 * (r1 + r2)
            v = (4.0/3.0)*math.pi*(r2**3 - r1**3)
            f_geom_avg += v * f_geom_point_to_sphere(r_mid)
            vsum += v
        f_geom_avg /= vsum
        return f_geom_avg * sum(e["branching"] for e in alphas
                                if csda_range_um(e["energy_MeV"]) >= (R_NUC))  # alpha must reach nucleus
    elif compartment == "Mem":
        f_geom = f_geom_point_to_sphere(R_CELL)
        return f_geom * sum(e["branching"] for e in alphas
                            if csda_range_um(e["energy_MeV"]) >= (R_CELL - R_NUC))
    else:
        raise ValueError(compartment)

def main():
    data = load_chains()
    emissions = data["emissions"]

    parents = ["Ac-225", "Ra-223", "Pb-212", "At-211"]
    compartments = ["Mem", "Cyto", "NucWall", "Nuc"]

    # Table 2 reference (Jolly & Fielding 2025, Table 2; 211At only)
    table2_211At = {
        # all are cGy/decay total dose to nucleus
        "g4em-dna_total":     {"Mem": 2.59, "Cyto": 3.85,  "Nuc": 14.92},
        "g4em-std-opt0_total":{"Mem": 0.93, "Cyto": 1.79,  "Nuc": 12.88},
        "alpha-only_dna":     {"Mem": 1.81, "Cyto": 3.67,  "Nuc": 16.63},
        "Guerra_Liberal_2021":{"Mem": 1.04, "Cyto": 1.98,  "Nuc": 8.26},
    }

    out = {"compartments": compartments,
           "dose_cGy_per_decay": {},
           "hits_per_decay_alpha": {},
           "table2_211At_reference": table2_211At}

    for parent in parents:
        out["dose_cGy_per_decay"][parent] = {}
        out["hits_per_decay_alpha"][parent] = {}
        for c in compartments:
            if c == "Mem":
                d = dose_from_external_uniform_shell(parent, emissions, R_CELL)
            elif c == "Cyto":
                d = dose_from_uniform_cytoplasm(parent, emissions)
            elif c == "NucWall":
                d = dose_from_external_uniform_shell(parent, emissions, R_NUC + 0.05)
            elif c == "Nuc":
                d = dose_from_uniform_nucleus(parent, emissions)
            out["dose_cGy_per_decay"][parent][c] = d
            out["hits_per_decay_alpha"][parent][c] = hits_per_decay(parent, emissions, c)

    # Pretty print
    lines = []
    lines.append("=== Analytical S-value (cGy/decay, alpha-only model) ===")
    lines.append(f"{'Isotope':<8} {'Mem':>10} {'Cyto':>10} {'NucWall':>10} {'Nuc':>10}")
    for parent in parents:
        row = [f"{out['dose_cGy_per_decay'][parent][c]:>10.3f}" for c in compartments]
        lines.append(f"{parent:<8} " + " ".join(row))

    lines.append("")
    lines.append("=== Alpha hits to nucleus surface per parent decay ===")
    lines.append(f"{'Isotope':<8} {'Mem':>10} {'Cyto':>10} {'NucWall':>10} {'Nuc':>10}")
    for parent in parents:
        row = [f"{out['hits_per_decay_alpha'][parent][c]:>10.3f}" for c in compartments]
        lines.append(f"{parent:<8} " + " ".join(row))

    lines.append("")
    lines.append("=== Cross-check: 211At vs Table 2 ===")
    lines.append(f"   Our Mem={out['dose_cGy_per_decay']['At-211']['Mem']:.3f},   "
                 f"Cyto={out['dose_cGy_per_decay']['At-211']['Cyto']:.3f},   "
                 f"Nuc={out['dose_cGy_per_decay']['At-211']['Nuc']:.3f}")
    lines.append(f"   Paper Mem range 0.93-2.59;  Cyto 1.79-3.85;  Nuc 12.88-16.63")
    lines.append(f"   Guerra-Liberal:  Mem={table2_211At['Guerra_Liberal_2021']['Mem']}, "
                 f"Cyto={table2_211At['Guerra_Liberal_2021']['Cyto']}, "
                 f"Nuc={table2_211At['Guerra_Liberal_2021']['Nuc']}")

    lines.append("")
    lines.append("=== Trend checks (qualitative claims from paper) ===")
    # Claim: dose(Mem) << dose(Cyto) < dose(NucWall) < dose(Nuc) for each isotope
    trend_ok = {}
    for parent in parents:
        d = out["dose_cGy_per_decay"][parent]
        ok = d["Mem"] < d["Cyto"] < d["NucWall"] < d["Nuc"]
        trend_ok[parent] = ok
        lines.append(f"   {parent}: Mem<Cyto<NucWall<Nuc -> {ok}  "
                     f"({d['Mem']:.2f} < {d['Cyto']:.2f} < {d['NucWall']:.2f} < {d['Nuc']:.2f})")
    # Claim: For Nuc compartment, Ac-225 and Ra-223 deliver more dose than Pb-212 and At-211 (more alphas/decay)
    nuc = {p: out["dose_cGy_per_decay"][p]["Nuc"] for p in parents}
    ordering_ok = min(nuc["Ac-225"], nuc["Ra-223"]) > max(nuc["Pb-212"], nuc["At-211"])
    lines.append(f"   Nuc-comp ordering: min(Ac,Ra)>max(Pb,At) -> {ordering_ok}  "
                 f"(Ac={nuc['Ac-225']:.1f}, Ra={nuc['Ra-223']:.1f}, "
                 f"Pb={nuc['Pb-212']:.1f}, At={nuc['At-211']:.1f})")
    out["trend_checks"] = {"compartment_ordering_per_isotope": trend_ok,
                            "nuc_dose_Ac_Ra_above_Pb_At": ordering_ok}

    txt = "\n".join(lines)
    print(txt)
    with open("results/04_table2_full.json", "w") as f:
        json.dump(out, f, indent=2)
    with open("results/04_table2_full.txt", "w") as f:
        f.write(txt + "\n")
    print("\nWrote results/04_table2_full.{json,txt}")

if __name__ == "__main__":
    main()
