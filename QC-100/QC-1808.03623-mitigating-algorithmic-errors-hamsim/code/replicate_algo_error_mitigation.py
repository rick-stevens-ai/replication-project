"""
Independent replication of key algorithmic-error-mitigation result of
Endo, Zhao, Li, Benjamin, Yuan, arXiv:1808.03623 (2018).

Paper setup (Sec. V, Fig. 1):
  H = J * sum_{i=1..n-1} Z_i Z_{i+1}  +  B * sum_{i=1..n} X_i
  J = 3, B = 2, t = 0.5, initial state |0...0>, observable A = X_1.
  Paper uses n = 5 qubits; we reproduce with n = 5 (small, no HPC needed).

Core mitigation idea (Sec. IV):
  For first-order Trotter, <A>(N) = <A>_exact + a1 / N + a2 / N^2 + ...
  With two step counts N1 < N2, linear extrapolation removes the 1/N term:
    <A>_lin_extrap = (N2 * <A>(N2) - N1 * <A>(N1)) / (N2 - N1)
  With three step counts N1 < N2 < N3, Richardson-style fit of a polynomial
  in 1/N of degree 2 (three unknowns: <A>_exact, a1, a2) removes 1/N AND 1/N^2.

This script computes:
  - exact evolution via full Hamiltonian exponentiation (reference truth)
  - Trotter statevector evolution for a range of N
  - raw Trotter error |<A>(N) - <A>_exact| for each N
  - linear (2-point) Richardson error at (N1,N2)=(15,25)  [paper Fig. 3 values]
  - three-point Richardson error at (N1,N2,N3)=(15,20,25) [paper Fig. 3 values]

No gate noise: this replication targets the *algorithmic* error result
(pure Trotter error mitigation), which is the paper's Section-IV / Fig.-3
central technical contribution.
"""

import json
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp, Operator
from scipy.linalg import expm

# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------
N_QUBITS = 5
J = 3.0
B = 2.0
T = 0.5

def build_hamiltonian(n=N_QUBITS, J=J, B=B):
    """H = J * sum Z_i Z_{i+1} + B * sum X_i  (open chain)."""
    terms = []
    coeffs = []
    # ZZ terms
    for i in range(n - 1):
        label = ['I'] * n
        label[i] = 'Z'
        label[i + 1] = 'Z'
        # Qiskit Pauli labels: qubit 0 is the RIGHTMOST character.
        terms.append(''.join(reversed(label)))
        coeffs.append(J)
    # X terms
    for i in range(n):
        label = ['I'] * n
        label[i] = 'X'
        terms.append(''.join(reversed(label)))
        coeffs.append(B)
    return SparsePauliOp(terms, coeffs=coeffs)

def build_observable_X1(n=N_QUBITS):
    """A = X_1 acting on qubit index 0 (first qubit)."""
    label = ['I'] * n
    label[0] = 'X'
    return SparsePauliOp([''.join(reversed(label))], coeffs=[1.0])

# ---------------------------------------------------------------------------
# Exact reference
# ---------------------------------------------------------------------------
def exact_expectation(H_op, A_op, t, n=N_QUBITS):
    H_mat = H_op.to_matrix()
    U = expm(-1j * H_mat * t)
    psi0 = np.zeros(2 ** n, dtype=complex)
    psi0[0] = 1.0
    psi_t = U @ psi0
    A_mat = A_op.to_matrix()
    return float(np.real(np.conj(psi_t) @ (A_mat @ psi_t)))

# ---------------------------------------------------------------------------
# First-order Trotter step: U_step = ( prod_k exp(-i H_k dt) ), then repeat N.
# We split H into ZZ pairs and single-qubit X terms.
# ---------------------------------------------------------------------------
def trotter_step_circuit(dt, n=N_QUBITS, J=J, B=B):
    qc = QuantumCircuit(n)
    # ZZ evolution via CNOT-Rz-CNOT decomposition:
    # exp(-i J dt Z_i Z_{i+1}) = CNOT(i,i+1) . Rz(2 J dt on i+1) . CNOT(i,i+1)
    for i in range(n - 1):
        qc.cx(i, i + 1)
        qc.rz(2.0 * J * dt, i + 1)
        qc.cx(i, i + 1)
    # X evolution: exp(-i B dt X_i) = Rx(2 B dt on i)
    for i in range(n):
        qc.rx(2.0 * B * dt, i)
    return qc

