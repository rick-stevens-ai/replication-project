"""
Independent replication support code for
  Vinkhuijzen, Coopmans, Elkouss, Dunjko, Laarman
  "LIMDD: A Decision Diagram for Simulation of Quantum Computing Including Stabilizer States"
  arXiv:2108.00931v5 (Quantum, 2023)

The paper introduces LIMDD, a new decision-diagram data structure that provably
subsumes QMDDs and stabilizer states. Per Sec. 6 (Discussion, p. 30):
    "we leave an implementation of the Pauli-LIMDD ... to future work."
so no reference LIMDD implementation ships with the paper. The claim we CAN
independently check is the underlying QMDD baseline behavior that motivates
LIMDD:

  (C1, testable)  QMDD correctly simulates Clifford + T circuits and its
                  extracted statevector agrees with Qiskit's dense simulator.
                  [SPOT-CHECK of DD-based simulation]
  (C2, testable)  QMDDs are more compact than a dense 2^n statevector on
                  low-entanglement or structured states (motivation for DD sim
                  in general -- Sec. 1, Fig. 2/3).
  (C3, testable, motivating LIMDD)  QMDDs require large-and-growing node counts
                  for cluster / stabilizer states (paper's Appendix B lower
                  bound: exponential in n). This is the concrete gap LIMDD
                  is designed to close.
  (C4, theoretical, NOT re-implementable here)  A Pauli-LIMDD would collapse
                  the cluster-state size to poly(n). No reference LIMDD
                  implementation exists.
  (C5, theoretical)  Table 1 asymptotic worst-case complexities of QMDD vs
                  LIMDD operations. Proven, not empirically re-verified.
  (C6, empirical) Table 2 heuristic Dicke-state stabilizer ranks via Bravyi
                  simulated annealing. Only up to n=9 with SURF supercomputer;
                  out of scope for a small CPU replication.

We therefore test C1, C2, C3 with actual simulation on a laptop CPU using
mqt.ddsim (the modern successor to the QMDD line of DD simulators) and
Qiskit's dense statevector as ground truth.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import qiskit
from qiskit import QuantumCircuit, qasm2
from qiskit.quantum_info import Statevector
from mqt import ddsim
from mqt.ddsim import CircuitSimulator
from mqt.core import load

HERE = Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def qc_to_ddsim(qc: QuantumCircuit):
    """Round-trip a Qiskit circuit into mqt.core via QASM2 so ddsim can run it."""
    qasm = qasm2.dumps(qc)
    # mqt.core.load accepts a QASM2 string
    return load(qasm)


def ddsim_statevector(qc: QuantumCircuit, seed: int = 42):
    """Simulate qc with mqt.ddsim; return (statevector, active_vector_nodes, sim_time)."""
    mqt_qc = qc_to_ddsim(qc)
    sim = CircuitSimulator(mqt_qc, seed=seed)
    t0 = time.perf_counter()
    # We need the state vector *and* the DD size. simulate() runs the circuit
    # (shots don't matter for our purposes; we only want the built DD state).
    sim.simulate(shots=0)
    dt = time.perf_counter() - t0
    dd_nodes = sim.get_active_vector_node_count()
    dd = sim.get_constructed_dd()
    # Extract full vector for ground-truth comparison. Works only for small n.
    # mqt.core.dd.VectorDD exposes a .get_vector() / __iter__ path; try both.
    vec = None
    for meth in ("get_vector", "to_vector", "as_array"):
        if hasattr(dd, meth):
            try:
                vec = np.asarray(getattr(dd, meth)(), dtype=complex)
                break
            except Exception:
                pass
    if vec is None:
        # Fallback: iterate over amplitudes
        try:
            vec = np.array([complex(a) for a in dd], dtype=complex)
        except Exception:
            vec = None
    return vec, dd_nodes, dt


def qiskit_statevector(qc: QuantumCircuit):
    t0 = time.perf_counter()
    sv = Statevector.from_instruction(qc).data
    dt = time.perf_counter() - t0
    return np.asarray(sv, dtype=complex), dt


def align_global_phase(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Return a * exp(i*phi) that matches b up to global phase."""
    # Find the first significantly non-zero entry in b
    idx = int(np.argmax(np.abs(b)))
    if np.abs(a[idx]) < 1e-12 or np.abs(b[idx]) < 1e-12:
        return a
    phi = np.angle(b[idx] / a[idx])
    return a * np.exp(1j * phi)


