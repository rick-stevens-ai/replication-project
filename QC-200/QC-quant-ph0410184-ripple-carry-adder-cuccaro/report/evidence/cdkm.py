"""
Independent reimplementation of the CDKM ripple-carry quantum adder.

Reference: Cuccaro, Draper, Kutin, Moulton. "A new quantum ripple-carry
addition circuit." arXiv:quant-ph/0410184 (2004).

Two circuits are implemented:
  * simple_adder(n)     : Section 2 construction (Fig 4). MAJ + UMA(2-CNOT).
  * optimized_adder(n)  : Section 3 pseudocode (Fig 5). Requires n >= 4.

Qubit convention (2n+1 qubits total, plus 1 output high bit Z = 2n+2 qubits):
    q[0]      = X  (single ancilla, initialized to |0>)
    q[2i+1]   = B_i  (i = 0..n-1)   -- holds b_i initially, s_i at end
    q[2i+2]   = A_i  (i = 0..n-1)   -- holds a_i throughout (restored)
    q[2n+1]   = Z    -- holds z initially, z XOR s_n at end
"""

from __future__ import annotations
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCXGate  # not strictly needed
from qiskit_aer import AerSimulator
from qiskit import transpile
import itertools


# ---------------------------------------------------------------------------
# Primitive gates (MAJ, UMA)
# ---------------------------------------------------------------------------

def maj(qc: QuantumCircuit, c, b, a) -> None:
    """In-place majority gate.
    Inputs on wires (c, b, a); outputs (c XOR a, b XOR a, MAJ(a,b,c)) on same wires.
    Implementation (Fig 1): CNOT(a,b); CNOT(a,c); CCX(c,b,a).
    """
    qc.cx(a, b)
    qc.cx(a, c)
    qc.ccx(c, b, a)


def uma_2cnot(qc: QuantumCircuit, c, b, a) -> None:
    """UMA gate, 2-CNOT version (Fig 2a). Inverse-of-MAJ-plus-add-into-b.
    Wires (c, b, a) after MAJ hold (c XOR a, b XOR a, MAJ). UMA restores
    a to A, c to top wire, and writes s = a XOR b XOR c into B.
    Implementation: CCX(c,b,a); CNOT(a,c); CNOT(c,b).
    """
    qc.ccx(c, b, a)
    qc.cx(a, c)
    qc.cx(c, b)


def uma_3cnot(qc: QuantumCircuit, c, b, a) -> None:
    """UMA gate, 3-CNOT version (Fig 2b). Same function, more parallelizable.
    Implementation:  X on b; CNOT(c,b); CCX(c,b,a); X on b; CNOT(a,c); CNOT(a,b).
    (Standard textbook form; equivalent to the 2-CNOT UMA.)
    """
    qc.x(b)
    qc.cx(c, b)
    qc.ccx(c, b, a)
    qc.x(b)
    qc.cx(a, c)
    qc.cx(a, b)


# ---------------------------------------------------------------------------
# Section 2 (Fig 4) simple adder
# ---------------------------------------------------------------------------

def simple_adder(n: int, uma_variant: str = "2cnot") -> QuantumCircuit:
    """CDKM simple ripple-carry adder from Section 2 / Figure 4.

    Uses 2n + 2 qubits: X, (B_i, A_i for i=0..n-1), Z.
    Post-condition: |a>|b>|z>|0> -> |a>|s mod 2^n>|z XOR s_n>|0>
    where s = a + b.
    """
    assert n >= 1
    nq = 2 * n + 2
    qc = QuantumCircuit(nq, name=f"cdkm_simple_n{n}")

    def X_idx(): return 0
    def B(i):    return 2 * i + 1
    def A(i):    return 2 * i + 2
    def Z_idx(): return 2 * n + 1

    # Forward MAJ ripple:  MAJ(X, B0, A0);  MAJ(A0, B1, A1); ... MAJ(A_{n-2}, B_{n-1}, A_{n-1})
    # Carry c_i is held in A_{i-1} (with A_{-1} := X).
    prev_carry = X_idx()
    for i in range(n):
        maj(qc, prev_carry, B(i), A(i))
        prev_carry = A(i)

    # Copy high bit c_n from A_{n-1} into Z
    qc.cx(A(n - 1), Z_idx())

    # Reverse UMA ripple:  UMA(A_{n-2}, B_{n-1}, A_{n-1});  ...  UMA(X, B0, A0)
    uma = uma_2cnot if uma_variant == "2cnot" else uma_3cnot
    for i in range(n - 1, -1, -1):
        top = X_idx() if i == 0 else A(i - 1)
        uma(qc, top, B(i), A(i))

    return qc


