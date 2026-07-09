#!/usr/bin/env python3
"""
Pathway over-representation, using the largest 2 Gy combo (most DEGs)
as a *proxy* background for "all expressed genes". This is imperfect
because Additional File 1a only stores the union of significant DEGs
across at least one combo (the table holds the genes that have an FDR
value the authors chose to publish). For a rigorous Fisher test we
would need the full 14,756-gene universe with their geneset annotations.

Strategy:
  - Background = the union of every gene that appears anywhere in AF1a
    (this is a *superset* of DEGs and a *subset* of the 14,756 detected
    genes -> resulting p-values are CONSERVATIVE upper bounds on
    significance).
  - Foreground = DEGs at FDR<0.05 for the (group, dose, model) combo.
  - Pathway membership = the 'In Geneset' column.

We report (a) fold enrichment, (b) right-tailed Fisher p-value, and
(c) the absolute pathway hit count vs. its membership in the background.
"""

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from math import lgamma

PROJECT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT / "results"
DEG_FILE = PROJECT / "data" / "AF1a_degs.tsv"
FDR_THRESH = 0.05


def log_factorial(n):
    return lgamma(n + 1)


def log_choose(n, k):
    if k < 0 or k > n:
        return float("-inf")
    return log_factorial(n) - log_factorial(k) - log_factorial(n - k)


def fisher_right(a, b, c, d):
    n = a + b + c + d
    r1 = a + b
    c1 = a + c
    log_denom = log_choose(n, c1)
    p = 0.0
    for x in range(a, min(r1, c1) + 1):
        log_num = log_choose(r1, x) + log_choose(n - r1, c1 - x)
        p += math.exp(log_num - log_denom)
    return min(p, 1.0)


