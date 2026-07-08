#!/usr/bin/env python3
"""
FRONT 3 — Subgroup-restricted GSVD on Group3 + Group4 patients only.

Rick's "sharpest pediatric-CN-specific test": the analog Alter et al. claim
for NBL is that the GSVD finds a tumor-exclusive pattern that prognosticates
within an open CN-driven cohort. In MB, the canonical CN-driven contrast is
Group3 (MYC-amplified, isochromosome 17q frequent) vs Group4 (isodicentric-
17q, the most common). Both are aggressively CN-driven; if the method works
for pediatric CN biology, it should find a survival-relevant axis here.

Procedure:
  1. Take Cavalli matched expr×meth cohort, restrict to subgroup ∈ {Group3, Group4}
  2. Re-run GSVD on this restricted matched cohort
  3. Score each patient with the first/last/shared arraylet
  4. Evaluate against the subgroup label and against the established
     prognostic ordering (Group3 worst within {G3,G4}).
  5. Compare GSVD vs PCA-on-each-layer at the same restricted task.

Output:
  /data/stevens/alter-pediatric-mb/results/f3_gsvd_g3g4.json
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, "/data/stevens/alter-pediatric-mb/code")
from gsvd_reference import gsvd, antisymmetric_patterns

DATA = Path("/data/stevens/alter-pediatric-mb/data")
RES  = Path("/data/stevens/alter-pediatric-mb/results")
RES.mkdir(parents=True, exist_ok=True)


def parse_geo_meta(p: Path):
    lines = p.read_text().splitlines()
    titles = gsms = subgroups = None
    for ln in lines:
        if ln.startswith("!Sample_title\t"):
            titles = [t.strip('"') for t in ln.split("\t")[1:]]
        elif ln.startswith("!Sample_geo_accession\t"):
            gsms = [t.strip('"') for t in ln.split("\t")[1:]]
        elif ln.startswith("!Sample_characteristics_ch1\t") and "subgroup:" in ln.lower():
            row = [t.strip('"') for t in ln.split("\t")[1:]]
            subgroups = [v.split(":", 1)[1].strip() if ":" in v else "" for v in row]
            break
    return titles, gsms, subgroups


def normalize_subgroup(s):
    if s is None or s == "": return None
    up = s.strip().replace(" ", "").upper()
    if up.startswith("SHH"): return "SHH"
    if up.startswith("WNT"): return "WNT"
    if "GRP3" in up or "GROUP3" in up: return "Group3"
    if "GRP4" in up or "GROUP4" in up: return "Group4"
    return None


def title_to_pid(t):
    return t[:-len("_methylation")] if t.endswith("_methylation") else t


def prep_features(X, top_n, log_transform=False):
    if log_transform:
        X = np.log2(X.astype(np.float32) + 1)
    nan_frac = np.isnan(X).mean(axis=1)
    keep = nan_frac < 0.10
    X = X[keep]
    if np.isnan(X).any():
        med = np.nanmedian(X, axis=1, keepdims=True)
        inds = np.where(np.isnan(X))
        X = X.copy(); X[inds] = np.take(med.ravel(), inds[0])
    v = X.var(axis=1)
    top = np.argsort(v)[::-1][:top_n]
    X = X[top]
    X = X - np.median(X, axis=1, keepdims=True)
    return X.astype(np.float64), top, keep


def main(top_rna=5000, top_meth=10000, seed=0):
    t0 = time.time()
    print(f"== F3 Group3+Group4 restricted GSVD (top_rna={top_rna}, top_meth={top_meth}) ==")
    rna_titles, _, sgs = parse_geo_meta(DATA / "gse85217_meta.txt")
    pid_to_sg = {title_to_pid(t): normalize_subgroup(s) for t, s in zip(rna_titles, sgs)}
    print(f"  subgroups available: {sum(1 for v in pid_to_sg.values() if v)}")

    # Load expr
    df = pd.read_csv(DATA / "gse85217_exp.txt.gz", sep="\t", low_memory=False)
    sample_cols = df.columns[5:].tolist()
    rna_pids = [title_to_pid(c) for c in sample_cols]
    X_rna = df[sample_cols].to_numpy(dtype=np.float32)
    print(f"  expr loaded {X_rna.shape}")

    # Load meth
    dfm = pd.read_csv(DATA / "gse85212_meth_beta.txt.gz", sep="\t", low_memory=False, na_values=["NA",""])
    sample_cols_m = dfm.columns[1:].tolist()
    meth_pids = [title_to_pid(c) for c in sample_cols_m]
    M = dfm[sample_cols_m].to_numpy(dtype=np.float32)
    print(f"  meth loaded {M.shape}")

    # Intersect, restrict to Group3 + Group4
    common = sorted(set(rna_pids) & set(meth_pids))
    g3g4 = [p for p in common if pid_to_sg.get(p) in ("Group3", "Group4")]
    print(f"  matched ∩ G3∪G4: {len(g3g4)}")
    sg_array = np.array([pid_to_sg[p] for p in g3g4])
    print(f"  G3={int(np.sum(sg_array=='Group3'))}  G4={int(np.sum(sg_array=='Group4'))}")

    rna_idx = [rna_pids.index(p) for p in g3g4]
    meth_idx = [meth_pids.index(p) for p in g3g4]
    X_r = X_rna[:, rna_idx]
    X_m = M[:, meth_idx]

    D1, _, _ = prep_features(X_r, top_n=top_rna)
    D2, _, _ = prep_features(X_m, top_n=top_meth)
    print(f"  D1 {D1.shape}  D2 {D2.shape}")

    print("== Running GSVD on G3+G4 only ==")
    t1 = time.time()
    res = gsvd(D1, D2)
    print(f"  GSVD done in {time.time()-t1:.1f}s; n_patterns={res.V.shape[1]}")
    print(f"  c/s head: {res.ratio[:5]};  tail: {res.ratio[-5:]}")

    k_first, k_last = antisymmetric_patterns(res)
    valid_idx = np.arange(res.V.shape[1])
    valid_idx = valid_idx[(valid_idx != k_first) & (valid_idx != k_last)]
    k_shared = valid_idx[np.argmin(np.abs(np.log(np.maximum(res.ratio[valid_idx], 1e-300))))]
    a_first = res.V[:, k_first]
    a_last  = res.V[:, k_last]
    a_shared = res.V[:, k_shared]

    cos_ang = float(np.dot(a_first, a_last) /
                    (np.linalg.norm(a_first) * np.linalg.norm(a_last)))
    print(f"  cos(first,last) = {cos_ang:.4f}")

    y = (sg_array == "Group3").astype(int)  # 1 if Group3
    from scipy.stats import pearsonr

    out = {
        "study": "Cavalli GSE85217×GSE85212 restricted to Group3+Group4 only",
        "n_total": int(len(g3g4)),
        "n_g3": int(y.sum()),
        "n_g4": int(len(y) - y.sum()),
        "cos_first_last_patient_mode": round(cos_ang, 6),
        "k_first": int(k_first), "k_last": int(k_last), "k_shared": int(k_shared),
        "ratio_first": float(res.ratio[k_first]),
        "ratio_last": float(res.ratio[k_last]),
        "ratio_shared": float(res.ratio[k_shared]),
        "top_n_rna": top_rna, "top_n_meth": top_meth,
    }

    # Each pattern vs Group3 binary label
    for name, vec in [("first", a_first), ("last", a_last), ("shared", a_shared)]:
        pr = pearsonr(y, vec)
        # 1D threshold classification — pick best sign+threshold (use median)
        best_acc = 0.0
        for sign in [+1, -1]:
            thr = np.median(sign * vec)
            pred = (sign * vec > thr).astype(int)
            acc = float(max((pred == y).mean(), ((1 - pred) == y).mean()))
            best_acc = max(best_acc, acc)
        out[f"GSVD_{name}_pattern_vs_Group3"] = {
            "pearson_r": round(float(pr.statistic), 4),
            "pearson_p": float(pr.pvalue),
            "1D_threshold_accuracy": round(best_acc, 4),
        }
        print(f"  GSVD {name}: r={pr.statistic:+.3f} P={pr.pvalue:.2e}  1D acc={best_acc:.3f}")

    # PCA baselines for comparison
    from numpy.linalg import svd
    Xc = D1 - D1.mean(axis=1, keepdims=True)
    Uf, Sf, Vtf = svd(Xc, full_matrices=False)
    Mc = D2 - D2.mean(axis=1, keepdims=True)
    Um, Sm, Vtm = svd(Mc, full_matrices=False)
    for kk in range(3):
        pr_e = pearsonr(y, Vtf[kk])
        pr_m = pearsonr(y, Vtm[kk])
        out[f"expr_PC{kk+1}_vs_Group3"] = {
            "pearson_r": round(float(pr_e.statistic), 4),
            "pearson_p": float(pr_e.pvalue),
        }
        out[f"meth_PC{kk+1}_vs_Group3"] = {
            "pearson_r": round(float(pr_m.statistic), 4),
            "pearson_p": float(pr_m.pvalue),
        }
        print(f"  expr PC{kk+1}: r={pr_e.statistic:+.3f} P={pr_e.pvalue:.2e}    meth PC{kk+1}: r={pr_m.statistic:+.3f} P={pr_m.pvalue:.2e}")

    # 2D GSVD nearest-centroid classification G3 vs G4
    feat = np.column_stack([a_first, a_last])
    feat_s = (feat - feat.mean(axis=0)) / (feat.std(axis=0) + 1e-12)
    cg3 = feat_s[y == 1].mean(axis=0)
    cg4 = feat_s[y == 0].mean(axis=0)
    d_g3 = np.linalg.norm(feat_s - cg3, axis=1)
    d_g4 = np.linalg.norm(feat_s - cg4, axis=1)
    pred = (d_g3 < d_g4).astype(int)
    acc_gsvd = float((pred == y).mean())
    out["GSVD_2D_centroid_G3vsG4_accuracy"] = round(acc_gsvd, 4)
    print(f"  GSVD 2D centroid G3vsG4 acc: {acc_gsvd:.3f}")

    # 2D PCA-expr centroid baseline
    pc_e = np.column_stack([Vtf[0], Vtf[1]])
    pc_e_s = (pc_e - pc_e.mean(axis=0)) / (pc_e.std(axis=0) + 1e-12)
    cg3_e = pc_e_s[y == 1].mean(axis=0); cg4_e = pc_e_s[y == 0].mean(axis=0)
    pred_e = (np.linalg.norm(pc_e_s - cg3_e, axis=1) < np.linalg.norm(pc_e_s - cg4_e, axis=1)).astype(int)
    acc_pca_e = float((pred_e == y).mean())
    out["PCA_expr_2D_centroid_G3vsG4_accuracy"] = round(acc_pca_e, 4)
    print(f"  PCA-expr 2D centroid G3vsG4 acc: {acc_pca_e:.3f}")
    # 2D PCA-meth centroid
    pc_m = np.column_stack([Vtm[0], Vtm[1]])
    pc_m_s = (pc_m - pc_m.mean(axis=0)) / (pc_m.std(axis=0) + 1e-12)
    cg3_m = pc_m_s[y == 1].mean(axis=0); cg4_m = pc_m_s[y == 0].mean(axis=0)
    pred_m = (np.linalg.norm(pc_m_s - cg3_m, axis=1) < np.linalg.norm(pc_m_s - cg4_m, axis=1)).astype(int)
    acc_pca_m = float((pred_m == y).mean())
    out["PCA_meth_2D_centroid_G3vsG4_accuracy"] = round(acc_pca_m, 4)
    print(f"  PCA-meth 2D centroid G3vsG4 acc: {acc_pca_m:.3f}")

    out["elapsed_sec"] = round(time.time() - t0, 1)
    with open(RES / "f3_gsvd_g3g4.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"== DONE in {out['elapsed_sec']}s ==")
    return out


if __name__ == "__main__":
    main()
