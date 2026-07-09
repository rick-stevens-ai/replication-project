#!/usr/bin/env python3
"""Replication analysis of Delgado-Suárez et al. 2021 (PLOS ONE 16:e0243681).

Uses AMRFinderPlus 4.2.7 calls made on the 68 GenBank assemblies of the
study's 77 isolates (BioProject PRJNA480281). Reproduces:
  - Serovar and sequence-type composition
  - MDR rates (>=3 antimicrobial classes)
  - LN vs GB MDR chi-square (paper: chi2=12.0, P=0.0005)
  - Typhimurium enrichment (paper: OR=45.8)
  - SGI-1 marker set carriage in Typhimurium
  - Widespread mutations (soxRS, pmrAB, acrB, gyrA/parE) prevalence
"""
import csv, json, math, sys
from collections import Counter, defaultdict
from scipy import stats

WORK = "/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-109-Salmonella-AMR-surveillance-cattle-poultry-2021/work"

# ---- Load metadata ----
# study isolates keyed by BioSample
iso = {}
with open(f"{WORK}/study_isolates.csv") as f:
    for r in csv.DictReader(f):
        iso[r['BioSample']] = r

# GCA -> BioSample map
gca2samn = {}
with open(f"{WORK}/study_assemblies.tsv") as f:
    for r in csv.DictReader(f, delimiter='\t'):
        gca2samn[r['Assembly Accession']] = r['Assembly BioSample Accession']

# Load AMR calls
amr_calls = defaultdict(list)   # samn -> list of gene records
with open(f"{WORK}/all_amr_calls.tsv") as f:
    r = csv.DictReader(f, delimiter='\t')
    for row in r:
        gca = row['assembly']
        samn = gca2samn.get(gca)
        if not samn: continue
        amr_calls[samn].append(row)

# Load POINT mutations (all mutations, wildtype+POINT)
mut_calls = defaultdict(list)
with open(f"{WORK}/all_mut_calls.tsv") as f:
    r = csv.DictReader(f, delimiter='\t')
    for row in r:
        gca = row['assembly']
        samn = gca2samn.get(gca)
        if not samn: continue
        mut_calls[samn].append(row)

print(f"Loaded {len(iso)} paper isolates, {len(amr_calls)} with AMR calls "
      f"({len(iso)-len(amr_calls)} missing = no NCBI assembly).")

# ---- Serovar composition (from paper metadata, sanity-check) ----
sv = Counter(v['Serovar'] for v in iso.values())
print("\n[Paper metadata] Serovar counts (all 77):", dict(sv))

# ---- Restrict comparisons to 68 with re-computed AMR ----
sub_iso = {s: iso[s] for s in amr_calls}
print(f"\n[Re-analysis subset] N={len(sub_iso)}")

sv_sub = Counter(v['Serovar'] for v in sub_iso.values())
print("[Re-analysis subset] Serovar counts:", dict(sv_sub))
src_sub = Counter(v['Isolation Source'] for v in sub_iso.values())
print("[Re-analysis subset] Source counts:", dict(src_sub))

# ---- Build per-isolate AMR class set (from AMRFinderPlus 4.2.7 core AMR only) ----
# Class column is UPPERCASE antimicrobial class (e.g. TETRACYCLINE, BETA-LACTAM)
def isolate_classes(recs):
    classes = set()
    genes = set()
    for r in recs:
        if r['Type'] != 'AMR': continue
        if r['Subtype'] == 'POINT':  # point mutations - keep track separately
            continue
        cl = r['Class'].strip()
        if cl and cl != 'NA':
            classes.add(cl)
        genes.add(r['Element symbol'])
    return classes, genes

per_iso = {}
for samn, recs in amr_calls.items():
    cls, genes = isolate_classes(recs)
    per_iso[samn] = {'classes': cls, 'genes': genes, 'nclasses': len(cls)}

nclass_dist = Counter(v['nclasses'] for v in per_iso.values())
print(f"\n[Genotypic MDR count] distribution of # AMR classes per isolate: {dict(sorted(nclass_dist.items()))}")
mdr = sum(1 for v in per_iso.values() if v['nclasses'] >= 3)
print(f"MDR (>=3 classes) genotypic count: {mdr}/{len(per_iso)} = {mdr/len(per_iso)*100:.1f}%")
print("Paper reports 26% MDR phenotypic (77 isolates); expected ~20 MDR.")

# ---- Top AMR genes ----
gene_count = Counter()
for v in per_iso.values():
    for g in v['genes']:
        gene_count[g] += 1
