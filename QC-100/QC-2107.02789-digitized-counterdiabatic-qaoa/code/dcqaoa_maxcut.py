#!/usr/bin/env python3
"""
Independent replication of MaxCut portion of:
Chandarana et al. 2021, arXiv:2107.02789
"Digitized-counterdiabatic quantum approximate optimization algorithm"

Implements standard QAOA and DC-QAOA (Digitized-Counterdiabatic QAOA)
for the unweighted MaxCut problem on small graphs, using Qiskit + statevector.

DC-QAOA layer (per paper Eq. 2, Eq. 9):
  U(beta_k, gamma_k, alpha_k) = U_CD(alpha_k) * U_M(beta_k) * U_C(gamma_k)
For MaxCut the CD-operator pool A = {sigma^z sigma^y, sigma^y sigma^z}
applied to all nearest-neighbor pairs (paper: 3-regular, we use n=4..6 graphs).

Standard QAOA layer:
  U(beta_k, gamma_k) = U_M(beta_k) * U_C(gamma_k)

Cost H_C = sum_{(i,j) in E} 0.5 * (Z_i Z_j - I) (so E[H_C] = -cut)
Approximation ratio R = <cut> / cut_max.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.optimize import minimize

# Qiskit 2.x
from qiskit.quantum_info import Statevector, SparsePauliOp

REPO_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = REPO_ROOT / "report" / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Utilities: build cost operator, exact max-cut for reference
# ---------------------------------------------------------------------------

def maxcut_cost_operator(graph: nx.Graph) -> SparsePauliOp:
    """H_C = sum_{(i,j) in E} 0.5*(Z_i Z_j - I).
    <H_C> = -<cut>. So minimizing <H_C> maximizes <cut>."""
    n = graph.number_of_nodes()
    paulis = []
    coeffs = []
    for (i, j) in graph.edges():
        # Z_i Z_j
        z = ["I"] * n
        z[n - 1 - i] = "Z"  # qiskit little-endian
        z[n - 1 - j] = "Z"
        paulis.append("".join(z))
        coeffs.append(0.5)
        # -I
        paulis.append("I" * n)
        coeffs.append(-0.5)
    return SparsePauliOp.from_list(list(zip(paulis, coeffs))).simplify()


def brute_force_max_cut(graph: nx.Graph) -> int:
    n = graph.number_of_nodes()
    best = 0
    for x in range(2 ** n):
        bits = [(x >> i) & 1 for i in range(n)]
        cut = sum(1 for (i, j) in graph.edges() if bits[i] != bits[j])
        if cut > best:
            best = cut
    return best


# ---------------------------------------------------------------------------
# Statevector-level layer application (fast, no shots)
# ---------------------------------------------------------------------------

_DIAG_CACHE: dict = {}


def _cost_diag(graph: nx.Graph) -> np.ndarray:
    key = (graph.number_of_nodes(), tuple(sorted(graph.edges())))
    if key in _DIAG_CACHE:
        return _DIAG_CACHE[key]
    n = graph.number_of_nodes()
    dim = 2 ** n
    # Vectorized: for each edge, compute Z_i*Z_j eigenvalues over the full basis.
    idx = np.arange(dim)
    diag = np.zeros(dim, dtype=np.float64)
    for (i, j) in graph.edges():
        zi = 1 - 2 * ((idx >> i) & 1)
        zj = 1 - 2 * ((idx >> j) & 1)
        diag += 0.5 * (zi * zj - 1)
    _DIAG_CACHE[key] = diag
    return diag


def apply_cost_layer(state: np.ndarray, graph: nx.Graph, gamma: float) -> np.ndarray:
    """exp(-i gamma * H_C) applied to statevector.
    Since H_C is diagonal in Z basis, we can precompute diagonal phases."""
    diag = _cost_diag(graph)
    phase = np.exp(-1j * gamma * diag)
    return phase * state


def apply_mixer_layer(state: np.ndarray, n: int, beta: float) -> np.ndarray:
    """exp(-i beta * sum_k X_k) = prod_k Rx(2 beta) applied to statevector."""
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    out = state.copy()
    for k in range(n):
        # Apply single-qubit gate [[c, s],[s, c]] on qubit k
        out = _apply_1q(out, k, np.array([[c, s], [s, c]], dtype=complex), n)
    return out


def _apply_1q(state: np.ndarray, qubit: int, U: np.ndarray, n: int) -> np.ndarray:
    # Reshape into (2,)*n tensor, apply U on axis (n-1-qubit) or qubit? little-endian: qubit index = bit i
    shp = state.reshape([2] * n)
    # In little-endian, the least significant bit index in x corresponds to qubit 0.
    # numpy reshape [2]*n treats first axis as most significant bit.
    # So qubit k corresponds to axis (n-1-k).
    axis = n - 1 - qubit
    shp = np.moveaxis(shp, axis, 0)
    shp = np.tensordot(U, shp, axes=([1], [0]))
    shp = np.moveaxis(shp, 0, axis)
    return shp.reshape(-1)


def _apply_2q(state: np.ndarray, q1: int, q2: int, U: np.ndarray, n: int) -> np.ndarray:
    """Apply 4x4 gate U on qubits (q1, q2) where basis order = |q1 q2>.
    U rows/cols indexed as 2*b1 + b2 with b1 = bit of q1, b2 = bit of q2."""
    shp = state.reshape([2] * n)
    ax1 = n - 1 - q1
    ax2 = n - 1 - q2
    # Move q1->0, q2->1
    shp = np.moveaxis(shp, [ax1, ax2], [0, 1])
    d = shp.shape
    m = shp.reshape(4, -1)
    m = U @ m
    m = m.reshape(d)
    m = np.moveaxis(m, [0, 1], [ax1, ax2])
    return m.reshape(-1)


# ---- Pauli 2q operators ---------------------------------------------------
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_I = np.eye(2, dtype=complex)


def _kron(A, B):
    return np.kron(A, B)


def _expm_pauli2(P: np.ndarray, alpha: float) -> np.ndarray:
    """exp(-i alpha P) where P is a tensor product of two Paulis (P^2 = I).
    = cos(alpha) I - i sin(alpha) P.
    """
    return np.cos(alpha) * np.eye(4, dtype=complex) - 1j * np.sin(alpha) * P


def apply_cd_layer_maxcut(state: np.ndarray, graph: nx.Graph, alpha: float) -> np.ndarray:
    """Apply the CD unitary for MaxCut per paper:
       A = {sigma^z sigma^y, sigma^y sigma^z} summed over NN-pairs.
       U_CD(alpha) = prod_{(i,j)} exp(-i alpha (Z_i Y_j + Y_i Z_j))
       Because [Z_i Y_j, Y_i Z_j] != 0 in general (share qubits), we
       Trotterize each pair as exp(-i alpha ZY) * exp(-i alpha YZ) which
       matches "digitized" application in the paper (Eq. 9 product form).
    """
    n = graph.number_of_nodes()
    ZY = _kron(_Z, _Y)
    YZ = _kron(_Y, _Z)
    UZY = _expm_pauli2(ZY, alpha)
    UYZ = _expm_pauli2(YZ, alpha)
    out = state
    for (i, j) in graph.edges():
        out = _apply_2q(out, i, j, UZY, n)
        out = _apply_2q(out, i, j, UYZ, n)
    return out


# ---------------------------------------------------------------------------
# QAOA and DC-QAOA driver
# ---------------------------------------------------------------------------

def initial_plus_state(n: int) -> np.ndarray:
    return np.ones(2 ** n, dtype=complex) / np.sqrt(2 ** n)


def energy_maxcut(state: np.ndarray, graph: nx.Graph) -> float:
    """<H_C> where H_C diag as above. Returns real energy."""
    diag = _cost_diag(graph)
    p = np.abs(state) ** 2
    return float(np.sum(p * diag))


def run_qaoa(graph: nx.Graph, p: int, params: np.ndarray) -> np.ndarray:
    n = graph.number_of_nodes()
    state = initial_plus_state(n)
    for k in range(p):
        gamma = params[2 * k]
        beta = params[2 * k + 1]
        state = apply_cost_layer(state, graph, gamma)
        state = apply_mixer_layer(state, n, beta)
    return state


def run_dcqaoa(graph: nx.Graph, p: int, params: np.ndarray) -> np.ndarray:
    n = graph.number_of_nodes()
    state = initial_plus_state(n)
    for k in range(p):
        gamma = params[3 * k]
        beta = params[3 * k + 1]
        alpha = params[3 * k + 2]
        state = apply_cost_layer(state, graph, gamma)
        state = apply_mixer_layer(state, n, beta)
        state = apply_cd_layer_maxcut(state, graph, alpha)
    return state


def optimize(graph: nx.Graph, p: int, variant: str, n_restarts: int = 20, seed: int = 0):
    """Return (best_energy, best_params, best_R)."""
    rng = np.random.default_rng(seed)
    cut_max = brute_force_max_cut(graph)
    n_params = (3 if variant == "dc" else 2) * p

    def objective(params):
        if variant == "dc":
            st = run_dcqaoa(graph, p, params)
        else:
            st = run_qaoa(graph, p, params)
        # H_C = -cut + const (0 offset since we subtract 0.5 per edge => E = -<cut>)
        # Actually: 0.5*(Z_i Z_j - 1) has eigenvalue 0 for cut edge, -1 for uncut → E = -<uncut>
        # But paper uses <cut>/cut_max as R. Let's derive directly.
        return energy_maxcut(st, graph)

    best_e = np.inf
    best_p = None
    for r in range(n_restarts):
        x0 = rng.uniform(-np.pi, np.pi, size=n_params)
        res = minimize(objective, x0, method="COBYLA", options={"maxiter": 500, "rhobeg": 0.3})
        if res.fun < best_e:
            best_e = float(res.fun)
            best_p = res.x
    # E = <H_C> = sum_edges 0.5*(<Z_i Z_j> - 1)
    # cut on state = sum_edges 0.5*(1 - <Z_i Z_j>) = -E
    cut_expected = -best_e
    R = cut_expected / cut_max
    return best_e, best_p, R, cut_max, cut_expected


def main():
    results = []
    # 3-regular graphs. Smallest 3-regular has 4 nodes = K4.
    # Use n=4 (K4, 6 edges, cut_max=4) and n=6 (3-regular with 9 edges).
    graphs = {
        "K4_n4_3reg": nx.complete_graph(4),   # K4 is 3-regular
        "n6_3reg_a": nx.random_regular_graph(3, 6, seed=1),
        "n8_3reg_a": nx.random_regular_graph(3, 8, seed=2),
    }

    p_values = [1, 2, 3, 4]

    for gname, G in graphs.items():
        n = G.number_of_nodes()
        m = G.number_of_edges()
        cut_max = brute_force_max_cut(G)
        print(f"\n=== Graph {gname}: n={n}, edges={m}, MaxCut={cut_max} ===")
        for p in p_values:
            for variant in ["qaoa", "dc"]:
                t0 = time.time()
                e, params, R, cm, ce = optimize(G, p, variant, n_restarts=25, seed=100 + p)
                dt = time.time() - t0
                print(f"  p={p} {variant:5s} E={e:.4f} cut={ce:.4f}/{cm} R={R:.4f}  ({dt:.1f}s, {len(params)} params)")
                results.append({
                    "graph": gname,
                    "n_qubits": n,
                    "n_edges": m,
                    "cut_max": cm,
                    "p": p,
                    "variant": variant,
                    "n_params": int(len(params)),
                    "energy": e,
                    "cut_expected": ce,
                    "approx_ratio": R,
                    "wall_seconds": dt,
                })

    out = EVIDENCE_DIR / "maxcut_results.json"
    with out.open("w") as f:
        json.dump({
            "paper": "arXiv:2107.02789",
            "experiment": "MaxCut approximation ratio vs depth p",
            "results": results,
        }, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
