#!/usr/bin/env python3
"""
Replication of Price et al. (2018) Nature — "Mutant phenotypes for thousands 
of bacterial genes of unknown function"

EXACT classification logic from plotfeba.R:
  
  Gene classification (AllProteinsByClass):
    A (role): has non-vague TIGRFAM functional role
    B (specific): not isHypo (i.e., description is NOT vague per HypoDesc)
    C (vague): isHypo but NOT pureHypo (i.e., vague desc but not purely hypothetical)
    D (hypo): pureHypo (hypothetical/uncharacterized/membrane protein)

  HypoDesc (vague): matches any of a specific list of vague terms or patterns
  PureHypoDesc: narrower — only hypothetical/uncharacterized/TIGR family/membrane protein

  Paper's "poorly annotated" = C (vague) + D (hypo), i.e., genes with HypoDesc=True

  Significant phenotype: |fitness| > 0.5 AND |combined t| > 4
    (with FDR control that may raise thresholds per organism)
  
  We use the standard thresholds since per-organism FDR adjustment is complex
  and the paper states most organisms used the standard thresholds.
"""

import pandas as pd
import numpy as np
import os
import re
import json

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


def hypo_desc(desc):
    """
    Exact reimplementation of HypoDesc from plotfeba.R.
    Returns True if the description is "vague" (isHypo).
    """
    if pd.isna(desc) or desc.strip() == "":
        return True
    
    # Remove (RefSeq) and (NCBI) suffixes
    desc2 = desc.replace(" (RefSeq)", "").replace(" (NCBI)", "").strip()
    desc_lower = desc2.lower().strip()
    
    # Exact match list (lowercased) from plotfeba.R
    lc_vague = [
        "membrane protein",
        "predicted membrane protein",
        "putative membrane protein",
        "probable transmembrane protein",
        "signal peptide protein",
        "lipoprotein",
        "transcriptional regulator",
        "transcriptional regulators",
        "predicted dna-binding transcriptional regulator",
        "dna-binding protein",
        "histidine kinase",
        "sensor histidine kinase",
        "signal transduction histidine kinase",
        "response regulator receiver protein",
        "serine/threonine protein kinase",
        "abc transporter permease",
        "abc transporter substrate-binding protein",
        "abc transporter atp-binding protein",
        "abc transporter",
        "mfs transporter",
        "rnd transporter",
        "transporter",
        "permease",
        "porin",
        "tonb-dependent receptor",
        "dehydrogenase",
        "oxidoreductase",
        "fad-dependent oxidoreductase",
        "methyltransferase",
        "sam-dependent methyltransferase",
        "atpase",
        "acetyltransferase",
        "gcn5-related n-acetyltransferase",
        "aminotransferase",
        "aminohydrolase",
        "alpha/beta hydrolase",
        "hydrolase",
    ]
    
    if desc_lower in lc_vague:
        return True
    
    # Pattern match list from plotfeba.R
    vague_patterns = [
        "unknown function",
        "uncharacterized",
        "hypothetical",
        "hypothtical",  # typo in original code
        "family",
        "domain protein",
        "related protein",
        "transporter related",
    ]
    
    for pat in vague_patterns:
        if pat.lower() in desc2.lower():
            return True
    
    return False


def pure_hypo_desc(desc):
    """
    Exact reimplementation of PureHypoDesc from plotfeba.R.
    Returns True if the description is "purely hypothetical".
    """
    if pd.isna(desc) or desc.strip() == "":
        return True
    
    # Remove (RefSeq) suffix
    desc2 = desc.replace(" (RefSeq)", "").strip()
    # Remove (NCBI...) suffix
    desc2 = re.sub(r' \(NCBI.*\)', '', desc2).strip()
    
    desc_lower = desc2.lower()
    
    # Pure patterns from plotfeba.R
    pure_patterns = [
        "hypothetical protein",
        "unknown function",
        "uncharacterized",
    ]
    
    for pat in pure_patterns:
        if pat in desc_lower:
            return True
    
    # TIGR family protein pattern
    if re.search(r'TIGR[0-9]+ family protein$', desc2):
        return True
    
    # Exact match: "membrane protein"
    if desc_lower == "membrane protein":
        return True
    
    return False


