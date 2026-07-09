#!/usr/bin/env python3
"""
s100-042 lightweight reproduction.

Paper: Mokari et al., Phys Med Biol 2018, doi:10.1088/1361-6560/aad7ee
"A Simulation Approach for Determining the Spectrum of DNA Damage Induced by Protons"

The full Monte Carlo (Geant4-DNA v10.3, B-DNA 216 bp segments in 100-nm water sphere,
Essb=17.5 eV, P_OH=0.13, chemistry up to 1 ns, isotropic proton point source 0.5–20 MeV)
cannot be run here. This script performs four audits/spot-checks that do NOT need MC:

(1) Table 2 normalization audit: per-row NB + SSB + SSB+ + 2SSB + DSB + DSB+ + DSB++ ≈ 100%,
    and SSBc = SSB+ + 2SSB, DSBc = DSB+ + DSB++.
(2) Table 3 internal arithmetic: SSBall + 2*DSBall counts as defined; per the paper's worked
    example at 100–150 eV interval ("1.39 SSBall per event" and "0.16 DSBall per event").
(3) Table 5 yield-from-distribution recomputation: Y = Σ n(E,y) P(E,y) / y.
    Reproduce paper's columns 4–5 using their Table 4 P(E,y) values.
(4) Table 5 (Gy·cell)^-1 ↔ (Gy·Gbp)^-1 unit conversion using 22 chr × 245 Mbp = 5.39 Gbp/cell.

(5) Damage-classification clustering: reimplement the Nikjoo et al [2] / Figure 2 algorithm
    on synthetic single-strand-break lists and verify each class (SSB, SSB+, 2SSB, DSB,
    DSB+, DSB++) is registered per the paper's 10-bp-window rule.
"""
from __future__ import annotations
import json, math
from dataclasses import dataclass

# ---------- (1) Table 2 normalization audit ----------
TABLE2 = [
    # (E_MeV, LET, NB, SSB, SSBplus, twoSSB, DSB, DSBplus, DSBplusplus, SSBc, DSBc, YSSB, YDSB)
    (0.5, 39.7, 26.59, 29.26, 4.06, 17.42, 10.27, 7.70, 4.68, 42.33, 54.63, 39.05, 7.80),
    (1.0, 24.2, 37.92, 31.16, 3.52, 13.75,  7.59, 4.90, 1.18, 35.66, 44.45, 50.92, 7.77),
    (2.0, 13.9, 50.44, 30.34, 2.59,  9.93,  4.67, 1.76, 0.28, 29.19, 30.42, 62.74, 6.36),
    (10., 3.4,  63.29, 27.35, 1.57,  5.19,  2.10, 0.47, 0.03, 19.81, 19.40, 73.45, 4.30),
    (20., 1.9,  67.92, 25.27, 1.10,  3.95,  1.50, 0.25, 0.01, 16.67, 14.65, 75.15, 3.50),
]

def audit_table2():
    print("="*72)
    print("(1) TABLE 2 NORMALIZATION AUDIT")
    print("="*72)
    print(f"{'E_MeV':>6} {'sum%':>7} {'SSBc_calc':>10} {'SSBc_pap':>9} {'DSBc_calc':>10} {'DSBc_pap':>9}")
    ok = True
    for r in TABLE2:
        E, LET, NB, SSB, SSBp, SSB2, DSB, DSBp, DSBpp, SSBc, DSBc, YSSB, YDSB = r
        s = NB + SSB + SSBp + SSB2 + DSB + DSBp + DSBpp
        SSBc_calc = SSBp + SSB2
        DSBc_calc = DSBp + DSBpp
        flag = "✓" if abs(s-100.0) < 0.5 and abs(SSBc_calc-SSBc) < 0.05 and abs(DSBc_calc-DSBc) < 0.05 else "✗"
        print(f"{E:>6} {s:>7.2f} {SSBc_calc:>10.2f} {SSBc:>9.2f} {DSBc_calc:>10.2f} {DSBc:>9.2f}  {flag}")
        if flag == "✗": ok = False
    print(f"  -> Table 2 normalization & definitions: {'PASS' if ok else 'FAIL'}")
    return ok

