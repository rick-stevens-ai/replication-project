#!/usr/bin/env python3
"""Fetch reference mecR1 protein (WP_000952923.1) via NCBI E-utilities,
then tblastn against SO1977 db to see if there's a truncated hit at contig edge.
Independent implementation."""
import urllib.request, subprocess, sys, os, tempfile

REF = "WP_000952923.1"
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id={REF}&rettype=fasta&retmode=text"
print(f"Fetching {REF} ...")
data = urllib.request.urlopen(url, timeout=30).read().decode()
print(data[:200])

with open("results/mecR1_ref.faa", "w") as f:
    f.write(data)

# tblastn against SO1977 db
cmd = ["tblastn", "-query", "results/mecR1_ref.faa", "-db", "results/SO1977_db",
       "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore",
       "-evalue", "1e-20"]
print("Running:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDERR:", res.stderr[:500] if res.stderr else "(none)")
print("--- tblastn hits (SO1977) ---")
print(res.stdout if res.stdout else "(no hits)")
with open("results/mecR1_tblastn_SO1977.tsv", "w") as f:
    f.write("qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\n")
    f.write(res.stdout)

# Also against MRSA252 as positive control
cmd2 = ["tblastn", "-query", "results/mecR1_ref.faa", "-db", "results/MRSA252_db",
        "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore",
        "-evalue", "1e-20"]
res2 = subprocess.run(cmd2, capture_output=True, text=True)
print("--- tblastn hits (MRSA252 control) ---")
print(res2.stdout if res2.stdout else "(no hits)")
