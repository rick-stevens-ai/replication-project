#!/usr/bin/env python3
"""
Lightweight reproduction / arithmetic audit of Mokari et al. 2018
"A Simulation Approach for Determining the Spectrum of DNA Damage Induced by Protons"
DOI 10.1088/1361-6560/aad7ee — LUCID rank 42

We cannot rerun Geant4-DNA in this subagent. Instead we audit the paper's
arithmetic / internal consistency for the published Tables 2, 3, 5 and the
two narrative arithmetic checks (mutual-exclusion overlap; Table 3 example
of SSBall/DSBall per event).

All checks pass if the printed numbers in the paper are internally consistent;
disagreements indicate transcription, rounding, or definitional inconsistencies.
"""

from __future__ import annotations
import math


# -----------------------------------------------------------------------------
# Table 2 — relative yield of strand-break categories vs proton energy
# columns: Energy(MeV), LET(keV/um), NB%, SSB%, SSB+%, 2SSB%, DSB%, DSB+%,
#          DSB++%, SSBc%, DSBc%, Y_SSB (Gy.Gbp)-1, Y_DSB (Gy.Gbp)-1
# -----------------------------------------------------------------------------
TABLE2 = [
    # E,    LET,  NB,    SSB,   SSB+, 2SSB,  DSB,   DSB+, DSB++, SSBc,  DSBc,  Yssb,  Ydsb
    (0.5,  39.7, 26.59, 29.26, 4.06, 17.42, 10.27, 7.70, 4.68, 42.33, 54.63, 39.05, 7.80),
    (1.0,  24.2, 37.92, 31.16, 3.52, 13.75,  7.59, 4.90, 1.18, 35.66, 44.45, 50.92, 7.77),
    (2.0,  13.9, 50.44, 30.34, 2.59,  9.93,  4.67, 1.76, 0.28, 29.19, 30.42, 62.74, 6.36),
    (10.0,  3.4, 63.29, 27.35, 1.57,  5.19,  2.10, 0.47, 0.03, 19.81, 19.40, 73.45, 4.30),
    (20.0,  1.9, 67.92, 25.27, 1.10,  3.95,  1.50, 0.25, 0.01, 16.67, 14.65, 75.15, 3.50),
]


def check_table2_definitions():
    print("=" * 80)
    print("CHECK 1: Table 2 internal consistency")
    print("  SSBc = SSB+ + 2SSB ;  DSBc = DSB+ + DSB++")
    print("  All categories should sum to 100 (NB + SSB + SSB+ + 2SSB + DSB + DSB+ + DSB++)")
    print("=" * 80)
    print(f"{'E(MeV)':>7} {'SSBc_calc':>10} {'SSBc_paper':>11} {'DSBc_calc':>10} {'DSBc_paper':>11} {'sum%':>7}")
    fails = 0
    for row in TABLE2:
        E, LET, NB, SSB, SSBp, SSB2, DSB, DSBp, DSBpp, SSBc_p, DSBc_p, _, _ = row
        SSBc_calc = SSBp + SSB2
        DSBc_calc = DSBp + DSBpp
        total = NB + SSB + SSBp + SSB2 + DSB + DSBp + DSBpp
        ok_s = math.isclose(SSBc_calc, SSBc_p, abs_tol=0.05)
        ok_d = math.isclose(DSBc_calc, DSBc_p, abs_tol=0.05)
        ok_t = math.isclose(total, 100.0, abs_tol=0.05)
        flag = "" if (ok_s and ok_d and ok_t) else "  *"
        if not (ok_s and ok_d and ok_t):
            fails += 1
        print(f"{E:>7} {SSBc_calc:>10.2f} {SSBc_p:>11.2f} {DSBc_calc:>10.2f} {DSBc_p:>11.2f} {total:>7.2f}{flag}")
    print(f"  -> {fails}/{len(TABLE2)} rows inconsistent")
    return fails


