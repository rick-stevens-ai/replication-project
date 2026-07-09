#!/usr/bin/env python3
"""Plot full-IMK predicted survival curves vs digitized Fig 3 data points."""
import json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from imk_full import survival_IMK

ROOT = os.path.join(os.path.dirname(__file__), '..')
with open(os.path.join(ROOT, 'results', 'fig3_digitized.json')) as f:
    dig = json.load(f)

def filter_data(pts, min_size=8, max_size=30, dose_max=None):
    out = [p for p in pts if min_size <= p['size'] <= max_size]
    if dose_max is not None:
        out = [p for p in out if p['dose'] <= dose_max]
    return out

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
cells = [('AGO1522', 'A_AGO1522', axes[0], 8.0),
         ('DU145',   'B_DU145',   axes[1], 10.0)]

for cell, panel_key, ax, D_max in cells:
    D = np.linspace(0.01, D_max, 100)

    # Model curves
    S_mf = [survival_IMK(cell, 'MF_inField', d)[0] for d in D]
    S_uf = [survival_IMK(cell, 'UF',         d)[0] for d in D]
    S_mf_TE = [np.exp(-survival_IMK(cell, 'MF_inField', d)[1]) for d in D]
    S_uf_TE = [np.exp(-survival_IMK(cell, 'UF',         d)[1]) for d in D]

    ax.plot(D, S_mf, '-',  color='blue',  lw=2, label='MF in-field (TE+NTE)')
    ax.plot(D, S_uf, '-',  color='green', lw=2, label='UF (TE+NTE)')
    ax.plot(D, S_mf_TE, '--', color='blue',  lw=1, alpha=0.6, label='MF in-field (TE only)')
    ax.plot(D, S_uf_TE, '--', color='green', lw=1, alpha=0.6, label='UF (TE only)')

    # Out-of-field model: at fixed in-field dose=4 Gy, vary scatter dose
    D_OF = np.linspace(0.01, min(0.5, D_max), 50)
    S_of = [survival_IMK(cell, 'MF_outField', 4.0, scatter_OF=d)[0] for d in D_OF]
    ax.plot(D_OF, S_of, '-', color='red', lw=2, label='MF out-of-field (D_IF=4 Gy)')

    # Digitized data points
    panel = dig[panel_key]
    mf_pts = filter_data(panel['blue_MF_inField'], dose_max=D_max)
    ax.scatter([p['dose'] for p in mf_pts], [p['surv'] for p in mf_pts],
               marker='D', color='blue', s=40, edgecolors='k', label='MF in-field (Fig 3 data)')
    of_pts = filter_data(panel['red_MF_outField'], min_size=10, max_size=30, dose_max=0.5)
    if of_pts:
        ax.scatter([p['dose'] for p in of_pts], [p['surv'] for p in of_pts],
                   marker='^', color='red', s=40, edgecolors='k', label='MF out-of-field (Fig 3 data)')

    if panel['green_UF']:
        uf_pts = filter_data(panel['green_UF'], dose_max=D_max)
        if uf_pts:
            ax.scatter([p['dose'] for p in uf_pts], [p['surv'] for p in uf_pts],
                       marker='D', facecolors='none', edgecolors='green', s=40, label='UF (Fig 3 data)')

    ax.set_yscale('log')
    ax.set_ylim(1e-4, 2)
    ax.set_xlim(0, D_max + 0.5)
    ax.set_xlabel('Dose (Gy)')
    ax.set_title(f'{cell}: Full IMK vs Fig 3 (digitized)')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=8, loc='lower left')

axes[0].set_ylabel('Cell surviving fraction')
plt.tight_layout()
out = os.path.join(ROOT, 'results', 'imk_vs_fig3_plot.png')
plt.savefig(out, dpi=120)
print('Wrote:', out)
