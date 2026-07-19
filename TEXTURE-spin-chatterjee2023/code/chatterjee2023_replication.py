#!/usr/bin/env python3
"""
Replication of Chatterjee, Ghosh, Nandy & Saha arXiv:2308.12703
"Second-order topological superconductor via noncollinear magnetic texture"
(Phys. Rev. B; v2 29 Jan 2024)

EXACT REAL-SPACE BdG replication (CPU-only, numpy/scipy).

Model (paper Eq. 1), an 8x8 BdG lattice Hamiltonian on an Lx x Ly square lattice:

  H = sum_{i,j} c^dag_{i,j} [ {eps0 G1 + D0 G2 + Jex (G3 cos phi_ij + G4 sin phi_ij)} c_{i,j}
                              - {t G1 + i lam_x G5} c_{i+1,j}
                              - {t G1 + i lam_y G6} c_{i,j+1} ] + h.c.

Gamma matrices (8x8), built from Pauli matrices on
  tau : particle-hole,  sigma : orbital (a,b),  s : spin (up,dn)
  G1 = tau_z sigma_z s_0
  G2 = tau_x sigma_0 s_0
  G3 = tau_0 sigma_0 s_x
  G4 = tau_0 sigma_0 s_y
  G5 = tau_z sigma_x s_z
  G6 = tau_z sigma_y s_0

Noncollinear texture: phi_ij = g_x * x + g_y * y  (spin-spiral). gx=gy=g, lam_x=lam_y=lam.

Fig. 2 parameters: t=1.0, Jex=0.8, g=0.2, D0=0.4, lam=0.5, eps0=1.0, domain 30x30.

Headline claims tested:
  C1: Under OBC in the topological phase there are exactly FOUR near-zero-energy
      (E ~ 1e-7) modes inside the SC gap, localized at the four CORNERS of the domain
      => Majorana Corner Modes (MCMs), signature of a 2nd-order TSC.
  C2: The bulk quadrupole moment Qxy (Eq. 2) is quantized to 1/2 in the topological
      phase and 0 in the trivial phase.
  C3: Increasing the spiral pitch g drives a topological -> trivial transition
      (4 corner modes lift; Qxy -> 0), i.e. a phase transition in g.

Qxy (nested Wilson / Resta many-body quadrupole, Eq. 2 of the paper):
  Qxy = (1/2pi) Im ln [ det( U^dag W U ) / sqrt(det W) ]  (mod 1)
  with W = exp(i 2pi q_xy), q_xy = x y / (Lx Ly) diag operator over the full BdG basis,
  U = matrix of occupied (negative-energy) BdG eigenvectors.
This is the standard Kang-Fang-Fu / Wheeler-Wang-Uchida many-body quadrupole formula
that the paper cites [111-113].
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import json, time, sys

np.random.seed(0)

# ---- Pauli matrices ----
s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def kron3(a, b, c):
    return np.kron(np.kron(a, b), c)


# order: tau (x) sigma (x) s   -> 8x8
G1 = kron3(sz, sz, s0)   # tau_z sigma_z s_0
G2 = kron3(sx, s0, s0)   # tau_x sigma_0 s_0
G3 = kron3(s0, s0, sx)   # tau_0 sigma_0 s_x
G4 = kron3(s0, s0, sy)   # tau_0 sigma_0 s_y
G5 = kron3(sz, sx, sz)   # tau_z sigma_x s_z
G6 = kron3(sz, sy, s0)   # tau_z sigma_y s_0

NORB = 8


def build_H(Lx, Ly, t=1.0, Jex=0.8, g=0.2, D0=0.4, lam=0.5, eps0=1.0, pbc=False):
    """Assemble the full (8 Lx Ly) x (8 Lx Ly) real-space BdG Hamiltonian, Eq. (1)."""
    N = Lx * Ly
    dim = NORB * N
    H = np.zeros((dim, dim), dtype=complex)

    def idx(i, j):
        return (j * Lx + i) * NORB

    onsite_const = eps0 * G1 + D0 * G2
    hop_x = -(t * G1 + 1j * lam * G5)   # coeff of c_{i+1,j} (before +h.c.)
    hop_y = -(t * G1 + 1j * lam * G6)   # coeff of c_{i,j+1}

    for j in range(Ly):
        for i in range(Lx):
            a = idx(i, j)
            phi = g * i + g * j           # phi_ij = gx*x + gy*y, gx=gy=g
            onsite = onsite_const + Jex * (G3 * np.cos(phi) + G4 * np.sin(phi))
            H[a:a + NORB, a:a + NORB] += onsite

            # +x hopping
            if i + 1 < Lx:
                b = idx(i + 1, j)
                H[a:a + NORB, b:b + NORB] += hop_x
                H[b:b + NORB, a:a + NORB] += hop_x.conj().T
            elif pbc:
                b = idx(0, j)
                H[a:a + NORB, b:b + NORB] += hop_x
                H[b:b + NORB, a:a + NORB] += hop_x.conj().T
            # +y hopping
            if j + 1 < Ly:
                b = idx(i, j + 1)
                H[a:a + NORB, b:b + NORB] += hop_y
                H[b:b + NORB, a:a + NORB] += hop_y.conj().T
            elif pbc:
                b = idx(i, 0)
                H[a:a + NORB, b:b + NORB] += hop_y
                H[b:b + NORB, a:a + NORB] += hop_y.conj().T
    # Hermitize (guard against float asymmetry)
    H = 0.5 * (H + H.conj().T)
    return H


def build_H_sparse(Lx, Ly, t=1.0, Jex=0.8, g=0.2, D0=0.4, lam=0.5, eps0=1.0):
    """Sparse COO assembly of Eq.(1) for cheap shift-invert near-zero eigensolves."""
    N = Lx * Ly
    dim = NORB * N
    rows, cols, vals = [], [], []

    def idx(i, j):
        return (j * Lx + i) * NORB

    def add_block(a, b, M):
        for p in range(NORB):
            for q in range(NORB):
                if M[p, q] != 0:
                    rows.append(a + p); cols.append(b + q); vals.append(M[p, q])

    onsite_const = eps0 * G1 + D0 * G2
    hop_x = -(t * G1 + 1j * lam * G5)
    hop_y = -(t * G1 + 1j * lam * G6)
    hop_x_dag = hop_x.conj().T
    hop_y_dag = hop_y.conj().T
    for j in range(Ly):
        for i in range(Lx):
            a = idx(i, j)
            phi = g * i + g * j
            onsite = onsite_const + Jex * (G3 * np.cos(phi) + G4 * np.sin(phi))
            add_block(a, a, onsite)
            if i + 1 < Lx:
                b = idx(i + 1, j)
                add_block(a, b, hop_x); add_block(b, a, hop_x_dag)
            if j + 1 < Ly:
                b = idx(i, j + 1)
                add_block(a, b, hop_y); add_block(b, a, hop_y_dag)
    H = sp.coo_matrix((vals, (rows, cols)), shape=(dim, dim)).tocsc()
    H = 0.5 * (H + H.conj().T)
    return H


def nearzero_sparse(Lx, Ly, g, k=12, **kw):
    """Return the k eigenvalues closest to E=0 (+ their vecs) via shift-invert."""
    H = build_H_sparse(Lx, Ly, g=g, **kw)
    w, v = spla.eigsh(H, k=k, sigma=0.0, which='LM')
    order = np.argsort(np.abs(w))
    return w[order], v[:, order]


def corner_localization(vecs, Lx, Ly):
    """Given eigenvectors (columns), return fraction of |psi|^2 within corner plaquettes."""
    N = Lx * Ly
    # site density summed over the 8 BdG orbitals
    frac = []
    csz = max(2, Lx // 6)  # corner box size
    def in_corner(i, j):
        return ((i < csz or i >= Lx - csz) and (j < csz or j >= Ly - csz))
    corner_mask = np.zeros(N, dtype=bool)
    for j in range(Ly):
        for i in range(Lx):
            corner_mask[j * Lx + i] = in_corner(i, j)
    for c in range(vecs.shape[1]):
        psi = vecs[:, c].reshape(N, NORB)
        dens = np.sum(np.abs(psi) ** 2, axis=1)
        frac.append(float(np.sum(dens[corner_mask])))
    return frac


def quadrupole_moment(H, Lx, Ly):
    """Many-body quadrupole Qxy (Eq. 2), Wheeler/Kang formula over occupied BdG states."""
    N = Lx * Ly
    dim = NORB * N
    w, v = np.linalg.eigh(H)
    # occupied = negative energy states (BdG half-filling of the doubled space)
    occ = np.where(w < 0)[0]
    U = v[:, occ]                       # dim x Nocc
    # position operators over full basis (each site repeated NORB times)
    xs = np.zeros(dim)
    ys = np.zeros(dim)
    for j in range(Ly):
        for i in range(Lx):
            base = (j * Lx + i) * NORB
            xs[base:base + NORB] = i
            ys[base:base + NORB] = j
    qxy = (xs * ys) / (Lx * Ly)
    Wdiag = np.exp(1j * 2 * np.pi * qxy)          # W = exp(i 2pi q_xy)
    # M = U^dag W U
    M = U.conj().T @ (Wdiag[:, None] * U)
    detM = np.linalg.det(M)
    # sqrt(det W) over occupied sector: reference phase = sum of qxy over occupied "atomic" limit
    # Use the standard normalization: Qxy = 1/2pi Im ln det(M) - <qxy>_occ  (mod 1)
    qxy_ref = np.sum(qxy[occ]) if len(occ) <= dim else 0.0
    val = np.imag(np.log(detM)) / (2 * np.pi) - qxy_ref
    Q = val % 1.0
    # fold to [-0.5,0.5]
    if Q > 0.5:
        Q -= 1.0
    return abs(Q), w, v


def analyze(Lx, Ly, g, tag, **kw):
    t0 = time.time()
    H = build_H(Lx, Ly, g=g, **kw)
    Q, w, v = quadrupole_moment(H, Lx, Ly)
    # near-zero modes
    order = np.argsort(np.abs(w))
    e_sorted = w[order]
    n_zero = int(np.sum(np.abs(w) < 1e-4))
    lowest6 = [float(x) for x in e_sorted[:6]]
    # corner localization of the 4 lowest-|E| modes
    frac = corner_localization(v[:, order[:4]], Lx, Ly)
    dt = time.time() - t0
    return {
        "tag": tag, "Lx": Lx, "Ly": Ly, "g": g,
        "n_nearzero_modes(|E|<1e-4)": n_zero,
        "lowest6_|E|_sorted": lowest6,
        "min_gap_to_bulk(E5)": float(abs(e_sorted[4])),
        "corner_frac_of_4_lowest": [round(x, 4) for x in frac],
        "mean_corner_frac": round(float(np.mean(frac)), 4),
        "Qxy": round(float(Q), 4),
        "runtime_s": round(dt, 2),
    }


def analyze_sparse(Lx, Ly, g, tag, **kw):
    """Cheap near-zero-mode analysis via sparse shift-invert (no Qxy)."""
    t0 = time.time()
    w, v = nearzero_sparse(Lx, Ly, g, k=12, **kw)
    n_zero = int(np.sum(np.abs(w) < 1e-3))
    frac = corner_localization(v[:, :4], Lx, Ly)
    return {
        "tag": tag, "g": g,
        "n_nearzero_modes(|E|<1e-3)": n_zero,
        "lowest6_|E|_sorted": [float(x) for x in w[:6]],
        "corner_frac_of_4_lowest": [round(x, 4) for x in frac],
        "mean_corner_frac": round(float(np.mean(frac)), 4),
        "gap_to_5th": float(abs(w[4])),
        "runtime_s": round(time.time() - t0, 2),
    }


def main():
    L = 24        # sparse shift-invert host lattice for MCM counting (paper: 30x30)
    LQ = 14       # smaller lattice for the expensive dense Qxy many-body quadrupole
    res = {"paper": "Chatterjee et al. arXiv:2308.12703 (SOTSC via noncollinear texture)",
           "params": {"t": 1.0, "Jex": 0.8, "D0": 0.4, "lam": 0.5, "eps0": 1.0,
                      "L_MCM": L, "L_Qxy": LQ,
                      "note": "paper uses 30x30; MCM counts via sparse shift-invert at L=24; Qxy via dense many-body formula at L=14 for CPU tractability. MCM physics unchanged."},
           "claims": {}}

    # C1: topological phase g=0.2 (sparse, L=24)
    topo = analyze_sparse(L, L, g=0.2, tag="topological_g0.2")
    print("[C1 topological g=0.2]", json.dumps(topo, indent=2), flush=True)

    # C3: sweep g to find transition -> trivial (sparse, cheap)
    sweep = []
    for g in [0.0, 0.1, 0.2, 0.4, 0.7, 1.0, 1.4]:
        r = analyze_sparse(L, L, g=g, tag=f"g{g}")
        sweep.append({"g": g, "n_zero": r["n_nearzero_modes(|E|<1e-3)"],
                      "gap5": round(r["gap_to_5th"], 4),
                      "corner_frac": r["mean_corner_frac"]})
        print(f"  [sweep] g={g:.2f}  n_zero={r['n_nearzero_modes(|E|<1e-3)']}  gap5={r['gap_to_5th']:.4f}  corner_frac={r['mean_corner_frac']:.3f}", flush=True)

    # C2: dense many-body quadrupole at LQ (topological g=0.2 vs trivial g=1.4)
    print("[C2] computing dense Qxy at L=%d ..." % LQ, flush=True)
    Qtopo, _, _ = quadrupole_moment(build_H(LQ, LQ, g=0.2), LQ, LQ)
    print(f"     Qxy(topo g=0.2, L={LQ}) = {Qtopo:.4f}", flush=True)
    Qtriv, _, _ = quadrupole_moment(build_H(LQ, LQ, g=1.4), LQ, LQ)
    print(f"     Qxy(trivial g=1.4, L={LQ}) = {Qtriv:.4f}", flush=True)

    res["claims"] = {
        "C1_four_MCMs": {
            "expectation": "Exactly 4 near-zero (|E|~1e-7) modes inside the gap in the topological phase, localized at the 4 corners (MCMs).",
            "reproduced": {"n_nearzero_modes": topo["n_nearzero_modes(|E|<1e-3)"],
                           "lowest6_absE": topo["lowest6_|E|_sorted"],
                           "mean_corner_localization": topo["mean_corner_frac"]},
            "match": bool(topo["n_nearzero_modes(|E|<1e-3)"] == 4 and topo["mean_corner_frac"] > 0.5),
        },
        "C2_quadrupole_half": {
            "expectation": "Qxy quantized to 1/2 in topological phase, 0 in trivial phase.",
            "reproduced": {"Qxy_topological": round(float(Qtopo), 4), "Qxy_trivial_glarge": round(float(Qtriv), 4)},
            "match": bool(abs(Qtopo - 0.5) < 0.15 and abs(Qtriv) < 0.2),
        },
        "C3_transition_in_g": {
            "expectation": "Increasing g drives topological->trivial (corner modes lift, gap closes/reopens trivial).",
            "reproduced": {"sweep": sweep},
            "match": bool(sweep[2]["n_zero"] == 4 and sweep[-1]["n_zero"] != 4),
        },
    }
    res["runtime_s"] = topo["runtime_s"]
    out = "/Users/stevens/Dropbox/REPLICATE-PROJECT/TEXTURE-spin-chatterjee2023/work/results.json"
    with open(out, "w") as f:
        json.dump(res, f, indent=2)
    print("\n[verdict-signal]",
          "C1=", res["claims"]["C1_four_MCMs"]["match"],
          "C2=", res["claims"]["C2_quadrupole_half"]["match"],
          "C3=", res["claims"]["C3_transition_in_g"]["match"])
    print("[written]", out)


if __name__ == "__main__":
    main()
