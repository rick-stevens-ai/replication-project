import re
from collections import defaultdict
GBK="results/repass/prokka_full/DJF10_clean.gbk"
features=[]
current=None; current_contig=None
with open(GBK) as fh:
    for line in fh:
        m_locus = re.match(r"^LOCUS\s+(\S+)", line)
        if m_locus: current_contig = m_locus.group(1); continue
        m_cds = re.match(r"^     (CDS|tRNA|tmRNA|rRNA)\s+(complement\()?(\d+)\.\.(\d+)\)?", line)
        if m_cds:
            if current: features.append(current)
            current = {'kind':m_cds.group(1),'contig':current_contig,'start':int(m_cds.group(3)),'end':int(m_cds.group(4)),'lt':None,'prod':None}
            continue
        m_lt = re.search(r'/locus_tag="([^"]+)"', line)
        if m_lt and current: current['lt'] = m_lt.group(1)
        m_p = re.search(r'/product="(.+?)"', line)
        if m_p and current: current['prod'] = m_p.group(1)
if current: features.append(current)

MOBILE_KW = ['transposase','integrase','recombinase','insertion sequence','IS[0-9]+','phage','bacteriophage','plasmid replication','RepA','RepB','RepC','prophage','virion','toxin','toxin-antitoxin','BRO domain','restriction','modification']
mobile_lts = set()
for f in features:
    if f['prod']:
        if any(re.search(k, f['prod'], re.I) for k in MOBILE_KW):
            mobile_lts.add(f['lt'])

# Pass-1 IS hits
import os
if os.path.exists("data/is_elements_blastx.tsv"):
    with open("data/is_elements_blastx.tsv") as fh:
        for line in fh:
            f = line.strip().split('\t')
            if f: mobile_lts.add(f[0].split()[0])

# Phage HMM hits
phage_lts = set()
with open("/tmp/phage_hits.tbl") as fh:
    for line in fh:
        if line.startswith("#"): continue
        f = line.split()
        if len(f) >= 5 and float(f[4]) < 1e-5:
            phage_lts.add(f[2])
all_mobility = mobile_lts | phage_lts
print(f"Total mobility-marker CDSs: {len(all_mobility)}")

# IslandViewer-style: use SLIDING WINDOW dinucleotide composition vs genome average
# But for draft assembly with short contigs we approximate by region content:
# An island candidate = a window (10-kb sliding) where >=15% of CDSs are hypothetical
# AND contains at least 1 mobility marker AND total length >= 4 kb

contig_features = defaultdict(list)
for f in features:
    contig_features[f['contig']].append(f)
for v in contig_features.values():
    v.sort(key=lambda x: x['start'])

islands = []
WINDOW_SIZE = 20  # window of 20 consecutive CDS
for contig, feats in contig_features.items():
    cds_only = [f for f in feats if f['kind']=='CDS']
    if len(cds_only) < WINDOW_SIZE: continue
    for i in range(0, len(cds_only) - WINDOW_SIZE + 1):
        window = cds_only[i:i+WINDOW_SIZE]
        hyp = sum(1 for w in window if w['prod'] and 'hypothetical' in w['prod'].lower())
        mob = sum(1 for w in window if w['lt'] in all_mobility)
        if hyp >= 12 and mob >= 1:  # ≥60% hypothetical + ≥1 mobility
            s = window[0]['start']; e = window[-1]['end']
            islands.append({'contig':contig,'start':s,'end':e,'length':e-s+1,'hyp':hyp,'mob':mob})

# Merge overlapping windows
islands.sort(key=lambda x: (x['contig'], x['start']))
merged = []
for isl in islands:
    if merged and merged[-1]['contig']==isl['contig'] and isl['start'] <= merged[-1]['end']:
        merged[-1]['end'] = max(merged[-1]['end'], isl['end'])
        merged[-1]['length'] = merged[-1]['end'] - merged[-1]['start'] + 1
        merged[-1]['hyp'] = max(merged[-1]['hyp'], isl['hyp'])
        merged[-1]['mob'] = max(merged[-1]['mob'], isl['mob'])
    else:
        merged.append(dict(isl))

# Filter to length >=4 kb (paper minimum)
real = [m for m in merged if m['length'] >= 4000]

print(f"\n=== Candidate genomic islands (hypothetical-rich window + mobility marker; len>=4kb) ===")
print(f"Total: {len(real)}")
print(f"\n{'#':>3} {'Contig':<10} {'Start':>8} {'End':>8} {'Len(bp)':>9} {'Hyp':>4} {'Mob':>4}")
print("-"*60)
for i,r in enumerate(sorted(real, key=lambda x: -x['length']),1):
    print(f"{i:>3} {r['contig']:<10} {r['start']:>8} {r['end']:>8} {r['length']:>9} {r['hyp']:>4} {r['mob']:>4}")

print(f"\nLength range (kb): {min(r['length'] for r in real)/1000:.1f} – {max(r['length'] for r in real)/1000:.1f}")
print(f"\n=== Paper: 18 islands, 4,228–69,769 bp ===")

import json
with open("results/repass/islands/custom_islands_v2.json","w") as fh:
    json.dump(real, fh, indent=2)
