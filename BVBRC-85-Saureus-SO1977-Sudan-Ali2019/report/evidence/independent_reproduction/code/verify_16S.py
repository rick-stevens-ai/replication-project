#!/usr/bin/env python3
"""Verify SO1977 16S rRNA is S. aureus by fetching a reference S. aureus 16S
directly from NCBI E-utilities and computing pairwise identity."""
import urllib.request, sys, subprocess

# NR_074995.1 = Staphylococcus aureus 16S rRNA reference sequence (NCBI reference bacterial ribosomal RNA)
REF_ACC = "NR_074995.1"
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={REF_ACC}&rettype=fasta&retmode=text"
print(f"Fetching S. aureus 16S reference: {REF_ACC}")
data = urllib.request.urlopen(url, timeout=60).read().decode()
first_line = data.split("\n",1)[0]
print(f"Header: {first_line}")

with open("results/Saureus_16S_ref.fa", "w") as f:
    f.write(data)

# Also fetch a different-species control (E. coli 16S) to prove specificity
CTRL_ACC = "NR_024570.1"  # E. coli
url_c = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={CTRL_ACC}&rettype=fasta&retmode=text"
print(f"Fetching E. coli 16S control: {CTRL_ACC}")
data_c = urllib.request.urlopen(url_c, timeout=60).read().decode()
print(f"Header: {data_c.split(chr(10),1)[0]}")

with open("results/Ecoli_16S_ctrl.fa", "w") as f:
    f.write(data_c)

# Build local blast DB from concat, then blast our SO1977 16S against it
with open("results/refs_16S.fa", "w") as f:
    f.write(data)
    f.write(data_c)

subprocess.run(["makeblastdb", "-in", "results/refs_16S.fa", "-dbtype", "nucl",
                "-out", "results/refs_16S_db"], check=True, capture_output=True)
res = subprocess.run(
    ["blastn", "-query", "results/SO1977_16S.fa", "-db", "results/refs_16S_db",
     "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore",
     "-word_size", "20"],
    capture_output=True, text=True)
print("--- BLAST SO1977 16S vs (S. aureus ref, E. coli ctrl) ---")
print(res.stdout)
with open("results/SO1977_16S_vs_refs.tsv", "w") as f:
    f.write("qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\n")
    f.write(res.stdout)
