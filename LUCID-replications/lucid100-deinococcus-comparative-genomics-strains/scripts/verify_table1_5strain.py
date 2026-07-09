#!/usr/bin/env python3
"""
verify_table1_5strain.py — Verify Table 1 of Jeong et al. 2024:
genome sizes of 5 D. radiodurans R1 strains.

Free public NCBI data only.
"""
import json
from pathlib import Path
from Bio import SeqIO

ROOT = Path(__file__).resolve().parent.parent
F4 = ROOT / 'artifacts' / 'genomes'
F12 = ROOT / 'artifacts' / 'genomes_5strain'
OUT = ROOT / 'artifacts' / 'table1'
OUT.mkdir(exist_ok=True)

# (strain, replicon, accession, file_dir, paper_size_bp)
TABLE1 = [
    ('ATCC 13939K', 'chr1', 'CP150840.1', F4,  2650014),
    ('ATCC 13939K', 'chr2', 'CP150841.1', F4,  412190),
    ('ATCC 13939K', 'pMP',  'CP150842.1', F4,  177364),
    ('ATCC 13939K', 'pCP',  'CP150843.1', F4,  45503),
    ('ATCC BAA-816','chr1', 'NC_001263.1',F4,  2648638),
    ('ATCC BAA-816','chr2', 'NC_001264.1',F4,  412348),
    ('ATCC BAA-816','pMP',  'NC_000958.1',F4,  177466),
    ('ATCC BAA-816','pCP',  'NC_000959.1',F4,  45704),
    ('R1-2016',     'chr1', 'CP015081.1', F12, 2646742),
    ('R1-2016',     'chr2', 'CP015082.1', F12, 433133),
    ('R1-2016',     'pMP',  'CP015083.1', F12, 203183),
    ('R1-2016',     'pCP',  'CP015084.1', F12, 61707),
    ('ATCC 13939E', 'chr1', 'CP038663.1', F12, 2644543),
    ('ATCC 13939E', 'chr2', 'CP038664.1', F12, 412189),
    ('ATCC 13939E', 'pMP',  'CP038665.1', F12, 177363),
    ('ATCC 13939E', 'pCP',  'CP038666.1', F12, 45503),
    ('ATCC 13939O', 'chr1', 'CP068791.1', F12, 2644251),
    ('ATCC 13939O', 'chr2', 'CP068792.1', F12, 412138),
    ('ATCC 13939O', 'pMP',  'CP068793.1', F12, 177322),
    ('ATCC 13939O', 'pCP',  'CP068794.1', F12, 45508),
]

results = []
strain_totals_paper = {
    'ATCC 13939K': 3285071, 'ATCC BAA-816': 3284156,
    'R1-2016':     3344765, 'ATCC 13939E':  3279598, 'ATCC 13939O': 3279219,
}
strain_totals_obs = {}

for strain, replicon, acc, fdir, paper_bp in TABLE1:
    rec = next(SeqIO.parse(fdir / f'{acc}.fa', 'fasta'))
    L = len(rec.seq)
    d = L - paper_bp
    results.append({
        'strain': strain, 'replicon': replicon, 'accession': acc,
        'paper_size_bp': paper_bp, 'observed_size_bp': L,
        'delta_bp': d,
        'verdict': 'EXACT' if d == 0 else ('AGREES_WITHIN_2bp' if abs(d) <= 2 else f'DIFFERS_BY_{d:+d}_bp'),
    })
    strain_totals_obs[strain] = strain_totals_obs.get(strain, 0) + L

print(f"{'Strain':<15} {'Replicon':<6} {'Accession':<14} {'Paper bp':>11} {'Obs bp':>11} {'Δ':>5}  Verdict")
print('-' * 90)
for r in results:
    print(f"{r['strain']:<15} {r['replicon']:<6} {r['accession']:<14} "
          f"{r['paper_size_bp']:>11} {r['observed_size_bp']:>11} {r['delta_bp']:>+5}  {r['verdict']}")

print()
print(f"{'Strain':<15} {'Paper total':>12} {'Obs total':>12} {'Δ':>5}  Verdict")
print('-' * 60)
total_results = []
for strain, paper_total in strain_totals_paper.items():
    obs = strain_totals_obs[strain]
    d = obs - paper_total
    v = 'EXACT' if d == 0 else (f'Δ={d:+d}')
    total_results.append({'strain': strain, 'paper_total': paper_total, 'observed_total': obs, 'delta': d, 'verdict': v})
    print(f"{strain:<15} {paper_total:>12,} {obs:>12,} {d:>+5}  {v}")

# Summary metrics
exact = sum(1 for r in results if r['verdict'] == 'EXACT')
total = len(results)
print(f"\nReplicons matching exactly: {exact}/{total}")

out = {
    'paper': 'Jeong et al. 2024 Table 1',
    'replicon_level': results,
    'strain_totals': total_results,
    'summary': {
        'replicons_exact_match': exact,
        'replicons_total': total,
        'all_strain_totals_match': all(r['verdict'] == 'EXACT' for r in total_results),
    }
}
with open(OUT / 'verification.json', 'w') as fh:
    json.dump(out, fh, indent=2)
# Markdown table
with open(OUT / 'table1.md', 'w') as fh:
    fh.write('# Table 1 verification (5-strain genome sizes)\n\n')
    fh.write('## Per-replicon\n\n')
    fh.write('| Strain | Replicon | Accession | Paper bp | Observed bp | Δ | Verdict |\n')
    fh.write('|---|---|---|---:|---:|---:|---|\n')
    for r in results:
        fh.write(f"| {r['strain']} | {r['replicon']} | {r['accession']} | {r['paper_size_bp']:,} | {r['observed_size_bp']:,} | {r['delta_bp']:+d} | {r['verdict']} |\n")
    fh.write('\n## Strain totals\n\n')
    fh.write('| Strain | Paper total | Observed total | Δ | Verdict |\n')
    fh.write('|---|---:|---:|---:|---|\n')
    for r in total_results:
        fh.write(f"| {r['strain']} | {r['paper_total']:,} | {r['observed_total']:,} | {r['delta']:+d} | {r['verdict']} |\n")

print(f"\nWrote: {OUT/'verification.json'}")
print(f"Wrote: {OUT/'table1.md'}")
