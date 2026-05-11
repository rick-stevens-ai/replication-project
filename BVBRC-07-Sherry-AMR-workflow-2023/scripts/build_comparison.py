#!/usr/bin/env python3
"""Build a 3-way AMR tool comparison table from AMRFinder, RGI, and ResFinder results."""

import os, sys, json, csv, re
from collections import defaultdict
from pathlib import Path

BASEDIR = Path(__file__).resolve().parent.parent
AMRFINDER_DIR = BASEDIR / "results" / "amrfinder"
RGI_DIR = BASEDIR / "results" / "rgi"
RESFINDER_DIR = BASEDIR / "results" / "resfinder"
OUTPUT_DIR = BASEDIR / "results"

def parse_amrfinder(tsv_path):
    """Parse AMRFinderPlus output, return list of (gene, amr_class, subclass, method)."""
    genes = []
    with open(tsv_path) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            gene = row.get('Element symbol', '').strip()
            amr_class = row.get('Class', '').strip()
            subclass = row.get('Subclass', '').strip()
            scope = row.get('Scope', '').strip()
            etype = row.get('Type', '').strip()
            # Only keep AMR genes, not stress/virulence
            if etype == 'AMR' or scope == 'core':
                genes.append({
                    'gene': gene,
                    'class': amr_class,
                    'subclass': subclass,
                    'tool': 'AMRFinderPlus'
                })
    return genes

def parse_rgi(txt_path):
    """Parse RGI output, return list of (gene, drug_class)."""
    genes = []
    with open(txt_path) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            gene = row.get('Best_Hit_ARO', '').strip()
            drug_class = row.get('Drug Class', '').strip()
            cutoff = row.get('Cut_Off', '').strip()
            # Only Strict and Perfect hits
            if cutoff in ('Strict', 'Perfect'):
                genes.append({
                    'gene': gene,
                    'class': drug_class,
                    'tool': 'RGI'
                })
    return genes

def parse_resfinder(tab_path):
    """Parse ResFinder results_tab output."""
    genes = []
    with open(tab_path) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            gene = row.get('Resistance gene', '').strip()
            phenotype = row.get('Phenotype', '').strip()
            identity = float(row.get('Identity', 0))
            if gene and identity >= 90:
                genes.append({
                    'gene': gene,
                    'class': phenotype,
                    'tool': 'ResFinder'
                })
    return genes

def normalize_gene_name(name):
    """Normalize gene name for comparison (lowercase, strip allele numbers)."""
    name = name.lower().strip()
    # Remove trailing allele numbers like -1, _1, etc. but keep family identifiers
    # e.g., tet(M) stays as tet(m), blaOXA-48 -> blaoxa
    return name

def get_gene_family(name):
    """Extract gene family from gene name for broader comparison."""
    name = name.lower().strip()
    # Common patterns: bla*, tet*, aac*, ant*, aph*, erm*, etc.
    # Remove allele-specific suffixes
    name = re.sub(r'[-_]\d+$', '', name)  # Remove trailing -1, _1
    name = re.sub(r'\d+$', '', name)  # Remove trailing numbers
    return name

