#!/usr/bin/env python3
"""
LUCID100 slot 26 — Botbayev et al. 2026 (Genes, DOI 10.3390/genes17020191)
Minimal statistical replication.

Strategy
--------
Tables 4–7 report only genotype *frequencies* (not raw counts). Table 1 gives N
per (location × ethnic) cell. We back-compute counts as round(N × freq), then
recompute:
    * Pearson chi-square on the 2 × 3 genotype contingency
    * Pearson chi-square on the 2 × 2 allele contingency (HWE-free count = 2N)
    * Allelic OR with 95% Woolf CI
    * Hardy–Weinberg equilibrium test in controls
and compare against the paper's printed chi², p, OR, CI.

This is a "table reconstruction" replication: it cannot confirm the underlying
genotype calls (raw data are "available on request"), but it confirms whether
the chi-square / OR statistics in the paper are mathematically consistent with
the published frequencies and group sizes — the most that public artifacts allow.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "tables" / "tables_extracted.json"
OUT  = HERE.parent / "results" / "replication_chi2.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

# N per cohort × ethnic group (Table 1)
N_GROUPS = {
    ("Control", "Kazakh"):       129,
    ("Control", "Russian"):      160,
    ("Stepnogorsk", "Kazakh"):    52,
    ("Stepnogorsk", "Russian"):  172,
    ("Balkashinskoye", "Kazakh"): 54,
    ("Balkashinskoye", "Russian"):184,
}

@dataclass
class SNPTable:
    locus: str
    rs: str
    genotypes: tuple  # length 3, e.g. ("I-/I-","I-/I+","I+/I+")
    # paper-reported rows: list of dicts {location, pop, miner_freqs[3], control_freqs[3], paper_chi2_gt, paper_p_gt, paper_chi2_al, paper_p_al, paper_OR, paper_CI}
    rows: list

def woolf_or_ci(a, b, c, d, alpha=0.05):
    """Allelic Odds Ratio with Woolf (log) 95% CI. Handle zero cells with +0.5."""
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    or_ = (a * d) / (b * c)
    se = math.sqrt(1/a + 1/b + 1/c + 1/d)
    z = stats.norm.ppf(1 - alpha/2)
    lo = math.exp(math.log(or_) - z*se)
    hi = math.exp(math.log(or_) + z*se)
    return or_, (lo, hi)

def hwe_chi2(counts):
    """Hardy–Weinberg chi^2 (df=1) for a 3-genotype count vector (AA, Aa, aa)."""
    AA, Aa, aa = counts
    n = AA + Aa + aa
    if n == 0:
        return float("nan"), float("nan")
    p = (2*AA + Aa) / (2*n)
    q = 1 - p
    exp = np.array([n*p*p, 2*n*p*q, n*q*q])
    obs = np.array([AA, Aa, aa])
    mask = exp > 0
    chi2 = float(((obs[mask] - exp[mask])**2 / exp[mask]).sum())
    pval = 1 - stats.chi2.cdf(chi2, df=1)
    return chi2, pval

def freqs_to_counts(freqs, n):
    """Round f * n while preserving sum to n (largest remainders)."""
    raw = np.array(freqs) * n
    base = np.floor(raw).astype(int)
    rem = raw - base
    short = int(round(n - base.sum()))
    if short > 0:
        # bump up the cells with largest fractional part
        order = np.argsort(-rem)
        for i in range(short):
            base[order[i]] += 1
    elif short < 0:
        order = np.argsort(rem)  # smallest fractional bumped down
        for i in range(-short):
            base[order[i]] = max(base[order[i]] - 1, 0)
    return base.tolist()

def chi2_genotype(miner_counts, control_counts):
    table = np.array([miner_counts, control_counts])
    if (table.sum(axis=0) == 0).any():
        cols = table.sum(axis=0) > 0
        table = table[:, cols]
    chi2, p, dof, _ = stats.chi2_contingency(table, correction=False)
    return chi2, p, dof

def chi2_allele(miner_counts, control_counts):
    # collapse genotype counts (AA, Aa, aa) into allele counts (A, a) by 2*AA+Aa, Aa+2*aa
    def alleles(c):
        AA, Aa, aa = c
        return [2*AA + Aa, Aa + 2*aa]
    m = alleles(miner_counts)
    c = alleles(control_counts)
    table = np.array([m, c])
    chi2, p, dof, _ = stats.chi2_contingency(table, correction=False)
    return chi2, p, dof, m, c

def main():
    data = json.loads(DATA.read_text())
    tables = data["tables"]

    snps = [
        # (table_key, rs, genotype_labels, paper rows)
        ("table_4_tp53_intron3_rs17878362", "rs17878362", ("I-/I-","I-/I+","I+/I+")),
        ("table_5_tp53_intron6_rs1625895",  "rs1625895",  ("GG","GA","AA")),
        ("table_6_tp53_exon4_rs1042522",    "rs1042522",  ("AA","AP","PP")),
        ("table_7_p21_codon31_rs1801270",   "rs1801270",  ("CC","CA","AA")),
    ]

    # group iteration through (location, ethnic) keys present in each paper table
    cohort_blocks = [
        ("Stepnogorsk",  "Kazakh"),
        ("Stepnogorsk",  "Russian"),
        ("Balkashinskoye","Kazakh"),
        ("Balkashinskoye","Russian"),
    ]

    out = {"meta": {"source_tables": str(DATA), "method": "freq*N reconstruction; Pearson chi2; Woolf OR"},
           "results": []}

    for tkey, rs, geno_labels in snps:
        t = tables[tkey]
        rows = t["rows"]  # 12 rows: 4 cohort blocks x 3 genotypes
        for bidx, (loc, pop) in enumerate(cohort_blocks):
            block = rows[bidx*3 : bidx*3 + 3]
            # Some rs1801270 blocks reorder genotype labels (CA/CC/AA in Balkashinskoye)
            # Sort by genotype label to match canonical order
            label_to_freq = {}
            paper_or = paper_ci = paper_chi2_gt = paper_p_gt = paper_chi2_al = paper_p_al = None
            for r in block:
                # row layout: [loc, pop, genotype, miner_freq, control_freq, OR, CI, chi2_gt, p_gt, chi2_al, p_al]
                # only the FIRST genotype row in each block carries the published stats; later rows have None in stat fields.
                gt = r[2]; mf = float(r[3]); cf = float(r[4])
                label_to_freq[gt] = (mf, cf)
                if r[5] is not None:
                    paper_or = r[5]
                if r[6] is not None:
                    paper_ci = r[6]
                if r[7] is not None:
                    paper_chi2_gt = r[7]
                if r[8] is not None:
                    paper_p_gt = r[8]
                if r[9] is not None:
                    paper_chi2_al = r[9]
                if r[10] is not None:
                    paper_p_al = r[10]

            miner_freqs   = [label_to_freq[g][0] for g in geno_labels]
            control_freqs = [label_to_freq[g][1] for g in geno_labels]

            n_miner   = N_GROUPS[(loc, pop)]
            n_control = N_GROUPS[("Control", pop)]
            miner_counts   = freqs_to_counts(miner_freqs,   n_miner)
            control_counts = freqs_to_counts(control_freqs, n_control)

            chi2_gt, p_gt, dof_gt   = chi2_genotype(miner_counts, control_counts)
            chi2_al, p_al, dof_al, m_alleles, c_alleles = chi2_allele(miner_counts, control_counts)

            # allelic OR: 2x2 = [[exposed minor, exposed major], [control minor, control major]]
            # use convention from many genetic studies: OR for risk allele = minor allele.
            # We follow: a=exposed_minor (a_allele), b=exposed_major (A_allele), c=control_minor, d=control_major
            a, b = m_alleles[1], m_alleles[0]  # minor, major in miners
            c, d = c_alleles[1], c_alleles[0]  # minor, major in controls
            or_, (lo, hi) = woolf_or_ci(a, b, c, d)

            # HWE in controls
            hwe_chi2_ctrl, hwe_p_ctrl = hwe_chi2(control_counts)
            hwe_chi2_min,  hwe_p_min  = hwe_chi2(miner_counts)

            result = {
                "snp": rs, "table": tkey, "location": loc, "population": pop,
                "n_miner": n_miner, "n_control": n_control,
                "genotype_labels": list(geno_labels),
                "miner_freqs": miner_freqs, "control_freqs": control_freqs,
                "miner_counts_reconstructed":   miner_counts,
                "control_counts_reconstructed": control_counts,
                "computed": {
                    "chi2_genotype":      round(chi2_gt, 3),
                    "p_genotype":         round(p_gt, 4),
                    "dof_genotype":       dof_gt,
                    "chi2_allele":        round(chi2_al, 3),
                    "p_allele":           round(p_al, 4),
                    "dof_allele":         dof_al,
                    "miner_alleles":      m_alleles,
                    "control_alleles":    c_alleles,
                    "OR_minor_vs_major":  round(or_, 3),
                    "OR_95CI":            [round(lo, 3), round(hi, 3)],
                    "HWE_controls_chi2":  round(hwe_chi2_ctrl, 3),
                    "HWE_controls_p":     round(hwe_p_ctrl, 4),
                    "HWE_miners_chi2":    round(hwe_chi2_min, 3),
                    "HWE_miners_p":       round(hwe_p_min, 4),
                },
                "paper_published": {
                    "chi2_genotype": paper_chi2_gt,
                    "p_genotype":    paper_p_gt,
                    "chi2_allele":   paper_chi2_al,
                    "p_allele":      paper_p_al,
                    "OR":            paper_or,
                    "CI":            paper_ci,
                }
            }
            out["results"].append(result)

    OUT.write_text(json.dumps(out, indent=2))

    # Print a compact summary
    print(f"Wrote {OUT}")
    print(f"{'SNP':<12} {'Loc':<14} {'Pop':<8} {'recomp p_gt':>12} {'paper p_gt':>12} {'recomp p_al':>12} {'paper p_al':>12} {'recomp OR':>10} {'paper OR':>10} {'HWE p (ctrl)':>14}")
    sig_match, sig_mismatch = 0, 0
    for r in out["results"]:
        c = r["computed"]; p = r["paper_published"]
        try:
            ppgt = float(p['p_genotype']); rpgt = c['p_genotype']
            agree = (rpgt < 0.05) == (ppgt < 0.05)
            if agree: sig_match += 1
            else:     sig_mismatch += 1
            flag = "" if agree else "  *MISMATCH*"
        except Exception:
            flag = ""
        print(f"{r['snp']:<12} {r['location']:<14} {r['population']:<8} "
              f"{c['p_genotype']:>12.4f} {str(p['p_genotype']):>12} "
              f"{c['p_allele']:>12.4f} {str(p['p_allele']):>12} "
              f"{c['OR_minor_vs_major']:>10.3f} {str(p['OR']):>10} "
              f"{c['HWE_controls_p']:>14.4f}{flag}")
    print(f"\nsignificance-direction agreements (genotype p<0.05): {sig_match}/{sig_match+sig_mismatch}")

if __name__ == "__main__":
    main()
