#!/usr/bin/env python3
"""
LUCID100 slot-58 smoke replication for:
  Soroko et al. 2024, "The Dose Rate of Corpuscular Ionizing Radiation Strongly
  Influences the Severity of DNA Damage, Cell Cycle Progression and Cellular
  Senescence in Human Epidermoid Carcinoma Cells" -- Curr. Issues Mol. Biol.
  46(12):13860-13880, DOI 10.3390/cimb46120828, PMC11726848 (CC BY 4.0).

The paper is wet-lab radiobiology (A431, MTT/comet/flow/SA-beta-gal). The
authors release no underlying numeric tables or code. What we *can*
replicate from public information alone:

  (1) The two reported survival "anchor points" per regime:
        HDR (600 Gy/h, 6 MeV e-): LD50 = 3.4 Gy,  D37 ~= 8 Gy
        LDR (0.5-3 Gy/h, 90Sr+90Y beta):
                                   LD50 = 10.8 Gy, D37 ~= 20 Gy
      LD50 here is the dose at which the MTT-counted viable fraction is 0.5
      relative to unirradiated control; D37 is the dose at which it falls to
      1/e (0.368). We assume the authors use that conventional definition.
  (2) Fit a Linear-Quadratic (LQ) survival model
            SF(D) = exp(-alpha D - G beta D^2),
      where G is the Lea-Catcheside protraction factor. For an instantaneous
      acute exposure (HDR) G=1; for an LDR exposure of duration t with a
      single-exponential sublethal-damage repair rate mu, the closed form is
            G(t) = 2 / (mu t)^2 * (mu t - 1 + exp(-mu t)).
      With t_LDR = 24 h fixed and a literature-typical repair half-time of
      ~1 h (mu = ln(2)/0.5 - ln(2)/2 h^-1; we sweep) we get G(t) << 1, which
      is what drives the dose-rate sparing effect the authors observe.
  (3) Solve for (alpha, beta) from the two HDR anchors, then compute the
      LDR dose-rate-modifying factor (DRMF):
            DRMF(D_LDR; D_HDR_iso) = D_LDR_isoeffect / D_HDR_isoeffect
      and compare to the empirical DRMF = 3.18 (LD50) and 2.5 (D37).
  (4) Translate to comet-tail DNA damage: the linear-track model predicts
      DSB yield proportional to alpha D for both regimes, so the LDR-to-HDR
      DSB ratio at equal physical dose should equal alpha_LDR/alpha_HDR. The
      authors measure tail % 4 Gy: LDR 3 vs HDR 5  -> 0.60, and 8 Gy: LDR 4
      vs HDR 8 -> 0.50, i.e. an LDR/HDR ratio ~= 0.55. Check whether this is
      consistent with the LQ-derived (alpha, beta).

This is a "light analytical replication" -- it does NOT recompute the wet-lab
endpoints (cell cycle, SA-beta-gal, ROS, giant cells, AnnV/PI) which require
actual irradiation and assays.

Outputs:
  outputs/fig_lq_survival.png      dose-response curves overlaid on anchors
  outputs/fig_drmf_vs_repair.png   DRMF vs repair half-time mu
  outputs/fig_comet_ratio.png      LDR/HDR DNA-break ratio vs dose
  outputs/smoke_summary.json       quantitative results, paper claims, deltas

Runs in well under 1 s on CPU, no GPU/HPC needed. Safe on CherryRd.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
OUTDIR = HERE.parent / "outputs"
OUTDIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Anchor points (digitized from paper text, not from a table)
# ---------------------------------------------------------------------------
ANCHORS = {
    "HDR": {"LD50": 3.4, "D37": 8.0, "G": 1.0, "dose_rate_Gy_per_h": 600.0,
            "duration_h": None, "particle": "6 MeV electrons"},
    "LDR": {"LD50": 10.8, "D37": 20.0,
            # representative dose rate; exposure fixed at 24 h
            "dose_rate_Gy_per_h_range": (0.25, 3.0),
            "duration_h": 24.0,
            "particle": "Sr-90+Y-90 betas"},
}
SF_LD50 = 0.50
SF_D37 = 1.0 / math.e


def G_factor(t_hours: float, mu_per_hour: float) -> float:
    """Lea-Catcheside protraction factor for a uniform exposure of duration t
    with single-exponential sublethal damage repair rate mu."""
    if mu_per_hour <= 0 or t_hours <= 0:
        return 1.0
    x = mu_per_hour * t_hours
    return 2.0 / (x * x) * (x - 1.0 + math.exp(-x))


def fit_alpha_beta_from_two_points(D1: float, SF1: float,
                                    D2: float, SF2: float,
                                    G: float = 1.0):
    """Solve  -ln SF = alpha*D + G*beta*D^2  for two (D, SF) pairs."""
    y1 = -math.log(SF1)
    y2 = -math.log(SF2)
    # alpha*D1 + G*beta*D1^2 = y1
    # alpha*D2 + G*beta*D2^2 = y2
    M = np.array([[D1, G * D1 * D1], [D2, G * D2 * D2]])
    rhs = np.array([y1, y2])
    sol = np.linalg.solve(M, rhs)
    return float(sol[0]), float(sol[1])  # alpha, beta


def isoeffective_dose(SF: float, alpha: float, beta: float, G: float) -> float:
    """Solve SF = exp(-alpha D - G*beta D^2) for D >= 0."""
    y = -math.log(SF)
    if beta * G <= 0:
        return y / alpha
    a, b, c = beta * G, alpha, -y
    disc = b * b - 4 * a * c
    return (-b + math.sqrt(disc)) / (2 * a)


def main() -> dict:
    # --- 1) Fit HDR LQ from the two HDR anchors (G=1)
    alpha_H, beta_H = fit_alpha_beta_from_two_points(
        ANCHORS["HDR"]["LD50"], SF_LD50,
        ANCHORS["HDR"]["D37"], SF_D37, G=1.0,
    )

    # --- 2) Fit LDR LQ from the two LDR anchors, with the LQ G-factor
    # We sweep repair half-times t12 in {0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0} h
    # (literature DSB repair: 0.5-1.5 h fast pathway, 4-8 h slow pathway).
    t_LDR = ANCHORS["LDR"]["duration_h"]
    t12_grid = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0])
    sweep = []
    for t12 in t12_grid:
        mu = math.log(2.0) / t12
        G = G_factor(t_LDR, mu)
        a_L, b_L = fit_alpha_beta_from_two_points(
            ANCHORS["LDR"]["LD50"], SF_LD50,
            ANCHORS["LDR"]["D37"], SF_D37, G=G,
        )
        sweep.append({
            "t_half_h": float(t12),
            "mu_per_h": mu,
            "G_factor": G,
            "alpha_LDR": a_L, "beta_LDR": b_L,
            "alpha_LDR_over_alpha_HDR": a_L / alpha_H,
            "beta_LDR_over_beta_HDR": b_L / beta_H if beta_H else float("nan"),
        })

    # --- 3) DRMF: if cells respond with the SAME intrinsic (alpha, beta) under
    # both regimes, the dose-rate sparing must come from G<1 alone. Use the
    # HDR LQ as the "intrinsic" and compute the LDR dose required for the
    # same SF given each t12. Compare predicted LDR LD50 to observed 10.8.
    drmf = []
    for t12 in t12_grid:
        mu = math.log(2.0) / t12
        G = G_factor(t_LDR, mu)
        pred_LD50 = isoeffective_dose(SF_LD50, alpha_H, beta_H, G)
        pred_D37 = isoeffective_dose(SF_D37, alpha_H, beta_H, G)
        drmf.append({
            "t_half_h": float(t12), "G": G,
            "predicted_LDR_LD50_Gy": pred_LD50,
            "predicted_LDR_D37_Gy": pred_D37,
            "drmf_LD50": pred_LD50 / ANCHORS["HDR"]["LD50"],
            "drmf_D37": pred_D37 / ANCHORS["HDR"]["D37"],
        })
    observed_drmf = {
        "LD50": ANCHORS["LDR"]["LD50"] / ANCHORS["HDR"]["LD50"],
        "D37": ANCHORS["LDR"]["D37"] / ANCHORS["HDR"]["D37"],
    }
    # Best-fit t12 (minimize sum-squared log of DRMF mismatch)
    losses = []
    for d in drmf:
        ll = (math.log(d["drmf_LD50"]) - math.log(observed_drmf["LD50"])) ** 2 \
             + (math.log(d["drmf_D37"]) - math.log(observed_drmf["D37"])) ** 2
        losses.append(ll)
    best_idx = int(np.argmin(losses))
    best_fit = drmf[best_idx]
    # Fine grid around best
    fine_t12 = np.linspace(0.1, 16.0, 800)
    fine_drmf_LD50 = []
    fine_drmf_D37 = []
    for t12 in fine_t12:
        mu = math.log(2.0) / t12
        G = G_factor(t_LDR, mu)
        fine_drmf_LD50.append(isoeffective_dose(SF_LD50, alpha_H, beta_H, G) / ANCHORS["HDR"]["LD50"])
        fine_drmf_D37.append(isoeffective_dose(SF_D37, alpha_H, beta_H, G) / ANCHORS["HDR"]["D37"])
    fine_drmf_LD50 = np.array(fine_drmf_LD50)
    fine_drmf_D37 = np.array(fine_drmf_D37)
    # Best fine t12 for combined target
    fine_loss = (np.log(fine_drmf_LD50) - math.log(observed_drmf["LD50"])) ** 2 \
                + (np.log(fine_drmf_D37) - math.log(observed_drmf["D37"])) ** 2
    fine_best_idx = int(np.argmin(fine_loss))
    fine_best_t12 = float(fine_t12[fine_best_idx])
    fine_best_G = G_factor(t_LDR, math.log(2.0) / fine_best_t12)

    # --- 4) Comet-tail ratio: under shared (alpha,beta) the LDR/HDR equal-dose
    # surviving-fraction is exp((alpha + beta*D)*D*(1-G)). DSB yield in this
    # framework is proportional to alpha*D (so LDR/HDR DSB ratio at equal D
    # would be 1.0). The paper instead reports an observable difference --
    # 4 Gy: LDR 3% vs HDR 5%; 8 Gy: LDR 4% vs HDR 8% (LDR/HDR ~= 0.6, 0.5).
    # That suggests breaks are also rejoined during the 24-h LDR exposure, so
    # we model the *residual* break fraction at the end of exposure as
    #         f_res(t, mu) = (1 - exp(-mu t)) / (mu t)
    # which is the standard repaired-during-exposure correction. Compare for
    # the best-fit mu.
    mu_best = math.log(2.0) / fine_best_t12
    f_res = (1.0 - math.exp(-mu_best * t_LDR)) / (mu_best * t_LDR)
    comet_pred_LDR_over_HDR_ratio = f_res  # at any dose
    observed_comet_ratio = {
        "4Gy": 3 / 5,
        "8Gy": 4 / 8,
        "mean": np.mean([3 / 5, 4 / 8]),
    }

    # --- Plots
    # (a) Survival curves
    D = np.linspace(0, 32, 400)
    SF_H = np.exp(-alpha_H * D - beta_H * D * D)
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.semilogy(D, SF_H, "C0-", lw=2, label=f"HDR LQ fit (alpha={alpha_H:.3f}, beta={beta_H:.4f})")
    SF_L = np.exp(-alpha_H * D - fine_best_G * beta_H * D * D)
    ax.semilogy(D, SF_L, "C3--", lw=2,
                label=(f"LDR LQ pred (G={fine_best_G:.3f}, "
                       f"t1/2={fine_best_t12:.2f} h)"))
    ax.plot([ANCHORS["HDR"]["LD50"], ANCHORS["HDR"]["D37"]],
            [SF_LD50, SF_D37], "C0o", ms=8, label="HDR anchors")
    ax.plot([ANCHORS["LDR"]["LD50"], ANCHORS["LDR"]["D37"]],
            [SF_LD50, SF_D37], "C3s", ms=8, label="LDR anchors")
    ax.axhline(SF_LD50, color="grey", lw=0.6, ls=":")
    ax.axhline(SF_D37, color="grey", lw=0.6, ls=":")
    ax.set_xlabel("Dose D (Gy)")
    ax.set_ylabel("Surviving fraction SF (MTT-relative)")
    ax.set_ylim(0.02, 1.05)
    ax.set_title("Soroko et al. 2024 -- LQ smoke fit\n(shared intrinsic LQ + Lea-Catcheside protraction)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUTDIR / "fig_lq_survival.png", dpi=130)
    plt.close(fig)

    # (b) DRMF vs repair half-time
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(fine_t12, fine_drmf_LD50, "C0-", lw=2, label="DRMF at SF=0.5 (LD50)")
    ax.plot(fine_t12, fine_drmf_D37, "C1-", lw=2, label="DRMF at SF=1/e (D37)")
    ax.axhline(observed_drmf["LD50"], color="C0", ls="--", lw=1,
               label=f"observed LD50 DRMF = {observed_drmf['LD50']:.2f}")
    ax.axhline(observed_drmf["D37"], color="C1", ls="--", lw=1,
               label=f"observed D37 DRMF  = {observed_drmf['D37']:.2f}")
    ax.axvline(fine_best_t12, color="grey", ls=":", lw=1,
               label=f"best-fit t1/2 = {fine_best_t12:.2f} h")
    ax.set_xlabel("Sublethal damage repair half-time t1/2 (h)")
    ax.set_ylabel("Predicted LDR/HDR isoeffective-dose ratio (DRMF)")
    ax.set_xscale("log")
    ax.set_title("DRMF vs repair kinetics (HDR LQ assumed intrinsic, t_LDR=24 h)")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUTDIR / "fig_drmf_vs_repair.png", dpi=130)
    plt.close(fig)

    # (c) Comet ratio sanity plot
    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    t12_for_plot = np.linspace(0.25, 16, 400)
    fres_arr = []
    for t12 in t12_for_plot:
        mu = math.log(2.0) / t12
        fres_arr.append((1.0 - math.exp(-mu * t_LDR)) / (mu * t_LDR))
    fres_arr = np.array(fres_arr)
    ax.plot(t12_for_plot, fres_arr, "C2-", lw=2, label="f_res = (1-e^{-mu t})/(mu t)")
    ax.axhline(observed_comet_ratio["mean"], color="grey", ls="--",
               label=f"observed LDR/HDR comet ratio ~= {observed_comet_ratio['mean']:.2f}")
    ax.axvline(fine_best_t12, color="grey", ls=":",
               label=f"survival-fit t1/2 = {fine_best_t12:.2f} h")
    ax.set_xlabel("Break-rejoining half-time during exposure (h)")
    ax.set_ylabel("Residual break fraction at end of 24 h LDR")
    ax.set_xscale("log")
    ax.set_title("Comet-tail LDR/HDR ratio under continuous repair")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUTDIR / "fig_comet_ratio.png", dpi=130)
    plt.close(fig)

    # --- 5) Alternative: a Hill / log-logistic model for MTT-relative viable
    # fraction. Two anchor points (LD50, D37) under-determine a 2-parameter
    # LQ for genuine survival because LD50=3.4 and D37=8 (HDR) imply only a
    # 1.36x drop across a 2.35x dose increase, which is much shallower than
    # exp(-alpha D). That shallowness is consistent with MTT readouts being
    # bounded by mitochondrial activity per surviving cell rather than
    # clonogenicity. A Hill curve V(D) = 1 / (1 + (D/LD50)^n) anchored at
    # the two reported points is the simplest descriptive surrogate. With
    # V(LD50)=0.5 by definition, n is fixed by V(D37)=1/e:
    #     1/(1 + (D37/LD50)^n) = 1/e   ->   (D37/LD50)^n = e - 1 = 1.718
    #     n = ln(1.718) / ln(D37/LD50)
    def hill_fit(LD50, D37):
        n = math.log(math.e - 1.0) / math.log(D37 / LD50)
        return n
    n_HDR = hill_fit(ANCHORS["HDR"]["LD50"], ANCHORS["HDR"]["D37"])
    n_LDR = hill_fit(ANCHORS["LDR"]["LD50"], ANCHORS["LDR"]["D37"])

    # Plot Hill alternative
    fig, ax = plt.subplots(figsize=(6, 4.2))
    D2 = np.linspace(0.1, 40, 400)
    V_H = 1.0 / (1.0 + (D2 / ANCHORS["HDR"]["LD50"]) ** n_HDR)
    V_L = 1.0 / (1.0 + (D2 / ANCHORS["LDR"]["LD50"]) ** n_LDR)
    ax.plot(D2, V_H, "C0-", lw=2, label=f"HDR Hill (n={n_HDR:.2f}, LD50={ANCHORS['HDR']['LD50']} Gy)")
    ax.plot(D2, V_L, "C3-", lw=2, label=f"LDR Hill (n={n_LDR:.2f}, LD50={ANCHORS['LDR']['LD50']} Gy)")
    ax.plot([ANCHORS["HDR"]["LD50"], ANCHORS["HDR"]["D37"]],
            [SF_LD50, SF_D37], "C0o", ms=8)
    ax.plot([ANCHORS["LDR"]["LD50"], ANCHORS["LDR"]["D37"]],
            [SF_LD50, SF_D37], "C3s", ms=8)
    ax.set_xlabel("Dose D (Gy)")
    ax.set_ylabel("MTT-relative viable fraction V")
    ax.set_title("Hill / log-logistic descriptive fit (MTT readout)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTDIR / "fig_hill_mtt.png", dpi=130)
    plt.close(fig)

    summary = {
        "paper": {
            "doi": "10.3390/cimb46120828",
            "pmc": "PMC11726848",
            "license": "CC BY 4.0",
        },
        "worktype_master_tsv": "simulation/model replication",
        "worktype_actual": "wet-lab radiobiology (A431 cells, 6 MeV e- and Sr/Y-90 betas, MTT/comet/flow/SA-beta-gal/ROS)",
        "qa_retag_recommendation": "RETAG worktype: wet-lab assay/radiobiology (dose-rate effect study).",
        "anchors": ANCHORS,
        "fit": {
            "HDR_LQ_alpha_per_Gy": alpha_H,
            "HDR_LQ_beta_per_Gy2": beta_H,
            "HDR_alpha_over_beta_Gy": alpha_H / beta_H if beta_H else None,
        },
        "LDR_LQ_sweep_over_t_half": sweep,
        "DRMF_vs_t_half": drmf,
        "DRMF_observed": observed_drmf,
        "DRMF_best_fit": {
            "t_half_h": fine_best_t12,
            "G_factor": fine_best_G,
            "predicted_LDR_LD50_Gy": float(isoeffective_dose(SF_LD50, alpha_H, beta_H, fine_best_G)),
            "predicted_LDR_D37_Gy": float(isoeffective_dose(SF_D37, alpha_H, beta_H, fine_best_G)),
        },
        "hill_fit_descriptive": {
            "note": "Two-point analytical Hill V(D)=1/(1+(D/LD50)^n); anchors LD50 and D37 fix LD50 and n.",
            "HDR": {"LD50_Gy": ANCHORS["HDR"]["LD50"], "hill_n": n_HDR},
            "LDR": {"LD50_Gy": ANCHORS["LDR"]["LD50"], "hill_n": n_LDR},
            "DMF_LD50_LDR_over_HDR": ANCHORS["LDR"]["LD50"] / ANCHORS["HDR"]["LD50"],
        },
        "comet_check": {
            "observed_LDR_over_HDR_4Gy": observed_comet_ratio["4Gy"],
            "observed_LDR_over_HDR_8Gy": observed_comet_ratio["8Gy"],
            "observed_LDR_over_HDR_mean": observed_comet_ratio["mean"],
            "predicted_residual_break_fraction_at_best_t_half": comet_pred_LDR_over_HDR_ratio,
            "best_t_half_h": fine_best_t12,
        },
        "interpretation": (
            "FINDING: A shared-intrinsic LQ + Lea-Catcheside protraction model "
            "CANNOT simultaneously reproduce the paper's reported HDR "
            f"(LD50={ANCHORS['HDR']['LD50']}, D37={ANCHORS['HDR']['D37']}) and LDR "
            f"(LD50={ANCHORS['LDR']['LD50']}, D37={ANCHORS['LDR']['D37']}) anchor points: the HDR "
            f"two-point LQ fit returns a negative beta (alpha={alpha_H:.3f}, "
            f"beta={beta_H:.4f}). The reason is that an HDR drop from SF=0.5 at "
            "3.4 Gy to SF=1/e at 8 Gy is a 1.36x decrease over a 2.35x dose "
            "increase -- much shallower than a plain exponential exp(-alpha D), "
            "let alone a downward-bending LQ shoulder. This is *very* unusual "
            "for clonogenic survival, and is consistent with the authors' own "
            "caveat that MTT readouts at 72 h conflate cell number, "
            "metabolic activity per cell, and cell-cycle arrest. The simplest "
            "descriptive model that fits both anchors per regime is a Hill / "
            f"log-logistic V(D) = 1/(1+(D/LD50)^n) with n_HDR={n_HDR:.2f} and "
            f"n_LDR={n_LDR:.2f}. Under this descriptive picture, the dose-modifying "
            f"factor at 50% viability is the clean ratio {observed_drmf['LD50']:.2f}, "
            "matching the paper's stated 3x sparing factor. Separately, the "
            "end-of-exposure residual break fraction (1-exp(-mu t))/(mu t) "
            "that would explain the LDR-vs-HDR comet ratio of ~0.55 requires a "
            "break-rejoining half-time of ~10-14 h (slow-component-only), not "
            "the fast 0.3-1.5 h commonly reported. So the comet data and the "
            "MTT-derived 'survival' data point to different physical regimes "
            "and probably should be modeled separately. Net: the headline 3x "
            "sparing is reproduced trivially as an empirical ratio; a single "
            "unifying biophysical model is not, and any future replication "
            "should ask the authors for the underlying MTT and comet tables."
        ),
        "limitations": [
            "Only two survival anchor points (LD50, D37) per regime were available -- the full MTT curves themselves were not released as numeric tables, so the LQ fit is exact-through-two-points rather than a real fit.",
            "G2/M arrest, SA-beta-gal, ROS, AnnV/PI, giant cells are all wet-lab endpoints with no closed-form smoke surrogate.",
            "alpha/beta units depend on the (questionable) assumption that MTT-relative viable cell counts at 72 h are a fair proxy for clonogenic survival; the paper itself flags MTT vs clonogenic differences."
        ],
    }
    with open(OUTDIR / "smoke_summary.json", "w") as f:
        json.dump(summary, f, indent=2, sort_keys=False, default=float)
    return summary


if __name__ == "__main__":
    s = main()
    print(json.dumps({
        "HDR_alpha": s["fit"]["HDR_LQ_alpha_per_Gy"],
        "HDR_beta": s["fit"]["HDR_LQ_beta_per_Gy2"],
        "HDR_alphaBeta_Gy": s["fit"]["HDR_alpha_over_beta_Gy"],
        "best_t_half_h": s["DRMF_best_fit"]["t_half_h"],
        "best_G": s["DRMF_best_fit"]["G_factor"],
        "predicted_LDR_LD50": s["DRMF_best_fit"]["predicted_LDR_LD50_Gy"],
        "predicted_LDR_D37": s["DRMF_best_fit"]["predicted_LDR_D37_Gy"],
        "observed_LDR_LD50": 10.8,
        "observed_LDR_D37": 20.0,
        "comet_LDR_over_HDR_mean": s["comet_check"]["observed_LDR_over_HDR_mean"],
        "comet_LDR_over_HDR_predicted": s["comet_check"]["predicted_residual_break_fraction_at_best_t_half"],
    }, indent=2))
