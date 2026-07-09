#!/usr/bin/env python3
"""
Faithful replication of the IMS (Ivanyos-Magniez-Santha, quant-ph/0102014)
Theorem 13 construction (§6): HSP for a group G with normal ELEMENTARY
ABELIAN 2-subgroup N of small index, plus G/N cyclic.

We take:
    N = (Z_2)^k    (elementary Abelian 2-group of order 2^k)
    G/N = Z_2  (cyclic of order 2)
    G = N x_semi Z_2  where the non-trivial coset element z = s acts on N
        by some fixed automorphism sigma (any invertible k x k matrix over F_2).

This class contains the wreath product Z_2^k ≀ Z_2 = (Z_2 x Z_2)^{k'} x_semi Z_2
(Rötteler-Beth 1998), which the paper explicitly generalizes.

We simulate the IMS §6 procedure end-to-end on statevectors:

1. Pick a hidden subgroup H of G.  For the demonstrator we take
       H = <(u, 1)> = {(0, 0), (u, 1)}   for some u in N
   an order-2 subgroup that is NOT contained in N (this is the interesting
   non-Abelian case; if H were in N it would trivially be an Abelian HSP).
2. Define f: G -> labels by choosing a canonical representative of each
   left coset gH.
3. Follow the IMS §6 reduction: for the single non-trivial coset rep
   z = (0, 1), build the auxiliary function on Z_2 x N:
       F(0, x) = f((x, 0))
       F(1, x) = f((x, 0) * z) = f((x, 1))
   which hides a subgroup K of Z_2 x N.
4. Reduce F's coset-state problem to Abelian HSP on Z_2 x (Z_2)^k =
   (Z_2)^{k+1}, and solve by the standard tensor-Hadamard Fourier sampling
   (each measurement gives a character of (Z_2)^{k+1} in K^perp).
5. From measurements recover generators of K, hence of H.

HEADLINE QUANTITATIVE CLAIMS the paper commits to for this class:
  * (Theorem 13 correctness) The reduction produces an Abelian HSP whose
    hidden subgroup, when recovered, yields generators for H.
  * Because (Z_2)^{k+1} is Abelian and every measurement outcome is a
    character trivial on K, the ENTIRE probability mass sits on K^perp
    (total_prob_on_perp == 1.0 within numerical precision).
  * The number of Abelian-HSP samples needed to fully generate K is
    O(log |K|) = O(k)  (standard random-Fourier-sampling bound).

We reproduce all three at k = 3, 4, 5.
"""

from __future__ import annotations
import json, math, sys, time
from dataclasses import dataclass, asdict
from itertools import product
from pathlib import Path

import numpy as np


# --- F_2^k arithmetic ----------------------------------------------------

def all_vecs(k):
    for bits in product((0, 1), repeat=k):
        yield np.array(bits, dtype=np.int8)


def vec_to_int(v):
    n = 0
    for b in v:
        n = (n << 1) | int(b)
    return n


def int_to_vec(n, k):
    return np.array([(n >> (k - 1 - i)) & 1 for i in range(k)], dtype=np.int8)


def xor(a, b):
    return np.bitwise_xor(a, b)


# --- The group G = (Z_2)^k semidirect Z_2 --------------------------------
# element = (x, b) with x in F_2^k, b in {0,1}
# sigma: an invertible k x k F_2 matrix (the outer automorphism used by z)
# multiplication: (x1, b1) * (x2, b2) = (x1 XOR sigma^{b1}(x2), b1 XOR b2)

def apply_sigma(sigma, x, times):
    y = x.copy()
    for _ in range(times):
        y = (sigma @ y) % 2
    return y


def group_mul(g, h, sigma):
    (x1, b1) = g
    (x2, b2) = h
    return (xor(x1, apply_sigma(sigma, x2, b1)), b1 ^ b2)


