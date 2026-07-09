#!/usr/bin/env python3
"""
Claim-consistency audit for Koturbash et al. 2016 (dvw025).

This does NOT fabricate biology. It only checks two things that ARE computable
from the published text:

  (A) Bonferroni arithmetic. The paper states alpha=0.05, m=5 -> per-test 0.01.
      For every quantitative claim with a published p-value in notes/claims.md,
      verify that the claim's significance call ("significant" vs not) is
      consistent with the published p compared against the Bonferroni-corrected
      0.01 threshold (not the naive 0.05 threshold the authors actually used
      verbally in places).

  (B) Monotonicity of the reported dose-response. For each tissue with multiple
      published cumulative-dose fold-change values, check whether the values
      are (weakly) monotone non-decreasing with dose, which is the qualitative
      claim of the paper ("dose-dependent").

Inputs: the published claims, hard-coded here from notes/claims.md (the paper
provides no machine-readable numbers).
Outputs: results/claim_consistency.tsv and results/claim_consistency.log.

Zero dependencies, stdlib only. No data fabrication.
"""
from __future__ import annotations
import csv
import os
from dataclasses import dataclass, asdict

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
os.makedirs(OUT_DIR, exist_ok=True)

ALPHA = 0.05
M = 5
ALPHA_CORR = ALPHA / M  # 0.01


@dataclass
class Claim:
    figure: str
    tissue: str
    timepoint: str
    cumulative_dose_Gy: float
    fold_change: float | None   # None if direction-only ("ns")
    p_value: float | None       # None if not reported, "<0.05" handled below
    p_bound: str | None         # "<0.05", "<0.005", ">=0.05" etc.
    paper_call: str             # "significant" or "ns"

# Quantitative DNA-damage claims (Fig 2) extracted verbatim from notes/claims.md
CLAIMS: list[Claim] = [
    # Frontal cortex
    Claim("Fig2", "frontal_cortex", "6h",  0.2, 1.85, 0.027, None,    "significant"),
    Claim("Fig2", "frontal_cortex", "6h",  0.3, 2.4,  None,  "<0.05", "significant"),
    Claim("Fig2", "frontal_cortex", "6h",  0.4, 2.7,  None,  "<0.05", "significant"),
    Claim("Fig2", "frontal_cortex", "6h",  0.5, 3.0,  None,  "<0.05", "significant"),
    Claim("Fig2", "frontal_cortex", "24h", 0.2, 2.1,  0.005, None,    "significant"),
    Claim("Fig2", "frontal_cortex", "24h", 0.3, 2.5,  None,  "<0.05", "significant"),
    Claim("Fig2", "frontal_cortex", "24h", 0.4, 3.0,  None,  "<0.05", "significant"),
    Claim("Fig2", "frontal_cortex", "24h", 0.5, 3.5,  None,  "<0.05", "significant"),
    # Cerebellum
    Claim("Fig2", "cerebellum", "6h",  0.1, 1.5, None, "<0.005", "significant"),
    Claim("Fig2", "cerebellum", "6h",  0.2, 1.35, None, "<0.005", "significant"),
    Claim("Fig2", "cerebellum", "6h",  0.3, 1.35, None, "<0.005", "significant"),
    Claim("Fig2", "cerebellum", "6h",  0.4, 1.4, None, "<0.005", "significant"),
    Claim("Fig2", "cerebellum", "6h",  0.5, 1.3, None, "<0.005", "significant"),
    Claim("Fig2", "cerebellum", "24h", 0.5, 1.3, None, "<0.005", "significant"),
    # Hippocampus
    Claim("Fig2", "hippocampus", "6h", 0.1, 1.5, 0.013, None, "significant"),
    # Olfactory bulb — paper: ns at all doses/times
    Claim("Fig2", "olfactory_bulb", "any", 0.1, None, None, ">=0.05", "ns"),

    # Methylation (Fig 4) — cumulative_dose treated as Day-1 dose 0.1 Gy
    Claim("Fig4", "cerebellum",     "6h",  0.1, 1.35, None, "<0.05", "significant"),
    Claim("Fig4", "hippocampus",    "6h",  0.1, 1.5,  None, "<0.05", "significant"),
    Claim("Fig4", "hippocampus",    "24h", 0.1, 1.6,  None, "<0.05", "significant"),
    Claim("Fig4", "frontal_cortex", "6h",  0.1, 1.2,  None, ">=0.05", "ns"),
    Claim("Fig4", "frontal_cortex", "24h", 0.1, 1.25, None, "<0.05", "significant"),
    Claim("Fig4", "olfactory_bulb", "any", 0.1, None, None, ">=0.05", "ns"),
]


