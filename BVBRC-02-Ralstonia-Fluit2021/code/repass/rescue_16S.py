#!/usr/bin/env python3
"""Rescue partial 16S extractions: stitch the best two non-overlapping fragments
   per genome if a single hit >=1000 bp is not found."""
from __future__ import annotations
import subprocess, pathlib, sys
from collections import OrderedDict

ROOT = pathlib.Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021")
GENOMES = sorted((ROOT/"data/genomes").glob("*.fasta"))
REF = ROOT/"data/refs/Rpickettii_16S.fna"
OUT = ROOT/"results/repass"
EXISTING = OUT/"16S.fasta"

GROUPS = {
    "551634": "E2", "551636": "E2", "543514": "E2", "551632": "E2", "551637": "E2",
    "543504": "E1", "551631": "E1", "551635": "E1",
    "535633": "D2", "535634": "D2", "535635": "D2", "545260": "D2", "545261": "D2", "535632": "D2",
    "535638": "D1", "543498": "D1",
    "551633": "G",
    "535637": "F",
}

def revcomp(s):
    t = str.maketrans("ACGTacgtNn","TGCAtgcaNn"); return s.translate(t)[::-1]

def read_fasta(path):
    out=OrderedDict(); name,buf=None,[]
    with open(path) as fh:
        for ln in fh:
            ln=ln.rstrip()
            if not ln: continue
            if ln.startswith(">"):
                if name: out[name]="".join(buf)
                name=ln[1:].split()[0]; buf=[]
            else: buf.append(ln)
    if name: out[name]="".join(buf)
    return out

def best_blastn_hits(query,subject,min_pid=90,min_len=400):
    r = subprocess.run(["blastn","-query",query,"-subject",subject,
                       "-outfmt","6 qseqid sseqid pident length qstart qend sstart send bitscore sstrand",
                       "-perc_identity",str(min_pid)], capture_output=True, text=True)
    hits=[]
    for ln in r.stdout.strip().splitlines():
        f=ln.split("\t")
        if int(f[3]) < min_len: continue
        hits.append(dict(sseqid=f[1], pident=float(f[2]), length=int(f[3]),
                         qstart=int(f[4]), qend=int(f[5]),
                         sstart=int(f[6]), send=int(f[7]),
                         bitscore=float(f[8]), sstrand=f[9]))
    return sorted(hits, key=lambda x: -x["bitscore"])

def extract(genome_fa, contig, s, e, strand):
    seqs = read_fasta(genome_fa); seq = seqs[contig]
    a,b = sorted((s,e)); region = seq[a-1:b]
    if strand == "minus": region = revcomp(region)
    return region

# Find which strains are missing from current 16S fasta
have = set()
for ln in open(EXISTING):
    if ln.startswith(">"): have.add(ln[1:].split("_")[0])

missing = []
for g in GENOMES:
    sid = g.stem
    if sid not in have: missing.append(g)

print(f"Missing 16S: {[m.stem for m in missing]}")

# For each missing one, look at all blastn hits and stitch
recovered = {}
for g in missing:
    sid = g.stem; grp = GROUPS[sid]
    hits = best_blastn_hits(str(REF), str(g), min_pid=90, min_len=200)
    print(f"\n{sid} ({grp}): {len(hits)} hits")
    for h in hits[:5]:
        print(f"  q{h['qstart']}-{h['qend']} -> {h['sseqid']} pid={h['pident']:.1f} len={h['length']} strand={h['sstrand']}")
    # Try to stitch: take hits sorted by qstart, fill query positions 1..end of ref
    # Order hits by qstart
    if not hits: continue
    by_qstart = sorted(hits, key=lambda x: x["qstart"])
    # greedy: pick highest-bitscore hit first; then add any non-overlapping in query coords
    chosen = []
    used_q = []
    for h in hits:
        q_lo, q_hi = sorted((h["qstart"], h["qend"]))
        overlap = any(not (q_hi < lo or q_lo > hi) for lo, hi in used_q)
        if overlap: continue
        chosen.append(h); used_q.append((q_lo, q_hi))
    chosen = sorted(chosen, key=lambda h: min(h["qstart"], h["qend"]))
    pieces = []
    total_qcov = 0
    for h in chosen:
        seq = extract(str(g), h["sseqid"], h["sstart"], h["send"], h["sstrand"])
        pieces.append(seq)
        total_qcov += abs(h["qend"] - h["qstart"]) + 1
    stitched = "".join(pieces)
    print(f"  stitched: {len(chosen)} pieces, {len(stitched)} bp, qcov={total_qcov}")
    recovered[f"{sid}_{grp}"] = stitched

# Append to existing fasta
with open(EXISTING, "a") as fh:
    for k, v in recovered.items():
        fh.write(f">{k}\n{v}\n")
print(f"\nAppended {len(recovered)} rescued sequences to {EXISTING}")
