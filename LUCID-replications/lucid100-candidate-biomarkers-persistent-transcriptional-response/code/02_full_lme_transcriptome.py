#!/usr/bin/env python3
"""
Whole-transcriptome LME extension of 01_smoke_lme_25genes.py.

Audits Liu et al. 2023 headline claims:
  - 266 HD DEGs at P(beta1) < 1e-5 (GSE8917)
  - 354 LD DEGs at P(beta1) < 1e-5 (GSE43151)
  -  25 genes common to both DEG lists (Table 2)
  - Cluster proportions: ~38% of LD DEGs in C1; ~35% of HD DEGs in C4

Reuses parsers from 01_smoke_lme_25genes.py. Parallelizes per-gene fits across
CPU cores via multiprocessing.Pool. Streams progress to stderr.

Outputs:
  results/full_lme_{HD,LD,VAL}.tsv
  results/full_lme_{HD,LD}_DEGs.tsv
  results/full_lme_common_DEGs.tsv
  results/full_lme_summary.json
"""
from __future__ import annotations
import importlib.util, json, os, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import multiprocessing as mp
from functools import partial

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "geo_series_matrix"
OUT  = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    "smoke25", ROOT / "code" / "01_smoke_lme_25genes.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)

PAPER = {
    "HD_DEGs": 266, "LD_DEGs": 354, "common_DEGs": 25,
    "P_THRESH": 1e-5,
    "LD_C1_pct_of_DEGs": 38.0, "HD_C4_pct_of_DEGs": 35.0,
    "HD_dataset": "GSE8917", "LD_dataset": "GSE43151", "VAL_dataset": "GSE23515",
}


def _fit_one(args):
    """Worker: fit LME (with OLS fallback) for one gene.
    args = (gene, long_sub_dict, fit_time).
    Returns dict.
    """
    gene, sub_dict, fit_time = args
    import statsmodels.api as sm
    from statsmodels.regression.mixed_linear_model import MixedLM
    sub = pd.DataFrame(sub_dict)
    if len(sub) < 6 or sub["donor"].nunique() < 2:
        return None
    if fit_time and sub["time_norm"].nunique() > 1:
        fixed_cols = ["dose_norm", "time_norm"]
    else:
        fixed_cols = ["dose_norm"]
    X = sm.add_constant(sub[fixed_cols], has_constant="add")
    est, ps, ll, method, err = {}, {}, float("nan"), "lme", None
    try:
        res = MixedLM(endog=sub["lfc"].values, exog=X.values,
                      groups=sub["donor"].values).fit(
            method="lbfgs", reml=False, disp=False)
        est = dict(zip(X.columns, res.fe_params))
        ps  = dict(zip(X.columns, res.pvalues))
        ll  = float(res.llf)
    except Exception as e1:
        err = str(e1)[:120]
        try:
            ols = sm.OLS(sub["lfc"].values, X.values).fit(
                cov_type="cluster",
                cov_kwds={"groups": sub["donor"].values})
            est = dict(zip(X.columns, ols.params))
            ps  = dict(zip(X.columns, ols.pvalues))
            ll  = float(ols.llf)
            method = "ols_cluster"
            err = None
        except Exception as e2:
            err = f"lme={err} ols={str(e2)[:80]}"
            method = "failed"
    return {
        "gene": gene, "n": int(len(sub)),
        "n_donors": int(sub["donor"].nunique()),
        "method": method,
        "beta0": est.get("const", float("nan")),
        "beta1_dose": est.get("dose_norm", float("nan")),
        "beta2_time": est.get("time_norm", float("nan")),
        "p1_dose":  ps.get("dose_norm",  float("nan")),
        "p2_time":  ps.get("time_norm",  float("nan")),
        "ll": ll, "error": err,
    }


