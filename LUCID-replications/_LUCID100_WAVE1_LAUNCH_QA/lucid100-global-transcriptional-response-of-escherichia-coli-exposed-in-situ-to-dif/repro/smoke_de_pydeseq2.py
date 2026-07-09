#!/usr/bin/env python3
"""
LUCID100 slot 7 — smoke replication for Wintenberg et al. mSystems 2023
(DOI 10.1128/msystems.00718-22, GSE208658).

Goal: rerun differential expression on the public GEO count matrix using
PyDESeq2 and compare DEG counts at the paper's reported cutoff
(|log2FC| > 2 AND padj < 0.05) against the paper's reported Fig. 2 numbers.

Paper-reported DEG counts (Fig. 2 / Results pp. 4-5):
  Pu-239  vs Control   Day 1: 590    Day 15: 11
  H-3     vs Control   Day 1: 46     Day 15: 2137
  Fe-55   vs FeCl3 Ctl Day 1: 1144   Day 15: 661

Input: ../artifacts/GSE208658_Ec_count_matrix.txt (tximport-style with
abundance.*, counts.*, length.* columns for 30 samples).

Output: deg_counts_replication.tsv printed to stdout and written next to
this script. We use raw counts only (counts.* columns), rounded to int.

This script is small: ~4566 genes x 6 samples per contrast = trivial,
fits well inside CherryRd-allowed compute.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from pydeseq2.dds import DeseqDataSet
from pydeseq2.default_inference import DefaultInference
from pydeseq2.ds import DeseqStats


HERE = Path(__file__).resolve().parent
ART = HERE.parent / "artifacts"
COUNTS_TSV = ART / "GSE208658_Ec_count_matrix.txt"
OUT_TSV = HERE / "deg_counts_replication.tsv"
OUT_DETAIL_DIR = HERE / "de_tables"
OUT_DETAIL_DIR.mkdir(exist_ok=True)


# Paper-reported DEG counts for direct comparison.
PAPER = {
    ("Pu239", "D1"): 590,
    ("Pu239", "D15"): 11,
    ("H3",    "D1"): 46,
    ("H3",    "D15"): 2137,
    ("Fe55",  "D1"): 1144,
    ("Fe55",  "D15"): 661,
}

# Contrast spec: (label, treated_token, control_token, day)
# Tokens match the column-name suffix in the count matrix:
#   counts.Ec_<token>_D<day>_R<rep>
CONTRASTS = [
    ("Pu239_vs_Con_D1",       "Pu239",   "Con",      "D1"),
    ("Pu239_vs_Con_D15",      "Pu239",   "Con",      "D15"),
    ("H3_vs_Con_D1",          "H3",      "Con",      "D1"),
    ("H3_vs_Con_D15",         "H3",      "Con",      "D15"),
    ("Fe55_vs_FeCl3Con_D1",   "Fe55",    "FeCl3Con", "D1"),
    ("Fe55_vs_FeCl3Con_D15",  "Fe55",    "FeCl3Con", "D15"),
]


def load_counts() -> pd.DataFrame:
    """Return a (gene x sample) int count matrix.

    The GEO matrix is tximport-style with three blocks of columns
    (abundance.*, counts.*, length.*).  We keep only counts.* and rename
    columns to the sample token.
    """
    df = pd.read_csv(COUNTS_TSV, sep="\t", index_col=0)
    # The first column (gene id) becomes the index; pandas may name it ''.
    count_cols = [c for c in df.columns if c.startswith("counts.")]
    counts = df[count_cols].copy()
    # Strip "counts.Ec_" prefix so columns are like "Pu239_D1_R1".
    counts.columns = [c.replace("counts.Ec_", "") for c in counts.columns]
    # tximport StringTie output can produce non-integer counts; round.
    counts = counts.round().astype(int)
    return counts


def build_sample_df(samples: list[str]) -> pd.DataFrame:
    """Parse <TOKEN>_<DAY>_<REP> into a tidy sample metadata frame."""
    rows = []
    for s in samples:
        # Split from the right because tokens like FeCl3Con contain no underscore here.
        parts = s.split("_")
        token, day, rep = parts[0], parts[1], parts[2]
        rows.append({"sample": s, "token": token, "day": day, "rep": rep})
    meta = pd.DataFrame(rows).set_index("sample")
    return meta


def run_contrast(counts: pd.DataFrame, meta: pd.DataFrame,
                 label: str, treated: str, control: str, day: str) -> dict:
    """Run a single DESeq2 contrast (treated vs control at one day)."""
    keep = meta.index[(meta["day"] == day) & (meta["token"].isin([treated, control]))]
    sub_counts = counts[keep].T  # PyDESeq2 expects samples x genes
    sub_meta = meta.loc[keep, ["token"]].rename(columns={"token": "condition"})
    sub_meta["condition"] = pd.Categorical(
        sub_meta["condition"], categories=[control, treated]
    )

    inference = DefaultInference(n_cpus=2)
    dds = DeseqDataSet(
        counts=sub_counts,
        metadata=sub_meta,
        design="~condition",
        inference=inference,
        quiet=True,
    )
    dds.deseq2()
    stats = DeseqStats(
        dds, contrast=["condition", treated, control], inference=inference, quiet=True
    )
    stats.summary()
    res = stats.results_df.copy()
    res.to_csv(OUT_DETAIL_DIR / f"{label}.tsv", sep="\t")

    # Paper cutoff: |log2FC| > 2 AND padj < 0.05.
    sig = res[(res["padj"].notna()) & (res["padj"] < 0.05) & (res["log2FoldChange"].abs() > 2)]
    return {
        "label": label,
        "n_genes_tested": int(res.shape[0]),
        "n_padj_below_0p05": int((res["padj"] < 0.05).sum()),
        "n_lfc_gt_2": int((res["log2FoldChange"].abs() > 2).sum()),
        "n_deg_paper_cutoff": int(sig.shape[0]),
        "n_up": int((sig["log2FoldChange"] > 0).sum()),
        "n_down": int((sig["log2FoldChange"] < 0).sum()),
    }


def main() -> int:
    counts = load_counts()
    print(f"[smoke] count matrix: {counts.shape[0]} genes x {counts.shape[1]} samples",
          file=sys.stderr)
    meta = build_sample_df(list(counts.columns))
    print("[smoke] sample token counts:", file=sys.stderr)
    print(meta["token"].value_counts().to_string(), file=sys.stderr)

    rows = []
    for label, treated, control, day in CONTRASTS:
        print(f"[smoke] running {label} ...", file=sys.stderr)
        rec = run_contrast(counts, meta, label, treated, control, day)
        key = (treated, day)
        rec["paper_deg_count"] = PAPER.get(key)
        rec["delta_vs_paper"] = (
            rec["n_deg_paper_cutoff"] - rec["paper_deg_count"]
            if rec["paper_deg_count"] is not None else None
        )
        rows.append(rec)

    out = pd.DataFrame(rows)
    out.to_csv(OUT_TSV, sep="\t", index=False)
    print("\n=== DEG COUNT REPLICATION (paper cutoff: |log2FC|>2 AND padj<0.05) ===")
    print(out.to_string(index=False))
    print(f"\nWrote {OUT_TSV}")
    print(f"Per-contrast full DE tables in {OUT_DETAIL_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
