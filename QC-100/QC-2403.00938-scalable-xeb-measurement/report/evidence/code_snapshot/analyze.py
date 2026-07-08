"""Analyze the XEB-MIPT sweep JSONs, print summary + save plot + summary CSV."""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here = Path(__file__).parent
ev = here.parent / 'report' / 'evidence'

def load(fname):
    with open(ev / fname) as f:
        return json.load(f)

runs = {
    4: load('sweep_L4.json'),
    6: load('sweep_L6.json'),
    8: load('sweep_L8.json'),
}

# Build combined table: L -> [(p, chi_diff_mean, chi_diff_sem, chi_same_mean)]
rows = []
for L, r in runs.items():
    for p_str in sorted(r['diff_input'][str(L)].keys(), key=float):
        d = r['diff_input'][str(L)][p_str]
        s = r['same_input'][str(L)][p_str]
        rows.append((L, float(p_str), d['mean'], d['sem'], d['n'], s['mean']))

# Print + CSV
csv_lines = ['L,p,chi_diff_mean,chi_diff_sem,n_circuits,chi_same_mean']
print('\nCombined results:')
print(f'  {"L":>3} {"p":>6} {"chi_diff":>10} {"sem":>8} {"n":>4} {"chi_same":>10}')
for (L, p, cd, se, n, cs) in rows:
    print(f'  {L:>3} {p:>6.3f} {cd:>10.4f} {se:>8.4f} {n:>4} {cs:>10.4f}')
    csv_lines.append(f'{L},{p:.3f},{cd:.6f},{se:.6f},{n},{cs:.6f}')

with open(ev / 'chi_vs_p_all_L.csv', 'w') as f:
    f.write('\n'.join(csv_lines) + '\n')
print(f'\nWrote {ev / "chi_vs_p_all_L.csv"}')

# Plot chi_diff vs p, one line per L
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
colors = {4: 'tab:blue', 6: 'tab:orange', 8: 'tab:green'}
for L in (4, 6, 8):
    r = runs[L]
    ps = sorted(r['diff_input'][str(L)].keys(), key=float)
    xs = [float(p) for p in ps]
    ys = [r['diff_input'][str(L)][p]['mean'] for p in ps]
    yerr = [r['diff_input'][str(L)][p]['sem'] for p in ps]
    ax1.errorbar(xs, ys, yerr=yerr, marker='o', label=f'L={L}', color=colors[L])
    ys_s = [r['same_input'][str(L)][p]['mean'] for p in ps]
    ax2.plot(xs, ys_s, marker='s', label=f'L={L}', color=colors[L])
ax1.axvline(0.14, ls='--', color='gray', alpha=0.6, label='paper $p_c=0.14$')
ax1.set_xlabel('p (mid-circuit measurement rate)')
ax1.set_ylabel(r'$\chi = E_C[\chi_C]$')
ax1.set_title(r'Linear XEB order parameter $\chi$ vs $p$'
              '\n' + r'($\rho=|0T\rangle^{L/2}$, $\sigma=|0\rangle^L$)')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_ylim(0.5, 1.05)

ax2.axhline(1.0, ls='--', color='gray', alpha=0.6, label='ideal $\chi=1$')
ax2.set_xlabel('p (mid-circuit measurement rate)')
ax2.set_ylabel(r'$\chi_{\rho=\sigma}$')
ax2.set_title(r'Sanity: $\chi$ with $\rho=\sigma=|0\rangle^L$ (should be exactly 1)')
ax2.legend()
ax2.grid(alpha=0.3)
ax2.set_ylim(0.95, 1.05)

plt.tight_layout()
outfig = ev / 'chi_vs_p.png'
plt.savefig(outfig, dpi=140)
print(f'Wrote {outfig}')

# Diagnostic: do the L curves cross?
# For each pair (L1, L2), find the smallest p where sign(chi(L1,p) - chi(L2,p)) flips.
def curve(L):
    r = runs[L]
    ps = sorted(r['diff_input'][str(L)].keys(), key=float)
    return [(float(p), r['diff_input'][str(L)][p]['mean']) for p in ps]

print()
print('Crossing diagnostic (does chi(L1) > chi(L2) hold uniformly, or do curves cross?):')
for L1, L2 in ((4, 6), (4, 8), (6, 8)):
    c1 = dict(curve(L1))
    c2 = dict(curve(L2))
    common = sorted(set(c1.keys()) & set(c2.keys()))
    diffs = [(p, c1[p] - c2[p]) for p in common]
    print(f'  L={L1} vs L={L2}: '
          + ', '.join(f'p={p:.3f}: dL={d:+.4f}' for p, d in diffs))

# For paper: in the volume-law phase (p < pc), chi(L) should INCREASE with L toward 1;
# in area-law (p > pc), chi(L) should DECREASE with L toward a const < 1.  Crossing = pc.
print()
print('Interpretation: in the volume-law phase (p < pc), chi grows toward 1 with L;')
print('in the area-law phase (p > pc), chi shrinks with L toward a const < 1.')
print('A sign flip of dL = chi(L1) - chi(L2) across p indicates a crossing near p ~ pc.')
