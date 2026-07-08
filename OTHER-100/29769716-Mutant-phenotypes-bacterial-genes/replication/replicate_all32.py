#!/usr/bin/env python3
"""
Full 32-organism replication of Price et al. (2018) Nature 556, 503-507.
"Mutant phenotypes for thousands of bacterial genes of unknown function"

Reimplements:
  1. HypoDesc / PureHypoDesc gene classification from plotfeba.R
  2. Replicate combination: combined_fitness = mean(fitness), combined_t = mean(t)*sqrt(n)
  3. Significant phenotype counting at standard threshold (|f|>0.5, |t|>4)
  4. Per-organism FDR control via threshold grid search on Time0 controls
  5. Specific phenotype counting from deposited files
"""

import pandas as pd
import numpy as np
import os
import re
import json
import sys
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/29769716-Mutant-phenotypes-bacterial-genes/data"
)
RESULTS_DIR = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/29769716-Mutant-phenotypes-bacterial-genes/replication"
)

# All 32 organisms from orginfo.tab
ALL_ORGANISMS = [
    "acidovorax_3H11", "ANA3", "azobra", "BFirm", "Caulo", "Cola",
    "Cup4G11", "Dino", "Dyella79", "HerbieS", "Kang", "Keio",
    "Korea", "Koxy", "Marino", "Miya", "MR1", "Phaeo", "PS",
    "pseudo13_GW456_L13", "pseudo1_N1B4", "pseudo3_N2E3",
    "pseudo5_N2C3_1", "pseudo6_N2E2", "psRCH2", "Pedo557",
    "Ponti", "PV4", "SB2B", "Smeli", "SynE", "WCS417"
]

# Threshold grid for FDR control (from plotfeba.R IdentifyWeakControlFDR)
THRESHOLD_GRID = [
    (0.5, 4.0),
    (0.7, 5.0),
    (0.9, 6.0),
    (1.0, 6.5),
]


def hypo_desc(desc):
    """Exact reimplementation of HypoDesc from plotfeba.R."""
    if pd.isna(desc) or str(desc).strip() == "":
        return True
    desc2 = str(desc).replace(" (RefSeq)", "").replace(" (NCBI)", "").strip()
    desc_lower = desc2.lower().strip()
    
    lc_vague = [
        "membrane protein", "predicted membrane protein", "putative membrane protein",
        "probable transmembrane protein", "signal peptide protein", "lipoprotein",
        "transcriptional regulator", "transcriptional regulators",
        "predicted dna-binding transcriptional regulator", "dna-binding protein",
        "histidine kinase", "sensor histidine kinase",
        "signal transduction histidine kinase", "response regulator receiver protein",
        "serine/threonine protein kinase",
        "abc transporter permease", "abc transporter substrate-binding protein",
        "abc transporter atp-binding protein", "abc transporter",
        "mfs transporter", "rnd transporter", "transporter", "permease",
        "porin", "tonb-dependent receptor",
        "dehydrogenase", "oxidoreductase", "fad-dependent oxidoreductase",
        "methyltransferase", "sam-dependent methyltransferase",
        "atpase", "acetyltransferase", "gcn5-related n-acetyltransferase",
        "aminotransferase", "aminohydrolase", "alpha/beta hydrolase", "hydrolase",
    ]
    if desc_lower in lc_vague:
        return True
    
    vague_patterns = [
        "unknown function", "uncharacterized", "hypothetical",
        "hypothtical",  # typo in original
        "family", "domain protein", "related protein", "transporter related",
    ]
    for pat in vague_patterns:
        if pat.lower() in desc2.lower():
            return True
    return False


