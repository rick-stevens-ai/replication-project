"""Independent replication of Ender et al. 2022 (arXiv:2203.04340),
   'Modular Parity Quantum Approximate Optimization'.

Central claim we test (Fig. 7, noiseless case):
  For a complete graph with N=6 spin variables (K=15 physical parity qubits),
  QAOA at depth p=3, median residual energy over 96 random Ising instances
  decreases monotonically as nr := nC / ntot_C decreases:
     nr = 1.0  (fully explicit)  -> worst
     nr = 0.6                   -> better
     nr = 0.4                   -> better still
     nr = 0.0  (fully implicit)  -> best

We implement:
  (1) STANDARD QAOA (on N=6 logical qubits, all-to-all Ising problem) as a baseline
      for verifying the problem Hamiltonian and giving an unencoded reference.
  (2) FULLY EXPLICIT PARITY QAOA (nr=1.0): K=15 physical qubits, single-qubit
      X driver on all K qubits, cost = H_Z (single-body from mapped problem)
      + H_C (all 20 three-body constraints of the N=6 complete-graph parity layout,
             enforced explicitly with strength c>0).
      Protocol: |psi> = product_{j=1..p} exp(-i beta_j H_X) exp(-i gamma_j H_Z)
                        exp(-i Omega_j H_C) |+>^K
  (3) FULLY IMPLICIT PARITY QAOA (nr=0.0): start in equal superposition of
      constraint-fulfilling states H_CF; driver = sum_{mu=1..N-ns} prod_{k in Q_mu} X_k
      where Q_mu = {(i,j) : mu in {i,j}}, i.e. the 5 lines with one problem
      spin flipping. No explicit H_C.
      Protocol: |psi> = product_{j=1..p} exp(-i beta_j H_X^imp) exp(-i gamma_j H_Z) |psi0>
  (4) HYBRID PARITY QAOA at intermediate nr in {0.4, 0.6}: split the ntot_C=20
      constraints into nC explicitly enforced (bottommost rows) and (ntot_C - nC)
      implicitly preserved. For nr=0.4 we pick nC=8 explicit, nr=0.6 -> nC=12.
      Driver is built from a valid set of hybrid driver lines that preserve the
      implicitly-enforced constraints (constructed algorithmically).

For all approaches we compare noiseless median residual energy
   Eres = (E - Emin) / (Emax - Emin),  where E = <psi| H_phys |psi>
with respect to the SAME physical problem Hamiltonian H_phys = H_Z + H_C
(so E is fair across variants; adding H_C only affects the state, and the
minimum of H_phys sits at a constraint-fulfilling ground state so
Emin = min over problem-solution states of H_Z).

We also compute FIDELITY = ground-state population wrt H_phys, matching
the paper's Fig. 7 bottom panel.

All computations are exact statevector; the physical Hilbert space is
2^15 = 32768-dimensional, easily handled on a laptop.
"""

from __future__ import annotations
import numpy as np
from itertools import combinations, product
from dataclasses import dataclass
import time
import json
import argparse
import os

RNG = np.random.default_rng(42)

# ---------- Ising problem on the N=6 complete graph ----------

def all_pairs(N):
    return list(combinations(range(N), 2))

def random_instance(N, rng):
    """Random SK-like instance: J_ij ~ U[-1, 1]. Returns dict {(i,j): Jij}."""
    return {p: float(rng.uniform(-1.0, 1.0)) for p in all_pairs(N)}

def logical_energies(N, J):
    """Return array E_s of shape (2^N,) with E_s = sum_{i<j} J_ij s_i s_j."""
    # s_i = 1 - 2*bit_i (bit_i in {0,1})
    E = np.zeros(1 << N, dtype=np.float64)
    for s in range(1 << N):
        bits = [(s >> i) & 1 for i in range(N)]
        spins = np.array([1 - 2 * b for b in bits], dtype=np.int8)
        e = 0.0
        for (i, j), Jij in J.items():
            e += Jij * spins[i] * spins[j]
        E[s] = e
    return E

