#!/usr/bin/env python3
"""
LUCID100 slot 48 — DSB / Model 2 / sensitivity claim audit (analytic).

Companion to smoke_scavenging_capacity.py.  Where the first script reproduces
the indirect-channel SSB scaling (Eq. 4), this script:

  1. Tabulates the paper's per-condition DSB G-values (CONV + UHDR), computes
     the UHDR/CONV ratios at each of the four DMSO concentrations, and checks
     the ~73.5% reduction claim at the lowest scavenging capacity.
  2. Cross-checks the bp-threshold sensitivity numbers in §3.2 (5/10/15 bp).
  3. Confirms the Model 2 UHDR/CONV SSB ratio (~3.5%) at the highest σ.
  4. Sanity-checks the *DSB pair-acceptance* combinatorics by Monte-Carlo
     sampling SSB site positions on a circular plasmid and applying the
     paper's two-on-opposite-strands-within-Nbp acceptance criterion.  This is
     a model of the paper's described post-processor (Section 2.2.3), used
     only to verify that the *shape* of the bp-threshold sensitivity is
     consistent with the paper's quoted means.

This script does NOT call TOPAS-nBio.  It re-derives the algebra the paper
presents and runs a small standalone Monte Carlo on the acceptance procedure.

Outputs:
  - scripts/smoke_dsb_results.csv
  - scripts/smoke_dsb_run.log
  - figures/smoke_dsb_ratio_vs_sigma.png
  - figures/smoke_dsb_bp_sensitivity.png
"""
from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---- Paper numbers ---------------------------------------------------------

DMSO = [1.0e-5, 1.0e-4, 1.0e-3, 1.0e-1]  # M
SIGMA = [7.1e9 * c for c in DMSO]         # s^-1

# §3.1 SSB G-values (/Gy/Da)
SSB_CONV = [3.63e-7, 9.31e-8, 1.63e-8, 6.59e-10]
SSB_UHDR = [1.64e-7, 7.95e-8, 1.62e-8, 6.59e-10]

# §3.2 DSB G-values (/Gy/Da)
DSB_CONV = [2.88e-8, 2.76e-9, 1.68e-10, 1.76e-11]
DSB_UHDR = [7.64e-9, 2.16e-9, 1.62e-9, 1.79e-11]  # NOTE: paper's third UHDR value
# Per the paper, the third UHDR DSB value (1.62e-9) is OOM-suspect when read
# off the PDF — see note in the run log.

# §3.1 Model 2 (single point @ 0.1 M DMSO + WR-1065)
M2_SSB_CONV = 1.03e-9
M2_SSB_UHDR = 9.92e-10

# §3.2 bp sensitivity (DSB means @ 0.1 M DMSO, 50 µg/mL)
# from text: "the impact of reducing the bp distance required for a DSB to
# occur from 10 bp to 5 bp causes the mean DSB yield to drop from 1.79 to
# 1.28 (×10⁻¹¹ Gy Da⁻¹) for UHDR and from 1.76 to 1.28 (×10⁻¹¹ Gy Da⁻¹) for
# CONV.  Conversely, increasing the distance threshold to 15 bp raises the
# mean DSBs to 2.00 and 1.92 (×10⁻¹¹ Gy Da⁻¹) for UHDR and CONV respectively."
BP_SENS_UHDR = {5: 1.28e-11, 10: 1.79e-11, 15: 2.00e-11}
BP_SENS_CONV = {5: 1.28e-11, 10: 1.76e-11, 15: 1.92e-11}

# §3.1 reported SSB-reduction percentages (CONV→UHDR)
SSB_REDUCTION_PCT_REPORTED = [54.7, 14.6, 1.1, 0.1]

# §3.2 reported DSB reduction at lowest σ
DSB_REDUCTION_PCT_REPORTED_LOW_SIGMA = 73.5

# Plasmid: pUC19, 2686 bp, double-stranded, circular
PLASMID_BP = 2686


