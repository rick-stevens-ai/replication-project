#!/usr/bin/env python3
"""
Replication of Šmejkal, Sinova, Jungwirth, arXiv:2204.10844
"Emerging research landscape of altermagnetism" (Perspective / foundational review)

REPLICATION TARGET (the reproducible core of a review):
  Reproduce the paper's central symmetry-classification claim + the representative
  altermagnet band model that underpins the whole Perspective:

  C1. Altermagnet = collinear compensated magnet with NONRELATIVISTIC spin-split bands
      whose splitting is even-parity (d-wave etc.) in momentum, with ZERO net moment.
      -> build a minimal d-wave altermagnet, show |M_net|=0 and a k-space spin
         splitting with d-wave nodes (Kramers degeneracy lifted at generic k, but
         restored on the nodal lines and by k -> C4 k combined with spin flip).

  C2. SYMMETRY CLASSIFICATION / IDENTIFICATION RULE (Sec II.B-C): the two spin
      sublattices are connected by a proper/improper ROTATION (not translation/
      inversion). This is what distinguishes altermagnet from conventional AFM.
      -> demonstrate that a rotation R_[C4] combined with spin flip is a symmetry
         (E_up(k) = E_dn(C4 k)), whereas translation/inversion is NOT the connecting
         op (E_up(k) != E_dn(k) generically and != E_dn(-k) distinction), so the
         classification rule holds numerically.

  C3. KRAMERS / NODES: the spin splitting Delta(k) has the d-wave form with sign
      changes and nodal lines (kx=+/-ky), so a BZ integral of Delta is zero
      (compensated) while local Delta != 0 (ferromagnet-like spin-split spectra).

  This is the "ferromagnetic-antiferromagnetic dichotomy" the abstract highlights.

CPU-only, numpy/scipy/matplotlib. Reuses the sasioglu2026 d-wave altermagnet TB template.
"""
import json, os, time
import numpy as np

t0 = time.time()
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(BASE, "work"); FIGS = os.path.join(BASE, "figs")
os.makedirs(WORK, exist_ok=True); os.makedirs(FIGS, exist_ok=True)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

t = 1.0; t_AM = 0.30   # spin-independent hop, altermagnetic anisotropic hop (units of t)

def E_spin(kx, ky, sigma):
    return -2*t*(np.cos(kx)+np.cos(ky)) - 2*sigma*t_AM*(np.cos(kx)-np.cos(ky))
def spin_split(kx, ky):
    return E_spin(kx,ky,+1) - E_spin(kx,ky,-1)     # = -4 t_AM (cos kx - cos ky), d-wave

N = 401
kk = np.linspace(-np.pi, np.pi, N)
KX, KY = np.meshgrid(kk, kk)
DELTA = spin_split(KX, KY)

# ---- C1: zero net moment, but locally spin split ----
net_split = np.mean(DELTA)                 # BZ average of spin splitting ~ 0 (compensated)
local_amp = np.max(np.abs(DELTA))          # local splitting large (ferromagnet-like)
# proxy net magnetization: filled-state spin imbalance at half filling (EF=0)
EF = 0.0
occ_up = (E_spin(KX,KY,+1) < EF).mean()
occ_dn = (E_spin(KX,KY,-1) < EF).mean()
net_moment = occ_up - occ_dn               # should be ~0 (compensated)

# ---- C2: symmetry classification / identification rule ----
# altermagnet connecting op = C4 rotation + spin flip:  E_up(k) == E_dn(C4 k)
# C4: (kx,ky) -> (-ky, kx)
Eup = E_spin(KX, KY, +1)
Edn_C4 = E_spin(-KY, KX, -1)               # E_dn evaluated at C4 k
c4_spinflip_residual = np.max(np.abs(Eup - Edn_C4))   # ~0 => C4+flip IS a symmetry
# conventional-AFM connecting ops that must FAIL for an altermagnet:
#   translation would give E_up(k)==E_dn(k); inversion E_up(k)==E_dn(-k)
transl_residual = np.max(np.abs(E_spin(KX,KY,+1) - E_spin(KX,KY,-1)))     # large => not translation-connected
inv_residual    = np.max(np.abs(E_spin(KX,KY,+1) - E_spin(-KX,-KY,-1)))   # d-wave is even => also ~0? check

# ---- C3: nodes on diagonals; sign-changing d-wave ----
diag = spin_split(kk, kk)                   # kx=ky -> node
diag_max = np.max(np.abs(diag))
antinode = spin_split(kk, np.zeros_like(kk))
antinode_amp = np.max(np.abs(antinode))
# count sign domains (d-wave has 4 lobes alternating sign around Gamma)
sgn = np.sign(DELTA)
# sample around a small circle to count sign changes = 4 for d-wave
th = np.linspace(0, 2*np.pi, 720, endpoint=False)
r = 0.6
circ = spin_split(r*np.cos(th), r*np.sin(th))
s = np.sign(circ)
s = s[s != 0]                               # drop exact zeros (nodes) before counting transitions
sign_changes = int(np.sum(np.diff(s) != 0))
sign_changes += int(s[0] != s[-1])          # wrap-around (circle is periodic)

