#!/usr/bin/env python3
"""
Custom PHASTER-style prophage finder.

Method:
  1. hmmscan Prokka proteins vs 25 phage Pfam HMMs (already done).
  2. Cluster phage-HMM-positive CDSs that are within N consecutive non-phage
     genes of each other (gap threshold = 5 like PHASTER).
  3. Require at least one integrase (PF00589/PF02899/PF13495) per region.
  4. Classify intact vs questionable vs incomplete by gene count:
       - Intact: >=15 phage genes or contains terminase + integrase + capsid
       - Questionable: >=10
       - Incomplete: >=5
  5. Output per-region: contig, start, stop, length, gene count, integrase ORF.

This is the core scoring approach used by PHASTER (Arndt et al. 2016).
"""
import re, sys
from collections import defaultdict
from pathlib import Path

GBK = "results/repass/prokka_full/DJF10_clean.gbk"
HMM_TBL = "/tmp/phage_hits.tbl"  # from earlier hmmscan with E<1e-5

# 1. Parse hmmscan tbl: per CDS, what phage HMMs hit?
cds_hmms = defaultdict(set)
hmm_categories = {
    'integrase':   {'Phage_integrase', 'Phage_int_SAM_1', 'Phage_int_SAM_4'},
    'terminase':   {'Terminase_1', 'Terminase_2', 'Terminase_3', 'Terminase_4',
                    'Terminase_5', 'Terminase_6', 'TerL_ATPase'},
    'baseplate':   {'Phage_baseplate', 'Phage_BR0599'},
    'holin':       {'Holin_T7', 'Phage_holin_2_3', 'Holin_LLH'},
    'lysin':       {'Phage_lysozyme', 'CHAP'},
    'tail':        {'Phage_tail_3', 'RHS_repeat', 'Phage_pRha', 'Phage_pRha2', 'GP49_phage'},
    'capsid_portal':{'Phage_GPD', 'HK97_gp10_likeprotein', 'Phage_HK97', 'Phage_GP14', 'Phage_AP'},
    'misc_phage':  {'ABM'},
}
hmm_to_cat = {hmm: cat for cat, hmms in hmm_categories.items() for hmm in hmms}

with open(HMM_TBL) as fh:
    for line in fh:
        if line.startswith("#"): continue
        f = line.split()
        if len(f) < 5: continue
        hmm_name, target = f[0], f[2]
        evalue = float(f[4])
        if evalue < 1e-5:
            cds_hmms[target].add(hmm_name)

print(f"Phage-HMM-hit CDSs: {len(cds_hmms)}")

# 2. Parse Prokka GBK: ordered list of (contig, locus_tag, start, end, product) per CDS
cds_list = []
current_contig = None
current_cds = None
with open(GBK) as fh:
    for line in fh:
        m_locus = re.match(r"^LOCUS\s+(\S+)", line)
        if m_locus:
            current_contig = m_locus.group(1)
            continue
        m_cds = re.match(r"^     CDS\s+(complement\()?(\d+)\.\.(\d+)\)?", line)
        if m_cds:
            if current_cds:
                cds_list.append(current_cds)
            current_cds = {
                'contig': current_contig,
                'start': int(m_cds.group(2)),
                'end': int(m_cds.group(3)),
                'locus_tag': None,
                'product': None,
            }
            continue
        m_lt = re.search(r'/locus_tag="([^"]+)"', line)
        if m_lt and current_cds:
            current_cds['locus_tag'] = m_lt.group(1)
        m_p = re.search(r'/product="(.+?)"', line)
        if m_p and current_cds:
            current_cds['product'] = m_p.group(1)
if current_cds:
    cds_list.append(current_cds)

print(f"Total CDSs from GBK: {len(cds_list)}")

# 3. Tag CDSs with phage HMM info
for cds in cds_list:
    lt = cds['locus_tag']
    if lt in cds_hmms:
        cds['phage_hmms'] = cds_hmms[lt]
        cds['phage_cats'] = {hmm_to_cat.get(h, 'misc') for h in cds_hmms[lt]}
    else:
        cds['phage_hmms'] = set()
        cds['phage_cats'] = set()

# 4. Cluster: walk through cds_list per contig, group phage CDSs separated by <= GAP non-phage genes
GAP = 5  # PHASTER default ~5
clusters = []
contig_groups = defaultdict(list)
for cds in cds_list:
    contig_groups[cds['contig']].append(cds)

for contig, cdss in contig_groups.items():
    current_cluster = []
    last_phage_idx = None
    for i, c in enumerate(cdss):
        is_phage = bool(c['phage_hmms'])
        if is_phage:
            if last_phage_idx is None or (i - last_phage_idx) <= GAP:
                current_cluster.append((i, c))
            else:
                if current_cluster:
                    clusters.append((contig, current_cluster, cdss))
                current_cluster = [(i, c)]
            last_phage_idx = i
    if current_cluster:
        clusters.append((contig, current_cluster, cdss))

