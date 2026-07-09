#!/usr/bin/env python3
"""
predict_kdr_lengths.py — independently verify paper-claimed KDR_xxxx CDS lengths.

Strategy: CP150840-3 (ATCC 13939K) GenBank deposits have NO feature annotations,
so KDR_xxxx locus tags exist only in the unreleased Prokka annotation referenced
by Supplementary Tables S1-S5 (which are blocked, see manifest).

Workaround: use BAA-816 RefSeq (NC_001263.1) gene coordinates for the homologous
locus, align the BAA-816 region to the 13939K replicon via minimap2, lift the
coordinate over, then extract the 13939K subsequence, find the longest ORF on
the same strand that starts with a Met within the region, and report its length.

For pseudogenes in BAA-816 (DnaN, SSB, BshC, MutS, RecJ) the paper's claim is
that a small indel restores the ORF in 13939K. For the DnaX-style fusion we
extend the search region across the predicted merge.

This produces evidence INDEPENDENT of the unreleased Prokka annotation.
"""

import json, sys, re
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
import mappy as mp

ROOT = Path(__file__).resolve().parent.parent
GB = ROOT / 'artifacts' / 'genbank'
FA = ROOT / 'artifacts' / 'genomes'
OUT = ROOT / 'artifacts' / 'kdr_predict'
OUT.mkdir(exist_ok=True)

# Map of paper claims:
# old_tag -> (ref_replicon_acc, qry_replicon_acc, paper_kdr_label, paper_aa, paper_section, extend_bp, note)
CLAIMS = [
    ('DR_0001', 'NC_001263.1', 'CP150840.1', 'KDR_0001',  361, '2.3.1', 50,
     'paper: 1bp G deletion at 1037 in DR_0001 restores ORF -> 361 aa β-clamp / 1086 nt'),
    ('DR_0100', 'NC_001263.1', 'CP150840.1', 'KDR_0099m',  301, '2.3.1', 1000,  # SSB in BAA-816 is 143 aa; in 13939K paper says continuous 906 bp ORF spanning DR_0099+DR_0100. So expect ~301 aa = (906-3)/3.
     'paper: 906-bp continuous ORF spanning DR_0099+DR_0100 (deinococcal SSB) in 13939K = 301 aa'),
    ('DR_0997', 'NC_001263.1', 'CP150840.1', 'KDR_0997',  203, '2.3.3', 100,
     'paper: G insertion at 543 in DR_0997 truncates DdrI -> 203 aa'),
    ('DR_1647', 'NC_001263.1', 'CP150840.1', 'KDR_1647',  520, '2.3.2', 100,
     'paper: extra C at 954 in DR_1647 restores ORF -> 520 aa BshC'),
    ('DR_2410', 'NC_001263.1', 'CP150840.1', 'KDR_2410m', 786, '2.3.1', 600,
     'paper: T deletion at 1825 fuses DR_2410+DR_2411 -> 786 aa DnaX'),
    ('DR_RS12440', 'NC_001263.1', 'CP150840.1', 'KDR_2418',  221, '2.3.6', 200,
     'paper: DrRRA shortened to 221 aa in 13939K (vs 373 aa BAA-816); RefSeq=DR_RS12440 (pseudo response regulator)'),
    ('DR_RS17245', 'NC_001263.1', 'CP150840.1', 'KDR_1417',  813, '2.3.5', 1500,
     'paper: PBP1b 1009 aa in BAA-816 BUT 807-818 aa in other R1 strains incl. 13939K (Fig 1G, Supp S4) -> midpoint ~813 aa expected'),
    ('DR_2367', 'NC_001263.1', 'CP150840.1', 'KDR_2367',  None, '2.3.7', 350,
     'paper: G insertion at DR_2367 stop codon extends KefB by 100 aa'),
]


