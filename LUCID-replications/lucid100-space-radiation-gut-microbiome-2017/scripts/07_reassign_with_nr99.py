#!/usr/bin/env python3
"""Convert DADA2 SILVA 138.1 NR99 train_set fasta -> seq+tax fasta usable
   by vsearch.  Header format in the source file is:
     >Bacteria;Firmicutes;Clostridia;...;Lachnospiraceae;
   We replace each header with a numeric ID and store id->tax in a map.
"""
import gzip, re
from pathlib import Path
REF = Path(__file__).resolve().parents[1]/"reference"
SRC = REF/"silva_nr99_v138.1_train_set.fa.gz"
OUT = REF/"silva_nr99_v138.fasta"
MAP = REF/"silva_nr99_v138.tax.tsv"

n = 0
with gzip.open(SRC, "rt") as fh, OUT.open("w") as fa, MAP.open("w") as mp:
    mp.write("seqid\ttaxonomy\n")
    cur_id = None
    cur_seq = []
    def flush():
        global n
        if cur_id is None: return
        seq = "".join(cur_seq)
        if len(seq) < 300: return
        n += 1
        new_id = f"ref_{n:07d}"
        fa.write(f">{new_id}\n{seq}\n")
        mp.write(f"{new_id}\t{cur_id}\n")
    for line in fh:
        if line.startswith(">"):
            flush()
            cur_id = line[1:].rstrip().rstrip(";")
            cur_seq = []
        else:
            cur_seq.append(line.rstrip())
    flush()
print(f"Wrote {n} reference seqs to {OUT}")
