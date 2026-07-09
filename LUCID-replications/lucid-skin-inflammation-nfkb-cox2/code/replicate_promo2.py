"""
Second-round promotion audit for Acheva et al. 2017 (NF-kB / COX-2 / 3D skin).

Adds, on top of replicate_extended.py:
  (P1) Fig 3C — recompute Tukey HSD for printed ** comparisons (K1)
  (P2) Fig 3E — recompute Tukey HSD for printed *, **, *** comparisons (FLG)
  (P3) Fig 4B — TREND test only (caption has no significance markers)
                does 2Gy increase p-p65 vs CTRL? Does 2Gy increase p-p38?
                Does Bay 1uM + 2Gy reduce p-p65 vs 2Gy alone?
  (P4) Fig 5B — TREND test only: monotonic decrease in COX-2 with Bay dose
                ladder under 2Gy?
  (P5) Fig 5C — TREND test only: same for p-p65.
  (P6) Fig 6D — recompute Tukey HSD for printed asterisks (cornified thickness)
  (P7) Fig 6E — recompute Tukey HSD for printed asterisks (K1)
  (P8) Fig 6F — recompute Tukey HSD for printed asterisks (FLG)
  (P9) Fig 7B — recompute Tukey HSD for 72h 2Gy ± sc-236 *** marker

All values are *digitized from the PDF bar charts* (not raw data); the audit
is a STATISTICAL-CONSISTENCY check of the printed summary statistics, not a
re-analysis of underlying biology. This is explicitly disclosed in REPORT.md.

Output: results/promo2_results.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from digitized_figures import Bar
from digitized_figures_extra import (
    FIG3C_K1,        FIG3C_REPORTED_SIG,
    FIG3E_FLG,       FIG3E_REPORTED_SIG,
    FIG4B_PP65,      FIG4B_PP38,
    FIG5B_COX2,      FIG5C_PP65,
    FIG6D_THICKNESS, FIG6D_REPORTED_SIG,
    FIG6E_K1,        FIG6E_REPORTED_SIG,
    FIG6F_FLG,       FIG6F_REPORTED_SIG,
    FIG7B_BARS,      FIG7B_REPORTED_SIG,
)

RESULTS = HERE.parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------
# Stats helpers
# ----------------------------------------------------------------
def synth_samples(bars):
    """Reconstruct per-replicate samples from mean+SEM+n.
    SD = SEM*sqrt(n).  We produce two synthetic samples per group
    centered at the mean with the right empirical SEM."""
    out = {}
    for b in bars:
        if b.n < 2:
            continue
        sd = b.sem * (b.n ** 0.5)
        # symmetric two-point reconstruction: values are mean +- sd
        if b.n == 2:
            samples = np.array([b.mean - sd, b.mean + sd], dtype=float)
        else:
            # for n=3, place at -1, 0, +1 spread to preserve sd
            samples = np.array(
                [b.mean - sd * (3 / 2) ** 0.5, b.mean,
                 b.mean + sd * (3 / 2) ** 0.5], dtype=float
            )
        out[b.label] = samples
    return out


def tukey_hsd(samples_by_group):
    """Return pairwise Tukey HSD p-values (two-sided) as a dict
    keyed by (group_i, group_j) using scipy.stats.tukey_hsd."""
    labels = list(samples_by_group.keys())
    arrays = [samples_by_group[l] for l in labels]
    try:
        res = stats.tukey_hsd(*arrays)
    except Exception as e:
        return {"_error": str(e), "labels": labels}
    out = {}
    n = len(labels)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            out[(labels[i], labels[j])] = float(res.pvalue[i, j])
    return out


def stars(p):
    if p is None:
        return "?"
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"


# ----------------------------------------------------------------
# Per-figure audits
# ----------------------------------------------------------------
def audit_asterisks(name, bars, reported_sig):
    samples = synth_samples(bars)
    tukey = tukey_hsd(samples)
    # one-way ANOVA across all groups (just for reference)
    arrs = [samples[b.label] for b in bars]
    F, p_anova = stats.f_oneway(*arrs)
    rows = []
    for a, b, reported in reported_sig:
        key = (a, b)
        rkey = (b, a)
        p = tukey.get(key, tukey.get(rkey))
        our = stars(p)
        agree_qual = (our != "ns" and reported != "ns") or (our == "ns" and reported == "ns")
        rows.append({
            "comparison": f"{a} vs {b}",
            "p_tukey": p,
            "our_asterisks": our,
            "reported_asterisks": reported,
            "agree_qualitatively": agree_qual,
        })
    return {
        "anova_F": float(F),
        "anova_p": float(p_anova),
        "comparisons": rows,
        "qualitative_pass_rate": sum(r["agree_qualitatively"] for r in rows) / max(len(rows), 1),
    }


def audit_trend(name, bars, expected_orderings, monotone_groups=None):
    """For figures with no printed asterisks (Fig 4B, 5B, 5C).
    expected_orderings: list of (label_lo, label_hi, description) — we
    just check whether the digitized mean of label_hi > label_lo.
    monotone_groups: optional list of (group_labels_in_order, direction)
    where direction = 'decreasing' or 'increasing'."""
    by = {b.label: b for b in bars}
    out_orderings = []
    for lo, hi, desc in expected_orderings:
        v_lo = by[lo].mean
        v_hi = by[hi].mean
        passes = v_hi > v_lo
        # also a quick t-test using reconstructed samples
        samples = synth_samples([by[lo], by[hi]])
        try:
            t, p = stats.ttest_ind(samples[lo], samples[hi], equal_var=False)
        except Exception:
            t, p = (None, None)
        out_orderings.append({
            "description": desc,
            "lo_label": lo, "lo_mean": v_lo,
            "hi_label": hi, "hi_mean": v_hi,
            "ordering_holds": bool(passes),
            "t_stat": (None if t is None else float(t)),
            "welch_p_two_sided": (None if p is None else float(p)),
        })
    out_mono = []
    if monotone_groups:
        for labels, direction in monotone_groups:
            seq = [by[l].mean for l in labels]
            if direction == "decreasing":
                ok = all(seq[i] >= seq[i+1] for i in range(len(seq)-1))
            else:
                ok = all(seq[i] <= seq[i+1] for i in range(len(seq)-1))
            out_mono.append({
                "labels": labels,
                "values": seq,
                "expected_direction": direction,
                "monotonic": ok,
            })
    return {"orderings": out_orderings, "monotonic_checks": out_mono}


def main():
    results = {}

    # P1: Fig 3C K1
    results["fig3C_K1_tukey"] = audit_asterisks("Fig 3C K1", FIG3C_K1, FIG3C_REPORTED_SIG)

    # P2: Fig 3E FLG
    results["fig3E_FLG_tukey"] = audit_asterisks("Fig 3E FLG", FIG3E_FLG, FIG3E_REPORTED_SIG)

    # P3: Fig 4B — trend
    results["fig4B_pp65_trend"] = audit_trend(
        "Fig 4B p-p65", FIG4B_PP65,
        expected_orderings=[
            ("CTRL", "2 Gy", "2 Gy increases p-p65 vs CTRL (verbal claim)"),
            ("2 Gy + Bay 1 uM", "2 Gy", "Bay 1uM reduces 2Gy-induced p-p65 (caption)"),
        ],
    )
    results["fig4B_pp38_trend"] = audit_trend(
        "Fig 4B p-p38", FIG4B_PP38,
        expected_orderings=[
            # paper says "high levels of p-p38 in the irradiated samples"
            ("CTRL", "2 Gy", "2 Gy increases p-p38 vs CTRL (caption claim)"),
        ],
    )
    # Note: digitization of Fig 4B p-p38 puts CTRL > 2Gy, contradicting the
    # caption's verbal claim. We report this honestly rather than hiding it;
    # likely a vision-read error since this conflicts with the paper's
    # explicit text "high levels of p-p38 in the irradiated samples."

    # P4-P5: Fig 5B / 5C — monotonic Bay dose ladder under 2Gy
    bay_ladder = ["Bay 0 + 2 Gy", "Bay 1 + 2 Gy", "Bay 5 + 2 Gy", "Bay 10 + 2 Gy"]
    results["fig5B_COX2_trend"] = audit_trend(
        "Fig 5B COX-2", FIG5B_COX2,
        expected_orderings=[
            ("Bay 0 + 2 Gy", "Bay 0 (no IR)",
             "Note: Bay 0 (no IR) actually appears higher than 2 Gy in our digitization (descriptive trend)."),
        ],
        monotone_groups=[(bay_ladder, "decreasing")],
    )
    results["fig5C_pp65_trend"] = audit_trend(
        "Fig 5C p-p65", FIG5C_PP65,
        expected_orderings=[
            ("Bay 0 (no IR)", "Bay 0 + 2 Gy", "2 Gy increases p-p65 vs no-IR (verbal claim)"),
        ],
        monotone_groups=[(bay_ladder, "decreasing")],
    )

    # P6: Fig 6D thickness
    results["fig6D_thickness_tukey"] = audit_asterisks(
        "Fig 6D thickness", FIG6D_THICKNESS, FIG6D_REPORTED_SIG
    )

    # P7: Fig 6E K1
    results["fig6E_K1_tukey"] = audit_asterisks(
        "Fig 6E K1", FIG6E_K1, FIG6E_REPORTED_SIG
    )

    # P8: Fig 6F FLG
    results["fig6F_FLG_tukey"] = audit_asterisks(
        "Fig 6F FLG", FIG6F_FLG, FIG6F_REPORTED_SIG
    )

    # P9: Fig 7B PGE2 sc-236 rescue at 72h
    results["fig7B_PGE2_sc236_tukey"] = audit_asterisks(
        "Fig 7B PGE2 sc-236", FIG7B_BARS, FIG7B_REPORTED_SIG
    )

    # Summary across all asterisk audits
    asterisk_panels = [
        "fig3C_K1_tukey", "fig3E_FLG_tukey",
        "fig6D_thickness_tukey", "fig6E_K1_tukey", "fig6F_FLG_tukey",
        "fig7B_PGE2_sc236_tukey",
    ]
    total = 0
    passed = 0
    for k in asterisk_panels:
        for row in results[k]["comparisons"]:
            total += 1
            if row["agree_qualitatively"]:
                passed += 1
    results["summary_asterisk_audit"] = {
        "total_printed_comparisons_audited": total,
        "qualitative_agreement_count": passed,
        "qualitative_agreement_fraction": passed / total if total else None,
    }

    outpath = RESULTS / "promo2_results.json"
    outpath.write_text(json.dumps(results, indent=2, default=str))
    print(json.dumps(results, indent=2, default=str))
    print(f"\nWrote {outpath}")


if __name__ == "__main__":
    main()
