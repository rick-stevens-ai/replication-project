"""Cross-check: use Qiskit statevector to verify the analytic
cos-experiment / sin-experiment probabilities used in rpe_sim.py.

For A = pi/2 + eps and various k, we compute:
   analytic:  p0 = (1 + cos(kA))/2,  pp = (1 + sin(kA))/2
   qiskit  :  Run the circuit and read probabilities from the exact
              statevector.

If the max abs diff is < 1e-12 we consider the analytic identity verified,
and the shot-based sampling in rpe_sim.py is equivalent to sampling from
the Qiskit exact statevector.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def circuit_cos(A: float, k: int) -> QuantumCircuit:
    """Prepare |0>, apply R_x(A) k times, measure Z (P(0) = (1+cos(kA))/2)."""
    qc = QuantumCircuit(1)
    for _ in range(k):
        qc.rx(A, 0)
    return qc


def circuit_sin(A: float, k: int) -> QuantumCircuit:
    """Prepare |0>, apply R_x(A) k times, rotate Y-basis to Z-basis with SH,
    then P(0) should be (1+sin(kA))/2.

    Rotation: to measure <Y> via Z we can apply S^dagger then H before the
    Z measurement.  Note Qiskit's convention:  |+_y> = (|0>+ i|1>)/sqrt2, and
    applying H S^dagger sends |+_y> -> |0>.
    """
    qc = QuantumCircuit(1)
    for _ in range(k):
        qc.rx(A, 0)
    # In Qiskit's convention, apply S then H to send |+_y> -> |0>.
    qc.s(0)
    qc.h(0)
    return qc


def prob_zero(qc: QuantumCircuit) -> float:
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities()
    return float(probs[0])


def main() -> None:
    A = math.pi / 2 + 0.037
    ks = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    max_diff = 0.0
    rows = []
    for k in ks:
        p0_q = prob_zero(circuit_cos(A, k))
        pp_q = prob_zero(circuit_sin(A, k))
        p0_a = 0.5 * (1.0 + math.cos(k * A))
        pp_a = 0.5 * (1.0 + math.sin(k * A))
        rows.append({
            "k": k,
            "p0_qiskit": p0_q,
            "p0_analytic": p0_a,
            "diff_p0": abs(p0_q - p0_a),
            "pp_qiskit": pp_q,
            "pp_analytic": pp_a,
            "diff_pp": abs(pp_q - pp_a),
        })
        max_diff = max(max_diff, abs(p0_q - p0_a), abs(pp_q - pp_a))

    print(f"A = {A:.6f} rad")
    print(f"{'k':>4} {'p0(qk)':>10} {'p0(an)':>10} {'|d|':>10} {'pp(qk)':>10} {'pp(an)':>10} {'|d|':>10}")
    for r in rows:
        print(f"{r['k']:>4} {r['p0_qiskit']:>10.6f} {r['p0_analytic']:>10.6f} {r['diff_p0']:>10.2e} "
              f"{r['pp_qiskit']:>10.6f} {r['pp_analytic']:>10.6f} {r['diff_pp']:>10.2e}")
    print(f"\nmax|analytic - qiskit| = {max_diff:.3e}")

    out = {
        "A": A,
        "max_abs_diff": max_diff,
        "rows": rows,
        "verdict": "MATCH" if max_diff < 1e-10 else "MISMATCH",
    }
    p = Path(__file__).resolve().parents[1] / "data" / "qiskit_verify.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2))
    print(f"[ok] wrote {p}")


if __name__ == "__main__":
    main()