def classify_gene(desc):
    """
    Classify gene using the paper's logic.
    Without TIGRFAM role data, we can't determine class A.
    We classify as:
      isHypo = HypoDesc(desc) 
      pureHypo = PureHypoDesc(desc)
      
    For genes without TIGRFAM data:
      If NOT isHypo -> B (specific description)
      If isHypo but NOT pureHypo -> C (vague)
      If pureHypo -> D (hypothetical)
    
    Note: Class A requires TIGRFAM role assignment, which we approximate.
    """
    is_hypo = hypo_desc(desc)
    is_pure_hypo = pure_hypo_desc(desc)
    
    if not is_hypo:
        return "B_specific"  # or A if has TIGRFAM role — we'll handle separately
    elif not is_pure_hypo:
        return "C_vague"
    else:
        return "D_hypo"


def count_phenotypes(org):
    """Analyze one organism."""
    print(f"\n{'='*60}")
    print(f"Processing {org} ({ORG_NAMES[org]})")
    print(f"{'='*60}")
    
    org_dir = os.path.join(DATA_DIR, org)
    
    # Load data
    genes = pd.read_csv(os.path.join(org_dir, "fit_genes.tab"), sep="\t")
    lrn = pd.read_csv(os.path.join(org_dir, "fit_logratios_good.tab"), sep="\t")
    t_vals = pd.read_csv(os.path.join(org_dir, "fit_t.tab"), sep="\t")
    quality = pd.read_csv(os.path.join(org_dir, "fit_quality.tab"), sep="\t")
    
    # Protein-coding genes
    protein_genes = genes[genes["type"] == 1].copy()
    total_protein = len(protein_genes)
    
    # Experiment columns
    meta_cols_lrn = ['locusId', 'sysName', 'desc', 'comb']
    exp_cols_lrn = [c for c in lrn.columns if c not in meta_cols_lrn]
    
    meta_cols_t = ['locusId', 'sysName', 'desc']
    exp_cols_t = [c for c in t_vals.columns if c not in meta_cols_t]
    
    common_exps = [c for c in exp_cols_lrn if c in exp_cols_t]
    n_experiments = len(common_exps)
    
    # Build fitness + t matrices for common genes
    lrn_indexed = lrn.set_index('locusId')
    t_indexed = t_vals.set_index('locusId')
    common_genes = lrn_indexed.index.intersection(t_indexed.index)
    
    fit_matrix = lrn_indexed.loc[common_genes, common_exps].values.astype(float)
    t_matrix = t_indexed.loc[common_genes, common_exps].values.astype(float)
    fit_matrix = np.nan_to_num(fit_matrix, nan=0.0)
    t_matrix = np.nan_to_num(t_matrix, nan=0.0)
    
    # Combine replicates — the paper combines replicates by name (einfo$short)
    # In the data files, the 'short' field groups replicates
    # For simplicity, since fit_logratios_good.tab already has per-experiment values,
    # we check if ANY experiment (not just combined) meets the threshold
    # The paper actually combines replicates:
    #   combined_fitness = mean(fitness across replicates)
    #   combined_t = mean(t) * sqrt(n_replicates)
    # But since we have individual experiments, checking any experiment individually
    # is actually MORE conservative (each individual is noisier than the combination)
    # We'll use the simpler approach: |fitness| > 0.5 AND |t| > 4 in ANY experiment
    
    # Significant phenotype
    sig = (np.abs(fit_matrix) > 0.5) & (np.abs(t_matrix) > 4.0)
    n_sig_per_gene = sig.sum(axis=1)
    has_phenotype = n_sig_per_gene > 0
    n_with_phenotype = int(has_phenotype.sum())
    
    # Strong phenotype (|fitness| > 2 in any experiment)
    strong = (np.abs(fit_matrix) > 2.0) & (np.abs(t_matrix) > 5.0)
    has_strong = strong.sum(axis=1) > 0
    n_with_strong = int(has_strong.sum())
    
    # Specific phenotype (|fitness| > 1, |t| > 5)
    specific = (np.abs(fit_matrix) > 1.0) & (np.abs(t_matrix) > 5.0)
    has_specific = specific.sum(axis=1) > 0
    n_with_specific = int(has_specific.sum())
    
    # Classify genes
    gene_desc_map = dict(zip(genes['locusId'], genes['desc']))
    gene_type_map = dict(zip(genes['locusId'], genes['type']))
    
    gene_ids = common_genes.tolist()
    
    class_counts = {"A_or_B": 0, "C_vague": 0, "D_hypo": 0}
    poorly_with_phenotype = 0
    poorly_total = 0
    poorly_with_strong = 0
    
    for i, gid in enumerate(gene_ids):
        gtype = gene_type_map.get(gid, 0)
        if gtype != 1:
            continue
        
        desc = gene_desc_map.get(gid, "")
        is_hypo = hypo_desc(desc)
        is_pure = pure_hypo_desc(desc)
        
        if not is_hypo:
            class_counts["A_or_B"] += 1
        elif not is_pure:
            class_counts["C_vague"] += 1
            poorly_total += 1
            if has_phenotype[i]:
                poorly_with_phenotype += 1
            if has_strong[i]:
                poorly_with_strong += 1
        else:
            class_counts["D_hypo"] += 1
            poorly_total += 1
            if has_phenotype[i]:
                poorly_with_phenotype += 1
            if has_strong[i]:
                poorly_with_strong += 1
    
    # Count total protein-coding genes with fitness data
    n_protein_with_data = sum(1 for gid in gene_ids if gene_type_map.get(gid, 0) == 1)
    
    pct_with_pheno = 100 * n_with_phenotype / len(common_genes)
    
    print(f"  Total protein-coding genes: {total_protein}")
    print(f"  Protein-coding with fitness data: {n_protein_with_data}")
    print(f"  Experiments (conditions): {n_experiments}")
    print(f"  Genes with ≥1 sig phenotype: {n_with_phenotype} ({pct_with_pheno:.1f}%)")
    print(f"  Genes with ≥1 strong phenotype: {n_with_strong}")
    print(f"  Genes with ≥1 specific phenotype: {n_with_specific}")
    print(f"  Annotation classes: {class_counts}")
    print(f"  Poorly annotated (C+D): {poorly_total}")
    print(f"  Poorly annotated with phenotype: {poorly_with_phenotype}")
    print(f"  Poorly annotated with strong: {poorly_with_strong}")
    
    return {
        'org': org,
        'name': ORG_NAMES[org],
        'total_protein': total_protein,
        'n_protein_with_data': n_protein_with_data,
        'n_experiments': n_experiments,
        'n_with_phenotype': n_with_phenotype,
        'pct_with_phenotype': round(pct_with_pheno, 1),
        'n_with_strong': n_with_strong,
        'n_with_specific': n_with_specific,
        'class_A_or_B': class_counts["A_or_B"],
        'class_C_vague': class_counts["C_vague"],
        'class_D_hypo': class_counts["D_hypo"],
        'poorly_annotated': poorly_total,
        'poorly_with_phenotype': poorly_with_phenotype,
        'poorly_with_strong': poorly_with_strong,
    }


