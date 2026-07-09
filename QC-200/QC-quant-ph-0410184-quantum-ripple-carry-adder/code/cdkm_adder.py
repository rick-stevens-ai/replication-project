"""
Cuccaro-Draper-Kutin-Moulton (CDKM) ripple-carry quantum adder.
arXiv:quant-ph/0410184

Two implementations:
  1) Basic "simple" adder using MAJ + UMA (Figure 4) — works for any n >= 1.
     Registers: X (1 ancilla), B (n), A (n), Z (1) — total 2n+2 qubits.
     Output: A unchanged, B holds low bits of sum, Z holds z XOR s_n.

  2) Optimized adder (Figure 5/6 pseudocode) — valid for n >= 4 per paper.
     Registers: A (n), B (n), X (1 ancilla), Z (1) — total 2n+2 qubits.
     Output identical: A unchanged, B_i = s_i for i<n, Z = z XOR s_n, X restored to 0.

We use the basic (Figure 4) adder as the primary correctness check for n=3,4,5
because the paper explicitly states it works for any n and it directly instantiates
the paper's core construction. We also implement the optimized (Figure 5) adder
for n>=4 to reproduce the size formula 2n-1 Toffoli, 5n-3 CNOT, 2n-4 NOT.
"""

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector


# ---------- MAJ / UMA primitives (Figures 1 and 2b) ----------

def MAJ(qc, c, b, a):
    """In-place majority. On input (c, b, a), leaves (c XOR a, b XOR a, MAJ(a,b,c)).

    Figure 1: two CNOTs then one Toffoli.
    """
    qc.cx(a, b)
    qc.cx(a, c)
    qc.ccx(c, b, a)


def UMA_3cnot(qc, c, b, a):
    """3-CNOT UMA (Figure 2b). Inverse of MAJ effect + writes sum.

    Applied to a wire that currently holds (c XOR a, b XOR a, c_{i+1}).
    After this gate the wires hold (c, s_i = a XOR b XOR c, a).
    """
    # Figure 2(b):  X on the middle wire, CNOT(c->b), Toffoli(c,b,a), X on middle,
    # CNOT(a->c), CNOT(a->b)
    # Reading from Figure 2b carefully (the standard published form):
    qc.x(b)
    qc.cx(c, b)
    qc.ccx(c, b, a)
    qc.x(b)
    qc.cx(a, c)
    qc.cx(a, b)


def UMA_2cnot(qc, c, b, a):
    """2-CNOT UMA (Figure 2a). Cleaner but less parallelizable.

    Reverses the MAJ effect and outputs (c, s_i, a).
    """
    qc.ccx(c, b, a)
    qc.cx(a, c)
    qc.cx(c, b)


# ---------- Simple adder (Figure 4) — any n>=1 ----------

def simple_adder(n):
    """Build the simple CDKM ripple-carry adder for two n-bit numbers.

    Qubit layout (indices, low to high in each block):
        X  : 1 qubit — ancilla holding c_0 = 0
        B  : n qubits — b_0..b_{n-1}, becomes s_0..s_{n-1}
        A  : n qubits — a_0..a_{n-1}, restored
        Z  : 1 qubit  — output, becomes z XOR s_n
    Total 2n+2.

    The registers are declared so index 0 of the returned circuit is X;
    then B[0..n-1] at indices 1..n; A[0..n-1] interleaved with B via MAJ order;
    but for simplicity we just declare A, B separately and wire them by index.
    """
    X = QuantumRegister(1, "X")
    B = QuantumRegister(n, "B")
    A = QuantumRegister(n, "A")
    Z = QuantumRegister(1, "Z")
    qc = QuantumCircuit(X, B, A, Z)

    # MAJ ripple: MAJ(X, B0, A0), then MAJ(A0, B1, A1), ..., MAJ(A_{n-2}, B_{n-1}, A_{n-1})
    # After each MAJ_i the "a" wire (A_i) holds c_{i+1}.
    if n >= 1:
        MAJ(qc, X[0], B[0], A[0])
    for i in range(1, n):
        MAJ(qc, A[i - 1], B[i], A[i])

    # Copy the top carry c_n (which sits in A_{n-1}) into Z.
    qc.cx(A[n - 1], Z[0])

    # UMA ripple in reverse order: UMA(A_{n-2}, B_{n-1}, A_{n-1}), ..., UMA(X, B_0, A_0)
    for i in range(n - 1, 0, -1):
        UMA_2cnot(qc, A[i - 1], B[i], A[i])
    UMA_2cnot(qc, X[0], B[0], A[0])

    return qc, X, B, A, Z


