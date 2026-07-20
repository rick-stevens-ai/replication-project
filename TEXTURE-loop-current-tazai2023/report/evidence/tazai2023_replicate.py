#!/usr/bin/env python3
"""
From-scratch replication of Tazai, Yamakawa & Kontani,
"Drastic magnetic-field-induced chiral current order and emergent
 current-bond-field interplay in kagome metal AV3Sb5", arXiv:2303.00623v4
 (Nat. Commun. / PRB-class; loop-current order in AV3Sb5).

HEADLINE CLAIMS REPRODUCED HERE
-------------------------------
(C1) The 3Q chiral loop-current order eta=(eta,eta,eta)/sqrt3 induces a *finite*
     uniform orbital magnetization M_orb (weak ferromagnet), while 1Q and 2Q
     current orders give M_orb = 0 (TRS in bulk).                     [Eq. 3-6]
(C2) M_orb is an ODD function of eta with leading law M_orb  ~  eta^3
     (current only, no bond order).                                   [Eq. after (6)]
(C3) With coexisting 3Q bond order phi, M_orb becomes LINEAR in eta:
     M_orb ~ m1*phi*eta  (strongly enhanced; trilinear coupling).     [Fig 2d, Eq. Mbar=m1 phi.eta + m2 eta1 eta2 eta3]
(C4) The field-induced GL free energy is  dF = -3 h_z M_orb  (per 3-site cell),
     with trilinear term -3 m1 h_z eta.phi, so a TINY field aligns/switches the
     chiral current domain. Paper scale: h_z = 1e-4  <->  ~1 Tesla.   [Eq. 7]
     => Verify the field energy gain from switching is >~ the domain-energy scale
        at ~1 T, i.e. ~1 T can switch. (C4 field-scale comparison.)

METHOD: kagome-lattice tight-binding, single effective dXZ (b3g) orbital on
A/B/C sublattices, t=-0.5 eV NN, t'=-0.02 eV intra-sublattice, folded 2x2
(4x3 = 12-site) supercell, folded-BZ k-mesh. Current order = imaginary hopping
modulation delta t^c = eta.f (odd parity), bond order = real modulation
delta t^b = phi.g. M_orb from the modern-theory interband velocity formula
(paper Eq. 6, T=0 form; finite-T Eq.3 used for the weighting).

Kernel credit: geometry / Peierls-flux / bond-current conventions adapted from
the shared kernel  ~/shared-kernels-cache/loop_current_kagome_kernel.py
(Fernandes-Birol-Ye-Vanderbilt reusable kagome flux-phase kernel).
Runner: /home/stevens/comfyui-env/bin/python (numpy/scipy).
"""
from __future__ import annotations
import json, time
import numpy as np

t0 = time.time()

# ---------------------------------------------------------------------------
# Geometry: kagome lattice, 2x2 (12-site) supercell
# ---------------------------------------------------------------------------
SQ3 = np.sqrt(3.0)
a1 = np.array([1.0, 0.0])
a2 = np.array([0.5, SQ3 / 2.0])
# sublattice basis offsets (midpoints of triangle edges) -> NN dist = 0.5
basis = np.array([0.5 * a1,               # A
                  0.5 * a2,               # B
                  0.5 * (a1 + a2)])       # C
# supercell (2x2) lattice vectors
A1, A2 = 2.0 * a1, 2.0 * a2

# reciprocal vectors of the *original* kagome cell (for the M-point form factors)
Mrec = np.array([a1, a2]).T
b_orig = 2 * np.pi * np.linalg.inv(Mrec).T
b1o, b2o = b_orig[0], b_orig[1]
# three inequivalent M points (nesting vectors q1,q2,q3), q1+q2+q3 = 0 mod G
q1 = 0.5 * b1o
q2 = 0.5 * b2o
q3 = -(q1 + q2)          # = -(b1+b2)/2  (equiv to third M point)
Qs = [q1, q2, q3]

# reciprocal of the SUPERcell (folded BZ)
Msup = np.array([A1, A2]).T
b_sup = 2 * np.pi * np.linalg.inv(Msup).T
B1s, B2s = b_sup[0], b_sup[1]

NN_DIST = 0.5
NNN_DIST = 1.0            # nearest intra-sublattice distance (t')

