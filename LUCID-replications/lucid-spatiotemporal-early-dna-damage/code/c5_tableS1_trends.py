"""
Claims C1, C2, C3 — qualitative trends in Table S1 (NBS1 FRAP fits).

Table S1 (as parsed from supplements/TableS1.txt):
  X-ray                      LET=1       k*on=0.372    koff=0.047
  C-ions                     LET=170     k*on=0.089    koff=0.026
  Ar-ions                    LET=1550    k*on=0.164    koff=0.016
  Ar-ions + CK2 inhibition   LET=1550    k*on=0.023    koff=0.007
  Ni-ions                    LET=3430    k*on=0.243    koff=0.030
  Xe-ions                    LET=8655    k*on=0.071    koff=0.010
  U-ions                     LET=14350   k*on=0.077    koff=0.011
  U-ions + CK2 inhibition    LET=15000   k*on=0.0054   koff=0.0040
                                                      (also second row 0.0280, 0.0040 -- ambiguous; we take the smaller k*on
                                                       row matching the CK2i convention)

Tests:
  C1: among the *no-inhibitor* rows, does koff DECREASE as LET INCREASES?
      Spearman rank correlation of koff vs LET should be strongly negative
      when we use the high-LET rows that the paper visualizes in Fig 8A.
      Paper claim: "With increasing LET, i.e., increasing lesion density,
      the binding constants decrease and approach values close to the one
      obtained after lower LET irradiation but with CK2 inhibition."

  C2: koff(Ar+CK2i) < koff(Ar)?   koff(U+CK2i) < koff(U)?
      Paper claim: CK2i isolates the inner-focus binding which is slower.

  C3: At high LET (Xe 8655, U 14350) koff is close to koff(Ar+CK2i)=0.007.
      Quantify the gap and compare to the X-ray baseline 0.047.
"""
import json, os

# Table S1 entries (LET in keV/um, k*on in 1/s, koff in 1/s)
table = [
    # tag,                       LET,    k_on,    koff
    ("X-ray",                       1.0,  0.372,  0.047),
    ("C-ions",                    170.0,  0.089,  0.026),
    ("Ar-ions",                  1550.0,  0.164,  0.016),
    ("Ar-ions+CK2i",             1550.0,  0.023,  0.007),
    ("Ni-ions",                  3430.0,  0.243,  0.030),
    ("Xe-ions",                  8655.0,  0.071,  0.010),
    ("U-ions",                  14350.0,  0.077,  0.011),
    ("U-ions+CK2i",             15000.0,  0.0054, 0.0040),
]

def spearman(xs, ys):
    """Minimal Spearman rank correlation."""
    n = len(xs)
    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0]*n
        for k, idx in enumerate(order):
            r[idx] = k + 1
        # ties (simple, OK for this size)
        return r
    rx, ry = ranks(xs), ranks(ys)
    dx = [a-b for a,b in zip(rx, ry)]
    return 1 - 6*sum(d*d for d in dx)/(n*(n*n-1))

# --- C1: koff vs LET trend, NO inhibitor rows ---
noinhib = [(tag, l, k_on, koff) for (tag, l, k_on, koff) in table if "CK2i" not in tag]
lets = [row[1] for row in noinhib]
koffs = [row[3] for row in noinhib]

print("=== C1: koff vs LET (no inhibitor) ===")
for tag, l, k_on, koff in noinhib:
    print(f"  {tag:>10s}  LET={l:>7.0f}  k*on={k_on:>7.4f}  koff={koff:>7.4f}")
rho = spearman(lets, koffs)
print(f"  Spearman rank correlation koff vs LET: rho = {rho:+.3f}")
# Test: linear fit slope sign
import statistics
mx, my = statistics.mean(lets), statistics.mean(koffs)
cov = sum((x-mx)*(y-my) for x,y in zip(lets, koffs)) / len(lets)
varx = sum((x-mx)**2 for x in lets) / len(lets)
slope = cov / varx
print(f"  Linear fit slope d(koff)/d(LET) = {slope:.3e}")
trend_decreases = slope < 0
print(f"  Paper claim 'koff decreases with LET': {trend_decreases}")

