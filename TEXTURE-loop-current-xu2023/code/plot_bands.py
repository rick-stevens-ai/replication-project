"""Plot single-magnon bands along Gamma-M-K-Gamma for representative points,
including the flat-band-on-boundary case. Writes ../work/magnon_bands.png."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from magnon_su3_kagome import magnon_bands, B1, B2, SQRT3

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work")

Gamma = np.array([0.0, 0.0])
M = 0.5 * B1
K = np.array([2*np.pi/3, -2*np.pi/SQRT3])

def path(pts, n=120):
    seg = []
    for a, b in zip(pts[:-1], pts[1:]):
        for t in np.linspace(0, 1, n, endpoint=False):
            seg.append(a + t*(b-a))
    seg.append(pts[-1])
    return np.array(seg)

kp = path([Gamma, M, K, Gamma])

cases = [
    ("stable FM  (J+KR=-1.2, KI=1.0)", -1.2, 1.0),
    ("boundary   (J+KR=-1/sqrt3, KI=1.0)", -1.0/SQRT3, 1.0),
    ("unstable   (J+KR=0.5, KI=0.3)", 0.5, 0.3),
]

fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=False)
for ax, (title, x, KI) in zip(axes, cases):
    bands = np.array([magnon_bands(k[0], k[1], x, KI) for k in kp])
    for b in range(3):
        ax.plot(bands[:, b], lw=1.5)
    ax.axhline(0, color="k", ls=":", lw=0.8)
    ax.set_title(title, fontsize=9)
    ax.set_xticks([0, 120, 240, 360])
    ax.set_xticklabels([r"$\Gamma$", "M", "K", r"$\Gamma$"])
    ax.set_ylabel("magnon energy (from FM)")
fig.suptitle("Single-magnon bands, Eq. A1  (Xu et al. arXiv:2306.16192)", fontsize=11)
fig.tight_layout()
out = os.path.join(WORK, "magnon_bands.png")
fig.savefig(out, dpi=130)
print("wrote", out)

# Chiral hexagon-mode phase check on the boundary flat band:
# paper states hexagon modes carry amplitudes e^{i j pi/3}. We probe the
# flat-band eigenvector's inter-sublattice phase winding at a generic k.
x, KI = -1.0/SQRT3, 1.0
kx, ky = 0.37, 0.11
from magnon_su3_kagome import magnon_matrix
w, V = np.linalg.eigh(magnon_matrix(kx, ky, x, KI))
lo = V[:, 0]
phases = np.angle(lo[1:]/lo[0]) if abs(lo[0]) > 1e-9 else np.angle(lo)
print("flat-band eigenvalue:", round(float(w[0]), 12))
print("flat-band inter-sublattice phases (rad):", np.round(phases, 4),
      " (~pi/3 multiples =", np.round(phases/(np.pi/3), 3), "x pi/3)")
