"""Generate figures: (a) kagome band structure Gamma-K-M-Gamma (paper Fig 1c),
(b) Chern-vs-flux phase diagram (QAH claim)."""
import numpy as np
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from claim4_bands_vhs import Hk_paper
SQRT3 = np.sqrt(3.0)
WORK = os.path.join(os.path.dirname(__file__), "..", "work")

# ---- band structure along Gamma-K-M-Gamma ----
Gam = np.array([0.0, 0.0]); K = np.array([4*np.pi/3, 0.0])
M = np.array([np.pi, np.pi/SQRT3])
def path(p, q, n): return [p + (q-p)*t for t in np.linspace(0, 1, n)]
kpath = path(Gam, K, 100) + path(K, M, 100) + path(M, Gam, 100)
E = np.array([np.sort(np.linalg.eigvalsh(Hk_paper(k[0], k[1]))) for k in kpath])
x = np.arange(len(kpath))
plt.figure(figsize=(6, 4))
for b in range(3):
    plt.plot(x, E[:, b], lw=1.6)
plt.axhline(0, ls=':', c='gray', lw=0.8, label='vH (M) E=0')
plt.axhline(2.0, ls='--', c='r', lw=0.8, label='flat band +2t')
for xc in [0, 100, 200, 300]:
    plt.axvline(xc, c='k', lw=0.4, alpha=0.3)
plt.xticks([0, 100, 200, 300], [r'$\Gamma$', 'K', 'M', r'$\Gamma$'])
plt.ylabel('E / t'); plt.title('Kagome TB band structure (paper Fig.1c)')
plt.legend(fontsize=8); plt.tight_layout()
plt.savefig(os.path.join(WORK, "fig_bands.png"), dpi=140)
print("wrote fig_bands.png")

# ---- Chern vs flux ----
import json
with open(os.path.join(WORK, "claim2c_output.json")) as f:
    d = json.load(f)
phi = [t["phi"] for t in d["table"]]
C = [t["C"] for t in d["table"]]
gap = [t["gap"] for t in d["table"]]
fig, ax1 = plt.subplots(figsize=(6, 4))
ax1.step(phi, C, where='mid', color='b', lw=1.8, label='C (lowest band)')
ax1.set_xlabel(r'Peierls flux $\phi$'); ax1.set_ylabel('Chern number', color='b')
ax1.set_yticks([-1, 0, 1]); ax1.axhline(0, c='gray', lw=0.5)
ax2 = ax1.twinx()
ax2.plot(phi, gap, color='orange', lw=1.2, alpha=0.7, label='gap')
ax2.set_ylabel('band gap / t', color='orange')
plt.title('Nagaosa flux state: QAH phase diagram')
fig.tight_layout()
plt.savefig(os.path.join(WORK, "fig_chern_vs_flux.png"), dpi=140)
print("wrote fig_chern_vs_flux.png")
