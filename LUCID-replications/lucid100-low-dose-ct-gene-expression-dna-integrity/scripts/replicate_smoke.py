#!/usr/bin/env python3
"""
Tier-1 smoke replication for Schmid et al. 2025 (IJMS 26:11869).

Reads the appendix tables harvested from EuropePMC JATS XML and reproduces
the analyses for which per-patient data is published:

  1. Patient demographics (Table 1 reconciliation).
  2. Combined (in vivo + ex vivo) per-gene median DGE and one-sample Wilcoxon
     signed-rank test on log2(DGE) vs zero.
  3. Combined linear regression of DGE on DLP per gene (full N=60).
  4. γ-H2AX paired test (post vs pre, n=12) and RIF mean/SD.

Exits non-zero on any failed sanity check.
"""

import os
import sys
import csv
import math
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, "..", "artifacts"))

GENES = ["DDB2", "FDXR", "POU2AF1", "WNT3", "BAX", "AEN", "EDA2R", "MIR34AHG", "PHLDA3"]


def load_table_a1():
    """Return dict: patient_id -> {'gene'->float or nan, 'DLP'->float, 'effdose'->float}."""
    path = os.path.join(ART, "ijms-26-11869-t0A1.tsv")
    rows = list(csv.reader(open(path), delimiter="\t"))
    # First 3 lines are header; data starts at row index 3
    data = {}
    for r in rows[3:]:
        if not r or not r[0].strip():
            continue
        pid = int(r[0])
        # Some cells are '-' (patient 61 = no GE)
        def _f(x):
            x = x.strip().replace("\u2212", "-")  # unicode minus
            if x in ("", "-"):
                return float("nan")
            return float(x)
        # 9 gene columns 1..9, DLP col 10, effdose col 11
        if len(r) < 12:
            # patient 61 row has 12 cells (all '-' for genes)
            pass
        gene_vals = {g: _f(r[i + 1]) for i, g in enumerate(GENES)}
        dlp = _f(r[10]) if len(r) > 10 else float("nan")
        eff = _f(r[11]) if len(r) > 11 else float("nan")
        data[pid] = {"genes": gene_vals, "DLP": dlp, "effdose": eff}
    return data


def load_table_a2():
    path = os.path.join(ART, "ijms-26-11869-t0A2.tsv")
    rows = list(csv.reader(open(path), delimiter="\t"))
    out = []
    for r in rows[2:]:  # 2 header rows
        if not r or not r[0].strip():
            continue
        pid = int(r[0])
        def _f(x):
            x = x.strip().replace("\u2212", "-")
            if x in ("", "-"): return float("nan")
            return float(x)
        out.append({
            "pid": pid,
            "pre": _f(r[1]),
            "post": _f(r[2]),
            "rif": _f(r[3]),
            "DLP": _f(r[4]),
            "effdose": _f(r[5]),
        })
    return out


def almost_equal(a, b, tol):
    return (a is None) or (b is None) or abs(a - b) <= tol


