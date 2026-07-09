#!/usr/bin/env python3
"""
s100-064 — Fig. 5 monotonicity audit
Claim: RBE_DSB monotonically increases with yD across the eight X-ray
spectra of Table 1.

We import the (yD, RBE_DSB) pairs from Table 1 and compute Pearson r and
a least-squares slope.  No external dependencies (stdlib math only).
"""

from __future__ import annotations
import math

# (beam, yD keV/um, RBE_DSB) from Table 1.
rows = [
    ("60 kVp",                 4.39, 1.18),
    ("100 kVp",                4.53, 1.17),
    ("200 kVp standard",       4.60, 1.00),
    ("250 kVp",                4.45, 1.39),
    ("6 MV in-field 1 cm",     2.45, 0.73),
    ("6 MV in-field 5 cm",     2.47, 0.76),
    ("6 MV in-field 10 cm",    2.44, 0.85),
    ("6 MV out-of-field 10 cm",3.00, 0.85),
]
xs = [r[1] for r in rows]
ys = [r[2] for r in rows]

n = len(xs)
mx = sum(xs) / n
my = sum(ys) / n
sxx = sum((x - mx) ** 2 for x in xs)
syy = sum((y - my) ** 2 for y in ys)
sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))

slope = sxy / sxx
intercept = my - slope * mx
r = sxy / math.sqrt(sxx * syy)

print("=== s100-064 :: Fig. 5 monotonicity audit ===")
print(f"{'Beam':<26s} {'yD (keV/um)':>12s} {'RBE_DSB':>9s}")
for b, x, y in rows:
    print(f"{b:<26s} {x:>12.2f} {y:>9.2f}")
print()
print(f"Linear fit  RBE_DSB = a*yD + b :  a = {slope:.4f}   b = {intercept:.4f}")
print(f"Pearson r          = {r:.4f}")
print(f"Pearson r^2        = {r*r:.4f}")
print()
# Group means (kVp vs MV) — the headline trend.
kvp_yd = [x for (b, x, _) in rows if "kVp" in b]
kvp_rb = [y for (b, _, y) in rows if "kVp" in b]
mv_yd  = [x for (b, x, _) in rows if "MV"  in b]
mv_rb  = [y for (b, _, y) in rows if "MV"  in b]
print(f"kVp mean yD = {sum(kvp_yd)/len(kvp_yd):.2f}   mean RBE = {sum(kvp_rb)/len(kvp_rb):.2f}")
print(f"MV  mean yD = {sum(mv_yd)/len(mv_yd):.2f}   mean RBE = {sum(mv_rb)/len(mv_rb):.2f}")
print()
ratio_yd  = (sum(kvp_yd)/len(kvp_yd)) / (sum(mv_yd)/len(mv_yd))
ratio_rbe = (sum(kvp_rb)/len(kvp_rb)) / (sum(mv_rb)/len(mv_rb))
print(f"kVp/MV ratio of yD  = {ratio_yd:.2f}")
print(f"kVp/MV ratio of RBE = {ratio_rbe:.2f}")
print()
print("Claim 'RBE_DSB monotonically increases with yD' is supported iff r > 0 "
      "AND kVp/MV yD ratio direction matches kVp/MV RBE direction.")