def fidelity(a: np.ndarray, b: np.ndarray) -> float:
    return float(abs(np.vdot(a, b)) ** 2)


# ---------------------------------------------------------------------------
# Circuits
# ---------------------------------------------------------------------------

def clifford_plus_t_circuit(n: int, k_t: int, seed: int = 0) -> QuantumCircuit:
    """A small Clifford + T circuit with n qubits and k_t T-gates.

    Structure: layer of H on all qubits, chain of CNOTs, then k_t T-gates on
    randomly chosen qubits, closed with H on all qubits. Deterministic given
    (n, k_t, seed).
    """
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for q in range(n - 1):
        qc.cx(q, q + 1)
    for _ in range(k_t):
        q = int(rng.integers(0, n))
        qc.t(q)
    # more entanglement + a mid-layer of S/CZ (still Clifford)
    for q in range(n - 1):
        qc.cz(q, q + 1)
    for q in range(n):
        qc.s(q)
    for q in range(n):
        qc.h(q)
    return qc


def linear_cluster_state_circuit(n: int) -> QuantumCircuit:
    """Prepare the 1D linear cluster state on n qubits.

    Standard recipe: apply H to every qubit, then CZ on every neighboring
    pair (i, i+1). Result is a stabilizer state; the paper (App. B) proves
    QMDDs require exponentially many nodes for the 2D cluster state; the 1D
    version is a simpler stabilizer state that lets us just show that node
    counts grow, and that a DD encoding of a stabilizer state is *not* free.
    """
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for q in range(n - 1):
        qc.cz(q, q + 1)
    return qc


def grid_cluster_state_circuit(rows: int, cols: int) -> QuantumCircuit:
    """Prepare the 2D-grid cluster state (the case treated in App. B)."""
    n = rows * cols
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    # horizontal edges
    for r in range(rows):
        for c in range(cols - 1):
            qc.cz(r * cols + c, r * cols + c + 1)
    # vertical edges
    for r in range(rows - 1):
        for c in range(cols):
            qc.cz(r * cols + c, (r + 1) * cols + c)
    return qc


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def exp_C1_C2_clifford_plus_t():
    """Test C1 (correctness vs Qiskit) and C2 (DD vs dense size)."""
    rows = []
    for n, kT in [(4, 2), (5, 3), (5, 4), (6, 3), (6, 4), (7, 4), (8, 4)]:
        qc = clifford_plus_t_circuit(n, kT, seed=n * 13 + kT)
        dd_vec, dd_nodes, dd_t = ddsim_statevector(qc)
        qk_vec, qk_t = qiskit_statevector(qc)
        dense_size = 2 ** n

        if dd_vec is not None and dd_vec.shape == qk_vec.shape:
            dd_vec_aligned = align_global_phase(dd_vec, qk_vec)
            fid = fidelity(dd_vec_aligned, qk_vec)
            l1 = float(np.max(np.abs(dd_vec_aligned - qk_vec)))
        else:
            fid = float("nan")
            l1 = float("nan")

        rows.append({
            "n_qubits": n,
            "n_T_gates": kT,
            "dd_active_vector_nodes": dd_nodes,
            "dense_statevector_amplitudes": dense_size,
            "compactness_ratio_dense_over_dd": dense_size / max(dd_nodes, 1),
            "fidelity_dd_vs_qiskit": fid,
            "max_abs_amp_diff": l1,
            "match_within_1e-9": bool(np.isfinite(fid) and abs(fid - 1.0) < 1e-9),
            "ddsim_time_s": dd_t,
            "qiskit_time_s": qk_t,
        })
        print(f"  n={n} kT={kT}  DD_nodes={dd_nodes:4d}  dense={dense_size:4d}  "
              f"fid={fid:.12f}  match={rows[-1]['match_within_1e-9']}")

    (EVID / "C1_C2_clifford_plus_t.json").write_text(
        json.dumps(rows, indent=2, default=str)
    )
    return rows


