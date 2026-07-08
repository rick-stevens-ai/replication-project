#!/usr/bin/env python3
"""
Fig 8 of arXiv:2304.07917 — 2-site 1D Hubbard model, PBC, t=-0.1, U=0.1, dtau=0.1.

Hamiltonian:
  H = t * sum_<i,j>,sigma  c_{i,sigma}^† c_{j,sigma}  +  U * sum_i n_{i,up} n_{i,down}

For 2 sites (m=2), we work in the (n_up, n_down) = (1, 1) half-filled sector
(4-dim subspace). The paper uses the initial state
  |psi_0> = 1/sqrt(2) ( |0110> - |1001> )
which is the singlet (theta=pi in Fig 6).

We build H in the full 16-dim Hilbert space via Jordan-Wigner mapping onto 4 qubits
(ordering: |n_1up n_1dn n_2up n_2dn> as MSB..LSB in the qubit register), then
apply Trotter-ITE using the paper's per-Pauli-string non-unitary gadget semantics.

The Hubbard hopping term expanded via JW gives non-trivial multi-qubit Pauli strings
(with fermionic phase); the U term gives single-site Pauli-Z terms. We assemble the
Pauli decomposition explicitly with fermionic annihilation/creation matrices, so no
external chem library is needed.
"""
from __future__ import annotations
import numpy as np, json
from numpy.linalg import eigh
from ite_tim import pauli_string, kron_all, apply_nonunitary_pauli_expm

# Fermionic operators via JW on 4 qubits (2 sites, 2 spins each)
def jw_c(n_qubits, k):
    """Annihilation operator c_k = (product of Z on qubits 0..k-1) . sigma_+_k
       Convention: c_k = (Z_0 ... Z_{k-1}) . sigma-_k with sigma- = (X+iY)/2."""
    Xp = np.array([[0,1],[0,0]], dtype=complex)  # sigma+ = X-iY-only? use lowering: |0><1|
    # In physicist convention  c^\dagger creates: c|1>=|0>, c|0>=0 -> c = |0><1|
    lower = np.array([[0,1],[0,0]], dtype=complex)
    ops = []
    Z = np.array([[1,0],[0,-1]], dtype=complex)
    I = np.eye(2, dtype=complex)
    for i in range(n_qubits):
        if i < k:
            ops.append(Z)
        elif i == k:
            ops.append(lower)
        else:
            ops.append(I)
    return kron_all(ops)

def build_hubbard_matrix(t, U, n_sites=2, pbc=True):
    """Build 4-qubit Hubbard H directly (2 sites * 2 spins = 4 qubits).
       Qubit ordering: 0->(site0,up), 1->(site0,dn), 2->(site1,up), 3->(site1,dn)."""
    n_q = 2*n_sites
    dim = 2**n_q
    H = np.zeros((dim,dim), dtype=complex)
    # helper: c[site][spin]
    def cq(site, spin):
        # spin 0=up, 1=dn
        k = 2*site + spin
        return jw_c(n_q, k)
    def cd(site, spin):
        return cq(site, spin).conj().T
    # Hopping (nearest neighbour, PBC)
    end = n_sites if pbc else n_sites-1
    for i in range(end):
        j = (i+1) % n_sites
        for spin in (0,1):
            H += t * (cd(i,spin) @ cq(j,spin) + cd(j,spin) @ cq(i,spin))
    # On-site U
    for i in range(n_sites):
        n_up = cd(i,0) @ cq(i,0)
        n_dn = cd(i,1) @ cq(i,1)
        H += U * (n_up @ n_dn)
    return H

def decompose_into_paulis(H):
    """Decompose 2^n x 2^n Hermitian matrix H into weighted Pauli strings.
       Returns list of (coeff (real), sites_ops dict). Excludes identity when 0."""
    dim = H.shape[0]
    n = int(np.log2(dim))
    labels = ['I','X','Y','Z']
    mats = {'I':np.eye(2,dtype=complex),
            'X':np.array([[0,1],[1,0]],dtype=complex),
            'Y':np.array([[0,-1j],[1j,0]],dtype=complex),
            'Z':np.array([[1,0],[0,-1]],dtype=complex)}
    from itertools import product
    terms = []
    for combo in product(labels, repeat=n):
        P = mats[combo[0]]
        for c in combo[1:]:
            P = np.kron(P, mats[c])
        coeff = np.trace(P.conj().T @ H) / dim
        c = coeff.real
        if abs(c) > 1e-10 or abs(coeff.imag) > 1e-10:
            if abs(coeff.imag) > 1e-8:
                raise RuntimeError(f"Non-real Pauli coefficient {coeff} for {combo}")
            sites_ops = {i: p for i, p in enumerate(combo) if p != 'I'}
            terms.append((c, sites_ops))
    return terms

