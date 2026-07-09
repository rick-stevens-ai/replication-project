"""
Full-truth-table verification of the CDKM adder for n=3,4,5 using
Qiskit statevector simulation. Also emits gate-count comparison to the
paper's Table / final-circuit claim.

Paper claim (optimized circuit, Section 3, n>=2):
    Toffoli: 2n - 1
    CNOT   : 5n - 3
    NOT    : 2n - 4
    Depth  : 2n + 4  (2n-1 Toffoli time-slices + 5 CNOT time-slices)

We validate:
  * Simple adder (Fig 4): correctness on ALL 2^(2n) (a,b) pairs.
  * Optimized adder (Fig 5): correctness on ALL 2^(2n) pairs AND
    gate-count formula match.
"""

import json
import sys
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

sys.path.insert(0, str(Path(__file__).parent))
from cdkm_adder import simple_adder, optimized_adder, count_gates, circuit_depth


def prep_inputs_simple(a, b, z, n):
    """Return a preparation circuit setting X=0, B=b, A=a, Z=z for the simple adder."""
    from qiskit import QuantumRegister

    X = QuantumRegister(1, "X")
    B = QuantumRegister(n, "B")
    A = QuantumRegister(n, "A")
    Z = QuantumRegister(1, "Z")
    prep = QuantumCircuit(X, B, A, Z)
    for i in range(n):
        if (a >> i) & 1:
            prep.x(A[i])
        if (b >> i) & 1:
            prep.x(B[i])
    if z & 1:
        prep.x(Z[0])
    return prep, (X, B, A, Z)


def prep_inputs_opt(a, b, z, n):
    from qiskit import QuantumRegister

    A = QuantumRegister(n, "A")
    B = QuantumRegister(n, "B")
    X = QuantumRegister(1, "X")
    Z = QuantumRegister(1, "Z")
    prep = QuantumCircuit(A, B, X, Z)
    for i in range(n):
        if (a >> i) & 1:
            prep.x(A[i])
        if (b >> i) & 1:
            prep.x(B[i])
    if z & 1:
        prep.x(Z[0])
    return prep, (A, B, X, Z)


def statevector_to_basis_bits(sv):
    """Given a Statevector that is a computational basis state (up to phase),
    return the integer index of the single basis state that carries all amplitude.
    Raises if not a basis state.
    """
    probs = np.abs(sv.data) ** 2
    idx = int(np.argmax(probs))
    if probs[idx] < 1.0 - 1e-9:
        raise ValueError(f"Not a computational basis state: max prob {probs[idx]}")
    return idx


def verify_simple(n):
    """Enumerate all (a,b,z) and check the adder maps to the expected basis state."""
    adder, X, B, A, Z = simple_adder(n)
    N = 2 * n + 2  # total qubit count

    # Qiskit orders qubits by declaration; index 0 is X, then B[0..n-1], A[0..n-1], Z.
    # Statevector int i has bit k for qubit k in little-endian by qubit index in the *circuit*,
    # but Statevector.from_int uses the qubit *label order* consistent with `qc.qubits`.
    # For safety we build inputs by applying X gates and reading Statevector.
    errors = []
    total = 0
    for a in range(2 ** n):
        for b in range(2 ** n):
            for z in (0, 1):
                prep, regs = prep_inputs_simple(a, b, z, n)
                full = prep.compose(adder)
                sv = Statevector.from_instruction(full)
                idx = statevector_to_basis_bits(sv)

                # Decompose idx per qubit ordering: qubit 0 = X, 1..n = B, n+1..2n = A, 2n+1 = Z
                # Statevector integer index has bit k = value of qubit k (little-endian by qubit index).
                bits = [(idx >> k) & 1 for k in range(N)]
                x_out = bits[0]
                b_out = sum(bits[1 + i] << i for i in range(n))
                a_out = sum(bits[1 + n + i] << i for i in range(n))
                z_out = bits[1 + 2 * n]

                exp_sum = (a + b) & ((1 << n) - 1)
                exp_sn = ((a + b) >> n) & 1
                exp_z = z ^ exp_sn
                total += 1
                if (x_out, b_out, a_out, z_out) != (0, exp_sum, a, exp_z):
                    errors.append(
                        dict(a=a, b=b, z=z, got=(x_out, b_out, a_out, z_out),
                             exp=(0, exp_sum, a, exp_z))
                    )
    return total, errors


