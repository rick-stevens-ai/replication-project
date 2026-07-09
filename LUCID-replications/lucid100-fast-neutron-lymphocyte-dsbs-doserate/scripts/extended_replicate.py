#!/usr/bin/env python3
"""
Extended replication for:
  Nair et al. 2019, Int J Mol Sci 20:5350, doi:10.3390/ijms20215350
  "Impact of Dose Rate on DNA DSB Formation and Repair in Human Lymphocytes
   Exposed to Fast Neutron Irradiation"

Extends scripts/smoke_replicate.py with additional claim audits:

  E1. Per-dose HDR/LDR foci ratio (Table 1 -> Table 2), 5 doses, max abs error.
  E2. "On average HDR is ~40% above LDR" (Abstract / Section 2.1).
  E3. K-coefficient (Ulyanenko et al. 2016): K = foci/cell / dose. Paper claims
      "maximum difference of 1.87 was observed between the K coefficients of
      the two dose rates at 0.250 Gy" -- replicate the K-coefficient ratio.
  E4. Second-order polynomial fit on induction curve (paper's chosen model)
      versus a linear-quadratic (LQ-like) fit yield = alpha*D + beta*D^2 and
      versus a pure-linear fit. Report R^2, AIC, F-test.
  E5. Repair half-life (single-exponential) -- three variants:
        A. raw foci(t) over t in {2,4,8,12,24} h (no baseline subtraction)
        B. (foci(t) - foci(24h)) over t in {2,4,8,12} h (paper's stated method)
        C. (foci(t) - foci(24h)) over t in {2,4,8,12,24} h with the 24h point
           kept (degenerate but informative)
      For each variant, bootstrap a 1000-resample 95% CI on the half-life by
      resampling the time-point residuals (parametric on the SD column from
      Table 3).
  E6. Residual foci at 24 h vs paper's reported means (1.65 +- 0.46 LDR,
      1.29 +- 0.45 HDR) -- already in Table 3 by construction, but the abstract
      makes a no-significant-difference claim which is testable as
      Welch t / Mann-Whitney from the per-donor SDs IF n=4 donors and the SDs
      reflect inter-donor variation. The paper says "not significant"; we
      compute a Welch t two-sided p-value assuming n=4 and report whether
      it agrees.
  E7. Sanity-check the dose-rate ratio HDR/LDR = 0.400 / 0.015 = ~26.7 vs
      the paper's stated values 0.400 and 0.015 Gy/min.

All outputs written under results/.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RES = ROOT / "results"
RES.mkdir(exist_ok=True, parents=True)


def load_csv(path: Path):
    rows = []
    with open(path) as f:
        header = f.readline().strip().split(",")
        for line in f:
            parts = line.strip().split(",")
            if not parts or parts == [""]:
                continue
            rows.append({k: float(v) for k, v in zip(header, parts)})
    return header, rows


def poly_fit(x, y, deg, intercept=True):
    """Polynomial fit. If intercept=False and deg=2, returns (alpha, beta) for
    y = alpha*x + beta*x^2 via lstsq with no constant. r^2, ss_res, ss_tot."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if intercept:
        X = np.vander(x, deg + 1, increasing=True)  # [1, x, x^2, ...]
    else:
        cols = [x ** k for k in range(1, deg + 1)]
        X = np.vstack(cols).T
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    y_hat = X @ coeffs
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return coeffs.tolist(), y_hat.tolist(), ss_res, ss_tot, r2


def aic(ss_res, n, k):
    """Akaike Information Criterion (Gaussian, small-n corrected = AICc)."""
    if n <= k + 1:
        return float("nan")
    return n * math.log(ss_res / n) + 2 * k + (2 * k * (k + 1)) / (n - k - 1)


