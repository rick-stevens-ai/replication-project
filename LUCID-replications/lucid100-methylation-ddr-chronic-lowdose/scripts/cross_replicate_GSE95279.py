#!/usr/bin/env python3
"""
Cross-replication of Priya et al. 2026 (IJRB 102:455-464, DOI 10.1080/09553002.2025.2607004)
using GSE95279 (Das/Cheriyan, BARC, same Kerala HLNRA cohort framework).

The paper itself reports its expression arm as "high inter-individual variation,
no dose-dependent change, no methylation-expression correlation" for the 4
hypermethylated genes (RAD23B, DNMT3A, MRE11A, BRCA1). The paper's methylation
matrix is not public; cross-replication of the methylation claim is not
feasible from public data. We CAN, however, test the closest claim that IS
testable: do these 4 genes show dose-dependent expression changes in a related
public Kerala HLNRA PBMC microarray dataset?

GSE95279:
  - Same lab (Bio-Sciences Group, BARC, India)
  - Same site (Kerala HLNRA coast)
  - Same tissue (PBMC), same sex (male)
  - n=36 subjects in 4 dose bins:
      Grp I:   <= 1.5  mGy/yr  (NLNRA control)
      Grp II:  1.51-5.0 mGy/yr (HLNRA low)
      Grp III: 5.01-15.0 mGy/yr (HLNRA mid)
      Grp IV:  > 15.0  mGy/yr  (HLNRA high)
  - Platform: HG-U133 Plus 2.0 (GPL570), log2 RMA-normalised in series matrix

Difference from Priya 2026: Priya stratifies on lifetime CUMULATIVE dose
(<100 vs >100 mSv) measured by personal dosimetry; GSE95279 stratifies on
annual residential background dose rate. Both are chronic LDIR proxies but
not numerically identical. So this is a CROSS-REPLICATION at the cohort level,
not a direct replication.

Output: results/cross_replication_GSE95279.{json,tsv}
"""
from __future__ import annotations

import csv
import gzip
import json
import math
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SM = ROOT / "data" / "GSE95279" / "GSE95279_series_matrix.txt"
OUT_DIR = ROOT / "results"
OUT_DIR.mkdir(exist_ok=True)

# Canonical HG-U133 Plus 2.0 probe sets for the 4 hypermethylated headline
# genes from Priya et al. 2026 + DDR + housekeeping controls.
PROBE_MAP = {
    "RAD23B":  ["201886_at"],                          # 201887_s_at not present
    "DNMT3A":  ["209125_at", "222640_at", "1567214_a_at"],
    "MRE11A":  ["205395_s_at", "205396_at", "211944_at", "215000_s_at"],
    "BRCA1":   ["204531_s_at", "211851_x_at"],         # 1568641_at not present
    # DDR controls present in Priya 16-gene panel but NOT in the hit list
    "ATM":     ["208442_s_at", "208443_x_at"],
    # Housekeeping
    "GAPDH":   ["212581_x_at"],
}

HEADLINE_HITS = {"RAD23B", "DNMT3A", "MRE11A", "BRCA1"}


# ---------- light-weight stats (no scipy dep) ----------
def mean(xs):
    return sum(xs) / len(xs)


def stdev(xs):
    if len(xs) < 2:
        return 0.0
    return statistics.stdev(xs)


def welch_t(a, b):
    """Return (t, df) for Welch's two-sample t."""
    n1, n2 = len(a), len(b)
    m1, m2 = mean(a), mean(b)
    v1 = statistics.variance(a) if n1 > 1 else 0.0
    v2 = statistics.variance(b) if n2 > 1 else 0.0
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return 0.0, max(n1 + n2 - 2, 1)
    t = (m1 - m2) / se
    num = (v1 / n1 + v2 / n2) ** 2
    den = (v1 ** 2) / ((n1 ** 2) * (n1 - 1)) + (v2 ** 2) / ((n2 ** 2) * (n2 - 1)) if n1 > 1 and n2 > 1 else 1.0
    df = num / den if den > 0 else max(n1 + n2 - 2, 1)
    return t, df


def two_sided_p_from_t(t, df):
    """Two-sided p-value for Student's t via scipy if available, else a
    Welch-Satterthwaite + cumulative approximation using math.erf."""
    try:
        from scipy.stats import t as student_t  # type: ignore
        return float(2 * (1 - student_t.cdf(abs(t), df)))
    except Exception:
        # Cornish-Fisher / normal-z approximation; only OK for df >= 10
        # Use the survival-function approximation via erfc
        if df >= 30:
            z = abs(t)
            return float(math.erfc(z / math.sqrt(2)))
        # crude lookup for small df won't be added here -- if scipy is missing
        # for small-df runs, flag it in output
        return float("nan")


