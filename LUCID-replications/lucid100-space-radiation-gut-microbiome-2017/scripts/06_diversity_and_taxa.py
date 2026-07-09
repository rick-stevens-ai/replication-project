#!/usr/bin/env python3
"""Compute alpha diversity, beta diversity (PCoA + PERMANOVA), per-group taxa
abundance, and Akkermansia/Bacteroidetes/Firmicutes summaries that the paper
makes specific claims about.

Outputs go to ../results/.
"""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import skbio
from skbio.stats.distance import permanova, DistanceMatrix
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.ordination import pcoa

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
RES  = ROOT / "results"
RES.mkdir(exist_ok=True)

# --- Load OTU table (samples in cols, OTUs in rows) ---
otu = pd.read_csv(WORK/"otu_table.tsv", sep="\t", index_col=0)
otu.index.name = "OTU"
print(f"OTU table: {otu.shape[0]} OTUs x {otu.shape[1]} samples")
# Transpose: samples x OTUs (skbio convention)
X = otu.T.astype(int)

# --- Load metadata ---
meta = pd.read_csv(ROOT/"data/sample_metadata.tsv", sep="\t").set_index("run")
meta = meta.loc[meta.index.intersection(X.index)]
X = X.loc[meta.index]
print(f"Samples with metadata: {len(meta)}")
print(meta.groupby(["dose_Gy","timepoint_day"]).size().to_string())

# --- Load taxonomy ---
tax = pd.read_csv(WORK/"otu_tax.tsv", sep="\t")
# Strip ';size=...' suffix on OTU id so it matches otu_table.tsv
tax["qid"] = tax["qid"].str.split(";").str[0]
tax = tax.drop_duplicates("qid").set_index("qid")
tax = tax.reindex(otu.index)
tax["taxonomy"] = tax["taxonomy"].fillna("Unassigned")
# Parse rank columns
def split_tax(t):
    parts = t.rstrip(";").split(";") if isinstance(t,str) else []
    parts += [""]*(7-len(parts))
    return parts[:7]
tax[["domain","phylum","class","order","family","genus","species"]] = \
    tax["taxonomy"].apply(lambda t: pd.Series(split_tax(t)))

# --- Rarefaction to 30,000 reads/sample (paper used 60k; we use 30k to keep more samples) ---
TARGET_DEPTH = 30000
depths = X.sum(axis=1)
print(f"Read depths per sample:  min={depths.min()}, median={int(depths.median())}, max={depths.max()}")
keep = depths[depths >= TARGET_DEPTH].index
print(f"Samples passing rarefaction depth {TARGET_DEPTH}: {len(keep)} of {len(X)}")

rng = np.random.default_rng(2026)
def rarefy_one(row, depth):
    counts = row.values.astype(int)
    total = counts.sum()
    if total < depth:
        return None
    # subsample without replacement
    flat = np.repeat(np.arange(len(counts)), counts)
    pick = rng.choice(flat, depth, replace=False)
    out = np.bincount(pick, minlength=len(counts))
    return out

rar = pd.DataFrame(
    {s: rarefy_one(X.loc[s], TARGET_DEPTH) for s in keep},
    index=X.columns,
).T  # samples x OTUs
rar = rar.loc[:, rar.sum(0) > 0]   # drop empty OTUs
print(f"Rarefied table: {rar.shape}")

meta_r = meta.loc[rar.index].copy()

# ===== ALPHA DIVERSITY =====
print("\n== Alpha diversity ==")
alpha_methods = ["observed_otus", "shannon", "faith_pd"]
alpha = {}
alpha["observed_otus"] = alpha_diversity("observed_otus", rar.values, ids=rar.index)
alpha["shannon"]       = alpha_diversity("shannon",       rar.values, ids=rar.index)
adf = pd.DataFrame(alpha)
adf = adf.join(meta_r[["dose_Gy","timepoint_day","group"]])
adf.to_csv(RES/"alpha_diversity.tsv", sep="\t")

# Per-group means
ag = adf.groupby(["dose_Gy","timepoint_day"])[["observed_otus","shannon"]].agg(["mean","std","count"])
ag.to_csv(RES/"alpha_diversity_by_group.tsv", sep="\t")
print(ag.to_string())

# Nonparametric Kruskal-Wallis across dose within each timepoint
kw_results = []
for tp in sorted(meta_r["timepoint_day"].unique()):
    sub = adf[adf["timepoint_day"]==tp]
    groups = [sub[sub["dose_Gy"]==d]["shannon"].values for d in sorted(sub["dose_Gy"].unique())]
    if all(len(g)>1 for g in groups):
        H, p = stats.kruskal(*groups)
        kw_results.append({"timepoint":tp, "metric":"shannon", "H":H, "p":p})

