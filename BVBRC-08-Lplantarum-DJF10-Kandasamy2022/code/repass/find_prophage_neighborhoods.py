import re
from collections import defaultdict
GBK = "results/repass/prokka_full/DJF10_clean.gbk"
HMM_TBL = "/tmp/phage_hits.tbl"
cds_hmms = defaultdict(set)
with open(HMM_TBL) as fh:
    for line in fh:
        if line.startswith("#"): continue
        f = line.split()
        if len(f) < 5: continue
        if float(f[4]) < 1e-5:
            cds_hmms[f[2]].add(f[0])
cds_list = []
current_contig = None; current_cds = None
prod = {}
current_lt_for_prod = None
with open(GBK) as fh:
    for line in fh:
        m_locus = re.match(r"^LOCUS\s+(\S+)", line)
        if m_locus: current_contig = m_locus.group(1); continue
        m_cds = re.match(r"^     CDS\s+(complement\()?(\d+)\.\.(\d+)\)?", line)
        if m_cds:
            if current_cds: cds_list.append(current_cds)
            current_cds = {'contig': current_contig, 'start': int(m_cds.group(2)), 'end': int(m_cds.group(3)), 'locus_tag': None, 'product': None}
            continue
        m_lt = re.search(r'/locus_tag="([^"]+)"', line)
        if m_lt:
            if current_cds: current_cds['locus_tag'] = m_lt.group(1)
            current_lt_for_prod = m_lt.group(1)
            continue
        m_p = re.search(r'/product="(.+?)"', line)
        if m_p and current_lt_for_prod: prod[current_lt_for_prod] = m_p.group(1)
if current_cds: cds_list.append(current_cds)
for c in cds_list:
    c['phage_hmms'] = cds_hmms.get(c['locus_tag'], set())
contig_cds = defaultdict(list)
for c in cds_list: contig_cds[c['contig']].append(c)

INTEGRASE_HMMS = {'Phage_integrase', 'Phage_int_SAM_1', 'Phage_int_SAM_4'}
TERMINASE_HMMS = {'Terminase_1','Terminase_2','Terminase_3','Terminase_4','Terminase_5','Terminase_6','TerL_ATPase'}

print("=== Integrase neighborhoods (+/- 30 genes) ===")
candidate_regions = []
for contig, cdss in contig_cds.items():
    for i,c in enumerate(cdss):
        if c['phage_hmms'] & INTEGRASE_HMMS:
            lo = max(0,i-30); hi=min(len(cdss)-1, i+30)
            window = cdss[lo:hi+1]
            phage_in_window = sum(1 for w in window if w['phage_hmms'])
            window_start = window[0]['start']; window_end = window[-1]['end']
            cats = set()
            for w in window:
                for h in w['phage_hmms']:
                    cats.add(h)
            has_term = bool(cats & TERMINASE_HMMS)
            if phage_in_window >= 2:
                print(f"\nContig {contig} integrase={c['locus_tag']} @ {c['start']}-{c['end']}")
                print(f"  Window {window_start}-{window_end} ({(window_end-window_start+1)/1000:.1f}kb), {len(window)} CDS, {phage_in_window} phage-HMM hits, terminase={has_term}")
                candidate_regions.append({'contig':contig,'integrase':c['locus_tag'],'integrase_start':c['start'],'integrase_end':c['end'],'window_start':window_start,'window_end':window_end,'len_kb':round((window_end-window_start+1)/1000,2),'n_phage_cdss':phage_in_window,'n_total_cdss':len(window),'has_terminase':has_term,'hmm_cats':sorted(cats)})

print(f"\n\n=== {len(candidate_regions)} candidate prophage regions (integrase + >=2 phage CDS in +/-30 window) ===")
print("Sorted by phage CDS count (descending)")
for r in sorted(candidate_regions, key=lambda x: -x['n_phage_cdss']):
    cls = "INTACT" if (r['has_terminase'] and r['n_phage_cdss']>=4) else ("QUESTIONABLE" if r['n_phage_cdss']>=3 else "INCOMPLETE")
    print(f"  {r['contig']} {r['window_start']}-{r['window_end']} ({r['len_kb']}kb) {r['n_phage_cdss']}/{r['n_total_cdss']} phage CDS — {cls} — integrase={r['integrase']} term={r['has_terminase']}")

import json
with open("results/repass/prophage/integrase_neighborhoods.json","w") as fh:
    json.dump(candidate_regions, fh, indent=2)
