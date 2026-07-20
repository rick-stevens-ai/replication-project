#!/usr/bin/env python3
"""
From-scratch replication of Feng, Jiang, Wang, Hu,
"Chiral flux phase in the Kagome superconductor AV3Sb5", arXiv:2103.07097 (2021).

Headline claim (recipe / paper Sec. III):
  For lambda = 0.3, among the three 2x2 (3Q) charge orders that break translation
  down to T(2a1,2a2) -- vCDW, CBO, CFP -- the CHIRAL FLUX PHASE (CFP, imaginary
  bond order = loop current) has the LOWEST ground-state energy at 5/4 van Hove
  filling:  E_CFP is ~0.195 t below CBO and ~0.435 t below vCDW per unit cell.
  CFP breaks time-reversal symmetry and gives an anomalous Hall / Chern insulator.

Model (paper Eqs. 1,4,7,9):
  * NN kagome tight-binding, 3 sublattices A,B,C, t=1 energy unit.
  * 2x2 quadrupled cell (4 sub-cells). Order parameters modulate at the three
    M-point wavevectors Qa,Qb,Qc.
  * vCDW:  onsite     Delta_v(R)   = lambda (cosQa.R, cosQb.R, cosQc.R) . (nA,nB,nC)
  * CBO :  real bond  Delta_CBO(R) = lambda (cosQa.R, cosQb.R, cosQc.R) . (A-B,B-C,C-A)
  * CFP :  imag bond  Delta_CFP(R) = i*lambda (cosQa.R,...) . (A-B,B-C,C-A)  (loop current)

Method: build a real-space L x L kagome cluster with periodic boundary conditions
(L multiple of 2 so the 2x2 order is commensurate), diagonalize, fill to 5/12 of
the states (= 5/4 of the 3 bands), sum occupied single-particle energies, and
report the total energy per ORIGINAL unit cell for each order vs lambda.

Physics kernel credit: geometry / Peierls-flux conventions adapted from the
shared TEXTURES-100 kagome loop-current kernels
  shared-kernels-cache/loop_current_kagome_kernel.py  (KagomeModel, half-bond
      Bloch convention, Fukui-Hatsugai-Suzuki Chern method)
  shared-kernels-cache/loop_current_meanfield_kernel.py (real-space cluster,
      bond-current J_ij = -2 Im[H_ij rho_ji], loop_order probe)
This script builds the 3Q 2x2 supercell orders on top of that geometry.
"""
from __future__ import annotations
import json, sys, os
import numpy as np

SQ3 = np.sqrt(3.0)
A1 = np.array([1.0, 0.0])
A2 = np.array([0.5, SQ3 / 2.0])

# Sublattice offsets (kernel half-bond convention): A=a1/2, B=a2/2, C=(a1+a2)/2
BASIS = np.array([0.5 * A1, 0.5 * A2, 0.5 * (A1 + A2)])

# M-point ordering wavevectors (paper): Qa=(0,2pi/sqrt3), Qb=(-pi,-pi/sqrt3), Qc=(pi,-pi/sqrt3)
Qa = np.array([0.0, 2.0 * np.pi / SQ3])
Qb = np.array([-np.pi, -np.pi / SQ3])
Qc = np.array([np.pi, -np.pi / SQ3])
QVEC = {0: Qa, 1: Qb, 2: Qc}   # index by sublattice/pair channel


def build_cluster(L):
    """L x L kagome cluster (L cells each direction), periodic. 3 sites/cell."""
    pos, sub, cell = [], [], []
    idx = {}
    n = 0
    for y in range(L):
        for x in range(L):
            R = x * A1 + y * A2
            for s in range(3):
                idx[(x, y, s)] = n
                pos.append(R + BASIS[s])
                sub.append(s)
                cell.append((x, y))
                n += 1
    return np.array(pos), np.array(sub), cell, idx, L