# 10d vs 30d at 0.1 Gy (paper claim: significant increase in PD at 30d for 0.1 Gy)
sub01 = adf[adf["dose_Gy"]==0.1]
if len(sub01)>0:
    g10 = sub01[sub01["timepoint_day"]==10]["shannon"].values
    g30 = sub01[sub01["timepoint_day"]==30]["shannon"].values
    if len(g10)>1 and len(g30)>1:
        U, p = stats.mannwhitneyu(g10, g30, alternative="two-sided")
        kw_results.append({"timepoint":"0.1Gy_10vs30","metric":"shannon","H":U,"p":p})

pd.DataFrame(kw_results).to_csv(RES/"alpha_diversity_tests.tsv", sep="\t", index=False)
print("\nAlpha diversity tests:")
print(pd.DataFrame(kw_results).to_string())

# ===== BETA DIVERSITY =====
print("\n== Beta diversity (Bray-Curtis, unweighted Jaccard) ==")
rar_norm = rar.div(rar.sum(1), axis=0)  # relative abundance
bc = beta_diversity("braycurtis", rar.values, ids=rar.index)
jac = beta_diversity("jaccard", (rar.values>0).astype(int), ids=rar.index)
bc.write(str(RES/"beta_braycurtis.dm"))
jac.write(str(RES/"beta_jaccard.dm"))

# PERMANOVA: dose-specific (treat as categorical) and time, recapitulating paper's
# ANOSIM/PERMANOVA on UniFrac (we don't have a tree, so use Bray-Curtis as proxy)
perm_results = []
for var in ["dose_Gy","timepoint_day"]:
    grp = meta_r[var].astype(str).values
    for metric_name, dm in [("braycurtis",bc),("jaccard",jac)]:
        try:
            res = permanova(dm, grp, permutations=999)
            perm_results.append({
                "metric": metric_name, "variable": var,
                "F": res["test statistic"], "p": res["p-value"],
                "n_groups": len(set(grp)), "n_samples": len(grp),
            })
        except Exception as e:
            perm_results.append({"metric":metric_name,"variable":var,"error":str(e)})

# pairwise irradiated vs control PERMANOVA at each timepoint and dose
for tp in sorted(meta_r["timepoint_day"].unique()):
    sub_meta = meta_r[meta_r["timepoint_day"]==tp]
    sub_ids = sub_meta.index.tolist()
    for d in [0.1, 0.25, 1.0]:
        ids_pair = sub_meta[(sub_meta["dose_Gy"]==0) | (sub_meta["dose_Gy"]==d)].index.tolist()
        if len(ids_pair) < 6:
            continue
        grp = sub_meta.loc[ids_pair, "dose_Gy"].apply(lambda x: "ctrl" if x==0 else "irrad").values
        dm_sub = bc.filter(ids_pair)
        try:
            res = permanova(dm_sub, grp, permutations=999)
            perm_results.append({
                "metric":"braycurtis", "variable":f"day{tp}_0_vs_{d}Gy",
                "F":res["test statistic"], "p":res["p-value"], "n_samples":len(grp),
            })
        except Exception as e:
            pass

pd.DataFrame(perm_results).to_csv(RES/"beta_permanova.tsv", sep="\t", index=False)
print(pd.DataFrame(perm_results).to_string())

# PCoA
pc = pcoa(bc)
coords = pc.samples.iloc[:, :3].copy()
coords.columns = ["PC1","PC2","PC3"]
coords = coords.join(meta_r[["dose_Gy","timepoint_day","group"]])
coords["explained_var_pc1"] = pc.proportion_explained.iloc[0]
coords["explained_var_pc2"] = pc.proportion_explained.iloc[1]
coords["explained_var_pc3"] = pc.proportion_explained.iloc[2]
coords.to_csv(RES/"pcoa_braycurtis.tsv", sep="\t")
print(f"\nPCoA explained variance (PC1-3): {pc.proportion_explained.iloc[:3].values}")

# ===== TAXONOMY ROLLUP =====
print("\n== Taxonomy rollup ==")
# Build relative abundance per phylum / family / genus per sample, then per group
rel = rar.div(rar.sum(1), axis=0)
tax_for_rar = tax.loc[rar.columns]

