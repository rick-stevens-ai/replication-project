#!/usr/bin/env python3
"""
Alternative DESeq2 design: pool all controls and treat the full design as
  ~ batch + group     (when both batches contribute to that comparison)
or just
  ~ group             (when only one batch contributes).

Since the paper does not describe batch correction inside DESeq2, we also test:
  - per-contrast with pooled controls and no batch in design.

For each dose rate we run two flavors and report DEG counts:
  A) per-contrast subset of samples, design ~ group, pooled controls
  B) per-contrast subset, design ~ batch + group (when batches differ)

Reference: Cantabella et al. 2022, Cancers 14:3793.
DEG criterion: |log2FC| >= log2(1.5) AND padj < 0.05.
"""
import math, json
from pathlib import Path
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
META = ROOT / "data/sample_metadata.tsv"
COUNTS = RESULTS / "counts_matrix.tsv.gz"

LFC_THRESH = math.log2(1.5)
PADJ_THRESH = 0.05

meta = pd.read_csv(META, sep="\t").set_index("gsm")
counts = pd.read_csv(COUNTS, sep="\t", index_col=0).T.astype(int)
inference = DefaultInference(n_cpus=1)

def deg_count(df, lfc=LFC_THRESH, padj=PADJ_THRESH):
    sig = (df["padj"].fillna(1) < padj) & (df["log2FoldChange"].abs() >= lfc)
    n = int(sig.sum())
    up = int(((df["log2FoldChange"] > 0) & sig).sum())
    dn = int(((df["log2FoldChange"] < 0) & sig).sum())
    return n, up, dn

def fit_contrast(samples, design, contrast, label):
    cm = counts.loc[samples].copy()
    md = meta.loc[samples, list({"group", "batch"})].copy()
    keep = cm.sum(axis=0) > 0
    cm = cm.loc[:, keep]
    dds = DeseqDataSet(counts=cm, metadata=md, design=design, refit_cooks=True,
                       inference=inference, quiet=True)
    dds.deseq2()
    ds = DeseqStats(dds, contrast=contrast, inference=inference, quiet=True)
    ds.summary()
    df = ds.results_df.copy()
    df["gene_id"] = df.index
    df = df.reset_index(drop=True)
    n, up, dn = deg_count(df)
    return label, n, up, dn, df, len(samples)

# All-batches comparisons (pool controls from EC015+EC017, plus the treated of interest)
rows = []
# d005: only in EC017 -> same as before, just sanity
samples = meta[meta["group"].isin(["control", "d005"])].index.tolist()
label, n, up, dn, df1, ns = fit_contrast(samples, "~ batch + group", ["group","d005","control"],
                                         "d005_pooled_~batch+group")
rows.append((label, ns, n, up, dn))
print(f"{label}: n={ns} -> DEG={n} (up={up}, dn={dn})")

samples = meta[meta["group"].isin(["control", "d005"])].index.tolist()
# without batch term
label, n, up, dn, df1b, ns = fit_contrast(samples, "~ group", ["group","d005","control"],
                                          "d005_pooled_~group")
rows.append((label, ns, n, up, dn))
print(f"{label}: n={ns} -> DEG={n} (up={up}, dn={dn})")

# d05: treated in EC015 only; pool ALL 9 controls (EC015 + EC017) with d05 (EC015)
samples = meta[meta["group"].isin(["control", "d05"])].index.tolist()
label, n, up, dn, df2, ns = fit_contrast(samples, "~ batch + group", ["group","d05","control"],
                                         "d05_pooled_~batch+group")
rows.append((label, ns, n, up, dn))
print(f"{label}: n={ns} -> DEG={n} (up={up}, dn={dn})")

samples = meta[meta["group"].isin(["control", "d05"])].index.tolist()
label, n, up, dn, df2b, ns = fit_contrast(samples, "~ group", ["group","d05","control"],
                                          "d05_pooled_~group")
rows.append((label, ns, n, up, dn))
print(f"{label}: n={ns} -> DEG={n} (up={up}, dn={dn})")
df2b_save = df2b.sort_values("padj")
df2b_save.to_csv(RESULTS/"deseq2_d05_pooled_nobatch.tsv.gz", sep="\t", index=False, compression="gzip")

# d5: treated in EC015 only
samples = meta[meta["group"].isin(["control", "d5"])].index.tolist()
label, n, up, dn, df3, ns = fit_contrast(samples, "~ batch + group", ["group","d5","control"],
                                         "d5_pooled_~batch+group")
rows.append((label, ns, n, up, dn))
print(f"{label}: n={ns} -> DEG={n} (up={up}, dn={dn})")

samples = meta[meta["group"].isin(["control", "d5"])].index.tolist()
label, n, up, dn, df3b, ns = fit_contrast(samples, "~ group", ["group","d5","control"],
                                          "d5_pooled_~group")
rows.append((label, ns, n, up, dn))
print(f"{label}: n={ns} -> DEG={n} (up={up}, dn={dn})")
df3b_save = df3b.sort_values("padj")
df3b_save.to_csv(RESULTS/"deseq2_d5_pooled_nobatch.tsv.gz", sep="\t", index=False, compression="gzip")

# Also save d005 best-effort
df1.sort_values("padj").to_csv(RESULTS/"deseq2_d005_pooled_batchadj.tsv.gz", sep="\t", index=False, compression="gzip")

summary = pd.DataFrame(rows, columns=["label","n_samples","n_deg","n_up","n_down"])
paper = {"d005":27, "d05":200, "d5":530}
def paper_for(label):
    for k,v in paper.items():
        if label.startswith(k+"_"): return v
    return None
summary["paper_n_deg"] = summary["label"].apply(paper_for)
summary["ratio"] = (summary["n_deg"]/summary["paper_n_deg"]).round(3)
print("\n=== Summary ===")
print(summary.to_string(index=False))
summary.to_csv(RESULTS/"deg_count_comparison_alt_designs.tsv", sep="\t", index=False)