def verify_optimized(n):
    adder, A, B, X, Z = optimized_adder(n)
    N = 2 * n + 2

    errors = []
    total = 0
    for a in range(2 ** n):
        for b in range(2 ** n):
            for z in (0, 1):
                prep, regs = prep_inputs_opt(a, b, z, n)
                full = prep.compose(adder)
                sv = Statevector.from_instruction(full)
                idx = statevector_to_basis_bits(sv)
                # ordering: A[0..n-1], B[0..n-1], X, Z
                bits = [(idx >> k) & 1 for k in range(N)]
                a_out = sum(bits[i] << i for i in range(n))
                b_out = sum(bits[n + i] << i for i in range(n))
                x_out = bits[2 * n]
                z_out = bits[2 * n + 1]

                exp_sum = (a + b) & ((1 << n) - 1)
                exp_sn = ((a + b) >> n) & 1
                exp_z = z ^ exp_sn
                total += 1
                if (a_out, b_out, x_out, z_out) != (a, exp_sum, 0, exp_z):
                    errors.append(
                        dict(a=a, b=b, z=z, got=(a_out, b_out, x_out, z_out),
                             exp=(a, exp_sum, 0, exp_z))
                    )
    return total, errors


def main(out_path):
    results = {"paper": "arXiv:quant-ph/0410184",
               "circuit": "Cuccaro-Draper-Kutin-Moulton ripple-carry quantum adder",
               "widths_tested": [3, 4, 5],
               "simple_adder": {},
               "optimized_adder": {},
               "gate_count_claim": {"toffoli": "2n-1", "cnot": "5n-3", "not": "2n-4",
                                    "depth": "2n+4"}}

    for n in (3, 4, 5):
        # Simple (Fig 4) — correctness only, gate counts differ (uses UMA_2cnot).
        total_s, errs_s = verify_simple(n)
        adder_s, *_ = simple_adder(n)
        gc_s = count_gates(adder_s)
        d_s = circuit_depth(adder_s)
        results["simple_adder"][f"n={n}"] = {
            "cases_tested": total_s,
            "errors": len(errs_s),
            "gate_counts": gc_s,
            "depth": d_s,
            "first_error_sample": errs_s[:3],
        }
        print(f"[simple n={n}] cases={total_s} errors={len(errs_s)} "
              f"gates={gc_s} depth={d_s}")

    for n in (3, 4, 5):
        if n < 4:
            # Optimized pseudocode is only stated for n>=4 in Figure 5.
            results["optimized_adder"][f"n={n}"] = {
                "note": "Figure 5 pseudocode not defined for n<4; skipped."
            }
            print(f"[opt n={n}] skipped (paper: n>=4 only)")
            continue
        total_o, errs_o = verify_optimized(n)
        adder_o, *_ = optimized_adder(n)
        gc_o = count_gates(adder_o)
        d_o = circuit_depth(adder_o)
        expected = {"toffoli": 2 * n - 1, "cnot": 5 * n - 3, "not": 2 * n - 4,
                    "depth": 2 * n + 4}
        match = {
            "toffoli": gc_o["ccx"] == expected["toffoli"],
            "cnot": gc_o["cx"] == expected["cnot"],
            "not": gc_o["x"] == expected["not"],
        }
        results["optimized_adder"][f"n={n}"] = {
            "cases_tested": total_o,
            "errors": len(errs_o),
            "gate_counts": gc_o,
            "expected_counts": expected,
            "matches_paper_size": match,
            "depth_measured": d_o,
            "depth_expected": expected["depth"],
            "first_error_sample": errs_o[:3],
        }
        print(f"[opt n={n}] cases={total_o} errors={len(errs_o)} "
              f"gates={gc_o} expected={expected} match={match} depth={d_o}")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote results to {out_path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    main(out)
