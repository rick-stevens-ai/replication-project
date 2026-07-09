#!/usr/bin/env python3
"""
Build a (genes x samples) count matrix and a sample sheet from the
GSE277249 per-sample featureCounts files.

The 18 samples are 6 cell lines, each in biological triplicate:

  parental_ANV5  : ANV51, ANV52, ANV53           (3 samples)
  CTC700  (ANV5) : M7001, M7002, M7003           (3 samples)  -- CTC-in
  CTC803  (ANV5) : M8031, M8032, M8033           (3 samples)  -- CTC-in
  parental_4T1   : M4t11, M4t12, M4t13           (3 samples)
  CTC1589 (4T1)  : M15891, M15892, M15893        (3 samples)  -- CTC-in
  CTC1592 (4T1)  : M15921, M15922, M15923        (3 samples)  -- CTC-in

Outputs:
  results/counts_matrix.tsv         (genes x samples)
  results/sample_sheet.tsv          (sample, cell_line, group, parental, lineage)
"""

import os
import re
import glob
import gzip
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COUNTS_DIR = os.path.join(ROOT, "data", "counts")
OUT_DIR = os.path.join(ROOT, "results")
os.makedirs(OUT_DIR, exist_ok=True)


def sample_label(filename: str) -> str:
    """Derive a short sample label from the file name, e.g.
    GSM8517116_M7001_S23.counts.txt -> M7001
    """
    base = os.path.basename(filename)
    m = re.match(r"GSM\d+_([A-Za-z0-9]+)_S\d+\.counts\.txt", base)
    if not m:
        raise ValueError(f"Cannot parse {base!r}")
    return m.group(1)


def cell_line(label: str) -> str:
    # ANV5 parental: ANV51, ANV52, ANV53
    if re.match(r"^ANV5\d$", label):
        return "ANV5_parental"
    # CTC-in from ANV5: M700* (CTC700) and M803* (CTC803)
    if label.startswith("M700"):
        return "CTC700"
    if label.startswith("M803"):
        return "CTC803"
    # 4T1 parental: M4t11, M4t12, M4t13
    if label.lower().startswith("m4t1"):
        return "4T1_parental"
    # CTC-in from 4T1: M1589*, M1592*
    if label.startswith("M1589"):
        return "CTC1589"
    if label.startswith("M1592"):
        return "CTC1592"
    raise ValueError(f"Unknown label {label!r}")


def parental(cl: str) -> str:
    return "ANV5" if cl in ("ANV5_parental", "CTC700", "CTC803") else "4T1"


def group(cl: str) -> str:
    return "parental" if cl.endswith("_parental") else "CTC_in"


def main():
    files = sorted(glob.glob(os.path.join(COUNTS_DIR, "GSM*.counts.txt")))
    if not files:
        files = sorted(glob.glob(os.path.join(COUNTS_DIR, "GSM*.counts.txt.gz")))
    print(f"[matrix] found {len(files)} count files")

    cols = {}
    info_cols = None
    for f in files:
        label = sample_label(f)
        opener = gzip.open if f.endswith(".gz") else open
        df = pd.read_csv(
            f,
            sep="\t",
            comment="#",
            dtype={"Geneid": str},
        )
        # last column is the count
        count_col = df.columns[-1]
        df = df.rename(columns={count_col: label})
        if info_cols is None:
            info_cols = df[["Geneid", "Chr", "Start", "End", "Strand", "Length"]].copy()
        cols[label] = df.set_index("Geneid")[label]

    counts = pd.DataFrame(cols)
    counts = counts.loc[info_cols["Geneid"].values]
    counts.index.name = "Geneid"
    print(f"[matrix] count matrix shape: {counts.shape}")

    # Strip Ensembl version suffix for downstream symbol mapping convenience
    counts.insert(0, "Length", info_cols.set_index("Geneid")["Length"].reindex(counts.index).values)

    out_matrix = os.path.join(OUT_DIR, "counts_matrix.tsv")
    counts.to_csv(out_matrix, sep="\t")
    print(f"[matrix] wrote {out_matrix}")

    # Sample sheet
    rows = []
    for lab in counts.columns:
        if lab == "Length":
            continue
        cl = cell_line(lab)
        rows.append(
            dict(
                sample=lab,
                cell_line=cl,
                group=group(cl),
                parental=parental(cl),
                lineage=cl,  # also keep per-cell-line label
            )
        )
    sheet = pd.DataFrame(rows)
    out_sheet = os.path.join(OUT_DIR, "sample_sheet.tsv")
    sheet.to_csv(out_sheet, sep="\t", index=False)
    print(f"[matrix] wrote {out_sheet}")
    print(sheet.to_string(index=False))


if __name__ == "__main__":
    main()
