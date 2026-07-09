#!/usr/bin/env python3
"""
Over-representation analysis (ORA) of DEGs from the d5_vs_control (full ~batch+group)
contrast against zebrafish GO Biological Process annotation via Ensembl BioMart REST.

Paper claims (Cantabella 2022):
  - visual perception (GO:0007601): fdr < 1e-22 at D05, < 1e-17 at D5
  - regulation of G protein-coupled receptor signaling (GO:0008277): fdr < 1e-8
  - serotonin metabolic process (GO:0042428): fdr = 0.002 / 0.03
"""
import json, math, sys, time, urllib.request, urllib.parse
from collections import defaultdict
from pathlib import Path
import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

LFC = math.log2(1.5)

CONTRASTS = {
    "d005_full_batchgroup": 0.05,
    "d05_full_batchgroup":  0.50,
    "d5_full_batchgroup":   5.00,
    # also the per-batch d5
    "d5_vs_control":        5.00,
    "d05_pooled_nobatch":   0.50,
}

def fetch_go_annotations_biomart():
    """Fetch zebrafish GO BP annotation via BioMart XML query.

    Returns dict {ensg_id: set(go_id, ...)} and a label dict {go_id: name}.
    """
    cache = RESULTS / "go_bp_drerio.tsv.gz"
    if cache.exists():
        df = pd.read_csv(cache, sep="\t")
        print(f"Loaded cached GO annotation: {len(df):,} rows")
    else:
        # BioMart REST endpoint
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "1" count = "" datasetConfigVersion = "0.6" >
    <Dataset name = "drerio_gene_ensembl" interface = "default" >
        <Filter name = "go_parent_term" value = "GO:0008150"/>
        <Attribute name = "ensembl_gene_id" />
        <Attribute name = "go_id" />
        <Attribute name = "name_1006" />
        <Attribute name = "namespace_1003" />
    </Dataset>
</Query>"""
        url = "https://www.ensembl.org/biomart/martservice?query=" + urllib.parse.quote(xml)
        print(f"Fetching GO annotation from Ensembl BioMart...")
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (replication study)"})
        with urllib.request.urlopen(req, timeout=180) as fh:
            text = fh.read().decode("utf-8")
        rows = [l.split("\t") for l in text.strip().split("\n") if l.strip()]
        df = pd.DataFrame(rows, columns=["ensembl_gene_id","go_id","go_name","namespace"])
        df = df[(df["namespace"]=="biological_process") & df["go_id"].str.startswith("GO:")]
        df.to_csv(cache, sep="\t", index=False, compression="gzip")
        print(f"Cached {len(df):,} BP annotations to {cache}")
    g2t = defaultdict(set)
    t2n = {}
    for _, r in df.iterrows():
        g2t[r["ensembl_gene_id"]].add(r["go_id"])
        t2n[r["go_id"]] = r["go_name"]
    return g2t, t2n

def ora(deg_set, universe, gene2term, term2name, min_term=5, max_term=2000):
    """Right-tailed Fisher exact test for each GO term."""
    deg_set = deg_set & universe
    term2genes = defaultdict(set)
    for g in universe:
        for t in gene2term.get(g, ()):
            term2genes[t].add(g)
    M = len(universe)
    n = len(deg_set)
    rows = []
    for t, genes in term2genes.items():
        K = len(genes)
        if K < min_term or K > max_term:
            continue
        k = len(genes & deg_set)
        if k == 0:
            continue
        # Fisher 2x2: [k, n-k; K-k, M-n-K+k]
        a = k; b = n - k; c = K - k; d = M - n - K + k
        if min(b, c, d) < 0:
            continue
        odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
        rows.append({
            "go_id": t, "go_name": term2name.get(t, ""),
            "k": k, "K": K, "n_deg": n, "M_universe": M,
            "odds_ratio": odds, "p": p,
            "gene_ratio": k/n if n else 0,
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["padj"] = multipletests(df["p"], method="fdr_bh")[1]
    df = df.sort_values("p")
    return df

def main():
    g2t, t2n = fetch_go_annotations_biomart()
    universe_template = None
    for label, dose in CONTRASTS.items():
        f = RESULTS / f"deseq2_{label}.tsv.gz"
        if not f.exists():
            print(f"Skipping {label}: not found")
            continue
        df = pd.read_csv(f, sep="\t")
        universe = set(df["gene_id"])
        sig = df[(df["padj"].fillna(1) < 0.05) & (df["log2FoldChange"].abs() >= LFC)]
        deg_set = set(sig["gene_id"])
        print(f"\n=== ORA: {label}  (dose={dose} mGy/h, |DEG|={len(deg_set)}, universe={len(universe)}) ===")
        if len(deg_set) < 3:
            print("  Too few DEGs for meaningful ORA.")
            continue
        ora_df = ora(deg_set, universe, g2t, t2n)
        if ora_df.empty:
            print("  No enriched terms.")
            continue
        out = RESULTS / f"ora_{label}.tsv"
        ora_df.to_csv(out, sep="\t", index=False)
        print(f"  Top 10 enriched GO BP terms (by p):")
        print(ora_df[["go_id","go_name","k","K","odds_ratio","p","padj","gene_ratio"]].head(10).to_string(index=False))
        # Specifically look for the paper's flagged terms
        for goid in ["GO:0007601","GO:0008277","GO:0042428"]:
            hit = ora_df[ora_df["go_id"]==goid]
            if not hit.empty:
                r = hit.iloc[0]
                print(f"  *** paper-flagged {goid} {t2n.get(goid,'')}: k={r['k']} K={r['K']} OR={r['odds_ratio']:.2f} p={r['p']:.3g} padj={r['padj']:.3g}")
            else:
                print(f"  *** paper-flagged {goid} not enriched in our hits")

if __name__ == "__main__":
    main()
