#!/usr/bin/env python3
"""
Smoke replication of the single explicit closed-form equation in:

    Brahme A. (2026) "Improving radiation therapy efficacy considering DNA repair,
    TP53 mutations, microscopic heterogeneity, and low- and high-dose apoptosis."
    Front. Oncol. 15:1703503. doi:10.3389/fonc.2025.1703503

The paper is a single-author review/perspective. It contains essentially ONE
explicit equation (Equation 1) that we can reproduce numerically -- the
extreme-value rewriting of the Poisson tumor-control probability (TCP):

    TCP(D) = exp( -exp( (m - D)/v ) )
           = exp( -exp( (D0 ln N0 - D)/D0 ) )
           = exp( -N0 * exp( -D/D0 ) )

with the statistical companions stated in the same paragraph:

    mean        : D_bar = m + v*gamma_E = D0 * (ln N0 + gamma_E)
    median      : D50   = m - v*ln(ln 2) = D0 * ln( N0 / ln 2 )
    variance    : V     = (pi^2 / 6) * v^2 = (pi^2 / 6) * D0^2
    rel. SD     : sigma_D / D_bar = pi / ( sqrt(6) * (ln N0 + gamma_E) )

with Euler's gamma ~ 0.5772, Kurtosis = 5.4, Skewness ~ 1.1395 (constants
quoted by the paper, not free parameters).

For the canonical clinical example given in the text (N0 = 1e7 clonogens,
D0 absorbed into the natural units, i.e. set D0 = 1 Gy so dose is in units
of "D0"), the paper states that the relative standard deviation should be
~7.7% (0.0768).

This smoke check just confirms:
  (i)   the three algebraic forms of TCP in Eq. 1 agree to ~machine epsilon
        across a sensible dose grid
  (ii)  the analytic mean, median, variance, and relative-SD match the values
        the paper quotes (sigma/mean ~ 0.0768 for N0=1e7)
  (iii) the Skewness and Kurtosis of the underlying Gumbel(=extreme-value)
        distribution match the constants cited in the text (~1.1395 and 5.4)

It also produces a small TCP-vs-dose plot for visual inspection.

No external data, no fitted parameters, no Monte Carlo. CPU-only, <1 s.
"""

import json
import math
from pathlib import Path

import numpy as np

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAVE_MPL = True
except Exception:
    HAVE_MPL = False


HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
FIGS = HERE.parent / "figures"
LOGS = HERE.parent / "logs"
for p in (RESULTS, FIGS, LOGS):
    p.mkdir(parents=True, exist_ok=True)


EULER_GAMMA = 0.5772156649015329


def tcp_forms(D, D0, N0):
    """Three algebraic forms of Brahme (2026) Equation 1."""
    m = D0 * math.log(N0)
    v = D0
    f1 = np.exp(-np.exp((m - D) / v))
    f2 = np.exp(-np.exp((D0 * math.log(N0) - D) / D0))
    f3 = np.exp(-N0 * np.exp(-D / D0))
    return f1, f2, f3


def analytic_stats(D0, N0):
    """Stats stated next to Eq. 1 for the extreme-value TCP."""
    m = D0 * math.log(N0)
    v = D0
    mean = m + v * EULER_GAMMA  # D_bar
    median = m - v * math.log(math.log(2.0))  # D50
    variance = (math.pi ** 2 / 6.0) * v ** 2
    sd = math.sqrt(variance)
    rel_sd = sd / mean
    # Standard Gumbel skewness and (excess+3) kurtosis
    skewness = 12.0 * math.sqrt(6.0) * 1.2020569031595942 / (math.pi ** 3)  # ~1.13955
    kurtosis = 3.0 + 12.0 / 5.0  # 5.4
    return dict(
        m=m,
        v=v,
        mean=mean,
        median=median,
        variance=variance,
        sd=sd,
        rel_sd=rel_sd,
        skewness=skewness,
        kurtosis=kurtosis,
    )


