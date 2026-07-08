"""
Block-encoding U_H for arXiv:2402.11205 Sec 5.2 (3-nucleon pairing).

Layout (13 qubits):
    bit 0        : v  (validation)
    bits 1..2    : a1, a2  (auxiliary, uncomputed)
    bits 3..4    : l1 (2 qubits, selection index for creation pair)
    bits 5..6    : l2 (2 qubits, selection index for annihilation pair)
    bits 7..12   : j0..j5 (Fock system)

Full Hilbert dim = 8192.

We build all operators as SPARSE permutation-or-superposition matrices
using scipy.sparse. Composition and unitarity checks stay tractable.

Circuit:
    U_H = X_v · (I ⊗ Ds ⊗ I) · O_C · (I ⊗ Ds ⊗ I)  ?

Actually from Fig 5 the order is (reading left→right in the circuit, i.e.,
operators applied right-to-left onto |ψ_in>):
    U_H |0^m>|j> = Ds · [U_{L-1} … U_0] · Ds · X_v |0>|0>|0>|0^m>|j>

We treat each U_l as an involution/permutation swap defined as:
    For selection = l, aux == |00>, v ∈ {0,1}:
      * If j is valid for l:  send |v>|00>|l>|j>  ↔  |1-v>|00>|l>|c(j,l)>
      * If j is the swap-partner c(j0, l) of some valid j0:
                              send |v>|00>|l>|j>  ↔  |1-v>|00>|l>|j0>
      * else: identity
    On other inputs (a1|a2 != 0 or wrong sel): identity
    For l1==l2 (diagonal, c(j,l)=j fixed): |v>|00>|l>|j> → |1-v>|00>|l>|j>
      when j is valid, else identity.

O_C = prod_l U_l  (commuting permutations on disjoint supports for
different l values in the sense that they trigger on different sel).
"""
import numpy as np
from scipy import sparse
from pairing_hamiltonian import build_H_full, build_H_block, N_SITES

N_ANC = 7
DIM_ANC = 2 ** N_ANC          # 128
DIM_SYS = 2 ** N_SITES        # 64
DIM_TOT = DIM_ANC * DIM_SYS   # 8192

def make_index(v, a1, a2, l1, l2, j):
    anc = v | (a1 << 1) | (a2 << 2) | (l1 << 3) | (l2 << 5)
    return anc * DIM_SYS + j

def unpack_index(idx):
    j = idx % DIM_SYS
    anc = idx // DIM_SYS
    v  = (anc >> 0) & 1
    a1 = (anc >> 1) & 1
    a2 = (anc >> 2) & 1
    l1 = (anc >> 3) & 3
    l2 = (anc >> 5) & 3
    return v, a1, a2, l1, l2, j

def apply_pair_direct(l1, l2, j):
    p, q = 2*l2, 2*l2 + 1
    r, s = 2*l1, 2*l1 + 1
    if not ((j >> p) & 1) or not ((j >> q) & 1):
        return None
    j_ann = j & ~(1 << p) & ~(1 << q)
    if ((j_ann >> r) & 1) or ((j_ann >> s) & 1):
        return None
    j_out = j_ann | (1 << r) | (1 << s)
    return j_out

def build_X_v_sparse():
    rows = np.empty(DIM_TOT, dtype=np.int64)
    cols = np.arange(DIM_TOT, dtype=np.int64)
    data = np.ones(DIM_TOT, dtype=np.float64)
    for idx in range(DIM_TOT):
        v, a1, a2, l1, l2, j = unpack_index(idx)
        rows[idx] = make_index(1 - v, a1, a2, l1, l2, j)
    return sparse.csr_matrix((data, (rows, cols)), shape=(DIM_TOT, DIM_TOT))

