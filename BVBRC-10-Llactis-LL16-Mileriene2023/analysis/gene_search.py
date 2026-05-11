#!/usr/bin/env python3
"""Search for specific genes/proteins in L. lactis LL16 genome using BLAST."""

import subprocess
import os
import json

GENOME = "../data/LL16_genome.fna"

# Key genes/proteins to search for from the paper
# We'll use tblastn with protein queries from known L. lactis genes

# GAD operon - glutamate decarboxylase (GABA production) 
# Tryptophan decarboxylase (serotonin) 
# Lactococcin B 
# Enterolysin A
# Bile salt hydrolase
# Fibronectin binding protein
# EPS genes
# Vitamin biosynthesis genes

# Let's first do simple text search in contig headers for any annotation hints
print("=== Checking contig headers ===")
with open(GENOME) as f:
    for line in f:
        if line.startswith(">"):
            print(line.strip()[:120])
            # Just print first few
            break

# For proper analysis, let's use Prodigal for gene prediction since it's simpler than Prokka
# Check if prodigal is available
result = subprocess.run(["which", "prodigal"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"\nProdigal found at: {result.stdout.strip()}")
else:
    print("\nProdigal not found, trying to install...")
    # Try pip or conda
    subprocess.run(["pip3", "install", "pyrodigal"], capture_output=True, text=True)
    
# Use pyrodigal for gene prediction
try:
    import pyrodigal
    print("pyrodigal available")
    HAS_PYRODIGAL = True
except ImportError:
    print("pyrodigal not available, installing...")
    subprocess.run(["pip3", "install", "pyrodigal"], capture_output=True, text=True)
    try:
        import pyrodigal
        HAS_PYRODIGAL = True
    except:
        HAS_PYRODIGAL = False

if HAS_PYRODIGAL:
    import pyrodigal
    
    # Parse genome
    seqs = []
    header = ""
    parts = []
    with open(GENOME) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    seqs.append((header, "".join(parts)))
                header = line[1:]
                parts = []
            else:
                parts.append(line)
    if header:
        seqs.append((header, "".join(parts)))
    
    # Run Prodigal
    orf_finder = pyrodigal.GeneFinder(meta=True)
    
    total_genes = 0
    all_proteins = []
    
    for hdr, seq in seqs:
        genes = orf_finder.find_genes(seq.encode())
        total_genes += len(genes)
        for gene in genes:
            prot = gene.translate()
            contig_id = hdr.split()[0]
            all_proteins.append({
                "contig": contig_id,
                "start": gene.begin,
                "end": gene.end,
                "strand": "+" if gene.strand == 1 else "-",
                "protein": str(prot)
            })
    
    print(f"\n=== GENE PREDICTION (pyrodigal/meta) ===")
    print(f"Total predicted genes: {total_genes}")
    print(f"Paper reports CDS: 2878")
    
    # Write proteins to FASTA for BLAST
    with open("LL16_proteins.faa", "w") as f:
        for i, p in enumerate(all_proteins):
            f.write(f">{p['contig']}_{p['start']}_{p['end']}_{p['strand']}\n")
            f.write(f"{p['protein']}\n")
    
    print(f"Wrote {len(all_proteins)} proteins to LL16_proteins.faa")
    
    # Save gene prediction results
    results = {
        "total_predicted_genes": total_genes,
        "protein_file": "LL16_proteins.faa"
    }
    with open("gene_prediction.json", "w") as f:
        json.dump(results, f, indent=2)

