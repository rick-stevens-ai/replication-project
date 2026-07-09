"""
Claims A4, A5, A6 — diffusion-coefficient arithmetic from the paper text.

A4: cube-root mass scaling for GFP-tagged NBS1 (137 kDa) and MDC1 (257 kDa)
    starting from D(GFP, 27 kDa) = 12 um^2/s.
    Paper Table 1: Dcalc(NBS1) = 7.0 um^2/s, Dcalc(MDC1) = 5.7 um^2/s.

A5: avg distance to centre of nucleus = 6.3 um; D(GFP) = 12 um^2/s ->
    "0.83 s for a GFP protein to travel 6.3 um" (paper text).

A6: same 6.3-um traversal time using Deff(NBS1)=0.25 and Deff(MDC1)=0.029:
    paper text says "~40 s" for NBS1 and "~340 s" for MDC1.

Method:
- Diffusion coefficient scaling under Stokes-Einstein / equal-density spherical
  proteins is D ∝ 1/R ∝ 1/M^(1/3) (volume ∝ mass; radius ∝ mass^1/3).
- "Time to travel distance L" by diffusion uses the mean-square-displacement
  relation. In 3D, <r^2> = 6 D t => t = L^2 / (6 D).
  The paper's quoted 0.83 s for L=6.3 um and D=12 um^2/s is consistent with
  that 3D form:  t = 6.3^2 / (6*12) = 39.69/72 = 0.5513 s -- NOT 0.83 s.
  Trying 2D (<r^2> = 4 D t):  t = 39.69/48 = 0.827 s  -> matches 0.83 s.
  So the paper uses the 2D (radial / cylindrical) form, which is natural for a
  cylindrically-shaped nucleus and matches their Sprague reaction-diffusion
  model.  We adopt t = L^2 / (4 D) for the reproduction.
"""
import json
import os

# Pure-GFP reference
D_GFP = 12.0    # um^2/s
M_GFP = 27.0    # kDa

# Target proteins (GFP-tagged)
M_NBS1 = 137.0  # kDa  (NBS1-GFP-GFP)
M_MDC1 = 257.0  # kDa  (MDC1-GFP)

PAPER_DCALC = {"NBS1": 7.0, "MDC1": 5.7}
PAPER_DEFF  = {"NBS1": 0.25, "MDC1": 0.029, "GFP": 12.0}

# A4: Stokes-Einstein cube-root scaling
def dcalc(m_target, m_ref=M_GFP, d_ref=D_GFP):
    return d_ref * (m_ref / m_target) ** (1.0 / 3.0)

d_nbs1_calc = dcalc(M_NBS1)
d_mdc1_calc = dcalc(M_MDC1)

print("=== A4: Dcalc from cube-root mass scaling ===")
print(f"  GFP:  D={D_GFP:.3f} um^2/s, M={M_GFP} kDa  (reference)")
for name, m, paper in [("NBS1", M_NBS1, PAPER_DCALC["NBS1"]),
                       ("MDC1", M_MDC1, PAPER_DCALC["MDC1"])]:
    d = dcalc(m)
    rel = (d - paper) / paper
    print(f"  {name}: M={m} kDa -> Dcalc={d:.3f} um^2/s  "
          f"(paper {paper:.3f})  rel err {rel:+.2%}")

# A5/A6: 2D diffusive traversal time for L = 6.3 um, t = L^2 / (4 D)
L = 6.3  # um, mean distance to nucleus center
def t2d(D, L=L):
    return L * L / (4.0 * D)

t_gfp_calc  = t2d(D_GFP)
t_nbs1_calc = t2d(PAPER_DEFF["NBS1"])
t_mdc1_calc = t2d(PAPER_DEFF["MDC1"])

paper_times = {"GFP": 0.83, "NBS1": 40.0, "MDC1": 340.0}

print("\n=== A5/A6: 2D traversal time for L=6.3 um, t = L^2/(4D) ===")
for name, D, paper in [("GFP",  D_GFP, paper_times["GFP"]),
                       ("NBS1", PAPER_DEFF["NBS1"], paper_times["NBS1"]),
                       ("MDC1", PAPER_DEFF["MDC1"], paper_times["MDC1"])]:
    t = t2d(D)
    rel = (t - paper) / paper
    print(f"  {name}: D={D:>7.3f} um^2/s -> t={t:>7.3f} s  "
          f"(paper {paper:>5.2f} s)  rel err {rel:+.2%}")

# Verdicts
def verdict(rel, tol=0.05):
    return "REPRODUCED" if abs(rel) < tol else (
        "ACCEPTABLE" if abs(rel) < 0.15 else "MISMATCH")

results = {
    "claim_A4_dcalc": {
        "GFP_reference":   {"M_kDa": M_GFP, "D_um2_s": D_GFP},
        "NBS1_computed":   d_nbs1_calc, "NBS1_paper": PAPER_DCALC["NBS1"],
        "NBS1_rel_err":    (d_nbs1_calc - PAPER_DCALC["NBS1"]) / PAPER_DCALC["NBS1"],
        "MDC1_computed":   d_mdc1_calc, "MDC1_paper": PAPER_DCALC["MDC1"],
        "MDC1_rel_err":    (d_mdc1_calc - PAPER_DCALC["MDC1"]) / PAPER_DCALC["MDC1"],
        "verdict_NBS1":    verdict((d_nbs1_calc - PAPER_DCALC["NBS1"]) / PAPER_DCALC["NBS1"]),
        "verdict_MDC1":    verdict((d_mdc1_calc - PAPER_DCALC["MDC1"]) / PAPER_DCALC["MDC1"]),
    },
    "claim_A5_GFP_traversal": {
        "L_um": L, "D_um2_s": D_GFP, "t_computed_s": t_gfp_calc,
        "t_paper_s": paper_times["GFP"],
        "rel_err": (t_gfp_calc - paper_times["GFP"]) / paper_times["GFP"],
        "geometry_assumed": "2D radial (cylindrical nucleus): t = L^2 / (4 D)",
        "verdict": verdict((t_gfp_calc - paper_times["GFP"]) / paper_times["GFP"]),
    },
    "claim_A6_NBS1_MDC1_traversal": {
        "L_um": L,
        "NBS1": {
            "D_um2_s": PAPER_DEFF["NBS1"],
            "t_computed_s": t_nbs1_calc,
            "t_paper_s": paper_times["NBS1"],
            "rel_err": (t_nbs1_calc - paper_times["NBS1"]) / paper_times["NBS1"],
            "verdict": verdict((t_nbs1_calc - paper_times["NBS1"]) / paper_times["NBS1"]),
        },
        "MDC1": {
            "D_um2_s": PAPER_DEFF["MDC1"],
            "t_computed_s": t_mdc1_calc,
            "t_paper_s": paper_times["MDC1"],
            "rel_err": (t_mdc1_calc - paper_times["MDC1"]) / paper_times["MDC1"],
            "verdict": verdict((t_mdc1_calc - paper_times["MDC1"]) / paper_times["MDC1"]),
        },
    },
}
out_path = os.path.join(os.path.dirname(__file__), "..", "results", "c4_diffusion.json")
out_path = os.path.normpath(out_path)
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved -> {out_path}")
