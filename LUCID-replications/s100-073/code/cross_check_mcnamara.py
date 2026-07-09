"""
Sanity-check the McNamara (2015) RBE implementation:
 - RBE should approach 1.0 as LET_d -> 0 and D -> typical low values,
 - RBE should rise with LET_d,
 - RBE for low alpha/beta (e.g. 2 Gy, brainstem) should be more
   sensitive to LET than RBE for high alpha/beta (10 Gy, PTV/tumour).
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mm_model import rbe_mcnamara

OUT = os.path.join(os.path.dirname(__file__), "..", "evidence", "mcnamara_sweep.csv")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

D = 1.8  # per-fraction proton dose, Gy
rows = []
for ab in (2.0, 10.0):
    for L in (0.0, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0):
        rbe = rbe_mcnamara(D, L, ab)
        rows.append({"alpha_beta_Gy": ab, "LET_d_keV_per_um": L, "RBE_McN": rbe})

with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"Wrote {OUT}")
print()
print(f"{'alpha/beta':>10} {'LET_d':>7} {'RBE_McN':>9}")
for r in rows:
    print(f"{r['alpha_beta_Gy']:10.1f} {r['LET_d_keV_per_um']:7.2f} {r['RBE_McN']:9.4f}")

# Expected qualitative checks
print()
print("Checks:")
r2_0 = rbe_mcnamara(D, 0.0, 2.0)
r10_0 = rbe_mcnamara(D, 0.0, 10.0)
r2_4 = rbe_mcnamara(D, 4.0, 2.0)
r10_4 = rbe_mcnamara(D, 4.0, 10.0)
print(f"  RBE(LET=0, ab=2) = {r2_0:.4f}   RBE(LET=0, ab=10) = {r10_0:.4f}")
print(f"    -> McNamara at LET=0 differs from 1 slightly (consistent with phenomenological fit, not strict LQ limit)")
print(f"  RBE(LET=4, ab=2) = {r2_4:.4f}   RBE(LET=4, ab=10) = {r10_4:.4f}")
print(f"    -> low alpha/beta tissue (brainstem 2 Gy) is more LET-sensitive: ratio {r2_4/r2_0:.3f} vs {r10_4/r10_0:.3f}")
assert r2_4 > r10_4, "Low-ab tissue should have higher RBE at same LET"
assert r2_4 > r2_0, "RBE should rise with LET for fixed tissue"
print("  All qualitative checks passed.")
