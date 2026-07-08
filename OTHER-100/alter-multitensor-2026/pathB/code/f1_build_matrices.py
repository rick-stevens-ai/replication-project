#!/usr/bin/env python3
"""
FRONT 1 — Build patient×gene expression matrix and merged clinical table,
then compute the standard-of-care baseline (MYCN, INSS, age) survival
statistics. This is the bar Front 2/Front 3 GSVD predictors must beat.

Outputs (under /data/stevens/alter-pathB/data/target_nbl/):
    expression_matrix.npy             - genes x patients float32 (raw STAR unstranded counts)
    expression_log2.npy               - log2(counts+1)
    gene_ids.txt
    patient_ids.txt
    clinical_merged.tsv               - one row per RNA patient, with all clinical fields
    
Outputs (under /data/stevens/alter-pathB/results/):
    f1_baseline_table.json            - survival_stats.report dict for MYCN / INSS / age / sex
    f1_baseline_summary.md            - human-readable
"""
from __future__ import annotations
import json, sys, os, glob, time
from pathlib import Path
import numpy as np
import pandas as pd
import openpyxl

sys.path.insert(0, "/data/stevens/alter-pathB/code")
from survival_stats import report as sv_report

DATA = Path("/data/stevens/alter-pathB/data/target_nbl")
RESULTS = Path("/data/stevens/alter-pathB/results")
RESULTS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load clinical (Discovery + Validation), keyed by TARGET USI
# ---------------------------------------------------------------------------
def load_clinical():
    rows = []
    sources = []
    for fp in sorted(glob.glob(str(DATA / "clinical" / "*ClinicalData_*xlsx"))):
        src = "Discovery" if "Discovery" in fp else "Validation"
        sources.append((src, fp))
        wb = openpyxl.load_workbook(fp, data_only=True)
        ws = wb["Clinical Data"]
        data = list(ws.iter_rows(values_only=True))
        header = list(data[0])
        for r in data[1:]:
            if not r or not r[0]:
                continue
            d = dict(zip(header, r))
            d["source_cohort"] = src
            rows.append(d)
    df = pd.DataFrame(rows)
    print(f"  clinical rows = {len(df)} (Discovery + Validation, deduped below)")
    # Deduplicate by USI keeping Discovery (paper used Discovery as primary)
    df["priority"] = (df["source_cohort"] == "Discovery").astype(int)
    df = df.sort_values("priority", ascending=False).drop_duplicates("TARGET USI", keep="first")
    df = df.drop(columns=["priority"])
    print(f"  after dedup-by-USI = {len(df)}")
    return df


# ---------------------------------------------------------------------------
# 2. Load STAR-Counts files; build genes x patients matrix
# ---------------------------------------------------------------------------
def load_expression():
    files_meta = pd.read_csv(DATA / "files_geq.tsv", sep="\t")
    files_meta = files_meta.dropna(subset=["case_submitter"])
    # Prefer Primary Tumor; if multiple files per patient, take the first
    primary = files_meta[files_meta["sample_type"] == "Primary Tumor"].copy()
    primary = primary.sort_values("file_id").drop_duplicates("case_submitter", keep="first")
    print(f"  primary-tumor RNA-Seq files (one per patient) = {len(primary)}")
    # Load gene order from the first file
    first = DATA / "expression" / f"{primary.iloc[0]['file_id']}.tsv"
    df0 = pd.read_csv(first, sep="\t", comment="#", skiprows=0)
    # The format has 4 lines of N_unmapped/etc; gene rows start at ENSG...
    df0 = df0[df0["gene_id"].str.startswith("ENSG", na=False)].reset_index(drop=True)
    gene_ids = df0["gene_id"].tolist()
    gene_names = df0["gene_name"].tolist()
    gene_types = df0["gene_type"].tolist()
    n_genes = len(gene_ids)
    patient_ids = primary["case_submitter"].tolist()
    n_patients = len(patient_ids)
    print(f"  matrix shape will be {n_genes} genes x {n_patients} patients")
    X = np.zeros((n_genes, n_patients), dtype=np.float32)
    for j, (_, row) in enumerate(primary.iterrows()):
        fp = DATA / "expression" / f"{row['file_id']}.tsv"
        df = pd.read_csv(fp, sep="\t", comment="#")
        df = df[df["gene_id"].str.startswith("ENSG", na=False)].reset_index(drop=True)
        if len(df) != n_genes:
            print(f"  WARN: {fp.name} has {len(df)} gene rows, expected {n_genes}")
            df = df.set_index("gene_id").reindex(gene_ids).reset_index()
        X[:, j] = df["unstranded"].fillna(0).to_numpy(dtype=np.float32)
        if (j + 1) % 25 == 0:
            print(f"  loaded {j+1}/{n_patients}")
    return X, gene_ids, gene_names, gene_types, patient_ids


