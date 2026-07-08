"""
Independent replication of key numerical experiment in
Deller et al. 2022, arXiv:2204.00340
"Quantum approximate optimization algorithm for qudit systems"

Reproduces (in a small-but-faithful setting):
  - Qutrit (d=3) QAOA for max-k-graph-coloring (k=3) on an N=6 graph
    with a penalty term for coloring constraint violations.
  - Compare against an equivalent qubit-QAOA encoding of the same
    max-3-coloring problem (2 qubits per node, penalty for the
    invalid |11> = "color 3" state) at the SAME depth p.
  - Report:
       * # basis states: qudit d^N=3^6=729  vs  qubit 2^(2N)=2^12=4096
       * Optimality gap  (E_qaoa - E_min)  as a function of p
       * Ground-state probability sum for the ground-state manifold
  - Central claim of the paper: qudit encoding is more resource-efficient
    (smaller Hilbert space) and reaches comparable/better approximation
    ratio at low p.

Pure numpy state-vector simulator, no external QC framework required.
"""

import json
import sys
import time

# force line-buffered stdout so we see progress
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass
import numpy as np
from numpy.linalg import eigh
import scipy.optimize as opt

RNG = np.random.default_rng(42)

# ------------------------------------------------------------------
# Problem definition: N=6 nodes, k=3 colors, an explicit small graph
# ------------------------------------------------------------------
N = 6
K = 3  # colors

# A moderately connected N=6 graph that is 3-colorable (analog of what
# the paper uses; picked so it has multiple valid 3-colorings).
# Edges as undirected pairs (i,j) with i<j.
EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)]

LAMBDA = 20.0   # penalty prefactor per paper (Sec IV, lambda=20)


# ------------------------------------------------------------------
# Utility: enumerate all classical colorings, compute cost
# ------------------------------------------------------------------
def classical_cost(coloring, edges=EDGES, lam=LAMBDA):
    """Constraint-violation penalty only (pure max-k-coloring)."""
    viol = sum(1 for (i, j) in edges if coloring[i] == coloring[j])
    return lam * viol

def all_colorings(n=N, k=K):
    out = []
    for idx in range(k ** n):
        c = []
        x = idx
        for _ in range(n):
            c.append(x % k)
            x //= k
        out.append(tuple(c))
    return out

def exact_ground(edges=EDGES, n=N, k=K, lam=LAMBDA):
    best = None
    best_states = []
    for c in all_colorings(n, k):
        e = classical_cost(c, edges, lam)
        if best is None or e < best:
            best = e
            best_states = [c]
        elif e == best:
            best_states.append(c)
    return best, best_states


# ------------------------------------------------------------------
# QUDIT (d=3) QAOA — pure numpy state vector on 3^N space
# ------------------------------------------------------------------
D = 3
DIM_QUDIT = D ** N   # 729

def basis_index_qudit(coloring):
    """Map coloring tuple -> flat basis index in 3^N Hilbert space.
    Convention: qudit 0 is least significant."""
    idx = 0
    for i, c in enumerate(coloring):
        idx += c * (D ** i)
    return idx

# Precompute diagonal of cost Hamiltonian H_C for qutrit encoding
def build_cost_diag_qudit():
    diag = np.zeros(DIM_QUDIT, dtype=np.float64)
    for c in all_colorings(N, K):
        diag[basis_index_qudit(c)] = classical_cost(c, EDGES, LAMBDA)
    return diag

# Mixer for qudits: generalized-X on each qudit summed.
# Generalized X (shift): X|z> = |(z+1) mod d>
# We build the sum-of-X_j matrix as a sparse-friendly operator.
# For d=3 N=6 dim=729, dense 729x729 is fine.
def build_mixer_qudit():
    # single-qudit X (shift by 1)
    X = np.zeros((D, D), dtype=np.complex128)
    for z in range(D):
        X[(z + 1) % D, z] = 1.0
    # Hermitian mixer: (X + X^dag) so it can be exponentiated with a real angle.
    Xh = X + X.conj().T
    # Sum_j I x ... x Xh x ... x I
    M = np.zeros((DIM_QUDIT, DIM_QUDIT), dtype=np.complex128)
    for j in range(N):
        op = np.array([[1.0]], dtype=np.complex128)
        for k in range(N):
            if k == j:
                op = np.kron(Xh, op)
            else:
                op = np.kron(np.eye(D, dtype=np.complex128), op)
        M += op
    return M

# Precompute mixer eigendecomposition for fast exp(-i beta M)
def prep_mixer_qudit():
    M = build_mixer_qudit()
    w, V = eigh(M)  # Hermitian
    return w, V

