#!/usr/bin/env python3
"""
LUCID-100 slot 35 — Villa et al. 2021 (doi:10.1038/s41598-021-91335-8)
Quantitative DESeq2 replication of supplementary tables S3-S7 from
GEO GSE176207 processed htseq counts.

This is the PASS-mid analysis the FIRST_PASS_REPORT planned for: it
runs PyDeseq2 on the 12 RNA-seq samples and 6 MAPS samples and
compares the reproduced log2FC and padj values against the published
supplement values from artifacts/supplement1.xlsx.

Contrasts:
  S4: PprSKD-0  vs WT-0       (sham, KD effect)
  S5: PprSKD-10 vs WT-10      (10 kGy, KD effect)
  S6: WT-10     vs WT-0       (IR effect in WT)
  S7: PprSKD-10 vs PprSKD-0   (IR effect in PprSKD)
  S3: MS2-PprS  vs MS2-blank  (MAPS pull-down enrichment)

Outputs:
  results/deseq2_<contrast>.tsv
  results/deseq2_comparison_<contrast>.tsv  -- merged with paper supplement
  results/deseq2_summary.json                -- agreement metrics per contrast
  figures/deseq2_<contrast>_scatter.png
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr

from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GEO = ROOT / "data" / "geo_GSE176207"
SUPPL = ROOT / "artifacts" / "supplement1.xlsx"
RES = ROOT / "results"
FIGS = ROOT / "figures"
RES.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)

RNASEQ = {
    "GSM5360101_KO2A0":  ("PprSKD", "A", "0"),
    "GSM5360102_KO2A10": ("PprSKD", "A", "10"),
    "GSM5360103_KO2B0":  ("PprSKD", "B", "0"),
    "GSM5360104_KO2B10": ("PprSKD", "B", "10"),
    "GSM5360105_KO2C0":  ("PprSKD", "C", "0"),
    "GSM5360106_KO2C10": ("PprSKD", "C", "10"),
    "GSM5360107_WTA0":   ("WT",     "A", "0"),
    "GSM5360108_WTA10":  ("WT",     "A", "10"),
    "GSM5360109_WTB0":   ("WT",     "B", "0"),
    "GSM5360110_WTB10":  ("WT",     "B", "10"),
    "GSM5360111_WTC0":   ("WT",     "C", "0"),
    "GSM5360112_WTC10":  ("WT",     "C", "10"),
}

MAPS = {
    "GSM5360113_MS2blankA": ("MS2blank", "A"),
    "GSM5360114_MS2blankB": ("MS2blank", "B"),
    "GSM5360115_MS2blankC": ("MS2blank", "C"),
    "GSM5360116_MS2Dsr2A":  ("MS2PprS",  "A"),
    "GSM5360117_MS2Dsr2B":  ("MS2PprS",  "B"),
    "GSM5360118_MS2Dsr2C":  ("MS2PprS",  "C"),
}

HTSEQ_DIAG_PREFIXES = (
    "__no_feature", "__ambiguous", "__too_low_aQual",
    "__not_aligned", "__alignment_not_unique",
)


def load_counts(samples: dict) -> pd.DataFrame:
    cols = {}
    for stem in samples:
        matches = list(GEO.glob(stem + "*.gz"))
        if not matches:
            raise FileNotFoundError(stem)
        path = matches[0]
        with gzip.open(path, "rt") as fh:
            df = pd.read_csv(fh, sep="\t", header=None, names=["gene", "count"])
        df = df[~df["gene"].str.startswith("__")]
        df = df.set_index("gene")["count"].astype(int)
        cols[stem] = df
    counts = pd.DataFrame(cols)
    counts = counts.fillna(0).astype(int)
    return counts


def run_deseq(counts: pd.DataFrame, metadata: pd.DataFrame, design: str,
              contrast: list) -> pd.DataFrame:
    # PyDeseq2 expects samples x genes
    counts_t = counts.T
    inference = DefaultInference(n_cpus=2)
    dds = DeseqDataSet(
        counts=counts_t,
        metadata=metadata,
        design=design,
        refit_cooks=True,
        inference=inference,
        quiet=True,
    )
    dds.deseq2()
    ds = DeseqStats(dds, contrast=contrast, inference=inference, quiet=True)
    ds.summary()
    out = ds.results_df.copy()
    out.index.name = "gene"
    return out


def load_paper_table(sheet: str, gene_col_hdr: str = "GeneID",
                     l2fc_hdr: str = "Log2FoldChange",
                     padj_hdr: str = "padj") -> pd.DataFrame:
    """Read a supplement sheet, return DataFrame with index=gene, paper_l2fc, paper_padj."""
    df = pd.read_excel(SUPPL, sheet_name=sheet, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    # Find gene column (S4 uses 'GeneID', S3/S5/S6/S7 use 'Gene Number')
    gene_col = None
    for c in df.columns:
        if c in ("GeneID", "Gene Number", "Gene_Number", "GeneNumber"):
            gene_col = c
            break
    if gene_col is None:
        # fall back to first column
        gene_col = df.columns[0]
    l2fc_col = None
    padj_col = None
    for c in df.columns:
        lc = c.lower().replace("-", "").replace("_", "").replace(" ", "")
        if lc in ("log2foldchange", "log2fc"):
            l2fc_col = c
        if lc == "padj":
            padj_col = c
    if l2fc_col is None or padj_col is None:
        raise RuntimeError(f"Could not find L2FC/padj columns in {sheet}: {df.columns.tolist()}")
    out = pd.DataFrame({
        "gene": df[gene_col].astype(str).str.strip(),
        "paper_l2fc": pd.to_numeric(df[l2fc_col], errors="coerce"),
        "paper_padj": pd.to_numeric(df[padj_col], errors="coerce"),
    }).dropna(subset=["gene"])
    out = out[out["gene"] != ""].set_index("gene")
    return out


def compare_and_plot(label: str, my_res: pd.DataFrame, paper: pd.DataFrame,
                     padj_threshold: float = 0.05):
    merged = paper.join(my_res[["log2FoldChange", "padj"]], how="left")
    merged = merged.rename(columns={"log2FoldChange": "repro_l2fc", "padj": "repro_padj"})
    merged["sign_match"] = np.sign(merged["paper_l2fc"]) == np.sign(merged["repro_l2fc"])

    out_csv = RES / f"deseq2_comparison_{label}.tsv"
    merged.to_csv(out_csv, sep="\t")

    sub = merged.dropna(subset=["repro_l2fc"])
    n = len(sub)
    metrics = {
        "n_paper_genes": int(len(paper)),
        "n_with_repro_value": int(n),
    }
    if n >= 3:
        sr, sp = spearmanr(sub["paper_l2fc"], sub["repro_l2fc"])
        pr, pp = pearsonr(sub["paper_l2fc"], sub["repro_l2fc"])
        metrics["spearman_l2fc"] = float(sr)
        metrics["spearman_l2fc_pvalue"] = float(sp)
        metrics["pearson_l2fc"] = float(pr)
        metrics["pearson_l2fc_pvalue"] = float(pp)
        metrics["sign_concordance"] = float(sub["sign_match"].sum() / n)
        # padj concordance: paper is sig at 0.05; in repro is padj < 0.05?
        repro_sig = (sub["repro_padj"] < padj_threshold).sum()
        metrics["n_paper_sig_at_0.05"] = int((sub["paper_padj"] < padj_threshold).sum())
        metrics["n_repro_sig_at_0.05_among_paper_genes"] = int(repro_sig)
        metrics["padj_concordance_at_0.05"] = float(
            ((sub["paper_padj"] < padj_threshold) ==
             (sub["repro_padj"] < padj_threshold)).sum() / n
        )

    # scatter
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.scatter(sub["paper_l2fc"], sub["repro_l2fc"], s=18, alpha=0.7)
    lim_min = float(np.nanmin([sub["paper_l2fc"].min(), sub["repro_l2fc"].min()]))
    lim_max = float(np.nanmax([sub["paper_l2fc"].max(), sub["repro_l2fc"].max()]))
    ax.plot([lim_min, lim_max], [lim_min, lim_max], "k--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel(f"Paper L2FC ({label})")
    ax.set_ylabel(f"Reproduced L2FC ({label})")
    title = f"{label}: n={n}"
    if "spearman_l2fc" in metrics:
        title += f", Spearman={metrics['spearman_l2fc']:.3f}, sign={metrics['sign_concordance']:.0%}"
    ax.set_title(title)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)
    fig.tight_layout()
    fig.savefig(FIGS / f"deseq2_{label}_scatter.png", dpi=130)
    plt.close(fig)

    return metrics


def main():
    summary = {}

    # ---- RNA-seq DESeq2 ----
    print("Loading RNA-seq counts…")
    rna = load_counts(RNASEQ)
    print(f"  counts: {rna.shape[0]} genes x {rna.shape[1]} samples")
    print(f"  library sizes: {rna.sum().to_dict()}")

    rna_meta = pd.DataFrame.from_dict(
        {s: {"strain": v[0], "replicate": v[1], "dose": v[2]} for s, v in RNASEQ.items()},
        orient="index",
    )
    rna_meta["group"] = rna_meta["strain"] + "_" + rna_meta["dose"]
    rna_meta.to_csv(RES / "rnaseq_metadata.tsv", sep="\t")

    # Single group factor + custom contrasts: ['group', A, B] -> log2(A/B)
    print("Running DESeq2 with design ~group …")
    # Get full DESeq2 fit once and then extract each contrast
    counts_t = rna.T
    inference = DefaultInference(n_cpus=2)
    dds = DeseqDataSet(
        counts=counts_t,
        metadata=rna_meta,
        design="~group",
        refit_cooks=True,
        inference=inference,
        quiet=True,
    )
    dds.deseq2()

    rna_contrasts = {
        "S4_PprSKD0_vs_WT0":       ("PprSKD_0",  "WT_0"),
        "S5_PprSKD10_vs_WT10":     ("PprSKD_10", "WT_10"),
        "S6_WT10_vs_WT0":          ("WT_10",     "WT_0"),
        "S7_PprSKD10_vs_PprSKD0":  ("PprSKD_10", "PprSKD_0"),
    }
    sheet_map = {
        "S4_PprSKD0_vs_WT0":      "Table S4",
        "S5_PprSKD10_vs_WT10":    "Table S5",
        "S6_WT10_vs_WT0":         "Table S6",
        "S7_PprSKD10_vs_PprSKD0": "Table S7",
    }

    for label, (numerator, denominator) in rna_contrasts.items():
        print(f"  contrast {label}: log2({numerator}/{denominator})")
        ds = DeseqStats(dds, contrast=["group", numerator, denominator],
                        inference=inference, quiet=True)
        ds.summary()
        res = ds.results_df.copy()
        res.index.name = "gene"
        res.to_csv(RES / f"deseq2_{label}.tsv", sep="\t")
        sheet = sheet_map[label]
        paper = load_paper_table(sheet)
        metrics = compare_and_plot(label, res, paper)
        # pprM specifically
        if "DR_0907" in res.index:
            metrics["DR_0907_repro_l2fc"] = float(res.loc["DR_0907", "log2FoldChange"])
            metrics["DR_0907_repro_padj"] = (
                float(res.loc["DR_0907", "padj"]) if not pd.isna(res.loc["DR_0907", "padj"]) else None
            )
        if "DR_0907" in paper.index:
            metrics["DR_0907_paper_l2fc"] = float(paper.loc["DR_0907", "paper_l2fc"])
            metrics["DR_0907_paper_padj"] = float(paper.loc["DR_0907", "paper_padj"])
        summary[label] = metrics
        print(f"    n_paper={metrics['n_paper_genes']}, n_with_repro={metrics['n_with_repro_value']}, "
              f"sign={metrics.get('sign_concordance', 'NA')}")

    # ---- MAPS DESeq2 ----
    print("Loading MAPS counts…")
    maps = load_counts(MAPS)
    print(f"  counts: {maps.shape[0]} genes x {maps.shape[1]} samples")
    maps_meta = pd.DataFrame.from_dict(
        {s: {"strain": v[0], "replicate": v[1]} for s, v in MAPS.items()},
        orient="index",
    )
    maps_meta.to_csv(RES / "maps_metadata.tsv", sep="\t")

    counts_t = maps.T
    dds_maps = DeseqDataSet(
        counts=counts_t,
        metadata=maps_meta,
        design="~strain",
        refit_cooks=True,
        inference=inference,
        quiet=True,
    )
    dds_maps.deseq2()
    ds_maps = DeseqStats(dds_maps, contrast=["strain", "MS2PprS", "MS2blank"],
                         inference=inference, quiet=True)
    ds_maps.summary()
    maps_res = ds_maps.results_df.copy()
    maps_res.index.name = "gene"
    maps_res.to_csv(RES / "deseq2_S3_MAPS_PprS_vs_blank.tsv", sep="\t")

    # Compare to Table S3 (MAPS L2FC + padj)
    s3 = load_paper_table("Table S3")
    metrics = compare_and_plot("S3_MAPS_PprS_vs_blank", maps_res, s3)
    # paper claim: ~130 interactors at sig threshold; let's see how many MAPS L2FC > 0 and padj < 0.05
    repro_sig = maps_res[(maps_res["padj"] < 0.05) & (maps_res["log2FoldChange"] > 0)]
    paper_sig = s3[(s3["paper_padj"] < 0.05) & (s3["paper_l2fc"] > 0)]
    overlap = set(repro_sig.index) & set(paper_sig.index)
    metrics["n_paper_interactors_padj_lt_0.05_pos_l2fc"] = int(len(paper_sig))
    metrics["n_repro_interactors_padj_lt_0.05_pos_l2fc"] = int(len(repro_sig))
    metrics["n_overlap_interactors"] = int(len(overlap))
    metrics["jaccard_interactors"] = (
        float(len(overlap) / len(set(repro_sig.index) | set(paper_sig.index)))
        if (len(repro_sig) + len(paper_sig)) else 0.0
    )
    if "DR_0907" in maps_res.index:
        metrics["DR_0907_repro_l2fc"] = float(maps_res.loc["DR_0907", "log2FoldChange"])
        metrics["DR_0907_repro_padj"] = (
            float(maps_res.loc["DR_0907", "padj"]) if not pd.isna(maps_res.loc["DR_0907", "padj"]) else None
        )
    if "DR_0907" in s3.index:
        metrics["DR_0907_paper_l2fc"] = float(s3.loc["DR_0907", "paper_l2fc"])
        metrics["DR_0907_paper_padj"] = float(s3.loc["DR_0907", "paper_padj"])
    summary["S3_MAPS_PprS_vs_blank"] = metrics
    print(f"  MAPS: n_paper_interactors={metrics['n_paper_interactors_padj_lt_0.05_pos_l2fc']}, "
          f"n_repro={metrics['n_repro_interactors_padj_lt_0.05_pos_l2fc']}, "
          f"overlap={metrics['n_overlap_interactors']}")

    with open(RES / "deseq2_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=str)
    print("\nSummary written to", RES / "deseq2_summary.json")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
