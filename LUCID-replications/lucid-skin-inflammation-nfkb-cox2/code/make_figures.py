"""
Reproduce / overlay the digitized values from Acheva et al. 2017 with our
4PL fits for Figure 2 and our recomputed fold-change for Figure 7.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from digitized_figures import (
    FIG1_SHIELDED, FIG1_IRRADIATED,
    FIG2A_SC236, FIG2B_BAY,
    FIG7A_CTRL, FIG7A_2GY,
)
from replicate_stats import fit_mtt, four_param_logistic

FIG_OUT = Path(__file__).resolve().parent.parent / "figures"
FIG_OUT.mkdir(parents=True, exist_ok=True)


def fig1_overlay():
    labels = [b.label for b in FIG1_SHIELDED]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    w = 0.38
    sh_means = [b.mean for b in FIG1_SHIELDED]
    sh_sems  = [b.sem  for b in FIG1_SHIELDED]
    ir_means = [b.mean for b in FIG1_IRRADIATED]
    ir_sems  = [b.sem  for b in FIG1_IRRADIATED]
    ax.bar(x - w/2, sh_means, w, yerr=sh_sems, capsize=3,
           label="2 Gy, Shielded", color="#bcbddc")
    ax.bar(x + w/2, ir_means, w, yerr=ir_sems, capsize=3,
           label="2 Gy, Irradiated", color="#54278f")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("COX-2 mRNA, rel. expression (2$^{-\\Delta\\Delta C_T}$, 18S ref)")
    ax.set_title("Spot-check of Fig 1: digitized COX-2 mRNA values + recomputed Tukey HSD")
    ax.axhline(1.0, color="k", lw=0.5, ls="--")
    ax.legend()
    fig.tight_layout()
    out = FIG_OUT / "fig1_digitized_overlay.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def fig2_overlay():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, bars, name, working in [
        (axes[0], FIG2A_SC236, "sc-236",      5.0),
        (axes[1], FIG2B_BAY,   "Bay 11-7085", 1.0),
    ]:
        # data
        xs = [float(b.label) if b.label.replace(".", "", 1).isdigit() else None for b in bars]
        ys = [b.mean for b in bars]
        es = [b.sem  for b in bars]
        keep = [i for i, v in enumerate(xs) if v is not None]
        xs_n = np.array([xs[i] for i in keep])
        ys_n = np.array([ys[i] for i in keep])
        es_n = np.array([es[i] for i in keep])
        ax.errorbar(xs_n, ys_n, yerr=es_n, fmt="o", color="k",
                    label="Digitized data")
        # 4PL fit
        fit = fit_mtt(bars, name)
        xx = np.geomspace(max(min(xs_n[xs_n > 0])/3, 1e-3), max(xs_n)*1.5, 200)
        yy = four_param_logistic(xx, fit["fit_top"], fit["fit_bottom"],
                                 fit["fit_IC50_uM"], fit["fit_hill"])
        ax.plot(xx, yy, "-", label=f"4PL fit  IC50={fit['fit_IC50_uM']:.2f} uM")
        ax.axvline(working, color="r", ls=":",
                   label=f"Authors' working conc {working} uM")
        ax.set_xscale("symlog", linthresh=0.5)
        ax.set_xlabel(f"{name}, [µmol/l]")
        ax.set_ylabel("% viability vs control")
        ax.set_title(f"Fig 2 spot-check — {name}")
        ax.set_ylim(0, 115)
        ax.legend(fontsize=8)
    fig.tight_layout()
    out = FIG_OUT / "fig2_dose_response_fits.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def fig7_overlay():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    t = np.array([0, 24, 48, 72])
    ctrl = np.array([b.mean for b in FIG7A_CTRL])
    ctrl_e = np.array([b.sem for b in FIG7A_CTRL])
    irr  = np.array([b.mean for b in FIG7A_2GY])
    irr_e  = np.array([b.sem for b in FIG7A_2GY])
    ax.errorbar(t - 1, ctrl, yerr=ctrl_e, fmt="o-", label="Control")
    ax.errorbar(t + 1, irr,  yerr=irr_e,  fmt="s-", label="2 Gy", color="C3")
    ax.annotate(f"6.4x baseline (paper claim: 6.5x)",
                xy=(72, 1600), xytext=(40, 1800),
                arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel("Time post-irradiation (h)")
    ax.set_ylabel("PGE2 (pg/ml)")
    ax.set_title("Fig 7 spot-check — PGE2 ELISA, digitized")
    ax.set_ylim(0, 2100)
    ax.legend()
    fig.tight_layout()
    out = FIG_OUT / "fig7_pge2_overlay.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main():
    outs = [fig1_overlay(), fig2_overlay(), fig7_overlay()]
    for o in outs:
        print("wrote", o)


if __name__ == "__main__":
    main()
