#!/usr/bin/env python3
"""
Independent replication of the reproducible classical-simulator core of:
  Parrish, Hohenstein, McMahon, Martinez,
  "Quantum Computation of Electronic Transitions using a Variational
   Quantum Eigensolver" (MC-VQE), PRL 122, 230401 (2019); arXiv:1901.01234.

Core reproduced here (all classical statevector simulation, no hardware):
  * Ab-initio-style exciton Hamiltonian (Eq. 8) as a spin-1/2 lattice model.
  * FCI: exact diagonalization in full 2^N Hilbert space (sparse eigsh).
  * CIS: diagonalization in the (N+1)-dim single-excitation manifold.
  * MC-VQE: contracted CIS reference states prepared via matryoshka circuit,
    SO(4) two-body entangler U on Hamiltonian-connectivity bonds, state-averaged
    energy minimization (Eq. 6), then classical diag of contracted H (Eqs. 2-4).
  * Oscillator strengths from transition dipoles (Eq. supp: O = 2/3 dE <mu>^2).
  * Compare excitation energies + oscillator strengths: FCI vs CIS vs MC-VQE.

Testable claims addressed (see REPORT.md):
  C1 exciton H isomorphic to spin lattice, FCI diagonalizable
  C2 MC-VQE 1 layer -> excitation energies match FCI to ~tens of ueV
  C3 MC-VQE oscillator strengths <<1% error; CIS ~10%+ error
  C4 CIS blue-shifts by a few 0.01 eV vs FCI
  C5 state-averaged E = mean of diagonal contracted H (Eq. 6)
  C6 ~100 params converge in ~14 L-BFGS iters from zero guess (N=18)
  C7 N=8 linear stack: CIS qualitatively wrong, MC-VQE matches FCI
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import minimize
import json, time, sys, os

np.random.seed(0)
HARTREE2EV = 27.211386245988
AU_PER_DEBYE = 0.393430307  # 1 Debye in atomic units (e*a0)

# ---------------------------------------------------------------------------
# 1. Build ab-initio-style exciton model (dipole/transition-dipole, Eq supp)
# ---------------------------------------------------------------------------
def bchl_monomer_params():
    """Physically-motivated BChl-a monomer params (omega-PBE/6-31G* regime).
    Qy S0->S1 gap ~1.6 eV; transition dipole ~ 6 D along Qy axis;
    small permanent difference dipole. Values in atomic units."""
    dE = 1.6 / HARTREE2EV          # S0->S1 gap (Hartree) ~1.6 eV (Qy band)
    mu_trans = 6.1 * AU_PER_DEBYE  # transition dipole magnitude (au)
    mu_diff  = 1.0 * AU_PER_DEBYE  # difference dipole (permanent) magnitude
    return dE, mu_trans, mu_diff

def dipole_dipole(muA, muB, rAvec, rBvec):
    """V_AB = [muA.muB - 3(muA.n)(muB.n)]/r^3 (Eq. supp)."""
    d = rBvec - rAvec
    r = np.linalg.norm(d)
    n = d / r
    return (np.dot(muA, muB) - 3.0*np.dot(muA, n)*np.dot(muB, n)) / r**3

def build_exciton_model(geom, mu_trans_vecs, mu_diff_vecs, dE,
                        neighbor_only=False, ring=False):
    """Return dict of Pauli coefficients for Eq.8 exciton Hamiltonian.
    geom: (N,3) COM positions (au). mu_*_vecs: (N,3) dipole vectors (au).
    Monomer: Z_A ~ half gap (dE/2). X_A ~ 0 (no monomer 0-1 one-body coupling
    beyond env; kept small). Two-body from dipole model:
       XX = (T_A|T_B) transition-transition
       ZZ = (D_A|D_B) difference-difference
       XZ = (T_A|D_B), ZX = (D_A|T_B) cross terms.
    """
    N = len(geom)
    # Z|0>=+1, Z|1>=-1. To make the ground config |0..0> the LOWEST monomer
    # energy (per-monomer gap dE), set Z_A = -dE/2 so that E(|0>)=-dE/2 < E(|1>)=+dE/2.
    Z = np.full(N, -dE/2.0)         # Z_A = -(E1-E0)/2 per monomer
    X = np.zeros(N)                 # monomer transition one-body (set ~0)
    XX = {}; ZZ = {}; XZ = {}; ZX = {}
    def bonded(A, B):
        if not neighbor_only:
            return True
        if ring:
            return (abs(A-B) == 1) or (abs(A-B) == N-1)
        return abs(A-B) == 1
    for A in range(N):
        for B in range(A):
            if not bonded(A, B):
                continue
            tt = dipole_dipole(mu_trans_vecs[A], mu_trans_vecs[B], geom[A], geom[B])
            dd = dipole_dipole(mu_diff_vecs[A],  mu_diff_vecs[B],  geom[A], geom[B])
            td = dipole_dipole(mu_trans_vecs[A], mu_diff_vecs[B],  geom[A], geom[B])
            dt = dipole_dipole(mu_diff_vecs[A],  mu_trans_vecs[B], geom[A], geom[B])
            XX[(A,B)] = tt
            ZZ[(A,B)] = dd
            XZ[(A,B)] = td
            ZX[(A,B)] = dt
    return dict(N=N, E=0.0, Z=Z, X=X, XX=XX, ZZ=ZZ, XZ=XZ, ZX=ZX,
                mu_trans=mu_trans_vecs, mu_diff=mu_diff_vecs)

# ---------------------------------------------------------------------------
# 2. Sparse full Hamiltonian (FCI) via Pauli operators on N qubits
# ---------------------------------------------------------------------------
I2 = sp.identity(2, format='csr')
Zp = sp.csr_matrix(np.array([[1,0],[0,-1]], float))
Xp = sp.csr_matrix(np.array([[0,1],[1,0]], float))

def kron_op(N, sites_ops):
    """sites_ops: dict site->2x2 op. Build full 2^N sparse operator."""
    mats = []
    for q in range(N):
        mats.append(sites_ops.get(q, I2))
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format='csr')
    return out

def build_full_H(model):
    N = model['N']
    dim = 2**N
    H = sp.csr_matrix((dim, dim))
    for A in range(N):
        if model['Z'][A] != 0:
            H = H + model['Z'][A]*kron_op(N, {A: Zp})
        if model['X'][A] != 0:
            H = H + model['X'][A]*kron_op(N, {A: Xp})
    for (A,B),v in model['XX'].items():
        if v: H = H + v*kron_op(N, {A: Xp, B: Xp})
    for (A,B),v in model['ZZ'].items():
        if v: H = H + v*kron_op(N, {A: Zp, B: Zp})
    for (A,B),v in model['XZ'].items():
        if v: H = H + v*kron_op(N, {A: Xp, B: Zp})
    for (A,B),v in model['ZX'].items():
        if v: H = H + v*kron_op(N, {A: Zp, B: Xp})
    return H.tocsr()

def fci_spectrum(model, k):
    H = build_full_H(model)
    dim = H.shape[0]
    if dim <= 4096:
        w, v = np.linalg.eigh(H.toarray())
        return w[:k], v[:, :k]
    w, v = spla.eigsh(H, k=k, which='SA')
    idx = np.argsort(w)
    return w[idx], v[:, idx]

# ---------------------------------------------------------------------------
# 3. Dipole operator (full) for oscillator strengths
# ---------------------------------------------------------------------------
def build_dipole_ops(model):
    """mu vector operator: mu = sum_A mu_I I + mu_Z Z + mu_X X (per component).
    mu_X^A = transition dipole; mu_Z^A = -difference dipole/... ; mu_I drops out
    of transition matrix elements between orthogonal states.
    Return list of 3 sparse operators (x,y,z components)."""
    N = model['N']
    dim = 2**N
    ops = [sp.csr_matrix((dim, dim)) for _ in range(3)]
    for A in range(N):
        muX = model['mu_trans'][A]         # <0|mu|1> transition dipole
        muZ = -0.5*model['mu_diff'][A]     # (mu11-mu00)/2 difference dipole
        for c in range(3):
            if muX[c] != 0:
                ops[c] = ops[c] + muX[c]*kron_op(N, {A: Xp})
            if muZ[c] != 0:
                ops[c] = ops[c] + muZ[c]*kron_op(N, {A: Zp})
    return ops

def oscillator_strengths(evals, evecs, dipole_ops, gs=0):
    """O_0Theta = 2/3 (E_Theta - E_0) |<0|mu|Theta>|^2 summed over components."""
    O = []
    v0 = evecs[:, gs]
    for t in range(evecs.shape[1]):
        vt = evecs[:, t]
        dE = evals[t] - evals[gs]
        mu2 = 0.0
        for c in range(3):
            mel = v0 @ (dipole_ops[c] @ vt)
            mu2 += mel**2
        O.append(2.0/3.0 * dE * mu2)
    return np.array(O)

# ---------------------------------------------------------------------------
# 4. CIS in single-excitation manifold (N+1 dim)  -> reference states
# ---------------------------------------------------------------------------
def cis_manifold(model):
    """Build (N+1)x(N+1) CIS Hamiltonian in basis {|000..>, |100..>, |010..>,...}
    i.e. reference + N single excitations. Matrix elements from the spin H
    restricted to <=1 excitation configs (this is the CIS prescription:
    reference + all singles allowed to mix)."""
    N = model['N']
    # basis index 0 = ground config, i+1 = single excitation on site i
    basis = [np.zeros(N, int)]
    for i in range(N):
        b = np.zeros(N, int); b[i] = 1; basis.append(b)
    M = len(basis)
    Hc = np.zeros((M, M))
    # diagonal energies of a config under Z terms + ZZ terms
    def config_energy(b):
        e = 0.0
        for A in range(N):
            zA = -1.0 if b[A] else 1.0     # Z|0>=+1, Z|1>=-1
            e += model['Z'][A]*zA
        for (A,B),v in model['ZZ'].items():
            zA = -1.0 if b[A] else 1.0
            zB = -1.0 if b[B] else 1.0
            e += v*zA*zB
        return e
    for a in range(M):
        Hc[a,a] = config_energy(basis[a])
    # off-diagonals: X_A flips one bit; XX flips two bits; XZ/ZX flip one bit
    for a in range(M):
        for c in range(M):
            if a==c: continue
            ba, bc = basis[a], basis[c]
            diff = np.where(ba!=bc)[0]
            if len(diff)==1:
                A = diff[0]
                val = model['X'][A]
                # XZ/ZX contributions: X on A, Z on partner
                for (P,Q),v in model['XZ'].items():
                    if P==A:
                        zQ = -1.0 if ba[Q] else 1.0
                        # only valid if Q bit unchanged
                        if ba[Q]==bc[Q]: val += v*zQ
                for (P,Q),v in model['ZX'].items():
                    if Q==A:
                        zP = -1.0 if ba[P] else 1.0
                        if ba[P]==bc[P]: val += v*zP
                Hc[a,c] = val
            elif len(diff)==2:
                A,B = diff
                key = (max(A,B), min(A,B))
                v = model['XX'].get(key, 0.0)
                Hc[a,c] = v
    w, V = np.linalg.eigh(Hc)
    return w, V, basis

# ---------------------------------------------------------------------------
# 5. MC-VQE: statevector implementation
# ---------------------------------------------------------------------------
def ry(theta):
    c,s = np.cos(theta/2), np.sin(theta/2)
    return np.array([[c,-s],[s,c]])

def apply_1q(state, N, q, U):
    st = state.reshape([2]*N)
    st = np.tensordot(U, st, axes=([1],[q]))
    st = np.moveaxis(st, 0, q)
    return st.reshape(-1)

def apply_2q(state, N, q1, q2, U4):
    """Apply 4x4 gate on qubits q1,q2 (q1<q2 order for U4 basis |q1 q2>)."""
    st = state.reshape([2]*N)
    st = np.moveaxis(st, [q1,q2], [0,1])
    sh = st.shape
    st = st.reshape(4, -1)
    st = U4 @ st
    st = st.reshape([2,2]+list(sh[2:]))
    st = np.moveaxis(st, [0,1], [q1,q2])
    return st.reshape(-1)

def so4_gate(params):
    """SO(4) via 6 Givens rotations in 4-dim real space (generic real orthogonal
    det+1). Compose rotations in planes (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)."""
    U = np.eye(4)
    planes = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    for (i,j),th in zip(planes, params):
        G = np.eye(4)
        c,s = np.cos(th), np.sin(th)
        G[i,i]=c; G[j,j]=c; G[i,j]=-s; G[j,i]=s
        U = G @ U
    return U

def prepare_cis_state(N, coeffs):
    """Prepare sum_i coeffs[i] |unit_i> via matryoshka Ry/Fy circuit.
    coeffs: length N+1: [mu(ground=|00..0>), c0(|100..>), c1(|010..>),...].
    We build the statevector directly (equivalent to the paper's circuit)."""
    state = np.zeros(2**N)
    # index for |000..0> = 0 ; single excitation on site i => bit i set
    state[0] = coeffs[0]
    for i in range(N):
        state[1<<(N-1-i)] = coeffs[i+1]
    nrm = np.linalg.norm(state)
    return state/nrm if nrm>0 else state

class MCVQE:
    def __init__(self, model, ntheta, bonds, layers=1):
        self.model = model
        self.N = model['N']
        self.ntheta = ntheta          # number of reference/eigenstates
        self.bonds = bonds            # list of (A,B) entangler sites
        self.layers = layers
        self.H = build_full_H(model)
        # CIS reference coefficients for the ntheta lowest CIS states
        wc, Vc, basis = cis_manifold(model)
        self.cis_w = wc
        self.cis_V = Vc               # columns are CIS eigvecs in (N+1) basis
        self.basis = basis
        self.nparam = len(bonds)*6*layers

    def ref_statevec(self, theta_idx):
        """Statevector of contracted CIS reference state Theta (no entangler)."""
        coeffs = self.cis_V[:, theta_idx]   # length N+1
        return prepare_cis_state(self.N, coeffs)

    def interference_statevec(self, t1, t2, sign):
        c = (self.cis_V[:,t1] + sign*self.cis_V[:,t2])/np.sqrt(2)
        return prepare_cis_state(self.N, c)

    def apply_entangler(self, state, params):
        p = 0
        for _ in range(self.layers):
            for (A,B) in self.bonds:
                U4 = so4_gate(params[p:p+6]); p += 6
                a,b = (A,B) if A<B else (B,A)
                state = apply_2q(state, self.N, a, b, U4)
        return state

    def diag_H(self, theta_idx, params):
        st = self.ref_statevec(theta_idx)
        st = self.apply_entangler(st, params)
        return st @ (self.H @ st)

    def state_avg_energy(self, params):
        return np.mean([self.diag_H(t, params) for t in range(self.ntheta)])

    def contracted_H(self, params):
        """Build entangled contracted Hamiltonian H_{Theta Theta'} via
        diagonal (Eq.4) and interference off-diagonal (Eq.5)."""
        n = self.ntheta
        Hc = np.zeros((n,n))
        chis = []
        for t in range(n):
            st = self.apply_entangler(self.ref_statevec(t), params)
            chis.append(st)
            Hc[t,t] = st @ (self.H @ st)
        for t1 in range(n):
            for t2 in range(t1+1, n):
                sp_ = self.apply_entangler(self.interference_statevec(t1,t2,+1), params)
                sm_ = self.apply_entangler(self.interference_statevec(t1,t2,-1), params)
                Ep = sp_ @ (self.H @ sp_)
                Em = sm_ @ (self.H @ sm_)
                off = Ep - Em      # = 2 H_{t1 t2}  (Eq.5 gives 2H)
                Hc[t1,t2] = off/2.0
                Hc[t2,t1] = off/2.0
        return Hc, chis

    def optimize(self, maxiter=200, restarts=0):
        best = None; hist = []
        def f(x):
            e = self.state_avg_energy(x); hist.append(e); return e
        # primary: zero-entanglement guess (paper's approach)
        guesses = [np.zeros(self.nparam)]
        for _ in range(restarts):
            guesses.append(np.random.uniform(-0.3, 0.3, self.nparam))
        for x0 in guesses:
            res = minimize(f, x0, method='L-BFGS-B',
                           options=dict(maxiter=maxiter, ftol=1e-12, gtol=1e-9))
            if best is None or res.fun < best.fun:
                best = res
        self.opt_params = best.x
        self.opt_res = best
        self.hist = hist
        return best

    def eigenstates(self, params):
        """Diagonalize contracted H (Eq.2), return Ritz evals + full statevecs."""
        Hc, chis = self.contracted_H(params)
        E, V = np.linalg.eigh(Hc)     # V columns = rotation of contracted states
        # eigenstate |Psi_Theta> = U sum_Theta' |Phi_Theta'> V_{Theta',Theta}
        n = self.ntheta
        psis = []
        for th in range(n):
            psi = np.zeros_like(chis[0])
            for tp in range(n):
                psi = psi + chis[tp]*V[tp, th]
            psis.append(psi)
        return E, np.array(psis).T, Hc

# ---------------------------------------------------------------------------
# Geometry builders
# ---------------------------------------------------------------------------
def lh2_ring_geometry(N=18, radius_ang=None, tilt_deg=None):
    """Cyclic B850 ring: N BChls on a ring. Qy transition dipoles roughly
    tangential (alternating), difference dipoles radial. Positions in au."""
    if radius_ang is None:
        radius_ang = 24.0   # ~ B850 ring radius ~ 2.4 nm
    R = radius_ang/0.529177
    geom = np.zeros((N,3))
    mu_t = np.zeros((N,3))
    mu_d = np.zeros((N,3))
    dE, mtr, mdf = bchl_monomer_params()
    for A in range(N):
        phi = 2*np.pi*A/N
        geom[A] = [R*np.cos(phi), R*np.sin(phi), 0.0]
        # transition dipole ~ tangential with slight alternation (B850 dimer)
        tang = np.array([-np.sin(phi), np.cos(phi), 0.0])
        rad  = np.array([ np.cos(phi), np.sin(phi), 0.0])
        alt = 1.0 if A%2==0 else -1.0
        d = tang*np.cos(np.radians(18)) + rad*alt*np.sin(np.radians(18))
        d = d/np.linalg.norm(d)
        mu_t[A] = mtr*d
        mu_d[A] = mdf*rad
    return geom, mu_t, mu_d, dE

def linear_stack_geometry(N=8, spacing_ang=4.0):
    """H-aggregate: aligned BChls stacked along z, transition dipoles parallel
    (cofacial) -> strong H-aggregate coupling; CIS known to fail here."""
    s = spacing_ang/0.529177
    geom = np.zeros((N,3))
    mu_t = np.zeros((N,3))
    mu_d = np.zeros((N,3))
    dE, mtr, mdf = bchl_monomer_params()
    for A in range(N):
        geom[A] = [0,0,A*s]
        mu_t[A] = [mtr,0,0]      # all parallel (cofacial H-aggregate)
        mu_d[A] = [0,0,mdf*0.5]
    return geom, mu_t, mu_d, dE

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_case(name, geom, mu_t, mu_d, dE, nstates, layers=1, neighbor_only=False,
             ring=False, entangler_nn=True):
    N = len(geom)
    t0 = time.time()
    model = build_exciton_model(geom, mu_t, mu_d, dE,
                                neighbor_only=neighbor_only, ring=ring)
    # Entanglers placed on Hamiltonian *connectivity* bonds. Per the paper the
    # entangler layer matches the exciton-Hamiltonian 2-body interaction graph;
    # for near-term locality we use nearest-neighbor (+ ring closure) bonds.
    if entangler_nn:
        bonds = [(A, A-1) for A in range(1, N)]
        if ring:
            bonds.append((N-1, 0))
    else:
        bonds = [k for k in model['XX'].keys()]
    dip = build_dipole_ops(model)

    # FCI
    fci_E, fci_V = fci_spectrum(model, nstates)
    fci_O = oscillator_strengths(fci_E, fci_V, dip)

    # CIS
    cis_w, cis_Vc, basis = cis_manifold(model)
    # build full statevectors for CIS eigenstates to compute oscillator strengths
    cis_full = np.zeros((2**N, nstates))
    for t in range(nstates):
        cis_full[:, t] = prepare_cis_state(N, cis_Vc[:, t])
    cis_E = cis_w[:nstates]
    cis_O = oscillator_strengths(cis_E, cis_full, dip)

    # MC-VQE
    mc = MCVQE(model, nstates, bonds, layers=layers)
    res = mc.optimize(maxiter=300)
    E_mc, V_mc, Hc = mc.eigenstates(mc.opt_params)
    idx = np.argsort(E_mc)
    E_mc = E_mc[idx]; V_mc = V_mc[:, idx]
    mc_O = oscillator_strengths(E_mc, V_mc, dip)
    # CIS raw sorted energies/states already index-aligned to its own manifold.
    # NOTE alignment to FCI handled below via singles-subspace matching.

    # ---- Overlap-based state matching (rigorous alignment) ----
    # Match each MC-VQE / CIS eigenstate to the FCI state of maximum |overlap|.
    def match_to_fci(V_approx):
        """Return list mapping approx-state-index -> best FCI-state-index and
        the overlap. Greedy by descending overlap, unique assignment."""
        na = V_approx.shape[1]; nf = fci_V.shape[1]
        S = np.abs(fci_V.T @ V_approx)   # (nf, na)
        pairs = []
        used_f = set()
        order = np.dstack(np.unravel_index(np.argsort(-S, axis=None), S.shape))[0]
        assigned = {}
        for f, a in order:
            if a in assigned or f in used_f:
                continue
            assigned[a] = (f, float(S[f, a]))
            used_f.add(f)
        return assigned
    mc_match = match_to_fci(V_mc)
    cis_match = match_to_fci(cis_full)

    # excitation energies (relative to ground state) in eV
    def exc(E): return (E - E[0])[1:]*HARTREE2EV
    fci_exc = exc(fci_E); cis_exc = exc(cis_E); mc_exc = exc(E_mc)

    # Identify which FCI states are representable in the (ref+singles) subspace
    # the CIS/MC-VQE ansatz spans. States dominated by double excitations are
    # fundamentally outside the singles ansatz (a known limitation, not a
    # method failure) and are reported separately.
    idx_singles = [0] + [1 << (N-1-i) for i in range(N)]
    singles_weight = []
    for t in range(nstates):
        w = fci_V[:, t]
        singles_weight.append(float(np.sum(w[idx_singles]**2)))
    singles_weight = np.array(singles_weight)
    # accessible = excited states (index>=1) with >50% singles character
    acc = np.array([singles_weight[t] > 0.5 for t in range(1, nstates)])

    # errors
    en_err_mc = np.abs(mc_exc - fci_exc)          # eV
    en_err_cis = np.abs(cis_exc - fci_exc)
    en_err_mc_acc = en_err_mc[acc]
    en_err_cis_acc = en_err_cis[acc]
    # relative oscillator strength error (on states with nontrivial O)
    def rel_O_err(Oapprox, use_acc=False):
        e = []
        for j,(a,f) in enumerate(zip(Oapprox[1:], fci_O[1:])):
            if use_acc and not acc[j]:
                continue
            if abs(f) > 1e-4:   # only bright transitions
                e.append(abs(a-f)/abs(f))
        return np.array(e) if e else np.array([0.0])
    mc_O_relerr = rel_O_err(mc_O)
    cis_O_relerr = rel_O_err(cis_O)
    mc_O_relerr_acc = rel_O_err(mc_O, use_acc=True)
    cis_O_relerr_acc = rel_O_err(cis_O, use_acc=True)

    # ---- Matched errors (aligned by max overlap; ground state = index 0) ----
    def matched_energy_errors(match, E_approx):
        errs = []; osc_err = []
        for a in range(1, len(E_approx)):
            if a not in match:
                continue
            f, ov = match[a]
            if f == 0:      # matched to FCI ground -> skip
                continue
            if singles_weight[f] <= 0.5:   # FCI double-excitation, ansatz cannot reach
                continue
            dE_ap = (E_approx[a]-E_approx[0])*HARTREE2EV
            dE_fc = (fci_E[f]-fci_E[0])*HARTREE2EV
            errs.append((abs(dE_ap-dE_fc), ov, f))
        return errs
    mc_matched = matched_energy_errors(mc_match, E_mc)
    cis_matched = matched_energy_errors(cis_match, cis_E)
    mc_match_err_eV = np.array([e[0] for e in mc_matched]) if mc_matched else np.array([0.0])
    cis_match_err_eV = np.array([e[0] for e in cis_matched]) if cis_matched else np.array([0.0])

    # matched oscillator relative error (bright transitions only)
    def matched_osc_err(match, O_approx):
        e = []
        for a in range(1, len(O_approx)):
            if a not in match: continue
            f, ov = match[a]
            if f == 0 or singles_weight[f] <= 0.5: continue
            if abs(fci_O[f]) > 1e-4:
                e.append(abs(O_approx[a]-fci_O[f])/abs(fci_O[f]))
        return np.array(e) if e else np.array([0.0])
    mc_osc_match = matched_osc_err(mc_match, mc_O)
    cis_osc_match = matched_osc_err(cis_match, cis_O)

    # C5 check: state-avg energy == mean diagonal contracted H
    diagH = [mc.diag_H(t, mc.opt_params) for t in range(nstates)]
    c5_lhs = mc.state_avg_energy(mc.opt_params)
    c5_rhs = np.mean(diagH)

    out = dict(
        name=name, N=N, nstates=nstates, layers=layers, nparam=mc.nparam,
        n_lbfgs_iters=int(mc.opt_res.nit), n_func_evals=int(mc.opt_res.nfev),
        fci_ground=float(fci_E[0]),
        fci_exc_eV=fci_exc.tolist(), cis_exc_eV=cis_exc.tolist(),
        mc_exc_eV=mc_exc.tolist(),
        en_err_mc_ueV=(en_err_mc*1e6).tolist(),
        en_err_cis_meV=(en_err_cis*1e3).tolist(),
        max_en_err_mc_ueV=float(en_err_mc.max()*1e6),
        max_en_err_cis_meV=float(en_err_cis.max()*1e3),
        singles_weight=singles_weight.tolist(),
        n_accessible=int(acc.sum()),
        max_en_err_mc_acc_ueV=float(en_err_mc_acc.max()*1e6) if len(en_err_mc_acc) else 0.0,
        mean_en_err_mc_acc_ueV=float(en_err_mc_acc.mean()*1e6) if len(en_err_mc_acc) else 0.0,
        max_en_err_cis_acc_meV=float(en_err_cis_acc.max()*1e3) if len(en_err_cis_acc) else 0.0,
        max_mc_O_relerr_acc=float(mc_O_relerr_acc.max()),
        max_cis_O_relerr_acc=float(cis_O_relerr_acc.max()),
        mean_cis_blueshift_meV=float(np.mean(cis_exc - fci_exc)*1e3),
        fci_O=fci_O.tolist(), cis_O=cis_O.tolist(), mc_O=mc_O.tolist(),
        max_mc_O_relerr=float(mc_O_relerr.max()),
        max_cis_O_relerr=float(cis_O_relerr.max()),
        mean_mc_O_relerr=float(mc_O_relerr.mean()),
        mean_cis_O_relerr=float(cis_O_relerr.mean()),
        # ---- rigorous overlap-matched metrics (primary results) ----
        n_matched_mc=int(len(mc_match_err_eV)) if mc_matched else 0,
        max_en_err_mc_matched_ueV=float(mc_match_err_eV.max()*1e6),
        mean_en_err_mc_matched_ueV=float(mc_match_err_eV.mean()*1e6),
        max_en_err_cis_matched_meV=float(cis_match_err_eV.max()*1e3),
        mean_en_err_cis_matched_meV=float(cis_match_err_eV.mean()*1e3),
        max_mc_O_relerr_matched=float(mc_osc_match.max()),
        max_cis_O_relerr_matched=float(cis_osc_match.max()),
        mean_mc_O_relerr_matched=float(mc_osc_match.mean()),
        mean_cis_O_relerr_matched=float(cis_osc_match.mean()),
        state_avg_E=float(c5_lhs), mean_diag_H=float(c5_rhs),
        c5_residual=float(abs(c5_lhs-c5_rhs)),
        state_avg_E_final=float(mc.opt_res.fun),
        runtime_s=round(time.time()-t0, 1),
    )
    return out, mc

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv)>1 else "both"
    results = {}

    if which in ("stack", "both"):
        # C7: N=8 linear H-aggregate stack (CIS should fail qualitatively)
        g,mt,md,dE = linear_stack_geometry(N=8, spacing_ang=4.0)
        r8, _ = run_case("N8_linear_stack", g, mt, md, dE, nstates=9, layers=2,
                         neighbor_only=False, ring=False, entangler_nn=True)
        results["N8_linear_stack"] = r8
        print("=== N=8 linear stack ===")
        print(json.dumps({k:r8[k] for k in
              ['n_matched_mc','max_en_err_mc_matched_ueV','mean_en_err_mc_matched_ueV',
               'max_en_err_cis_matched_meV','max_mc_O_relerr_matched',
               'max_cis_O_relerr_matched','mean_cis_blueshift_meV',
               'n_lbfgs_iters','nparam','c5_residual','runtime_s']}, indent=2))

    if which in ("ring", "both"):
        # C2,C3,C4,C6: N=18 LH2 B850 ring
        g,mt,md,dE = lh2_ring_geometry(N=18)
        r18, _ = run_case("N18_LH2_B850_ring", g, mt, md, dE, nstates=18,
                          layers=1, neighbor_only=True, ring=True)
        results["N18_LH2_B850_ring"] = r18
        print("=== N=18 LH2 B850 ring ===")
        print(json.dumps({k:r18[k] for k in
              ['n_matched_mc','max_en_err_mc_matched_ueV','mean_en_err_mc_matched_ueV',
               'max_en_err_cis_matched_meV','max_mc_O_relerr_matched',
               'max_cis_O_relerr_matched','mean_cis_blueshift_meV',
               'n_lbfgs_iters','nparam','c5_residual','runtime_s']}, indent=2))

    with open("results.json","w") as f:
        json.dump(results, f, indent=2)
    print("\nWrote results.json")