# -----------------------------------------------------------------------------
# Table 3 — frequency of hits / break types vs deposited energy
# (2 MeV protons, 216 bp DNA, total counts NOT per-event-normalized)
# columns: E_lo, E_hi, total_hits, NB, SSB, SSB+, 2SSB, DSB, DSB+, DSB++
# -----------------------------------------------------------------------------
TABLE3 = [
    (   0,   20, 9933, 8649, 1211,   9,  56,    8,   0,  0),
    (  20,   40, 4627, 2867, 1569,  26, 144,   21,   0,  0),
    (  40,   60, 2744,  979, 1471,  37, 203,   53,   1,  0),
    (  60,   80, 1911,  430, 1075,  64, 275,   61,   6,  0),
    (  80,  100, 1351,  173,  725,  72, 291,   84,   6,  0),
    ( 100,  150, 1913,  128,  739, 168, 563,  261,  52,  2),
    ( 150,  200, 1076,   19,  266, 105, 383,  215,  81,  7),
    ( 200,  250,  636,    2,   78,  77, 225,  172,  76,  6),
    ( 250,  300,  369,    0,   21,  28, 124,  111,  70, 15),
    ( 300,  350,  198,    0,    4,  14,  43,   68,  60,  9),
    ( 350,  400,   80,    0,    0,   4,  12,   23,  29, 12),
    ( 400,  450,   35,    0,    0,   1,   5,    8,  15,  6),
    ( 450,  999,  128,    0,   37,   8,  30,   22,  22,  9),
]


def check_table3_narrative():
    print()
    print("=" * 80)
    print("CHECK 2: Paper's worked example, 2 MeV, deposited E in [100,150] eV")
    print("  Paper claims: 1913 total hits, SSBall = 739+168+2*(563+261+52+2) = 2663,")
    print("                                       => 1.39 SSBall/event")
    print("                DSBall = 315             => 0.16 DSBall/event")
    print("=" * 80)
    row = next(r for r in TABLE3 if r[0] == 100)
    _, _, total_hits, NB, SSB, SSBp, SSB2, DSB, DSBp, DSBpp = row
    # Definition (from paper): each DSB contributes 2 SSBs; SSB+ contributes 1
    # 2SSB contributes 2; DSB+ contributes 2; DSB++ contributes 2 (per Charlton citation)
    SSBall = SSB + SSBp + 2 * (SSB2 + DSB + DSBp + DSBpp)
    DSBall = DSB + DSBp + DSBpp
    print(f"  total_hits      = {total_hits}")
    print(f"  SSBall computed = {SSBall}   (paper: 2663)")
    print(f"  SSBall/event    = {SSBall/total_hits:.3f}   (paper: 1.39)")
    print(f"  DSBall computed = {DSBall}   (paper: 315)")
    print(f"  DSBall/event    = {DSBall/total_hits:.3f}   (paper: 0.16)")
    ok = (SSBall == 2663) and (DSBall == 315)
    print(f"  -> internally consistent: {ok}")
    # Also verify the 50% statement: "for proton energies less than 2 MeV, more than
    # 50% of energy depositions within the DNA volume resulted in strand breaks"
    # i.e. break% = (100 - NB%)
    print()
    print("  Quick: %hits-causing-breaks (any) from Table 2 = 100 - NB%:")
    for r in TABLE2:
        E = r[0]; nb = r[2]
        print(f"    E={E:>4} MeV   breaks_per_hit = {100-nb:5.2f}%   (paper claim: >50% for E<2 MeV)")
    return ok


