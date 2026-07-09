#!/usr/bin/env python3
"""
Download protein FASTA files from BV-BRC for P. aeruginosa and E. coli genomes.
Uses the BV-BRC Data API with protein+fasta accept header.
"""

import os
import sys
import time
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

BVBRC_API = "https://www.bv-brc.org/api"


def download_proteins(genome_id, output_file, max_retries=3):
    """Download protein FASTA for a genome from BV-BRC."""
    url = (f"{BVBRC_API}/genome_feature/"
           f"?eq(genome_id,{genome_id})"
           f"&eq(annotation,PATRIC)"
           f"&eq(feature_type,CDS)"
           f"&limit(25000)")
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/protein+fasta')
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read().decode('utf-8', errors='replace')
            
            if not data.strip() or not data.strip().startswith('>'):
                return 0
            
            with open(output_file, 'w') as f:
                f.write(data)
            
            # Count sequences
            count = data.count('\n>')  + (1 if data.startswith('>') else 0)
            return count
            
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 5
                time.sleep(wait)
            else:
                print(f"    FAILED {genome_id}: {e}", flush=True)
                return -1
        except Exception as e:
            print(f"    ERROR {genome_id}: {e}", flush=True)
            return -1


def download_organism(org_name, genome_ids_file, protein_dir):
    """Download all missing protein files for an organism."""
    
    with open(genome_ids_file) as f:
        genome_ids = [l.strip() for l in f if l.strip()]
    
    os.makedirs(protein_dir, exist_ok=True)
    
    # Check which are already downloaded
    existing = set()
    for gid in genome_ids:
        fpath = os.path.join(protein_dir, f'{gid}.faa')
        if os.path.exists(fpath) and os.path.getsize(fpath) > 100:
            existing.add(gid)
    
    missing = [gid for gid in genome_ids if gid not in existing]
    
    print(f"\n{org_name}: {len(genome_ids)} genomes total, "
          f"{len(existing)} already downloaded, {len(missing)} to fetch", flush=True)
    
    if not missing:
        print("  All done!", flush=True)
        return
    
    success = 0
    failed = 0
    empty = 0
    
    for i, gid in enumerate(missing):
        fpath = os.path.join(protein_dir, f'{gid}.faa')
        n_prots = download_proteins(gid, fpath)
        
        if n_prots > 0:
            success += 1
        elif n_prots == 0:
            empty += 1
        else:
            failed += 1
        
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(missing)} "
                  f"(success={success}, empty={empty}, failed={failed})", flush=True)
        
        # Rate limiting
        time.sleep(0.3)
    
    print(f"\n  Complete: {success} downloaded, {empty} empty, {failed} failed", flush=True)


def main():
    org = sys.argv[1] if len(sys.argv) > 1 else 'pa'
    
    if org in ('pa', 'both'):
        download_organism(
            'P. aeruginosa',
            os.path.join(DATA_DIR, 'pa_genome_ids.txt'),
            os.path.join(DATA_DIR, 'P_aeruginosa_proteins')
        )
    
    if org in ('ec', 'both'):
        download_organism(
            'E. coli',
            os.path.join(DATA_DIR, 'ec_genome_ids.txt'),
            os.path.join(DATA_DIR, 'E_coli_proteins')
        )


if __name__ == '__main__':
    main()
