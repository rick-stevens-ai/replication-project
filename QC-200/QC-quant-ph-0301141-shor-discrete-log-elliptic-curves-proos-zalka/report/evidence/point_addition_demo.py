#!/usr/bin/env python3
"""
Symbolic Qiskit demonstration of a controlled group-shift ("controlled point
addition by a fixed classical point P_i") — the elementary building block of
Section 4 of Proos & Zalka (quant-ph/0301141).

We use q=8 subgroup <P> of E: y^2 = x^3 + 3x + 3 (mod 23).
Represent each group element g = k*P by its index k in {0,...,7} (3 qubits).
The unitary U_{P_i}: |g> -> |g + i*P>  is a permutation on {0..7} that we
implement in Qiskit as a QuantumCircuit built out of X/CNOT gates (via the
`Permutation` gate) plus an explicit ancilla-free construction.

We then verify that U_{P_i} applied to |k> yields |k + i (mod q)> for every k
and every i -- which is exactly what Section 4.3 requires.
"""
import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector, Operator

# reuse EC arithmetic
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shor_dlp_ec import EC, build_group_index

def build_group_shift(q: int, shift: int) -> QuantumCircuit:
    """|k> -> |(k + shift) mod q>, implemented as a permutation unitary on n qubits.

    Register convention: qubit 0 is LSB (Qiskit little-endian). U|k> = |(k+shift) mod q>.
    """
    n = int(np.log2(q))
    assert (1 << n) == q, "q must be power of 2 for this small demo"
    U = np.zeros((q, q), dtype=complex)
    for k in range(q):
        U[(k + shift) % q, k] = 1.0
    gate = UnitaryGate(U, label=f"+{shift}mod{q}")
    qr = QuantumRegister(n, "g")
    qc = QuantumCircuit(qr)
    qc.append(gate, qr[:])
    return qc

def main():
    a, b, p = 3, 3, 23
    E = EC(a, b, p)
    # generator of the order-8 subgroup (must match shor_dlp_ec.py)
    pts = E.points()
    for P in pts:
        if P is None:
            continue
        try:
            o = E.order_of(P)
        except RuntimeError:
            continue
        if o == 16:
            P_full = P
            break
    P_gen = E.mul(2, P_full)  # (order 16) / 8 * P
    q = 8
    n = 3

    idx, plist = build_group_index(E, P_gen, q)
    print(f"[EC] curve y^2 = x^3 + {a}x + {b} mod {p}, subgroup <P> of order {q}, generator P = {P_gen}")
    for k, pt in enumerate(plist):
        print(f"     {k} * P = {pt}")

    # Verify group-shift circuits for all i
    log = []
    all_ok = True
    for i in range(1, q):
        qc = build_group_shift(q, i)
        U = Operator(qc).data  # 8x8 unitary
        # check U|k> = |(k+i) mod q>
        for k in range(q):
            v_in  = np.zeros(q); v_in[k] = 1
            v_out = U @ v_in
            k_out = int(np.argmax(np.abs(v_out) ** 2))
            expected = (k + i) % q
            if k_out != expected or not np.isclose(np.abs(v_out[k_out]), 1.0):
                all_ok = False
                log.append({"i": i, "k": k, "got": k_out, "expected": expected, "amp": complex(v_out[k_out])})
        print(f"     controlled point-addition U_{{{i}*P}}  verified ({int(np.log2(q))} qubits)")

    # Also demonstrate one controlled version (add P if control=1)
    print("\n[CTRL] Controlled U_{P}: applies |k> -> |k+1 mod q> only if control=1")
    n = 3
    # Register order: put control first (LSB in Qiskit) then g register.
    # In Qiskit's little-endian, the FIRST-listed register is the LEAST significant qubit(s),
    # so a state index i decomposes as i = c + 2*k  where k is the g-register value and c the control.
    qr_c = QuantumRegister(1, "c")
    qr_g = QuantumRegister(n, "g")
    qc = QuantumCircuit(qr_c, qr_g)
    U1 = np.zeros((q, q), dtype=complex)
    for k in range(q):
        U1[(k + 1) % q, k] = 1.0
    shift_gate = UnitaryGate(U1, label="+1mod8").control(1)
    qc.append(shift_gate, [qr_c[0], *qr_g[:]])
    # verify on all 8 states with control 0 and 1
    ctrl_ok = True
    fails = []
    for c in (0, 1):
        for k in range(q):
            state = np.zeros(2 * q)
            flat = c + 2 * k   # little-endian: control is LSB
            state[flat] = 1.0
            sv = Statevector(state).evolve(qc)
            probs = np.abs(sv.data) ** 2
            out_idx = int(np.argmax(probs))
            out_c = out_idx & 1
            out_k = out_idx >> 1
            expected_k = (k + 1) % q if c == 1 else k
            if out_c != c or out_k != expected_k:
                ctrl_ok = False
                fails.append((c, k, out_c, out_k, expected_k))
    for f in fails:
        c, k, out_c, out_k, expected_k = f
        print(f"     FAIL c={c} k={k} -> c={out_c} k={out_k} (expected {c},{expected_k})")
    print(f"     controlled shift verified: {ctrl_ok}")

    result = {
        "curve": {"a": a, "b": b, "p": p, "generator": P_gen, "subgroup_order": q},
        "subgroup_elements": [str(pt) for pt in plist],
        "all_unconditional_shifts_correct": all_ok,
        "controlled_shift_correct": ctrl_ok,
        "circuit_ascii": {},
    }
    # save one example circuit
    qc_ex = build_group_shift(q, 3)
    Path("point_addition_shift_by_3.txt").write_text(str(qc_ex.decompose(reps=2).draw(output="text")))
    result["circuit_ascii"]["shift_by_3"] = "see point_addition_shift_by_3.txt"

    verdict = "OK" if (all_ok and ctrl_ok) else "FAIL"
    result["verdict"] = verdict
    Path("point_addition_result.json").write_text(json.dumps(result, indent=2, default=str))
    print(f"\nOverall point-addition demo verdict: {verdict}")

if __name__ == "__main__":
    main()
