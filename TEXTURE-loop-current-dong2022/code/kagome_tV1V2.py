#!/usr/bin/env python3
"""
Replication of arXiv:2209.10768 (Dong, Wang, Zhou 2023):
Loop-current CDW driven by long-range Coulomb repulsion on the kagome lattice.

Self-consistent Hartree-Fock (bond/Fock-channel) solver for the single-orbital
t-V1-V2 model at van Hove filling n = 5/12, on a 2x2-enlarged kagome cell.

Reuses geometry/current concepts from the shared TEXTURES-100 loop-current kernel
(loop_current_meanfield_kernel.py); here we build the momentum-space 12-band
solver required for the paper's 2x2 complex bond order parameters.

Claims addressed:
  C1  nn susceptibility peaks in REAL channel; nnn in IMAGINARY channel (bare chi at M).
  C2  weak-coupling ratio V2/V1 ~ 2.36 for real->imaginary boundary.
  C3  spontaneous Im(chi) (loop currents) only for sufficiently large V2;
      first-order ISD->LC transition.
  C4  Chern numbers of LC states (Fukui-Hatsugai on folded BZ).
  C5  vH sublattice localization / small charge disproportionation.

Real code only. t=1 energy unit throughout.
"""
from __future__ import annotations
import json, sys, itertools
import numpy as np

SQ3 = np.sqrt(3.0)

# ---------------------------------------------------------------------------
# Kagome geometry: 3 sublattices. Positions in the primitive cell (paper Fig 1a):
#   r1 = r - a3/2, r2 = r, r3 = r + a1/2, with a1=(1,0), a2=(-1/2, sqrt3/2).
# We use standard kagome: sublattice offsets at midpoints of the triangle edges.
# ---------------------------------------------------------------------------
a1 = np.array([1.0, 0.0])
a2 = np.array([0.5, SQ3 / 2.0])          # triangular Bravais lattice
# Canonical kagome sublattice positions = midpoints of the up-triangle edges.
delta = np.array([
    [0.5, 0.0],          # sublattice 1 (A): midpoint of a1 edge
    [0.25, SQ3 / 4.0],   # sublattice 2 (B): midpoint of a2 edge
    [0.75, SQ3 / 4.0],   # sublattice 3 (C): midpoint of (a1..a2) edge
])

# Nearest-neighbor bonds (intra up-triangle + inter down-triangle links).
# (subl_i, subl_j, cell-offset R in (n1,n2) integer units) with j displaced by R.
# Derived to reproduce the canonical closed-form kagome Bloch H below.
NN_BONDS = [
    (0, 1, (0, 0)),    # A-B intra (up triangle)
    (1, 2, (0, 0)),    # B-C intra
    (2, 0, (0, 0)),    # C-A intra
    (0, 1, (1, -1)),   # A -> B in cell (+a1 -a2)  (down triangle)
    (1, 2, (-1, 1)),   # B -> C in cell (-a1 +a2)
    (2, 0, (1, 0)),    # C -> A in cell (+a1)
]
# Next-nearest-neighbor bonds (across hexagon; connect different sublattices
# along the Q_alpha nesting directions, free of sublattice obstruction).
NNN_BONDS = [
    (0, 1, (1, 0)),
    (0, 1, (0, -1)),
    (1, 2, (0, 1)),
    (1, 2, (-1, 0)),
    (2, 0, (0, 1)),
    (2, 0, (1, -1)),
]


def hk_tb(k, t=1.0):
    """3x3 canonical kagome tight-binding Bloch Hamiltonian (nn hopping).
    Uses the standard closed form H_ss' = -2 t cos(k . d_ss') with half-bond
    vectors; reproduces flat band at +2t and vH saddles at M with E={-2,0,2}t."""
    # Standard kagome half-bond vectors: pair A-B via a1/2, B-C via a2/2,
    # C-A via a3/2 with a3=a2-a1. This yields C3-symmetric spectrum: all three
    # inequivalent M points give E={-2,0,2}t (flat band +2t, vH saddle 0).
    a3 = a2 - a1
    dAB = a1 / 2.0
    dBC = a2 / 2.0
    dCA = a3 / 2.0
    H = np.zeros((3, 3), complex)
    H[0, 1] = -2 * t * np.cos(np.dot(k, dAB))
    H[1, 2] = -2 * t * np.cos(np.dot(k, dBC))
    H[2, 0] = -2 * t * np.cos(np.dot(k, dCA))
    H[1, 0] = np.conj(H[0, 1])
    H[2, 1] = np.conj(H[1, 2])
    H[0, 2] = np.conj(H[2, 0])
    return H


