#!/usr/bin/env python3
"""
run_ewf_frag.py -- EWF fragmentation with per-fragment solver dispatch mirroring the
paper (arXiv:2606.30402): FCI for small fragments, simulated ext-SQD for large ones.

For each cluster:
  1. RHF/6-31+G*  -> Vayesta EWF, IAO fragmentation (1 frag/atom), MP2 BNO bath eta=1e-5.
  2. For EVERY fragment, obtain a PySCF mean-field object in the embedded cluster space
     via Vayesta's RClusterHamiltonian.to_pyscf_mf().
  3. Solve each fragment three ways:
        - CCSD              (always)
        - FCI               (only if determinant space tractable)
        - SQD-sim           (genuine LUCJ+SQD on a simulator for M<=16, else selected-CI)
  4. Report per-fragment CCSD/FCI/SQD-sim energies -> measure SQD-vs-FCI agreement claim.
  5. Report Vayesta's own EWF-CCSD total as the embedded reference.

No IBM hardware: the ext-SQD quantum step is simulated (statevector sampler / selected-CI).
Outputs: results/frag_<system>.json
"""
import os, json, time, sys, math
import numpy as np
from pyscf import gto, scf, fci, cc, ao2mo

BASIS="6-31+g*"
RESDIR="results"; os.makedirs(RESDIR,exist_ok=True)
ETA=1e-5
FCI_DET_CAP=3_000_000
HARTREE2KCAL=627.5094740631

SYSTEMS={"FLiBe":{"charge":0,"spin":0},
         "FLiBeF":{"charge":-1,"spin":0},
         "FLiBeTF":{"charge":0,"spin":0}}

def read_xyz(path):
    atoms=[]
    with open(path) as f:
        n=int(f.readline()); f.readline()
        for _ in range(n):
            p=f.readline().split(); atoms.append((p[0],float(p[1]),float(p[2]),float(p[3])))
    return atoms

def build_mol(atoms,chg,spin):
    mol=gto.Mole(); mol.atom=[(a[0],(a[1],a[2],a[3])) for a in atoms]
    mol.basis=BASIS; mol.charge=chg; mol.spin=spin
    mol.verbose=1; mol.max_memory=200000; mol.build(); return mol

def rhf(mol):
    mf=scf.RHF(mol).density_fit(); mf.conv_tol=1e-9; mf.level_shift=0.2; mf.max_cycle=200
    mf.kernel()
    if not mf.converged:
        mf=mf.newton(); mf.max_cycle=100; mf.kernel(mf.make_rdm1())
    if not mf.converged:
        mf.level_shift=0.0; mf.kernel(mf.make_rdm1())
    return mf

def frag_mf(frag):
    """PySCF RHF for the embedded fragment via Vayesta RClusterHamiltonian.to_pyscf_mf()."""
    ham=frag.hamil
    clus=frag.cluster
    norb=int(clus.norb_active); na=int(clus.nocc_active)
    mf=ham.to_pyscf_mf()
    try:
        if not getattr(mf,'converged',True):
            mf.max_cycle=200; mf.conv_tol=1e-10; mf.kernel()
    except Exception:
        pass
    return mf, norb, na

def det_count(norb,na):
    try: return math.comb(norb,na)
    except Exception: return 10**18

def solve_fci_mf(mf):
    cis=fci.FCI(mf); cis.max_cycle=300; cis.conv_tol=1e-10
    return float(cis.kernel()[0])

def solve_ccsd_mf(mf):
    mycc=cc.CCSD(mf); mycc.max_cycle=120; mycc.conv_tol=1e-7
    mycc.kernel()
    return float(mf.e_tot+mycc.e_corr), bool(mycc.converged), mycc

def mo_integrals(mf, norb):
    ecore=float(mf.energy_nuc())
    h1_mo=mf.mo_coeff.T @ mf.get_hcore() @ mf.mo_coeff
    eri=mf._eri
    if eri is None:
        eri=mf.mol.intor('int2e')
    h2_mo=ao2mo.restore(1, ao2mo.full(eri, mf.mo_coeff), norb)
    return h1_mo, h2_mo, ecore