# ---------------------------------------------------------------------------
# 3. Merge clinical onto patient list
# ---------------------------------------------------------------------------
def merge_clinical(clinical_df, patient_ids):
    cl = clinical_df.set_index("TARGET USI")
    # USIs in expression: e.g. TARGET-30-PAPTLD; clinical USI may be TARGET-30-PAPTLD or PAPTLD
    rows = []
    for pid in patient_ids:
        short = pid.replace("TARGET-30-", "")
        if pid in cl.index:
            r = cl.loc[pid].to_dict()
        elif short in cl.index:
            r = cl.loc[short].to_dict()
        else:
            r = {c: None for c in cl.columns}
        r["patient_id"] = pid
        rows.append(r)
    out = pd.DataFrame(rows)
    matched = out["Vital Status"].notna().sum()
    print(f"  clinical merged: {matched}/{len(out)} have Vital Status")
    return out


# ---------------------------------------------------------------------------
# 4. Compute survival_stats.report for MYCN, INSS, age, sex baselines
# ---------------------------------------------------------------------------
def baseline_stats(cl):
    out = {}
    # Build (times, events) from Overall Survival Time + Vital Status
    times = pd.to_numeric(cl["Overall Survival Time in Days"], errors="coerce").to_numpy()
    vs = cl["Vital Status"].astype(str).str.strip()
    events = (vs == "Dead").astype(int).to_numpy()
    valid = ~np.isnan(times) & (times > 0)
    print(f"  patients with valid (time>0, vital) = {valid.sum()}")
    times = times[valid]; events = events[valid]
    cl_v = cl[valid].reset_index(drop=True)

    # --- MYCN baseline ---
    mycn = cl_v["MYCN status"].astype(str).str.strip().str.lower()
    # "Amplified" vs "Not Amplified" (other strings -> NaN -> excluded)
    mycn_map = mycn.map({"amplified": 1, "not amplified": 0})
    m = mycn_map.notna()
    if m.sum() >= 20:
        rep = sv_report(times[m], events[m], mycn_map[m].to_numpy(dtype=int), "MYCN_amplification")
        out["MYCN_amplification"] = rep
        print(f"  MYCN baseline: n={rep['n_total']} events={rep['n_events']} "
              f"C={rep['concordance']} HR={rep['cox_hr']} CI={rep['cox_ci']} "
              f"logrankP={rep['logrank_p']:.3g}")

    # --- INSS stage ---
    inss_raw = cl_v["INSS Stage"].astype(str).str.strip()
    # TARGET stores values as 'Stage 1', 'Stage 2A', ..., 'Stage 4', 'Stage 4s', 'Stage 3'.
    inss_map = {
        "Stage 1": 1, "Stage 2A": 2, "Stage 2B": 3, "Stage 3": 4,
        "Stage 4": 5, "Stage 4s": 0, "Stage 4S": 0,
        "1":1, "2A":2, "2B":3, "3":4, "4":5, "4S":0, "4s":0,
    }
    inss_lab = inss_raw.map(inss_map)
    # Binary high-stage (Stage 4 only) variant for direct comparison with paper
    inss_high = (inss_raw == "Stage 4").astype(int)
    m2 = inss_lab.notna()
    if m2.sum() >= 20:
        rep = sv_report(times[m2], events[m2], inss_lab[m2].to_numpy(dtype=int), "INSS_stage")
        out["INSS_stage"] = rep
        print(f"  INSS baseline (ordered): n={rep['n_total']} events={rep['n_events']} "
              f"C={rep['concordance']} HR={rep['cox_hr']} logrankP={rep['logrank_p']:.3g}")
        rep2 = sv_report(times[m2], events[m2], inss_high[m2].to_numpy(dtype=int), "INSS_stage4_binary")
        out["INSS_stage4_binary"] = rep2
        print(f"  INSS Stage-4 binary: n={rep2['n_total']} events={rep2['n_events']} "
              f"C={rep2['concordance']} HR={rep2['cox_hr']} logrankP={rep2['logrank_p']:.3g}")

    # --- Age at diagnosis (binary >= 18 months threshold like paper) ---
    age = pd.to_numeric(cl_v["Age at Diagnosis in Days"], errors="coerce")
    age_high = (age >= 18 * 30.4375).astype(int)
    m3 = age.notna()
    if m3.sum() >= 20:
        rep = sv_report(times[m3], events[m3], age_high[m3].to_numpy(dtype=int), "age_ge_18mo")
        out["age_ge_18mo"] = rep
        print(f"  Age>=18mo: n={rep['n_total']} events={rep['n_events']} "
              f"C={rep['concordance']} HR={rep['cox_hr']} logrankP={rep['logrank_p']:.3g}")

    # --- Sex ---
    sex = cl_v["Gender"].astype(str).str.strip().str.lower().map({"male":0, "female":1})
    m4 = sex.notna()
    if m4.sum() >= 20:
        rep = sv_report(times[m4], events[m4], sex[m4].to_numpy(dtype=int), "sex")
        out["sex"] = rep
        print(f"  Sex: n={rep['n_total']} events={rep['n_events']} "
              f"C={rep['concordance']} HR={rep['cox_hr']} logrankP={rep['logrank_p']:.3g}")

    # --- COG Risk Group ---
    cog = cl_v["COG Risk Group"].astype(str).str.strip()
    cog_map = {"Low Risk":0,"Intermediate Risk":1,"High Risk":2}
    cog_lab = cog.map(cog_map)
    m5 = cog_lab.notna()
    if m5.sum() >= 20:
        rep = sv_report(times[m5], events[m5], cog_lab[m5].to_numpy(dtype=int), "COG_risk")
        out["COG_risk"] = rep
        print(f"  COG Risk: n={rep['n_total']} events={rep['n_events']} "
              f"C={rep['concordance']} HR={rep['cox_hr']} logrankP={rep['logrank_p']:.3g}")
    return out


