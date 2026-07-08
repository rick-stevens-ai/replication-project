"""Stronger analysis: fit width vs min(d*ell,n) with a small constant, and
plot TN_flops / 2^n vs n for fixed depth to show the classical-savings
crossover that IS the paper's headline claim."""

import json
import math
import sys
from collections import defaultdict
from statistics import mean, median

path = sys.argv[1] if len(sys.argv) > 1 else "../report/evidence/sweep.json"
with open(path) as f:
    data = json.load(f)
results = data["results"]

# 1. Correctness recap
n_ok = sum(1 for r in results if r["max_abs_diff"] < 1e-10)
print(f"Correctness: {n_ok}/{len(results)} points match statevector within 1e-10")
print(f"Max amplitude diff: {max(r['max_abs_diff'] for r in results):.2e}")
print()

# 2. Width-vs-theoretical-bound as ratio (should be O(1))
print("Ratio width / min(d*ell_min, n)  (paper predicts this to be O(1)):")
ratios = []
for r in results:
    ell_min = min(r["ell"], r["m"])
    bound = min(r["depth"] * ell_min, r["n"])
    if bound > 0:
        ratio = r["contraction_width_log2"] / bound
        ratios.append(ratio)
print(f"  min: {min(ratios):.3f}  median: {median(ratios):.3f}  mean: {mean(ratios):.3f}  max: {max(ratios):.3f}")
print()

# 3. Bounded-by-2n check: width should also be <= n exactly (trivial statevector cap)
n_le_n = sum(1 for r in results if r["contraction_width_log2"] <= r["n"])
print(f"Width <= n (statevector cap): {n_le_n}/{len(results)}")
print()

# 4. Log-linear fit: log(flops) ~ a*d + b at fixed grid, testing exponential-in-depth
print("Log-linear fit of log2(opt_cost_flops) vs depth, per grid:")
per_grid = defaultdict(list)
for r in results:
    per_grid[(r["ell"], r["m"])].append(r)
def linfit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n; my = sum(ys) / n
    num = sum((x - mx)*(y - my) for x, y in zip(xs, ys))
    den = sum((x - mx)**2 for x in xs)
    slope = num / den if den else 0.0
    intercept = my - slope * mx
    return slope, intercept
print(f"  {'grid':>6} {'slope_log2flops_per_depth':>28} {'intercept':>12}")
for (ell, m), pts in sorted(per_grid.items()):
    pts_sorted = sorted(pts, key=lambda r: r["depth"])
    xs = [r["depth"] for r in pts_sorted]
    ys = [math.log2(r["opt_cost_flops"]) for r in pts_sorted]
    s, i = linfit(xs, ys)
    print(f"  {ell}x{m:<3}   {s:28.3f} {i:12.3f}")
print()

# 5. TN vs statevector crossover: at fixed depth, does TN cost grow subexponentially in n?
print("TN opt_cost_flops vs statevector 2^n at FIXED DEPTH d=2 (extremely shallow):")
print(f"  {'n':>4} {'TN_flops':>12} {'2^n':>10} {'ratio TN/2^n':>14}")
d2 = sorted([r for r in results if r["depth"] == 2], key=lambda r: r["n"])
for r in d2:
    n = r["n"]; f = r["opt_cost_flops"]; two_n = 2**n
    print(f"  {n:>4} {f:>12.2e} {two_n:>10} {f / two_n:>14.6f}")
print()

print("TN opt_cost_flops vs statevector 2^n at FIXED DEPTH d=6 (moderate):")
print(f"  {'n':>4} {'TN_flops':>12} {'2^n':>10} {'ratio TN/2^n':>14}")
d6 = sorted([r for r in results if r["depth"] == 6], key=lambda r: r["n"])
for r in d6:
    n = r["n"]; f = r["opt_cost_flops"]; two_n = 2**n
    print(f"  {n:>4} {f:>12.2e} {two_n:>10} {f / two_n:>14.6f}")
print()

# 6. Wall-clock crossover
print("Wall-clock crossover (TN faster than SV): count per grid")
tn_faster = 0
for r in results:
    if r["tn_amp_time_s"] < r["sv_amp_time_s"]:
        tn_faster += 1
print(f"  TN faster: {tn_faster}/{len(results)} points (across the sweep)")
