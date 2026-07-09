"""QC: PCA + sample-sample correlation on rlog-like (log1p of normalized) counts."""
import gzip, os
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

cols = {}
for gsm, fid, batch, cond in SAMPLES:
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
df = pd.concat(cols.values(), axis=1)

# Size-factor normalize (median-of-ratios proxy: CPM is fine for QC)
cpm = df.div(df.sum(0), axis=1) * 1e6
log_cpm = np.log2(cpm + 1)

# Focus on batch1 only for the 5 mGy/h discrepancy
b1 = [g for g,_,b,_ in SAMPLES if b=="B1"]
sub = log_cpm[b1]
# Sample-sample correlation
corr = sub.corr()
print("Batch1 sample-sample log2CPM correlation matrix:")
print(corr.round(3).to_string())
print()
labels = {g: c for g,_,_,c in SAMPLES}
print("Conditions:", {g:labels[g] for g in b1})

# PCA top 2000 variable genes
top = sub.var(1).sort_values(ascending=False).head(2000).index
X = sub.loc[top].T.values
X = X - X.mean(0)
U,S,Vt = np.linalg.svd(X, full_matrices=False)
pcs = U[:,:3] * S[:3]
print("\nBatch1 PC1/PC2/PC3 per sample (var explained:", (S[:3]**2/(S**2).sum()*100).round(1), "%):")
for i,g in enumerate(b1):
    print(f"  {g} ({labels[g]}): {pcs[i,0]:+.2f}  {pcs[i,1]:+.2f}  {pcs[i,2]:+.2f}")
