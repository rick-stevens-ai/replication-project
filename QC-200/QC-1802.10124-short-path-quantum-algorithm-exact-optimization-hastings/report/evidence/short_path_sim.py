#!/usr/bin/env python3
"""
Independent replication of Hastings 2018 "A Short Path Quantum Algorithm for Exact Optimization"
arXiv:1802.10124.

Core object: family of Hamiltonians H_s = H_Z - s * B * (X/N)^K with X = sum_i X_i.
Ground state at s=1 is target; ground state at s=0 (H_s = H_Z - B * (X/N)^K when s=1 in
their convention; note paper evolves s from 1 to 0) is the driver-dominated state.

Actually re-reading paper Algorithm 1:
  - Prepare |+>^N (which is the ground state of -B*(X/N)^K, i.e. s -> infinity limit
    or the pure driver ground state ~ H_{s=infty}).
  - Evolve from s=1 to s=0 (paper's convention).
  - At s=0: H_0 = H_Z (pure objective).
  - Success = measure and get true ground state of H_Z.
  - Overlap P_ov = |<+^N | psi_{0, s=1}>|^2 where psi_{0,s} is ground state of H_s.

Wait - re-read: H_s = H_Z - s B (X/N)^K.
  At s=0: H_s = H_Z, ground state is target computational basis state (up to degeneracy).
  At s=1: H_s = H_Z - B (X/N)^K, mixes objective with driver.
  |+>^N is ground state of -(X/N)^K only when the H_Z term is negligible relative to B.

So the "short path" is s: 1 -> 0. At s=1 the ground state has strong overlap with |+>^N
(if B is large enough). Then the algorithm uses the measurement algorithm to project
along the interpolation to the s=0 ground state.

Key predictions we can test at small N:
  1. P_ov = |<+^N | psi_{0,s=1}>|^2 as a function of B (should be Omega(1) for B in right range).
  2. Spectral gap of H_s along s in [0,1] stays open (not superpoly small).
  3. Total expected queries (algorithm success probability = P_ov * P_succ; amplitude
     amplification gives runtime ~ 1/sqrt(P_ov)); compared to Grover which is 2^{N/2}.
  4. Empirical constant improvement over Grover: measure T_short-path / T_Grover
     both scaled by 2^{-N/2}.

This is a *simulation* (build full 2^N Hamiltonian, diagonalize, compute overlaps).
No hardware. N up to 12 => matrices 4096x4096, fine.
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.linalg as sla
import json
import time
import os
import sys
from itertools import product

# Pauli matrices
I2 = sp.eye(2, format='csr')
X2 = sp.csr_matrix([[0.0, 1.0], [1.0, 0.0]])
Z2 = sp.csr_matrix([[1.0, 0.0], [0.0, -1.0]])

def kron_list(ops):
    """Kronecker product of a list of 2x2 sparse ops."""
    out = ops[0]
    for op in ops[1:]:
        out = sp.kron(out, op, format='csr')
    return out

def single_pauli(N, i, P):
    """Pauli P on qubit i (0-indexed), identity elsewhere. Uses convention qubit 0 = leftmost."""
    ops = [I2] * N
    ops[i] = P
    return kron_list(ops)

def build_HX(N):
    """H_X = sum_i X_i (paper's X, not driver H_x with negative sign)."""
    H = sp.csr_matrix((2**N, 2**N))
    for i in range(N):
        H = H + single_pauli(N, i, X2)
    return H

def build_HZ_ising(N, J, h):
    """H_Z = sum_{i<j} J[i,j] Z_i Z_j + sum_i h[i] Z_i (D=2 case, MAX-2-LIN2).
    Vectorized over 2^N basis states."""
    dim = 2**N
    # Compute spin arrays for all basis states at once
    # Bit i of basis index b (with i=0 leftmost) => spin = 1 - 2*bit
    idxs = np.arange(dim, dtype=np.int64)
    # Extract bits: shape (dim, N)
    bits = ((idxs[:, None] >> (N - 1 - np.arange(N))) & 1).astype(np.int8)
    spins = (1 - 2 * bits).astype(np.float64)  # (dim, N)
    # h contribution
    diag = spins @ h  # (dim,)
    # J contribution: sum_{i<j} J[i,j] * s_i * s_j
    # = 0.5 * (spins @ J @ spins.T) diagonal - 0.5 * sum J_ii s_i^2 (but J_ii=0)
    # Use symmetric J (already symmetric), compute per-state: sum_{i<j} = 0.5 * (s . J . s)
    # Since J is symmetric with zero diag: s.J.s = 2 * sum_{i<j} J_ij s_i s_j
    Js = spins @ J  # (dim, N)
    quad = np.einsum('ij,ij->i', Js, spins) * 0.5
    diag = diag + quad
    return sp.diags(diag, format='csr'), diag

def random_maxk2_instance(N, rng, weight_scale=1.0):
    """Generate a random MAX-2-SAT-like Ising instance: J symmetric, +-1 * uniform weight, no self."""
    J = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            J[i,j] = weight_scale * rng.choice([-1.0, 1.0])
            J[j,i] = J[i,j]
    h = weight_scale * rng.choice([-1.0, 1.0], size=N)
    return J, h

def random_sk_instance(N, rng):
    """Sherrington-Kirkpatrick spin glass: J_ij ~ N(0, 1/sqrt(N)); h_i = 0."""
    J = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            J[i,j] = rng.normal(0, 1.0/np.sqrt(N))
            J[j,i] = J[i,j]
    h = np.zeros(N)
    return J, h

def build_short_path_H(HZ_diag, XN_K, N, s, B):
    """H_s = H_Z - s * B * (X/N)^K where XN_K is precomputed (X/N)^K.
    HZ_diag is 1-D diagonal of H_Z. Returns dense.
    """
    H = -s * B * XN_K.copy()
    # add H_Z on diagonal
    dim = H.shape[0]
    H[np.arange(dim), np.arange(dim)] += HZ_diag
    return H

def ground_state(H, k_low=2):
    """Return (E0, psi0, [E0, E1, ...k_low]) for smallest algebraic eigenvalues.
    Uses subset_by_index for speed."""
    dim = H.shape[0]
    if dim <= 64:
        w, v = np.linalg.eigh(H)
        return float(w[0]), v[:, 0], w[:k_low]
    # scipy.linalg.eigh with subset
    w, v = sla.eigh(H, subset_by_index=[0, k_low - 1])
    return float(w[0]), v[:, 0], w

def uniform_plus_state(N):
    """|+>^N as vector."""
    dim = 2**N
    return np.ones(dim) / np.sqrt(dim)

def classical_ground_state(diag):
    """True ground state of H_Z = sum_i diag[i] |i><i|. Returns E0 and list of ground indices."""
    E0 = float(diag.min())
    idxs = np.flatnonzero(np.isclose(diag, E0))
    return E0, list(idxs)


def analyze_instance(N, J, h, K_values, b_values, instance_label=""):
    """For a given instance and grid of (K, b), compute:
       - P_ov = |<+^N | psi_{0,s=1}>|^2
       - Spectral gap min along path s in [0,1]
       - Overlap with true classical ground state
    """
    HZ_sp, HZ_diag = build_HZ_ising(N, J, h)
    HX_sp = build_HX(N)
    HX = HX_sp.toarray()
    dim = 2**N
    E0_z, gs_idxs = classical_ground_state(HZ_diag)
    plus = uniform_plus_state(N)

    # Precompute (X/N)^K for each K (dense matrix power)
    XN = HX / N
    XN_K_cache = {}
    for K in K_values:
        XN_K_cache[K] = np.linalg.matrix_power(XN, K)

    results = []
    # s-grid: 6 points is enough to see min gap (finer grid didn't change qualitative picture in tests)
    s_grid = np.linspace(0.0, 1.0, 6)  # 0, 0.2, 0.4, 0.6, 0.8, 1.0
    for K in K_values:
        XN_K = XN_K_cache[K]
        for b in b_values:
            B = b * abs(E0_z)  # B > 0 per paper's normalization
            # Gap along path
            gaps = []
            H_s_ground_energies = []
            for s in s_grid:
                Hs = build_short_path_H(HZ_diag, XN_K, N, s, B)
                E0s, v0s, ws = ground_state(Hs)
                gap = float(ws[1] - ws[0])
                gaps.append(gap)
                H_s_ground_energies.append(E0s)
            # Ground state at s=1
            H1 = build_short_path_H(HZ_diag, XN_K, N, 1.0, B)
            E0_1, psi0_1, _ = ground_state(H1)
            # Ground state at s=0
            H0 = build_short_path_H(HZ_diag, XN_K, N, 0.0, B)
            E0_0, psi0_0, _ = ground_state(H0)
            # Overlaps
            P_ov_plus = float(abs(np.vdot(plus, psi0_1))**2)
            P_overlap_0_1 = float(abs(np.vdot(psi0_0, psi0_1))**2)  # |<psi_00|psi_01>|^2
            # Overlap of psi0_1 with true classical ground states
            P_success_direct = float(sum(abs(psi0_0[i])**2 for i in gs_idxs))
            # (Should be ~1 at s=0 up to degeneracy.)
            # Amplitude amplification requires ~1/sqrt(P_ov_plus * P_success_direct) rounds
            # Each round = O(polyN) queries; but for the O*(2^{N/2}) scaling, effective queries scale like
            # sqrt(1/P_ov). Grover baseline scales like sqrt(2^N).
            # We compare: T_short_path ~ 1/sqrt(P_ov_plus * P_success_direct)
            # T_Grover ~ sqrt(2^N / (# ground states))
            eff_queries_short = 1.0 / np.sqrt(max(P_ov_plus * P_success_direct, 1e-300))
            eff_queries_grover = np.sqrt(2**N / len(gs_idxs))
            ratio = eff_queries_short / eff_queries_grover
            row = dict(
                instance=instance_label,
                N=N, K=int(K), b=float(b), B=float(B),
                E0_z=float(E0_z), num_ground_states=len(gs_idxs),
                gaps=[float(g) for g in gaps],
                min_gap=float(min(gaps)),
                P_ov_plus_psi01=P_ov_plus,
                P_ov_psi00_psi01=P_overlap_0_1,
                P_success_direct=float(P_success_direct),
                eff_queries_short=float(eff_queries_short),
                eff_queries_grover=float(eff_queries_grover),
                ratio_short_over_grover=float(ratio),
            )
            results.append(row)
    return results


def main():
    outdir = os.path.dirname(os.path.abspath(__file__))
    seed = 20260705
    rng = np.random.default_rng(seed)

    # Per-N configuration; N=12 is slow (dense eigh on 4096x4096) so we shrink K/b/inst.
    Ns = [6, 8, 10, 12]
    n_instances_per_N = {6: 20, 8: 20, 10: 20, 12: 4}
    K_per_N = {6: [3, 5], 8: [3, 5], 10: [3, 5], 12: [3]}
    b_per_N = {6: [0.3, 0.6, 0.9], 8: [0.3, 0.6, 0.9], 10: [0.3, 0.6, 0.9], 12: [0.3, 0.9]}
    ensembles = ['maxk2', 'sk']

    all_results = []
    t0 = time.time()

    for ensemble in ensembles:
        for N in Ns:
            n_inst = n_instances_per_N[N]
            K_values = K_per_N[N]
            b_values = b_per_N[N]
            print(f"\n=== ensemble={ensemble} N={N} (n_inst={n_inst}, K={K_values}, b={b_values}) ===", flush=True)
            for inst_id in range(n_inst):
                if ensemble == 'maxk2':
                    J, h = random_maxk2_instance(N, rng)
                else:
                    J, h = random_sk_instance(N, rng)
                label = f"{ensemble}_N{N}_inst{inst_id}"
                t_i = time.time()
                res = analyze_instance(N, J, h, K_values, b_values, instance_label=label)
                all_results.extend(res)
                print(f"  inst {inst_id}: {time.time()-t_i:.2f}s cumulative {time.time()-t0:.1f}s", flush=True)

    # Save
    out_path = os.path.join(outdir, "results.json")
    with open(out_path, 'w') as f:
        json.dump({
            'seed': seed,
            'Ns': Ns,
            'n_instances_per_N': n_instances_per_N,
            'K_per_N': {str(k): v for k, v in K_per_N.items()},
            'b_per_N': {str(k): v for k, v in b_per_N.items()},
            'ensembles': ensembles,
            'wall_time_s': time.time() - t0,
            'results': all_results,
        }, f, indent=2)
    print(f"\nDone. Wrote {out_path}, {len(all_results)} rows, wall {time.time()-t0:.1f}s")

    # Summary
    try:
        import statistics
        print("\n=== SUMMARY (median values per (ensemble,N,K,b)) ===")
        from collections import defaultdict
        groups = defaultdict(list)
        for r in all_results:
            key = (r['instance'].split('_')[0], r['N'], r['K'], r['b'])
            groups[key].append(r)
        for key in sorted(groups.keys()):
            rs = groups[key]
            med_pov = statistics.median([r['P_ov_plus_psi01'] for r in rs])
            med_gap = statistics.median([r['min_gap'] for r in rs])
            med_ratio = statistics.median([r['ratio_short_over_grover'] for r in rs])
            print(f"  ens={key[0]} N={key[1]} K={key[2]} b={key[3]:.2f} "
                  f"median P_ov={med_pov:.4f} min_gap={med_gap:.4f} T_sp/T_G={med_ratio:.4f}")
    except Exception as e:
        print(f"summary generation failed (results still saved): {e}")

if __name__ == '__main__':
    main()
