#!/usr/bin/env python3
"""
Replication of Turner et al. BMC Mol Cell Biol 2019, 20:13
DOI: 10.1186/s12860-019-0195-2

"Effect of dose and dose rate on temporal γ-H2AX kinetics in mouse blood
and spleen mononuclear cells in vivo following Cesium-137 administration"

Model (paper Eq. 1):
    F(A,t) = b + k * A * t * exp(Q1 + Q2)
    Q1     = -α * A
    Q2     = 1 - (1 + r*t)^p

with parameters fit by maximum-likelihood / nonlinear weighted least squares.
Authors' reported best fit (blood MNCs, Table 2):
    b = 1006            (fixed = control mean)
    k = 4.65e5  (MBq^-1 day^-1)
    α = 0.255   (MBq^-1)
    r = 1.07e6  (day^-1)
    p = 0.153   (unitless)

We refit the same model to the published Table S2 means, weighted by SEMs,
and reproduce the figures and Monte-Carlo activity-inversion.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import minimize
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
RES = ROOT / "results"
FIG.mkdir(exist_ok=True)
RES.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
def model_F(A, t, b, k, alpha, r, p):
    """γ-H2AX fluorescence model, Turner et al. 2019, Eq. 1."""
    A = np.asarray(A, dtype=float)
    t = np.asarray(t, dtype=float)
    Q1 = -alpha * A
    # (1 + r*t) is huge here; (1+r*t)^p with p<<1 stays finite. Use exp(p*log()).
    Q2 = 1.0 - np.exp(p * np.log1p(r * t))
    return b + k * A * t * np.exp(Q1 + Q2)


def neg_log_like(params, A, t, F, sem, b_fixed, r_max=1e8):
    """Negative log likelihood (Gaussian, weights = 1/sem^2).

    Note: the (1 + r*t)^p term is highly degenerate when r*t >> 1 because
    (r*t)^p only depends on p*log(r) in that limit. To break the degeneracy
    and recover the paper's reported parameterization (r ~ 1e6, p ~ 0.15),
    we bound r to a physically sensible range r_max (paper's r is 1.07e6).
    """
    k, alpha, r, p = params
    # constraints
    if k <= 0 or r <= 0 or alpha <= 0 or p <= 0 or p >= 1.0:
        return 1e15
    if r > r_max:
        return 1e15
    Fm = model_F(A, t, b_fixed, k, alpha, r, p)
    resid = (F - Fm) / sem
    return 0.5 * np.sum(resid * resid)


def fit_model(df_irr, b_fixed, x0=None):
    """Fit the 4 free parameters to irradiated data only (paper's procedure)."""
    A = df_irr["activity_MBq"].values
    t = df_irr["time_d"].values
    F = df_irr["F_mean"].values
    sem = df_irr["F_sem"].values

    if x0 is None:
        x0 = [4.65e5, 0.255, 1.07e6, 0.153]  # paper's reported values

    # Multi-start to reduce local-minimum risk
    best = None
    starts = [
        x0,
        [1e5, 0.10, 1e5, 0.20],
        [1e6, 0.40, 5e6, 0.10],
        [3e5, 0.30, 5e5, 0.15],
        [5e5, 0.25, 1e6, 0.15],
        [4.65e5, 0.255, 1.07e6, 0.153],  # paper's reported best fit
    ]
    for s0 in starts:
        try:
            res = minimize(
                neg_log_like,
                s0,
                args=(A, t, F, sem, b_fixed),
                method="Nelder-Mead",
                options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 100000, "maxfev": 100000},
            )
            if best is None or res.fun < best.fun:
                best = res
        except Exception:
            continue
    return best


# -----------------------------------------------------------------------------
# Profile-likelihood-ish CIs by random sampling within 95% NLL region
# -----------------------------------------------------------------------------
from scipy.stats import chi2


def parameter_ci_samples(best, A, t, F, sem, b_fixed, n=20000, scale=0.5, rng_seed=42):
    """Sample around best fit; keep those within Δ(-2 logL) ≤ χ²(0.95, df=1) = 3.84.

    Returns array of accepted parameter vectors (k, α, r, p) plus the
    threshold used.  Used both for CIs and for Monte-Carlo activity inversion.
    """
    rng = np.random.default_rng(rng_seed)
    nll0 = best.fun  # already 0.5 * SSR_w
    thresh = nll0 + 0.5 * chi2.ppf(0.95, df=1)  # for single-param CI
    # for joint 4-param region use df=4
    thresh_joint = nll0 + 0.5 * chi2.ppf(0.95, df=4)

    accepted = []
    p0 = np.array(best.x)
    # log-space jitter so r, k can vary widely
    log_p0 = np.log(p0)
    for _ in range(n):
        step = rng.normal(scale=scale, size=4)
        cand = np.exp(log_p0 + step)
        if cand[3] >= 1.0 or cand[3] <= 0:
            continue
        nll = neg_log_like(cand, A, t, F, sem, b_fixed)
        if nll <= thresh_joint:
            accepted.append((cand, nll))
    return accepted, thresh, thresh_joint


def per_param_ci(accepted, idx, best_val):
    """1-D CIs from accepted samples (rough; paper uses true profile likelihood)."""
    vals = np.array([a[0][idx] for a in accepted])
    return float(vals.min()), float(vals.max())


# -----------------------------------------------------------------------------
# Activity inversion
# -----------------------------------------------------------------------------
def invert_activity(F_obs, t, b, k, alpha, r, p, A_grid=None):
    """For given F, t and parameters, find A minimizing (F_model(A,t) - F)^2."""
    if A_grid is None:
        A_grid = np.linspace(0.01, 20.0, 4000)
    F_pred = model_F(A_grid, t, b, k, alpha, r, p)
    return A_grid[np.argmin((F_pred - F_obs) ** 2)]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    blood = pd.read_csv(DATA / "blood_h2ax.csv")
    spleen = pd.read_csv(DATA / "spleen_h2ax.csv")

    # Background (control) mean → b
    b_blood = blood.loc[blood.activity_MBq == 0, "F_mean"].mean()
    b_spleen = spleen.loc[spleen.activity_MBq == 0, "F_mean"].mean()
    print(f"Blood control mean   b = {b_blood:.1f}  (paper: 1006 ± 36)")
    print(f"Spleen control mean  b = {b_spleen:.1f}  (paper: 878 ± 18)")

    out_lines = []
    out_lines.append("# Replication results — Turner et al. 2019\n")
    out_lines.append(f"Blood control mean (fitted b): {b_blood:.1f} (paper: 1006)\n")
    out_lines.append(f"Spleen control mean (fitted b): {b_spleen:.1f} (paper: 878)\n\n")

    # -- Fit blood --
    blood_irr = blood[blood.activity_MBq > 0].reset_index(drop=True)
    best = fit_model(blood_irr, b_fixed=b_blood)
    k, alpha, r, p = best.x
    print("\n--- BLOOD FIT ---")
    print(f"  k     = {k:.3e}   (paper 4.65e5)")
    print(f"  alpha = {alpha:.4f}   (paper 0.255)")
    print(f"  r     = {r:.3e}   (paper 1.07e6)")
    print(f"  p     = {p:.4f}   (paper 0.153)")
    print(f"  weighted SSR (2*NLL) = {2*best.fun:.3f}  on {len(blood_irr)} points")

    out_lines.append("## Blood MNC fit\n\n")
    out_lines.append("| param | replication | paper best | paper 95% CI |\n")
    out_lines.append("|------|-------------|-----------|-------------|\n")
    paper_blood = {
        "k": (4.65e5, (3.28e5, 6.60e5)),
        "α": (0.255, (0.183, 0.323)),
        "r": (1.07e6, (7.54e5, 1.52e6)),
        "p": (0.153, (0.146, 0.159)),
    }
    my_vals = {"k": k, "α": alpha, "r": r, "p": p}
    for name in ["k", "α", "r", "p"]:
        v = my_vals[name]
        bv, (lo, hi) = paper_blood[name]
        out_lines.append(
            f"| {name} | {v:.4g} | {bv:.4g} | {lo:.3g} – {hi:.3g} |\n"
        )
    out_lines.append(f"\nWeighted SSR (2·NLL): {2*best.fun:.3f} on n={len(blood_irr)}\n\n")

    # -- Monte Carlo CI sampling --
    A_arr = blood_irr["activity_MBq"].values
    t_arr = blood_irr["time_d"].values
    F_arr = blood_irr["F_mean"].values
    sem_arr = blood_irr["F_sem"].values

    accepted, thr1, thrJ = parameter_ci_samples(
        best, A_arr, t_arr, F_arr, sem_arr, b_blood, n=30000, scale=0.6
    )
    print(f"  accepted (within joint 95% region) = {len(accepted)}")
    out_lines.append(
        f"Monte-Carlo accepted parameter sets within joint 95% region: **{len(accepted)}** of 30000 attempts.\n\n"
    )

    if accepted:
        ranges = {}
        for i, name in enumerate(["k", "α", "r", "p"]):
            lo, hi = per_param_ci(accepted, i, best.x[i])
            ranges[name] = (lo, hi)
            out_lines.append(
                f"- replicated joint 95% range for **{name}**: {lo:.3g} – {hi:.3g}\n"
            )
        out_lines.append("\n")

    # -- Plot Fig. 4-style curves --
    times = np.linspace(0.01, 14, 200)
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = {5.74: "tab:blue", 6.66: "tab:orange", 7.65: "tab:green", 9.28: "tab:red"}
    for A_lvl, sub in blood_irr.groupby("activity_MBq"):
        c = colors[A_lvl]
        ax.errorbar(
            sub["time_d"], sub["F_mean"], yerr=sub["F_sem"],
            fmt="o", color=c, label=f"{A_lvl} MBq",
        )
        Fm = model_F(A_lvl, times, b_blood, k, alpha, r, p)
        ax.plot(times, Fm, "-", color=c)
    ax.axhline(b_blood, ls="--", color="grey", label=f"control b={b_blood:.0f}")
    ax.set_xlabel("Time after injection (days)")
    ax.set_ylabel("Mean γ-H2AX fluorescence (a.u.)")
    ax.set_title("Replication of Turner et al. 2019, Fig. 4 (blood MNCs)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig4_replication_blood.png", dpi=140)
    plt.close(fig)

    # -- Monte Carlo activity inversion (Fig. 5 replication) --
    # For each (A_true, t) data point, compute predicted activity using each
    # accepted parameter set; collect median + min/max.
    rng = np.random.default_rng(7)
    sub_accepted = accepted if len(accepted) <= 2000 else [
        accepted[i] for i in rng.choice(len(accepted), 2000, replace=False)
    ]

    inv_records = []
    for _, row in blood_irr.iterrows():
        ests = []
        for params, _nll in sub_accepted:
            kk, aa, rr, pp = params
            A_est = invert_activity(row["F_mean"], row["time_d"], b_blood, kk, aa, rr, pp)
            ests.append(A_est)
        ests = np.array(ests)
        # also estimate using best-fit
        A_best = invert_activity(row["F_mean"], row["time_d"], b_blood, k, alpha, r, p)
        inv_records.append({
            "activity_MBq_true": row["activity_MBq"],
            "time_d": row["time_d"],
            "F_mean": row["F_mean"],
            "A_est_bestfit": A_best,
            "A_est_median": float(np.median(ests)),
            "A_est_min": float(np.min(ests)),
            "A_est_max": float(np.max(ests)),
        })
    inv_df = pd.DataFrame(inv_records)
    inv_df.to_csv(RES / "blood_inversion.csv", index=False)

    # Correlations by time window
    out_lines.append("## Replicated correlations (true vs Monte-Carlo median) — blood\n\n")
    out_lines.append("Paper Table 3 reported (Pearson, Spearman):\n\n")
    out_lines.append("| Time | paper Pearson (p) | paper Spearman (p) | replicated Pearson (p) | replicated Spearman (p) |\n")
    out_lines.append("|------|-------------------|---------------------|-----------------------|------------------------|\n")
    paper_corrs = {
        (2, 3):   ("0.857 (0.00659)", "0.929 (0.00223)"),
        (2, 5):   ("0.610 (0.0350)",  "0.804 (0.00161)"),
        (2, 7):   ("0.539 (0.0312)",  "0.691 (0.00302)"),
        (2, 14):  ("0.337 (0.147)",   "0.380 (0.0980)"),
    }
    correlations = {}
    for (lo, hi), (pp, ps) in paper_corrs.items():
        mask = (inv_df["time_d"] >= lo) & (inv_df["time_d"] <= hi)
        x = inv_df.loc[mask, "activity_MBq_true"].values
        y = inv_df.loc[mask, "A_est_median"].values
        if len(x) >= 3:
            pr, pp_val = pearsonr(x, y)
            sr, sp_val = spearmanr(x, y)
        else:
            pr, pp_val, sr, sp_val = (np.nan,) * 4
        out_lines.append(
            f"| {lo}–{hi} d | {pp} | {ps} | {pr:.3f} ({pp_val:.3g}) | {sr:.3f} ({sp_val:.3g}) |\n"
        )
        correlations[f"{lo}-{hi}d"] = {
            "pearson_r": pr, "pearson_p": pp_val,
            "spearman_r": sr, "spearman_p": sp_val,
        }

    # Fig 5 replication
    fig, ax = plt.subplots(figsize=(7, 5))
    times_unique = sorted(inv_df["time_d"].unique())
    cmap = plt.get_cmap("viridis", len(times_unique))
    for i, td in enumerate(times_unique):
        sub = inv_df[inv_df["time_d"] == td].sort_values("activity_MBq_true")
        ax.errorbar(
            sub["activity_MBq_true"], sub["A_est_median"],
            yerr=[sub["A_est_median"] - sub["A_est_min"],
                  sub["A_est_max"] - sub["A_est_median"]],
            fmt="o-", color=cmap(i), label=f"{td} d", capsize=3,
        )
    lim = [0, 11]
    ax.plot(lim, lim, "k--", label="1:1")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("True injected 137Cs activity (MBq)")
    ax.set_ylabel("Estimated injected activity (MBq)")
    ax.set_title("Replication of Turner et al. 2019, Fig. 5 (blood)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig5_replication_blood.png", dpi=140)
    plt.close(fig)

    # -- ROC (Fig S2 replication) --
    # Binary: low (5.74, 6.66) = 0; high (7.65, 9.28) = 1.
    # Score: estimated activity scaled to max across mice groups.
    from sklearn.metrics import roc_auc_score, roc_curve
    y_true = (inv_df["activity_MBq_true"] >= 7.0).astype(int).values
    score = (inv_df["A_est_median"] / inv_df["A_est_median"].max()).values
    try:
        auc = roc_auc_score(y_true, score)
        fpr, tpr, _ = roc_curve(y_true, score)
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot(fpr, tpr, "-", label=f"AUC={auc:.3f}")
        ax.plot([0, 1], [0, 1], "k--", alpha=0.4)
        ax.set_xlabel("FPR"); ax.set_ylabel("TPR")
        ax.set_title("ROC: low (5.74,6.66) vs high (7.65,9.28) MBq — replicated")
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIG / "figS2_replication_roc.png", dpi=140)
        plt.close(fig)
        out_lines.append(f"\n## ROC analysis\n\nReplicated AUC = {auc:.3f} (paper: 0.93, CI 0.806–1.0)\n")
        correlations["AUC"] = float(auc)
    except Exception as e:
        out_lines.append(f"\n## ROC analysis FAILED: {e}\n")

    # -- Spleen fit (paper says it fails for early time points; we just do whole-set fit) --
    spleen_irr = spleen[spleen.activity_MBq > 0].reset_index(drop=True)
    try:
        best_s = fit_model(spleen_irr, b_fixed=b_spleen)
        kS, aS, rS, pS = best_s.x
        print("\n--- SPLEEN FIT ---")
        print(f"  k={kS:.3e} α={aS:.4f} r={rS:.3e} p={pS:.4f}")
        out_lines.append("\n## Spleen MNC fit (paper: only day 14 meaningful)\n")
        out_lines.append(f"- k = {kS:.3g}, α = {aS:.3g}, r = {rS:.3g}, p = {pS:.3g}\n")
        out_lines.append(f"- weighted SSR = {2*best_s.fun:.3f}\n")
        # Day-14 only correlation as the paper highlighted
        sub14 = spleen_irr[spleen_irr.time_d == 14]
        A14_est = []
        for _, row in sub14.iterrows():
            A14_est.append(invert_activity(row["F_mean"], row["time_d"], b_spleen, kS, aS, rS, pS))
        if len(A14_est) >= 3:
            pr, pp_v = pearsonr(sub14["activity_MBq"], A14_est)
            sr, sp_v = spearmanr(sub14["activity_MBq"], A14_est)
            out_lines.append(
                f"- spleen day-14 Pearson r = {pr:.3f} (p={pp_v:.3g}); paper: 0.866 (p=0.134)\n"
                f"- spleen day-14 Spearman r = {sr:.3f} (p={sp_v:.3g}); paper: 1.0 (p=0.083)\n"
            )
    except Exception as e:
        out_lines.append(f"\nSpleen fit failed: {e}\n")

    # Save summary
    (RES / "summary.md").write_text("".join(out_lines))
    print("\nWrote", RES / "summary.md")
    print("Wrote", FIG / "fig4_replication_blood.png")
    print("Wrote", FIG / "fig5_replication_blood.png")
    print("Wrote", FIG / "figS2_replication_roc.png")

    # Also dump a JSON of the headline numbers
    import json
    headline = {
        "blood_b": b_blood,
        "blood_best_fit": {"k": k, "alpha": alpha, "r": r, "p": p,
                            "weighted_SSR": 2*best.fun, "n_pts": len(blood_irr)},
        "paper_blood_best_fit": {"k": 4.65e5, "alpha": 0.255, "r": 1.07e6, "p": 0.153},
        "correlations_replicated": correlations,
        "paper_correlations": {
            "2-3d": {"pearson_r": 0.857, "pearson_p": 0.00659,
                     "spearman_r": 0.929, "spearman_p": 0.00223},
            "2-5d": {"pearson_r": 0.610, "pearson_p": 0.0350,
                     "spearman_r": 0.804, "spearman_p": 0.00161},
            "2-7d": {"pearson_r": 0.539, "pearson_p": 0.0312,
                     "spearman_r": 0.691, "spearman_p": 0.00302},
            "2-14d": {"pearson_r": 0.337, "pearson_p": 0.147,
                      "spearman_r": 0.380, "spearman_p": 0.0980},
            "AUC": 0.93,
        },
    }
    (RES / "headline.json").write_text(json.dumps(headline, indent=2, default=str))


if __name__ == "__main__":
    main()