print(f"[C1] BZ-avg splitting={net_split:.2e} (expect~0)  local max|Delta|={local_amp:.3f}  net_moment(half-fill)={net_moment:.2e}")
print(f"[C2] C4+spinflip residual={c4_spinflip_residual:.2e} (expect~0 => altermagnet rule holds)")
print(f"     translation residual={transl_residual:.3f} (expect large => NOT AFM-translation)")
print(f"     inversion residual={inv_residual:.2e}")
print(f"[C3] diagonal node max|Delta|={diag_max:.2e} (expect~0)  antinode amp={antinode_amp:.3f}  sign_changes_on_circle={sign_changes} (expect 4 => d-wave)")

# ---- figures ----
fig, ax = plt.subplots(1,2, figsize=(12,5))
im = ax[0].pcolormesh(KX,KY,DELTA,cmap="RdBu_r",shading="auto",vmin=-2.4,vmax=2.4)
ax[0].plot([-np.pi,np.pi],[-np.pi,np.pi],'k--',lw=.8); ax[0].plot([-np.pi,np.pi],[np.pi,-np.pi],'k--',lw=.8)
ax[0].set_title("d-wave altermagnet spin splitting\n(zero net moment, 4 alternating lobes)")
ax[0].set_xlabel("$k_x$"); ax[0].set_ylabel("$k_y$"); ax[0].set_aspect('equal')
fig.colorbar(im, ax=ax[0], label=r"$\Delta=E_\uparrow-E_\downarrow$")
ax[1].contour(KX,KY,Eup,levels=[EF],colors="red"); ax[1].contour(KX,KY,E_spin(KX,KY,-1),levels=[EF],colors="blue")
ax[1].set_title("Spin-split Fermi surfaces (EF=0)\nred=up blue=down (ferromagnet-like split)")
ax[1].set_xlabel("$k_x$"); ax[1].set_ylabel("$k_y$"); ax[1].set_aspect('equal')
plt.tight_layout(); plt.savefig(os.path.join(FIGS,"fig1_dwave_classification.png"),dpi=130); plt.close()

def claim(exp,rep,match,note): return {"expectation":exp,"reproduced":rep,"match":bool(match),"note":note}
results = {
  "paper":"Smejkal, Sinova, Jungwirth arXiv:2204.10844 (Emerging research landscape of altermagnetism)",
  "model":{"t":t,"t_AM":t_AM,"form":"Delta(k)=-4 t_AM (cos kx - cos ky) d-wave altermagnet"},
  "claims":{
    "C1_compensated_yet_spinsplit": claim(
      "Collinear compensated magnet: zero net magnetization but nonrelativistic spin-split bands.",
      {"BZ_avg_split":float(net_split),"net_moment_halffill":float(net_moment),"local_max_split":float(local_amp)},
      abs(net_split)<1e-6 and abs(net_moment)<1e-6 and local_amp>0.5,
      "M_net~0 (AFM-like) with large local spin splitting (FM-like) = the altermagnet dichotomy."),
    "C2_symmetry_classification": claim(
      "Spin sublattices connected by proper/improper ROTATION (C4+spin flip), not translation/inversion.",
      {"C4_spinflip_residual":float(c4_spinflip_residual),"translation_residual":float(transl_residual)},
      c4_spinflip_residual<1e-9 and transl_residual>0.5,
      "E_up(k)=E_dn(C4 k) holds exactly (rotation connects sublattices); translation does NOT => altermagnet identification rule."),
    "C3_dwave_nodes": claim(
      "Even-parity d-wave splitting: nodal lines on diagonals, 4 alternating-sign lobes, BZ-compensated.",
      {"diagonal_node_max":float(diag_max),"antinode_amp":float(antinode_amp),"sign_changes_on_circle":sign_changes},
      diag_max<1e-9 and sign_changes==4,
      "Nodes at kx=+/-ky, exactly 4 sign changes around Gamma => d-wave; local Delta!=0 but integrates to 0."),
  },
  "notes":"Review paper: reproduced its central symmetry-classification + representative d-wave model that anchors the Perspective. Material-specific DFT band structures (Sec II.A) are out of scope (no DFT).",
  "runtime_s":None,
}
results["runtime_s"]=round(time.time()-t0,2)
with open(os.path.join(WORK,"results.json"),"w") as f: json.dump(results,f,indent=2)
print(f"[done] {results['runtime_s']}s  verdict-signal: "
      f"C1={results['claims']['C1_compensated_yet_spinsplit']['match']} "
      f"C2={results['claims']['C2_symmetry_classification']['match']} "
      f"C3={results['claims']['C3_dwave_nodes']['match']}")