def pearson(x, y):
    n = len(x)
    if n < 3:
        return 0.0, float("nan")
    mx, my = mean(x), mean(y)
    sx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    sy = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if sx == 0 or sy == 0:
        return 0.0, float("nan")
    r = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (sx * sy)
    # t = r * sqrt((n-2) / (1-r^2))
    if abs(r) >= 1:
        return r, 0.0
    t = r * math.sqrt((n - 2) / (1 - r * r))
    return r, two_sided_p_from_t(t, n - 2)


def bh_fdr(pvals):
    """Benjamini-Hochberg FDR. Returns q-values in original order."""
    m = len(pvals)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: pvals[i])
    ranked = [pvals[i] for i in order]
    q_sorted = [min(p * m / (k + 1), 1.0) for k, p in enumerate(ranked)]
    # monotone enforce
    for i in range(m - 2, -1, -1):
        q_sorted[i] = min(q_sorted[i], q_sorted[i + 1])
    q = [0.0] * m
    for rank, idx in enumerate(order):
        q[idx] = q_sorted[rank]
    return q


# ---------- parse series matrix ----------
DOSE_RE = re.compile(r"annual background radiation dose:\s*(.+)")

def parse_series_matrix(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    samples_titles = []
    samples_geo = []
    sample_chars: list[list[str]] = []
    in_table = False
    header = None
    table_rows: dict[str, list[float]] = {}

    with opener(path, "rt") as fh:
        for line in fh:
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                continue
            if line.startswith("!Sample_title"):
                samples_titles = [t.strip('"') for t in line.split("\t")[1:]]
            elif line.startswith("!Sample_geo_accession"):
                samples_geo = [t.strip('"') for t in line.split("\t")[1:]]
            elif line.startswith("!Sample_characteristics_ch1"):
                sample_chars.append([t.strip('"') for t in line.split("\t")[1:]])
            elif line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            elif line.startswith("!series_matrix_table_end"):
                in_table = False
            elif in_table:
                parts = line.split("\t")
                if header is None:
                    header = [p.strip('"') for p in parts]
                    continue
                probe = parts[0].strip('"')
                try:
                    vals = [float(v) for v in parts[1:]]
                except ValueError:
                    continue
                table_rows[probe] = vals

    # extract per-sample dose label
    dose_labels = []
    for sample_idx in range(len(samples_geo)):
        d = None
        for cline in sample_chars:
            m = DOSE_RE.match(cline[sample_idx])
            if m:
                d = m.group(1).strip()
                break
        dose_labels.append(d)

    # map dose labels -> integer rank 0..3 and bin midpoint mGy
    label_rank = {
        "<=1.5 mGy": (0, 1.0),
        "1.51-5.0 mGy": (1, 3.25),
        "5.01-15.0 mGy": (2, 10.0),
        ">15.0 mGy": (3, 20.0),
    }
    ranks = []
    mids = []
    for d in dose_labels:
        if d in label_rank:
            r, m = label_rank[d]
        else:
            r, m = (-1, float("nan"))
        ranks.append(r)
        mids.append(m)

    return {
        "samples": samples_geo,
        "titles": samples_titles,
        "dose_labels": dose_labels,
        "dose_rank": ranks,
        "dose_mid_mGy": mids,
        "probes": table_rows,
    }


def gene_summary(values_by_sample, dose_rank, dose_mid):
    """Per-gene stats: NLNRA vs HLNRA Welch t; ordinal Pearson r vs dose
    rank; Pearson r vs midpoint mGy."""
    nlnra = [v for v, r in zip(values_by_sample, dose_rank) if r == 0]
    hlnra = [v for v, r in zip(values_by_sample, dose_rank) if r >= 1]
    high  = [v for v, r in zip(values_by_sample, dose_rank) if r == 3]
    low   = [v for v, r in zip(values_by_sample, dose_rank) if r == 0]
    t, df = welch_t(hlnra, nlnra)
    p_hl = two_sided_p_from_t(t, df)
    t2, df2 = welch_t(high, low)
    p_extreme = two_sided_p_from_t(t2, df2)
    r_ord, p_ord = pearson(values_by_sample, dose_rank)
    r_mid, p_mid = pearson(values_by_sample, dose_mid)
    return {
        "n_NLNRA": len(nlnra),
        "n_HLNRA_all": len(hlnra),
        "mean_NLNRA": round(mean(nlnra), 4) if nlnra else None,
        "mean_HLNRA": round(mean(hlnra), 4) if hlnra else None,
        "delta_log2_HLNRA_vs_NLNRA": round(mean(hlnra) - mean(nlnra), 4) if nlnra and hlnra else None,
        "welch_t_HLNRA_vs_NLNRA": round(t, 4),
        "welch_df": round(df, 2),
        "welch_p_HLNRA_vs_NLNRA": round(p_hl, 5) if not math.isnan(p_hl) else None,
        "welch_p_GrpIV_vs_GrpI": round(p_extreme, 5) if not math.isnan(p_extreme) else None,
        "pearson_r_dose_rank": round(r_ord, 4),
        "pearson_p_dose_rank": round(p_ord, 5) if not math.isnan(p_ord) else None,
        "pearson_r_dose_mid_mGy": round(r_mid, 4),
        "pearson_p_dose_mid_mGy": round(p_mid, 5) if not math.isnan(p_mid) else None,
    }


def main() -> int:
    if not SM.exists():
        sys.exit(f"missing series matrix: {SM}")

    data = parse_series_matrix(SM)
    n_samples = len(data["samples"])
    print(f"[info] parsed series matrix: n_samples={n_samples}, n_probes={len(data['probes'])}")
    print(f"[info] dose-bin counts: ", {
        l: data['dose_labels'].count(l) for l in sorted(set(data['dose_labels']))
    })

    # gather per-gene per-probe stats
    rows = []
    for gene, probes in PROBE_MAP.items():
        for probe in probes:
            v = data["probes"].get(probe)
            if v is None:
                rows.append({"gene": gene, "probe": probe, "present": False})
                continue
            s = gene_summary(v, data["dose_rank"], data["dose_mid_mGy"])
            rows.append({
                "gene": gene,
                "probe": probe,
                "present": True,
                "is_headline_hit": gene in HEADLINE_HITS,
                **s,
            })

    # FDR across present probes (BH on Welch HLNRA vs NLNRA p-values)
    present_idx = [i for i, r in enumerate(rows) if r.get("present") and r.get("welch_p_HLNRA_vs_NLNRA") is not None]
    pvals = [rows[i]["welch_p_HLNRA_vs_NLNRA"] for i in present_idx]
    qvals = bh_fdr(pvals)
    for i, q in zip(present_idx, qvals):
        rows[i]["bh_q_HLNRA_vs_NLNRA"] = round(q, 4)

    # Pearson on dose-rank, BH FDR
    pvals_r = [rows[i].get("pearson_p_dose_rank") for i in present_idx
               if rows[i].get("pearson_p_dose_rank") is not None]
    idx_r = [i for i in present_idx if rows[i].get("pearson_p_dose_rank") is not None]
    qvals_r = bh_fdr(pvals_r)
    for i, q in zip(idx_r, qvals_r):
        rows[i]["bh_q_pearson_dose_rank"] = round(q, 4)

    # write outputs
    out_json = OUT_DIR / "cross_replication_GSE95279.json"
    out_tsv = OUT_DIR / "cross_replication_GSE95279.tsv"
    out_json.write_text(json.dumps({
        "source_paper_doi": "10.1080/09553002.2025.2607004",
        "source_paper_label": "Priya et al. 2026, Int J Radiat Biol 102:455-464",
        "cross_dataset_GEO": "GSE95279",
        "cross_dataset_lab": "Bio-Sciences Group, BARC, India",
        "cross_dataset_site": "Kerala HLNRA + NLNRA control",
        "cross_dataset_tissue": "PBMC, male only",
        "cross_dataset_n": n_samples,
        "cross_dataset_platform": "GPL570 (HG-U133 Plus 2.0)",
        "dose_stratification_GSE95279": "annual background dose-rate bins (mGy/yr)",
        "dose_stratification_Priya":    "lifetime cumulative dose bins (<100 / >100 mSv)",
        "stratification_note": "Different but related chronic LDIR proxies; this is a CROSS-replication, not a direct replication.",
        "headline_hypermethylated_genes_Priya": sorted(HEADLINE_HITS),
        "tested_genes": sorted(PROBE_MAP.keys()),
        "fdr_correction": "Benjamini-Hochberg over all probes tested in this script",
        "rows": rows,
    }, indent=2, sort_keys=True))

    fields = sorted({k for r in rows for k in r.keys()})
    with out_tsv.open("w") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # print a short pretty summary to stdout
    print()
    print("=== headline 4-gene expression vs HLNRA dose (GSE95279) ===")
    print(f"{'gene':<8} {'probe':<16} {'dHLNRA':>8} {'pHLvNL':>8} {'qBH':>7} {'r_rank':>7} {'pRank':>8}")
    for r in rows:
        if not r.get("present"):
            print(f"{r['gene']:<8} {r['probe']:<16} (probe absent)")
            continue
        flag = "*" if r.get("is_headline_hit") else " "
        print(f"{r['gene']:<8}{flag} {r['probe']:<16} "
              f"{r.get('delta_log2_HLNRA_vs_NLNRA','-'):>8} "
              f"{r.get('welch_p_HLNRA_vs_NLNRA','-'):>8} "
              f"{r.get('bh_q_HLNRA_vs_NLNRA','-'):>7} "
              f"{r.get('pearson_r_dose_rank','-'):>7} "
              f"{r.get('pearson_p_dose_rank','-'):>8}")

    print(f"\nwrote {out_json}")
    print(f"wrote {out_tsv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
