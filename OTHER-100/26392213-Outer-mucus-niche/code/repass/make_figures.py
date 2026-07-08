#!/usr/bin/env python3
"""Generate re-pass figures: PCoA on weighted UniFrac + Shannon boxplots."""
import os, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import skbio
from skbio import TreeNode
from skbio.diversity import beta_diversity
from skbio.stats.ordination import pcoa

BASE = Path(os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/26392213-Outer-mucus-niche"))
RES = BASE / "results" / "repass"
WORK = RES / "work"

for ds in ['SPF', 'sDMDMm2']:
    rare = pd.read_csv(RES / f"{ds}_otu_rarefied.csv.gz", index_col=0)
    meta = pd.read_csv(RES / f"{ds}_meta_repass.csv", index_col=0)
    tree = TreeNode.read(str(WORK / f"{ds}_otus.nwk"), convert_underscores=False)
    tree_taxa = {n.name for n in tree.tips() if n.name}
    cols = [c for c in rare.columns if c in tree_taxa]
    rare = rare[cols]
    rare = rare.loc[rare.sum(axis=1) > 0]
    ids = [str(s) for s in rare.index]
    otu_ids = [str(c) for c in rare.columns]
    dm = beta_diversity('weighted_unifrac', rare.values, ids=ids,
                        taxa=otu_ids, tree=tree, validate=False)
    pc = pcoa(dm, number_of_dimensions=2)
    pcs = pc.samples
    pcs['Compartment'] = meta.loc[pcs.index, 'Compartment']
    pcs['Location'] = meta.loc[pcs.index, 'Location']

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, color_by in zip(axes, ['Compartment', 'Location']):
        for grp in sorted(pcs[color_by].unique()):
            sub = pcs[pcs[color_by] == grp]
            ax.scatter(sub['PC1'], sub['PC2'], label=grp, s=60, alpha=0.75,
                       edgecolor='black', linewidth=0.4)
        ev = pc.proportion_explained
        ax.set_xlabel(f"PC1 ({ev[0]*100:.1f}%)")
        ax.set_ylabel(f"PC2 ({ev[1]*100:.1f}%)")
        ax.set_title(f"{ds}: PCoA on weighted UniFrac, colored by {color_by}")
        ax.legend(fontsize=8, loc='best')
        ax.grid(alpha=0.3)
    plt.tight_layout()
    out = RES / f"{ds}_PCoA_wUniFrac_repass.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"wrote {out}")

# Shannon comparison
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
ln2 = np.log(2)
for ax, ds, paper_mean, paper_sd in zip(axes,
        ['SPF', 'sDMDMm2'], [8.22, 1.98], [0.88, 0.38]):
    df = pd.read_csv(RES / f"{ds}_alpha_repass.csv")
    df['shannon_log2'] = df['shannon'] / ln2
    groups = ['Outer Mucus', 'Luminal Content']
    data = [df[df.Compartment == g].shannon_log2.values for g in groups]
    bp = ax.boxplot(data, labels=groups, patch_artist=True, widths=0.5)
    for patch, color in zip(bp['boxes'], ['#4daf4a', '#377eb8']):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    # overlay paper value (colon content only)
    cc = df[(df.Compartment == 'Luminal Content') & (df.Location == 'Colon')]
    ax.axhline(paper_mean, color='red', linestyle='--', alpha=0.7,
               label=f"paper: {paper_mean}±{paper_sd} (colon content)")
    ax.set_ylabel('Shannon diversity (log2)')
    ax.set_title(f"{ds}: alpha diversity by compartment")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
plt.tight_layout()
out = RES / "shannon_compartment_repass.png"
plt.savefig(out, dpi=130)
plt.close()
print(f"wrote {out}")

print("done")
