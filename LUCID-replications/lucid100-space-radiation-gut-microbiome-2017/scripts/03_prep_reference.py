#!/usr/bin/env python3
"""Convert mothur SILVA seed alignment -> ungapped FASTA + tax map,
   and extract V4 region (515F..806R) for compact reference."""
import re, sys
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "reference"
ALIGN = REF / "silva.seed_v138_1.align"
TAX   = REF / "silva.seed_v138_1.tax"
OUT_FASTA = REF / "silva_seed_v138_1.ungapped.fasta"
OUT_TAX   = REF / "silva_seed_v138_1.tax.tsv"
OUT_V4    = REF / "silva_seed_v138_1.v4.fasta"

# Parse taxonomy file (acc \t taxonomy)
tax = {}
with TAX.open() as fh:
    for line in fh:
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2:
            tax[parts[0]] = parts[1].rstrip(";")

# Parse aligned fasta (gap char is '-' or '.')
gap_re = re.compile(r"[-.]")

n_full = 0
n_v4   = 0

# 515F: GTGYCAGCMGCCGCGGTAA   806R: GGACTACNVGGGTWTCTAAT
# Use IUPAC-tolerant regex match on ungapped seq
def iupac_to_regex(p):
    m = {'A':'A','C':'C','G':'G','T':'T','U':'T','R':'[AG]','Y':'[CT]','S':'[GC]','W':'[AT]','K':'[GT]','M':'[AC]','B':'[CGT]','D':'[AGT]','H':'[ACT]','V':'[ACG]','N':'[ACGT]'}
    return ''.join(m[c] for c in p.upper())

fwd_re = re.compile(iupac_to_regex("GTGYCAGCMGCCGCGGTAA"))
# reverse complement of 806R: ATTAGAWACCCBNGTAGTCC
rev_re = re.compile(iupac_to_regex("ATTAGAWACCCBNGTAGTCC"))

cur_id = None
cur_seq = []
def flush(fid, fseq, fa_h, v4_h):
    global n_full, n_v4
    if not fid:
        return
    acc = fid.split()[0]
    seq = gap_re.sub("", "".join(fseq)).upper().replace("U","T")
    if len(seq) < 300:
        return
    if acc not in tax:
        return
    fa_h.write(f">{acc}\n{seq}\n")
    n_full += 1
    # Extract V4 between 515F primer and 806R revcomp
    m1 = fwd_re.search(seq)
    if not m1:
        return
    m2 = rev_re.search(seq, m1.end())
    if not m2:
        return
    v4 = seq[m1.end():m2.start()]
    if 200 <= len(v4) <= 350:
        v4_h.write(f">{acc}\n{v4}\n")
        n_v4 += 1

with ALIGN.open() as fh, OUT_FASTA.open("w") as fa, OUT_V4.open("w") as v4f:
    for line in fh:
        if line.startswith(">"):
            flush(cur_id, cur_seq, fa, v4f)
            cur_id = line[1:].rstrip()
            cur_seq = []
        else:
            cur_seq.append(line.rstrip())
    flush(cur_id, cur_seq, fa, v4f)

# Write taxonomy tsv (only IDs in fasta)
with OUT_TAX.open("w") as out:
    out.write("seqid\ttaxonomy\n")
    for k, v in tax.items():
        out.write(f"{k}\t{v}\n")

print(f"Wrote ungapped FASTA: {n_full} seqs -> {OUT_FASTA}")
print(f"Wrote V4 FASTA:        {n_v4} seqs -> {OUT_V4}")
print(f"Wrote tax map:         {len(tax)} entries -> {OUT_TAX}")