def main():
    t0 = time.time()
    print("== Loading clinical (XLSX) ==")
    clinical_df = load_clinical()
    print("== Loading expression matrix (STAR Counts) ==")
    X, gene_ids, gene_names, gene_types, patient_ids = load_expression()
    np.save(DATA / "expression_matrix.npy", X)
    # log2(counts + 1)
    Xl = np.log2(X.astype(np.float32) + 1)
    np.save(DATA / "expression_log2.npy", Xl)
    (DATA / "gene_ids.txt").write_text("\n".join(gene_ids))
    (DATA / "gene_names.txt").write_text("\n".join(gene_names))
    (DATA / "gene_types.txt").write_text("\n".join(gene_types))
    (DATA / "patient_ids.txt").write_text("\n".join(patient_ids))
    print(f"  saved expression matrices, X.shape = {X.shape}")
    print("== Merging clinical onto RNA patients ==")
    merged = merge_clinical(clinical_df, patient_ids)
    merged.to_csv(DATA / "clinical_merged.tsv", sep="\t", index=False)
    # FULL clinical (Discovery+Validation, not RNA-restricted) for baseline
    print("== Computing standard-of-care baseline survival stats (FULL clinical) ==")
    out_full = baseline_stats(clinical_df)
    print("== Computing baseline survival stats (RNA-restricted subset, n=" 
          + str(len(merged)) + ") ==")
    out_rna = baseline_stats(merged)
    payload = {
        "n_clinical_total": int(len(clinical_df)),
        "n_rna_patients": int(len(patient_ids)),
        "baseline_full_cohort": out_full,
        "baseline_rna_subset": out_rna,
        "elapsed_sec": round(time.time() - t0, 1),
    }
    with open(RESULTS / "f1_baseline_table.json", "w") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"== DONE in {payload['elapsed_sec']}s ==")


if __name__ == "__main__":
    main()
