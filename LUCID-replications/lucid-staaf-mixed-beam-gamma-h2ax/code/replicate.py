"""
Replication of Staaf et al. 2012 (Genome Integrity 3:8) — mixed-beam γ-H2AX.

Goals:
  1. Refit linear dose-response curves for X-ray, alpha, mixed-observed,
     mixed-predicted IRIF (total and large) and reproduce the reported R²
     and slope/RBE values.
  2. Reproduce author's "additivity" prediction independently:
        f_mix_pred(D_α, D_X) = f_α(D_α) + f_X(D_X)
     where each component dose in mixed beam is 25% α / 75% X.
  3. Test the "large-foci delay" hypothesis: relative LF fraction observed
     vs predicted at the 0.5 h time point (Fig 5).
  4. Produce all figures and a comparison table.
"""

import sys, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "data"))
import digitized_data as DD  # noqa

OUTDIR = os.path.abspath(os.path.join(HERE, "..", "results"))
FIGDIR = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(FIGDIR, exist_ok=True)


def to_arrays(points):
    """Convert list of (x, y, sd) tuples to numpy arrays."""
    a = np.array(points, dtype=float)
    return a[:, 0], a[:, 1], a[:, 2]


def linfit_through_origin(x, y, sd=None):
    """Linear fit y = b*x (forced through origin)."""
    x = np.asarray(x); y = np.asarray(y)
    if sd is not None:
        w = 1.0 / np.maximum(np.asarray(sd), 1e-9) ** 2
        b = np.sum(w * x * y) / np.sum(w * x * x)
        # residual std error of slope
        resid = y - b * x
        # weighted R^2
        ss_res = np.sum(w * resid ** 2)
        ss_tot = np.sum(w * (y - np.average(y, weights=w)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        # slope SE
        b_se = np.sqrt(1.0 / np.sum(w * x * x))
        return b, b_se, r2
    else:
        b = np.sum(x * y) / np.sum(x * x)
        resid = y - b * x
        ss_res = np.sum(resid ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        b_se = np.sqrt(ss_res / max(len(x) - 1, 1) / np.sum(x * x))
        return b, b_se, r2


def linfit(x, y):
    """Standard linear regression y = a + b*x using scipy."""
    res = stats.linregress(x, y)
    return res.slope, res.intercept, res.rvalue ** 2, res.stderr


def fit_with_origin_anchor(points, anchor_zero=True, baseline=0.0):
    """
    Fit linear y = a + b*x.
    If anchor_zero, also include a (0, baseline) point with the baseline foci value,
    which matches the author's approach (control subtracted).
    """
    x, y, sd = to_arrays(points)
    if anchor_zero:
        x = np.concatenate([[0.0], x])
        y = np.concatenate([[baseline], y])
        sd = np.concatenate([[sd.mean()], sd])
    slope, intercept, r2, se = linfit(x, y)
    return {
        "slope": float(slope), "intercept": float(intercept),
        "R2": float(r2), "slope_SE": float(se),
        "x": x.tolist(), "y": y.tolist(),
    }


def main():
    results = {}

    # =========================================================================
    # 1. Dose response fits (Figure 2A, 2B, 3A, 3B)
    # =========================================================================
    results["fits"] = {}

    for figname, datasets in [
        ("fig2A_totalIRIF_number_vs_dose", {
            "xray":      DD.fig2A_xray,
            "alpha":     DD.fig2A_alpha,
            "mixed_obs": DD.fig2A_mixed_obs,
            "mixed_pred":DD.fig2A_mixed_pred,
        }),
        ("fig2B_totalIRIF_area_vs_dose", {
            "xray":      DD.fig2B_xray,
            "alpha":     DD.fig2B_alpha,
            "mixed_obs": DD.fig2B_mixed_obs,
            "mixed_pred":DD.fig2B_mixed_pred,
        }),
        ("fig3A_LF_number_vs_dose", {
            "xray":      DD.fig3A_xray,
            "alpha":     DD.fig3A_alpha,
            "mixed_obs": DD.fig3A_mixed_obs,
            "mixed_pred":DD.fig3A_mixed_pred,
        }),
        ("fig3B_LF_area_vs_dose", {
            "xray":      DD.fig3B_xray,
            "alpha":     DD.fig3B_alpha,
            "mixed_obs": DD.fig3B_mixed_obs,
            "mixed_pred":DD.fig3B_mixed_pred,
        }),
    ]:
        results["fits"][figname] = {}
        for series_name, points in datasets.items():
            r = fit_with_origin_anchor(points, anchor_zero=True)
            results["fits"][figname][series_name] = r

    # =========================================================================
    # 2. RBE = slope_alpha / slope_X for total IRIF and LF (number-based)
    # =========================================================================
    sX_tot = results["fits"]["fig2A_totalIRIF_number_vs_dose"]["xray"]["slope"]
    sA_tot = results["fits"]["fig2A_totalIRIF_number_vs_dose"]["alpha"]["slope"]
    seX_tot = results["fits"]["fig2A_totalIRIF_number_vs_dose"]["xray"]["slope_SE"]
    seA_tot = results["fits"]["fig2A_totalIRIF_number_vs_dose"]["alpha"]["slope_SE"]
    rbe_tot = sA_tot / sX_tot
    # SD propagation: SD(A/X) ≈ |A/X| * sqrt((sA/A)^2 + (sX/X)^2)
    rbe_tot_sd = abs(rbe_tot) * np.sqrt((seA_tot / sA_tot) ** 2 +
                                         (seX_tot / sX_tot) ** 2)

    sX_lf = results["fits"]["fig3A_LF_number_vs_dose"]["xray"]["slope"]
    sA_lf = results["fits"]["fig3A_LF_number_vs_dose"]["alpha"]["slope"]
    seX_lf = results["fits"]["fig3A_LF_number_vs_dose"]["xray"]["slope_SE"]
    seA_lf = results["fits"]["fig3A_LF_number_vs_dose"]["alpha"]["slope_SE"]
    rbe_lf = sA_lf / sX_lf
    rbe_lf_sd = abs(rbe_lf) * np.sqrt((seA_lf / sA_lf) ** 2 +
                                       (seX_lf / sX_lf) ** 2)

    results["RBE"] = {
        "total_foci_replicated": {"value": float(rbe_tot), "sd": float(rbe_tot_sd)},
        "total_foci_reported":   {"value": 0.76, "sd": 0.52},
        "large_foci_replicated": {"value": float(rbe_lf), "sd": float(rbe_lf_sd)},
        "large_foci_reported":   {"value": 2.54, "sd": 1.11},
    }

    # =========================================================================
    # 3. Independent additivity check at the three mixed doses (2A)
    # =========================================================================
    # mixed = 25% alpha + 75% X
    # mixed total 0.27 -> 0.07 alpha + 0.20 X
    # mixed total 0.53 -> 0.13 alpha + 0.40 X
    # mixed total 0.80 -> 0.20 alpha + 0.60 X
    # (Per paper, exact split for 0.80 mixed: 0.20 alpha + 0.60 X. We'll use these.)
    component_doses = [
        (0.27, 0.07, 0.20),
        (0.53, 0.13, 0.40),
        (0.80, 0.20, 0.60),
    ]

    def f_from_fit(fit, d):
        return fit["intercept"] + fit["slope"] * d

    fX_tot = results["fits"]["fig2A_totalIRIF_number_vs_dose"]["xray"]
    fA_tot = results["fits"]["fig2A_totalIRIF_number_vs_dose"]["alpha"]
    fX_lf  = results["fits"]["fig3A_LF_number_vs_dose"]["xray"]
    fA_lf  = results["fits"]["fig3A_LF_number_vs_dose"]["alpha"]

    additivity_total = []
    additivity_LF = []
    for dtot, da, dx in component_doses:
        pred_tot = f_from_fit(fA_tot, da) + f_from_fit(fX_tot, dx)
        pred_lf  = f_from_fit(fA_lf,  da) + f_from_fit(fX_lf,  dx)
        # observed values
        obs_tot = dict([(p[0], (p[1], p[2])) for p in DD.fig2A_mixed_obs])[dtot]
        obs_lf  = dict([(p[0], (p[1], p[2])) for p in DD.fig3A_mixed_obs])[dtot]
        author_pred_tot = dict([(p[0], (p[1], p[2])) for p in DD.fig2A_mixed_pred])[dtot]
        author_pred_lf  = dict([(p[0], (p[1], p[2])) for p in DD.fig3A_mixed_pred])[dtot]
        additivity_total.append({
            "dose_total_Gy": dtot, "dose_alpha_Gy": da, "dose_X_Gy": dx,
            "observed":      obs_tot[0], "observed_SD": obs_tot[1],
            "our_predicted": float(pred_tot),
            "author_predicted": author_pred_tot[0],
            "diff_obs_minus_pred": float(obs_tot[0] - pred_tot),
        })
        additivity_LF.append({
            "dose_total_Gy": dtot, "dose_alpha_Gy": da, "dose_X_Gy": dx,
            "observed":      obs_lf[0], "observed_SD": obs_lf[1],
            "our_predicted": float(pred_lf),
            "author_predicted": author_pred_lf[0],
            "diff_obs_minus_pred": float(obs_lf[0] - pred_lf),
        })

    results["additivity_total_IRIF"] = additivity_total
    results["additivity_LF"] = additivity_LF

    # =========================================================================
    # 4. Large-foci DELAY test: Fig 5 — observed vs predicted relative LF at
    #    each time point (paired t-test of difference).
    # =========================================================================
    def paired_t_from_means(m1, sd1, m2, sd2, n):
        """Approximate Welch two-sample t (we don't have raw paired data)."""
        se = np.sqrt(sd1 ** 2 / n + sd2 ** 2 / n)
        t  = (m1 - m2) / se if se > 0 else float("nan")
        dof = n - 1
        p   = 2 * (1 - stats.t.cdf(abs(t), dof))
        return float(t), float(p)

    n_experiments = 4  # paper reports 4 independent experiments
    lf_delay_tests = []
    for (t, obs_m, obs_sd), (_, pred_m, pred_sd) in zip(DD.fig5A_obs, DD.fig5A_pred):
        t_stat, p_val = paired_t_from_means(obs_m, obs_sd, pred_m, pred_sd, n_experiments)
        lf_delay_tests.append({
            "time_h": t,
            "obs_relative_LF_pct": obs_m, "obs_SD": obs_sd,
            "pred_relative_LF_pct": pred_m, "pred_SD": pred_sd,
            "diff_obs_minus_pred": obs_m - pred_m,
            "t_stat": t_stat, "p_value": p_val,
        })
    results["large_foci_delay_number_test"] = lf_delay_tests

    lf_delay_area = []
    for (t, obs_m, obs_sd), (_, pred_m, pred_sd) in zip(DD.fig5B_obs, DD.fig5B_pred):
        t_stat, p_val = paired_t_from_means(obs_m, obs_sd, pred_m, pred_sd, n_experiments)
        lf_delay_area.append({
            "time_h": t,
            "obs_relative_LF_area_pct": obs_m, "obs_SD": obs_sd,
            "pred_relative_LF_area_pct": pred_m, "pred_SD": pred_sd,
            "diff_obs_minus_pred": obs_m - pred_m,
            "t_stat": t_stat, "p_value": p_val,
        })
    results["large_foci_delay_area_test"] = lf_delay_area

    # =========================================================================
    # 5. Fluence cross-check: alpha particles per nucleus for 0.27 Gy, 60s
    # =========================================================================
    flu, flu_sd = DD.reported["fluence_alpha_particles_per_s_per_cm2"]
    avg_area, _ = DD.reported["avg_DNA_area_um2_doseresp"]  # μm²
    # particles per nucleus = (flu / 1e8 [µm²/cm²]) * avg_area * time_s
    particles_per_nucleus = (flu / 1e8) * avg_area * 60.0
    particles_per_nucleus_sd = (flu_sd / 1e8) * avg_area * 60.0
    results["fluence_check"] = {
        "calculated_particles_per_nucleus_60s_0p27Gy":
            {"value": float(particles_per_nucleus), "sd": float(particles_per_nucleus_sd)},
        "reported_in_paper":
            {"value": 3.57, "sd": 0.68},
    }

    # =========================================================================
    # WRITE JSON RESULTS
    # =========================================================================
    with open(os.path.join(OUTDIR, "replication_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # =========================================================================
    # FIGURES
    # =========================================================================

    # Figure rep-2A: total IRIF number vs dose with linear fits
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, points, marker, color, label in [
        ("xray",   DD.fig2A_xray,  "o", "k", "X-ray (digitized)"),
        ("alpha",  DD.fig2A_alpha, "o", "tab:red", "Alpha (digitized)"),
        ("mixed_obs",  DD.fig2A_mixed_obs,  "s", "tab:blue",   "Mixed observed (digitized)"),
        ("mixed_pred", DD.fig2A_mixed_pred, "s", "lightgray",  "Mixed predicted by authors"),
    ]:
        x, y, sd = to_arrays(points)
        ax.errorbar(x, y, yerr=sd, fmt=marker, color=color, label=label, capsize=3,
                    markerfacecolor=("white" if "obs" in name or name in ("alpha",) else color))
        fit = results["fits"]["fig2A_totalIRIF_number_vs_dose"][name]
        xx = np.linspace(0, 0.85, 50)
        ax.plot(xx, fit["intercept"] + fit["slope"] * xx, "--", color=color, alpha=0.6,
                label=f"  fit: y={fit['intercept']:.2f}+{fit['slope']:.2f}D, R²={fit['R2']:.2f}")
    # Overlay our independent additivity prediction
    doses = [d[0] for d in component_doses]
    pred_y = [row["our_predicted"] for row in additivity_total]
    ax.plot(doses, pred_y, "^", color="green", markersize=10, label="Mixed predicted (this work, from α & X fits)")
    ax.set_xlabel("Total dose (Gy)")
    ax.set_ylabel("γ-H2AX IRIF per nucleus (1 h post-irradiation)")
    ax.set_title("Replication of Staaf et al. 2012, Fig 2A — Total IRIF dose response")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "rep_fig2A_total_IRIF_dose_response.png"), dpi=150)
    plt.close(fig)

    # Figure rep-3A: large foci number vs dose
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, points, marker, color, label in [
        ("xray",   DD.fig3A_xray,  "o", "k", "X-ray"),
        ("alpha",  DD.fig3A_alpha, "o", "tab:red", "Alpha"),
        ("mixed_obs",  DD.fig3A_mixed_obs,  "s", "tab:blue",   "Mixed observed"),
        ("mixed_pred", DD.fig3A_mixed_pred, "s", "lightgray",  "Mixed predicted (author)"),
    ]:
        x, y, sd = to_arrays(points)
        ax.errorbar(x, y, yerr=sd, fmt=marker, color=color, label=label, capsize=3,
                    markerfacecolor=("white" if "obs" in name or name in ("alpha",) else color))
        fit = results["fits"]["fig3A_LF_number_vs_dose"][name]
        xx = np.linspace(0, 0.85, 50)
        ax.plot(xx, fit["intercept"] + fit["slope"] * xx, "--", color=color, alpha=0.6,
                label=f"  fit: R²={fit['R2']:.2f}, slope={fit['slope']:.2f}")
    pred_y = [row["our_predicted"] for row in additivity_LF]
    ax.plot(doses, pred_y, "^", color="green", markersize=10, label="Mixed predicted (this work)")
    ax.set_xlabel("Total dose (Gy)")
    ax.set_ylabel("Large γ-H2AX foci per nucleus (1 h post-irradiation)")
    ax.set_title("Replication of Staaf et al. 2012, Fig 3A — LF dose response")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "rep_fig3A_LF_dose_response.png"), dpi=150)
    plt.close(fig)

    # Figure rep-5: large-foci delay (Fig 5A)
    fig, ax = plt.subplots(figsize=(7, 5))
    times = [r["time_h"] for r in lf_delay_tests]
    obs   = [r["obs_relative_LF_pct"] for r in lf_delay_tests]
    obs_sd= [r["obs_SD"] for r in lf_delay_tests]
    pred  = [r["pred_relative_LF_pct"] for r in lf_delay_tests]
    pred_sd=[r["pred_SD"] for r in lf_delay_tests]
    width = 0.18
    xpos = np.arange(len(times))
    ax.bar(xpos - width/2, pred, width, yerr=pred_sd, label="Predicted (additivity)", color="black", capsize=4)
    ax.bar(xpos + width/2, obs,  width, yerr=obs_sd,  label="Observed", color="lightgray", edgecolor="k", capsize=4)
    for i, r in enumerate(lf_delay_tests):
        sig = "**" if r["p_value"] < 0.01 else ("*" if r["p_value"] < 0.05 else "")
        if sig:
            ax.text(xpos[i], max(obs[i], pred[i]) + 6, sig, ha="center", fontsize=14)
    ax.set_xticks(xpos)
    ax.set_xticklabels([f"{t} h" for t in times])
    ax.set_ylabel("Relative LF number (% of total IRIF)")
    ax.set_title("Replication of Staaf 2012 Fig 5A — Large-foci delay test")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "rep_fig5A_LF_delay.png"), dpi=150)
    plt.close(fig)

    # Figure rep-5B: large-foci AREA delay (the headline finding)
    fig, ax = plt.subplots(figsize=(7, 5))
    times = [r["time_h"] for r in lf_delay_area]
    obs   = [r["obs_relative_LF_area_pct"] for r in lf_delay_area]
    obs_sd= [r["obs_SD"] for r in lf_delay_area]
    pred  = [r["pred_relative_LF_area_pct"] for r in lf_delay_area]
    pred_sd=[r["pred_SD"] for r in lf_delay_area]
    width = 0.18
    xpos = np.arange(len(times))
    ax.bar(xpos - width/2, pred, width, yerr=pred_sd, label="Predicted (additivity)", color="black", capsize=4)
    ax.bar(xpos + width/2, obs,  width, yerr=obs_sd,  label="Observed", color="lightgray", edgecolor="k", capsize=4)
    for i, r in enumerate(lf_delay_area):
        sig = "**" if r["p_value"] < 0.01 else ("*" if r["p_value"] < 0.05 else "")
        if sig:
            ax.text(xpos[i], max(obs[i], pred[i]) + 6, sig, ha="center", fontsize=14)
    ax.set_xticks(xpos)
    ax.set_xticklabels([f"{t} h" for t in times])
    ax.set_ylabel("Relative LF area (% of total IRIF area)")
    ax.set_title("Replication of Staaf 2012 Fig 5B \u2014 LARGE-FOCI DELAY (headline)\n"
                 "Observed << Predicted at 0.5 h \u2014 paper reports p<0.001")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "rep_fig5B_LF_AREA_delay_headline.png"), dpi=150)
    plt.close(fig)

    # Figure: repair kinetics (Fig 2C-D)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, datasets, ylabel, title in [
        (axes[0], {
            "X-ray (0.8 Gy)":    DD.fig2C_xray,
            "Alpha (0.27 Gy)":   DD.fig2C_alpha,
            "Mixed obs (0.53)":  DD.fig2C_mixed_obs,
            "Mixed pred":        DD.fig2C_mixed_pred,
        }, "IRIF per nucleus", "Fig 2C: total IRIF repair kinetics"),
        (axes[1], {
            "X-ray (0.8 Gy)":    DD.fig3C_xray,
            "Alpha (0.27 Gy)":   DD.fig3C_alpha,
            "Mixed obs (0.53)":  DD.fig3C_mixed_obs,
            "Mixed pred":        DD.fig3C_mixed_pred,
        }, "Large foci per nucleus", "Fig 3C: LF repair kinetics"),
    ]:
        for label, points in datasets.items():
            x, y, sd = to_arrays(points)
            ax.errorbar(x, y, yerr=sd, marker="o", label=label, capsize=3)
        ax.set_xlabel("Time after irradiation (h)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        ax.set_xscale("symlog", linthresh=1)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "rep_fig2C_3C_repair_kinetics.png"), dpi=150)
    plt.close(fig)

    # Console summary
    print("="*70)
    print("REPLICATION SUMMARY — Staaf et al. 2012")
    print("="*70)
    print(f"RBE_total (replicated): {rbe_tot:.2f} ± {rbe_tot_sd:.2f} | reported: 0.76 ± 0.52")
    print(f"RBE_LF    (replicated): {rbe_lf:.2f} ± {rbe_lf_sd:.2f} | reported: 2.54 ± 1.11")
    print()
    print("R² values (replicated vs reported):")
    for fn in ["xray", "alpha", "mixed_obs", "mixed_pred"]:
        r = results["fits"]["fig2A_totalIRIF_number_vs_dose"][fn]["R2"]
        rep = DD.reported.get(f"R2_{fn}_total", "?")
        print(f"  Total IRIF {fn}: {r:.2f}   reported: {rep}")
    for fn in ["xray", "alpha", "mixed_obs", "mixed_pred"]:
        r = results["fits"]["fig3A_LF_number_vs_dose"][fn]["R2"]
        rep = DD.reported.get(f"R2_{fn}_LF", "?")
        print(f"  LF         {fn}: {r:.2f}   reported: {rep}")
    print()
    print("Additivity check (total IRIF):")
    for row in additivity_total:
        print(f"  D={row['dose_total_Gy']} Gy: obs={row['observed']:.2f}±{row['observed_SD']:.2f}, "
              f"our_pred={row['our_predicted']:.2f}, author_pred={row['author_predicted']:.2f}")
    print()
    print("Additivity check (LF):")
    for row in additivity_LF:
        print(f"  D={row['dose_total_Gy']} Gy: obs={row['observed']:.2f}±{row['observed_SD']:.2f}, "
              f"our_pred={row['our_predicted']:.2f}, author_pred={row['author_predicted']:.2f}")
    print()
    print("Large-foci delay (Fig 5A): obs vs pred relative LF count")
    for r in lf_delay_tests:
        print(f"  t={r['time_h']} h: obs={r['obs_relative_LF_pct']:.1f}, "
              f"pred={r['pred_relative_LF_pct']:.1f}, diff={r['diff_obs_minus_pred']:+.1f}, "
              f"p≈{r['p_value']:.3f}")
    print()
    print(f"Fluence check: calc {results['fluence_check']['calculated_particles_per_nucleus_60s_0p27Gy']['value']:.2f} "
          f"± {results['fluence_check']['calculated_particles_per_nucleus_60s_0p27Gy']['sd']:.2f}  "
          f"vs reported 3.57 ± 0.68")
    print()
    print("Outputs:")
    print(f"  JSON:    {OUTDIR}/replication_results.json")
    print(f"  Figures: {FIGDIR}/*.png")


if __name__ == "__main__":
    main()