def get_baa816_feature(ref_acc, tag):
    rec = SeqIO.read(GB / f'{ref_acc}.gb', 'genbank')
    for feat in rec.features:
        if feat.type != 'gene':
            continue
        olts = feat.qualifiers.get('old_locus_tag', []) + feat.qualifiers.get('locus_tag', [])
        if tag in olts:
            return rec, feat
    # Fallback: search CDS features too (some RefSeq pseudos lack a 'gene' wrapper match)
    for feat in rec.features:
        if feat.type != 'CDS':
            continue
        olts = feat.qualifiers.get('old_locus_tag', []) + feat.qualifiers.get('locus_tag', [])
        if tag in olts:
            return rec, feat
    return rec, None


def longest_orf(seq_dna, min_len_aa=50, start_codons=('ATG','GTG','TTG'), require_start=True):
    """Find longest ORF on the + strand starting with a start codon (any frame)."""
    s = str(seq_dna).upper()
    best = None
    for frame in (0, 1, 2):
        i = frame
        while i + 3 <= len(s):
            codon = s[i:i+3]
            if (not require_start) or codon in start_codons:
                # scan to stop
                j = i
                aa_count = 0
                while j + 3 <= len(s):
                    c = s[j:j+3]
                    if c in ('TAA','TAG','TGA'):
                        break
                    j += 3
                    aa_count += 1
                if aa_count >= min_len_aa:
                    cand = (aa_count, i, j, frame, codon)
                    if best is None or aa_count > best[0]:
                        best = cand
                i = j + 3 if j > i else i + 3
            else:
                i += 3
    return best


def predict_one(claim):
    old_tag, ref_acc, qry_acc, kdr_label, paper_aa, sec, extend, note = claim
    rec_ref, feat = get_baa816_feature(ref_acc, old_tag)
    if feat is None:
        return {
            'old_tag': old_tag, 'kdr_label': kdr_label, 'status': 'NO_REF_FEATURE',
            'paper_aa': paper_aa, 'note': note,
        }

    ref_start = int(feat.location.start)
    ref_end   = int(feat.location.end)
    ref_strand = feat.location.strand
    # Expand search window
    win_start = max(0, ref_start - extend)
    win_end   = min(len(rec_ref.seq), ref_end + extend)
    ref_region = str(rec_ref.seq[win_start:win_end])

    # Load 13939K replicon
    qry_seq_full = str(SeqIO.read(FA / f'{qry_acc}.fa', 'fasta').seq)
    # Align ref region to full qry replicon (asm5)
    a = mp.Aligner(seq=qry_seq_full, preset='asm5')
    hits = list(a.map(ref_region))
    if not hits:
        return {
            'old_tag': old_tag, 'kdr_label': kdr_label, 'status': 'NO_MAP',
            'paper_aa': paper_aa, 'note': note,
        }
    # Best primary hit
    h = sorted(hits, key=lambda x: (-x.mlen, -x.blen))[0]
    qry_start, qry_end = h.r_st, h.r_en
    qry_region = qry_seq_full[qry_start:qry_end]
    # For - strand BAA-816 features the alignment will be on - strand of qry too
    if (ref_strand == -1) != (h.strand == -1):
        # Mixed: need to revcomp the qry region so that the orientation matches BAA-816 +sense
        qry_region_oriented = str(Seq(qry_region).reverse_complement())
    elif ref_strand == -1:
        qry_region_oriented = str(Seq(qry_region).reverse_complement())
    else:
        qry_region_oriented = qry_region

    # Find longest ORF in the oriented region
    orf = longest_orf(qry_region_oriented, min_len_aa=40)
    if orf is None:
        return {
            'old_tag': old_tag, 'kdr_label': kdr_label, 'status': 'NO_ORF',
            'paper_aa': paper_aa, 'note': note,
            'qry_region_len': len(qry_region_oriented),
        }
    aa_len, i_start, i_end, frame, start_codon = orf

    out = {
        'old_tag': old_tag,
        'kdr_label': kdr_label,
        'paper_aa': paper_aa,
        'paper_section': sec,
        'note': note,
        'baa816_pseudo': 'pseudo' in feat.qualifiers,
        'baa816_gene': feat.qualifiers.get('gene',[''])[0],
        'baa816_loc': f'{ref_start}..{ref_end}({"+" if ref_strand==1 else "-"})',
        'baa816_span_nt': ref_end - ref_start,
        'qry_replicon': qry_acc,
        'qry_aligned_loc': f'{qry_start}..{qry_end}({"+" if h.strand==1 else "-"})',
        'qry_region_len': len(qry_region_oriented),
        'predicted_orf_aa': aa_len,
        'predicted_orf_nt': aa_len * 3,
        'orf_start_codon': start_codon,
        'orf_frame': frame,
        'orf_offset_in_region': i_start,
    }
    if paper_aa is not None:
        d = aa_len - paper_aa
        out['delta_aa'] = d
        if d == 0:
            out['verdict'] = f'EXACT_MATCH ({aa_len} aa = paper)'
        elif abs(d) <= 2:
            out['verdict'] = f'AGREES_WITHIN_2aa (predicted {aa_len}, paper {paper_aa}, Δ={d:+d})'
        elif abs(d) <= 5:
            out['verdict'] = f'AGREES_WITHIN_5aa (predicted {aa_len}, paper {paper_aa}, Δ={d:+d})'
        elif abs(d) <= 15:
            out['verdict'] = f'CLOSE (predicted {aa_len}, paper {paper_aa}, Δ={d:+d})'
        else:
            out['verdict'] = f'DISAGREES (predicted {aa_len}, paper {paper_aa}, Δ={d:+d})'
    else:
        out['delta_aa'] = None
        out['verdict'] = f'ORF found, length={aa_len} aa (no numeric paper expectation)'
    return out


