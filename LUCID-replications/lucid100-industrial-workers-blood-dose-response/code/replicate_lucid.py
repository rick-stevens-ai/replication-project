#!/usr/bin/env python3
"""
Replication scaffold for:
  Guo et al. 2022, "Dose-Response Effects of Low-Dose Ionizing Radiation on
  Blood Parameters in Industrial Irradiation Workers." Dose-Response 20(2).
  DOI: 10.1177/15593258221105695  (Open Access, PMC9174562)

Replication strategy
--------------------
No individual-level data are deposited. We perform a TWO-LEVEL replication
on the *published* tables:

(A) INTERNAL CONSISTENCY of Table 3 (Generalized Linear Model)
    - For each Z = beta / SE, recompute Z and compare to printed Z.
    - For each printed 95% CI [lo, hi], recompute (beta - 1.96*SE, beta + 1.96*SE)
      and check whether the printed CI agrees.
    - Re-derive two-sided p-value from Z and compare to printed P.
    Result: directly checks whether the printed numbers are mutually
    consistent. This does NOT require the raw cohort data.

(B) APPROXIMATE REFIT from Table 2 marginal distributions (simulation re-fit)
    - For each blood parameter (RBC, PLT, HB), Table 2 gives per-dose-group
      median + IQR and per-dose-group N.
    - We simulate individual changes ~ Normal with mean = median (approx) and
      sigma = IQR/1.349, then fit a GLM with dose-group as categorical, lowest
      group as reference.
    - We compare the simulated betas to the published Table 3 betas.
    Caveat: this is a *coarse* sanity check; it ignores sex/age/smoking
    adjustments and IQR-based sigma is only exact for Normal data. We report
    relative agreement.

Outputs land in ../results/ and ../figures/.
"""
from __future__ import annotations
import json, math, os, sys
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

# ---------- Published Table 3 (transcribed from paper.xml) ----------
# Columns: outcome, group_label, beta, SE, Z_printed, p_printed, ci_lo, ci_hi
T3 = [
    # RBC (paper prints unit as 1e9/L, but blood-cell norms in Methods say 1e12/L for RBC;
    # this is almost certainly a typo in the published Table 3 header.)
    ("RBC", "1.417-2.585 mSv",  -0.067, 0.027, -2.520, 0.012, -0.119, 0.015),
    ("RBC", "2.585-2.903 mSv",   0.009, 0.028,  0.340, 0.733, -0.045, 0.064),
    ("RBC", "2.903-4.908 mSv",  -0.052, 0.032, -1.660, 0.098, -0.114, 0.010),
    # PLT (1e9/L)
    ("PLT", "1.417-2.585 mSv", 15.932, 3.573,  4.460, 1e-4,   8.929, 22.934),
    ("PLT", "2.585-2.903 mSv", 17.195, 3.685,  4.670, 1e-4,   9.973, 24.417),
    ("PLT", "2.903-4.908 mSv", 21.062, 4.205,  5.010, 1e-4,  12.821, 29.303),
    # HB (g/L)
    ("HB",  "1.417-2.585 mSv",  1.681, 0.808,  2.080, 0.037,  0.098,  3.264),
    ("HB",  "2.585-2.903 mSv",  5.383, 0.842,  6.390, 1e-4,   3.732,  7.034),
    ("HB",  "2.903-4.908 mSv",  1.922, 0.962,  2.000, 0.046,  0.037,  3.806),
]