# -----------------------------------------------------------------------------
# Check 3 — narrative mutual-exclusion arithmetic for 0.5 MeV, single damage site
#   All=29.7%, Direct=31.2%, Indirect=32.4%, overlap=16.9% (per paper)
# -----------------------------------------------------------------------------
def check_overlap_arithmetic():
    print()
    print("=" * 80)
    print("CHECK 3: Inclusion-exclusion for single-site breaks (paper's worked example)")
    print("=" * 80)
    All, Direct, Indirect, overlap_paper = 29.7, 31.2, 32.4, 16.9
    # paper logic: All = Direct + Indirect - 2*overlap
    # => overlap = (Direct + Indirect - All) / 2
    overlap_calc = (Direct + Indirect - All) / 2.0
    print(f"  All={All}, Direct={Direct}, Indirect={Indirect}")
    print(f"  overlap (paper)     = {overlap_paper:.1f}%")
    print(f"  overlap (computed)  = {overlap_calc:.1f}%   (formula: (D+I-A)/2)")
    ok = math.isclose(overlap_calc, overlap_paper, abs_tol=0.1)
    print(f"  -> consistent: {ok}")
    # Then "only single direct" = 31.2 - 16.9 = 14.3, "only single indirect" = 32.4 - 16.9 = 15.5
    print(f"  only-direct  = {Direct-overlap_paper:.1f}% (paper: 14.3%)")
    print(f"  only-indirect= {Indirect-overlap_paper:.1f}% (paper: 15.5%)")
    return ok


# -----------------------------------------------------------------------------
# Check 4 — Y_cell vs Y_Gbp conversion (Table 5 right-hand columns)
#   Paper: 22 chromosomes/cell × 245 Mbp/chromosome = 5390 Mbp/cell = 5.39 Gbp/cell
#   => Y_cell  =  Y_Gbp  ×  5.39
# Table 5 reports:
#   E    Y_SSB_Gbp (col 4)  Y_DSB_Gbp (col 5)  Y_SSB_cell  Y_DSB_cell
#   0.5    38.97               7.76              210.05      41.83
#   1      50.66               7.68              273.06      41.39
#   2      62.72               6.38              338.06      34.39
#   10     73.46               4.27              395.95      23.01
#   20     75.02               3.58              404.36      19.30
# -----------------------------------------------------------------------------
TABLE5_CELL = [
    (0.5, 38.97, 7.76, 210.05, 41.83),
    (1.0, 50.66, 7.68, 273.06, 41.39),
    (2.0, 62.72, 6.38, 338.06, 34.39),
    (10.0, 73.46, 4.27, 395.95, 23.01),
    (20.0, 75.02, 3.58, 404.36, 19.30),
]


def check_cell_conversion():
    print()
    print("=" * 80)
    print("CHECK 4: Y(Gy.cell)^-1 vs Y(Gy.Gbp)^-1 conversion")
    print("  Cell genome = 22 × 245 Mbp = 5390 Mbp = 5.39 Gbp")
    print("  Y_cell should = Y_Gbp × 5.39")
    print("=" * 80)
    factor = 22 * 245 / 1000.0   # 5.39
    print(f"  Conversion factor (computed) = {factor:.3f} Gbp/cell")
    print(f"{'E(MeV)':>7} {'Yssb_Gbp':>9} {'Yssb_cell_calc':>15} {'Yssb_cell_paper':>17}"
          f" {'Ydsb_Gbp':>9} {'Ydsb_cell_calc':>15} {'Ydsb_cell_paper':>17}")
    fails = 0
    for E, YsG, YdG, YsC, YdC in TABLE5_CELL:
        YsC_calc = YsG * factor
        YdC_calc = YdG * factor
        ok_s = math.isclose(YsC_calc, YsC, rel_tol=0.01)
        ok_d = math.isclose(YdC_calc, YdC, rel_tol=0.01)
        flag = "" if (ok_s and ok_d) else "  *"
        if not (ok_s and ok_d):
            fails += 1
        print(f"{E:>7} {YsG:>9.2f} {YsC_calc:>15.2f} {YsC:>17.2f}"
              f" {YdG:>9.2f} {YdC_calc:>15.2f} {YdC:>17.2f}{flag}")
    print(f"  -> {fails}/{len(TABLE5_CELL)} rows inconsistent")
    return fails


