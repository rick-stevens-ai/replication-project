#!/usr/bin/env python3
"""
Smoke-test replication of the headline transcriptomic claims in
Ruiz-Fernandez de Cordoba et al. 2025
(STTT, DOI 10.1038/s41392-025-02271-2).

The paper isolated CTC-in subpopulations from ANV5 (CTC700, CTC803) and 4T1
(CTC1589, CTC1592) parental lines and compared their transcriptomes
to the matched parental cells by RNA-seq.  The deposited matrix in GSE277249
is gene-level featureCounts against GENCODE vM32 (mouse).

Headline claims we can check from this matrix alone:

  (H1) ENPP1 is up-regulated in CTC-in vs parental in BOTH lineages
       (paper Fig. 1c,d; Fig. 1d shows RT-qPCR validation).

  (H2) The signature genes called out in Fig. 1c
       (TIMELESS, STAT5a/Stat5a, ERN1) are up in CTC-in.

  (H3) CD24a and NUDT21 are DOWN in CTC-in (paper text + Supp. Fig. 1c).

  (H4) DEGs in CTC-in vs parental are enriched in GO categories
       compatible with "Response to radiation", "Stemness", "Inflammatory
       response", "Tissue remodeling" (paper Fig. 1b).

We compute DEGs with PyDESeq2 separately within each parental lineage
(ANV5 family: parental ANV5 vs pooled CTC700+CTC803;
 4T1 family:  parental 4T1  vs pooled CTC1589+CTC1592).
The 'B > 5' moderated-t statistic of the paper (limma) is *not* DESeq2,
so we do not expect identical gene lists, but the direction and
biological pathway enrichment should agree.

Outputs (results/):
  deg_ANV5.tsv, deg_4T1.tsv      : full DESeq2 tables
  hypothesis_check.json          : pass/fail per claim
  ego_<lineage>.tsv              : GO BP enrichment (gseapy enrichr / Mouse)

Figures (figures/):
  fig1_pca.png                   : PCA of samples
  fig2_enpp1_counts.png          : normalized ENPP1 expression by group
  fig3_signature_heatmap.png     : log2(normalized+1) heatmap of signature genes
"""

from __future__ import annotations

import json
import os
import warnings
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

# ----------------------------------------------------------------------------
# 1. Load matrix + sample sheet, build gene symbol map
# ----------------------------------------------------------------------------

counts = pd.read_csv(os.path.join(RES, "counts_matrix.tsv"), sep="\t", index_col="Geneid")
length_col = counts.pop("Length")
sheet = pd.read_csv(os.path.join(RES, "sample_sheet.tsv"), sep="\t")
sheet = sheet.set_index("sample").loc[counts.columns]

print(f"[smoke] counts: {counts.shape}, samples: {len(sheet)}")
print(sheet["cell_line"].value_counts().to_string())

# Mouse Ensembl -> symbol mapping via mygene (offline-safe: try local cache, else hit API)
def fetch_gene_symbols(ensembl_ids: List[str]) -> pd.DataFrame:
    cache = os.path.join(RES, "ensembl_symbol_mouse.tsv")
    have = pd.read_csv(cache, sep="\t") if os.path.exists(cache) else pd.DataFrame()

    needed = set(ensembl_ids) - set(have.get("ensembl", []))
    if needed:
        try:
            import mygene  # type: ignore

            mg = mygene.MyGeneInfo()
            out = mg.querymany(
                list(needed),
                scopes="ensembl.gene",
                fields="symbol,name",
                species="mouse",
                returnall=False,
                verbose=False,
            )
            rows = []
            for r in out:
                rows.append(
                    dict(
                        ensembl=r.get("query"),
                        symbol=r.get("symbol"),
                        name=r.get("name"),
                    )
                )
            add = pd.DataFrame(rows).drop_duplicates("ensembl")
            have = pd.concat([have, add], ignore_index=True).drop_duplicates("ensembl")
            have.to_csv(cache, sep="\t", index=False)
        except Exception as exc:  # pragma: no cover
            print(f"[smoke] mygene unavailable ({exc}); using Ensembl IDs only")
    return have.set_index("ensembl") if not have.empty else pd.DataFrame(columns=["symbol"])


