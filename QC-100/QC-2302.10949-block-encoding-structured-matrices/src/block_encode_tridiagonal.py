"""
Replication of Sünderhauf, Campbell, Camps (2023) arXiv:2302.10949
"Block-encoding structured matrices for data input in quantum computing"

Reproduces the base scheme (Sec 2.1.2 + Sec 3.3) for small symmetric
tridiagonal matrices, verifying:

  (a) The constructed unitary U satisfies:
        <0|_data <0|_s <i|_out  U  |0>_data |0>_s |j>_out
        = A[i, j] / (S_pad * ||A||_max)
      to machine precision (paper eq. 12).

  (b) Cost claim (Sec 3.3): the base-scheme block encoding uses
        1 + log2(S_pad) = 3 flag qubits (with S_pad = 4, sparsity S = 3)
      independent of N, vs Gilyén et al.'s 3 + log2(N) flag qubits.

CIRCUIT (paper eq. 11), corrected register understanding:

  Registers:
    data (1 qubit, dim 2)         - flag qubit that carries the rotation
    s    (n_s qubits, dim S_pad)  - flag qubit (used as s_c on left, s_r on right)
    out  (n_out qubits, dim N)    - "output" register (j on left, i on right)

  The (d, m) labels in the circuit are NOT independent qubits: they
  parametrize the same (s, out) space of dimension S*N = M*D (paper
  eq. 5), where the oracles O_c and O_r are PERMUTATIONS between the
  (sc, j) / (sr, i) orderings and the (d, m) ordering:

        O_c |d> |m> = |sc> |j>        (paper eq. 6)
        O_r |d> |m> = |sr> |i>

  Concretely, (d, m) is an index in [0..D_pad) x [0..M) of size D_pad*M,
  which equals S_pad*N. We enumerate a bijection between these two.

  Total flag qubits (base scheme):  1 + log2(S_pad) = 3   (constant in N)
  Total qubits:                     1 + log2(S_pad) + log2(N) = 3 + log2(N)

  Compared to Gilyén et al. (paper Sec 3.3 explicit claim):
    3 + log2(N) flag qubits (5 for N=4, 6 for N=8, 7 for N=16, ...)
"""

import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector


# -----------------------------------------------------------------------------
# Tridiagonal labelling (paper Sec 3.3, eq. 57-60)
# -----------------------------------------------------------------------------

def tridiag_labels(N):
    """
    All (d, m) pairs for a symmetric tridiagonal N x N matrix, with the
    paper's padding: D_pad = 2N, M = 2, S_pad = 4 (=> D_pad*M = S_pad*N = 4N).

    Returns list of length D_pad*M with 'i', 'j', 'in_range', 'value_index'.
    """
    D_pad = 2 * N
    M = 2
    pairs = []
    for d in range(D_pad):
        d_hi = d // 2
        d_lo = d % 2
        for m in range(M):
            oor = (d_lo == 0 and m == 1) or (d == 2 * N - 1)
            if oor:
                pairs.append({"d": d, "m": m, "in_range": False,
                              "i": -1, "j": -1, "value_index": -1})
            else:
                i = d_hi + m
                j = d_hi + (d_lo if m == 0 else 0)
                pairs.append({"d": d, "m": m, "in_range": True,
                              "i": i, "j": j, "value_index": d})
    return pairs


def tridiagonal_matrix(main_diag, off_diag):
    N = len(main_diag)
    A = np.zeros((N, N), dtype=float)
    for i in range(N):
        A[i, i] = main_diag[i]
    for i in range(N - 1):
        A[i, i + 1] = off_diag[i]
        A[i + 1, i] = off_diag[i]
    return A


def make_A_vector(A):
    """Distinct entries A_d, d = 0..2N-2 in the paper's labelling."""
    N = A.shape[0]
    vec = np.zeros(2 * N - 1, dtype=float)
    for d in range(2 * N - 1):
        d_hi = d // 2
        d_lo = d % 2
        if d_lo == 0:
            vec[d] = A[d_hi, d_hi]
        else:
            vec[d] = A[d_hi, d_hi + 1]
    return vec


# -----------------------------------------------------------------------------
# Build the oracles as permutations on the (s, out) = (d, m) space
# -----------------------------------------------------------------------------

