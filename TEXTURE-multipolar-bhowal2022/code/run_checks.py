"""
Run the machine-checkable claims against the minimal TB model and write results
(JSON + figures) into ../work/.

Claims checked (see report/REPORT.tex for prose):

C1. NRSS EXISTS along Gamma->M with spin along z: the top-valence spin splitting
    Delta E_s(kx=ky) is non-zero and of order tens of meV.  (Paper Fig. 3d peak
    ~ -0.03 eV.)

C2. d-WAVE / C4 SIGN REVERSAL: Delta E_s changes sign under (kx,ky)->(kx,-ky),
    i.e. [110] vs [1-10].  Equivalently O32- recip rep kx*ky*mz changes sign.

C3. SYMMETRIC IN k (even), NOT Rashba-antisymmetric:
    Delta E_s(k) == Delta E_s(-k).

C4. OCTUPOLE-SPLITTING PROPORTIONALITY: the DFT-analog (exact-diag) splitting
    tracks the analytic octupole form (32/eps) t3 t4 sin(kx a) sin(ky a); and
    both vanish if the inter-sublattice hoppings t3 OR t4 -> 0.

C5. NO SPLITTING ON ZONE AXES: Delta E_s = 0 whenever kx=0 or ky=0 (Gamma->X,
    Gamma->Z), consistent with kx*ky*mz octupole node lines.
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import model as M
RY = M.RY_TO_EV

OUT = os.path.join(os.path.dirname(__file__), "..", "work")
os.makedirs(OUT, exist_ok=True)

results = {}


# ---- Gamma -> M path (kz=0), kx=ky from 0 to pi -------------------------------
N = 401
kline = np.linspace(0.0, np.pi, N)          # kx=ky along [110]; reduced units a=1
dEs_exact = np.array([M.spin_splitting_topvalence(k, k, 0.0) for k in kline])
dEs_appx = np.array([M.spin_splitting_approx(k, k, 0.0) for k in kline])
dEs_exact_ev = dEs_exact * RY
dEs_appx_ev = dEs_appx * RY

peak_idx = int(np.argmax(np.abs(dEs_exact_ev)))
results["C1_NRSS_exists"] = {
    "max_abs_split_eV": float(np.max(np.abs(dEs_exact_ev))),
    "peak_k_over_pi": float(kline[peak_idx] / np.pi),
    "paper_fig3d_peak_eV_approx": -0.03,
    "nonzero": bool(np.max(np.abs(dEs_exact_ev)) > 1e-3),
}

# ---- C2: C4 sign reversal [110] vs [1-10] ------------------------------------
k0 = np.pi / 3
dE_110 = M.spin_splitting_topvalence(k0, k0, 0.0)
dE_1m10 = M.spin_splitting_topvalence(k0, -k0, 0.0)
oct_110 = M.octupole_O32_recip(k0, k0)
oct_1m10 = M.octupole_O32_recip(k0, -k0)
results["C2_C4_sign_reversal"] = {
    "dEs_[110]_eV": float(dE_110 * RY),
    "dEs_[1-10]_eV": float(dE_1m10 * RY),
    "sign_flips": bool(np.sign(dE_110) == -np.sign(dE_1m10) and abs(dE_110) > 1e-6),
    "octupole_kxky_[110]": float(oct_110),
    "octupole_kxky_[1-10]": float(oct_1m10),
    "octupole_sign_flips": bool(np.sign(oct_110) == -np.sign(oct_1m10)),
}

# ---- C3: symmetric (even) in k -----------------------------------------------
kv = np.pi / 4
dE_p = M.spin_splitting_topvalence(kv, kv, 0.1)
dE_m = M.spin_splitting_topvalence(-kv, -kv, -0.1)
results["C3_even_in_k"] = {
    "dEs_(+k)_eV": float(dE_p * RY),
    "dEs_(-k)_eV": float(dE_m * RY),
    "even_symmetric": bool(abs(dE_p - dE_m) < 1e-12),
    "abs_diff_eV": float(abs(dE_p - dE_m) * RY),
}

# ---- C4: proportionality to octupole form + vanishing when t3 or t4 -> 0 -----
# correlation between exact splitting and analytic octupole form over the path
mask = np.abs(dEs_exact_ev) > 1e-9
corr = float(np.corrcoef(dEs_exact_ev[mask], dEs_appx_ev[mask])[0, 1])
# ratio of peak magnitudes
ratio = float(np.max(np.abs(dEs_appx_ev)) / np.max(np.abs(dEs_exact_ev)))

# turn off t4
dEs_t4off = np.array([M.spin_splitting_topvalence(k, k, 0.0, t4=0.0) for k in kline]) * RY
dEs_t3off = np.array([M.spin_splitting_topvalence(k, k, 0.0, t3=0.0) for k in kline]) * RY
results["C4_octupole_proportional"] = {
    "pearson_r_exact_vs_analytic": corr,
    "peak_ratio_analytic_over_exact": ratio,
    "max_abs_split_t4_off_eV": float(np.max(np.abs(dEs_t4off))),
    "max_abs_split_t3_off_eV": float(np.max(np.abs(dEs_t3off))),
    "vanishes_without_intersublattice_hopping": bool(
        np.max(np.abs(dEs_t4off)) < 1e-6 and np.max(np.abs(dEs_t3off)) < 1e-6),
}

# ---- C5: node lines kx=0 or ky=0 ---------------------------------------------
dE_GX = np.array([M.spin_splitting_topvalence(k, 0.0, 0.0) for k in kline]) * RY  # Gamma->X
dE_GZ = np.array([M.spin_splitting_topvalence(0.0, 0.0, k) for k in kline]) * RY  # Gamma->Z
results["C5_node_lines"] = {
    "max_abs_split_Gamma_to_X_eV": float(np.max(np.abs(dE_GX))),
    "max_abs_split_Gamma_to_Z_eV": float(np.max(np.abs(dE_GZ))),
    "zero_on_axes": bool(np.max(np.abs(dE_GX)) < 1e-9 and np.max(np.abs(dE_GZ)) < 1e-9),
}

# ---- provenance --------------------------------------------------------------
results["_meta"] = {
    "paper": "Bhowal & Spaldin, arXiv:2212.03756 (=2205.09500), PRX 2024",
    "system": "rutile MnF2 (NRSS altermagnetic AFM)",
    "model": "8-band spinful TB, Eqs.(2)-(6), Table I params (Ry)",
    "params_Ry": dict(t1=M.T1, t2=M.T2, t3=M.T3, t4=M.T4, e1=M.E1, e2=M.E2),
    "J_Ry": M.J_RY, "2J_eV": M.TWO_J_EV, "Ry_to_eV": RY,
}

with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

# ---- Figure 1: reproduce Fig. 3(d) style comparison --------------------------
plt.figure(figsize=(6, 4))
xx = kline / np.pi
plt.plot(xx, dEs_exact_ev, "b-", lw=2, label=r"exact diag $\Delta E_s$ (Eq. 4/5)")
plt.plot(xx, dEs_appx_ev, "r--", lw=1.5, label=r"analytic Eq. (6): $\frac{32}{\epsilon}t_3t_4\sin k_x\sin k_y$")
plt.axhline(0, color="k", lw=0.5)
plt.xlabel(r"$k$ along $\Gamma\to M$  ($k_x=k_y$, units of $\pi/a$)")
plt.ylabel(r"$\Delta E_s$ (eV)")
plt.title(r"MnF$_2$ NRSS: top-valence spin splitting (cf. paper Fig. 3d)")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_spin_splitting_GM.png"), dpi=140)
plt.close()

# ---- Figure 2: d-wave map of octupole rep / splitting over kx,ky plane -------
kg = np.linspace(-np.pi, np.pi, 241)
KX, KY = np.meshgrid(kg, kg)
DE = np.vectorize(lambda a, b: M.spin_splitting_topvalence(a, b, 0.0))(KX, KY) * RY
plt.figure(figsize=(5.4, 4.6))
vmax = np.max(np.abs(DE))
im = plt.pcolormesh(KX / np.pi, KY / np.pi, DE, cmap="RdBu_r", vmin=-vmax, vmax=vmax, shading="auto")
plt.colorbar(im, label=r"$\Delta E_s$ (eV)")
plt.xlabel(r"$k_x\ (\pi/a)$"); plt.ylabel(r"$k_y\ (\pi/a)$")
plt.title(r"$d$-wave NRSS $\propto k_xk_y m_z$ (O$_{32}^-$ octupole rep)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_dwave_map.png"), dpi=140)
plt.close()

print(json.dumps(results, indent=2))
