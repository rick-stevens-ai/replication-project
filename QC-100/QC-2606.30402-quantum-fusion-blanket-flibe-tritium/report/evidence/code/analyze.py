#!/usr/bin/env python3
"""
analyze.py -- Post-process FLiBe replication results into the paper's comparison tables.
Reproduces (qualitatively) the central claims of arXiv:2606.30402:
  * T1 diagnostics -> single-reference character (paper: 0.014-0.016)
  * Conformational relative energies (System 1) full-molecule vs EWF
  * Tritium binding energies E_bind = E(FLiBeTF) - E(FLiBeF-) across methods
  * SQD-sim vs FCI agreement at the fragment level (paper: MAD 0.3, max 0.7 kcal/mol)
  * embedding-vs-fullmolecule offset (paper: ~11-12 conformational, ~110 binding kcal/mol)
Outputs: results/analysis.json + prints tables.
"""
import json, os, glob
import numpy as np
H2K=627.5094740631
R="results"

def load(sysn):
    p=f"{R}/ladder_{sysn}.json"
    return json.load(open(p)) if os.path.exists(p) else []

def loadfrag(sysn):
    p=f"{R}/frag_{sysn}.json"
    return json.load(open(p)) if os.path.exists(p) else []

def col(rows, key):
    return {r["cluster"]: r.get(key) for r in rows}

def main():
    out={}
    flibe=load("FLiBe"); flibef=load("FLiBeF"); flibetf=load("FLiBeTF")

    # --- T1 diagnostics ---
    t1={r["cluster"]: r.get("T1_diagnostic") for r in flibe if r.get("T1_diagnostic") is not None}
    out["T1_diagnostic_FLiBe"]=t1
    if t1:
        vals=[v for v in t1.values() if v]
        out["T1_range"]=[min(vals),max(vals)]
        print(f"T1 diagnostic (FLiBe): range {min(vals):.4f}-{max(vals):.4f} "
              f"(paper: 0.014-0.016; <0.02 => single-reference)")

    # --- Conformational relative energies (System 1) vs cluster 1 ---
    methods=["RHF","MP2","CCSD","PBE-D3","B3LYP","PBE0"]
    conf={}
    for m in methods:
        c=col(flibe,m)
        if c.get(1) is None: continue
        rel={k:(v-c[1])*H2K for k,v in c.items() if v is not None}
        conf[m]=rel
    out["conformational_relE_kcal"]=conf
    print("\n=== Conformational relative energies (kcal/mol, ref=cluster1) ===")
    print("cluster " + " ".join(f"{m:>10}" for m in conf))
    for cl in sorted(set().union(*[set(v) for v in conf.values()])) if conf else []:
        print(f"  {cl:>3}   " + " ".join(f"{conf[m].get(cl,float('nan')):>10.2f}" for m in conf))

    # --- Tritium binding energies E_bind = E(FLiBeTF) - E(FLiBeF-) ---
    print("\n=== Tritium binding energies Ebind (kcal/mol) ===")
    bind={}
    for m in methods:
        tf=col(flibetf,m); an=col(flibef,m)
        row={}
        for cl in range(1,10):
            if tf.get(cl) is not None and an.get(cl) is not None:
                row[cl]=(tf[cl]-an[cl])*H2K
        if row: bind[m]=row
    out["Ebind_kcal_fullmolecule"]=bind
    print("cluster " + " ".join(f"{m:>10}" for m in bind))
    allcl=sorted(set().union(*[set(v) for v in bind.values()])) if bind else []
    for cl in allcl:
        print(f"  {cl:>3}   " + " ".join(f"{bind[m].get(cl,float('nan')):>10.1f}" for m in bind))
    # summary range
    allvals=[v for row in bind.values() for v in row.values()]
    if allvals:
        out["Ebind_range_fullmol"]=[min(allvals),max(allvals)]
        print(f"\nFull-molecule Ebind range: {min(allvals):.0f} to {max(allvals):.0f} kcal/mol "
              f"(paper full-molecule band: -222 to -380)")

    # --- Fragment SQD-sim vs FCI agreement ---
    print("\n=== Fragment-level SQD-sim vs FCI agreement ===")
    fragcmp={}
    for sysn in ["FLiBe","FLiBeF","FLiBeTF"]:
        fr=loadfrag(sysn); diffs=[]
        for clus in fr:
            for f in clus.get("fragments",[]):
                efci=f.get("E_FCI"); esqd=f.get("E_SQDsim")
                if efci is not None and esqd is not None:
                    diffs.append(abs(esqd-efci)*H2K)
        if diffs:
            fragcmp[sysn]={"n":len(diffs),"MAD":float(np.mean(diffs)),
                           "max":float(np.max(diffs))}
            print(f"  {sysn}: n={len(diffs)} frags with both, "
                  f"MAD={np.mean(diffs):.3f} max={np.max(diffs):.3f} kcal/mol "
                  f"(paper: MAD 0.3, max 0.7)")
    out["SQDsim_vs_FCI_kcal"]=fragcmp

    # --- EWF totals vs full-molecule (embedding offset) ---
    print("\n=== EWF-CCSD total vs full-molecule CCSD (embedding offset) ===")
    emb={}
    for sysn,rows in [("FLiBe",flibe),("FLiBeF",flibef),("FLiBeTF",flibetf)]:
        fr=loadfrag(sysn)
        ewf={c["cluster"]:c.get("EWF-CCSD_total") for c in fr}
        full=col(rows,"CCSD")
        off={}
        for cl in range(1,10):
            if ewf.get(cl) is not None and full.get(cl) is not None:
                off[cl]=(ewf[cl]-full[cl])*H2K
        if off:
            emb[sysn]={"offsets_kcal":off,"mean":float(np.mean(list(off.values())))}
            print(f"  {sysn}: mean EWF-CCSD - CCSD offset = {np.mean(list(off.values())):.1f} kcal/mol")
    out["embedding_offset_kcal"]=emb

    json.dump(out, open(f"{R}/analysis.json","w"), indent=2)
    print("\nWrote results/analysis.json")

if __name__=="__main__":
    main()