def build_column_oracle_perm(pairs, N, S_pad, D_pad, M):
    """
    Build O_c as a permutation on the (s, out) space of dimension S_pad*N.
    O_c |d>|m> = |sc>|j>  is a bijection between the (d, m) enumeration
    (dim D_pad*M) and the (sc, j) enumeration (dim S_pad*N). Since
    D_pad*M = S_pad*N, both are dim 4N.

    Convention: We flatten (d, m) as index `dm = d + D_pad * m` in
    [0..4N). We flatten (sc, j) as index `sj = sc + S_pad * j` in
    [0..4N). O_c is a permutation such that column dm of O_c is a
    standard basis vector e_{sj} for some sj = f_c(dm).

    Assignment rule:
      For each j in 0..N-1, collect all in-range pairs (d, m) with
      j(d,m) = j; assign them sc = 0, 1, 2, ... in some canonical order
      (which one goes to sc=0 is IRRELEVANT for the block encoding, only
      that they occupy the S_pad "slots" for that j).
      Any remaining sc slots (S_pad - n_inrange_for_j) get assigned to
      out-of-range pairs to complete the bijection.
    """
    n_slots = S_pad * N          # 4N
    assert n_slots == D_pad * M

    perm_dm_to_sj = -np.ones(n_slots, dtype=int)  # index by dm
    used_sj = np.zeros(n_slots, dtype=bool)

    def sj_index(sc, j):
        return sc + S_pad * j

    def dm_index(d, m):
        return d + D_pad * m

    # In-range pairs first, assigning sc = 0, 1, ... for each j
    sc_next_for_j = [0] * N
    for P in pairs:
        if not P["in_range"]:
            continue
        j = P["j"]
        sc = sc_next_for_j[j]
        sc_next_for_j[j] += 1
        assert sc < S_pad
        sj = sj_index(sc, j)
        dm = dm_index(P["d"], P["m"])
        assert not used_sj[sj]
        perm_dm_to_sj[dm] = sj
        used_sj[sj] = True

    # Out-of-range pairs: fill remaining sj slots
    remaining_sj = [k for k in range(n_slots) if not used_sj[k]]
    remaining_dm = [k for k, v in enumerate(perm_dm_to_sj) if v < 0]
    assert len(remaining_dm) == len(remaining_sj)
    for dm, sj in zip(remaining_dm, remaining_sj):
        perm_dm_to_sj[dm] = sj

    # Sanity: perm_dm_to_sj should be a permutation of [0..4N)
    assert sorted(perm_dm_to_sj.tolist()) == list(range(n_slots))
    return perm_dm_to_sj  # perm[dm] = sj  meaning O_c maps |dm> -> |sj>


def build_row_oracle_perm(pairs, N, S_pad, D_pad, M):
    """
    Same as build_column_oracle_perm but using i(d,m) instead of j(d,m).
    O_r |d>|m> = |sr>|i>.
    """
    n_slots = S_pad * N
    perm_dm_to_si = -np.ones(n_slots, dtype=int)
    used_si = np.zeros(n_slots, dtype=bool)

    def si_index(sr, i):
        return sr + S_pad * i

    def dm_index(d, m):
        return d + D_pad * m

    sr_next_for_i = [0] * N
    for P in pairs:
        if not P["in_range"]:
            continue
        i = P["i"]
        sr = sr_next_for_i[i]
        sr_next_for_i[i] += 1
        assert sr < S_pad
        si = si_index(sr, i)
        dm = dm_index(P["d"], P["m"])
        perm_dm_to_si[dm] = si
        used_si[si] = True

    remaining_si = [k for k in range(n_slots) if not used_si[k]]
    remaining_dm = [k for k, v in enumerate(perm_dm_to_si) if v < 0]
    for dm, si in zip(remaining_dm, remaining_si):
        perm_dm_to_si[dm] = si

    assert sorted(perm_dm_to_si.tolist()) == list(range(n_slots))
    return perm_dm_to_si


def perm_to_matrix(perm):
    """Build a permutation matrix P such that P |x> = |perm[x]>."""
    n = len(perm)
    P = np.zeros((n, n), dtype=complex)
    for x, y in enumerate(perm):
        P[y, x] = 1.0
    return P