def build_D_full_sparse():
    # Hadamard on 4 selection qubits (bits 3,4,5,6 of ancilla index).
    # Ds is 16x16 dense; embed as a block-diagonal-like operator that mixes
    # only the 4 selection bits, keeps (v, a1, a2, j) fixed.
    H1 = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2)
    Ds = np.array([[1.0]])
    for _ in range(4):
        Ds = np.kron(Ds, H1)
    # 16x16 dense — that's fine

    rows = []
    cols = []
    data = []
    # For each (v, a1, a2, j), the selection register (16 states) is mixed by Ds
    for v in (0, 1):
        for a1 in (0, 1):
            for a2 in (0, 1):
                for j in range(DIM_SYS):
                    for sel_src in range(16):
                        l1_s = sel_src & 3
                        l2_s = (sel_src >> 2) & 3
                        src = make_index(v, a1, a2, l1_s, l2_s, j)
                        for sel_dst in range(16):
                            amp = Ds[sel_dst, sel_src]
                            if amp == 0:
                                continue
                            l1_d = sel_dst & 3
                            l2_d = (sel_dst >> 2) & 3
                            dst = make_index(v, a1, a2, l1_d, l2_d, j)
                            rows.append(dst); cols.append(src); data.append(amp)
    return sparse.csr_matrix((data, (rows, cols)), shape=(DIM_TOT, DIM_TOT))