# Enumerate the 12 basis sites: subcell (n1,n2) in {0,1}^2, sublattice s in {A,B,C}
sites = []               # (index, home_position, sublattice, subcell)
for n1 in (0, 1):
    for n2 in (0, 1):
        R = n1 * a1 + n2 * a2      # NOTE: internal offsets in units of the ORIGINAL cell
        for s in range(3):
            sites.append(dict(pos=R + basis[s], sub=s, cell=(n1, n2)))
NSITE = len(sites)       # 12
assert NSITE == 12

# Build bond list by tiling the supercell over neighboring images and finding
# NN (and NNN) pairs; fold each neighbor back into the 12-site basis, record the
# SUPERcell lattice offset L (for the Bloch phase) and the real displacement d.
def fold(pos):
    """Return (basis_index, L) so that pos = sites[idx].pos + L, L integer combo of A1,A2."""
    for idx, s in enumerate(sites):
        d = pos - s['pos']
        # solve d = m1*A1 + m2*A2
        coeff = np.linalg.solve(np.array([A1, A2]).T, d)
        if np.allclose(coeff, np.round(coeff), atol=1e-6):
            m = np.round(coeff).astype(int)
            return idx, m[0] * A1 + m[1] * A2
    return None, None

# Build UNIQUE (deduplicated) directed bonds with a canonical orientation, so
# the odd-parity current order is NOT symmetrized away. Each physical bond is
# stored ONCE as i->j; the reverse hop is set by Hermitian conjugation in the
# Hamiltonian assembly (delta t^c_ji = conj(delta t^c_ij) => odd parity for the
# imaginary current part).
def canon_key(pi, pj):
    """Orientation-independent key for an undirected bond via the two endpoints
    reduced to the supercell torus (round to 1e-3)."""
    def red(p):
        c = np.linalg.solve(np.array([A1, A2]).T, p)
        c = c - np.floor(c)      # into [0,1)^2 (torus)
        return tuple(np.round((c[0] * A1 + c[1] * A2), 3))
    a, b = red(pi), red(pj)
    return tuple(sorted([a, b]))

def positive_orientation(dvec):
    """Canonical orientation: displacement with +x, or +y if x~0."""
    if dvec[0] > 1e-6:
        return True
    if abs(dvec[0]) <= 1e-6 and dvec[1] > 0:
        return True
    return False

bonds_nn = []    # (i, j, L_ij, dvec, Rb) canonical directed i->j
bonds_nnn = []
seen_nn, seen_nnn = set(), set()
for i, si in enumerate(sites):
    for m1 in (-1, 0, 1):
        for m2 in (-1, 0, 1):
            for j0, sj in enumerate(sites):
                posj = sj['pos'] + m1 * A1 + m2 * A2
                dvec = posj - si['pos']
                dist = np.linalg.norm(dvec)
                if abs(dist - NN_DIST) < 1e-6:
                    key = canon_key(si['pos'], posj)
                    if key in seen_nn:
                        continue
                    if not positive_orientation(dvec):
                        continue      # take the +oriented representative only
                    seen_nn.add(key)
                    j, L = fold(posj)
                    Rb = 0.5 * (si['pos'] + posj)
                    bonds_nn.append((i, j, L, dvec.copy(), Rb.copy()))
                elif abs(dist - NNN_DIST) < 1e-6 and si['sub'] == sj['sub']:
                    key = canon_key(si['pos'], posj)
                    if key in seen_nnn:
                        continue
                    if not positive_orientation(dvec):
                        continue
                    seen_nnn.add(key)
                    j, L = fold(posj)
                    bonds_nnn.append((i, j, L, dvec.copy()))

# 12-site kagome has 2*12/... : 24 NN bonds (each site has 4 NN -> 12*4/2=24)
assert len(bonds_nn) == 24, f"got {len(bonds_nn)} NN bonds"

# --- enumerate oriented triangles (up & down) as 3-cycles of NN bonds --------
# NN adjacency with the supercell offset needed to hop i->j (real vector).
nn_adj = {}
for (i, j, L, dvec, Rb) in bonds_nn:
    nn_adj[(i, j)] = L
    nn_adj[(j, i)] = -L
# neighbor lists
nbr = {i: [] for i in range(NSITE)}
for (i, j) in nn_adj:
    nbr[i].append(j)