COST_DIAG_QUDIT = build_cost_diag_qudit()
MIX_W_QUDIT, MIX_V_QUDIT = prep_mixer_qudit()

def qaoa_state_qudit(gammas, betas):
    """Apply p layers of QAOA on qutrit init state (equal superposition)."""
    dim = DIM_QUDIT
    psi = np.ones(dim, dtype=np.complex128) / np.sqrt(dim)
    for g, b in zip(gammas, betas):
        # exp(-i g H_C) diagonal
        psi = np.exp(-1j * g * COST_DIAG_QUDIT) * psi
        # exp(-i b M) via eigendecomposition
        # = V diag(exp(-i b w)) V^dag
        psi = MIX_V_QUDIT.conj().T @ psi
        psi = np.exp(-1j * b * MIX_W_QUDIT) * psi
        psi = MIX_V_QUDIT @ psi
    return psi

def cost_expectation_qudit(params):
    p = len(params) // 2
    gammas = params[:p]
    betas = params[p:]
    psi = qaoa_state_qudit(gammas, betas)
    return float(np.real(np.sum(np.abs(psi) ** 2 * COST_DIAG_QUDIT)))


# ------------------------------------------------------------------
# QUBIT-encoded QAOA for the SAME problem
# Encoding: 2 qubits per node encode color 0,1,2 (binary 00,01,10);
# the invalid 11 pattern is penalized by a large "invalid" penalty M_inv.
# Total qubits: 2N = 12  ->  2^12 = 4096 states.
# ------------------------------------------------------------------
NQ = 2 * N
DIM_QUBIT = 2 ** NQ
INV_PENALTY = 50.0  # penalize the invalid |11> per-node "color 3"

def qubit_state_to_coloring(bits):
    """bits: length-NQ tuple of {0,1}. Qubits (2i,2i+1) encode node i color.
    Convention: color = 2*bit_high + bit_low. 3 = invalid."""
    coloring = []
    invalid = False
    for i in range(N):
        b0 = bits[2 * i]
        b1 = bits[2 * i + 1]
        c = 2 * b1 + b0
        if c == 3:
            invalid = True
            coloring.append(-1)
        else:
            coloring.append(c)
    return tuple(coloring), invalid

def build_cost_diag_qubit():
    diag = np.zeros(DIM_QUBIT, dtype=np.float64)
    # For each computational basis index, decompose to bits, compute cost.
    for idx in range(DIM_QUBIT):
        bits = [(idx >> b) & 1 for b in range(NQ)]
        col, inv = qubit_state_to_coloring(bits)
        if inv:
            # count invalid nodes and penalize
            n_inv = sum(1 for c in col if c == -1)
            diag[idx] = INV_PENALTY * n_inv + LAMBDA * sum(
                1 for (i, j) in EDGES if col[i] != -1 and col[j] != -1 and col[i] == col[j]
            )
        else:
            diag[idx] = classical_cost(col)
    return diag

def prep_mixer_qubit():
    """Standard qubit mixer: sum_j X_j. Use eigendecomposition-free approach:
    apply per-qubit RX rotations, which is exact for the transverse-field mixer.
    exp(-i beta sum X_j) factorizes as product of exp(-i beta X_j).
    We'll implement this by reshape/tensor operations."""
    # Nothing to prep; we'll apply per-qubit rotations in state_qubit.
    return None

COST_DIAG_QUBIT = build_cost_diag_qubit()
prep_mixer_qubit()

def apply_rx_all(psi, beta):
    """Apply exp(-i beta X) to every qubit. Factorized: per-qubit 2x2 gate."""
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    gate = np.array([[c, s], [s, c]], dtype=np.complex128)
    psi = psi.reshape([2] * NQ)
    for q in range(NQ):
        # move axis q to front, apply gate, move back
        psi = np.moveaxis(psi, q, 0)
        shape = psi.shape
        psi = gate @ psi.reshape(2, -1)
        psi = psi.reshape(shape)
        psi = np.moveaxis(psi, 0, q)
    return psi.reshape(DIM_QUBIT)

def qaoa_state_qubit(gammas, betas):
    psi = np.ones(DIM_QUBIT, dtype=np.complex128) / np.sqrt(DIM_QUBIT)
    for g, b in zip(gammas, betas):
        psi = np.exp(-1j * g * COST_DIAG_QUBIT) * psi
        psi = apply_rx_all(psi, b)
    return psi

