#!/usr/bin/env python3
"""
Audit: check if known AMR genes from the paper's S4 Dataset appear in our
top 50 features. Paper uses 1-indexed cluster IDs; our pipeline uses 0-indexed.
"""

import json
import re
import openpyxl

BASE_DIR = '/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-12-ML-AMR-pangenomes-Hyun2020'

# Load our results
with open(f'{BASE_DIR}/results/S_aureus_results.json') as f:
    our_results = json.load(f)

# Load paper's S4 annotations
wb = openpyxl.load_workbook(f'{BASE_DIR}/data/S4_Dataset_annotations.xlsx', read_only=True)

# Map paper sheet names to our antibiotic names
sheet_to_abx = {
    'SA_CIP': 'ciprofloxacin',
    'SA_CLI': 'clindamycin',
    'SA_ERY': 'erythromycin',
    'SA_GEN': 'gentamicin',
    'SA_SXT': 'trimethoprim/sulfamethoxazole',
    'SA_TET': 'tetracycline',
}


def paper_cluster_to_ours(paper_id):
    """Convert paper cluster ID (1-indexed) to our naming (0-indexed).
    Paper: Cluster_92_Allele_18 -> core91_allele18
    Paper: Cluster_624 (accessory) -> acc623
    """
    # Parse paper format: Cluster_N or Cluster_N_Allele_M
    m = re.match(r'Cluster_(\d+)(?:_Allele_(\d+))?', paper_id)
    if not m:
        return None
    
    cid = int(m.group(1)) - 1  # Convert to 0-indexed
    allele = m.group(2)
    
    if allele is not None:
        return f"core{cid}_allele{allele}"
    else:
        # Could be accessory or core (if allele not specified, paper lists the cluster)
        return cid  # Return the cluster number to match against both core and acc


print("=" * 100)
print("AMR GENE AUDIT: S. aureus — Known AMR genes in our top 50 features")
print("=" * 100)

total_found = 0
total_expected = 0

for sheet_name, abx in sheet_to_abx.items():
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    
    # Get paper's known AMR genes
    paper_known = []
    for r in rows:
        if r and r[7] and 'Known AMR' in str(r[7]):
            paper_known.append({
                'paper_id': str(r[0]),
                'paper_rank': int(r[1]),
                'gene': r[5] or '',
                'annotation': r[6] or '',
                'comment': r[7]
            })
    
    # Get our top 50
    if abx not in our_results['antibiotics']:
        print(f"\n{sheet_name} ({abx}): NOT RUN")
        continue
    
    our_top50 = our_results['antibiotics'][abx]['top_50']
    our_feature_names = [f['feature'] for f in our_top50]
    
    print(f"\n{'─'*80}")
    print(f"{sheet_name} ({abx})")
    print(f"Paper: {len(paper_known)} known AMR genes in top 50")
    print(f"{'─'*80}")
    
    found = 0
    for pk in paper_known:
        paper_id = pk['paper_id']
        converted = paper_cluster_to_ours(paper_id)
        
        # Search in our top 50
        our_rank = None
        matched_feature = None
        
        if isinstance(converted, str):
            # Allele-specific match
            for i, fname in enumerate(our_feature_names):
                if fname == converted:
                    our_rank = i + 1
                    matched_feature = fname
                    break
        elif isinstance(converted, int):
            # Cluster number match (could be core or acc)
            target_core = f"core{converted}_"
            target_acc = f"acc{converted}"
            for i, fname in enumerate(our_feature_names):
                if fname.startswith(target_core) or fname == target_acc:
                    our_rank = i + 1
                    matched_feature = fname
                    break
        
        status = "✅ FOUND" if our_rank else "❌ NOT IN TOP 50"
        if our_rank:
            found += 1
        
        print(f"  Paper: {paper_id} (rank {pk['paper_rank']}) = {pk['gene']} | "
              f"{pk['annotation'][:60]}")
        print(f"    Ours: {matched_feature or '---'} "
              f"{'(rank ' + str(our_rank) + ')' if our_rank else ''} "
              f"→ {status}")
    
    total_found += found
    total_expected += len(paper_known)
    print(f"\n  Summary: Found {found}/{len(paper_known)} known AMR genes in our top 50")

print(f"\n{'='*80}")
print(f"OVERALL: Found {total_found}/{total_expected} known AMR genes in our top 50 features")
print(f"Paper claims: known AMR genes in top 50 in 15/16 cases")
print(f"{'='*80}")