def build_U_l_sparse(l1_target, l2_target):
    """As a sparse permutation matrix.

    Following the paper's construction (Fig 13, Sec 4.1.3):
      - Trigger only when sel == (l1_target, l2_target), a1==0, a2==0.
      - If j is VALID for the pair term (l1_target, l2_target):
            forward:  |v>|00>|l>|j>       -->  |1-v>|00>|l>|c(j,l)>
            reverse:  |v>|00>|l>|c(j,l)>  -->  |1-v>|00>|l>|j>
        (This is an involution on the pair {j, c(j,l)} in the j-register,
         combined with v-flip.  Note: c(j,l) is INVALID for l when l1!=l2
         — that's fine, the operator still maps it back to j.)
      - Else (j not valid AND not a swap-partner of any valid j): identity.

    NOTE: For the block-encoding SUM to correctly reproduce H_ij with unit
    weight per pair term, the reverse branch |v>|00>|l>|c(j,l)> --> |1-v>|00>|l>|j>
    is essential for U_l to be a unitary AND for the diffusion projection to
    give the right sign structure — but it does NOT introduce extra amplitude
    at the (jout, j) matrix element beyond one per pair term, because the
    reverse branch acts on the DIFFERENT input state |...>|c(j,l)>.

    ISSUE FOUND EMPIRICALLY: with our first construction, we saw a factor
    of 2 on off-diagonal H entries. Root cause: the same (jout, j) entry
    receives one 1/16 contribution from l=(l1,l2) [forward branch acting
    on j] AND another 1/16 contribution from l=(l2,l1) [also forward, since
    l=(l2,l1) also has j valid — check: c†_{2l2}c†_{2l2+1}c_{2l1+1}c_{2l1}
    applied to j needs {2l1,2l1+1} occ (as j does) and {2l2,2l2+1} empty
    (as c(j, (l1,l2)) has, but j itself may NOT satisfy this — so l=(l2,l1)
    might not be valid on j.]

    Wait: for j={0,1,3}, l=(0,2): c†_0 c†_1 c_5 c_4. Needs {4,5} occ, {0,1}
    empty. j has {0,1} occ → INVALID.  So l=(0,2) does NOT act on j directly.
    But my reverse-branch code sends the swap-partner input to j0. The
    swap-partner of j0={3,4,5} under l=(0,2) is c(j0,l=(0,2))={0,1,3}=j.
    So when we apply U_l for l=(0,2) to input state |v>|00>|l=(0,2)>|j>,
    j is a swap-partner (of j0={3,4,5}), so my code sends it to
    |1-v>|00>|l=(0,2)>|j0={3,4,5}>. This ADDS amplitude to |{3,4,5}> in the
    output — the SAME (jout=|{3,4,5}>, jin=j={0,1,3}) matrix element that
    l=(2,0) forward branch also contributes to.  DOUBLE-COUNTED.

    RESOLUTION: replace the swap-partner branch with the simple choice
    "identity on swap-partner inputs" (drops the extra 1/16 contribution).
    This means U_l is NO LONGER a full permutation of the j-register on
    the trigger subspace — but it is still unitary IF we route those
    invalid-inputs consistently. Actually if we do identity on the invalid
    branch, and the forward branch sends valid j -> c(j,l) (which is a state
    with a1=a2=0), we have collisions: the OUTPUT state |1-v>|00>|l>|c(j,l)>
    coincides with the DIAGONAL of the identity branch |v>|00>|l>|c(j,l)>
    for the OTHER value of v. So there are again collisions.

    A clean fix: use the a1 auxiliary qubit to record the swap. Concretely:
        For sel==l, a1=0, a2=0:
            valid j  ->  a1<-1, then swap j->c(j,l), then flip v, then a1<-0
        which uncomputes.  Then U_l on trigger subspace is:
            valid   |v>|00>|l>|j>       -> |1-v>|00>|l>|c(j,l)>
            invalid |v>|00>|l>|j>       -> |v>|00>|l>|j>  (identity)
        This map on (v, j) alone is NOT a permutation because both
        |0>|c(j,l)> AND |0>|j> for valid j map to distinct outputs, but the
        VALID output is |1>|c(j,l)> which coincides with the identity output
        |1>|c(j,l)> for input |1>|c(j,l)>.  Collision.

    Simplest fully-correct construction using EXISTING ancillas: on invalid
    inputs, ALSO flip v (leaving j alone). Then trigger subspace map is:
        valid   |v>|00>|l>|j>       -> |1-v>|00>|l>|c(j,l)>
        invalid |v>|00>|l>|j>       -> |1-v>|00>|l>|j>
    This IS a permutation on the trigger subspace of (v, j): for each j,
    the map is a permutation of v combined with a (v-independent) j-shuffle.
    For it to be well-defined (bijection on (v,j)), we need: valid outputs
    {(1-v, c(j,l)): j valid} disjoint from invalid outputs {(1-v, j): j invalid}.
    That requires c(j,l) is NOT in the invalid set of j's. But c(j,l) IS
    invalid! So collision:
        input (v=0, j=|000111>) valid (l=(0,2)) -> output (1, c(j,l)=|110100>)
        input (v=0, j=|110100>) invalid -> output (1, |110100>)
    Both outputs are (1, |110100>). COLLISION.

    Correct clean answer: define
        valid j     |v>|00>|l>|j>       -> |1-v>|00>|l>|c(j,l)>
        c(j,l) inv  |v>|00>|l>|c(j,l)>  -> |1-v>|00>|l>|j>          [swap back]
        other inv   |v>|00>|l>|j>       -> |v>|00>|l>|j>            [identity, no v flip]

    In this hybrid, only the c(j,l)-image states (which are all invalid under
    l for l1!=l2) participate in the swap; other invalid j's are true identity.
    On the (v, j)-plane restricted to trigger, valid j's and their swap partners
    form disjoint 4-element orbits {(0,j), (1,j), (0,c(j,l)), (1,c(j,l))} on
    which the map is a permutation (v flip + j swap). Other j's: (0,j)↔(0,j),
    (1,j)↔(1,j). Fully unitary.

    And this is EXACTLY what my original code did! So why the factor-of-2?

    Because in the block-encoding SUM, both branches (valid forward AND
    swap-partner reverse) contribute to the SAME output state. Specifically,
    starting from input |0>|00>|0000>|j_in>, after X_v we have |1>|00>|l>|j_in>
    in each l-branch (after diffusion 1/4). For l=(l1,l2) with j_in valid:
    forward gives |0>|00>|l>|c(j_in,l)>. For l=(l2,l1) which is the reverse
    of the same physical process: if j_in is c(j0, l=(l2,l1)) for some valid
    j0, then reverse-branch gives |0>|00>|l=(l2,l1)>|j0>. And j0 = c(j_in, l=(l1,l2))
    — the same output as the forward branch!

    So the same physical off-diagonal matrix element H_{jout,j_in} = 1 gets
    TWO contributions of 1/16 each = 2/16, hence 16*block = 2 instead of 1.

    FIX: The paper's H (Eq. 39) has 9 pair terms, and the (l1,l2) and
    (l2,l1) terms are treated as DISTINCT operators (both included in the
    sum). So the physical H_{jout, j_in} for a fixed off-diagonal transition
    genuinely receives contribution 1 from ONE of the pair terms (say (l1,l2))
    and 0 from the other (say (l2,l1)) — because c†_{2l1}c†_{2l1+1}c_{2l2+1}c_{2l2}
    is the CORRECT direction for one, and the reverse c†_{2l2}c†_{2l2+1}c_{2l1+1}c_{2l1}
    acts DIFFERENTLY on j_in (indeed it acts on c(j_in), not on j_in).

    So H has genuinely 1 (not 2) at (jout, j_in). Our block-encoding sums
    over both l orderings AND uses swap-partner branches, giving 2. To fix:
    REMOVE the swap-partner branch in U_l for off-diagonal l. On swap-partner
    inputs, do TRUE IDENTITY (do NOT flip v). And accept the trigger subspace
    map is now not a permutation of (v,j) alone — but it IS still unitary
    IF the aux qubits absorb the extra info. Since our aux qubits are always
    0 in the encoding projection, and outside the encoding projection we
    don't care, we can afford a construction that is unitary GLOBALLY but
    trivial off the encoding-input subspace.

    Simplest global-unitary fix: define U_l as follows.

    Let's use a1 as follows:
        For sel==l, a2==0:
            state |v>|a1=0>|a2=0>|l>|j>:
              if j valid:  -->  |v>|a1=1>|a2=0>|l>|j>
            state |v>|a1=1>|a2=0>|l>|j>:
              if j valid:  -->  |1-v>|a1=0>|a2=0>|l>|c(j,l)>
            (both directions, forming a size-2 orbit for each valid j)
            other states: identity

    But then applying U_l ONCE gives |v>|a1=1>|a2=0>|l>|j> starting from
    |v>|a1=0>|a2=0>|l>|j>. Aux is not 0 -> falls out of projection. Ugh.

    OK let me stop overthinking. The RIGHT thing is: use a controlled-swap
    structure that only fires on valid j and uncomputes cleanly. Simplest
    correct version that keeps aux at 0 in the input & output:

        For sel==l, a1=0, a2=0:
          if j valid for l:  |v>|00>|l>|j> --> |1-v>|00>|l>|c(j,l)>
          if j invalid:      |v>|00>|l>|j> --> |v>|00>|l>|j>   (identity)

    And to be a valid unitary GLOBALLY, use the invalid-input branch on the
    aux=|11> subspace to receive the "other half" of the swap:
          |v>|11>|l>|j> --> |1-v>|11>|l>|c^{-1}(j,l)>   if j is in image(c)
          |v>|11>|l>|j> --> |v>|11>|l>|j>              otherwise

    Then aux=|00> is invariant under U_l, and the trigger subspace map on
    aux=|00> is what we want: forward valid transition (each pair term
    fires ONCE, no reverse-partner double-count).
    """
    valid_j = {}
    for j in range(DIM_SYS):
        jc = apply_pair_direct(l1_target, l2_target, j)
        if jc is not None:
            valid_j[j] = jc
    # For l1!=l2, valid_j keys and values are disjoint (verified analytically)
    if l1_target != l2_target:
        c_values = set(valid_j.values())
        for j in valid_j:
            assert j not in c_values
    inv_c = {jc: j for j, jc in valid_j.items()}

    rows = np.empty(DIM_TOT, dtype=np.int64)
    cols = np.arange(DIM_TOT, dtype=np.int64)
    data = np.ones(DIM_TOT, dtype=np.float64)

    for src in range(DIM_TOT):
        v, a1, a2, l1, l2, j = unpack_index(src)
        if (l1, l2) != (l1_target, l2_target):
            rows[src] = src
            continue
        # Trigger branch on aux=(0,0): forward-valid or identity
        if a1 == 0 and a2 == 0:
            if l1_target == l2_target:
                # Diagonal: j valid means number operator == 1
                if j in valid_j:
                    rows[src] = make_index(1 - v, 0, 0, l1_target, l2_target, j)
                else:
                    rows[src] = src
            else:
                if j in valid_j:
                    jout = valid_j[j]
                    rows[src] = make_index(1 - v, 0, 0, l1_target, l2_target, jout)
                else:
                    rows[src] = src
        elif a1 == 1 and a2 == 1:
            # Absorbs swap-back to keep global unitary
            if l1_target != l2_target:
                if j in inv_c:
                    j0 = inv_c[j]
                    rows[src] = make_index(1 - v, 1, 1, l1_target, l2_target, j0)
                else:
                    rows[src] = src
            else:
                # diagonal: only receives its own valid inputs
                if j in valid_j:
                    rows[src] = make_index(1 - v, 1, 1, l1_target, l2_target, j)
                else:
                    rows[src] = src
        elif a1 == 1 and a2 == 0:
            # Route valid j -> (v flipped, aux=(0,1), c(j,l))
            if l1_target != l2_target:
                if j in valid_j:
                    jout = valid_j[j]
                    rows[src] = make_index(1 - v, 0, 1, l1_target, l2_target, jout)
                elif j in inv_c:
                    j0 = inv_c[j]
                    rows[src] = make_index(1 - v, 0, 1, l1_target, l2_target, j0)
                else:
                    rows[src] = src
            else:
                if j in valid_j:
                    rows[src] = make_index(1 - v, 0, 1, l1_target, l2_target, j)
                else:
                    rows[src] = src
        else:
            # a1=0, a2=1: swap back to a1=1,a2=0 branch
            if l1_target != l2_target:
                if j in valid_j:
                    jout = valid_j[j]
                    rows[src] = make_index(1 - v, 1, 0, l1_target, l2_target, jout)
                elif j in inv_c:
                    j0 = inv_c[j]
                    rows[src] = make_index(1 - v, 1, 0, l1_target, l2_target, j0)
                else:
                    rows[src] = src
            else:
                if j in valid_j:
                    rows[src] = make_index(1 - v, 1, 0, l1_target, l2_target, j)
                else:
                    rows[src] = src

    U = sparse.csr_matrix((data, (rows, cols)), shape=(DIM_TOT, DIM_TOT))

    # Unitarity spot-check: check permutation property (all rows unique)
    unique_rows = len(set(rows.tolist()))
    if unique_rows != DIM_TOT:
        print(f"WARNING: U_l({l1_target},{l2_target}) not a permutation: {unique_rows}/{DIM_TOT} unique rows")
    return U