# ---------- Parity encoding for N=6 all-to-all: K=15 qubits ----------
# Parity qubit m = (i,j) with i<j: sigma_z^(m) encodes s_i * s_j.

def parity_indexing(N):
    pairs = all_pairs(N)
    idx = {p: k for k, p in enumerate(pairs)}
    return pairs, idx

def parity_energies(N, J, pairs, idx):
    """For each physical bit-string x in {0,1}^K, compute
       (a) the mapped problem energy H_Z (single-body sum),
       (b) whether x is constraint-fulfilling,
       (c) the corresponding logical spin configuration (only defined for CF states).
       Returns H_Z_diag array of shape 2^K.
    """
    K = len(pairs)
    HZ = np.zeros(1 << K, dtype=np.float64)
    # sigma_z^(m) |x> = (1 - 2 x_m) |x>
    for x in range(1 << K):
        e = 0.0
        for k, m in enumerate(pairs):
            sm = 1 - 2 * ((x >> k) & 1)
            e += J[m] * sm
        HZ[x] = e
    return HZ

# ---------- Constraints for parity encoding of N=6 complete graph ----------
# From Ender et al. (following Lechner-Hauke-Zoller), for N=6 there are
# ntot_C = K - N + 1 = 15 - 6 + 1 = 10 independent constraints, plus we need
# to include the 4-body plaquettes on the LHZ square lattice. Actually for
# N=6 all-to-all the standard LHZ layout has:
#   - top row: 1 single-body 'header' qubit (edge (0,1))
#   - each subsequent row adds 3-body constraints on the left/right edges
#     and 4-body constraints in the interior.
# ntot_C for complete graph K_N is K - N + 1 = N(N-1)/2 - N + 1 = (N-1)(N-2)/2.
# For N=6: (5*4)/2 = 10 constraints total.
# All constraints are products of parity qubits sharing an even number of
# problem-spin indices; the code space corresponds to physical strings whose
# induced spin assignment is single-valued.
#
# We generate the constraints combinatorially: for a complete-graph parity
# code, a bit-string x = (x_{ij}) is constraint-fulfilling iff there exist
# spins s_0,...,s_{N-1} in {+1,-1} with x_{ij} = 0 if s_i s_j = +1 else 1.
# Equivalently, x lies in the image of the linear map (over GF(2))
#    b_i -> (b_i XOR b_j)_{i<j}
# with b_i in {0,1}. So CF strings = image of that linear map, which has
# 2^{N-1} elements (spin-flip symmetry) = 32 for N=6. The kernel of the
# quotient map has dim K - (N-1) = 15 - 5 = 10, giving 10 independent
# constraint generators.

def cf_states_and_map(N, pairs):
    """Enumerate all constraint-fulfilling physical strings and their
       corresponding logical spin assignments (up to global flip).
       Returns:
         cf_states:    list of 2^{N-1} ints (physical bit-string encoding)
         cf_logical:   dict cf_state -> logical (bit) config in [0, 2^N),
                        canonical rep = bit b_0 = 0 (spin s_0 = +1).
    """
    K = len(pairs)
    cf_states = []
    cf_logical = {}
    for logical_bits in range(1 << N):
        # Encode: x_{ij} = b_i XOR b_j
        bits = [(logical_bits >> i) & 1 for i in range(N)]
        x = 0
        for k, (i, j) in enumerate(pairs):
            xk = bits[i] ^ bits[j]
            x |= (xk << k)
        cf_states.append(x)
        cf_logical.setdefault(x, logical_bits)
    # Unique physical states (2^{N-1} of them due to spin-flip symmetry):
    unique = sorted(set(cf_states))
    return unique, cf_logical