def group_inv(g, sigma):
    (x, b) = g
    if b == 0:
        return (x, 0)  # self-inverse in F_2^k
    # (x, 1)^{-1} = (sigma^{-1}(x), 1) since (x,1)(y,1) = (x XOR sigma(y), 0);
    # setting y = sigma^{-1}(x) gives (x XOR x, 0) = (0, 0).
    # Over F_2, sigma^{-1} = sigma^{-1 mod something}; we just precompute.
    inv = np.linalg.inv(sigma).astype(int) % 2
    return (inv @ x % 2, 1)


# --- Hidden subgroup H = {(0,0), (u, 1)} ---------------------------------
# Sanity: (u,1)(u,1) = (u XOR sigma(u), 0).  For this to equal (0,0) we need
# sigma(u) = u  (u must be a fixed point of sigma).  Otherwise H has order > 2.
# We choose sigma with at least one fixed vector u != 0 and use that u.

def choose_sigma_and_u(k, seed=42):
    rng = np.random.default_rng(seed)
    while True:
        M = rng.integers(0, 2, size=(k, k)).astype(np.int8)
        # invertible over F_2?
        if int_det_gf2(M) == 1:
            # find a nontrivial fixed vector: (M - I) v = 0 mod 2 with v != 0
            fixed = kernel_gf2((M - np.eye(k, dtype=np.int8)) % 2)
            nonzero = [v for v in fixed if np.any(v)]
            if nonzero:
                return M, nonzero[0]


def int_det_gf2(M):
    A = M.copy().astype(np.int8) % 2
    n = A.shape[0]
    det = 1
    for i in range(n):
        pivot = -1
        for r in range(i, n):
            if A[r, i] == 1:
                pivot = r
                break
        if pivot == -1:
            return 0
        if pivot != i:
            A[[i, pivot]] = A[[pivot, i]]
            det ^= 0   # sign doesn't matter in F_2
        for r in range(n):
            if r != i and A[r, i] == 1:
                A[r] = (A[r] ^ A[i])
    return det


def kernel_gf2(M):
    """Return a list of basis vectors for the nullspace of M over F_2."""
    A = M.copy().astype(np.int8) % 2
    rows, cols = A.shape
    r = 0
    pivots = []
    for c in range(cols):
        pivot = -1
        for rr in range(r, rows):
            if A[rr, c] == 1:
                pivot = rr
                break
        if pivot == -1:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        for rr in range(rows):
            if rr != r and A[rr, c] == 1:
                A[rr] = A[rr] ^ A[r]
        pivots.append(c)
        r += 1
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int8)
        v[f] = 1
        for i, pc in enumerate(pivots):
            if A[i, f] == 1:
                v[pc] = 1
        basis.append(v)
    return basis


# --- Oracle f hiding H ---------------------------------------------------

def coset_label(g, u, sigma):
    """Left cosets of H = {(0,0), (u,1)} in G. Two elements are equivalent
    iff their difference is in H. We compute a canonical label per coset."""
    (x, b) = g
    if b == 0:
        # (x, 0) H = {(x, 0), (x XOR u, 1)}
        return (tuple(x), 0)
    else:
        # (x, 1) H = {(x, 1), (x XOR sigma(u), 0)}
        # Canonical rep = the b=0 element: (x XOR sigma(u), 0)
        return (tuple(xor(x, apply_sigma(sigma, u, 1))), 0)


# --- IMS §6 reduction: auxiliary function F on Z_2 x N -------------------

def build_F_table(k, u, sigma):
    """F: Z_2 x F_2^k -> label
    F(0, x) = f(x, 0)
    F(1, x) = f((x, 0) * (0, 1)) = f((x XOR sigma(0), 1)) = f((x, 1))
    """
    z = (np.zeros(k, dtype=np.int8), 1)
    table = {}
    for b in (0, 1):
        for x in all_vecs(k):
            g = (x, 0)
            g_shift = group_mul(g, z, sigma) if b == 1 else g
            lbl = coset_label(g_shift, u, sigma)
            table[(b, tuple(x))] = lbl
    return table


