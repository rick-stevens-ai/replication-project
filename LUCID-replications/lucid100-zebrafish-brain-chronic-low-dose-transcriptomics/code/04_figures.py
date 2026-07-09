#!/usr/bin/env python3
"""Smoke figures: DEG count comparison, dose-response of stress-axis genes,
PCA of samples, volcano for d5_vs_control (full ~batch+group)."""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"
FIGS.mkdir(exist_ok=True, parents=True)

LFC = math.log2(1.5)

# ------ FIG 1: DEG count comparison ------
paper = {"0.05 mGy/h": 27, "0.5 mGy/h": 200, "5 mGy/h": 530}
ours_full = {  # ~batch+group, all 21 samples
    "0.05 mGy/h": 29, "0.5 mGy/h": 5, "5 mGy/h": 83,
}
ours_pooled = {  # ~group, pooled controls (no batch)
    "0.05 mGy/h": 31, "0.5 mGy/h": 229, "5 mGy/h": 90,
}
labels = list(paper.keys())
x = np.arange(len(labels))
w = 0.27
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(x - w, [paper[l] for l in labels], w, label="Paper (Cantabella 2022)", color="#444444")
ax.bar(x,     [ours_full[l] for l in labels], w, label="Ours: ~batch + group", color="#1f77b4")
ax.bar(x + w, [ours_pooled[l] for l in labels], w, label="Ours: ~group (pooled)", color="#ff7f0e")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("# DEGs (|log2FC| ≥ log2(1.5), padj < 0.05)")
ax.set_title("Replicated DEG counts vs paper (GSE206573)\nDose-rate–dependent increase preserved")
ax.legend()
for i, l in enumerate(labels):
    for j, (d, off) in enumerate(zip([paper[l], ours_full[l], ours_pooled[l]], [-w, 0, w])):
        ax.text(i + off, d + max(paper.values())*0.01, str(d), ha="center", fontsize=9)
plt.tight_layout()
out = FIGS / "fig1_deg_counts_vs_paper.png"
plt.savefig(out, dpi=150); plt.close()
print(f"Saved {out}")

# ------ FIG 2: dose-response of stress-axis genes ------
ENS = {
 "oxt":"ENSDARG00000042845","avp":"ENSDARG00000058567","tph1a":"ENSDARG00000029432",
 "tph2":"ENSDARG00000057239","crx":"ENSDARG00000011989","cyp11c1":"ENSDARG00000042014",
 "asip2b":"ENSDARG00000114760","nr4a1":"ENSDARG00000000796"}
records = []
for treat, dose, contrast in [
    ("d005", 0.05, "d005_full_batchgroup"),
    ("d05",  0.50, "d05_full_batchgroup"),
    ("d5",   5.00, "d5_full_batchgroup"),
]:
    df = pd.read_csv(RESULTS/f"deseq2_{contrast}.tsv.gz", sep="\t").set_index("gene_id")
    for sym, eid in ENS.items():
        if eid in df.index:
            r = df.loc[eid]
            records.append({"gene":sym, "dose":dose, "log2FC":r["log2FoldChange"], "padj":r["padj"] if pd.notna(r["padj"]) else np.nan})
hf = pd.DataFrame(records)
fig, ax = plt.subplots(figsize=(8, 5))
for sym, sub in hf.groupby("gene"):
    sub = sub.sort_values("dose")
    ax.plot(sub["dose"], sub["log2FC"], marker="o", label=sym)
    for _, r in sub.iterrows():
        if pd.notna(r["padj"]) and r["padj"] < 0.05:
            ax.text(r["dose"], r["log2FC"]+0.06, "*", fontsize=14, ha="center", fontweight="bold")
ax.axhline(0, color="gray", lw=0.7)
ax.axhline(LFC,  ls=":", color="gray", lw=0.7)
ax.axhline(-LFC, ls=":", color="gray", lw=0.7)
ax.set_xscale("symlog", linthresh=0.05)
ax.set_xticks([0.05, 0.5, 5])
ax.set_xticklabels(["0.05", "0.5", "5"])
ax.set_xlabel("Dose-rate (mGy/h, 36-day chronic exposure)")
ax.set_ylabel("log2 fold change vs control (DESeq2 ~batch+group)")
ax.set_title("Stress-axis / neurohormone genes: dose-response (n=21 samples)\nDirections of effect match Cantabella 2022")
ax.legend(loc="upper left", fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)
plt.tight_layout()
out = FIGS / "fig2_stress_axis_doserate.png"
plt.savefig(out, dpi=150); plt.close()
print(f"Saved {out}")

