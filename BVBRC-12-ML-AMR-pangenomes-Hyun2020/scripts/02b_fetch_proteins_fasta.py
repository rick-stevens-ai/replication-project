#!/usr/bin/env python3
"""
Step 2b: Fetch protein FASTA sequences from BV-BRC using http_accept=protein+fasta.
"""

import os
import sys
import time
import urllib.request
import urllib.error

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def read_genome_ids(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return [line.strip() for line in f if line.strip()]

def fetch_proteins_fasta(genome_id, output_dir, max_retries=3):
    """Fetch protein FASTA via BV-BRC protein+fasta endpoint."""
    outfile = os.path.join(output_dir, f"{genome_id}.faa")
    if os.path.exists(outfile) and os.path.getsize(outfile) > 100:
        return True
    
    url = (f"https://www.bv-brc.org/api/genome_feature/"
           f"?and(eq(genome_id,{genome_id}),eq(annotation,PATRIC),eq(feature_type,CDS))"
           f"&limit(25000)"
           f"&http_accept=application/protein+fasta")
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read().decode()
            
            if not data or not data.startswith('>'):
                return False
            
            with open(outfile, 'w') as f:
                f.write(data)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(3 * (attempt + 1))
            else:
                print(f"  Failed {genome_id}: {e}", file=sys.stderr)
                return False
    return False

def main():
    organisms = [
        ('S_aureus', 'sa_genome_ids.txt', 288),
        ('P_aeruginosa', 'pa_genome_ids.txt', 456),
        ('E_coli', 'ec_genome_ids.txt', 1588),
    ]
    
    for org_name, id_file, expected_count in organisms:
        print(f"\n{'='*60}")
        print(f"Fetching proteins for {org_name} ({expected_count} genomes)...")
        sys.stdout.flush()
        
        output_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
        os.makedirs(output_dir, exist_ok=True)
        
        genome_ids = read_genome_ids(id_file)
        
        success = 0
        failed = []
        already = 0
        
        for i, gid in enumerate(genome_ids):
            outfile = os.path.join(output_dir, f"{gid}.faa")
            if os.path.exists(outfile) and os.path.getsize(outfile) > 100:
                already += 1
                success += 1
                continue
            
            if fetch_proteins_fasta(gid, output_dir):
                success += 1
            else:
                failed.append(gid)
            
            if (i + 1) % 50 == 0:
                print(f"  {org_name}: {i+1}/{len(genome_ids)} "
                      f"(success={success}, cached={already}, failed={len(failed)})")
                sys.stdout.flush()
            
            time.sleep(0.4)
        
        print(f"  {org_name} DONE: {success} success, {len(failed)} failed")
        sys.stdout.flush()
        
        if failed:
            with open(os.path.join(DATA_DIR, f'{org_name}_failed_ids.txt'), 'w') as f:
                f.write('\n'.join(failed))

if __name__ == '__main__':
    main()
