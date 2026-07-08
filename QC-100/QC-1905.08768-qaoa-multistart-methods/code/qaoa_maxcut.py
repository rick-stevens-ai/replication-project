"""
Independent replication of the CORE claim of Shaydulin et al. 2019
"Multistart Methods for Quantum Approximate Optimization" (arXiv:1905.08768)

CLAIM UNDER TEST (headline / testable):
  For QAOA parameter optimization on small graphs, multistart (best-of-M random
  restarts) finds substantially better parameters (higher expectation of the
  problem Hamiltonian and higher approximation ratio) than a single-start local
  optimizer under an equal or smaller function-evaluation budget.

  The paper demonstrates this for modularity-maximization on 10-12 vertex graphs
  with COBYLA/BOBYQA/NEWUOA/etc. vs. APOSMM (a formal multistart framework),
  with p=1,2,4 QAOA depth, showing single-start local methods almost always
  converge to a low-quality local optimum well before exhausting a 1000-eval
  budget, whereas multistart reaches near-optimal (Fig. 2 / Fig. 3).

REPLICATION DESIGN (small-but-faithful):
  * Problem: MAX-CUT (the closely-related problem the paper explicitly
    references and for which multistart utility should also hold; the paper's
    theoretical multistart argument is problem-agnostic — landscape has many
    local optima).
  * n = 8 vertex 3-regular graph (small enough for exact statevector, large
    enough that the QAOA landscape is nontrivial and has multiple local
    optima — matches the paper's "small connected graphs with community
    structure" regime).
  * p = 1 and p = 2 QAOA depth (matches paper's dim(D)=2 and dim(D)=4 cases).
  * Optimizer: COBYLA (one of the 6 the paper tests).
  * Single-start: 1 random init, budget = 1000 fn evals (paper's budget).
  * Multistart:  M random inits, each run to convergence, budget shared
                 (each run capped at 1000/M evals), take best.
  * 20 random seeds per condition to get medians + quartiles (paper uses
    10 seeds × 6 problems = 60; we use 20 seeds × 1 problem = 20 runs
    per condition).
  * Real Qiskit Aer statevector simulation — no shot noise, so we are giving
    the single-start optimizer its BEST possible case. If multistart still
    wins on noiseless expectation values, that is a stronger reproduction
    of the paper's landscape argument.

Success criterion for REPLICATED verdict:
  Multistart (M >= 5) median-best-<H_C> exceeds single-start median-best-<H_C>
  by a clear margin (>= 5% relative on approximation ratio) for at least p=1
  or p=2. This mirrors the paper's Fig. 2 finding that local methods without
  restart underperform APOSMM by a large margin (often ratio < 0.5 vs ~1.0).
"""
import json
import os
import sys
import time
import numpy as np
import networkx as nx
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "report",
    "evidence",
)
os.makedirs(RESULTS_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Problem: MAX-CUT on a small graph
# ---------------------------------------------------------------------------
def build_graph(n=8, seed=42):
    """3-regular graph on n vertices (n must be even)."""
    G = nx.random_regular_graph(3, n, seed=seed)
    return G


def maxcut_hamiltonian(G):
    """Build H_C = sum_{(i,j) in E} 0.5*(I - Z_i Z_j).
    Returns SparsePauliOp with n qubits.
    """
    n = G.number_of_nodes()
    pauli_list = []
    for i, j in G.edges():
        z = ["I"] * n
        z[i] = "Z"
        z[j] = "Z"
        # 0.5*(I - Z_i Z_j)  -> +0.5*I  -0.5*ZZ
        pauli_list.append(("".join(z[::-1]), -0.5))  # Qiskit is little-endian
        pauli_list.append(("I" * n, 0.5))
    return SparsePauliOp.from_list(pauli_list).simplify()


def brute_force_maxcut(G):
    """Exact MAX-CUT for small graphs — for approximation ratio."""
    n = G.number_of_nodes()
    best = 0
    for s in range(1 << n):
        cut = 0
        for i, j in G.edges():
            bi = (s >> i) & 1
            bj = (s >> j) & 1
            if bi != bj:
                cut += 1
        if cut > best:
            best = cut
    return best


# ---------------------------------------------------------------------------
# QAOA circuit + expectation
# ---------------------------------------------------------------------------
def qaoa_circuit(G, params, p):
    """QAOA(p) circuit for MAX-CUT on graph G.
    params = [gamma_1..gamma_p, beta_1..beta_p]
    """
    n = G.number_of_nodes()
    gammas = params[:p]
    betas = params[p:]
    qc = QuantumCircuit(n)
    # initial superposition
    for q in range(n):
        qc.h(q)
    for layer in range(p):
        # cost: exp(-i gamma sum_{(i,j) in E} 0.5*(I - Z_i Z_j))
        # constants drop out; each ZZ term becomes RZZ(2*gamma*(-0.5)*(-1)?) ...
        # for MAX-CUT the standard is RZZ(2*gamma) on each edge (up to global phase)
        g = gammas[layer]
        for (i, j) in G.edges():
            qc.rzz(2.0 * g, i, j)
        # mixer: exp(-i beta sum_i X_i) = product of RX(2*beta) on each qubit
        b = betas[layer]
        for q in range(n):
            qc.rx(2.0 * b, q)
    return qc


class QAOAObjective:
    """Callable expectation-value oracle with an evaluation counter."""

    def __init__(self, G, H_C, p):
        self.G = G
        self.H_C = H_C
        self.p = p
        self.n_evals = 0
        self.best_value = -np.inf
        self.best_params = None
        self.history = []

    def __call__(self, params):
        self.n_evals += 1
        qc = qaoa_circuit(self.G, params, self.p)
        sv = Statevector.from_instruction(qc)
        # expectation of H_C (real)
        val = float(np.real(sv.expectation_value(self.H_C)))
        if val > self.best_value:
            self.best_value = val
            self.best_params = np.array(params)
        self.history.append(val)
        # scipy minimizes, so return negative
        return -val


# ---------------------------------------------------------------------------
# Optimization runs
# ---------------------------------------------------------------------------
def random_init(p, rng):
    """Random initial (gamma, beta) in the paper's domain."""
    # gamma in [0, 2pi), beta in [0, pi)
    gammas = rng.uniform(0.0, 2.0 * np.pi, size=p)
    betas = rng.uniform(0.0, np.pi, size=p)
    return np.concatenate([gammas, betas])


def single_start_run(G, H_C, p, seed, budget=1000):
    rng = np.random.default_rng(seed)
    obj = QAOAObjective(G, H_C, p)
    x0 = random_init(p, rng)
    try:
        minimize(
            obj,
            x0,
            method="COBYLA",
            options={"maxiter": budget, "rhobeg": 0.5, "catol": 1e-4, "disp": False},
        )
    except Exception as e:  # noqa
        pass
    return obj.best_value, obj.best_params, obj.n_evals


def multistart_run(G, H_C, p, seed, M, total_budget=1000):
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
        obj = QAOAObjective(G, H_C, p)
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


def sample_cut_from_params(G, params, p, n_samples=10000, seed=0):
    """Sample bitstrings from the QAOA state and return the best MAX-CUT value found."""
    rng = np.random.default_rng(seed)
    qc = qaoa_circuit(G, params, p)
    sv = Statevector.from_instruction(qc)
    probs = np.abs(sv.data) ** 2
    # sanity: normalize numerical drift
    probs = probs / probs.sum()
    n = G.number_of_nodes()
    idx = rng.choice(len(probs), size=n_samples, p=probs)
    best_cut = 0
    for s in idx:
        cut = 0
        for i, j in G.edges():
            bi = (int(s) >> i) & 1
            bj = (int(s) >> j) & 1
            if bi != bj:
                cut += 1
        if cut > best_cut:
            best_cut = cut
    return best_cut


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    n_vertices = 8
    graph_seed = 42
    G = build_graph(n=n_vertices, seed=graph_seed)
    print(f"Graph: n={n_vertices}, m={G.number_of_edges()}, 3-regular seed={graph_seed}")
    print(f"Edges: {list(G.edges())}")
    exact_maxcut = brute_force_maxcut(G)
    print(f"Exact MAX-CUT = {exact_maxcut}")

    H_C = maxcut_hamiltonian(G)
    # For MAX-CUT with H = sum 0.5*(I - Z_i Z_j), max eigenvalue == exact_maxcut
    # so approximation ratio = <H_C> / exact_maxcut

    results = {
        "graph": {
            "n_vertices": n_vertices,
            "n_edges": G.number_of_edges(),
            "graph_seed": graph_seed,
            "edges": [list(e) for e in G.edges()],
            "exact_maxcut": exact_maxcut,
        },
        "conditions": {},
    }

    n_seeds = 20
    budget = 1000
    ms_values = [5, 10, 20]

    for p in [1, 2]:
        print(f"\n===== QAOA p={p} =====")
        # --- single-start ---
        ss_H = []
        ss_ratio = []
        ss_evals = []
        for seed in range(n_seeds):
            val, params, ne = single_start_run(G, H_C, p, seed=seed, budget=budget)
            ss_H.append(val)
            ss_ratio.append(val / exact_maxcut)
            ss_evals.append(ne)
        cond_key = f"p={p}/single_start"
        results["conditions"][cond_key] = {
            "H_C_values": ss_H,
            "approx_ratios": ss_ratio,
            "n_evals_used": ss_evals,
            "median_H_C": float(np.median(ss_H)),
            "median_ratio": float(np.median(ss_ratio)),
            "q25_ratio": float(np.percentile(ss_ratio, 25)),
            "q75_ratio": float(np.percentile(ss_ratio, 75)),
            "budget": budget,
        }
        print(
            f"  single-start (budget {budget}): median <H_C>={np.median(ss_H):.3f}  "
            f"median ratio={np.median(ss_ratio):.3f}  "
            f"median evals used={np.median(ss_evals):.0f}"
        )

        # --- multistart, budget capped equal to single-start ---
        for M in ms_values:
            ms_H = []
            ms_ratio = []
            ms_evals = []
            for seed in range(n_seeds):
                val, params, ne = multistart_run(G, H_C, p, seed=seed, M=M, total_budget=budget)
                ms_H.append(val)
                ms_ratio.append(val / exact_maxcut)
                ms_evals.append(ne)
            cond_key = f"p={p}/multistart_M={M}"
            results["conditions"][cond_key] = {
                "H_C_values": ms_H,
                "approx_ratios": ms_ratio,
                "n_evals_used": ms_evals,
                "median_H_C": float(np.median(ms_H)),
                "median_ratio": float(np.median(ms_ratio)),
                "q25_ratio": float(np.percentile(ms_ratio, 25)),
                "q75_ratio": float(np.percentile(ms_ratio, 75)),
                "M": M,
                "budget": budget,
            }
            print(
                f"  multistart M={M:2d} (shared budget {budget}): "
                f"median <H_C>={np.median(ms_H):.3f}  "
                f"median ratio={np.median(ms_ratio):.3f}  "
                f"median evals used={np.median(ms_evals):.0f}"
            )

    results["wall_seconds"] = time.time() - t0

    out = os.path.join(RESULTS_DIR, "qaoa_multistart_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out}")
    print(f"Wall time: {results['wall_seconds']:.1f}s")

    # ---- verdict math ----
    def gap(key_ms, key_ss):
        ms_med = results["conditions"][key_ms]["median_ratio"]
        ss_med = results["conditions"][key_ss]["median_ratio"]
        return ms_med - ss_med, ms_med, ss_med

    print("\n----- multistart vs single-start (approx ratio, median over 20 seeds) -----")
    for p in [1, 2]:
        for M in ms_values:
            d, ms, ss = gap(f"p={p}/multistart_M={M}", f"p={p}/single_start")
            rel = d / ss * 100 if ss > 0 else float("nan")
            print(
                f"  p={p} M={M:2d}: MS={ms:.3f}  SS={ss:.3f}  "
                f"Δ={d:+.3f}  Δ_rel={rel:+.1f}%"
            )


if __name__ == "__main__":
    main()