# --- C2: CK2 inhibitor lowers koff ---
print("\n=== C2: CK2 inhibitor lowers koff ===")
pairs = [
    ("Ar (1550)", 0.016, 0.007),       # without / with CK2i
    ("U (14350 vs 15000)", 0.011, 0.0040),
]
c2_ok = True
for label, base, ck2i in pairs:
    drop = (base - ck2i) / base
    print(f"  {label:>22s}  koff={base:.4f} -> {ck2i:.4f}  drop {drop:.1%}")
    if not (ck2i < base):
        c2_ok = False
print(f"  Paper claim 'CK2i lowers koff (inner-focus is slower)': {c2_ok}")

# --- C3: high-LET koff approaches Ar+CK2i value ---
print("\n=== C3: high-LET koff approaches inner-focus (CK2i) baseline ===")
inner_baseline = 0.007   # Ar+CK2i koff
xray_koff = 0.047
xe_koff = 0.010
u_koff = 0.011
print(f"  X-ray baseline koff      = {xray_koff}")
print(f"  Ar+CK2i baseline koff    = {inner_baseline}   <- inner-focus pure")
print(f"  Xe-ions (LET=8655) koff  = {xe_koff}")
print(f"  U-ions  (LET=14350) koff = {u_koff}")
gap_xray   = abs(xray_koff - inner_baseline)
gap_xe     = abs(xe_koff - inner_baseline)
gap_u      = abs(u_koff - inner_baseline)
print(f"  |X-ray - inner|          = {gap_xray:.4f}")
print(f"  |Xe   - inner|           = {gap_xe:.4f}")
print(f"  |U    - inner|           = {gap_u:.4f}")
gap_shrunk = (gap_xe < gap_xray) and (gap_u < gap_xray)
fold_xray = gap_xray / inner_baseline
fold_u    = gap_u    / inner_baseline
print(f"  high-LET gap shrinks vs X-ray baseline: {gap_shrunk}")
print(f"  X-ray gap is {fold_xray:.1f}x baseline; U gap is {fold_u:.1f}x baseline.")

results = {
    "C1_koff_vs_LET": {
        "rows_no_inhibitor": [
            {"tag": t, "LET": l, "k_on": k_on, "koff": koff}
            for (t, l, k_on, koff) in noinhib
        ],
        "spearman_rho": rho,
        "linear_slope_per_keVum": slope,
        "trend_decreases": trend_decreases,
        "verdict": "REPRODUCED" if trend_decreases and rho < -0.3 else (
                   "WEAK" if trend_decreases else "MISMATCH"),
        "note": "Bin around Ni-ions (3430) is the obvious outlier in the table — "
                "see paper Fig 8A error bars. We do not exclude it.",
    },
    "C2_CK2i_lowers_koff": {
        "Ar_pair":   {"without_CK2i": 0.016,  "with_CK2i": 0.007},
        "U_pair":    {"without_CK2i": 0.011,  "with_CK2i": 0.0040},
        "verdict": "REPRODUCED" if c2_ok else "MISMATCH",
    },
    "C3_high_LET_approaches_inner": {
        "inner_baseline_koff":  inner_baseline,
        "X_ray_baseline_koff":  xray_koff,
        "high_LET_koffs":       {"Xe_8655": xe_koff, "U_14350": u_koff},
        "abs_gaps_to_inner":    {"X_ray": gap_xray, "Xe": gap_xe, "U": gap_u},
        "fold_ratios_vs_inner": {"X_ray": fold_xray, "U": fold_u},
        "verdict": "REPRODUCED" if gap_shrunk else "MISMATCH",
    },
}
out_path = os.path.join(os.path.dirname(__file__), "..", "results", "c5_tableS1_trends.json")
out_path = os.path.normpath(out_path)
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved -> {out_path}")