def solve_sqd_sim(mf, norb, na, mycc=None, shots=100000, seed=0):
    """Simulated ext-SQD. LUCJ+SQD on statevector sim for M<=16; selected-CI otherwise."""
    h1_mo,h2_mo,ecore=mo_integrals(mf,norb)
    nelec=(na,na); last=""
    if norb<=16:
        try:
            import ffsim
            from qiskit_addon_sqd.fermion import solve_fermion
            if mycc is None:
                _,_,mycc=solve_ccsd_mf(mf)
            ucj=ffsim.UCJOpSpinBalanced.from_t_amplitudes(mycc.t2, t1=mycc.t1, n_reps=1)
            ref=ffsim.hartree_fock_state(norb,nelec)
            psi=ffsim.apply_unitary(ref, ucj, norb=norb, nelec=nelec)
            addr=ffsim.sample_state_vector(psi, norb=norb, nelec=nelec, shots=shots, seed=seed)
            bs=np.array([[int(c) for c in s] for s in addr], dtype=bool)
            res=solve_fermion(bs, h1_mo, h2_mo, open_shell=False)
            return float(res[0])+ecore, "LUCJ+SQD(sim,shots=%d)"%shots
        except Exception as ex:
            last=str(ex)[:150]
    else:
        last="M>16"
    try:
        from pyscf.fci import selected_ci_spin0 as sci
        s=sci.SCI(); s.select_cutoff=1e-4; s.ci_coeff_cutoff=1e-4
        e,_=s.kernel(h1_mo,h2_mo,norb,(na,na),ecore=ecore)
        return float(e), "selectedCI(sim-SQD; %s)"%last
    except Exception as ex2:
        return None, "SQD-sim-FAILED: %s"%str(ex2)[:120]

def run_cluster(xyz, chg, spin):
    from vayesta import ewf
    atoms=read_xyz(xyz); mol=build_mol(atoms,chg,spin); mf=rhf(mol)
    out={"xyz":os.path.basename(xyz),"nao":mol.nao_nr(),"RHF":float(mf.e_tot),
         "RHF_converged":bool(mf.converged)}
    emb=ewf.EWF(mf, bath_options=dict(threshold=ETA), solver='CCSD')
    with emb.iao_fragmentation() as f: f.add_all_atomic_fragments()
    emb.kernel()
    out["EWF-CCSD_total"]=float(emb.e_tot)
    frags=[]
    for i,frag in enumerate(emb.fragments):
        rec={"idx":i,"atom":getattr(frag,'name','?')}
        try:
            mf_f,norb,na=frag_mf(frag)
            rec["norb"]=norb; rec["na"]=na; rec["dets_per_spin"]=det_count(norb,na)
            try:
                e_cc,conv,mycc=solve_ccsd_mf(mf_f); rec["E_CCSD"]=e_cc; rec["CCSD_conv"]=conv
            except Exception as ex:
                rec["E_CCSD"]=None; rec["CCSD_err"]=str(ex)[:100]; mycc=None
            if det_count(norb,na)<=FCI_DET_CAP:
                try: rec["E_FCI"]=solve_fci_mf(mf_f)
                except Exception as ex: rec["E_FCI"]=None; rec["FCI_err"]=str(ex)[:100]
            else:
                rec["E_FCI"]=None; rec["FCI_skip"]="too_large"
            try:
                e_sqd,meth=solve_sqd_sim(mf_f,norb,na,mycc=mycc)
                rec["E_SQDsim"]=e_sqd; rec["SQD_method"]=meth
            except Exception as ex:
                rec["E_SQDsim"]=None; rec["SQD_err"]=str(ex)[:120]
        except Exception as ex:
            rec["frag_err"]=str(ex)[:150]
        frags.append(rec)
    out["fragments"]=frags
    return out

def main():
    which=sys.argv[1] if len(sys.argv)>1 else "all"
    targets=SYSTEMS.keys() if which=="all" else [which]
    for sysname in targets:
        info=SYSTEMS[sysname]; res=[]
        for c in range(1,10):
            xyz=f"clusters/{sysname}/{sysname}_c{c}.xyz"
            if not os.path.exists(xyz): continue
            print(f"[{sysname} c{c}] ...",flush=True); t0=time.time()
            try:
                r=run_cluster(xyz, info["charge"], info["spin"]); r["cluster"]=c
            except Exception as ex:
                r={"cluster":c,"error":str(ex)[:200]}
            r["walltime_s"]=round(time.time()-t0,1)
            res.append(r)
            with open(f"{RESDIR}/frag_{sysname}.json","w") as f: json.dump(res,f,indent=2)
            nf=len(r.get("fragments",[]))
            print(f"   EWF-CCSD={r.get('EWF-CCSD_total')} nfrag={nf} ({r['walltime_s']}s)",flush=True)
    print("Frag solve done.")

if __name__=="__main__":
    main()