# ---------- Published Table 2 marginals (median(IQR) per dose group) -------
# Columns: outcome, group_label, N, median, q1, q3, p_overall
T2 = [
    ("RBC", "0.101-1.417 mSv", 159,  0.04, -0.16, 0.23, 0.007),
    ("RBC", "1.417-2.585 mSv", 236, -0.04, -0.20, 0.14, 0.007),
    ("RBC", "2.585-2.903 mSv", 194,  0.02, -0.10, 0.22, 0.007),
    ("RBC", "2.903-4.908 mSv", 116, -0.02, -0.18, 0.16, 0.007),
    ("PLT", "0.101-1.417 mSv", 159, -6.20, -26.30, 15.20, 0.001),
    ("PLT", "1.417-2.585 mSv", 236, 12.45,  -6.60, 28.15, 0.001),
    ("PLT", "2.585-2.903 mSv", 194, 12.85,  -7.30, 31.00, 0.001),
    ("PLT", "2.903-4.908 mSv", 116,  9.45,  -4.10, 33.75, 0.001),
    ("HB",  "0.101-1.417 mSv", 159, -1.20, -6.30,   4.30, 0.001),
    ("HB",  "1.417-2.585 mSv", 236,  0.20, -4.10,   5.30, 0.001),
    ("HB",  "2.585-2.903 mSv", 194,  4.30, -0.60,   9.30, 0.001),
    ("HB",  "2.903-4.908 mSv", 116,  0.30, -3.80,   5.90, 0.001),
]

GROUPS = ["0.101-1.417 mSv", "1.417-2.585 mSv", "2.585-2.903 mSv", "2.903-4.908 mSv"]
RNG_SEED = 20260609
N_BOOT = 400

# ---------- (A) Internal-consistency check of Table 3 ----------
def check_internal_consistency():
    rows = []
    for outcome, grp, beta, se, Zp, Pp, lo, hi in T3:
        Z_recomp = beta / se
        # two-sided p from |Z|
        P_recomp = 2.0 * (1.0 - stats.norm.cdf(abs(Z_recomp)))
        # 95% CI via Wald (z=1.96)
        ci_lo_recomp = beta - 1.96 * se
        ci_hi_recomp = beta + 1.96 * se
        rows.append({
            "outcome": outcome,
            "group": grp,
            "beta": beta,
            "SE": se,
            "Z_printed": Zp,
            "Z_recomp": round(Z_recomp, 3),
            "Z_abs_diff": round(abs(Zp - Z_recomp), 3),
            "P_printed": Pp,
            "P_recomp": round(P_recomp, 4),
            "CI_lo_printed": lo,
            "CI_lo_recomp": round(ci_lo_recomp, 3),
            "CI_hi_printed": hi,
            "CI_hi_recomp": round(ci_hi_recomp, 3),
            "CI_lo_abs_diff": round(abs(lo - ci_lo_recomp), 3),
            "CI_hi_abs_diff": round(abs(hi - ci_hi_recomp), 3),
        })
    df = pd.DataFrame(rows)
    df.to_csv(RES / "table3_internal_consistency.csv", index=False)
    return df

# ---------- (B) Approximate refit by simulation from Table 2 ----------
def simulate_and_refit(outcome: str, rng: np.random.Generator):
    rows = [r for r in T2 if r[0] == outcome]
    # Build long-form synthetic dataset
    chunks = []
    for _, grp, N, med, q1, q3, _p in rows:
        # IQR -> sigma assuming Normal: sigma ~= IQR / 1.349
        sigma = (q3 - q1) / 1.349
        # Use median as mean (Normal symmetric assumption)
        y = rng.normal(loc=med, scale=sigma, size=N)
        chunks.append(pd.DataFrame({"y": y, "group": grp}))
    df = pd.concat(chunks, ignore_index=True)
    # Encode group as dummy variables with lowest group as reference
    df["group"] = pd.Categorical(df["group"], categories=GROUPS, ordered=True)
    X = pd.get_dummies(df["group"], drop_first=True).astype(float)
    X = sm.add_constant(X)
    model = sm.GLM(df["y"], X, family=sm.families.Gaussian()).fit()
    # Extract betas
    out = {}
    for grp in GROUPS[1:]:
        out[grp] = {
            "beta_sim": float(model.params[grp]),
            "SE_sim":   float(model.bse[grp]),
            "p_sim":    float(model.pvalues[grp]),
        }
    return out