@dataclass
class DSBRow:
    dmso_M: float
    sigma: float
    dsb_conv: float
    dsb_uhdr: float
    reduction_pct_repro: float


def reduction_pct(conv: float, uhdr: float) -> float:
    return 100.0 * (conv - uhdr) / conv if conv else float("nan")


# ---- Standalone MC for DSB pair-acceptance --------------------------------
#
# Model: for a fixed *expected* number of SSB sites N per plasmid per Gy, draw
# N positions uniformly on a circular plasmid of length L bp.  Assign each
# position to strand 0 or 1 with equal probability.  A DSB is counted if any
# two SSB sites are on opposite strands and within ≤ T bp (cyclic distance).
# We sweep T ∈ {5, 10, 15} bp and report the *fraction of plasmid samples*
# yielding ≥1 DSB.  The paper's 10⁶-iteration post-processor on per-strand
# IDs is a richer version of this same scheme — we run a smaller version here
# (1e5 plasmid samples per condition) just to confirm that the *shape* of the
# bp-threshold sensitivity goes the right way (15 > 10 > 5).

def simulate_dsb_pair_acceptance(
    n_ssb_per_plasmid: float,
    bp_thresholds=(5, 10, 15),
    n_iter: int = 100_000,
    L: int = PLASMID_BP,
    seed: int = 1234,
) -> dict[int, float]:
    rng = random.Random(seed)
    out = {t: 0 for t in bp_thresholds}
    # We treat n_ssb as a Poisson rate per plasmid so the distribution width
    # matches the paper's tabulated standard deviations qualitatively.
    for _ in range(n_iter):
        n = poisson(rng, n_ssb_per_plasmid)
        if n < 2:
            continue
        positions = [(rng.randint(0, L - 1), rng.randint(0, 1)) for _ in range(n)]
        positions.sort()
        for t in bp_thresholds:
            if has_pair_within(positions, t, L):
                out[t] += 1
    return {t: out[t] / n_iter for t in bp_thresholds}


def poisson(rng: random.Random, mean: float) -> int:
    if mean <= 0:
        return 0
    L_exp = math.exp(-mean)
    k, p = 0, 1.0
    while True:
        k += 1
        p *= rng.random()
        if p < L_exp:
            return k - 1


def has_pair_within(positions, t: int, L: int) -> bool:
    n = len(positions)
    for i in range(n):
        x_i, s_i = positions[i]
        for j in range(i + 1, n):
            x_j, s_j = positions[j]
            if s_i == s_j:
                continue
            d = x_j - x_i
            if d > L // 2:
                d = L - d
            if d <= t:
                return True
            # positions are sorted; once linear gap > t+ allow break unless
            # cyclic wrap brings it back.  Cheap conservative continue.
    return False


# ---- Main -----------------------------------------------------------------

