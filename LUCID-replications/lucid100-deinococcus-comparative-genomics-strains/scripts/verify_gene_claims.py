#!/usr/bin/env python3
"""
verify_gene_claims.py — spot-check named-gene length claims from the paper
against actual GenBank annotations for both BAA-816 (RefSeq) and ATCC 13939K
(this paper's GenBank entries CP150840-CP150843).

Free public data only. CPU only. ~1s runtime.

Outputs:
  artifacts/gene_claims/results.json
  artifacts/gene_claims/results.tsv
  artifacts/gene_claims/print summary to stdout
"""

import json, sys, os, re
from pathlib import Path
from Bio import SeqIO

ROOT = Path(__file__).resolve().parent.parent
GB = ROOT / 'artifacts' / 'genbank'
OUT = ROOT / 'artifacts' / 'gene_claims'
OUT.mkdir(exist_ok=True)

# Paper-claimed numbers (Section 2.3.x of Jeong et al., 2024)
# (locus_tag, gene_symbol, expected_aa, source_strain, paper_section, note)
CLAIMS = [
    # BAA-816 side (NC_001263.1, locus tags DR_*)
    ('DR_0001', 'DnaN', 393, 'BAA-816',  '2.3.1', 'paper: 393 aa per AE000513.1 annotation; omitted in NC_001263.1'),
    ('DR_0099', 'SSB',  143, 'BAA-816',  '2.3.1', 'paper: 143 aa truncated form in BAA-816'),
    ('DR_0997', 'DdrI', 260, 'BAA-816',  '2.3.3', 'paper: 260-aa CRP in BAA-816'),
    ('DR_2418', 'DrRRA', 373, 'BAA-816', '2.3.6', 'paper: 373 aa DrRRA in BAA-816'),
    ('DR_2410', 'DnaX',  None, 'BAA-816','2.3.1', 'paper: gene split in BAA-816, merged in 13939K'),
    ('DR_1647', 'BshC',  None, 'BAA-816','2.3.2', 'paper: pseudogene in BAA-816 (no CDS or short fragment)'),
    ('DR_1417', 'PBP1b/mrcB', 1009, 'BAA-816', '2.3.5', 'paper: 1009 aa PBP1b in BAA-816'),

    # ATCC 13939K side (CP150840-CP150843, locus tags KDR_*)
    ('KDR_0001', 'DnaN',  361, '13939K', '2.3.1', 'paper: 361 aa β-clamp, 1086 nt CDS'),
    ('KDR_0002', 'DnaA',  454, '13939K', '2.3',   'paper: 454 aa DnaA in 13939K vs 466 aa in 13939E/O'),
    ('KDR_0997', 'DdrI',  203, '13939K', '2.3.3', 'paper: 203 aa truncated DdrI'),
    ('KDR_1647', 'BshC',  520, '13939K', '2.3.2', 'paper: 520 aa BshC, extra C at position 954'),
    ('KDR_2418', 'DrRRA', 221, '13939K', '2.3.6', 'paper: 221 aa shortened DrRRA'),
    ('KDR_2410m','DnaX',  786, '13939K', '2.3.1', 'paper: 786 aa DnaX (fused DR_2410+DR_2411)'),
]

# Map BAA-816 -> RefSeq accession (one file per replicon)
BAA816_FILES = ['NC_001263.1.gb', 'NC_001264.1.gb', 'NC_000958.1.gb', 'NC_000959.1.gb']
ATCC_FILES   = ['CP150840.1.gb',  'CP150841.1.gb',  'CP150842.1.gb',  'CP150843.1.gb']


def index_features(files, expected_prefix=None):
    """Return dict: { (locus_tag or old_locus_tag) : list of feature dicts }
       Includes 'CDS' and 'gene' features."""
    idx = {}
    for f in files:
        rec = SeqIO.read(GB / f, 'genbank')
        for feat in rec.features:
            if feat.type not in ('CDS', 'gene'):
                continue
            q = feat.qualifiers
            lts = []
            for key in ('locus_tag', 'old_locus_tag'):
                for v in q.get(key, []):
                    lts.append(v)
            if not lts:
                continue
            entry = {
                'replicon': rec.id,
                'type': feat.type,
                'location': str(feat.location),
                'start': int(feat.location.start),
                'end': int(feat.location.end),
                'strand': feat.location.strand,
                'gene': q.get('gene', [''])[0],
                'product': q.get('product', [''])[0],
                'pseudo': 'pseudo' in q or 'pseudogene' in q,
                'translation': q.get('translation', [''])[0],
                'protein_id': q.get('protein_id', [''])[0],
                'locus_tags': lts,
            }
            if feat.type == 'CDS' and entry['translation']:
                entry['aa_len'] = len(entry['translation'])
            elif feat.type == 'CDS':
                entry['aa_len'] = None  # pseudo CDS often has no translation
            else:
                entry['aa_len'] = None
            entry['nt_len'] = entry['end'] - entry['start']
            for lt in lts:
                idx.setdefault(lt, []).append(entry)
    return idx


def find_feature(idx, locus_tag):
    """Return best matching CDS feature for a locus_tag."""
    # Direct hit
    hits = idx.get(locus_tag, [])
    if not hits:
        return None
    # Prefer CDS over gene
    cds = [h for h in hits if h['type'] == 'CDS']
    if cds:
        return cds[0]
    return hits[0]


