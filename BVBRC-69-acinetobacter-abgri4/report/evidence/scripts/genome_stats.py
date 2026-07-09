#!/usr/bin/env python3
"""Genome stats for the 4 Chan 2020 A. baumannii isolates."""
from Bio import SeqIO
import glob, os, json

STRAINS = ['ABUH763', 'ABUH773', 'ABUH793', 'ABUH796']
BASE = '/data/stevens/bvbrc69-abgri4/genomes'
stats = {}
for s in STRAINS:
    stats[s] = {'replicons': []}
    tot = 0
    gc_tot = 0
    for f in sorted(glob.glob(os.path.join(BASE, s, '*.fna'))):
        if '_all' in f:
            continue
        for r in SeqIO.parse(f, 'fasta'):
            L = len(r.seq)
            gc = (r.seq.count('G') + r.seq.count('C') + r.seq.count('g') + r.seq.count('c'))
            stats[s]['replicons'].append({
                'file': os.path.basename(f),
                'accession': r.id,
                'length': L,
                'gc_pct': round(100 * gc / L, 2),
                'description': r.description,
            })
            tot += L
            gc_tot += gc
    stats[s]['total_length'] = tot
    stats[s]['overall_gc_pct'] = round(100 * gc_tot / tot, 2) if tot else 0
    stats[s]['n_replicons'] = len(stats[s]['replicons'])

print(json.dumps(stats, indent=2))
with open('/data/stevens/bvbrc69-abgri4/evidence/genome_stats.json', 'w') as fh:
    json.dump(stats, fh, indent=2)
print('\n=== SUMMARY ===')
print(f"{'Strain':10s} {'Repls':>5s} {'Total bp':>12s} {'GC%':>6s}")
for s, d in stats.items():
    print(f"{s:10s} {d['n_replicons']:>5d} {d['total_length']:>12,d} {d['overall_gc_pct']:>6.2f}")
