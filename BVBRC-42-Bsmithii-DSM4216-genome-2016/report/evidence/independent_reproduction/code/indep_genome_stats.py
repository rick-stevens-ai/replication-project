#!/usr/bin/env python3
"""
Independent reproduction of B. smithii DSM 4216 genome stats.

Written fresh 2026-07-03 for the reproduction audit — does NOT read the
original replication's genome_stats.py. Uses only stdlib.

Inputs:
  --fna  genome FASTA (GCA or GCF)
  --gff  annotation GFF3 (matching the FASTA)
Output: JSON with per-replicon length + GC + feature counts.
"""
import argparse
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

def parse_fasta(path):
    """Yield (seqid, sequence_upper) tuples from a FASTA file."""
    seqid, buf = None, []
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith(">"):
                if seqid is not None:
                    yield seqid, "".join(buf).upper()
                # SeqID is the token after ">" up to first whitespace
                seqid = line[1:].split()[0]
                buf = []
            else:
                buf.append(line)
        if seqid is not None:
            yield seqid, "".join(buf).upper()

def gc_and_len(seq):
    n = len(seq)
    gc = seq.count("G") + seq.count("C")
    at = seq.count("A") + seq.count("T")
    n_amb = n - (gc + at)
    return n, gc, at, n_amb

def parse_gff_features(path):
    """
    Return dict: seqid -> list of (feat_type, start, end, attrs_dict).
    Also return global counter of feature types.
    """
    features_by_seq = defaultdict(list)
    ftype_counter = Counter()
    with open(path) as f:
        for line in f:
            if not line or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9:
                continue
            seqid, source, ftype, start, end, score, strand, phase, attrs = parts
            try:
                start_i = int(start)
                end_i = int(end)
            except ValueError:
                continue
            attr_dict = {}
            for kv in attrs.split(";"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    attr_dict[k.strip()] = v.strip()
            features_by_seq[seqid].append((ftype, start_i, end_i, attr_dict))
            ftype_counter[ftype] += 1
    return features_by_seq, ftype_counter

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fna", required=True)
    ap.add_argument("--gff", required=True)
    ap.add_argument("--label", default="genome")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # --- Genome FASTA ---
    replicons = []
    total_len = 0
    total_gc = 0
    total_at = 0
    total_amb = 0
    for seqid, seq in parse_fasta(args.fna):
        n, gc, at, amb = gc_and_len(seq)
        replicons.append({
            "seqid": seqid,
            "length_bp": n,
            "gc_bp": gc,
            "at_bp": at,
            "ambig_bp": amb,
            "gc_pct_over_len": round(100.0 * gc / n, 4) if n else None,
            "gc_pct_over_gc_at": round(100.0 * gc / (gc + at), 4) if (gc + at) else None,
        })
        total_len += n
        total_gc += gc
        total_at += at
        total_amb += amb

    genome_gc_over_len = round(100.0 * total_gc / total_len, 4) if total_len else None
    genome_gc_over_gcat = round(100.0 * total_gc / (total_gc + total_at), 4) if (total_gc + total_at) else None

    # --- GFF features ---
    feats_by_seq, ftype_counter = parse_gff_features(args.gff)

    # Feature counts (whole genome). NCBI GFF: CDS, gene, rRNA, tRNA, ncRNA, tmRNA, exon, region, pseudogene
    # rRNA operon count: count DISTINCT loci of 16S rRNAs (one 16S per operon in bacteria).
    # We approximate rRNA operons via 16S rRNA count (per-seqid).
    # Coding fraction: sum of |end-start+1| for CDS features / total_len
    cds_bp = 0
    cds_count = 0
    rRNA_count = 0
    tRNA_count = 0
    gene_count = 0
    pseudogene_count = 0
    rRNA_16S_count = 0
    for seqid, feats in feats_by_seq.items():
        for ftype, start, end, attrs in feats:
            if ftype == "CDS":
                cds_bp += (end - start + 1)
                cds_count += 1
            elif ftype == "rRNA":
                rRNA_count += 1
                # 16S detection: look at 'product' or 'Name' attribute
                prod = (attrs.get("product") or attrs.get("Name") or "").lower()
                if "16s" in prod or "s_rrna" in prod or "small subunit ribosomal" in prod:
                    rRNA_16S_count += 1
            elif ftype == "tRNA":
                tRNA_count += 1
            elif ftype == "gene":
                gene_count += 1
            elif ftype == "pseudogene":
                pseudogene_count += 1

    coding_fraction = round(100.0 * cds_bp / total_len, 4) if total_len else None

    out = {
        "label": args.label,
        "input_fna": str(args.fna),
        "input_gff": str(args.gff),
        "total_length_bp": total_len,
        "genome_gc_pct_over_len": genome_gc_over_len,
        "genome_gc_pct_over_gc_at": genome_gc_over_gcat,
        "n_replicons": len(replicons),
        "replicons": replicons,
        "coding_bp": cds_bp,
        "coding_fraction_pct": coding_fraction,
        "feature_counts": {
            "gene": gene_count,
            "CDS": cds_count,
            "rRNA": rRNA_count,
            "rRNA_16S_est": rRNA_16S_count,   # ≈ operon count
            "tRNA": tRNA_count,
            "pseudogene": pseudogene_count,
        },
        "ftype_counter_all": dict(ftype_counter),
    }
    Path(args.out).write_text(json.dumps(out, indent=2))
    # Also print a short summary
    print(json.dumps({
        "label": args.label,
        "total_length_bp": total_len,
        "gc_pct": genome_gc_over_len,
        "n_replicons": len(replicons),
        "replicon_lengths": [(r["seqid"], r["length_bp"]) for r in replicons],
        "CDS": cds_count,
        "rRNA": rRNA_count,
        "rRNA_16S_est_operons": rRNA_16S_count,
        "tRNA": tRNA_count,
        "gene": gene_count,
        "pseudogene": pseudogene_count,
        "coding_fraction_pct": coding_fraction,
    }, indent=2))

if __name__ == "__main__":
    main()