# ---------- (2) Table 3 internal arithmetic, 100–150 eV row ----------
TABLE3 = {
    # bin (eV) -> dict
    (0,20):     dict(total=9933, NB=8649, SSB=1211, SSBp=9,   SSB2=56,  DSB=8,   DSBp=0,  DSBpp=0),
    (20,40):    dict(total=4627, NB=2867, SSB=1569, SSBp=26,  SSB2=144, DSB=21,  DSBp=0,  DSBpp=0),
    (40,60):    dict(total=2744, NB=979,  SSB=1471, SSBp=37,  SSB2=203, DSB=53,  DSBp=1,  DSBpp=0),
    (60,80):    dict(total=1911, NB=430,  SSB=1075, SSBp=64,  SSB2=275, DSB=61,  DSBp=6,  DSBpp=0),
    (80,100):   dict(total=1351, NB=173,  SSB=725,  SSBp=72,  SSB2=291, DSB=84,  DSBp=6,  DSBpp=0),
    (100,150):  dict(total=1913, NB=128,  SSB=739,  SSBp=168, SSB2=563, DSB=261, DSBp=52, DSBpp=2),
    (150,200):  dict(total=1076, NB=19,   SSB=266,  SSBp=105, SSB2=383, DSB=215, DSBp=81, DSBpp=7),
    (200,250):  dict(total=636,  NB=2,    SSB=78,   SSBp=77,  SSB2=225, DSB=172, DSBp=76, DSBpp=6),
    (250,300):  dict(total=369,  NB=0,    SSB=21,   SSBp=28,  SSB2=124, DSB=111, DSBp=70, DSBpp=15),
    (300,350):  dict(total=198,  NB=0,    SSB=4,    SSBp=14,  SSB2=43,  DSB=68,  DSBp=60, DSBpp=9),
    (350,400):  dict(total=80,   NB=0,    SSB=0,    SSBp=4,   SSB2=12,  DSB=23,  DSBp=29, DSBpp=12),
    (400,450):  dict(total=35,   NB=0,    SSB=0,    SSBp=1,   SSB2=5,   DSB=8,   DSBp=15, DSBpp=6),
    # >450 omitted from per-event check (open bin, no mid for yield calc anyway)
}

def audit_table3_worked_example():
    print("="*72)
    print("(2) TABLE 3 WORKED-EXAMPLE AUDIT (paper p. 7)")
    print("="*72)
    r = TABLE3[(100,150)]
    # Paper definitions: SSBall = SSB + SSB+ + 2*(2SSB + DSB + DSB+ + DSB++)
    SSBall = r["SSB"] + r["SSBp"] + 2*(r["SSB2"] + r["DSB"] + r["DSBp"] + r["DSBpp"])
    DSBall = r["DSB"] + r["DSBp"] + r["DSBpp"]
    per_event_SSB = SSBall / r["total"]
    per_event_DSB = DSBall / r["total"]
    print(f"  100-150 eV bin: total hits = {r['total']}")
    print(f"  SSBall = SSB + SSB+ + 2*(2SSB + DSB + DSB+ + DSB++) = {SSBall}")
    print(f"  DSBall = DSB + DSB+ + DSB++ = {DSBall}")
    print(f"  per-event SSBall = {per_event_SSB:.3f}   (paper says 1.39)")
    print(f"  per-event DSBall = {per_event_DSB:.3f}   (paper says 0.16)")
    ok = (abs(SSBall - 2663) == 0 and DSBall == 315
          and abs(per_event_SSB - 1.39) < 0.01
          and abs(per_event_DSB - 0.16) < 0.005)
    print(f"  -> Worked-example arithmetic: {'PASS' if ok else 'FAIL'}")
    return ok

