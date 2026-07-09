"""Reproduce the central claims of Friedrich 2012 (RR2964) using the static
GLOBLE model in globle_static.py.

Figures produced:

  fig1_dose_response_RT112.png
      RT112 -ln(S) vs dose, showing low-dose LQ behaviour and high-dose
      transition to a straight (exponential-in-D) line.  Compares static
      GLOBLE to the LQ approximation S = exp(-(alpha D + beta D^2)).

  fig2_alpha_beta_anticorr.png
      Beta vs alpha for the 17 cell lines in the catalogue (LQ-equivalent
      from GLOBLE).  Reproduces the paper's "intrinsic anti-correlation"
      between beta and alpha that the model predicts.

  fig3_class_decomposition_RT112.png
      Decomposition of -ln(S) into isolated-DSB vs clustered-DSB
      contributions, illustrating that the high-dose linear regime is driven
      by the clustered class.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from globle_static import (
    CELL_LINES, ALPHA_DSB, N_L,
    survival, lq_survival, damage_classes,
)


FIG_DIR = Path(__file__).resolve().parent.parent / "figures"
RES_DIR = Path(__file__).resolve().parent.parent / "results"
FIG_DIR.mkdir(exist_ok=True)
RES_DIR.mkdir(exist_ok=True)


def fig1_dose_response(name: str = "RT112") -> None:
    p = CELL_LINES[name]
    doses = np.linspace(0.01, 20.0, 400)
    s_globle = np.array([survival(p, d) for d in doses])
    s_lq     = np.array([lq_survival(p.alpha_lq, p.beta_lq, d) for d in doses])

    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(doses, -np.log(s_globle), label="static GLOBLE (Friedrich 2012)", lw=2)
    ax.plot(doses, -np.log(s_lq),     label=f"LQ small-D limit  α={p.alpha_lq:.3f}, β={p.beta_lq:.4f}",
            lw=1.4, ls="--")
    # Asymptotic high-dose linear tangent
    slope = p.eps_c * ALPHA_DSB
    intercept = -math.log(survival(p, 18.0)) - slope * 18.0
    ax.plot(doses, slope * doses + intercept, label=f"high-D asymptote slope={slope:.3f}/Gy",
            lw=1.0, ls=":", color="k")
    ax.set_xlabel("Photon dose D (Gy)")
    ax.set_ylabel("-ln S(D)")
    ax.set_title(f"Friedrich 2012 static GLOBLE — {name}")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "fig1_dose_response_RT112.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"  wrote {out}")


def fig2_alpha_beta_anticorr() -> None:
    alphas = np.array([p.alpha_lq for p in CELL_LINES.values()])
    betas  = np.array([p.beta_lq  for p in CELL_LINES.values()])
    a_over_b = alphas / betas        # paper's preferred axis (Eq. relating LQ ratio)
    names  = list(CELL_LINES.keys())

    try:
        from scipy.stats import spearmanr
        rho_ab, _ = spearmanr(alphas, betas)
        rho_aab, _ = spearmanr(alphas, a_over_b)
    except Exception:
        rho_ab = rho_aab = float("nan")
    r_ab = float(np.corrcoef(alphas, betas)[0, 1])
    r_aab = float(np.corrcoef(alphas, a_over_b)[0, 1])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    ax = axes[0]
    ax.scatter(alphas, betas, c="C3", zorder=3)
    for x, y, n in zip(alphas, betas, names):
        ax.annotate(n, (x, y), fontsize=7, xytext=(3, 2), textcoords="offset points")
    ax.set_xlabel("alpha (LQ-equivalent) [/Gy]")
    ax.set_ylabel("beta (LQ-equivalent) [/Gy^2]")
    ax.set_title(f"β vs α  (Pearson r={r_ab:.2f}, Spearman ρ={rho_ab:.2f})")
    ax.grid(alpha=0.3)

    ax = axes[1]
    ax.scatter(alphas, a_over_b, c="C0", zorder=3)
    for x, y, n in zip(alphas, a_over_b, names):
        ax.annotate(n, (x, y), fontsize=7, xytext=(3, 2), textcoords="offset points")
    ax.set_xlabel("alpha (LQ-equivalent) [/Gy]")
    ax.set_ylabel("alpha / beta  [Gy]")
    ax.set_title(f"α/β ratio vs α  (Pearson r={r_aab:.2f}, Spearman ρ={rho_aab:.2f})\n"
                 f"paper predicts large α/β (small β/α) for large α")
    ax.grid(alpha=0.3)

    fig.suptitle("GLOBLE-derived LQ coefficients across 17 cell lines")
    fig.tight_layout()
    out = FIG_DIR / "fig2_alpha_beta_anticorr.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    (RES_DIR / "alpha_beta_correlation.json").write_text(json.dumps(
        {"pearson_r_alpha_beta": r_ab, "spearman_rho_alpha_beta": rho_ab,
         "pearson_r_alpha_aob": r_aab, "spearman_rho_alpha_aob": rho_aab,
         "alphas": alphas.tolist(), "betas": betas.tolist(),
         "alpha_over_beta": a_over_b.tolist(), "cells": names}, indent=2))
    print(f"  wrote {out}")
    print(f"    β vs α:        Pearson r={r_ab:+.3f}  Spearman ρ={rho_ab:+.3f}")
    print(f"    α/β vs α:      Pearson r={r_aab:+.3f}  Spearman ρ={rho_aab:+.3f}")


def fig3_class_decomposition(name: str = "RT112") -> None:
    p = CELL_LINES[name]
    doses = np.linspace(0.01, 20.0, 400)
    iso_contrib = np.array([p.eps_i * damage_classes(d)[1] for d in doses])
    clu_contrib = np.array([p.eps_c * damage_classes(d)[2] for d in doses])

    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(doses, iso_contrib + clu_contrib, label="-ln S(D) total", lw=2)
    ax.plot(doses, iso_contrib, label="isolated-DSB contribution (eps_i n_i)", ls="--")
    ax.plot(doses, clu_contrib, label="clustered-DSB contribution (eps_c n_c)", ls="--")
    ax.set_xlabel("Photon dose D (Gy)")
    ax.set_ylabel("Contribution to -ln S")
    ax.set_title(f"Damage-class decomposition — {name}")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "fig3_class_decomposition_RT112.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"  wrote {out}")


if __name__ == "__main__":
    print("Friedrich 2012 (RR2964) static GLOBLE — figure smoke replication")
    print(f"  alpha_DSB = {ALPHA_DSB}/Gy/cell   N_L = {N_L} loops/nucleus")
    fig1_dose_response()
    fig2_alpha_beta_anticorr()
    fig3_class_decomposition()
    print("Done.")
