"""Variant: prefilter genes with sum>=10 in the contrast; also try independentFiltering on/off via padj recompute."""
import gzip, os, json
import pandas as pd, numpy as np

SAMPLES = [
    ("GSM6257033","C1_36d_EC015","B1","ctrl"),
    ("GSM6257034","C2_36d_EC015","B1","ctrl"),
    ("GSM6257035","C3_36d_EC015","B1","ctrl"),
    ("GSM6257036","051_36d_EC015","B1","d05"),
    ("GSM6257037","052_36d_EC015","B1","d05"),
    ("GSM6257038","053_36d_EC015","B1","d05"),
    ("GSM6257039","51_36d_EC015","B1","d5"),
    ("GSM6257040","52_36d_EC015","B1","d5"),
    ("GSM6257041","53_36d_EC015","B1","d5"),
    ("GSM6257042","C1_36d_EC017","B2","ctrl"),
    ("GSM6257043","C2_36d_EC017","B2","ctrl"),
    ("GSM6257044","C3_36d_EC017","B2","ctrl"),
    ("GSM6257045","C4_36d_EC017","B2","ctrl"),
    ("GSM6257046","C5_36d_EC017","B2","ctrl"),
    ("GSM6257047","C6_36d_EC017","B2","ctrl"),
    ("GSM6257048","I0051_36d_EC017","B2","d005"),
    ("GSM6257049","I0052_36d_EC017","B2","d005"),
    ("GSM6257050","I0053_36d_EC017","B2","d005"),
    ("GSM6257051","I0054_36d_EC017","B2","d005"),
    ("GSM6257052","I0055_36d_EC017","B2","d005"),
    ("GSM6257053","I0056_36d_EC017","B2","d005"),
]

def load_counts():
    cols = {}
    for gsm, fid, _,_ in SAMPLES:
        path = f"{gsm}_Sample_{fid}.counts.txt.gz"
        genes, vals = [], []
        with gzip.open(path, "rt") as fh:
            for line in fh:
                parts = line.rstrip().split("\t")
                if parts[0].startswith("N_"):
                    continue
                genes.append(parts[0])
                vals.append(int(parts[3]))
        cols[gsm] = pd.Series(vals, index=genes, name=gsm)
    return pd.concat(cols.values(), axis=1)

def make_meta():
    return pd.DataFrame([{"sample":g,"batch":b,"condition":c} for g,_,b,c in SAMPLES]).set_index("sample")

def run(counts_all, meta_all, batch, ctrl, treat, label):
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.default_inference import DefaultInference
    from pydeseq2.ds import DeseqStats
    keep = (meta_all["batch"]==batch) & meta_all["condition"].isin([ctrl,treat])
    meta = meta_all[keep].copy()
    counts = counts_all.loc[:, meta.index].T.astype(int)
    inf = DefaultInference(n_cpus=1)
    dds = DeseqDataSet(counts=counts, metadata=meta, design="~condition", inference=inf, quiet=True)
    dds.deseq2()
    st = DeseqStats(dds, contrast=["condition", treat, ctrl], inference=inf, quiet=True)
    st.summary()
    res = st.results_df.copy()
    out = {}
    # Try a few thresholds
    for p in (0.05, 0.1):
        for l in (0.0, 0.585, 1.0):
            sig = (res["padj"] < p) & (res["log2FoldChange"].abs() >= l)
            out[f"padj<{p}_lfc>={l}"] = int(sig.sum())
    print(f"\n[{label}] (batch={batch}, {treat} vs {ctrl})")
    for k,v in out.items(): print(f"  {k}: {v}")
    return out, res

def run_drop_outlier(counts_all, meta_all, drop):
    """Re-run 5 mGy/h vs ctrl after dropping a suspected outlier sample."""
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.default_inference import DefaultInference
    from pydeseq2.ds import DeseqStats
    keep = (meta_all["batch"]=="B1") & meta_all["condition"].isin(["ctrl","d5"]) & (~meta_all.index.isin(drop))
    meta = meta_all[keep].copy()
    counts = counts_all.loc[:, meta.index].T.astype(int)
    inf = DefaultInference(n_cpus=1)
    dds = DeseqDataSet(counts=counts, metadata=meta, design="~condition", inference=inf, quiet=True)
    dds.deseq2()
    st = DeseqStats(dds, contrast=["condition","d5","ctrl"], inference=inf, quiet=True)
    st.summary()
    res = st.results_df.copy()
    out = {}
    for p in (0.05,0.1):
        for l in (0.0, 0.585, 1.0):
            sig = (res["padj"]<p) & (res["log2FoldChange"].abs()>=l)
            out[f"padj<{p}_lfc>={l}"] = int(sig.sum())
    print(f"\n[5 mGy/h vs ctrl  drop={drop}]")
    for k,v in out.items(): print(f"  {k}: {v}")
    return out

def main():
    counts = load_counts()
    meta = make_meta()
    print(f"Counts: {counts.shape}")
    print("=== Standard ===")
    s_005,_ = run(counts, meta, "B2","ctrl","d005","0.05 mGy/h")
    s_05 ,_ = run(counts, meta, "B1","ctrl","d05" ,"0.5  mGy/h")
    s_5  ,_ = run(counts, meta, "B1","ctrl","d5"  ,"5    mGy/h")

    print("\n=== Drop GSM6257039 (5mGy outlier on PCA) ===")
    s_5_drop = run_drop_outlier(counts, meta, ["GSM6257039"])

    summary = {"paper":{"0.05":27,"0.5":200,"5":530},
               "recovered":{"0.05":s_005,"0.5":s_05,"5":s_5,"5_drop39":s_5_drop}}
    with open("summary.json","w") as fh:
        json.dump(summary, fh, indent=2)
    print("\n=== SUMMARY vs paper (27/200/530) ===")
    print(json.dumps(summary["recovered"], indent=2))

if __name__=="__main__":
    main()