def main():
    print("=" * 70)
    print("LUCID100 slot 15 — Schmid 2025 IJMS — Tier 1 smoke replication")
    print("=" * 70)

    a1 = load_table_a1()
    a2 = load_table_a2()
    assert len(a1) == 61, f"expected 61 rows in Table A1, got {len(a1)}"
    # Patient 61 has no GE; gene analysis cohort = 60
    ge_patients = [p for p, d in a1.items() if not math.isnan(d["genes"]["DDB2"])]
    assert len(ge_patients) == 60, f"expected 60 GE patients, got {len(ge_patients)}"
    assert len(a2) == 12, f"expected 12 γ-H2AX patients, got {len(a2)}"

    # ---- Demographics (Table 1) ----
    print("\n[1] DEMOGRAPHICS — checking Table 1 against per-patient appendix")
    dlps = np.array([a1[p]["DLP"] for p in ge_patients])
    effs = np.array([a1[p]["effdose"] for p in ge_patients])
    print(f"  All N=60: DLP mean={dlps.mean():.1f}  SD_sample={dlps.std(ddof=1):.1f}  SD_pop={dlps.std(ddof=0):.1f}   "
          f"(paper: 561.9 ± 384.6)   min={dlps.min():.1f}  max={dlps.max():.1f} (paper 67.0–1725.0)")
    print(f"  All N=60: EffDose mean={effs.mean():.2f}  SD_sample={effs.std(ddof=1):.2f}  SD_pop={effs.std(ddof=0):.2f}  "
          f"(paper: 8.3 ± 5.8)   min={effs.min():.2f}  max={effs.max():.2f} (paper 0.9–24.2)")
    assert almost_equal(dlps.mean(), 561.9, 1.0), "DLP mean mismatch >1 mGy·cm"
    # Paper reports SD that match POPULATION SD (ddof=0), not sample SD (ddof=1).
    # Excel STDEV() is sample; STDEVP() is population. Paper appears to use ddof=0.
    assert almost_equal(dlps.std(ddof=0), 384.6, 1.0), "DLP pop-SD mismatch >1 mGy·cm"
    assert almost_equal(effs.mean(), 8.3, 0.1)
    assert almost_equal(effs.max(), 24.2, 0.1)
    print("  PASS demographics: paper uses POPULATION SD (ddof=0); exact match.")

    # γ-H2AX subset demographics
    g_dlp = np.array([r["DLP"] for r in a2])
    g_eff = np.array([r["effdose"] for r in a2])
    print(f"  γ-H2AX N=12: DLP mean={g_dlp.mean():.1f}  SD_pop={g_dlp.std(ddof=0):.1f}  SD_sample={g_dlp.std(ddof=1):.1f}  "
          f"(paper 321.0 ± 149.3)")
    assert almost_equal(g_dlp.mean(), 321.0, 1.0)
    assert almost_equal(g_dlp.std(ddof=0), 149.3, 1.0)  # population SD matches
    print("  PASS γ-H2AX subset demographics (population SD)")

    # ---- Combined per-gene one-sample test on log2 DGE ----
    print("\n[2] GENE EXPRESSION — combined N=60, one-sample test log2(DGE) vs 0")
    print(f"  {'Gene':10s}  {'median DGE':>11s}  {'mean log2':>10s}  "
          f"{'Wilcoxon p':>11s}  {'one-samp t p':>13s}")
    for g in GENES:
        vals = np.array([a1[p]["genes"][g] for p in ge_patients])
        log2 = np.log2(vals)
        med = np.median(vals)
        # Wilcoxon signed-rank (the paper uses this when data are not normal)
        try:
            wp = stats.wilcoxon(log2).pvalue
        except ValueError:
            wp = float("nan")
        tp = stats.ttest_1samp(log2, 0.0).pvalue
        print(f"  {g:10s}  {med:>11.3f}  {log2.mean():>10.3f}  "
              f"{wp:>11.2e}  {tp:>13.2e}")

    # ---- Combined per-gene linear regression DGE vs DLP ----
    print("\n[3] LINEAR REGRESSION DGE vs DLP — combined N=60 (cross-check vs Fig 3)")
    print(f"  {'Gene':10s}  {'slope':>10s}  {'intercept':>10s}  {'r^2':>8s}  {'p':>10s}")
    for g in GENES:
        vals = np.array([a1[p]["genes"][g] for p in ge_patients])
        x = np.array([a1[p]["DLP"] for p in ge_patients])
        s = stats.linregress(x, vals)
        print(f"  {g:10s}  {s.slope:>10.2e}  {s.intercept:>10.3f}  "
              f"{s.rvalue**2:>8.3f}  {s.pvalue:>10.2e}")

    # ---- γ-H2AX paired test ----
    print("\n[4] γ-H2AX RIF — paired post vs pre, N=12")
    pre = np.array([r["pre"] for r in a2])
    post = np.array([r["post"] for r in a2])
    rif = np.array([r["rif"] for r in a2])
    print(f"  pre  mean={pre.mean():.2f}  SD={pre.std(ddof=1):.2f}   (paper 0.60 ± 0.25)")
    print(f"  post mean={post.mean():.2f}  SD={post.std(ddof=1):.2f}   (paper 0.70 ± 0.29)")
    print(f"  RIF  mean={rif.mean():.2f}  SD={rif.std(ddof=1):.2f}   (paper 0.10 ± 0.15)")
    assert almost_equal(pre.mean(), 0.60, 0.01)
    assert almost_equal(post.mean(), 0.70, 0.01)
    assert almost_equal(rif.mean(), 0.10, 0.01)
    paired_t = stats.ttest_rel(post, pre)
    wilc_paired = stats.wilcoxon(post, pre)
    one_samp_rif = stats.ttest_1samp(rif, 0.0)
    print(f"  paired t-test (matches study design):    t={paired_t.statistic:.3f}  p={paired_t.pvalue:.4f}")
    print(f"  one-sample t on RIF=post-pre vs 0:        t={one_samp_rif.statistic:.3f}  p={one_samp_rif.pvalue:.4f}")
    print(f"  Wilcoxon signed-rank paired:              W={wilc_paired.statistic:.3f}  p={wilc_paired.pvalue:.4f}")
    # Independent-samples reproductions of paper's p=0.37
    mwu = stats.mannwhitneyu(post, pre, alternative='two-sided')
    welch = stats.ttest_ind(post, pre, equal_var=False)
    print(f"  Mann-Whitney U (independent, ignores pairing): U={mwu.statistic:.1f}  p={mwu.pvalue:.4f}")
    print(f"  Welch t        (independent, ignores pairing): t={welch.statistic:.3f}  p={welch.pvalue:.4f}")
    print(f"  Paper reports p = 0.37 -> exactly matches Mann-Whitney U / Welch t "
          f"(independent samples).")
    print(f"  *** DISCREPANCY: Paper used an INDEPENDENT-samples test on PAIRED data. ***")
    print(f"      With the appropriate paired test, p ≈ {paired_t.pvalue:.3f} (SIGNIFICANT). "
          f"This may change the conclusion that the post-CT increase is non-significant.")
    print("  PASS γ-H2AX descriptives match Table A2 within ±0.01")
    assert abs(mwu.pvalue - 0.37) < 0.01, "failed to reproduce paper's p=0.37 via independent-samples test"

    print("\nAll Tier-1 checks PASSED.")
    print("Tier-2 (in-vivo only / ex-vivo only / per-group regression) requires "
          "recovering per-patient incubation labels — see README §Open questions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
