#!/usr/bin/env python3
"""
Pathway enrichment of our HD/LD DEG lists via Enrichr (Liu et al. 2023 Fig 1C/D, 4C).

The paper reports p53 signaling and apoptosis/DNA-damage-response enrichment as
the headline pathway calls. We check whether our independently-derived HD and LD
DEG lists hit the same KEGG / GO terms.

Writes results/pathways_HD.tsv, results/pathways_LD.tsv,
       results/pathways_summary.json.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT / "results"

try:
    import gseapy as gp
except Exception as e:
    print(f"gseapy unavailable: {e}", file=sys.stderr)
    sys.exit(2)

HD = pd.read_csv(OUT / "full_lme_HD_DEGs.tsv", sep="\t")["gene"].dropna().tolist()
LD = pd.read_csv(OUT / "full_lme_LD_DEGs.tsv", sep="\t")["gene"].dropna().tolist()

LIBRARIES = [
    "KEGG_2021_Human",
    "GO_Biological_Process_2023",
    "WikiPathway_2023_Human",
]

def run(genes, label):
    print(f"\n== {label}: {len(genes)} genes -> Enrichr", flush=True)
    enr = gp.enrichr(gene_list=genes,
                     gene_sets=LIBRARIES,
                     organism="human",
                     outdir=None,
                     cutoff=0.05)
    r = enr.results
    r["label"] = label
    r.to_csv(OUT / f"pathways_{label}.tsv", sep="\t", index=False)
    # Top hits per library
    out = {}
    for lib in LIBRARIES:
        sub = r[r["Gene_set"] == lib].sort_values("Adjusted P-value").head(10)
        out[lib] = sub[["Term","P-value","Adjusted P-value","Odds Ratio","Genes"]].to_dict(orient="records")
    return out

summary = {}
summary["HD"] = run(HD, "HD")
summary["LD"] = run(LD, "LD")

(OUT / "pathways_summary.json").write_text(json.dumps(summary, indent=2, default=str))

# Print a compact top-5 view per side
for side in ("HD","LD"):
    print(f"\n=== {side} top pathways ===")
    for lib in LIBRARIES:
        print(f"--- {lib}")
        for row in summary[side][lib][:5]:
            term = row["Term"]; padj = row["Adjusted P-value"]
            print(f"  q={padj:.2e}  {term}")
