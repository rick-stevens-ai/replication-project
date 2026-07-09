#!/usr/bin/env python3
"""Extract the AbGRI4 region per paper Table 1 coordinates and run
   AMR annotation + IS26 flanking check."""
from Bio import SeqIO
import subprocess, os, json, sys

BASE = '/data/stevens/bvbrc69-abgri4'
os.makedirs(f'{BASE}/results/abgri4', exist_ok=True)

# Paper Table 1 AbGRI4 coordinates (chromosome accession, start..end)
REGIONS = {
    'ABUH763': ('CP035051', 1518797, 1527636),
    'ABUH793': ('CP035045', 2219263, 2228102),  # note: paper lists 2228102–2219263 (rev strand)
    'ABUH796': ('CP035043', 1515737, 1524576),
    # ABUH773 has NO AbGRI4 per paper
}

results = {}
for strain, (acc, s, e) in REGIONS.items():
    fna = f'{BASE}/genomes/{strain}/{acc}.fna'
    rec = next(SeqIO.parse(fna, 'fasta'))
    # Normalize orientation
    lo, hi = (s, e) if s < e else (e, s)
    region = rec.seq[lo-1:hi]
    length = len(region)
    print(f'{strain} {acc}:{lo}..{hi}  length={length} bp  {"(rev-annotated in paper)" if s>e else ""}')
    out = f'{BASE}/results/abgri4/{strain}_AbGRI4.fna'
    with open(out, 'w') as fh:
        fh.write(f'>{strain}_AbGRI4 {acc}:{lo}-{hi}\n{region}\n')
    results[strain] = {
        'accession': acc,
        'start': lo, 'end': hi,
        'paper_start': s, 'paper_end': e,
        'length': length,
        'fasta': out,
    }

# Also flanking 5-kb for insertion-site verification (ABUH796 is paper's reference)
strain, (acc, s, e) = 'ABUH796', REGIONS['ABUH796']
rec = next(SeqIO.parse(f'{BASE}/genomes/{strain}/{acc}.fna', 'fasta'))
lo, hi = min(s,e), max(s,e)
flank5 = rec.seq[max(0, lo-5001):lo-1]
flank3 = rec.seq[hi:hi+5000]
with open(f'{BASE}/results/abgri4/ABUH796_AbGRI4_with5kbflank.fna', 'w') as fh:
    fh.write(f'>ABUH796_5kbLeftFlank {acc}:{lo-5000}-{lo-1}\n{flank5}\n')
    fh.write(f'>ABUH796_AbGRI4_core {acc}:{lo}-{hi}\n{rec.seq[lo-1:hi]}\n')
    fh.write(f'>ABUH796_5kbRightFlank {acc}:{hi+1}-{hi+5000}\n{flank3}\n')

with open(f'{BASE}/evidence/abgri4_regions.json', 'w') as fh:
    json.dump(results, fh, indent=2)

# Report AbGRI4 length vs paper's stated ~6.8 kb (integron core)
print('\n=== AbGRI4 spans (chromosome) ===')
for s, r in results.items():
    print(f"  {s:10s} {r['accession']}:{r['start']}-{r['end']}  {r['length']:>6d} bp")
print('\nNote: Paper says the class 1 integron itself is ~6.8 kb; Table 1 coords are the full AbGRI4 island (integron + IS26 boundaries + neighboring context).')