# ---------- Optimized adder (Figure 5 pseudocode) — n>=4 ----------
# The pseudocode uses register names A, B, X, Z. We map them directly.
# NOTE: In Figure 5 pseudocode A_i is a *memory location*; A_i ^= A_{i-1} B_i means
# CCX with controls (A_{i-1}, B_i) and target A_i.
# "Negate B_i" means X gate on B_i. "B_i ^= A_i" means CX (A_i -> B_i).

def optimized_adder(n):
    """Optimized CDKM adder from Figure 5, valid for n >= 4.

    Layout:
        A (n), B (n), X (1 ancilla), Z (1 output)
    """
    if n < 4:
        raise ValueError("Figure 5 pseudocode requires n >= 4")

    A = QuantumRegister(n, "A")
    B = QuantumRegister(n, "B")
    X = QuantumRegister(1, "X")
    Z = QuantumRegister(1, "Z")
    qc = QuantumCircuit(A, B, X, Z)

    # for i = 1 to n-1: B_i ^= A_i
    for i in range(1, n):
        qc.cx(A[i], B[i])

    # X ^= A_1
    qc.cx(A[1], X[0])
    # X ^= A_0 B_0 ; A_1 ^= A_2   (parallel, order doesn't affect correctness on same/different wires)
    qc.ccx(A[0], B[0], X[0])
    qc.cx(A[2], A[1])
    # A_1 ^= X B_1 ; A_2 ^= A_3
    qc.ccx(X[0], B[1], A[1])
    qc.cx(A[3], A[2])

    # for i = 2 to n-3: A_i ^= A_{i-1} B_i ; A_{i+1} ^= A_{i+2}
    for i in range(2, n - 2):
        qc.ccx(A[i - 1], B[i], A[i])
        qc.cx(A[i + 2], A[i + 1])

    # A_{n-2} ^= A_{n-3} B_{n-2} ; Z ^= A_{n-1}
    qc.ccx(A[n - 3], B[n - 2], A[n - 2])
    qc.cx(A[n - 1], Z[0])
    # Z ^= A_{n-2} B_{n-1} ; for i = 1 to n-2: Negate B_i
    qc.ccx(A[n - 2], B[n - 1], Z[0])
    for i in range(1, n - 1):
        qc.x(B[i])

    # B_1 ^= X ; for i = 2 to n-1: B_i ^= A_{i-1}
    qc.cx(X[0], B[1])
    for i in range(2, n):
        qc.cx(A[i - 1], B[i])

    # A_{n-2} ^= A_{n-3} B_{n-2}
    qc.ccx(A[n - 3], B[n - 2], A[n - 2])

    # for i = n-3 down to 2: A_i ^= A_{i-1} B_i ; A_{i+1} ^= A_{i+2} ; Negate B_{i+1}
    for i in range(n - 3, 1, -1):
        qc.ccx(A[i - 1], B[i], A[i])
        qc.cx(A[i + 2], A[i + 1])
        qc.x(B[i + 1])

    # A_1 ^= X B_1 ; A_2 ^= A_3 ; Negate B_2
    qc.ccx(X[0], B[1], A[1])
    qc.cx(A[3], A[2])
    qc.x(B[2])

    # X ^= A_0 B_0 ; A_1 ^= A_2 ; Negate B_1
    qc.ccx(A[0], B[0], X[0])
    qc.cx(A[2], A[1])
    qc.x(B[1])

    # X ^= A_1
    qc.cx(A[1], X[0])

    # for i = 0 to n-1: B_i ^= A_i
    for i in range(n):
        qc.cx(A[i], B[i])

    return qc, A, B, X, Z


# ---------- Gate counting helpers ----------

def count_gates(qc):
    """Return dict of {ccx, cx, x} counts."""
    counts = {"ccx": 0, "cx": 0, "x": 0}
    for inst in qc.data:
        name = inst.operation.name
        if name in counts:
            counts[name] += 1
    return counts


def circuit_depth(qc):
    return qc.depth()
