#!/usr/bin/env python
"""Re-pass companion figures: phase-shift null distributions vs observed."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
F3 = HERE.parent.parent / "data" / "15yr_stochastic_analysis" / "data_release" / "figure_3"
OUT = HERE.parent.parent / "figures" / "repass"
OUT.mkdir(parents=True, exist_ok=True)

bfs = np.load(F3 / "pshift_bfs.npy")
oss = np.load(F3 / "pshift_optstat.npy")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

# Left: BF null distribution
ax = axes[0]
ax.hist(np.log10(np.clip(bfs, 1e-6, None)), bins=80, color="steelblue", alpha=0.7)
for v, c, lab in [(np.log10(200), "C3", "obs BF=200 (14 freq)"),
                  (np.log10(1000), "C1", "obs BF=1000 (5 freq)")]:
    ax.axvline(v, color=c, linestyle="--", lw=1.8, label=lab)
ax.set_xlabel(r"$\log_{10}\,\mathrm{BF}_{HD/CURN}$ under phase-shift null")
ax.set_ylabel("count")
ax.set_title("Bayesian phase-shift null (n=5097)")
ax.legend(fontsize=9)

# Right: OS S/N null distribution
ax = axes[1]
ax.hist(oss, bins=80, color="darkorange", alpha=0.7)
for v, c, lab in [(4.0, "C0", "obs S/N=4 (curn_13/3)"),
                  (5.0, "C3", "obs S/N=5 (curn_gamma)")]:
    ax.axvline(v, color=c, linestyle="--", lw=1.8, label=lab)
ax.set_xlabel("HD optimal-statistic S/N under phase-shift null")
ax.set_ylabel("count")
ax.set_yscale("log")
ax.set_title("Optimal-statistic phase-shift null (n=400,000)")
ax.legend(fontsize=9)

fig.suptitle("Re-pass: empirical p-values for HD detection (NANOGrav 15yr)", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "phase_shift_null_distributions.png", dpi=130, bbox_inches="tight")
print(f"wrote {OUT / 'phase_shift_null_distributions.png'}")

# Spline ORF plot
import la_forge.core as co
TC = HERE.parent.parent / "data" / "15yr_stochastic_analysis" / "tutorials" / "presampled_cores"
core = co.Core(corepath=str(TC / "spline_orf_vg.core"))
ps = list(core.params)
pos = np.array([1e-3, 25, 49.3, 82.5, 121.8, 150, 180])
fig2, ax = plt.subplots(figsize=(7.5, 4.2))

# HD reference
def hd(xi_deg):
    xi = np.deg2rad(np.asarray(xi_deg))
    x = (1 - np.cos(xi)) / 2.0
    x = np.where(x < 1e-12, 1e-12, x)
    return 1.5 * x * np.log(x) - 0.25 * x + 0.5
xx = np.linspace(0.01, 180, 500)
ax.plot(xx, hd(xx), "k--", lw=1.4, label="HD theory")
ax.axhline(0, color="k", lw=0.5)

cols = [core.chain[:, ps.index(f"gw_orf_spline_{i}")] for i in range(7)]
parts = ax.violinplot(cols, positions=pos, widths=14.0, showextrema=False)
for pc in parts["bodies"]:
    pc.set_facecolor("steelblue"); pc.set_alpha(0.45); pc.set_edgecolor("steelblue")
# Mark HD zero crossings
for xc in [49.3, 121.8]:
    ax.axvline(xc, color="red", ls=":", lw=0.8, alpha=0.6)
ax.text(49.3, -0.35, "HD zero", color="red", fontsize=8, ha="center")
ax.text(121.8, -0.35, "HD zero", color="red", fontsize=8, ha="center")

ax.set_xlabel(r"separation angle $\xi_{ab}$ [deg]")
ax.set_ylabel(r"$\Gamma(\xi_{ab})$")
ax.set_title("Spline ORF (re-pass) — HD overlay + zero-crossings")
ax.set_xlim(-5, 185)
ax.set_ylim(-0.4, 1.0)
ax.legend(loc="upper right", fontsize=9)
fig2.tight_layout()
fig2.savefig(OUT / "spline_orf_repass.png", dpi=130, bbox_inches="tight")
print(f"wrote {OUT / 'spline_orf_repass.png'}")

# fref decorrelation
import la_forge.core as co2
core2 = co2.Core(corepath=str(TC / "hd_14f_pl_vg.core"))
ps2 = list(core2.params)
la = core2.chain[:, ps2.index("gw__log10_A")]
gm = core2.chain[:, ps2.index("gw__gamma")]
fref_grid = np.logspace(-1.7, 0.7, 41)
corrs = []
for fr in fref_grid:
    delta = 0.5 * (3 - gm) * np.log10(fr / 1.0)
    la_n = la + delta
    corrs.append(np.corrcoef(la_n, gm)[0, 1])

fig3, ax3 = plt.subplots(figsize=(7, 4))
ax3.plot(fref_grid, corrs, "o-", color="steelblue")
ax3.axhline(0, color="k", lw=0.6)
ax3.axvline(1.0, color="C1", ls="--", lw=1.2, label=r"$f_\mathrm{ref}=1/$yr (paper default)")
ax3.axvline(0.1, color="C2", ls="--", lw=1.2, label=r"$f_\mathrm{ref}=0.1/$yr (paper Fig. 1)")
ax3.set_xscale("log")
ax3.set_xlabel(r"$f_\mathrm{ref}$ [1/yr]")
ax3.set_ylabel(r"$\mathrm{corr}(\log_{10}A,\gamma)$")
ax3.set_title("Re-pass: A-gamma correlation vs reference frequency (hd_14f_pl_vg)")
ax3.legend(fontsize=9, loc="lower right")
ax3.grid(alpha=0.3)
fig3.tight_layout()
fig3.savefig(OUT / "fref_decorrelation_repass.png", dpi=130, bbox_inches="tight")
print(f"wrote {OUT / 'fref_decorrelation_repass.png'}")