def brillouin_grid(nk):
    """Uniform grid over the primitive BZ (reciprocal of a1,a2)."""
    b1, b2 = recip(a1, a2)
    ks = []
    for m in range(nk):
        for n in range(nk):
            ks.append((m / nk) * b1 + (n / nk) * b2)
    return np.array(ks), b1, b2


def recip(a1, a2):
    A = np.array([a1, a2]).T
    B = 2 * np.pi * np.linalg.inv(A).T
    return B[0], B[1]


# ---------------------------------------------------------------------------
# C5 + band structure: chemical potential for filling.
# ---------------------------------------------------------------------------
def _fermi(e, mu, T):
    if T <= 0:
        return (e < mu).astype(float)
    x = np.clip((e - mu) / T, -60, 60)
    return 1.0 / (1.0 + np.exp(x))


def fermi_mu(evals, filling, T):
    """Find mu for target filling (fraction of states occupied)."""
    target = filling * evals.size
    lo, hi = evals.min() - 20, evals.max() + 20
    for _ in range(200):
        mu = 0.5 * (lo + hi)
        occ = _fermi(evals, mu, T).sum()
        if occ > target:
            hi = mu
        else:
            lo = mu
    return 0.5 * (lo + hi)


def tb_bands_and_dos(nk=48, t=1.0, filling=5.0 / 12.0):
    """Baseline tight-binding: bands, vH filling check, sublattice weight at M."""
    ks, b1, b2 = brillouin_grid(nk)
    all_e = []
    for k in ks:
        e = np.linalg.eigvalsh(hk_tb(k, t))
        all_e.extend(e.tolist())
    all_e = np.array(sorted(all_e))
    mu = fermi_mu(all_e, filling, T=0.0)
    # Three C3-related inequivalent M points (BZ-edge midpoints). Use M1=b1/2 and
    # its +-120 deg rotations so all three are symmetry-equivalent.
    def _rot(th):
        c, s = np.cos(th), np.sin(th)
        return np.array([[c, -s], [s, c]])
    M1 = 0.5 * b1
    Mpts = {"M1": M1, "M2": _rot(2*np.pi/3) @ M1, "M3": _rot(-2*np.pi/3) @ M1}
    e_M, v_M = np.linalg.eigh(hk_tb(M1, t))
    subweight = np.abs(v_M) ** 2  # rows=sublattice, cols=band
    # vH sublattice support: for each M point, the E=0 (vH) band has weight ~0 on
    # one sublattice (sublattice interference). Record the minimum sublattice
    # weight of the vH band at each M point.
    vh_min_weight = {}
    for nm, Mp in Mpts.items():
        e, v = np.linalg.eigh(hk_tb(Mp, t))
        vh_band = int(np.argmin(np.abs(e)))  # the E~0 vH saddle band
        vh_min_weight[nm] = float(np.min(np.abs(v[:, vh_band]) ** 2))
    return dict(mu=float(mu), bandmin=float(all_e.min()), bandmax=float(all_e.max()),
                M_energies=e_M.tolist(), M_subweight=subweight.tolist(),
                vh_band_min_sublattice_weight=vh_min_weight)


