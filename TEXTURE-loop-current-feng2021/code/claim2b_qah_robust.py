"""
claim2b_qah_robust.py
=====================
Robust QAH check for the Nagaosa chiral flux state.

The bare per-band Chern in claim2 is fragile because (i) at some flux values a
pair of bands touches and (ii) numpy sorts eigenvectors by energy so a band
"index" can swap identity across the BZ near touchings. The physically robust,
gauge-invariant statement is:

  For a filled set of bands separated from the rest by a gap, the TOTAL Chern
  number C_tot = sum over filled bands is a well-defined integer equal to the
  quantized anomalous Hall conductance sigma_xy = C_tot e^2/h.

We compute C_tot for n_filled = 1 and n_filled = 2 using a MULTI-BAND
(non-abelian) Fukui-Hatsugai-Suzuki plaquette formula (determinant of the
overlap matrix of the occupied subspace). We verify:
  * plain kagome: every gapped filled set has C_tot = 0 (TRS).
  * Nagaosa flux (pi/2): the lowest band alone is gapped and carries
    |C_tot| = 1  => quantized anomalous Hall (QAH), matching the paper.
"""
import numpy as np
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from kagome_loopcurrent_kernel import KagomeModel, B1, B2

def occ_chern(model, nfill, nk=60):
    """Total Chern of the lowest `nfill` bands via non-abelian FHS."""
    f = np.linspace(0.0, 1.0, nk, endpoint=False)
    # eigenvector blocks (occupied subspace) on the grid
    U = np.empty((nk, nk, 3, nfill), dtype=complex)
    Ev = np.empty((nk, nk, 3))
    for i, u in enumerate(f):
        for j, v in enumerate(f):
            k = u*B1 + v*B2
            w, V = np.linalg.eigh(model.hamiltonian(k[0], k[1]))
            Ev[i, j] = w.real
            U[i, j] = V[:, :nfill]
    def link(a, b):
        M = a.conj().T @ b            # nfill x nfill overlap
        d = np.linalg.det(M)
        return d/abs(d) if abs(d) > 1e-12 else 1.0+0j
    F = 0.0
    for i in range(nk):
        for j in range(nk):
            u1 = U[i, j]; u2 = U[(i+1) % nk, j]
            u3 = U[(i+1) % nk, (j+1) % nk]; u4 = U[i, (j+1) % nk]
            Ux = link(u1, u2); Uy = link(u2, u3)
            Uxp = link(u4, u3); Uyp = link(u1, u4)
            F += np.angle(Ux*Uy/(Uxp*Uyp))
    C = int(np.round(F/(2*np.pi)))
    # gap above the occupied set (min over BZ of E[nfill]-E[nfill-1])
    if nfill < 3:
        gap = float(np.min(Ev[:, :, nfill] - Ev[:, :, nfill-1]))
    else:
        gap = np.inf
    return C, gap

if __name__ == "__main__":
    out = {}
    for label, (flux, patt) in {
        "plain": (0.0, 'none'),
        "nagaosa_pi2": (np.pi/2, 'uniform'),
        "nagaosa_pi3": (np.pi/3, 'uniform'),
    }.items():
        m = KagomeModel(t=1.0, flux=flux, flux_pattern=patt)
        rec = {}
        for nfill in (1, 2):
            C, gap = occ_chern(m, nfill, nk=54)
            rec[f"nfill{nfill}"] = {"C_tot": C, "gap_above": round(gap, 5)}
        out[label] = rec
        print(f"[{label}] flux={flux:.4f}")
        for nfill in (1, 2):
            r = rec[f"nfill{nfill}"]
            print(f"   filled={nfill}: C_tot={r['C_tot']:+d}  gap_above={r['gap_above']:.5f}")

    # verdict
    v = {
        "plain_all_trivial": (out["plain"]["nfill1"]["C_tot"] == 0
                              and out["plain"]["nfill2"]["C_tot"] == 0),
        "nagaosa_lowest_gapped": out["nagaosa_pi2"]["nfill1"]["gap_above"] > 1e-2,
        "nagaosa_QAH_lowest": abs(out["nagaosa_pi2"]["nfill1"]["C_tot"]) == 1,
    }
    out["verdict"] = v
    print("\n=== VERDICT ===")
    print(json.dumps(v, indent=2))
    with open(os.path.join(os.path.dirname(__file__), "..", "work",
              "claim2b_output.json"), "w") as fh:
        json.dump(out, fh, indent=2)