# -----------------------------------------------------------------------------
# Check 5 — Table 5 two-method yield agreement (column 2&3 vs 4&5)
# -----------------------------------------------------------------------------
TABLE5_METHODS = [
    # E, YSSB_method1 (Table2), YDSB_method1, YSSB_method2 (from PE freq), YDSB_method2
    (0.5, 39.05, 7.80, 38.97, 7.76),
    (1.0, 50.92, 7.77, 50.66, 7.68),
    (2.0, 62.74, 6.36, 62.72, 6.38),
    (10.0, 73.45, 4.30, 73.46, 4.27),
    (20.0, 75.15, 3.50, 75.02, 3.58),
]


def check_two_methods():
    print()
    print("=" * 80)
    print("CHECK 5: Table 5 — yield by direct count vs Charlton-style ΣP(E)·n(E)/y")
    print("  paper claim: 'the two methods of calculation are the same' → small Δ")
    print("=" * 80)
    print(f"{'E(MeV)':>7} {'ΔYSSB%':>8} {'ΔYDSB%':>8}")
    for E, Y1s, Y1d, Y2s, Y2d in TABLE5_METHODS:
        ds = 100.0 * (Y2s - Y1s) / Y1s
        dd = 100.0 * (Y2d - Y1d) / Y1d
        print(f"{E:>7} {ds:>8.2f} {dd:>8.2f}")
    print("  (small % differences => internally consistent; large ones => discrepancy)")


# -----------------------------------------------------------------------------
# Check 6 — Sanity on Table 3 totals: column sums should be consistent
# total_hits = NB + SSB + SSB+ + 2SSB + DSB + DSB+ + DSB++   (one classification per hit)
# -----------------------------------------------------------------------------
def check_table3_row_sums():
    print()
    print("=" * 80)
    print("CHECK 6: Table 3 row sums (NB+SSB+SSB++2SSB+DSB+DSB++DSB++ ?= total_hits)")
    print("  (one classification per event)")
    print("=" * 80)
    fails = 0
    for r in TABLE3:
        lo, hi, total, NB, SSB, SSBp, SSB2, DSB, DSBp, DSBpp = r
        s = NB + SSB + SSBp + SSB2 + DSB + DSBp + DSBpp
        diff = s - total
        flag = "" if diff == 0 else "  *"
        if diff != 0:
            fails += 1
        print(f"  [{lo:>4},{hi:>4}] eV   total={total:>5}  sum_of_cats={s:>5}  Δ={diff:+d}{flag}")
    print(f"  -> {fails}/{len(TABLE3)} rows inconsistent")
    return fails


# -----------------------------------------------------------------------------
# Check 7 — geometry sanity:  216 bp B-DNA → 73.44 nm
#   B-DNA rise per bp = 3.4 Å = 0.34 nm
# -----------------------------------------------------------------------------
def check_geometry():
    print()
    print("=" * 80)
    print("CHECK 7: B-DNA geometry")
    print("  Paper: 216 bp = 73.44 nm; 432 nucleotides")
    print("=" * 80)
    L_calc = 216 * 0.34
    print(f"  216 bp × 0.34 nm/bp = {L_calc:.2f} nm   (paper: 73.44 nm)")
    print(f"  216 bp × 2 strands  = {216*2} nucleotides   (paper: 432)")
    ok = math.isclose(L_calc, 73.44, abs_tol=0.02) and 216*2 == 432
    print(f"  -> consistent: {ok}")


if __name__ == "__main__":
    print()
    print("Mokari et al. 2018 — DOI 10.1088/1361-6560/aad7ee")
    print("Arithmetic / internal-consistency spot-checks")
    print()
    fails = 0
    fails += check_table2_definitions()
    check_table3_narrative()
    check_overlap_arithmetic()
    fails += check_cell_conversion()
    check_two_methods()
    fails += check_table3_row_sums()
    check_geometry()
    print()
    print("=" * 80)
    print(f"OVERALL inconsistencies flagged: {fails}")
    print("=" * 80)
