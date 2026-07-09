#!/usr/bin/env python3
"""
Replication of Weinstein/Lloyd/Cory (1999), quant-ph/9906059,
"Implementation of the Quantum Fourier Transform."

We reproduce the Coppersmith decomposition of the QFT that the paper builds on:
  - A_j  = Hadamard on qubit j                                (paper Eq. 5)
  - B_jk = controlled-phase(theta_jk),  theta_jk = pi/2^(k-j)  (paper Eq. 6)
For an L-qubit register indexed j = L-1, L-2, ..., 0, apply
  B_{j,j+1} B_{j,j+2} ... B_{j,L-1} A_j                        (paper Eq. 7)
(the paper indexes j from L-1 down to 0). We implement this directly, then
verify against the analytic amplitudes for QFT_q and against Qiskit's own QFT.
"""
from __future__ import annotations
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT as QiskitQFT
from qiskit.quantum_info import Statevector, Operator


def coppersmith_qft(n: int, do_swaps: bool = True) -> QuantumCircuit:
    """Build the QFT via the Coppersmith decomposition used in the paper.

    We use Qiskit's little-endian convention (qubit 0 = LSB). The paper writes
    j = L-1..0 as the "lead bit"; that is the standard Coppersmith recursion.
    """
    qc = QuantumCircuit(n, name=f"QFT{n}")
    # Apply H on qubit j, then controlled-phase from every lower-index target
    # onto qubit j with angle pi/2^(j-target).  (Little-endian: qubit n-1 is MSB.)
    for j in reversed(range(n)):        # j = n-1, n-2, ..., 0  (== paper's L-1..0)
        qc.h(j)                         # A_j
        for k in reversed(range(j)):    # k = j-1, j-2, ..., 0
            theta = np.pi / (2 ** (j - k))    # matches theta_jk = pi/2^(k-j) after relabel
            qc.cp(theta, k, j)          # B_{j,k}
    if do_swaps:
        for i in range(n // 2):
            qc.swap(i, n - 1 - i)
    return qc


def analytic_qft_amplitudes(x: int, n: int) -> np.ndarray:
    """(1/sqrt(2^n)) * sum_y exp(2 pi i x y / 2^n) |y>  (paper Eq. 1/3)."""
    q = 2 ** n
    y = np.arange(q)
    amps = np.exp(2j * np.pi * x * y / q) / np.sqrt(q)
    return amps


def count_gates(qc: QuantumCircuit) -> dict:
    counts = dict(qc.count_ops())
    return counts


def verify_correctness(n: int) -> dict:
    """Apply QFT_n to every computational-basis input, compare to analytic."""
    qft = coppersmith_qft(n, do_swaps=True)
    q = 2 ** n
    max_err = 0.0
    per_x_err = []
    for x in range(q):
        # Prepare |x> in little-endian: bit i is (x >> i) & 1
        init = QuantumCircuit(n)
        for i in range(n):
            if (x >> i) & 1:
                init.x(i)
        full = init.compose(qft)
        sv = Statevector.from_instruction(full).data
        # Qiskit statevector index k has qubit 0 as LSB, so index k corresponds
        # to computational-basis element |k> in the standard ordering used by
        # the analytic formula.
        analytic = analytic_qft_amplitudes(x, n)
        err = float(np.max(np.abs(sv - analytic)))
        per_x_err.append(err)
        if err > max_err:
            max_err = err
    return {
        "n": n,
        "num_inputs_checked": q,
        "max_abs_amplitude_error": max_err,
        "matches_analytic_to_machine_precision": max_err < 1e-10,
        "per_x_max_error_sample": per_x_err[:8],
    }


def verify_paper_eq4_matrix() -> dict:
    """QFT_4 (2-qubit) matrix from paper Eq. 4 vs our circuit."""
    qft2 = coppersmith_qft(2, do_swaps=True)
    U = Operator(qft2).data
    paper_U = 0.5 * np.array([
        [1,  1,  1,  1],
        [1, 1j, -1, -1j],
        [1, -1,  1, -1],
        [1, -1j, -1, 1j],
    ], dtype=complex)
    err = float(np.max(np.abs(U - paper_U)))
    return {
        "check": "paper Eq. 4 QFT_4 matrix",
        "max_abs_matrix_error_vs_paper_eq4": err,
        "matches_paper_eq4": err < 1e-10,
        "our_matrix_real": U.real.tolist(),
        "our_matrix_imag": U.imag.tolist(),
        "paper_matrix_real": paper_U.real.tolist(),
        "paper_matrix_imag": paper_U.imag.tolist(),
    }


def verify_gate_count_claim(n: int) -> dict:
    """Paper's Coppersmith decomposition implies:
        - n Hadamards (one per qubit, A_j)
        - n(n-1)/2 controlled-phase gates (B_jk for each pair j<k)
    We build WITHOUT swaps (swaps are a bit-reversal convention, not counted
    in the Coppersmith gate-count claim itself) and check.
    """
    qc = coppersmith_qft(n, do_swaps=False)
    counts = count_gates(qc)
    n_h = counts.get("h", 0)
    n_cp = counts.get("cp", 0)
    expected_h = n
    expected_cp = n * (n - 1) // 2
    return {
        "n": n,
        "hadamards_measured": n_h,
        "hadamards_expected": expected_h,
        "hadamards_match": n_h == expected_h,
        "controlled_phase_measured": n_cp,
        "controlled_phase_expected": expected_cp,
        "controlled_phase_match": n_cp == expected_cp,
        "total_two_qubit_measured": n_cp,
        "asymptotic": "O(n^2)  (paper Eq. 7 structure)",
        "gate_ops": counts,
    }


def compare_to_qiskit_builtin(n: int) -> dict:
    """Sanity: our circuit == qiskit.circuit.library.QFT up to global phase."""
    ours = Operator(coppersmith_qft(n, do_swaps=True)).data
    ref = Operator(QiskitQFT(n, do_swaps=True)).data
    # allow global phase
    ratio = ours / np.where(np.abs(ref) > 1e-10, ref, 1)
    phases = ratio[np.abs(ref) > 1e-10]
    max_dev = float(np.max(np.abs(phases - phases[0])))
    err = float(np.max(np.abs(ours - phases[0] * ref)))
    return {
        "n": n,
        "matches_qiskit_QFT_up_to_global_phase": err < 1e-10,
        "max_abs_error_after_global_phase": err,
        "phase_variation": max_dev,
    }


def anchor_test_case() -> dict:
    """The paper says (page 4) it applies the QFT to the diagonal (thermal)
    starting state Iz1 + Iz2 + Iz3 on a 3-qubit register, and shows selected
    spectra.  That is an NMR density-matrix statement, not a pure-state one.
    As an *ideal-statevector anchor*, we instead pick QFT_3|000> (the uniform
    superposition, since e^{2 pi i * 0 * y / 8} = 1) and QFT_3|001>, and check
    they match the analytic formula bit-for-bit.
    """
    qft3 = coppersmith_qft(3, do_swaps=True)
    out = {}
    for x in (0, 1, 3, 7):
        init = QuantumCircuit(3)
        for i in range(3):
            if (x >> i) & 1:
                init.x(i)
        sv = Statevector.from_instruction(init.compose(qft3)).data
        analytic = analytic_qft_amplitudes(x, 3)
        out[f"x={x}"] = {
            "amplitudes_real": sv.real.tolist(),
            "amplitudes_imag": sv.imag.tolist(),
            "analytic_real": analytic.real.tolist(),
            "analytic_imag": analytic.imag.tolist(),
            "max_abs_error_vs_analytic": float(np.max(np.abs(sv - analytic))),
        }
    return out


def main():
    results = {"claims": {}}

    # C1/C2: Coppersmith gate structure + count
    results["claims"]["C1_gate_structure_and_count"] = {
        n: verify_gate_count_claim(n) for n in (3, 4, 5)
    }

    # C3: correctness against analytic formula (n = 3, 4, 5)
    results["claims"]["C3_analytic_correctness"] = {
        n: verify_correctness(n) for n in (3, 4, 5)
    }

    # Paper Eq. 4: explicit QFT_4 matrix
    results["claims"]["C4_paper_eq4_matrix"] = verify_paper_eq4_matrix()

    # Sanity vs Qiskit's own QFT
    results["claims"]["S_vs_qiskit_builtin"] = {
        n: compare_to_qiskit_builtin(n) for n in (3, 4, 5)
    }

    # 3-qubit anchor case
    results["claims"]["anchor_3qubit_selected_inputs"] = anchor_test_case()

    # Print sequence of gates for QFT_3 (matches Coppersmith)
    qc3 = coppersmith_qft(3, do_swaps=False)
    results["QFT3_gate_sequence"] = [
        (instr.name, [q._index for q in qargs], [float(p) for p in instr.params])
        for instr, qargs, _ in qc3.data
    ]

    with open("report/evidence/results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Human-readable summary
    print("=" * 72)
    print("Weinstein/Lloyd/Cory 1999 (quant-ph/9906059)  —  QFT replication")
    print("=" * 72)
    for n in (3, 4, 5):
        gc = results["claims"]["C1_gate_structure_and_count"][n]
        cc = results["claims"]["C3_analytic_correctness"][n]
        sc = results["claims"]["S_vs_qiskit_builtin"][n]
        print(f"n={n}:  H={gc['hadamards_measured']}/{gc['hadamards_expected']}"
              f"  CP={gc['controlled_phase_measured']}/{gc['controlled_phase_expected']}"
              f"  max amp err={cc['max_abs_amplitude_error']:.2e}"
              f"  vs Qiskit err={sc['max_abs_error_after_global_phase']:.2e}")
    eq4 = results["claims"]["C4_paper_eq4_matrix"]
    print(f"Eq. 4 QFT_4 matrix: match={eq4['matches_paper_eq4']}  "
          f"err={eq4['max_abs_matrix_error_vs_paper_eq4']:.2e}")


if __name__ == "__main__":
    main()
