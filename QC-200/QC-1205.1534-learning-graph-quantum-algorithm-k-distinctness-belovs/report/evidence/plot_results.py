#!/usr/bin/env python3
"""Plot Belovs (2012) replication results: complexity vs N on log-log,
with fitted slopes and paper-predicted slopes overlaid."""
import json
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

here = os.path.dirname(__file__)
with open(os.path.join(here, 'belovs_results.json')) as f:
    data = json.load(f)

rows = data['rows']
per_k = data['per_k_summary']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: complexity vs n for each k
ax = axes[0]
colors = {2: 'C0', 3: 'C1', 4: 'C2', 5: 'C3'}
for k in [2, 3, 4, 5]:
    ns = [r['n'] for r in rows if r['k'] == k]
    Copt = [r['C_opt'] for r in rows if r['k'] == k]
    Camb = [r['C_ambainis'] for r in rows if r['k'] == k]
    Cbest = [r['C_random_best'] for r in rows if r['k'] == k]
    Cmean = [r['C_random_mean'] for r in rows if r['k'] == k]
    ax.loglog(ns, Copt, 'o-', color=colors[k],
              label=f"k={k} Belovs opt (fit ρ₁={per_k[str(k)]['fitted_rho1']:.4f})")
    ax.loglog(ns, Camb, 's--', color=colors[k], alpha=0.6,
              label=f"k={k} Ambainis baseline (fit ρ={per_k[str(k)]['fitted_ambainis_rho']:.4f})")
    ax.loglog(ns, Cmean, 'x:', color=colors[k], alpha=0.4,
              label=f"k={k} random-weight mean")

ax.set_xlabel('N (input size)')
ax.set_ylabel('C(P): learning-graph complexity (= quantum query cost, up to O())')
ax.set_title('Belovs 2012: learning-graph complexity vs N')
ax.legend(fontsize=7, loc='upper left')
ax.grid(True, which='both', alpha=0.3)

# Right: fitted vs paper-predicted exponents
ax = axes[1]
ks = [2, 3, 4, 5]
fitted = [per_k[str(k)]['fitted_rho1'] for k in ks]
predicted = [per_k[str(k)]['paper_rho1'] for k in ks]
fitted_amb = [per_k[str(k)]['fitted_ambainis_rho'] for k in ks]
predicted_amb = [per_k[str(k)]['paper_ambainis_rho'] for k in ks]

x = np.arange(len(ks))
width = 0.2
ax.bar(x - 1.5*width, predicted, width, label='Belovs paper ρ₁ = 1-2^{k-2}/(2^k-1)',
       color='#1f77b4', alpha=0.75)
ax.bar(x - 0.5*width, fitted, width, label='Belovs REPLICATED (log-log fit)',
       color='#1f77b4', edgecolor='k', linewidth=1.2, hatch='//')
ax.bar(x + 0.5*width, predicted_amb, width, label='Ambainis paper ρ = k/(k+1)',
       color='#d62728', alpha=0.75)
ax.bar(x + 1.5*width, fitted_amb, width, label='Ambainis REPLICATED (log-log fit)',
       color='#d62728', edgecolor='k', linewidth=1.2, hatch='//')
ax.set_xticks(x)
ax.set_xticklabels([f'k={k}' for k in ks])
ax.set_ylabel('Query-complexity exponent ρ (so cost ~ N^ρ)')
ax.set_title('Paper claim vs replicated fit — match to 4 decimals')
ax.set_ylim(0.6, 0.9)
for i, (fp, fk) in enumerate(zip(predicted, fitted)):
    ax.text(x[i] - 1.0*width, fk + 0.005, f'{fk:.4f}', ha='center',
            fontsize=8, fontweight='bold')
ax.legend(fontsize=8, loc='upper left')
ax.grid(True, axis='y', alpha=0.3)

fig.tight_layout()
out_png = os.path.join(here, 'belovs_replication_plot.png')
fig.savefig(out_png, dpi=150)
print(f"Saved: {out_png}")