print(f"\nRaw phage-CDS clusters: {len(clusters)}")

# 5. Score and classify each cluster
results = []
for contig, cluster, all_cdss in clusters:
    phage_cdss = [c for _, c in cluster]
    if len(phage_cdss) < 2:
        continue  # skip lone phage genes (likely orphan integrase)
    start_idx = cluster[0][0]
    end_idx = cluster[-1][0]
    start_bp = min(c['start'] for c in phage_cdss)
    end_bp = max(c['end'] for c in phage_cdss)
    # Extend to include +/- GAP boundary genes (the actual region in PHASTER)
    region_start_idx = max(0, start_idx - 2)
    region_end_idx = min(len(all_cdss) - 1, end_idx + 2)
    region_cdss = all_cdss[region_start_idx:region_end_idx + 1]
    region_start_bp = min(c['start'] for c in region_cdss)
    region_end_bp = max(c['end'] for c in region_cdss)
    region_len = region_end_bp - region_start_bp + 1
    n_phage = len(phage_cdss)
    n_total = len(region_cdss)
    cats = set()
    for c in phage_cdss:
        cats.update(c['phage_cats'])
    has_integrase = 'integrase' in cats
    has_terminase = 'terminase' in cats
    has_capsid = 'capsid_portal' in cats
    has_tail = 'tail' in cats
    has_baseplate = 'baseplate' in cats
    
    # Classify
    score = n_phage
    if has_terminase: score += 5
    if has_integrase: score += 3
    if has_capsid:    score += 3
    if has_tail:      score += 2
    if has_baseplate: score += 2
    if score >= 15 and has_integrase and has_terminase:
        cls = "INTACT"
    elif score >= 8:
        cls = "QUESTIONABLE"
    elif score >= 5:
        cls = "INCOMPLETE"
    else:
        cls = "TOO_WEAK"
    
    integrase_locus = next((c['locus_tag'] for c in phage_cdss if 'integrase' in c['phage_cats']), None)
    
    results.append({
        'contig': contig,
        'region_start': region_start_bp,
        'region_end': region_end_bp,
        'region_len_kb': round(region_len/1000, 2),
        'n_phage_cdss': n_phage,
        'n_total_cdss': n_total,
        'categories': sorted(cats),
        'has_integrase': has_integrase,
        'has_terminase': has_terminase,
        'has_capsid': has_capsid,
        'integrase_locus': integrase_locus,
        'score': score,
        'classification': cls,
    })

print(f"Candidate regions (>=2 phage CDSs): {len(results)}")
print()
print(f"{'Contig':<10} {'Start':>8} {'End':>8} {'Len(kb)':>8} {'Phage':>6} {'Total':>6} {'Score':>6} {'Class':<14} {'Integrase':<25} {'Cats':<60}")
print("-" * 160)
for r in sorted(results, key=lambda x: -x['score']):
    print(f"{r['contig']:<10} {r['region_start']:>8} {r['region_end']:>8} {r['region_len_kb']:>8} {r['n_phage_cdss']:>6} {r['n_total_cdss']:>6} {r['score']:>6} {r['classification']:<14} {str(r['integrase_locus']):<25} {','.join(r['categories']):<60}")

# Filter to intact/questionable/incomplete (PHASTER-style three-tier output)
phaster_like = [r for r in results if r['classification'] in ('INTACT', 'QUESTIONABLE', 'INCOMPLETE')]
intact = sum(1 for r in phaster_like if r['classification'] == 'INTACT')
quest  = sum(1 for r in phaster_like if r['classification'] == 'QUESTIONABLE')
incomp = sum(1 for r in phaster_like if r['classification'] == 'INCOMPLETE')

print(f"\n=== PHASTER-style summary ===")
print(f"  Total regions: {len(phaster_like)}")
print(f"  Intact:        {intact}")
print(f"  Questionable:  {quest}")
print(f"  Incomplete:    {incomp}")

import json
Path("results/repass/prophage").mkdir(parents=True, exist_ok=True)
with open("results/repass/prophage/custom_prophages.json","w") as fh:
    json.dump(results, fh, indent=2)
print("Wrote results/repass/prophage/custom_prophages.json")

# Compare to paper
print(f"\n=== Paper claim (Kandasamy 2022 Table 6) ===")
print(f"  3 regions: 2 intact (R1=16.8kb, R3=53.9kb), 1 questionable (R2=19.7kb)")
print(f"  R1: 16.8kb, 31 proteins, integrase ORF 379616-380770, Entero_phiSHEF4")
print(f"  R2: 19.7kb, 22 proteins, integrase ORF 262710-263867, Entero_vB_EfaS_AL2")
print(f"  R3: 53.9kb, 56 proteins, integrase ORF 205632-206768, Lactob_Sha1")