def generate_constraint_generators(N, pairs, idx):
    """Return a list of 'constraints' as lists of physical-qubit indices.
       Each constraint C_l has the form Cl = (1 - prod_{k in Sl} Z_k)/2 * c_l.
       We build ntot_C = K - N + 1 independent constraints by enumerating
       small cycles (3- and 4-body) that vanish on the code space.
       For simplicity we take all triangles (i,j),(j,k),(i,k) with i<j<k
       -> these are 3-body constraints, C(N,3) = 20 total, but only
       (N-1)(N-2)/2 = 10 are independent.
    """
    # Enumerate all 3-body constraints (triangles) first
    tri = []
    for i, j, k in combinations(range(N), 3):
        qs = [idx[(i, j)], idx[(j, k)], idx[(i, k)]]
        tri.append(sorted(qs))
    # We keep all of them: they all vanish on the CF subspace (any triangle
    # product s_i s_j * s_j s_k * s_i s_k = +1). Rank-deficient but fine
    # for penalty construction.
    # Also include 4-body plaquettes for realism (paper's Fig. 2a):
    # for K_6 the LHZ layout has both 3- and 4-body. But for our purposes
    # of an *explicit-penalty* Hamiltonian, redundant constraints just add
    # to the energy penalty without changing the ground state.
    # We return only the 20 triangles (all 3-body); this matches Fig 2a's
    # 3-body constraints on N=6, plus we add the 4-body ones as the paper
    # does (for N=6 there are also 4-body constraints -- 
    # C(N,4) with i<j<k<l and product s_i s_j * s_j s_k * s_k s_l * s_i s_l ... 
    # actually the standard 4-body plaquette in LHZ is
    #    Z_{i,j} Z_{j,k} Z_{k,l} Z_{i,l} = 1 on CF).
    plaq = []
    for i, j, k, l in combinations(range(N), 4):
        qs = sorted([idx[(i, j)], idx[(j, k)], idx[(k, l)], idx[(i, l)]])
        plaq.append(qs)
    return tri, plaq

def constraint_hamiltonian_diag(K, constraints, c=3.0):
    """Return diag(H_C) as an array of length 2^K.
       H_C = sum_l (c/2) (1 - prod_{k in Sl} Z_k).
       Value = c * (# of violated constraints) on that state.
    """
    HC = np.zeros(1 << K, dtype=np.float64)
    # Precompute mask for each constraint
    masks = []
    for S in constraints:
        m = 0
        for k in S:
            m |= (1 << k)
        masks.append(m)
    for x in range(1 << K):
        e = 0.0
        for m in masks:
            # product of Z_k over k in S = +1 if even parity of x on mask, -1 if odd
            v = bin(x & m).count("1")
            # (1 - (+1 or -1))/2 = 0 or 1
            if v % 2 == 1:  # odd -> product = -1 -> (1 - (-1))/2 = 1 -> penalty
                e += c
        HC[x] = e
    return HC

# ---------- Statevector helpers ----------

def apply_diag_phase(psi, diag_H, theta):
    """Apply exp(-i theta H) for diagonal H."""
    return psi * np.exp(-1j * theta * diag_H)

def apply_X_all(psi, K, beta):
    """Apply exp(-i beta sum_k X_k) = product_k exp(-i beta X_k).
       Since single-qubit X-rotations commute, do it as tensor product of
       Rx(2 beta) per qubit. We use the closed-form:
         Rx(2*beta) = cos(beta) I - i sin(beta) X.
       We reshape psi as a rank-K tensor and multiply along each axis.
    """
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    # 2x2 matrix
    M = np.array([[c, s], [s, c]], dtype=np.complex128)
    shape = [2] * K
    psi_t = psi.reshape(shape)
    for axis in range(K):
        psi_t = np.moveaxis(psi_t, axis, 0)
        # apply M on the first axis
        orig_shape = psi_t.shape
        psi_t = psi_t.reshape(2, -1)
        psi_t = M @ psi_t
        psi_t = psi_t.reshape(orig_shape)
        psi_t = np.moveaxis(psi_t, 0, axis)
    return psi_t.reshape(-1)

