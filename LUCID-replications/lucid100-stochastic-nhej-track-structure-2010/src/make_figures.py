"""Generate figures for the NHEJ structural-replication report.

Reads data/tune2.json (fast rejoining scenario, 2 Gy),
       data/tune1.json (diffusive scenario with misrejoining),
       data/dose_response.json (clean low-residual regime, 0.5-10 Gy),
       data/dose_response_misrejoin.json (misrejoin vs dose).
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
FIGS = os.path.join(ROOT, "figures")
os.makedirs(FIGS, exist_ok=True)


def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


# ---------- Figure 1: DSB rejoining kinetics (residual fraction vs time) ----------
def fig_rejoining_kinetics():
    tune2 = load("tune2.json")          # 2 Gy, n=5, fast rejoining params
    tune1 = load("tune1.json")          # 2 Gy, n=5, diffusion+misrejoin params

    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    for label, run, marker, color in [
        ("Scenario A: tethered, fast (tune2)", tune2, "o", "tab:blue"),
        ("Scenario B: diffusive, slow+misrejoin (tune1)", tune1, "s", "tab:orange"),
    ]:
        r = run["results"][0]
        t = np.array(r["sample_times"])
        f = np.array(r["mean_residual_fraction"])
        ax.plot(t, f, marker=marker, color=color, linewidth=1.8, label=label)

    # literature reference biexponential band for 137Cs gamma in human fibroblasts:
    # fast t1/2 ~ 15 min (~70% amplitude), slow t1/2 ~ 150 min (~30% amplitude),
    # asymptote ~5% at 24h (Rothkamm & Lobrich 2003, Karlsson & Stenerlow 2004).
    t_lit = np.linspace(0, 1440, 400)
    lo = 0.7 * np.exp(-np.log(2)*t_lit/20.0) + 0.30 * np.exp(-np.log(2)*t_lit/180.0)
    hi = 0.7 * np.exp(-np.log(2)*t_lit/10.0) + 0.30 * np.exp(-np.log(2)*t_lit/120.0)
    ax.fill_between(t_lit, lo, hi, color="gray", alpha=0.25,
                    label="Literature biexp band (fibroblast, 137Cs γ)")

    ax.set_xscale("log")
    ax.set_xlim(2, 1600)
    ax.set_xlabel("Time after irradiation (min)")
    ax.set_ylabel("Residual DSB fraction")
    ax.set_title("DSB rejoining kinetics, 2 Gy γ-equivalent\n"
                 "(structural replication of Friedland et al. 2010)")
    ax.set_ylim(0, 1.05)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    out = os.path.join(FIGS, "fig1_rejoining_kinetics.png")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    print("wrote", out)


# ---------- Figure 2: residual DSB fraction at 24 h vs dose ----------
def fig_residual_vs_dose():
    dr = load("dose_response.json")
    drm = load("dose_response_misrejoin.json")

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for label, run, marker, color in [
        ("Scenario A: tethered (low residual)", dr, "o", "tab:blue"),
        ("Scenario B: diffusive (high residual)", drm, "s", "tab:orange"),
    ]:
        doses = np.array([r["dose_gy"] for r in run["results"]])
        f24 = np.array([r["mean_residual_fraction"][-1] for r in run["results"]])
        ax.plot(doses, f24, marker=marker, color=color, linewidth=1.8, label=label)

    ax.set_xscale("log")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Residual DSB fraction at 24 h")
    ax.set_title("Residual DSB fraction at 24 h vs dose\n"
                 "(Friedland 2010 abstract claim C4: some scenarios overestimate residuals)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    out = os.path.join(FIGS, "fig2_residual_vs_dose.png")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    print("wrote", out)


# ---------- Figure 3: mis-rejoin fraction vs dose ----------
def fig_misrejoin_vs_dose():
    dr = load("dose_response.json")
    drm = load("dose_response_misrejoin.json")

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for label, run, marker, color in [
        ("Scenario A: tethered, R_syn=50 nm", dr, "o", "tab:blue"),
        ("Scenario B: diffusive, R_syn=50 nm, D=1e-3", drm, "s", "tab:orange"),
    ]:
        doses = np.array([r["dose_gy"] for r in run["results"]])
        mf = np.array([r["misrejoin_fraction"] for r in run["results"]])
        ax.plot(doses, mf, marker=marker, color=color, linewidth=1.8, label=label)

    # Reference: BIANCA / Forster 2019 give a linear-quadratic shape on Nmr,
    # which on FRACTION translates to a slowly rising curve with dose.
    ax.set_xscale("log")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Mis-rejoin fraction (mis / total rejoined)")
    ax.set_title("Mis-rejoin fraction vs dose\n"
                 "(qualitative cross-check vs abstract claim C5 & proxy Forster 2019)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    out = os.path.join(FIGS, "fig3_misrejoin_vs_dose.png")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    print("wrote", out)


# ---------- Figure 4: ablation - dirty ends drive the slow tail (claim C7) ----------
def fig_dirty_ablation():
    loose30 = load("promo_loose_geom_pdirty30.json")  # p_dirty=0.30
    loose0 = load("promo_loose_geom_pdirty0.json")    # p_dirty=0.0
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for label, run, marker, color in [
        ("p_dirty = 0.30 (with complex DSBs)", loose30, "o", "tab:red"),
        ("p_dirty = 0.00 (clean DSBs only)", loose0, "s", "tab:green"),
    ]:
        r = run["results"][0]
        t = np.array(r["sample_times"])
        f = np.array(r["mean_residual_fraction"])
        ax.plot(t, np.maximum(f, 1e-4), marker=marker, color=color,
                linewidth=1.8, label=label)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2, 1600)
    ax.set_ylim(1e-4, 1.5)
    ax.set_xlabel("Time after irradiation (min)")
    ax.set_ylabel("Residual DSB fraction (log)")
    ax.set_title("Ablation: complex (dirty) DSBs drive the slow tail (claim C7)\n"
                 "2 Gy, loose-geometry regime (D=1e-3 \u00b5m\u00b2/min, R_syn=200 nm)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="lower left")
    out = os.path.join(FIGS, "fig4_dirty_ablation.png")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    print("wrote", out)


# ---------- Figure 5: geometry confound (claim C7 fails under tight geometry) ----------
def fig_geometry_confound():
    henth = load("promo_henthorn_anchor.json")        # p_dirty=0.30, tight
    abl0 = load("promo_ablation_pdirty0.json")        # p_dirty=0.00, tight
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for label, run, marker, color in [
        ("p_dirty = 0.30", henth, "o", "tab:red"),
        ("p_dirty = 0.00", abl0, "s", "tab:green"),
    ]:
        # pick 2 Gy
        r = [x for x in run["results"] if abs(x["dose_gy"] - 2.0) < 1e-6][0]
        t = np.array(r["sample_times"])
        f = np.array(r["mean_residual_fraction"])
        ax.plot(t, f, marker=marker, color=color, linewidth=1.8, label=label)
    ax.set_xscale("log")
    ax.set_xlim(2, 1600)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Time after irradiation (min)")
    ax.set_ylabel("Residual DSB fraction")
    ax.set_title("Negative finding: under tight geometry (R_syn=25 nm, D=1e-4),\n"
                 "dirty-end content does NOT change long-time residual (geometry-limited)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    out = os.path.join(FIGS, "fig5_geometry_confound.png")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    print("wrote", out)


if __name__ == "__main__":
    fig_rejoining_kinetics()
    fig_residual_vs_dose()
    fig_misrejoin_vs_dose()
    fig_dirty_ablation()
    fig_geometry_confound()