def hidden_K_from_F(F, k):
    """Find the hidden subgroup K of (Z_2)^{k+1} directly from the table by
    picking (b, x) with F(b, x) == F(0, 0). K is a subgroup because F is a
    coset-labelling function on the Abelian group Z_2 x F_2^k."""
    ref = F[(0, tuple(np.zeros(k, dtype=np.int8)))]
    K = []
    for (bx, lbl) in F.items():
        if lbl == ref:
            K.append(bx)
    return K


# --- Statevector simulation of Fourier sampling on (Z_2)^{k+1} -----------

def coset_state_density(F, k):
    """rho = (1/|G|) sum_c |cK><cK| where G = Z_2 x F_2^k. Realized as
       rho = M M^dagger  where M[i, v] = 1/sqrt(|G|) if F(i)=v else 0.
    """
    dim = 2 ** (k + 1)
    values = {}
    ord_i = []
    for b in (0, 1):
        for x_int in range(2 ** k):
            x = int_to_vec(x_int, k)
            v = F[(b, tuple(x))]
            values.setdefault(v, len(values))
            ord_i.append(values[v])
    D = len(values)
    M = np.zeros((dim, D), dtype=complex)
    for i, vi in enumerate(ord_i):
        M[i, vi] = 1.0 / math.sqrt(dim)
    rho = M @ M.conj().T
    return rho


def hadamard_kplus1(kp1):
    H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
    U = H
    for _ in range(kp1 - 1):
        U = np.kron(U, H)
    return U


def measurement_distribution(rho, kp1):
    U = hadamard_kplus1(kp1)
    rho_hat = U @ rho @ U.conj().T
    p = np.real(np.diag(rho_hat))
    p = np.clip(p, 0.0, None)
    p /= p.sum()
    return p


def K_perp(K, k):
    """Return list of characters chi in (Z_2)^{k+1} trivial on K.
    A character is indexed by y in (Z_2)^{k+1}; chi_y(v) = (-1)^{y . v}.
    """
    kp1 = k + 1
    perp = []
    for y_int in range(2 ** kp1):
        y = int_to_vec(y_int, kp1)
        ok = True
        for (b, x_tup) in K:
            v = np.concatenate([[b], np.array(x_tup, dtype=np.int8)])
            if int(np.dot(y, v) % 2) != 0:
                ok = False
                break
        if ok:
            perp.append(y_int)
    return perp


def recover_K_from_samples(samples, K_size, kp1, cap=None):
    """Each sample is y in K^perp; K^perp has size 2^{kp1}/|K|.
    Standard Abelian-HSP fact: after O(log|K^perp|) random samples we
    span K^perp with high prob; then K = (K^perp)^perp.
    Returns basis of recovered K (list of int y-vectors) and number
    of samples actually consumed."""
    rank = 0
    basis = []  # rows spanning subspace of characters seen so far
    n_used = 0
    target_rank = kp1 - int(round(math.log2(K_size)))
    # target rank of K^perp = kp1 - log2(|K|)
    for y in samples:
        n_used += 1
        v = int_to_vec(y, kp1).astype(np.int8)
        # gaussian-eliminate against basis
        w = v.copy()
        for b in basis:
            if w.dot(b) % 2 == 1 and b.dot(b) % 2 == 1:  # not correct
                pass
        # simpler: just add & test rank via matrix
        M = np.array(basis + [v], dtype=np.int8)
        r = gf2_rank(M)
        if r > rank:
            basis.append(v)
            rank = r
        if rank == target_rank:
            break
        if cap and n_used >= cap:
            break
    return basis, n_used, rank, target_rank


def gf2_rank(M):
    A = M.copy().astype(np.int8) % 2
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        pivot = -1
        for rr in range(r, rows):
            if A[rr, c] == 1:
                pivot = rr
                break
        if pivot == -1:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        for rr in range(rows):
            if rr != r and A[rr, c] == 1:
                A[rr] = A[rr] ^ A[r]
        r += 1
    return r