def exp_C3_stabilizer_states():
    """Test C3: QMDD size on stabilizer / cluster states (motivation for LIMDD).

    We measure active vector node count for 1D linear cluster states of
    increasing n and for 2D grid cluster states. Per the paper (App. B), 2D
    cluster states are the ones with the exponential lower bound; 1D is
    easier and grows more slowly.
    """
    lin_rows = []
    for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        qc = linear_cluster_state_circuit(n)
        _, dd_nodes, dd_t = ddsim_statevector(qc)
        lin_rows.append({
            "topology": "1D-linear-cluster",
            "n_qubits": n,
            "dd_active_vector_nodes": dd_nodes,
            "dense_statevector_amplitudes": 2 ** n,
            "ddsim_time_s": dd_t,
        })
        print(f"  1D cluster n={n:2d}  DD_nodes={dd_nodes:6d}  dense={2**n:6d}")

    grid_rows = []
    for rows_, cols_ in [(2, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4)]:
        qc = grid_cluster_state_circuit(rows_, cols_)
        _, dd_nodes, dd_t = ddsim_statevector(qc)
        grid_rows.append({
            "topology": f"2D-grid-{rows_}x{cols_}",
            "rows": rows_,
            "cols": cols_,
            "n_qubits": rows_ * cols_,
            "dd_active_vector_nodes": dd_nodes,
            "dense_statevector_amplitudes": 2 ** (rows_ * cols_),
            "ddsim_time_s": dd_t,
        })
        print(f"  2D cluster {rows_}x{cols_}  n={rows_*cols_:2d}  "
              f"DD_nodes={dd_nodes:6d}  dense={2**(rows_*cols_):6d}")

    (EVID / "C3_stabilizer_dd_size.json").write_text(
        json.dumps({"linear": lin_rows, "grid": grid_rows}, indent=2, default=str)
    )
    return lin_rows, grid_rows


def versions_manifest():
    import platform
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "qiskit": qiskit.__version__,
        "mqt.ddsim": getattr(ddsim, "__version__", "unknown"),
        "numpy": np.__version__,
    }


def main():
    print("== Versions ==")
    v = versions_manifest()
    for k, val in v.items():
        print(f"  {k:14s} {val}")
    (EVID / "versions.json").write_text(json.dumps(v, indent=2))

    print("\n== C1 + C2: Clifford + T circuits, DD vs Qiskit ==")
    c12 = exp_C1_C2_clifford_plus_t()

    print("\n== C3: DD size on stabilizer / cluster states ==")
    lin, grid = exp_C3_stabilizer_states()

    all_match = all(r["match_within_1e-9"] for r in c12)
    max_compact = max(r["compactness_ratio_dense_over_dd"] for r in c12)

    summary = {
        "C1_all_clifford_plus_t_states_match_qiskit": all_match,
        "C1_num_tested": len(c12),
        "C2_max_compactness_ratio_dense_over_dd": max_compact,
        "C3_1D_max_qubits_tested": max(r["n_qubits"] for r in lin),
        "C3_1D_max_dd_nodes": max(r["dd_active_vector_nodes"] for r in lin),
        "C3_2D_max_qubits_tested": max(r["n_qubits"] for r in grid),
        "C3_2D_max_dd_nodes": max(r["dd_active_vector_nodes"] for r in grid),
    }
    (EVID / "summary.json").write_text(json.dumps(summary, indent=2))
    print("\n== Summary ==")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
