#!/usr/bin/env python3
"""
Step 1: Fetch AMR phenotype data from BV-BRC API for all genomes.
Matches the paper's approach of using experimentally measured AMR phenotypes.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def read_genome_ids(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return [line.strip() for line in f if line.strip()]

def fetch_amr_batch(genome_ids, batch_size=50):
    """Fetch AMR data from BV-BRC API in batches."""
    all_records = []
    for i in range(0, len(genome_ids), batch_size):
        batch = genome_ids[i:i+batch_size]
        ids_str = ','.join(batch)
        url = (f"https://www.bv-brc.org/api/genome_amr/"
               f"?in(genome_id,({ids_str}))"
               f"&select(genome_id,antibiotic,resistant_phenotype,"
               f"measurement_sign,measurement_value,measurement_unit,"
               f"testing_standard,laboratory_typing_method)"
               f"&limit(25000)")
        
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
                all_records.extend(data)
        except Exception as e:
            print(f"  Error fetching batch {i//batch_size}: {e}", file=sys.stderr)
            time.sleep(5)
            # Retry once
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode())
                    all_records.extend(data)
            except Exception as e2:
                print(f"  Retry failed: {e2}", file=sys.stderr)
        
        if (i // batch_size) % 10 == 0:
            print(f"  Fetched {i+len(batch)}/{len(genome_ids)} genomes...")
        time.sleep(0.3)  # Rate limiting
    
    return all_records

def main():
    organisms = {
        'S_aureus': ('sa_genome_ids.txt', 288),
        'P_aeruginosa': ('pa_genome_ids.txt', 456),
        'E_coli': ('ec_genome_ids.txt', 1588),
    }
    
    for org_name, (id_file, expected_count) in organisms.items():
        print(f"\n{'='*60}")
        print(f"Fetching AMR data for {org_name}...")
        
        genome_ids = read_genome_ids(id_file)
        assert len(genome_ids) == expected_count, \
            f"Expected {expected_count} genomes for {org_name}, got {len(genome_ids)}"
        
        records = fetch_amr_batch(genome_ids)
        print(f"  Total AMR records: {len(records)}")
        
        # Save raw data
        outfile = os.path.join(DATA_DIR, f'{org_name}_amr_raw.json')
        with open(outfile, 'w') as f:
            json.dump(records, f, indent=2)
        
        # Summarize
        antibiotics = {}
        for rec in records:
            ab = rec.get('antibiotic', 'unknown')
            pheno = rec.get('resistant_phenotype', 'unknown')
            if ab not in antibiotics:
                antibiotics[ab] = {'Susceptible': 0, 'Resistant': 0, 'Intermediate': 0, 'other': 0}
            if pheno in antibiotics[ab]:
                antibiotics[ab][pheno] += 1
            else:
                antibiotics[ab]['other'] += 1
        
        print(f"\n  Antibiotics with data ({len(antibiotics)}):")
        for ab in sorted(antibiotics.keys()):
            counts = antibiotics[ab]
            total = sum(counts.values())
            print(f"    {ab}: S={counts['Susceptible']}, R={counts['Resistant']}, "
                  f"I={counts['Intermediate']}, total={total}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