def fit_lme_parallel(long_df: pd.DataFrame, fit_time: bool, nproc: int = None):
    nproc = nproc or max(1, (os.cpu_count() or 4) - 1)
    groups = long_df.groupby("gene")
    tasks = [
        (gene, sub[["dose_norm", "time_norm", "donor", "lfc"]].to_dict(orient="list"),
         fit_time)
        for gene, sub in groups
    ]
    print(f"   parallel fit: {len(tasks)} genes on {nproc} workers", file=sys.stderr, flush=True)
    t0 = time.time()
    results = []
    with mp.Pool(processes=nproc) as pool:
        for i, r in enumerate(pool.imap_unordered(_fit_one, tasks, chunksize=64), 1):
            if r is not None:
                results.append(r)
            if i % 1000 == 0:
                print(f"     ...{i}/{len(tasks)} ({(time.time()-t0):.0f}s)",
                      file=sys.stderr, flush=True)
    print(f"   parallel fit done in {(time.time()-t0):.1f}s, kept {len(results)} fits",
          file=sys.stderr, flush=True)
    return pd.DataFrame(results)


def run_full(name: str, gz: Path, meta_parser, fit_time: bool):
    print(f"\n== {name}: read {gz.name}", flush=True)
    t0 = time.time()
    meta_raw, expr = smoke.read_series_matrix(gz)
    meta = meta_parser(meta_raw)
    print(f"   meta rows={len(meta)}  expr={expr.shape}  read in {time.time()-t0:.1f}s", flush=True)
    plat = None
    for col in meta_raw.columns:
        if col.lower().startswith("sample_platform_id"):
            plat = meta_raw[col].iloc[0]; break
    if plat is None:
        for col in meta_raw.columns:
            if "platform" in col.lower():
                v = meta_raw[col].iloc[0]
                if isinstance(v, str) and v.startswith("GPL"):
                    plat = v; break
    print(f"   platform = {plat}", flush=True)
    annot = smoke.get_platform_annotation(plat, ROOT / "data" / "platform_annot")
    p2s = smoke.probe_to_symbol(annot)

    # Map probes -> symbol positionally
    expr_probe_ids = [str(p) for p in expr.index]
    sym_for_row = [p2s.get(pid) for pid in expr_probe_ids]
    keep_mask = np.array([s is not None for s in sym_for_row])
    expr_keep = expr.iloc[keep_mask].copy()
    expr_keep.index = [s for s in sym_for_row if s is not None]
    print(f"   probes mapped to a symbol: {int(keep_mask.sum())}/{expr.shape[0]}", flush=True)

    expr_g = expr_keep.groupby(level=0).mean()
    print(f"   unique gene symbols: {expr_g.shape[0]}", flush=True)

    gene_mean = expr_g.mean(axis=1)
    gene_var  = expr_g.var(axis=1)
    keep_g = (gene_mean > 4.0) & (gene_var > 1e-4)
    expr_g = expr_g.loc[keep_g]
    print(f"   expressed-gene set after filter: {expr_g.shape[0]}", flush=True)

    sub_meta = meta.loc[meta.index.intersection(expr_g.columns)]
    print(f"   informative samples (dose/time parsed): {len(sub_meta)}", flush=True)

    print(f"   building LFC table...", flush=True)
    t1 = time.time()
    long_df = smoke.lfc_table(expr_g, sub_meta)
    print(f"   long_df rows = {len(long_df)} in {time.time()-t1:.1f}s", flush=True)

    fit = fit_lme_parallel(long_df, fit_time=fit_time)
    if not fit.empty:
        fit["cluster"] = [smoke.cluster_of(b1, b2)
                          for b1, b2 in zip(fit["beta1_dose"], fit["beta2_time"])]
    fit["dataset"] = name
    return fit