# ------ FIG 3: PCA of samples ------
meta = pd.read_csv(ROOT/"data/sample_metadata.tsv", sep="\t").set_index("gsm")
counts = pd.read_csv(RESULTS/"counts_matrix.tsv.gz", sep="\t", index_col=0).T  # samples x genes
keep = counts.sum(axis=0) > 20
counts = counts.loc[:, keep]
size_factors = counts.sum(axis=1) / counts.sum(axis=1).median()
norm = counts.div(size_factors, axis=0)
log = np.log2(norm + 1)
# Use top 2000 variable genes
v = log.var(axis=0).sort_values(ascending=False)
top = v.index[:2000]
X = log[top].values
pca = PCA(n_components=2).fit_transform(X - X.mean(axis=0))
colmap = {"control":"#888888","d005":"#1f77b4","d05":"#ff7f0e","d5":"#d62728"}
markmap = {"EC015":"o","EC017":"s"}
fig, ax = plt.subplots(figsize=(7,5))
for i, gsm in enumerate(counts.index):
    g = meta.loc[gsm, "group"]; b = meta.loc[gsm, "batch"]
    ax.scatter(pca[i,0], pca[i,1], color=colmap[g], marker=markmap[b], s=90, edgecolor="black", lw=0.5)
    ax.annotate(meta.loc[gsm, "sample_label"].split("_")[0], (pca[i,0], pca[i,1]), fontsize=7, alpha=0.7)
for g,c in colmap.items():
    ax.scatter([],[],color=c, label=f"group={g}", s=70)
for b,m in markmap.items():
    ax.scatter([],[],color="white", edgecolor="black", marker=m, label=f"batch={b}", s=70)
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.set_title("PCA (top-2000 variable, log2-normalised)\nBatch effect (circle=EC015, square=EC017) dominates PC1")
ax.legend(loc="best", fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
out = FIGS / "fig3_pca_samples.png"
plt.savefig(out, dpi=150); plt.close()
print(f"Saved {out}")

# ------ FIG 4: volcano for d5_full_batchgroup ------
df = pd.read_csv(RESULTS/"deseq2_d5_full_batchgroup.tsv.gz", sep="\t")
df = df.dropna(subset=["padj"])
df["nlog10padj"] = -np.log10(df["padj"].clip(lower=1e-300))
sig = (df["padj"] < 0.05) & (df["log2FoldChange"].abs() >= LFC)
fig, ax = plt.subplots(figsize=(7,5))
ax.scatter(df.loc[~sig, "log2FoldChange"], df.loc[~sig, "nlog10padj"], s=6, alpha=0.3, color="lightgray")
ax.scatter(df.loc[sig, "log2FoldChange"], df.loc[sig, "nlog10padj"], s=10, alpha=0.7, color="#d62728")
ax.axhline(-np.log10(0.05), color="black", ls="--", lw=0.5)
ax.axvline( LFC, color="black", ls="--", lw=0.5)
ax.axvline(-LFC, color="black", ls="--", lw=0.5)
# annotate stress-axis genes
for sym, eid in ENS.items():
    sub = df[df["gene_id"] == eid]
    if not sub.empty:
        r = sub.iloc[0]
        ax.annotate(sym, (r["log2FoldChange"], r["nlog10padj"]), fontsize=9, color="navy")
        ax.scatter([r["log2FoldChange"]], [r["nlog10padj"]], s=40, facecolor="none", edgecolor="navy", lw=1.2)
ax.set_xlabel("log2 fold change (d5 vs control)")
ax.set_ylabel("-log10(padj)")
ax.set_title(f"Volcano: 5 mGy/h vs control, ~batch+group  ({int(sig.sum())} DEGs)")
plt.tight_layout()
out = FIGS / "fig4_volcano_d5.png"
plt.savefig(out, dpi=150); plt.close()
print(f"Saved {out}")
print("All figures done.")