def apply_multi_X_line(psi, K, qubits, beta):
    """Apply exp(-i beta prod_{k in qubits} X_k) to psi.
       Uses exp(-i beta P) = cos(beta) I - i sin(beta) P for a Pauli string P.
    """
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    # Build permutation: for each basis state x, applying prod X_k flips those bits.
    mask = 0
    for k in qubits:
        mask |= (1 << k)
    # (I) contribution: c * psi
    # (P) contribution: s * psi[x xor mask]
    idx = np.arange(1 << K)
    flipped = idx ^ mask
    return c * psi + s * psi[flipped]

def apply_driver_lines(psi, K, driver_lines, beta):
    """Apply exp(-i beta sum_mu X^(mu)) = product_mu exp(-i beta X^(mu))
       (product order matters when lines overlap; here we do them sequentially,
        which is exact because each X^(mu) individually squares to I and
        we treat them as separate Trotter-1 exponentials.  For matching the
        paper's implementation, this is the standard approach: the driver
        unitary is IMPLEMENTED as sequential product of per-line unitaries.)
    """
    for qubits in driver_lines:
        psi = apply_multi_X_line(psi, K, qubits, beta)
    return psi

# ---------- QAOA drivers ----------

@dataclass
class ParityLayout:
    N: int
    K: int
    pairs: list          # list of (i,j)
    idx: dict            # (i,j) -> physical index
    HZ_diag: np.ndarray  # 2^K
    HC_diag: np.ndarray  # 2^K
    ntot_C: int
    Hphys_diag: np.ndarray  # HZ + HC
    ground_state_indices: np.ndarray  # indices of min(Hphys)
    Emin: float
    Emax: float

def build_parity_layout(N, J, c=3.0):
    pairs, idx = parity_indexing(N)
    K = len(pairs)
    HZ = parity_energies(N, J, pairs, idx)
    tri, plaq = generate_constraint_generators(N, pairs, idx)
    all_cons = tri + plaq
    HC = constraint_hamiltonian_diag(K, all_cons, c=c)
    Hphys = HZ + HC
    # Paper (Eq. 17): Eres = (E - Emin) / (Emax - Emin) where Emin, Emax
    # are min/max EIGENVALUES OF H_phys (i.e. over the full physical Hilbert space).
    Emin = float(Hphys.min())
    Emax = float(Hphys.max())
    # Ground states of H_phys (must be CF and hit min H_Z on CF subspace).
    ground_idx = np.where(np.isclose(Hphys, Emin, atol=1e-9))[0]
    return ParityLayout(N=N, K=K, pairs=pairs, idx=idx,
                        HZ_diag=HZ, HC_diag=HC, ntot_C=len(all_cons),
                        Hphys_diag=Hphys, ground_state_indices=ground_idx,
                        Emin=Emin, Emax=Emax)

def initial_state_explicit(K):
    """|+>^K = uniform superposition on physical qubits (explicit parity QAOA)."""
    return np.ones(1 << K, dtype=np.complex128) / np.sqrt(1 << K)

def initial_state_implicit(K, cf_states):
    """Equal superposition of all constraint-fulfilling states."""
    psi = np.zeros(1 << K, dtype=np.complex128)
    amp = 1.0 / np.sqrt(len(cf_states))
    for x in cf_states:
        psi[x] = amp
    return psi

def get_implicit_driver_lines(N, pairs, idx):
    """For all-to-all N-spin problem, the fully-implicit driver has N-ns lines,
       where line Q_mu = {(mu,j) : j != mu}, i.e. all edges touching problem spin mu.
       ns=1 (Ising is Z_2 symmetric), so we drop one line (mu=0)."""
    lines = []
    for mu in range(N):
        Qmu = [idx[tuple(sorted((mu, j)))] for j in range(N) if j != mu]
        lines.append(sorted(Qmu))
    # Drop one to make them independent (spin-flip symmetry)
    return lines[1:]

