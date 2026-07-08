#!/usr/bin/env python3
"""FRONT 3 — independent TCGA-GBM cohort, GSVD on CNV x expression (the method's
NATIVE copy-number data type, the paper's own prior validation domain).
Tests merit + generalizability + the quantum ablations on independent open data."""
from __future__ import annotations
import json, os, sys, glob
import numpy as np
import pandas as pd

sys.path.insert(0, "code")
import gsvd_reference as G
import survival_stats as S

D = "data/tcga_gbm"; OUT = "results"; os.makedirs(OUT, exist_ok=True)


def submitter_from_fname(fn):
    import re
    m = re.search(r"(TCGA-\d\d-\d{4})", fn)
    return m.group(1) if m else None


def cont_c(t, e, sc):
    m = np.isfinite(t) & np.isfinite(e) & (t > 0) & np.isfinite(sc)
    if m.sum() < 10 or len(np.unique(e[m])) < 2:
        return None, int(m.sum())
    return float(S.concordance_index(t[m], e[m], sc[m])), int(m.sum())


def build_layer_cnv(files_map, patients, gene_col="gene_id", val_col="copy_number"):
    base = pd.read_csv(next(iter(files_map.values())), sep="\t")
    genes = base[gene_col].tolist()
    cols, order = [], []
    for p, fp in files_map.items():
        df = pd.read_csv(fp, sep="\t")
        v = pd.to_numeric(df[val_col], errors="coerce").to_numpy()
        cols.append(v); order.append(p)
    M = np.array(cols).T  # genes x patients
    return M, genes, order


def build_layer_rna(files_map):
    rows = []
    order = []
    genes0 = None
    for p, fp in files_map.items():
        df = pd.read_csv(fp, sep="\t", comment="#")
        # STAR augmented: columns gene_id, ..., unstranded
        if "gene_id" not in df.columns:
            df = pd.read_csv(fp, sep="\t", skiprows=1)
        gid = df["gene_id"] if "gene_id" in df.columns else df.iloc[:,0]
        col = df["unstranded"] if "unstranded" in df.columns else df.iloc[:,3]
        s = pd.Series(pd.to_numeric(col, errors="coerce").to_numpy(), index=gid.astype(str))
        s = s[~s.index.str.startswith("N_")]
        if genes0 is None: genes0 = s.index
        rows.append(s.reindex(genes0).to_numpy()); order.append(p)
    M = np.array(rows).T
    return M, list(genes0), order


def prep(A, k=5000):
    A = np.asarray(A, float)
    A = np.nan_to_num(A, nan=np.nanmedian(A))
    v = A.var(1); i = np.argsort(v)[::-1][:k]; A = A[i]
    return (A - A.mean(1, keepdims=True)) / (A.std(1, keepdims=True) + 1e-9)


def main():
    res = {}
    clin = pd.read_csv(os.path.join(D, "cases_flat.tsv"), sep="\t")
    clin["sub"] = clin["submitter_id"].astype(str).str.extract(r"(TCGA-\d\d-\d{4})")[0]
    clin = clin.dropna(subset=["sub"]).drop_duplicates("sub")
    surv = {r["sub"]: (r["time_days"]/30.44, r["event"]) for _, r in clin.iterrows()
            if pd.notna(r.get("time_days"))}

    # map files -> submitter, one per patient
    def fmap(sub):
        d = {}
        for fp in glob.glob(os.path.join(D, sub, "*")):
            s = submitter_from_fname(os.path.basename(fp))
            if s and s not in d:
                d[s] = fp
        return d
    cnv_files = fmap("cnv"); rna_files = fmap("rna")
    common = [s for s in cnv_files if s in rna_files and s in surv]
    res["matched_cnv_rna_surv"] = len(common)
    if len(common) < 30:
        res["error"] = f"too few matched ({len(common)})"
        json.dump(res, open(os.path.join(OUT,"f3_results.json"),"w"), indent=2, default=str)
        print(json.dumps(res, indent=2)); return
    common = sorted(common)
    cm = {s: cnv_files[s] for s in common}; rm = {s: rna_files[s] for s in common}
    Mc, gc, oc = build_layer_cnv(cm, common)
    Mr, gr_, orr = build_layer_rna(rm)
    # align both to intersection order
    order = [s for s in oc if s in set(orr)]
    ic = [oc.index(s) for s in order]; ir = [orr.index(s) for s in order]
    Mc = Mc[:, ic]; Mr = Mr[:, ir]
    t = np.array([surv[s][0] for s in order]); e = np.array([surv[s][1] for s in order])
    Mr = np.log2(np.nan_to_num(Mr, nan=0)+1)
    L1 = prep(Mc); L2 = prep(Mr)
    res["shapes"] = {"cnv": list(L1.shape), "rna": list(L2.shape), "patients": len(order)}

    gres = G.gsvd(L1, L2); kf, kl = G.antisymmetric_patterns(gres)
    af = gres.V[:, kf]; al = gres.V[:, kl]
    res["C2_orthogonality_cos"] = float(abs(np.dot(af, al)/(np.linalg.norm(af)*np.linalg.norm(al))))
    res["C1_first_C"] = cont_c(t, e, af)[0]
    res["C2_last_C"] = cont_c(t, e, al)[0]
    res["C4_combined_C"] = cont_c(t, e, af - al)[0]
    # logrank for combined 3-class
    comb3 = G.combine_predictors(af, al)
    m = np.isfinite(t)&np.isfinite(e)&(t>0)
    res["C4_combined_logrankP"] = float(S.log_rank(t[m], e[m], comb3[m]).p_value) if len(np.unique(comb3[m]))>1 else None

    # baselines on SAME patients
    # age as a standard prognostic in GBM
    agem = {r["sub"]: r.get("age_at_diagnosis_days") for _, r in clin.iterrows()}
    age = np.array([ (agem.get(s) or np.nan) for s in order ], float)
    res["age_C"] = cont_c(t, e, age)[0]
    U,s_,Vt = np.linalg.svd(L1, full_matrices=False)  # CNV PCA
    res["PCA_cnv_pc1_C"] = cont_c(t, e, Vt[0])[0]
    Um,sm,Vtm = np.linalg.svd(L2, full_matrices=False)  # RNA PCA
    res["PCA_rna_pc1_C"] = cont_c(t, e, Vtm[0])[0]
    res["cnv_alone_pc1to3_C"] = cont_c(t, e, Vt[0]+Vt[1]+Vt[2])[0]
    try:
        from lifelines import CoxPHFitter
        msk = np.isfinite(t)&np.isfinite(e)&(t>0)
        feats = np.hstack([Vt[:10].T, Vtm[:10].T])  # 10 CNV PCs + 10 RNA PCs
        df = pd.DataFrame(feats[msk], columns=[f"f{i}" for i in range(feats.shape[1])])
        df["T"]=t[msk]; df["E"]=e[msk]
        res["penalized_cox_C"] = float(CoxPHFitter(penalizer=0.2).fit(df,"T","E").concordance_index_)
    except Exception as ex:
        res["penalized_cox_C"] = f"err:{str(ex)[:120]}"

    json.dump(res, open(os.path.join(OUT,"f3_results.json"),"w"), indent=2, default=str)
    print(json.dumps(res, indent=2, default=str))


if __name__ == "__main__":
    main()
