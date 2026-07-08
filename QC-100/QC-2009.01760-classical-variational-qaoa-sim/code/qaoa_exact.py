"""
QAOA MaxCut exact statevector simulation + Appendix A p=1 analytical formula
verification for Medvidović & Carleo 2020/21 (arXiv:2009.01760).

Reproduces the paper's "exact" p=1 curve used as the benchmark against which
the classical variational (RBM/NN) approximation is compared (see Fig. 2, Fig. 4a).
"""
from __future__ import annotations

import json
import math
from itertools import product

import networkx as nx
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


# ---------- Graph ----------
def random_3_regular_graph(n: int, seed: int = 0) -> nx.Graph:
    """Random 3-regular graph on n nodes (n must be even).

    Matches the paper's setting (Fig. 3, Fig. 4): random 3-regular graphs.
    """
    return nx.random_regular_graph(3, n, seed=seed)


# ---------- Analytical p=1 formula (Appendix A, Eq. A1) ----------
def qaoa_p1_energy_analytical(G: nx.Graph, gamma: float, beta: float) -> float:
    """Exact QAOA MaxCut cost at p=1 for arbitrary graph G, Eq. A1.

    C(gamma, beta) = 1/2 * sum_{<k,l>}
        [ sin(4 beta) sin(2 gamma) * (cos^{q_k}(2 gamma) + cos^{q_l}(2 gamma))
          + sin^2(2 beta) * cos^{q_k + q_l - 2 Delta_kl}(2 gamma) *
                  (1 - cos^{Delta_kl}(4 gamma)) ]

    NOTE the paper's convention: for a vertex k, q_k + 1 is the DEGREE of k.
    So q_k = deg(k) - 1  (edges other than <k,l> incident to k).
    Delta_kl = number of common neighbours of k and l.

    Cost operator uses C = sum_{<i,j> in E} Z_i Z_j (Eq. 1 of the paper), so
    this returns <gamma,beta| sum Z_i Z_j |gamma,beta>, NOT the MaxCut value
    (max cut = (|E| - <C>)/2 under +/-1 convention).
    """
    total = 0.0
    for k, l in G.edges():
        qk = G.degree(k) - 1
        ql = G.degree(l) - 1
        # common neighbours excluding k,l themselves
        nk = set(G.neighbors(k)) - {l}
        nl = set(G.neighbors(l)) - {k}
        delta_kl = len(nk & nl)

        term1 = (
            math.sin(4 * beta)
            * math.sin(2 * gamma)
            * (math.cos(2 * gamma) ** qk + math.cos(2 * gamma) ** ql)
        )
        term2 = (
            math.sin(2 * beta) ** 2
            * math.cos(2 * gamma) ** (qk + ql - 2 * delta_kl)
            * (1 - math.cos(4 * gamma) ** delta_kl)
        )
        total += term1 + term2
    return 0.5 * total


# ---------- Qiskit statevector QAOA ----------
def qaoa_cost_op(G: nx.Graph, n_qubits: int) -> SparsePauliOp:
    """Build C = sum_{<i,j> in E} Z_i Z_j as a SparsePauliOp."""
    paulis = []
    coeffs = []
    for i, j in G.edges():
        z = ["I"] * n_qubits
        z[i] = "Z"
        z[j] = "Z"
        # qiskit uses little-endian string reversal in from_list
        paulis.append("".join(reversed(z)))
        coeffs.append(1.0)
    return SparsePauliOp.from_list(list(zip(paulis, coeffs)))


def qaoa_circuit(G: nx.Graph, gammas, betas, n_qubits: int) -> QuantumCircuit:
    """Build a p-layer QAOA circuit for MaxCut on G.

    Initial state: |+>^n (Hadamards on |0>^n).
    Cost layer:    exp(-i gamma sum_{<i,j>} Z_i Z_j)  -> RZZ(2 gamma) per edge
    Mixer layer:   exp(-i beta sum_i X_i)             -> RX(2 beta) per qubit
    """
    assert len(gammas) == len(betas)
    p = len(gammas)
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    for layer in range(p):
        for i, j in G.edges():
            qc.rzz(2 * gammas[layer], i, j)
        for i in range(n_qubits):
            qc.rx(2 * betas[layer], i)
    return qc


def qaoa_energy_statevector(G: nx.Graph, gammas, betas) -> float:
    n = G.number_of_nodes()
    qc = qaoa_circuit(G, gammas, betas, n)
    sv = Statevector(qc)
    op = qaoa_cost_op(G, n)
    return float(np.real(sv.expectation_value(op)))


def qaoa_statevector(G: nx.Graph, gammas, betas) -> np.ndarray:
    n = G.number_of_nodes()
    qc = qaoa_circuit(G, gammas, betas, n)
    return Statevector(qc).data


# ---------- Sanity check driver ----------
def sweep_p1(G: nx.Graph, ngrid: int = 21) -> dict:
    """Sweep p=1 (gamma, beta) grid, compare analytical vs statevector."""
    gammas = np.linspace(0, math.pi, ngrid)
    betas = np.linspace(0, math.pi / 2, ngrid)
    ana = np.zeros((ngrid, ngrid))
    exa = np.zeros((ngrid, ngrid))
    for i, g in enumerate(gammas):
        for j, b in enumerate(betas):
            ana[i, j] = qaoa_p1_energy_analytical(G, g, b)
            exa[i, j] = qaoa_energy_statevector(G, [g], [b])
    max_abs = float(np.max(np.abs(ana - exa)))
    rms = float(np.sqrt(np.mean((ana - exa) ** 2)))
    return {
        "ngrid": ngrid,
        "gammas": gammas.tolist(),
        "betas": betas.tolist(),
        "analytical": ana.tolist(),
        "statevector": exa.tolist(),
        "max_abs_diff": max_abs,
        "rms_diff": rms,
    }


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    ngrid = int(sys.argv[3]) if len(sys.argv) > 3 else 21
    out = sys.argv[4] if len(sys.argv) > 4 else "../data/p1_sweep.json"

    G = random_3_regular_graph(n, seed=seed)
    print(f"[qaoa_exact] n={n} seed={seed} |E|={G.number_of_edges()} 3-regular={all(d==3 for _,d in G.degree())}")

    result = sweep_p1(G, ngrid=ngrid)
    result["n"] = n
    result["seed"] = seed
    result["num_edges"] = G.number_of_edges()
    result["edges"] = list(map(list, G.edges()))
    print(
        f"[qaoa_exact] p=1 sweep {ngrid}x{ngrid}: max |ana-exa| = {result['max_abs_diff']:.3e}"
        f"  rms = {result['rms_diff']:.3e}"
    )

    import os
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(result, f)
    print(f"[qaoa_exact] wrote {out}")