print("\n[Re-analysis] top 25 AMR genes (68 study isolates):")
for g, n in gene_count.most_common(25):
    print(f"  {g}: {n}")

# ---- LN vs GB MDR chi-square (Claim C_LN_GB) ----
ln_mdr = ln_no = gb_mdr = gb_no = 0
for samn, meta in sub_iso.items():
    is_mdr = per_iso[samn]['nclasses'] >= 3
    src = meta['Isolation Source']
    if src == 'Lymph nodes':
        if is_mdr: ln_mdr += 1
        else: ln_no += 1
    elif src == 'Ground beef':
        if is_mdr: gb_mdr += 1
        else: gb_no += 1
print(f"\n[LN vs GB MDR 2x2] LN: MDR={ln_mdr} nonMDR={ln_no} | GB: MDR={gb_mdr} nonMDR={gb_no}")
table = [[ln_mdr, ln_no], [gb_mdr, gb_no]]
chi2, p, dof, exp = stats.chi2_contingency(table, correction=False)
print(f"Chi-square (no Yates): chi2={chi2:.2f}, dof={dof}, p={p:.4g}")
chi2c, pc, _, _ = stats.chi2_contingency(table, correction=True)
print(f"Chi-square (Yates):    chi2={chi2c:.2f}, p={pc:.4g}")
if gb_no>0 and ln_mdr>=0:
    or_ = (gb_mdr * ln_no) / max(gb_no * ln_mdr, 1e-9) if ln_mdr>0 else float('inf')
    print(f"OR (GB MDR vs LN MDR) approx: {or_:.2f}")
odds_ratio, fisher_p = stats.fisher_exact(table)
print(f"Fisher exact OR={odds_ratio:.2f}, p={fisher_p:.4g}")
print(f"Paper reports: chi2=12.0, P=0.0005, OR=6.5 (95%CI 2.1-20.1)")

# ---- Typhimurium (incl. monophasic) MDR enrichment (Claim C_TYPH) ----
typh = {s for s,m in sub_iso.items() if m['Serovar'] in ('Typhimurium','1,4,[5],12:i:-')}
other = {s for s in sub_iso if s not in typh}
tt = sum(1 for s in typh if per_iso[s]['nclasses'] >= 3)
tn = len(typh) - tt
ot = sum(1 for s in other if per_iso[s]['nclasses'] >= 3)
on = len(other) - ot
print(f"\n[Typhimurium vs other MDR] Typh: MDR={tt}/{len(typh)} | Other: MDR={ot}/{len(other)}")
table = [[tt, tn], [ot, on]]
chi2, p, _, _ = stats.chi2_contingency(table, correction=False)
odds_ratio, fisher_p = stats.fisher_exact(table)
print(f"Chi-square: chi2={chi2:.2f}, p={p:.4g}; Fisher OR={odds_ratio:.2f}, p={fisher_p:.4g}")
print("Paper reports: chi2=24.5, P<0.0001, OR=45.8 (95%CI 5.3-399.2)")

# ---- SGI-1 marker set in Typhimurium (Claim C_SGI1) ----
# Paper: 9/10 Typhimurium carry SGI-1 penta-resistance markers (aadA2, blaCARB-2, floR, sul1, tetG)
sgi1_markers = {'aadA2', 'blaCARB-2', 'floR', 'sul1', 'tet(G)'}
sgi1_count = 0
sgi1_hits_dist = Counter()
for s in typh:
    genes = per_iso[s]['genes']
    # AMRFinderPlus renames some alleles - check both blaCARB-2 and CARB-2 forms
    normalized = set()
    for g in genes:
        normalized.add(g)
        if g.startswith('blaCARB'): normalized.add('blaCARB-2')
        if g in ('tetG','tet(G)'): normalized.add('tet(G)')
    hits = sgi1_markers & normalized
    sgi1_hits_dist[len(hits)] += 1
    if len(hits) == 5:
        sgi1_count += 1
print(f"\n[SGI-1 penta-marker in Typh/monophasic] full-set carriage: {sgi1_count}/{len(typh)}")
print(f"marker-hit distribution: {dict(sorted(sgi1_hits_dist.items()))}")
print("Paper reports: 9/10 Typhimurium carry SGI-1 (aadA2, blaCARB-2, floR, sul1, tetG)")

