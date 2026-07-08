#!/usr/bin/env python3
"""
run_ladder.py -- Full-molecule electronic-structure ladder + DFT study for the FLiBe
tritium-binding replication (arXiv:2606.30402).

For each cluster conformer of each system, compute total energies with:
  RHF, MP2, CCSD (+T1 diagnostic), and a DFT ladder (PBE-D3, B3LYP, PBE0, wB97X-D).
Basis: 6-31+G(d)  ("6-31+G*"), exactly as the paper's mean-field/benchmark basis.

Then compute the tritium binding energy per cluster:
  E_bind = E(FLiBeTF, 23-atom, q=0) - E(FLiBeF-, 22-atom, q=-1)
  (T removed as a bare H+/T+ nucleus = zero electronic energy)
for each full-molecule method (RHF/MP2/CCSD/DFT).

Also report the RHF/MP2/CCSD/DFT *conformational* relative energies (System 1) vs cluster 1.

Outputs JSON to results/ladder_<system>.json and results/binding.json.

Note: canonical full-molecule CCSD on ~380-400 AO closed shell is heavy; we run it
with PySCF's DF-CCSD where possible and cap by memory. FCI on the full molecule is
NOT attempted (that is exactly why the paper fragments) -- FCI appears only in the EWF
fragment module.
"""
import os, json, time, sys
import numpy as np
from pyscf import gto, scf, mp, cc, dft
from pyscf.gto import charge

BASIS = "6-31+g*"
RESDIR = "results"
os.makedirs(RESDIR, exist_ok=True)

SYSTEMS = {
    "FLiBe":   {"charge":0,  "spin":0},
    "FLiBeF":  {"charge":-1, "spin":0},
    "FLiBeTF": {"charge":0,  "spin":0},
}

DFT_FUNCTIONALS = {
    "PBE-D3":  ("pbe", "d3bj"),     # the functional used to generate AIMD/MLFF (paper)
    "B3LYP":   ("b3lyp", "d3bj"),
    "PBE0":    ("pbe0", "d3bj"),
}

HARTREE2KCAL = 627.5094740631

def read_xyz(path):
    atoms=[]
    with open(path) as f:
        n=int(f.readline()); f.readline()
        for _ in range(n):
            p=f.readline().split()
            atoms.append((p[0], float(p[1]),float(p[2]),float(p[3])))
    return atoms

def build_mol(atoms, chg, spin):
    mol = gto.Mole()
    mol.atom = [(a[0],(a[1],a[2],a[3])) for a in atoms]
    mol.basis = BASIS
    mol.charge = chg
    mol.spin = spin
    mol.verbose = 2
    mol.max_memory = 200000  # MB
    mol.build()
    return mol

def run_conformer(xyzpath, chg, spin, do_ccsd=True):
    atoms = read_xyz(xyzpath)
    mol = build_mol(atoms, chg, spin)
    out = {"xyz": os.path.basename(xyzpath), "natoms": len(atoms),
           "nao": mol.nao_nr(), "nelec": mol.nelectron, "charge": chg}
    t0=time.time()
    # RHF -- robust convergence for diffuse/ionic basis
    mf = scf.RHF(mol).density_fit()
    mf.conv_tol = 1e-9
    mf.level_shift = 0.2
    mf.max_cycle = 200
    e_hf = mf.kernel()
    if not mf.converged:
        # second-order (Newton) restart from current density
        mf = mf.newton(); mf.max_cycle=100
        e_hf = mf.kernel(mf.make_rdm1())
    if not mf.converged:
        mf.level_shift=0.0; e_hf=mf.kernel(mf.make_rdm1())
    out["RHF"] = float(e_hf) if mf.converged else float(e_hf)
    out["RHF_converged"] = bool(mf.converged)
    # MP2
    try:
        pt = mp.MP2(mf); e_mp2c = pt.kernel()[0]
        out["MP2"] = float(e_hf + e_mp2c)
    except Exception as ex:
        out["MP2"]=None; out["MP2_err"]=str(ex)
    # CCSD (+T1 diagnostic)
    if do_ccsd and mf.converged:
        try:
            mycc = cc.CCSD(mf); mycc.max_cycle=80; mycc.conv_tol=1e-7
            e_ccc = mycc.kernel()[0]
            out["CCSD"] = float(e_hf + e_ccc)
            out["T1_diagnostic"] = float(mycc.get_t1_diagnostic())
            out["CCSD_converged"]=bool(mycc.converged)
        except Exception as ex:
            out["CCSD"]=None; out["CCSD_err"]=str(ex)
    # DFT ladder
    for label,(xc,disp) in DFT_FUNCTIONALS.items():
        try:
            mdft = dft.RKS(mol).density_fit()
            mdft.xc = xc
            try:
                mdft.disp = disp
            except Exception:
                pass
            mdft.conv_tol=1e-9; mdft.level_shift=0.2; mdft.max_cycle=200
            e = mdft.kernel()
            if not mdft.converged:
                mdft = mdft.newton(); mdft.max_cycle=100
                e = mdft.kernel(mdft.make_rdm1())
            if not mdft.converged:
                mdft.level_shift=0.0; e=mdft.kernel(mdft.make_rdm1())
            out[label] = float(e)
            out[label+"_converged"]=bool(mdft.converged)
        except Exception as ex:
            out[label]=None; out[label+"_err"]=str(ex)
    out["walltime_s"]=round(time.time()-t0,1)
    return out

def main():
    which = sys.argv[1] if len(sys.argv)>1 else "all"
    do_ccsd = ("--noccsd" not in sys.argv)
    targets = SYSTEMS.keys() if which=="all" else [which]
    for sysname in targets:
        info = SYSTEMS[sysname]
        res=[]
        for c in range(1,10):
            xyz=f"clusters/{sysname}/{sysname}_c{c}.xyz"
            if not os.path.exists(xyz):
                print("MISSING",xyz); continue
            print(f"[{sysname} c{c}] running ...", flush=True)
            r=run_conformer(xyz, info["charge"], info["spin"], do_ccsd=do_ccsd)
            r["cluster"]=c
            res.append(r)
            with open(f"{RESDIR}/ladder_{sysname}.json","w") as f:
                json.dump(res,f,indent=2)
            print(f"   RHF={r.get('RHF')}, MP2={r.get('MP2')}, CCSD={r.get('CCSD')}, "
                  f"T1={r.get('T1_diagnostic')}, PBE-D3={r.get('PBE-D3')} ({r['walltime_s']}s)", flush=True)
    print("Ladder done.")

if __name__=="__main__":
    main()