# ---------------------------------------------------------------------------
# C1: bare bond susceptibility at q=M for real vs imaginary, nn vs nnn channels.
# chi_O(q=M) = sum_k [f(e_a k) - f(e_b k+M)] / (e_a k - e_b k+M) |<a k|O|b k+M>|^2
# We use a simple Lindhard-style static bond susceptibility with bond operators.
# ---------------------------------------------------------------------------
def bare_bond_susceptibility(nk=60, t=1.0, filling=5.0 / 12.0, T=0.005):
    ks, b1, b2 = brillouin_grid(nk)
    M = 0.5 * b1
    # precompute mu at this T
    all_e = []
    for k in ks:
        all_e.extend(np.linalg.eigvalsh(hk_tb(k, t)).tolist())
    mu = fermi_mu(np.array(sorted(all_e)), filling, T)

    def fermi(e):
        return 1.0 / (1.0 + np.exp((e - mu) / T))

    # bond operator matrices in sublattice space for a representative nn and nnn bond
    # nn: sublattice 1-2 pair;  nnn: sublattice 1-2 across hexagon.
    def bond_op(i, j, real=True):
        Op = np.zeros((3, 3), complex)
        if real:
            Op[i, j] = 1.0
            Op[j, i] = 1.0
        else:  # imaginary (current) part
            Op[i, j] = 1j
            Op[j, i] = -1j
        return Op

    chans = {
        "nn_real": bond_op(0, 1, real=True),
        "nn_imag": bond_op(0, 1, real=False),
        "nnn_real": bond_op(0, 2, real=True),
        "nnn_imag": bond_op(0, 2, real=False),
    }
    out = {c: 0.0 for c in chans}
    eps = 1e-9
    for k in ks:
        eA, vA = np.linalg.eigh(hk_tb(k, t))
        eB, vB = np.linalg.eigh(hk_tb(k + M, t))
        fA = fermi(eA)
        fB = fermi(eB)
        for c, Op in chans.items():
            # matrix element <a,k| Op |b,k+M>
            Mel = vA.conj().T @ Op @ vB   # (band_a, band_b)
            for a in range(3):
                for b in range(3):
                    de = eA[a] - eB[b]
                    df = fA[a] - fB[b]
                    if abs(de) < eps:
                        # degenerate: use -f'(e)
                        contrib = -(fA[a] * (1 - fA[a]) / T) * abs(Mel[a, b]) ** 2
                    else:
                        contrib = (df / de) * abs(Mel[a, b]) ** 2
                    out[c] += contrib.real
    n = len(ks)
    for c in out:
        out[c] = out[c] / n
    return out


# ---------------------------------------------------------------------------
# C3 + C4: self-consistent HF on the 2x2 (12-site) cluster with complex bonds.
# We build a 12-orbital momentum-space Hamiltonian over the folded (reduced) BZ.
# Order parameters live on the 24 nn + 24 nnn bonds of the 2x2 supercell.
# ---------------------------------------------------------------------------
class Supercell:
    """2x2 kagome supercell = 12 sites. Enumerate sites + nn/nnn bonds with
    supercell-periodic connectivity, tracking the inter-supercell translation
    for Bloch phases over the reduced BZ."""
    def __init__(self):
        # site index = (cx, cy, s) with cx,cy in {0,1}, s in {0,1,2}
        self.sites = [(cx, cy, s) for cx in range(2) for cy in range(2) for s in range(3)]
        self.index = {sv: i for i, sv in enumerate(self.sites)}
        self.N = len(self.sites)  # 12
        # supercell lattice vectors
        self.A1 = 2 * a1
        self.A2 = 2 * a2
        self.pos = np.array([cx * a1 + cy * a2 + delta[s] for (cx, cy, s) in self.sites])
        self.nn = self._bonds(NN_BONDS)
        self.nnn = self._bonds(NNN_BONDS)

    def _bonds(self, bondlist):
        """Return list of (i, j, superR) where i,j are supercell site indices and
        superR is the integer inter-supercell translation (in A1,A2 units) applied
        to site j. Undirected, each physical bond once (i<j by canonical rule)."""
        out = []
        seen = set()
        for (si, sj, R) in bondlist:
            for cx in range(2):
                for cy in range(2):
                    i = self.index[(cx, cy, si)]
                    # target primitive cell coords
                    tx = cx + R[0]
                    ty = cy + R[1]
                    # fold into supercell (mod 2), record super-translation
                    scx = tx // 2 if tx >= 0 else -((-tx + 1) // 2)
                    # use python floor division for correct sign
                    scx = tx // 2
                    scy = ty // 2
                    fx = tx % 2
                    fy = ty % 2
                    j = self.index[(fx, fy, sj)]
                    key = tuple(sorted([(i, 0, 0), (j, scx, scy)]))
                    # canonical dedup: represent bond by (min,max) with relative R
                    a, b = (i, j) if i <= j else (j, i)
                    rel = (scx, scy) if i <= j else (-scx, -scy)
                    k = (a, b, rel)
                    if k in seen:
                        continue
                    seen.add(k)
                    out.append((i, j, (scx, scy)))
        return out