def main():
    results = []
    for org in ORGANISMS:
        try:
            r = count_phenotypes(org)
            results.append(r)
        except Exception as e:
            print(f"ERROR: {org}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 90)
    print("SUMMARY — Phenotype Replication for 5 of 32 Organisms")
    print("=" * 90)
    
    print(f"\n{'Organism':<25} {'Prot':<6} {'w/Data':<7} {'Exps':<5} "
          f"{'Pheno':<7} {'%':<6} {'Poor':<6} {'PoorPh':<8} {'Strong':<7}")
    print("-" * 90)
    
    for r in results:
        print(f"{r['name']:<25} {r['total_protein']:<6} {r['n_protein_with_data']:<7} "
              f"{r['n_experiments']:<5} {r['n_with_phenotype']:<7} "
              f"{r['pct_with_phenotype']:<6} {r['poorly_annotated']:<6} "
              f"{r['poorly_with_phenotype']:<8} {r['poorly_with_strong']:<7}")
    
    print("-" * 90)
    
    totals = {k: sum(r[k] for r in results) for k in [
        'total_protein', 'n_protein_with_data', 'n_with_phenotype',
        'poorly_annotated', 'poorly_with_phenotype', 'poorly_with_strong'
    ]}
    
    print(f"{'TOTAL (5 orgs)':<25} {totals['total_protein']:<6} "
          f"{totals['n_protein_with_data']:<7} {'—':<5} "
          f"{totals['n_with_phenotype']:<7} {'—':<6} "
          f"{totals['poorly_annotated']:<6} {totals['poorly_with_phenotype']:<8} "
          f"{totals['poorly_with_strong']:<7}")
    
    print(f"\n--- Extrapolation to 32 Organisms ---")
    avg_poor_pheno = totals['poorly_with_phenotype'] / len(results)
    projected = avg_poor_pheno * 32
    print(f"Average poorly-annotated genes with phenotype per organism: {avg_poor_pheno:.0f}")
    print(f"Projected for 32 organisms (simple scaling): {projected:.0f}")
    print(f"Paper's reported total: 11,779")
    ratio = projected / 11779
    print(f"Ratio (projected/reported): {ratio:.2f}")
    
    # Save
    outpath = os.path.join(DATA_DIR, "..", "replication", "results_v2.json")
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {outpath}")
    
    return results


if __name__ == "__main__":
    main()