# ---- Widespread mutations audit ----
# Paper: all 77 have gyrA/gyrB/parE QRDR mutations; all have soxRS mutations; all have pmrAB; 68/77 acrB
print("\n[Widespread point mutations audit]")
targets = {
    'gyrA (any POINT)': lambda r: r['Element symbol'].startswith('gyrA') and r['Subtype']=='POINT' and 'WILDTYPE' not in r['Element name'],
    'gyrB (any POINT)': lambda r: r['Element symbol'].startswith('gyrB') and r['Subtype']=='POINT' and 'WILDTYPE' not in r['Element name'],
    'parE (any POINT)': lambda r: r['Element symbol'].startswith('parE') and r['Subtype']=='POINT' and 'WILDTYPE' not in r['Element name'],
    'parC (any POINT)': lambda r: r['Element symbol'].startswith('parC') and r['Subtype']=='POINT' and 'WILDTYPE' not in r['Element name'],
    'ramR (any)':       lambda r: r['Element symbol'].startswith('ramR') and 'WILDTYPE' not in r['Element name'],
    'acrB (any)':       lambda r: r['Element symbol'].startswith('acrB') and 'WILDTYPE' not in r['Element name'],
    'soxR (any)':       lambda r: r['Element symbol'].startswith('soxR') and 'WILDTYPE' not in r['Element name'],
    'soxS (any)':       lambda r: r['Element symbol'].startswith('soxS') and 'WILDTYPE' not in r['Element name'],
    'pmrA (any)':       lambda r: r['Element symbol'].startswith('pmrA') and 'WILDTYPE' not in r['Element name'],
    'pmrB (any)':       lambda r: r['Element symbol'].startswith('pmrB') and 'WILDTYPE' not in r['Element name'],
}
# Combine amr + mut records for per-isolate mutation catalog
for name, pred in targets.items():
    count = 0
    for samn in sub_iso:
        recs = list(amr_calls[samn]) + list(mut_calls[samn])
        if any(pred(r) for r in recs):
            count += 1
    print(f"  {name}: {count}/{len(sub_iso)} ({count/len(sub_iso)*100:.0f}%)")

# ---- ramR-MDR association (paper: chi2=17.7, p<0.0001) ----
ramR_mdr = 0; ramR_no = 0; no_ramR_mdr = 0; no_ramR_no = 0
for samn in sub_iso:
    has_ramR = any(r['Element symbol'].startswith('ramR') and 'WILDTYPE' not in r['Element name']
                   for r in list(amr_calls[samn]) + list(mut_calls[samn]))
    is_mdr = per_iso[samn]['nclasses'] >= 3
    if has_ramR:
        if is_mdr: ramR_mdr += 1
        else: ramR_no += 1
    else:
        if is_mdr: no_ramR_mdr += 1
        else: no_ramR_no += 1
table = [[ramR_mdr, ramR_no], [no_ramR_mdr, no_ramR_no]]
chi2, p, _, _ = stats.chi2_contingency(table, correction=False) if all(sum(r) for r in table) else (float('nan'), float('nan'), None, None)
print(f"\n[ramR mutation vs MDR] ramR+ MDR/nonMDR: {ramR_mdr}/{ramR_no} | ramR- MDR/nonMDR: {no_ramR_mdr}/{no_ramR_no}")
print(f"chi2={chi2:.2f}, p={p:.4g}  (paper: chi2=17.7, p<0.0001)")

# ---- write JSON summary ----
summary = {
    "n_reanalyzed": len(sub_iso),
    "n_paper": len(iso),
    "n_missing_no_ncbi_assembly": len(iso) - len(sub_iso),
    "top_amr_genes_reanalysis": gene_count.most_common(25),
    "mdr_count_reanalysis": mdr,
    "mdr_pct_reanalysis": round(mdr/len(per_iso)*100, 1),
    "paper_mdr_pct": 26,
    "LN_vs_GB": {
        "LN_MDR": ln_mdr, "LN_nonMDR": ln_no,
        "GB_MDR": gb_mdr, "GB_nonMDR": gb_no,
        "our_chi2": round(float(chi2c),2), "our_p": float(pc),
        "our_fisher_OR": round(float(odds_ratio),2), "our_fisher_p": float(fisher_p),
        "paper_chi2": 12.0, "paper_p": 0.0005, "paper_OR": 6.5
    },
    "typhimurium": {
        "n": len(typh), "n_MDR": tt,
        "SGI1_5marker_hits": sgi1_count,
        "SGI1_hit_distribution": dict(sgi1_hits_dist),
        "paper_SGI1_count": "9/10"
    }
}
with open(f"{WORK}/../report/evidence/replication_summary.json","w") as f:
    json.dump(summary, f, indent=2)
print(f"\nWrote report/evidence/replication_summary.json")