# ---------- (3) Table 4 P(E,y) and Table 5 yield-from-distribution reproduction ----------
# Table 4 values (×1e-5). Bins same as Table 3. Open bin >450 carried with mid=475 only when present.
# Empty cells in paper (10/20 MeV at high E) treated as 0.
TABLE4 = {
    #   (lo,hi):  [ 0.5,   1,     2,     10,    20  ]   ×1e-5
    (0,20):     [0.105, 0.314, 0.857, 2.399, 3.543],
    (20,40):    [0.092, 0.209, 0.399, 0.718, 0.841],
    (40,60):    [0.074, 0.138, 0.237, 0.368, 0.406],
    (60,80):    [0.065, 0.106, 0.165, 0.233, 0.231],
    (80,100):   [0.051, 0.078, 0.117, 0.138, 0.132],
    (100,150):  [0.093, 0.133, 0.165, 0.177, 0.154],
    (150,200):  [0.060, 0.081, 0.093, 0.058, 0.032],
    (200,250):  [0.041, 0.053, 0.055, 0.019, 0.002],
    (250,300):  [0.031, 0.038, 0.032, 0.004, 0.0  ],
    (300,350):  [0.024, 0.030, 0.017, 0.002, 0.0  ],
    (350,400):  [0.021, 0.020, 0.007, 0.0,   0.0  ],
    (400,450):  [0.016, 0.016, 0.003, 0.0,   0.0  ],
    (450,500):  [0.074, 0.030, 0.010, 0.0,   0.0  ],  # ">450" — use mid 475 per paper convention
}
ENERGIES = [0.5, 1.0, 2.0, 10.0, 20.0]
Y_BP = 216  # segment length in bp

# Table 3 is given only for 2 MeV. We can reproduce the 2-MeV column of Table 5 from Charlton et al
# formula: Y = sum over E_bin midpoints of n(E,y) * P(E,y) / y
# where n(E,y) per bin = (SSBall_bin / total_hits_bin) for SSB, (DSBall_bin / total_hits_bin) for DSB.

def n_per_hit_for_2MeV():
    """Return {(lo,hi): (n_SSB, n_DSB)} per-hit using Table 3 (which is 2-MeV data)."""
    out = {}
    for bin_, r in TABLE3.items():
        SSBall = r["SSB"] + r["SSBp"] + 2*(r["SSB2"] + r["DSB"] + r["DSBp"] + r["DSBpp"])
        DSBall = r["DSB"] + r["DSBp"] + r["DSBpp"]
        out[bin_] = (SSBall / r["total"], DSBall / r["total"])
    return out

def audit_yield_recompute_2MeV():
    print("="*72)
    print("(3) TABLE 5 YIELD-FROM-DISTRIBUTION RECOMPUTATION (2 MeV)")
    print("="*72)
    print("    Y = Σ_E n(E,y) * P(E,y) / y    [Charlton et al 1989]")
    print("    y = 216 bp;  P from Table 4 (×1e-5);  n from Table 3 per-hit.")
    n_per_hit = n_per_hit_for_2MeV()
    Y_SSB = 0.0
    Y_DSB = 0.0
    for bin_, (n_ssb, n_dsb) in n_per_hit.items():
        # match this bin to Table 4 (Table 3 has no >450 explicit; Table 4 has it as (450,500))
        if bin_ not in TABLE4: continue
        P = TABLE4[bin_][2] * 1e-5  # 2-MeV column
        Y_SSB += n_ssb * P / Y_BP
        Y_DSB += n_dsb * P / Y_BP
    # Convert from "breaks per bp per Gy" to "breaks per Gbp per Gy"
    Y_SSB_Gbp = Y_SSB * 1e9
    Y_DSB_Gbp = Y_DSB * 1e9
    print(f"  Recomputed Y_SSB(2 MeV) = {Y_SSB_Gbp:.2f}  (Gy·Gbp)^-1   [paper Table 5 col 4: 62.72]")
    print(f"  Recomputed Y_DSB(2 MeV) = {Y_DSB_Gbp:.2f}  (Gy·Gbp)^-1   [paper Table 5 col 5: 6.38]")
    ok_ssb = abs(Y_SSB_Gbp - 62.72) / 62.72 < 0.10
    ok_dsb = abs(Y_DSB_Gbp - 6.38)  / 6.38  < 0.20  # DSB more sensitive to bin midpoint
    print(f"  -> Yield-formula self-consistency: SSB {'PASS' if ok_ssb else 'FAIL'}, "
          f"DSB {'PASS' if ok_dsb else 'FAIL'}")
    return ok_ssb and ok_dsb

