#!/usr/bin/env python3
"""
DESeq2 differential expression per dose-rate group vs matched-batch controls.

Paper (Cantabella et al. 2022, Cancers 14:3793):
  - DESeq2 v1.30.1; |fold change| >= 1.5  AND  padj (fdr) < 0.05
  - 27 DEGs at 0.05 mGy/h, 200 DEGs at 0.5 mGy/h, 530 DEGs at 5 mGy/h.

Design constraint: batch is confounded with dose-rate
  EC015 = controls (n=3) + d05 (n=3) + d5  (n=3)
  EC017 = controls (n=6) + d005 (n=6)
So we do PER-BATCH DESeq2:
  DDS_A on EC015 with design ~ group, contrasts: d05 vs control, d5 vs control
  DDS_B on EC017 with design ~ group, contrasts: d005 vs control
"""
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
META = ROOT / "data/sample_metadata.tsv"
COUNTS = RESULTS / "counts_matrix.tsv.gz"

FC_THRESH = 1.5
LFC_THRESH = math.log2(FC_THRESH)
PADJ_THRESH = 0.05

meta = pd.read_csv(META, sep="\t").set_index("gsm")
counts = pd.read_csv(COUNTS, sep="\t", index_col=0)
# DESeq2 wants samples as rows.
counts = counts.T
# Drop pseudoautosomal/etc. nothing for now; pydeseq2 needs ints.
counts = counts.astype(int)

print(f"Counts: {counts.shape} (samples x genes)")
print(f"Cutoffs: |log2FC| >= {LFC_THRESH:.4f}  AND  padj < {PADJ_THRESH}")

inference = DefaultInference(n_cpus=1)

def run_one_batch(batch_id, contrasts):
    """Fit DESeq2 on samples within one batch, return dict of results-by-contrast."""
    samples = meta[meta["batch"] == batch_id].index.tolist()
    cm = counts.loc[samples].copy()
    md = meta.loc[samples, ["group"]].copy()
    print(f"\n=== Batch {batch_id}: n={len(samples)}  groups={md['group'].value_counts().to_dict()} ===")
    # Pre-filter very low-count genes (DESeq2 default keeps all; for speed and to
    # mimic the paper's normal practice we drop all-zero genes only).
    keep = cm.sum(axis=0) > 0
    cm = cm.loc[:, keep]
    print(f"  Genes kept after zero filter: {cm.shape[1]} (dropped {(~keep).sum()})")
    dds = DeseqDataSet(
        counts=cm,
        metadata=md,
        design="~ group",
        refit_cooks=True,
        inference=inference,
        quiet=True,
    )
    dds.deseq2()
    out = {}
    for contrast_label, (treated, ref) in contrasts.items():
        ds = DeseqStats(dds, contrast=["group", treated, ref], inference=inference, quiet=True)
        ds.summary()
        df = ds.results_df.copy()
        df["gene_id"] = df.index
        df = df.reset_index(drop=True)
        df["abs_log2FC"] = df["log2FoldChange"].abs()
        df["is_deg"] = (df["padj"] < PADJ_THRESH) & (df["abs_log2FC"] >= LFC_THRESH)
        n_total = int(df["is_deg"].sum())
        n_up = int(((df["is_deg"]) & (df["log2FoldChange"] > 0)).sum())
        n_down = int(((df["is_deg"]) & (df["log2FoldChange"] < 0)).sum())
        print(f"  {contrast_label}: {n_total} DEGs (up={n_up}, down={n_down})")
        out[contrast_label] = (df, n_total, n_up, n_down)
    return out

results_A = run_one_batch(
    "EC015",
    contrasts={
        "d05_vs_control": ("d05", "control"),
        "d5_vs_control":  ("d5",  "control"),
    },
)
results_B = run_one_batch(
    "EC017",
    contrasts={
        "d005_vs_control": ("d005", "control"),
    },
)

# Aggregate
summary_rows = []
paper_counts = {"d005_vs_control": 27, "d05_vs_control": 200, "d5_vs_control": 530}
all_results = {}
for label, (df, ntot, nup, ndn) in {**results_A, **results_B}.items():
    out = RESULTS / f"deseq2_{label}.tsv.gz"
    df.sort_values("padj", inplace=True)
    df.to_csv(out, sep="\t", index=False, compression="gzip")
    print(f"Wrote {out}  ({len(df)} rows)")
    all_results[label] = df
    paper_n = paper_counts.get(label)
    ratio = (ntot / paper_n) if paper_n else None
    summary_rows.append({
        "contrast": label,
        "our_n_deg": ntot,
        "our_n_up": nup,
        "our_n_down": ndn,
        "paper_n_deg": paper_n,
        "our/paper": round(ratio, 3) if ratio else None,
    })

summary = pd.DataFrame(summary_rows)
summary.to_csv(RESULTS / "deg_count_comparison.tsv", sep="\t", index=False)
print("\n=== DEG count comparison vs paper ===")
print(summary.to_string(index=False))

# Persist a small JSON summary
out_json = {
    "cutoffs": {"abs_log2FC": LFC_THRESH, "padj": PADJ_THRESH, "fold_change": FC_THRESH},
    "paper_counts": paper_counts,
    "our_counts": {r["contrast"]: {"total": r["our_n_deg"], "up": r["our_n_up"], "down": r["our_n_down"]} for r in summary_rows},
    "ratio_our_over_paper": {r["contrast"]: r["our/paper"] for r in summary_rows},
}
with open(RESULTS / "deg_count_comparison.json", "w") as fh:
    json.dump(out_json, fh, indent=2)
print(f"\nJSON: {RESULTS/'deg_count_comparison.json'}")