def nn_bonds(idx, L):
    """Return NN bonds as (i, j, s_i, s_j, cellR_for_channel, channel).

    Kagome NN graph: within a cell up-triangle A-B, B-C, C-A; plus down-triangle
    bonds connecting neighboring cells. We enumerate by the known kagome
    connectivity so each bond gets a clean (sublattice-pair, reference-cell).
    Channels: 0=A-B (Qa), 1=B-C (Qb), 2=C-A (Qc).
    """
    bonds = []

    def add(i, j, ch, R):
        bonds.append((i, j, ch, R))

    for y in range(L):
        for x in range(L):
            A = idx[(x, y, 0)]; B = idx[(x, y, 1)]; C = idx[(x, y, 2)]
            R = np.array([x, y]) @ np.array([A1, A2])  # cell position vector
            # ---- up triangle (intra-cell) ----
            add(A, B, 0, R)      # A-B  channel Qa
            add(B, C, 1, R)      # B-C  channel Qb
            add(C, A, 2, R)      # C-A  channel Qc
            # ---- down triangle (inter-cell) ----
            # Kagome down-triangle for this cell links C(x,y), B(x+1,y), A(x,y+1)
            Bx = idx[((x + 1) % L, y, 1)]
            Ay = idx[(x, (y + 1) % L, 2)]  # note: choose partner sublattices below
            # Physical kagome down triangle: A(x,y+? )... use standard corner-sharing
            # bonds: B(x,y)-? We construct the three down-triangle NN bonds that
            # close the corner-sharing network:
            #   A(x,y) - C(x-1,y)   (A-C  -> channel Qc, pair C-A)
            #   B(x,y) - A(x,y)+ ... handled; use explicit neighbor set below.
            pass
    # Build the full NN set robustly by geometric distance instead (safer):
    return bonds


def nn_bonds_geom(pos, sub, cell, L):
    """Robust NN detection by distance, with channel + reference cell assignment."""
    N = len(pos)
    # minimum-image distances under the cluster's periodic supercell
    Lx = L * A1; Ly = L * A2
    T = np.array([Lx, Ly]).T          # columns are supercell vectors
    Tinv = np.linalg.inv(T)
    nn = 0.5  # kagome NN distance (half of |a|=1)
    bonds = []
    for i in range(N):
        for j in range(i + 1, N):
            d = pos[j] - pos[i]
            f = Tinv @ d
            f -= np.round(f)
            dmin = T @ f
            r = np.hypot(*dmin)
            if abs(r - nn) < 1e-6:
                si, sj = sub[i], sub[j]
                pair = frozenset((si, sj))
                if pair == frozenset((0, 1)):
                    ch = 0                      # A-B -> Qa
                elif pair == frozenset((1, 2)):
                    ch = 1                      # B-C -> Qb
                elif pair == frozenset((2, 0)):
                    ch = 2                      # C-A -> Qc
                else:
                    continue                    # same-sublattice: not NN in kagome
                # reference cell = cell of the lower-index-sublattice endpoint,
                # taken at the bond midpoint for a consistent 2x2 modulation
                mid = pos[i] + 0.5 * dmin
                bonds.append((i, j, ch, mid))
    return bonds


def build_H(pos, sub, cell, bonds, t=1.0, lam=0.0, order="normal"):
    N = len(pos)
    H = np.zeros((N, N), complex)
    # onsite (vCDW)
    for i in range(N):
        s = sub[i]
        if order == "vcdw":
            Rc = pos[i] - BASIS[s]                # cell origin for this site
            H[i, i] += -lam * np.cos(QVEC[s] @ Rc)
    # hoppings
    for (i, j, ch, mid) in bonds:
        amp = -t
        if order == "cbo":
            amp += -lam * np.cos(QVEC[ch] @ mid)
        elif order == "cfp":
            amp += -1j * lam * np.cos(QVEC[ch] @ mid)
        H[i, j] += amp
        H[j, i] += np.conj(amp)
    return H


def total_energy(H, filling=5.0 / 12.0):
    N = H.shape[0]
    ev = np.linalg.eigvalsh(H)
    nocc = int(round(filling * N))
    return float(np.sum(ev[:nocc])), nocc, ev


def bond_currents_conservation(H, rho, bonds, N):
    """Return max |net current| at any site (0 => current conserved)."""
    net = np.zeros(N)
    for (i, j, ch, mid) in bonds:
        Jij = -2.0 * np.imag(H[i, j] * rho[j, i])
        net[i] += Jij
        net[j] -= Jij
    return float(np.max(np.abs(net)))


