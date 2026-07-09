#!/usr/bin/env python3
"""V2 replication analysis with corrected mutation parsing.
AMRFinderPlus 4.x outputs *every* residue in the QRDR (both wildtype X_X and
observed mutations X_Y). A true 'mutation' is X != Y at position N.
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from scipy import stats

WORK = "/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-109-Salmonella-AMR-surveillance-cattle-poultry-2021/work"

iso = {}
with open(f"{WORK}/study_isolates.csv") as f:
    for r in csv.DictReader(f):
        iso[r['BioSample']] = r

gca2samn = {}
with open(f"{WORK}/study_assemblies.tsv") as f:
    for r in csv.DictReader(f, delimiter='\t'):
        gca2samn[r['Assembly Accession']] = r['Assembly BioSample Accession']

amr_calls = defaultdict(list)
with open(f"{WORK}/all_amr_calls.tsv") as f:
    for row in csv.DictReader(f, delimiter='\t'):
        samn = gca2samn.get(row['assembly'])
        if samn: amr_calls[samn].append(row)

mut_calls = defaultdict(list)
with open(f"{WORK}/all_mut_calls.tsv") as f:
    for row in csv.DictReader(f, delimiter='\t'):
        samn = gca2samn.get(row['assembly'])
        if samn: mut_calls[samn].append(row)

def is_true_mutation(symbol):
    # symbol like "gyrA_S83Y" -> real; "gyrA_S83S" -> silent
    m = re.match(r'^([a-zA-Z]+)_([A-Z])(\d+)([A-Z])$', symbol)
    if not m: return False
    gene, wt, pos, mt = m.groups()
    return wt != mt

def has_gene_mutation(samn, gene_prefix):
    for r in list(amr_calls[samn]) + list(mut_calls[samn]):
        sym = r['Element symbol']
        if not sym.startswith(gene_prefix + '_'): continue
        if is_true_mutation(sym): return True
    return False

def has_gene_present(samn, gene):
    """AMR gene present (from AMR gene calls, not mutations)"""
    for r in amr_calls[samn]:
        if r['Element symbol'] == gene: return True
    return False

sub_iso = {s: iso[s] for s in amr_calls}
N = len(sub_iso)
print(f"N={N} re-analyzed isolates")

# Per-isolate AMR class set
def isolate_classes(samn):
    cls = set()
    for r in amr_calls[samn]:
        if r['Type']=='AMR' and r['Subtype']!='POINT' and r['Class'] not in ('NA',''):
            cls.add(r['Class'])
    return cls

per_iso_cls = {s: isolate_classes(s) for s in sub_iso}
mdr_set = {s for s,c in per_iso_cls.items() if len(c)>=3}
print(f"\nMDR (>=3 acquired AMR classes) = {len(mdr_set)}/{N} = {len(mdr_set)/N*100:.1f}%")

# ---- Widespread mutations (corrected) ----
print("\n[Widespread mutations, corrected: silent variants excluded]")
for gene in ['gyrA','gyrB','parE','parC','ramR','acrB','soxR','soxS','pmrA','pmrB']:
    n = sum(1 for s in sub_iso if has_gene_mutation(s, gene))
    print(f"  {gene}: {n}/{N} ({n/N*100:.0f}%)")

# ---- ramR mutation vs MDR (correct direction) ----
ramR_pos = {s for s in sub_iso if has_gene_mutation(s, 'ramR')}
ramR_neg = set(sub_iso) - ramR_pos
mdr_ramR_pos = ramR_pos & mdr_set
mdr_ramR_neg = ramR_neg & mdr_set
tbl = [[len(mdr_ramR_pos), len(ramR_pos)-len(mdr_ramR_pos)],
       [len(mdr_ramR_neg), len(ramR_neg)-len(mdr_ramR_neg)]]
print(f"\n[ramR mutation vs MDR]")
print(f"  ramR+ : MDR={tbl[0][0]}, nonMDR={tbl[0][1]}  (n={len(ramR_pos)})")
print(f"  ramR- : MDR={tbl[1][0]}, nonMDR={tbl[1][1]}  (n={len(ramR_neg)})")
chi2, p, _, _ = stats.chi2_contingency(tbl, correction=False)
odds, fp = stats.fisher_exact(tbl)
print(f"  chi2={chi2:.2f}, p={p:.4g}; Fisher OR={odds:.2f}, p={fp:.4g}")
print(f"  Paper: chi2=17.7, p<0.0001; MDR strongly associated with ramR mutation")

# ---- LN vs GB with genotypic MDR ----
ln = [s for s,m in sub_iso.items() if m['Isolation Source']=='Lymph nodes']
gb = [s for s,m in sub_iso.items() if m['Isolation Source']=='Ground beef']
ln_mdr = sum(1 for s in ln if s in mdr_set)
gb_mdr = sum(1 for s in gb if s in mdr_set)
tbl = [[gb_mdr, len(gb)-gb_mdr],[ln_mdr, len(ln)-ln_mdr]]
chi2, p, _, _ = stats.chi2_contingency(tbl, correction=False)
odds, fp = stats.fisher_exact(tbl)
print(f"\n[LN vs GB MDR (genotypic)] LN {ln_mdr}/{len(ln)}, GB {gb_mdr}/{len(gb)}")
print(f"  chi2={chi2:.2f}, p={p:.4g}; Fisher OR(GB vs LN)={odds:.2f}, p={fp:.4g}")
print(f"  Paper (phenotypic): chi2=12.0, p=0.0005, OR=6.5")

# ---- Typhimurium + monophasic ----
typh = {s for s,m in sub_iso.items() if m['Serovar'] in ('Typhimurium','1,4,[5],12:i:-')}
other = set(sub_iso) - typh
t_mdr = sum(1 for s in typh if s in mdr_set)
o_mdr = sum(1 for s in other if s in mdr_set)
tbl = [[t_mdr, len(typh)-t_mdr],[o_mdr, len(other)-o_mdr]]
chi2, p, _, _ = stats.chi2_contingency(tbl, correction=False)
odds, fp = stats.fisher_exact(tbl)
print(f"\n[Typh vs other MDR] Typh {t_mdr}/{len(typh)}, Other {o_mdr}/{len(other)}")
print(f"  chi2={chi2:.2f}, p={p:.4g}; Fisher OR(Typh vs Other)={odds:.2f}, p={fp:.4g}")
print(f"  Paper: chi2=24.5, p<0.0001, OR=45.8")

# ---- SGI-1 penta marker ----
sgi1 = {'aadA2','blaCARB-2','floR','sul1','tet(G)'}
sgi1_full = 0
sgi1_dist = Counter()
per_typh = {}
for s in typh:
    genes = {r['Element symbol'] for r in amr_calls[s]}
    hits = len(genes & sgi1)
    per_typh[s] = (iso[s]['Serovar'], iso[s]['Isolate name'], sorted(genes & sgi1))
    sgi1_dist[hits] += 1
    if hits == 5: sgi1_full += 1
print(f"\n[SGI-1 markers in Typh+monophasic] full 5/5: {sgi1_full}/{len(typh)}")
print(f"  hit distribution: {dict(sorted(sgi1_dist.items()))}")
print(f"  per-isolate details:")
for s, (sv, name, hits) in per_typh.items():
    print(f"    {s} ({sv}, {name}): {len(hits)}/5 -> {hits}")
print(f"  Paper: 9/10 Typhimurium carry all 5 SGI-1 markers")

# ---- Phenotype vs genotype agreement (approx from Fig 2) ----
# Paper Fig 2: strong pearson correlation between # phenotypic-nonsusceptible and # genotypic-nonsusceptible per antibiotic
# Since we don't have phenotype data (not in supplementary), we skip.

# ---- Serovar/ST claim (Kentucky ST-198, Typhimurium ST-19/ST-34) ----
# We'd need to run mlst on the 68 assemblies. Do it quickly.
# (deferred - flag in report)

# ---- Save v2 summary ----
out = {
    "N_reanalyzed": N,
    "N_missing_no_asm": 77 - N,
    "MDR_genotypic_count": len(mdr_set),
    "MDR_genotypic_pct": round(len(mdr_set)/N*100,1),
    "widespread_mutations": {
        gene: sum(1 for s in sub_iso if has_gene_mutation(s, gene))
        for gene in ['gyrA','gyrB','parE','parC','ramR','acrB','soxR','soxS','pmrA','pmrB']
    },
    "ramR_vs_MDR_v2": {
        "ramR_pos_n": len(ramR_pos),
        "ramR_pos_MDR": len(mdr_ramR_pos),
        "ramR_neg_MDR": len(mdr_ramR_neg),
        "our_chi2": round(float(chi2),2),
    },
    "LN_GB_v2": {"LN_MDR": ln_mdr, "LN_n": len(ln), "GB_MDR": gb_mdr, "GB_n": len(gb)},
    "Typh_v2": {"Typh_MDR": t_mdr, "Typh_n": len(typh), "SGI1_full5": sgi1_full,
                "SGI1_dist": dict(sgi1_dist),
                "per_typh_details": {k: v for k,v in per_typh.items()}}
}
with open(f"{WORK}/../report/evidence/replication_summary_v2.json","w") as f:
    json.dump(out, f, indent=2, default=str)
print("\nWrote replication_summary_v2.json")
