#!/usr/bin/env python
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here = Path(__file__).resolve().parent.parent
with open(here / 'report' / 'evidence' / 'results.json') as fp:
    r = json.load(fp)

ms = np.array(r['ms_std'])
F_s = np.array(r['standard_rb']['survival'])
s_s = np.array(r['standard_rb']['survival_sem'])
F_r = np.array(r['real_rb']['survival'])
s_r = np.array(r['real_rb']['survival_sem'])
F_re = np.array(r['real_rb_reduced']['survival'])
s_re = np.array(r['real_rb_reduced']['survival_sem'])

fit_s = r['standard_rb']['fit']
fit_r = r['real_rb']['fit']
fit_re = r['real_rb_reduced']['fit']

ms_fine = np.linspace(0, ms.max(), 400)
model = lambda m, A, B, f: A + B * (f ** m)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.errorbar(ms, F_s, yerr=s_s, fmt='o', color='C0', label=f'Std Clifford RB (|G|=24, 30 seq)  f={fit_s["f"]:.4f}, r={fit_s["r"]:.4f}')
ax.plot(ms_fine, model(ms_fine, fit_s['A'], fit_s['B'], fit_s['f']), '-', color='C0', alpha=0.7)

ax.errorbar(ms, F_r, yerr=s_r, fmt='s', color='C1', label=f'Real Clifford RB (|G|=8, 30 seq)  b={fit_r["f"]:.4f}, r_R={fit_r["r"]:.4f}')
ax.plot(ms_fine, model(ms_fine, fit_r['A'], fit_r['B'], fit_r['f']), '-', color='C1', alpha=0.7)

ax.errorbar(ms, F_re, yerr=s_re, fmt='^', color='C2', label=f'Real Clifford RB (|G|=8, 10 seq)  b={fit_re["f"]:.4f}, r_R={fit_re["r"]:.4f}')
ax.plot(ms_fine, model(ms_fine, fit_re['A'], fit_re['B'], fit_re['f']), '--', color='C2', alpha=0.7)

ax.set_xlabel('Sequence length m')
ax.set_ylabel('Average survival probability F(m)')
ax.set_title(f'Real vs Standard Randomized Benchmarking\n1-qubit, real-diagonal noise (X/2,Z/2), p={r["p_inject"]}')
ax.legend(loc='upper right', fontsize=8)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(here / 'report' / 'evidence' / 'rb_curves.png', dpi=140)
print('saved rb_curves.png')