# Strip version suffix on Ensembl IDs: ENSMUSG00000....N -> ENSMUSG00000....
counts.index = counts.index.str.replace(r"\.\d+$", "", regex=True)
counts = counts.groupby(counts.index).sum()  # safe even if no dupes
print(f"[smoke] counts after dedupe: {counts.shape}")

gene_map = fetch_gene_symbols(counts.index.tolist())
print(f"[smoke] symbols mapped: {len(gene_map)} / {len(counts)}")

# ----------------------------------------------------------------------------
# 2. DESeq2 differential expression: CTC-in vs parental within each lineage
# ----------------------------------------------------------------------------

from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

results: Dict[str, pd.DataFrame] = {}
for lineage in ["ANV5", "4T1"]:
    keep = sheet.index[sheet["parental"] == lineage]
    sub_counts = counts[keep].T.astype(int)  # samples x genes
    sub_sheet = sheet.loc[keep, ["group"]].copy()
    sub_sheet["group"] = pd.Categorical(sub_sheet["group"], categories=["parental", "CTC_in"])

    dds = DeseqDataSet(
        counts=sub_counts,
        metadata=sub_sheet,
        design_factors="group",
        refit_cooks=True,
        quiet=True,
    )
    dds.deseq2()
    ds = DeseqStats(dds, contrast=["group", "CTC_in", "parental"], quiet=True)
    ds.summary()
    res = ds.results_df.copy()
    res["ensembl"] = res.index
    res = res.join(gene_map[["symbol", "name"]], how="left")
    res = res.sort_values("padj", na_position="last")
    out = os.path.join(RES, f"deg_{lineage}.tsv")
    res.to_csv(out, sep="\t", index=False)
    print(f"[smoke] {lineage}: wrote {out} ({(res['padj'] < 0.05).sum()} sig at padj<0.05)")
    results[lineage] = res


# ----------------------------------------------------------------------------
# 3. Hypothesis checks
# ----------------------------------------------------------------------------

def lookup(res: pd.DataFrame, symbol: str) -> dict:
    sym_lc = symbol.lower()
    sub = res[res["symbol"].astype(str).str.lower() == sym_lc]
    if sub.empty:
        return dict(found=False, symbol=symbol)
    row = sub.iloc[0]
    return dict(
        found=True,
        symbol=symbol,
        ensembl=row["ensembl"],
        log2fc=float(row["log2FoldChange"]),
        padj=float(row["padj"]) if not pd.isna(row["padj"]) else None,
        baseMean=float(row["baseMean"]),
    )


hypotheses = {
    "H1_ENPP1_up": {"genes": ["Enpp1"], "direction": "up", "lineages": ["ANV5", "4T1"]},
    "H2a_TIMELESS_up": {"genes": ["Timeless"], "direction": "up", "lineages": ["ANV5", "4T1"]},
    "H2b_STAT5a_up": {"genes": ["Stat5a"], "direction": "up", "lineages": ["ANV5", "4T1"]},
    "H2c_ERN1_up": {"genes": ["Ern1"], "direction": "up", "lineages": ["ANV5", "4T1"]},
    "H3a_Cd24a_down": {"genes": ["Cd24a"], "direction": "down", "lineages": ["ANV5", "4T1"]},
    "H3b_Nudt21_down": {"genes": ["Nudt21"], "direction": "down", "lineages": ["ANV5", "4T1"]},
}

check = {}
for h, spec in hypotheses.items():
    per = {}
    for lineage in spec["lineages"]:
        info = lookup(results[lineage], spec["genes"][0])
        if info["found"]:
            if spec["direction"] == "up":
                info["direction_ok"] = info["log2fc"] > 0
            else:
                info["direction_ok"] = info["log2fc"] < 0
            info["sig_padj_lt_0p05"] = (info["padj"] is not None) and (info["padj"] < 0.05)
        per[lineage] = info
    per["consistent_direction"] = all(
        per[l].get("direction_ok", False) for l in spec["lineages"]
    )
    per["consistent_significant"] = all(
        per[l].get("sig_padj_lt_0p05", False) for l in spec["lineages"]
    )
    check[h] = per

