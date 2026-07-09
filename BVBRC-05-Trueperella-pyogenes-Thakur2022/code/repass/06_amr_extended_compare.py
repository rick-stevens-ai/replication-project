#!/usr/bin/env python3
"""Pass-2: extended AMR comparison vs paper claims.

Paper specific AMR claims to test (Section 3.10):
  - 13 of 19 genomes harbour tet(W) (mosaic tet(W/N/W))
  - 7 of 19 genomes harbour ermX
  - No ARG in DSM20630, NCTC5224, Bu5, UFV1
  - Max ARGs in SH01 (6), SH02 (6), TP1 (5)
"""
import os, csv
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022")
AMR = ROOT / "analysis" / "amr"
OUT = ROOT / "results" / "repass"

strains = ["2012CQ-ZSH","Arash114","Bu5","DSM20630","MS249","NCTC5224","SH01","SH02","SH03",
           "TP-2849","TP1","TP2","TP3","TP4","TP4479","TP6375","TP8","UFV1","jx18"]

# Aggregate per-strain ARG genes (CARD)
per_strain = {}
for s in strains:
    p = AMR / f"{s}_card.tsv"
    genes = []
    if p.exists():
        with open(p) as f:
            next(f, None)
            for line in f:
                t = line.rstrip().split("\t")
                if len(t) > 5:
                    genes.append(t[5])
    per_strain[s] = genes

# Has tet(W)? (paper: mosaic tet(W/N/W))
def has_tetW(genes):
    for g in genes:
        if g.lower().startswith("tet(w"):
            return True
    return False

def has_ermX(genes):
    for g in genes:
        if g.lower().replace(" ","") in ("erm(x)", "ermx") or g.lower().startswith("erm(x"):
            return True
    return False

n_tetW = sum(1 for s in strains if has_tetW(per_strain[s]))
n_ermX = sum(1 for s in strains if has_ermX(per_strain[s]))
no_arg_strains = [s for s in strains if not per_strain[s]]

print(f"=== AMR re-pass summary ===")
print(f"Strains analyzed: {len(strains)}")
print(f"tet(W*) carriers: {n_tetW} / 19  (paper: 13/19)")
print(f"ermX  carriers : {n_ermX} / 19  (paper: 7/19)")
print(f"No-ARG strains : {no_arg_strains}  (paper: ['DSM20630','NCTC5224','Bu5','UFV1'])")

print("\nPer-strain ARG count vs paper top-3 (paper: SH01=6, SH02=6, TP1=5)")
counts = [(s, len(per_strain[s])) for s in strains]
counts.sort(key=lambda x: -x[1])
for s, n in counts[:5]:
    print(f"  {s:12s}: {n}  {per_strain[s]}")

# Save TSV
with open(OUT / "amr_extended_compare.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["strain","n_args","args","has_tetW","has_ermX"])
    for s in strains:
        w.writerow([s, len(per_strain[s]), ";".join(per_strain[s]),
                    has_tetW(per_strain[s]), has_ermX(per_strain[s])])

print(f"\nSaved: {OUT/'amr_extended_compare.tsv'}")
