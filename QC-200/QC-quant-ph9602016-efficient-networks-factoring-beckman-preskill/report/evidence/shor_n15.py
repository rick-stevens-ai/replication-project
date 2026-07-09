#!/usr/bin/env python3
"""
Independent replication: Beckman, Chari, Devabhaktuni, Preskill (1996)
  quant-ph/9602016 -- "Efficient networks for quantum factoring"

Section VII: N=15 special-purpose factoring circuit.

Paper's claims for N=15 (Sec. VII, and Table in Sec. VI):
  * General purpose (K=4, L=8):  21 qubits, ~15,284 laser pulses
  * With K=4, L=2 overwriting add: 11 qubits, ~1,406 laser pulses
  * Special-purpose (classical lookup for x^a mod 15):
      L+K = 2+4 = 6 qubits, EXP_N in 32-36 laser pulses,
      plus L(2L-1)=6 pulses for QFT_2 => 38 laser pulses total
      to "factor 15" with x=7.

Here we implement:
  * The special-purpose entangled state |a>|7^a mod 15>, a in {0,1,2,3}
    using the paper's EXP_N(x=7, N=15) construction (Eq. 7.5) with
    exactly 6 storage qubits (2 for |a>, 4 for |b> = 7^a mod 15).
  * QFT_2 on the input register.
  * Measurement, extract y in {0,1,2,3}, reduce y/4 to lowest terms => r,
    then compute gcd(7^(r/2) +/- 1, 15) = {3, 5}.

We verify:
  1. The state before QFT is exactly the lookup table Eq. (7.3):
        a=00 -> 0001 (1),   a=01 -> 0111 (7)
        a=10 -> 0100 (4),   a=11 -> 1101 (13)
  2. QPE with L=2 gives y uniform over {0,1,2,3} (paper: "perfectly peaked
     at y/L = integer/r; here r divides 2^L so the distribution is peaked
     on all four values"). With L=2 and r=4, y/4 -> integer/r for all
     y in {0,1,2,3}; y=1 or y=3 in lowest terms yield r=4 directly.
  3. Recovering r=4 => factors gcd(7^2 +/- 1, 15) = gcd(48,15)=3, gcd(50,15)=5.

For comparison, we also do the *general* Shor for N=15 with x=7 using
Qiskit's simulator on a bigger circuit (2*K=8-qubit phase register) and
verify the peaks are at y/2^L in {0, 1/4, 2/4, 3/4}.
"""
import json
import math
from fractions import Fraction

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT


def paper_expn_x7_n15():
    """
    Build the EXP_N(x=7, N=15) operator from Eq. (7.5):
        EXP_N = C_a1 * C[[a1,a0]],b1 * C_a0 * C[[a1,a0]],b2 *
                C_a1 * C[[a1,a0]],b0 * C_a0 * C[[a1,a0]],b3 *
                C_b2 * C_b0

    In the paper's notation, C_alpha with subscript is a NOT on that qubit
    (an unconditional flip), and C[[a1,a0]],b_j is a Toffoli with the two
    a-qubits as controls and b_j as target. Reading the equation right-to-
    left, the *first* operations applied are C_b2 and C_b0 (unconditional
    NOTs on b0 and b2), which produce the initial 'all 1's in b0,b2' table.
    Then the Toffolis, alternated with NOTs on a-qubits, fix each row.

    We use 6 qubits:  a[0], a[1] (input), b[0..3] (output).
    Register order: total wire order is [a0, a1, b0, b1, b2, b3].
    """
    qa = QuantumRegister(2, 'a')   # a[0]=a0, a[1]=a1
    qb = QuantumRegister(4, 'b')   # b[0]..b[3]
    qc = QuantumCircuit(qa, qb, name="EXP_N_x7_N15")

    # Step 1: prepare uniform superposition on |a>: 2 Hadamards = 2 laser pulses
    qc.h(qa[0])
    qc.h(qa[1])

    # Now apply EXP_N(x=7, N=15) = Eq. (7.5), read right-to-left:
    # Rightmost is applied FIRST: C_b0 then C_b2
    qc.x(qb[0])       # C_b0  (NOT on b0)
    qc.x(qb[2])       # C_b2  (NOT on b2)
    # Next: C[[a1,a0]],b3 -- Toffoli(a1,a0 -> b3)
    qc.ccx(qa[1], qa[0], qb[3])
    # C_a0 (NOT on a0)
    qc.x(qa[0])
    # C[[a1,a0]],b0 -- Toffoli(a1,a0 -> b0)
    qc.ccx(qa[1], qa[0], qb[0])
    # C_a1 (NOT on a1)
    qc.x(qa[1])
    # C[[a1,a0]],b2
    qc.ccx(qa[1], qa[0], qb[2])
    # C_a0 (NOT on a0)
    qc.x(qa[0])
    # C[[a1,a0]],b1
    qc.ccx(qa[1], qa[0], qb[1])
    # C_a1 (NOT on a1)   -- this is the LAST-applied operator (leftmost in Eq. 7.5)
    qc.x(qa[1])
    return qc, qa, qb


