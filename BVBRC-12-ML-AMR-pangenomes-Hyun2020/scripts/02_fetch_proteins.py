#!/usr/bin/env python3
"""
Step 2: Fetch protein FASTA sequences from BV-BRC for all genomes.
Downloads PATRIC annotation protein sequences.
"""

import json
import os
import sys
import time
import urllib.request
import gzip

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def read_genome_ids(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return [line.strip() for line in f if line.strip()]

def fetch_proteins_for_genome(genome_id, output_dir, max_retries=3):
    """Fetch protein FASTA for a single genome from BV-BRC."""
    outfile = os.path.join(output_dir, f"{genome_id}.faa")
    if os.path.exists(outfile) and os.path.getsize(outfile) > 100:
        return True  # Already downloaded
    
    # Use the genome_feature API to get protein sequences
    url = (f"https://www.bv-brc.org/api/genome_feature/"
           f"?and(eq(genome_id,{genome_id}),eq(annotation,PATRIC),eq(feature_type,CDS))"
           f"&select(patric_id,aa_sequence,product)"
           f"&limit(25000)"
           f"&http_accept=application/json")
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
            
            if not data:
                return False
            
            with open(outfile, 'w') as f:
                for feat in data:
                    pid = feat.get('patric_id', 'unknown')
                    seq = feat.get('aa_sequence', '')
                    product = feat.get('product', 'hypothetical protein')
                    if seq:
                        f.write(f">{pid} {product}\n{seq}\n")
            
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  Failed {genome_id}: {e}", file=sys.stderr)
                return False
    return False

def main():
    organisms = {
        'S_aureus': ('sa_genome_ids.txt', 288),
        'P_aeruginosa': ('pa_genome_ids.txt', 456),
        'E_coli': ('ec_genome_ids.txt', 1588),
    }
    
    for org_name, (id_file, expected_count) in organisms.items():
        print(f"\n{'='*60}")
        print(f"Fetching proteins for {org_name} ({expected_count} genomes)...")
        
        output_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
        os.makedirs(output_dir, exist_ok=True)
        
        genome_ids = read_genome_ids(id_file)
        
        success = 0
        failed = 0
        skipped = 0
        
        for i, gid in enumerate(genome_ids):
            outfile = os.path.join(output_dir, f"{gid}.faa")
            if os.path.exists(outfile) and os.path.getsize(outfile) > 100:
                skipped += 1
                success += 1
                continue
            
            if fetch_proteins_for_genome(gid, output_dir):
                success += 1
            else:
                failed += 1
            
            if (i + 1) % 25 == 0:
                print(f"  Progress: {i+1}/{len(genome_ids)} "
                      f"(success={success}, failed={failed}, skipped={skipped})")
            
            time.sleep(0.5)  # Rate limiting
        
        print(f"  Final: {success} success, {failed} failed, {skipped} skipped "
              f"out of {len(genome_ids)} genomes")
        
        # Count total proteins
        total_proteins = 0
        for gid in genome_ids:
            fpath = os.path.join(output_dir, f"{gid}.faa")
            if os.path.exists(fpath):
                with open(fpath) as f:
                    total_proteins += sum(1 for line in f if line.startswith('>'))
        print(f"  Total proteins: {total_proteins}")

if __name__ == '__main__':
    main()
