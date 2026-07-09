#!/usr/bin/env python3
"""Independent genome stats for BVBRC-85 replication check.
Compute genome size, GC%, contig count, N50, largest contig for a FASTA.
Written from scratch 2026-07-03 — no imports from the original replication code.
"""
from __future__ import annotations
import sys, json, hashlib, argparse

def parse_fasta(path):
    """Yield (header, seq_str) from a FASTA file, without external libs."""
    header, chunks = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            if line[0] == '>':
                if header is not None:
                    yield header, ''.join(chunks)
                header = line[1:].split()[0]
                chunks = []
            else:
                chunks.append(line.upper())
        if header is not None:
            yield header, ''.join(chunks)

def stats(path):
    lengths = []
    gc = 0
    at = 0
    other = 0
    for _, seq in parse_fasta(path):
        lengths.append(len(seq))
        for b in seq:
            if b in 'GC':
                gc += 1
            elif b in 'AT':
                at += 1
            else:
                other += 1
    total = sum(lengths)
    lengths_sorted = sorted(lengths, reverse=True)
    # N50: smallest contig at cumulative 50%
    cum = 0
    n50 = None
    for L in lengths_sorted:
        cum += L
        if cum >= total / 2:
            n50 = L
            break
    md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
    return {
        'file': path,
        'md5': md5,
        'contigs': len(lengths),
        'total_bp': total,
        'largest_contig': lengths_sorted[0] if lengths_sorted else 0,
        'smallest_contig': lengths_sorted[-1] if lengths_sorted else 0,
        'n50': n50,
        'gc_bases': gc,
        'at_bases': at,
        'other_bases': other,
        'gc_percent': round(100.0 * gc / (gc + at), 4) if (gc+at) else 0.0,
        'gc_percent_incl_ambig': round(100.0 * gc / total, 4) if total else 0.0,
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('fasta', nargs='+')
    args = ap.parse_args()
    out = {p: stats(p) for p in args.fasta}
    print(json.dumps(out, indent=2))
