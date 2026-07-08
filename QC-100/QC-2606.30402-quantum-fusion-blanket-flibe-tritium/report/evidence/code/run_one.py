#!/usr/bin/env python3
"""run_one.py SYSTEM CLUSTER -- run the full-molecule ladder for a single conformer.
Writes results/one_<system>_c<cluster>.json. Designed for parallel launch (1 per proc)."""
import os, json, sys, time
os.environ.setdefault("OMP_NUM_THREADS","6")
import run_ladder as R
sysname=sys.argv[1]; c=int(sys.argv[2])
info=R.SYSTEMS[sysname]
xyz=f"clusters/{sysname}/{sysname}_c{c}.xyz"
t0=time.time()
r=R.run_conformer(xyz, info["charge"], info["spin"], do_ccsd=("--ccsd" in sys.argv))
r["cluster"]=c
os.makedirs("results",exist_ok=True)
with open(f"results/one_{sysname}_c{c}.json","w") as f: json.dump(r,f,indent=2)
print(f"DONE {sysname} c{c}: RHF={r.get('RHF')} MP2={r.get('MP2')} PBE-D3={r.get('PBE-D3')} "
      f"CCSD={r.get('CCSD')} T1={r.get('T1_diagnostic')} ({round(time.time()-t0,1)}s)",flush=True)
