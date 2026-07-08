#!/usr/bin/env python
"""
QAOA_2 for MAX-CUT via Qiskit Aer (much faster than pure Statevector).

Uses save_expectation_value with SparsePauliOp for the cost Hamiltonian.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import networkx as nx
from scipy.optimize import minimize

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator


def maxcut_hamiltonian(graph, node_to_qubit):
    """H_C = sum_e 0.5*(I - Z_u Z_v) as SparsePauliOp."""
    n = len(node_to_qubit)
    paulis = []
    coeffs = []
    m = graph.number_of_edges()
    for (u, v) in graph.edges():
        iu = node_to_qubit[u]
        iv = node_to_qubit[v]
        z_str = ["I"] * n
        z_str[iu] = "Z"
        z_str[iv] = "Z"
        # Qiskit Pauli string ordering: leftmost = highest qubit index
        paulis.append("".join(reversed(z_str)))
        coeffs.append(-0.5)
    # constant: +m*0.5 on identity
    paulis.append("I" * n)
    coeffs.append(0.5 * m)
    return SparsePauliOp(paulis, coeffs=coeffs)


def build_param_circuit(graph, node_to_qubit):
    """Parameterized QAOA_2 circuit."""
    n = len(node_to_qubit)
    g1 = Parameter("g1")
    b1 = Parameter("b1")
    g2 = Parameter("g2")
    b2 = Parameter("b2")
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    for (u, v) in graph.edges():
        qc.rzz(2.0 * g1, node_to_qubit[u], node_to_qubit[v])
    for i in range(n):
        qc.rx(2.0 * b1, i)
    for (u, v) in graph.edges():
        qc.rzz(2.0 * g2, node_to_qubit[u], node_to_qubit[v])
    for i in range(n):
        qc.rx(2.0 * b2, i)
    return qc, [g1, b1, g2, b2]


def cost_eval_factory(graph, backend="aer"):
    """Return a fast evaluator for <H_C> using Aer + precomputed ZZ signs.

    All ZZ operators are diagonal in the computational basis; we precompute
    an integer sign array per edge and reuse across all parameter evaluations.
    Cost per call: 1 statevector sim + ~m*2^n float multiplies (no sparse matmul).
    """
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    n2q = {v: i for i, v in enumerate(nodes)}
    m = graph.number_of_edges()
    edge_pairs = [(n2q[u], n2q[v]) for u, v in graph.edges()]

    qc, params = build_param_circuit(graph, n2q)
    sim = AerSimulator(method="statevector")
    qc_t = transpile(qc, sim)

    # Precompute sum_e (-1)^{b_u XOR b_v} per basis state x.
    # Since <H_C> = 0.5*(m - sum_e <Z_u Z_v>), and each ZZ is diagonal, we only
    # need the SUM of edge-signs per x, not per-edge signs (saves 52x memory).
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    sum_signs = np.zeros(N, dtype=np.int32)
    for (iu, iv) in edge_pairs:
        xor = ((xs >> iu) & 1) ^ ((xs >> iv) & 1)
        sum_signs += (1 - 2 * xor).astype(np.int32)
    sum_signs = sum_signs.astype(np.float64)

    def evaluate(vals):
        bound = qc_t.assign_parameters({params[i]: vals[i] for i in range(4)})
        bound2 = bound.copy()
        bound2.save_statevector()
        result = sim.run(bound2, shots=1).result()
        sv = np.array(result.get_statevector(bound2))
        probs = (sv.real * sv.real + sv.imag * sv.imag).astype(np.float64)
        zz_total = float(np.dot(sum_signs, probs))  # sum_e <Z_u Z_v>
        # <H_C> = 0.5*(m - sum_e <Z_u Z_v>)
        return 0.5 * (m - zz_total)

    return evaluate, n, m, None, n2q


def optimize(evaluator, restarts=15, seed=42, maxiter=200):
    rng = np.random.default_rng(seed)
    best = -np.inf
    best_x = None
    trials = []
    for k in range(restarts):
        x0 = rng.uniform(low=[0, 0, 0, 0],
                         high=[np.pi, np.pi / 2, np.pi, np.pi / 2])
        res = minimize(lambda v: -evaluator(v), x0, method="COBYLA",
                       options={"maxiter": maxiter, "rhobeg": 0.15})
        val = -res.fun
        trials.append({"restart": k, "cut": float(val), "x": [float(z) for z in res.x]})
        if val > best:
            best = val
            best_x = res.x
        print(f"  [restart {k}] cut={val:.5f}  best={best:.5f}")
    return best, best_x, trials


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="heawood",
                    choices=["heawood", "mobius_kantor", "pg23"])
    ap.add_argument("--restarts", type=int, default=15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--maxiter", type=int, default=200)
    ap.add_argument("--out", default="report/evidence/qaoa2_aer.json")
    args = ap.parse_args()

    if args.graph == "heawood":
        G = nx.heawood_graph(); D = 3; target = 0.7559
    elif args.graph == "mobius_kantor":
        G = nx.moebius_kantor_graph(); D = 3; target = 0.7559
    elif args.graph == "pg23":
        import sys; sys.path.insert(0, "code")
        from pg23_incidence import build_incidence_graph
        G = build_incidence_graph(); D = 4; target = 0.6693

    n = G.number_of_nodes()
    m = G.number_of_edges()
    girth = int(nx.girth(G))
    print(f"[qaoa2-aer] graph={args.graph} n={n} edges={m} D={D} girth={girth}")
    print(f"[qaoa2-aer] paper target: {target}")

    t0 = time.time()
    evaluator, _, _, _, _ = cost_eval_factory(G)
    print(f"[qaoa2-aer] setup done in {time.time()-t0:.1f}s")

    # smoke test one eval
    t1 = time.time()
    v = evaluator([0.5, 0.4, 0.3, 0.2])
    print(f"[qaoa2-aer] 1-eval smoke: cut={v:.4f} in {time.time()-t1:.2f}s")

    best, best_x, trials = optimize(evaluator, restarts=args.restarts,
                                     seed=args.seed, maxiter=args.maxiter)
    cut_fraction = best / m
    elapsed = time.time() - t0
    out = {
        "graph": args.graph,
        "n_vertices": n, "n_edges": m, "D": D, "girth": girth,
        "expected_cut_edges": float(best),
        "cut_fraction": float(cut_fraction),
        "paper_target_cut_fraction": target,
        "abs_diff_vs_paper": float(abs(cut_fraction - target)),
        "best_params": [float(z) for z in best_x],
        "n_restarts": args.restarts,
        "elapsed_sec": elapsed,
        "trials_top5": sorted(trials, key=lambda d: -d["cut"])[:5],
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[qaoa2-aer] BEST cut fraction = {cut_fraction:.5f}  (target: {target})")
    print(f"[qaoa2-aer] abs diff = {abs(cut_fraction - target):.5f}")
    print(f"[qaoa2-aer] elapsed = {elapsed:.1f}s -> {args.out}")


if __name__ == "__main__":
    main()
