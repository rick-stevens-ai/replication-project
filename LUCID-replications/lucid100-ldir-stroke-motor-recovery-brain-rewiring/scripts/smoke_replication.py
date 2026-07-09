#!/usr/bin/env python3
"""
LUCID100 slot 52 smoke replication
Paper: Au et al. 2024, Brain Behav Immun (DOI 10.1016/j.bbi.2023.09.015)
Dataset: GEO GSE244016 (24 mouse cortex RNA-seq samples, 300 mGy X-ray vs sham,
naive + D1/D3/D7 post-photothrombotic-stroke ipsilateral cortex).

Smoke claims tested (lightweight, no DESeq2 install needed):
  (S1) Build a 24-sample raw counts matrix from GEO RAW files.
  (S2) Library-size + TMM-like CPM normalization, log2(CPM+1).
  (S3) For each timepoint (D1, D3, D7), compute Welch t-test of
       log2(CPM+1) between LDIR (300 mGy) and Sham (n=3 vs n=3).
  (S4) Count "LDIR-upregulated" genes (logFC>0.585, p<0.05) and
       check enrichment in curated microglia / inflammation / phagocytosis
       gene sets vs background; report Fisher exact OR + p.
  (S5) Test the paper's narrative direction: at D3 (peak inflammatory
       resolution window per paper), pro-inflammatory cytokines should be
       DOWN in LDIR vs Sham; anti-inflammatory + phagocytosis markers UP.

Outputs (written to ../results/):
  counts_matrix.tsv, cpm_log2.tsv, sample_meta.tsv
  de_<timepoint>.tsv  (per-gene logFC + p)
  smoke_summary.json  (structured verdict)
  smoke_summary.md    (human readable)
"""
from __future__ import annotations
import gzip, json, os, sys, re, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW  = ROOT / "artifacts" / "GSE244016_RAW"
OUT  = ROOT / "results"
OUT.mkdir(exist_ok=True, parents=True)

# ---- 1. parse sample sheet from filenames -------------------------------
PAT = re.compile(r"(GSM\d+)_(.+)\.txt\.gz$")
def parse_label(label: str) -> dict:
    """Convert e.g. 'D1-Stroke-300mGy-X-ray-Ipsi-1' into structured fields."""
    L = label
    rec = {"label": L, "timepoint": "naive", "stroke": False,
           "dose_mGy": 0, "rep": None}
    m = re.match(r"^D(\d+)-Stroke-(Sham|300mGy-X-ray)-Ipsi-(\d+)$", L)
    if m:
        rec["timepoint"] = f"D{m.group(1)}"
        rec["stroke"] = True
        rec["dose_mGy"] = 0 if m.group(2) == "Sham" else 300
        rec["rep"] = int(m.group(3))
        return rec
    m = re.match(r"^Naive-(Sham|300mGy-X-ray)-Cortex-(\d+)$", L)
    if m:
        rec["dose_mGy"] = 0 if m.group(1) == "Sham" else 300
        rec["rep"] = int(m.group(2))
        return rec
    raise ValueError(f"Unparsed label: {L}")

def load_counts() -> tuple[pd.DataFrame, pd.DataFrame]:
    files = sorted(RAW.glob("GSM*.txt.gz"))
    if not files:
        raise SystemExit(f"No GSM*.txt.gz under {RAW}")
    counts, meta = {}, []
    for fp in files:
        m = PAT.search(fp.name)
        gsm, label = m.group(1), m.group(2)
        rec = parse_label(label); rec["gsm"] = gsm; rec["file"] = fp.name
        rec["group"] = f"{rec['timepoint']}_{ 'stroke' if rec['stroke'] else 'naive'}_{'LDIR' if rec['dose_mGy']>0 else 'Sham'}"
        meta.append(rec)
        df = pd.read_csv(fp, sep="\t", compression="gzip")
        # collapse duplicate gene symbols (sum counts) — common in mouse GENCODE
        s = df.groupby("GeneName")["RawCount"].sum()
        counts[gsm] = s
    M = pd.DataFrame(counts).fillna(0).astype(int)
    meta_df = pd.DataFrame(meta).set_index("gsm").loc[M.columns]
    return M, meta_df

def cpm_log2(counts: pd.DataFrame) -> pd.DataFrame:
    libsize = counts.sum(axis=0)
    cpm = counts.divide(libsize, axis=1) * 1e6
    return np.log2(cpm + 1.0)