def trotter_evolution_expectation(N, t=T, n=N_QUBITS, J=J, B=B, A_op=None):
    """Apply first-order Trotter with N steps, statevector, return <X_1>."""
    dt = t / N
    step = trotter_step_circuit(dt, n, J, B)
    qc = QuantumCircuit(n)
    for _ in range(N):
        qc.compose(step, inplace=True)
    sv = Statevector.from_int(0, dims=2 ** n).evolve(qc)
    val = sv.expectation_value(A_op)
    return float(np.real(val))

# ---------------------------------------------------------------------------
# Richardson-style extrapolation in 1/N
# ---------------------------------------------------------------------------
def linear_richardson_2pt(N1, N2, A1, A2):
    """Assume A(N) = A_exact + a1 / N. Solve for A_exact."""
    return (N2 * A2 - N1 * A1) / (N2 - N1)

def poly_richardson(Ns, As, degree):
    """Fit A(N) = A_exact + a1 x + a2 x^2 + ... in x=1/N, degree = order.
    Number of points = degree + 1. Returns A_exact (constant term)."""
    xs = np.array([1.0 / N for N in Ns], dtype=float)
    ys = np.array(As, dtype=float)
    # numpy.polyfit fits highest-degree first; constant term is coef[-1]
    coefs = np.polyfit(xs, ys, degree)
    return float(coefs[-1])

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    H_op = build_hamiltonian()
    A_op = build_observable_X1()

    t0 = time.time()
    exact_val = exact_expectation(H_op, A_op, T)
    t_exact = time.time() - t0

    print(f"[exact] <X_1>(t={T}) = {exact_val:.12f}   (computed in {t_exact:.3f}s)")

    # Sweep N values (paper Fig. 2 uses N in [10, 200]; Fig. 3 mitigation uses
    # N triple (25,20,15) and linear pair (25,15)).  We evaluate a wide sweep
    # so we can also show the raw error curve.
    N_sweep = [5, 8, 10, 12, 15, 18, 20, 25, 30, 40, 50, 75, 100, 150, 200]
    sweep = []
    for N in N_sweep:
        t0 = time.time()
        val = trotter_evolution_expectation(N, A_op=A_op)
        dt = time.time() - t0
        err = abs(val - exact_val)
        sweep.append({"N": N, "val": val, "err": err, "sec": dt})
        print(f"[trotter] N={N:4d}  <X_1>={val:.10f}  |err|={err:.3e}  ({dt:.2f}s)")

    # Extract the paper's specific mitigation instances
    val_by_N = {row["N"]: row["val"] for row in sweep}

    # Paper Fig. 3 uses N=(25) alone (no mitigation), (25,15) linear, (25,20,15) 3-point.
    A_N25 = val_by_N[25]
    A_N20 = val_by_N[20]
    A_N15 = val_by_N[15]

    err_no_mit_N25 = abs(A_N25 - exact_val)
    A_lin_25_15 = linear_richardson_2pt(15, 25, A_N15, A_N25)
    err_lin_25_15 = abs(A_lin_25_15 - exact_val)

    A_3pt_25_20_15 = poly_richardson([15, 20, 25], [A_N15, A_N20, A_N25], degree=2)
    err_3pt_25_20_15 = abs(A_3pt_25_20_15 - exact_val)

    # Also try a larger triple (10, 15, 25) purely for visualization of scaling.
    A_N10 = val_by_N[10]
    A_3pt_25_15_10 = poly_richardson([10, 15, 25], [A_N10, A_N15, A_N25], degree=2)
    err_3pt_25_15_10 = abs(A_3pt_25_15_10 - exact_val)

    # And a small-N triple (5, 8, 10) to test at bad-Trotter regime.
    A_N5 = val_by_N[5]
    A_N8 = val_by_N[8]
    err_no_mit_N5 = abs(A_N5 - exact_val)
    err_no_mit_N8 = abs(A_N8 - exact_val)
    err_no_mit_N10 = abs(A_N10 - exact_val)
    A_3pt_10_8_5 = poly_richardson([5, 8, 10], [A_N5, A_N8, A_N10], degree=2)
    err_3pt_10_8_5 = abs(A_3pt_10_8_5 - exact_val)
    A_lin_10_5 = linear_richardson_2pt(5, 10, A_N5, A_N10)
    err_lin_10_5 = abs(A_lin_10_5 - exact_val)

    result = {
        "system": {
            "n_qubits": N_QUBITS, "J": J, "B": B, "t": T,
            "observable": "X_1",
            "initial_state": "|0>^n",
            "hamiltonian": "J * sum Z_i Z_{i+1} (open chain) + B * sum X_i",
        },
        "exact_expectation_X1": exact_val,
        "trotter_sweep": sweep,
        "mitigation_paper_Fig3": {
            "no_mitigation_N25": {"value": A_N25, "abs_error": err_no_mit_N25},
            "linear_2pt_N=(15,25)": {"value": A_lin_25_15, "abs_error": err_lin_25_15},
            "richardson_3pt_N=(15,20,25)": {"value": A_3pt_25_20_15, "abs_error": err_3pt_25_20_15},
            "improvement_linear_over_raw":   err_no_mit_N25 / err_lin_25_15 if err_lin_25_15 > 0 else float("inf"),
            "improvement_3pt_over_raw":      err_no_mit_N25 / err_3pt_25_20_15 if err_3pt_25_20_15 > 0 else float("inf"),
            "improvement_3pt_over_linear":   err_lin_25_15 / err_3pt_25_20_15 if err_3pt_25_20_15 > 0 else float("inf"),
        },
        "mitigation_small_N_regime": {
            "raw_N5":  {"value": A_N5,  "abs_error": err_no_mit_N5},
            "raw_N8":  {"value": A_N8,  "abs_error": err_no_mit_N8},
            "raw_N10": {"value": A_N10, "abs_error": err_no_mit_N10},
            "linear_2pt_N=(5,10)": {"value": A_lin_10_5, "abs_error": err_lin_10_5},
            "richardson_3pt_N=(5,8,10)": {"value": A_3pt_10_8_5, "abs_error": err_3pt_10_8_5},
            "improvement_3pt_over_raw_N10": err_no_mit_N10 / err_3pt_10_8_5 if err_3pt_10_8_5 > 0 else float("inf"),
        },
        "mitigation_wider_triple": {
            "richardson_3pt_N=(10,15,25)": {"value": A_3pt_25_15_10, "abs_error": err_3pt_25_15_10},
            "improvement_over_raw_N25": err_no_mit_N25 / err_3pt_25_15_10 if err_3pt_25_15_10 > 0 else float("inf"),
        },
    }

    outfile = outdir / "results.json"
    outfile.write_text(json.dumps(result, indent=2))
    print(f"\nWrote {outfile}")

    print("\n=========== HEADLINE ============")
    print(f"exact  <X_1> = {exact_val:.10f}")
    print(f"raw N=25     err = {err_no_mit_N25:.3e}")
    print(f"linear (15,25) err = {err_lin_25_15:.3e}    x{err_no_mit_N25/err_lin_25_15:.1f} better than raw")
    print(f"3pt (15,20,25) err = {err_3pt_25_20_15:.3e}    x{err_no_mit_N25/err_3pt_25_20_15:.1f} better than raw")
    print()
    print(f"small-N regime:")
    print(f"raw N=10     err = {err_no_mit_N10:.3e}")
    print(f"3pt (5,8,10) err = {err_3pt_10_8_5:.3e}    x{err_no_mit_N10/err_3pt_10_8_5:.1f} better")
    print("=================================")

if __name__ == "__main__":
    main()