def cost_expectation_qubit(params):
    p = len(params) // 2
    gammas = params[:p]
    betas = params[p:]
    psi = qaoa_state_qubit(gammas, betas)
    return float(np.real(np.sum(np.abs(psi) ** 2 * COST_DIAG_QUBIT)))


# ------------------------------------------------------------------
# Optimization loop
# ------------------------------------------------------------------
def optimize_qaoa(cost_fn, p, n_restarts=20, seed=0):
    rng = np.random.default_rng(seed)
    best = None
    best_x = None
    all_vals = []
    for r in range(n_restarts):
        x0 = np.concatenate([
            rng.uniform(0, 2 * np.pi, p),   # gammas
            rng.uniform(0, np.pi, p),        # betas
        ])
        res = opt.minimize(cost_fn, x0, method="L-BFGS-B",
                           options={"maxiter": 200, "ftol": 1e-8})
        all_vals.append(res.fun)
        if best is None or res.fun < best:
            best = res.fun
            best_x = res.x
    return best, best_x, all_vals


# ------------------------------------------------------------------
# Main: run both encodings for p in {1,2,3,4,5} and report
# ------------------------------------------------------------------
def main():
    t0 = time.time()
    print("[INIT] starting; dim_qudit=%d dim_qubit=%d" % (DIM_QUDIT, DIM_QUBIT), flush=True)

    # 1. Exact ground state
    E_min, gs_states = exact_ground()
    print(f"[EXACT] ground E = {E_min:.4f}  |gs|={len(gs_states)} valid colorings", flush=True)

    ps = [1, 2, 3, 4, 5]
    results = {"paper": "arXiv:2204.00340",
               "N": N, "K": K, "edges": EDGES, "lambda": LAMBDA,
               "E_min": E_min, "n_gs": len(gs_states),
               "dim_qudit": DIM_QUDIT, "dim_qubit": DIM_QUBIT,
               "runs": []}

    # ground-state index set for probability accounting
    gs_idx_qudit = set(basis_index_qudit(c) for c in gs_states)

    def gs_prob_qudit(psi):
        return float(sum(abs(psi[i]) ** 2 for i in gs_idx_qudit))

    def gs_prob_qubit(psi):
        # sum over all bit-strings that decode to a valid ground-state coloring
        total = 0.0
        gs_col_set = set(gs_states)
        for idx in range(DIM_QUBIT):
            bits = [(idx >> b) & 1 for b in range(NQ)]
            col, inv = qubit_state_to_coloring(bits)
            if not inv and col in gs_col_set:
                total += abs(psi[idx]) ** 2
        return float(total)

    N_RESTARTS = 15
    for p in ps:
        print(f"\n=== p={p} ===", flush=True)
        # QUDIT
        t = time.time()
        best_qd, x_qd, all_qd = optimize_qaoa(cost_expectation_qudit, p, n_restarts=N_RESTARTS, seed=100 + p)
        psi_qd = qaoa_state_qudit(x_qd[:p], x_qd[p:])
        gs_p_qd = gs_prob_qudit(psi_qd)
        gap_qd = best_qd - E_min
        t_qd = time.time() - t
        print(f"  qudit (d=3):  <H_C>={best_qd:.4f}  gap={gap_qd:.4f}  P(gs)={gs_p_qd:.4f}  t={t_qd:.1f}s", flush=True)

        # QUBIT
        t = time.time()
        best_qb, x_qb, all_qb = optimize_qaoa(cost_expectation_qubit, p, n_restarts=N_RESTARTS, seed=200 + p)
        psi_qb = qaoa_state_qubit(x_qb[:p], x_qb[p:])
        gs_p_qb = gs_prob_qubit(psi_qb)
        gap_qb = best_qb - E_min
        t_qb = time.time() - t
        print(f"  qubit (2q/n): <H_C>={best_qb:.4f}  gap={gap_qb:.4f}  P(gs)={gs_p_qb:.4f}  t={t_qb:.1f}s", flush=True)

        results["runs"].append({
            "p": p,
            "qudit": {"best_cost": best_qd, "gap": gap_qd, "P_gs": gs_p_qd, "time_s": t_qd,
                      "all_restarts": all_qd, "best_params": x_qd.tolist()},
            "qubit": {"best_cost": best_qb, "gap": gap_qb, "P_gs": gs_p_qb, "time_s": t_qb,
                      "all_restarts": all_qb, "best_params": x_qb.tolist()},
        })

    results["total_wall_s"] = time.time() - t0

    with open("../results/replication_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nTotal wall: {results['total_wall_s']:.1f}s -> results/replication_results.json", flush=True)


if __name__ == "__main__":
    main()
