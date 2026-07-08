"""Grover's algorithm on the reduced 4-round SIMON (n=3, k=6, T=4)
from Anand-Maitra-Mukhopadhyay 2020 (arXiv:2004.10686), Fig 10 + Fig 14.

We build a fully reversible Qiskit circuit that:
  1. Prepares the 6 KEY qubits in uniform superposition.
  2. For each known (plaintext, ciphertext) pair, encrypts the plaintext
     under the superposed key using the SIMON round function + key schedule
     (all Toffoli/CNOT/NOT — no measurement inside the oracle).
  3. Compares each output block to the classical ciphertext; if ALL match,
     flips a phase (Grover oracle with -1 on marked states).
  4. UNCOMPUTES the encryption (reversibility) so the KEY register is
     the only qubit register that carries information into the diffuser.
  5. Applies the standard Grover diffuser on the 6-qubit KEY register.
  6. Iterates the (oracle+diffuser) an optimal ~floor(pi/4 * sqrt(N/M)) times.
  7. Measures the KEY register on Aer statevector/qasm simulator.

We reproduce the paper's claim from Figure 14a: for the SINGLE-pair oracle
with M = [0,1,1,1,0,1] and C = [0,1,1,1,1,1], the histogram shows two
dominant peaks: K = [0,0,1,1,1,0] and K' = [1,1,1,0,0,0].

We also run Figure 14b (two-pair oracle) and verify unique-key extraction.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import List, Tuple

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

# ---------- Constants ----------
N = 3               # SIMON word size
BLOCK = 2 * N       # 6
KEYLEN = 2 * N      # 6 (m = 2)
ROUNDS = 4
# Round constants c_2 = c_3 = [0,0,1] (LSB-first) = 4 (bit 2 is set)
# In qubit-list terms: bit index 2 of the 3-qubit register.
ROUND_CONSTANTS_BITS = {  # which bits (0..N-1) are 1 in c_j
    2: [2],  # [0,0,1] -> bit 2
    3: [2],
}


# ==================== Quantum SIMON subcircuits ====================
#
# Bit convention: for a 3-qubit word stored on qubits [q0, q1, q2],
# qubit qi corresponds to bit i (LSB-first, same as our classical impl).
# S^1 (left rotate by 1) on the classical value x = sum b_i 2^i is
# x' with b'_i = b_{(i-1) mod 3}.  So the "new bit at position i" comes
# from the "old bit at position (i-1) mod 3".  When we want to XOR
# S^1(L) into some target using CNOTs, we do CNOT(L[(i-1) mod n], target[i]).
# Equivalently, CNOT(L[j], target[(j+1) mod n]) for all j.
#
# S^{-1} = rotate RIGHT by 1: new bit i = old bit (i+1) mod n
# CNOT(L[j], target[(j-1) mod n])


def _rotl_index(j: int, i: int) -> int:
    """Where does the source bit at position j land in S^i(x)?"""
    return (j + i) % N


def add_rotated_word(qc: QuantumCircuit, src, dst, shift: int) -> None:
    """dst ^= S^{shift}(src) using CNOTs."""
    for j in range(N):
        qc.cx(src[j], dst[_rotl_index(j, shift)])


def add_and_of_rotations(qc: QuantumCircuit, L, dst, shift_a: int, shift_b: int) -> None:
    """dst ^= (S^{shift_a}(L) & S^{shift_b}(L)) using Toffolis.

    (S^a(L))_i = L_{(i - a) mod n}   (this is the value at position i
    after shifting).  Equivalently, the bit L_j appears at position
    (j + a) mod n in S^a(L).

    So the AND at position i is: L_{(i-a) mod n} AND L_{(i-b) mod n}.
    Thus dst[i] ^= L[(i-a) mod n] * L[(i-b) mod n].
    """
    for i in range(N):
        a_src = (i - shift_a) % N
        b_src = (i - shift_b) % N
        qc.ccx(L[a_src], L[b_src], dst[i])


def round_function_inplace(qc: QuantumCircuit, L, R, k) -> None:
    """Apply the reduced-SIMON round update in place, then swap so that:
       output L = original R XOR f(L, k), output R = original L.

    Implementation (following Fig 10 style):
      * R ^= (S^1(L) & S^2(L))      [n Toffolis]
      * R ^= L                       [n CNOTs; S^0(L) is just L]
      * R ^= k                       [n CNOTs]
      * swap L and R                 [3n CNOTs (or use qc.swap)]
    """
    add_and_of_rotations(qc, L, R, 1, 2)
    for j in range(N):
        qc.cx(L[j], R[j])
    for j in range(N):
        qc.cx(k[j], R[j])
    # swap L <-> R
    for j in range(N):
        qc.swap(L[j], R[j])


def key_expansion_step(qc: QuantumCircuit, prev_key, target_key, round_idx: int) -> None:
    """Compute target_key = S^{-1}(prev_key) XOR S^{-2}(prev_key)
       XOR round_constant.

    (In the paper's in-place scheme, k_{j} = c XOR k_{j-2} XOR S^{-1}(k_{j-1})
     XOR S^{-2}(k_{j-1}) is written INTO the qubits holding the old k_{j-2}.
     Here we compute into a fresh register `target_key` that was ALREADY
     initialized to k_{j-2} classically... but in the Grover setting we do
     everything in-place. See build_encrypt_uncompute for the actual layout.)

    THIS helper is NOT used directly by build_encrypt_uncompute (see below);
    the in-place scheme is inlined there for clarity.
    """
    # add S^{-1}(prev)
    add_rotated_word(qc, prev_key, target_key, -1)
    # add S^{-2}(prev)
    add_rotated_word(qc, prev_key, target_key, -2)
    # xor round constant
    for bit_idx in ROUND_CONSTANTS_BITS.get(round_idx, []):
        qc.x(target_key[bit_idx])


def encrypt_inplace(qc: QuantumCircuit,
                    L, R,
                    key_regs: List) -> None:
    """4-round reduced-SIMON encryption in place.

    key_regs is a list of T=4 3-qubit registers holding k_0..k_3.
    After the call, L,R hold the ciphertext.  key_regs[0], key_regs[1] are
    unchanged (they hold the input key words).  key_regs[2], key_regs[3]
    were initialized to |0> and now hold the two derived round keys.
    """
    # Derive k_2 into key_regs[2] (starts at |0>):
    #   k_2 = c_2 XOR k_0 XOR S^{-1}(k_1) XOR S^{-2}(k_1)
    # Compute k_0 XOR ...
    for j in range(N):
        qc.cx(key_regs[0][j], key_regs[2][j])
    add_rotated_word(qc, key_regs[1], key_regs[2], -1)
    add_rotated_word(qc, key_regs[1], key_regs[2], -2)
    for bit_idx in ROUND_CONSTANTS_BITS.get(2, []):
        qc.x(key_regs[2][bit_idx])

    # Derive k_3 into key_regs[3]:
    #   k_3 = c_3 XOR k_1 XOR S^{-1}(k_2) XOR S^{-2}(k_2)
    for j in range(N):
        qc.cx(key_regs[1][j], key_regs[3][j])
    add_rotated_word(qc, key_regs[2], key_regs[3], -1)
    add_rotated_word(qc, key_regs[2], key_regs[3], -2)
    for bit_idx in ROUND_CONSTANTS_BITS.get(3, []):
        qc.x(key_regs[3][bit_idx])

    # Now apply 4 rounds
    for j in range(ROUNDS):
        round_function_inplace(qc, L, R, key_regs[j])


def uncompute_encrypt_inplace(qc: QuantumCircuit,
                              L, R,
                              key_regs: List) -> None:
    """Inverse of encrypt_inplace, so that ancillae return to |0>."""
    # Reverse round loop
    for j in reversed(range(ROUNDS)):
        # round_function_inplace applied in this order:
        #   ccx (AND); cx L->R; cx k->R; swap L,R
        # Inverse: swap L,R; cx k->R; cx L->R; ccx  (all self-inverse)
        for jj in range(N):
            qc.swap(L[jj], R[jj])
        for jj in range(N):
            qc.cx(key_regs[j][jj], R[jj])
        for jj in range(N):
            qc.cx(L[jj], R[jj])
        # invert AND
        for i in reversed(range(N)):
            a_src = (i - 1) % N
            b_src = (i - 2) % N
            qc.ccx(L[a_src], L[b_src], R[i])

    # Reverse k_3 derivation
    for bit_idx in ROUND_CONSTANTS_BITS.get(3, []):
        qc.x(key_regs[3][bit_idx])
    add_rotated_word(qc, key_regs[2], key_regs[3], -2)
    add_rotated_word(qc, key_regs[2], key_regs[3], -1)
    for j in range(N):
        qc.cx(key_regs[1][j], key_regs[3][j])
    # Reverse k_2 derivation
    for bit_idx in ROUND_CONSTANTS_BITS.get(2, []):
        qc.x(key_regs[2][bit_idx])
    add_rotated_word(qc, key_regs[1], key_regs[2], -2)
    add_rotated_word(qc, key_regs[1], key_regs[2], -1)
    for j in range(N):
        qc.cx(key_regs[0][j], key_regs[2][j])


# ==================== Grover oracle ====================

def load_plaintext(qc: QuantumCircuit, L, R, m_bits_L: List[int],
                   m_bits_R: List[int]) -> None:
    """Set L,R = m_bits (they must be |0> to start; we use X gates)."""
    for j in range(N):
        if m_bits_L[j]:
            qc.x(L[j])
        if m_bits_R[j]:
            qc.x(R[j])


def compare_and_flag(qc: QuantumCircuit, L, R,
                     c_bits_L: List[int], c_bits_R: List[int],
                     flag_qubit) -> None:
    """Flip flag_qubit iff (L,R) == c_bits.

    Strategy: XOR c_bits into (L,R) so that "match" means (L,R)==|0..0>,
    then Toffoli-controlled on the NOT of all bits, then XOR c_bits back.
    We flip flag using an X sandwich on each qubit + a multi-controlled X
    with all controls on |0>.  Simplest: apply X to every position where
    c_bits is 0 (so we control on 1 everywhere), do a 6-controlled X,
    then undo the Xs.
    """
    # Combine into a single 6-list
    c_all = list(c_bits_L) + list(c_bits_R)
    qubits = list(L) + list(R)
    # Apply X where c_bit == 0 so we can then do an "all-1" multi-controlled X
    for i, b in enumerate(c_all):
        if b == 0:
            qc.x(qubits[i])
    qc.mcx(qubits, flag_qubit)
    for i, b in enumerate(c_all):
        if b == 0:
            qc.x(qubits[i])


def build_grover_circuit(pairs: List[Tuple[List[int], List[int]]],
                         num_iterations: int) -> Tuple[QuantumCircuit,
                                                       QuantumRegister,
                                                       ClassicalRegister]:
    """Build the full Grover circuit for the given (M, C) pairs.

    Each pair is (M_bits[6], C_bits[6]) with the paper's ordering:
      M = [L(0), L(1), L(2), R(0), R(1), R(2)]
      C same.

    Layout (qubit-efficient, single-copy L/R/K2/K3):
      - KEY: 6 qubits (k0[0..2] || k1[0..2]) in uniform superposition.
      - L, R: 3+3 encryption workspace (reset to plaintext each pair).
      - K2, K3: 3+3 derived-round-key ancillae (|0> in/out).
      - flag_per_pair: 1 flag qubit per (M,C) pair.
      - phase_kickback: 1 qubit in |-> that receives the mark.

    Each Grover iteration:
      For each pair p:
        1. load plaintext into L,R (X on '1' bits).
        2. encrypt_inplace(L, R, [K0, K1, K2, K3]).
        3. compare_and_flag(L, R, C) -> flag[p].
        4. UNCOMPUTE step 2 (uncompute_encrypt_inplace).
        5. UNCOMPUTE step 1 (X back).
      Now flag[p] holds whether K matches pair p, and L,R,K2,K3 are back
      to |0>.  Do MCX(flags, phase_kickback).
      Then reverse the pair loop and re-run steps 1..5 to CLEAR all flags
      back to |0>. (compare_and_flag is self-inverse when applied twice.)
      Then apply the standard 6-qubit diffuser on KEY.
    """
    # Registers
    K0 = QuantumRegister(N, name='k0')
    K1 = QuantumRegister(N, name='k1')
    L = QuantumRegister(N, name='L')
    R = QuantumRegister(N, name='R')
    K2 = QuantumRegister(N, name='k2')
    K3 = QuantumRegister(N, name='k3')
    flag_regs = [QuantumRegister(1, name=f'flag{p}') for p in range(len(pairs))]
    phase_kickback = QuantumRegister(1, name='phase')
    creg = ClassicalRegister(2 * N, name='keyout')

    all_regs = [K0, K1, L, R, K2, K3] + flag_regs + [phase_kickback]
    qc = QuantumCircuit(*all_regs, creg)

    key_regs = [K0, K1, K2, K3]

    # Prepare KEY in superposition
    for j in range(N):
        qc.h(K0[j])
        qc.h(K1[j])

    # Prepare phase kickback qubit |->
    qc.x(phase_kickback[0])
    qc.h(phase_kickback[0])

    def apply_all_pair_flags():
        for p_idx, (m_bits, c_bits) in enumerate(pairs):
            m_L, m_R = m_bits[0:3], m_bits[3:6]
            c_L, c_R = c_bits[0:3], c_bits[3:6]
            load_plaintext(qc, L, R, m_L, m_R)
            encrypt_inplace(qc, L, R, key_regs)
            compare_and_flag(qc, L, R, c_L, c_R, flag_regs[p_idx][0])
            uncompute_encrypt_inplace(qc, L, R, key_regs)
            load_plaintext(qc, L, R, m_L, m_R)  # X self-inverse

    # Grover iterations
    for it in range(num_iterations):
        qc.barrier()
        apply_all_pair_flags()               # set flags per pair
        flag_qubits = [f[0] for f in flag_regs]
        qc.mcx(flag_qubits, phase_kickback[0])  # phase kickback
        apply_all_pair_flags()               # clear flags (self-inverse)

        qc.barrier()
        # Diffuser on the 6-qubit KEY register
        key_qubits = list(K0) + list(K1)
        for q in key_qubits:
            qc.h(q)
            qc.x(q)
        qc.h(key_qubits[-1])
        qc.mcx(key_qubits[:-1], key_qubits[-1])
        qc.h(key_qubits[-1])
        for q in key_qubits:
            qc.x(q)
            qc.h(q)

    # Measure KEY
    key_qubits = list(K0) + list(K1)
    for i, q in enumerate(key_qubits):
        qc.measure(q, creg[i])

    return qc, (K0, K1), creg


# ==================== Simulation driver ====================

def run(pairs: List[Tuple[List[int], List[int]]],
        num_iterations: int,
        shots: int = 20000,
        use_statevector: bool = False):
    qc, key_regs, creg = build_grover_circuit(pairs, num_iterations)
    print(f"Circuit built. Num qubits: {qc.num_qubits}, depth (pre-transpile): "
          f"{qc.depth()}")

    sim = AerSimulator(method='statevector')
    tqc = transpile(qc, sim, optimization_level=1)
    print(f"Transpiled depth: {tqc.depth()}")
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()

    # Qiskit returns counts keyed by bitstring with rightmost = bit 0
    # of the classical register (i.e. creg[0] is rightmost char).
    # We measured key_qubits[i] -> creg[i], so bit i of the key = char at
    # position (len - 1 - i).
    normed = {}
    for bitstr, ct in counts.items():
        # reverse so that idx i corresponds to bit i
        b = bitstr[::-1]
        normed[b] = ct
    return normed, qc, tqc


def optimal_iterations(N_search: int, M_solutions: int) -> int:
    """Optimal number of Grover iterations."""
    if M_solutions <= 0:
        return 0
    theta = math.asin(math.sqrt(M_solutions / N_search))
    k = round((math.pi / 2 - theta) / (2 * theta))
    return max(1, int(k))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pairs', choices=['one', 'two'], default='one',
                    help="Use one or two plaintext-ciphertext pairs.")
    ap.add_argument('--iterations', type=int, default=None,
                    help="Override number of Grover iterations.")
    ap.add_argument('--shots', type=int, default=20000)
    ap.add_argument('--outfile', type=str, default=None)
    args = ap.parse_args()

    # Paper's pairs (Fig 14):
    M1 = [0, 1, 1, 1, 0, 1]
    C1 = [0, 1, 1, 1, 1, 1]
    M2 = [0, 0, 1, 1, 0, 1]
    C2 = [1, 1, 0, 0, 1, 1]

    if args.pairs == 'one':
        pairs = [(M1, C1)]
        num_solutions = 2  # from classical brute force
    else:
        pairs = [(M1, C1), (M2, C2)]
        num_solutions = 1

    N_search = 1 << (2 * N)  # 64
    it = args.iterations if args.iterations is not None else \
        optimal_iterations(N_search, num_solutions)
    print(f"Grover: N={N_search}, M={num_solutions}, iterations={it}, "
          f"pairs={args.pairs}, shots={args.shots}")

    counts, qc, tqc = run(pairs, it, shots=args.shots)

    # Sort by count desc
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    print("\nTop 8 measurement outcomes (bitstring shown as "
          "[k0(0)k0(1)k0(2)k1(0)k1(1)k1(2)], LSB-first):")
    total = sum(counts.values())
    for bstr, ct in ranked[:8]:
        bits_list = [int(c) for c in bstr]
        prob = ct / total
        print(f"  {bstr}  = {bits_list}  count={ct}  prob={prob:.4f}")

    # Compute probability mass on the classical solutions
    from classical_brute import (M1_bits, C1_bits, M2_bits, C2_bits,
                                 split_state)
    from simon_classical import encrypt as classical_encrypt, bits_to_int, int_to_bits

    marked = []
    for k0 in range(1 << N):
        for k1 in range(1 << N):
            ok = True
            for m_bits, c_bits in pairs:
                L0 = bits_to_int(m_bits[0:3]); R0 = bits_to_int(m_bits[3:6])
                Lc = bits_to_int(c_bits[0:3]); Rc = bits_to_int(c_bits[3:6])
                Le, Re = classical_encrypt(L0, R0, k0, k1)
                if not (Le == Lc and Re == Rc):
                    ok = False; break
            if ok:
                kbits = int_to_bits(k0, 3) + int_to_bits(k1, 3)
                bstr = ''.join(str(b) for b in kbits)
                marked.append(bstr)
    print(f"\nClassically marked keys: {marked}")
    marked_prob = sum(counts.get(b, 0) for b in marked) / total
    unmarked_prob = 1 - marked_prob
    print(f"Total probability on marked keys: {marked_prob:.4f}")
    print(f"Total probability on unmarked keys: {unmarked_prob:.4f}")
    print(f"Uniform baseline (M/N): {num_solutions / N_search:.4f}")
    speedup = marked_prob / (num_solutions / N_search)
    print(f"Amplification vs uniform: {speedup:.2f}x")

    result = {
        'pairs': args.pairs,
        'num_pairs': len(pairs),
        'num_iterations': it,
        'shots': args.shots,
        'total_qubits': qc.num_qubits,
        'circuit_depth_pre': qc.depth(),
        'circuit_depth_post': tqc.depth(),
        'counts': counts,
        'marked_keys': marked,
        'marked_prob': marked_prob,
        'uniform_baseline': num_solutions / N_search,
        'amplification_x': speedup,
        'N_search_space': N_search,
        'M_solutions': num_solutions,
    }
    if args.outfile:
        with open(args.outfile, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nWrote {args.outfile}")


if __name__ == "__main__":
    main()
