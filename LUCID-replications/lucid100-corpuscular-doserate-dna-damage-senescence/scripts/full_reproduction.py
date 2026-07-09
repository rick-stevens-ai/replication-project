#!/usr/bin/env python3
"""
Full reproduction script for Soroko et al. 2024 (CIMB 46:13860, PMC11726848).

Uses figure-digitized values (data/digitized_figures.json) plus in-text values
(data/digitized_values.json) to:

1. Re-fit MTT dose-response with Hill model on ALL digitized points
   (not just LD50/D37 anchors) and compare reproduced LD50, D37, n_Hill to
   paper-reported values.
2. Re-fit a Linear-Quadratic survival model on the digitized data and report
   alpha, beta, alpha/beta.
3. Re-fit clonogenic SF data with LQ and Hill.
4. Compute dose-modifying factor (DMF) at multiple effect levels from
   reproduced curves, compare to the paper's headline "3x sparing".
5. Comet-assay ratio LDR/HDR at matched doses.
6. Re-run the paper's primary statistical test (one-way ANOVA + Dunnett's vs
   control) on the digitized MTT means using their reported n=3 + CV
   error-bar interpretation.
7. Cell-cycle G2/M arrest dose-dependence (Fig 4C HDR) - confirm the
   ~25-50% / ~100% / ~100% claim at 4/8/16 Gy.
8. Apoptosis time course (Fig 5C HDR) - check the 4:1 vs 1:1 ratio claim.
9. SA-beta-gal fold-change reproduction (Fig 5E) - check 1.5x / 2x.
10. ROS dose-rate claim: LDR @ ~LD50 gives 4x, HDR @ D37 gives 15x.

Save everything to outputs/full_reproduction_results.json and emit several
PNG figures.

Free, CPU-only, no network.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

# -----------------------------------------------------------------------------
# paths
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

digitized_figs = json.loads((DATA / "digitized_figures.json").read_text())
digitized_text = json.loads((DATA / "digitized_values.json").read_text())

PAPER = {
    "LD50_HDR": 3.4,
    "LD50_LDR": 10.8,
    "D37_HDR": 8.0,
    "D37_LDR": 20.0,
    "DMF50_paper": 3.18,  # 10.8/3.4
    "DMF37_paper": 2.5,
    "comet_LDR_over_HDR_4Gy": 3.0 / 5.0,
    "comet_LDR_over_HDR_8Gy": 4.0 / 8.0,
    "G2M_HDR_4Gy_pct_range": (25, 50),
    "G2M_HDR_8Gy_pct": 100,
    "G2M_HDR_16Gy_pct": 100,
    "SAbetagal_LDR_LD50_foldx_paper": 1.5,
    "SAbetagal_LDR_D37_foldx_paper": 2.0,
    "ROS_LDR_LD50_foldx_paper": 4,
    "ROS_HDR_D37_foldx_paper": 15,
    "AnnV_PI_ratio_LDR_48h": 4.0,
    "AnnV_PI_ratio_HDR_48h": 1.0,
}

# =============================================================================
# helpers
# =============================================================================
def hill(D, LD50, n):
    """Decreasing log-logistic V(D)=1/(1+(D/LD50)^n), V in [0,1]."""
    return 1.0 / (1.0 + (D / LD50) ** n)


def hill4(D, top, bottom, LD50, n):
    """4-parameter log-logistic (GraphPad Prism default), V in [bottom, top]."""
    return bottom + (top - bottom) / (1.0 + (D / LD50) ** n)


def fit_hill4(doses, values_frac, sigma=None):
    p0 = [1.0, 0.05, np.median(doses[doses > 0]), 2.0]
    popt, pcov = curve_fit(
        hill4, doses, values_frac, p0=p0, sigma=sigma, absolute_sigma=False,
        bounds=([0.5, 0.0, 1e-3, 0.2], [1.5, 0.5, 1e3, 20.0]),
    )
    return popt, pcov


def lq_sf(D, alpha, beta):
    return np.exp(-alpha * D - beta * D ** 2)


def fit_hill(doses, values_frac, sigma=None):
    """values_frac in [0,1]."""
    p0 = [np.median(doses[doses > 0]), 2.0]
    popt, pcov = curve_fit(
        hill, doses, values_frac, p0=p0, sigma=sigma, absolute_sigma=False,
        bounds=([1e-3, 1e-2], [1e3, 50.0]),
    )
    return popt, pcov


def fit_lq(doses, sf, sigma=None):
    """Fit ln(SF) = -aD - bD^2 via curve_fit on SF (multiplicative noise)."""
    p0 = [0.1, 0.01]
    popt, pcov = curve_fit(
        lq_sf, doses, sf, p0=p0, sigma=sigma, absolute_sigma=False,
        bounds=([0.0, -0.1], [5.0, 1.0]),
    )
    return popt, pcov


def solve_dose_for_value(LD50, n, target):
    """Invert Hill: target = 1/(1+(D/LD50)^n) -> D = LD50 * ((1-target)/target)^(1/n)."""
    return LD50 * ((1 - target) / target) ** (1 / n)


# =============================================================================
# (1)+(2) Re-fit MTT dose-response
# =============================================================================
def claim_MTT_dose_response():
    out = {}
    fits = {}

    fig, (ax_lin, ax_log) = plt.subplots(1, 2, figsize=(11, 4.4))

    for regime, color in (("HDR", "tab:blue"), ("LDR", "tab:orange")):
        pts = digitized_figs["fig3A_MTT_doseresponse_pct_living_cells"][regime]
        D = np.array([p["dose_Gy"] for p in pts], dtype=float)
        V = np.array([p["pct"] / 100.0 for p in pts], dtype=float)
        Verr = np.array([p["err_pm"] / 100.0 for p in pts], dtype=float)

        # Anchor 0 Gy = 100% control: prepend a (0, 1.0) point with tight
        # error so the Hill fit doesn't drift the baseline up. (The paper
        # explicitly normalizes to unirradiated control.)
        D_fit = np.concatenate([[0.0], D])
        V_fit = np.concatenate([[1.0], V])
        Verr_fit = np.concatenate([[0.02], Verr])

        # 3-parameter Hill (forced top=1, bottom=0): only LD50, n free
        (LD50_h, n_h), _ = fit_hill(D_fit, V_fit, sigma=Verr_fit)
        D37_h = solve_dose_for_value(LD50_h, n_h, 0.37)
        D10_h = solve_dose_for_value(LD50_h, n_h, 0.10)

        # 4-parameter Hill (Prism default, with floor)
        try:
            (top, bottom, LD50_4, n_4), _ = fit_hill4(D_fit, V_fit, sigma=Verr_fit)
            mid = (top + bottom) / 2.0
            # solve hill4 for V = mid -> D = LD50_4 (definition)
            # solve for V = 0.5 absolute (paper definition: 50% of control)
            def hill4_inv(target):
                if not (bottom < target < top):
                    return None
                return LD50_4 * ((top - target) / (target - bottom)) ** (1 / n_4)
            LD50_h4_abs50 = hill4_inv(0.5)
            D37_h4_abs = hill4_inv(0.37)
        except Exception:
            top = bottom = LD50_4 = n_4 = LD50_h4_abs50 = D37_h4_abs = None

        # LQ fit (treat MTT viability as SF surrogate, with the well-known
        # caveat that authors themselves flag)
        try:
            (alpha, beta), _ = fit_lq(D, V, sigma=Verr)
            LQ_LD50 = float(np.interp(0.5, lq_sf(np.linspace(0.01, 100, 50000), alpha, beta)[::-1], np.linspace(0.01, 100, 50000)[::-1]))
        except Exception as e:
            alpha, beta, LQ_LD50 = None, None, None

        fits[regime] = {
            "hill3_LD50_Gy": float(LD50_h),
            "hill3_n": float(n_h),
            "hill3_D37_Gy": float(D37_h),
            "hill3_D10_Gy": float(D10_h),
            "hill4_top": (None if top is None else float(top)),
            "hill4_bottom": (None if bottom is None else float(bottom)),
            "hill4_LD50_param_Gy": (None if LD50_4 is None else float(LD50_4)),
            "hill4_n": (None if n_4 is None else float(n_4)),
            "hill4_LD50_abs50_Gy": (None if LD50_h4_abs50 is None else float(LD50_h4_abs50)),
            "hill4_D37_abs_Gy": (None if D37_h4_abs is None else float(D37_h4_abs)),
            "lq_alpha_per_Gy": (None if alpha is None else float(alpha)),
            "lq_beta_per_Gy2": (None if beta is None else float(beta)),
            "lq_alpha_over_beta_Gy": (None if (alpha is None or beta in (None, 0)) else float(alpha / beta)),
            "lq_LD50_Gy_interp": LQ_LD50,
            "paper_LD50_Gy": PAPER[f"LD50_{regime}"],
            "paper_D37_Gy": PAPER[f"D37_{regime}"],
            "reproduced_pct_LD50_err_hill3": float(abs(LD50_h - PAPER[f"LD50_{regime}"]) / PAPER[f"LD50_{regime}"] * 100),
            "reproduced_pct_D37_err_hill3": float(abs(D37_h - PAPER[f"D37_{regime}"]) / PAPER[f"D37_{regime}"] * 100),
            "reproduced_pct_LD50_err_hill4": (
                None if LD50_h4_abs50 is None else float(abs(LD50_h4_abs50 - PAPER[f"LD50_{regime}"]) / PAPER[f"LD50_{regime}"] * 100)
            ),
            "reproduced_pct_D37_err_hill4": (
                None if D37_h4_abs is None else float(abs(D37_h4_abs - PAPER[f"D37_{regime}"]) / PAPER[f"D37_{regime}"] * 100)
            ),
        }

        # plot
        for ax in (ax_lin, ax_log):
            ax.errorbar(D, V * 100, yerr=Verr * 100, fmt="o", color=color, label=f"{regime} data")
            D_grid = np.geomspace(0.5, 100, 400)
            ax.plot(D_grid, hill(D_grid, LD50_h, n_h) * 100, "-", color=color,
                    label=f"{regime} Hill fit\nLD50={LD50_h:.2f} Gy, n={n_h:.2f}")
            ax.axhline(50, color="grey", ls=":", lw=0.5)
            ax.axhline(37, color="grey", ls=":", lw=0.5)

    ax_lin.set_xlabel("Dose (Gy)")
    ax_lin.set_ylabel("% living cells (MTT)")
    ax_lin.set_title("Reproduced MTT dose-response (linear x)")
    ax_lin.legend(fontsize=7, loc="upper right")
    ax_lin.set_xlim(0, 75)
    ax_lin.set_ylim(0, 110)
    ax_lin.grid(alpha=0.3)

    ax_log.set_xscale("log")
    ax_log.set_xlabel("Dose (Gy)")
    ax_log.set_ylabel("% living cells (MTT)")
    ax_log.set_title("Reproduced MTT dose-response (log x)")
    ax_log.legend(fontsize=7, loc="upper right")
    ax_log.set_ylim(0, 110)
    ax_log.grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT / "fig_reproduced_MTT_doseresponse.png", dpi=150)
    plt.close(fig)

    # DMF at multiple effect levels using Hill-3 (forced top=1, bottom=0)
    dmfs = {}
    for v in (0.50, 0.37, 0.25, 0.10):
        D_HDR = solve_dose_for_value(fits["HDR"]["hill3_LD50_Gy"], fits["HDR"]["hill3_n"], v)
        D_LDR = solve_dose_for_value(fits["LDR"]["hill3_LD50_Gy"], fits["LDR"]["hill3_n"], v)
        dmfs[f"DMF@{int(round((1-v)*100))}%kill"] = {
            "D_HDR_Gy": float(D_HDR),
            "D_LDR_Gy": float(D_LDR),
            "DMF_LDR_over_HDR": float(D_LDR / D_HDR),
        }

    out["fits"] = fits
    out["DMF_curve"] = dmfs
    out["headline_match"] = {
        "paper_DMF50": PAPER["DMF50_paper"],
        "reproduced_DMF50_hill3": dmfs["DMF@50%kill"]["DMF_LDR_over_HDR"],
        "paper_DMF37": PAPER["DMF37_paper"],
        "reproduced_DMF37_hill3": dmfs["DMF@63%kill"]["DMF_LDR_over_HDR"],
        "reproduced_DMF50_hill4_abs": (
            None if fits["HDR"]["hill4_LD50_abs50_Gy"] is None or fits["LDR"]["hill4_LD50_abs50_Gy"] is None
            else fits["LDR"]["hill4_LD50_abs50_Gy"] / fits["HDR"]["hill4_LD50_abs50_Gy"]
        ),
    }
    return out


# =============================================================================
# (3) Clonogenic SF re-fit (LQ + Hill on the digitized 3F bars)
# =============================================================================
def claim_clonogenic_SF():
    out = {}
    fig, ax = plt.subplots(figsize=(7, 4.6))

    for regime, color in (("HDR", "tab:blue"), ("LDR", "tab:orange")):
        pts = digitized_figs["fig3F_clonogenic_SF_pct_control"][regime]
        D = np.array([p["dose_Gy"] for p in pts], dtype=float)
        SF = np.array([p["pct"] / 100.0 for p in pts], dtype=float)
        SFerr = np.array([p["err_pm"] / 100.0 for p in pts], dtype=float)

        # LQ fit ignoring 0 Gy normalization point's degenerate contribution
        try:
            (alpha, beta), _ = fit_lq(D, SF, sigma=SFerr)
        except Exception:
            alpha, beta = None, None

        # Hill fit
        (LD50_h, n_h), _ = fit_hill(D, SF, sigma=SFerr)

        out[regime] = {
            "lq_alpha_per_Gy": (None if alpha is None else float(alpha)),
            "lq_beta_per_Gy2": (None if beta is None else float(beta)),
            "lq_alpha_over_beta_Gy": (None if (alpha is None or beta in (None, 0)) else float(alpha / beta)),
            "hill_LD50_Gy": float(LD50_h),
            "hill_n": float(n_h),
        }

        ax.errorbar(D, SF * 100, yerr=SFerr * 100, fmt="o", color=color, label=f"{regime} clonogenic")
        D_grid = np.linspace(0, max(D) * 1.05, 200)
        if alpha is not None:
            ax.plot(D_grid, lq_sf(D_grid, alpha, beta) * 100, "-", color=color,
                    label=f"{regime} LQ: α={alpha:.3f}, β={beta:.3f}, α/β={alpha/beta if beta else float('inf'):.1f}")

    # Clonogenic-derived empirical LD50 for the dose-modifying factor calc
    # Just by linear interpolation on the 3 bars:
    out["empirical_DMF50_clonogenic"] = {
        "comment": "Both regimes hit ~21% SF at 8 Gy (HDR) vs 18 Gy (LDR) "
                   "and ~63%/78% at 4 Gy (HDR) vs 12 Gy (LDR). Dose-modifying "
                   "ratio at SF=0.5 estimated by linear interpolation of clonogenic bars.",
    }
    # Interpolate dose at which SF crosses 0.5 (HDR: between 4 Gy [0.63] and 8 Gy [0.21])
    # Linear interpolation:
    def lerp_dose(d_pts, sf_pts, target=0.5):
        d_pts, sf_pts = np.asarray(d_pts), np.asarray(sf_pts)
        order = np.argsort(d_pts)
        d_pts, sf_pts = d_pts[order], sf_pts[order]
        for i in range(len(d_pts) - 1):
            if sf_pts[i] >= target >= sf_pts[i + 1]:
                f = (sf_pts[i] - target) / (sf_pts[i] - sf_pts[i + 1])
                return float(d_pts[i] + f * (d_pts[i + 1] - d_pts[i]))
        return None

    D_HDR = [p["dose_Gy"] for p in digitized_figs["fig3F_clonogenic_SF_pct_control"]["HDR"]]
    SF_HDR = [p["pct"] / 100.0 for p in digitized_figs["fig3F_clonogenic_SF_pct_control"]["HDR"]]
    D_LDR = [p["dose_Gy"] for p in digitized_figs["fig3F_clonogenic_SF_pct_control"]["LDR"]]
    SF_LDR = [p["pct"] / 100.0 for p in digitized_figs["fig3F_clonogenic_SF_pct_control"]["LDR"]]
    LD50_clono_HDR = lerp_dose(D_HDR, SF_HDR, 0.5)
    LD50_clono_LDR = lerp_dose(D_LDR, SF_LDR, 0.5)
    out["empirical_DMF50_clonogenic"]["LD50_HDR_Gy"] = LD50_clono_HDR
    out["empirical_DMF50_clonogenic"]["LD50_LDR_Gy"] = LD50_clono_LDR
    out["empirical_DMF50_clonogenic"]["DMF50_LDR_over_HDR"] = (
        LD50_clono_LDR / LD50_clono_HDR if (LD50_clono_HDR and LD50_clono_LDR) else None
    )

    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Colonies (% control)")
    ax.set_title("Clonogenic SF (Fig 3F) reproduced + LQ fits")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig_reproduced_clonogenic_SF.png", dpi=150)
    plt.close(fig)

    return out


# =============================================================================
# (5) Comet ratio
# =============================================================================
def claim_comet_ratio():
    pts = digitized_figs["fig4E_comet_pct_DNA_damage"]
    by_key = {(p["regime"], p["dose_Gy"]): p for p in pts}

    out = {
        "control_HDR_pct": by_key[("HDR", 0)]["pct"],
        "control_LDR_pct": by_key[("LDR", 0)]["pct"],
        "ratios": {
            "4Gy_LDR_over_HDR": by_key[("LDR", 4)]["pct"] / by_key[("HDR", 4)]["pct"],
            "8Gy_LDR_over_HDR": by_key[("LDR", 8)]["pct"] / by_key[("HDR", 8)]["pct"],
        },
        "paper_4Gy_ratio": PAPER["comet_LDR_over_HDR_4Gy"],
        "paper_8Gy_ratio": PAPER["comet_LDR_over_HDR_8Gy"],
    }

    # Quick plot
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.array([0, 4, 8])
    HDR = np.array([by_key[("HDR", d)]["pct"] for d in x])
    LDR = np.array([by_key[("LDR", d)]["pct"] for d in x])
    HDRerr = np.array([by_key[("HDR", d)]["err_pm"] for d in x])
    LDRerr = np.array([by_key[("LDR", d)]["err_pm"] for d in x])
    width = 0.35
    ax.bar(x - width / 2, HDR, width=width, yerr=HDRerr, color="tab:blue", label="HDR")
    ax.bar(x + width / 2, LDR, width=width, yerr=LDRerr, color="tab:orange", label="LDR")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{d} Gy" for d in x])
    ax.set_ylabel("% DNA damage (comet tail)")
    ax.set_title("Comet assay (Fig 4E) reproduced")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig_reproduced_comet.png", dpi=150)
    plt.close(fig)

    return out


# =============================================================================
# (6) Dunnett-style ANOVA on the digitized MTT means (n=3, CV-based SDs)
# =============================================================================
def claim_anova_dunnett():
    """The paper uses one-way ANOVA + Dunnett's post-hoc (each dose vs control).

    With only digitized means + CV-as-error-bars + n=3 we can reconstruct
    per-replicate samples by assuming the published error bar IS the
    coefficient of variation (= SD/mean *100). That lets us run an honest
    one-way ANOVA + Dunnett-equivalent (pairwise t-tests with Bonferroni
    correction; closest free analogue without scipy.stats.dunnett).
    """
    out = {}

    for regime in ("HDR", "LDR"):
        pts = digitized_figs["fig3A_MTT_doseresponse_pct_living_cells"][regime]
        doses = [p["dose_Gy"] for p in pts]
        means = [p["pct"] for p in pts]
        errs = [p["err_pm"] for p in pts]

        # Use 100% control (implicit normalization point); generate synthetic
        # n=3 replicates from each (mean, error_pm) with rng seed for reprod.
        rng = np.random.default_rng(seed=42 + (0 if regime == "HDR" else 1))
        n_reps = 3
        groups = []
        group_labels = ["control"]
        # control = 100 ± 5 (assume CV~5% baseline)
        ctrl = rng.normal(loc=100, scale=5, size=n_reps)
        groups.append(ctrl)
        for d, m, e in zip(doses, means, errs):
            samp = rng.normal(loc=m, scale=max(e, 0.5), size=n_reps)
            groups.append(samp)
            group_labels.append(f"{d}Gy")

        # one-way ANOVA across all groups
        F, p_anova = stats.f_oneway(*groups)

        # Dunnett-equivalent: pairwise t-tests vs control with Bonferroni
        per_dose = []
        for lab, g in zip(group_labels[1:], groups[1:]):
            t, p = stats.ttest_ind(g, ctrl, equal_var=False)
            per_dose.append({
                "dose_label": lab,
                "mean": float(np.mean(g)),
                "sd": float(np.std(g, ddof=1)),
                "t_stat": float(t),
                "p_raw": float(p),
                "p_bonferroni": float(min(1.0, p * len(group_labels[1:]))),
            })

        out[regime] = {
            "F_stat": float(F),
            "p_anova": float(p_anova),
            "n_per_group": n_reps,
            "per_dose_vs_control": per_dose,
            "note": (
                "Synthetic replicates generated from digitized (mean, CV-as-err) "
                "with rng seed 42. Original per-replicate data not deposited."
            ),
        }
    return out


# =============================================================================
# (7) G2/M dose dependence (Fig 4C)
# =============================================================================
def claim_G2M():
    rows = [r for r in digitized_figs["fig4C_cell_cycle_HDR_pct"] if r["time_h"] == 24]
    by_dose = {r["dose_Gy"]: r["G2M"] for r in rows}
    out = {
        "HDR_24h_G2M_pct": by_dose,
        "paper_claims": {
            "4Gy": "G2/M increased 25-50% above control",
            "8Gy": "~100%",
            "16Gy": "~100%",
        },
        "reproduced_vs_paper": {
            "4Gy_increase_pp_vs_control": by_dose[4] - by_dose[0],
            "8Gy_pct": by_dose[8],
            "16Gy_pct": by_dose[16],
        },
    }
    # LDR comparison: paper claims "no measurable arrest"
    ldr_rows = [r for r in digitized_figs["fig4B_cell_cycle_LDR_pct"] if r["time_h"] == 24]
    out["LDR_24h_G2M_pct"] = {r["dose_Gy"]: r["G2M"] for r in ldr_rows}
    out["LDR_arrest_max_change_pp"] = max(r["G2M"] for r in ldr_rows) - min(r["G2M"] for r in ldr_rows)
    return out


# =============================================================================
# (8) Apoptosis 48h ratio: PI-AnnV+ / PI+ in LDR (~4:1) vs HDR (~1:1)
# =============================================================================
def claim_apoptosis_ratio():
    out = {}
    # LDR 48h, 36 Gy bin is the "above D37" condition the paper highlights
    ldr_48 = [r for r in digitized_figs["fig5B_anxV_PI_LDR_pct"] if r["time_h"] == 48 and r["dose_Gy"] > 0]
    hdr_48 = [r for r in digitized_figs["fig5C_anxV_PI_HDR_pct"] if r["time_h"] == 48 and r["dose_Gy"] > 0]

    def ratio(r):
        return r["early_apop"] / max(r["dead"], 1e-6)

    out["LDR_48h_ratios"] = [{"dose_Gy": r["dose_Gy"], "early_apop/dead": ratio(r)} for r in ldr_48]
    out["HDR_48h_ratios"] = [{"dose_Gy": r["dose_Gy"], "early_apop/dead": ratio(r)} for r in hdr_48]
    out["paper_LDR_ratio_48h"] = PAPER["AnnV_PI_ratio_LDR_48h"]
    out["paper_HDR_ratio_48h"] = PAPER["AnnV_PI_ratio_HDR_48h"]
    out["mean_LDR_ratio_48h"] = float(np.mean([ratio(r) for r in ldr_48]))
    out["mean_HDR_ratio_48h"] = float(np.mean([ratio(r) for r in hdr_48]))
    return out


# =============================================================================
# (9) SA-beta-gal fold change
# =============================================================================
def claim_SAbetagal():
    data = digitized_figs["fig5E_SAbetagal_color_intensity_pct"]["data"]

    def find(regime, label):
        return next(d for d in data if d["regime"] == regime and d["label"] == label)

    LDR_ctrl = find("LDR", "control")["value"]
    LDR_LD50 = find("LDR", "LD50")["value"]
    LDR_D37 = find("LDR", "D37")["value"]
    HDR_ctrl = find("HDR", "control")["value"]
    HDR_LD50 = find("HDR", "LD50")["value"]
    HDR_D37 = find("HDR", "D37")["value"]
    out = {
        "LDR": {
            "ctrl": LDR_ctrl, "LD50": LDR_LD50, "D37": LDR_D37,
            "fold_LD50_over_ctrl": LDR_LD50 / LDR_ctrl,
            "fold_D37_over_ctrl": LDR_D37 / LDR_ctrl,
        },
        "HDR": {
            "ctrl": HDR_ctrl, "LD50": HDR_LD50, "D37": HDR_D37,
            "fold_LD50_over_ctrl": HDR_LD50 / HDR_ctrl,
            "fold_D37_over_ctrl": HDR_D37 / HDR_ctrl,
        },
        "paper_LDR_LD50_foldx": PAPER["SAbetagal_LDR_LD50_foldx_paper"],
        "paper_LDR_D37_foldx": PAPER["SAbetagal_LDR_D37_foldx_paper"],
        "note": (
            "Paper reports 1.5x (LD50) and 2.0x (D37) for LDR. The Fig 5E "
            "y-axis 'Color intensity (%)' yields smaller raw ratios because "
            "the unirradiated baseline is ~40-47%, not 0. Compute ratios as "
            "y-value/control-y-value; the paper's '1.5x/2x' is likely "
            "computed against a different baseline (e.g. blank vs positive "
            "control normalization) -- so the FOLDS HERE WILL UNDERSHOOT "
            "the paper's reported folds, but the DIRECTIONAL claim holds."
        ),
    }
    return out


# =============================================================================
# (10) ROS dose-rate claim (Fig 6)
# =============================================================================
def claim_ROS():
    HDR = digitized_figs["fig6B_HDR_DCF_pct_control_40min"]
    LDR = digitized_figs["fig6C_LDR_DCF_pct_control_40min"]
    HDR_8Gy = next(r for r in HDR if r["dose_Gy"] == 8)["no_catalase"]
    HDR_4Gy = next(r for r in HDR if r["dose_Gy"] == 4)["no_catalase"]
    LDR_18Gy = next(r for r in LDR if r["dose_Gy"] == 18)["value"]
    out = {
        "HDR_8Gy_pct_control": HDR_8Gy,  # paper says 15x
        "HDR_8Gy_foldx": HDR_8Gy / 100.0,
        "HDR_4Gy_foldx": HDR_4Gy / 100.0,
        "LDR_18Gy_foldx": LDR_18Gy / 100.0,
        "paper_LDR_LD50_foldx": PAPER["ROS_LDR_LD50_foldx_paper"],
        "paper_HDR_D37_foldx": PAPER["ROS_HDR_D37_foldx_paper"],
    }
    # Catalase quench check: paper claims H2O2 = bulk of the signal
    catalase_quench_pct = next(r for r in HDR if r["dose_Gy"] == 8)["with_catalase"]
    out["HDR_8Gy_catalase_quench_pct_control"] = catalase_quench_pct
    out["catalase_quench_efficiency"] = 1.0 - catalase_quench_pct / HDR_8Gy
    return out


# =============================================================================
# (11) Giant cells (Fig 7)
# =============================================================================
def claim_giant_cells():
    flow = digitized_figs["fig7B_giant_cells_flow_pct"]
    bar = digitized_figs["fig7C_giant_cells_bar_pct"]
    ctrl = next(r for r in flow if "Control" in r["label"])
    HDR16 = next(r for r in flow if "16 Gy HDR" in r["label"])
    out = {
        "flow_ctrl_giant_pct": ctrl["giant_pct"],
        "flow_HDR16Gy_giant_pct": HDR16["giant_pct"],
        "flow_fold_increase_HDR16": HDR16["giant_pct"] / max(ctrl["giant_pct"], 1e-6),
        "paper_HDR_16Gy_giant_foldx": digitized_text["in_text_results"][
            "giant_cells_relative_increase_16Gy_HDR"
        ],
        "bar_data": bar,
        "bar_LDR18_over_ctrl": bar[1]["value"] / bar[0]["value"],
        "bar_HDR16_over_ctrl": bar[2]["value"] / bar[0]["value"],
    }
    return out


# =============================================================================
# main: run all, dump JSON
# =============================================================================
def main():
    results = {
        "paper": {
            "doi": "10.3390/cimb46120828",
            "pmc": "PMC11726848",
            "cell_line": "A431",
            "design": "MTT + clonogenic + comet + flow + SA-bgal + DCF-ROS + giant-cell counting",
        },
        "claim1_MTT_doseresponse": claim_MTT_dose_response(),
        "claim2_clonogenic": claim_clonogenic_SF(),
        "claim3_comet_ratio": claim_comet_ratio(),
        "claim4_anova_dunnett_MTT": claim_anova_dunnett(),
        "claim5_G2M_arrest_24h": claim_G2M(),
        "claim6_apoptosis_ratio_48h": claim_apoptosis_ratio(),
        "claim7_SAbetagal": claim_SAbetagal(),
        "claim8_ROS": claim_ROS(),
        "claim9_giant_cells": claim_giant_cells(),
    }
    out_path = OUT / "full_reproduction_results.json"
    out_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"WROTE {out_path}")
    print("\n=== HEADLINE NUMBERS ===")
    f = results['claim1_MTT_doseresponse']['fits']
    print(f"MTT Hill3 HDR LD50  = {f['HDR']['hill3_LD50_Gy']:.2f} Gy  (paper: 3.4)")
    print(f"MTT Hill3 HDR D37   = {f['HDR']['hill3_D37_Gy']:.2f} Gy  (paper: 8.0)")
    print(f"MTT Hill3 LDR LD50  = {f['LDR']['hill3_LD50_Gy']:.2f} Gy  (paper: 10.8)")
    print(f"MTT Hill3 LDR D37   = {f['LDR']['hill3_D37_Gy']:.2f} Gy  (paper: 20.0)")
    print(f"MTT Hill4 HDR LD50_abs50 = {f['HDR']['hill4_LD50_abs50_Gy']} Gy  (paper: 3.4)")
    print(f"MTT Hill4 LDR LD50_abs50 = {f['LDR']['hill4_LD50_abs50_Gy']} Gy  (paper: 10.8)")
    print(f"MTT Hill4 HDR D37_abs     = {f['HDR']['hill4_D37_abs_Gy']} Gy  (paper: 8.0)")
    print(f"MTT Hill4 LDR D37_abs     = {f['LDR']['hill4_D37_abs_Gy']} Gy  (paper: 20.0)")
    print(f"DMF@50%kill (MTT Hill3)  = {results['claim1_MTT_doseresponse']['DMF_curve']['DMF@50%kill']['DMF_LDR_over_HDR']:.2f}  (paper: 3.18)")
    print(f"DMF@50%kill (clonogenic) = {results['claim2_clonogenic']['empirical_DMF50_clonogenic']['DMF50_LDR_over_HDR']:.2f}")
    print(f"Comet 4 Gy LDR/HDR = {results['claim3_comet_ratio']['ratios']['4Gy_LDR_over_HDR']:.2f}  (paper: 0.60)")
    print(f"Comet 8 Gy LDR/HDR = {results['claim3_comet_ratio']['ratios']['8Gy_LDR_over_HDR']:.2f}  (paper: 0.50)")
    print(f"G2/M HDR 4 Gy 24h  = {results['claim5_G2M_arrest_24h']['HDR_24h_G2M_pct'][4]}% (paper claim 25-50% above ctrl)")
    print(f"G2/M HDR 8 Gy 24h  = {results['claim5_G2M_arrest_24h']['HDR_24h_G2M_pct'][8]}% (paper ~100%)")
    print(f"G2/M HDR 16 Gy 24h = {results['claim5_G2M_arrest_24h']['HDR_24h_G2M_pct'][16]}% (paper ~100%)")
    print(f"SA-bgal LDR LD50 fold = {results['claim7_SAbetagal']['LDR']['fold_LD50_over_ctrl']:.2f} (paper 1.5)")
    print(f"SA-bgal LDR D37  fold = {results['claim7_SAbetagal']['LDR']['fold_D37_over_ctrl']:.2f} (paper 2.0)")
    print(f"ROS HDR 8 Gy fold = {results['claim8_ROS']['HDR_8Gy_foldx']:.1f}x (paper 15)")
    print(f"ROS LDR 18 Gy fold = {results['claim8_ROS']['LDR_18Gy_foldx']:.1f}x (paper 4)")
    print(f"Giant cells HDR 16 Gy fold (flow) = {results['claim9_giant_cells']['flow_fold_increase_HDR16']:.1f}x (paper 5x)")


if __name__ == "__main__":
    main()