def main():
    # Get all genome accessions
    assemblies = sorted([f.stem for f in (BASEDIR / "data" / "assemblies").glob("*.fna")])
    
    results = {}
    summary_stats = {
        'total_genomes': len(assemblies),
        'amrfinder_genomes': 0,
        'rgi_genomes': 0,
        'resfinder_genomes': 0,
        'all_three': 0
    }
    
    for acc in assemblies:
        entry = {'accession': acc, 'amrfinder': [], 'rgi': [], 'resfinder': []}
        
        # AMRFinderPlus
        amr_tsv = AMRFINDER_DIR / f"{acc}.tsv"
        if amr_tsv.exists():
            entry['amrfinder'] = parse_amrfinder(amr_tsv)
            summary_stats['amrfinder_genomes'] += 1
        
        # RGI
        rgi_txt = RGI_DIR / f"{acc}.txt"
        if rgi_txt.exists():
            entry['rgi'] = parse_rgi(rgi_txt)
            summary_stats['rgi_genomes'] += 1
        
        # ResFinder
        rf_tab = RESFINDER_DIR / acc / "ResFinder_results_tab.txt"
        if rf_tab.exists():
            entry['resfinder'] = parse_resfinder(rf_tab)
            summary_stats['resfinder_genomes'] += 1
        
        if amr_tsv.exists() and rgi_txt.exists() and rf_tab.exists():
            summary_stats['all_three'] += 1
        
        results[acc] = entry
    
    # Build per-genome comparison
    comparison = []
    total_amr = defaultdict(int)
    total_rgi = defaultdict(int)
    total_rf = defaultdict(int)
    
    concordance_all3 = 0
    concordance_2of3 = 0
    concordance_1only = 0
    total_unique_genes = 0
    
    for acc, entry in results.items():
        amr_genes = set(normalize_gene_name(g['gene']) for g in entry['amrfinder'])
        rgi_genes = set(normalize_gene_name(g['gene']) for g in entry['rgi'])
        rf_genes = set(normalize_gene_name(g['gene']) for g in entry['resfinder'])
        
        all_genes = amr_genes | rgi_genes | rf_genes
        total_unique_genes += len(all_genes)
        
        for g in all_genes:
            in_amr = g in amr_genes
            in_rgi = g in rgi_genes
            in_rf = g in rf_genes
            count = sum([in_amr, in_rgi, in_rf])
            
            if count == 3:
                concordance_all3 += 1
            elif count == 2:
                concordance_2of3 += 1
            else:
                concordance_1only += 1
        
        for g in entry['amrfinder']:
            cls = g['class'] if g['class'] else 'UNKNOWN'
            total_amr[cls] += 1
        for g in entry['rgi']:
            cls = g['class'].split(';')[0].strip() if g['class'] else 'UNKNOWN'
            total_rgi[cls] += 1
        for g in entry['resfinder']:
            cls = g['class'].split(',')[0].strip() if g['class'] else 'UNKNOWN'
            total_rf[cls] += 1
        
        comparison.append({
            'accession': acc,
            'amrfinder_count': len(entry['amrfinder']),
            'rgi_count': len(entry['rgi']),
            'resfinder_count': len(entry['resfinder']),
            'amrfinder_genes': sorted(set(g['gene'] for g in entry['amrfinder'])),
            'rgi_genes': sorted(set(g['gene'] for g in entry['rgi'])),
            'resfinder_genes': sorted(set(g['gene'] for g in entry['resfinder']))
        })
    
    # Save comparison table
    with open(OUTPUT_DIR / "tool_comparison.json", 'w') as f:
        json.dump({
            'summary': summary_stats,
            'concordance': {
                'all_three_tools': concordance_all3,
                'two_of_three': concordance_2of3,
                'one_only': concordance_1only,
                'total_unique_genes': total_unique_genes
            },
            'per_genome': comparison
        }, f, indent=2)
    
    # Print summary
    print(f"=== 3-Way AMR Tool Comparison ===")
    print(f"Total genomes: {len(assemblies)}")
    print(f"AMRFinderPlus results: {summary_stats['amrfinder_genomes']}")
    print(f"RGI results: {summary_stats['rgi_genomes']}")
    print(f"ResFinder results: {summary_stats['resfinder_genomes']}")
    print(f"All three tools: {summary_stats['all_three']}")
    print()
    
    if total_unique_genes > 0:
        print(f"=== Gene Concordance (normalized names) ===")
        print(f"All 3 tools agree: {concordance_all3} ({100*concordance_all3/total_unique_genes:.1f}%)")
        print(f"2 of 3 agree: {concordance_2of3} ({100*concordance_2of3/total_unique_genes:.1f}%)")
        print(f"1 tool only: {concordance_1only} ({100*concordance_1only/total_unique_genes:.1f}%)")
        print(f"Total unique gene calls: {total_unique_genes}")
    
    print()
    print("=== Per-Genome Summary ===")
    print(f"{'Accession':<25} {'AMRFinder':>10} {'RGI':>10} {'ResFinder':>10}")
    print("-" * 60)
    for c in comparison:
        print(f"{c['accession']:<25} {c['amrfinder_count']:>10} {c['rgi_count']:>10} {c['resfinder_count']:>10}")
    
    # AMR class distribution
    print()
    print("=== AMR Class Distribution (top 10) ===")
    all_classes = set(list(total_amr.keys()) + list(total_rgi.keys()) + list(total_rf.keys()))
    class_data = []
    for cls in all_classes:
        class_data.append((cls, total_amr.get(cls, 0), total_rgi.get(cls, 0), total_rf.get(cls, 0)))
    class_data.sort(key=lambda x: -(x[1] + x[2] + x[3]))
    
    print(f"{'AMR Class':<40} {'AMRFinder':>10} {'RGI':>10} {'ResFinder':>10}")
    print("-" * 75)
    for cls, a, r, rf in class_data[:15]:
        print(f"{cls[:40]:<40} {a:>10} {r:>10} {rf:>10}")

if __name__ == "__main__":
    main()
