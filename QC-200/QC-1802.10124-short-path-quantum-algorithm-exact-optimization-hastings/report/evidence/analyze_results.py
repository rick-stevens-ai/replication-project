#!/usr/bin/env python3
"""Post-process results.json into summary tables + figures + a summary.json for the report."""
import json, os, statistics
from collections import defaultdict

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'results.json')) as f:
    R = json.load(f)

results = R['results']
print(f"Loaded {len(results)} result rows; total wall {R.get('wall_time_s'):.1f}s")

# Group by (ensemble, N, K, b)
groups = defaultdict(list)
for r in results:
    ens = r['instance'].split('_')[0]
    key = (ens, r['N'], r['K'], r['b'])
    groups[key].append(r)

# Median table
def med(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0: return None
    if n % 2 == 1: return xs[n//2]
    return 0.5 * (xs[n//2 - 1] + xs[n//2])

def pct(xs, p):
    xs = sorted(xs)
    idx = int(round((len(xs) - 1) * p / 100.0))
    return xs[idx]

summary = []
for key in sorted(groups.keys()):
    rs = groups[key]
    ens, N, K, b = key
    pov = [r['P_ov_plus_psi01'] for r in rs]
    gap = [r['min_gap'] for r in rs]
    ratio = [r['ratio_short_over_grover'] for r in rs]
    pov0001 = [r['P_ov_psi00_psi01'] for r in rs]
    psuccdir = [r['P_success_direct'] for r in rs]
    ngs = [r['num_ground_states'] for r in rs]
    summary.append(dict(
        ensemble=ens, N=N, K=K, b=b, n_inst=len(rs),
        median_P_ov=med(pov),
        p25_P_ov=pct(pov, 25),
        p75_P_ov=pct(pov, 75),
        median_min_gap=med(gap),
        median_P_ov_00_01=med(pov0001),
        median_P_succ_direct=med(psuccdir),
        median_ratio_short_over_grover=med(ratio),
        p25_ratio=pct(ratio, 25),
        p75_ratio=pct(ratio, 75),
        median_num_ground_states=med(ngs),
    ))

with open(os.path.join(here, 'summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

# Human-readable table
print("\n==== SUMMARY (median across instances) ====")
print(f"{'ens':6} {'N':>3} {'K':>3} {'b':>5} {'nInst':>5} {'P_ov':>7} {'gap':>7} {'P00.01':>7} {'Pdir':>7} {'#GS':>4} {'T_sp/T_G':>9}")
for row in summary:
    print(f"{row['ensemble']:6} {row['N']:3d} {row['K']:3d} {row['b']:5.2f} "
          f"{row['n_inst']:5d} {row['median_P_ov']:7.4f} {row['median_min_gap']:7.4f} "
          f"{row['median_P_ov_00_01']:7.4f} {row['median_P_succ_direct']:7.4f} "
          f"{int(row['median_num_ground_states']):4d} {row['median_ratio_short_over_grover']:9.4f}")

# Scaling analysis: for fixed (ensemble, K, b), how does T_sp/T_G change with N?
# The paper predicts a constant improvement: ratio ~ exp(-b/(2DK) * N) with D=2.
# So log(ratio) should be linear in N with slope -b/(2*2*K).
print("\n==== SCALING (log ratio vs N) ====")
import math
by_scan = defaultdict(list)
for row in summary:
    by_scan[(row['ensemble'], row['K'], row['b'])].append((row['N'], row['median_ratio_short_over_grover']))
for key, pts in sorted(by_scan.items()):
    if len(pts) < 2:
        continue
    pts.sort()
    Ns = [p[0] for p in pts]
    ratios = [p[1] for p in pts]
    logr = [math.log(max(r, 1e-30)) for r in ratios]
    # Fit slope by least squares vs N
    n = len(Ns)
    xm = sum(Ns)/n
    ym = sum(logr)/n
    num = sum((Ns[i]-xm)*(logr[i]-ym) for i in range(n))
    den = sum((Ns[i]-xm)**2 for i in range(n))
    slope = num/den if den > 0 else 0
    b = key[2]; K = key[1]
    theory_slope = -b/(2*2*K)  # D=2 for 2-body Ising
    print(f"  ens={key[0]} K={K} b={b}: Ns={Ns} ratios={[f'{r:.3f}' for r in ratios]} "
          f"empirical slope={slope:+.4f} theory slope={theory_slope:+.4f}")

# Save scaling analysis too
scaling = []
for key, pts in sorted(by_scan.items()):
    if len(pts) < 2: continue
    pts.sort()
    Ns = [p[0] for p in pts]; ratios = [p[1] for p in pts]
    logr = [math.log(max(r, 1e-30)) for r in ratios]
    n=len(Ns); xm=sum(Ns)/n; ym=sum(logr)/n
    num=sum((Ns[i]-xm)*(logr[i]-ym) for i in range(n))
    den=sum((Ns[i]-xm)**2 for i in range(n))
    slope=num/den if den>0 else 0
    b=key[2]; K=key[1]
    scaling.append(dict(ensemble=key[0], K=K, b=b, Ns=Ns, ratios=ratios,
                        empirical_slope=slope, theory_slope=-b/(2*2*K)))
with open(os.path.join(here, 'scaling.json'), 'w') as f:
    json.dump(scaling, f, indent=2)
print("\nWrote summary.json + scaling.json")
