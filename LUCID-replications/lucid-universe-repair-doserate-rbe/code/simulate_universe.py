"""Driver: reproduce the headline trends of Liew et al. 2022.

Outputs (under ../results/ and ../figures/):

  - fig1_proton_rbe_vs_doserate_moderate.json   (Figure 1 analogue)
  - fig2_proton_rbe_vs_doserate_high.json       (Figure 2 analogue)
  - table2_max_relative_difference.json/csv     (Table 2)
  - fig3_sensitivity.json                       (Figure 3 left+right panels)
  - fig4_R_TD50.json                            (Figure 4 left panel + Table 3 R_TD50)
  - fig5_RBE_benchmark.json                     (Figure 4 middle/right + Figure 5)

Figures are saved as PNG with the same stem.

All numbers are formula-level reproductions; raw FLUKA SOBP / TD50 fits are not
available, so SOBP dose-rate values are taken from Table 3 of the paper and
the measured RBE points are reproduced from the paper-quoted MADs.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from universe_core import (
    PARAMS_DU145,
    PARAMS_RSC_NO_REPAIR,
    PARAMS_RSC_WITH_REPAIR,
    survival_no_repair,
    survival_with_repair,
    dose_for_survival,
    CellParams,
    LN2,
)
from kiefer_chatterjee import survival_ion_no_repair


RESULTS = HERE.parent / "results"
FIGURES = HERE.parent / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

DEFAULT_SEED = 20260529


# ---------------------------------------------------------------------------
# Plot helpers (optional matplotlib)
# ---------------------------------------------------------------------------
def _maybe_import_pyplot():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except Exception as e:
        print(f"[warn] matplotlib unavailable: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Ion + repair survival (combines the two modules)
# ---------------------------------------------------------------------------
def survival_ion_with_repair(
    dose_Gy: float,
    dose_rate_Gy_per_min: float,
    LET_keV_um: float,
    particle: str,
    params: CellParams,
    nucleus_radius_um: float = 5.0,
    n_iter: int = 600,
    n_time_steps: int = 50,
    rng: np.random.Generator | None = None,
) -> float:
    """Approximate the dose-rate effect on ion survival.

    Strategy (consistent with the paper's GPU implementation): split the total
    dose into N_t fractions, generate the DSB pattern for each fraction with
    the same tools used by survival_ion_no_repair, then apply the repair
    kinetics on the cumulative damage pattern.  As a fast approximation we
    factorize the dose-rate dependence as

        S(D, D_dot) = S_norepair(D) ** g(D_dot, D, half_lives, params)

    where g is the dose-rate suppression factor derived from the photon
    Eq. (5)/repair MC.  At low dose-rates g < 1 (lots of repair), at high
    dose-rates g -> 1 (no repair).  We compute g by comparing photon survival
    at the same dose between the no-repair limit and the requested dose rate.

    This factorization is exact under the assumption that ion-induced DSB
    repair with the same half-lives as photon-induced DSB, which is the
    assumption used throughout the paper.
    """
    rng = rng or np.random.default_rng()
    S_ion0 = survival_ion_no_repair(
        dose_Gy, LET_keV_um, particle, params,
        nucleus_radius_um=nucleus_radius_um, n_iter=n_iter, rng=rng,
    )
    # Photon repair correction at the same dose & dose-rate
    S_ph_norep = survival_no_repair(
        dose_Gy, params, n_iter=max(n_iter * 4, 2000), rng=rng,
    )
    S_ph_rep = survival_with_repair(
        dose_Gy, dose_rate_Gy_per_min, params,
        n_iter=max(n_iter * 2, 1500), n_time_steps=n_time_steps, rng=rng,
    )
    # Express ion survival assuming the same fractional repair suppression
    if S_ph_norep <= 0 or S_ion0 <= 0:
        return S_ion0
    # log(S_ph_rep) / log(S_ph_norep) is the "g" exponent; we apply it to ion
    g = np.log(max(S_ph_rep, 1e-12)) / np.log(max(S_ph_norep, 1e-12))
    return float(S_ion0 ** g)


# ---------------------------------------------------------------------------
# Figure 1 / 2 / Table 2: RBE vs dose-rate
# ---------------------------------------------------------------------------
def proton_rbe_curves(
    dose_grid: list[float],
    LET_list: list[float],
    dose_rate_Gy_per_s: list[float],
    ref_dose_rate_Gy_per_min: float = 2.0,
    target_S: float = 0.1,    # ignored when use_iso_dose=True
    params: CellParams = PARAMS_DU145,
    n_iter: int = 800,
    rng: np.random.Generator | None = None,
) -> dict:
    """For each (dose, LET) point, sweep the proton dose-rate and compute
    fixed-reference RBE, dose-rate adapted RBE, and no-repair RBE.

    RBE here follows the paper's iso-effect definition.  At each dose D and
    dose-rate D_dot, we:
      1. compute ion survival S_ion(D, D_dot, LET)
      2. find the photon dose D_ph such that S_ph(D_ph, ref-or-adapted rate) = S_ion
      3. RBE = D_ph / D
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED)
    results = {"doses_Gy": dose_grid, "LETs_keV_um": LET_list,
               "dose_rates_Gy_per_s": dose_rate_Gy_per_s,
               "ref_dose_rate_Gy_per_min": ref_dose_rate_Gy_per_min,
               "curves": {}}

    # Photon dose at reference rate, as a callable
    def photon_dose_for_survival_at_rate(S_target, rate_Gy_per_min, max_iter=18, tol=8e-3):
        return dose_for_survival(
            S_target,
            lambda Dx, dm=rate_Gy_per_min: survival_with_repair(
                Dx, dm, params, n_iter=900, n_time_steps=25, rng=rng),
            d_lo=0.1, d_hi=40, max_iter=max_iter, tol=tol,
        )

    def photon_dose_for_survival_norep(S_target, max_iter=20, tol=5e-3):
        return dose_for_survival(
            S_target,
            lambda Dx: survival_no_repair(Dx, params, n_iter=3000, rng=rng),
            d_lo=0.1, d_hi=40, max_iter=max_iter, tol=tol,
        )

    # Sweep over LET, D, D_dot
    for LET in LET_list:
        for D in dose_grid:
            key = f"LET={LET}_D={D}"
            curve = {"dose_rate_Gy_per_s": dose_rate_Gy_per_s,
                     "fixed_reference_RBE": [],
                     "dose_rate_adapted_RBE": [],
                     "no_repair_RBE": None,
                     "S_ion": [],
                     "S_ion_norep": None}
            # No-repair ion survival at this (D, LET)
            S_ion_norep = survival_ion_no_repair(
                D, LET, "proton", params, n_iter=700, rng=rng,
            )
            curve["S_ion_norep"] = float(S_ion_norep)
            # No-repair photon dose for this survival -> no-repair RBE
            if 0 < S_ion_norep < 1:
                Dph_norep_match = photon_dose_for_survival_norep(S_ion_norep)
                curve["no_repair_RBE"] = float(Dph_norep_match / D)
            else:
                curve["no_repair_RBE"] = float("nan")

            for D_dot in dose_rate_Gy_per_s:
                D_dot_min = D_dot * 60.0
                S_ion = survival_ion_with_repair(
                    D, D_dot_min, LET, "proton", params,
                    n_iter=300, n_time_steps=25, rng=rng,
                )
                curve["S_ion"].append(float(S_ion))
                if not (0 < S_ion < 1):
                    curve["fixed_reference_RBE"].append(float("nan"))
                    curve["dose_rate_adapted_RBE"].append(float("nan"))
                    continue
                Dph_fix = photon_dose_for_survival_at_rate(
                    S_ion, ref_dose_rate_Gy_per_min)
                Dph_adapt = photon_dose_for_survival_at_rate(
                    S_ion, D_dot_min)
                curve["fixed_reference_RBE"].append(
                    float(Dph_fix / D) if Dph_fix > 0 else float("nan"))
                curve["dose_rate_adapted_RBE"].append(
                    float(Dph_adapt / D) if Dph_adapt > 0 else float("nan"))
            results["curves"][key] = curve
            print(f"  [{key}] no-repair RBE = {curve['no_repair_RBE']:.3f}  "
                  f"fixed-ref range = [{min(curve['fixed_reference_RBE']):.3f}, "
                  f"{max(curve['fixed_reference_RBE']):.3f}]")

    return results


