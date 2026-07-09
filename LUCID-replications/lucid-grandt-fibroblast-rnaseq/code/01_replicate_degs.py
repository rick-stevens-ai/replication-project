#!/usr/bin/env python3
"""
Replication of Grandt et al. 2022 (KiKme, Mol Med 28:105, DOI 10.1186/s10020-022-00520-6)

Replication targets (from main text, Results section):
  R1. After 0.05 Gy (LDIR), FDR<0.05 DEG counts (model 1):
        N0 = 236, N1 = 653, N2+ = 694
  R2. After 0.05 Gy, fraction upregulated (model 1):
        N0 = 44.07% (n_up = 104), N2+ = 40.63%, N1 = 37.67%
  R3. After 2 Gy, "the number of DEGs was similar across donor groups"
        (no exact numbers in main text; we extract them from AF1a).
  R4. Top genes after 2 Gy with highest |LFC| (text):
        CDKN1A, TIGAR, HSPA4L, MDM2, BLOC1S2, PPM1D, SESN1, BTG2, FBXO22, PCNA, TRIAP1
  R5. Top genes after 0.05 Gy (text):
        SESN1, MDM2, CDKN1A, TIGAR, BTG2, BLOC1S2, PPM1D, PHLDB3, FBXO22, AEN, TRIAP1, POLH
  R6. Interaction analysis after 2 Gy, model 1: seven genes differentially expressed
        depending on donor group (FDR<0.05 in N2+/N1 vs N0):
        LINC00601, COBLL1, SESN2, BIN3, TNFRSF10A, EEF1AKNMT, BTG2
  R7. Total genes detected in the experiment: 14,756.
  R8. Pathway enrichment: HALLMARK_P53_PATHWAY (and KEGG_P53_SIGNALING_PATHWAY)
        should be the top enriched pathway in DEGs across groups and doses.

Data source: AF1.xlsx (Additional File 1) supplementary table from BMC Mol Med.
"""

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
DATA = PROJECT / "data"
RESULTS = PROJECT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

DEG_FILE = DATA / "AF1a_degs.tsv"
INT_FILE = DATA / "AF1b_degs_interaction.tsv"

FDR_THRESH = 0.05


def load_degs(path):
    rows = []
    with open(path) as f:
        rdr = csv.DictReader(f, delimiter="\t")
        for r in rdr:
            try:
                r["log2FC"] = float(r["log2FC"])
                r["FDR"] = float(r["FDR"])
                r["P-value"] = float(r["P-value"])
            except (ValueError, TypeError):
                continue
            rows.append(r)
    return rows


