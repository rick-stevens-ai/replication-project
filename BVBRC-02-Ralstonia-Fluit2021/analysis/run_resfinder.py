#!/usr/bin/env python3
"""Run ResFinder-like AMR gene detection using BLAST against ResFinder DB."""
import os
import sys
import glob
import subprocess
import json
from Bio import SeqIO

WORKDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021")
GENOME_DIR = os.path.join(WORKDIR, "data/genomes")
RESFINDER_DIR = os.path.join(WORKDIR, "analysis/resfinder")

# Expected results from paper
EXPECTED = {
    "551634": ["blaOXA-22", "blaOXA-60"],
    "551636": ["blaOXA-22", "blaOXA-60"],
    "543514": ["blaOXA-22", "blaOXA-60"],
    "551632": ["blaOXA-22", "blaOXA-60"],
    "551637": ["blaOXA-22", "blaOXA-60"],
    "543504": ["blaOXA-22", "blaOXA-60"],
    "551631": ["blaOXA-22", "blaOXA-60"],
    "551635": ["blaOXA-22", "blaOXA-60"],
    "535633": ["blaOXA-22", "blaOXA-60"],
    "535634": ["blaOXA-22", "blaOXA-60"],
    "535635": ["blaOXA-22", "blaOXA-60"],
    "545260": ["blaOXA-22", "blaOXA-60", "aadA2", "ant(2'')-Ia", "aph(6)-Id", "cmlA1", "strA", "sul1"],
    "545261": ["blaOXA-22", "blaOXA-60", "aadA2", "ant(2'')-Ia", "aph(6)-Id", "cmlA1", "strA", "sul1"],
    "535632": ["blaOXA-22", "blaOXA-60"],
    "535638": ["blaOXA-22", "blaOXA-60"],
    "543498": ["blaOXA-22", "blaOXA-60"],
    "551633": ["blaOXA-22", "blaOXA-60"],
    "535637": ["blaOXA-22", "blaOXA-60"],
}

def setup_resfinder_db():
    """Download ResFinder database if not present."""
    db_dir = os.path.join(WORKDIR, "data/resfinder_db")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print("Downloading ResFinder database...")
        subprocess.run([
            "git", "clone", "https://bitbucket.org/genomicepidemiology/resfinder_db.git",
            db_dir
        ], check=True)
    return db_dir

def run_blast_resfinder(genome_path, db_dir, strain):
    """Run BLAST against ResFinder DB for a single genome."""
    results = []
    # Combine all ResFinder gene files
    all_genes = os.path.join(db_dir, "all_genes.fasta")
    if not os.path.exists(all_genes):
        with open(all_genes, 'w') as out:
            for fasta in glob.glob(os.path.join(db_dir, "*.fsa")):
                for rec in SeqIO.parse(fasta, 'fasta'):
                    out.write(f">{rec.id}\n{str(rec.seq)}\n")
        # Make BLAST database
        subprocess.run(["makeblastdb", "-in", all_genes, "-dbtype", "nucl", "-out", 
                       os.path.join(db_dir, "resfinder_all")], check=True, capture_output=True)
    
    # Run BLAST
    blast_out = os.path.join(RESFINDER_DIR, f"{strain}_blast.tsv")
    cmd = [
        "blastn", "-query", genome_path,
        "-db", os.path.join(db_dir, "resfinder_all"),
        "-out", blast_out,
        "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore slen",
        "-evalue", "1e-10",
        "-perc_identity", "80",
        "-num_threads", "4"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Parse results - filter for ≥80% coverage and ≥90% identity (ResFinder defaults)
    hits = {}
    if os.path.exists(blast_out) and os.path.getsize(blast_out) > 0:
        with open(blast_out) as f:
            for line in f:
                parts = line.strip().split('\t')
                sseqid = parts[1]
                pident = float(parts[2])
                length = int(parts[3])
                slen = int(parts[12])
                coverage = length / slen * 100
                gene_name = sseqid.split('_')[0]
                if pident >= 80 and coverage >= 60:
                    if gene_name not in hits or pident > hits[gene_name]['pident']:
                        hits[gene_name] = {'pident': pident, 'coverage': coverage, 'sseqid': sseqid}
    
    return hits

def main():
    os.makedirs(RESFINDER_DIR, exist_ok=True)
    
    # Setup DB
    db_dir = setup_resfinder_db()
    
    genomes = sorted(glob.glob(os.path.join(GENOME_DIR, "*.fasta")))
    print(f"Running ResFinder analysis on {len(genomes)} genomes...")
    
    all_results = {}
    for gf in genomes:
        strain = os.path.basename(gf).replace('.fasta', '')
        print(f"\n  Strain {strain}:")
        hits = run_blast_resfinder(gf, db_dir, strain)
        all_results[strain] = hits
        
        # Check against expected
        expected = EXPECTED.get(strain, [])
        found_genes = set(hits.keys())
        
        oxa22 = any('OXA-22' in g or 'oxa-22' in g.lower() for g in found_genes)
        oxa60 = any('OXA-60' in g or 'oxa-60' in g.lower() for g in found_genes)
        
        print(f"    Found {len(hits)} resistance genes")
        for gene, info in sorted(hits.items()):
            print(f"      {gene}: {info['pident']:.1f}% identity, {info['coverage']:.1f}% coverage")
        
        if not oxa22:
            print(f"    WARNING: OXA-22 family NOT found (expected)")
        if not oxa60:
            print(f"    WARNING: OXA-60 family NOT found (expected)")
    
    # Summary
    summary_file = os.path.join(RESFINDER_DIR, "resfinder_summary.tsv")
    with open(summary_file, 'w') as f:
        f.write("Strain\tGenes_Found\tOXA22\tOXA60\tAdditional_Genes\n")
        for strain in sorted(all_results):
            hits = all_results[strain]
            genes = sorted(hits.keys())
            oxa22 = "Yes" if any('OXA-22' in g or 'oxa-22' in g.lower() for g in genes) else "No"
            oxa60 = "Yes" if any('OXA-60' in g or 'oxa-60' in g.lower() for g in genes) else "No"
            additional = [g for g in genes if 'OXA' not in g.upper()]
            f.write(f"{strain}\t{','.join(genes)}\t{oxa22}\t{oxa60}\t{','.join(additional)}\n")
    
    print(f"\nSummary saved to {summary_file}")

if __name__ == "__main__":
    main()
