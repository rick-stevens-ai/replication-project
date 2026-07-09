"""
Re-run DESeq2 differential expression on GSE206573 to test the paper's
27 / 200 / 530 DEG counts at 0.05 / 0.5 / 5 mGy/h (Cantabella et al. 2022).

Library: Illumina Stranded mRNA-Seq (dUTP) -> use column 4 (reverse-stranded)
from the STAR ReadsPerGene.out.tab files.

Design:
  - Batch1 (EC015): C1,C2,C3 = control;  051,052,053 = 0.5 mGy/h; 51,52,53 = 5 mGy/h
  - Batch2 (EC017): C1..C6   = control;  I0051..I0056 = 0.05 mGy/h

Within-batch contrasts:
  0.05 mGy/h vs ctrl (batch2 only): N=6 vs 6
  0.5  mGy/h vs ctrl (batch1 only): N=3 vs 3
  5    mGy/h vs ctrl (batch1 only): N=3 vs 3

Threshold: paper uses DESeq2 v1.22.2. Standard call: adjusted p (BH) < 0.05.
We report DEG counts at padj<0.05 (with and without |log2FC|>=1 filters), and
print the strictest match to 27 / 200 / 530.
"""
import gzip, glob, os, sys, json
import pandas as pd
import numpy as np

SAMPLES = [
    # (GSM, file_id, batch, condition)
    ("GSM6257033","C1_36d_EC015","B1","ctrl"),
    ("GSM6257034","C2_36d_EC015","B1","ctrl"),
    ("GSM6257035","C3_36d_EC015","B1","ctrl"),
    ("GSM6257036","051_36d_EC015","B1","d05"),   # 0.5
    ("GSM6257037","052_36d_EC015","B1","d05"),
    ("GSM6257038","053_36d_EC015","B1","d05"),
    ("GSM6257039","51_36d_EC015","B1","d5"),     # 5
    ("GSM6257040","52_36d_EC015","B1","d5"),
    ("GSM6257041","53_36d_EC015","B1","d5"),
    ("GSM6257042","C1_36d_EC017","B2","ctrl"),
    ("GSM6257043","C2_36d_EC017","B2","ctrl"),
    ("GSM6257044","C3_36d_EC017","B2","ctrl"),
    ("GSM6257045","C4_36d_EC017","B2","ctrl"),
    ("GSM6257046","C5_36d_EC017","B2","ctrl"),
    ("GSM6257047","C6_36d_EC017","B2","ctrl"),
    ("GSM6257048","I0051_36d_EC017","B2","d005"), # 0.05
    ("GSM6257049","I0052_36d_EC017","B2","d005"),
    ("GSM6257050","I0053_36d_EC017","B2","d005"),
    ("GSM6257051","I0054_36d_EC017","B2","d005"),
    ("GSM6257052","I0055_36d_EC017","B2","d005"),
    ("GSM6257053","I0056_36d_EC017","B2","d005"),
]

def load_counts():
    cols = {}
    for gsm, fid, batch, cond in SAMPLES:
        path = f"GSM{gsm[3:]}_Sample_{fid}.counts.txt.gz"
        if not os.path.exists(path):
            # try lookup
            cand = glob.glob(f"{gsm}_Sample_{fid}.counts.txt.gz")
            assert cand, f"missing {gsm} {fid}"
            path = cand[0]
        genes, vals = [], []
        with gzip.open(path, "rt") as fh:
            for line in fh:
                parts = line.rstrip().split("\t")
                if parts[0].startswith("N_"):
                    continue
                genes.append(parts[0])
                vals.append(int(parts[3]))   # reverse-stranded (col 4)
        cols[gsm] = pd.Series(vals, index=genes, name=gsm)
    df = pd.concat(cols.values(), axis=1)
    return df

def make_meta():
    rows = []
    for gsm, fid, batch, cond in SAMPLES:
        rows.append({"sample": gsm, "batch": batch, "condition": cond})
    return pd.DataFrame(rows).set_index("sample")

def run_contrast(counts_all, meta_all, b, ctrl_label, treat_label, name, do_lfc=False):
    """Run DESeq2 (pydeseq2) within batch b, ctrl vs treat."""
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.default_inference import DefaultInference
    from pydeseq2.ds import DeseqStats

    keep = (meta_all["batch"] == b) & meta_all["condition"].isin([ctrl_label, treat_label])
    meta = meta_all[keep].copy()
    counts = counts_all.loc[:, meta.index].T   # samples x genes
    counts = counts.astype(int)
    # Drop all-zero genes? DESeq2 keeps everything; leave as-is.
    inference = DefaultInference(n_cpus=1)
    dds = DeseqDataSet(
        counts=counts,
        metadata=meta,
        design="~condition",
        ref_level=("condition", ctrl_label),
        inference=inference,
        quiet=True,
    )
    dds.deseq2()
    stat = DeseqStats(dds, contrast=["condition", treat_label, ctrl_label], inference=inference, quiet=True)
    stat.summary()
    res = stat.results_df.copy()
    # Counts
    out = {}
    for thr_p in (0.05, 0.1):
        sig = res["padj"] < thr_p
        out[f"padj<{thr_p}"] = int(sig.sum())
        for thr_l in (1.0, 0.585):  # 2x and 1.5x
            out[f"padj<{thr_p}_|log2FC|>={thr_l}"] = int((sig & (res["log2FoldChange"].abs() >= thr_l)).sum())
    print(f"[{name}] (batch={b}, {treat_label} vs {ctrl_label}, n={ (meta['condition']==treat_label).sum()} vs { (meta['condition']==ctrl_label).sum()})")
    for k,v in out.items():
        print(f"   {k}: {v}")
    return res, out

def main():
    counts = load_counts()
    meta = make_meta()
    print(f"Loaded counts: {counts.shape[0]} genes x {counts.shape[1]} samples")
    print(f"Library depths (col-4 reverse stranded), millions:")
    print((counts.sum(0)/1e6).round(2).to_string())
    print()

    summary = {}
    res_005, s_005 = run_contrast(counts, meta, "B2", "ctrl", "d005", "0.05 mGy/h")
    summary["0.05"] = s_005
    res_05 , s_05  = run_contrast(counts, meta, "B1", "ctrl", "d05" , "0.5 mGy/h")
    summary["0.5"]  = s_05
    res_5  , s_5   = run_contrast(counts, meta, "B1", "ctrl", "d5"  , "5 mGy/h")
    summary["5"]    = s_5

    # Save tables
    for tag, res in [("d005", res_005), ("d05", res_05), ("d5", res_5)]:
        res.to_csv(f"de_{tag}.tsv", sep="\t")

    print("\n=== Paper claims: 27 / 200 / 530 DEGs at 0.05 / 0.5 / 5 mGy/h ===")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