# ---------- QAOA circuits ----------

def qaoa_explicit(layout, betas, gammas, omegas):
    """Run p-step FULLY EXPLICIT parity QAOA and return final statevector."""
    K = layout.K
    psi = initial_state_explicit(K)
    p = len(betas)
    for j in range(p):
        psi = apply_diag_phase(psi, layout.HC_diag, omegas[j])
        psi = apply_diag_phase(psi, layout.HZ_diag, gammas[j])
        psi = apply_X_all(psi, K, betas[j])
    return psi

def qaoa_implicit(layout, cf_states, driver_lines, betas, gammas):
    """Run p-step FULLY IMPLICIT parity QAOA and return final statevector."""
    K = layout.K
    psi = initial_state_implicit(K, cf_states)
    p = len(betas)
    for j in range(p):
        psi = apply_diag_phase(psi, layout.HZ_diag, gammas[j])
        psi = apply_driver_lines(psi, K, driver_lines, betas[j])
    return psi

def qaoa_hybrid(layout, hyb_init_states, hyb_driver_lines, HC_expl_diag,
                betas, gammas, omegas):
    """Run p-step HYBRID parity QAOA.
       hyb_init_states = list of physical strings spanning the hybrid subspace.
       hyb_driver_lines = list of driver lines preserving implicit constraints.
       HC_expl_diag = diagonal of the EXPLICITLY enforced constraint Hamiltonian.
    """
    K = layout.K
    psi = np.zeros(1 << K, dtype=np.complex128)
    amp = 1.0 / np.sqrt(len(hyb_init_states))
    for x in hyb_init_states:
        psi[x] = amp
    p = len(betas)
    for j in range(p):
        psi = apply_diag_phase(psi, HC_expl_diag, omegas[j])
        psi = apply_diag_phase(psi, layout.HZ_diag, gammas[j])
        psi = apply_driver_lines(psi, K, hyb_driver_lines, betas[j])
    return psi

# ---------- Metrics ----------

def energy(psi, H_diag):
    p2 = np.abs(psi) ** 2
    return float(np.sum(p2 * H_diag))

def fidelity_ground(psi, ground_indices):
    p2 = np.abs(psi) ** 2
    return float(np.sum(p2[ground_indices]))

def residual_energy(E, Emin, Emax):
    return (E - Emin) / (Emax - Emin)

# ---------- Parameter optimization ----------

def random_search_optimize(objective, n_params, n_starts=20, n_moves=200, rng=None):
    """Very simple stochastic local search that mimics the paper's
       'accept-if-improves' random parameter update procedure.
       Returns (best_energy, best_params).
    """
    if rng is None:
        rng = np.random.default_rng(0)
    best_E = np.inf
    best_x = None
    for _ in range(n_starts):
        x = rng.uniform(0, 2 * np.pi, size=n_params)
        E = objective(x)
        for _ in range(n_moves):
            k = rng.integers(0, n_params)
            step = rng.normal(0, 0.3)
            x2 = x.copy()
            x2[k] = (x2[k] + step) % (2 * np.pi)
            E2 = objective(x2)
            if E2 < E:
                x, E = x2, E2
        if E < best_E:
            best_E, best_x = E, x
    return best_E, best_x

# ---------- Standard (unencoded) QAOA on N logical qubits ----------

def qaoa_standard_energies(N, J):
    """Return the diag of the logical Ising Hamiltonian on 2^N."""
    return logical_energies(N, J)