def verify_lookup_table():
    """
    Run EXP_N(7,15) on each input |a> in {0,1,2,3}, |0000>_b -> should get
    |a>|7^a mod 15>.  This uses the same gate sequence but WITHOUT the
    initial Hadamards.
    """
    sim = AerSimulator(method="statevector")
    print("Verifying lookup table |a>|7^a mod 15>:")
    print("  a | expected 7^a mod 15 | measured b")
    print("  --+---------------------+-----------")
    ok = True
    for a in range(4):
        qa = QuantumRegister(2, 'a')
        qb = QuantumRegister(4, 'b')
        cb = ClassicalRegister(4, 'cb')
        ca = ClassicalRegister(2, 'ca')
        qc = QuantumCircuit(qa, qb, cb, ca)
        # Prepare |a>
        if a & 1:
            qc.x(qa[0])
        if a & 2:
            qc.x(qa[1])
        # Apply EXP_N(7,15) circuit (no Hadamards)
        qc.x(qb[0])
        qc.x(qb[2])
        qc.ccx(qa[1], qa[0], qb[3])
        qc.x(qa[0])
        qc.ccx(qa[1], qa[0], qb[0])
        qc.x(qa[1])
        qc.ccx(qa[1], qa[0], qb[2])
        qc.x(qa[0])
        qc.ccx(qa[1], qa[0], qb[1])
        qc.x(qa[1])
        qc.measure(qb, cb)
        qc.measure(qa, ca)
        t = transpile(qc, sim)
        res = sim.run(t, shots=1000).result().get_counts()
        # Only one outcome expected
        assert len(res) == 1, f"unexpected non-deterministic outcome: {res}"
        key = next(iter(res))
        # key format: "ca cb" (Qiskit lists later-added classical registers first)
        parts = key.split()
        ca_bits = parts[0]
        cb_bits = parts[1]
        a_meas = int(ca_bits, 2)
        b_meas = int(cb_bits, 2)
        expected = pow(7, a, 15)
        ok_row = (a_meas == a and b_meas == expected)
        print(f"  {a} |         {expected:2d}          |    {b_meas:2d}   {'OK' if ok_row else 'MISMATCH'}")
        ok = ok and ok_row
    return ok


def factor_15_paper_special_purpose(shots=4000):
    """
    Full special-purpose 'factor 15' circuit from Sec. VII:
      * 6 storage qubits (2 for a, 4 for b)
      * Hadamards on a: prepare uniform superposition
      * EXP_N(7,15) entangles |a>|7^a mod 15>
      * QFT_2 on the a register (L=2)
      * Measure a register -> y in {0,1,2,3}
    """
    qa = QuantumRegister(2, 'a')
    qb = QuantumRegister(4, 'b')
    ca = ClassicalRegister(2, 'ca')
    qc = QuantumCircuit(qa, qb, ca)

    # Prepare superposition
    qc.h(qa[0])
    qc.h(qa[1])
    # EXP_N(7,15) minus the initial Hadamards
    qc.x(qb[0])
    qc.x(qb[2])
    qc.ccx(qa[1], qa[0], qb[3])
    qc.x(qa[0])
    qc.ccx(qa[1], qa[0], qb[0])
    qc.x(qa[1])
    qc.ccx(qa[1], qa[0], qb[2])
    qc.x(qa[0])
    qc.ccx(qa[1], qa[0], qb[1])
    qc.x(qa[1])

    # Apply QFT_2 on qa
    qft2 = QFT(num_qubits=2, do_swaps=True)
    qc.append(qft2.to_gate(), qa)

    qc.measure(qa, ca)

    sim = AerSimulator(method="statevector")
    t = transpile(qc, sim)
    counts = sim.run(t, shots=shots).result().get_counts()
    return qc, counts