def approximate_refit():
    rng = np.random.default_rng(RNG_SEED)
    summary_rows = []
    boot_rows = []
    for outcome in ["RBC", "PLT", "HB"]:
        # bootstrap to get a distribution of beta_sim
        beta_dist = {g: [] for g in GROUPS[1:]}
        for b in range(N_BOOT):
            out = simulate_and_refit(outcome, rng)
            for g in GROUPS[1:]:
                beta_dist[g].append(out[g]["beta_sim"])
        for g in GROUPS[1:]:
            arr = np.array(beta_dist[g])
            beta_pub = next(r[2] for r in T3 if r[0] == outcome and r[1] == g)
            se_pub   = next(r[3] for r in T3 if r[0] == outcome and r[1] == g)
            beta_sim_mean = float(arr.mean())
            beta_sim_std  = float(arr.std(ddof=1))
            # z-score of (sim - pub) in units of published SE
            z_vs_pub = (beta_sim_mean - beta_pub) / se_pub
            summary_rows.append({
                "outcome": outcome,
                "group": g,
                "beta_published": beta_pub,
                "SE_published": se_pub,
                "beta_sim_mean": round(beta_sim_mean, 4),
                "beta_sim_std":  round(beta_sim_std, 4),
                "abs_diff": round(abs(beta_sim_mean - beta_pub), 4),
                "z_vs_published_SE": round(z_vs_pub, 3),
                "agrees_within_2SE": bool(abs(z_vs_pub) <= 2.0),
            })
            for v in arr:
                boot_rows.append({"outcome": outcome, "group": g, "beta_sim": float(v)})
    pd.DataFrame(summary_rows).to_csv(RES / "table3_approx_refit_summary.csv", index=False)
    pd.DataFrame(boot_rows).to_csv(RES / "table3_approx_refit_bootstrap.csv", index=False)
    return pd.DataFrame(summary_rows)

# ---------- Figure: published vs simulated betas ----------
def plot_betas(summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, outcome in zip(axes, ["RBC", "PLT", "HB"]):
        sub = summary[summary["outcome"] == outcome]
        x = np.arange(len(sub))
        ax.errorbar(x - 0.1, sub["beta_published"], yerr=1.96 * sub["SE_published"],
                    fmt="o", color="black", label="published β ± 95% CI")
        ax.errorbar(x + 0.1, sub["beta_sim_mean"], yerr=1.96 * sub["beta_sim_std"],
                    fmt="s", color="C1", label="simulated refit β ± 1.96·std")
        ax.set_xticks(x); ax.set_xticklabels(sub["group"], rotation=20, ha="right", fontsize=8)
        ax.set_title(outcome); ax.axhline(0, color="grey", lw=0.5, ls="--")
        ax.legend(fontsize=8)
    fig.suptitle("Guo 2022 — published β vs simulated refit from Table 2 marginals")
    fig.tight_layout()
    fig.savefig(FIG / "beta_published_vs_simulated.png", dpi=150)
    plt.close(fig)

def main():
    print("=== (A) Internal consistency of Table 3 ===")
    a = check_internal_consistency()
    print(a.to_string(index=False))
    print()
    print("=== (B) Approximate refit from Table 2 marginals ===")
    b = approximate_refit()
    print(b.to_string(index=False))
    plot_betas(b)
    summary = {
        "paper": "Guo et al. 2022, Dose-Response 20(2)",
        "doi": "10.1177/15593258221105695",
        "n_workers": 705,
        "checks": {
            "internal_consistency": {
                "max_abs_Z_diff": float(a["Z_abs_diff"].max()),
                "max_abs_CI_lo_diff": float(a["CI_lo_abs_diff"].max()),
                "max_abs_CI_hi_diff": float(a["CI_hi_abs_diff"].max()),
            },
            "approximate_refit": {
                "n_bootstrap": N_BOOT,
                "n_betas_within_2_published_SE": int(b["agrees_within_2SE"].sum()),
                "n_betas_total": int(len(b)),
            }
        }
    }
    (RES / "summary.json").write_text(json.dumps(summary, indent=2))
    print("\nWrote:")
    for p in sorted(RES.glob("*")):
        print(" ", p)
    for p in sorted(FIG.glob("*")):
        print(" ", p)

if __name__ == "__main__":
    main()
