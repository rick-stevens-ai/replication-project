#!/usr/bin/env python3
"""Extract 16S rRNA sequence from SO1977 FASTA using GFF annotations."""
from __future__ import annotations
import sys

def parse_fasta(path):
    header, chunks = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip()
            if not line: continue
            if line.startswith('>'):
                if header:
                    yield header, ''.join(chunks)
                header = line[1:].split()[0]
                chunks = []
            else:
                chunks.append(line)
        if header:
            yield header, ''.join(chunks)

def rc(s):
    comp = str.maketrans('ACGTNacgtn', 'TGCANtgcan')
    return s.translate(comp)[::-1]

def main():
    fasta = "downloads/SO1977/ncbi_dataset/data/GCA_002224825.1/GCA_002224825.1_ASM222482v1_genomic.fna"
    gff = "downloads/SO1977_gff/ncbi_dataset/data/GCA_002224825.1/genomic.gff"
    contigs = dict(parse_fasta(fasta))
    print(f"Loaded {len(contigs)} contigs")

    with open("results/SO1977_16S.fa", "w") as out:
        n = 0
        with open(gff) as gh:
            for line in gh:
                if line.startswith('#'): continue
                p = line.rstrip().split('\t')
                if len(p) < 9: continue
                if p[2] != 'rRNA': continue
                if '16S ribosomal RNA' not in p[8]: continue
                contig, start, end, strand = p[0], int(p[3]), int(p[4]), p[6]
                seq = contigs[contig][start-1:end]
                if strand == '-':
                    seq = rc(seq)
                n += 1
                out.write(f">16S_{n} {contig}:{start}-{end}({strand}) len={len(seq)}\n")
                for i in range(0, len(seq), 80):
                    out.write(seq[i:i+80] + '\n')
                print(f"16S #{n}: {contig}:{start}-{end}({strand}) len={len(seq)}")
        print(f"Extracted {n} 16S sequence(s)")

if __name__ == '__main__':
    main()
