"""
Replication of Ruigrok et al. (EJNMMI 2022, DOI 10.1007/s00259-022-05821-w),
"In vitro dose-effect relationships of actinium-225- and lutetium-177-labeled
PSMA-I&T".

Replication target (quantitative):
  - Linear dose-response model fits S = exp(-alpha * D) for both isotopes.
  - Reported: alpha(Lu-177)  = 0.16 ± 0.01 Gy^-1
             alpha(Ac-225)   = 0.67 ± 0.06 Gy^-1
             RBE             = 4.2  ± 0.46
             R^2             > 0.96

Inputs:
  - Table 3 (paper, "average" cellular dimension column) for absorbed doses
    delivered over 7 days as a function of activity concentration.
  - Survival fractions digitized from Figure 3 panels A and C.

What this replicates (HONESTLY):
  - The model fit step on the dose-response data.
  - The RBE calculation.
  - A sanity check of the time-integrated activity * S-value pipeline,
    using the paper's S-values (Table 2) and the biological half-life
    (t_1/2_bio = 2.3 h, plateau 41%) reported in the text.

What this DOES NOT replicate:
  - Geant4 Monte Carlo S-value computation (out of scope; would need full
    cell geometry, EM/hadronic physics list configuration, days of CPU).
  - Wet-lab clonogenic counts (no raw data deposited).
  - 53BP1 foci counting.
  - IC50 displacement curves.

Therefore the digitized survival values from Figure 3 carry digitization noise
~5 percentage points in survival; this is well above the published per-point
SEMs. The recovered alpha is expected to land near the published value but
with somewhat wider uncertainty.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

OUT = Path(__file__).resolve().parent.parent
RESULTS = OUT / "results"
FIGURES = OUT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# 1.  Published Table 3 (average cellular dimension column).
# -----------------------------------------------------------------------------

# Lu-177: concentration in MBq/mL -> absorbed dose to nucleus (Gy)
LU_DOSE_AVG = {
    0.0: 0.0,
    0.1: 0.74,
    0.2: 1.48,
    0.3: 2.22,
    0.4: 2.96,
    0.5: 3.70,
    # Higher concentrations (1, 2, 5 MBq/mL) are NOT in Table 3 -> the
    # authors note the highest concentrations were not included in dose-
    # response correlations. We respect that.
}

# Ac-225: concentration in kBq/mL -> absorbed dose to nucleus (Gy)
AC_DOSE_AVG = {
    0.0:    0.0,
    0.037:  0.08,
    0.10:   0.22,
    0.185:  0.41,
    0.25:   0.56,
    0.37:   0.83,
    0.50:   1.12,
    0.75:   1.67,
    # 1.25, 1.85, 3.7 kBq/mL excluded by the authors from the linear fit.
}


# -----------------------------------------------------------------------------
# 2.  Survival fractions digitized from Figure 3 panels A and C.
#     Source: visual read of the published figure (see code/digitization.md).
#     Uncertainty: ~5 percentage-points in survival.
# -----------------------------------------------------------------------------

# Panel A: Ac-225 (kBq/mL -> survival fraction in [0,1]).
# Read 1: initial visual estimate of Fig. 3A.
# Read 2: second visual estimate from a higher-resolution render.
# We report both fits separately for transparency.
AC_SURV_READ1 = {
    0.0:    1.00,
    0.037:  0.92,
    0.10:   0.60,
    0.185:  0.55,
    0.25:   0.52,
    0.37:   0.48,
    0.50:   0.42,
    0.75:   0.15,
    1.25:   0.003,   # excluded by paper from linear fit
    1.85:   0.001,   # excluded by paper from linear fit
}
AC_SURV_READ2 = {
    0.0:    1.00,
    # high-res image read picked these out:
    0.12:   0.80,
    0.25:   0.63,
    0.50:   0.50,
    0.75:   0.38,
    1.25:   0.28,
    1.85:   0.13,
}

# Panel C: Lu-177 (MBq/mL -> survival fraction in [0,1]).
LU_SURV_READ1 = {
    0.0:  1.00,
    0.1:  0.78,
    0.2:  0.55,
    0.3:  0.42,
    0.4:  0.40,
    0.5:  0.40,
    1.0:  0.42,   # excluded by paper
    2.0:  0.36,   # excluded by paper
    5.0:  0.22,   # excluded by paper
}
LU_SURV_READ2 = {
    0.0:  1.00,
    0.37: 0.80,
    0.5:  0.45,
    1.0:  0.47,
    2.0:  0.36,
    5.0:  0.22,
}

# Default to read1 (more concentration coverage matching Table 3).
AC_SURV_DIGITIZED = AC_SURV_READ1
LU_SURV_DIGITIZED = LU_SURV_READ1


# -----------------------------------------------------------------------------
# 3.  Build (Dose, Survival) tables for the fit.
# -----------------------------------------------------------------------------

def build_table(dose_map: dict[float, float], surv_map: dict[float, float],
                conc_label: str) -> pd.DataFrame:
    rows = []
    for c, d in dose_map.items():
        if c not in surv_map:
            continue
        rows.append({conc_label: c, "Dose_Gy": d, "Survival": surv_map[c]})
    return pd.DataFrame(rows)


lu_df = build_table(LU_DOSE_AVG, LU_SURV_DIGITIZED, "conc_MBq_per_mL")
ac_df = build_table(AC_DOSE_AVG, AC_SURV_DIGITIZED, "conc_kBq_per_mL")

lu_df.to_csv(RESULTS / "lu177_dose_survival.csv", index=False)
ac_df.to_csv(RESULTS / "ac225_dose_survival.csv", index=False)


# -----------------------------------------------------------------------------
# 4.  Fit the linear model S = exp(-alpha * D) on log(S) vs D.
# -----------------------------------------------------------------------------

def linear_model(D, alpha):
    return np.exp(-alpha * D)


def fit_alpha(df: pd.DataFrame) -> dict:
    D = df["Dose_Gy"].values
    S = df["Survival"].values
    # Fit in log-space which is what a true "linear" log-survival model means.
    mask = S > 0
    Dm = D[mask]
    logS = np.log(S[mask])
    # log S = -alpha * D  ->  slope through origin
    # Use curve_fit on S = exp(-alpha D) with sigma in survival space.
    popt, pcov = curve_fit(linear_model, Dm, S[mask], p0=[0.1])
    alpha = popt[0]
    alpha_se = float(np.sqrt(pcov[0, 0]))
    Spred = linear_model(D, alpha)
    # R^2 in log-survival space (which is how authors quote R^2 > 0.96).
    ss_res = np.sum((logS - (-alpha * Dm)) ** 2)
    ss_tot = np.sum((logS - logS.mean()) ** 2)
    r2_log = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    # R^2 in linear survival space.
    ss_res_lin = np.sum((S - Spred) ** 2)
    ss_tot_lin = np.sum((S - S.mean()) ** 2)
    r2_lin = 1.0 - ss_res_lin / ss_tot_lin if ss_tot_lin > 0 else float("nan")
    return {
        "alpha_Gy_inv": alpha,
        "alpha_SE": alpha_se,
        "R2_log_survival": r2_log,
        "R2_linear_survival": r2_lin,
        "n_points": int(mask.sum()),
    }


lu_fit = fit_alpha(lu_df)
ac_fit = fit_alpha(ac_df)

# Second-read fits for honesty about digitization noise.
ac_df_r2 = build_table(AC_DOSE_AVG, AC_SURV_READ2, "conc_kBq_per_mL")
lu_df_r2 = build_table(LU_DOSE_AVG, LU_SURV_READ2, "conc_MBq_per_mL")
# Read2 has different concentration coverage; some don't have published Table 3
# entries. We restrict to overlap.
lu_fit_r2 = fit_alpha(lu_df_r2) if len(lu_df_r2) >= 2 else None
ac_fit_r2 = fit_alpha(ac_df_r2) if len(ac_df_r2) >= 2 else None


# -----------------------------------------------------------------------------
# 5.  RBE = alpha_Ac / alpha_Lu, with error propagation.
# -----------------------------------------------------------------------------

rbe = ac_fit["alpha_Gy_inv"] / lu_fit["alpha_Gy_inv"]
rbe_se = rbe * np.sqrt(
    (ac_fit["alpha_SE"] / ac_fit["alpha_Gy_inv"]) ** 2
    + (lu_fit["alpha_SE"] / lu_fit["alpha_Gy_inv"]) ** 2
)


# -----------------------------------------------------------------------------
# 6.  Dosimetry pipeline sanity check.
#
# Paper's pipeline:
#   D_nucleus = sum over decay path of  A_tilde(t) * S_value
# where A_tilde is the time-integrated activity.
#
# For the spherical / cytoplasm / Lu-177 / average dimension geometry,
# S = 1.98e-4 Gy/(Bq*s)  (Table 2, floating set-up, cytoplasm, average).
# Membrane-bound fraction 0.76 internalized vs membrane (paper).
#
# Time-integrated activity per cell during incubation (3 h) +
# post-incubation:
#   - uptake = 1.88 %AA / 100,000 cells (avg over 1h, 3h Lu)
#         -> per cell: 1.88e-2 / 1e5 = 1.88e-7 of added activity
#   - biological t1/2 = 2.3 h, plateau 41% of bound activity at infinity.
#   - physical t1/2(Lu-177) = 6.647 d
#   - integrate to 7 days post-incubation.
#
# We compute D_nucleus per (MBq/mL initial concentration) and compare
# to Table 3 entries.
# -----------------------------------------------------------------------------

# Constants
S_LU_AVG_CYT = 1.98e-4   # Gy/(Bq*s)   floating, cytoplasm, average dim
S_LU_AVG_MEM = 1.04e-4   # Gy/(Bq*s)   floating, cell membrane, average dim
S_AC_AVG_CYT = 1.01e-1   # Gy/(Bq*s)
S_AC_AVG_MEM = 5.63e-2   # Gy/(Bq*s)
S_LU_CROSS   = 1.13e-6   # Gy/(Bq*s)   cross dose Lu-177 in uptake phase

# Physical half-lives
T_HALF_LU = 6.647 * 24 * 3600        # s   (Lu-177 = 6.647 d)
T_HALF_AC = 9.92  * 24 * 3600        # s   (Ac-225 = 9.92 d)

LAMBDA_LU = np.log(2) / T_HALF_LU
LAMBDA_AC = np.log(2) / T_HALF_AC

# Biological excretion: t_1/2_bio = 2.3 h, fraction retained at infinity = 0.41
T_HALF_BIO = 2.3 * 3600              # s
LAMBDA_BIO = np.log(2) / T_HALF_BIO
F_PLATEAU  = 0.41

# Incubation phase: 3 h with cells in 1.5 mL medium in Eppendorf tubes
INCUBATION = 3 * 3600                # s
INTEG_END  = INCUBATION + 7 * 86400  # 7 days post-incubation

# Membrane vs internal split (per paper)
F_MEMBRANE   = 1.0 - 0.76            # 0.24 on membrane
F_INTERNAL   = 0.76                  # 0.76 internalized in cytoplasm

# Uptake (average between 1 h and 3 h for Lu-177): 1.88 %AA / 100,000 cells.
UPTAKE_PCT_PER_100K = 1.88           # %AA / 1e5 cells
N_CELLS = 100_000                    # cells per well


def time_integrated_activity_per_cell(A0_per_cell_Bq: float,
                                      lambda_phys: float) -> float:
    """Return integrated Bq*s over [t_incub, t_incub + 7d]."""
    # During incubation (0..INCUBATION): A_bound(t) builds up; we approximate
    # using the average uptake reported by the paper (instant uptake assumption
    # is what the paper itself does -- see Methods/Dosimetry section).
    # So at t = INCUBATION, the cell holds A0_per_cell_Bq * exp(-lambda_phys * INCUBATION).
    # Then cells are washed; we model retention as:
    #   A(t > INC) = A0_post * [ (1-F_PLATEAU)*exp(-(lambda_bio+lambda_phys)*tau)
    #                          + F_PLATEAU      *exp(-lambda_phys*tau) ]
    # where tau = t - INCUBATION.
    A0_post = A0_per_cell_Bq * np.exp(-lambda_phys * INCUBATION)

    # During incubation: assume constant binding -> approximate A_bound = A0 over [0, INCUBATION]
    # That's the paper's assumption ("instant uptake").
    A_int_incub = A0_per_cell_Bq * INCUBATION

    tau_end = INTEG_END - INCUBATION
    lam_fast = LAMBDA_BIO + lambda_phys
    lam_slow = lambda_phys

    int_fast = (1.0 - F_PLATEAU) * (1.0 - np.exp(-lam_fast * tau_end)) / lam_fast
    int_slow = F_PLATEAU         * (1.0 - np.exp(-lam_slow * tau_end)) / lam_slow

    A_int_post = A0_post * (int_fast + int_slow)
    return A_int_incub + A_int_post


def predicted_nucleus_dose_Lu(conc_MBq_per_mL: float) -> float:
    """Predict average-dimension absorbed dose to nucleus for Lu-177."""
    if conc_MBq_per_mL == 0.0:
        return 0.0
    # Added activity in the 1.5 mL Eppendorf tube
    A_added_Bq = conc_MBq_per_mL * 1e6 * 1.5
    # Activity bound per cell at saturation: uptake_pct% of added per 100k cells.
    A_per_cell_Bq = A_added_Bq * (UPTAKE_PCT_PER_100K / 100.0) / N_CELLS
    A_int_Bq_s = time_integrated_activity_per_cell(A_per_cell_Bq, LAMBDA_LU)
    # Distribute over membrane and cytoplasm with respective S-values.
    S_eff = F_INTERNAL * S_LU_AVG_CYT + F_MEMBRANE * S_LU_AVG_MEM
    D_self = A_int_Bq_s * S_eff
    return D_self


def predicted_nucleus_dose_Ac(conc_kBq_per_mL: float,
                              uptake_pct_per_100k: float = 1.87) -> float:
    """Predict average-dimension absorbed dose to nucleus for Ac-225.
    Uses Ac-225 self uptake reported in paper (1.87 %AA/1e5 cells at 1 h, 1.86 at 3 h)."""
    if conc_kBq_per_mL == 0.0:
        return 0.0
    A_added_Bq = conc_kBq_per_mL * 1e3 * 1.5
    A_per_cell_Bq = A_added_Bq * (uptake_pct_per_100k / 100.0) / N_CELLS
    A_int_Bq_s = time_integrated_activity_per_cell(A_per_cell_Bq, LAMBDA_AC)
    S_eff = F_INTERNAL * S_AC_AVG_CYT + F_MEMBRANE * S_AC_AVG_MEM
    return A_int_Bq_s * S_eff


lu_doseimg = pd.DataFrame({
    "conc_MBq_per_mL": list(LU_DOSE_AVG.keys()),
    "D_published_Gy":  list(LU_DOSE_AVG.values()),
    "D_replicated_Gy": [predicted_nucleus_dose_Lu(c) for c in LU_DOSE_AVG],
})
ac_doseimg = pd.DataFrame({
    "conc_kBq_per_mL": list(AC_DOSE_AVG.keys()),
    "D_published_Gy":  list(AC_DOSE_AVG.values()),
    "D_replicated_Gy": [predicted_nucleus_dose_Ac(c) for c in AC_DOSE_AVG],
})

lu_doseimg.to_csv(RESULTS / "lu177_dose_pipeline_check.csv", index=False)
ac_doseimg.to_csv(RESULTS / "ac225_dose_pipeline_check.csv", index=False)


# -----------------------------------------------------------------------------
# 7.  Plots.
# -----------------------------------------------------------------------------

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7.5, 5.5))
D_grid = np.linspace(0, 6, 200)

# Ac-225
ax.scatter(ac_df["Dose_Gy"], ac_df["Survival"], color="C3", marker="^",
           label=f"[225Ac]Ac-PSMA-I&T digitized")
ax.plot(D_grid, np.exp(-ac_fit["alpha_Gy_inv"] * D_grid),
        color="C3", linewidth=2,
        label=f"fit α={ac_fit['alpha_Gy_inv']:.2f} Gy⁻¹")

# Lu-177
ax.scatter(lu_df["Dose_Gy"], lu_df["Survival"], color="C0", marker="o",
           label=f"[177Lu]Lu-PSMA-I&T digitized")
ax.plot(D_grid, np.exp(-lu_fit["alpha_Gy_inv"] * D_grid),
        color="C0", linewidth=2,
        label=f"fit α={lu_fit['alpha_Gy_inv']:.2f} Gy⁻¹")

# Published reference fits
ax.plot(D_grid, np.exp(-0.67 * D_grid), color="C3", linestyle="--",
        linewidth=1, label="paper α=0.67 (Ac-225)")
ax.plot(D_grid, np.exp(-0.16 * D_grid), color="C0", linestyle="--",
        linewidth=1, label="paper α=0.16 (Lu-177)")

ax.set_yscale("log")
ax.set_xlabel("Dose to nucleus (Gy)")
ax.set_ylabel("Survival fraction")
ax.set_xlim(0, 6)
ax.set_ylim(1e-2, 1.2)
ax.set_title("Replication: linear dose-response S = exp(-αD)\n"
             f"RBE_repl = {rbe:.2f}±{rbe_se:.2f}   (paper: 4.2±0.46)")
ax.grid(True, alpha=0.3, which="both")
ax.legend(fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig(FIGURES / "dose_response_replication.png", dpi=180)
plt.close(fig)


# Pipeline check plot
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].plot(lu_doseimg["D_published_Gy"], lu_doseimg["D_replicated_Gy"],
             "o-", color="C0")
axes[0].plot([0, lu_doseimg["D_published_Gy"].max()],
             [0, lu_doseimg["D_published_Gy"].max()],
             "k--", linewidth=1, label="y = x")
axes[0].set_xlabel("Published dose (Gy)")
axes[0].set_ylabel("Replicated dose (Gy)")
axes[0].set_title("Lu-177 dose pipeline check\n(Table 3 vs MIRD-style replication)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(ac_doseimg["D_published_Gy"], ac_doseimg["D_replicated_Gy"],
             "^-", color="C3")
axes[1].plot([0, ac_doseimg["D_published_Gy"].max()],
             [0, ac_doseimg["D_published_Gy"].max()],
             "k--", linewidth=1, label="y = x")
axes[1].set_xlabel("Published dose (Gy)")
axes[1].set_ylabel("Replicated dose (Gy)")
axes[1].set_title("Ac-225 dose pipeline check")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURES / "dose_pipeline_check.png", dpi=180)
plt.close(fig)


# -----------------------------------------------------------------------------
# 8.  Persist results.
# -----------------------------------------------------------------------------

published = {
    "alpha_Lu177_Gy_inv": 0.16,
    "alpha_Lu177_SE":     0.01,
    "alpha_Ac225_Gy_inv": 0.67,
    "alpha_Ac225_SE":     0.06,
    "RBE":                4.2,
    "RBE_SE":             0.46,
}

summary = {
    "lu177_read1": lu_fit,
    "ac225_read1": ac_fit,
    "lu177_read2": lu_fit_r2,
    "ac225_read2": ac_fit_r2,
    "RBE_replicated": rbe,
    "RBE_replicated_SE": rbe_se,
    "published": published,
    "agreement": {
        "alpha_Lu177_ratio":   lu_fit["alpha_Gy_inv"] / published["alpha_Lu177_Gy_inv"],
        "alpha_Ac225_ratio":   ac_fit["alpha_Gy_inv"] / published["alpha_Ac225_Gy_inv"],
        "RBE_ratio":           rbe                    / published["RBE"],
        "alpha_Lu_z":   (lu_fit["alpha_Gy_inv"] - published["alpha_Lu177_Gy_inv"])
                         / np.hypot(lu_fit["alpha_SE"], published["alpha_Lu177_SE"]),
        "alpha_Ac_z":   (ac_fit["alpha_Gy_inv"] - published["alpha_Ac225_Gy_inv"])
                         / np.hypot(ac_fit["alpha_SE"], published["alpha_Ac225_SE"]),
        "RBE_z":        (rbe - published["RBE"])
                         / np.hypot(rbe_se, published["RBE_SE"]),
    },
}

with open(RESULTS / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=float)


# Console echo
print("\n=== LUCID replication summary ===")
print(f"alpha Lu-177  read1 = {lu_fit['alpha_Gy_inv']:.3f} ± {lu_fit['alpha_SE']:.3f} Gy^-1"
      f"   (paper 0.16 ± 0.01)")
print(f"  R^2 (log-survival) = {lu_fit['R2_log_survival']:.3f}   (paper R^2 > 0.96)")
if lu_fit_r2 is not None:
    print(f"alpha Lu-177  read2 = {lu_fit_r2['alpha_Gy_inv']:.3f} ± {lu_fit_r2['alpha_SE']:.3f} Gy^-1")
print(f"alpha Ac-225  read1 = {ac_fit['alpha_Gy_inv']:.3f} ± {ac_fit['alpha_SE']:.3f} Gy^-1"
      f"   (paper 0.67 ± 0.06)")
print(f"  R^2 (log-survival) = {ac_fit['R2_log_survival']:.3f}   (paper R^2 > 0.96)")
if ac_fit_r2 is not None:
    print(f"alpha Ac-225  read2 = {ac_fit_r2['alpha_Gy_inv']:.3f} ± {ac_fit_r2['alpha_SE']:.3f} Gy^-1")
print(f"RBE (read1) = alpha_Ac/alpha_Lu = {rbe:.2f} ± {rbe_se:.2f}   (paper 4.2 ± 0.46)")
if lu_fit_r2 is not None and ac_fit_r2 is not None:
    rbe_r2 = ac_fit_r2['alpha_Gy_inv'] / lu_fit_r2['alpha_Gy_inv']
    print(f"RBE (read2)                       = {rbe_r2:.2f}")
print(f"\nDose pipeline check (Lu-177):")
print(lu_doseimg.to_string(index=False))
print(f"\nDose pipeline check (Ac-225):")
print(ac_doseimg.to_string(index=False))
