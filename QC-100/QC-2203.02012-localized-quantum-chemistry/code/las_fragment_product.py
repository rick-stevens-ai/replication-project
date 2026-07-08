"""
Complement to the main VQE replication: compute an approximate LASSCF-style
"fragment-product" energy for (H2)2. Each H2 fragment is treated as an
independent CAS(2,2), and we form the non-interacting-fragment product energy
using localized orbitals per fragment. This mirrors the paper's LASSCF entry
(the "before UCC" reference in LAS-UCC) — it should:
  - be a good approximation at LARGE H2-H2 separation
  - degrade at SHORT separation (loss of interfragment correlation)
whereas the full CASCI/FCI and full-orbital VQE reproduce chemical accuracy at
all separations. This is exactly the qualitative story in Fig. 3 of the paper.
"""
import json
from pathlib import Path
from pyscf import gto, scf, fci, lo, ao2mo, mcscf
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EVID = ROOT / "report" / "evidence"

def build_h4(r_intra=0.74, r_inter=1.5):
    z0 = 0.0; z1 = r_intra; z2 = r_intra + r_inter; z3 = r_intra + r_inter + r_intra
    return [("H", (0., 0., z0)),
            ("H", (0., 0., z1)),
            ("H", (0., 0., z2)),
            ("H", (0., 0., z3))]

def h2_fci_energy(r):
    """FCI energy of an isolated H2 at bond length r (Angstrom), STO-3G."""
    mol = gto.M(atom=[("H",(0,0,0)),("H",(0,0,r))], basis="sto-3g", verbose=0)
    mf = scf.RHF(mol).run(verbose=0)
    e_fci, _ = fci.FCI(mf).kernel()
    return e_fci

def las_product_h4(r_intra, r_inter):
    """Approximate LASSCF-style energy for (H2)2: E_LAS ≈ 2 * E_FCI(H2) + V_inter_MF
    where V_inter_MF is the mean-field (RHF) interaction correction estimated as
    E_HF[(H2)2] - 2 * E_HF[H2]. That is, we take the intra-fragment part exactly
    (per-fragment FCI) and the inter-fragment part at mean-field level.
    This is a cheap surrogate for LASSCF's non-interacting-fragment product wave
    function evaluated in the full 4-orbital LAS basis.
    """
    # Full (H2)2 RHF
    mol4 = gto.M(atom=build_h4(r_intra, r_inter), basis="sto-3g", verbose=0)
    mf4 = scf.RHF(mol4).run(verbose=0)
    e_hf4 = mf4.e_tot
    # Single H2 RHF
    mol2 = gto.M(atom=[("H",(0,0,0)),("H",(0,0,r_intra))], basis="sto-3g", verbose=0)
    mf2 = scf.RHF(mol2).run(verbose=0)
    e_hf2 = mf2.e_tot
    e_fci2 = fci.FCI(mf2).kernel()[0]
    # Full FCI for reference (= CASCI(4,4) with STO-3G on H4)
    e_fci4 = fci.FCI(mf4).kernel()[0]
    # LAS product energy (surrogate)
    v_inter_mf = e_hf4 - 2.0 * e_hf2
    e_las = 2.0 * e_fci2 + v_inter_mf
    return {
        "r_intra": r_intra,
        "r_inter": r_inter,
        "e_hf_dimer": e_hf4,
        "e_hf_monomer": e_hf2,
        "e_fci_monomer": e_fci2,
        "e_fci_dimer_full": e_fci4,
        "e_las_product_surrogate": e_las,
        "err_las_vs_fci_mHa": (e_las - e_fci4) * 1e3,
    }

def main():
    out = {"description": "LASSCF-surrogate for (H2)2 at 3 separations"}
    out["geometries"] = []
    for label, r_intra, r_inter in [
        ("short", 0.74, 1.0),
        ("equilibrium", 0.74, 1.5),
        ("long", 0.74, 3.0),
    ]:
        res = las_product_h4(r_intra, r_inter)
        res["label"] = label
        print(f"{label:12s}  r_inter={r_inter}  E_FCI_full={res['e_fci_dimer_full']:.6f}  "
              f"E_LAS_prod={res['e_las_product_surrogate']:.6f}  "
              f"err_LAS_vs_FCI={res['err_las_vs_fci_mHa']:+.3f} mHa")
        out["geometries"].append(res)
    p = EVID / "las_fragment_product.json"
    p.write_text(json.dumps(out, indent=2))
    print("wrote", p)

if __name__ == "__main__":
    main()