# ---------------------------------------------------------------------------
# Table 2: max relative difference fixed-reference vs no-repair RBE at saturation
# ---------------------------------------------------------------------------
def build_table2(curves_data: dict) -> dict:
    """Compute (FixedRef_RBE_max - NoRepair_RBE) / NoRepair_RBE on the (D, LET) grid."""
    table = {"doses_Gy": curves_data["doses_Gy"],
             "LETs_keV_um": curves_data["LETs_keV_um"],
             "matrix": []}
    for D in curves_data["doses_Gy"]:
        row = []
        for LET in curves_data["LETs_keV_um"]:
            key = f"LET={LET}_D={D}"
            c = curves_data["curves"][key]
            fr_max = max(c["fixed_reference_RBE"])
            nr = c["no_repair_RBE"]
            rel_diff = (fr_max - nr) / nr if nr > 0 else float("nan")
            row.append(float(rel_diff))
        table["matrix"].append(row)
    return table


# ---------------------------------------------------------------------------
# Figure 4 left: R_TD50 (photon-only effect of dose rate at TD50)
# ---------------------------------------------------------------------------
def compute_R_TD50_curve(
    params: CellParams,
    n_fractions: int,
    target_S: float,
    dose_rate_Gy_per_min_grid: list[float],
    ref_dose_rate_Gy_per_min: float = 3.75,
    rng: np.random.Generator | None = None,
) -> dict:
    """R_TD50(D_dot) = TD50_photon(ref dose rate) / TD50_photon(D_dot).

    For multi-fraction irradiation, each fraction is independent and the
    total survival is the product over fractions of the single-fraction
    survival.  We solve for the per-fraction dose that, when applied
    n_fractions times, produces survival target_S, i.e. per-fraction target =
    target_S ** (1/n_fractions).
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED + 100)
    per_fx_target = target_S ** (1.0 / n_fractions)
    # TD50 at the reference dose rate
    TD50_ref = dose_for_survival(
        per_fx_target, lambda D: survival_with_repair(
            D, ref_dose_rate_Gy_per_min, params, n_iter=1500, rng=rng),
        d_lo=0.5, d_hi=40, max_iter=30, tol=4e-3,
    )
    R_vals = []
    TD50_dot = []
    for D_dot in dose_rate_Gy_per_min_grid:
        D = dose_for_survival(
            per_fx_target, lambda Dx: survival_with_repair(
                Dx, D_dot, params, n_iter=1200, rng=rng),
            d_lo=0.5, d_hi=40, max_iter=25, tol=5e-3,
        )
        TD50_dot.append(D)
        R_vals.append(float(TD50_ref / D) if D > 0 else float("nan"))
    return {
        "n_fractions": n_fractions,
        "ref_dose_rate_Gy_per_min": ref_dose_rate_Gy_per_min,
        "TD50_ref_per_fraction_Gy": float(TD50_ref),
        "dose_rate_Gy_per_min": dose_rate_Gy_per_min_grid,
        "TD50_at_rate_per_fraction_Gy": [float(x) for x in TD50_dot],
        "R_TD50": R_vals,
    }


# ---------------------------------------------------------------------------
# Figure 5 benchmark — proton & helium SOBP RBE at 4 depths
# ---------------------------------------------------------------------------
# Table 3 values, copied verbatim from the paper:
SOBP_TABLE3 = {
    "proton_1fx": {
        "depths_mm":     [35,    100,   120,   127  ],
        "LET_keV_um":    [2.0,   3.0,   4.1,   5.3  ],
        "dose_rate_Gy_per_min": [11, 18, 42, 53],
        "R_TD50":        [1.042, 1.051, 1.059, 1.061],
    },
    "proton_2fx": {
        "depths_mm":     [35,    100,   120,   127  ],
        "LET_keV_um":    [2.0,   3.0,   4.1,   5.3  ],
        "dose_rate_Gy_per_min": [8, 14, 31, 41],
        "R_TD50":        [1.022, 1.031, 1.038, 1.040],
    },
    "helium_1fx": {
        "depths_mm":     [35,    100,   120,   127  ],
        "LET_keV_um":    [4.2,   9.3,   14.4,  22.0 ],
        "dose_rate_Gy_per_min": [11, 11, 10, 9],
        "R_TD50":        [1.042, 1.042, 1.041, 1.036],
    },
    "helium_2fx": {
        "depths_mm":     [35,    100,   120,   127  ],
        "LET_keV_um":    [4.2,   9.3,   14.4,  22.0 ],
        "dose_rate_Gy_per_min": [8, 7, 7, 6],
        "R_TD50":        [1.022, 1.018, 1.018, 1.015],
    },
}

# Measured RBE values for proton SOBP from Saager et al. 2018 (digitized from
# Figure 4 middle panel of Liew et al. 2022).  Approximate values:
MEASURED_RBE = {
    "proton_1fx": [1.13, 1.18, 1.30, 1.45],   # approx, digitized from Liew Fig 4
    "proton_2fx": [1.10, 1.15, 1.27, 1.38],
    "helium_1fx": [1.30, 1.65, 2.05, 2.55],   # approx, digitized from Liew Fig 4
    "helium_2fx": [1.28, 1.60, 2.00, 2.40],
}


def compute_figure5_benchmark(
    target_S: float = 0.5,
    rng: np.random.Generator | None = None,
) -> dict:
    """For each Table 3 entry, compute predicted RBE = no_repair_RBE * R_TD50
    and compare to digitized measured values.

    Uses the rat spinal cord with-repair params for the radiosensitivity, but
    the relevant trend is the no-repair RBE vs LET (and the R_TD50 factor),
    so we use the RSC_with_repair K_iDSB / K_cDSB to set the photon reference.
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED + 200)
    params = PARAMS_RSC_WITH_REPAIR

    # Photon dose for target_S at no-repair limit
    Dph_norep = dose_for_survival(
        target_S, lambda D: survival_no_repair(D, params, n_iter=4000, rng=rng),
        d_lo=0.5, d_hi=60, max_iter=40, tol=2e-3,
    )

    out = {"target_survival": target_S, "Dph_norep_Gy": float(Dph_norep),
           "predictions": {}, "measured": MEASURED_RBE, "table3": SOBP_TABLE3,
           "MAD_percent": {}}

    for key, tbl in SOBP_TABLE3.items():
        particle = key.split("_")[0]
        preds = []
        no_repair_RBEs = []
        for LET, R_TD in zip(tbl["LET_keV_um"], tbl["R_TD50"]):
            Dp = dose_for_survival(
                target_S, lambda Dx: survival_ion_no_repair(
                    Dx, LET, particle, params, n_iter=500, rng=rng),
                d_lo=0.05, d_hi=40, max_iter=25, tol=5e-3,
            )
            no_repair_RBE = Dph_norep / Dp if Dp > 0 else float("nan")
            no_repair_RBEs.append(float(no_repair_RBE))
            preds.append(float(no_repair_RBE * R_TD))
        out["predictions"][key] = {
            "no_repair_RBE": no_repair_RBEs,
            "predicted_RBE": preds,
            "measured_RBE": MEASURED_RBE[key],
        }
        # MAD: mean abs(percent deviation)
        meas = np.array(MEASURED_RBE[key])
        pr = np.array(preds)
        mad = float(np.mean(np.abs(pr - meas) / meas) * 100.0)
        out["MAD_percent"][key] = mad
        print(f"  {key}: predicted RBEs = {['%.2f' % p for p in preds]}, "
              f"measured = {MEASURED_RBE[key]}, MAD = {mad:.2f}%")
    return out


