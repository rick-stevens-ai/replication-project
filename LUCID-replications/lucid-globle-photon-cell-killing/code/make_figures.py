"""Reproduce Figures 2, 3, 4, 5, 6 of Herr et al. 2014 with the GLOBLE model."""
from __future__ import annotations

import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from globle import (
    GlobleParams,
    survival_single_dose,
    survival_static,
    survival_split_dose,
    survival_low_dose_rate_closed_form,
    lq_params_from_globle,
    survival_lq_lc,
    lea_catcheside_G,
    LN2,
)
from cell_lines import CELL_LINES, DOSE_RATES, ParamSet

OUTDIR_FIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
OUTDIR_RES = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
os.makedirs(OUTDIR_FIG, exist_ok=True)
os.makedirs(OUTDIR_RES, exist_ok=True)


def _make_globle(ps: ParamSet) -> GlobleParams:
    return GlobleParams(eps_i=ps.eps_i, eps_c=ps.eps_c, hlt_i=ps.hlt_i)


def survival_curve_doses(p: GlobleParams, doses: np.ndarray, dose_rate: float) -> np.ndarray:
    return np.array([survival_single_dose(p, float(D), dose_rate) for D in doses])


# ---------------- Figure 2 ---------------- #

def fig2_panel(ax, cell_line: str, max_dose: float, log_y: bool = True):
    ps = CELL_LINES[cell_line]["dose_rate"]
    p  = _make_globle(ps)
    doses = np.linspace(0.05, max_dose, 80)
    rates = DOSE_RATES[cell_line]
    series = {}
    for r in rates:
        S = survival_curve_doses(p, doses, r)
        ax.plot(doses, S, label=f"{r:g} Gy/h")
        series[f"{r:g} Gy/h"] = S.tolist()
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Survival probability")
    if log_y:
        ax.set_yscale("log")
        ax.set_ylim(1e-4, 1.1)
    ax.set_title(
        f"{cell_line}\nε_i={ps.eps_i}, ε_c={ps.eps_c}, HLT_i={ps.hlt_i:g} h"
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, loc="lower left")
    return doses.tolist(), series


def figure2():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    rt_d, rt_s = fig2_panel(axes[0], "RT112", max_dose=12.0)
    mt_d, mt_s = fig2_panel(axes[1], "MT",    max_dose=12.0)
    fig.suptitle("Fig. 2 reproduction: dose-rate effect (Herr et al. 2014)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR_FIG, "fig2_dose_rate_RT112_MT.png"), dpi=150)
    plt.close(fig)

    with open(os.path.join(OUTDIR_RES, "fig2_data.json"), "w") as f:
        json.dump({
            "RT112": {"doses_gy": rt_d, "survival_by_dose_rate": rt_s},
            "MT":    {"doses_gy": mt_d, "survival_by_dose_rate": mt_s},
        }, f, indent=2)


# ---------------- Figure 3: MT split dose ---------------- #

def figure3():
    ps = CELL_LINES["MT"]["split"]
    p  = _make_globle(ps)
    t1 = np.linspace(0.001, 12.0, 200)
    out = {}
    fig, ax = plt.subplots(figsize=(7, 5))
    for d in [5.0, 6.0]:
        S = np.array([survival_split_dose(p, d, t) for t in t1])
        ax.plot(t1, S, label=f"{int(d)}+{int(d)} Gy")
        out[f"{int(d)}+{int(d)} Gy"] = S.tolist()
    ax.set_xlabel("Time between fractions $t_1$ (h)")
    ax.set_ylabel("Survival probability")
    ax.set_yscale("log")
    ax.set_title(
        f"Fig. 3 reproduction — MT split dose\nε_i={ps.eps_i}, ε_c={ps.eps_c}, HLT_i={ps.hlt_i:g} h"
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR_FIG, "fig3_split_dose_MT.png"), dpi=150)
    plt.close(fig)

    with open(os.path.join(OUTDIR_RES, "fig3_data.json"), "w") as f:
        json.dump({"t1_h": t1.tolist(), **out}, f, indent=2)


# ---------------- Figure 4: LQ–Lea-Catcheside vs GLOBLE ---------------- #

def globle_G_equivalent(p: GlobleParams, T_h: float, alpha: float, beta: float) -> float:
    """Compute the GLOBLE equivalent of the Lea–Catcheside factor by extracting the
    second-derivative-in-dose at D=0 of −ln S(D,T), normalised against 2β."""
    if T_h <= 0:
        return 1.0
    dose_rate = lambda D: D / T_h
    h = 1e-3
    # Use survival at three small doses with the same T (so dose-rate varies):
    # We want d²(−ln S)/dD² at D=0 with the *protraction time* T fixed.
    # Numerically: ratios are tiny; we use a quadratic fit through three doses.
    Ds = np.array([h, 2 * h, 3 * h])
    Ss = np.array([survival_single_dose(p, float(D), float(dose_rate(D))) for D in Ds])
    nl = -np.log(Ss)
    # fit nl = a*D + c*D^2
    A = np.vstack([Ds, Ds * Ds]).T
    coeffs, *_ = np.linalg.lstsq(A, nl, rcond=None)
    a_fit, c_fit = coeffs
    # c_fit ≈ G*β  (since −lnS ≈ αD + G·β·D²)
    return c_fit / beta


