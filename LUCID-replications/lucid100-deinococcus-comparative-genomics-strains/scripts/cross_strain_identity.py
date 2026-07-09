#!/usr/bin/env python3
"""
cross_strain_identity.py — Cross-strain pairwise nucleotide identity on chromosome 1
across all 5 D. radiodurans R1 strains in Jeong et al. 2024.

Implements a simple ANI-style calc via minimap2 asm5 alignment statistics
(matches / aligned bases). NOT real ANI (no Mash/skani/pyani), but a
defensible proxy that uses public sequence and CPU-only tools.

Paper claim (text only): 99.98% nucleotide identity between 13939K and BAA-816.
"""
import json, re
from pathlib import Path
from Bio import SeqIO
import mappy as mp

ROOT = Path(__file__).resolve().parent.parent
F4  = ROOT / 'artifacts' / 'genomes'
F12 = ROOT / 'artifacts' / 'genomes_5strain'
OUT = ROOT / 'artifacts' / 'cross_strain'
OUT.mkdir(exist_ok=True)

# chr1 only (largest replicon; representative)
STRAINS = [
    ('ATCC 13939K',  F4  / 'CP150840.1.fa'),
    ('ATCC BAA-816', F4  / 'NC_001263.1.fa'),
    ('R1-2016',      F12 / 'CP015081.1.fa'),
    ('ATCC 13939E',  F12 / 'CP038663.1.fa'),
    ('ATCC 13939O',  F12 / 'CP068791.1.fa'),
]

def load(p):
    rec = next(SeqIO.parse(p, 'fasta'))
    return str(rec.seq)

seqs = {name: load(p) for name, p in STRAINS}
print('Loaded chr1 of 5 strains:')
for name, s in seqs.items():
    print(f'  {name:<14}  {len(s):,} bp')

# Pairwise: align each strain's chr1 to each other strain's chr1
def ani_substitution(ref, qry):
    '''Substitution-only nucleotide identity (standard ANI definition).
    Excludes indel bases; counts matches / (matches + substitutions).'''
    a = mp.Aligner(seq=ref, preset='asm5')
    hits = [h for h in a.map(qry, cs=True) if h.is_primary]
    matches = subs = ins_bp = del_bp = 0
    aligned_ref_bp = 0
    for h in hits:
        aligned_ref_bp += h.r_en - h.r_st
        for m in re.finditer(r'(:\d+|\*[a-z]{2}|\+[a-z]+|-[a-z]+)', h.cs):
            tok = m.group(0)
            if tok.startswith(':'):
                matches += int(tok[1:])
            elif tok.startswith('*'):
                subs += 1
            elif tok.startswith('+'):
                ins_bp += len(tok) - 1
            elif tok.startswith('-'):
                del_bp += len(tok) - 1
    non_indel = matches + subs
    ani = (100.0 * matches / non_indel) if non_indel else 0.0
    return {
        'identity_pct': round(ani, 4),
        'matches': matches,
        'substitutions': subs,
        'qry_insertions_bp': ins_bp,
        'qry_deletions_bp': del_bp,
        'non_indel_aligned': non_indel,
        'coverage_ref_pct': round(100.0 * aligned_ref_bp / len(ref), 2) if ref else 0.0,
        'aligned_ref_bp': aligned_ref_bp,
    }

results = []
names = [n for n, _ in STRAINS]
matrix = {n: {} for n in names}
for ref_name in names:
    for qry_name in names:
        if qry_name == ref_name:
            matrix[ref_name][qry_name] = 100.0
            continue
        ani = ani_substitution(seqs[ref_name], seqs[qry_name])
        results.append({'ref': ref_name, 'qry': qry_name, **ani})
        matrix[ref_name][qry_name] = ani['identity_pct']

# Print matrix
print('\nPairwise chr1 nucleotide identity (%) — minimap2 asm5')
print('=' * 80)
hdr = '              ' + '  '.join(f'{n[:11]:>11}' for n in names)
print(hdr)
for r in names:
    row = f'{r[:13]:<13} ' + '  '.join(f'{matrix[r][q]:>11.4f}' for q in names)
    print(row)

# Headline claim: paper says 13939K vs BAA-816 = 99.98% nt identity
key = matrix['ATCC 13939K']['ATCC BAA-816']
print(f'\nPaper headline claim: 13939K vs BAA-816 chr1 identity = 99.98%')
print(f'Our chr1 calc:                                           {key:.4f}%')
delta = abs(key - 99.98)
if delta < 0.01:
    verdict = f'EXACT_MATCH ({key:.4f}% vs paper 99.98%)'
elif delta < 0.05:
    verdict = f'AGREES_WITHIN_0.05 ({key:.4f}% vs 99.98%, Δ={key-99.98:+.4f})'
else:
    verdict = f'DIFFERS ({key:.4f}% vs 99.98%, Δ={key-99.98:+.4f})'
print(f'Verdict: {verdict}')

out = {
    'paper': 'Jeong et al. 2024 — body text claim "99.98% nucleotide identity" (chr1 ATCC 13939K vs BAA-816)',
    'method': 'minimap2 asm5 via mappy; identity = matches / aligned_length (mlen/blen) summed over primary hits',
    'note': 'NOT canonical ANI (skani/pyani); proxy. Restricted to chr1 only for runtime.',
    'matrix': matrix,
    'pairs': results,
    'headline_check': {
        'paper_value_pct': 99.98,
        'observed_value_pct': key,
        'verdict': verdict,
    },
}
with open(OUT / 'cross_strain.json', 'w') as fh:
    json.dump(out, fh, indent=2)
print(f'\nWrote: {OUT / "cross_strain.json"}')