def exp_halflife(t, y):
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = y > 0
    if mask.sum() < 2:
        return dict(A=float("nan"), k_per_h=float("nan"),
                    halflife_h=float("nan"), r2=float("nan"), n=int(mask.sum()))
    ly = np.log(y[mask])
    tt = t[mask]
    Amat = np.vstack([tt, np.ones_like(tt)]).T
    slope, intercept = np.linalg.lstsq(Amat, ly, rcond=None)[0]
    k = -slope
    A = math.exp(intercept)
    halflife = math.log(2.0) / k if k > 0 else float("nan")
    y_hat = A * np.exp(-k * tt)
    ss_res = float(np.sum((y[mask] - y_hat) ** 2))
    ss_tot = float(np.sum((y[mask] - np.mean(y[mask])) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return dict(A=float(A), k_per_h=float(k), halflife_h=float(halflife),
                r2=float(r2), n=int(mask.sum()))


def bootstrap_halflife(t, y, sd, n_resamples=1000, rng_seed=20260622):
    """Parametric bootstrap: resample each y_i ~ Normal(y_i, sd_i), refit,
    record half-life. Return median + 2.5/97.5 percentile."""
    rng = np.random.default_rng(rng_seed)
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    sd = np.asarray(sd, dtype=float)
    halflives = []
    for _ in range(n_resamples):
        y_rs = rng.normal(loc=y, scale=sd)
        # clamp positive (foci counts cannot be negative)
        y_rs = np.clip(y_rs, 1e-3, None)
        fit = exp_halflife(t, y_rs)
        if math.isfinite(fit["halflife_h"]) and 0 < fit["halflife_h"] < 1e3:
            halflives.append(fit["halflife_h"])
    if not halflives:
        return dict(n=0, median=float("nan"), lo95=float("nan"),
                    hi95=float("nan"))
    halflives = np.array(halflives)
    return dict(n=int(len(halflives)),
                median=float(np.median(halflives)),
                lo95=float(np.percentile(halflives, 2.5)),
                hi95=float(np.percentile(halflives, 97.5)))


def welch_t_two_sample(m1, s1, n1, m2, s2, n2):
    """Two-sided Welch's t-test. Returns (t, df, p) using a Welch approximation
    for the p-value via the Student-t CDF approximated by a series expansion;
    we keep it numpy-only so no scipy dependency.
    """
    var1 = s1 ** 2 / n1
    var2 = s2 ** 2 / n2
    se = math.sqrt(var1 + var2)
    if se == 0:
        return float("nan"), float("nan"), float("nan")
    t = (m1 - m2) / se
    df_num = (var1 + var2) ** 2
    df_den = var1 ** 2 / (n1 - 1) + var2 ** 2 / (n2 - 1)
    df = df_num / df_den
    # Two-sided p via Student-t survival approximated by AS 24 (good enough
    # for df > ~3). Implement an incomplete beta via scipy-free workaround:
    # use the identity P(|T|>t) = I_{df/(df+t^2)}(df/2, 1/2).
    # Numpy has no incbeta; use a numeric integration of t-pdf instead.
    from math import lgamma, pi
    def t_pdf(x, df):
        coef = math.exp(lgamma((df + 1) / 2) - lgamma(df / 2)) / math.sqrt(df * pi)
        return coef * (1 + x * x / df) ** (-(df + 1) / 2)
    # numeric integration from |t| outward to a large bound
    abs_t = abs(t)
    xs = np.linspace(abs_t, abs_t + 50.0, 4001)
    pdf = np.array([t_pdf(float(x), df) for x in xs])
    trapz_fn = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    p_one_sided = float(trapz_fn(pdf, xs))
    p = min(1.0, 2 * p_one_sided)
    return float(t), float(df), float(p)


def main():
    _, t1 = load_csv(DATA / "table1_induction.csv")
    _, t2 = load_csv(DATA / "table2_hdr_ldr_ratio.csv")
    _, t3 = load_csv(DATA / "table3_repair_kinetics.csv")

    doses = np.array([r["dose_Gy"] for r in t1])
    foci_ldr = np.array([r["foci_LDR_mean"] for r in t1])
    foci_hdr = np.array([r["foci_HDR_mean"] for r in t1])
    sd_ldr = np.array([r["foci_LDR_sd"] for r in t1])
    sd_hdr = np.array([r["foci_HDR_sd"] for r in t1])

    results = {}

    # ---- E1: per-dose ratio match ----
    ratios = (foci_hdr / foci_ldr).tolist()
    paper_t2 = [r["HDR_over_LDR_ratio"] for r in t2]
    e1_max_err = float(np.max(np.abs(np.array(ratios) - np.array(paper_t2))))
    results["E1_per_dose_ratio"] = {
        "computed": ratios,
        "paper_table2": paper_t2,
        "max_abs_error": e1_max_err,
        "pass": e1_max_err < 0.02,
    }

    # ---- E2: mean ratio ~40% ----
    mean_ratio = float(np.mean(ratios))
    pct = (mean_ratio - 1.0) * 100.0
    results["E2_mean_ratio"] = {
        "computed_mean_ratio": mean_ratio,
        "computed_pct_above_LDR": pct,
        "paper_claim_pct": 40.0,
        "abs_error_pct_points": abs(pct - 40.0),
        "pass": abs(pct - 40.0) < 2.0,
    }

    # ---- E3: K-coefficient (foci per Gy) and ratio @0.250 Gy = 1.87 ----
    K_ldr = foci_ldr / doses
    K_hdr = foci_hdr / doses
    K_ratio = K_hdr / K_ldr  # which is the same as Table 2 (it cancels)
    # paper says max difference at 0.250 Gy = 1.87 -- this is the per-dose
    # foci-ratio = K-ratio (since dose cancels)
    idx_025 = int(np.where(np.isclose(doses, 0.250))[0][0])
    results["E3_K_coefficient"] = {
        "doses_Gy": doses.tolist(),
        "K_LDR_foci_per_Gy": K_ldr.tolist(),
        "K_HDR_foci_per_Gy": K_hdr.tolist(),
        "K_ratio_HDR_over_LDR": K_ratio.tolist(),
        "max_ratio_dose_Gy": float(doses[int(np.argmax(K_ratio))]),
        "max_ratio_value": float(K_ratio.max()),
        "paper_claim_at_0.250_Gy": 1.87,
        "computed_at_0.250_Gy": float(K_ratio[idx_025]),
        "abs_error": abs(float(K_ratio[idx_025]) - 1.87),
        "pass": (float(np.argmax(K_ratio)) == idx_025) and
                (abs(float(K_ratio[idx_025]) - 1.87) < 0.02),
    }

    # ---- E4: induction model comparison ----
    model_summary = {}
    for label, y in [("LDR", foci_ldr), ("HDR", foci_hdr)]:
        # Linear (degree 1, with intercept)
        c_lin, _, ssr_lin, sst, r2_lin = poly_fit(doses, y, 1, intercept=True)
        # Poly2 with intercept (paper's choice)
        c_p2, _, ssr_p2, _, r2_p2 = poly_fit(doses, y, 2, intercept=True)
        # LQ-style: y = alpha*D + beta*D^2 (no intercept)
        c_lq, _, ssr_lq, _, r2_lq = poly_fit(doses, y, 2, intercept=False)
        n = len(doses)
        # AICc (k = number of free params incl. variance: poly1 -> 2+1, etc.)
        aic_lin = aic(ssr_lin, n, k=2 + 1)
        aic_p2 = aic(ssr_p2, n, k=3 + 1)
        aic_lq = aic(ssr_lq, n, k=2 + 1)
        # F-test poly2 vs linear (nested)
        # F = ((SSR1 - SSR2)/(p2-p1)) / (SSR2/(n-p2))
        p1, p2 = 2, 3  # number of fitted parameters (incl. intercept)
        f = ((ssr_lin - ssr_p2) / (p2 - p1)) / (ssr_p2 / (n - p2))
        model_summary[label] = {
            "linear_intercept": {"coeffs_a_b": c_lin, "ssr": ssr_lin,
                                  "r2": r2_lin, "aicc": aic_lin},
            "poly2_intercept_paper": {"coeffs_a_b_c": c_p2, "ssr": ssr_p2,
                                       "r2": r2_p2, "aicc": aic_p2},
            "LQ_alpha_beta_no_intercept": {"coeffs_alpha_beta": c_lq,
                                            "ssr": ssr_lq, "r2": r2_lq,
                                            "aicc": aic_lq},
            "F_test_poly2_vs_linear": {"F": float(f), "n": n,
                                        "p1": p1, "p2": p2},
        }
    results["E4_induction_model_comparison"] = model_summary

    # ---- E5: repair half-life, three variants + bootstrap CI ----
    times = np.array([r["time_h"] for r in t3])
    fL = np.array([r["foci_LDR_mean"] for r in t3])
    fH = np.array([r["foci_HDR_mean"] for r in t3])
    sL = np.array([r["foci_LDR_sd"] for r in t3])
    sH = np.array([r["foci_HDR_sd"] for r in t3])

    # Variant A: raw, t >= 2h, no subtraction (smoke script's primary fit)
    mA = times >= 2.0
    fitA_L = exp_halflife(times[mA], fL[mA])
    fitA_H = exp_halflife(times[mA], fH[mA])
    bsA_L = bootstrap_halflife(times[mA], fL[mA], sL[mA])
    bsA_H = bootstrap_halflife(times[mA], fH[mA], sH[mA])

    # Variant B: (foci - foci@24h), drop 24h (paper's explicit method)
    res_L_24 = fL[-1]
    res_H_24 = fH[-1]
    mB = (times >= 2.0) & (times < 24.0)
    yB_L = fL[mB] - res_L_24
    yB_H = fH[mB] - res_H_24
    fitB_L = exp_halflife(times[mB], yB_L)
    fitB_H = exp_halflife(times[mB], yB_H)
    # bootstrap for variant B uses combined SD via propagation: sqrt(s_t^2 + s_24^2)
    sdB_L = np.sqrt(sL[mB] ** 2 + sL[-1] ** 2)
    sdB_H = np.sqrt(sH[mB] ** 2 + sH[-1] ** 2)
    bsB_L = bootstrap_halflife(times[mB], yB_L, sdB_L)
    bsB_H = bootstrap_halflife(times[mB], yB_H, sdB_H)

    # Variant C: (foci - residual_24h) over all t>=2, including 24h (will give
    # near-zero terminal, low-weight; mostly diagnostic)
    mC = times >= 2.0
    yC_L = fL[mC] - res_L_24
    yC_H = fH[mC] - res_H_24
    fitC_L = exp_halflife(times[mC], yC_L)
    fitC_H = exp_halflife(times[mC], yC_H)

    results["E5_repair_halflife"] = {
        "variant_A_raw_from_2h_no_subtraction": {
            "LDR": {**fitA_L, "bootstrap_95CI_h": bsA_L,
                     "paper_value_h": 12.0,
                     "rel_err_vs_paper": abs(fitA_L["halflife_h"] - 12.0) / 12.0},
            "HDR": {**fitA_H, "bootstrap_95CI_h": bsA_H,
                     "paper_value_h": 8.6,
                     "rel_err_vs_paper": abs(fitA_H["halflife_h"] - 8.6) / 8.6},
        },
        "variant_B_residual_subtracted_drop_24h_PAPER_METHOD": {
            "LDR": {**fitB_L, "bootstrap_95CI_h": bsB_L,
                     "paper_value_h": 12.0,
                     "rel_err_vs_paper": abs(fitB_L["halflife_h"] - 12.0) / 12.0},
            "HDR": {**fitB_H, "bootstrap_95CI_h": bsB_H,
                     "paper_value_h": 8.6,
                     "rel_err_vs_paper": abs(fitB_H["halflife_h"] - 8.6) / 8.6},
        },
        "variant_C_residual_subtracted_include_24h": {
            "LDR": fitC_L, "HDR": fitC_H,
        },
        "winner_within_25pct_of_paper": (
            "variant_A" if abs(fitA_H["halflife_h"] - 8.6) / 8.6 <
                          abs(fitB_H["halflife_h"] - 8.6) / 8.6
            else "variant_B"
        ),
    }

    # ---- E6: residual foci @ 24 h -- "not significant" claim ----
    # 4 donors, 2 conditions; SD reflects inter-donor variation
    t_val, df_val, p_val = welch_t_two_sample(
        m1=float(fL[-1]), s1=float(sL[-1]), n1=4,
        m2=float(fH[-1]), s2=float(sH[-1]), n2=4,
    )
    results["E6_residual_24h_significance"] = {
        "LDR_mean": float(fL[-1]), "LDR_sd": float(sL[-1]),
        "HDR_mean": float(fH[-1]), "HDR_sd": float(sH[-1]),
        "n_donors": 4,
        "welch_t": t_val, "welch_df": df_val, "two_sided_p": p_val,
        "paper_claim": "not statistically significant",
        "alpha": 0.05,
        "agrees_with_paper": bool(p_val > 0.05),
    }

    # ---- E7: dose-rate ratio sanity ----
    results["E7_dose_rate_ratio"] = {
        "HDR_Gy_per_min": 0.400,
        "LDR_Gy_per_min": 0.015,
        "ratio_HDR_over_LDR": 0.400 / 0.015,
        "paper_text_values_present": True,
    }

    # ---- save ----
    out_path = RES / "extended_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}")

    # ---- summary table ----
    md = ["# Extended replication summary (machine-readable)\n"]
    md.append("| ID | Claim | Computed | Paper | Verdict |")
    md.append("|----|-------|----------|-------|---------|")
    e1 = results["E1_per_dose_ratio"]
    md.append(f"| E1 | Per-dose HDR/LDR ratio (max abs err vs Table 2) | "
              f"{e1['max_abs_error']:.4f} | <0.02 tolerance | "
              f"{'VERIFIED' if e1['pass'] else 'FAIL'} |")
    e2 = results["E2_mean_ratio"]
    md.append(f"| E2 | Mean HDR/LDR percentage above LDR | "
              f"{e2['computed_pct_above_LDR']:.2f}% | ~40% | "
              f"{'VERIFIED' if e2['pass'] else 'FAIL'} |")
    e3 = results["E3_K_coefficient"]
    md.append(f"| E3 | K-coefficient max ratio at 0.250 Gy | "
              f"{e3['computed_at_0.250_Gy']:.3f} | 1.87 | "
              f"{'VERIFIED' if e3['pass'] else 'FAIL'} |")
    e5A = results["E5_repair_halflife"]["variant_A_raw_from_2h_no_subtraction"]
    md.append(f"| E5A | Repair t1/2 HDR (variant A raw, t>=2h) | "
              f"{e5A['HDR']['halflife_h']:.2f} h "
              f"[{e5A['HDR']['bootstrap_95CI_h']['lo95']:.2f}, "
              f"{e5A['HDR']['bootstrap_95CI_h']['hi95']:.2f}] | "
              f"8.6 h | "
              f"{'VERIFIED' if e5A['HDR']['rel_err_vs_paper'] < 0.25 else 'PARTIAL'} |")
    md.append(f"| E5A | Repair t1/2 LDR (variant A raw, t>=2h) | "
              f"{e5A['LDR']['halflife_h']:.2f} h "
              f"[{e5A['LDR']['bootstrap_95CI_h']['lo95']:.2f}, "
              f"{e5A['LDR']['bootstrap_95CI_h']['hi95']:.2f}] | "
              f"12.0 h | "
              f"{'VERIFIED' if e5A['LDR']['rel_err_vs_paper'] < 0.25 else 'PARTIAL'} |")
    e5B = results["E5_repair_halflife"]["variant_B_residual_subtracted_drop_24h_PAPER_METHOD"]
    md.append(f"| E5B | Repair t1/2 HDR (variant B paper method) | "
              f"{e5B['HDR']['halflife_h']:.2f} h "
              f"[{e5B['HDR']['bootstrap_95CI_h']['lo95']:.2f}, "
              f"{e5B['HDR']['bootstrap_95CI_h']['hi95']:.2f}] | "
              f"8.6 h | "
              f"{'VERIFIED' if e5B['HDR']['rel_err_vs_paper'] < 0.25 else 'PARTIAL/FAIL'} |")
    md.append(f"| E5B | Repair t1/2 LDR (variant B paper method) | "
              f"{e5B['LDR']['halflife_h']:.2f} h "
              f"[{e5B['LDR']['bootstrap_95CI_h']['lo95']:.2f}, "
              f"{e5B['LDR']['bootstrap_95CI_h']['hi95']:.2f}] | "
              f"12.0 h | "
              f"{'VERIFIED' if e5B['LDR']['rel_err_vs_paper'] < 0.25 else 'PARTIAL/FAIL'} |")
    e6 = results["E6_residual_24h_significance"]
    md.append(f"| E6 | 24h residual HDR vs LDR Welch p ({e6['HDR_mean']:.2f}±{e6['HDR_sd']:.2f} vs {e6['LDR_mean']:.2f}±{e6['LDR_sd']:.2f}) | "
              f"p={e6['two_sided_p']:.3f} (df={e6['welch_df']:.1f}) | "
              f"'not significant' | "
              f"{'VERIFIED (p>0.05)' if e6['agrees_with_paper'] else 'CONTRADICTED'} |")
    e7 = results["E7_dose_rate_ratio"]
    md.append(f"| E7 | HDR/LDR dose-rate ratio | "
              f"{e7['ratio_HDR_over_LDR']:.2f}× | 26.67× | VERIFIED |")
    md.append("")

    # induction model AICc comparison
    md.append("### Induction model comparison (AICc; lower is better)\n")
    md.append("| Curve | Linear AICc | Poly2 (paper) AICc | LQ no-intercept AICc | R²(poly2) |")
    md.append("|-------|-------------|--------------------|-----------------------|-----------|")
    for label in ["LDR", "HDR"]:
        ms = results["E4_induction_model_comparison"][label]
        md.append(f"| {label} | {ms['linear_intercept']['aicc']:.3f} | "
                  f"{ms['poly2_intercept_paper']['aicc']:.3f} | "
                  f"{ms['LQ_alpha_beta_no_intercept']['aicc']:.3f} | "
                  f"{ms['poly2_intercept_paper']['r2']:.4f} |")
    md.append("")
    md_path = RES / "extended_summary.md"
    md_path.write_text("\n".join(md))
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