def build_HF_bloch(sc, chi_nn, chi_nnn, k, t, V1, V2):
    """Build 12x12 mean-field Bloch Hamiltonian at reduced-BZ momentum k.
    chi_nn[b], chi_nnn[b] are complex bond OPs indexed by bond position in
    sc.nn / sc.nnn lists.  Follows Eq. (20)."""
    H = np.zeros((sc.N, sc.N), complex)
    # nn bonds: hopping amplitude -(t + V1 * conj(chi))
    for b, (i, j, R) in enumerate(sc.nn):
        Rvec = R[0] * sc.A1 + R[1] * sc.A2
        dr = (sc.pos[j] + Rvec) - sc.pos[i]
        ph = np.exp(1j * np.dot(k, dr))
        amp = -(t + V1 * np.conj(chi_nn[b]))
        H[i, j] += amp * ph
        H[j, i] += np.conj(amp * ph)
    # nnn bonds: amplitude -(V2 * conj(chi'))  (no bare hopping on nnn)
    for b, (i, j, R) in enumerate(sc.nnn):
        Rvec = R[0] * sc.A1 + R[1] * sc.A2
        dr = (sc.pos[j] + Rvec) - sc.pos[i]
        ph = np.exp(1j * np.dot(k, dr))
        amp = -(V2 * np.conj(chi_nnn[b]))
        H[i, j] += amp * ph
        H[j, i] += np.conj(amp * ph)
    return H


