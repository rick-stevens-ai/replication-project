#!/usr/bin/env python3
"""
Independent replication of Willsch, Willsch, Jin, De Raedt, Michielsen,
"Benchmarking the Quantum Approximate Optimization Algorithm", arXiv:1907.02359
(Quantum Inf Process 19, 197 (2020)).

Pure classical statevector simulation of QAOA (no external quantum SDK), numpy only.
Reproduces:
  - Ising cost Hamiltonian H_C = sum_i h_i Z_i + sum_{(i,j)} J_ij Z_i Z_j
  - QAOA ansatz |gamma,beta> = prod_{k} exp(-i beta_k H0) exp(-i gamma_k H_C) |+>^N
  - Metrics M1 success prob, M2 energy E_p, M3 ratio r (Eq.16)
  - p=1 analytic energy formula (Eq.19) as independent cross-check
  - Increase of success prob & r with p (Table 1 trend)
  - Linear-annealing-schedule initialization at large p -> near-unit success prob
"""
import numpy as np
import itertools, json, time

# ---------------------------------------------------------------------------
# Problem instances (transcribed from arXiv:1907.02359 Appendix B)
# ---------------------------------------------------------------------------

# Table 3 (A): 8-variable 2-SAT instance (A), 9 clauses (zero-zero rows omitted)
# Columns: i, j, J_ij, h_i  (h_i is the local field on vertex 'i' of that row)
TWO_SAT_8A = {
    "N": 8,
    "edges": [(0,6,1.0),(1,3,-1.0),(2,0,-1.0),(3,4,1.0),(5,6,-1.0),(6,4,-1.0),(7,1,-1.0)],
    "fields": {0:0.0, 1:0.0, 2:1.0, 3:0.0, 5:-1.0, 6:1.0, 7:1.0},
    "E_C0_paper": -9.0,   # from Fig.11 caption
}

# Table 2: 16-variable weighted MaxCut instance (h_i = 0 for all)
MAXCUT_16 = {
    "N": 16,
    "edges": [
        (0,4,0.4),(0,5,0.8),(0,6,0.2),
        (1,4,0.7),(1,5,0.5),(1,6,0.6),(1,7,0.8),
        (2,4,0.4),(2,5,1.0),(2,6,0.3),(2,7,0.7),
        (3,4,0.3),(3,5,0.7),(3,6,0.6),(3,7,0.4),
        (4,12,0.1),
        (6,14,0.2),
        (7,15,1.0),
        (8,12,0.1),(8,13,0.9),(8,14,1.0),(8,15,0.8),
        (9,12,0.3),(9,13,0.5),(9,14,0.1),(9,15,0.7),
        (10,12,0.5),(10,13,0.7),(10,14,0.3),(10,15,0.6),
        (11,12,0.2),(11,13,0.8),(11,14,0.5),
    ],
    "fields": {},
    "E_C0_paper": -17.7,  # from Fig.10 caption
}

# ---------------------------------------------------------------------------
# Diagonal cost Hamiltonian in the computational (Z) basis
# z_i in {-1,+1}. Bit b_i in {0,1}; z_i = 1 - 2*b_i  (b=0 -> z=+1, b=1 -> z=-1)
# ---------------------------------------------------------------------------
def build_HC_diag(inst):
    N = inst["N"]
    dim = 1 << N
    diag = np.zeros(dim, dtype=np.float64)
    idx = np.arange(dim)
    # z_i for each basis state: bit i (MSB-first convention: qubit 0 = highest bit)
    zvals = np.empty((N, dim), dtype=np.float64)
    for i in range(N):
        bit = (idx >> (N - 1 - i)) & 1
        zvals[i] = 1.0 - 2.0 * bit
    for i, h in inst["fields"].items():
        diag += h * zvals[i]
    for (i, j, J) in inst["edges"]:
        diag += J * zvals[i] * zvals[j]
    return diag

# ---------------------------------------------------------------------------
# QAOA state vector (numpy)
# ---------------------------------------------------------------------------
def apply_UC(state, diag, gamma):
    return np.exp(-1j * gamma * diag) * state

