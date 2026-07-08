"""
Independent replication of the CORE claim of Shaydulin et al. 2019
"Multistart Methods for Quantum Approximate Optimization" (arXiv:1905.08768)

FAST implementation: pure-numpy QAOA statevector evolution + expectation.
Cross-validated against Qiskit statevector for one random point below.

CLAIM UNDER TEST (headline / testable):
  For QAOA parameter optimization on small graphs, multistart (best-of-M
  random restarts) finds substantially better parameters (higher
  expectation of the problem Hamiltonian and higher approximation ratio)
  than a single-start local optimizer under an equal function-evaluation
  budget. Paper: Figs. 2 and 3, p=1,2,4, n=10-12 modularity clustering.

REPLICATION DESIGN:
  * Problem: MAX-CUT on a 3-regular graph, n=8 (fits in 256-D statevector).
    The paper's argument (many local optima → multistart helps) is
    problem-agnostic; MAX-CUT on random 3-regular graphs is the canonical
    QAOA benchmark and is explicitly referenced throughout the paper.
  * QAOA depth p = 1, 2, 4 (matches paper's three cases exactly).
  * Optimizer: COBYLA (paper tests COBYLA/BOBYQA/NEWUOA/NM/PRAXIS/SBPLX;
    COBYLA is one of the six and is the most widely used QAOA baseline).
  * Single-start:  1 random init, budget = 1000 fn evals (paper's number).
  * Multistart:    M random inits, EQUAL total budget shared (per-init
    budget = 1000/M) — the paper is stricter (APOSMM uses smart
    coordination), so multistart-as-random-restart is a WEAKER form of
    multistart than the paper's APOSMM; if it still wins that reproduces
    the qualitative claim.
  * 20 seeds per condition (paper: 10 seeds × 6 problems = 60 runs;
    we use 20 seeds × 1 problem = 20 runs, comparable statistical power
    for the size effect we're testing).

Success criterion for REPLICATED:
  Multistart median approx-ratio > single-start median approx-ratio by a
  clear margin for at least p=2 or p=4 (where the paper reports the
  largest gap; p=1 is 2D and easy so the gap is smallest there).
"""
import json
import os
import sys
import time
import numpy as np
import networkx as nx
from scipy.optimize import minimize

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "report",
    "evidence",
)
os.makedirs(RESULTS_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Problem
# ---------------------------------------------------------------------------
def build_graph(n=8, seed=42):
    return nx.random_regular_graph(3, n, seed=seed)


def brute_force_maxcut(G):
    n = G.number_of_nodes()
    edges = list(G.edges())
    best = 0
    for s in range(1 << n):
        c = 0
        for i, j in edges:
            if ((s >> i) & 1) != ((s >> j) & 1):
                c += 1
        if c > best:
            best = c
    return best


# ---------------------------------------------------------------------------
# Fast QAOA statevector kernel (pure numpy)
# ---------------------------------------------------------------------------
def make_maxcut_diag(G, n):
    """Diagonal of H_C = sum_{(i,j)} 0.5*(I - Z_i Z_j) in computational basis.
    Value at basis state |x> equals number of edges cut by bitstring x.
    Returns array of length 2^n (real).
    """
    diag = np.zeros(1 << n, dtype=np.float64)
    edges = list(G.edges())
    all_states = np.arange(1 << n, dtype=np.int64)
    for i, j in edges:
        bi = ((all_states >> i) & 1).astype(np.float64)
        bj = ((all_states >> j) & 1).astype(np.float64)
        diag += (bi != bj).astype(np.float64)
    return diag


def apply_rx_layer(state, beta, n):
    """Apply exp(-i * beta * X_q) = RX(2*beta) simultaneously on every qubit.
    For each qubit, RX(theta) = cos(theta/2) I - i sin(theta/2) X.
    Here theta = 2*beta so cos(theta/2)=cos(beta), sin(theta/2)=sin(beta).
    """
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    # apply to each qubit in turn
    dim = 1 << n
    for q in range(n):
        # reshape so that qubit q is a leading axis of size 2
        # standard trick: view state as shape (2**(n-1-q), 2, 2**q)
        shape = (1 << (n - 1 - q), 2, 1 << q)
        v = state.reshape(shape)
        a = v[:, 0, :].copy()
        b = v[:, 1, :].copy()
        v[:, 0, :] = c * a + s * b
        v[:, 1, :] = s * a + c * b
        state = v.reshape(dim)
    return state


def apply_cost_layer(state, gamma, cost_diag):
    """Apply exp(-i * gamma * H_C). H_C is diagonal so it's a phase multiply."""
    phases = np.exp(-1j * gamma * cost_diag)
    return state * phases


def qaoa_statevector(G, params, p, cost_diag, n):
    """Return the QAOA(p) statevector for given params on graph G."""
    gammas = params[:p]
    betas = params[p:]
    # start in |+>^n
    state = np.ones(1 << n, dtype=np.complex128) / np.sqrt(1 << n)
    for layer in range(p):
        state = apply_cost_layer(state, gammas[layer], cost_diag)
        state = apply_rx_layer(state, betas[layer], n)
    return state


def qaoa_expectation(G, params, p, cost_diag, n):
    """<psi(params)| H_C |psi(params)> where H_C is diagonal in comp basis."""
    state = qaoa_statevector(G, params, p, cost_diag, n)
    probs = (state.conj() * state).real
    return float(np.dot(probs, cost_diag))


# ---------------------------------------------------------------------------
# Cross-check against Qiskit for one point (paranoia)
# ---------------------------------------------------------------------------
def qiskit_expectation(G, params, p):
    """Cross-check reference using Qiskit's Statevector + SparsePauliOp.

    We build H_C = sum_{(i,j) in E} 0.5*(I - Z_i Z_j) exactly, and the QAOA
    cost unitary as exp(-i * gamma * H_C).  For a single edge (i,j):
        exp(-i * gamma * 0.5 * (I - Z_i Z_j))
          = exp(-i * gamma/2) * exp(+i * gamma/2 * Z_i Z_j)
          = exp(-i * gamma/2) * RZZ(-gamma)
    (global phase absorbed).  Total per-layer prefactor is exp(-i * gamma/2 * |E|).
    The MIXER uses exp(-i * beta * X_q) = RX(2*beta).
    """
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector, SparsePauliOp

    n = G.number_of_nodes()
    gammas = params[:p]
    betas = params[p:]
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for layer in range(p):
        g = gammas[layer]
        for (i, j) in G.edges():
            qc.rzz(-g, i, j)  # exp(+i g/2 Z_i Z_j)
        b = betas[layer]
        for q in range(n):
            qc.rx(2.0 * b, q)  # exp(-i b X)
    sv = Statevector.from_instruction(qc)
    # Build H_C in Qiskit (little-endian labels)
    pauli_list = []
    for i, j in G.edges():
        z = ["I"] * n
        z[i] = "Z"
        z[j] = "Z"
        pauli_list.append(("".join(z[::-1]), -0.5))
        pauli_list.append(("I" * n, 0.5))
    H_C = SparsePauliOp.from_list(pauli_list).simplify()
    return float(np.real(sv.expectation_value(H_C)))


# ---------------------------------------------------------------------------
# Optimization
# ---------------------------------------------------------------------------
class Oracle:
    def __init__(self, G, p, cost_diag, n):
        self.G = G
        self.p = p
        self.cost_diag = cost_diag
        self.n = n
        self.n_evals = 0
        self.best_value = -np.inf
        self.best_params = None

    def __call__(self, params):
        self.n_evals += 1
        v = qaoa_expectation(self.G, params, self.p, self.cost_diag, self.n)
        if v > self.best_value:
            self.best_value = v
            self.best_params = np.array(params)
        return -v  # scipy minimizes


def random_init(p, rng):
    gammas = rng.uniform(0.0, 2.0 * np.pi, size=p)
    betas = rng.uniform(0.0, np.pi, size=p)
    return np.concatenate([gammas, betas])


def single_start(G, p, cost_diag, n, seed, budget=1000):
    rng = np.random.default_rng(seed)
    obj = Oracle(G, p, cost_diag, n)
    x0 = random_init(p, rng)
    try:
        minimize(
            obj,
            x0,
            method="COBYLA",
            options={"maxiter": budget, "rhobeg": 0.5, "catol": 1e-4, "disp": False},
        )
    except Exception:
        pass
    return obj.best_value, obj.best_params, obj.n_evals


def multistart(G, p, cost_diag, n, seed, M, total_budget=1000):
    rng = np.random.default_rng(seed)
    per_run = max(1, total_budget // M)
    global_best = -np.inf
    global_best_params = None
    total_evals = 0
    for _ in range(M):
        if total_evals >= total_budget:
            break
        remaining = total_budget - total_evals
        this_budget = min(per_run, remaining)
        obj = Oracle(G, p, cost_diag, n)
        x0 = random_init(p, rng)
        try:
            minimize(
                obj,
                x0,
                method="COBYLA",
                options={"maxiter": this_budget, "rhobeg": 0.5, "catol": 1e-4, "disp": False},
            )
        except Exception:
            pass
        total_evals += obj.n_evals
        if obj.best_value > global_best:
            global_best = obj.best_value
            global_best_params = obj.best_params
    return global_best, global_best_params, total_evals


def main():
    t0 = time.time()
    n = 8
    graph_seed = 42
    G = build_graph(n=n, seed=graph_seed)
    print(f"Graph: n={n}, m={G.number_of_edges()}, 3-regular seed={graph_seed}")
    print(f"Edges: {list(G.edges())}")
    exact = brute_force_maxcut(G)
    print(f"Exact MAX-CUT = {exact}")

    cost_diag = make_maxcut_diag(G, n)
    print(f"cost_diag: min={cost_diag.min()}, max={cost_diag.max()} (should match MAX-CUT={exact})")
    assert cost_diag.max() == exact, "sanity check failed"

    # ---- cross-check numpy kernel against qiskit ----
    rng = np.random.default_rng(0)
    test_p = 2
    test_params = random_init(test_p, rng)
    v_np = qaoa_expectation(G, test_params, test_p, cost_diag, n)
    v_qk = qiskit_expectation(G, test_params, test_p)
    print(
        f"Cross-check p={test_p}: numpy={v_np:.10f}  qiskit={v_qk:.10f}  "
        f"|Δ|={abs(v_np-v_qk):.2e}"
    )
    assert abs(v_np - v_qk) < 1e-8, "numpy vs qiskit disagreement!"

    results = {
        "graph": {
            "n_vertices": n,
            "n_edges": G.number_of_edges(),
            "graph_seed": graph_seed,
            "edges": [list(e) for e in G.edges()],
            "exact_maxcut": int(exact),
        },
        "cross_check": {
            "test_p": int(test_p),
            "test_params": test_params.tolist(),
            "numpy_expectation": float(v_np),
            "qiskit_expectation": float(v_qk),
            "abs_diff": float(abs(v_np - v_qk)),
        },
        "conditions": {},
    }

    n_seeds = 20
    budget = 1000
    ms_values = [5, 10, 20]

    for p in [1, 2, 4]:
        print(f"\n===== QAOA p={p} =====", flush=True)
        # single
        ss_H, ss_r, ss_e = [], [], []
        for seed in range(n_seeds):
            v, params, ne = single_start(G, p, cost_diag, n, seed=seed, budget=budget)
            ss_H.append(v)
            ss_r.append(v / exact)
            ss_e.append(ne)
        key_ss = f"p={p}/single_start"
        results["conditions"][key_ss] = dict(
            H_C_values=ss_H,
            approx_ratios=ss_r,
            n_evals_used=ss_e,
            median_H_C=float(np.median(ss_H)),
            median_ratio=float(np.median(ss_r)),
            q25_ratio=float(np.percentile(ss_r, 25)),
            q75_ratio=float(np.percentile(ss_r, 75)),
            budget=budget,
        )
        print(
            f"  single-start (budget {budget}): median <H_C>={np.median(ss_H):.3f}  "
            f"median ratio={np.median(ss_r):.3f}  median evals={np.median(ss_e):.0f}",
            flush=True,
        )

        for M in ms_values:
            ms_H, ms_r, ms_e = [], [], []
            for seed in range(n_seeds):
                v, params, ne = multistart(
                    G, p, cost_diag, n, seed=seed, M=M, total_budget=budget
                )
                ms_H.append(v)
                ms_r.append(v / exact)
                ms_e.append(ne)
            key_ms = f"p={p}/multistart_M={M}"
            results["conditions"][key_ms] = dict(
                H_C_values=ms_H,
                approx_ratios=ms_r,
                n_evals_used=ms_e,
                median_H_C=float(np.median(ms_H)),
                median_ratio=float(np.median(ms_r)),
                q25_ratio=float(np.percentile(ms_r, 25)),
                q75_ratio=float(np.percentile(ms_r, 75)),
                M=M,
                budget=budget,
            )
            print(
                f"  multistart M={M:2d} (shared budget {budget}): "
                f"median <H_C>={np.median(ms_H):.3f}  "
                f"median ratio={np.median(ms_r):.3f}  "
                f"median evals={np.median(ms_e):.0f}",
                flush=True,
            )

    results["wall_seconds"] = time.time() - t0

    out = os.path.join(RESULTS_DIR, "qaoa_multistart_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out}")
    print(f"Wall: {results['wall_seconds']:.1f}s")

    # Verdict summary
    print("\n----- multistart vs single-start (median approx ratio over 20 seeds) -----")
    print(f"{'condition':<28}{'SS med':>10}{'MS med':>10}{'Δ':>10}{'Δ_rel%':>10}")
    for p in [1, 2, 4]:
        ss = results["conditions"][f"p={p}/single_start"]["median_ratio"]
        for M in ms_values:
            ms = results["conditions"][f"p={p}/multistart_M={M}"]["median_ratio"]
            d = ms - ss
            r = 100.0 * d / ss if ss > 0 else float("nan")
            print(f"  p={p} M={M:2d}                    {ss:>10.3f}{ms:>10.3f}{d:>+10.3f}{r:>+10.1f}")


if __name__ == "__main__":
    main()
