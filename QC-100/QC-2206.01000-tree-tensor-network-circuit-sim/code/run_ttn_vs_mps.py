#!/usr/bin/env python
"""
QC-100 replication: arXiv:2206.01000 (Seitz, Medina, Cruz, Huang, Mendl 2023)
"Simulating quantum circuits using tree tensor networks"

Replication scope (per QC_WAVE_BRIEF): show that a bounded-bond-dim tree tensor
network (TTN) representation of a quantum-circuit statevector approximates the
exact statevector to controllable error as bond dimension chi grows, and does
comparably to or better than MPS at the same chi for a circuit family the paper
targets (tree-clusterable circuits, Sect. 4.1 / Fig. 12).

Method
------
1. Build a "tree-like" circuit on N=12 qubits (three 4-qubit clusters). Inside
   each cluster, apply a dense sequence of random 2-qubit haar unitaries between
   every pair (this is intra-cluster entanglement). Between clusters, apply only
   a few (kG=2 in paper terminology) cross-cluster CNOTs that go through a single
   central "root" qubit per cluster.
2. Build the "hard for MPS" circuit: same qubits but with all-to-all long-range
   random 2-qubit gates (models the QFT-like / lattice case the paper says MPS
   handles badly).
3. Simulate exactly via quimb.tensor.CircuitDense (statevector).
4. Simulate via quimb.tensor.CircuitMPS at chi in {2, 4, 8, 16, 32}. Compute
   fidelity F = |<exact|approx>|^2.
5. For TTN: build a balanced-binary tree tensor factorization of the exact
   statevector. Recursively split |psi> at a chosen partition, take SVD, keep
   at most chi singular values on the middle bond. Do this recursively down
   the tree. Compute fidelity of the reconstructed state to exact.
6. Report fidelity(chi) curves for MPS vs TTN on both circuits.

This isolates the *representational* claim (TTN vs MPS at fixed chi on tree-
structured entanglement), which is the paper's headline advantage. Full runtime
comparisons for O(30-100) qubit dry-runs are out of scope for a small
statevector-verified reproduction, but we replicate the qualitative signature:
TTN >= MPS in fidelity at same chi on tree-clusterable circuits.
"""
import json
import time
import numpy as np
import quimb.tensor as qtn
import quimb as qu
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "report" / "evidence"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 20260704
N = 12  # 3 clusters of 4 qubits
CLUSTER_SIZE = 4
NUM_CLUSTERS = N // CLUSTER_SIZE
CHIS = [2, 4, 8, 16, 32]

rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------- circuits ---
def random_haar_2q():
    """Sample a Haar-random 2q unitary via QR on a random complex Gaussian."""
    A = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    Q, R = np.linalg.qr(A)
    d = np.diag(R)
    ph = d / np.abs(d)
    return Q * ph


def apply_2q_gate(circ, U, i, j):
    """Apply arbitrary 2q gate U to qubits (i,j) via quimb.Circuit.apply_gate."""
    circ.apply_gate_raw(U, (i, j), gate_round=None)


def build_tree_like_circuit(N=12, cluster_size=4, seed=SEED):
    """Fig 12-style: 3 clusters of 4 qubits, dense intra-cluster random gates,
    few inter-cluster gates threading through cluster roots (qubits 0,4,8)."""
    local = np.random.default_rng(seed)
    circ = qtn.Circuit(N=N)
    # Init: apply a random 1q gate on each qubit for a non-trivial starting state
    for q in range(N):
        # Random rotation
        theta, phi, lam = local.uniform(0, 2*np.pi, size=3)
        circ.apply_gate('U3', theta, phi, lam, q)

    def haar():
        A = local.standard_normal((4, 4)) + 1j * local.standard_normal((4, 4))
        Q, R = np.linalg.qr(A)
        d = np.diag(R)
        return Q * (d / np.abs(d))

    # Intra-cluster dense entanglement (depth 3 sweeps of all pairs)
    for _sweep in range(3):
        for c in range(NUM_CLUSTERS):
            base = c * cluster_size
            qubits = list(range(base, base + cluster_size))
            for a_idx in range(len(qubits)):
                for b_idx in range(a_idx + 1, len(qubits)):
                    U = haar()
                    circ.apply_gate_raw(U, (qubits[a_idx], qubits[b_idx]))
    # Inter-cluster: only via cluster roots (qubits 0, 4, 8)
    roots = [c * cluster_size for c in range(NUM_CLUSTERS)]
    for _ in range(2):
        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                U = haar()
                circ.apply_gate_raw(U, (roots[i], roots[j]))
    return circ