def welch_de(expr: pd.DataFrame, group_a_cols, group_b_cols, label_a, label_b) -> pd.DataFrame:
    """logFC = mean(a) - mean(b), Welch t-test on log2 CPM."""
    A = expr[group_a_cols].to_numpy()
    B = expr[group_b_cols].to_numpy()
    mean_a, mean_b = A.mean(axis=1), B.mean(axis=1)
    logfc = mean_a - mean_b
    # filter low-expression: require mean log2cpm >= 1 in at least one arm
    keep = (mean_a >= 1) | (mean_b >= 1)
    t, p = stats.ttest_ind(A, B, axis=1, equal_var=False, nan_policy="omit")
    out = pd.DataFrame({
        "gene": expr.index,
        "mean_log2cpm_" + label_a: mean_a,
        "mean_log2cpm_" + label_b: mean_b,
        "logFC_" + label_a + "_vs_" + label_b: logfc,
        "p_welch": p,
        "keep": keep,
    })
    out = out[out["keep"]].drop(columns="keep").reset_index(drop=True)
    # BH FDR
    p_vals = out["p_welch"].fillna(1.0).values
    n = len(p_vals)
    order = np.argsort(p_vals)
    ranks = np.empty(n, dtype=int); ranks[order] = np.arange(1, n+1)
    bh = p_vals * n / ranks
    out["fdr_bh"] = np.minimum.accumulate(bh[order[::-1]])[::-1][np.argsort(order)]
    out["fdr_bh"] = np.clip(out["fdr_bh"], 0, 1)
    return out.sort_values("p_welch")

# Curated mouse gene sets (small, hand-picked; not exhaustive — smoke only)
GENE_SETS = {
    "microglia_homeostatic": [
        "Tmem119","P2ry12","Cx3cr1","Sall1","Hexb","Csf1r","Trem2","Tgfbr1","Olfml3","Sparc"
    ],
    "microglia_DAM_phagocytic": [
        "Trem2","Tyrobp","Apoe","Cst7","Cd9","Itgax","Spp1","Lpl","Axl","Cd68",
        "Cd163","Mertk","Gas6","Lyz2","Lyz1","Clec7a"
    ],
    "pro_inflammatory_cytokines": [
        "Tnf","Il1b","Il6","Ccl2","Ccl3","Ccl4","Ccl5","Cxcl1","Cxcl2","Cxcl10",
        "Nos2","Ptgs2","Nlrp3","Casp1","Il18"
    ],
    "anti_inflammatory_resolution": [
        "Il10","Tgfb1","Arg1","Mrc1","Cd206","Chil3","Ym1","Retnla","Klf4","Socs3",
        "Anxa1","Lxr","Nr4a1","Mertk"
    ],
    "axonal_projection_brain_rewiring": [
        "Gap43","Sprr1a","Bdnf","Ntrk2","Sema3a","Sema6d","Robo2","Slit1","Plxna1",
        "L1cam","Ncam1","Dcx","Stmn1","Stmn2","Stmn4","Map1b","Atf3","Sox11","Klf6","Klf7"
    ],
}

def fisher_enrich(de: pd.DataFrame, gene_col: str, lfc_col: str,
                  direction: str = "up", p_cut: float = 0.05,
                  lfc_cut: float = 0.585) -> dict:
    """Fisher exact enrichment of each GENE_SET in 'changed' subset of DE table."""
    if direction == "up":
        changed = de[(de[lfc_col] > lfc_cut) & (de["p_welch"] < p_cut)][gene_col]
    else:
        changed = de[(de[lfc_col] < -lfc_cut) & (de["p_welch"] < p_cut)][gene_col]
    bg = set(de[gene_col])
    changed = set(changed) & bg
    rows = []
    for name, gs in GENE_SETS.items():
        gs_in_bg = set(gs) & bg
        a = len(changed & gs_in_bg)
        b = len(gs_in_bg - changed)
        c = len(changed - gs_in_bg)
        d = len(bg - changed - gs_in_bg)
        if a + b == 0 or a + c == 0:
            rows.append({"set": name, "k_hit": a, "set_size_bg": len(gs_in_bg),
                         "changed_total": len(changed), "OR": float("nan"), "p": 1.0})
            continue
        OR, p = stats.fisher_exact([[a,b],[c,d]], alternative="greater")
        rows.append({"set": name, "k_hit": a, "set_size_bg": len(gs_in_bg),
                     "changed_total": len(changed), "OR": OR, "p": p,
                     "hits": sorted(changed & gs_in_bg)})
    return rows

