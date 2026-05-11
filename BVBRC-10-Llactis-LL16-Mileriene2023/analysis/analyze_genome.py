#!/usr/bin/env python3
"""Comprehensive analysis of L. lactis LL16 genome for paper replication."""

import json
import os
from collections import defaultdict

GENOME_FILE = "../data/LL16_genome.fna"

def parse_fasta(filepath):
    """Parse a FASTA file and return list of (header, sequence) tuples."""
    sequences = []
    header = ""
    seq_parts = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    sequences.append((header, "".join(seq_parts)))
                header = line[1:]
                seq_parts = []
            else:
                seq_parts.append(line)
    if header:
        sequences.append((header, "".join(seq_parts)))
    return sequences

def genome_stats(sequences):
    """Calculate basic genome statistics."""
    lengths = [len(s) for _, s in sequences]
    total = sum(lengths)
    
    # GC content
    gc = sum(s.count('G') + s.count('C') + s.count('g') + s.count('c') for _, s in sequences)
    at = sum(s.count('A') + s.count('T') + s.count('a') + s.count('t') for _, s in sequences)
    gc_pct = gc / (gc + at) * 100 if (gc + at) > 0 else 0
    
    # N50
    sorted_lengths = sorted(lengths, reverse=True)
    cumsum = 0
    n50 = 0
    l50 = 0
    for i, l in enumerate(sorted_lengths):
        cumsum += l
        if cumsum >= total / 2:
            n50 = l
            l50 = i + 1
            break
    
    return {
        "total_length": total,
        "num_contigs": len(sequences),
        "gc_content": round(gc_pct, 2),
        "longest_contig": max(lengths),
        "shortest_contig": min(lengths),
        "n50": n50,
        "l50": l50,
        "mean_contig_length": round(total / len(sequences), 1),
    }

def find_orfs(sequence, min_length=300):
    """Simple ORF finder - finds all ORFs >= min_length bp."""
    start_codons = {"ATG", "GTG", "TTG"}
    stop_codons = {"TAA", "TAG", "TGA"}
    orfs = []
    
    for frame in range(3):
        i = frame
        start_pos = None
        while i < len(sequence) - 2:
            codon = sequence[i:i+3].upper()
            if codon in start_codons and start_pos is None:
                start_pos = i
            elif codon in stop_codons and start_pos is not None:
                orf_len = i + 3 - start_pos
                if orf_len >= min_length:
                    orfs.append((start_pos, i + 3, orf_len, '+'))
                start_pos = None
            i += 3
    
    # Reverse complement
    comp = str.maketrans('ATGCatgc', 'TACGtacg')
    rev_seq = sequence[::-1].translate(comp)
    
    for frame in range(3):
        i = frame
        start_pos = None
        while i < len(rev_seq) - 2:
            codon = rev_seq[i:i+3].upper()
            if codon in start_codons and start_pos is None:
                start_pos = i
            elif codon in stop_codons and start_pos is not None:
                orf_len = i + 3 - start_pos
                if orf_len >= min_length:
                    orfs.append((len(sequence) - i - 3, len(sequence) - start_pos, orf_len, '-'))
                start_pos = None
            i += 3
    
    return orfs

# Main analysis
print("=" * 60)
print("L. lactis LL16 Genome Analysis")
print("=" * 60)

sequences = parse_fasta(GENOME_FILE)
stats = genome_stats(sequences)

print(f"\n=== GENOME STATISTICS ===")
for k, v in stats.items():
    print(f"  {k}: {v}")

# Paper claims comparison
print(f"\n=== COMPARISON WITH PAPER CLAIMS ===")
paper_claims = {
    "genome_size": 2589406,
    "gc_content": 35.4,
    "subsystems": 246,
    "num_cds": 2878,
    "num_rnas": 63,
}

print(f"  Paper genome size: {paper_claims['genome_size']} bp")
print(f"  Our genome size (NCBI deposit): {stats['total_length']} bp")
print(f"  Difference: {paper_claims['genome_size'] - stats['total_length']} bp")
print(f"  Note: NCBI may filter short contigs from WGS deposit")
print(f"  Paper GC content: {paper_claims['gc_content']}%")
print(f"  Our GC content: {stats['gc_content']}%")

# Count total ORFs across all contigs
print(f"\n=== ORF PREDICTION ===")
total_orfs = 0
all_orf_lengths = []
for header, seq in sequences:
    orfs = find_orfs(seq, min_length=300)
    total_orfs += len(orfs)
    all_orf_lengths.extend([l for _, _, l, _ in orfs])

print(f"  Total ORFs (≥300bp/100aa): {total_orfs}")
print(f"  Paper reports CDS: {paper_claims['num_cds']}")

# Save results
results = {
    "genome_stats": stats,
    "paper_claims": paper_claims,
    "total_orfs_predicted": total_orfs,
}

with open("genome_stats.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to genome_stats.json")
