#!/usr/bin/env python
"""
QAOA_2 for MAX-CUT on high-girth D-regular graphs (memory-efficient v2).

Compute <H_C> = sum_e 0.5*(1 - <Z_u Z_v>) using the statevector and pure
NumPy bitmask reshaping, avoiding an (N, n) bit matrix that would blow up
memory at 26+ qubits.

Uses Statevector.from_instruction plus |ψ|^2 marginals per edge.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import networkx as nx
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def build_qaoa2_circuit(graph, gamma1, beta1, gamma2, beta2, node_to_qubit):
    n = len(node_to_qubit)
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    for (u, v) in graph.edges():
        qc.rzz(2.0 * gamma1, node_to_qubit[u], node_to_qubit[v])
    for i in range(n):
        qc.rx(2.0 * beta1, i)
    for (u, v) in graph.edges():
        qc.rzz(2.0 * gamma2, node_to_qubit[u], node_to_qubit[v])
    for i in range(n):
        qc.rx(2.0 * beta2, i)
    return qc


def zz_expectation(probs, n, i, j):
    """Compute <Z_i Z_j> from a length-2^n probability vector.
    Qiskit convention: state index x has bit b_k = (x >> k) & 1 for qubit k.
    <Z_i Z_j> = sum_x (-1)^(b_i XOR b_j) * probs[x].
    """
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    bi = ((xs >> i) & 1)
    bj = ((xs >> j) & 1)
    xor = bi ^ bj
    signs = 1 - 2 * xor  # +1 same, -1 differ
    return float(np.dot(signs.astype(np.float64), probs))


def cut_expectation(graph, params, node_to_qubit, edge_pairs, N_cache):
    """Expected number of cut edges."""
    gamma1, beta1, gamma2, beta2 = params
    n = len(node_to_qubit)
    qc = build_qaoa2_circuit(graph, gamma1, beta1, gamma2, beta2, node_to_qubit)
    sv = Statevector.from_instruction(qc)
    probs = np.abs(sv.data) ** 2  # dense length 2^n
    m = len(edge_pairs)
    zz_sum = 0.0
    for (iu, iv) in edge_pairs:
        zz_sum += zz_expectation(probs, n, iu, iv)
    return 0.5 * (m - zz_sum)


def neg_cut(params, graph, node_to_qubit, edge_pairs, N_cache):
    return -cut_expectation(graph, params, node_to_qubit, edge_pairs, N_cache)


def optimize_qaoa2(graph, restarts=20, seed=42, verbose=False):
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    node_to_qubit = {v: i for i, v in enumerate(nodes)}
    edge_pairs = [(node_to_qubit[u], node_to_qubit[v]) for u, v in graph.edges()]
    N_cache = {}
    rng = np.random.default_rng(seed)
    best = -np.inf
    best_params = None
    trials = []
    for k in range(restarts):
        x0 = rng.uniform(low=[0, 0, 0, 0],
                         high=[np.pi, np.pi / 2, np.pi, np.pi / 2])
        try:
            res = minimize(neg_cut, x0,
                           args=(graph, node_to_qubit, edge_pairs, N_cache),
                           method="COBYLA",
                           options={"maxiter": 300, "rhobeg": 0.15})
            val = -res.fun
        except Exception as e:
            print(f"[qaoa2] restart {k} failed: {e}")
            continue
        trials.append({"restart": k, "cut": float(val),
                       "x": [float(z) for z in res.x]})
        if val > best:
            best = val
            best_params = res.x
        if verbose:
            print(f"[qaoa2] restart {k}: cut = {val:.5f}, best = {best:.5f}")
    return best, best_params, trials


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="heawood",
                    choices=["heawood", "mobius_kantor", "pg23"])
    ap.add_argument("--restarts", type=int, default=25)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="report/evidence/qaoa2_result.json")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if args.graph == "heawood":
        G = nx.heawood_graph()
        D = 3
        target = 0.7559  # Table 1
    elif args.graph == "mobius_kantor":
        G = nx.moebius_kantor_graph()
        D = 3
        target = 0.7559
    elif args.graph == "pg23":
        import sys
        sys.path.insert(0, "code")
        from pg23_incidence import build_incidence_graph
        G = build_incidence_graph()
        D = 4
        target = 0.6693  # Table 1: 0.5 + 0.1693
    n = G.number_of_nodes()
    m = G.number_of_edges()
    girth = int(nx.girth(G))
    print(f"[qaoa2] graph={args.graph} n={n} edges={m} D={D} girth={girth}")
    print(f"[qaoa2] paper target cut fraction (D={D} girth>5): {target}")

    t0 = time.time()
    best, best_params, trials = optimize_qaoa2(G, restarts=args.restarts,
                                                seed=args.seed,
                                                verbose=args.verbose)
    cut_fraction = best / m
    elapsed = time.time() - t0
    out = {
        "graph": args.graph,
        "n_vertices": n,
        "n_edges": m,
        "D": D,
        "girth": girth,
        "expected_cut_edges": float(best),
        "cut_fraction": float(cut_fraction),
        "paper_target_cut_fraction": target,
        "paper_target_improvement_over_random": target - 0.5,
        "achieved_improvement_over_random": float(cut_fraction - 0.5),
        "abs_diff_vs_paper": float(abs(cut_fraction - target)),
        "best_params": {"gamma1": float(best_params[0]),
                         "beta1": float(best_params[1]),
                         "gamma2": float(best_params[2]),
                         "beta2": float(best_params[3])},
        "n_restarts": args.restarts,
        "elapsed_sec": elapsed,
        "trials_top5": sorted(trials, key=lambda d: -d["cut"])[:5],
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[qaoa2] BEST cut fraction = {cut_fraction:.5f}  (paper target: {target:.5f})")
    print(f"[qaoa2] abs diff = {abs(cut_fraction - target):.5f}")
    print(f"[qaoa2] elapsed = {elapsed:.1f} s -> {args.out}")


if __name__ == "__main__":
    main()
