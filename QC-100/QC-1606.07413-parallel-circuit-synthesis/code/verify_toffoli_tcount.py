#!/usr/bin/env python3
"""
Verify claim C1/C2 of Di Matteo & Mosca (arXiv:1606.07413):
Toffoli, Fredkin, Peres, Quantum OR, Negated Toffoli all have T-count 7
when decomposed over Clifford+T.

We verify by:
  1. Constructing each 3-qubit target unitary explicitly.
  2. Applying the canonical Clifford+T decomposition (Nielsen-Chuang / standard).
  3. Counting the number of T and T-dagger gates and checking correctness
     of the decomposition (unitary equivalence).

Reference decompositions (all with T-count 7):
  Toffoli via {H, CNOT, T, T†, S} — the canonical 6 CNOT + 7 T decomposition
  from Nielsen & Chuang §4.3 / Barenco et al 1995.
"""

import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.circuit.library import CCXGate, CSwapGate

def canonical_toffoli_clifford_t():
    """The standard 7-T decomposition of Toffoli (control control target = q0 q1 q2)."""
    qc = QuantumCircuit(3, name='toffoli_ct')
    qc.h(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(1); qc.t(2)
    qc.cx(0, 1)
    qc.h(2)
    qc.t(0); qc.tdg(1)
    qc.cx(0, 1)
    return qc

def fredkin_from_toffoli():
    """Fredkin (CSWAP) = CNOT_{2,1} · CCNOT_{0,1,2} · CNOT_{2,1}.
    T-count same as Toffoli since CNOT is Clifford.
    """
    qc = QuantumCircuit(3, name='fredkin')
    qc.cx(2, 1)
    qc.compose(canonical_toffoli_clifford_t(), inplace=True)
    qc.cx(2, 1)
    return qc

def peres_from_toffoli():
    """Peres gate: Toffoli followed by CNOT(control0, target1).
    Peres(a,b,c) -> (a, a⊕b, ab⊕c). T-count = 7 (only from the Toffoli piece).
    """
    qc = QuantumCircuit(3, name='peres')
    qc.compose(canonical_toffoli_clifford_t(), inplace=True)
    qc.cx(0, 1)
    return qc

def quantum_or_from_toffoli():
    """Quantum OR: negate both controls, Toffoli, negate both controls, negate target.
    (a OR b) = NOT(NOT a AND NOT b).  T-count = 7.
    """
    qc = QuantumCircuit(3, name='qor')
    qc.x(0); qc.x(1)
    qc.compose(canonical_toffoli_clifford_t(), inplace=True)
    qc.x(0); qc.x(1); qc.x(2)
    return qc

def negated_toffoli_from_toffoli():
    """Negated Toffoli: X on target then Toffoli — same T-count."""
    qc = QuantumCircuit(3, name='ntof')
    qc.x(2)
    qc.compose(canonical_toffoli_clifford_t(), inplace=True)
    return qc

def count_t_gates(qc):
    """Count T and Tdg gates in a circuit."""
    t_count = 0
    for inst in qc.data:
        name = inst.operation.name.lower()
        if name in ('t', 'tdg'):
            t_count += 1
    return t_count

def verify_unitary_equivalence(qc, target_gate):
    """Check qc implements target_gate up to global phase."""
    U_qc = Operator(qc).data
    U_target = Operator(target_gate).data
    # Global phase equivalence: U_qc = e^{i phi} U_target
    # ratio should be a scalar of unit modulus, equal across all nonzero entries
    ratio = None
    for i in range(U_qc.shape[0]):
        for j in range(U_qc.shape[1]):
            if abs(U_target[i, j]) > 1e-9:
                r = U_qc[i, j] / U_target[i, j]
                if ratio is None:
                    ratio = r
                else:
                    if abs(r - ratio) > 1e-6:
                        return False, None
    return (ratio is not None and abs(abs(ratio) - 1.0) < 1e-6), ratio

def swap_gate():
    qc = QuantumCircuit(3)
    qc.swap(1, 2)  # controlled by qubit 0 for CSWAP
    return qc

def main():
    results = []

    # Reference: canonical Toffoli decomposition
    tof = canonical_toffoli_clifford_t()
    ok, phase = verify_unitary_equivalence(tof, CCXGate())
    tc = count_t_gates(tof)
    results.append({
        'circuit': 'Toffoli',
        'paper_t_count': 7,
        'measured_t_count': tc,
        'unitary_correct': bool(ok),
        'global_phase': f"{phase.real:+.4f}{phase.imag:+.4f}j" if phase is not None else None,
        'match': tc == 7 and bool(ok),
    })

    # Fredkin
    frd = fredkin_from_toffoli()
    ok, phase = verify_unitary_equivalence(frd, CSwapGate())
    tc = count_t_gates(frd)
    results.append({
        'circuit': 'Fredkin',
        'paper_t_count': 7,
        'measured_t_count': tc,
        'unitary_correct': bool(ok),
        'match': tc == 7 and bool(ok),
    })

    # Peres, Q-OR, negated Toffoli: verify T-count = 7 and unitary matches expected truth table
    for name, ctor, spec in [
        ('Peres', peres_from_toffoli, lambda a, b, c: (a, a ^ b, (a & b) ^ c)),
        ('QuantumOR', quantum_or_from_toffoli, lambda a, b, c: (a, b, c ^ (a | b))),
        ('NegatedToffoli', negated_toffoli_from_toffoli, lambda a, b, c: (a, b, c ^ (1 ^ (a & b)))),
    ]:
        qc = ctor()
        tc = count_t_gates(qc)
        # Build target unitary from truth table (order: qubit 0 is LSB in Qiskit)
        U_target = np.zeros((8, 8), dtype=complex)
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    ap, bp, cp = spec(a, b, c)
                    # Qiskit basis state |q2 q1 q0>: index = q2*4 + q1*2 + q0
                    in_idx = c * 4 + b * 2 + a
                    out_idx = cp * 4 + bp * 2 + ap
                    U_target[out_idx, in_idx] = 1.0
        U_qc = Operator(qc).data
        # Global-phase equivalence
        ratio = None
        ok = True
        for i in range(8):
            for j in range(8):
                if abs(U_target[i, j]) > 1e-9:
                    r = U_qc[i, j] / U_target[i, j]
                    if ratio is None:
                        ratio = r
                    elif abs(r - ratio) > 1e-6:
                        ok = False
                        break
            if not ok:
                break
        ok = ok and (ratio is not None) and abs(abs(ratio) - 1.0) < 1e-6
        results.append({
            'circuit': name,
            'paper_t_count': 7,
            'measured_t_count': tc,
            'unitary_correct': bool(ok),
            'match': tc == 7 and bool(ok),
        })

    print(json.dumps(results, indent=2))

    # Summary
    all_match = all(r['match'] for r in results)
    print("\n=== SUMMARY ===")
    print(f"All 5 circuits have T-count 7 and correct unitaries: {all_match}")
    return results, all_match

if __name__ == '__main__':
    results, ok = main()
    import sys
    with open('report/evidence/tcount_verification.json', 'w') as f:
        json.dump({'results': results, 'all_match': ok}, f, indent=2)
    sys.exit(0 if ok else 1)
