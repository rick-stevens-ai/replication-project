#!/usr/bin/env python3
"""Compute ANIb from pyani BLAST output files with correct format parsing."""
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
    """Parse pyani BLAST output. 
    Pyani format columns (custom -outfmt):
    0: qseqid, 1: sseqid, 2: align_len, 3: mismatches, 4: pident,
    5: nident, 6: qlen, 7: slen, 8: qstart, 9: qend, 10: sstart,
    11: send, 12: nident2, 13: pident2, 14: evalue
    """
    if not os.path.exists(blast_file) or os.path.getsize(blast_file) == 0:
        return None, 0, 0
    
    # Best hit per query fragment (highest pident)
    best_hits = {}
    with open(blast_file) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 7:
                continue
            qseqid = parts[0]
            aln_len = int(parts[2])
            pident = float(parts[4])
            qlen = int(parts[6])
            
            # Keep best hit per fragment
            if qseqid not in best_hits or pident > best_hits[qseqid][0]:
                best_hits[qseqid] = (pident, aln_len, qlen)
    
    # Calculate ANI: mean identity of aligned fragments
    # Filter: alignment must cover ≥70% of query fragment and identity ≥30%
    identities = []
    total_aligned = 0
    for qid, (pid, alen, qlen) in best_hits.items():
        coverage = alen / qlen if qlen > 0 else 0
        if coverage >= 0.7 and pid >= 30:
            identities.append(pid)
            total_aligned += alen
    
    if identities:
        ani = np.mean(identities) / 100.0  # Convert from % to fraction
    else:
        ani = 0
    
    return ani, len(identities), total_aligned

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
        
        blast_file = os.path.join(BLAST_DIR, f"{s1}_vs_{s2}.blast_tab")
        if not os.path.exists(blast_file):
            continue
        
        ani, n_frags, aligned = parse_blast_for_ani(blast_file)
        if ani is not None and ani > 0:
            ani_matrix.loc[s1, s2] = ani

# Print compact matrix
print("\n=== ANIb Matrix ===")
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)
print(ani_matrix.to_string(float_format=lambda x: f"{x:.4f}" if pd.notna(x) else "  N/A "))

# Within-group analysis
print("\n=== Within-group ANI ===")
for group in sorted(set(GROUPS.values())):
    group_strains = [s for s, g in GROUPS.items() if g == group]
    if len(group_strains) < 2:
        sp = SPECIES[group_strains[0]]
        print(f"  Group {group} ({sp}): single strain {group_strains[0]}")
        continue
    anis = []
    for i, s1 in enumerate(group_strains):
        for s2 in group_strains[i+1:]:
            v = ani_matrix.loc[s1, s2]
            if pd.notna(v) and v > 0:
                anis.append(v)
    if anis:
        sp = SPECIES[group_strains[0]]
        print(f"  Group {group} ({sp}): {min(anis):.4f}-{max(anis):.4f} mean={np.mean(anis):.4f} (n={len(anis)})")
        if min(anis) >= 0.95:
            print(f"    → All pairs ≥0.95 → VERIFIED as same species")
        else:
            print(f"    → Some pairs <0.95 → needs review")
    else:
        print(f"  Group {group}: no valid ANI pairs")

# Between-group analysis  
print("\n=== Between-group ANI (selected) ===")
groups_list = sorted(set(GROUPS.values()))
for i, g1 in enumerate(groups_list):
    for g2 in groups_list[i+1:]:
        s1_list = [s for s, g in GROUPS.items() if g == g1]
        s2_list = [s for s, g in GROUPS.items() if g == g2]
        anis = []
        for s1 in s1_list:
            for s2 in s2_list:
                v = ani_matrix.loc[s1, s2]
                if pd.notna(v) and v > 0:
                    anis.append(v)
        if anis:
            # D1 vs D2 and E1 vs E2 are expected to be ≥0.95 (same species)
            g1b = g1.rstrip('12')
            g2b = g2.rstrip('12')
            same_species = (g1b == g2b)
            symbol = "≥0.95" if min(anis) >= 0.95 else "<0.95"
            cat = "(same species)" if same_species else "(different species)"
            print(f"  {g1} vs {g2}: {min(anis):.4f}-{max(anis):.4f} mean={np.mean(anis):.4f} → {symbol} {cat}")

# Save
ani_matrix.to_csv(os.path.join(ANI_DIR, "ANIb_matrix.tsv"), sep='\t')
print(f"\nMatrix saved to {os.path.join(ANI_DIR, 'ANIb_matrix.tsv')}")