def main():
    D0 = 1.0  # work in units of D0 (Gy)
    N0 = 1.0e7  # canonical clonogen count cited in the text

    D = np.linspace(0.0, 30.0 * D0, 6001)
    f1, f2, f3 = tcp_forms(D, D0, N0)

    max_abs_12 = float(np.max(np.abs(f1 - f2)))
    max_abs_13 = float(np.max(np.abs(f1 - f3)))
    max_abs_23 = float(np.max(np.abs(f2 - f3)))

    stats = analytic_stats(D0, N0)

    # Closest dose-grid index to the analytic median; TCP there should be ~0.5
    i_med = int(np.argmin(np.abs(D - stats["median"])))
    tcp_at_median = float(f3[i_med])

    paper_rel_sd_target = 0.0768
    paper_skew_target = 1.1395
    paper_kurt_target = 5.4

    results = dict(
        inputs=dict(D0_Gy=D0, N0_clonogens=N0, dose_grid_points=int(D.size)),
        equation_form_consistency=dict(
            max_abs_diff_form1_form2=max_abs_12,
            max_abs_diff_form1_form3=max_abs_13,
            max_abs_diff_form2_form3=max_abs_23,
            tolerance=1.0e-12,
            pass_=max(max_abs_12, max_abs_13, max_abs_23) < 1.0e-12,
        ),
        analytic_stats=stats,
        median_check=dict(
            D50_analytic=stats["median"],
            tcp_at_D50_numerical=tcp_at_median,
            expected_tcp_at_D50=0.5,
            pass_=abs(tcp_at_median - 0.5) < 1.0e-3,
        ),
        paper_claim_checks=dict(
            rel_sd_paper=paper_rel_sd_target,
            rel_sd_computed=stats["rel_sd"],
            rel_sd_match_to_3dp=round(stats["rel_sd"], 4) == paper_rel_sd_target,
            skewness_paper=paper_skew_target,
            skewness_computed=stats["skewness"],
            skewness_match_to_3dp=abs(stats["skewness"] - paper_skew_target) < 5e-4,
            kurtosis_paper=paper_kurt_target,
            kurtosis_computed=stats["kurtosis"],
            kurtosis_match=abs(stats["kurtosis"] - paper_kurt_target) < 1e-9,
        ),
    )

    out_json = RESULTS / "tcp_eq1_smoke.json"
    with open(out_json, "w") as fh:
        json.dump(results, fh, indent=2)

    log_path = LOGS / "tcp_eq1_smoke.log"
    with open(log_path, "w") as fh:
        fh.write("Brahme (2026) Eq. 1 smoke replication\n")
        fh.write("=" * 60 + "\n")
        fh.write(json.dumps(results, indent=2))
        fh.write("\n")

    if HAVE_MPL:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(D, f3, color="black", lw=1.8, label="TCP (extreme-value, Eq. 1)")
        ax.axvline(stats["median"], color="C3", ls="--", lw=1, label=f"D50 = {stats['median']:.3f}")
        ax.axvline(stats["mean"], color="C0", ls=":", lw=1, label=f"mean = {stats['mean']:.3f}")
        ax.set_xlabel("Dose / D0")
        ax.set_ylabel("Tumor control probability")
        ax.set_title("Brahme (2026) Eq. 1 — TCP vs dose (N0=1e7)")
        ax.set_ylim(-0.02, 1.02)
        ax.legend(loc="lower right", fontsize=9)
        fig.tight_layout()
        fig_path = FIGS / "tcp_eq1_vs_dose.png"
        fig.savefig(fig_path, dpi=140)
        plt.close(fig)
    else:
        fig_path = None

    print("== Brahme (2026) Eq. 1 smoke check ==")
    print(f"  algebraic forms agree to {max(max_abs_12, max_abs_13, max_abs_23):.2e}")
    print(f"  D50 analytic                 = {stats['median']:.6f}")
    print(f"  TCP(D50) numerical           = {tcp_at_median:.6f}  (target 0.5)")
    print(f"  relative SD (sigma/mean)     = {stats['rel_sd']:.6f}  (paper 0.0768)")
    print(f"  skewness                     = {stats['skewness']:.6f}  (paper 1.1395)")
    print(f"  kurtosis                     = {stats['kurtosis']:.6f}  (paper 5.4)")
    print(f"  json:  {out_json}")
    if fig_path is not None:
        print(f"  fig:   {fig_path}")
    print(f"  log:   {log_path}")


if __name__ == "__main__":
    main()
