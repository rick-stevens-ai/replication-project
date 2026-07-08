#!/usr/bin/env python3
"""
FRONT 2 — GSVD on Cavalli matched MB expression × methylation
(GSE85217 expression + GSE85212 methylation, n=763 patient-matched on
MB_SubtypeStudy_XXXXX ids).

This mirrors the NBL Path-B FRONT 2 protocol exactly:
  D1 = expression (genes × patients), top-N high-variance, row-median-centered
  D2 = methylation beta (CpGs × patients), top-N high-variance, row-median-centered
  GSVD → arraylets most-exclusive to each layer (u1,1 and u1,N analogs)
  Patient-mode coords from V → continuous predictor score
  Compare unsupervised: GSVD vs PCA on each layer

OS: Cavalli's GEO release does NOT include per-sample OS (paper supplement
is paywalled). The honest substitute is subgroup-recovery: in MB, SUBGROUP
is the dominant prognostic axis (Group3 has worst OS, WNT has best — well
established and reproducible in our FRONT 1 mbl_icgc analysis at C=0.61).
Therefore an unsupervised method's prognostic value is bounded by how well
it RECOVERS subgroup from the omic matrices without using subgroup labels.

Tests run here:
  T1. C2 orthogonality: cos(u_first, u_last) (paper claims ~0)
  T2. GSVD arraylet vs subgroup correlation (Pearson, Spearman)
  T3. GSVD 2D nearest-centroid subgroup classification accuracy
  T4. Same tests on top expression PCs (apples-to-apples baseline)
  T5. Group3 vs Group4 binary separation: GSVD vs PC1
  T6. ARI between unsupervised k=4 KMeans on the GSVD 2D map and ground-truth
      subgroup labels; same for PCA top-2.

Output:
  /data/stevens/alter-pediatric-mb/results/f2_gsvd_cavalli.json
"""
from __future__ import annotations
import json, sys, time, gzip
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, "/data/stevens/alter-pediatric-mb/code")
from gsvd_reference import (gsvd, antisymmetric_patterns,
                             classify_patients, combine_predictors)
from survival_stats import cox_univariate, concordance_index, log_rank

DATA = Path("/data/stevens/alter-pediatric-mb/data")
RES  = Path("/data/stevens/alter-pediatric-mb/results")
RES.mkdir(parents=True, exist_ok=True)


def parse_geo_meta(meta_path: Path):
    lines = meta_path.read_text().splitlines()
    titles = None; gsms = None; subgroups = None
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
    if t.endswith("_methylation"):
        return t[:-len("_methylation")]
    return t


def load_expression():
    print("== Loading expression GSE85217 ==")
    t0 = time.time()
    df = pd.read_csv(DATA / "gse85217_exp.txt.gz", sep="\t", low_memory=False)
    print(f"  shape: {df.shape}  ({time.time()-t0:.1f}s)")
    sample_cols = df.columns[5:].tolist()
    pids = [title_to_pid(c) for c in sample_cols]
    gene_ids = df["Probe.Set.Name"].astype(str).tolist()
    gene_symbols = df["HGNC_symbol_from_ensemblv77"].astype(str).tolist()
    X = df[sample_cols].to_numpy(dtype=np.float32)
    print(f"  X expr: {X.shape}  pid_example={pids[:3]}")
    return X, gene_ids, gene_symbols, pids


def load_methylation():
    print("== Loading methylation GSE85212 ==")
    t0 = time.time()
    df = pd.read_csv(DATA / "gse85212_meth_beta.txt.gz", sep="\t", low_memory=False, na_values=["NA",""])
    print(f"  shape: {df.shape}  ({time.time()-t0:.1f}s)")
    cpg_ids = df.iloc[:, 0].astype(str).tolist()
    sample_cols = df.columns[1:].tolist()
    pids = [title_to_pid(c) for c in sample_cols]
    M = df[sample_cols].to_numpy(dtype=np.float32)
    print(f"  M meth: {M.shape}  pid_example={pids[:3]}")
    return M, cpg_ids, pids


