#!/usr/bin/env python
"""
QAOA_2 for MAX-CUT on high-girth D-regular graphs.
Reproduce Marwaha 2021 (arXiv:2101.05513) Table 1 QAOA2 values.

For D=3, girth>5, the reported maximum expected cut fraction is
0.5 + 0.2559 = 0.7559 (matches WL20).

For D=4, girth>5: 0.5 + 0.1693 = 0.6693.
For D=5, girth>5: 0.5 + 0.1907 = 0.6907.

Strategy: use a large-enough D-regular girth>=6 graph on ~14-20 qubits and run
statevector simulation with Qiskit-Aer, optimizing the 4 QAOA angles.
Compare the achieved <C>/|E| to the paper's reported cut fraction.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import networkx as nx
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


def heawood_graph():
    """Heawood graph: 3-regular, 14 vertices, girth 6."""
    return nx.heawood_graph()


def mobius_kantor_graph():
    """Mobius-Kantor: 3-regular, 16 vertices, girth 6."""
    return nx.moebius_kantor_graph()


def build_qaoa2_circuit(graph, gamma1, beta1, gamma2, beta2):
    """Standard QAOA_2 circuit for MAX-CUT.
    H_C = sum_{(u,v) in E} 0.5*(I - Z_u Z_v)
    U_C(gamma) = exp(-i gamma H_C), U_B(beta) = exp(-i beta sum_j X_j).
    """
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    qc = QuantumCircuit(n)
    # initial state |+>^n
    for i in range(n):
        qc.h(i)
    # layer p=1
    for (u, v) in graph.edges():
        qc.rzz(2.0 * gamma1, idx[u], idx[v])
    for i in range(n):
        qc.rx(2.0 * beta1, i)
    # layer p=2
    for (u, v) in graph.edges():
        qc.rzz(2.0 * gamma2, idx[u], idx[v])
    for i in range(n):
        qc.rx(2.0 * beta2, i)
    return qc


_BITS_CACHE = {}

def _bit_matrix(n):
    if n in _BITS_CACHE:
        return _BITS_CACHE[n]
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    bits = np.zeros((N, n), dtype=np.int8)
    for i in range(n):
        bits[:, i] = ((xs >> i) & 1).astype(np.int8)
    _BITS_CACHE[n] = bits
    return bits

def cut_expectation(graph, params):
    """<H_C> where H_C = sum_e 0.5*(I - Z_u Z_v).
    Returns the expected number of cut edges.
    """
    gamma1, beta1, gamma2, beta2 = params
    qc = build_qaoa2_circuit(graph, gamma1, beta1, gamma2, beta2)
    sv = Statevector.from_instruction(qc)
    probs = np.abs(sv.data) ** 2  # length 2^n, Qiskit little-endian
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    bits = _bit_matrix(n)  # (N, n) with bits[x,i] = (x>>i)&1
    # For each edge, compute <Z_u Z_v> = sum_x (-1)^(x_u XOR x_v) p(x)
    # <cut> = 0.5*(m - sum_e <Z_u Z_v>)
    edges = list(graph.edges())
    m = len(edges)
    zz_sum = 0.0
    for (u, v) in edges:
        iu, iv = idx[u], idx[v]
        xor = bits[:, iu] ^ bits[:, iv]  # 0 same, 1 differ
        signs = 1 - 2 * xor  # +1 same, -1 differ
        zz_sum += float(np.dot(signs.astype(np.float64), probs))
    exp_cut = 0.5 * (m - zz_sum)
    return exp_cut


def negative_cut(params, graph):
    return -cut_expectation(graph, params)


def optimize_qaoa2(graph, n_restarts=20, seed=42):
    rng = np.random.default_rng(seed)
    best = None
    best_params = None
    trials = []
    for k in range(n_restarts):
        # QAOA parameters typically in reasonable ranges
        x0 = rng.uniform(low=[0, 0, 0, 0],
                         high=[np.pi, np.pi/2, np.pi, np.pi/2])
        res = minimize(negative_cut, x0, args=(graph,), method="COBYLA",
                       options={"maxiter": 400, "rhobeg": 0.15})
        val = -res.fun
        trials.append({"restart": k, "x0": x0.tolist(),
                       "x": res.x.tolist(), "cut": float(val)})
        if best is None or val > best:
            best = val
            best_params = res.x
    return best, best_params, trials


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="heawood",
                    choices=["heawood", "mobius_kantor"])
    ap.add_argument("--restarts", type=int, default=25)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="report/evidence/qaoa2_result.json")
    args = ap.parse_args()

    t0 = time.time()
    if args.graph == "heawood":
        G = heawood_graph()
        D = 3
        expected_cut_fraction = 0.7559  # 0.5 + 0.2559
    elif args.graph == "mobius_kantor":
        G = mobius_kantor_graph()
        D = 3
        expected_cut_fraction = 0.7559
    n = G.number_of_nodes()
    m = G.number_of_edges()
    girth = nx.girth(G) if hasattr(nx, "girth") else None
    # compute girth manually if needed
    if girth is None:
        try:
            girth = min(len(c) for c in nx.cycle_basis(G))
        except Exception:
            girth = -1
    print(f"[qaoa2] graph={args.graph} n={n} edges={m} D={D} girth={girth}")
    print(f"[qaoa2] paper cut fraction target for D={D}, girth>5: {expected_cut_fraction}")

    best, best_params, trials = optimize_qaoa2(G, n_restarts=args.restarts,
                                                seed=args.seed)
    cut_fraction = best / m
    elapsed = time.time() - t0
    out = {
        "graph": args.graph,
        "n_vertices": n,
        "n_edges": m,
        "D": D,
        "girth": int(girth),
        "expected_cut_edges": float(best),
        "cut_fraction": float(cut_fraction),
        "paper_target_cut_fraction": expected_cut_fraction,
        "paper_target_improvement_over_random": expected_cut_fraction - 0.5,
        "achieved_improvement_over_random": float(cut_fraction - 0.5),
        "abs_diff_vs_paper": float(abs(cut_fraction - expected_cut_fraction)),
        "rel_diff_vs_paper": float(abs(cut_fraction - expected_cut_fraction) / expected_cut_fraction),
        "best_params": {"gamma1": float(best_params[0]),
                         "beta1": float(best_params[1]),
                         "gamma2": float(best_params[2]),
                         "beta2": float(best_params[3])},
        "n_restarts": args.restarts,
        "elapsed_sec": float(elapsed),
        "trials_top5": sorted(trials, key=lambda d: -d["cut"])[:5],
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[qaoa2] BEST cut fraction = {cut_fraction:.5f}  (paper D=3 girth>5 target: {expected_cut_fraction:.5f})")
    print(f"[qaoa2] abs diff = {abs(cut_fraction - expected_cut_fraction):.5f}")
    print(f"[qaoa2] elapsed = {elapsed:.1f} s")
    print(f"[qaoa2] wrote {args.out}")


if __name__ == "__main__":
    main()
