#!/usr/bin/env python3
"""
FRONT 2 — Two-layer GSVD on open NBL data.

Test of the paper's central method-generalizability claims (C1, C2, C3, C4, C5):
- D1 = tumor RNA-Seq expression (log2 counts), patients × top-N high-variance genes
- D2 = tumor methylation beta values (Illumina 450K), patients × top-N high-variance CpGs

Both layers come from primary tumor of the SAME patients. The paper's
"tumor genome + blood genome" patient-matched two-layer GSVD is exactly
this structure (two patient-matched feature blocks). The patterns the
GSVD extracts should be:
- u1,1 analog : pattern most exclusive to D1 (tumor RNA), the one
                that drives RNA but not methylation
- u1,N analog : pattern most exclusive to D2 (methylation), orthogonal
                in the (c,s) sense to the first
The paper claims these are survival-predictive; the COMBINED predictor
should beat the best single standard-of-care biomarker.

NOTE on convention. Our gsvd() returns columns sorted by c/s ascending.
We feed (D1 = RNA, D2 = Methylation). Then:
    k_first (last column, n-1) = most-RNA-exclusive  -> "tumor-like" pattern
    k_last  (first column, 0)  = most-Meth-exclusive -> "methylation-like" pattern

We also pick the "~100th" pattern as the column with c/s closest to 1
(the most-shared pattern), which the paper claims captures demographic /
sex artifact (C3).
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, "/data/stevens/alter-pathB/code")
from gsvd_reference import gsvd, ho_gsvd, antisymmetric_patterns, combine_predictors
from survival_stats import report as sv_report

DATA = Path("/data/stevens/alter-pathB/data/target_nbl")
RES = Path("/data/stevens/alter-pathB/results")
RES.mkdir(exist_ok=True, parents=True)

# ---------------------------------------------------------------------------
# Load RNA expression (genes x patients)
# ---------------------------------------------------------------------------
def load_rna():
    X = np.load(DATA/"expression_log2.npy")  # (60660, 153) log2(counts+1)
    pids = (DATA/"patient_ids.txt").read_text().strip().splitlines()
    gene_ids = (DATA/"gene_ids.txt").read_text().strip().splitlines()
    gene_names = (DATA/"gene_names.txt").read_text().strip().splitlines()
    gene_types = (DATA/"gene_types.txt").read_text().strip().splitlines()
    print(f"  RNA: {X.shape} genes x patients = {len(gene_ids)} x {len(pids)}")
    return X, pids, gene_ids, gene_names, gene_types

# ---------------------------------------------------------------------------
# Load methylation (CpGs x patients) from per-file txt
# ---------------------------------------------------------------------------
def load_meth(target_patients):
    """Load methylation beta-value files; restrict to Primary Tumor of target_patients.

    GDC Methylation Beta Value files: TSV with columns Composite Element REF + beta.
    Format (example): 'cg00000029\t0.4275' (no header).
    """
    files_meta = pd.read_csv(DATA/"files_meth.tsv", sep="\t")
    files_meta = files_meta.dropna(subset=["case_submitter"])
    primary = files_meta[files_meta["sample_type"]=="Primary Tumor"].copy()
    # Keep only patients with RNA
    primary = primary[primary["case_submitter"].isin(target_patients)]
    primary = primary.sort_values("file_id").drop_duplicates("case_submitter", keep="first")
    print(f"  meth primary-tumor files matching RNA patients: {len(primary)}")
    if len(primary)==0: return None, None
    # Load first file to get CpG index
    f0 = DATA/"meth"/f"{primary.iloc[0]['file_id']}_{primary.iloc[0]['file_name']}"
    print(f"  reading first meth file: {f0.name}")
    df0 = pd.read_csv(f0, sep="\t", header=None, names=["cpg","beta"], na_values=["NA","",".","NaN"])
    cpgs = df0["cpg"].tolist()
    n_cpg = len(cpgs)
    n_pat = len(primary)
    print(f"  meth matrix shape: {n_cpg} CpGs x {n_pat} patients")
    M = np.full((n_cpg, n_pat), np.nan, dtype=np.float32)
    M[:,0] = df0["beta"].to_numpy(dtype=np.float32)
    pat_list = [primary.iloc[0]["case_submitter"]]
    for j in range(1, n_pat):
        row = primary.iloc[j]
        fp = DATA/"meth"/f"{row['file_id']}_{row['file_name']}"
        df = pd.read_csv(fp, sep="\t", header=None, names=["cpg","beta"], na_values=["NA","",".","NaN"])
        if len(df)!=n_cpg:
            df = df.set_index("cpg").reindex(cpgs).reset_index()
        M[:,j] = df["beta"].to_numpy(dtype=np.float32)
        pat_list.append(row["case_submitter"])
        if (j+1)%25==0: print(f"  meth loaded {j+1}/{n_pat}")
    return M, pat_list, cpgs

# ---------------------------------------------------------------------------
# Helpers: prep matrix (filter, center) for GSVD
# ---------------------------------------------------------------------------
def prep_features(X, top_n=5000, log_transform=False):
    """X: features x patients. Returns top_n highest-variance rows,
       median-centered per row (paper centers profiles at autosomal median;
       row-centering is the matrix analog and the standard pre-GSVD step)."""
    if log_transform:
        X = np.log2(X.astype(np.float32) + 1)
    # Drop rows that are all-NaN or constant
    nan_frac = np.isnan(X).mean(axis=1)
    keep = nan_frac < 0.10
    X = X[keep, :]
    # Impute remaining NaN with row median (simple)
    if np.isnan(X).any():
        med = np.nanmedian(X, axis=1, keepdims=True)
        inds = np.where(np.isnan(X))
        X = X.copy()
        X[inds] = np.take(med.ravel(), inds[0])
    var = X.var(axis=1)
    top = np.argsort(var)[::-1][:top_n]
    X = X[top, :]
    # Center per row (median subtract -> robust)
    X = X - np.median(X, axis=1, keepdims=True)
    return X.astype(np.float64), top, keep

# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run(top_n_rna=5000, top_n_meth=10000, seed=0):
    rng = np.random.default_rng(seed)
    print(f"== FRONT 2 GSVD pipeline (top_n_rna={top_n_rna}, top_n_meth={top_n_meth}) ==")
    t0 = time.time()
    X_rna, rna_pids, gene_ids, gene_names, gene_types = load_rna()
    M, meth_pids, cpgs = load_meth(set(rna_pids))
    if M is None:
        return {"error":"no methylation"}
    # Intersect patients
    common = [p for p in rna_pids if p in set(meth_pids)]
    print(f"  matched patients: {len(common)}")
    rna_idx = [rna_pids.index(p) for p in common]
    meth_idx = [meth_pids.index(p) for p in common]
    X_r = X_rna[:, rna_idx]
    X_m = M[:, meth_idx]
    # Prep
    D1, top_rna, keep_rna = prep_features(X_r, top_n=top_n_rna, log_transform=False)
    D2, top_meth, keep_meth = prep_features(X_m, top_n=top_n_meth, log_transform=False)
    print(f"  D1 (RNA, top {top_n_rna} by var, median-centered): {D1.shape}")
    print(f"  D2 (Meth, top {top_n_meth} by var, median-centered): {D2.shape}")
    # GSVD
    print("== Running GSVD ==")
    t1 = time.time()
    result = gsvd(D1, D2)
    print(f"  GSVD done in {time.time()-t1:.1f}s; n_patterns={result.V.shape[1]}")
    print(f"  c/s ratios head: {result.ratio[:5]}; tail: {result.ratio[-5:]}")
    # Pattern indices
    k_first, k_last = antisymmetric_patterns(result)   # u1,1 analog and u1,N analog
    # Find a "balanced" / shared pattern (closest to c=s); the paper's u1,100
    ratios = result.ratio
    # exclude already-picked extremes
    valid_idx = np.arange(result.V.shape[1])
    valid_idx = valid_idx[(valid_idx != k_first) & (valid_idx != k_last)]
    k_shared = valid_idx[np.argmin(np.abs(np.log(np.maximum(ratios[valid_idx],1e-300))))]
    print(f"  k_first={k_first}, k_last={k_last}, k_shared={k_shared}")

    # Build patient-mode coordinates from V
    # V[:, k] are coefficients of the n patients in the shared right basis;
    # the patient scores = V[:, k] directly (this is the same convention used
    # in tests/classify_patients).
    a_first  = result.V[:, k_first]
    a_last   = result.V[:, k_last]
    a_shared = result.V[:, k_shared]

    # ---- Survival evaluation ----
    print("== Survival evaluation ==")
    cl = pd.read_csv(DATA/"clinical_merged.tsv", sep="\t").set_index("patient_id")
    cl = cl.reindex(common)
    times = pd.to_numeric(cl["Overall Survival Time in Days"], errors="coerce").to_numpy()
    vs = cl["Vital Status"].astype(str).str.strip()
    events = (vs=="Dead").astype(int).to_numpy()
    valid = ~np.isnan(times) & (times>0)
    print(f"  patients with valid time/event: {valid.sum()}/{len(common)}")
    t_v = times[valid]; e_v = events[valid]
    res = {"n_total":int(len(common)), "n_with_followup":int(valid.sum()),
           "k_first":int(k_first), "k_last":int(k_last), "k_shared":int(k_shared),
           "ratio_first":float(result.ratio[k_first]),
           "ratio_last":float(result.ratio[k_last]),
           "ratio_shared":float(result.ratio[k_shared]),
           "top_n_rna":top_n_rna, "top_n_meth":top_n_meth, "seed":seed}

    # --- Single-pattern survival on continuous score (Cox) ---
    for name, a in [("first_pattern_continuous", a_first[valid]),
                    ("last_pattern_continuous",  a_last[valid]),
                    ("shared_pattern_continuous",a_shared[valid])]:
        try:
            rep = sv_report(t_v, e_v, np.zeros_like(a, dtype=int), label=name)  # placeholder for groups
            from survival_stats import cox_univariate, concordance_index
            cox = cox_univariate(t_v, e_v, a.astype(float))
            cidx = concordance_index(t_v, e_v, a.astype(float))
            res[name] = {"cox_hr":round(cox.hr,4),"cox_ci":[round(cox.ci_lower,4),round(cox.ci_upper,4)],
                         "cox_wald_p":cox.wald_p,"concordance":round(cidx,4)}
            print(f"  {name}: HR={cox.hr:.3f} ({cox.ci_lower:.2f}-{cox.ci_upper:.2f}) P={cox.wald_p:.3g} C={cidx:.3f}")
        except Exception as e:
            res[name] = {"error":str(e)}

    # --- Binary classification (sign) on each ---
    from gsvd_reference import classify_patients
    g_first = classify_patients(a_first[valid])
    g_last  = classify_patients(a_last[valid])
    g_shared= classify_patients(a_shared[valid])
    for name, g in [("first_pattern_sign", g_first),
                    ("last_pattern_sign", g_last),
                    ("shared_pattern_sign", g_shared)]:
        try:
            rep = sv_report(t_v, e_v, g, label=name)
            res[name] = rep
            print(f"  {name}: n={rep['n_total']} HR={rep['cox_hr']} P={rep['logrank_p']:.3g} C={rep['concordance']}")
        except Exception as e:
            res[name] = {"error":str(e)}

    # --- COMBINED predictor (3-class: low/mid/high by joint sign) ---
    g_combined = combine_predictors(a_first[valid], a_last[valid])
    try:
        rep = sv_report(t_v, e_v, g_combined, label="combined_first_last_3class")
        res["combined_first_last_3class"] = rep
        # Also continuous combined score for concordance (sum of standardized arraylets)
        from survival_stats import cox_univariate, concordance_index
        af = a_first[valid]; al = a_last[valid]
        af_s = (af - af.mean()) / (af.std() if af.std()>0 else 1)
        al_s = (al - al.mean()) / (al.std() if al.std()>0 else 1)
        comb_score = af_s + al_s
        cox = cox_univariate(t_v, e_v, comb_score)
        cidx_comb = concordance_index(t_v, e_v, comb_score)
        res["combined_continuous_sum_zscore"] = {
            "cox_hr":round(cox.hr,4),
            "cox_ci":[round(cox.ci_lower,4),round(cox.ci_upper,4)],
            "cox_wald_p":cox.wald_p,
            "concordance":round(cidx_comb,4),
        }
        print(f"  COMBINED 3-class: n={rep['n_total']} HR={rep['cox_hr']} P={rep['logrank_p']:.3g} C={rep['concordance']}")
        print(f"  COMBINED continuous-sum: HR={cox.hr:.3f} P={cox.wald_p:.3g} C={cidx_comb:.3f}")
    except Exception as e:
        res["combined_first_last_3class"] = {"error":str(e)}

    # --- C3 test: does the shared pattern correlate with sex? ---
    sex = cl["Gender"].astype(str).str.strip().str.lower().map({"male":0,"female":1})
    sex_v = sex[valid].to_numpy(dtype=float)
    s_ok = ~np.isnan(sex_v)
    if s_ok.sum()>10:
        from scipy.stats import pointbiserialr, mannwhitneyu
        for name, a in [("first_pattern", a_first[valid]),
                        ("last_pattern", a_last[valid]),
                        ("shared_pattern", a_shared[valid])]:
            r = pointbiserialr(sex_v[s_ok], a[s_ok])
            res[f"{name}_vs_sex"] = {"pearson_r":round(float(r.statistic),4),"p":float(r.pvalue)}
            print(f"  {name} vs sex: r={r.statistic:.3f} P={r.pvalue:.3g}")

    # --- C2 test: orthogonality of the two patterns ---
    cos_ang = float(np.dot(a_first, a_last) / (np.linalg.norm(a_first)*np.linalg.norm(a_last)))
    res["cos_angle_first_vs_last_patient_mode"] = round(cos_ang, 6)
    print(f"  cos(angle) between first/last patterns (patient mode): {cos_ang:.4f}")

    # Persist GSVD output
    np.save(RES/"f2_V.npy", result.V)
    np.save(RES/"f2_c.npy", result.c)
    np.save(RES/"f2_s.npy", result.s)
    res["elapsed_sec"] = round(time.time()-t0,1)
    res["matched_patients"] = common
    with open(RES/f"f2_results_seed{seed}_n{top_n_rna}x{top_n_meth}.json","w") as f:
        json.dump(res, f, indent=2, default=str)
    print(f"== DONE in {res['elapsed_sec']}s ==")
    return res

if __name__ == "__main__":
    out = run(top_n_rna=5000, top_n_meth=10000, seed=0)
