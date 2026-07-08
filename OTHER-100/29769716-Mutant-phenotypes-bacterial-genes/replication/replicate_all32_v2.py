#!/usr/bin/env python3
"""
Full 32-organism replication of Price et al. (2018) Nature 556, 503-507.
"Mutant phenotypes for thousands of bacterial genes of unknown function"

v2: Proper FDR control using Time0 columns in fit_t.tab

Key insight from the data structure:
- fit_logratios_good.tab: fitness values for SUCCESSFUL non-Time0 experiments only
- fit_t.tab: t-statistics for ALL experiments including Time0
- Time0 experiments are negative controls with u=FALSE in fit_quality.tab
- The FDR control compares phenotype calls in Time0 vs real experiments

IdentifyWeakControlFDR logic (from plotfeba.R):
  For each threshold pair (fit, t):
    Count genes with |fitness|>fit & |t|>t in Time0 experiments
    Count genes with |fitness|>fit & |t|>t in real experiments  
    If Time0 false-positive rate is too high, use stricter threshold
    
  The paper says most organisms used the standard (0.5, 4) but some needed
  stricter thresholds. The criterion is roughly:
    n_false_positives_in_t0 < 2% of tested genes, OR
    FDR = (FP_rate * n_real_exps) / n_real_positives < 0.05
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

ALL_ORGANISMS = [
    "acidovorax_3H11", "ANA3", "azobra", "BFirm", "Caulo", "Cola",
    "Cup4G11", "Dino", "Dyella79", "HerbieS", "Kang", "Keio",
    "Korea", "Koxy", "Marino", "Miya", "MR1", "Phaeo", "PS",
    "pseudo13_GW456_L13", "pseudo1_N1B4", "pseudo3_N2E3",
    "pseudo5_N2C3_1", "pseudo6_N2E2", "psRCH2", "Pedo557",
    "Ponti", "PV4", "SB2B", "Smeli", "SynE", "WCS417"
]

# Threshold grid for FDR control (from plotfeba.R)
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
        "hypothtical", "family", "domain protein", "related protein",
        "transporter related",
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


def load_specific_phenotypes(org):
    """Load deposited specific_phenotypes file."""
    sp_path = os.path.join(DATA_DIR, org, "specific_phenotypes")
    try:
        sp = pd.read_csv(sp_path, sep="\t")
        n_genes = sp['locusId'].nunique() if 'locusId' in sp.columns else 0
        n_pairs = len(sp)
        return n_genes, n_pairs
    except:
        return 0, 0


def process_organism(org):
    """Full analysis pipeline for one organism with proper FDR control."""
    org_dir = os.path.join(DATA_DIR, org)
    
    try:
        genes = pd.read_csv(os.path.join(org_dir, "fit_genes.tab"), sep="\t")
        lrn = pd.read_csv(os.path.join(org_dir, "fit_logratios_good.tab"), sep="\t")
        t_vals = pd.read_csv(os.path.join(org_dir, "fit_t.tab"), sep="\t")
        quality = pd.read_csv(os.path.join(org_dir, "fit_quality.tab"), sep="\t")
    except Exception as e:
        print(f"  ERROR loading {org}: {e}")
        return None
    
    # Parse quality to identify Time0 and successful experiments
    # u column: TRUE = successful, FALSE = failed/Time0
    quality['u_bool'] = quality['u'].astype(str).str.upper() == 'TRUE'
    
    name_to_short = dict(zip(quality['name'], quality['short']))
    name_to_success = dict(zip(quality['name'], quality['u_bool']))
    
    # Total protein-coding genes
    protein_genes = genes[genes['type'] == 1]
    total_protein = len(protein_genes)
    
    # Parse column names in logratios and t files
    meta_cols_lrn = {'locusId', 'sysName', 'desc', 'comb'}
    meta_cols_t = {'locusId', 'sysName', 'desc'}
    
    exp_cols_lrn = [c for c in lrn.columns if c not in meta_cols_lrn]
    exp_cols_t = [c for c in t_vals.columns if c not in meta_cols_t]
    
    # Map column names to experiment names and short names
    def parse_col(col):
        """Parse column like 'set1IT003 D-Glucose (C)' -> (set1IT003, D-Glucose (C))"""
        parts = col.split(' ', 1)
        return parts[0], (parts[1] if len(parts) > 1 else '')
    
    # Identify Time0 columns in t_vals (these are NOT in logratios)
    t0_cols_in_t = []
    real_cols_in_t = []
    for col in exp_cols_t:
        exp_name, short = parse_col(col)
        exp_short = name_to_short.get(exp_name, short)
        if exp_short == 'Time0' or short == 'Time0':
            t0_cols_in_t.append(col)
        else:
            real_cols_in_t.append(col)
    
    # Real experiment columns common between logratios and t
    common_real_exps = [c for c in exp_cols_lrn if c in set(exp_cols_t)]
    
    # Successful experiments count (as the paper defines it)
    n_successful = int(quality['u_bool'].sum())
    n_total_quality = len(quality)
    
    # Count non-Time0 successful experiments (= what goes into fit_logratios_good)
    n_non_t0_successful = len(common_real_exps)
    
    # Build gene indices
    lrn_indexed = lrn.set_index('locusId')
    t_indexed = t_vals.set_index('locusId')
    common_genes = lrn_indexed.index.intersection(t_indexed.index)
    
    if len(common_genes) == 0:
        return None
    
    # ===== COMBINE REPLICATES =====
    # Group real experiments by condition (short name)
    condition_groups = defaultdict(list)
    for col in common_real_exps:
        exp_name, short = parse_col(col)
        exp_short = name_to_short.get(exp_name, short)
        if exp_short and exp_short != 'Time0':
            condition_groups[exp_short].append(col)
    
    # Build combined fitness and t matrices
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
        fit_vals = np.nan_to_num(fit_vals, nan=0.0)
        t_vals_arr = np.nan_to_num(t_vals_arr, nan=0.0)
        
        combined_fit[cond] = np.nanmean(fit_vals, axis=1)
        combined_t[cond] = np.nanmean(t_vals_arr, axis=1) * np.sqrt(n_rep)
    
    conditions = sorted(combined_fit.keys())
    n_conditions = len(conditions)
    
    if n_conditions == 0:
        return None
    
    comb_fit_matrix = np.column_stack([combined_fit[c] for c in conditions])
    comb_t_matrix = np.column_stack([combined_t[c] for c in conditions])
    
    # ===== FDR CONTROL using Time0 =====
    # Time0 experiments exist in fit_t.tab but NOT in fit_logratios_good.tab
    # For FDR control, we need t-values for Time0.
    # The paper's IdentifyWeakControlFDR uses t-values from Time0 experiments.
    # Since fit_logratios_good doesn't have Time0, we use only t-values for FDR check.
    # The key criterion: how many genes have |t| > threshold in Time0?
    
    t0_valid = [c for c in t0_cols_in_t if c in t_indexed.columns]
    n_t0 = len(t0_valid)
    
    selected_thresh = (0.5, 4.0)  # default
    fdr_details = {}
    
    if n_t0 >= 2:
        t0_t_matrix = t_indexed.loc[common_genes, t0_valid].values.astype(float)
        t0_t_matrix = np.nan_to_num(t0_t_matrix, nan=0.0)
        
        n_genes = len(common_genes)
        
        # For each threshold level, compute false positive rate from Time0
        # The paper's criterion: at the selected threshold, the expected number of
        # false-positive "significant genes" (extrapolated from Time0 to real experiments)
        # should be < 5% of the actual significant genes found
        for ft, tt in THRESHOLD_GRID:
            # In Time0: count genes with |t| > threshold in any Time0 experiment
            # We don't have fitness values for Time0, but we can use just |t|
            # The paper actually uses both fitness and t for Time0,
            # but since Time0 fitness should be ~0 by definition,
            # genes with large |t| in Time0 represent false positives
            t0_sig = np.abs(t0_t_matrix) > tt
            
            # Fraction of gene-experiment pairs that are false positives
            fp_rate_per_exp = t0_sig.sum() / (n_genes * n_t0) if (n_genes * n_t0) > 0 else 0
            
            # Expected false positive genes in real experiments
            # = fp_rate_per_exp * n_conditions * n_genes
            # A gene is a false positive if it appears significant in any experiment
            # P(gene is FP in at least one experiment) ≈ 1 - (1 - fp_rate_per_exp)^n_conditions
            p_any_fp = 1 - (1 - fp_rate_per_exp) ** n_conditions
            expected_fp_genes = p_any_fp * n_genes
            
            # Count actual significant genes at this threshold (combined)
            sig_at_thresh = (np.abs(comb_fit_matrix) > ft) & (np.abs(comb_t_matrix) > tt)
            actual_sig = (sig_at_thresh.sum(axis=1) > 0).sum()
            
            # FDR = expected_fp / actual_sig
            fdr = expected_fp_genes / actual_sig if actual_sig > 0 else 1.0
            
            fdr_details[f"({ft},{tt})"] = {
                'fp_rate_per_exp': round(fp_rate_per_exp, 6),
                'expected_fp_genes': round(expected_fp_genes, 1),
                'actual_sig_genes': int(actual_sig),
                'fdr': round(fdr, 4),
            }
            
            if fdr <= 0.05:
                selected_thresh = (ft, tt)
                break
        else:
            # None of the thresholds achieved FDR <= 0.05, use strictest
            selected_thresh = THRESHOLD_GRID[-1]
    
    # ===== COUNT PHENOTYPES =====
    # Standard threshold (0.5, 4.0) using combined replicates
    sig_std = (np.abs(comb_fit_matrix) > 0.5) & (np.abs(comb_t_matrix) > 4.0)
    has_pheno_std = sig_std.sum(axis=1) > 0
    n_sig_std = int(has_pheno_std.sum())
    
    # FDR-selected threshold using combined replicates
    ft_sel, tt_sel = selected_thresh
    sig_fdr = (np.abs(comb_fit_matrix) > ft_sel) & (np.abs(comb_t_matrix) > tt_sel)
    has_pheno_fdr = sig_fdr.sum(axis=1) > 0
    n_sig_fdr = int(has_pheno_fdr.sum())
    
    # Threshold sensitivity
    thresh_results = {}
    for ft, tt in THRESHOLD_GRID:
        sig_t = (np.abs(comb_fit_matrix) > ft) & (np.abs(comb_t_matrix) > tt)
        n_sig_t = int((sig_t.sum(axis=1) > 0).sum())
        thresh_results[f"({ft},{tt})"] = n_sig_t
    
    # ===== CLASSIFY GENES =====
    gene_desc_map = dict(zip(genes['locusId'], genes['desc']))
    gene_type_map = dict(zip(genes['locusId'], genes['type']))
    gene_ids = common_genes.tolist()
    
    n_protein_with_data = sum(1 for gid in gene_ids if gene_type_map.get(gid, 0) == 1)
    
    poorly_total = 0
    poorly_pheno_std = 0
    poorly_pheno_fdr = 0
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
                poorly_pheno_std += 1
            if has_pheno_fdr[i]:
                poorly_pheno_fdr += 1
        else:
            class_counts["D_hypo"] += 1
            poorly_total += 1
            if has_pheno_std[i]:
                poorly_pheno_std += 1
            if has_pheno_fdr[i]:
                poorly_pheno_fdr += 1
    
    # Specific phenotypes from deposited file
    sp_genes, sp_pairs = load_specific_phenotypes(org)
    
    pct_sig = 100 * n_sig_std / len(common_genes) if len(common_genes) > 0 else 0
    pct_sig_fdr = 100 * n_sig_fdr / len(common_genes) if len(common_genes) > 0 else 0
    
    return {
        'org': org,
        'total_protein': total_protein,
        'n_protein_with_data': n_protein_with_data,
        'n_total_experiments': n_total_quality,
        'n_successful_experiments': n_successful,
        'n_non_t0_experiments': n_non_t0_successful,
        'n_conditions': n_conditions,
        'n_genes_with_data': len(common_genes),
        'n_t0_controls': n_t0,
        # Standard threshold
        'n_sig_std': n_sig_std,
        'pct_sig_std': round(pct_sig, 1),
        'poorly_pheno_std': poorly_pheno_std,
        # FDR-adjusted threshold
        'fdr_threshold': list(selected_thresh),
        'n_sig_fdr': n_sig_fdr,
        'pct_sig_fdr': round(pct_sig_fdr, 1),
        'poorly_pheno_fdr': poorly_pheno_fdr,
        # Classification
        'class_A_or_B': class_counts["A_or_B"],
        'class_C_vague': class_counts["C_vague"],
        'class_D_hypo': class_counts["D_hypo"],
        'poorly_annotated': poorly_total,
        # Specific phenotypes
        'sp_genes': sp_genes,
        'sp_pairs': sp_pairs,
        # Details
        'threshold_sensitivity': thresh_results,
        'fdr_details': fdr_details,
        'n_replicates_dist': dict(pd.Series(list(n_replicates.values())).value_counts().sort_index()),
    }


def main():
    print("=" * 80)
    print("FULL 32-ORGANISM REPLICATION v2 — Price et al. (2018)")
    print("With proper FDR control using Time0 t-statistics")
    print("=" * 80)
    
    results = []
    failed = []
    
    for i, org in enumerate(ALL_ORGANISMS):
        print(f"\n[{i+1}/32] Processing {org}...", end=" ", flush=True)
        r = process_organism(org)
        if r:
            results.append(r)
            ft, tt = r['fdr_threshold']
            thresh_str = f"({ft},{tt})"
            fdr_note = " *STRICT*" if (ft, tt) != (0.5, 4.0) else ""
            print(f"OK — {r['n_conditions']} conds, "
                  f"{r['n_t0_controls']} T0, "
                  f"FDR→{thresh_str}{fdr_note}, "
                  f"sig(std)={r['n_sig_std']}, "
                  f"sig(fdr)={r['n_sig_fdr']}, "
                  f"poor+pheno(fdr)={r['poorly_pheno_fdr']}")
        else:
            failed.append(org)
            print("FAILED")
    
    # ==================== Summary ====================
    print("\n" + "=" * 140)
    print(f"SUMMARY — {len(results)}/32 organisms processed")
    print("=" * 140)
    
    header = (f"{'Organism':<22} {'Prot':>5} {'wData':>6} {'Exps':>5} {'Conds':>5} "
              f"{'T0':>3} {'FDRth':>10} "
              f"{'SigS':>5} {'%S':>5} {'SigF':>5} {'%F':>5} "
              f"{'Poor':>6} {'PPstd':>6} {'PPfdr':>6} "
              f"{'SpGn':>5} {'SpPr':>5}")
    print(header)
    print("-" * 140)
    
    for r in results:
        ft, tt = r['fdr_threshold']
        thresh_str = f"({ft},{tt})"
        print(f"{r['org']:<22} {r['total_protein']:>5} {r['n_protein_with_data']:>6} "
              f"{r['n_non_t0_experiments']:>5} {r['n_conditions']:>5} "
              f"{r['n_t0_controls']:>3} {thresh_str:>10} "
              f"{r['n_sig_std']:>5} {r['pct_sig_std']:>5.1f} "
              f"{r['n_sig_fdr']:>5} {r['pct_sig_fdr']:>5.1f} "
              f"{r['poorly_annotated']:>6} {r['poorly_pheno_std']:>6} "
              f"{r['poorly_pheno_fdr']:>6} "
              f"{r['sp_genes']:>5} {r['sp_pairs']:>5}")
    
    print("-" * 140)
    
    # Totals
    t = lambda key: sum(r[key] for r in results)
    
    print(f"{'TOTAL':.<22} {t('total_protein'):>5} {t('n_protein_with_data'):>6} "
          f"{t('n_non_t0_experiments'):>5} {t('n_conditions'):>5} "
          f"{'':>3} {'':>10} "
          f"{t('n_sig_std'):>5} {'':>5} "
          f"{t('n_sig_fdr'):>5} {'':>5} "
          f"{t('poorly_annotated'):>6} {t('poorly_pheno_std'):>6} "
          f"{t('poorly_pheno_fdr'):>6} "
          f"{t('sp_genes'):>5} {t('sp_pairs'):>5}")
    
    print(f"\n{'='*80}")
    print("HEADLINE COMPARISON")
    print(f"{'='*80}")
    
    print(f"\n{'Metric':<50} {'Paper':>10} {'Ours(std)':>10} {'Ours(FDR)':>10}")
    print("-" * 80)
    print(f"{'Organisms analyzed':<50} {'32':>10} {f'{len(results)}':>10} {f'{len(results)}':>10}")
    print(f"{'Total successful experiments':<50} {'~4,870':>10} {t('n_non_t0_experiments'):>10} {t('n_non_t0_experiments'):>10}")
    print(f"{'Conditions (after replicate combination)':<50} {'—':>10} {t('n_conditions'):>10} {t('n_conditions'):>10}")
    print(f"{'Genes w/ significant phenotype (all)':<50} {'—':>10} {t('n_sig_std'):>10} {t('n_sig_fdr'):>10}")
    print(f"{'Poorly-annotated genes w/ phenotype':<50} {'11,779':>10} {t('poorly_pheno_std'):>10} {t('poorly_pheno_fdr'):>10}")
    print(f"{'Specific phenotype genes (deposited)':<50} {'—':>10} {t('sp_genes'):>10} {t('sp_genes'):>10}")
    print(f"{'Specific phenotype pairs (deposited)':<50} {'—':>10} {t('sp_pairs'):>10} {t('sp_pairs'):>10}")
    
    # Organisms needing stricter thresholds
    strict_orgs = [r['org'] for r in results if tuple(r['fdr_threshold']) != (0.5, 4.0)]
    print(f"\nOrganisms with FDR-adjusted stricter thresholds: {len(strict_orgs)}")
    for org_name in strict_orgs:
        r = next(x for x in results if x['org'] == org_name)
        print(f"  {org_name}: {tuple(r['fdr_threshold'])}")
    
    if failed:
        print(f"\nFAILED organisms: {', '.join(failed)}")
    
    # Save — convert numpy types for JSON
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)
    
    outpath = os.path.join(RESULTS_DIR, "results_all32_v2.json")
    with open(outpath, 'w') as f:
        json.dump({
            'results': results,
            'failed': failed,
            'totals': {
                'n_processed': len(results),
                'n_total': 32,
                'total_protein': t('total_protein'),
                'total_with_data': t('n_protein_with_data'),
                'total_experiments': t('n_non_t0_experiments'),
                'total_conditions': t('n_conditions'),
                'total_sig_std': t('n_sig_std'),
                'total_sig_fdr': t('n_sig_fdr'),
                'total_poorly': t('poorly_annotated'),
                'total_poorly_pheno_std': t('poorly_pheno_std'),
                'total_poorly_pheno_fdr': t('poorly_pheno_fdr'),
                'total_sp_genes': t('sp_genes'),
                'total_sp_pairs': t('sp_pairs'),
            }
        }, f, indent=2, cls=NumpyEncoder)
    print(f"\nResults saved to {outpath}")
    
    return results, failed


if __name__ == "__main__":
    main()