def main():
    print(f"Loading {DEG_FILE} ...")
    degs = load_degs(DEG_FILE)
    print(f"  -> {len(degs):,} rows")
    print(f"Loading {INT_FILE} ...")
    inter = load_degs(INT_FILE)
    print(f"  -> {len(inter):,} rows")

    # Sanity: column values present
    groups = Counter((r["Group"], r["Dose"], r["Model"]) for r in degs)
    print("\n(Group, Dose, Model) row counts in AF1a (each = total tested genes):")
    for k, v in sorted(groups.items()):
        print(f"  {k}: {v:,}")

    # === R7. Total genes detected ===
    genes_per_combo = {k: v for k, v in groups.items()}
    print("\nR7 check: paper reports 14,756 detected genes.")
    print(f"  Observed per-combo row counts (which equal #tested genes): {sorted(set(genes_per_combo.values()))}")

    # === R1, R2, R3. DEG counts by group/dose/model at FDR<0.05 ===
    sig = defaultdict(lambda: {"n_total": 0, "n_up": 0, "n_down": 0})
    for r in degs:
        if r["FDR"] < FDR_THRESH:
            key = (r["Group"], r["Dose"], r["Model"])
            sig[key]["n_total"] += 1
            if r["log2FC"] > 0:
                sig[key]["n_up"] += 1
            else:
                sig[key]["n_down"] += 1

    deg_table = []
    for k in sorted(sig):
        s = sig[k]
        s["frac_up"] = s["n_up"] / s["n_total"] if s["n_total"] else float("nan")
        deg_table.append({
            "Group": k[0], "Dose": k[1], "Model": k[2],
            "DEGs": s["n_total"], "Up": s["n_up"], "Down": s["n_down"],
            "PctUp": round(100 * s["frac_up"], 2)
        })

    with open(RESULTS / "deg_counts.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Group", "Dose", "Model", "DEGs", "Up", "Down", "PctUp"], delimiter="\t")
        w.writeheader()
        for row in deg_table:
            w.writerow(row)

    print("\n=== DEG counts at FDR<0.05 (replicates Fig 2a, Fig 5a, Table-like) ===")
    print(f"{'Group':<6} {'Dose':<8} {'Model':<10} {'DEGs':>6} {'Up':>6} {'Down':>6} {'PctUp':>7}")
    for row in deg_table:
        print(f"{row['Group']:<6} {row['Dose']:<8} {row['Model']:<10} {row['DEGs']:>6} {row['Up']:>6} {row['Down']:>6} {row['PctUp']:>6.2f}%")

    # Compare to paper
    expected_ldir_m1 = {"N0": 236, "N1": 653, "N2+": 694}
    expected_ldir_pctup_m1 = {"N0": 44.07, "N1": 37.67, "N2+": 40.63}
    expected_ldir_nup_m1_N0 = 104

    print("\n=== R1/R2 verification (0.05 Gy, model 1) ===")
    for row in deg_table:
        if row["Dose"] == "0.05 Gy" and row["Model"] == "model 1":
            exp_n = expected_ldir_m1[row["Group"]]
            exp_p = expected_ldir_pctup_m1[row["Group"]]
            match_n = "✓" if row["DEGs"] == exp_n else "✗"
            match_p = "✓" if abs(row["PctUp"] - exp_p) < 0.5 else "✗"
            print(f"  {row['Group']:<4}: DEGs={row['DEGs']} (paper={exp_n}) {match_n} | "
                  f"%Up={row['PctUp']:.2f}% (paper={exp_p}%) {match_p} | "
                  f"n_up={row['Up']} (paper N0={expected_ldir_nup_m1_N0 if row['Group']=='N0' else '?'})")

    # === R5. Top genes by adjusted p-value across groups after 0.05 Gy ===
    print("\n=== R5 verification: top genes by FDR after 0.05 Gy, model 1 ===")
    expected_top_ldir = {"SESN1", "MDM2", "CDKN1A", "TIGAR", "BTG2", "BLOC1S2",
                         "PPM1D", "PHLDB3", "FBXO22", "AEN", "TRIAP1", "POLH"}
    for group in ["N0", "N1", "N2+"]:
        subset = [r for r in degs if r["Dose"] == "0.05 Gy" and r["Model"] == "model 1" and r["Group"] == group]
        subset.sort(key=lambda r: r["FDR"])
        top12 = [r["Gene"] for r in subset[:12]]
        hits = expected_top_ldir & set(top12)
        print(f"  {group}: top12 by FDR = {top12}")
        print(f"    overlap with paper top set ({len(expected_top_ldir)}): {len(hits)}/{len(top12)} -> {sorted(hits)}")

    # === R4. Top genes after 2 Gy ===
    print("\n=== R4 verification: top genes by |log2FC| (among FDR<0.05) after 2 Gy, model 1 ===")
    expected_top_hdir = {"CDKN1A", "TIGAR", "HSPA4L", "MDM2", "BLOC1S2", "PPM1D",
                         "SESN1", "BTG2", "FBXO22", "PCNA", "TRIAP1"}
    for group in ["N0", "N1", "N2+"]:
        subset = [r for r in degs if r["Dose"] == "2 Gy" and r["Model"] == "model 1"
                  and r["Group"] == group and r["FDR"] < FDR_THRESH]
        subset.sort(key=lambda r: abs(r["log2FC"]), reverse=True)
        top12 = [r["Gene"] for r in subset[:12]]
        hits = expected_top_hdir & set(top12)
        print(f"  {group}: top12 by |LFC| = {top12}")
        print(f"    overlap with paper top set ({len(expected_top_hdir)}): {len(hits)}/{len(top12)} -> {sorted(hits)}")

    # === R6. 7 interaction genes after 2 Gy ===
    print("\n=== R6 verification: interaction analysis after 2 Gy, FDR<0.05 ===")
    expected_int = {"LINC00601", "COBLL1", "SESN2", "BIN3", "TNFRSF10A", "EEF1AKNMT", "BTG2"}
    int_sig = defaultdict(list)
    for r in inter:
        if r["Dose"] == "2 Gy" and r["FDR"] < FDR_THRESH:
            int_sig[r["Comparison"]].append((r["Gene"], r["FDR"], r["log2FC"]))
    for comp, items in sorted(int_sig.items()):
        items.sort(key=lambda x: x[1])
        print(f"  Comparison: {comp}  (n_sig={len(items)})")
        for g, fdr, lfc in items[:15]:
            mark = " ★" if g in expected_int else ""
            print(f"    {g:<15} FDR={fdr:.3g}  LFC={lfc:+.3f}{mark}")
    # Specifically: report whether the 7 named genes are recovered in any 2 Gy interaction comparison
    union_sig = {g for items in int_sig.values() for g, _, _ in items}
    recovered = expected_int & union_sig
    missing = expected_int - union_sig
    print(f"\n  Paper's 7 named genes: recovered={sorted(recovered)} | missing={sorted(missing)}")

    # === R8. Pathway enrichment: HALLMARK_P53_PATHWAY over-representation ===
    print("\n=== R8 verification: HALLMARK_P53_PATHWAY enrichment in DEGs ===")
    # Use Fisher's exact (right-tailed) using the gene -> geneset annotations in the table itself.
    # Universe = all genes tested for that (group, dose, model). Background = those with HALLMARK_P53_PATHWAY in 'In Geneset'.
    from math import lgamma

    def log_factorial(n):
        return lgamma(n + 1)

    def log_choose(n, k):
        if k < 0 or k > n:
            return float("-inf")
        return log_factorial(n) - log_factorial(k) - log_factorial(n - k)

    def fisher_right(a, b, c, d):
        # Right-tailed (over-representation) p-value via hypergeometric tail
        # 2x2 table: a in_path & sig, b in_path & not sig, c not_path & sig, d not_path & not sig
        n = a + b + c + d
        r1 = a + b  # row1 total: in path
        c1 = a + c  # col1 total: sig
        # Sum P(X >= a) where X ~ Hypergeometric(N=n, K=r1, n=c1)
        # max a = min(r1, c1)
        log_denom = log_choose(n, c1)
        p = 0.0
        for x in range(a, min(r1, c1) + 1):
            log_num = log_choose(r1, x) + log_choose(n - r1, c1 - x)
            p += math.exp(log_num - log_denom)
        return p

    PATHWAYS = ["HALLMARK_P53_PATHWAY", "KEGG_P53_SIGNALING_PATHWAY",
                "HALLMARK_E2F_TARGETS", "REACTOME_P53_DEPENDENT_G1_DNA_DAMAGE_RESPONSE",
                "REACTOME_CELL_CYCLE", "KEGG_CELL_CYCLE", "REACTOME_DNA_REPAIR",
                "HALLMARK_DNA_REPAIR"]

    pw_rows = []
    for combo in sorted({(r["Group"], r["Dose"], r["Model"]) for r in degs}):
        subset = [r for r in degs if (r["Group"], r["Dose"], r["Model"]) == combo]
        n_total = len(subset)
        sig_genes = {r["Gene"] for r in subset if r["FDR"] < FDR_THRESH}
        n_sig = len(sig_genes)
        if n_sig == 0:
            continue
        for pw in PATHWAYS:
            in_path = {r["Gene"] for r in subset if r.get("In Geneset") and pw in r["In Geneset"]}
            a = len(sig_genes & in_path)
            b = len(in_path - sig_genes)
            c = n_sig - a
            d = n_total - n_sig - b
            if a == 0 or len(in_path) == 0:
                continue
            p = fisher_right(a, b, c, d)
            expected = (n_sig / n_total) * len(in_path)
            fold = a / expected if expected > 0 else float("inf")
            pw_rows.append({
                "Group": combo[0], "Dose": combo[1], "Model": combo[2],
                "Pathway": pw, "Path_size": len(in_path),
                "DEG_in_path": a, "Expected": round(expected, 2),
                "FoldEnrich": round(fold, 2), "Fisher_p": p
            })
    pw_rows.sort(key=lambda r: (r["Dose"], r["Group"], r["Model"], r["Fisher_p"]))
    with open(RESULTS / "pathway_enrichment.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t",
                           fieldnames=["Group", "Dose", "Model", "Pathway", "Path_size",
                                       "DEG_in_path", "Expected", "FoldEnrich", "Fisher_p"])
        w.writeheader()
        for row in pw_rows:
            w.writerow(row)

    # Print headline result: HALLMARK_P53_PATHWAY in each combo
    print("\nHALLMARK_P53_PATHWAY enrichment (right-tailed Fisher, our own re-run):")
    print(f"  {'Group':<6} {'Dose':<8} {'Model':<10} {'a/K':>10} {'Fold':>6} {'p':>11}")
    for row in pw_rows:
        if row["Pathway"] == "HALLMARK_P53_PATHWAY":
            print(f"  {row['Group']:<6} {row['Dose']:<8} {row['Model']:<10} "
                  f"{row['DEG_in_path']}/{row['Path_size']:<7} "
                  f"{row['FoldEnrich']:>6.2f}x {row['Fisher_p']:>11.3g}")

    print("\nKEGG_P53_SIGNALING_PATHWAY:")
    for row in pw_rows:
        if row["Pathway"] == "KEGG_P53_SIGNALING_PATHWAY":
            print(f"  {row['Group']:<6} {row['Dose']:<8} {row['Model']:<10} "
                  f"{row['DEG_in_path']}/{row['Path_size']:<7} "
                  f"{row['FoldEnrich']:>6.2f}x {row['Fisher_p']:>11.3g}")

    # Save key numbers JSON for the report
    summary = {
        "deg_counts": deg_table,
        "interaction_2Gy_FDR05": {
            comp: [{"gene": g, "fdr": fdr, "lfc": lfc} for g, fdr, lfc in items]
            for comp, items in int_sig.items()
        },
        "interaction_paper_named_genes_recovered": sorted(recovered),
        "interaction_paper_named_genes_missing": sorted(missing),
    }
    with open(RESULTS / "replication_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nWrote {RESULTS/'deg_counts.tsv'}, {RESULTS/'pathway_enrichment.tsv'}, {RESULTS/'replication_summary.json'}")


if __name__ == "__main__":
    main()
