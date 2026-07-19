#!/usr/bin/env python3
"""Generate Fig: (a) LDOS of the 4 zero modes at corners, (b) eigenvalue spectrum,
(c) near-zero-mode count / gap vs spiral pitch g (topological -> trivial transition)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chatterjee2023_replication import build_H_sparse, nearzero_sparse, NORB
import scipy.sparse.linalg as spla

L = 24
# (a) LDOS of 4 near-zero modes + (b) spectrum
w, v = nearzero_sparse(L, L, g=0.2, k=20)
N = L * L
dens = np.zeros(N)
for c in range(4):
    psi = v[:, c].reshape(N, NORB)
    dens += np.sum(np.abs(psi) ** 2, axis=1)
dens = dens.reshape(L, L)

fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
im = ax[0].imshow(dens, origin="lower", cmap="inferno")
ax[0].set_title("(a) LDOS of 4 zero-modes (E~0)\nMajorana corner modes, g=0.2")
ax[0].set_xlabel("x"); ax[0].set_ylabel("y")
plt.colorbar(im, ax=ax[0], fraction=0.046)

idx = np.argsort(w)
ax[1].plot(np.abs(w[idx]), "o-", ms=4)
ax[1].axhline(0, color="k", lw=0.5)
ax[1].set_title("(b) |E| spectrum near gap (OBC)\n4 modes pinned to E~0")
ax[1].set_xlabel("state index (sorted by |E|)"); ax[1].set_ylabel("|E|")
ax[1].set_ylim(-0.01, max(np.abs(w)) * 1.1)

# (c) transition vs g
gs = [0.0, 0.1, 0.2, 0.4, 0.7, 0.85, 1.0, 1.2, 1.4]
nz, gaps = [], []
for g in gs:
    wg, _ = nearzero_sparse(L, L, g=g, k=12)
    nz.append(int(np.sum(np.abs(wg) < 1e-3)))
    gaps.append(float(np.sort(np.abs(wg))[4]))
ax2 = ax[2]
ax2.plot(gs, gaps, "s-", color="tab:blue", label="gap to 5th mode")
ax2.set_xlabel("spiral pitch g"); ax2.set_ylabel("gap to bulk (5th |E|)", color="tab:blue")
ax2b = ax2.twinx()
ax2b.plot(gs, nz, "o--", color="tab:red", label="# zero modes")
ax2b.set_ylabel("# near-zero modes", color="tab:red")
ax2.set_title("(c) topological -> trivial transition in g\n4 MCMs persist to g~0.7, gone by g~1.0")
ax2.axvline(0.9, color="gray", ls=":", lw=1)

plt.tight_layout()
out = "/Users/stevens/Dropbox/REPLICATE-PROJECT/TEXTURE-spin-chatterjee2023/figs/fig1_mcm_quadrupole.png"
plt.savefig(out, dpi=130)
print("saved", out)