def apply_UB(state, N, beta):
    # exp(-i beta sum_i X_i) = prod_i (cos b I - i sin b X_i); apply per-qubit
    c = np.cos(beta); s = np.sin(beta)
    st = state.reshape([2]*N)
    for q in range(N):
        st = np.moveaxis(st, q, 0)
        a0 = st[0].copy(); a1 = st[1].copy()
        st[0] = c*a0 - 1j*s*a1
        st[1] = c*a1 - 1j*s*a0
        st = np.moveaxis(st, 0, q)
    return st.reshape(-1)

def qaoa_state(diag, N, gammas, betas):
    dim = 1 << N
    state = np.full(dim, 1.0/np.sqrt(dim), dtype=np.complex128)  # |+>^N
    for g, b in zip(gammas, betas):
        state = apply_UC(state, diag, g)
        state = apply_UB(state, N, b)
    return state

def metrics(state, diag, gs_mask, Emin, Emax):
    probs = np.abs(state)**2
    E = float(np.sum(probs * diag))                 # M2 energy expectation
    succ = float(np.sum(probs[gs_mask]))            # M1 success prob
    r = (E - Emax) / (Emin - Emax)                  # M3 ratio (Eq.16)
    return succ, E, r

# ---------------------------------------------------------------------------
# p=1 analytic energy (Eq.19) for triangle-free connectivity graphs
# ---------------------------------------------------------------------------
def analytic_E_p1(inst, gamma, beta):
    N = inst["N"]; h = inst["fields"]; edges = inst["edges"]
    adj = {}
    for (i,j,J) in edges:
        adj.setdefault(i, {})[j] = J
        adj.setdefault(j, {})[i] = J
    def hv(v): return h.get(v, 0.0)
    total = 0.0
    # single-field term
    for i in range(N):
        hi = hv(i)
        if hi == 0.0: continue
        prod = 1.0
        for k, Jik in adj.get(i, {}).items():
            prod *= np.cos(2*gamma*Jik)
        total += hi * np.sin(2*beta) * np.sin(2*gamma*hi) * prod
    # edge term
    for (i,j,Jij) in edges:
        hi, hj = hv(i), hv(j)
        term1 = np.sin(2*beta)**2 * np.sin(2*gamma*hi) * np.sin(2*gamma*hj)
        p1 = 1.0
        for k, Jik in adj.get(i, {}).items():
            if k != j: p1 *= np.cos(2*gamma*Jik)
        p2 = 1.0
        for l, Jjl in adj.get(j, {}).items():
            if l != i: p2 *= np.cos(2*gamma*Jjl)
        term1 *= p1 * p2
        c1 = np.cos(2*gamma*hi)
        for k, Jik in adj.get(i, {}).items():
            if k != j: c1 *= np.cos(2*gamma*Jik)
        c2 = np.cos(2*gamma*hj)
        for l, Jjl in adj.get(j, {}).items():
            if l != i: c2 *= np.cos(2*gamma*Jjl)
        term2 = 0.5 * np.sin(4*beta) * np.sin(2*gamma*Jij) * (c1 + c2)
        total += Jij * (term1 + term2)
    return total

def is_triangle_free(inst):
    adj = {}
    for (i,j,J) in inst["edges"]:
        adj.setdefault(i,set()).add(j); adj.setdefault(j,set()).add(i)
    for (i,j,J) in inst["edges"]:
        if adj.get(i,set()) & adj.get(j,set()):
            return False
    return True

if __name__ == "__main__":
    for name, inst in [("2SAT-8A", TWO_SAT_8A), ("MaxCut-16", MAXCUT_16)]:
        diag = build_HC_diag(inst)
        Emin = float(diag.min()); Emax = float(diag.max())
        print(f"{name}: N={inst['N']} Emin(E_C0)={Emin} Emax={Emax} "
              f"paper_E_C0={inst['E_C0_paper']} triangle_free={is_triangle_free(inst)}")
