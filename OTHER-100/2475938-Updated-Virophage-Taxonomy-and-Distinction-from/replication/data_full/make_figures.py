#!/usr/bin/env python3
"""Generate full-scale heatmap and tree figures for virophage replication."""
import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import Phylo

os.chdir(os.path.dirname(__file__))

# ------------- Heatmap of marker scores across all genomes -------------
df = pd.read_csv("hmm_summary_full.tsv", sep="\t")
print(f"Loaded {len(df)} genomes")

# Sort: by classification then by total marker score
score_cols = ["MCP","ATPase","PRO","Penton","PLV"]
df["total_marker"] = df[["MCP","ATPase","PRO","Penton"]].sum(axis=1)
order = {"VIROPHAGE":0,"Virophage_partial":1,"PLV":2,"Other/unclassified":3}
df["_o"] = df["classification"].map(order).fillna(4)
df = df.sort_values(["_o","total_marker"], ascending=[True,False]).reset_index(drop=True)

# Heatmap: log10(score+1)
mat = np.log10(df[score_cols].values + 1.0)

fig_h = max(8, len(df)*0.10)
fig, ax = plt.subplots(figsize=(8, fig_h))
sns.heatmap(mat, ax=ax, cmap="viridis",
            xticklabels=score_cols,
            yticklabels=False,
            cbar_kws={"label":"log10(HMM bit-score + 1)"})

# Add classification color strip on the left
class_colors = {"VIROPHAGE":"#2ca02c","Virophage_partial":"#98df8a",
                "PLV":"#1f77b4","Other/unclassified":"#aaaaaa"}
import matplotlib.patches as mpatches
for i, cls in enumerate(df["classification"]):
    ax.add_patch(mpatches.Rectangle((-0.4,i),0.4,1,
                 color=class_colors.get(cls,"#aaa"),clip_on=False))
ax.set_xlim(-0.5, mat.shape[1])
ax.set_title(f"HMM marker scan — {len(df)} virophage/PLV candidate genomes (full-scale)")
# Legend
patches = [mpatches.Patch(color=v, label=k) for k,v in class_colors.items()]
ax.legend(handles=patches, loc="upper left", bbox_to_anchor=(1.15,1.0))
plt.tight_layout()
plt.savefig("hmm_heatmap_full.png", dpi=150, bbox_inches="tight")
plt.savefig("hmm_heatmap_full.pdf", bbox_inches="tight")
plt.close()
print("wrote hmm_heatmap_full.{png,pdf}")

# ------------- Phylogenetic tree of 70-genome 4-marker concat -------------
tree_path = "markers_full/concat.treefile"
tree = Phylo.read(tree_path, "newick")

# Midpoint root
tree.root_at_midpoint()

# Color leaves by classification
cls_lookup = dict(zip(df.accession, df.classification))
title_lookup = dict(zip(df.accession, df.title))

# Tally clades for results json
n_in_tree = sum(1 for _ in tree.get_terminals())
print(f"Tree has {n_in_tree} terminals")

fig, ax = plt.subplots(figsize=(11, max(12, n_in_tree*0.18)))
def label_func(c):
    if not c.name: return ""
    cls = cls_lookup.get(c.name,"?")
    title = title_lookup.get(c.name,"")[:48]
    return f"{c.name}  [{cls}]  {title}"

Phylo.draw(tree, axes=ax, do_show=False, label_func=label_func,
           branch_labels=lambda c: "")
ax.set_title(f"Virophage 4-marker concatenated phylogeny ({n_in_tree} genomes)\nMCP+ATPase+PRO+Penton, IQ-TREE LG+G, 1000 UFBoot")
plt.tight_layout()
plt.savefig("phylogeny_4markers_full.png", dpi=150, bbox_inches="tight")
plt.savefig("phylogeny_4markers_full.pdf", bbox_inches="tight")
plt.close()
print("wrote phylogeny_4markers_full.{png,pdf}")

# ------------- results_full.json -------------
results = {
    "scale": {
        "genomes_scanned": int(len(df)),
        "input_source": "NCBI nuccore (Lavidaviridae + virophage + Polinton-like + Adintovirus + Maviricidae) length 5–100 kb",
        "search_terms": ["Lavidaviridae[Organism]", "virophage[All]", "Polinton-like virus",
                         "Adintovirus", "Maviricidae", "Mininucleoviridae"],
        "filter": "5kb ≤ length ≤ 100kb",
        "predicted_proteins": 4676,
    },
    "classification_counts": {
        k: int(v) for k,v in df.classification.value_counts().items()
    },
    "marker_presence": {
        "MCP": int((df.MCP>0).sum()),
        "ATPase": int((df.ATPase>0).sum()),
        "PRO": int((df.PRO>0).sum()),
        "Penton": int((df.Penton>0).sum()),
        "PLV_PC_054": int((df.PLV>0).sum()),
        "all_4_markers": int(((df[["MCP","ATPase","PRO","Penton"]]>0).all(axis=1)).sum()),
    },
    "phylogeny": {
        "method": "IQ-TREE 2 partitioned (per-marker LG+G), 1000 UFBoot + 1000 SH-aLRT",
        "n_taxa": int(n_in_tree),
        "n_partitions": 4,
        "concat_length_aa": 1403,
        "tree_file": "markers_full/concat.treefile",
    },
    "members_by_clade_heuristic": {},
}

# Quick clade partition: find subtrees enriched for each class (heuristic)
# For each terminal, store classification
results["members_by_clade_heuristic"]["VIROPHAGE_in_tree"] = sorted(
    [t.name for t in tree.get_terminals() if cls_lookup.get(t.name)=="VIROPHAGE"])
results["members_by_clade_heuristic"]["PLV_in_tree"] = sorted(
    [t.name for t in tree.get_terminals() if cls_lookup.get(t.name)=="PLV"])
results["members_by_clade_heuristic"]["Other_in_tree"] = sorted(
    [t.name for t in tree.get_terminals()
     if cls_lookup.get(t.name) not in ("VIROPHAGE","PLV")])

with open("results_full.json","w") as f:
    json.dump(results, f, indent=2)
print("wrote results_full.json")
print(json.dumps(results["classification_counts"], indent=2))
print(json.dumps(results["marker_presence"], indent=2))
