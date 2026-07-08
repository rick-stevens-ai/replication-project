"""
Match the paper's (H2)2 basis choice (6-31G, active space (4,4) per Sec. III.A)
for the LAS-surrogate: at 6-31G, LASSCF should visibly fail chemical accuracy
at short r_inter, while full CASCI(4,4) is still exact within the active space.
This mirrors Fig. 3's inset.
Note: CAS(4,4)/6-31G for H4 is still classically tractable so we can compute
the CASCI reference exactly.
"""
import json
from pathlib import Path
from pyscf import gto, scf, fci, mcscf
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EVID = ROOT / "report" / "evidence"

def build_h4(r_intra, r_inter):
    z0 = 0.0; z1 = r_intra; z2 = r_intra + r_inter; z3 = r_intra + r_inter + r_intra
    return [("H", (0., 0., z0)),
            ("H", (0., 0., z1)),
            ("H", (0., 0., z2)),
            ("H", (0., 0., z3))]

def las_product_h4(r_intra, r_inter, basis="6-31g"):
    # Dimer
    mol4 = gto.M(atom=build_h4(r_intra, r_inter), basis=basis, verbose=0)
    mf4 = scf.RHF(mol4).run(verbose=0)
    e_hf4 = mf4.e_tot
    # CASCI(4,4) reference on the dimer
    mc = mcscf.CASCI(mf4, ncas=4, nelecas=4)
    e_casci = mc.kernel()[0]
    # Monomer
    mol2 = gto.M(atom=[("H",(0,0,0)),("H",(0,0,r_intra))], basis=basis, verbose=0)
    mf2 = scf.RHF(mol2).run(verbose=0)
    e_hf2 = mf2.e_tot
    mc2 = mcscf.CASCI(mf2, ncas=2, nelecas=2)
    e_cas2 = mc2.kernel()[0]
    v_inter_mf = e_hf4 - 2.0 * e_hf2
    e_las = 2.0 * e_cas2 + v_inter_mf
    return {
        "basis": basis,
        "r_intra": r_intra,
        "r_inter": r_inter,
        "e_hf_dimer": e_hf4,
        "e_casci_dimer_full": e_casci,
        "e_hf_monomer": e_hf2,
        "e_casci_monomer": e_cas2,
        "e_las_product_surrogate": e_las,
        "err_las_vs_casci_mHa": (e_las - e_casci) * 1e3,
    }

def main():
    out = {"description": "LASSCF-surrogate vs CASCI(4,4) for (H2)2 at 6-31G (paper basis)"}
    out["geometries"] = []
    for label, r_intra, r_inter in [
        ("very_short", 0.74, 0.6),
        ("short", 0.74, 1.0),
        ("equilibrium", 0.74, 1.5),
        ("long", 0.74, 3.0),
        ("very_long", 0.74, 5.0),
    ]:
        res = las_product_h4(r_intra, r_inter, basis="6-31g")
        res["label"] = label
        print(f"{label:12s}  r_inter={r_inter}  E_CASCI={res['e_casci_dimer_full']:.6f}  "
              f"E_LAS_prod={res['e_las_product_surrogate']:.6f}  "
              f"err_LAS_vs_CASCI={res['err_las_vs_casci_mHa']:+.3f} mHa")
        out["geometries"].append(res)
    p = EVID / "las_6-31g.json"
    p.write_text(json.dumps(out, indent=2))
    print("wrote", p)

if __name__ == "__main__":
    main()