def main():
    fit_h = run_full("GSE8917_HD",
                     DATA / "GSE8917_series_matrix.txt.gz",
                     smoke.parse_meta_gse8917, fit_time=True)
    fit_h.to_csv(OUT / "full_lme_HD_GSE8917.tsv", sep="\t", index=False)
    print(f"   wrote full_lme_HD_GSE8917.tsv  ({len(fit_h)} genes)", flush=True)

    fit_l = run_full("GSE43151_LD",
                     DATA / "GSE43151_series_matrix.txt.gz",
                     smoke.parse_meta_gse43151, fit_time=True)
    fit_l.to_csv(OUT / "full_lme_LD_GSE43151.tsv", sep="\t", index=False)
    print(f"   wrote full_lme_LD_GSE43151.tsv ({len(fit_l)} genes)", flush=True)

    fit_v = run_full("GSE23515_VAL",
                     DATA / "GSE23515_series_matrix.txt.gz",
                     smoke.parse_meta_gse23515, fit_time=False)
    fit_v.to_csv(OUT / "full_lme_VAL_GSE23515.tsv", sep="\t", index=False)
    print(f"   wrote full_lme_VAL_GSE23515.tsv ({len(fit_v)} genes)", flush=True)

    p = PAPER["P_THRESH"]
    hd_de = fit_h[fit_h["p1_dose"].notna() & (fit_h["p1_dose"] < p)].copy()
    ld_de = fit_l[fit_l["p1_dose"].notna() & (fit_l["p1_dose"] < p)].copy()
    common = set(hd_de["gene"]) & set(ld_de["gene"])

    def cluster_props(de):
        if de.empty: return {}
        return de["cluster"].value_counts(normalize=True).mul(100).round(1).to_dict()

    # Recover whether the 12 paper-named biomarkers are recovered by our DE list
    BIOMARKERS = ["ARHGEF3","BAX","BBC3","CCDC109B","DCP1B","DDB2",
                  "F11R","GADD45A","GSS","PLK3","TNFRSF10B","XPC"]
    bm_recovered_HD = sorted(set(BIOMARKERS) & set(hd_de["gene"]))
    bm_recovered_LD = sorted(set(BIOMARKERS) & set(ld_de["gene"]))
    bm_recovered_both = sorted(set(bm_recovered_HD) & set(bm_recovered_LD))

    summary = {
        "paper_claims": PAPER,
        "ours": {
            "HD_genes_total":          int(len(fit_h)),
            "HD_genes_fit_with_p":     int(fit_h["p1_dose"].notna().sum()),
            "HD_DEGs_at_p1e-5":        int(len(hd_de)),
            "LD_genes_total":          int(len(fit_l)),
            "LD_genes_fit_with_p":     int(fit_l["p1_dose"].notna().sum()),
            "LD_DEGs_at_p1e-5":        int(len(ld_de)),
            "VAL_genes_total":         int(len(fit_v)),
            "common_DEGs_HD_LD":       int(len(common)),
            "HD_DEG_cluster_pct":      cluster_props(hd_de),
            "LD_DEG_cluster_pct":      cluster_props(ld_de),
            "biomarkers_recovered_in_HD_DEG":  bm_recovered_HD,
            "biomarkers_recovered_in_LD_DEG":  bm_recovered_LD,
            "biomarkers_recovered_in_BOTH":    bm_recovered_both,
        },
        "comparison": {
            "HD_DEG_count_ratio_ours_over_paper":
                round(len(hd_de) / PAPER["HD_DEGs"], 3),
            "LD_DEG_count_ratio_ours_over_paper":
                round(len(ld_de) / PAPER["LD_DEGs"], 3),
            "common_DEG_count_ratio":
                round(len(common) / PAPER["common_DEGs"], 3) if PAPER["common_DEGs"] else None,
        },
    }
    (OUT / "full_lme_summary.json").write_text(json.dumps(summary, indent=2))

    hd_de.to_csv(OUT / "full_lme_HD_DEGs.tsv", sep="\t", index=False)
    ld_de.to_csv(OUT / "full_lme_LD_DEGs.tsv", sep="\t", index=False)
    pd.DataFrame({"gene": sorted(common)}).to_csv(
        OUT / "full_lme_common_DEGs.tsv", sep="\t", index=False)

    print("\n=== Headline comparison ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