def initial_singlet_state():
    """|psi> = 1/sqrt(2) (|0110> - |1001>) on qubit register (0,1,2,3) MSB->LSB
       matching |n1_up n1_dn n2_up n2_dn>."""
    # In big-endian: |0110> = binary 0110 = 6, |1001> = 9. Kron convention: qubit 0 is MSB in np.kron order.
    # Let's just be explicit with kron order matching pauli_string / kron_all in ite_tim.py.
    # pauli_string kron order is ops[0] kron ops[1] kron ... so qubit 0 is MSB.
    # Basis state |b0 b1 b2 b3> lives at index b0*8 + b1*4 + b2*2 + b3.
    psi = np.zeros(16, dtype=complex)
    # |0110>: b0=0,b1=1,b2=1,b3=0 -> index 0*8+1*4+1*2+0 = 6
    psi[6] = 1.0/np.sqrt(2)
    # |1001>: b0=1,b1=0,b2=0,b3=1 -> index 8+0+0+1 = 9
    psi[9] = -1.0/np.sqrt(2)
    return psi

def energy(psi, H):
    nrm = float(np.vdot(psi,psi).real)
    if nrm < 1e-300: return float('nan')
    return float((np.vdot(psi, H@psi).real)/nrm)

def trotter_step(psi, terms, n, dtau):
    p = 1.0
    for coeff, sites in terms:
        # Skip pure identity terms (constant shift): they only add a scalar to H
        if not sites:
            continue
        psi, ps = apply_nonunitary_pauli_expm(psi, coeff, sites, n, dtau)
        p *= ps
    return psi, p

def main():
    n_sites = 2
    n_q = 2*n_sites
    t = -0.1
    U = 0.1
    dtau = 0.1
    n_steps = 60

    # NB: 2-site Hubbard: paper's Fig 8 matches E0 = -0.156 (Lieb-Wu formula), which
    # corresponds to open boundary conditions (with PBC, the hopping doubles and E0
    # would be ~-0.353). Use pbc=False here.
    H = build_hubbard_matrix(t, U, n_sites=n_sites, pbc=False)
    evals, _ = eigh(H)
    E0 = float(evals[0])
    print(f"# 2-site 1D Hubbard, OBC, t={t}, U={U}, dtau={dtau}, {n_steps} steps")
    print(f"# Exact E0 = {E0:.10f}")

    terms = decompose_into_paulis(H)
    non_identity = [(c,s) for c,s in terms if s]
    identity_const = sum(c for c,s in terms if not s)  # constant shift, doesn't affect state evolution
    print(f"# Pauli decomposition: {len(non_identity)} non-identity terms (+ identity shift {identity_const})")

    psi = initial_singlet_state()
    p_cum = 1.0
    hist = []
    E = energy(psi, H)
    hist.append({'step':0,'beta':0.0,'E':E,'p_cum':p_cum,'dE':E-E0})
    for k in range(1, n_steps+1):
        psi, p_step = trotter_step(psi, terms, n_q, dtau)
        p_cum *= p_step
        E = energy(psi, H)
        hist.append({'step':k,'beta':k*dtau,'E':E,'p_cum':p_cum,'dE':E-E0})

    print(f"# {'step':>4}  {'beta':>5}  {'<E>':>14}  {'<E>-E0':>13}  {'p_cum':>12}")
    for r in hist[::5] + [hist[-1]]:
        print(f"  {r['step']:>4}  {r['beta']:5.2f}  {r['E']:+.8f}  {r['dE']:+.4e}  {r['p_cum']:.4e}")

    final = hist[-1]
    out = {
        'model':'2-site 1D Hubbard, OBC (matches paper Fig 8 E0 = -0.156 via Lieb-Wu)',
        'params':{'t':t,'U':U,'dtau':dtau,'n_steps':n_steps},
        'E0_exact':E0,
        'E_ITE_final':final['E'],
        'abs_error_final':abs(final['dE']),
        'p_cum_final':final['p_cum'],
        'n_pauli_terms_nonI':len(non_identity),
        'converged_within_1e-2':bool(abs(final['dE'])<1e-2),
        'converged_within_1e-3':bool(abs(final['dE'])<1e-3),
        'history':hist,
    }
    with open('ite_hubbard_result.json','w') as f:
        json.dump(out, f, indent=2)

    print()
    print(f"Final |<E>-E0| = {abs(final['dE']):.4e}")
    print(f"Final cumulative success prob = {final['p_cum']:.4e}")

if __name__ == '__main__':
    main()
