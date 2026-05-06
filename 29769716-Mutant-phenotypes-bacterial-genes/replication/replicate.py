#!/usr/bin/env python3
"""
Replication of Price et al. (2018) Nature — "Mutant phenotypes for thousands 
of bacterial genes of unknown function"

Core claim: 11,779 protein-coding genes of unknown function have mutant 
phenotypes across 32 bacteria.

We replicate the analysis for 5 of the 32 organisms:
  - Keio (E. coli BW25113)
  - MR1 (S. oneidensis MR-1)
  - psRCH2 (P. stutzeri RCH2)
  - Smeli (S. meliloti 1021)
  - Caulo (C. crescentus NA1000)

Criteria from paper:
  Significant phenotype: |fitness| > 0.5 AND |t| > 4
  (Some organisms may use stricter thresholds for FDR < 5%)
"""

import pandas as pd
import numpy as np
import os
import re
import json
from collections import defaultdict

DATA_DIR = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/29769716-Mutant-phenotypes-bacterial-genes/data"
)

ORGANISMS = ["Keio", "MR1", "psRCH2", "Smeli", "Caulo"]

ORG_NAMES = {
    "Keio": "E. coli BW25113",
    "MR1": "S. oneidensis MR-1",
    "psRCH2": "P. stutzeri RCH2",
    "Smeli": "S. meliloti 1021",
    "Caulo": "C. crescentus NA1000",
}

# Standard threshold from paper
FITNESS_THRESH = 0.5
T_THRESH = 4.0

# Specific phenotype thresholds
SPEC_FITNESS_THRESH = 1.0
SPEC_T_THRESH = 5.0


def classify_gene_function(desc):
    """
    Classify gene annotation quality based on description.
    Returns one of:
      'A_known' - has specific known function (enzyme name, pathway, etc.)
      'B_specific_domain' - has specific domain but not fully characterized
      'C_vague' - vague annotation (transporter, membrane protein, etc.)
      'D_hypothetical' - hypothetical, unknown, uncharacterized
    
    The paper's 11,779 count includes genes NOT annotated with a 
    "detailed function" — roughly C + D categories.
    """
    if pd.isna(desc) or desc.strip() == "":
        return "D_hypothetical"
    
    desc_lower = desc.lower().strip()
    
    # D: Hypothetical / unknown / uncharacterized
    hypo_patterns = [
        r'^hypothetical protein',
        r'^conserved hypothetical',
        r'^predicted protein',
        r'^uncharacterized protein',
        r'^protein of unknown function',
        r'^unknown function',
        r'^orf\b',
        r'^unknown$',
        r'^putative uncharacterized',
    ]
    for pat in hypo_patterns:
        if re.search(pat, desc_lower):
            return "D_hypothetical"
    
    # Also catch DUF/UPF family proteins (uncharacterized families)
    if re.search(r'\bDUF\d+\b', desc) or re.search(r'\bUPF\d+\b', desc):
        return "D_hypothetical"
    
    # C: Vague annotations — general category without specific function
    vague_patterns = [
        r'^(putative |probable )?(membrane protein|inner membrane protein|outer membrane protein)$',
        r'^(putative |probable )?transporter$',
        r'^(putative |probable )?transcriptional regulator$',
        r'^(putative |probable )?oxidoreductase$',
        r'^(putative |probable )?hydrolase$',
        r'^(putative |probable )?transferase$',
        r'^(putative |probable )?lipoprotein$',
        r'^(putative |probable )?exported protein$',
        r'^(putative |probable )?signal peptide protein$',
        r'^(putative |probable )?secreted protein$',
        r'^(putative |probable )?fimbrial protein$',
        r'^(putative |probable )?periplasmic protein$',
        r'^(putative |probable )?cytoplasmic protein$',
    ]
    for pat in vague_patterns:
        if re.search(pat, desc_lower):
            return "C_vague"
    
    # Also vague: short descriptions that are just domain names or general terms
    vague_keywords = [
        'domain protein', 'domain-containing protein', 'family protein',
        'repeat protein', 'motif protein'
    ]
    # Only classify as vague if description is ONLY a domain reference
    if any(desc_lower.endswith(kw) for kw in vague_keywords):
        # Check if there's an EC number or specific function word
        if not re.search(r'EC \d+\.\d+', desc) and not re.search(
            r'(synthase|kinase|dehydrogenase|reductase|ligase|lyase|isomerase|'
            r'protease|peptidase|nuclease|helicase|polymerase|carboxylase|'
            r'decarboxylase|aminotransferase|phosphatase|esterase|'
            r'permease|symporter|antiporter)', desc_lower
        ):
            return "C_vague"
    
    # A: Known function — has EC number, specific enzyme/pathway name
    if re.search(r'EC \d+\.\d+', desc):
        return "A_known"
    
    known_function_words = [
        'synthase', 'kinase', 'dehydrogenase', 'reductase', 'ligase',
        'lyase', 'isomerase', 'protease', 'peptidase', 'nuclease',
        'helicase', 'polymerase', 'carboxylase', 'decarboxylase',
        'aminotransferase', 'phosphatase', 'mutase', 'epimerase',
        'recombinase', 'topoisomerase', 'gyrase', 'primase',
        'ribosomal protein', 'trna', 'rrna', 'sigma factor',
        'rna polymerase', 'dna polymerase', 'dna repair',
        'cell division', 'flagell', 'chemotaxis', 'pilus',
        'type ii secretion', 'type iii secretion', 'type iv secretion',
        'two-component', 'histidine kinase', 'response regulator',
        'abc transporter', 'pts system', 'phosphotransferase',
        'cytochrome', 'ferredoxin', 'thioredoxin',
        'chaperone', 'protease', 'peptidoglycan',
        'lipopolysaccharide', 'capsul',
    ]
    
    for word in known_function_words:
        if word in desc_lower:
            return "A_known"
    
    # B: Specific domain but not fully known — has putative/probable + specific term
    if re.search(r'(putative|probable|predicted|possible)', desc_lower):
        return "B_specific_domain"
    
    # Default: if it has a reasonable description, classify as known
    # Short descriptions (<15 chars) are often vague
    if len(desc_lower) < 15:
        return "C_vague"
    
    return "A_known"


