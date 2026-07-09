#!/usr/bin/env python3
"""
R6 — Cross-panel logical-chain test (promotion audit add-on).

S1 only published hiPSCs-anchored γH2AX significance. For the qPCR panels (S2–S5)
the paper published BOTH the HC-anchored half AND the iPSC-anchored half, which
together encode all three pairwise comparisons. We use S1 to score
'hiPSCs vs HC-402-05a' damage; for repair we use BOTH 'hiPSCs vs HC' and
'hiPSC-DCHs vs HC' from S2–S5.

Logical-chain claim being tested:
  Where γH2AX(hiPSCs vs HC) is significant (DSBs are higher in stem cells
  than in mature chondrocytes), at least one of the four repair-gene panels
  should be significant in the same (dose,time) cell.

This is the falsifiable inference of the paper's narrative
"more damage in iPSCs/DCHs -> activates major DDR pathways" at the
significance-pattern level (we cannot test the fold-change because the
mean values were never deposited).

Output: replication/promo/r6_cross_panel.csv  + JSON summary.
"""
import csv, json
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "parsed_supp" / "all_supp_significance.csv"
rows = list(csv.DictReader(open(src)))

def grab(panel_prefix, query, comp_target, dose, time):
    for r in rows:
        if not r['panel'].startswith(panel_prefix): continue
        if r['cell_line'].strip() != query: continue
        if r['comparison'].strip() != comp_target: continue
        if r['dose_Gy'].strip() != dose: continue
        if r['time'].strip() != time: continue
        return r['sig']
    return None

doses = ['0 Gy','1 Gy','2 Gy','5 Gy']
times = ['1h','5h','9h','24h']
out_rows, hits, total = [], 0, 0
for d in doses:
    for t in times:
        # γH2AX hiPSCs vs HC (only direction published in S1)
        g_iPSC_HC = grab('S1_gH2AX', 'hiPSCs', 'vs. HC-402-05a', d, t)
        # for repair: hiPSCs vs HC AND hiPSC-DCHs vs HC, from S2-S5 (B half == iPSC-anchor)
        def repair(panel_prefix, query):
            return grab(panel_prefix, query, 'vs. HC-402-05a', d, t)

        # B-half = hiPSC-anchored (rows are hiPSCs vs HC and hiPSCs vs DCHs).
        # A-half = HC-anchored (rows are HC vs hiPSCs and HC vs DCHs)
        #   -> 'HC vs DCHs' is the DCH-vs-HC contrast (just inverted sign).
        def both_anchors(panel_prefix):
            ips = grab(panel_prefix.replace('_A_anchorHC','_B_anchoriPSC'),
                       'hiPSCs', 'vs. HC-402-05a', d, t)
            dch = grab(panel_prefix.replace('_B_anchoriPSC','_A_anchorHC'),
                       'HC-402-05a', 'vs. hiPSC-DCHs', d, t)
            return ips, dch
        bi, bd = both_anchors('S2_BRCA2_B_anchoriPSC')
        ri, rd = both_anchors('S3_RAD51_B_anchoriPSC')
        pi, pd = both_anchors('S4_PRKDC_B_anchoriPSC')
        xi, xd = both_anchors('S5_XRCC4_B_anchoriPSC')
        rep = {
            'BRCA2': {'iPSC': bi, 'DCH': bd},
            'RAD51': {'iPSC': ri, 'DCH': rd},
            'PRKDC': {'iPSC': pi, 'DCH': pd},
            'XRCC4': {'iPSC': xi, 'DCH': xd},
        }
        sigs = [v for gene in rep.values() for v in gene.values()]
        any_repair_sig = any(s and s != 'ns' for s in sigs)

        damage = (g_iPSC_HC and g_iPSC_HC != 'ns')
        if damage is None or g_iPSC_HC is None:
            consistent = None
        else:
            if damage:
                consistent = bool(any_repair_sig)
            else:
                consistent = True
            total += 1
            if consistent: hits += 1
        out_rows.append({
            'dose': d, 'time': t,
            'gH2AX_iPSCvsHC': g_iPSC_HC or 'NA',
            'BRCA2_iPSC': rep['BRCA2']['iPSC'] or 'NA',
            'BRCA2_DCH':  rep['BRCA2']['DCH'] or 'NA',
            'RAD51_iPSC': rep['RAD51']['iPSC'] or 'NA',
            'RAD51_DCH':  rep['RAD51']['DCH'] or 'NA',
            'PRKDC_iPSC': rep['PRKDC']['iPSC'] or 'NA',
            'PRKDC_DCH':  rep['PRKDC']['DCH'] or 'NA',
            'XRCC4_iPSC': rep['XRCC4']['iPSC'] or 'NA',
            'XRCC4_DCH':  rep['XRCC4']['DCH'] or 'NA',
            'damage_sig': damage,
            'any_repair_sig': any_repair_sig,
            'consistent_with_chain': consistent,
        })

outdir = root / 'promo'
outdir.mkdir(exist_ok=True)
with open(outdir/'r6_cross_panel.csv','w') as fh:
    w = csv.DictWriter(fh, fieldnames=out_rows[0].keys())
    w.writeheader(); w.writerows(out_rows)

summary = {
    'cells_tested': total,
    'consistent_chain': hits,
    'fraction': hits/total if total else None,
    'note': 'damage_sig=True implies any_repair_sig=True for chain to hold',
}
print(json.dumps(summary, indent=2))
print('\nPer-cell (16 design cells):')
for r in out_rows:
    flag = '✓' if r['consistent_with_chain'] else ('✗' if r['consistent_with_chain'] is False else '?')
    print(f"  {r['dose']:5s} {r['time']:4s} damage={str(r['damage_sig']):5s} repair={str(r['any_repair_sig']):5s} chain={flag}")
