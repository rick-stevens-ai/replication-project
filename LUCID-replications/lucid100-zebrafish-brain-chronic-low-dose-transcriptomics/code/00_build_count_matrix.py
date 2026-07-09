#!/usr/bin/env python3
"""
Build a count matrix from per-sample STAR `ReadsPerGene` files in GSE206573.

The paper used TruSeq mRNA Stranded -> reverse-stranded. We:
  - Use col 4 (reverse strand) as the primary count
  - Sanity-check: vs col 2 (unstranded) and col 3 (forward), confirm col 4
    has the highest assigned-to-feature fraction (lowest N_noFeature share).
"""
import gzip
import os
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COUNTS_DIR = ROOT / "data/counts"
META = ROOT / "data/sample_metadata.tsv"
OUT_DIR = ROOT / "results"
OUT_DIR.mkdir(exist_ok=True, parents=True)

meta = pd.read_csv(META, sep="\t")
print(f"Loaded metadata: {len(meta)} samples")

def parse_counts(path: Path):
    """Return tuple (qc_df, gene_df) for one STAR ReadsPerGene file."""
    rows = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            rows.append(parts)
    cols = ["gene_id", "unstranded", "fwd", "rev"]
    df = pd.DataFrame(rows, columns=cols)
    for c in cols[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    qc_mask = df["gene_id"].str.startswith("N_")
    qc = df[qc_mask].copy()
    gene = df[~qc_mask].copy()
    return qc, gene

# Pick a sample with which we evaluate strandedness.
qc0, gene0 = parse_counts(COUNTS_DIR / "GSM6257033_Sample_C1_36d_EC015.counts.txt.gz")
print("\nStrandedness check (GSM6257033):")
print(qc0.to_string(index=False))
totals = {c: gene0[c].sum() for c in ("unstranded", "fwd", "rev")}
print(f"Assigned-to-feature sums: {totals}")
# Prefer the strand with HIGHEST assigned counts (= lowest N_noFeature share).
best_strand = max(totals, key=totals.get)
print(f"-> Selected strand: {best_strand}")

# Build matrices
counts_mat = None
qc_records = []
sample_order = []
for _, row in meta.iterrows():
    gsm = row["gsm"]
    matches = list(COUNTS_DIR.glob(f"{gsm}_*.counts.txt.gz"))
    if len(matches) != 1:
        raise SystemExit(f"Expected 1 file for {gsm}, got {len(matches)}")
    qc, gene = parse_counts(matches[0])
    series = gene.set_index("gene_id")[best_strand].astype(int)
    series.name = gsm
    if counts_mat is None:
        counts_mat = series.to_frame()
    else:
        counts_mat = counts_mat.join(series, how="outer")
    qc_pivot = qc.set_index("gene_id")[best_strand].to_dict()
    qc_pivot["sample"] = gsm
    qc_pivot["assigned_to_feature"] = int(gene[best_strand].sum())
    qc_records.append(qc_pivot)
    sample_order.append(gsm)

counts_mat = counts_mat[sample_order].fillna(0).astype(int)
counts_mat.index.name = "gene_id"
print(f"\nCount matrix: {counts_mat.shape[0]} genes x {counts_mat.shape[1]} samples")

out_counts = OUT_DIR / "counts_matrix.tsv.gz"
counts_mat.to_csv(out_counts, sep="\t", compression="gzip")
print(f"Wrote {out_counts}")

qc_df = pd.DataFrame(qc_records)
qc_df = qc_df[["sample", "N_unmapped", "N_multimapping", "N_noFeature", "N_ambiguous", "assigned_to_feature"]]
qc_df["library_size"] = qc_df[["N_unmapped", "N_multimapping", "N_noFeature", "N_ambiguous", "assigned_to_feature"]].sum(axis=1)
qc_df["pct_assigned"] = 100.0 * qc_df["assigned_to_feature"] / qc_df["library_size"]
qc_df.to_csv(OUT_DIR / "library_qc.tsv", sep="\t", index=False)
print(f"Wrote {OUT_DIR/'library_qc.tsv'}")
print("\nLibrary QC summary (head):")
print(qc_df.head(5).to_string(index=False))
print("\nReads_assigned per group:")
joined = qc_df.merge(meta, left_on="sample", right_on="gsm")
print(joined.groupby(["batch", "group"])["assigned_to_feature"].agg(["count", "mean", "min", "max"]).round(0).to_string())