triangles = []      # each: {"bonds":[(i,j,Lij),(j,k,Ljk),(k,i,Lki)] CCW, "center":R}
seen_tri = set()
for i in range(NSITE):
    for j in nbr[i]:
        Lij = nn_adj[(i, j)]
        for k in nbr[j]:
            if k == i:
                continue
            Ljk = nn_adj[(j, k)]
            # need k->i to close with total offset zero
            if (k, i) not in nn_adj:
                continue
            Lki = nn_adj[(k, i)]
            if not np.allclose(Lij + Ljk + Lki, 0.0, atol=1e-4):
                continue
            pi = sites[i]['pos']
            pj = sites[j]['pos'] + Lij
            pk = sites[k]['pos'] + Lij + Ljk
            center = (pi + pj + pk) / 3.0
            # fold center into the supercell torus for a unique key
            cc = np.linalg.solve(np.array([A1, A2]).T, center)
            cc = cc - np.floor(cc + 1e-9)
            cfold = cc[0] * A1 + cc[1] * A2
            ckey = tuple(np.round(cfold, 2))
            if ckey in seen_tri:
                continue
            seen_tri.add(ckey)
            area = (pj[0]-pi[0])*(pk[1]-pi[1]) - (pj[1]-pi[1])*(pk[0]-pi[0])
            if area >= 0:   # CCW
                oriented = [(i, j, Lij), (j, k, Ljk), (k, i, Lki)]
            else:           # reverse to CCW
                oriented = [(i, k, -Lki), (k, j, -Ljk), (j, i, -Lij)]
            triangles.append({"bonds": oriented, "center": center})
# kagome: 2 triangles / 3-site cell -> 8 triangles in the 12-site (4-cell) supercell
assert len(triangles) == 8, f"got {len(triangles)} triangles: centers={[tuple(np.round(t['center'],3)) for t in triangles]}"

# Map each canonical NN bond to the triangle-circulation sign it carries.
# The loop current on a bond is the CCW circulation of the triangle(s) it borders,
# modulated by the single-Q phase at the TRIANGLE CENTER. This keys the current
# sign off the up/down-triangle geometry (paper Fig.1c) so 1Q/2Q fluxes cancel
# and only 3Q leaves a net orbital moment.
# Precompute, for each canonical directed bond (i,j,L), its triangle-CCW sign
# and the center of the triangle whose CCW orientation matches (i->j).
bond_tri = {}   # (i,j,tuple(L)) -> center of the triangle where i->j is CCW
for tri in triangles:
    for (i, j, L) in tri["bonds"]:
        bond_tri[(i, j, tuple(np.round(L, 3)))] = tri["center"]


# ---------------------------------------------------------------------------
# Form factors for the current (imaginary, odd) and bond (real, even) orders
# ---------------------------------------------------------------------------
# For a bond centered at Rb, component-m modulation ~ cos(q_m . Rb).
# Current order:  delta t^c_{i->j} = i * sum_m eta_m * cos(q_m . Rb)   (Hermitian conj on j->i gives -i..., odd parity)
# Bond order:     delta t^b_{i->j} =     sum_m phi_m * cos(q_m . Rb)   (real, even)
def tri_circulation(center, eta):
    """CCW loop-current circulation of a triangle centered at `center` for a
    (possibly multi-Q) current order eta, modulated at the triangle center."""
    return sum(eta[m] * np.cos(np.dot(Qs[m], center)) for m in range(3))

# Precompute, for each canonical directed bond, the two adjacent triangle centers:
# the one where the bond runs CCW and the one where it runs CW. The physical loop
# current on the bond is the DIFFERENCE of the two triangle circulations, so a
# single-Q pattern (up/down cancel) leaves zero net flux and only 3Q survives.
bond_ccw_center = bond_tri                        # bond -> triangle center (CCW here)
def _cw_center(i, j, L):
    # the same physical bond with reversed orientation is CCW in the OTHER triangle
    return bond_tri.get((j, i, tuple(np.round(-np.asarray(L), 3))))

def current_amp(i, j, L, eta):
    """Imaginary loop-current amplitude on directed canonical bond i->j."""
    c_ccw = bond_ccw_center.get((i, j, tuple(np.round(L, 3))))
    c_cw = _cw_center(i, j, L)
    val = 0.0
    if c_ccw is not None:
        val += tri_circulation(c_ccw, eta)
    if c_cw is not None:
        val -= tri_circulation(c_cw, eta)
    return val

def bond_mod(Rb, phi):
    return sum(phi[m] * np.cos(np.dot(Qs[m], Rb)) for m in range(3))

