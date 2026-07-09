#!/usr/bin/env python3
"""
Shor's algorithm for N=21 using generic QPE + unitary permutation for x^k mod 21.
We pick x=2 (gcd(2,21)=1, order 6) and x=4 (order 3).  With n_count=8-10 phase
qubits we should see peaks at multiples of 2^n_count / r.

This is not from the paper directly, but the brief asked for "N=15 and 21
if feasible" for the resource-count comparison.
"""
import math
from fractions import Fraction

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT, UnitaryGate


def perm_matrix(xp, N, bits):
    dim = 2 ** bits
    P = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if 1 <= y < N and math.gcd(y, N) == 1:
            new_y = (xp * y) % N
        else:
            new_y = y
        P[new_y, y] = 1.0
    return P


def shor_qpe(x, N, n_count=8, n_target=5, shots=8000):
    q_count = QuantumRegister(n_count, 'c')
    q_target = QuantumRegister(n_target, 't')
    c_count = ClassicalRegister(n_count, 'm')
    qc = QuantumCircuit(q_count, q_target, c_count)

    for i in range(n_count):
        qc.h(q_count[i])
    qc.x(q_target[0])  # initial |1>

    for j in range(n_count):
        xp = pow(x, 2 ** j, N)
        P = perm_matrix(xp, N, n_target)
        U = UnitaryGate(P, label=f"x^{2**j}").control(1)
        qc.append(U, [q_count[j]] + list(q_target))

    qc.append(QFT(num_qubits=n_count, inverse=True, do_swaps=True).to_gate(), q_count)
    qc.measure(q_count, c_count)

    sim = AerSimulator(method="statevector")
    t = transpile(qc, sim)
    counts = sim.run(t, shots=shots).result().get_counts()
    return counts


def analyse(counts, N, x, n_count):
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:10]
    print(f"  N={N}, x={x}, n_count={n_count}: top 10:")
    for k, c in top:
        y = int(k, 2)
        f = Fraction(y, 2 ** n_count).limit_denominator(N)
        print(f"    y={y:4d}  count={c:4d}  y/{2**n_count} = {y/2**n_count:.4f} -> {f}")
    for k, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        y = int(k, 2)
        if y == 0:
            continue
        frac = Fraction(y, 2 ** n_count).limit_denominator(N)
        r = frac.denominator
        if r % 2 == 0:
            f1 = math.gcd(pow(x, r // 2, N) - 1, N)
            f2 = math.gcd(pow(x, r // 2, N) + 1, N)
            if 1 < f1 < N and 1 < f2 < N:
                print(f"  --> Recovered r={r} from y={y}; factors of {N} = ({f1},{f2})")
                return r, (f1, f2)
    return None, None


if __name__ == "__main__":
    print("=== N=21, x=2 (order 6) ===")
    c = shor_qpe(2, 21, n_count=8, n_target=5)
    analyse(c, 21, 2, 8)

    print("\n=== N=21, x=4 (order 3) ===")
    c = shor_qpe(4, 21, n_count=8, n_target=5)
    analyse(c, 21, 4, 8)

    print("\n=== N=15, x=2 (order 4) as second cross-check ===")
    c = shor_qpe(2, 15, n_count=8, n_target=4)
    analyse(c, 15, 2, 8)
