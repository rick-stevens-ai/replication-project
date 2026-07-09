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

# Pass-1 IS_blastx hits: read data/is_elements.tsv to know which CDSs are IS proteins
is_lts = set()
import os
if os.path.exists("data/is_elements.tsv"):
    with open("data/is_elements.tsv") as fh:
        for line in fh:
            f = line.strip().split('\t')
            if f and f[0].startswith("DJF10") or f[0].startswith("HMK"):
                is_lts.add(f[0].split()[0])
print(f"Pass-1 IS-positive CDSs (data/is_elements.tsv): {len(is_lts)}")
# Also try is_elements_blastx
if os.path.exists("data/is_elements_blastx.tsv"):
    with open("data/is_elements_blastx.tsv") as fh:
        for line in fh:
            f = line.strip().split('\t')
            if f: is_lts.add(f[0].split()[0])
print(f"Combined IS-positive CDSs: {len(is_lts)}")

# Mobile-element keywords in Prokka product names
MOBILE_KW = ['transposase','integrase','recombinase','insertion sequence','IS[0-9]+','phage','bacteriophage','plasmid replication','RepA','RepB','RepC','prophage','virion','toxin']
mobile_lts = set()
for f in features:
    if f['prod']:
        if any(re.search(k, f['prod'], re.I) for k in MOBILE_KW):
            mobile_lts.add(f['lt'])

# Combine with Pass-1 IS hits
combined = mobile_lts | is_lts
print(f"Mobility CDSs (mobile-element keywords or IS-positive): {len(combined)}")

# Add phage HMM hits from /tmp/phage_hits.tbl
phage_lts = set()
with open("/tmp/phage_hits.tbl") as fh:
    for line in fh:
        if line.startswith("#"): continue
        f = line.split()
        if len(f) >= 5 and float(f[4]) < 1e-5:
            phage_lts.add(f[2])
combined |= phage_lts
print(f"Plus phage-HMM hits: {len(combined)}")

# Find regions: walk per-contig, group mobility-positive CDSs within 10-gene gap
GAP = 10
contig_features = defaultdict(list)
for f in features:
    contig_features[f['contig']].append(f)
for v in contig_features.values():
    v.sort(key=lambda x: x['start'])

islands = []
for contig, feats in contig_features.items():
    cur = []
    last_idx = None
    for i,f in enumerate(feats):
        if f['lt'] in combined or f['kind'] in ('tRNA','tmRNA'):  # tRNA often flanks islands
            if last_idx is None or (i - last_idx) <= GAP:
                cur.append((i,f))
            else:
                if len(cur) >= 3:
                    s = min(c[1]['start'] for c in cur); e = max(c[1]['end'] for c in cur)
                    if e - s >= 4000:
                        islands.append({'contig':contig,'start':s,'end':e,'length':e-s+1,'features_count':len(cur),'tRNAs':sum(1 for c in cur if c[1]['kind'] in ('tRNA','tmRNA'))})
                cur = [(i,f)]
            last_idx = i
    if len(cur) >= 3:
        s = min(c[1]['start'] for c in cur); e = max(c[1]['end'] for c in cur)
        if e - s >= 4000:
            islands.append({'contig':contig,'start':s,'end':e,'length':e-s+1,'features_count':len(cur),'tRNAs':sum(1 for c in cur if c[1]['kind'] in ('tRNA','tmRNA'))})

# Filter to bona-fide GI candidates: must contain >=2 mobility CDS (not just tRNAs)
def n_mobility(s,e,contig):
    return sum(1 for f in contig_features[contig] if (s<=f['start']<=e or s<=f['end']<=e) and f['lt'] in combined)

real = []
for isl in islands:
    n_m = n_mobility(isl['start'],isl['end'],isl['contig'])
    if n_m >= 2:
        isl['n_mobility'] = n_m
        real.append(isl)

print(f"\n=== Candidate genomic islands (mobility-gene clustering, gap<=10 ORFs, len>=4kb, >=2 mobility CDS) ===")
print(f"Total candidate islands: {len(real)}")
print(f"\nLength distribution (kb): {sorted([round(r['length']/1000,1) for r in real])}")
print(f"\n{'#':>3} {'Contig':<10} {'Start':>8} {'End':>8} {'Len(bp)':>8} {'Mobility':>9} {'tRNAs':>6}")
print("-"*65)
for i,r in enumerate(sorted(real, key=lambda x: -x['length']), 1):
    print(f"{i:>3} {r['contig']:<10} {r['start']:>8} {r['end']:>8} {r['length']:>8} {r['n_mobility']:>9} {r['tRNAs']:>6}")

import json
with open("results/repass/islands/custom_islands.json","w") as fh:
    json.dump(real, fh, indent=2)

PAPER = {"n_islands":18, "len_range":(4228, 69769)}
print(f"\n=== Paper claim (Kandasamy 2022 section 2.5.2) ===")
print(f"  18 genomic islands, length 4,228–69,769 bp")
print(f"\n=== Comparison ===")
print(f"  Paper N: 18 | Ours: {len(real)}")
print(f"  Paper range: 4228-69769 | Ours: {min((r['length'] for r in real),default=0)}-{max((r['length'] for r in real),default=0)}")
