#!/usr/bin/env python3
"""Independent S. aureus MLST caller.
Uses pubMLST S. aureus scheme allele FASTAs + profile table shipped with mlst v2.19.0.
Runs blastn of each locus against the target genome DB, requires 100% identity
+ 100% coverage of the allele length, then looks up the allelic profile in
the scheme table.
Written from scratch 2026-07-03 (no reuse of the original replication's MLST code)."""
import subprocess, sys, os, glob, csv, re

DB_DIR = "/usr/local/Cellar/mlst/2.19.0/libexec/db/pubmlst/saureus"
GENOME_DB = "results/SO1977_db"

LOCI = ["arcC", "aroE", "glpF", "gmk", "pta", "tpi", "yqiL"]

def allele_length(fa_path):
    """Return dict allele_name -> sequence length (all alleles in a locus fasta)."""
    lengths = {}
    cur, buf = None, []
    with open(fa_path) as fh:
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            if line[0] == '>':
                if cur is not None:
                    lengths[cur] = len(''.join(buf))
                cur = line[1:].split()[0]
                buf = []
            else:
                buf.append(line)
        if cur is not None:
            lengths[cur] = len(''.join(buf))
    return lengths

def call_locus(locus):
    fa = os.path.join(DB_DIR, f"{locus}.tfa")
    lens = allele_length(fa)
    # blastn each allele set against SO1977 db; want 100% id, 100% cov
    cmd = ["blastn", "-query", fa, "-db", GENOME_DB,
           "-outfmt", "6 qseqid sseqid pident length mismatch qstart qend sstart send evalue bitscore qlen",
           "-perc_identity", "100", "-dust", "no", "-word_size", "20"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    hits = []
    for line in res.stdout.splitlines():
        parts = line.split('\t')
        if len(parts) < 12: continue
        qid, sid, pident, length = parts[0], parts[1], float(parts[2]), int(parts[3])
        qlen = int(parts[11])
        if pident == 100.0 and length == qlen:
            # allele name format like "arcC_43"
            m = re.match(rf"^{locus}[_-](\d+)$", qid)
            allele_num = m.group(1) if m else qid
            hits.append((qid, allele_num, sid, parts[7], parts[8]))
    return hits

def load_profiles():
    """Return dict (arcC, aroE, glpF, gmk, pta, tpi, yqiL) -> ST."""
    prof = {}
    with open(os.path.join(DB_DIR, "saureus.txt")) as fh:
        rd = csv.reader(fh, delimiter='\t')
        header = next(rd)
        # find loci columns
        idx = {h: i for i, h in enumerate(header)}
        for row in rd:
            key = tuple(row[idx[l]] for l in LOCI)
            prof[key] = row[idx['ST']]
    return prof

def main():
    calls = {}
    for locus in LOCI:
        hits = call_locus(locus)
        if not hits:
            print(f"{locus}: NO 100/100 HIT")
            calls[locus] = None
        elif len(set(h[1] for h in hits)) == 1:
            calls[locus] = hits[0][1]
            print(f"{locus}: allele {hits[0][1]}  ({hits[0][2]}:{hits[0][3]}-{hits[0][4]})")
        else:
            print(f"{locus}: MULTIPLE alleles at 100/100: {[h[1] for h in hits]}")
            calls[locus] = hits[0][1]

    print()
    key = tuple(calls[l] for l in LOCI)
    print("Profile:", " ".join(f"{l}({calls[l]})" for l in LOCI))
    profiles = load_profiles()
    st = profiles.get(key)
    if st:
        print(f"MATCH: ST{st}")
    else:
        print("NO exact profile match in saureus.txt")
    # Save
    with open("results/mlst_independent_SO1977.txt", "w") as f:
        f.write("locus\tallele\n")
        for l in LOCI:
            f.write(f"{l}\t{calls[l]}\n")
        f.write(f"\nProfile\t{'-'.join(str(calls[l]) for l in LOCI)}\n")
        f.write(f"ST\t{st or 'NO_MATCH'}\n")

if __name__ == '__main__':
    main()
