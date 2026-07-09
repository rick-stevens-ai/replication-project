"""
Spot-check replication of Acheva et al. 2017 statistical claims.

What we re-do:
  1. From digitized mean+SEM+N values, reconstruct synthetic samples that
     have exactly that mean and SD = SEM * sqrt(N).  This lets us re-run
     a one-way ANOVA + Tukey HSD and compare the asterisks to those printed.
     With N=2 (Figs 2, 7) the test is essentially unpowered; with N=3
     (Fig 1) it is only marginally better.
  2. Re-fit Figure 2A (sc-236) and 2B (Bay 11-7085) MTT dose-response with
     a 4-parameter logistic and report IC50, then compare to the authors'
     chosen working concentrations (5 uM for sc-236, 1 uM for Bay 11-7085).
  3. Recompute the "PGE2 at 72 h is 6.5x baseline" claim against the
     digitized values.

Outputs go to ../results/.
"""
from __future__ import annotations
import json, math, os, sys
from pathlib import Path
import numpy as np
from scipy import stats, optimize

sys.path.insert(0, str(Path(__file__).parent))
from digitized_figures import (
    FIG1_SHIELDED, FIG1_IRRADIATED,
    FIG2A_SC236, FIG2B_BAY,
    FIG7A_CTRL, FIG7A_2GY,
    FIG7_CLAIM_FOLD_72H,
    FIG1_REPORTED_SIG,
)

RESULTS = Path(__file__).resolve().parent.parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
FIG_OUT = Path(__file__).resolve().parent.parent / "figures"
FIG_OUT.mkdir(parents=True, exist_ok=True)


def synth_samples(mean: float, sem: float, n: int) -> np.ndarray:
    """Return n values with exact mean and exact SD = sem*sqrt(n)."""
    if n < 2:
        raise ValueError("need n>=2")
    sd = sem * math.sqrt(n)
    # For n=2, the unique solution (up to order) for a sample with given mean
    # and SD is mean +- sd*sqrt((n-1)/n) ... actually for n=2, sd = |x1-x2|/sqrt(2)
    # so x = mean +- sd/sqrt(2).
    # We'll just construct any sample with exact mean and SD using a symmetric
    # construction around the mean.
    base = np.zeros(n)
    base[0] = -1.0
    base[-1] = 1.0
    # set remaining to zero; rescale to match desired SD and shift to mean
    if n > 2:
        # use a symmetric pattern with zeros in middle so SD comes from extremes
        pass
    cur_sd = np.std(base, ddof=1)
    if cur_sd == 0:
        return np.full(n, mean)
    base = base * (sd / cur_sd)
    base = base + mean
    # numerical sanity
    assert abs(np.mean(base) - mean) < 1e-6
    assert abs(np.std(base, ddof=1) - sd) < 1e-6
    return base


def reconstruct_groups(bars):
    return {b.label: synth_samples(b.mean, b.sem, b.n) for b in bars}


def oneway_anova_and_pairwise(groups: dict, alpha=0.05):
    labels = list(groups.keys())
    arrays = [groups[l] for l in labels]
    F, p = stats.f_oneway(*arrays)
    # Tukey HSD via scipy (>=1.7)
    try:
        from scipy.stats import tukey_hsd
        flat = arrays
        tk = tukey_hsd(*flat)
        n = len(labels)
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                pij = float(tk.pvalue[i, j])
                pairs.append({
                    "a": labels[i], "b": labels[j],
                    "mean_diff": float(np.mean(arrays[j]) - np.mean(arrays[i])),
                    "p_tukey": pij,
                    "asterisks": stars(pij),
                })
    except Exception as exc:
        pairs = [{"error": f"tukey_hsd unavailable: {exc}"}]
    return {
        "anova_F": float(F),
        "anova_p": float(p),
        "n_per_group": [int(len(a)) for a in arrays],
        "labels": labels,
        "pairwise_tukey": pairs,
    }