def build_hard_circuit(N=12, seed=SEED + 1):
    """All-to-all random 2q gates, no cluster structure. Models the case
    where entanglement doesn't match a tree (paper's 'lattice / QFT' regime)."""
    local = np.random.default_rng(seed)
    circ = qtn.Circuit(N=N)
    for q in range(N):
        theta, phi, lam = local.uniform(0, 2*np.pi, size=3)
        circ.apply_gate('U3', theta, phi, lam, q)

    def haar():
        A = local.standard_normal((4, 4)) + 1j * local.standard_normal((4, 4))
        Q, R = np.linalg.qr(A)
        d = np.diag(R)
        return Q * (d / np.abs(d))

    # 2 rounds of all-to-all random 2q gates
    for _ in range(2):
        pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
        local.shuffle(pairs)
        for (i, j) in pairs:
            U = haar()
            circ.apply_gate_raw(U, (i, j))
    return circ


# ---------------------------------------------------------------- sim helpers ---
def exact_statevector_from_circuit(circ):
    """Contract quimb circuit to a full statevector via CircuitDense-equivalent
    contraction (small N)."""
    psi = circ.to_dense()
    # to_dense returns a numpy array shape (2**N, 1) usually
    arr = np.asarray(psi).reshape(-1)
    # Normalize (should already be unit norm but be safe against numerical drift)
    arr = arr / np.linalg.norm(arr)
    return arr


def mps_fidelity_at_chi(gates_source_fn, chi, seed):
    """Simulate the same circuit via CircuitMPS(chi=chi) and compute fidelity
    to the exact statevector."""
    # Rebuild circuit with deterministic seed so it matches the exact sim
    circ_exact = gates_source_fn(seed=seed)
    psi_exact = exact_statevector_from_circuit(circ_exact)

    circ_mps = gates_source_fn(seed=seed, circuit_cls=qtn.CircuitMPS,
                               circuit_opts={'max_bond': chi, 'cutoff': 0.0})
    psi_mps_tn = circ_mps.psi  # MatrixProductState
    # Convert MPS to dense statevector
    dense = psi_mps_tn.to_dense()
    v = np.asarray(dense).reshape(-1)
    # Normalize
    n = np.linalg.norm(v)
    if n < 1e-30:
        return 0.0
    v = v / n
    F = float(np.abs(np.vdot(psi_exact, v))**2)
    return F