# -----------------------------------------------------------------------------
# Build the block-encoding unitary U (paper eq. 11)
# -----------------------------------------------------------------------------

def build_block_encoding(A):
    """
    Build U on registers (data, s, out):
        data: 1 qubit
        s   : log2(S_pad) = 2 qubits    (used as s_c on left, s_r on right)
        out : log2(N)     qubits         (j on left, i on right)

    Total: n_total = 1 + 2 + log2(N) qubits.

    U = (H_S^dag on s ⊗ I) . O_r . R_data . O_c^dag . (H_S on s ⊗ I)

    where:
      - H_S on s = Hadamard^{log2 S_pad} (S_pad = 4 => H⊗H).
      - O_c is a permutation on the (s, out) space, mapping (d, m) index
        (in a chosen enumeration) to (sc, j) index. Then O_c^dag is its
        inverse. We build O_c on (s ⊗ out) space, tensor with I_data.
        R_data acts on data qubit, multiplexed on the (d, m) index which
        in the (s, out) subspace corresponds to a specific enumeration
        we make explicit.

    The Odata rotation is done AFTER O_c^dag, at which point the state
    of (s, out) is in the (d, m) enumeration. We apply R(A_d/||A||_max)
    controlled on the (d, m) index (which is now the (s, out) index
    read via the inverse permutation of O_c).

    NB: The paper draws O_c and O_r as acting on the (d, m, s_c, j)
    registers separately; in our implementation we exploit MD = NS to
    keep (d, m) implicit as an alternative labelling of the same
    log2(NS)-qubit register.
    """
    N = A.shape[0]
    assert (N & (N - 1)) == 0 and N >= 2

    S_pad = 4
    D_pad = 2 * N
    M = 2

    n_data = 1
    n_s = int(np.log2(S_pad))         # 2
    n_out = int(np.log2(N))           # log2(N)
    n_flag = n_data + n_s
    n_total = n_data + n_s + n_out

    dim = 2 ** n_total
    dim_sout = (2 ** n_s) * N          # = S_pad * N = 4N

    Avec = make_A_vector(A)
    Amax = float(np.max(np.abs(Avec)))
    assert Amax > 0

    pairs = tridiag_labels(N)

    perm_c_dm_to_sj = build_column_oracle_perm(pairs, N, S_pad, D_pad, M)
    perm_r_dm_to_si = build_row_oracle_perm(pairs, N, S_pad, D_pad, M)

    # O_c as a matrix on (s, out) space: O_c |dm> = |sj>
    # We use the (s, out) subspace with little-endian:
    #    sub_idx(s, out) = s + S_pad * out
    # and identify this with the (sc, j) enumeration. To apply O_c on
    # the (d, m) enumeration, we index columns by dm.
    O_c_sout = np.zeros((dim_sout, dim_sout), dtype=complex)
    for dm in range(dim_sout):
        sj = perm_c_dm_to_sj[dm]
        # O_c: column dm becomes basis vector at row sj. But we treat
        # the (s, out) space as a SINGLE labelling — the column index
        # `dm` is the (d, m) label (in flat order dm = d + D_pad*m), and
        # the row index `sj` is the (sc, j) label (in flat order
        # sj = sc + S_pad*j).
        # Since both labels index the SAME Hilbert space of dim 4N, we
        # treat the labels as different orderings and identify the
        # (s, out) basis with the (sc, j) ordering. Then O_c takes a
        # state labelled by dm (in the alternative basis) to a state
        # labelled by sj (in the primary basis).
        O_c_sout[sj, dm] = 1.0

    # Similarly O_r maps (d, m) to (sr, i)
    O_r_sout = np.zeros((dim_sout, dim_sout), dtype=complex)
    for dm in range(dim_sout):
        si = perm_r_dm_to_si[dm]
        O_r_sout[si, dm] = 1.0

    # HS on s register (dim 4): H ⊗ H
    H2 = (1.0 / np.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=complex)
    HS_op = np.kron(H2, H2)    # 4x4 acts on s register

    # Full-space HS: I_out ⊗ HS  (little-endian: s is lower qubits within
    # the (s, out) block, after data qubit)
    HS_sout = np.kron(np.eye(N), HS_op)  # dim 4N x 4N (little-endian in (s, out))

    # Full-space data-qubit rotation R_data:
    # R_data acts on the data qubit, MULTIPLEXED on (d, m).
    # After O_c^dag, the (s, out) register is in the (d, m) enumeration
    # (because O_c^dag = permutation from (sc, j) back to (d, m)).
    # So we apply R_data to the data qubit CONTROLLED on the (s, out)
    # register interpreted as `dm`. For each dm in 0..4N-1:
    #   - if dm corresponds to an in-range pair with value index k
    #     (dm gives us (d, m); look up value_index in `pairs`):
    #       alpha = A[value_index] / ||A||_max
    #   - else alpha = 0.
    # We build R_data as a block-diagonal on (data, sout).

    R_data_full = np.zeros((dim, dim), dtype=complex)
    # Basis index: full = data + 2 * (s + S_pad * out) = data + 2 * sout
    for dm in range(dim_sout):
        # Recover (d, m) from flat index dm = d + D_pad*m
        m_ = dm // D_pad
        d_ = dm % D_pad
        # Find corresponding pair (list is ordered by d, m in same way)
        P = None
        for cand in pairs:
            if cand["d"] == d_ and cand["m"] == m_:
                P = cand
                break
        if P is not None and P["in_range"]:
            alpha = Avec[P["value_index"]] / Amax
        else:
            alpha = 0.0
        beta = np.sqrt(max(0.0, 1.0 - alpha * alpha))
        R22 = np.array([[alpha, -1j * beta],
                        [-1j * beta, alpha]], dtype=complex)
        # Little-endian: full index = data + 2*sout
        base = 2 * dm
        R_data_full[base, base] = R22[0, 0]
        R_data_full[base, base + 1] = R22[0, 1]
        R_data_full[base + 1, base] = R22[1, 0]
        R_data_full[base + 1, base + 1] = R22[1, 1]

    # Embed HS, O_c, O_r as full-space operators (tensor with I_data)
    def embed_sout(op_sout):
        # Little-endian: full_op = op_sout (acting on qubits 1..n_total-1)
        # tensored with I on data qubit (qubit 0).
        # full_op = op_sout ⊗ I_data  (with data as LSB)
        return np.kron(op_sout, np.eye(2 ** n_data))

    HS_full = embed_sout(HS_sout)
    O_c_full = embed_sout(O_c_sout)
    O_r_full = embed_sout(O_r_sout)

    O_c_dag_full = O_c_full.conj().T

    # U = HS_dag . O_r . R_data . O_c_dag . HS
    # (HS = HS_dag because it's a real symmetric H⊗H)
    U = HS_full @ O_r_full @ R_data_full @ O_c_dag_full @ HS_full

    residual = float(np.max(np.abs(U.conj().T @ U - np.eye(dim))))
    is_unitary = residual < 1e-9

    # Extract top-left N x N block via basis indices
    # <data=0, s=0, out=i| U |data=0, s=0, out=j>
    def idx(data, s, out):
        # little-endian: data (LSB), then s, then out
        return data + (s << n_data) + (out << (n_data + n_s))

    subnorm = S_pad * Amax
    A_hat = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            A_hat[i, j] = U[idx(0, 0, i), idx(0, 0, j)]

    err = float(np.max(np.abs(A_hat - A / subnorm)))
    result = {
        "N": N,
        "S_pad": S_pad,
        "D_pad": D_pad,
        "M": M,
        "n_flag_qubits_base_scheme": 1 + int(np.log2(S_pad)),
        "n_flag_qubits_gilyen": 3 + int(np.log2(N)),
        "n_total_qubits": n_total,
        "subnormalisation_alpha": subnorm,
        "block_encoding_max_error": err,
        "is_unitary": bool(is_unitary),
        "unitary_residual": residual,
        "A": A.tolist(),
        "A_over_alpha": (A / subnorm).tolist(),
        "A_hat_recovered_real": A_hat.real.tolist(),
        "A_hat_recovered_imag": A_hat.imag.tolist(),
    }
    return U, result