def self_consistent(sc, t, V1, V2, filling=5.0 / 12.0, nk=12, T=0.002,
                    seed="ISD", max_iter=400, tol=1e-6, mix=0.5, rng_seed=0):
    """Self-consistent HF loop. Returns converged bond OPs + energy + observables."""
    b1s, b2s = recip(sc.A1, sc.A2)
    ks = [(m / nk) * b1s + (n / nk) * b2s for m in range(nk) for n in range(nk)]
    nnb, nnnb = len(sc.nn), len(sc.nnn)
    rng = np.random.default_rng(rng_seed)

    # initial guesses
    if seed == "ISD":
        chi_nn = np.full(nnb, 0.5, complex)
        chi_nnn = np.zeros(nnnb, complex)
    elif seed == "LC":
        chi_nn = np.full(nnb, 0.4, complex) + 0.15j * rng.standard_normal(nnb)
        chi_nnn = 0.3j * (rng.standard_normal(nnnb) + 1j * rng.standard_normal(nnnb))
    elif seed == "LCstrong":
        chi_nn = 0.4 * np.ones(nnb, complex) + 0.3j * np.ones(nnb)
        chi_nnn = (-0.1 - 0.45j) * np.ones(nnnb, complex)
    else:
        chi_nn = 0.4 * np.ones(nnb, complex) + 0.1j * rng.standard_normal(nnb)
        chi_nnn = 0.2j * rng.standard_normal(nnnb) + 0.1 * rng.standard_normal(nnnb)

    def measure(chi_nn, chi_nnn):
        new_nn = np.zeros(nnb, complex)
        new_nnn = np.zeros(nnnb, complex)
        all_e = []
        rhos = []
        for k in ks:
            H = build_HF_bloch(sc, chi_nn, chi_nnn, k, t, V1, V2)
            e, v = np.linalg.eigh(H)
            all_e.append(e)
            rhos.append((e, v, k))
        flat = np.sort(np.concatenate(all_e))
        mu = fermi_mu(flat, filling, T)
        Eband = 0.0
        for (e, v, k) in rhos:
            f = _fermi(e, mu, T)
            rho = (v * f) @ v.conj().T   # rho_ij = <c_j^dag c_i>
            Eband += np.sum(e * f)
            # bond OP chi_ij = <c_i^dag c_j + ...> spin sum => factor 2
            for b, (i, j, R) in enumerate(sc.nn):
                Rvec = R[0] * sc.A1 + R[1] * sc.A2
                dr = (sc.pos[j] + Rvec) - sc.pos[i]
                ph = np.exp(1j * np.dot(k, dr))
                # <c_i^dag c_j> = rho_ji * phase back; use rho[j,i]
                new_nn[b] += 2.0 * rho[j, i] * np.conj(ph)
            for b, (i, j, R) in enumerate(sc.nnn):
                Rvec = R[0] * sc.A1 + R[1] * sc.A2
                dr = (sc.pos[j] + Rvec) - sc.pos[i]
                ph = np.exp(1j * np.dot(k, dr))
                new_nnn[b] += 2.0 * rho[j, i] * np.conj(ph)
        nkt = len(ks)
        new_nn /= nkt
        new_nnn /= nkt
        Eband /= nkt
        return new_nn, new_nnn, mu, Eband

    for it in range(max_iter):
        new_nn, new_nnn, mu, Eband = measure(chi_nn, chi_nnn)
        dnn = np.max(np.abs(new_nn - chi_nn))
        dnnn = np.max(np.abs(new_nnn - chi_nnn))
        chi_nn = mix * new_nn + (1 - mix) * chi_nn
        chi_nnn = mix * new_nnn + (1 - mix) * chi_nnn
        if max(dnn, dnnn) < tol:
            break

    # Physical loop current around triangular plaquettes, measured directly from
    # the converged mean-field Hamiltonian and density matrix (kernel approach:
    # J_ij = -2 Im[H_ij rho_ji]). Gauge-invariant; zero for a real CDW.
    phys_current = physical_triangle_current(sc, chi_nn, chi_nnn, t, V1, V2, filling, ks, T)
    # total MF energy per site: Eband + interaction correction (+V|chi|^2 terms)
    # E_MF = Eband(with MF H) + V1 sum|chi_nn|^2 + V2 sum|chi_nnn|^2  (double-count fix)
    Ecorr = V1 * np.sum(np.abs(chi_nn) ** 2) + V2 * np.sum(np.abs(chi_nnn) ** 2)
    E_per_site = (Eband + Ecorr) / sc.N
    max_Im_nn = float(np.max(np.abs(chi_nn.imag)))
    max_Im_nnn = float(np.max(np.abs(chi_nnn.imag)))
    # Gauge-invariant loop-current order parameter: sum of Peierls flux around
    # each triangular plaquette = arg(product of complex bond OPs around loop).
    loop_flux = triangle_flux(sc, chi_nn)
    return dict(chi_nn=chi_nn, chi_nnn=chi_nnn, mu=float(mu),
                E_per_site=float(E_per_site), iters=it + 1,
                max_Im_nn=max_Im_nn, max_Im_nnn=max_Im_nnn,
                loop_flux=float(loop_flux),
                phys_loop_current=float(phys_current),
                conv=float(max(dnn, dnnn)))


def physical_triangle_current(sc, chi_nn, chi_nnn, t, V1, V2, filling, ks, T):
    """Mean absolute physical current circulating each triangular plaquette,
    J_ij = -2 Im[H_ij rho_ji], averaged over the reduced BZ. Nonzero => TRS
    broken loop-current state; zero => real CDW."""
    # triangles from nn adjacency
    adj = {}
    for (i, j, R) in sc.nn:
        adj.setdefault(i, set()).add(j)
        adj.setdefault(j, set()).add(i)
    tris = set()
    for i in adj:
        for j in adj[i]:
            for k in adj[i] & adj.get(j, set()):
                tris.add(tuple(sorted((i, j, k))))
    # bond lookup (i,j)-> (index,R) for building H_ij with phase per k
    nnmap = {}
    for b, (i, j, R) in enumerate(sc.nn):
        nnmap[(i, j)] = (b, R, +1)
        nnmap[(j, i)] = (b, R, -1)
    loop_vals = []
    # accumulate rho over BZ
    rho_acc = np.zeros((sc.N, sc.N), complex)
    all_e = []
    grids = []
    for k in ks:
        H = build_HF_bloch(sc, chi_nn, chi_nnn, k, t, V1, V2)
        e, v = np.linalg.eigh(H)
        all_e.append(e)
        grids.append((e, v, k))
    flat = np.sort(np.concatenate(all_e))
    mu = fermi_mu(flat, filling, T)
    # For each triangle compute circulating current summed over k with proper phases
    tri_current = {tri: 0.0 for tri in tris}
    for (e, v, k) in grids:
        f = _fermi(e, mu, T)
        rho = (v * f) @ v.conj().T
        H = build_HF_bloch(sc, chi_nn, chi_nnn, k, t, V1, V2)
        for tri in tris:
            a, b2, c = tri
            J = 0.0
            for (p, q) in [(a, b2), (b2, c), (c, a)]:
                if (p, q) in nnmap:
                    J += -2.0 * np.imag(H[p, q] * rho[q, p])
            tri_current[tri] += J
    nkt = len(ks)
    vals = [abs(tri_current[tri]) / nkt for tri in tris]
    return float(np.mean(vals)) if vals else 0.0