def build_circuit_generic(seed, circuit_cls=qtn.Circuit, circuit_opts=None,
                          kind='tree', N=N, cluster_size=CLUSTER_SIZE):
    """Unified builder so exact and MPS runs execute the SAME gate sequence."""
    local = np.random.default_rng(seed)
    opts = dict(circuit_opts or {})
    circ = circuit_cls(N=N, **opts)

    # Init 1q gates
    init_angles = [local.uniform(0, 2*np.pi, size=3) for _ in range(N)]
    for q, (theta, phi, lam) in enumerate(init_angles):
        circ.apply_gate('U3', theta, phi, lam, q)

    def haar():
        A = local.standard_normal((4, 4)) + 1j * local.standard_normal((4, 4))
        Q, R = np.linalg.qr(A)
        d = np.diag(R)
        return Q * (d / np.abs(d))

    if kind == 'tree':
        # Intra-cluster dense
        for _sweep in range(3):
            for c in range(N // cluster_size):
                base = c * cluster_size
                qubits = list(range(base, base + cluster_size))
                for a_idx in range(len(qubits)):
                    for b_idx in range(a_idx + 1, len(qubits)):
                        U = haar()
                        circ.apply_gate_raw(U, (qubits[a_idx], qubits[b_idx]))
        # Inter-cluster via roots
        roots = [c * cluster_size for c in range(N // cluster_size)]
        for _ in range(2):
            for i in range(len(roots)):
                for j in range(i + 1, len(roots)):
                    U = haar()
                    circ.apply_gate_raw(U, (roots[i], roots[j]))
    elif kind == 'hard':
        for _ in range(2):
            pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
            local.shuffle(pairs)
            for (i, j) in pairs:
                U = haar()
                circ.apply_gate_raw(U, (i, j))
    else:
        raise ValueError(kind)
    return circ


# ---------------------------------------------------------------- TTN compression ---
def ttn_compress_fidelity(psi_exact, N, chi, tree='balanced'):
    """Given the exact statevector, form a balanced-binary tree tensor network
    representation with max bond dimension chi at every internal edge, and
    compute the fidelity of the reconstructed state to psi_exact.

    We do this by recursive SVD-with-truncation on hierarchical bipartitions:
        Level 1 split: qubits {0..N/2-1} | {N/2..N-1}
        Level 2 splits: each half in {0..N/4-1}|{N/4..N/2-1} etc.
    This is the standard 'balanced binary TTN' scheme.
    """
    assert (N & (N - 1) == 0) or True  # not strict pow2 required for our tree
    v = psi_exact.reshape([2] * N)

    def recursive_ttn_reconstruct(vec, qubit_indices, chi):
        """Return a reconstructed tensor of shape (2,2,...,2) approximating vec
        via truncated hierarchical SVD."""
        n = len(qubit_indices)
        if n <= 2:
            return vec  # leaf: keep exact
        # Split into two halves
        half = n // 2
        left_dims = 2 ** half
        right_dims = 2 ** (n - half)
        M = vec.reshape(left_dims, right_dims)
        U, S, Vh = np.linalg.svd(M, full_matrices=False)
        # Truncate to chi
        k = min(chi, len(S))
        U = U[:, :k]
        S = S[:k]
        Vh = Vh[:k, :]
        # Recurse: reshape U into (2,)*half x (k,), Vh into (k,) x (2,)*(n-half)
        left_tensor = U.reshape([2] * half + [k])
        right_tensor = Vh.reshape([k] + [2] * (n - half))
        # Move virtual bond to end for right recursion
        # We recurse on the physical-index tensor with the virtual index as an
        # extra 'environment' dim. For simplicity, contract S into left, and
        # recurse-compress each half by treating virtual bond as a fixed spectator.

        # Contract S into left:
        left_tensor = left_tensor * S  # broadcast: last axis is k, S has shape (k,)

        # Recurse on left half:
        # left_tensor shape (2,)*half + (k,); flatten physical -> (2**half, k)
        left_recon = recurse_on_side(left_tensor, half, chi, side='left')
        right_recon = recurse_on_side(right_tensor, n - half, chi, side='right')
        # Contract virtual bond
        # left_recon shape (2,)*half + (k,) ; right_recon shape (k,) + (2,)*(n-half)
        L = left_recon.reshape(2 ** half, k)
        R = right_recon.reshape(k, 2 ** (n - half))
        out = L @ R
        return out.reshape([2] * n)

    def recurse_on_side(tensor, n_phys, chi, side):
        """Compress a subtree that has n_phys physical indices and one virtual
        bond (last axis if left, first axis if right)."""
        if n_phys <= 2:
            return tensor
        if side == 'left':
            # tensor shape (2,)*n_phys + (k,)
            k = tensor.shape[-1]
            half = n_phys // 2
            # Move virtual to the right end already
            M = tensor.reshape(2 ** half, 2 ** (n_phys - half) * k)
            U, S, Vh = np.linalg.svd(M, full_matrices=False)
            kk = min(chi, len(S))
            U = U[:, :kk]; S = S[:kk]; Vh = Vh[:kk, :]
            left_t = (U * S).reshape([2] * half + [kk])
            right_t = Vh.reshape([kk] + [2] * (n_phys - half) + [k])
            # Recurse on children
            left_c = recurse_on_side(left_t, half, chi, side='left')
            # right_t has virtual bonds on BOTH ends (kk on left, k on right).
            # Recurse: further split its physical block
            right_c = recurse_two_sided(right_t, n_phys - half, chi)
            # Contract kk bond
            Lflat = left_c.reshape(2 ** half, kk)
            Rflat = right_c.reshape(kk, 2 ** (n_phys - half) * k)
            out = (Lflat @ Rflat).reshape([2] * n_phys + [k])
            return out
        else:
            # side == 'right'; tensor shape (k,) + (2,)*n_phys
            k = tensor.shape[0]
            half = n_phys // 2
            M = tensor.reshape(k * 2 ** half, 2 ** (n_phys - half))
            U, S, Vh = np.linalg.svd(M, full_matrices=False)
            kk = min(chi, len(S))
            U = U[:, :kk]; S = S[:kk]; Vh = Vh[:kk, :]
            left_t = (U * S).reshape([k] + [2] * half + [kk])
            right_t = Vh.reshape([kk] + [2] * (n_phys - half))
            left_c = recurse_two_sided(left_t, half, chi)
            right_c = recurse_on_side(right_t, n_phys - half, chi, side='right')
            Lflat = left_c.reshape(k * 2 ** half, kk)
            Rflat = right_c.reshape(kk, 2 ** (n_phys - half))
            out = (Lflat @ Rflat).reshape([k] + [2] * n_phys)
            return out

    def recurse_two_sided(tensor, n_phys, chi):
        """Subtree with virtual bonds on BOTH ends."""
        if n_phys <= 2:
            return tensor
        # shape (k1,) + (2,)*n_phys + (k2,)
        k1 = tensor.shape[0]
        k2 = tensor.shape[-1]
        half = n_phys // 2
        M = tensor.reshape(k1 * 2 ** half, 2 ** (n_phys - half) * k2)
        U, S, Vh = np.linalg.svd(M, full_matrices=False)
        kk = min(chi, len(S))
        U = U[:, :kk]; S = S[:kk]; Vh = Vh[:kk, :]
        left_t = (U * S).reshape([k1] + [2] * half + [kk])
        right_t = Vh.reshape([kk] + [2] * (n_phys - half) + [k2])
        left_c = recurse_two_sided(left_t, half, chi)
        right_c = recurse_two_sided(right_t, n_phys - half, chi)
        Lflat = left_c.reshape(k1 * 2 ** half, kk)
        Rflat = right_c.reshape(kk, 2 ** (n_phys - half) * k2)
        out = (Lflat @ Rflat).reshape([k1] + [2] * n_phys + [k2])
        return out

    recon = recursive_ttn_reconstruct(v, list(range(N)), chi)
    recon_flat = recon.reshape(-1)
    # Normalize
    n = np.linalg.norm(recon_flat)
    if n < 1e-30:
        return 0.0
    recon_flat = recon_flat / n
    F = float(np.abs(np.vdot(psi_exact, recon_flat))**2)
    return F


# ---------------------------------------------------------------- experiment ---
def run_experiment(kind, seed):
    print(f"\n=== Circuit kind={kind} seed={seed} N={N} ===")
    t0 = time.time()
    circ_exact = build_circuit_generic(seed=seed, kind=kind)
    psi_exact = exact_statevector_from_circuit(circ_exact)
    print(f"  exact statevector: shape={psi_exact.shape} norm={np.linalg.norm(psi_exact):.6f} "
          f"({time.time()-t0:.2f}s)")

    mps_results = {}
    ttn_results = {}
    for chi in CHIS:
        t = time.time()
        F_mps = mps_fidelity_at_chi(
            lambda seed=seed, circuit_cls=qtn.Circuit, circuit_opts=None:
                build_circuit_generic(seed=seed, circuit_cls=circuit_cls,
                                      circuit_opts=circuit_opts, kind=kind),
            chi=chi, seed=seed)
        dt_mps = time.time() - t
        t = time.time()
        F_ttn = ttn_compress_fidelity(psi_exact, N, chi)
        dt_ttn = time.time() - t
        mps_results[chi] = F_mps
        ttn_results[chi] = F_ttn
        print(f"  chi={chi:3d}  MPS F={F_mps:.6f} ({dt_mps:.2f}s)   "
              f"TTN F={F_ttn:.6f} ({dt_ttn:.2f}s)")
    return {'kind': kind, 'seed': seed, 'N': N,
            'mps': mps_results, 'ttn': ttn_results}


def main():
    all_results = {}
    for kind in ['tree', 'hard']:
        all_results[kind] = run_experiment(kind, SEED)

    out = RESULTS_DIR / "fidelity_vs_chi.json"
    with open(out, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nWrote {out}")

    # Compact CSV
    csv_path = RESULTS_DIR / "fidelity_vs_chi.csv"
    with open(csv_path, "w") as f:
        f.write("circuit_kind,chi,ansatz,fidelity\n")
        for kind, r in all_results.items():
            for chi, F in r['mps'].items():
                f.write(f"{kind},{chi},MPS,{F:.8f}\n")
            for chi, F in r['ttn'].items():
                f.write(f"{kind},{chi},TTN,{F:.8f}\n")
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