# ---------------------------------------------------------------------------
# Section 3 (Fig 5) optimized adder -- direct transliteration of pseudocode
# ---------------------------------------------------------------------------

def optimized_adder(n: int) -> QuantumCircuit:
    """CDKM optimized ripple-carry adder, direct transliteration of Figure 5
    pseudocode. Valid for n >= 4. Uses 2n + 2 qubits, single ancilla X.

    Figure 5 pseudocode note: X ends holding c_1 during the middle of the
    circuit (not c_0 -- see paper "Note that, in Figure 4, the ancilla
    contains c_0 and is the topmost wire; in Figure 6, the ancilla contains
    c_1 and is the third wire from the top.").

    Register layout below matches Figure 6: A_i on even-index qubits, B_i
    on odd-index qubits, X the ancilla, Z the high-bit output.
    """
    assert n >= 4, "Figure 5 pseudocode requires n >= 4"
    nq = 2 * n + 2
    qc = QuantumCircuit(nq, name=f"cdkm_opt_n{n}")

    X = 0
    def B(i): return 2 * i + 1
    def A(i): return 2 * i + 2
    Z = 2 * n + 1

    # Line 1: for i = 1 to n-1: B_i ^= A_i
    for i in range(1, n):
        qc.cx(A(i), B(i))
    # Line 2: X ^= A_1
    qc.cx(A(1), X)
    # Line 3: X ^= A_0 B_0 ;  A_1 ^= A_2
    qc.ccx(A(0), B(0), X)
    qc.cx(A(2), A(1))
    # Line 4: A_1 ^= X B_1 ; A_2 ^= A_3
    qc.ccx(X, B(1), A(1))
    qc.cx(A(3), A(2))
    # Line 5 loop: for i = 2 to n-3:  A_i ^= A_{i-1} B_i ; A_{i+1} ^= A_{i+2}
    for i in range(2, n - 2):
        qc.ccx(A(i - 1), B(i), A(i))
        qc.cx(A(i + 2), A(i + 1))
    # Line 6: A_{n-2} ^= A_{n-3} B_{n-2} ; Z ^= A_{n-1}
    qc.ccx(A(n - 3), B(n - 2), A(n - 2))
    qc.cx(A(n - 1), Z)
    # Line 7: Z ^= A_{n-2} B_{n-1} ; for i = 1 to n-2: Negate B_i
    qc.ccx(A(n - 2), B(n - 1), Z)
    for i in range(1, n - 1):
        qc.x(B(i))
    # Line 8: B_1 ^= X ; for i = 2 to n-1: B_i ^= A_{i-1}
    qc.cx(X, B(1))
    for i in range(2, n):
        qc.cx(A(i - 1), B(i))
    # Line 9: A_{n-2} ^= A_{n-3} B_{n-2}
    qc.ccx(A(n - 3), B(n - 2), A(n - 2))
    # Line 10 loop: for i = n-3 down to 2:
    #                A_i ^= A_{i-1} B_i ; A_{i+1} ^= A_{i+2} ; Negate B_{i+1}
    for i in range(n - 3, 1, -1):
        qc.ccx(A(i - 1), B(i), A(i))
        qc.cx(A(i + 2), A(i + 1))
        qc.x(B(i + 1))
    # Line 11: A_1 ^= X B_1 ; A_2 ^= A_3 ; Negate B_2
    qc.ccx(X, B(1), A(1))
    qc.cx(A(3), A(2))
    qc.x(B(2))
    # Line 12: X ^= A_0 B_0 ; A_1 ^= A_2 ; Negate B_1
    qc.ccx(A(0), B(0), X)
    qc.cx(A(2), A(1))
    qc.x(B(1))
    # Line 13: X ^= A_1
    qc.cx(A(1), X)
    # Line 14: for i = 0 to n-1: B_i ^= A_i
    for i in range(n):
        qc.cx(A(i), B(i))

    return qc


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def encode_inputs(qc_data: QuantumCircuit, n: int, a: int, b: int, z: int = 0) -> QuantumCircuit:
    """Prepend X gates so a, b, z are encoded on the wires. Ancilla X stays |0>."""
    prep = QuantumCircuit(2 * n + 2)
    for i in range(n):
        if (a >> i) & 1:
            prep.x(2 * i + 2)  # A_i
        if (b >> i) & 1:
            prep.x(2 * i + 1)  # B_i
    if z & 1:
        prep.x(2 * n + 1)      # Z
    return prep.compose(qc_data)