def is_poorly_annotated(gene_class):
    """Paper's poorly-annotated = not annotated with detailed function"""
    return gene_class in ("C_vague", "D_hypothetical")


def load_organism_data(org):
    """Load fitness data for one organism."""
    org_dir = os.path.join(DATA_DIR, org)
    
    # Load genes
    genes = pd.read_csv(os.path.join(org_dir, "fit_genes.tab"), sep="\t")
    
    # Load fitness values (logratios for good experiments)
    lrn = pd.read_csv(os.path.join(org_dir, "fit_logratios_good.tab"), sep="\t")
    
    # Load t-values
    t_vals = pd.read_csv(os.path.join(org_dir, "fit_t.tab"), sep="\t")
    
    # Load quality
    quality = pd.read_csv(os.path.join(org_dir, "fit_quality.tab"), sep="\t")
    
    return genes, lrn, t_vals, quality


def count_phenotypes(org):
    """
    For one organism, count:
    - Total protein-coding genes
    - Genes with fitness data (used=TRUE)
    - Genes with at least one significant phenotype
    - Of those, how many are "poorly annotated"
    - Number of successful experiments
    """
    print(f"\n{'='*60}")
    print(f"Processing {org} ({ORG_NAMES[org]})")
    print(f"{'='*60}")
    
    genes, lrn, t_vals, quality = load_organism_data(org)
    
    # Filter to protein-coding genes (type=1)
    protein_genes = genes[genes["type"] == 1].copy()
    total_protein = len(protein_genes)
    print(f"Total protein-coding genes: {total_protein}")
    
    # Genes with fitness data
    used_genes = protein_genes[protein_genes["used"] == True]
    n_used = len(used_genes)
    print(f"Genes with fitness data (used=TRUE): {n_used}")
    
    # Count successful experiments
    # In quality table, u=TRUE means successful
    if 'u' in quality.columns:
        n_success = quality['u'].sum()
        n_total_exp = len(quality[quality['short'] != 'Time0']) if 'short' in quality.columns else len(quality)
    else:
        n_success = 'N/A'
        n_total_exp = 'N/A'
    print(f"Successful experiments: {n_success}")
    
    # The fitness data (lrn) has columns: locusId, sysName, desc, comb, then experiment columns
    # The t-value data (t_vals) has columns: locusId, sysName, desc, then experiment columns (including Time0)
    
    # Get experiment columns from lrn (skip metadata columns)
    meta_cols_lrn = ['locusId', 'sysName', 'desc', 'comb']
    exp_cols_lrn = [c for c in lrn.columns if c not in meta_cols_lrn]
    
    # Get experiment columns from t_vals that match lrn experiments
    meta_cols_t = ['locusId', 'sysName', 'desc']
    exp_cols_t = [c for c in t_vals.columns if c not in meta_cols_t]
    
    # Match experiments between lrn and t_vals
    common_exps = [c for c in exp_cols_lrn if c in exp_cols_t]
    print(f"Experiment columns (fitness): {len(exp_cols_lrn)}")
    print(f"Experiment columns (t-values): {len(exp_cols_t)}")
    print(f"Matched experiments: {len(common_exps)}")
    
    # For each gene, check if |fitness| > 0.5 AND |t| > 4 in any experiment
    # Merge on locusId
    lrn_indexed = lrn.set_index('locusId')
    t_indexed = t_vals.set_index('locusId')
    
    # Get common genes
    common_genes = lrn_indexed.index.intersection(t_indexed.index)
    print(f"Genes in both fitness and t-value tables: {len(common_genes)}")
    
    # Extract numeric matrices
    fit_matrix = lrn_indexed.loc[common_genes, common_exps].values.astype(float)
    t_matrix = t_indexed.loc[common_genes, common_exps].values.astype(float)
    
    # Replace NaN with 0
    fit_matrix = np.nan_to_num(fit_matrix, nan=0.0)
    t_matrix = np.nan_to_num(t_matrix, nan=0.0)
    
    # Apply threshold: |fitness| > 0.5 AND |t| > 4
    sig = (np.abs(fit_matrix) > FITNESS_THRESH) & (np.abs(t_matrix) > T_THRESH)
    
    # For each gene, count number of conditions with significant phenotype
    n_sig_per_gene = sig.sum(axis=1)
    
    # Genes with at least one significant phenotype
    has_phenotype = n_sig_per_gene > 0
    n_with_phenotype = has_phenotype.sum()
    
    pct_with_phenotype = 100 * n_with_phenotype / len(common_genes)
    print(f"Genes with ≥1 significant phenotype: {n_with_phenotype} ({pct_with_phenotype:.1f}%)")
    
    # Also apply stricter threshold for specific phenotype: |fitness| > 1 AND |t| > 5
    sig_specific = (np.abs(fit_matrix) > SPEC_FITNESS_THRESH) & (np.abs(t_matrix) > SPEC_T_THRESH)
    has_specific = sig_specific.sum(axis=1) > 0
    n_with_specific = has_specific.sum()
    print(f"Genes with ≥1 specific phenotype (|f|>1,|t|>5): {n_with_specific}")
    
    # Classify genes by annotation quality
    gene_desc_map = dict(zip(genes['locusId'], genes['desc']))
    gene_type_map = dict(zip(genes['locusId'], genes['type']))
    
    gene_ids = common_genes.tolist()
    
    class_counts = defaultdict(int)
    poorly_annotated_with_phenotype = 0
    poorly_annotated_total = 0
    
    results_per_gene = []
    
    for i, gid in enumerate(gene_ids):
        gtype = gene_type_map.get(gid, 0)
        if gtype != 1:  # only protein-coding
            continue
        
        desc = gene_desc_map.get(gid, "")
        gclass = classify_gene_function(desc)
        class_counts[gclass] += 1
        
        is_poor = is_poorly_annotated(gclass)
        if is_poor:
            poorly_annotated_total += 1
        
        if has_phenotype[i]:
            if is_poor:
                poorly_annotated_with_phenotype += 1
            results_per_gene.append({
                'locusId': gid,
                'desc': desc,
                'class': gclass,
                'poorly_annotated': is_poor,
                'n_sig_conditions': int(n_sig_per_gene[i]),
                'has_specific': bool(has_specific[i]),
            })
    
    print(f"\nAnnotation classification (protein-coding genes with fitness data):")
    for cls in sorted(class_counts.keys()):
        print(f"  {cls}: {class_counts[cls]}")
    
    print(f"\nPoorly annotated genes (C+D): {poorly_annotated_total}")
    print(f"Poorly annotated with ≥1 phenotype: {poorly_annotated_with_phenotype}")
    
    return {
        'org': org,
        'name': ORG_NAMES[org],
        'total_protein': total_protein,
        'n_used': n_used,
        'n_fitness_genes': len(common_genes),
        'n_experiments': len(common_exps),
        'n_with_phenotype': int(n_with_phenotype),
        'pct_with_phenotype': round(pct_with_phenotype, 1),
        'n_with_specific': int(n_with_specific),
        'class_counts': dict(class_counts),
        'poorly_annotated_total': poorly_annotated_total,
        'poorly_annotated_with_phenotype': poorly_annotated_with_phenotype,
    }