def p_is_below(p: float | None, bound: str | None, thr: float) -> bool | None:
    """Decide if 'p < thr' given either a numeric p or a bound string."""
    if p is not None:
        return p < thr
    if bound is None:
        return None
    # bound like "<0.05" or "<0.005" or ">=0.05"
    if bound.startswith("<"):
        b = float(bound[1:])
        if b <= thr:
            return True          # p < b <= thr -> definitely below
        # b > thr; we only know p < b; cannot conclude p < thr -> unknown
        return None
    if bound.startswith(">="):
        b = float(bound[2:])
        if b >= thr:
            return False         # p >= b >= thr -> not below
        return None
    return None


def main() -> int:
    tsv_path = os.path.join(OUT_DIR, "claim_consistency.tsv")
    log_path = os.path.join(OUT_DIR, "claim_consistency.log")

    rows = []
    n_total = 0
    n_consistent_naive = 0
    n_consistent_bonf  = 0
    n_unknown_bonf     = 0

    for c in CLAIMS:
        n_total += 1
        d = asdict(c)
        # naive: paper used alpha=0.05 verbally in places
        below_05 = p_is_below(c.p_value, c.p_bound, 0.05)
        # bonferroni: 0.01
        below_01 = p_is_below(c.p_value, c.p_bound, ALPHA_CORR)

        naive_consistent = (
            (c.paper_call == "significant" and below_05 is True) or
            (c.paper_call == "ns"          and below_05 is False)
        )
        if naive_consistent:
            n_consistent_naive += 1

        if below_01 is None:
            n_unknown_bonf += 1
            bonf_consistent = "unknown"
        else:
            bc = (
                (c.paper_call == "significant" and below_01 is True) or
                (c.paper_call == "ns"          and below_01 is False)
            )
            if bc:
                n_consistent_bonf += 1
            bonf_consistent = "yes" if bc else "no"

        d["below_alpha_0.05"] = below_05
        d["below_alpha_0.01_bonf"] = below_01
        d["naive_consistent"] = naive_consistent
        d["bonferroni_consistent"] = bonf_consistent
        rows.append(d)

    with open(tsv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    # Monotonicity check (Fig 2 dose-response per tissue/time)
    series = {}
    for c in CLAIMS:
        if c.figure != "Fig2" or c.fold_change is None:
            continue
        key = (c.tissue, c.timepoint)
        series.setdefault(key, []).append((c.cumulative_dose_Gy, c.fold_change))

    mono_lines = []
    n_mono_total = 0
    n_mono_increasing = 0
    for (tissue, time), pts in series.items():
        pts.sort()
        if len(pts) < 2:
            continue
        n_mono_total += 1
        is_mono_inc = all(pts[i+1][1] >= pts[i][1] for i in range(len(pts)-1))
        if is_mono_inc:
            n_mono_increasing += 1
        mono_lines.append(f"  {tissue:18s} {time:4s}: doses={[p[0] for p in pts]} folds={[p[1] for p in pts]} monotone_nondecreasing={is_mono_inc}")

    log = []
    log.append("Claim-consistency audit: Koturbash et al. 2016 (dvw025)")
    log.append(f"Total claims audited: {n_total}")
    log.append(f"Consistent at naive alpha=0.05    : {n_consistent_naive}/{n_total}")
    log.append(f"Consistent at Bonferroni alpha=0.01: {n_consistent_bonf}/{n_total} (unknown: {n_unknown_bonf})")
    log.append("")
    log.append("Dose-response monotonicity (Fig 2):")
    log.extend(mono_lines)
    log.append("")
    log.append(f"Monotone-non-decreasing series: {n_mono_increasing}/{n_mono_total}")
    log.append("")
    log.append(f"Outputs: {tsv_path}, {log_path}")

    text = "\n".join(log) + "\n"
    with open(log_path, "w") as f:
        f.write(text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