def measure_all_bits(counts, n):
    """Given the Aer 'counts' dict (bit-reversed convention), return dict of
    single-outcome measurement string parsed into (X, B0..B_{n-1}, A0..A_{n-1}, Z).
    """
    assert len(counts) == 1, f"non-deterministic result: {counts}"
    key = next(iter(counts))
    # Qiskit prints classical bits in little-endian: bitstring[-1] is cbit 0.
    bits = key[::-1]  # bits[i] is qubit i now
    X = int(bits[0])
    B = [int(bits[2 * i + 1]) for i in range(n)]
    A = [int(bits[2 * i + 2]) for i in range(n)]
    Z = int(bits[2 * n + 1])
    return X, B, A, Z


def verify(adder_fn, n: int, tag: str, uma_variant: str = "2cnot") -> dict:
    """Run adder on all 2^(2n) (a,b) pairs plus z in {0,1}.
    Verify:  final B == (a+b) mod 2^n, final A == a, final X == 0,
             final Z == z XOR s_n where s_n = ((a+b) >> n) & 1.
    """
    sim = AerSimulator()
    if adder_fn is optimized_adder:
        base = adder_fn(n)
    else:
        base = adder_fn(n, uma_variant=uma_variant)
    n_tests = 0
    n_pass = 0
    failures = []
    for a in range(1 << n):
        for b in range(1 << n):
            for z in (0, 1):
                qc = encode_inputs(base, n, a, b, z)
                qc.measure_all()
                tc = transpile(qc, sim)
                result = sim.run(tc, shots=1).result()
                counts = result.get_counts()
                X, B, A, Z = measure_all_bits(counts, n)
                b_out = sum(bit << i for i, bit in enumerate(B))
                a_out = sum(bit << i for i, bit in enumerate(A))
                s_full = a + b
                s_mod = s_full & ((1 << n) - 1)
                s_n = (s_full >> n) & 1
                ok = (X == 0 and a_out == a and b_out == s_mod and Z == (z ^ s_n))
                n_tests += 1
                if ok:
                    n_pass += 1
                else:
                    if len(failures) < 5:
                        failures.append({
                            "a": a, "b": b, "z": z, "expected_s_mod": s_mod,
                            "expected_s_n": s_n, "got_X": X, "got_A": a_out,
                            "got_B": b_out, "got_Z": Z,
                        })
    return {
        "tag": tag, "n": n, "n_tests": n_tests, "n_pass": n_pass,
        "all_pass": n_pass == n_tests, "failures_sample": failures,
    }


def resource_counts(qc: QuantumCircuit) -> dict:
    """Count Toffoli (ccx), CNOT (cx), NOT (x); also 2q-depth after
    decomposing Toffoli into a canonical form is complicated -- we report
    logical/high-level depth and gate counts as in the paper.
    """
    ops = qc.count_ops()
    return {
        "toffoli":   ops.get("ccx", 0),
        "cnot":      ops.get("cx", 0),
        "not":       ops.get("x", 0),
        "num_qubits": qc.num_qubits,
        "depth_high_level": qc.depth(),
    }


if __name__ == "__main__":
    import json, sys
    results = {"simple_2cnot": [], "simple_3cnot": [], "optimized": []}

    for n in [2, 3, 4, 6, 8]:
        qc = simple_adder(n, "2cnot")
        r = resource_counts(qc)
        r.update({"n": n})
        results["simple_2cnot"].append(r)

        qc = simple_adder(n, "3cnot")
        r = resource_counts(qc)
        r.update({"n": n})
        results["simple_3cnot"].append(r)

        if n >= 4:
            qc = optimized_adder(n)
            r = resource_counts(qc)
            r.update({"n": n})
            results["optimized"].append(r)

    print(json.dumps(results, indent=2))