def main():
    print('Predicting KDR_xxxx CDS lengths via BAA-816→13939K coordinate lift + ORF search...')
    results = [predict_one(c) for c in CLAIMS]
    out_json = OUT / 'predictions.json'
    with open(out_json, 'w') as fh:
        json.dump({
            'description': 'Independent ORF-length predictions for paper-claimed 13939K CDSs.',
            'method': 'Lift BAA-816 RefSeq gene coordinates to CP150840-3 via minimap2 asm5, expand by 50-1000 bp, find longest start-codon ORF on oriented strand.',
            'limitations': [
                'CP150840-3 GenBank deposits have NO feature annotations (only source); KDR_xxxx tags exist only in supplementary tables.',
                'ORF prediction is naive: longest Met/Val/Leu-start ORF in the oriented region; does not run Prokka or use BLAST homology.',
                'Reading-frame restored vs broken is sensitive to a single bp; results should match paper to within ±2 aa if claims are correct.',
            ],
            'results': results,
        }, fh, indent=2)

    # Pretty print
    print(f"\n{'KDR_label':<12} {'BAA-816 ψ':>8} {'baa_span_nt':>11} {'paper_aa':>8} {'pred_aa':>7} {'Δ':>5}  verdict")
    print('-' * 110)
    for r in results:
        psu = 'pseudo' if r.get('baa816_pseudo') else 'CDS'
        d = r.get('delta_aa')
        dstr = (f'{d:+d}' if d is not None else '-')
        pa = r.get('paper_aa')
        pa_str = str(pa) if pa is not None else '-'
        pred = r.get('predicted_orf_aa')
        pred_str = str(pred) if pred is not None else '-'
        span = r.get('baa816_span_nt')
        span_str = str(span) if span is not None else '-'
        print(f"{r.get('kdr_label',''):<12} {psu:>8} {span_str:>11} "
              f"{pa_str:>8} {pred_str:>7} {dstr:>5}  {r.get('verdict','')}")
    print(f"\nWrote: {out_json}")


if __name__ == '__main__':
    main()