def pure_hypo_desc(desc):
    """Exact reimplementation of PureHypoDesc from plotfeba.R."""
    if pd.isna(desc) or str(desc).strip() == "":
        return True
    desc2 = str(desc).replace(" (RefSeq)", "").strip()
    desc2 = re.sub(r' \(NCBI.*?\)', '', desc2).strip()
    desc_lower = desc2.lower()
    
    pure_patterns = ["hypothetical protein", "unknown function", "uncharacterized"]
    for pat in pure_patterns:
        if pat in desc_lower:
            return True
    if re.search(r'TIGR[0-9]+ family protein$', desc2):
        return True
    if desc_lower == "membrane protein":
        return True
    return False


def load_organism_data(org):
    """Load all data files for one organism."""
    org_dir = os.path.join(DATA_DIR, org)
    
    genes = pd.read_csv(os.path.join(org_dir, "fit_genes.tab"), sep="\t")
    lrn = pd.read_csv(os.path.join(org_dir, "fit_logratios_good.tab"), sep="\t")
    t_vals = pd.read_csv(os.path.join(org_dir, "fit_t.tab"), sep="\t")
    quality = pd.read_csv(os.path.join(org_dir, "fit_quality.tab"), sep="\t")
    
    return genes, lrn, t_vals, quality


def get_experiment_columns(lrn, t_vals):
    """Get experiment columns common to fitness and t-statistic matrices."""
    meta_cols_lrn = {'locusId', 'sysName', 'desc', 'comb'}
    meta_cols_t = {'locusId', 'sysName', 'desc'}
    
    exp_cols_lrn = [c for c in lrn.columns if c not in meta_cols_lrn]
    exp_cols_t = [c for c in t_vals.columns if c not in meta_cols_t]
    
    common_exps = [c for c in exp_cols_lrn if c in exp_cols_t]
    return common_exps


def combine_replicates(lrn, t_vals, quality, common_exps):
    """
    Combine biological replicates by condition (short name).
    combined_fitness = mean(fitness across replicates)
    combined_t = mean(t) * sqrt(n_replicates)
    
    Returns combined fitness and t matrices with condition names as columns.
    """
    # Map experiment name -> short name (condition)
    successful = quality[quality['u'] == True] if 'u' in quality.columns else quality[quality['u'] == 'TRUE']
    name_to_short = dict(zip(successful['name'], successful['short']))
    
    # Filter to experiments that are in both common_exps and quality
    # The column names in lrn/t may include both name and short, like "set1IT003 D-Glucose (C)"
    # We need to parse them
    exp_to_short = {}
    for col in common_exps:
        # Column format is typically "setXITNNN short_name" 
        parts = col.split(' ', 1)
        exp_name = parts[0]
        if exp_name in name_to_short:
            exp_to_short[col] = name_to_short[exp_name]
        elif len(parts) > 1:
            # The short name might be the rest
            exp_to_short[col] = parts[1] if parts[1] != 'Time0' else 'Time0'
        else:
            exp_to_short[col] = col
    
    # Group experiments by condition (short name)
    condition_groups = defaultdict(list)
    time0_exps = []
    for col, short in exp_to_short.items():
        if short == 'Time0':
            time0_exps.append(col)
        else:
            condition_groups[short].append(col)
    
    # Build combined matrices
    lrn_indexed = lrn.set_index('locusId')
    t_indexed = t_vals.set_index('locusId')
    common_genes = lrn_indexed.index.intersection(t_indexed.index)
    
    combined_fit = {}
    combined_t = {}
    n_replicates = {}
    
    for cond, cols in condition_groups.items():
        valid_cols = [c for c in cols if c in lrn_indexed.columns and c in t_indexed.columns]
        if not valid_cols:
            continue
        
        n_rep = len(valid_cols)
        n_replicates[cond] = n_rep
        
        fit_vals = lrn_indexed.loc[common_genes, valid_cols].values.astype(float)
        t_vals_arr = t_indexed.loc[common_genes, valid_cols].values.astype(float)
        
        # Replace NaN with 0
        fit_vals = np.nan_to_num(fit_vals, nan=0.0)
        t_vals_arr = np.nan_to_num(t_vals_arr, nan=0.0)
        
        combined_fit[cond] = np.nanmean(fit_vals, axis=1)
        combined_t[cond] = np.nanmean(t_vals_arr, axis=1) * np.sqrt(n_rep)
    
    conditions = sorted(combined_fit.keys())
    fit_matrix = np.column_stack([combined_fit[c] for c in conditions])
    t_matrix = np.column_stack([combined_t[c] for c in conditions])
    
    return common_genes, conditions, fit_matrix, t_matrix, n_replicates, time0_exps


