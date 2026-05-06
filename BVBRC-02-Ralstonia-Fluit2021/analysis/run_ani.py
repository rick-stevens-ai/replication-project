#!/usr/bin/env python3
"""Run ANIb analysis on assembled Ralstonia genomes using pyani."""
import os
import sys
import glob
import subprocess
import pandas as pd
import numpy as np

WORKDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021")
GENOME_DIR = os.path.join(WORKDIR, "data/genomes")
ANI_DIR = os.path.join(WORKDIR, "analysis/ani")

# Species assignments from paper
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

GROUPS = {
    "551634": "E2", "551636": "E2", "543514": "E2", "551632": "E2", "551637": "E2",
    "543504": "E1", "551631": "E1", "551635": "E1",
    "535633": "D2", "535634": "D2", "535635": "D2", "545260": "D2",
    "545261": "D2", "535632": "D2", "535638": "D1", "543498": "D1",
    "551633": "G", "535637": "F"
}

def run_anib():
    os.makedirs(ANI_DIR, exist_ok=True)
    
    genomes = sorted(glob.glob(os.path.join(GENOME_DIR, "*.fasta")))
    if len(genomes) < 18:
        print(f"WARNING: Only {len(genomes)} genomes found, expected 18")
    
    print(f"Running ANIb on {len(genomes)} genomes...")
    
    # Use pyani's average_nucleotide_identity module directly
    from pyani import anib, pyani_config
    from pyani.pyani_tools import BLASTfunctions
    
    # Or use command-line pyani
    cmd = [
        "average_nucleotide_identity.py",
        "-i", GENOME_DIR,
        "-o", ANI_DIR,
        "-m", "ANIb",
        "--workers", "4",
        "-f", "--gformat", "pdf",
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout[-500:] if result.stdout else "No stdout")
    if result.returncode != 0:
        print(f"STDERR: {result.stderr[-500:]}")
    
    # Parse results
    ani_file = os.path.join(ANI_DIR, "ANIb_percentage_identity.tab")
    if os.path.exists(ani_file):
        df = pd.read_csv(ani_file, sep='\t', index_col=0)
        print(f"\nANIb matrix: {df.shape[0]}x{df.shape[1]}")
        
        # Check clustering with 0.95 cutoff
        print("\n=== Species group validation (0.95 cutoff) ===")
        for s1 in df.index:
            strain1 = os.path.basename(s1).replace('.fasta','')
            for s2 in df.columns:
                strain2 = os.path.basename(s2).replace('.fasta','')
                if strain1 >= strain2:
                    continue
                ani_val = df.loc[s1, s2]
                same_group = GROUPS.get(strain1) == GROUPS.get(strain2)
                if same_group and ani_val < 0.95:
                    print(f"  ISSUE: {strain1}-{strain2} ANI={ani_val:.4f} but same group {GROUPS.get(strain1)}")
                elif not same_group and ani_val >= 0.95:
                    print(f"  ISSUE: {strain1}-{strain2} ANI={ani_val:.4f} but different groups ({GROUPS.get(strain1)} vs {GROUPS.get(strain2)})")
        
        # Summarize within-group and between-group ANI
        groups_set = set(GROUPS.values())
        print("\n=== Within-group ANI ranges ===")
        for g in sorted(groups_set):
            strains_in_group = [s for s, gr in GROUPS.items() if gr == g]
            if len(strains_in_group) < 2:
                print(f"  Group {g}: only 1 strain ({strains_in_group[0]})")
                continue
            anis = []
            for i, s1 in enumerate(strains_in_group):
                for s2 in strains_in_group[i+1:]:
                    # Find matching column names
                    for c1 in df.index:
                        if s1 in str(c1):
                            for c2 in df.columns:
                                if s2 in str(c2):
                                    anis.append(df.loc[c1, c2])
            if anis:
                print(f"  Group {g}: {min(anis):.4f} - {max(anis):.4f} (n={len(anis)} pairs)")
        
        # Save summary
        summary_file = os.path.join(ANI_DIR, "ani_summary.txt")
        with open(summary_file, 'w') as f:
            f.write("ANIb Summary for Fluit et al. 2021 Replication\n")
            f.write(f"Genomes analyzed: {df.shape[0]}\n\n")
            f.write(df.to_string())
        print(f"\nSummary saved to {summary_file}")
    else:
        print(f"ANIb output not found at {ani_file}")
        print(f"Files in {ANI_DIR}: {os.listdir(ANI_DIR)}")

if __name__ == "__main__":
    run_anib()