# ---------------------------------------------------------------------------
# Figure 3: sensitivity to ref dose rate (left) and T_iDSB_half (right)
# ---------------------------------------------------------------------------
def figure3_sensitivity(
    rng: np.random.Generator | None = None,
) -> dict:
    rng = rng or np.random.default_rng(DEFAULT_SEED + 300)
    LET, D = 8.0, 6.0
    dose_rates_Gy_per_s = [0.1, 0.3, 1.0, 3.0, 10.0]
    # Left panel: two reference dose-rates 2 vs 1 Gy/min
    out = {"LET_keV_um": LET, "dose_Gy": D,
           "dose_rates_Gy_per_s": dose_rates_Gy_per_s,
           "left": {}, "right": {}}
    target_S = 0.1
    for ref_rate in [2.0, 1.0]:
        curves = proton_rbe_curves(
            dose_grid=[D], LET_list=[LET],
            dose_rate_Gy_per_s=dose_rates_Gy_per_s,
            ref_dose_rate_Gy_per_min=ref_rate,
            target_S=target_S, params=PARAMS_DU145, rng=rng,
        )
        out["left"][f"ref_rate_{ref_rate}_Gy_per_min"] = curves["curves"][f"LET={LET}_D={D}"]
    # Right panel: T_iDSB = 4 (default DU145) vs 30 min
    for T_iDSB in [4.0, 30.0]:
        params = CellParams(
            name=f"DU145_T={T_iDSB}",
            K_iDSB=PARAMS_DU145.K_iDSB,
            K_cDSB=PARAMS_DU145.K_cDSB,
            T_iDSB_half_min=T_iDSB,
            T_cDSB_half_min=PARAMS_DU145.T_cDSB_half_min,
        )
        curves = proton_rbe_curves(
            dose_grid=[D], LET_list=[LET],
            dose_rate_Gy_per_s=dose_rates_Gy_per_s,
            ref_dose_rate_Gy_per_min=2.0,
            target_S=target_S, params=params, rng=rng,
        )
        out["right"][f"T_iDSB_{T_iDSB}_min"] = curves["curves"][f"LET={LET}_D={D}"]
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    plt = _maybe_import_pyplot()
    rng = np.random.default_rng(DEFAULT_SEED)
    t0 = time.time()

    # --- Figures 1 & 2 ---
    print("\n=== Figure 1 (moderate doses) ===")
    fig1 = proton_rbe_curves(
        dose_grid=[2.0, 6.0],
        LET_list=[2.0, 8.0, 25.0],
        dose_rate_Gy_per_s=[0.1, 0.3, 1.0, 3.0, 10.0],
        ref_dose_rate_Gy_per_min=2.0,
        target_S=0.1,
        params=PARAMS_DU145,
        n_iter=500, rng=rng,
    )
    (RESULTS / "fig1_proton_rbe_vs_doserate_moderate.json").write_text(
        json.dumps(fig1, indent=2))

    print("\n=== Figure 2 (high doses) ===")
    fig2 = proton_rbe_curves(
        dose_grid=[12.0, 24.0],
        LET_list=[2.0, 8.0, 25.0],
        dose_rate_Gy_per_s=[0.1, 0.3, 1.0, 3.0, 10.0],
        ref_dose_rate_Gy_per_min=2.0,
        target_S=0.1,
        params=PARAMS_DU145,
        n_iter=500, rng=rng,
    )
    (RESULTS / "fig2_proton_rbe_vs_doserate_high.json").write_text(
        json.dumps(fig2, indent=2))

    # --- Table 2: combined ---
    combined_curves = {"doses_Gy": [2.0, 6.0, 12.0, 24.0],
                       "LETs_keV_um": [2.0, 8.0, 25.0],
                       "curves": {**fig1["curves"], **fig2["curves"]}}
    table2 = build_table2(combined_curves)
    (RESULTS / "table2_max_relative_difference.json").write_text(
        json.dumps(table2, indent=2))
    # CSV
    with open(RESULTS / "table2_max_relative_difference.csv", "w") as f:
        f.write("Dose_Gy," + ",".join(f"LET_{L}_keV_um" for L in table2["LETs_keV_um"]) + "\n")
        for D, row in zip(table2["doses_Gy"], table2["matrix"]):
            f.write(f"{D}," + ",".join(f"{v*100:.2f}%" for v in row) + "\n")

    # --- Figure 3 ---
    print("\n=== Figure 3 (sensitivity) ===")
    fig3 = figure3_sensitivity(rng=rng)
    (RESULTS / "fig3_sensitivity.json").write_text(json.dumps(fig3, indent=2))

    # --- Figure 4 left: R_TD50 vs dose rate ---
    print("\n=== Figure 4 left (R_TD50 curves) ===")
    rates = [0.1, 0.5, 1.0, 2.0, 3.75, 10, 30, 100]
    fig4 = {
        "ref_dose_rate_Gy_per_min": 3.75,
        "target_total_survival": 0.5,
        "1fx": compute_R_TD50_curve(
            PARAMS_RSC_WITH_REPAIR, n_fractions=1, target_S=0.5,
            dose_rate_Gy_per_min_grid=rates, rng=rng),
        "2fx": compute_R_TD50_curve(
            PARAMS_RSC_WITH_REPAIR, n_fractions=2, target_S=0.5,
            dose_rate_Gy_per_min_grid=rates, rng=rng),
    }
    (RESULTS / "fig4_R_TD50.json").write_text(json.dumps(fig4, indent=2))

    # --- Figure 5 benchmark ---
    print("\n=== Figure 5 (SOBP RBE benchmark) ===")
    fig5 = compute_figure5_benchmark(target_S=0.5, rng=rng)
    (RESULTS / "fig5_RBE_benchmark.json").write_text(json.dumps(fig5, indent=2))

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f} s.")

    # ----- PLOTS -----
    if plt is None:
        return
    # Fig 1/2 combined
    for tag, data in [("fig1", fig1), ("fig2", fig2)]:
        n_d = len(data["doses_Gy"]); n_l = len(data["LETs_keV_um"])
        fig, axes = plt.subplots(n_d, n_l, figsize=(4.0 * n_l, 3.0 * n_d), sharex=True)
        axes = np.atleast_2d(axes)
        for i, D in enumerate(data["doses_Gy"]):
            for j, LET in enumerate(data["LETs_keV_um"]):
                ax = axes[i, j]
                c = data["curves"][f"LET={LET}_D={D}"]
                rates = c["dose_rate_Gy_per_s"]
                ax.plot(rates, c["fixed_reference_RBE"], "g--", label="fixed-ref RBE")
                ax.plot(rates, c["dose_rate_adapted_RBE"], "orange", linestyle=":",
                        label="dose-rate adapted RBE")
                ax.axhline(c["no_repair_RBE"], color="blue", linestyle="-",
                           label="no-repair RBE")
                ax.set_xscale("log")
                ax.set_title(f"LET={LET} keV/µm, D={D} Gy")
                ax.set_xlabel("Dose rate [Gy/s]")
                ax.set_ylabel("Proton RBE")
                ax.grid(True, alpha=0.3)
                if i == 0 and j == 0:
                    ax.legend(loc="best", fontsize=8)
        fig.tight_layout()
        fig.savefig(FIGURES / f"{tag}_proton_rbe_vs_doserate.png", dpi=130)
        plt.close(fig)

    # Fig 3 sensitivity
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharex=True)
    rates = fig3["dose_rates_Gy_per_s"]
    for label, c in fig3["left"].items():
        axes[0].plot(rates, c["fixed_reference_RBE"], "g--",
                     label=f"fix-ref {label}")
        axes[0].plot(rates, c["dose_rate_adapted_RBE"], "orange", linestyle=":",
                     label=f"adapt {label}")
        axes[0].axhline(c["no_repair_RBE"], color="blue", linestyle="-", alpha=0.3,
                        label=f"no-rep {label}")
    axes[0].set_xscale("log")
    axes[0].set_title("Sensitivity to reference dose rate (D=6 Gy, LET=8 keV/µm)")
    axes[0].set_xlabel("Dose rate [Gy/s]"); axes[0].set_ylabel("RBE")
    axes[0].grid(True, alpha=0.3); axes[0].legend(fontsize=7)
    for label, c in fig3["right"].items():
        axes[1].plot(rates, c["fixed_reference_RBE"], "g--",
                     label=f"fix-ref {label}")
        axes[1].plot(rates, c["dose_rate_adapted_RBE"], "orange", linestyle=":",
                     label=f"adapt {label}")
        axes[1].axhline(c["no_repair_RBE"], color="blue", linestyle="-", alpha=0.3,
                        label=f"no-rep {label}")
    axes[1].set_xscale("log")
    axes[1].set_title("Sensitivity to T_iDSB half-life (D=6 Gy, LET=8 keV/µm)")
    axes[1].set_xlabel("Dose rate [Gy/s]"); axes[1].set_ylabel("RBE")
    axes[1].grid(True, alpha=0.3); axes[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig3_sensitivity.png", dpi=130)
    plt.close(fig)

    # Fig 4 R_TD50
    fig, ax = plt.subplots(figsize=(6, 4))
    for tag, color, ls in [("1fx", "k", "-"), ("2fx", "purple", "--")]:
        c = fig4[tag]
        ax.plot(c["dose_rate_Gy_per_min"], c["R_TD50"], color=color, linestyle=ls,
                marker="o", label=f"{tag}")
    ax.set_xscale("log"); ax.set_xlabel("Dose rate [Gy/min]"); ax.set_ylabel("R_TD50")
    ax.set_title("R_TD50 — relative TD50 between reference (3.75 Gy/min) and applied rate")
    ax.grid(True, alpha=0.3); ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "fig4_R_TD50.png", dpi=130)
    plt.close(fig)

    # Fig 5 benchmark
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True)
    keys = [("proton_1fx", 0, 0, "Proton 1 fx"),
            ("proton_2fx", 0, 1, "Proton 2 fx"),
            ("helium_1fx", 1, 0, "Helium 1 fx"),
            ("helium_2fx", 1, 1, "Helium 2 fx")]
    for key, r, c, title in keys:
        ax = axes[r, c]
        depths = SOBP_TABLE3[key]["depths_mm"]
        preds = fig5["predictions"][key]["predicted_RBE"]
        meas = fig5["predictions"][key]["measured_RBE"]
        ax.plot(depths, preds, "-o", label="UNIVERSE (modif.)", color="C0")
        ax.plot(depths, meas, "s", label="measured (digitized)",
                color="C3", markersize=8, fillstyle="none")
        ax.set_title(f"{title}  MAD={fig5['MAD_percent'][key]:.2f}%")
        ax.set_xlabel("Depth [mm]"); ax.set_ylabel("RBE")
        ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig5_RBE_benchmark.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