# ----------------------------------------------------------------------------
# 4. Pathway enrichment (Enrichr / gseapy) on intersected up-DEGs
# ----------------------------------------------------------------------------

def top_up_symbols(res: pd.DataFrame, padj_cut: float = 0.05, lfc_cut: float = 1.0) -> List[str]:
    sub = res[(res["padj"] < padj_cut) & (res["log2FoldChange"] > lfc_cut)]
    return [s for s in sub["symbol"].dropna().tolist() if s]


up_anv5 = top_up_symbols(results["ANV5"])
up_4t1 = top_up_symbols(results["4T1"])
common_up = sorted(set(up_anv5) & set(up_4t1))
print(
    f"[smoke] up-DEGs ANV5: {len(up_anv5)}, 4T1: {len(up_4t1)}, intersection: {len(common_up)}"
)

enrich_summary = {}
try:
    import gseapy as gp

    if common_up:
        enr = gp.enrichr(
            gene_list=common_up,
            gene_sets="GO_Biological_Process_2023",
            organism="mouse",
            outdir=os.path.join(RES, "enrichr_common_up"),
            no_plot=True,
            verbose=False,
        )
        enrich_summary["common_up"] = enr.res2d.head(15).to_dict(orient="records")
except Exception as exc:
    print(f"[smoke] enrichr skipped: {exc}")

# ----------------------------------------------------------------------------
# 5. Figures
# ----------------------------------------------------------------------------

# Fig 1: PCA on log-CPM
from numpy.linalg import svd

lib = counts.sum(axis=0)
cpm = (counts.divide(lib, axis=1) * 1e6).fillna(0)
logcpm = np.log2(cpm + 1)
# keep most-variable genes
var = logcpm.var(axis=1).sort_values(ascending=False)
top = var.head(2000).index
X = logcpm.loc[top].T.values
X = X - X.mean(axis=0, keepdims=True)
U, S, VT = svd(X, full_matrices=False)
pc = U[:, :2] * S[:2]

fig, ax = plt.subplots(figsize=(6, 5))
colors = {
    "ANV5_parental": "tab:blue",
    "CTC700": "tab:cyan",
    "CTC803": "tab:purple",
    "4T1_parental": "tab:red",
    "CTC1589": "tab:orange",
    "CTC1592": "tab:pink",
}
for cl, c in colors.items():
    idx = np.array([sheet.loc[s, "cell_line"] == cl for s in counts.columns])
    ax.scatter(pc[idx, 0], pc[idx, 1], c=c, label=cl, s=60, edgecolor="k", linewidth=0.5)
total = (S ** 2) / (S ** 2).sum()
ax.set_xlabel(f"PC1 ({total[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({total[1]*100:.1f}%)")
ax.set_title("GSE277249 — PCA of top-2000 variable genes (log2 CPM)")
ax.legend(fontsize=8, loc="best")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig1_pca.png"), dpi=150)
plt.close()

# Fig 2: ENPP1 normalized counts per group
def enpp1_counts() -> pd.Series:
    # find ENPP1 by symbol via gene_map
    ens = gene_map.index[gene_map["symbol"].astype(str).str.lower() == "enpp1"]
    if len(ens) == 0:
        return pd.Series(dtype=float)
    e = ens[0]
    return counts.loc[e]