def collapse(level):
    df = rel.T.copy()
    df["taxon"] = tax_for_rar[level].fillna("").replace("", "Unassigned").values
    out = df.groupby("taxon").sum().T
    return out

phylum_rel = collapse("phylum")
family_rel = collapse("family")
genus_rel = collapse("genus")

# Save per-sample
phylum_rel.to_csv(RES/"phylum_relative_abundance.tsv", sep="\t")
family_rel.to_csv(RES/"family_relative_abundance.tsv", sep="\t")
genus_rel.to_csv(RES/"genus_relative_abundance.tsv", sep="\t")

# Per-group means
def group_mean(df):
    j = df.join(meta_r[["dose_Gy","timepoint_day"]])
    return j.groupby(["dose_Gy","timepoint_day"]).mean()

phylum_gm = group_mean(phylum_rel)
family_gm = group_mean(family_rel)
genus_gm = group_mean(genus_rel)
phylum_gm.to_csv(RES/"phylum_relabund_by_group.tsv", sep="\t")
family_gm.to_csv(RES/"family_relabund_by_group.tsv", sep="\t")
genus_gm.to_csv(RES/"genus_relabund_by_group.tsv", sep="\t")

print("\nPhylum mean relative abundance by group (top 6):")
top_phyla = phylum_rel.mean(0).sort_values(ascending=False).head(6).index
print((phylum_gm[top_phyla]*100).round(2).to_string())

# Specific paper claims
print("\n== Targeted claims ==")
def find_taxon(table, name_pattern):
    cols = [c for c in table.columns if name_pattern.lower() in c.lower()]
    if not cols:
        return None
    return table[cols].sum(1)

# Akkermansia (Verrucomicrobia)
akk = find_taxon(genus_rel, "Akkermansia")
verr = find_taxon(phylum_rel, "Verrucomicrobi")
bact = find_taxon(phylum_rel, "Bacteroidot") if find_taxon(phylum_rel, "Bacteroidot") is not None else find_taxon(phylum_rel, "Bacteroidet")
firm = find_taxon(phylum_rel, "Firmicutes") if find_taxon(phylum_rel, "Firmicutes") is not None else find_taxon(phylum_rel, "Bacillota")

summary = pd.DataFrame(index=meta_r.index)
if akk is not None:  summary["Akkermansia_genus_rel"] = akk
if verr is not None: summary["Verrucomicrobia_phylum_rel"] = verr
if bact is not None: summary["Bacteroidota_phylum_rel"] = bact
if firm is not None: summary["Firmicutes_phylum_rel"] = firm
summary = summary.join(meta_r[["dose_Gy","timepoint_day"]])
summary.to_csv(RES/"targeted_taxa_per_sample.tsv", sep="\t")

tg = summary.groupby(["dose_Gy","timepoint_day"]).agg(["mean","std","count"])
tg.to_csv(RES/"targeted_taxa_by_group.tsv", sep="\t")
print("\nTargeted taxa per group (means × 100):")
print((tg.xs("mean",axis=1,level=1)*100).round(3).to_string())

# Statistical test for Akkermansia bloom at 0.1Gy/10d vs ctrl/10d
if akk is not None:
    g_ctrl_10 = summary[(summary["dose_Gy"]==0)   & (summary["timepoint_day"]==10)]["Akkermansia_genus_rel"].dropna()
    g_01_10   = summary[(summary["dose_Gy"]==0.1) & (summary["timepoint_day"]==10)]["Akkermansia_genus_rel"].dropna()
    if len(g_ctrl_10)>1 and len(g_01_10)>1:
        U, p = stats.mannwhitneyu(g_ctrl_10, g_01_10, alternative="two-sided")
        print(f"\nAkkermansia 0Gy/10d (mean={g_ctrl_10.mean()*100:.2f}%) vs 0.1Gy/10d (mean={g_01_10.mean()*100:.2f}%): MWU U={U} p={p:.4g}")
        with (RES/"akkermansia_test.json").open("w") as fh:
            json.dump({
                "ctrl_10d_mean_pct": float(g_ctrl_10.mean()*100),
                "ctrl_10d_n": int(len(g_ctrl_10)),
                "irr01Gy_10d_mean_pct": float(g_01_10.mean()*100),
                "irr01Gy_10d_n": int(len(g_01_10)),
                "MWU_U": float(U),
                "p_value": float(p),
                "paper_claim": "Verrucomicrobia up to ~18% at 0.1Gy/10d vs <1% controls",
            }, fh, indent=2)

print("\nAll outputs in:", RES)