def main():
    print('Indexing BAA-816 RefSeq features...')
    baa = index_features(BAA816_FILES)
    print(f'  {len(baa)} locus tags indexed (BAA-816)')
    print('Indexing ATCC 13939K features...')
    atcc = index_features(ATCC_FILES)
    print(f'  {len(atcc)} locus tags indexed (13939K)')

    results = []
    for lt, sym, expected, strain, section, note in CLAIMS:
        idx = baa if strain == 'BAA-816' else atcc
        feat = find_feature(idx, lt)
        row = {
            'locus_tag': lt,
            'gene_symbol': sym,
            'strain': strain,
            'paper_section': section,
            'paper_expected_aa': expected,
            'paper_note': note,
        }
        if feat is None:
            row['status'] = 'NOT_FOUND'
            row['observed_aa'] = None
            row['observed_nt'] = None
            row['observed_pseudo'] = None
            row['observed_product'] = None
            row['verdict'] = 'MISSING_IN_GENBANK'
            row['delta_aa'] = None
        else:
            row['status'] = 'FOUND'
            row['observed_aa'] = feat['aa_len']
            row['observed_nt'] = feat['nt_len']
            row['observed_pseudo'] = feat['pseudo']
            row['observed_product'] = feat['product']
            row['observed_replicon'] = feat['replicon']
            row['observed_gene'] = feat['gene']
            if expected is None:
                # No numeric expectation; just record what's there
                if 'pseudo' in note.lower() and feat['pseudo']:
                    row['verdict'] = 'AGREES (pseudogene as paper claims)'
                elif feat['pseudo']:
                    row['verdict'] = f'PSEUDOGENE (paper note: {note})'
                else:
                    row['verdict'] = f'CDS present, aa={feat["aa_len"]}, see note'
                row['delta_aa'] = None
            else:
                obs = feat['aa_len']
                if obs is None:
                    if feat['pseudo']:
                        row['verdict'] = f'PSEUDOGENE in GenBank (no translation); paper expects {expected} aa'
                    else:
                        row['verdict'] = f'NO_TRANSLATION (paper expects {expected} aa)'
                    row['delta_aa'] = None
                else:
                    delta = obs - expected
                    row['delta_aa'] = delta
                    if delta == 0:
                        row['verdict'] = f'EXACT_MATCH ({obs} aa)'
                    elif abs(delta) <= 2:
                        row['verdict'] = f'AGREES_WITHIN_2aa (obs={obs}, expected={expected}, Δ={delta:+d})'
                    elif abs(delta) <= 5:
                        row['verdict'] = f'AGREES_WITHIN_5aa (obs={obs}, expected={expected}, Δ={delta:+d})'
                    else:
                        row['verdict'] = f'DISAGREES (obs={obs}, expected={expected}, Δ={delta:+d})'
        results.append(row)

    # Write JSON
    out_json = OUT / 'results.json'
    with open(out_json, 'w') as fh:
        json.dump({
            'description': 'Spot-check of named-gene length claims in Jeong et al. 2024 (DOI 10.3389/fmicb.2024.1410024)',
            'method': 'Parse GenBank CDS features from NCBI eutils-fetched records; compare translation aa length to paper-stated values.',
            'data_source': 'NCBI nuccore via eutils efetch (free, public).',
            'results': results,
        }, fh, indent=2)

    # Write TSV
    out_tsv = OUT / 'results.tsv'
    cols = ['strain','locus_tag','gene_symbol','paper_section','paper_expected_aa',
            'observed_aa','delta_aa','observed_pseudo','observed_product','verdict']
    with open(out_tsv, 'w') as fh:
        fh.write('\t'.join(cols) + '\n')
        for r in results:
            fh.write('\t'.join(str(r.get(c, '')) for c in cols) + '\n')

    # Pretty print
    print('\n=== Gene-claim spot check ===')
    print(f"{'strain':<8} {'locus_tag':<12} {'gene':<14} {'paper_aa':>8} {'obs_aa':>7} {'Δ':>5}  verdict")
    print('-' * 110)
    for r in results:
        paa = r['paper_expected_aa']
        oaa = r['observed_aa']
        d   = r['delta_aa']
        print(f"{r['strain']:<8} {r['locus_tag']:<12} {r['gene_symbol']:<14} "
              f"{str(paa if paa is not None else '-'):>8} "
              f"{str(oaa if oaa is not None else '-'):>7} "
              f"{(f'{d:+d}' if d is not None else '-'):>5}  {r['verdict']}")
    # Summary
    n = len(results)
    exact = sum(1 for r in results if 'EXACT' in (r['verdict'] or ''))
    near  = sum(1 for r in results if 'AGREES' in (r['verdict'] or '') and 'EXACT' not in r['verdict'])
    disagree = sum(1 for r in results if 'DISAGREES' in (r['verdict'] or ''))
    print(f"\nTotals: {exact} EXACT, {near} AGREES_NEAR, {disagree} DISAGREE, {n - exact - near - disagree} OTHER")
    print(f"\nWrote: {out_json}")
    print(f"Wrote: {out_tsv}")


if __name__ == '__main__':
    main()