def prep_features(X, top_n=5000, log_transform=False):
    if log_transform:
        X = np.log2(X.astype(np.float32) + 1)
    nan_frac = np.isnan(X).mean(axis=1)
    keep = nan_frac < 0.10
    X = X[keep, :]
    if np.isnan(X).any():
        med = np.nanmedian(X, axis=1, keepdims=True)
        inds = np.where(np.isnan(X))
        X = X.copy(); X[inds] = np.take(med.ravel(), inds[0])
    var = X.var(axis=1)
    top = np.argsort(var)[::-1][:top_n]
    X = X[top, :]
    X = X - np.median(X, axis=1, keepdims=True)
    return X.astype(np.float64), top, keep


def kmeans(X, k, seed=0, n_init=10, max_iter=200):
    """Tiny pure-numpy kmeans (n_pat × dim)."""
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    best_labels, best_inertia = None, np.inf
    for trial in range(n_init):
        idx = rng.choice(n, k, replace=False)
        centroids = X[idx].copy()
        for _ in range(max_iter):
            d = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
            labels = d.argmin(axis=1)
            new_centroids = np.array([X[labels == j].mean(axis=0)
                                       if (labels == j).sum() > 0
                                       else centroids[j]
                                       for j in range(k)])
            if np.allclose(new_centroids, centroids): break
            centroids = new_centroids
        inertia = np.sum((X - centroids[labels])**2)
        if inertia < best_inertia:
            best_inertia, best_labels = inertia, labels
    return best_labels


def adjusted_rand(labels_true, labels_pred):
    """ARI from scipy if available, else hand-rolled."""
    try:
        from sklearn.metrics import adjusted_rand_score
        return float(adjusted_rand_score(labels_true, labels_pred))
    except ImportError:
        pass
    # Hand-rolled ARI
    from collections import Counter
    n = len(labels_true)
    a_lab = sorted(set(labels_true)); b_lab = sorted(set(labels_pred))
    ct = np.zeros((len(a_lab), len(b_lab)), dtype=int)
    for i, t in enumerate(labels_true):
        for j, p in enumerate(labels_pred):
            if t == a_lab[ct.shape[0]-1]: pass
        # vectorized below
    # Faster:
    a_idx = {v: i for i, v in enumerate(a_lab)}
    b_idx = {v: i for i, v in enumerate(b_lab)}
    ct = np.zeros((len(a_lab), len(b_lab)), dtype=int)
    for t, p in zip(labels_true, labels_pred):
        ct[a_idx[t], b_idx[p]] += 1
    from math import comb
    n_ij_sum = sum(comb(int(x), 2) for x in ct.ravel())
    a_sum = sum(comb(int(x), 2) for x in ct.sum(axis=1))
    b_sum = sum(comb(int(x), 2) for x in ct.sum(axis=0))
    total = comb(n, 2)
    expected = a_sum * b_sum / total if total > 0 else 0
    maxv = 0.5 * (a_sum + b_sum)
    if maxv == expected:
        return 1.0 if n_ij_sum == expected else 0.0
    return float((n_ij_sum - expected) / (maxv - expected))


