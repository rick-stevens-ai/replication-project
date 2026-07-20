#!/usr/bin/env python3
"""
C4 (strong test): impose the paper's Table-I converged complex bond order
parameters directly into the 2x2 mean-field Bloch Hamiltonian and compute the
total Chern number of the 5 occupied bands (nvH = 5/12 -> 5 of 12 bands).

Rationale: the self-consistent HF in kagome_tV1V2.py collapses to the trivial
real (ISD) state without the paper's symmetric-correction subtraction scheme,
so it cannot self-stabilize the metastable LC states. But we can still test the
paper's TOPOLOGICAL claim (C4) directly: take the paper's OWN reported converged
bond values (Table I) as the mean field and ask whether they produce the claimed
orbital-Chern-insulator band topology (nonzero total Chern, gapped) vs the ISD
real state (Chern 0).

We assign the three C6 nn bond classes chi1,chi2,chi3 and three nnn classes
chi'1,chi'2,chi'3 to the 24 nn / 24 nnn supercell bonds using the triangle
geometry. The class of an nn bond is decided by which triangular plaquette type
it borders; the sign (current direction) is set by the paper's LC1..4 rule
(flip chi2 for LC2 etc.) via the ORIENTATION of the directed bond within its
up/down triangle. This is an approximate realization of Fig. 2's labeling but
preserves the two physical ingredients the Chern number depends on: (i) the
complex phase pattern (loop currents) and (ii) the C6/2x2 modulation.
"""
from __future__ import annotations
import numpy as np
import kagome_tV1V2 as M

# Paper Table I converged bonds (vH filling n=5/12).
TABLE_I = {
    "ISD": dict(V=(2.0,1.0), chi=[0.631, 0.636, 0.181],
                chip=[0.007, 0.025, -0.071]),
    "LC1": dict(V=(0.5,2.5), chi=[0.255+0.045j, 0.411+0.015j, 0.381+0.060j],
                chip=[-0.115-0.450j, 0.037+0.294j, -0.004+0.050j], N=1),
    "LC2": dict(V=(0.8,1.6), chi=[0.378+0.069j, 0.375-0.069j, 0.490+0.064j],
                chip=[-0.060-0.109j, -0.068+0.075j, -0.001+0.095j], N=-1),
    "LC3": dict(V=(2.0,3.0), chi=[0.453+0.161j, 0.162+0.047j, 0.348-0.205j],
                chip=[0.087+0.235j, -0.279-0.421j, 0.045+0.020j], N=0),
    "LC4": dict(V=(2.0,2.5), chi=[0.179+0.334j, 0.359-0.182j, 0.466-0.022j],
                chip=[-0.181-0.114j, 0.053-0.127j, 0.018+0.235j], N=-1),
}


def _classify_bonds(sc):
    """Assign each of the 24 nn bonds to a class in {0,1,2} (chi1,chi2,chi3) and
    each of the 24 nnn bonds to a class in {0,1,2} (chi'1,chi'2,chi'3), using a
    C3-symmetric rule based on the sublattice pair of the bond. The kagome nn
    bond connects sublattice pair (AB),(BC),(CA); we fold the 2x2 modulation so
    that the three pair types map to the three C6 classes, and the up- vs down-
    triangle orientation sets the intra-class sign (current direction)."""
    nn_class = []
    nn_sign = []
    for (i, j, R) in sc.nn:
        si = sc.sites[i][2]; sj = sc.sites[j][2]
        pair = tuple(sorted((si, sj)))
        cls = {(0,1):0, (1,2):1, (0,2):2}[pair]
        # up-triangle (R=(0,0)) -> +1, down-triangle (R!=0) -> alternate sign
        sgn = +1 if R == (0,0) else -1
        nn_class.append(cls); nn_sign.append(sgn)
    nnn_class = []
    nnn_sign = []
    for (i, j, R) in sc.nnn:
        si = sc.sites[i][2]; sj = sc.sites[j][2]
        pair = tuple(sorted((si, sj)))
        cls = {(0,1):0, (1,2):1, (0,2):2}[pair]
        sgn = +1 if (R[0]+R[1]) >= 0 else -1
        nnn_class.append(cls); nnn_sign.append(sgn)
    return np.array(nn_class), np.array(nn_sign), np.array(nnn_class), np.array(nnn_sign)


def build_imposed(sc, chi123, chip123, current_flip=(1,1,1)):
    """Build 24-length nn and nnn complex bond arrays from the 3 class values.
    current_flip = per-class sign of the imaginary (current) part -> encodes
    LC1..4 (which classes have reversed current)."""
    nnc, nns, nnnc, nnns = _classify_bonds(sc)
    chi_nn = np.empty(len(sc.nn), complex)
    chi_nnn = np.empty(len(sc.nnn), complex)
    for b in range(len(sc.nn)):
        cls = nnc[b]; sgn = nns[b] * current_flip[cls]
        val = chi123[cls]
        chi_nn[b] = val.real + 1j*sgn*val.imag if isinstance(val, complex) else val
    for b in range(len(sc.nnn)):
        cls = nnnc[b]; sgn = nnns[b] * current_flip[cls]
        val = chip123[cls]
        chi_nnn[b] = val.real + 1j*sgn*val.imag if isinstance(val, complex) else val
    return chi_nn, chi_nnn


def total_gap(sc, chi_nn, chi_nnn, t, V1, V2, filling=5.0/12.0, nk=24, T=0.004):
    b1s, b2s = M.recip(sc.A1, sc.A2)
    nocc = int(round(filling*sc.N))
    gaps = []
    all_e = []
    for m in range(nk):
        for n in range(nk):
            k = (m/nk)*b1s + (n/nk)*b2s
            H = M.build_HF_bloch(sc, chi_nn, chi_nnn, k, t, V1, V2)
            e = np.linalg.eigvalsh(H)
            all_e.append(e)
            gaps.append(e[nocc]-e[nocc-1])
    return float(min(gaps))


if __name__ == "__main__":
    import json, os
    sc = M.Supercell()
    out = {}
    # LC current-flip patterns (which nn classes have reversed current):
    # LC1 all anticlockwise; LC2 flip chi2; LC3 flip chi3; LC4 flip chi2+chi3.
    flips = {"LC1":(1,1,1), "LC2":(1,-1,1), "LC3":(1,1,-1), "LC4":(1,-1,-1)}
    for state in ["ISD","LC1","LC2","LC3","LC4"]:
        d = TABLE_I[state]
        chi123 = [complex(x) for x in d["chi"]]
        chip123 = [complex(x) for x in d["chip"]]
        flip = flips.get(state,(1,1,1))
        chi_nn, chi_nnn = build_imposed(sc, chi123, chip123, current_flip=flip)
        V1,V2 = d["V"]
        C = M.chern_number(sc, chi_nn, chi_nnn, t=1.0, V1=V1, V2=V2, nk=18, T=0.004)
        g = total_gap(sc, chi_nn, chi_nnn, t=1.0, V1=V1, V2=V2, nk=18, T=0.004)
        lf = M.triangle_flux(sc, chi_nn)
        rec = dict(V=[V1,V2], chern_occupied=int(C), indirect_gap=round(g,4),
                   loop_flux=round(lf,4), paper_N=d.get("N"))
        out[state] = rec
        print(f"{state}: Chern={C:+d} (paper N={d.get('N')})  gap={g:.4f}  loop_flux={lf:.4f}")
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","work","imposed_chern.json")
    with open(OUT,"w") as f:
        json.dump(out, f, indent=2)
    print("wrote", OUT)