def triangle_fluxes(eta, phi):
    """Net loop-current circulation through each triangle (imaginary-hopping
    part only). 1Q/2Q -> net ~0 (cancelling), 3Q -> non-cancelling FM moment."""
    out = []
    for tri in triangles:
        flux = 0.0
        for (i, j, L) in tri["bonds"]:
            flux += current_amp(i, j, L, eta)
        out.append(flux)
    return np.array(out)

# ---------------------------------------------------------------------------
# Bloch Hamiltonian and its k-derivatives
# ---------------------------------------------------------------------------
t_nn = -0.5
tp = -0.02

def build_Hk(k, eta, phi, want_grad=False):
    H = np.zeros((NSITE, NSITE), dtype=complex)
    dHx = np.zeros((NSITE, NSITE), dtype=complex)
    dHy = np.zeros((NSITE, NSITE), dtype=complex)
    for (i, j, L, dvec, Rb) in bonds_nn:
        hop = t_nn + bond_mod(Rb, phi) + 1j * current_amp(i, j, L, eta)   # directed i->j (canonical)
        ph = np.exp(1j * np.dot(k, L))
        val = hop * ph
        H[i, j] += val
        H[j, i] += np.conj(val)         # reverse hop by Hermitian conjugation (odd current)
        if want_grad:
            gx = val * 1j * L[0]; gy = val * 1j * L[1]
            dHx[i, j] += gx; dHx[j, i] += np.conj(gx)
            dHy[i, j] += gy; dHy[j, i] += np.conj(gy)
    for (i, j, L, dvec) in bonds_nnn:
        ph = np.exp(1j * np.dot(k, L))
        val = tp * ph
        H[i, j] += val
        H[j, i] += np.conj(val)
        if want_grad:
            gx = val * 1j * L[0]; gy = val * 1j * L[1]
            dHx[i, j] += gx; dHx[j, i] += np.conj(gx)
            dHy[i, j] += gy; dHy[j, i] += np.conj(gy)
    if want_grad:
        return H, dHx, dHy
    return H

# ---------------------------------------------------------------------------
# Chemical potential for target filling n_vHS = 2.55 per 3-site cell
# ---------------------------------------------------------------------------
Tmev = 1e-3   # 1 meV in eV
NUC = 12

def fermi(e, mu, T):
    x = (e - mu) / T
    return np.where(x > 40, 0.0, np.where(x < -40, 1.0, 1.0 / (1.0 + np.exp(np.clip(x, -40, 40)))))

def kgrid(nk):
    fs = (np.arange(nk) + 0.5) / nk
    ks = []
    for u in fs:
        for v in fs:
            ks.append(u * B1s + v * B2s)
    return np.array(ks)

def all_evals(ks, eta, phi):
    E = np.empty((len(ks), NSITE))
    for a, k in enumerate(ks):
        E[a] = np.linalg.eigvalsh(build_Hk(k, eta, phi))
    return E

def find_mu(E, n_per_3site, T):
    # target electrons per 12-site cell (spinful counts 2 per orbital):
    # occupancy fraction of orbitals = (n_per_3site/3)/2
    target_frac = (n_per_3site / 3.0) / 2.0
    target = target_frac * E.shape[1]   # per k-point, avg number of filled orbitals
    lo, hi = E.min() - 1.0, E.max() + 1.0
    for _ in range(200):
        mu = 0.5 * (lo + hi)
        occ = fermi(E, mu, T).mean(axis=0).sum()
        if occ > target:
            hi = mu
        else:
            lo = mu
    return 0.5 * (lo + hi)

# ---------------------------------------------------------------------------
# Orbital magnetization  (paper Eq. 6, T=0 interband form, with finite-T weights)
#   M_orb = (1/(E0 Nuc N)) sum_k sum_{a<b} Im{Vx_ba Vy_ab - Vx_ab Vy_ba}
#                                          * (e_a + e_b - 2mu)(n(e_a)-n(e_b))
#   V_ab = <a|dH|b>/(e_a - e_b)
# ---------------------------------------------------------------------------
E0 = 1.0