def count_sig_at_threshold(fit_matrix, t_matrix, fit_thresh, t_thresh):
    """Count genes with at least one significant phenotype at given thresholds."""
    sig = (np.abs(fit_matrix) > fit_thresh) & (np.abs(t_matrix) > t_thresh)
    has_phenotype = sig.sum(axis=1) > 0
    return int(has_phenotype.sum()), has_phenotype


def fdr_control(lrn_indexed, t_indexed, common_genes, quality, common_exps, exp_to_short_map):
    """
    Implement per-organism FDR control similar to IdentifyWeakControlFDR.
    Uses Time0 (negative control) experiments to estimate false positive rate.
    Selects the loosest threshold from the grid where FDR <= target.
    
    Returns: selected (fit_thresh, t_thresh) tuple
    """
    # Identify Time0 experiments
    successful = quality[(quality['u'] == True) | (quality['u'] == 'TRUE')]
    name_to_short = dict(zip(successful['name'], successful['short']))
    
    time0_cols = []
    non_time0_cols = []
    for col in common_exps:
        parts = col.split(' ', 1)
        exp_name = parts[0]
        short = name_to_short.get(exp_name, '')
        if short == 'Time0' or (len(parts) > 1 and parts[1] == 'Time0'):
            time0_cols.append(col)
        else:
            non_time0_cols.append(col)
    
    if len(time0_cols) < 2:
        # Not enough Time0 controls — use default threshold
        return (0.5, 4.0), len(time0_cols)
    
    # Get Time0 fitness and t values
    valid_t0 = [c for c in time0_cols if c in lrn_indexed.columns and c in t_indexed.columns]
    if len(valid_t0) < 2:
        return (0.5, 4.0), len(valid_t0)
    
    t0_fit = lrn_indexed.loc[common_genes, valid_t0].values.astype(float)
    t0_t = t_indexed.loc[common_genes, valid_t0].values.astype(float)
    t0_fit = np.nan_to_num(t0_fit, nan=0.0)
    t0_t = np.nan_to_num(t0_t, nan=0.0)
    
    n_genes = len(common_genes)
    n_non_t0 = len(non_time0_cols)
    
    # For each threshold, count false positives in Time0 and real positives in non-Time0
    # FDR ≈ (FP_rate_from_t0 * n_non_t0_exps) / real_positives
    # The paper uses: if the fraction of genes passing threshold in Time0 is > 2/n_non_t0_exps,
    # the threshold is too loose
    
    best_thresh = (0.5, 4.0)
    for ft, tt in THRESHOLD_GRID:
        # False positive rate from Time0
        t0_sig = (np.abs(t0_fit) > ft) & (np.abs(t0_t) > tt)
        # Fraction of genes that are "significant" in any Time0 experiment
        t0_any = t0_sig.sum(axis=1) > 0
        fp_rate = t0_any.sum() / n_genes if n_genes > 0 else 0
        
        # Expected false positives per non-Time0 experiment
        # If fp_rate * n_non_t0 < target (e.g. < 0.05 * n_genes), accept
        # The paper's criterion is more nuanced, but roughly:
        # accept if fewer than 2% of genes are false positives in Time0
        if fp_rate < 0.02:
            best_thresh = (ft, tt)
            break
    
    return best_thresh, len(valid_t0)


def load_specific_phenotypes(org):
    """Load the deposited specific_phenotypes file."""
    sp_path = os.path.join(DATA_DIR, org, "specific_phenotypes")
    try:
        sp = pd.read_csv(sp_path, sep="\t")
        n_genes = sp['locusId'].nunique() if 'locusId' in sp.columns else 0
        n_pairs = len(sp)
        return n_genes, n_pairs
    except Exception:
        return 0, 0


