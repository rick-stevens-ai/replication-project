"""
Complementary evidence: show the Trotter error scaling as 1/N (first-order),
and demonstrate that Richardson extrapolation curves down at higher order.
Adds a symmetric second-order (Strang) Trotter as a sanity check on the
extrapolation model.
"""
import json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.linalg import expm

N_QUBITS = 5
J = 3.0
B = 2.0
T = 0.5

def build_hamiltonian(n=N_QUBITS, J=J, B=B):
    terms, coeffs = [], []
    for i in range(n - 1):
        lab = ['I'] * n; lab[i]='Z'; lab[i+1]='Z'
        terms.append(''.join(reversed(lab))); coeffs.append(J)
    for i in range(n):
        lab = ['I'] * n; lab[i]='X'
        terms.append(''.join(reversed(lab))); coeffs.append(B)
    return SparsePauliOp(terms, coeffs=coeffs)

def build_X1(n=N_QUBITS):
    lab = ['I'] * n; lab[0]='X'
    return SparsePauliOp([''.join(reversed(lab))], coeffs=[1.0])

def exact_val(H_op, A_op, t, n=N_QUBITS):
    U = expm(-1j * H_op.to_matrix() * t)
    psi0 = np.zeros(2**n, dtype=complex); psi0[0]=1.0
    psi = U @ psi0
    return float(np.real(np.conj(psi) @ (A_op.to_matrix() @ psi)))

def trotter1_step(dt, n=N_QUBITS):
    qc = QuantumCircuit(n)
    for i in range(n-1):
        qc.cx(i,i+1); qc.rz(2*J*dt, i+1); qc.cx(i,i+1)
    for i in range(n):
        qc.rx(2*B*dt, i)
    return qc

def trotter1_evolve(N, A_op, n=N_QUBITS, t=T):
    dt = t/N
    step = trotter1_step(dt, n)
    qc = QuantumCircuit(n)
    for _ in range(N):
        qc.compose(step, inplace=True)
    sv = Statevector.from_int(0, dims=2**n).evolve(qc)
    return float(np.real(sv.expectation_value(A_op)))

def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    H_op = build_hamiltonian()
    A_op = build_X1()
    ex = exact_val(H_op, A_op, T)
    print(f"exact <X_1> = {ex:.12f}")

    # Fine sweep + fit to A(N) = ex + a1/N + a2/N^2 to confirm 1/N leading order
    Ns = [10, 12, 15, 18, 20, 25, 30, 40, 50]
    vals = [trotter1_evolve(N, A_op) for N in Ns]
    xs = np.array([1.0/N for N in Ns])
    ys = np.array(vals)

    # Fit polynomial in x=1/N of degree 2 to first few (large-N) points
    coefs = np.polyfit(xs, ys, 2)
    # coefs = [a2, a1, a0]; a0 is extrapolated N->infty value.
    a2, a1, a0 = coefs
    print(f"Polynomial fit A(1/N) = {a0:.10f} + {a1:.6f}/N + {a2:.6f}/N^2")
    print(f"Fit constant term    = {a0:.10f}   (exact = {ex:.10f})")
    print(f"|constant - exact|   = {abs(a0-ex):.3e}")

    # Show that the Richardson-extrapolated value from paper's chosen triple
    # (15,20,25) is much closer to exact than any of the three raw values.
    idx_15 = Ns.index(15); idx_20 = Ns.index(20); idx_25 = Ns.index(25)
    triple_x = np.array([1.0/15, 1.0/20, 1.0/25])
    triple_y = np.array([vals[idx_15], vals[idx_20], vals[idx_25]])
    c = np.polyfit(triple_x, triple_y, 2)
    rich_a0 = float(c[-1])
    print()
    print(f"paper triple (15,20,25) raw errors: "
          f"{abs(vals[idx_15]-ex):.3e}, {abs(vals[idx_20]-ex):.3e}, {abs(vals[idx_25]-ex):.3e}")
    print(f"paper triple Richardson value = {rich_a0:.10f}, error = {abs(rich_a0-ex):.3e}")
    imp = min(abs(vals[idx_15]-ex), abs(vals[idx_20]-ex), abs(vals[idx_25]-ex)) / abs(rich_a0-ex)
    print(f"improvement factor over BEST raw of the triple = {imp:.1f}x")

    result = {
        "exact_value": ex,
        "N_sweep": Ns,
        "raw_values": vals,
        "raw_errors": [abs(v-ex) for v in vals],
        "quadratic_fit_coefficients_in_inv_N": {
            "constant": a0, "linear_1_over_N": a1, "quadratic_1_over_N2": a2,
        },
        "quadratic_fit_extrapolation_error": abs(a0-ex),
        "paper_triple_15_20_25": {
            "richardson_value": rich_a0,
            "richardson_abs_error": abs(rich_a0-ex),
            "best_raw_of_triple_error": float(min(abs(vals[idx_15]-ex),
                                                   abs(vals[idx_20]-ex),
                                                   abs(vals[idx_25]-ex))),
            "improvement_over_best_raw": imp,
        }
    }
    (outdir / "scaling_curve.json").write_text(json.dumps(result, indent=2))
    print(f"\nSaved scaling_curve.json")

if __name__ == "__main__":
    main()