def main():
    print(f"[smoke] loading 24 GSM count files from {RAW} ...")
    counts, meta = load_counts()
    print(f"[smoke] counts: {counts.shape[0]} genes × {counts.shape[1]} samples")
    counts.to_csv(OUT/"counts_matrix.tsv", sep="\t")
    meta.to_csv(OUT/"sample_meta.tsv", sep="\t")

    expr = cpm_log2(counts)
    expr.to_csv(OUT/"cpm_log2.tsv", sep="\t")

    summary = {"dataset":"GSE244016","n_samples":int(counts.shape[1]),
               "n_genes":int(counts.shape[0]),
               "library_sizes":counts.sum(axis=0).astype(int).to_dict(),
               "per_timepoint":{}}

    for tp in ["D1","D3","D7"]:
        ldir = meta[(meta.timepoint==tp) & (meta.dose_mGy==300) & meta.stroke].index.tolist()
        sham = meta[(meta.timepoint==tp) & (meta.dose_mGy==0)   & meta.stroke].index.tolist()
        print(f"[smoke] {tp}: LDIR={ldir}  Sham={sham}")
        if len(ldir) < 2 or len(sham) < 2:
            summary["per_timepoint"][tp] = {"error":"insufficient samples"}; continue
        de = welch_de(expr, ldir, sham, "LDIR", "Sham")
        de_path = OUT/f"de_{tp}_LDIR_vs_Sham.tsv"
        de.to_csv(de_path, sep="\t", index=False)
        lfc_col = "logFC_LDIR_vs_Sham"
        n_up   = int(((de[lfc_col]> 0.585) & (de.p_welch<0.05)).sum())
        n_down = int(((de[lfc_col]<-0.585) & (de.p_welch<0.05)).sum())
        up_enrich   = fisher_enrich(de, "gene", lfc_col, "up")
        down_enrich = fisher_enrich(de, "gene", lfc_col, "down")
        summary["per_timepoint"][tp] = {
            "ldir_samples": ldir, "sham_samples": sham,
            "n_de_genes_tested": int(len(de)),
            "n_up_LDIR_vs_Sham_p05_lfc05": n_up,
            "n_down_LDIR_vs_Sham_p05_lfc05": n_down,
            "enrichment_up_in_LDIR": up_enrich,
            "enrichment_down_in_LDIR": down_enrich,
            "de_file": de_path.name,
        }

    # Naive LDIR vs Sham as a sanity contrast (LDIR alone, no stroke)
    n_ldir = meta[(meta.timepoint=='naive') & (meta.dose_mGy==300)].index.tolist()
    n_sham = meta[(meta.timepoint=='naive') & (meta.dose_mGy==0)].index.tolist()
    if len(n_ldir)>=2 and len(n_sham)>=2:
        de = welch_de(expr, n_ldir, n_sham, "LDIR", "Sham")
        de.to_csv(OUT/"de_naive_LDIR_vs_Sham.tsv", sep="\t", index=False)
        lfc_col = "logFC_LDIR_vs_Sham"
        summary["naive_LDIR_vs_Sham"] = {
            "n_up_p05_lfc05": int(((de[lfc_col]>0.585) & (de.p_welch<0.05)).sum()),
            "n_down_p05_lfc05": int(((de[lfc_col]<-0.585) & (de.p_welch<0.05)).sum()),
        }

    with open(OUT/"smoke_summary.json","w") as fh:
        json.dump(summary, fh, indent=2, default=str)

    # Markdown render
    md = ["# Smoke replication summary — GSE244016 (LDIR + photothrombotic stroke)",""]
    md.append(f"- samples: **{summary['n_samples']}**, genes: **{summary['n_genes']}**")
    md.append(f"- library size range: {min(summary['library_sizes'].values()):,} – {max(summary['library_sizes'].values()):,}")
    md.append("")
    md.append("## DE counts per timepoint (LDIR vs Sham, stroke ipsi cortex, Welch t-test on log2(CPM+1), |logFC|>0.585, p<0.05)")
    for tp, rec in summary["per_timepoint"].items():
        if "error" in rec:
            md.append(f"- **{tp}** — skipped: {rec['error']}"); continue
        md.append(f"- **{tp}**: tested {rec['n_de_genes_tested']:,} expressed genes; "
                  f"up_in_LDIR = {rec['n_up_LDIR_vs_Sham_p05_lfc05']}, "
                  f"down_in_LDIR = {rec['n_down_LDIR_vs_Sham_p05_lfc05']}")
    md.append("")
    md.append("## Curated gene-set enrichment in LDIR-up gene list (Fisher exact, one-sided greater)")
    for tp, rec in summary["per_timepoint"].items():
        if "error" in rec: continue
        md.append(f"### {tp}")
        md.append("| set | hits/setSize | OR | p | example hits |")
        md.append("|-----|-------------|----|---|---------------|")
        for e in rec["enrichment_up_in_LDIR"]:
            hits = ", ".join(e.get("hits", [])[:8])
            md.append(f"| {e['set']} | {e['k_hit']}/{e['set_size_bg']} | "
                      f"{e['OR']:.2f} | {e['p']:.2g} | {hits} |")
        md.append("")
        md.append("LDIR-DOWN enrichment (testing 'pro-inflammatory cytokines down at D3' paper claim)")
        md.append("| set | hits/setSize | OR | p | example hits |")
        md.append("|-----|-------------|----|---|---------------|")
        for e in rec["enrichment_down_in_LDIR"]:
            hits = ", ".join(e.get("hits", [])[:8])
            md.append(f"| {e['set']} | {e['k_hit']}/{e['set_size_bg']} | "
                      f"{e['OR']:.2f} | {e['p']:.2g} | {hits} |")
        md.append("")
    (OUT/"smoke_summary.md").write_text("\n".join(md))
    print("[smoke] DONE")
    print(f"[smoke] results in {OUT}")

if __name__ == "__main__":
    main()