enpp1 = enpp1_counts()
fig, ax = plt.subplots(figsize=(7, 4))
if not enpp1.empty:
    order = [
        "ANV5_parental",
        "CTC700",
        "CTC803",
        "4T1_parental",
        "CTC1589",
        "CTC1592",
    ]
    pos = []
    for i, cl in enumerate(order):
        samps = sheet.index[sheet["cell_line"] == cl]
        y = enpp1[samps].values
        ax.scatter([i] * len(y), y, s=70, c=colors[cl], edgecolor="k", linewidth=0.5)
        ax.plot([i - 0.2, i + 0.2], [np.mean(y)] * 2, "k-", lw=2)
        pos.append(i)
    ax.set_xticks(pos)
    ax.set_xticklabels(order, rotation=20, ha="right")
    ax.set_ylabel("ENPP1 raw counts")
    ax.set_yscale("log")
    ax.set_title("ENPP1 expression: parental vs CTC-in (GSE277249)")
else:
    ax.text(0.5, 0.5, "ENPP1 (Enpp1) not mapped", ha="center")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig2_enpp1_counts.png"), dpi=150)
plt.close()

# Fig 3: heatmap of signature genes (Fig. 1c set)
SIG = [
    "Enpp1",
    "Timeless",
    "Stat5a",
    "Ern1",
    "Aldh1a3",
    "Lgr5",
    "Bmi1",
    "Sox2",
    "Cd24a",
    "Nudt21",
    "Cd44",
    "Brca1",
    "Brca2",
    "Atm",
    "Atr",
    "Rad51",
    "Parp1",
    "H2ax",
    "H2afx",
]
sym_to_ens = {s.lower(): e for e, s in zip(gene_map.index, gene_map["symbol"].astype(str))}
ens_for = [sym_to_ens.get(s.lower()) for s in SIG]
mask = [(e is not None and e in counts.index) for e in ens_for]
SIG_kept = [s for s, k in zip(SIG, mask) if k]
ens_kept = [e for e, k in zip(ens_for, mask) if k]
mat = np.log2(counts.loc[ens_kept] + 1)
mat.index = SIG_kept
# Z-score by row
z = (mat.subtract(mat.mean(axis=1), axis=0)).divide(mat.std(axis=1).replace(0, 1), axis=0)
# Order columns by lineage
col_order = []
for cl in [
    "ANV5_parental",
    "CTC700",
    "CTC803",
    "4T1_parental",
    "CTC1589",
    "CTC1592",
]:
    col_order += list(sheet.index[sheet["cell_line"] == cl])
z = z[col_order]
fig, ax = plt.subplots(figsize=(8.5, max(3, 0.3 * len(SIG_kept) + 1)))
im = ax.imshow(z.values, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
ax.set_yticks(range(len(SIG_kept)))
ax.set_yticklabels(SIG_kept)
ax.set_xticks(range(len(col_order)))
ax.set_xticklabels(col_order, rotation=70, ha="right", fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.6, label="Row z-score (log2 counts+1)")
ax.set_title("CTC signature genes (paper Fig. 1c set)")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig3_signature_heatmap.png"), dpi=150)
plt.close()

# ----------------------------------------------------------------------------
# 6. Summary JSON
# ----------------------------------------------------------------------------
summary = dict(
    counts_shape=list(counts.shape),
    samples=int(counts.shape[1]),
    n_sig_padj_0p05=dict(
        ANV5=int((results["ANV5"]["padj"] < 0.05).sum()),
        T4T1=int((results["4T1"]["padj"] < 0.05).sum()),
    ),
    up_DEGs=dict(
        ANV5=len(up_anv5),
        T4T1=len(up_4t1),
        intersection=len(common_up),
    ),
    hypothesis_checks=check,
    pathway_top_intersect_up=enrich_summary.get("common_up", []),
)

out_json = os.path.join(RES, "hypothesis_check.json")
with open(out_json, "w") as fh:
    json.dump(summary, fh, indent=2, default=str)
print(f"[smoke] wrote {out_json}")

# Compact stdout summary
print("\n=== Hypothesis verdicts ===")
for h, per in check.items():
    print(f"  {h}: dir_consistent={per['consistent_direction']} sig_consistent={per['consistent_significant']}")
print("\n=== Top common-up enriched GO BP (Enrichr) ===")
for row in enrich_summary.get("common_up", [])[:10]:
    print(f"  {row.get('Term')}  q={row.get('Adjusted P-value'):.2e}  hits={row.get('Overlap')}")