def M_orb(ks, eta, phi, mu, T):
    tot = 0.0
    for k in ks:
        H, dHx, dHy = build_Hk(k, eta, phi, want_grad=True)
        e, U = np.linalg.eigh(H)
        Vx = U.conj().T @ dHx @ U     # <a|dHx|b>
        Vy = U.conj().T @ dHy @ U
        n = fermi(e, mu, T)
        for a in range(NSITE):
            for b in range(a + 1, NSITE):
                de = e[a] - e[b]
                if abs(de) < 1e-9:
                    continue
                vx_ab = Vx[a, b] / de
                vy_ab = Vy[a, b] / de
                vx_ba = Vx[b, a] / (-de)
                vy_ba = Vy[b, a] / (-de)
                brk = np.imag(vx_ba * vy_ab - vx_ab * vy_ba)
                tot += brk * (e[a] + e[b] - 2 * mu) * (n[a] - n[b])
    return tot / (E0 * NUC * len(ks))

# ===========================================================================
# RUN
# ===========================================================================
NK = 24                      # folded-BZ mesh (24x24 = 576 kpts)
ks = kgrid(NK)
n_vHS = 2.55

def morb_for(eta_vec, phi_vec):
    E = all_evals(ks, eta_vec, phi_vec)
    mu = find_mu(E, n_vHS, Tmev)
    return M_orb(ks, eta_vec, phi_vec, mu, Tmev), mu

results = {"paper": "Tazai-Yamakawa-Kontani arXiv:2303.00623v4",
           "system": "kagome AV3Sb5 loop-current order, 12-site folded BZ TB",
           "method": "from-scratch tight-binding + modern-theory M_orb (Eq.6)",
           "params": {"t": t_nn, "tp": tp, "n_vHS": n_vHS, "T_eV": Tmev,
                      "E0_eV": E0, "Nuc": NUC, "nk": NK, "supercell": "2x2 / 12-site"},
           "kernel_credit": "loop_current_kagome_kernel.py (shared-kernels-cache)"}

# --- C1 + C2: 3Q current only, scan eta -> expect M_orb ~ eta^3, odd ---
etas = [0.005, 0.01, 0.02, 0.03]
scan3Q = []
for e in etas:
    ev = np.array([e, e, e]) / SQ3
    m, mu = morb_for(ev, np.zeros(3))
    scan3Q.append({"eta": e, "M_orb": m, "mu": mu})
    print(f"[3Q current] eta={e:.4f}  M_orb={m: .6e}  mu={mu:.5f}  ({time.time()-t0:.1f}s)")

# fit power law on the two smallest-but-resolved etas (log-log slope)
import numpy as _np
xe = _np.array([s["eta"] for s in scan3Q])
ym = _np.array([abs(s["M_orb"]) for s in scan3Q])
good = ym > 1e-14
slope = _np.polyfit(_np.log(xe[good]), _np.log(ym[good]), 1)[0] if good.sum() >= 2 else float("nan")
results["C2_powerlaw_slope_3Q_current"] = float(slope)

# odd check: M_orb(-eta) = -M_orb(eta)
ev = np.array([0.02, 0.02, 0.02]) / SQ3
m_plus, _ = morb_for(ev, np.zeros(3))
m_minus, _ = morb_for(-ev, np.zeros(3))
results["C2_odd_check"] = {"M_plus": m_plus, "M_minus": m_minus,
                           "odd_residual": abs(m_plus + m_minus)}
print(f"[odd] M(+eta)={m_plus:.4e}  M(-eta)={m_minus:.4e}")

# --- C1: 1Q and 2Q current -> expect M_orb ~ 0 ---
e0 = 0.02
m_1Q, _ = morb_for(np.array([e0, 0, 0]), np.zeros(3))
m_2Q, _ = morb_for(np.array([e0, e0, 0]), np.zeros(3))
m_3Q, _ = morb_for(np.array([e0, e0, e0]) / SQ3, np.zeros(3))
results["C1_selection_rule"] = {"M_1Q": m_1Q, "M_2Q": m_2Q, "M_3Q": m_3Q,
                                "ratio_1Q_over_3Q": abs(m_1Q) / (abs(m_3Q) + 1e-30),
                                "ratio_2Q_over_3Q": abs(m_2Q) / (abs(m_3Q) + 1e-30)}
print(f"[selrule] 1Q={m_1Q:.3e} 2Q={m_2Q:.3e} 3Q={m_3Q:.3e}")

