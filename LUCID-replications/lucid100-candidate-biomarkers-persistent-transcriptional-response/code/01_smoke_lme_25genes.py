#!/usr/bin/env python3
"""
Smoke replication of Liu et al. 2023 (DOI 10.1080/09553002.2023.2241897), Table 2.

What this does (minimal, CPU-light — runs in <2 min on a laptop):
  1. Parse the three GEO series matrices (already downloaded).
  2. Resolve probe IDs -> gene symbols for the 25 Table-2 genes per platform.
     (Uses GEO platform annotations downloaded on demand.)
  3. Compute per-sample log-fold-change (LFC) relative to dose=0 baseline at the
     matching time point (mean of 0 Gy replicates within each time bucket).
  4. Fit a linear mixed-effects model
        LFC ~ beta0 + beta1 * dose_norm + beta2 * time_norm + (1 | donor)
     using statsmodels MixedLM, on each gene, for GSE8917 (HD) and GSE43151 (LD).
  5. Compare estimated (beta1, beta2, p2) and cluster assignment vs Table 2.
  6. Write a TSV + a JSON summary; print a quick agreement report.

Caveats vs Liu et al.:
  - They used MATLAB fitlme on log-raw intensities ("log(E/E0)"); we approximate
    LFC = log2(intensity / mean(intensity at dose=0, matched time)). Slopes will
    differ by ln(2) <-> log2 (~1.44 factor), so we compare *sign* and ordering,
    not absolute magnitudes.
  - They report only beta-of-dose p-value < 1e-5 selection up front; we don't
    re-derive the whole DE list here, only re-fit on the 25 genes they reported.
  - Donor IDs in GSE8917 are per-time-block (different donors at 6 h vs 24 h).
    We use sample_title to extract a donor handle.

Outputs:
  results/lme_smoke_HD_GSE8917.tsv
  results/lme_smoke_LD_GSE43151.tsv
  results/lme_smoke_agreement.tsv
  results/lme_smoke_summary.json
"""
from __future__ import annotations
import gzip, io, json, os, re, sys, time, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "geo_series_matrix"
OUT  = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

TABLE2 = pd.read_csv(ROOT / "data" / "table2_25_common_DE_genes.tsv",
                     sep="\t", comment="#")
GENES = TABLE2["gene"].tolist()

# ---- helpers ---------------------------------------------------------------

def read_series_matrix(path: Path):
    """Return (meta_df, expr_df) for a GEO series matrix.
    meta_df: index=sample_geo_accession, columns=meta fields (Sample_title,
             Sample_source_name_ch1, Sample_characteristics_ch1.*, ...)
    expr_df: index=probe_id, columns=sample_geo_accession (float)
    """
    meta_rows = {}
    sample_acc = None
    expr_lines = []
    in_table = False
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                in_table = False
                continue
            if in_table:
                expr_lines.append(line)
                continue
            if line.startswith("!Sample_"):
                # !Sample_title<TAB>"a"<TAB>"b"...
                toks = [t.strip().strip('"') for t in line.rstrip("\n").split("\t")]
                key  = toks[0].lstrip("!")
                vals = toks[1:]
                # GEO appends a suffix when the same key repeats (e.g. characteristics)
                base = key
                k = key
                i = 1
                while k in meta_rows:
                    i += 1
                    k = f"{base}_{i}"
                meta_rows[k] = vals
    # Build expression frame from the table lines
    if not expr_lines:
        raise RuntimeError(f"No expression table in {path}")
    expr_io = io.StringIO("".join(expr_lines))
    expr = pd.read_csv(expr_io, sep="\t", index_col=0, na_values=["null", "NaN", ""])
    expr.index.name = "probe_id"
    expr.columns = [c.strip('"') for c in expr.columns]
    # Meta as DataFrame: rows = samples (use Sample_geo_accession as index)
    n = expr.shape[1]
    # truncate any meta vector to n
    meta_rows = {k: (v[:n] + [None] * max(0, n - len(v))) for k, v in meta_rows.items()}
    meta = pd.DataFrame(meta_rows)
    if "Sample_geo_accession" in meta.columns:
        meta.index = meta["Sample_geo_accession"]
    else:
        meta.index = expr.columns
    return meta, expr