def perp_from_basis(basis, kp1):
    """Given basis of K^perp (as row vectors), compute (K^perp)^perp = K
    as list of vectors in F_2^{kp1}."""
    if not basis:
        # perp of {0} is all of F_2^{kp1}
        return [int_to_vec(i, kp1) for i in range(2 ** kp1)]
    M = np.array(basis, dtype=np.int8) % 2
    K_recovered = []
    for i in range(2 ** kp1):
        v = int_to_vec(i, kp1)
        if all((M[j].dot(v) % 2) == 0 for j in range(M.shape[0])):
            K_recovered.append(v)
    return K_recovered


# --- Driver --------------------------------------------------------------

@dataclass
class CaseResult:
    k: int
    n_G: int
    sigma_flat: list
    u: list
    K: list
    K_size: int
    n_perp: int
    total_prob_on_perp: float
    max_prob_off_perp: float
    all_on_perp: bool
    samples_taken: int
    recovered_K: list
    match: bool


def run_case(k, seed=42, n_trials=200):
    sigma, u = choose_sigma_and_u(k, seed=seed)
    F = build_F_table(k, u, sigma)
    K = hidden_K_from_F(F, k)
    rho = coset_state_density(F, k)
    probs = measurement_distribution(rho, k + 1)
    perp = set(K_perp(K, k))
    on_perp = sum(probs[i] for i in perp)
    off_perp = [probs[i] for i in range(len(probs)) if i not in perp]
    max_off = max(off_perp) if off_perp else 0.0

    rng = np.random.default_rng(seed)
    samples = list(rng.choice(len(probs), size=n_trials, p=probs))
    basis, n_used, rank, target = recover_K_from_samples(samples, len(K), k + 1)
    K_rec = perp_from_basis(basis, k + 1)
    # Compare recovered K to true K as sets
    K_true_set = set(tuple(np.concatenate([[b], np.array(x)])) for (b, x) in K)
    K_rec_set = set(tuple(v) for v in K_rec)
    match = (K_true_set == K_rec_set)

    return CaseResult(
        k=k, n_G=2 ** (k + 1),
        sigma_flat=[int(x) for x in sigma.flatten().tolist()],
        u=[int(x) for x in u.tolist()],
        K=[[int(b), [int(x) for x in tup]] for (b, tup) in K],
        K_size=len(K),
        n_perp=len(perp),
        total_prob_on_perp=float(on_perp),
        max_prob_off_perp=float(max_off),
        all_on_perp=bool(max_off < 1e-12),
        samples_taken=int(n_used),
        recovered_K=[[int(x) for x in v] for v in sorted(K_rec_set)],
        match=bool(match),
    )


def main():
    import qiskit, qiskit_aer
    header = {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "qiskit": qiskit.__version__,
        "qiskit_aer": qiskit_aer.__version__,
    }
    print("versions:", header)
    results = []
    t0 = time.time()
    for k in (2, 3, 4, 5, 6):
        for seed in (7, 13, 42):
            r = run_case(k, seed=seed, n_trials=400)
            results.append(asdict(r))
            print(f"[k={k} seed={seed:>2}]  |G|={r.n_G:<3}  |K|={r.K_size}  "
                  f"|K^perp|={r.n_perp}  onPerp={r.total_prob_on_perp:.8f}  "
                  f"maxOffPerp={r.max_prob_off_perp:.2e}  "
                  f"samples={r.samples_taken}  match={r.match}")
    dt = time.time() - t0
    out = {"versions": header, "wall_seconds": dt, "cases": results}
    def _clean(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (list, tuple)):
            return [_clean(x) for x in o]
        if isinstance(o, dict):
            return {k: _clean(v) for k, v in o.items()}
        return o
    Path(__file__).with_name("ims_theorem13_results.json").write_text(
        json.dumps(_clean(out), indent=2))
    print(f"\nwall={dt:.2f}s   saved: ims_theorem13_results.json")


if __name__ == "__main__":
    main()
