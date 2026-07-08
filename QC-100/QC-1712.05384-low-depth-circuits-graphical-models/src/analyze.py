"""Analyze sweep.json:
  - Verify TN==SV amplitude within 1e-10 for all points (correctness).
  - Fit contraction_width vs depth at fixed ell*m; check for the paper's
    predicted min(O(d*ell), O(n)) upper bound.
  - Compare TN opt_cost_flops vs statevector cost 2**n.

The paper's Fig 4 shows max_tensor_rank (== contraction width) growing roughly
linearly with depth for 6x6/6x7/7x7 up to depths 25-45. At small n and small d
we operate in the *low-depth* regime where width should be bounded by
d * ell for ell < m (min lateral dim). We report:
  - per (ell, m, d): width vs the theoretical upper bound min(d*ell, n).
  - fraction of points satisfying width <= min(d*ell, n).
  - a monotonicity check: for fixed ell*m, width nondecreasing in d.
"""

import json
import math
import sys
from collections import defaultdict
from statistics import mean

path = sys.argv[1] if len(sys.argv) > 1 else "../report/evidence/sweep.json"
with open(path) as f:
    data = json.load(f)
results = data["results"]

max_diff = max(r["max_abs_diff"] for r in results)
n_points = len(results)

print(f"# TN-vs-SV correctness check")
print(f"points:      {n_points}")
print(f"max_abs_diff over ALL points: {max_diff:.2e}")
tol = 1e-10
n_ok = sum(1 for r in results if r["max_abs_diff"] < tol)
print(f"points with |tn-sv| < {tol}: {n_ok} / {n_points}")
print()

print("# Theoretical bound check: contraction_width <= min(d*ell_min, n)")
# ell_min in the paper is the *smaller* lateral dimension. In our sweep the
# code uses (ell, m) with ell <= m by convention in the default sweep.
n_pass_bound = 0
per_grid = defaultdict(list)
for r in results:
    ell = r["ell"]; m = r["m"]; d = r["depth"]; n = r["n"]
    ell_min = min(ell, m)
    bound = min(d * ell_min, n)
    w = r["contraction_width_log2"]
    per_grid[(ell, m)].append((d, w, bound, r["opt_cost_flops"], r["statevector_cost_2n"]))
    if w <= bound + 1e-9:
        n_pass_bound += 1
print(f"points satisfying width <= min(d*ell_min, n): {n_pass_bound} / {n_points}")
print()

print("# Width-vs-depth (grouped by grid; width is our TN analog of treewidth)")
print(f"{'grid':>8} {'n':>4} {'d':>3} {'width':>6} {'bound=min(d*l,n)':>16} {'flops':>10} {'2**n':>10} {'ratio 2^n/flops':>16}")
for (ell, m), pts in sorted(per_grid.items()):
    for (d, w, bound, flops, sv2n) in sorted(pts):
        ratio = sv2n / max(flops, 1)
        n = ell * m
        print(f"{ell}x{m:<3}   {n:>4} {d:>3} {w:>6.2f} {bound:>16} {flops:>10.2e} {sv2n:>10} {ratio:>16.3f}")
    print()

print("# Monotonicity in depth (width should be nondecreasing as d increases at fixed grid)")
mono_ok = True
for (ell, m), pts in sorted(per_grid.items()):
    ws = [w for (d, w, _b, _f, _s) in sorted(pts)]
    for a, b in zip(ws, ws[1:]):
        if b + 1e-9 < a:
            print(f"  MONO VIOLATION at grid={ell}x{m}: widths={ws}")
            mono_ok = False
            break
print("monotonicity in depth:", "OK" if mono_ok else "VIOLATED")
print()

print("# Ratio TN cost / statevector cost per grid (mean over depths)")
print(f"{'grid':>8} {'n':>4} {'mean(flops)':>14} {'2^n':>10} {'mean(flops)/2^n':>18}")
for (ell, m), pts in sorted(per_grid.items()):
    n = ell * m
    mflops = mean(p[3] for p in pts)
    print(f"{ell}x{m:<3}   {n:>4} {mflops:>14.2e} {2**n:>10} {mflops / (2**n):>18.4f}")