# -----------------------------------------------------------------------------
# Qiskit statevector reverification
# -----------------------------------------------------------------------------

def verify_via_qiskit(U, N, S_pad):
    n_data = 1
    n_s = int(np.log2(S_pad))
    n_out = int(np.log2(N))
    n_total = n_data + n_s + n_out
    out_shift = n_data + n_s

    A_hat = np.zeros((N, N), dtype=complex)
    for j in range(N):
        init = np.zeros(2 ** n_total, dtype=complex)
        init[j << out_shift] = 1.0
        qc = QuantumCircuit(n_total)
        qc.append(UnitaryGate(U, label="U_BE"), list(range(n_total)))
        sv = Statevector(init).evolve(qc)
        arr = sv.data
        for i in range(N):
            A_hat[i, j] = arr[i << out_shift]
    return A_hat


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    outdir = Path(__file__).resolve().parents[1] / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    all_results = []
    for N in (4, 8, 16):
        rng = np.random.default_rng(seed=N)
        main_diag = rng.uniform(-1.0, 1.0, size=N)
        off_diag = rng.uniform(-1.0, 1.0, size=N - 1)
        A = tridiagonal_matrix(main_diag, off_diag)

        U, result = build_block_encoding(A)
        subnorm = result["subnormalisation_alpha"]

        # Qiskit re-verification
        try:
            A_hat_qk = verify_via_qiskit(U, N=N, S_pad=result["S_pad"])
            qk_err = float(np.max(np.abs(A_hat_qk - A / subnorm)))
            result["qiskit_check_error"] = qk_err
            result["qiskit_check_ok"] = qk_err < 1e-9
        except Exception as e:
            result["qiskit_check_error"] = None
            result["qiskit_check_ok"] = False
            result["qiskit_exception"] = str(e)

        print(f"=== N = {N} ===")
        print(f"  padded (S, D, M) = ({result['S_pad']}, {result['D_pad']}, {result['M']})")
        print(f"  flag qubits (this paper base):  1 + log2(S_pad) = {result['n_flag_qubits_base_scheme']}")
        print(f"  flag qubits (Gilyén et al.):    3 + log2(N)     = {result['n_flag_qubits_gilyen']}")
        print(f"  total qubits: {result['n_total_qubits']}")
        print(f"  subnormalisation alpha = S*||A||max = {subnorm:.6f}")
        print(f"  U unitary residual:              {result['unitary_residual']:.2e}")
        print(f"  block-encoding max err (numpy):  {result['block_encoding_max_error']:.2e}")
        print(f"  qiskit statevector check err:    {result.get('qiskit_check_error')}")
        print()

        np.save(outdir / f"U_N{N}.npy", U)
        all_results.append(result)

    # Cost-only verification for larger N
    for N in (32, 64, 128, 256, 1024, 4096):
        S_pad = 4
        base = 1 + int(np.log2(S_pad))
        gil = 3 + int(np.log2(N))
        all_results.append({"N": N, "cost_only": True, "S_pad": S_pad,
                            "n_flag_qubits_base_scheme": base,
                            "n_flag_qubits_gilyen": gil})

    # Save JSON summary
    with open(outdir / "block_encoding_results.json", "w") as f:
        json.dump(all_results, f, indent=2, default=float)

    print("=" * 72)
    print("REPRODUCTION OF PAPER SEC 3.3 FLAG-QUBIT COST CLAIM (tridiagonal)")
    print("=" * 72)
    print(f"{'N':>5}  {'base scheme (this paper)':>25}  {'Gilyén et al.':>15}  {'savings':>10}")
    for r in all_results:
        N = r["N"]
        b = r["n_flag_qubits_base_scheme"]
        g = r["n_flag_qubits_gilyen"]
        print(f"{N:>5}  {b:>25d}  {g:>15d}  {g - b:>+10d}")
    print()
    print("Paper claim (Sec 3.3): base scheme has 1 + log2(S) = 3 flag qubits,")
    print("independent of N; Gilyén et al. scheme has 3 + log2(N) flag qubits.")
    print("(The full/PREP-augmented scheme adds a `del` flag => 4 total.)")
    return all_results


if __name__ == "__main__":
    main()