def figure4():
    # Two hypothetical cell lines from the paper's Figure 4 caption.
    # The paper-quoted values for the α/β=5.26 Gy case (ε_i=0.002, ε_c=0.19) are
    # internally inconsistent with Eq.(8) α = ε_i·α_DSB given α=0.15/Gy and α_DSB=30/Gy/cell;
    # the consistent values are ε_i=0.005, ε_c≈0.20 (see PROGRESS / REPORT for friction tag).
    # We use the *consistent* values so the GLOBLE-equivalent G matches the LQ G
    # to leading order as the paper claims.
    configs = [
        ("α/β=1 Gy",    dict(alpha=0.025, beta=0.025,  eps_i=0.000833, eps_c=0.1683)),
        ("α/β=5.26 Gy", dict(alpha=0.15,  beta=0.0285, eps_i=0.005,    eps_c=0.20)),
    ]
    r = LN2 / 0.5   # paper: r = ln2/0.5h
    Ts = np.logspace(-3, 2.5, 60)   # protraction time, h
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(12, 5))

    out_pack = {}
    for name, cfg in configs:
        alpha, beta = cfg["alpha"], cfg["beta"]
        p = GlobleParams(eps_i=cfg["eps_i"], eps_c=cfg["eps_c"], hlt_i=0.5)
        G_lq = np.array([lea_catcheside_G(r, T) for T in Ts])
        G_gl = np.array([globle_G_equivalent(p, float(T), alpha, beta) for T in Ts])
        axA.plot(Ts, G_lq, "--", label=f"{name} LQ G")
        axA.plot(Ts, G_gl, "-",  label=f"{name} GLOBLE G")
        rel = (G_gl - G_lq) / np.where(np.abs(G_lq) > 1e-12, G_lq, np.nan)
        axB.plot(Ts, rel, label=name)
        out_pack[name] = {"T_h": Ts.tolist(), "G_LQ": G_lq.tolist(), "G_GLOBLE": G_gl.tolist()}

    axA.set_xscale("log")
    axA.set_xlabel("Protraction time T (h)")
    axA.set_ylabel("Lea-Catcheside factor G")
    axA.set_title("Fig. 4A — LQ vs GLOBLE-equivalent G")
    axA.grid(True, which="both", alpha=0.3)
    axA.legend(fontsize=7)

    axB.set_xscale("log")
    axB.set_xlabel("Protraction time T (h)")
    axB.set_ylabel("(G_GLOBLE − G_LQ) / G_LQ")
    axB.set_title("Fig. 4B — relative deviation")
    axB.set_ylim(-0.5, 5)
    axB.grid(True, which="both", alpha=0.3)
    axB.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR_FIG, "fig4_lq_vs_globle.png"), dpi=150)
    plt.close(fig)

    with open(os.path.join(OUTDIR_RES, "fig4_data.json"), "w") as f:
        json.dump(out_pack, f, indent=2)


# ---------------- Figure 5: deterministic effects ---------------- #

def isoeffective_dose(p: GlobleParams, dose_rate_gy_per_h: float, reference_acute_dose: float,
                      d_lo: float = 0.1, d_hi: float = 200.0) -> float:
    """Bisect to find D such that S(D, Ḋ) == S_static(D_ref).  S monotone-decreasing in D."""
    target = math.log(survival_static(p, reference_acute_dose))
    def f(D):
        return math.log(survival_single_dose(p, D, dose_rate_gy_per_h)) - target
    # f(d_lo) > 0 (less dose, higher S → log S > target since target very negative)
    flo, fhi = f(d_lo), f(d_hi)
    for _ in range(80):
        if flo * fhi <= 0:
            break
        d_hi *= 2.0
        fhi = f(d_hi)
    for _ in range(80):
        mid = 0.5 * (d_lo + d_hi)
        fm = f(mid)
        if fm == 0 or (d_hi - d_lo) < 1e-4:
            return mid
        if flo * fm < 0:
            d_hi, fhi = mid, fm
        else:
            d_lo, flo = mid, fm
    return 0.5 * (d_lo + d_hi)