def recover_r_and_factor(counts, N=15, x=7, L=2):
    """From measured y-values, apply the continued-fraction procedure to
    recover r, then compute the factor via gcd(x^{r/2} +/- 1, N)."""
    r_candidates = {}
    for key, c in counts.items():
        y = int(key, 2)
        # Reduce y / 2^L to lowest terms; denominator is our candidate r
        frac = Fraction(y, 2 ** L)
        r = frac.denominator
        r_candidates[r] = r_candidates.get(r, 0) + c
    return r_candidates


def compute_factors(N, x, r):
    if r % 2 != 0:
        return None
    a = pow(x, r // 2, N)
    f1 = math.gcd(a - 1, N)
    f2 = math.gcd(a + 1, N)
    return (f1, f2)


def general_shor_n15_qpe(x=7, N=15, n_count=8, shots=4000):
    """
    A more general Shor-style circuit: use n_count phase-estimation qubits
    controlling repeated modular multiplication by x mod N.  This is closer
    to Shor's original algorithm than the paper's special-purpose network.
    For N=15 with x=7 (r=4) we expect peaks at y such that y/2^n_count is
    close to k/4 for k=0,1,2,3.

    We use Qiskit's decomposition of controlled multipliers via a tiny hand-
    built modular mult, which is fine for N=15 and x=7 (permutation on 4-bit
    y register: y -> 7 y mod 15).
    """
    # Precompute the permutation for x^(2^j) mod 15 acting on 4-bit y-register
    def perm_matrix(xp, N, bits):
        dim = 2 ** bits
        P = np.zeros((dim, dim), dtype=complex)
        for y in range(dim):
            if 1 <= y < N and math.gcd(y, N) == 1:
                new_y = (xp * y) % N
            else:
                new_y = y  # identity on values not in Z_N^*
            P[new_y, y] = 1.0
        return P

    from qiskit.circuit.library import UnitaryGate

    n_target = 4  # bits for y-register (need >= ceil(log2 N))
    q_count = QuantumRegister(n_count, 'c')
    q_target = QuantumRegister(n_target, 't')
    c_count = ClassicalRegister(n_count, 'm')
    qc = QuantumCircuit(q_count, q_target, c_count)

    # Superposition on counting register
    for i in range(n_count):
        qc.h(q_count[i])
    # Initialise target to |1>
    qc.x(q_target[0])

    # Controlled U^{2^j} for each counting qubit
    for j in range(n_count):
        xp = pow(x, 2 ** j, N)
        P = perm_matrix(xp, N, n_target)
        U = UnitaryGate(P, label=f"Mx^{2**j} mod {N}").control(1)
        qc.append(U, [q_count[j]] + list(q_target))

    # Inverse QFT on counting register
    qc.append(QFT(num_qubits=n_count, inverse=True, do_swaps=True).to_gate(), q_count)

    qc.measure(q_count, c_count)

    sim = AerSimulator(method="statevector")
    t = transpile(qc, sim)
    counts = sim.run(t, shots=shots).result().get_counts()
    return qc, counts


def main():
    out = {}

    print("=" * 70)
    print("Step 1: verify EXP_N(7,15) reproduces the lookup table in Eq. (7.3)")
    print("=" * 70)
    lookup_ok = verify_lookup_table()
    out["lookup_table_reproduced"] = bool(lookup_ok)

    print()
    print("=" * 70)
    print("Step 2: run the special-purpose 'factor 15' circuit (6 qubits)")
    print("=" * 70)
    qc_sp, counts_sp = factor_15_paper_special_purpose(shots=8000)
    print(f"Circuit width: {qc_sp.num_qubits} qubits")
    print(f"Total gates in the un-transpiled circuit: {qc_sp.size()}")
    # Count "elementary" pulses per paper's conventions:
    # H = 1 pulse; X = 1 pulse; CCX (Toffoli) = 6 laser pulses in Cirac-Zoller.
    # This gate counting is model-dependent; we report what we can.
    ops = qc_sp.count_ops()
    print(f"Gate breakdown: {dict(ops)}")
    out["special_purpose_qubits"] = qc_sp.num_qubits
    out["special_purpose_gate_counts"] = {str(k): int(v) for k, v in ops.items()}
    print("Measurement counts (y): (should be approx uniform over {0,1,2,3})")
    for y in range(4):
        key = format(y, '02b')
        print(f"  y={y} ({key}): {counts_sp.get(key, 0)}")
    out["special_purpose_counts"] = counts_sp

    print()
    print("Recovering r from y/2^L reduction:")
    r_cands = recover_r_and_factor(counts_sp, N=15, x=7, L=2)
    print(f"  r-candidates -> vote:  {r_cands}")
    out["r_candidates_special_purpose"] = r_cands
    # Best-supported r that is even and gives a factor
    for r in sorted(r_cands, key=r_cands.get, reverse=True):
        f = compute_factors(15, 7, r)
        if f and 1 < f[0] < 15 and 1 < f[1] < 15:
            print(f"  Chose r = {r}, factors gcd(7^{r//2} +/- 1, 15) = {f}")
            out["special_purpose_recovered_r"] = r
            out["special_purpose_factors"] = list(f)
            break

    print()
    print("=" * 70)
    print("Step 3: general Shor-style QPE on N=15, x=7 with n_count=8 phase qubits")
    print("=" * 70)
    qc_g, counts_g = general_shor_n15_qpe(x=7, N=15, n_count=8, shots=8000)
    print(f"Circuit width: {qc_g.num_qubits} qubits (8 counting + 4 target)")
    # Top 8 outcomes
    top = sorted(counts_g.items(), key=lambda kv: -kv[1])[:8]
    print("Top 8 measurement outcomes:")
    for k, c in top:
        y = int(k, 2)
        frac = Fraction(y, 2 ** 8)
        print(f"  y = {y:3d} (bin {k})  count={c}  y/256 = {y/256:.4f} -> {frac}")

    # Recover r via continued fractions and pick even r that yields factor
    from math import gcd
    N = 15
    x = 7
    best_r = None
    for k, c in sorted(counts_g.items(), key=lambda kv: -kv[1]):
        y = int(k, 2)
        if y == 0:
            continue
        frac = Fraction(y, 2 ** 8).limit_denominator(N)
        r = frac.denominator
        if r % 2 == 0:
            f1 = gcd(pow(x, r // 2, N) - 1, N)
            f2 = gcd(pow(x, r // 2, N) + 1, N)
            if 1 < f1 < N and 1 < f2 < N:
                best_r = r
                out["general_shor_recovered_r"] = r
                out["general_shor_factors"] = [f1, f2]
                out["general_shor_used_y"] = y
                print(f"  --> Recovered r = {r} from y = {y}; factors = {(f1, f2)}")
                break
    if best_r is None:
        print("  Could not recover r from top measurements (unexpected).")
    out["general_shor_top_counts"] = dict(top)

    with open("evidence_shor_n15.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print()
    print("Wrote evidence_shor_n15.json")

    # Return final verdict on whether the paper's claims replicate
    verdict = {
        "lookup_table_matches_paper": bool(lookup_ok),
        "special_purpose_qubits_expected": 6,
        "special_purpose_qubits_measured": qc_sp.num_qubits,
        "special_purpose_recovered_r": out.get("special_purpose_recovered_r"),
        "special_purpose_factors": out.get("special_purpose_factors"),
        "general_shor_recovered_r": out.get("general_shor_recovered_r"),
        "general_shor_factors": out.get("general_shor_factors"),
    }
    print("VERDICT_JSON:", json.dumps(verdict))


if __name__ == "__main__":
    main()