def main():
    all_results = []
    
    for org in ORGANISMS:
        try:
            result = count_phenotypes(org)
            all_results.append(result)
        except Exception as e:
            print(f"ERROR processing {org}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    total_poorly_with_phenotype = sum(r['poorly_annotated_with_phenotype'] for r in all_results)
    total_poorly_annotated = sum(r['poorly_annotated_total'] for r in all_results)
    total_with_phenotype = sum(r['n_with_phenotype'] for r in all_results)
    total_fitness_genes = sum(r['n_fitness_genes'] for r in all_results)
    
    print(f"\n{'Organism':<25} {'Genes':<8} {'w/Fit':<8} {'Exps':<6} "
          f"{'Pheno':<8} {'%Pheno':<8} {'Poor':<8} {'PoorPheno':<10}")
    print("-" * 100)
    
    for r in all_results:
        print(f"{r['name']:<25} {r['total_protein']:<8} {r['n_fitness_genes']:<8} "
              f"{r['n_experiments']:<6} {r['n_with_phenotype']:<8} "
              f"{r['pct_with_phenotype']:<8} {r['poorly_annotated_total']:<8} "
              f"{r['poorly_annotated_with_phenotype']:<10}")
    
    print("-" * 100)
    print(f"{'TOTAL (5 orgs)':<25} {'':<8} {total_fitness_genes:<8} "
          f"{'':<6} {total_with_phenotype:<8} {'':<8} "
          f"{total_poorly_annotated:<8} {total_poorly_with_phenotype:<10}")
    
    # Scale-up estimate
    # Paper covers 32 organisms; we did 5
    # Simple extrapolation for comparison
    print(f"\n--- Scale-up Estimate ---")
    print(f"Our 5 organisms: {total_poorly_with_phenotype} poorly-annotated genes with phenotypes")
    print(f"Paper's 32 organisms: 11,779 poorly-annotated genes with phenotypes")
    avg_per_org = total_poorly_with_phenotype / len(all_results)
    print(f"Our average per organism: {avg_per_org:.0f}")
    print(f"Projected for 32 organisms: {avg_per_org * 32:.0f}")
    print(f"Paper reported: 11,779")
    
    # Save results
    output_path = os.path.join(DATA_DIR, "..", "replication", "results.json")
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")
    
    return all_results


if __name__ == "__main__":
    results = main()