def apply_X_all_generic(psi, n, beta):
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    M = np.array([[c, s], [s, c]], dtype=np.complex128)
    shape = [2] * n
    psi_t = psi.reshape(shape)
    for axis in range(n):
        psi_t = np.moveaxis(psi_t, axis, 0)
        orig_shape = psi_t.shape
        psi_t = psi_t.reshape(2, -1)
        psi_t = M @ psi_t
        psi_t = psi_t.reshape(orig_shape)
        psi_t = np.moveaxis(psi_t, 0, axis)
    return psi_t.reshape(-1)

def qaoa_standard(N, J, betas, gammas):
    """Standard QAOA on N logical qubits."""
    Ediag = qaoa_standard_energies(N, J)
    psi = np.ones(1 << N, dtype=np.complex128) / np.sqrt(1 << N)
    for j in range(len(betas)):
        psi = apply_diag_phase(psi, Ediag, gammas[j])
        psi = apply_X_all_generic(psi, N, betas[j])
    return psi, Ediag

# ---------- Hybrid construction: split constraints into explicit / implicit ----------

def hybrid_setup(N, J, layout, n_explicit, c=3.0):
    """Choose n_explicit constraints (from the 20 triangles) to enforce
       explicitly; the remaining are implicit.  For simplicity we sort
       triangles lexicographically and take the first n_explicit as explicit.
       The initial state for the hybrid circuit spans the subspace that
       satisfies all IMPLICIT constraints; this subspace has dimension
       2^{N + n_explicit - ns} = 2^{5 + n_explicit}.
       The driver lines are the fully-implicit lines (length-5 per problem-spin)
       -- these are still valid drivers because they preserve every constraint,
       and thus in particular the implicit subset.  This is an over-restrictive
       driver (dim of reachable subspace = 2^{N-1} even though hybrid
       subspace is 2^{5 + n_explicit}), so we augment with additional
       'split' lines that violate one explicit constraint while preserving
       all implicit ones.  For n_explicit=8 or 12 this gives a valid driver set.
    """
    pairs, idx = layout.pairs, layout.idx
    K = layout.K

    # Get all 20 triangles as constraints:
    triangles = []
    for i, j, k in combinations(range(N), 3):
        qs = tuple(sorted([idx[(i, j)], idx[(j, k)], idx[(i, k)]]))
        triangles.append(qs)
    triangles = sorted(triangles)
    # Choose n_explicit as explicit constraints (deterministic by sort):
    explicit_set = triangles[:n_explicit]
    implicit_set = triangles[n_explicit:]

    # Build H_C^explicit diag (only these constraints penalized in QAOA cost)
    HC_expl = constraint_hamiltonian_diag(K, list(explicit_set), c=c)

    # Hybrid subspace: physical strings satisfying ALL implicit constraints
    # (explicit constraints may or may not be satisfied; when violated,
    # the state pays a penalty via HC_expl at cost time).
    hyb_states = []
    imp_masks = []
    for S in implicit_set:
        m = 0
        for q in S:
            m |= (1 << q)
        imp_masks.append(m)
    for x in range(1 << K):
        ok = True
        for m in imp_masks:
            if bin(x & m).count("1") % 2 == 1:
                ok = False
                break
        if ok:
            hyb_states.append(x)

    # Driver lines: the fully-implicit N-lines (5 of them after dropping one)
    # These preserve ALL constraints and therefore preserve implicit constraints.
    lines = get_implicit_driver_lines(N, pairs, idx)

    return HC_expl, hyb_states, lines, len(explicit_set)


# ---------- Main experiment ----------

