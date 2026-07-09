#!/usr/bin/env python3
"""
PASS-2 re-pass for Fluit et al. 2021 (BVBRC-02-Ralstonia).

For each of the 18 assembled genomes:
  - Extract the best-hit 16S rRNA gene region (blastn vs R. pickettii type-strain 16S)
  - Extract the best-hit OXA-22 family protein (tblastn vs OXA-22 reference)
  - Extract the best-hit OXA-60 family protein (tblastn vs OXA-60 reference)

Then build maximum-likelihood trees (FastTree) for each, and report tree-length /
topology / per-strain group consistency vs the published group assignments.
"""
from __future__ import annotations
import os, sys, subprocess, json, shutil, tempfile, pathlib, re
from collections import OrderedDict

ROOT = pathlib.Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-02-Ralstonia-Fluit2021")
GENOMES = sorted((ROOT/"data/genomes").glob("*.fasta"))
REFS = ROOT/"data/refs"
OUT = ROOT/"results/repass"
OUT.mkdir(parents=True, exist_ok=True)

# Paper-published group assignments (from paper_notes.md, verified against paper.txt)
GROUPS = {
    "551634": "E2", "551636": "E2", "543514": "E2", "551632": "E2", "551637": "E2",
    "543504": "E1", "551631": "E1", "551635": "E1",
    "535633": "D2", "535634": "D2", "535635": "D2", "545260": "D2", "545261": "D2", "535632": "D2",
    "535638": "D1", "543498": "D1",
    "551633": "G",
    "535637": "F",
}

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)

def revcomp(s):
    t = str.maketrans("ACGTacgtNn", "TGCAtgcaNn")
    return s.translate(t)[::-1]

def read_fasta(path):
    """Return ordered dict id->seq."""
    out = OrderedDict()
    name, buf = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip()
            if not line: continue
            if line.startswith(">"):
                if name: out[name] = "".join(buf)
                name = line[1:].split()[0]
                buf = []
            else:
                buf.append(line)
    if name: out[name] = "".join(buf)
    return out

def extract_region(genome_fa, contig_id, start, end, strand):
    """1-based inclusive coordinates; strand 'plus' or 'minus'."""
    seqs = read_fasta(genome_fa)
    s = seqs[contig_id]
    a, b = sorted((start, end))
    region = s[a-1:b]
    if strand == "minus":
        region = revcomp(region)
    return region