def density_matrix(H, nocc):
    w, V = np.linalg.eigh(H)
    occ = np.zeros(len(w)); occ[:nocc] = 1.0
    return (V * occ) @ V.conj().T


def run(L=12, lam=0.3):
    pos, sub, cell, idx, L = build_cluster(L)
    bonds = nn_bonds_geom(pos, sub, cell, L)
    Ncells = L * L
    N = len(pos)
    out = {}
    for order in ("normal", "vcdw", "cbo", "cfp"):
        H = build_H(pos, sub, cell, bonds, t=1.0, lam=lam, order=order)
        E, nocc, ev = total_energy(H)
        rho = density_matrix(H, nocc)
        maxnet = bond_currents_conservation(H, rho, bonds, N)
        # loop-current order parameter: mean oriented current magnitude
        Jvals = [abs(-2.0 * np.imag(H[i, j] * rho[j, i])) for (i, j, ch, mid) in bonds]
        out[order] = dict(E_per_cell=E / Ncells, nocc=nocc, N=N,
                          max_site_net_current=maxnet,
                          mean_abs_bond_current=float(np.mean(Jvals)),
                          hermitian=bool(np.allclose(H, H.conj().T)),
                          trs_broken=bool(not np.allclose(H, H.conj())))
    return out, len(bonds)


def sweep(L=12, lams=None):
    if lams is None:
        lams = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    rows = []
    for lam in lams:
        r, nb = run(L=L, lam=lam)
        rows.append(dict(lam=lam,
                         E_normal=r["normal"]["E_per_cell"],
                         E_vcdw=r["vcdw"]["E_per_cell"],
                         E_cbo=r["cbo"]["E_per_cell"],
                         E_cfp=r["cfp"]["E_per_cell"]))
    return rows


if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    detail, nbonds = run(L=L, lam=0.3)
    rows = sweep(L=L)

    # headline comparisons at lambda=0.3
    E = {k: detail[k]["E_per_cell"] for k in detail}
    dE_cfp_cbo = E["cbo"] - E["cfp"]     # >0 means CFP lower than CBO
    dE_cfp_vcdw = E["vcdw"] - E["cfp"]   # >0 means CFP lower than vCDW
    winner = min(("vcdw", "cbo", "cfp"), key=lambda k: E[k])

    result = dict(
        paper="Feng, Jiang, Wang, Hu, arXiv:2103.07097 (2021)",
        title="Chiral flux phase in the Kagome superconductor AV3Sb5",
        method="from-scratch NN kagome tight-binding + 3Q 2x2 mean-field orders, real-space PBC cluster",
        kernel_credit=["loop_current_kagome_kernel.py (geometry, Peierls/Chern conventions)",
                       "loop_current_meanfield_kernel.py (real-space cluster, J_ij=-2Im[H_ij rho_ji])"],
        cluster=dict(L=L, N_sites=detail["normal"]["N"], N_cells=L * L, N_bonds=nbonds,
                     filling="5/12 (=5/4 van Hove filling)", nocc=detail["cfp"]["nocc"]),
        lambda_compare=0.3,
        energies_per_cell_lam0p3=E,
        winner_lam0p3=winner,
        dE_CBO_minus_CFP=dE_cfp_cbo,
        dE_vCDW_minus_CFP=dE_cfp_vcdw,
        paper_dE_CBO_minus_CFP=0.195,
        paper_dE_vCDW_minus_CFP=0.435,
        cfp_trs_broken=detail["cfp"]["trs_broken"],
        cbo_trs_broken=detail["cbo"]["trs_broken"],
        cfp_current_conservation_maxnet=detail["cfp"]["max_site_net_current"],
        cfp_mean_abs_bond_current=detail["cfp"]["mean_abs_bond_current"],
        detail=detail,
        sweep=rows,
    )
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "feng2021_result.json")
    with open(outpath, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: result[k] for k in
                      ("energies_per_cell_lam0p3", "winner_lam0p3",
                       "dE_CBO_minus_CFP", "dE_vCDW_minus_CFP",
                       "paper_dE_CBO_minus_CFP", "paper_dE_vCDW_minus_CFP",
                       "cfp_trs_broken", "cfp_current_conservation_maxnet")}, indent=2))
    print("saved ->", outpath)
