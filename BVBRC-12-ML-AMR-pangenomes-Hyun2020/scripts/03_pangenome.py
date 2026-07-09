#!/usr/bin/env python3
"""
Step 3: Pan-genome construction using CD-Hit.
Matches paper: identity threshold 0.8, word length 5.
Core genes: missing in ≤10 genomes; Unique: present in ≤10 genomes.
"""

import os
import sys
import subprocess
import json
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')

CORE_THRESHOLD = 10  # Gene is core if missing from ≤10 genomes

def read_genome_ids(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return [line.strip() for line in f if line.strip()]

def concatenate_proteins(org_name, genome_ids):
    """Concatenate all protein files, tagging each sequence with genome ID."""
    prot_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
    outfile = os.path.join(DATA_DIR, f'{org_name}_all_proteins.faa')
    
    if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
        print(f"  Using existing concatenated file: {outfile}")
        return outfile
    
    total_seqs = 0
    with open(outfile, 'w') as out:
        for gid in genome_ids:
            fpath = os.path.join(prot_dir, f'{gid}.faa')
            if not os.path.exists(fpath):
                print(f"  WARNING: Missing proteins for {gid}", file=sys.stderr)
                continue
            with open(fpath) as f:
                for line in f:
                    if line.startswith('>'):
                        total_seqs += 1
                    out.write(line)
    
    print(f"  Total sequences: {total_seqs}")
    return outfile

def run_cdhit(input_faa, output_prefix, identity=0.8, word_length=5, threads=4):
    """Run CD-Hit to cluster proteins."""
    clstr_file = f"{output_prefix}.clstr"
    if os.path.exists(clstr_file) and os.path.getsize(clstr_file) > 100:
        print(f"  Using existing CD-Hit output: {clstr_file}")
        return output_prefix
    
    cmd = [
        'cd-hit',
        '-i', input_faa,
        '-o', output_prefix,
        '-c', str(identity),
        '-n', str(word_length),
        '-d', '0',  # full description
        '-M', '8000',  # memory limit MB
        '-T', str(threads),
    ]
    
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  CD-Hit error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print(f"  CD-Hit stdout: {result.stdout[-500:]}")
    return output_prefix

def parse_cdhit_clusters(clstr_file):
    """Parse CD-Hit cluster file to get gene clusters and alleles."""
    clusters = {}
    current_cluster = None
    
    with open(clstr_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>Cluster'):
                current_cluster = int(line.split()[1])
                clusters[current_cluster] = []
            elif current_cluster is not None and line:
                # Parse member: "0  2681aa, >fig|1280.15931.peg.1175|C3B39... *"
                parts = line.split('>')
                if len(parts) >= 2:
                    seq_id = parts[1].split('|')[0] + '|' + parts[1].split('|')[1] if '|' in parts[1] else parts[1].split()[0]
                    # Extract full PATRIC ID
                    full_id = parts[1].split('...')[0].strip()
                    if full_id.endswith('*'):
                        full_id = full_id[:-1].strip()
                    # More robust parsing
                    raw = parts[1].strip()
                    # Get the sequence ID up to the first space or |
                    # Format: fig|GENOME.peg.N|LOCUS| description
                    seq_parts = raw.split('|')
                    if len(seq_parts) >= 2:
                        patric_id = f"fig|{seq_parts[1]}"
                        # Extract genome ID from patric_id
                        # fig|1280.15931.peg.2071
                        genome_id = '.'.join(seq_parts[1].split('.')[:-1])  # Remove .peg.N
                    else:
                        patric_id = raw.split()[0]
                        genome_id = 'unknown'
                    
                    is_rep = '*' in line
                    clusters[current_cluster].append({
                        'patric_id': patric_id,
                        'genome_id': genome_id,
                        'is_representative': is_rep,
                        'raw': raw[:100]
                    })
    
    return clusters

def classify_genes(clusters, n_genomes):
    """Classify genes as core, accessory, or unique based on genome presence."""
    gene_info = {}
    
    for cluster_id, members in clusters.items():
        # Get unique genome IDs in this cluster
        genomes_with_gene = set()
        for m in members:
            genomes_with_gene.add(m['genome_id'])
        
        n_present = len(genomes_with_gene)
        n_missing = n_genomes - n_present
        
        if n_missing <= CORE_THRESHOLD:
            gene_type = 'core'
        elif n_present <= CORE_THRESHOLD:
            gene_type = 'unique'
        else:
            gene_type = 'accessory'
        
        gene_info[cluster_id] = {
            'type': gene_type,
            'n_genomes': n_present,
            'n_alleles': len(members),
            'genomes': list(genomes_with_gene)
        }
    
    return gene_info

def main():
    organisms = [
        ('S_aureus', 'sa_genome_ids.txt', 288),
        ('P_aeruginosa', 'pa_genome_ids.txt', 456),
        ('E_coli', 'ec_genome_ids.txt', 1588),
    ]
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    for org_name, id_file, expected_count in organisms:
        print(f"\n{'='*60}")
        print(f"Pan-genome construction for {org_name}")
        
        genome_ids = read_genome_ids(id_file)
        
        # Check if all proteins are available
        prot_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
        available = [gid for gid in genome_ids 
                     if os.path.exists(os.path.join(prot_dir, f'{gid}.faa'))
                     and os.path.getsize(os.path.join(prot_dir, f'{gid}.faa')) > 100]
        
        if len(available) < expected_count:
            print(f"  WARNING: Only {len(available)}/{expected_count} genomes have proteins")
            if len(available) < expected_count * 0.9:
                print(f"  Skipping — need at least 90% of genomes")
                continue
        
        # Concatenate proteins
        print(f"  Concatenating proteins...")
        all_proteins = concatenate_proteins(org_name, available)
        
        # Run CD-Hit
        output_prefix = os.path.join(RESULTS_DIR, f'{org_name}_cdhit')
        print(f"  Running CD-Hit...")
        run_cdhit(all_proteins, output_prefix)
        
        # Parse clusters
        clstr_file = f"{output_prefix}.clstr"
        if os.path.exists(clstr_file):
            print(f"  Parsing clusters...")
            clusters = parse_cdhit_clusters(clstr_file)
            
            # Classify genes
            gene_info = classify_genes(clusters, len(available))
            
            n_core = sum(1 for g in gene_info.values() if g['type'] == 'core')
            n_acc = sum(1 for g in gene_info.values() if g['type'] == 'accessory')
            n_uniq = sum(1 for g in gene_info.values() if g['type'] == 'unique')
            
            print(f"\n  Pan-genome summary for {org_name}:")
            print(f"    Total gene clusters: {len(clusters)}")
            print(f"    Core genes (missing ≤{CORE_THRESHOLD}): {n_core}")
            print(f"    Accessory genes: {n_acc}")
            print(f"    Unique genes (present ≤{CORE_THRESHOLD}): {n_uniq}")
            
            # Save gene info
            info_file = os.path.join(RESULTS_DIR, f'{org_name}_gene_info.json')
            with open(info_file, 'w') as f:
                json.dump(gene_info, f)
            
            # Save cluster summary
            summary_file = os.path.join(RESULTS_DIR, f'{org_name}_pangenome_summary.json')
            with open(summary_file, 'w') as f:
                json.dump({
                    'organism': org_name,
                    'n_genomes': len(available),
                    'total_clusters': len(clusters),
                    'core_genes': n_core,
                    'accessory_genes': n_acc,
                    'unique_genes': n_uniq,
                    'core_threshold': CORE_THRESHOLD,
                }, f, indent=2)
        else:
            print(f"  ERROR: CD-Hit cluster file not found")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