# ---------- (4) (Gy·cell)^-1 unit conversion ----------
def audit_unit_conversion():
    print("="*72)
    print("(4) UNIT CONVERSION (Gy·Gbp)^-1 ↔ (Gy·cell)^-1")
    print("="*72)
    N_CHR = 22
    MBP_PER_CHR = 245
    Gbp_per_cell = N_CHR * MBP_PER_CHR / 1000.0  # = 5.390
    print(f"  Cell content: {N_CHR} chr × {MBP_PER_CHR} Mbp = {Gbp_per_cell} Gbp/cell")
    print(f"{'E_MeV':>6} {'Y_SSB_Gbp':>10} {'YSSB_cell_calc':>15} {'YSSB_cell_paper':>16} "
          f"{'Y_DSB_Gbp':>10} {'YDSB_cell_calc':>15} {'YDSB_cell_paper':>16}")
    # Paper Table 5 (cols 4,5,6,7): Y_SSB_Gbp Y_DSB_Gbp -> Y_SSB_cell Y_DSB_cell
    table5_check = [
        (0.5,  38.97, 7.76, 210.05, 41.83),
        (1.0,  50.66, 7.68, 273.06, 41.39),
        (2.0,  62.72, 6.38, 338.06, 34.39),
        (10.,  73.46, 4.27, 395.95, 23.01),
        (20.,  75.02, 3.58, 404.36, 19.30),
    ]
    ok = True
    for E, YSGbp, YDGbp, YSCell, YDCell in table5_check:
        Y_S = YSGbp * Gbp_per_cell
        Y_D = YDGbp * Gbp_per_cell
        flag_s = abs(Y_S - YSCell) / YSCell < 0.01
        flag_d = abs(Y_D - YDCell) / YDCell < 0.01
        print(f"{E:>6} {YSGbp:>10.2f} {Y_S:>15.2f} {YSCell:>16.2f}     "
              f"{YDGbp:>10.2f} {Y_D:>15.2f} {YDCell:>16.2f}   "
              f"{'✓' if flag_s and flag_d else '✗'}")
        if not (flag_s and flag_d): ok = False
    print(f"  -> Unit conversion (×{Gbp_per_cell} Gbp/cell): {'PASS' if ok else 'FAIL'}")
    return ok

# ---------- (5) Damage-classification clustering algorithm ----------
@dataclass(frozen=True)
class SB:
    """A single strand-break event."""
    bp_pos: int        # 1..216 (bp position on segment)
    strand: int        # 0 or 1 (the two complementary strands)
    origin: str        # "direct" | "indirect"