def get_platform_annotation(gpl: str, cache_dir: Path) -> pd.DataFrame:
    """Return a probe-id -> gene-symbol map for a GEO platform.

    Caches a *trimmed* table (just the !platform_table block) at
    cache_dir/{gpl}_annot.tsv.gz so we never re-pay the 1-2 GB family.soft
    cost on subsequent runs. If only the family.soft.gz exists upstream
    (e.g. GPL13497), we stream-extract just the platform table while saving.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = cache_dir / f"{gpl}_annot.tsv.gz"
    if not out.exists():
        prefix = re.sub(r"\d{1,3}$", "nnn", gpl)
        # try smaller annot first
        annot_url = f"https://ftp.ncbi.nlm.nih.gov/geo/platforms/{prefix}/{gpl}/annot/{gpl}.annot.gz"
        try:
            print(f"  fetching annotation: {annot_url}", file=sys.stderr)
            urllib.request.urlretrieve(annot_url, out)
        except Exception as e:
            print(f"  annot fetch failed ({e}); falling back to family.soft.gz (stream-extract)",
                  file=sys.stderr)
            soft_url = f"https://ftp.ncbi.nlm.nih.gov/geo/platforms/{prefix}/{gpl}/soft/{gpl}_family.soft.gz"
            tmp = out.with_suffix(".soft.gz")
            urllib.request.urlretrieve(soft_url, tmp)
            # Stream-extract just the !platform_table block, then drop the big soft
            in_tbl = False
            extracted = out.with_suffix(".tsv")
            with gzip.open(tmp, "rt", errors="replace") as fh, open(extracted, "w") as eo:
                for line in fh:
                    s = line.rstrip("\n")
                    if s.startswith("!platform_table_begin"):
                        in_tbl = True; continue
                    if s.startswith("!platform_table_end"):
                        break
                    if in_tbl:
                        eo.write(line)
            # gzip it in place
            import subprocess
            subprocess.check_call(["gzip", "-f", str(extracted)])
            (extracted.parent / (extracted.name + ".gz")).rename(out)
            tmp.unlink(missing_ok=True)
    rows = []
    in_tbl = False
    header = None
    has_marker = False
    # Peek the first ~50 lines to decide whether this gz has the
    # `!platform_table_begin` marker (annot.gz / extracted family.soft.gz with
    # marker) or is a bare TSV (extracted-then-stripped table).
    with gzip.open(out, "rt", errors="replace") as fh:
        peek = "".join([next(fh, "") for _ in range(50)])
        has_marker = "!platform_table_begin" in peek
    with gzip.open(out, "rt", errors="replace") as fh:
        if not has_marker:
            in_tbl = True
        for line in fh:
            s = line.rstrip("\n")
            if has_marker and s.startswith("!platform_table_begin"):
                in_tbl = True; continue
            if s.startswith("!platform_table_end"):
                break
            if in_tbl:
                fields = s.split("\t")
                if header is None:
                    header = fields
                else:
                    rows.append(fields[:len(header)])
    annot = pd.DataFrame(rows, columns=header)
    return annot


def probe_to_symbol(annot: pd.DataFrame) -> dict[str, str]:
    """Map probe_id -> first gene symbol (uppercased)."""
    # Common header variants
    pid_col = next((c for c in annot.columns if c.lower() in
                    ("id", "probeid", "probe_id", "probe id", "probe name")), annot.columns[0])
    sym_col = None
    for cand in ("Gene symbol", "GeneSymbol", "Gene Symbol", "Symbol",
                 "Gene_Symbol", "GENE_SYMBOL"):
        if cand in annot.columns:
            sym_col = cand; break
    if sym_col is None:
        for c in annot.columns:
            if "symbol" in c.lower():
                sym_col = c; break
    if sym_col is None:
        raise RuntimeError("No gene-symbol column in platform annotation")
    out = {}
    for pid, sym in zip(annot[pid_col], annot[sym_col]):
        if not isinstance(sym, str) or not sym:
            continue
        first = sym.split("///")[0].strip().upper()
        if first:
            out.setdefault(str(pid), first)
    return out


# ---- per-dataset metadata parsers -----------------------------------------

DOSE_TIME_RE_GSE8917 = re.compile(r"_(\d+)hr_([\d\.]+)Gy_rep(\d+)")
def parse_meta_gse8917(meta: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for acc, ttl in meta["Sample_title"].items():
        m = DOSE_TIME_RE_GSE8917.search(ttl)
        if not m:
            continue
        hr, gy, rep = m.group(1), m.group(2), m.group(3)
        rows.append({
            "sample": acc, "title": ttl,
            "time_h": float(hr), "dose_Gy": float(gy),
            "donor": f"{hr}h_rep{rep}",  # per-time donor handle
        })
    return pd.DataFrame(rows).set_index("sample")


DOSE_TIME_RE_GSE43151 = re.compile(r"TCD4_(\d+H\d+|\d+H)_D(\d+)Gy_Ind(\d+)")
# GSE43151 dose tokens encode mGy/Gy with the decimal stripped:
#   D0Gy   -> 0,   D0005Gy -> 0.005, D001Gy -> 0.010, D0025Gy -> 0.025,
#   D005Gy -> 0.050, D01Gy -> 0.100, D05Gy -> 0.500
GSE43151_DOSE_LOOKUP = {
    "0": 0.0,
    "0005": 0.005, "001": 0.01,  "0025": 0.025,
    "005":  0.05,  "01":  0.1,   "05":   0.5,
}
def _parse_43151_time(tok: str) -> float:
    # "2H30" -> 2.5, "5H" -> 5.0, "7H30" -> 7.5, "10H" -> 10.0
    m = re.match(r"(\d+)H(\d+)?", tok)
    if not m: return float("nan")
    h = float(m.group(1)); mn = float(m.group(2) or 0)
    return h + mn / 60.0
def parse_meta_gse43151(meta: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for acc, ttl in meta["Sample_title"].items():
        m = DOSE_TIME_RE_GSE43151.search(ttl)
        if not m:
            continue
        t = _parse_43151_time(m.group(1))
        dose_tok = m.group(2)
        if dose_tok not in GSE43151_DOSE_LOOKUP:
            continue  # unknown dose encoding
        gy = GSE43151_DOSE_LOOKUP[dose_tok]
        ind = m.group(3)
        rows.append({"sample": acc, "title": ttl,
                     "time_h": t, "dose_Gy": gy, "donor": f"Ind{ind}"})
    return pd.DataFrame(rows).set_index("sample")


def parse_meta_gse23515(meta: pd.DataFrame) -> pd.DataFrame:
    """Format: 'Female_Non-smoker_0.1Gy_rep1' / 'Male_Smoker_2Gy_rep3' / '..._0Gy_rep5'."""
    rows = []
    for acc, ttl in meta["Sample_title"].items():
        m = re.match(r"^(Male|Female)_(Smoker|Non-smoker)_([\d\.]+)Gy_rep(\d+)$", ttl)
        if not m:
            continue
        sex, smoke, gy, rep = m.groups()
        rows.append({"sample": acc, "title": ttl, "time_h": 6.0,
                     "dose_Gy": float(gy),
                     "donor": f"{sex[0]}{smoke[0]}{rep}"})
    return pd.DataFrame(rows).set_index("sample")


# ---- core: build LFC table & fit LME --------------------------------------

def lfc_table(expr_genes: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    """Return long-format LFC dataframe: columns gene, sample, dose_norm, time_norm, donor, lfc."""
    # Baseline = mean of dose=0 samples at the same time bucket
    df = meta.copy()
    # If no dose=0 at this time bucket, fall back to global dose=0 mean
    base = {}
    for t in df["time_h"].unique():
        ctl = df[(df["dose_Gy"] == 0) & (df["time_h"] == t)].index
        if len(ctl) == 0:
            ctl = df[df["dose_Gy"] == 0].index
        if len(ctl) == 0:
            continue
        base[t] = expr_genes.loc[:, ctl].mean(axis=1)
    # global fallback
    glob_ctl_idx = df[df["dose_Gy"] == 0].index
    glob_base = expr_genes.loc[:, glob_ctl_idx].mean(axis=1) if len(glob_ctl_idx) else expr_genes.mean(axis=1)
    # Normalize dose/time to [0,1]
    dmax = df["dose_Gy"].max()
    tmax = df["time_h"].max() if df["time_h"].nunique() > 1 else 1.0
    long_rows = []
    for samp, row in df.iterrows():
        if row["dose_Gy"] == 0:
            continue  # baseline doesn't carry information about slope
        b = base.get(row["time_h"], glob_base)
        if samp not in expr_genes.columns:
            continue
        # log2 LFC (raw GEO matrices are already in log2 for Agilent typically;
        # check by range; if range > 100 assume linear and log-transform)
        col = expr_genes[samp]
        if col.dropna().abs().max() > 50:
            with np.errstate(invalid="ignore", divide="ignore"):
                col = np.log2(col.clip(lower=1.0))
                b_use = np.log2(b.clip(lower=1.0))
        else:
            b_use = b
        lfc = col - b_use
        for g, v in lfc.items():
            if pd.isna(v):
                continue
            long_rows.append({
                "gene": g, "sample": samp,
                "dose_norm": row["dose_Gy"] / dmax,
                "time_norm": row["time_h"] / tmax if tmax else 0.0,
                "donor": row["donor"], "lfc": float(v),
            })
    return pd.DataFrame(long_rows)


def fit_lme(long_df: pd.DataFrame, fit_time: bool = True) -> pd.DataFrame:
    """Fit LFC ~ const + beta1*dose + beta2*time + (1|donor) per gene.

    When the random-intercept LME fails (typical reason: donors are nested
    within time blocks so the donor random effect absorbs time; statsmodels
    raises a Singular matrix in REML/MLE), we fall back to plain OLS with
    cluster-robust standard errors by donor. This matches the paper's design
    in those datasets (e.g. GSE8917 had different donors at 6 h vs 24 h).
    """
    import statsmodels.api as sm
    from statsmodels.regression.mixed_linear_model import MixedLM
    out = []
    for gene, sub in long_df.groupby("gene"):
        if len(sub) < 6 or sub["donor"].nunique() < 2:
            continue
        if fit_time and sub["time_norm"].nunique() > 1:
            fixed_cols = ["dose_norm", "time_norm"]
        else:
            fixed_cols = ["dose_norm"]
        X = sm.add_constant(sub[fixed_cols], has_constant="add")
        # ---- attempt 1: LME with random intercept by donor ----
        est = {}; ps = {}; ll = float("nan"); method = "lme"; err = None
        try:
            res = MixedLM(endog=sub["lfc"].values, exog=X.values,
                          groups=sub["donor"].values).fit(
                method="lbfgs", reml=False, disp=False)
            est = dict(zip(X.columns, res.fe_params))
            ps  = dict(zip(X.columns, res.pvalues))
            ll  = float(res.llf)
        except Exception as e1:
            err = str(e1)[:120]
            # ---- attempt 2: OLS with cluster-robust SEs ----
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
        out.append({
            "gene": gene,
            "n": len(sub),
            "n_donors": sub["donor"].nunique(),
            "method": method,
            "beta0": est.get("const", float("nan")),
            "beta1_dose": est.get("dose_norm", float("nan")),
            "beta2_time": est.get("time_norm", float("nan")),
            "p1_dose": ps.get("dose_norm", float("nan")),
            "p2_time": ps.get("time_norm", float("nan")),
            "ll": ll,
            "error": err,
        })
    return pd.DataFrame(out)


def cluster_of(b1, b2):
    if any(pd.isna(x) for x in (b1, b2)): return "NA"
    if b1 > 0 and b2 > 0: return "C1"
    if b1 > 0 and b2 < 0: return "C2"
    if b1 < 0 and b2 > 0: return "C3"
    return "C4"


# ---- driver ---------------------------------------------------------------

def run_dataset(name: str, gz: Path, meta_parser, fit_time: bool):
    print(f"== {name}: read {gz.name}")
    t0 = time.time()
    meta_raw, expr = read_series_matrix(gz)
    meta = meta_parser(meta_raw)
    print(f"   meta rows={len(meta)}  expr={expr.shape}  read in {time.time()-t0:.1f}s")
    # Detect platform from raw meta
    plat = None
    for col in meta_raw.columns:
        if col.lower().startswith("sample_platform_id"):
            plat = meta_raw[col].iloc[0]
            break
    if plat is None:
        for col in meta_raw.columns:
            if "platform" in col.lower():
                v = meta_raw[col].iloc[0]
                if isinstance(v, str) and v.startswith("GPL"):
                    plat = v; break
    print(f"   platform = {plat}")
    annot = get_platform_annotation(plat, ROOT / "data" / "platform_annot")
    p2s = probe_to_symbol(annot)
    # Restrict to genes of interest
    targets = set(GENES)
    keep_probes = [p for p in expr.index if str(p) in p2s and p2s[str(p)] in targets]
    expr_t = expr.loc[keep_probes].copy()
    expr_t.index = [p2s[str(p)] for p in keep_probes]
    # Collapse to one expression per gene (mean across probes)
    expr_g = expr_t.groupby(level=0).mean()
    print(f"   genes matched: {expr_g.shape[0]}/{len(targets)}")
    # Build LFC table on samples we know dose/time for
    sub_meta = meta.loc[meta.index.intersection(expr_g.columns)]
    long_df = lfc_table(expr_g, sub_meta)
    fit = fit_lme(long_df, fit_time=fit_time)
    if not fit.empty:
        fit["cluster"] = [cluster_of(b1, b2) for b1, b2 in zip(fit["beta1_dose"], fit["beta2_time"])]
    fit["dataset"] = name
    return meta, expr_g, fit


def main():
    summary = {"datasets": {}, "agreement": {}}
    meta_h, expr_h, fit_h = run_dataset(
        "GSE8917_HD",
        DATA / "GSE8917_series_matrix.txt.gz",
        parse_meta_gse8917, fit_time=True,
    )
    meta_l, expr_l, fit_l = run_dataset(
        "GSE43151_LD",
        DATA / "GSE43151_series_matrix.txt.gz",
        parse_meta_gse43151, fit_time=True,
    )
    meta_v, expr_v, fit_v = run_dataset(
        "GSE23515_VAL",
        DATA / "GSE23515_series_matrix.txt.gz",
        parse_meta_gse23515, fit_time=False,
    )
    fit_h.to_csv(OUT / "lme_smoke_HD_GSE8917.tsv", sep="\t", index=False)
    fit_l.to_csv(OUT / "lme_smoke_LD_GSE43151.tsv", sep="\t", index=False)
    fit_v.to_csv(OUT / "lme_smoke_VAL_GSE23515.tsv", sep="\t", index=False)

    # Agreement vs Table 2
    t2 = TABLE2.set_index("gene")
    rows = []
    for gene in GENES:
        h = fit_h.set_index("gene").reindex([gene]).iloc[0]
        l = fit_l.set_index("gene").reindex([gene]).iloc[0]
        rows.append({
            "gene": gene,
            "panel": t2.loc[gene, "panel"],
            "HD_beta1_paper": t2.loc[gene, "HD_beta1"],
            "HD_beta1_ours":  h.get("beta1_dose"),
            "HD_beta2_paper": t2.loc[gene, "HD_beta2"],
            "HD_beta2_ours":  h.get("beta2_time"),
            "HD_cluster_paper": t2.loc[gene, "HD_cluster"],
            "HD_cluster_ours":  h.get("cluster", "NA"),
            "HD_sign_dose_match": (np.sign(t2.loc[gene, "HD_beta1"]) == np.sign(h.get("beta1_dose", 0))) if not pd.isna(h.get("beta1_dose")) else False,
            "LD_beta1_paper": t2.loc[gene, "LD_beta1"],
            "LD_beta1_ours":  l.get("beta1_dose"),
            "LD_beta2_paper": t2.loc[gene, "LD_beta2"],
            "LD_beta2_ours":  l.get("beta2_time"),
            "LD_cluster_paper": t2.loc[gene, "LD_cluster"],
            "LD_cluster_ours":  l.get("cluster", "NA"),
            "LD_sign_dose_match": (np.sign(t2.loc[gene, "LD_beta1"]) == np.sign(l.get("beta1_dose", 0))) if not pd.isna(l.get("beta1_dose")) else False,
        })
    agree = pd.DataFrame(rows)
    agree.to_csv(OUT / "lme_smoke_agreement.tsv", sep="\t", index=False)
    summary["agreement"] = {
        "HD_dose_sign_match_pct": float(agree["HD_sign_dose_match"].mean()) * 100,
        "LD_dose_sign_match_pct": float(agree["LD_sign_dose_match"].mean()) * 100,
        "HD_cluster_match_pct":   float((agree["HD_cluster_ours"] == agree["HD_cluster_paper"]).mean()) * 100,
        "LD_cluster_match_pct":   float((agree["LD_cluster_ours"] == agree["LD_cluster_paper"]).mean()) * 100,
        "n_genes_HD_fit":         int(agree["HD_beta1_ours"].notna().sum()),
        "n_genes_LD_fit":         int(agree["LD_beta1_ours"].notna().sum()),
        "n_genes_total":          int(len(agree)),
    }
    summary["datasets"]["GSE8917_HD"]   = {"n_samples": int(len(meta_h)), "n_genes_fit": int(len(fit_h.dropna(subset=["beta1_dose"])))}
    summary["datasets"]["GSE43151_LD"]  = {"n_samples": int(len(meta_l)), "n_genes_fit": int(len(fit_l.dropna(subset=["beta1_dose"])))}
    summary["datasets"]["GSE23515_VAL"] = {"n_samples": int(len(meta_v)), "n_genes_fit": int(len(fit_v.dropna(subset=["beta1_dose"])))}

    (OUT / "lme_smoke_summary.json").write_text(json.dumps(summary, indent=2))
    print("\nSummary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