def process_organism(org):
    """Full analysis pipeline for one organism."""
    try:
        genes, lrn, t_vals, quality = load_organism_data(org)
    except Exception as e:
        print(f"  ERROR loading {org}: {e}")
        return None
    
    # Protein-coding genes
    protein_genes = genes[genes['type'] == 1]
    total_protein = len(protein_genes)
    
    # Get experiment columns
    common_exps = get_experiment_columns(lrn, t_vals)
    n_total_experiments = len(common_exps)
    
    # Successful experiments from quality
    if 'u' in quality.columns:
        n_successful = int((quality['u'] == True).sum()) if quality['u'].dtype == bool else int((quality['u'] == 'TRUE').sum())
    else:
        n_successful = n_total_experiments
    
    # Combine replicates
    common_genes, conditions, fit_matrix, t_matrix, n_reps, time0_exps = \
        combine_replicates(lrn, t_vals, quality, common_exps)
    
    n_conditions = len(conditions)
    
    # Also build per-experiment matrices (without combining)
    lrn_indexed = lrn.set_index('locusId')
    t_indexed = t_vals.set_index('locusId')
    
    # Filter common_exps to non-Time0 successful experiments
    successful = quality[(quality['u'] == True) | (quality['u'] == 'TRUE')]
    name_to_short = dict(zip(successful['name'], successful['short']))
    
    non_t0_exps = []
    for col in common_exps:
        parts = col.split(' ', 1)
        exp_name = parts[0]
        short = name_to_short.get(exp_name, '')
        if short != 'Time0' and not (len(parts) > 1 and parts[1] == 'Time0'):
            non_t0_exps.append(col)
    
    # Per-experiment (non-combined) matrices
    valid_exps = [c for c in non_t0_exps if c in lrn_indexed.columns and c in t_indexed.columns]
    n_valid_experiments = len(valid_exps)
    
    if n_valid_experiments == 0 or len(common_genes) == 0:
        print(f"  WARNING: {org} has no valid experiments or genes")
        return None
    
    exp_fit = lrn_indexed.loc[common_genes, valid_exps].values.astype(float)
    exp_t = t_indexed.loc[common_genes, valid_exps].values.astype(float)
    exp_fit = np.nan_to_num(exp_fit, nan=0.0)
    exp_t = np.nan_to_num(exp_t, nan=0.0)
    
    # FDR control 
    fdr_thresh, n_t0 = fdr_control(lrn_indexed, t_indexed, common_genes, quality, common_exps, None)
    
    # Count significant phenotypes at standard threshold using COMBINED replicates
    n_sig_std, has_pheno_std = count_sig_at_threshold(fit_matrix, t_matrix, 0.5, 4.0)
    
    # Count at FDR-controlled threshold using per-experiment data
    n_sig_fdr, has_pheno_fdr = count_sig_at_threshold(exp_fit, exp_t, fdr_thresh[0], fdr_thresh[1])
    
    # Count using combined replicates at FDR threshold
    n_sig_comb_fdr, has_pheno_comb_fdr = count_sig_at_threshold(fit_matrix, t_matrix, fdr_thresh[0], fdr_thresh[1])
    
    # Threshold sensitivity
    thresh_results = {}
    for ft, tt in THRESHOLD_GRID:
        n_sig, _ = count_sig_at_threshold(fit_matrix, t_matrix, ft, tt)
        thresh_results[f"({ft},{tt})"] = n_sig
    
    # Classify genes
    gene_desc_map = dict(zip(genes['locusId'], genes['desc']))
    gene_type_map = dict(zip(genes['locusId'], genes['type']))
    
    gene_ids = common_genes.tolist()
    n_protein_with_data = sum(1 for gid in gene_ids if gene_type_map.get(gid, 0) == 1)
    
    poorly_total = 0
    poorly_with_phenotype_std = 0
    poorly_with_phenotype_fdr = 0
    class_counts = {"A_or_B": 0, "C_vague": 0, "D_hypo": 0}
    
    for i, gid in enumerate(gene_ids):
        if gene_type_map.get(gid, 0) != 1:
            continue
        
        desc = gene_desc_map.get(gid, "")
        is_hypo = hypo_desc(desc)
        is_pure = pure_hypo_desc(desc)
        
        if not is_hypo:
            class_counts["A_or_B"] += 1
        elif not is_pure:
            class_counts["C_vague"] += 1
            poorly_total += 1
            if has_pheno_std[i]:
                poorly_with_phenotype_std += 1
            if has_pheno_comb_fdr[i]:
                poorly_with_phenotype_fdr += 1
        else:
            class_counts["D_hypo"] += 1
            poorly_total += 1
            if has_pheno_std[i]:
                poorly_with_phenotype_std += 1
            if has_pheno_comb_fdr[i]:
                poorly_with_phenotype_fdr += 1
    
    # Specific phenotypes from deposited file
    sp_genes, sp_pairs = load_specific_phenotypes(org)
    
    pct_with_pheno = 100 * n_sig_std / len(common_genes) if len(common_genes) > 0 else 0
    
    result = {
        'org': org,
        'total_protein': total_protein,
        'n_protein_with_data': n_protein_with_data,
        'n_total_experiments': n_total_experiments,
        'n_successful_experiments': n_successful,
        'n_valid_experiments': n_valid_experiments,
        'n_conditions': n_conditions,
        'n_genes_with_data': len(common_genes),
        'n_sig_std': n_sig_std,
        'pct_sig_std': round(pct_with_pheno, 1),
        'fdr_threshold': fdr_thresh,
        'n_t0_controls': n_t0,
        'n_sig_fdr_perexp': n_sig_fdr,
        'n_sig_comb_fdr': n_sig_comb_fdr,
        'class_A_or_B': class_counts["A_or_B"],
        'class_C_vague': class_counts["C_vague"],
        'class_D_hypo': class_counts["D_hypo"],
        'poorly_annotated': poorly_total,
        'poorly_with_phenotype_std': poorly_with_phenotype_std,
        'poorly_with_phenotype_fdr': poorly_with_phenotype_fdr,
        'sp_genes': sp_genes,
        'sp_pairs': sp_pairs,
        'threshold_sensitivity': thresh_results,
    }
    
    return result