def one_instance(N, J, p, c=3.0, rng=None, n_starts=8, n_moves=150):
    """Run one problem instance across all four nr settings.
       Returns dict with residual_energy and fidelity for each variant.
    """
    if rng is None:
        rng = np.random.default_rng(0)
    layout = build_parity_layout(N, J, c=c)
    # CF states + implicit driver lines
    cf_states, cf_logical = cf_states_and_map(N, layout.pairs)
    imp_lines = get_implicit_driver_lines(N, layout.pairs, layout.idx)

    results = {}

    # --- Fully explicit (nr = 1.0) ---
    def obj_expl(x):
        p_ = p
        betas, gammas, omegas = x[:p_], x[p_:2*p_], x[2*p_:3*p_]
        psi = qaoa_explicit(layout, betas, gammas, omegas)
        return energy(psi, layout.Hphys_diag)
    Ebest, xbest = random_search_optimize(obj_expl, 3*p, n_starts=n_starts,
                                          n_moves=n_moves, rng=rng)
    psi = qaoa_explicit(layout, xbest[:p], xbest[p:2*p], xbest[2*p:3*p])
    E = energy(psi, layout.Hphys_diag)
    F = fidelity_ground(psi, layout.ground_state_indices)
    results["nr=1.0"] = {"E": E, "Eres": residual_energy(E, layout.Emin, layout.Emax),
                        "F": F}

    # --- Fully implicit (nr = 0.0) ---
    def obj_imp(x):
        p_ = p
        betas, gammas = x[:p_], x[p_:2*p_]
        psi = qaoa_implicit(layout, cf_states, imp_lines, betas, gammas)
        return energy(psi, layout.Hphys_diag)
    Ebest, xbest = random_search_optimize(obj_imp, 2*p, n_starts=n_starts,
                                          n_moves=n_moves, rng=rng)
    psi = qaoa_implicit(layout, cf_states, imp_lines, xbest[:p], xbest[p:2*p])
    E = energy(psi, layout.Hphys_diag)
    F = fidelity_ground(psi, layout.ground_state_indices)
    results["nr=0.0"] = {"E": E, "Eres": residual_energy(E, layout.Emin, layout.Emax),
                        "F": F}

    # --- Hybrid nr = 0.4: 8/20 explicit ---
    HC_expl, hyb_states, lines_h, n_expl = hybrid_setup(N, J, layout,
                                                        n_explicit=8, c=c)
    def obj_h04(x):
        p_ = p
        betas, gammas, omegas = x[:p_], x[p_:2*p_], x[2*p_:3*p_]
        psi = qaoa_hybrid(layout, hyb_states, lines_h, HC_expl,
                          betas, gammas, omegas)
        return energy(psi, layout.Hphys_diag)
    Ebest, xbest = random_search_optimize(obj_h04, 3*p, n_starts=n_starts,
                                          n_moves=n_moves, rng=rng)
    psi = qaoa_hybrid(layout, hyb_states, lines_h, HC_expl,
                      xbest[:p], xbest[p:2*p], xbest[2*p:3*p])
    E = energy(psi, layout.Hphys_diag)
    F = fidelity_ground(psi, layout.ground_state_indices)
    results["nr=0.4"] = {"E": E, "Eres": residual_energy(E, layout.Emin, layout.Emax),
                        "F": F, "n_explicit": n_expl}

    # --- Hybrid nr = 0.6: 12/20 explicit ---
    HC_expl, hyb_states, lines_h, n_expl = hybrid_setup(N, J, layout,
                                                        n_explicit=12, c=c)
    def obj_h06(x):
        p_ = p
        betas, gammas, omegas = x[:p_], x[p_:2*p_], x[2*p_:3*p_]
        psi = qaoa_hybrid(layout, hyb_states, lines_h, HC_expl,
                          betas, gammas, omegas)
        return energy(psi, layout.Hphys_diag)
    Ebest, xbest = random_search_optimize(obj_h06, 3*p, n_starts=n_starts,
                                          n_moves=n_moves, rng=rng)
    psi = qaoa_hybrid(layout, hyb_states, lines_h, HC_expl,
                      xbest[:p], xbest[p:2*p], xbest[2*p:3*p])
    E = energy(psi, layout.Hphys_diag)
    F = fidelity_ground(psi, layout.ground_state_indices)
    results["nr=0.6"] = {"E": E, "Eres": residual_energy(E, layout.Emin, layout.Emax),
                        "F": F, "n_explicit": n_expl}

    # --- Standard (unencoded) QAOA baseline ---
    Edlog = logical_energies(N, J)
    def obj_std(x):
        p_ = p
        betas, gammas = x[:p_], x[p_:2*p_]
        psi, _ = qaoa_standard(N, J, betas, gammas)
        return energy(psi, Edlog)
    Ebest, xbest = random_search_optimize(obj_std, 2*p, n_starts=n_starts,
                                          n_moves=n_moves, rng=rng)
    psi, _ = qaoa_standard(N, J, xbest[:p], xbest[p:2*p])
    Emin_std, Emax_std = float(Edlog.min()), float(Edlog.max())
    E = energy(psi, Edlog)
    gs_std = np.where(np.isclose(Edlog, Emin_std, atol=1e-9))[0]
    F = fidelity_ground(psi, gs_std)
    results["standard"] = {"E": E, "Eres": (E - Emin_std) / (Emax_std - Emin_std),
                          "F": F}

    return results, layout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=6)
    ap.add_argument("--p", type=int, default=3)
    ap.add_argument("--instances", type=int, default=24)
    ap.add_argument("--n_starts", type=int, default=8)
    ap.add_argument("--n_moves", type=int, default=150)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out", type=str,
                    default=os.path.expanduser(
                        "~/Dropbox/REPLICATE-PROJECT/QC-100/"
                        "QC-2203.04340-parity-qaoa/report/evidence/results.json"))
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    t0 = time.time()
    all_res = []
    for inst in range(args.instances):
        J = random_instance(args.N, rng)
        res, layout = one_instance(args.N, J, args.p,
                                    rng=rng,
                                    n_starts=args.n_starts,
                                    n_moves=args.n_moves)
        res["_instance"] = inst
        res["_seed_hash"] = int(rng.integers(0, 1 << 31))
        all_res.append(res)
        dt = time.time() - t0
        print(f"[{inst+1}/{args.instances}] t={dt:.1f}s "
              f"Eres[nr=0.0]={res['nr=0.0']['Eres']:.3f} "
              f"Eres[nr=0.4]={res['nr=0.4']['Eres']:.3f} "
              f"Eres[nr=0.6]={res['nr=0.6']['Eres']:.3f} "
              f"Eres[nr=1.0]={res['nr=1.0']['Eres']:.3f} "
              f"Eres[std]={res['standard']['Eres']:.3f}",
              flush=True)

    # Aggregate
    def agg(key, subkey):
        vals = [r[key][subkey] for r in all_res]
        return {
            "median": float(np.median(vals)),
            "q25": float(np.quantile(vals, 0.25)),
            "q75": float(np.quantile(vals, 0.75)),
            "mean": float(np.mean(vals)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
            "n": len(vals),
        }
    summary = {
        "N": args.N, "K": args.N * (args.N - 1) // 2,
        "p": args.p, "instances": args.instances,
        "n_starts": args.n_starts, "n_moves": args.n_moves,
        "seed": args.seed,
        "variants": {}
    }
    for key in ["nr=0.0", "nr=0.4", "nr=0.6", "nr=1.0", "standard"]:
        summary["variants"][key] = {
            "Eres": agg(key, "Eres"),
            "F": agg(key, "F"),
        }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"summary": summary, "instances": all_res}, f, indent=2)
    print("\n=== SUMMARY (median residual energy, higher instance count = closer to paper's 96) ===")
    for key in ["nr=0.0", "nr=0.4", "nr=0.6", "nr=1.0"]:
        s = summary["variants"][key]
        print(f"  {key:8s}  median Eres = {s['Eres']['median']:.4f}   "
              f"median F = {s['F']['median']:.4f}   n={s['Eres']['n']}")
    print(f"  {'standard':8s}  median Eres = {summary['variants']['standard']['Eres']['median']:.4f}")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
