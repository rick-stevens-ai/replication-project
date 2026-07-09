#!/usr/bin/env python3
"""
KEGG BRITE category surrogate for BlastKOALA (Table 3 in Kandasamy 2022).

Method:
  1. Parse Pass-1 SwissProt blastp annotation (data/sprot_annotation.tsv)
     to extract EC numbers per CDS (1,720 annotated CDSs).
  2. Parse KEGG REST data:
       - ec_to_pathway.tsv  (ec:1.1.1.1 -> path:map00010)
       - ko00001.json       (BRITE hierarchy: top-level "09100 Metabolism", etc.,
                              with pathway -> KO -> gene mapping)
  3. Build pathway -> top-level BRITE category mapping by walking ko00001.json.
  4. For each EC, find pathways, find their top-level BRITE category, count.
  5. Compare to paper Table 3 (22 KO categories with N genes + %).

LIMITATIONS:
  - BlastKOALA uses KO inference from KEGG GENES (not EC alone). EC->pathway
    is broader (one EC can hit many pathways). This OVER-counts by design.
  - One CDS counts once per top-level BRITE category (deduped per CDS), even
    if its EC maps to many pathways under that category.
  - Hypothetical / no-EC CDSs are NOT included (under-count vs BlastKOALA).
"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

# 1. Parse our CDS annotations -> set of EC numbers
ec_per_cds = {}
with open("data/sprot_annotation.tsv") as fh:
    for line in fh:
        f = line.rstrip("\n").split("\t")
        if len(f) < 6: continue
        locus = f[0]
        info = f[5]
        # info like "P65629 1.1.1.1~~~..."
        m = re.match(r"\S+\s+([0-9.\-]+)~~~", info)
        if m:
            ec = m.group(1)
            # Skip if all dashes
            if ec and "." in ec and not ec.startswith("-"):
                ec_per_cds[locus] = ec

print(f"CDSs with EC: {len(ec_per_cds)}")

# 2. EC -> pathway map
ec_to_paths = defaultdict(set)
with open("results/repass/kegg/ec_to_pathway.tsv") as fh:
    for line in fh:
        ec, p = line.strip().split("\t")
        ec_clean = ec.replace("ec:","")
        path_clean = p.replace("path:","")
        ec_to_paths[ec_clean].add(path_clean)

print(f"ECs in KEGG: {len(ec_to_paths)}")

# 3. BRITE: walk ko00001.json hierarchy
# Top-level "name" e.g. "09100 Metabolism"
# Second level e.g. "09101 Carbohydrate metabolism"
# Third level e.g. "00010 Glycolysis / Gluconeogenesis [PATH:ko00010]"
# Fourth (leaf): "K00844 ..."
ko00001 = json.load(open("results/repass/kegg/ko00001.json"))

# path_id -> (top_level, second_level)
path_to_cats = {}
for top in ko00001.get("children", []):
    top_name = top["name"]   # "09100 Metabolism" / "09120 Genetic information processing" / etc.
    top_id = top_name.split()[0]
    for second in top.get("children", []):
        sec_name = second["name"]
        sec_id = sec_name.split()[0]
        for path in second.get("children", []):
            pname = path["name"]
            # Extract "[PATH:koXXXXX]"  -> "mapXXXXX"
            mm = re.search(r"\[PATH:ko(\d+)\]", pname)
            if mm:
                pid = "map" + mm.group(1)
                path_to_cats[pid] = (top_name, sec_name)

print(f"KEGG pathways mapped to BRITE categories: {len(path_to_cats)}")

# 4. For each CDS, find pathway hits, find unique top-level categories
top_cat_cds = defaultdict(set)    # top_name -> set of CDS
sec_cat_cds = defaultdict(set)    # sec_name -> set of CDS

unassigned_ec = set()
for cds, ec in ec_per_cds.items():
    # Handle "1.1.1.-" partial EC: also match parent ECs
    paths = set()
    if ec in ec_to_paths:
        paths.update(ec_to_paths[ec])
    # parent EC search (1.1.1.- matches all 1.1.1.x)
    if ec.endswith(".-"):
        prefix = ec[:-1]
        for e2 in ec_to_paths:
            if e2.startswith(prefix):
                paths.update(ec_to_paths[e2])
    if not paths:
        unassigned_ec.add(ec)
        continue
    for p in paths:
        if p in path_to_cats:
            top, sec = path_to_cats[p]
            top_cat_cds[top].add(cds)
            sec_cat_cds[sec].add(cds)

print(f"\nUnique CDSs assigned to >=1 BRITE top-level: {sum(1 for s in set().union(*top_cat_cds.values()) for _ in [s])}" if top_cat_cds else "0")
total_unique = len(set().union(*top_cat_cds.values())) if top_cat_cds else 0
print(f"Total unique CDS with any KEGG BRITE call: {total_unique}")

# 5. Per second-level (matches paper Table 3 granularity)
PAPER_TABLE3 = [
    ("09101", "Carbohydrate metabolism", 226, 13.59),
    ("09102", "Energy metabolism", 37, 2.22),
    ("09103", "Lipid metabolism", 39, 2.35),
    ("09104", "Nucleotide metabolism", 68, 4.09),
    ("09105", "Amino acid metabolism", 97, 5.83),
    ("09106", "Metabolism of other amino acids", 20, 1.20),
    ("09107", "Glycan biosynthesis and metabolism", 37, 2.22),
    ("09108", "Metabolism of cofactors and vitamins", 65, 3.91),
    ("09109", "Metabolism of terpenoids and polyketides", 10, 0.60),
    ("09110", "Biosynthesis of secondary metabolites", 5, 0.30),
    ("09111", "Xenobiotics biodegradation and metabolism", 8, 0.48),
    ("09120", "Genetic information processing", 161, 9.68),
    ("09130", "Environmental information processing", 164, 9.86),
    ("09140", "Cellular processes", 11, 0.66),
    ("09150", "Organismal systems", 8, 0.48),
    ("09160", "Human diseases", 3, 0.18),
    ("09181", "Protein families: metabolism", 39, 2.35),
    ("09182", "Protein families: genetic information processing", 229, 13.77),
    ("09183", "Protein families: signaling and cellular processes", 184, 11.06),
    ("09191", "Unclassified: metabolism", 110, 6.61),
]

# Find our sec_cat_cds entries by ID prefix
our_by_id = {}
for sec_name, cds_set in sec_cat_cds.items():
    pid = sec_name.split()[0]
    our_by_id[pid] = len(cds_set)

print(f"\n=== KEGG BRITE second-level (paper Table 3 comparison) ===")
print(f"\n{'ID':>6} {'Category':<55} {'Paper N':>7} {'Paper %':>8} {'Ours N':>7} {'Verdict':<10}")
print("-" * 110)
matches = 0
paper_total = 1660  # ~ sum of Table 3 paper Ns
ours_total = total_unique
for pid, name, pn, pp in PAPER_TABLE3:
    on = our_by_id.get(pid, 0)
    # Within 50% of paper N OR within 5 absolute (good for low-count categories)
    delta = on - pn
    sign = "✅" if abs(delta) <= max(5, 0.4*pn) else ("⚠️" if abs(delta) <= max(15, 0.7*pn) else "❌")
    if abs(delta) <= max(5, 0.4*pn):
        matches += 1
    print(f"{pid:>6} {name:<55} {pn:>7} {pp:>7.2f}% {on:>7} {sign}")

print(f"\nCategories matching within 40% relative or 5 absolute: {matches}/{len(PAPER_TABLE3)}")
print(f"Paper total assigned: ~1669 (52.1% of CDSs); ours: {total_unique}")
print(f"\n=== Top-level summary ===")
for top_name, cds_set in sorted(top_cat_cds.items(), key=lambda x: -len(x[1])):
    print(f"  {top_name}: {len(cds_set)}")

# Save JSON
out = {"total_unique_cds_with_kegg": total_unique,
       "second_level_counts": {pid: our_by_id.get(pid, 0) for pid,_,_,_ in PAPER_TABLE3},
       "top_level_counts": {k: len(v) for k,v in top_cat_cds.items()}}
Path("results/repass/kegg").mkdir(parents=True, exist_ok=True)
with open("results/repass/kegg/kegg_brite_counts.json","w") as fh:
    json.dump(out, fh, indent=2)