def blastn_best(query_fa, subject_fa, min_pid=80.0, min_len=400):
    """Run blastn and return best hit dict (or None)."""
    cmd = [
        "blastn","-query",query_fa,"-subject",subject_fa,
        "-outfmt","6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sstrand",
        "-perc_identity",str(min_pid),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip(): return None
    best = None
    for line in r.stdout.strip().splitlines():
        f = line.split("\t")
        length = int(f[3]); bit = float(f[11])
        if length < min_len: continue
        if best is None or bit > best["bitscore"]:
            best = dict(
                qseqid=f[0], sseqid=f[1], pident=float(f[2]), length=length,
                qstart=int(f[6]), qend=int(f[7]),
                sstart=int(f[8]), send=int(f[9]),
                bitscore=bit, sstrand=f[12],
            )
    return best

def tblastn_best(query_faa, subject_fa, min_pid=70.0, min_len=150):
    """Return best tblastn hit dict."""
    cmd = [
        "tblastn","-query",query_faa,"-subject",subject_fa,
        "-outfmt","6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sframe",
        "-evalue","1e-30",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip(): return None
    best = None
    for line in r.stdout.strip().splitlines():
        f = line.split("\t")
        pid = float(f[2]); length=int(f[3]); bit=float(f[11])
        if pid < min_pid or length < min_len: continue
        if best is None or bit > best["bitscore"]:
            best = dict(
                qseqid=f[0], sseqid=f[1], pident=pid, length=length,
                qstart=int(f[6]), qend=int(f[7]),
                sstart=int(f[8]), send=int(f[9]),
                bitscore=bit, sframe=int(f[12]),
            )
    return best

def extract_nuc_from_tblastn(genome_fa, hit):
    """Given a tblastn hit, pull the underlying nucleotide region and translate."""
    strand = "plus" if hit["sstart"] < hit["send"] else "minus"
    seq = extract_region(genome_fa, hit["sseqid"], hit["sstart"], hit["send"], strand)
    return seq

def translate(nt):
    table = {
        'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L',
        'ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V',
        'TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P',
        'ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A',
        'TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q',
        'AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E',
        'TGT':'C','TGC':'C','TGA':'*','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R',
        'AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G',
    }
    out = []
    for i in range(0, len(nt)-2, 3):
        codon = nt[i:i+3].upper()
        out.append(table.get(codon,'X'))
    return "".join(out).rstrip('*')

def main():
    summary = {"16S":[], "OXA22":[], "OXA60":[]}
    s16_records = OrderedDict()
    oxa22_records = OrderedDict()
    oxa60_records = OrderedDict()

    ref16s = REFS/"Rpickettii_16S.fna"
    refoxa22 = REFS/"OXA-22.faa"
    refoxa60 = REFS/"OXA-60.faa"

    for g in GENOMES:
        sid = g.stem  # e.g. 535632
        grp = GROUPS.get(sid, "?")
        label = f"{sid}_{grp}"
        # 16S extraction: blastn 16S ref vs genome
        hit = blastn_best(str(ref16s), str(g), min_pid=90, min_len=1000)
        if hit:
            seq = extract_region(str(g), hit["sseqid"], hit["sstart"], hit["send"], hit["sstrand"])
            s16_records[label] = seq
            summary["16S"].append({"strain":sid, "group":grp, "pident":hit["pident"], "length":hit["length"], "contig":hit["sseqid"]})
        else:
            summary["16S"].append({"strain":sid, "group":grp, "missing":True})

        # OXA-22 extraction via tblastn
        h22 = tblastn_best(str(refoxa22), str(g), min_pid=70, min_len=150)
        if h22:
            nt = extract_nuc_from_tblastn(str(g), h22)
            aa = translate(nt)
            oxa22_records[label] = aa
            summary["OXA22"].append({"strain":sid, "group":grp, "pident":h22["pident"], "length":h22["length"], "aa_len":len(aa)})
        else:
            summary["OXA22"].append({"strain":sid, "group":grp, "missing":True})

        # OXA-60 extraction via tblastn
        h60 = tblastn_best(str(refoxa60), str(g), min_pid=70, min_len=150)
        if h60:
            nt = extract_nuc_from_tblastn(str(g), h60)
            aa = translate(nt)
            oxa60_records[label] = aa
            summary["OXA60"].append({"strain":sid, "group":grp, "pident":h60["pident"], "length":h60["length"], "aa_len":len(aa)})
        else:
            summary["OXA60"].append({"strain":sid, "group":grp, "missing":True})

        print(f"  {sid}({grp}): 16S {'OK' if hit else 'NO'} ({hit['length'] if hit else 0}bp), "
              f"OXA22 {'OK' if h22 else 'NO'} ({h22['length'] if h22 else 0}aa, {h22['pident'] if h22 else 0:.1f}%), "
              f"OXA60 {'OK' if h60 else 'NO'} ({h60['length'] if h60 else 0}aa, {h60['pident'] if h60 else 0:.1f}%)", flush=True)

    # Write FASTAs
    for name, recs in (("16S", s16_records), ("OXA22", oxa22_records), ("OXA60", oxa60_records)):
        outfa = OUT/f"{name}.fasta"
        with open(outfa,"w") as fh:
            for k,v in recs.items():
                fh.write(f">{k}\n{v}\n")
        print(f"Wrote {outfa} ({len(recs)} seqs)")

    with open(OUT/"extract_summary.json","w") as fh:
        json.dump(summary, fh, indent=2)

if __name__ == "__main__":
    main()
