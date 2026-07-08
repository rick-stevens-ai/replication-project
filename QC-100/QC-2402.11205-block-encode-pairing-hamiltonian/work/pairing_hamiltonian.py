"""
Build the pairing Hamiltonian of Liu-Du-Lin-Vary-Yang (arXiv:2402.11205),
Sec. 5.2 (three-nucleon system, 6 single-particle basis).

    H_pair = sum_{l1,l2 in {0,1,2}} c†_{2l1} c†_{2l1+1} c_{2l2+1} c_{2l2}   (Eq. 39, 40)

Represent 6 single-particle states as 6 qubits (occupation basis). Order:
    |j> = |j0 j1 j2 j3 j4 j5>,  j_k in {0,1}
where j_k=1 means the k-th single-particle state is occupied.

We use OpenFermion for the operator algebra, but build the many-body matrix
by *direct action on occupation basis kets* to avoid any Jordan-Wigner sign
convention ambiguity.

Since the H_pair term c†_{2l1} c†_{2l1+1} c_{2l2+1} c_{2l2} only annihilates
states where sites {2l2, 2l2+1} are BOTH occupied AND sites {2l1, 2l1+1} are
both empty (or =={2l2,2l2+1}), and always moves *pairs*, the phase factor is
+1 in the natural pair-ordered convention used in the paper (see Sec. 4.1.3).
"""
import numpy as np
from itertools import combinations

N_SITES = 6

def basis_states_with_n_particles(n_particles):
    """Return list of integers j (0..63) with popcount == n_particles.
       Bit k of j represents occupation of site k.
    """
    states = []
    for occ in combinations(range(N_SITES), n_particles):
        j = 0
        for k in occ:
            j |= (1 << k)
        states.append(j)
    return sorted(states)


def occupied_sites(j):
    return [k for k in range(N_SITES) if (j >> k) & 1]


def M_J(j):
    """Total angular-momentum projection for basis state j, using Table 1
       of the paper. Site k has 2*m_j given by:
         k=0: -1, k=1: +1, k=2: -1, k=3: +1, k=4: -1, k=5: +1
       So m_j(k) = -1/2 if k even, +1/2 if k odd.
    """
    total_2mj = 0
    for k in occupied_sites(j):
        total_2mj += (+1 if (k % 2 == 1) else -1)
    return total_2mj  # returns 2*M_J, integer


def apply_pair_term(l1, l2, j):
    """Apply c†_{2l1} c†_{2l1+1} c_{2l2+1} c_{2l2} to |j>.
    Returns (jout, phase) or None if annihilated. Phase is +/-1 using the
    paper's convention (pair operators are pseudo-one-body; phase = +1).
    """
    p, q = 2*l2, 2*l2 + 1          # to annihilate (need both occupied)
    r, s = 2*l1, 2*l1 + 1          # to create   (need both empty, or same as p,q)

    # 1) c_{q} then c_{p} : both must be occupied in j
    if not ((j >> p) & 1) or not ((j >> q) & 1):
        return None
    j_ann = j & ~(1 << p)
    j_ann = j_ann & ~(1 << q)

    # 2) c†_{s} then c†_{r} : both must be empty in j_ann
    if ((j_ann >> r) & 1) or ((j_ann >> s) & 1):
        return None
    j_out = j_ann | (1 << r) | (1 << s)

    # phase: paper says +1 for pair operators, see Sec. 4.1.3 remark
    return (j_out, +1)


def build_H_full():
    """Build the 64x64 Hamiltonian in the full 6-qubit occupation basis."""
    dim = 2**N_SITES
    H = np.zeros((dim, dim), dtype=float)
    for j in range(dim):
        for l1 in range(3):
            for l2 in range(3):
                res = apply_pair_term(l1, l2, j)
                if res is not None:
                    jout, phase = res
                    H[jout, j] += phase
    return H


def build_H_block(mj_target_times_2, n_particles=3):
    """Build the block of H in the subspace of fixed particle number and
       fixed 2*M_J value. Returns (H_block, basis_list) where basis_list is
       the ordered list of integers j in that subspace.
    """
    all_bs = basis_states_with_n_particles(n_particles)
    subspace = [j for j in all_bs if M_J(j) == mj_target_times_2]
    idx = {j: i for i, j in enumerate(subspace)}
    d = len(subspace)
    Hb = np.zeros((d, d), dtype=float)
    for j in subspace:
        col = idx[j]
        for l1 in range(3):
            for l2 in range(3):
                res = apply_pair_term(l1, l2, j)
                if res is not None:
                    jout, phase = res
                    if jout in idx:
                        Hb[idx[jout], col] += phase
    return Hb, subspace


if __name__ == "__main__":
    Hfull = build_H_full()
    print("H_full shape:", Hfull.shape, "nnz:", np.count_nonzero(Hfull))
    print("Hermitian?:", np.allclose(Hfull, Hfull.T))

    # Paper Sec. 5.2: MJ = +1/2 sector should be 9-dim and match Eq. (41)
    Hb, basis = build_H_block(+1, n_particles=3)  # 2*MJ = +1
    print(f"\nMJ=+1/2 sector: dim = {len(basis)}")
    print("Basis states (occupation-integer -> occupied sites):")
    # Paper's ordering:
    # (0,1,3), (0,1,5), (0,3,5), (1,2,3), (1,2,5), (1,3,4), (1,4,5), (2,3,5), (3,4,5)
    for j in basis:
        print(f"  j={j:2d} ({j:06b} = |{format(j,'06b')[::-1]}>)  occupied={occupied_sites(j)}, 2*M_J={M_J(j)}")

    print("\nH block (MJ=+1/2):")
    print(Hb.astype(int))

    # Expected matrix from paper Eq. (41), in paper's basis ordering
    # (0,1,3), (0,1,5), (0,3,5), (1,2,3), (1,2,5), (1,3,4), (1,4,5), (2,3,5), (3,4,5)
    expected = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
    ], dtype=int)

    # Rebuild basis in the paper's stated order and re-derive block
    def bits_to_int(occ_tuple):
        j = 0
        for k in occ_tuple:
            j |= (1 << k)
        return j
    paper_order = [(0,1,3),(0,1,5),(0,3,5),(1,2,3),(1,2,5),(1,3,4),(1,4,5),(2,3,5),(3,4,5)]
    ints = [bits_to_int(t) for t in paper_order]
    P = np.zeros((9,9))
    for new_i, j in enumerate(ints):
        old_i = basis.index(j)
        P[new_i, old_i] = 1
    Hb_reordered = P @ Hb @ P.T
    print("\nH block reordered to paper's ordering:")
    print(Hb_reordered.astype(int))
    print("\nMatches paper Eq. (41)?", np.array_equal(Hb_reordered.astype(int), expected))
    print("Frobenius diff:", np.linalg.norm(Hb_reordered - expected))