def stars(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    return "ns"


# ---------------- Figure 1 spot-check ----------------
def spotcheck_fig1():
    out = {}
    for arm, bars in [("shielded", FIG1_SHIELDED), ("irradiated", FIG1_IRRADIATED)]:
        groups = reconstruct_groups(bars)
        out[arm] = oneway_anova_and_pairwise(groups)
    # compare asterisks for irradiated arm to those reported
    pair_lookup = {(p["a"], p["b"]): p for p in out["irradiated"]["pairwise_tukey"]}
    pair_lookup.update({(p["b"], p["a"]): p for p in out["irradiated"]["pairwise_tukey"]})
    compare = []
    for a_full, b_full, reported in FIG1_REPORTED_SIG:
        a = a_full.split(":", 1)[1]
        b = b_full.split(":", 1)[1]
        key = (a, b)
        rec = pair_lookup.get(key, None)
        compare.append({
            "pair": f"{a} vs {b}",
            "reported_asterisks": reported,
            "our_p_tukey": rec["p_tukey"] if rec else None,
            "our_asterisks": rec["asterisks"] if rec else None,
            "agree_qualitatively":
                (rec and (rec["asterisks"] != "ns") and (reported in ("*", "**", "***")))
        })
    out["asterisk_comparison"] = compare
    return out


# ---------------- Figure 2 dose-response refit ----------------
def four_param_logistic(x, top, bottom, ic50, hill):
    return bottom + (top - bottom) / (1.0 + (x / ic50) ** hill)


def fit_mtt(bars, name):
    # x = concentration in uM; skip DMSO row (it isn't a dose of inhibitor)
    xs, ys, sems = [], [], []
    for b in bars:
        if b.label == "DMSO":
            continue
        xs.append(float(b.label))
        ys.append(b.mean)
        sems.append(b.sem if b.sem > 0 else 1.0)
    xs = np.array(xs); ys = np.array(ys); sems = np.array(sems)
    # need x > 0 for logistic in conc; replace 0 with a small value
    xs_fit = np.where(xs == 0, 1e-3, xs)
    p0 = [100.0, 0.0, np.median(xs_fit[xs_fit > 0]), 1.0]
    try:
        popt, pcov = optimize.curve_fit(
            four_param_logistic, xs_fit, ys, p0=p0, sigma=sems,
            absolute_sigma=False, maxfev=20000,
            bounds=([50, -10, 1e-4, 0.1], [150, 50, 1e3, 10.0]),
        )
        top, bottom, ic50, hill = popt
        # interpolated viability at the "working concentration" the authors used
        return {
            "name": name,
            "concentrations_uM": xs.tolist(),
            "viability_pct": ys.tolist(),
            "sem_pct": sems.tolist(),
            "fit_top": float(top),
            "fit_bottom": float(bottom),
            "fit_IC50_uM": float(ic50),
            "fit_hill": float(hill),
        }
    except Exception as exc:
        return {"name": name, "error": str(exc),
                "concentrations_uM": xs.tolist(),
                "viability_pct": ys.tolist()}


# ---------------- Figure 7 fold-change check ----------------
def check_fig7_fold():
    # author's claim: PGE2 at 72h post-2Gy is 6.5x baseline non-irradiated
    # which "baseline" do they mean? "initial levels of the non-irradiated
    # 3D cultures medium" => CTRL at 0h = 250 pg/ml (digitized)
    baseline_0h = FIG7A_CTRL[0].mean
    val_72h_2gy = FIG7A_2GY[-1].mean
    fold_vs_ctrl_0h = val_72h_2gy / baseline_0h if baseline_0h else float("inf")
    # Alternative: vs CTRL at 72h
    ctrl_72h = FIG7A_CTRL[-1].mean
    fold_vs_ctrl_72h = val_72h_2gy / ctrl_72h if ctrl_72h else float("inf")
    # Alternative: vs 2 Gy at 0 h (own time-zero)
    own_t0 = FIG7A_2GY[0].mean
    fold_vs_own_0h = val_72h_2gy / own_t0 if own_t0 else float("inf")
    return {
        "claim_in_paper_text": FIG7_CLAIM_FOLD_72H,
        "PGE2_2Gy_72h_pg_per_ml": val_72h_2gy,
        "PGE2_ctrl_0h_pg_per_ml": baseline_0h,
        "PGE2_ctrl_72h_pg_per_ml": ctrl_72h,
        "PGE2_2Gy_0h_pg_per_ml": own_t0,
        "fold_2Gy72h_over_ctrl0h": fold_vs_ctrl_0h,
        "fold_2Gy72h_over_ctrl72h": fold_vs_ctrl_72h,
        "fold_2Gy72h_over_2Gy0h": fold_vs_own_0h,
        "agrees_with_claim_within_30pct": abs(fold_vs_ctrl_0h - FIG7_CLAIM_FOLD_72H) / FIG7_CLAIM_FOLD_72H < 0.3
            if math.isfinite(fold_vs_ctrl_0h) else False,
    }


# ---------------- 2^-ddCT identity check ----------------
def ddct_identity_demo():
    """
    The paper gives the 2^-ddCT pipeline as Eqs:
        dCT_test  = CT_target_test - CT_ref_test
        dCT_calib = CT_target_calib - CT_ref_calib
        ddCT      = dCT_test - dCT_calib
        ratio     = 2^-ddCT
    Confirm with a synthetic example: a 2.4-fold upregulation should give
    ddCT = -log2(2.4) (when target gene rises and reference stays put).
    """
    fold_target = 2.4
    CT_target_test  = 25.0 - math.log2(fold_target)   # higher expression -> lower CT
    CT_target_calib = 25.0
    CT_ref_test     = 18.0
    CT_ref_calib    = 18.0
    dCT_test  = CT_target_test  - CT_ref_test
    dCT_calib = CT_target_calib - CT_ref_calib
    ddCT      = dCT_test - dCT_calib
    ratio     = 2 ** (-ddCT)
    return {
        "input_fold": fold_target,
        "CT_target_test": CT_target_test,
        "CT_target_calib": CT_target_calib,
        "CT_ref_test": CT_ref_test,
        "CT_ref_calib": CT_ref_calib,
        "ddCT": ddCT,
        "computed_ratio_2^-ddCT": ratio,
        "agrees": abs(ratio - fold_target) < 1e-9,
    }


def main():
    results = {}
    results["fig1_spotcheck"] = spotcheck_fig1()
    results["fig2a_sc236_fit"] = fit_mtt(FIG2A_SC236, "sc-236")
    results["fig2b_bay_fit"] = fit_mtt(FIG2B_BAY, "Bay 11-7085")
    results["fig7_fold_check"] = check_fig7_fold()
    results["ddct_identity"] = ddct_identity_demo()

    out_path = RESULTS / "spotcheck_results.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"Wrote {out_path}")

    # Pretty summary
    print()
    print("=" * 70)
    print("FIG 1 (COX-2 qRT-PCR) — irradiated arm asterisk audit")
    print("=" * 70)
    for c in results["fig1_spotcheck"]["asterisk_comparison"]:
        print(f"  {c['pair']:35s}  paper={c['reported_asterisks']:>3}  "
              f"our_p={c['our_p_tukey']:.4g}  our={c['our_asterisks']:>3}  "
              f"qual_agree={c['agree_qualitatively']}")

    print()
    print("=" * 70)
    print("FIG 2A (sc-236 MTT) 4PL fit")
    print("=" * 70)
    f2a = results["fig2a_sc236_fit"]
    print(f"  IC50 = {f2a.get('fit_IC50_uM', 'NA'):.3f} uM   hill={f2a.get('fit_hill','NA'):.3f}")
    print(f"  Authors used 5 uM as working dose; per fit, viability at 5 uM = "
          f"{four_param_logistic(5.0, f2a['fit_top'], f2a['fit_bottom'], f2a['fit_IC50_uM'], f2a['fit_hill']):.1f}%")

    print()
    print("=" * 70)
    print("FIG 2B (Bay 11-7085 MTT) 4PL fit")
    print("=" * 70)
    f2b = results["fig2b_bay_fit"]
    print(f"  IC50 = {f2b.get('fit_IC50_uM','NA'):.3f} uM   hill={f2b.get('fit_hill','NA'):.3f}")
    print(f"  Authors used 1 uM as working dose; per fit, viability at 1 uM = "
          f"{four_param_logistic(1.0, f2b['fit_top'], f2b['fit_bottom'], f2b['fit_IC50_uM'], f2b['fit_hill']):.1f}%")

    print()
    print("=" * 70)
    print("FIG 7 PGE2 fold-change check")
    print("=" * 70)
    f7 = results["fig7_fold_check"]
    print(f"  paper claim:                  PGE2 72h(2Gy) = {f7['claim_in_paper_text']} x baseline 0h")
    print(f"  our digitized 72h(2Gy):       {f7['PGE2_2Gy_72h_pg_per_ml']:.0f} pg/ml")
    print(f"  our digitized CTRL 0h:        {f7['PGE2_ctrl_0h_pg_per_ml']:.0f} pg/ml")
    print(f"  fold over CTRL 0h:            {f7['fold_2Gy72h_over_ctrl0h']:.2f}x  (claim agrees? {f7['agrees_with_claim_within_30pct']})")
    print(f"  fold over CTRL 72h:           {f7['fold_2Gy72h_over_ctrl72h']:.2f}x")
    print(f"  fold over 2Gy 0h (own t0):    {f7['fold_2Gy72h_over_2Gy0h']:.2f}x  <-- this is what 6.5x most likely means")

    print()
    print("=" * 70)
    print("2^-ddCT identity check")
    print("=" * 70)
    d = results["ddct_identity"]
    print(f"  input fold = {d['input_fold']}  ->  computed ratio = {d['computed_ratio_2^-ddCT']:.6f}  agree={d['agrees']}")


if __name__ == "__main__":
    main()