def main():
    rows = []
    with open(DEG_FILE) as f:
        rdr = csv.DictReader(f, delimiter="\t")
        for r in rdr:
            try:
                r["FDR"] = float(r["FDR"])
                r["log2FC"] = float(r["log2FC"])
            except (ValueError, TypeError):
                continue
            rows.append(r)

    # Build background: union of all genes anywhere in AF1a (gene -> "In Geneset")
    gene_to_path = {}
    for r in rows:
        if r["Gene"] not in gene_to_path:
            gs = r.get("In Geneset") or ""
            gene_to_path[r["Gene"]] = set() if (gs in ("", "NA")) else set(p.strip() for p in gs.split("|") if p.strip())
        else:
            # Some genes may be annotated in another row with paths; union them
            gs = r.get("In Geneset") or ""
            if gs not in ("", "NA"):
                for p in gs.split("|"):
                    p = p.strip()
                    if p:
                        gene_to_path[r["Gene"]].add(p)

    background_genes = set(gene_to_path.keys())
    print(f"Background gene universe (union across all combos in AF1a) = {len(background_genes):,}")
    print(f"  (Paper reports 14,756 total detected; AF1a only stores rows the authors output, "
          "so this is a subset and Fisher p-values are conservative.)")

    PATHWAYS = [
        "HALLMARK_P53_PATHWAY",
        "KEGG_P53_SIGNALING_PATHWAY",
        "REACTOME_P53_DEPENDENT_G1_DNA_DAMAGE_RESPONSE",
        "HALLMARK_E2F_TARGETS",
        "REACTOME_CELL_CYCLE",
        "KEGG_CELL_CYCLE",
        "REACTOME_DNA_REPAIR",
        "HALLMARK_DNA_REPAIR",
        "HALLMARK_APOPTOSIS",
        "KEGG_APOPTOSIS",
        "REACTOME_APOPTOSIS",
        "HALLMARK_MTORC1_SIGNALING",
        "HALLMARK_HYPOXIA",
    ]
    path_to_genes = {pw: {g for g, ps in gene_to_path.items() if pw in ps} for pw in PATHWAYS}
    print("\nPathway membership in background:")
    for pw, gs in path_to_genes.items():
        print(f"  {pw:<55} {len(gs):>5}")

    # For each (group, dose, model), compute fold enrichment + Fisher right-tail p
    combos = sorted({(r["Group"], r["Dose"], r["Model"]) for r in rows})
    out_rows = []
    for combo in combos:
        sig_genes = {r["Gene"] for r in rows if (r["Group"], r["Dose"], r["Model"]) == combo and r["FDR"] < FDR_THRESH}
        n_sig = len(sig_genes)
        N = len(background_genes)
        if n_sig == 0:
            continue
        for pw in PATHWAYS:
            K = len(path_to_genes[pw])
            if K == 0:
                continue
            a = len(sig_genes & path_to_genes[pw])
            b = K - a
            c = n_sig - a
            d = N - n_sig - b
            expected = K * n_sig / N
            fold = a / expected if expected > 0 else float("inf")
            p = fisher_right(a, b, c, d)
            out_rows.append({
                "Group": combo[0], "Dose": combo[1], "Model": combo[2],
                "Pathway": pw, "K_in_bg": K, "n_DEG": n_sig,
                "a_hits": a, "expected": round(expected, 2),
                "fold": round(fold, 2), "p_right_fisher": p,
            })

    out_rows.sort(key=lambda r: (r["Dose"], r["Group"], r["Model"], r["p_right_fisher"]))
    with open(RESULTS / "pathway_enrichment_bg.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t",
                           fieldnames=["Group", "Dose", "Model", "Pathway",
                                       "K_in_bg", "n_DEG", "a_hits",
                                       "expected", "fold", "p_right_fisher"])
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print("\n=== Headline: HALLMARK_P53_PATHWAY enrichment per combo (model 1) ===")
    print(f"  {'Group':<5} {'Dose':<8}   a/K       fold  p")
    for r in out_rows:
        if r["Pathway"] == "HALLMARK_P53_PATHWAY" and r["Model"] == "model 1":
            print(f"  {r['Group']:<5} {r['Dose']:<8} {r['a_hits']:>3}/{r['K_in_bg']:<4} "
                  f"{r['fold']:>6.2f}x  {r['p_right_fisher']:.3g}")

    print("\n=== HALLMARK_E2F_TARGETS enrichment (paper claims E2F1 upstream regulator after HDIR in N1,N2+) ===")
    print(f"  {'Group':<5} {'Dose':<8}   a/K       fold  p")
    for r in out_rows:
        if r["Pathway"] == "HALLMARK_E2F_TARGETS" and r["Model"] == "model 1":
            print(f"  {r['Group']:<5} {r['Dose']:<8} {r['a_hits']:>3}/{r['K_in_bg']:<4} "
                  f"{r['fold']:>6.2f}x  {r['p_right_fisher']:.3g}")

    print("\n=== HALLMARK_DNA_REPAIR / REACTOME_DNA_REPAIR (paper: DNA-repair as downstream in N0 only at LDIR) ===")
    for r in out_rows:
        if r["Pathway"] in ("HALLMARK_DNA_REPAIR", "REACTOME_DNA_REPAIR") and r["Model"] == "model 1" and r["Dose"] == "0.05 Gy":
            print(f"  {r['Group']:<5} {r['Pathway']:<20} {r['a_hits']:>3}/{r['K_in_bg']:<4} "
                  f"{r['fold']:>6.2f}x  {r['p_right_fisher']:.3g}")

    # Print top 8 pathways per (dose, model 1) ranked by Fisher p
    print("\n=== Top-5 enriched pathways per (group, dose) at model 1 ===")
    sorted_out = sorted([r for r in out_rows if r["Model"] == "model 1"],
                        key=lambda r: (r["Dose"], r["Group"], r["p_right_fisher"]))
    last_key = None
    n = 0
    for r in sorted_out:
        k = (r["Dose"], r["Group"])
        if k != last_key:
            print(f"\n  [{r['Dose']} | {r['Group']}]")
            last_key = k
            n = 0
        if n < 5:
            print(f"    {r['Pathway']:<55} a/K={r['a_hits']}/{r['K_in_bg']} "
                  f"fold={r['fold']:.2f}x  p={r['p_right_fisher']:.2g}")
            n += 1


if __name__ == "__main__":
    main()
