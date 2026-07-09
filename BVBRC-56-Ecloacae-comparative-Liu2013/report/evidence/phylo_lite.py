#!/usr/bin/env python3
"""Lightweight phylogenomic check (C8) across 8 Enterobacter + 3 Pantoea outgroup.
Compute proteome-wide AAI (average amino acid identity of reciprocal best hits)
via DIAMOND, build NJ tree from AAI distance, confirm:
 (a) ENHKU01 closest relative = ATCC13047 (paper text)
 (b) Enterobacter cluster distinct from Pantoea outgroup
 (c) overall Enterobacter clade structure sane."""
import subprocess,os,glob,json,itertools
from collections import defaultdict
OUT="/data/stevens/bvbrc56/work"; PDIR=f"{OUT}/proteins"
ALL=["ENHKU01","ATCC13047","EcWSU1","SDM","Eaerogenes_KCTC2190",
     "Elignolyticus_SCF1","Easburiae_LF7a","Enterobacter_sp638",
     "Pantoea_At9b","Pvagans_C91","Pananatis_LMG20103"]

def rbh_aai(a,b):
    da=f"{PDIR}/{a}.faa"; db=f"{PDIR}/{b}.faa"
    o1=f"{OUT}/tmp_{a}_{b}.m8"; o2=f"{OUT}/tmp_{b}_{a}.m8"
    subprocess.run(f"diamond makedb --in {db} -d {OUT}/tmpB --quiet",shell=True,check=True)
    subprocess.run(f"diamond blastp -q {da} -d {OUT}/tmpB -o {o1} --outfmt 6 qseqid sseqid pident length qlen -e 1e-5 -k 1 --quiet --threads 32",shell=True,check=True)
    subprocess.run(f"diamond makedb --in {da} -d {OUT}/tmpA --quiet",shell=True,check=True)
    subprocess.run(f"diamond blastp -q {db} -d {OUT}/tmpA -o {o2} --outfmt 6 qseqid sseqid pident length qlen -e 1e-5 -k 1 --quiet --threads 32",shell=True,check=True)
    best1={}; 
    for ln in open(o1):
        q,s,pid,l,ql=ln.split("\t"); best1[q]=(s,float(pid),int(l),int(ql))
    best2={}
    for ln in open(o2):
        q,s,pid,l,ql=ln.split("\t"); best2[q]=(s,float(pid))
    pids=[]
    for q,(s,pid,l,ql) in best1.items():
        if l/ql>=0.5 and s in best2 and best2[s][0]==q:
            pids.append(pid)
    return (sum(pids)/len(pids) if pids else 0.0, len(pids))

n=len(ALL); aai={}
for a,b in itertools.combinations(ALL,2):
    v,cnt=rbh_aai(a,b)
    aai[(a,b)]=v; aai[(b,a)]=v
    print(f"AAI {a:20s} {b:20s} = {v:.2f}%  (rbh {cnt})")
for a in ALL: aai[(a,a)]=100.0

# closest relative of ENHKU01
others=[(b,aai[("ENHKU01",b)]) for b in ALL if b!="ENHKU01"]
others.sort(key=lambda x:-x[1])
print("\nENHKU01 closest relatives (by AAI):")
for b,v in others[:4]: print(f"   {b:20s} {v:.2f}%")

# build distance matrix + NJ tree via biopython
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix
labels=ALL
mat=[]
for i,a in enumerate(labels):
    row=[]
    for j in range(i+1):
        b=labels[j]
        row.append(round((100.0-aai[(a,b)])/100.0,4))
    mat.append(row)
dm=DistanceMatrix(names=labels, matrix=mat)
tree=DistanceTreeConstructor().nj(dm)
from io import StringIO
from Bio import Phylo
buf=StringIO(); Phylo.write(tree,buf,"newick"); nwk=buf.getvalue()
open(f"{OUT}/enterobacter_aai.nwk","w").write(nwk)
json.dump({f"{a}|{b}":round(v,2) for (a,b),v in aai.items() if a<b},
          open(f"{OUT}/aai_matrix.json","w"),indent=2)
print("\nNEWICK:",nwk)
Phylo.draw_ascii(tree)