def figure5():
    # Pneumonitis: α/β=3 Gy, ε_i=0.00333, ε_c=0.229, reference D50 acute = 10 Gy.
    # Bone marrow:  α/β=8 Gy, ε_i=0.00333, ε_c=0.09,  reference D50 acute =  3 Gy.
    cases = [
        ("Pneumonitis", 10.0, dict(eps_i=0.00333, eps_c=0.229), 10.0, 30.0, "tab:green"),
        ("Bone marrow",  3.0, dict(eps_i=0.00333, eps_c=0.09),   3.0, 0.07, "tab:red"),
    ]
    # Use dose-rate grid covering 0.01 .. 100 Gy/h
    rates = np.logspace(-2.5, 2.0, 25)

    fig, ax = plt.subplots(figsize=(7, 5))
    out = {}
    for label, D50_acute, params, theta_inf, theta_1, colour in cases:
        # empirical curve
        emp = theta_inf + theta_1 / rates
        ax.plot(rates, emp, "-", color=colour, label=f"{label} empirical Eq.42")
        # GLOBLE prediction band: HLT_i = 0.1, 0.5, 1.0 h
        for hlt, ls in zip([0.1, 0.5, 1.0], [":", "--", "-."]):
            p = GlobleParams(eps_i=params["eps_i"], eps_c=params["eps_c"], hlt_i=hlt)
            iso = np.array([isoeffective_dose(p, float(r), D50_acute) for r in rates])
            ax.plot(rates, iso, ls, color=colour, alpha=0.8,
                    label=f"{label} GLOBLE HLT_i={hlt} h")
            out[f"{label}__HLT{hlt}"] = {"rates": rates.tolist(),
                                          "isoeffective_dose_gy": iso.tolist()}
        out[f"{label}__empirical"] = {"rates": rates.tolist(),
                                        "D50_gy": emp.tolist()}

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Dose rate (Gy/h)")
    ax.set_ylabel("Isoeffective dose / D50 (Gy)")
    ax.set_title("Fig. 5 reproduction — deterministic effects: pneumonitis & bone marrow")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR_FIG, "fig5_deterministic.png"), dpi=150)
    plt.close(fig)

    with open(os.path.join(OUTDIR_RES, "fig5_data.json"), "w") as f:
        json.dump(out, f, indent=2)


# ---------------- Figure 6: LL — split-dose prediction from dose-rate fit ---------------- #

def figure6():
    fitset   = CELL_LINES["LL"]["split"]      # dashed: split-dose fit (good)
    predset  = CELL_LINES["LL"]["dose_rate"]  # dotted: predicted from dose-rate fit (mismatch)
    p_fit  = _make_globle(fitset)
    p_pred = _make_globle(predset)
    t1 = np.linspace(0.001, 10.0, 200)
    S_fit  = np.array([survival_split_dose(p_fit,  5.0, t) for t in t1])
    S_pred = np.array([survival_split_dose(p_pred, 5.0, t) for t in t1])
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(t1, S_fit,  "--", label="GLOBLE fit (split-dose params)")
    ax.plot(t1, S_pred, ":",  label="GLOBLE prediction (dose-rate params)")
    ax.set_xlabel("Time between fractions $t_1$ (h)")
    ax.set_ylabel("Survival probability")
    ax.set_yscale("log")
    ax.set_title("Fig. 6 reproduction — LL split dose 5+5 Gy:\nsplit-dose fit vs prediction from dose-rate fit")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR_FIG, "fig6_LL_split_dose_prediction.png"), dpi=150)
    plt.close(fig)
    with open(os.path.join(OUTDIR_RES, "fig6_data.json"), "w") as f:
        json.dump({"t1_h": t1.tolist(),
                   "S_fit_split":    S_fit.tolist(),
                   "S_pred_doserate": S_pred.tolist()}, f, indent=2)


# ---------------- All-cell-line dose-rate survival table ---------------- #

def all_cell_lines_table():
    """Dump survival(D=2 Gy) and survival(D=8 Gy) at each dose rate for every
    cell line, using the 'dose_rate' Table 2 parameters.  Used for the
    claim-by-claim agreement audit."""
    out = {}
    for cl, sets in CELL_LINES.items():
        if "dose_rate" not in sets:
            continue
        ps = sets["dose_rate"]
        p  = _make_globle(ps)
        rates = DOSE_RATES.get(cl, [])
        row = {"eps_i": ps.eps_i, "eps_c": ps.eps_c, "hlt_i": ps.hlt_i,
               "survival": {}}
        for r in rates:
            row["survival"][f"{r:g} Gy/h"] = {
                "D=2Gy": survival_single_dose(p, 2.0, r),
                "D=8Gy": survival_single_dose(p, 8.0, r),
            }
        out[cl] = row
    with open(os.path.join(OUTDIR_RES, "all_cell_lines_survival.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    print(">> Figure 2 (dose-rate effect, RT112 + MT)")
    figure2()
    print(">> Figure 3 (MT split dose)")
    figure3()
    print(">> Figure 4 (LQ vs GLOBLE Lea-Catcheside G)")
    figure4()
    print(">> Figure 5 (deterministic effects)")
    figure5()
    print(">> Figure 6 (LL split-dose predicted from dose-rate fit)")
    figure6()
    print(">> All-cell-line survival table")
    all_cell_lines_table()
    print("Done.  Outputs in figures/ and results/.")