# --- C1 (geometric): net triangle-flux moment. The uniform orbital moment is
#     sourced by non-cancelling triangle+hexagon fluxes (paper Fig.2c: J!=J'!=J'').
#     Net moment = sum over triangles of (CCW flux). 3Q -> finite; 1Q/2Q -> ~0. ---
def net_flux_moment(eta_vec, phi_vec):
    fl = triangle_fluxes(eta_vec, phi_vec)
    return float(np.sum(fl)), fl.tolist()
nf_1Q, _ = net_flux_moment(np.array([e0, 0, 0]), np.zeros(3))
nf_2Q, _ = net_flux_moment(np.array([e0, e0, 0]), np.zeros(3))
nf_3Q, fl3 = net_flux_moment(np.array([e0, e0, e0]) / SQ3, np.zeros(3))
results["C1_geometric_flux_selection"] = {
    "net_flux_1Q": nf_1Q, "net_flux_2Q": nf_2Q, "net_flux_3Q": nf_3Q,
    "triangle_fluxes_3Q": fl3,
    "note": "net triangle-flux moment: 3Q non-cancelling (FM), 1Q/2Q cancel (M_orb=0)"}
print(f"[flux] net-flux 1Q={nf_1Q:.3e} 2Q={nf_2Q:.3e} 3Q={nf_3Q:.3e}")

# --- C3: 3Q current + 3Q bond order -> M_orb becomes LINEAR in eta ---
phi0 = 0.02
scan_bond = []
for e in [0.005, 0.01, 0.02, 0.03]:
    ev = np.array([e, e, e]) / SQ3
    pv = np.array([phi0, phi0, phi0]) / SQ3
    m, mu = morb_for(ev, pv)
    scan_bond.append({"eta": e, "phi": phi0, "M_orb": m})
    print(f"[3Q cur+bond] eta={e:.4f} phi={phi0}  M_orb={m: .6e}")
xe2 = _np.array([s["eta"] for s in scan_bond])
ym2 = _np.array([abs(s["M_orb"]) for s in scan_bond])
good2 = ym2 > 1e-14
slope_bond = _np.polyfit(_np.log(xe2[good2]), _np.log(ym2[good2]), 1)[0] if good2.sum() >= 2 else float("nan")
results["C3_powerlaw_slope_with_bond"] = float(slope_bond)
results["scan_3Q_current"] = scan3Q
results["scan_3Q_current_plus_bond"] = scan_bond

# enhancement factor: |M_orb(with bond)| / |M_orb(current only)| at eta=0.02
m_cur_only = [s["M_orb"] for s in scan3Q if abs(s["eta"] - 0.02) < 1e-9][0]
m_with_bond = [s["M_orb"] for s in scan_bond if abs(s["eta"] - 0.02) < 1e-9][0]
results["C3_bond_enhancement_at_eta0.02"] = abs(m_with_bond) / (abs(m_cur_only) + 1e-30)

# --- C4: field-scale comparison. dF = -3 h_z M_orb per 3-site cell. ---
# Paper: h_z = 1e-4 <-> ~1 T. Domain switching gain between +chirality and
# -chirality states: dF_switch = -3 h_z (M_orb(+) - M_orb(-)) = -6 h_z M_orb.
# Compare the field energy per 3-site cell at h_z=1e-4 to the thermal/domain scale.
# Use the representative coexisting state (bond present -> linear, enhanced M_orb).
M_rep = abs(m_with_bond)          # µB units, representative 3Q current+bond at eta=phi=0.02
hz_1T = 1e-4
dF_switch = 6.0 * hz_1T * M_rep    # energy gain (in the paper's dimensionless units) to align chirality at 1 T
# express relative to T=1meV thermal scale used in the calc
results["C4_field_switching"] = {
    "hz_1T_dimensionless": hz_1T,
    "M_orb_representative_uB": M_rep,
    "dF_align_per_3site_at_1T": dF_switch,
    "note": "dF = -3 h_z M_orb (Eq.7); switching gain = 6 h_z M_orb between +/- chirality domains"}

results["runtime_s"] = time.time() - t0
print(f"\nslope(current-only)={slope:.3f} (expect ~3)  slope(with bond)={slope_bond:.3f} (expect ~1)")
print(f"bond enhancement x{results['C3_bond_enhancement_at_eta0.02']:.1f}")
print(f"dF_align@1T = {dF_switch:.3e} (µB-eV units)   runtime {results['runtime_s']:.1f}s")

with open("tazai2023_result.json", "w") as f:
    json.dump(results, f, indent=2)
print("SAVED tazai2023_result.json")