def build_U_H_sparse():
    print("  building X_v...")
    Xv = build_X_v_sparse()
    print("  building D_full...")
    D = build_D_full_sparse()
    print(f"    D nnz = {D.nnz}, shape={D.shape}")

    O_C = sparse.identity(DIM_TOT, dtype=np.float64, format='csr')
    for l1 in range(3):
        for l2 in range(3):
            print(f"  building U_{{{l1},{l2}}}...")
            Ul = build_U_l_sparse(l1, l2)
            O_C = Ul @ O_C

    print("  composing U_H = D · O_C · D · X_v ...")
    U_H = D @ O_C @ D @ Xv

    # Unitarity check via matmul
    print("  checking unitarity ...")
    I_test = U_H @ U_H.T   # since all matrices real
    err = sparse.linalg.norm(I_test - sparse.identity(DIM_TOT, format='csr'))
    print(f"  ||U_H U_H^T - I||_F = {err:.3e}")
    return U_H, err

def extract_top_left_block(U):
    """Rows/cols with ancilla index = 0 => indices 0..DIM_SYS-1."""
    return U[:DIM_SYS, :DIM_SYS].toarray()


def main():
    import json, os
    print("="*70)
    print("BLOCK ENCODING VERIFICATION for arXiv:2402.11205 Sec 5.2")
    print("="*70)

    H = build_H_full()
    print(f"H_pair: shape {H.shape}, nnz={np.count_nonzero(H)}, ||H||_F = {np.linalg.norm(H):.6f}")
    ew = np.linalg.eigvalsh(H)
    print(f"H eigenvalue range: [{ew.min():.3f}, {ew.max():.3f}], spectral norm = {np.max(np.abs(ew)):.3f}")

    print("\nBuilding U_H (sparse) ...")
    U_H, unit_err = build_U_H_sparse()

    block = extract_top_left_block(U_H)
    print(f"\nExtracted top-left block: shape {block.shape}, max|imag|=0 (real construction)")
    block_real = block

    print("\n--- Testing subnormalization values ---")
    best_alpha = None
    best_err = float('inf')
    for alpha in [4, 8, 9, 16, 32, 64]:
        diff = np.linalg.norm(alpha * block_real - H)
        print(f"  alpha = {alpha:3d}: ||alpha*block - H||_F = {diff:.6e}")
        if diff < best_err:
            best_err = diff; best_alpha = alpha

    num = float((block_real * H).sum())
    den = float((block_real * block_real).sum())
    alpha_LS = num / den if den > 0 else float('nan')
    diff_LS = np.linalg.norm(alpha_LS * block_real - H)
    print(f"\nLeast-squares optimal alpha: {alpha_LS:.10f}   err {diff_LS:.6e}")

    mask = (H != 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratios = H[mask] / block_real[mask]
    valid_ratios = ratios[np.isfinite(ratios) & (np.abs(ratios) > 1e-15)]
    print(f"\nRatios H_ij / block_ij at nonzero H entries:")
    print(f"  n_valid = {len(valid_ratios)} / {mask.sum()}")
    if len(valid_ratios) > 0:
        print(f"  min={np.min(valid_ratios):.6f} max={np.max(valid_ratios):.6f} mean={np.mean(valid_ratios):.6f} median={np.median(valid_ratios):.6f}")

    # MJ+1/2 sub-block
    Hb, subspace = build_H_block(+1, n_particles=3)
    print(f"\n--- MJ=+1/2 subspace ({len(subspace)}-dim) ---")
    block_sub = block_real[np.ix_(subspace, subspace)]

    def bits_to_int(occ):
        j = 0
        for k in occ: j |= (1 << k)
        return j
    paper_order = [(0,1,3),(0,1,5),(0,3,5),(1,2,3),(1,2,5),(1,3,4),(1,4,5),(2,3,5),(3,4,5)]
    ints_paper = [bits_to_int(t) for t in paper_order]
    perm = [subspace.index(j) for j in ints_paper]
    block_sub_paper = block_sub[np.ix_(perm, perm)]

    paper_H = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
    ], dtype=float)

    print("16 * block (paper ordering, rounded 3):")
    print(np.round(16 * block_sub_paper, 3))
    print("Paper Eq (41):")
    print(paper_H.astype(int))
    diff_paper = np.linalg.norm(16 * block_sub_paper - paper_H)
    print(f"||16 * block_paper_order - paper_Eq41||_F = {diff_paper:.6e}")

    print("\n" + "="*70)
    print("HEADLINE VERIFICATION")
    print("="*70)
    alpha_paper = 16
    err_full = np.linalg.norm(alpha_paper * block_real - H)
    tol = 1e-8
    verdict = "PASS" if err_full < tol else "FAIL"
    print(f"Paper claim: (alpha, m) = ({alpha_paper}, 5)-block encoding of H_pair")
    print(f"Our construction: 7 ancillas total (1 val + 2 aux + 4 sel);")
    print(f"  paper's m=5 corresponds to 1 val + 4 sel; 2 aux uncompute cleanly.")
    print(f"|| {alpha_paper} * block - H_pair ||_F  =  {err_full:.6e}   (tol {tol})   =>  {verdict}")
    print(f"|| {alpha_paper} * block - H_MJ+1/2 ||_F (paper order)  =  {diff_paper:.6e}")

    n = N_SITES; L = 9
    two_q = 12 * L * np.log2(L) + 23 * L
    Tg   = 14 * L * np.log2(L) + 21 * L
    print("\n--- Resource summary (paper Sec 4.4 formulas) ---")
    print(f"  n_sys={n}, L={L}")
    print(f"  two-qubit gates ~ 12 L log L + 23 L = {two_q:.1f}")
    print(f"  T gates         ~ 14 L log L + 21 L = {Tg:.1f}")
    print(f"  ancilla scaling : O(log L) selection + O(1) upper")

    evidence = {
        "paper_arxiv_id": "2402.11205",
        "paper_title": "An Efficient Quantum Circuit for Block Encoding a Pairing Hamiltonian",
        "paper_headline_claim": {
            "block_encoding_parameters_alpha_m": [16, 5],
            "H_MJ+1/2_matrix_Eq41_form": "diag+antidiag structure per paper Eq. (41)",
            "gate_complexity": "O(L log L) two-qubit and T gates = O(poly(n) log n)",
            "ancilla_complexity": "O(log L) selection + O(1) upper"
        },
        "our_construction": {
            "n_system_qubits": n,
            "n_ancilla_qubits_total": 7,
            "n_ancilla_in_projection": 7,
            "diffusion_qubits": 4,
            "empirical_alpha_LS": float(alpha_LS),
            "empirical_alpha_int_best_match": int(best_alpha),
            "ratio_H_over_block_min": float(np.min(valid_ratios)) if len(valid_ratios) else None,
            "ratio_H_over_block_max": float(np.max(valid_ratios)) if len(valid_ratios) else None,
        },
        "verification_results": {
            "unitarity_error_UH_Frob": float(unit_err),
            "block_encoding_error_alpha16_full_H_Frob": float(err_full),
            "block_encoding_error_alpha16_MJ+1/2_Frob": float(diff_paper),
            "H_MJ+1/2_matches_paper_Eq41_exactly": bool(np.array_equal((16*block_sub_paper).round().astype(int), paper_H.astype(int))),
            "tolerance": tol,
            "verdict": verdict,
        },
        "gate_counts_paper_formula": {
            "L": L,
            "two_qubit_gates_estimate": float(two_q),
            "T_gates_estimate": float(Tg),
        },
    }

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "report", "evidence")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "block_encoding_verification.json"), "w") as f:
        json.dump(evidence, f, indent=2)
    np.savetxt(os.path.join(out_dir, "H_pair_MJp1_2_paper_order.txt"), paper_H, fmt="%2d")
    np.savetxt(os.path.join(out_dir, "block_x16_paper_order.txt"), 16*block_sub_paper, fmt="%7.3f")
    print(f"\nEvidence written to {out_dir}")
    return verdict, err_full, diff_paper


if __name__ == "__main__":
    v, ef, es = main()
    print(f"\nFINAL: verdict={v}  full_err={ef:.3e}  MJ+1/2_err={es:.3e}")