def run(top_n_rna=5000, top_n_meth=10000, seed=0):
    t0 = time.time()
    print(f"== F2 pipeline (top_n_rna={top_n_rna}, top_n_meth={top_n_meth}, seed={seed}) ==")

    X_rna, gene_ids, gene_symbols, rna_pids = load_expression()
    M, cpg_ids, meth_pids = load_methylation()

    rna_titles, rna_gsms, rna_sgs_raw = parse_geo_meta(DATA / "gse85217_meta.txt")
    rna_title_to_sg = {title_to_pid(t): normalize_subgroup(s)
                       for t, s in zip(rna_titles, rna_sgs_raw)}
    print(f"  subgroup labels available: {len(rna_title_to_sg)}")

    common = sorted(set(rna_pids) & set(meth_pids))
    print(f"  matched patients (expr ∩ meth): {len(common)}")
    rna_idx  = [rna_pids.index(p)  for p in common]
    meth_idx = [meth_pids.index(p) for p in common]
    X_r = X_rna[:, rna_idx]
    X_m = M[:, meth_idx]
    print(f"  X_r {X_r.shape}  X_m {X_m.shape}")

    D1, top_rna, _ = prep_features(X_r, top_n=top_n_rna, log_transform=False)
    D2, top_meth, _ = prep_features(X_m, top_n=top_n_meth, log_transform=False)
    print(f"  D1 (expr) {D1.shape}  D2 (meth) {D2.shape}")

    print("== Running GSVD ==")
    t1 = time.time()
    result = gsvd(D1, D2)
    print(f"  GSVD done in {time.time()-t1:.1f}s  n_patterns={result.V.shape[1]}")
    print(f"  c/s head: {result.ratio[:5]};  tail: {result.ratio[-5:]}")

    k_first, k_last = antisymmetric_patterns(result)
    ratios = result.ratio
    valid_idx = np.arange(result.V.shape[1])
    valid_idx = valid_idx[(valid_idx != k_first) & (valid_idx != k_last)]
    k_shared = valid_idx[np.argmin(np.abs(np.log(np.maximum(ratios[valid_idx], 1e-300))))]
    print(f"  k_first={k_first} k_last={k_last} k_shared={k_shared}")

    a_first  = result.V[:, k_first]
    a_last   = result.V[:, k_last]
    a_shared = result.V[:, k_shared]

    # T1 orthogonality
    cos_ang = float(np.dot(a_first, a_last) /
                    (np.linalg.norm(a_first) * np.linalg.norm(a_last)))
    print(f"  T1: cos(first,last) patient-mode = {cos_ang:.4f}")

    out = {
        "study": "Cavalli GSE85217×GSE85212 (n=763 patient-matched expr×meth)",
        "n_total": len(common),
        "k_first": int(k_first), "k_last": int(k_last), "k_shared": int(k_shared),
        "ratio_first": float(ratios[k_first]), "ratio_last": float(ratios[k_last]),
        "ratio_shared": float(ratios[k_shared]),
        "T1_cos_first_last_patient_mode": round(cos_ang, 6),
        "top_n_rna": top_n_rna, "top_n_meth": top_n_meth, "seed": seed,
    }

    sg_order = {"WNT": 0, "SHH": 1, "Group4": 2, "Group3": 3}
    sg = [rna_title_to_sg.get(p) for p in common]
    sg_known = np.array([i for i, s in enumerate(sg) if s in sg_order])
    sg_array = np.array([sg[i] for i in sg_known])
    score = np.array([sg_order[s] for s in sg_array], dtype=float)
    print(f"  patients with known subgroup: {len(sg_known)}")
    out["n_with_subgroup"] = int(len(sg_known))
    out["subgroup_distribution"] = {k: int(np.sum(sg_array == k)) for k in sg_order}

    from scipy.stats import pearsonr, spearmanr

    # T2: GSVD arraylet vs prognostic-ordered subgroup score
    for name, a in [("first_pattern", a_first[sg_known]),
                    ("last_pattern", a_last[sg_known]),
                    ("shared_pattern", a_shared[sg_known])]:
        pr = pearsonr(score, a); sr = spearmanr(score, a)
        out[f"T2_{name}_vs_prognostic_score"] = {
            "pearson_r": round(float(pr.statistic), 4),
            "pearson_p": float(pr.pvalue),
            "spearman_r": round(float(sr.statistic), 4),
            "spearman_p": float(sr.pvalue),
        }
        print(f"  T2 {name}: pearson r={pr.statistic:+.3f} P={pr.pvalue:.2e}  spearman r={sr.statistic:+.3f}")

    # T3: 2D nearest-centroid subgroup classification accuracy
    feat = np.column_stack([a_first[sg_known], a_last[sg_known]])
    # standardize
    feat_s = (feat - feat.mean(axis=0)) / (feat.std(axis=0) + 1e-12)
    centroids = {k: feat_s[sg_array == k].mean(axis=0)
                  for k in sg_order if (sg_array == k).sum() >= 3}
    pred = []
    for i in range(len(sg_known)):
        best, best_d = None, np.inf
        for k, c in centroids.items():
            d = np.linalg.norm(feat_s[i] - c)
            if d < best_d: best, best_d = k, d
        pred.append(best)
    pred = np.array(pred)
    acc_gsvd_centroid = float((pred == sg_array).mean())
    out["T3_GSVD_2D_nearest_centroid_subgroup_accuracy"] = round(acc_gsvd_centroid, 4)
    print(f"  T3 GSVD 2D nearest-centroid acc: {acc_gsvd_centroid:.3f}")

    # T6: unsupervised KMeans k=4 ARI vs subgroup
    km_labels_gsvd = kmeans(feat_s, k=4, seed=seed, n_init=20)
    ari_gsvd = adjusted_rand(sg_array, km_labels_gsvd)
    out["T6_GSVD_2D_kmeans4_ARI_vs_subgroup"] = round(float(ari_gsvd), 4)
    print(f"  T6 GSVD 2D KMeans4 ARI vs subgroup: {ari_gsvd:.3f}")

    # T4: PCA baseline on D1 alone (expression) — top 2 patient-mode PCs
    print("== PCA expression baseline (D1 alone) ==")
    Xc = D1 - D1.mean(axis=1, keepdims=True)
    from numpy.linalg import svd
    Uf, Sf, Vtf = svd(Xc, full_matrices=False)
    # Vtf[k, :] are patient-mode coords
    pc = Vtf[:2, sg_known].T  # n_known × 2
    pc_s = (pc - pc.mean(axis=0)) / (pc.std(axis=0) + 1e-12)
    for kk in range(2):
        pr = pearsonr(score, pc[:, kk])
        out[f"T4_expr_PC{kk+1}_vs_prognostic_score"] = {
            "pearson_r": round(float(pr.statistic), 4),
            "pearson_p": float(pr.pvalue),
        }
        print(f"  T4 expr PC{kk+1}: pearson r={pr.statistic:+.3f} P={pr.pvalue:.2e}")
    cents_pca = {k: pc_s[sg_array == k].mean(axis=0)
                  for k in sg_order if (sg_array == k).sum() >= 3}
    pred_pca = []
    for i in range(len(sg_known)):
        best, best_d = None, np.inf
        for k, c in cents_pca.items():
            d = np.linalg.norm(pc_s[i] - c)
            if d < best_d: best, best_d = k, d
        pred_pca.append(best)
    pred_pca = np.array(pred_pca)
    acc_pca_centroid = float((pred_pca == sg_array).mean())
    out["T4_PCA_expr_2D_nearest_centroid_subgroup_accuracy"] = round(acc_pca_centroid, 4)
    km_labels_pca = kmeans(pc_s, k=4, seed=seed, n_init=20)
    ari_pca = adjusted_rand(sg_array, km_labels_pca)
    out["T4_PCA_expr_2D_kmeans4_ARI_vs_subgroup"] = round(float(ari_pca), 4)
    print(f"  T4 PCA-expr 2D nearest-centroid acc: {acc_pca_centroid:.3f}  ARI: {ari_pca:.3f}")

    # T4b: PCA on D2 alone (methylation) — same diagnostic
    Mc = D2 - D2.mean(axis=1, keepdims=True)
    Um, Sm, Vtm = svd(Mc, full_matrices=False)
    pcm = Vtm[:2, sg_known].T
    pcm_s = (pcm - pcm.mean(axis=0)) / (pcm.std(axis=0) + 1e-12)
    for kk in range(2):
        pr = pearsonr(score, pcm[:, kk])
        out[f"T4b_meth_PC{kk+1}_vs_prognostic_score"] = {
            "pearson_r": round(float(pr.statistic), 4),
            "pearson_p": float(pr.pvalue),
        }
        print(f"  T4b meth PC{kk+1}: pearson r={pr.statistic:+.3f} P={pr.pvalue:.2e}")
    cents_pca_m = {k: pcm_s[sg_array == k].mean(axis=0)
                    for k in sg_order if (sg_array == k).sum() >= 3}
    pred_pca_m = []
    for i in range(len(sg_known)):
        best, best_d = None, np.inf
        for k, c in cents_pca_m.items():
            d = np.linalg.norm(pcm_s[i] - c)
            if d < best_d: best, best_d = k, d
        pred_pca_m.append(best)
    pred_pca_m = np.array(pred_pca_m)
    acc_pca_meth = float((pred_pca_m == sg_array).mean())
    km_labels_pca_m = kmeans(pcm_s, k=4, seed=seed, n_init=20)
    ari_pca_m = adjusted_rand(sg_array, km_labels_pca_m)
    out["T4b_PCA_meth_2D_nearest_centroid_subgroup_accuracy"] = round(acc_pca_meth, 4)
    out["T4b_PCA_meth_2D_kmeans4_ARI_vs_subgroup"] = round(float(ari_pca_m), 4)
    print(f"  T4b PCA-meth 2D nearest-centroid acc: {acc_pca_meth:.3f}  ARI: {ari_pca_m:.3f}")

    # T5: Group3 vs Group4 binary -- the CN-driven pair Rick called out.
    g3g4_mask = (sg_array == "Group3") | (sg_array == "Group4")
    y34 = (sg_array[g3g4_mask] == "Group3").astype(int)
    n34 = int(g3g4_mask.sum())
    print(f"  T5: Group3 vs Group4 only, n={n34}")
    # Try the most-discriminant arraylet (compute pearson r vs y34 for ALL patterns)
    if n34 >= 20:
        f1 = a_first[sg_known][g3g4_mask]
        fL = a_last[sg_known][g3g4_mask]
        fS = a_shared[sg_known][g3g4_mask]
        for name, vec in [("first", f1), ("last", fL), ("shared", fS)]:
            pr = pearsonr(y34, vec)
            out[f"T5_GSVD_{name}_pattern_vs_G3G4"] = {
                "pearson_r": round(float(pr.statistic), 4),
                "pearson_p": float(pr.pvalue),
            }
            # 1D classification by sign
            best_acc = 0.0
            for sign in [+1, -1]:
                thr = np.median(sign * vec)
                pred = (sign * vec > thr).astype(int)
                acc = float(max((pred == y34).mean(), (1 - pred == y34).mean()))
                best_acc = max(best_acc, acc)
            out[f"T5_GSVD_{name}_pattern_G3G4_thresh_acc"] = round(best_acc, 4)
            print(f"  T5 {name}: pearson r={pr.statistic:+.3f} P={pr.pvalue:.2e} 1D-thresh acc={best_acc:.3f}")
        # expr PC1 baseline
        pc1_34 = Vtf[0, sg_known][g3g4_mask]
        pr = pearsonr(y34, pc1_34)
        out["T5_expr_PC1_vs_G3G4"] = {
            "pearson_r": round(float(pr.statistic), 4),
            "pearson_p": float(pr.pvalue),
        }
        # meth PC1 baseline
        pcm1_34 = Vtm[0, sg_known][g3g4_mask]
        pr2 = pearsonr(y34, pcm1_34)
        out["T5_meth_PC1_vs_G3G4"] = {
            "pearson_r": round(float(pr2.statistic), 4),
            "pearson_p": float(pr2.pvalue),
        }
        print(f"  T5 expr PC1 vs G3vsG4: r={pr.statistic:+.3f} P={pr.pvalue:.2e}")
        print(f"  T5 meth PC1 vs G3vsG4: r={pr2.statistic:+.3f} P={pr2.pvalue:.2e}")

    # Persist
    np.save(RES / "f2_V.npy", result.V)
    np.save(RES / "f2_c.npy", result.c)
    np.save(RES / "f2_s.npy", result.s)
    np.save(RES / "f2_arraylet_first.npy", a_first)
    np.save(RES / "f2_arraylet_last.npy", a_last)
    out["matched_patients_first10"] = common[:10]
    out["elapsed_sec"] = round(time.time() - t0, 1)
    with open(RES / f"f2_gsvd_cavalli_n{top_n_rna}x{top_n_meth}.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"== DONE in {out['elapsed_sec']}s ==")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--top_rna", type=int, default=5000)
    ap.add_argument("--top_meth", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    run(top_n_rna=args.top_rna, top_n_meth=args.top_meth, seed=args.seed)