def main():
    print("=" * 80)
    print("FULL 32-ORGANISM REPLICATION — Price et al. (2018)")
    print("=" * 80)
    
    results = []
    failed = []
    
    for i, org in enumerate(ALL_ORGANISMS):
        print(f"\n[{i+1}/32] Processing {org}...", end=" ", flush=True)
        r = process_organism(org)
        if r:
            results.append(r)
            print(f"OK — {r['n_conditions']} conditions, "
                  f"{r['n_sig_std']} sig genes, "
                  f"{r['poorly_with_phenotype_std']} poorly-annotated w/ pheno, "
                  f"FDR thresh: {r['fdr_threshold']}")
        else:
            failed.append(org)
            print("FAILED")
    
    # ==================== Summary ====================
    print("\n" + "=" * 120)
    print(f"SUMMARY — {len(results)}/32 organisms processed")
    print("=" * 120)
    
    # Per-organism table
    header = (f"{'Organism':<22} {'Prot':>5} {'wData':>6} {'Exps':>5} {'Conds':>5} "
              f"{'SigGn':>6} {'%Sig':>5} {'Poor':>6} {'PrPh':>6} {'PrFDR':>6} "
              f"{'FDRth':>10} {'SpGn':>5} {'SpPr':>5}")
    print(header)
    print("-" * 120)
    
    for r in results:
        ft, tt = r['fdr_threshold']
        thresh_str = f"({ft},{tt})"
        print(f"{r['org']:<22} {r['total_protein']:>5} {r['n_protein_with_data']:>6} "
              f"{r['n_valid_experiments']:>5} {r['n_conditions']:>5} "
              f"{r['n_sig_std']:>6} {r['pct_sig_std']:>5.1f} "
              f"{r['poorly_annotated']:>6} {r['poorly_with_phenotype_std']:>6} "
              f"{r['poorly_with_phenotype_fdr']:>6} "
              f"{thresh_str:>10} "
              f"{r['sp_genes']:>5} {r['sp_pairs']:>5}")
    
    print("-" * 120)
    
    # Totals
    total_protein = sum(r['total_protein'] for r in results)
    total_with_data = sum(r['n_protein_with_data'] for r in results)
    total_experiments = sum(r['n_valid_experiments'] for r in results)
    total_conditions = sum(r['n_conditions'] for r in results)
    total_sig = sum(r['n_sig_std'] for r in results)
    total_poorly = sum(r['poorly_annotated'] for r in results)
    total_poorly_pheno_std = sum(r['poorly_with_phenotype_std'] for r in results)
    total_poorly_pheno_fdr = sum(r['poorly_with_phenotype_fdr'] for r in results)
    total_sp_genes = sum(r['sp_genes'] for r in results)
    total_sp_pairs = sum(r['sp_pairs'] for r in results)
    
    print(f"{'TOTAL':.<22} {total_protein:>5} {total_with_data:>6} "
          f"{total_experiments:>5} {total_conditions:>5} "
          f"{total_sig:>6} {'':>5} "
          f"{total_poorly:>6} {total_poorly_pheno_std:>6} "
          f"{total_poorly_pheno_fdr:>6} "
          f"{'':>10} "
          f"{total_sp_genes:>5} {total_sp_pairs:>5}")
    
    print(f"\n--- HEADLINE COMPARISON ---")
    print(f"Paper claims:")
    print(f"  Total successful experiments: ~4,870")
    print(f"  Poorly-annotated genes with phenotypes: 11,779")
    print(f"  Specific phenotypes (gene-condition pairs): mentioned but count varies")
    print(f"")
    print(f"Our replication ({len(results)}/32 organisms):")
    print(f"  Total experiments (non-Time0, successful): {total_experiments}")
    print(f"  Total conditions (after combining replicates): {total_conditions}")
    print(f"  Poorly-annotated w/ phenotype (std thresh): {total_poorly_pheno_std}")
    print(f"  Poorly-annotated w/ phenotype (FDR-adjusted): {total_poorly_pheno_fdr}")
    print(f"  Specific phenotype genes (deposited): {total_sp_genes}")
    print(f"  Specific phenotype pairs (deposited): {total_sp_pairs}")
    print(f"  Coverage: {len(results)}/32 = {100*len(results)/32:.1f}%")
    
    if failed:
        print(f"\n  FAILED organisms: {', '.join(failed)}")
    
    # Save results
    outpath = os.path.join(RESULTS_DIR, "results_all32.json")
    # Convert tuples to lists for JSON
    for r in results:
        r['fdr_threshold'] = list(r['fdr_threshold'])
    with open(outpath, 'w') as f:
        json.dump({
            'results': results,
            'failed': failed,
            'totals': {
                'n_processed': len(results),
                'n_total': 32,
                'total_protein': total_protein,
                'total_with_data': total_with_data,
                'total_experiments': total_experiments,
                'total_conditions': total_conditions,
                'total_sig_std': total_sig,
                'total_poorly': total_poorly,
                'total_poorly_pheno_std': total_poorly_pheno_std,
                'total_poorly_pheno_fdr': total_poorly_pheno_fdr,
                'total_sp_genes': total_sp_genes,
                'total_sp_pairs': total_sp_pairs,
            }
        }, f, indent=2)
    print(f"\nResults saved to {outpath}")
    
    return results, failed


if __name__ == "__main__":
    main()
