"""
run_analysis.py — verify the machine-checkable claims of Gmitra et al. (2013)
and generate SOF-texture figures. Writes results/metrics.json and figs/*.png.

Machine-checkable claims tested:
  C1. Extraction round-trip: the symmetry formulas Eqs.(4-9) recover the input
      (alpha,beta) from model bands to high precision (method self-consistency).
  C2. alpha_1(theta) changes SIGN as magnetization rotates (magnetic control).
  C3. alpha_1*beta_1 flips sign between [1-10] (theta=0) and [110] (theta=pi/2)
      => flip of SOF symmetry axes; band n=2 product does NOT flip sign.
  C4. SOF magnitude near Gamma scales linearly with k (|w| ~ k); higher contours
      show the anisotropic "butterfly" (non-circular polar |w|/k).
  C5. Angular dependence is a pure cos(2theta) (C2v): the reconstructed
      alpha_n(theta),beta_n(theta) equal Table I Eqs.(10-11) exactly by
      construction, and their amplitude ordering matches the paper's statement
      that band n=1 is more magnetization-sensitive than n=2 (|B1|>|B2|... in
      the relevant ratio sense).
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sof_model as m

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIGS = os.path.join(ROOT, "figs")
RES = os.path.join(ROOT, "results")
os.makedirs(FIGS, exist_ok=True)
os.makedirs(RES, exist_ok=True)

metrics = {}

# --------------------------------------------------------------------------
# C1. Extraction round-trip (Eqs. 4-9)
# --------------------------------------------------------------------------
rng = np.random.default_rng(0)
thetas_test = np.array([0.3, 0.7, 1.0, 1.3, 2.0, 2.5, 3.0, 4.0, 5.0])
max_err_ab = 0.0
max_err_wxy = 0.0
for n in (1, 2, 3, 4):
    for th in thetas_test:
        a_true, b_true = m.alpha_beta(n, th)
        a_ext, b_ext = m.extract_alpha_beta(th, a_true, b_true)
        max_err_ab = max(max_err_ab, abs(a_ext - a_true), abs(b_ext - b_true))
        # w_xy extraction at a finite k
        kx, ky = 0.02, 0.013
        wx_t, wy_t = m.sof_linear(kx, ky, a_true, b_true)
        wx_e, wy_e = m.extract_wxy(kx, ky, th, a_true, b_true)
        max_err_wxy = max(max_err_wxy, abs(wx_e - wx_t), abs(wy_e - wy_t))

metrics["C1_extraction_roundtrip"] = {
    "max_abs_err_alpha_beta_meVA": float(max_err_ab),
    "max_abs_err_wxy_meV": float(max_err_wxy),
    "tolerance_meVA": 1e-6,
    "pass": bool(max_err_ab < 1e-6 and max_err_wxy < 1e-9),
    "note": "Eqs.(4-9) recover input alpha,beta and w_x,w_y from model bands.",
}

# --------------------------------------------------------------------------
# C2 & C3. Sign change of alpha_1(theta) and product sign flip
# --------------------------------------------------------------------------
th = np.linspace(0, 2 * np.pi, 2001)
a1, b1 = m.alpha_beta(1, th)
a2, b2 = m.alpha_beta(2, th)

a1_min, a1_max = float(a1.min()), float(a1.max())
alpha1_sign_change = bool(a1_min < 0 < a1_max)

# products at the two crystallographic axes
def ab_at(n, angle):
    a, b = m.alpha_beta(n, angle)
    return float(a), float(b)

a1_0, b1_0 = ab_at(1, 0.0)          # [1-10]
a1_90, b1_90 = ab_at(1, np.pi / 2)  # [110]
a2_0, b2_0 = ab_at(2, 0.0)
a2_90, b2_90 = ab_at(2, np.pi / 2)

p1_0, p1_90 = a1_0 * b1_0, a1_90 * b1_90
p2_0, p2_90 = a2_0 * b2_0, a2_90 * b2_90

metrics["C2_alpha1_sign_change"] = {
    "alpha1_min_meVA": a1_min,
    "alpha1_max_meVA": a1_max,
    "changes_sign": alpha1_sign_change,
    "pass": alpha1_sign_change,
}
metrics["C3_product_sign_flip"] = {
    "band1": {"alpha_beta_at_[1-10]": p1_0, "alpha_beta_at_[110]": p1_90,
              "flips_sign": bool(p1_0 * p1_90 < 0)},
    "band2": {"alpha_beta_at_[1-10]": p2_0, "alpha_beta_at_[110]": p2_90,
              "flips_sign": bool(p2_0 * p2_90 < 0)},
    "pass": bool((p1_0 * p1_90 < 0) and not (p2_0 * p2_90 < 0)),
    "note": "Paper: band1 product flips sign (axis flip); band2 does not.",
}

# --------------------------------------------------------------------------
# C4. Linear-in-k scaling near Gamma + anisotropy (butterfly) on larger contour
# d = 3.997 A (diagonal spacing). Contours k = pi/(100 d), pi/(8 d), pi/(5 d).
# --------------------------------------------------------------------------
d = 3.997
kcontours = {"pi/100d": np.pi / (100 * d),
             "pi/8d": np.pi / (8 * d),
             "pi/5d": np.pi / (5 * d)}
phi = np.linspace(0, 2 * np.pi, 720)

# linearity: |w| at two small radii should scale linearly => |w|/k constant vs k
th_probe = 0.0  # [1-10]
a, b = m.alpha_beta(1, th_probe)
k_small = np.array([1e-4, 2e-4, 4e-4])
wovk = []
for k in k_small:
    wovk.append(np.mean([m.sof_magnitude_linear(k, p, a, b) for p in phi]))
wovk = np.array(wovk)
lin_dev = float(np.max(np.abs(wovk - wovk[0])) / abs(wovk[0]))
metrics["C4_linear_scaling"] = {
    "mean_|w|/k_at_k(1e-4,2e-4,4e-4)": wovk.tolist(),
    "relative_deviation": lin_dev,
    "pass": bool(lin_dev < 1e-9),
    "note": "In the linear regime |w|/k is k-independent (const polar radius).",
}

# anisotropy metric: ratio max/min of |w|/k around a contour (1 = isotropic)
def anisotropy(n, theta, k):
    a, b = m.alpha_beta(n, theta)
    r = np.array([m.sof_magnitude_linear(k, p, a, b) for p in phi])
    return float(r.max() / r.min())

aniso_110bar = anisotropy(1, 0.0, kcontours["pi/8d"])
aniso_110 = anisotropy(1, np.pi / 2, kcontours["pi/8d"])
metrics["C4_anisotropy"] = {
    "band1_theta=[1-10]_maxmin_ratio": aniso_110bar,
    "band1_theta=[110]_maxmin_ratio": aniso_110,
    "pass": bool(aniso_110bar > 1.05 or aniso_110 > 1.05),
    "note": "Non-unit max/min ratio => anisotropic SOF texture (butterfly).",
}

# --------------------------------------------------------------------------
# C5. Pure cos(2theta) C2v angular form + band1>band2 sensitivity
# relative angular modulation amplitude |B/A|
# --------------------------------------------------------------------------
def mod_amp(n):
    Ap, Bp, Am, Bm = m.TABLE_I[n]
    return abs(Bp / Ap), abs(Bm / Am)

b1_alpha_mod, b1_beta_mod = mod_amp(1)
b2_alpha_mod, b2_beta_mod = mod_amp(2)
metrics["C5_C2v_angular"] = {
    "band1_alpha_|B/A|": b1_alpha_mod, "band1_beta_|B/A|": b1_beta_mod,
    "band2_alpha_|B/A|": b2_alpha_mod, "band2_beta_|B/A|": b2_beta_mod,
    "band1_more_sensitive_than_band2": bool(b1_alpha_mod > b2_alpha_mod),
    "pass": bool(b1_alpha_mod > b2_alpha_mod),
    "note": "Paper: band1 alpha angular dependence much stronger than band2.",
}

# --------------------------------------------------------------------------
# FIGURES
# --------------------------------------------------------------------------
# Fig A: alpha_n(theta), beta_n(theta)  (reproduces Fig.3 structure at E=0)
fig, axs = plt.subplots(2, 2, figsize=(9, 6))
thd = np.degrees(th)
axs[0, 0].plot(thd, a1); axs[0, 0].set_title(r"$\alpha_1(\theta)$ [meV$\AA$]")
axs[0, 0].axhline(0, color="k", lw=0.5)
axs[0, 1].plot(thd, b1, "r"); axs[0, 1].set_title(r"$\beta_1(\theta)$ [meV$\AA$]")
axs[1, 0].plot(thd, a2); axs[1, 0].set_title(r"$\alpha_2(\theta)$ [meV$\AA$]")
axs[1, 1].plot(thd, b2, "r"); axs[1, 1].set_title(r"$\beta_2(\theta)$ [meV$\AA$]")
for ax in axs.flat:
    ax.set_xlabel(r"$\theta$ (deg)"); ax.set_xlim(0, 360); ax.grid(alpha=0.3)
fig.suptitle("SOC parameters vs magnetization angle (E=0), Table I / Eqs.(10-11)")
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "fig3_soc_vs_theta.png"), dpi=130)
plt.close(fig)

# Fig B: SOF "butterfly" vector fields + polar |w|/k, band n=1, two thetas, 3 contours
fig, axs = plt.subplots(3, 2, figsize=(8, 11), subplot_kw={})
labels = list(kcontours.items())
for row, (kname, kval) in enumerate(labels):
    for col, (thlab, thval) in enumerate([("[1-10]", 0.0), ("[110]", np.pi / 2)]):
        ax = axs[row, col]
        a, b = m.alpha_beta(1, thval)
        pp = np.linspace(0, 2 * np.pi, 48)
        kx = kval * np.cos(pp); ky = kval * np.sin(pp)
        wx, wy = m.sof_linear(kx, ky, a, b)
        # normalize arrow lengths (paper rescales) but keep direction
        norm = np.hypot(wx, wy); norm[norm == 0] = 1
        ax.quiver(np.cos(pp), np.sin(pp), wx / norm, wy / norm,
                  norm, cmap="viridis", scale=25, width=0.006)
        ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
        ax.set_title(f"n=1  k={kname}  M||{thlab}", fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("SOF 'butterflies' w(k) on Gamma-centered contours (Fig.2)")
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "fig2_sof_butterflies.png"), dpi=130)
plt.close(fig)

# Fig C: polar |w|/k for band1 at the two magnetizations, largest contour
fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(6, 6))
for thval, lab, c in [(0.0, "M||[1-10]", "C0"), (np.pi / 2, "M||[110]", "C3")]:
    a, b = m.alpha_beta(1, thval)
    r = np.array([m.sof_magnitude_linear(kcontours["pi/5d"], p, a, b) for p in phi])
    ax.plot(phi, r, c, label=lab)
ax.set_title(r"$|w|/k$ polar (band 1, k=$\pi/5d$)")
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "fig2_polar_wk.png"), dpi=130)
plt.close(fig)

# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------
passes = [v.get("pass") for k, v in metrics.items() if isinstance(v, dict) and "pass" in v]
metrics["_summary"] = {
    "n_claims_checked": len(passes),
    "n_pass": int(sum(bool(p) for p in passes)),
    "all_pass": bool(all(passes)),
}

with open(os.path.join(RES, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

print(json.dumps(metrics["_summary"], indent=2))
for k, v in metrics.items():
    if isinstance(v, dict) and "pass" in v:
        print(f"  {k}: {'PASS' if v['pass'] else 'FAIL'}")
