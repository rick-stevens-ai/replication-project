#!/usr/bin/env python3
"""Generate scaling plot for the BHT replication."""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / 'bht_results.json') as f:
    R = json.load(f)

rows = R['rows']
Ns = np.array([r['N'] for r in rows])
bht = np.array([r['bht_mean_total_queries'] for r in rows])
cls_ = np.array([r['classical_mean_queries'] for r in rows])
cbr = np.array([r['N_cuberoot'] for r in rows])
sqr = np.array([r['N_sqrt'] for r in rows])

# Fit slopes on the "asymptotic" range N>=64 (drop tiny-N noise)
mask = Ns >= 64
def fit(x, y, m):
    lx, ly = np.log(x[m]), np.log(y[m])
    s, i = np.polyfit(lx, ly, 1)
    return s, i
sb, ib = fit(Ns, bht, mask)
sc, ic = fit(Ns, cls_, mask)
sb_all, _ = fit(Ns, bht, np.ones_like(Ns, dtype=bool))
sc_all, _ = fit(Ns, cls_, np.ones_like(Ns, dtype=bool))

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.loglog(Ns, cls_, 'o-', color='C3', label=f'Classical birthday attack  (fit slope N≥64 = {sc:.2f}, expected 0.500)')
ax.loglog(Ns, bht, 's-', color='C0', label=f'BHT quantum (real Qiskit)  (fit slope N≥64 = {sb:.2f}, expected 0.333)')
# Reference lines
ax.loglog(Ns, 1.15 * sqr, 'k--', alpha=0.4, label=r'$1.15\sqrt{N}$  reference')
ax.loglog(Ns, 1.7 * cbr, 'k:',  alpha=0.4, label=r'$1.7\,N^{1/3}$  reference')

ax.set_xlabel('Domain size N')
ax.set_ylabel('Mean function evaluations (queries)')
ax.set_title('BHT Collision-finding — real Qiskit statevector Grover step\n'
             'arXiv:quant-ph/9705002 (Brassard, Høyer, Tapp 1997)')
ax.grid(True, which='both', ls='-', alpha=0.3)
ax.legend(loc='upper left', fontsize=9)
fig.tight_layout()
out = HERE / 'bht_scaling.png'
fig.savefig(out, dpi=140)
print(f"Wrote {out}")
print(f"BHT fit (all N)     slope = {sb_all:.3f}")
print(f"BHT fit (N>=64)     slope = {sb:.3f}")
print(f"Classical (all N)   slope = {sc_all:.3f}")
print(f"Classical (N>=64)   slope = {sc:.3f}")
