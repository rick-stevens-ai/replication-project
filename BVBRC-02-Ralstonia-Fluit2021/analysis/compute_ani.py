#!/usr/bin/env python3
"""Compute ANIb from existing BLAST output files."""
import os
import glob
import pandas as pd
import numpy as np

ANI_DIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021/analysis/ani")
BLAST_DIR = os.path.join(ANI_DIR, "blastn_output")

GROUPS = {
    "551634": "E2", "551636": "E2", "543514": "E2", "551632": "E2", "551637": "E2",
    "543504": "E1", "551631": "E1", "551635": "E1",
    "535633": "D2", "535634": "D2", "535635": "D2", "545260": "D2",
    "545261": "D2", "535632": "D2", "535638": "D1", "543498": "D1",
    "551633": "G", "535637": "F"
}

SPECIES = {
    "551634": "R. pickettii", "551636": "R. pickettii", "543514": "R. pickettii",
    "551632": "R. pickettii", "551637": "R. pickettii", "543504": "R. pickettii",
    "551631": "R. pickettii", "551635": "R. pickettii",
    "535633": "R. mannitolilytica", "535634": "R. mannitolilytica",
    "535635": "R. mannitolilytica", "545260": "R. mannitolilytica",
    "545261": "R. mannitolilytica", "535632": "R. mannitolilytica",
    "535638": "R. mannitolilytica", "543498": "R. mannitolilytica",
    "551633": "R. insidiosa", "535637": "R. new spp."
}

def parse_blast_for_ani(blast_file):
    """Parse a BLAST output file and calculate ANI for the comparison."""
    if not os.path.exists(blast_file) or os.path.getsize(blast_file) == 0:
        return None, 0, 0
    
    total_identity = 0
    total_aligned = 0
    n_fragments = 0
    
    with open(blast_file) as f:
        # Track best hit per query fragment
        best_hits = {}
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 12:
                continue
            qseqid = parts[0]
            pident = float(parts[2])
            length = int(parts[3])
            
            # Only count alignments >= 30% of fragment (1020bp -> 306bp min)
            if length >= 306:
                if qseqid not in best_hits or pident > best_hits[qseqid][0]:
                    best_hits[qseqid] = (pident, length)
    
    for qid, (pid, alen) in best_hits.items():
        if pid >= 30:  # Minimum identity filter for ANIb
            total_identity += pid * alen
            total_aligned += alen
            n_fragments += 1
    
    if total_aligned > 0:
        ani = total_identity / total_aligned / 100
    else:
        ani = 0
    
    return ani, n_fragments, total_aligned

# Get strain list
strains = sorted(GROUPS.keys())

# Parse all BLAST results
print("Parsing BLAST results...")
ani_matrix = pd.DataFrame(index=strains, columns=strains, dtype=float)

for s1 in strains:
    for s2 in strains:
        if s1 == s2:
            ani_matrix.loc[s1, s2] = 1.0
            continue
        
        # Look for the BLAST output file
        blast_file = os.path.join(BLAST_DIR, f"{s1}_vs_{s2}.blast_tab")
        if not os.path.exists(blast_file):
            # Try alternative naming
            for bf in glob.glob(os.path.join(BLAST_DIR, f"*{s1}*vs*{s2}*")):
                blast_file = bf
                break
        
        ani, n_frags, aligned = parse_blast_for_ani(blast_file)
        if ani is not None:
            ani_matrix.loc[s1, s2] = ani

print("\n=== ANIb Matrix (pairwise) ===")
print(ani_matrix.to_string(float_format=lambda x: f"{x:.4f}" if pd.notna(x) else "N/A"))

# Within-group analysis
print("\n=== Within-group ANI ===")
for group in sorted(set(GROUPS.values())):
    group_strains = [s for s, g in GROUPS.items() if g == group]
    if len(group_strains) < 2:
        print(f"  Group {group}: only 1 strain ({group_strains[0]}, {SPECIES[group_strains[0]]})")
        continue
    anis = []
    for i, s1 in enumerate(group_strains):
        for s2 in group_strains[i+1:]:
            v = ani_matrix.loc[s1, s2]
            if pd.notna(v):
                anis.append(v)
    if anis:
        print(f"  Group {group} ({SPECIES[group_strains[0]]}): min={min(anis):.4f} max={max(anis):.4f} mean={np.mean(anis):.4f} (n={len(anis)} pairs)")
    else:
        print(f"  Group {group}: no valid ANI values")

# Between-group analysis
print("\n=== Between-group ANI ===")
groups_list = sorted(set(GROUPS.values()))
for i, g1 in enumerate(groups_list):
    for g2 in groups_list[i+1:]:
        s1_list = [s for s, g in GROUPS.items() if g == g1]
        s2_list = [s for s, g in GROUPS.items() if g == g2]
        anis = []
        for s1 in s1_list:
            for s2 in s2_list:
                v = ani_matrix.loc[s1, s2]
                if pd.notna(v):
                    anis.append(v)
        if anis:
            above95 = sum(1 for a in anis if a >= 0.95)
            print(f"  {g1} vs {g2}: min={min(anis):.4f} max={max(anis):.4f} mean={np.mean(anis):.4f} (≥0.95: {above95}/{len(anis)})")

# Save
ani_matrix.to_csv(os.path.join(ANI_DIR, "ANIb_matrix.tsv"), sep='\t')
print(f"\nSaved ANIb matrix to {os.path.join(ANI_DIR, 'ANIb_matrix.tsv')}")

# Clustering validation
print("\n=== Clustering Validation (0.95 cutoff) ===")
issues = 0
for i, s1 in enumerate(strains):
    for s2 in strains[i+1:]:
        v = ani_matrix.loc[s1, s2]
        if pd.isna(v):
            continue
        same = GROUPS[s1] == GROUPS[s2]
        if same and v < 0.95:
            print(f"  ISSUE: {s1} & {s2} same group ({GROUPS[s1]}) but ANI={v:.4f}")
            issues += 1
        elif not same and v >= 0.95:
            # Check if within same species-level group (D1/D2 or E1/E2)
            g1_base = GROUPS[s1].rstrip('12')
            g2_base = GROUPS[s2].rstrip('12')
            if g1_base == g2_base:
                pass  # D1 vs D2 or E1 vs E2 may be ≥0.95
            else:
                print(f"  ISSUE: {s1} & {s2} different groups ({GROUPS[s1]} vs {GROUPS[s2]}) but ANI={v:.4f}")
                issues += 1

if issues == 0:
    print("  No clustering issues found - grouping VERIFIED")
else:
    print(f"  {issues} clustering issues found")