def triangle_flux(sc, chi_nn):
    """Gauge-invariant loop-current OP: mean |Im| of the product of the three
    complex nn bond order parameters around each triangular plaquette.
    A real CDW has zero triangle flux; a loop-current state has nonzero flux."""
    # map bond (i,j) -> chi index for nn bonds
    bmap = {}
    for b, (i, j, R) in enumerate(sc.nn):
        bmap[(i, j)] = (b, +1)
        bmap[(j, i)] = (b, -1)
    # find triangles: triples of sites mutually nn-connected within supercell
    adj = {}
    for (i, j, R) in sc.nn:
        adj.setdefault(i, set()).add(j)
        adj.setdefault(j, set()).add(i)
    fluxes = []
    tris = set()
    for i in adj:
        for j in adj[i]:
            for k in adj[i] & adj.get(j, set()):
                tri = tuple(sorted((i, j, k)))
                if tri in tris:
                    continue
                tris.add(tri)
                a, b2, c = tri
                prod = 1.0 + 0j
                ok = True
                for (p, q) in [(a, b2), (b2, c), (c, a)]:
                    if (p, q) not in bmap:
                        ok = False
                        break
                    idx, sgn = bmap[(p, q)]
                    z = chi_nn[idx] if sgn > 0 else np.conj(chi_nn[idx])
                    prod *= z
                if ok:
                    fluxes.append(np.imag(prod))
    if not fluxes:
        return 0.0
    return float(np.mean(np.abs(fluxes)))


# ---------------------------------------------------------------------------
# C4: Chern number of occupied bands via Fukui-Hatsugai on the reduced BZ.
# ---------------------------------------------------------------------------
def chern_number(sc, chi_nn, chi_nnn, t, V1, V2, filling=5.0 / 12.0, nk=24, T=0.002):
    b1s, b2s = recip(sc.A1, sc.A2)
    # determine number of occupied bands from filling
    nocc = int(round(filling * sc.N))
    # build eigenvector grid
    U = np.empty((nk, nk), object)
    for m in range(nk):
        for n in range(nk):
            k = (m / nk) * b1s + (n / nk) * b2s
            H = build_HF_bloch(sc, chi_nn, chi_nnn, k, t, V1, V2)
            e, v = np.linalg.eigh(H)
            U[m, n] = v[:, :nocc]  # occupied subspace
    # Fukui-Hatsugai
    F_total = 0.0
    for m in range(nk):
        for n in range(nk):
            u00 = U[m, n]
            u10 = U[(m + 1) % nk, n]
            u11 = U[(m + 1) % nk, (n + 1) % nk]
            u01 = U[m, (n + 1) % nk]
            def link(a, b):
                d = np.linalg.det(a.conj().T @ b)
                return d / abs(d) if abs(d) > 1e-12 else 1.0
            U1 = link(u00, u10)
            U2 = link(u10, u11)
            U3 = link(u11, u01)
            U4 = link(u01, u00)
            F = np.log(U1 * U2 * U3 * U4).imag
            F_total += F
    C = F_total / (2 * np.pi)
    return int(round(C))


if __name__ == "__main__":
    print("kagome_tV1V2 module — import from run scripts.")