def classify_segment(sbs: list[SB], window_bp: int = 10) -> str:
    """
    Classify the damage status of one 216-bp DNA segment per Mokari Fig. 2:
      NB:     no SB anywhere on the segment
      SSB:    exactly one SB
      SSB+:   two or more SBs all on the SAME strand AND within window_bp of each other
      2SSB:   two or more SBs all on the SAME strand BUT spaced > window_bp apart
              (or SBs on different strands but spaced > window_bp apart) — both lonely SSBs
      DSB:    exactly two SBs, on opposite strands, within window_bp
      DSB+:   a DSB plus additional SB(s) within window_bp of the DSB
      DSB++:  more than one DSB in the segment
    This is a faithful classifier of one segment after damage formation; the paper applies the
    same logic over the entire DNA database. We focus on per-segment classification because
    that's what Fig. 2 / Table 2 frequencies enumerate.
    """
    if not sbs:
        return "NB"

    # Identify DSB pair seeds: pairs of opposite-strand SBs within window
    sbs_sorted = sorted(sbs, key=lambda s: (s.bp_pos, s.strand))

    # Find all DSB anchor pairs (opposite-strand SBs within window_bp)
    dsb_pairs = []  # list of (i,j) into sbs_sorted that are paired
    used = set()
    for i, a in enumerate(sbs_sorted):
        if i in used: continue
        # find closest opposite-strand partner within window
        best = None
        for j, b in enumerate(sbs_sorted):
            if j == i or j in used: continue
            if b.strand == a.strand: continue
            if abs(b.bp_pos - a.bp_pos) <= window_bp:
                if best is None or abs(b.bp_pos - a.bp_pos) < abs(sbs_sorted[best].bp_pos - a.bp_pos):
                    best = j
        if best is not None:
            dsb_pairs.append((i, best))
            used.add(i); used.add(best)

    n_dsb = len(dsb_pairs)
    leftovers = [s for k, s in enumerate(sbs_sorted) if k not in used]

    if n_dsb >= 2:
        return "DSB++"
    if n_dsb == 1:
        # any leftover SB within window of either DSB partner → DSB+
        i, j = dsb_pairs[0]
        dsb_positions = [sbs_sorted[i].bp_pos, sbs_sorted[j].bp_pos]
        for s in leftovers:
            if any(abs(s.bp_pos - p) <= window_bp for p in dsb_positions):
                return "DSB+"
        return "DSB"

    # No DSB. Only SSBs left.
    if len(leftovers) == 1:
        return "SSB"

    # 2+ SSBs and no DSB pair possible (so all on same strand, or opposite-strand pairs > window apart).
    # SSB+ iff there exist two SBs on the same strand within window_bp.
    for s in range(2):
        same = sorted([x.bp_pos for x in leftovers if x.strand == s])
        for k in range(1, len(same)):
            if same[k] - same[k-1] <= window_bp:
                return "SSB+"
    return "2SSB"

def audit_classifier():
    print("="*72)
    print("(5) DAMAGE-CLASSIFICATION ALGORITHM (Mokari Fig. 2 / Nikjoo classes)")
    print("="*72)
    cases = [
        ("NB     ", [],                                                "NB"),
        ("SSB    ", [SB(50, 0, "direct")],                              "SSB"),
        ("SSB+   ", [SB(50, 0, "direct"), SB(53, 0, "indirect")],       "SSB+"),
        ("2SSB-s ", [SB(50, 0, "direct"), SB(80, 0, "indirect")],       "2SSB"),  # same strand, far apart
        ("2SSB-os", [SB(50, 0, "direct"), SB(80, 1, "indirect")],       "2SSB"),  # opp strand, far apart
        ("DSB    ", [SB(50, 0, "direct"), SB(54, 1, "indirect")],       "DSB"),
        ("DSB+   ", [SB(50, 0, "direct"), SB(54, 1, "indirect"),
                     SB(57, 0, "indirect")],                            "DSB+"),
        ("DSB++  ", [SB(50, 0, "direct"), SB(54, 1, "indirect"),
                     SB(120, 0, "direct"), SB(123, 1, "indirect")],     "DSB++"),
    ]
    ok = True
    for name, sbs, expected in cases:
        got = classify_segment(sbs)
        flag = "✓" if got == expected else "✗"
        print(f"  {name}  expected={expected:6s}  got={got:6s}  {flag}")
        if got != expected: ok = False
    print(f"  -> Classifier matches paper Figure 2 definitions: {'PASS' if ok else 'FAIL'}")
    return ok

def main():
    results = {}
    results["table2_normalization"] = audit_table2()
    results["table3_worked_example"] = audit_table3_worked_example()
    results["yield_recompute_2MeV"] = audit_yield_recompute_2MeV()
    results["unit_conversion"]      = audit_unit_conversion()
    results["classifier"]           = audit_classifier()
    print("="*72)
    print("SUMMARY")
    print("="*72)
    for k, v in results.items():
        print(f"  {k:30s} {'PASS' if v else 'FAIL'}")
    return results

if __name__ == "__main__":
    main()