def main() -> int:
    here = Path(__file__).resolve().parent
    proj = here.parent
    fig = proj / "figures"
    fig.mkdir(exist_ok=True)

    rows = [
        DSBRow(c, s, dc, du, reduction_pct(dc, du))
        for c, s, dc, du in zip(DMSO, SIGMA, DSB_CONV, DSB_UHDR)
    ]

    # CSV
    with (here / "smoke_dsb_results.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([
            "DMSO_M", "sigma_s-1",
            "DSB_CONV_per_Gy_per_Da", "DSB_UHDR_per_Gy_per_Da",
            "reduction_pct_repro", "reduction_pct_paper_lowest_sigma_only",
            "ssb_reduction_pct_repro", "ssb_reduction_pct_paper",
        ])
        for r, ssb_red_paper in zip(rows, SSB_REDUCTION_PCT_REPORTED):
            ssb_red_repro = reduction_pct(SSB_CONV[DMSO.index(r.dmso_M)],
                                          SSB_UHDR[DMSO.index(r.dmso_M)])
            w.writerow([
                f"{r.dmso_M:.2g}", f"{r.sigma:.3g}",
                f"{r.dsb_conv:.3g}", f"{r.dsb_uhdr:.3g}",
                f"{r.reduction_pct_repro:.2f}",
                f"{DSB_REDUCTION_PCT_REPORTED_LOW_SIGMA:.1f}" if r.dmso_M == 1.0e-5 else "",
                f"{ssb_red_repro:.2f}",
                f"{ssb_red_paper:.2f}",
            ])

    # bp sensitivity MC.  Choose mean SSB rate such that DSB rate ~ 1.79e-11
    # at the 10 bp threshold.  This is *not* a fit to absolute G-values — it
    # only checks the *qualitative* monotonicity 5 < 10 < 15.
    pair_frac = simulate_dsb_pair_acceptance(n_ssb_per_plasmid=2.5,
                                             n_iter=200_000)

    # Plot ratio (UHDR/CONV) DSB
    fig1, ax1 = plt.subplots(figsize=(6.5, 4.5))
    sigmas = [r.sigma for r in rows]
    ratios = [r.dsb_uhdr / r.dsb_conv for r in rows]
    ax1.semilogx(sigmas, ratios, "o-", label="UHDR/CONV  (DSB reproduced from paper §3.2)")
    ax1.axhline(1.0, color="k", lw=0.5, ls=":")
    ax1.axhline(1.0 - DSB_REDUCTION_PCT_REPORTED_LOW_SIGMA / 100.0,
                color="red", ls="--", lw=1.0,
                label=f"paper @ lowest σ: 1 − 0.735 = {1-0.735:.3f}")
    ax1.set_xlabel(r"$\sigma_{\cdot OH}$ (s$^{-1}$)")
    ax1.set_ylabel("UHDR / CONV  DSB ratio")
    ax1.set_title("Smoke: DSB UHDR/CONV vs scavenging capacity\n(Masilela et al 2026 §3.2)")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(fontsize=9)
    fig1.tight_layout()
    fig1.savefig(fig / "smoke_dsb_ratio_vs_sigma.png", dpi=140)
    plt.close(fig1)

    # Plot bp sensitivity (paper vs MC monotonicity)
    bp = [5, 10, 15]
    paper_uhdr = [BP_SENS_UHDR[t] * 1e11 for t in bp]
    paper_conv = [BP_SENS_CONV[t] * 1e11 for t in bp]
    mc_y = [pair_frac[t] for t in bp]
    fig2, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].plot(bp, paper_uhdr, "o-", label="UHDR (paper §3.2)")
    axes[0].plot(bp, paper_conv, "s-", label="CONV (paper §3.2)")
    axes[0].set_xlabel("DSB bp distance threshold")
    axes[0].set_ylabel(r"mean DSB ($\times 10^{-11}$ /Gy/Da)")
    axes[0].set_title("Paper-quoted DSB sensitivity to bp threshold")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[1].plot(bp, mc_y, "o-", color="purple")
    axes[1].set_xlabel("DSB bp distance threshold")
    axes[1].set_ylabel("simulated P[≥1 DSB per plasmid sample]")
    axes[1].set_title("Standalone MC pair-acceptance\n(monotonicity sanity check, 2e5 samples)")
    axes[1].grid(True, alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(fig / "smoke_dsb_bp_sensitivity.png", dpi=140)
    plt.close(fig2)

    # Log
    with (here / "smoke_dsb_run.log").open("w") as fh:
        fh.write("LUCID100 slot 48 — DSB / Model 2 / bp-sensitivity audit\n")
        fh.write("Paper: 10.1088/1361-6560/ae62c6\n\n")

        fh.write("=== §3.2 DSB UHDR/CONV ratios reproduced from paper text ===\n")
        fh.write(f"{'DMSO_M':>10} {'sigma':>12} {'DSB_CONV':>12} {'DSB_UHDR':>12} "
                 f"{'UHDR/CONV':>11} {'red.%':>8}\n")
        for r in rows:
            fh.write(f"{r.dmso_M:>10.0e} {r.sigma:>12.3e} "
                     f"{r.dsb_conv:>12.3e} {r.dsb_uhdr:>12.3e} "
                     f"{r.dsb_uhdr/r.dsb_conv:>11.4f} {r.reduction_pct_repro:>8.2f}\n")
        fh.write(f"\nPaper claims at lowest σ: ~73.5% reduction (DSB).\n")
        fh.write(f"Reproduced from quoted numbers: {rows[0].reduction_pct_repro:.2f}%  ")
        fh.write("✓\n" if abs(rows[0].reduction_pct_repro - 73.5) < 2.0 else "✗\n")

        fh.write("\nNote: the third UHDR DSB value (1.62e-9 at 1e-3 M DMSO) reads off the\n"
                 "PDF higher than its CONV counterpart (1.68e-10). This appears to be a\n"
                 "typesetting error in the paper text (a missing exponent change).  Paper\n"
                 "§3.2 says: 'no statistically significant differences observed at the two\n"
                 "highest scavenging capacities' — that statement is inconsistent with the\n"
                 "literal 1.62e-9 number, so we flag it but do not fabricate a correction.\n")

        fh.write("\n=== §3.1 SSB reduction percentages ===\n")
        for c, paper, conv, uhdr in zip(DMSO, SSB_REDUCTION_PCT_REPORTED, SSB_CONV, SSB_UHDR):
            repro = reduction_pct(conv, uhdr)
            ok = "✓" if abs(repro - paper) < 1.0 else "✗"
            fh.write(f"  DMSO={c:.0e} M:  paper={paper:5.1f}%  repro={repro:6.2f}%  {ok}\n")

        fh.write("\n=== §3.1 Model 2 @ 0.1 M DMSO + WR-1065 ===\n")
        m2_red = reduction_pct(M2_SSB_CONV, M2_SSB_UHDR)
        fh.write(f"  SSB CONV={M2_SSB_CONV:.2e}  UHDR={M2_SSB_UHDR:.2e}  red={m2_red:.2f}%\n")
        fh.write(f"  Paper: 3.5% reduction  {'✓' if abs(m2_red-3.5) < 0.3 else '✗'}\n")

        fh.write("\n=== §3.2 bp sensitivity (paper-quoted vs MC monotonicity) ===\n")
        fh.write("  paper UHDR  (5/10/15 bp)  = "
                 f"{paper_uhdr[0]:.2f}/{paper_uhdr[1]:.2f}/{paper_uhdr[2]:.2f}  ×1e-11\n")
        fh.write("  paper CONV  (5/10/15 bp)  = "
                 f"{paper_conv[0]:.2f}/{paper_conv[1]:.2f}/{paper_conv[2]:.2f}  ×1e-11\n")
        fh.write("  monotonic 5 < 10 < 15  (paper UHDR):  "
                 f"{'✓' if paper_uhdr[0] < paper_uhdr[1] < paper_uhdr[2] else '✗'}\n")
        fh.write("  monotonic 5 < 10 < 15  (paper CONV):  "
                 f"{'✓' if paper_conv[0] < paper_conv[1] < paper_conv[2] else '✗'}\n")
        fh.write("  standalone MC P[≥1 DSB | T bp]:  "
                 f"{mc_y[0]:.4f} / {mc_y[1]:.4f} / {mc_y[2]:.4f}\n")
        fh.write("  monotonic MC 5 < 10 < 15:           "
                 f"{'✓' if mc_y[0] < mc_y[1] < mc_y[2] else '✗'}\n")

    print("wrote", here / "smoke_dsb_results.csv")
    print("wrote", here / "smoke_dsb_run.log")
    print("wrote", fig / "smoke_dsb_ratio_vs_sigma.png")
    print("wrote", fig / "smoke_dsb_bp_sensitivity.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
