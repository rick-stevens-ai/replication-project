#!/usr/bin/env python3
"""
Independent replication of Braun & Georgeot 2005 (arXiv:quant-ph/0510159)
"A Quantitative Measure of Interference"

Core formula (Eq. 8, unitary case):
    I(P(U)) = N - sum_{i,k} |U_ik|^4
where N is the Hilbert-space dimension.

Interference bits:  n_I = log2(I(P(U)) + 1)
"""

import json
import math
import numpy as np

RESULTS = {}

# --- Core measure -----------------------------------------------------------

def I_unitary(U):
    """Interference measure for a unitary U (Eq. 8)."""
    U = np.asarray(U, dtype=complex)
    N = U.shape[0]
    assert U.shape[1] == N, "U must be square"
    # Sanity-check unitarity
    resid = np.max(np.abs(U.conj().T @ U - np.eye(N)))
    assert resid < 1e-9, f"U not unitary, residual {resid}"
    return float(N - np.sum(np.abs(U) ** 4))

def i_bits(I_val):
    """Interference bits n_I = log2(I + 1)."""
    return math.log2(I_val + 1.0)

# --- Standard gates ---------------------------------------------------------

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
CNOT = np.array(
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1],
     [0, 0, 1, 0]], dtype=complex,
)
SWAP = np.array(
    [[1, 0, 0, 0],
     [0, 0, 1, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1]], dtype=complex,
)
TOFFOLI = np.eye(8, dtype=complex)
TOFFOLI[[6, 7]] = TOFFOLI[[7, 6]]

def QFT(N):
    """N x N Quantum Fourier Transform matrix."""
    j, k = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    return np.exp(2j * math.pi * j * k / N) / math.sqrt(N)

def kron(*mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

# --- Test set: standard-gate values ----------------------------------------

print("=" * 72)
print("Braun & Georgeot 2005 — interference measure I(P(U)) = N - Σ|U_ik|^4")
print("=" * 72)

standard = []
def record(name, U, paper_claim=None, note=""):
    N = U.shape[0]
    I_val = I_unitary(U)
    nI = i_bits(I_val)
    row = {
        "name": name,
        "N": N,
        "I": I_val,
        "i_bits": nI,
        "paper_claim": paper_claim,
        "note": note,
    }
    standard.append(row)
    tag = ""
    if paper_claim is not None:
        ok = math.isclose(I_val, paper_claim, abs_tol=1e-9)
        tag = "  [MATCH]" if ok else f"  [MISMATCH claim={paper_claim}]"
    print(f"  {name:22s}  N={N:<4d}  I = {I_val:15.10f}   n_I = {nI:8.5f}{tag}")

# Section IV.A / IV.B / IV.C examples
record("Identity_1q",       I2,                    paper_claim=0.0,          note="perm/id → 0")
record("Pauli-X (permut.)", X,                     paper_claim=0.0,          note="permutation matrix → 0")
record("Pauli-Y",           Y,                     paper_claim=0.0,          note="|Y_ik|^2 same as X → 0")
record("Pauli-Z (diag)",    Z,                     paper_claim=0.0,          note="diagonal, |Z_ik|=δ → 0")
record("Hadamard (1 qubit)",H,                     paper_claim=1.0,          note='"one i-bit" — Sec. IV.A.4')
record("CNOT",              CNOT,                  paper_claim=0.0,          note="permutation of comp. basis → 0")
record("SWAP",              SWAP,                  paper_claim=0.0,          note="permutation → 0")
record("Toffoli (CCX)",     TOFFOLI,               paper_claim=0.0,          note="permutation → 0")

# Walsh-Hadamard W_n on n qubits — paper: I(W_n) = 2^n - 1
for n in (1, 2, 3, 4):
    W = kron(*([H] * n))
    record(f"Walsh-Hadamard n={n}", W, paper_claim=(2 ** n - 1), note=f"expected 2^n-1={2**n-1}, {n} i-bits")

# QFT_n on n qubits (N = 2^n). Paper: |QFT_ik| = 1/sqrt(N) → I = N - 1
for n in (1, 2, 3, 4, 5):
    N = 2 ** n
    U = QFT(N)
    record(f"QFT n={n}", U, paper_claim=(N - 1), note=f"|U_ik|=1/√N → I = N-1 = {N-1}")

# Beam splitter Sec. IV.C: I(U_BS) = 2 (1 - cos^4 θ - sin^4 θ)
# At θ = π/4 gives I=1 (Hadamard-equivalent). Cross-check at several θ.
def U_BS(theta):
    return np.array([[math.cos(theta), 1j * math.sin(theta)],
                     [1j * math.sin(theta), math.cos(theta)]], dtype=complex)

bs_rows = []
print("\nBeam-splitter formula check: I(U_BS(θ)) = 2(1 - cos^4 θ - sin^4 θ)")
for theta_deg in (0, 15, 30, 45, 60, 90):
    theta = math.radians(theta_deg)
    U = U_BS(theta)
    I_val = I_unitary(U)
    paper = 2 * (1 - math.cos(theta) ** 4 - math.sin(theta) ** 4)
    ok = math.isclose(I_val, paper, abs_tol=1e-10)
    print(f"  θ={theta_deg:3d}°   I_num={I_val:.10f}   I_formula={paper:.10f}   {'[MATCH]' if ok else '[MISMATCH]'}")
    bs_rows.append({"theta_deg": theta_deg, "I_num": I_val, "I_formula": paper, "match": ok})

# --- Multiplicativity / tensor sanity check --------------------------------
# I(U⊗V) relation (not a strict factorization; test what actually holds).
# For A, B unitaries of dims N_A, N_B, Σ|A_ik|^4 * Σ|B_ik|^4 = Σ|(A⊗B)_ik|^4
# So (N_A*N_B) - I(A⊗B) = (N_A - I(A))(N_B - I(B))
print("\nTensor identity check: (N_AB - I(A⊗B)) == (N_A - I(A))(N_B - I(B))")
tensor_rows = []
pairs = [("H", H), ("QFT4", QFT(4)), ("CNOT", CNOT), ("X", X)]
for n1, A in pairs:
    for n2, B in pairs:
        AB = np.kron(A, B)
        NA, NB = A.shape[0], B.shape[0]
        lhs = NA * NB - I_unitary(AB)
        rhs = (NA - I_unitary(A)) * (NB - I_unitary(B))
        ok = math.isclose(lhs, rhs, abs_tol=1e-9)
        tensor_rows.append({"A": n1, "B": n2, "lhs": lhs, "rhs": rhs, "match": ok})
        print(f"  {n1:5s} ⊗ {n2:5s}   lhs={lhs:.10f}   rhs={rhs:.10f}   {'[MATCH]' if ok else '[MISMATCH]'}")

# --- Grover algorithm sim ---------------------------------------------------
# U_G = D · O, where O flips sign of marked item, D = 2|s><s| - I is diffusion.
# Compute I after building the full unitary U_G^k acting on the initial
# equipartitioned state s. Verify Braun-Georgeot claim:
#   accumulated interference reaches I ≈ 2n - 2 after full run (Sec. IV.F)
#   "actually used" interference (after removing initial W_n) tends to
#   ≈ 8 (asymptotically → 3 i-bits, 24/N + O(1/N^2))
print("\nGrover-algorithm interference (marked = 0, n = 3..8):")
grover_rows = []
def grover_U(n, marked=0):
    N = 2 ** n
    O = np.eye(N, dtype=complex)
    O[marked, marked] = -1
    s = np.ones(N, dtype=complex) / math.sqrt(N)
    D = 2 * np.outer(s, s.conj()) - np.eye(N, dtype=complex)
    return D @ O, O, D

for n in range(3, 9):
    N = 2 ** n
    UG_step, O, D = grover_U(n, marked=0)
    W = kron(*([H] * n))
    # Optimal iteration count ≈ (π/4) sqrt(N)
    k = int(round((math.pi / 4) * math.sqrt(N)))
    # Full unitary: (D O)^k W  applied to |0>
    U_total = np.linalg.matrix_power(UG_step, k) @ W
    I_full = I_unitary(U_total)
    # "Actually used" — remove the initial W_n by computing I of (D O)^k alone
    U_alg = np.linalg.matrix_power(UG_step, k)
    I_used = I_unitary(U_alg)
    row = {
        "n": n, "N": N, "k_iters": k,
        "I_potential_full_unitary": I_full,
        "I_actually_used_no_W": I_used,
        "i_bits_used": i_bits(I_used),
    }
    grover_rows.append(row)
    print(f"  n={n}  N={N:4d}  k={k:3d}   I(full)={I_full:8.4f}  I(actual-used)={I_used:7.4f}  n_I={i_bits(I_used):5.3f}")

# --- Teleportation "I = 6, ≈ 2.58 i-bits" sanity ---------------------------
# Sec. IV.D: the full teleportation circuit produces I = 6 (≈ 2.58 i-bits).
# Reproduce the circuit: 3 qubits, initial (|0>+e^{iφ}|1>)_a ⊗ Bell_bc,
# but the paper reports I on the propagator, not a state. We build the
# 8x8 unitary of the full protocol (up to and including the two-qubit
# Bell measurement replaced by CNOT+H): H_3, CNOT_23 create Bell(bc), then
# CNOT_12, H_1 do the Bell-measurement basis change. This is the standard
# teleportation *encoding* unitary.
print("\nTeleportation encoding-unitary interference:")
def op_on(qubits, op, total, positions):
    """Embed op on 'positions' (list of qubit indices) in an n-qubit register."""
    # Very small n so we can afford explicit kron with I's + explicit reorder.
    from itertools import product
    n = total
    N = 2 ** n
    # Convert op to a full-register matrix by kron'ing with identities where op acts
    # first then permuting qubits so op lands on 'positions'.
    # Simpler: build op on qubits 0..len(positions)-1 kron I on the rest, then apply SWAP perm.
    k = len(positions)
    full = np.kron(op, np.eye(2 ** (n - k), dtype=complex))  # op on qubits 0..k-1
    # Map [0..k-1] onto 'positions'. We need a permutation P s.t. permuting register
    # positions [0..k-1] -> positions gives our desired action.
    order = list(positions) + [i for i in range(n) if i not in positions]
    # Build the permutation matrix that reorders basis-vector qubit ordering
    perm = np.zeros((N, N), dtype=complex)
    for bits in product((0, 1), repeat=n):
        new_bits = [0] * n
        for src, dst in enumerate(order):
            new_bits[dst] = bits[src]
        i = 0
        for b in bits: i = (i << 1) | b
        j = 0
        for b in new_bits: j = (j << 1) | b
        perm[j, i] = 1
    return perm @ full @ perm.conj().T

# 3-qubit teleportation encoding: q0=alice's-msg, q1=alice's-EPR-half, q2=bob
n = 3
Id = np.eye(2, dtype=complex)
H3_on_q2 = op_on([], H, n, [2])            # H on qubit 2 → prep half of Bell
CNOT_23  = op_on([], CNOT, n, [2, 1])      # CNOT q2→q1 makes Bell(1,2)
CNOT_12  = op_on([], CNOT, n, [0, 1])      # Alice's CNOT (msg control, half target)
H_on_q0  = op_on([], H, n, [0])            # Alice's H
U_tele = H_on_q0 @ CNOT_12 @ CNOT_23 @ H3_on_q2
I_tele = I_unitary(U_tele)
print(f"  U_tele (8×8, 3 qubits):  I = {I_tele:.6f}   n_I = {i_bits(I_tele):.5f}")
print(f"  Paper claim: I = 6, n_I ≈ 2.58   →  {'MATCH' if math.isclose(I_tele, 6.0, abs_tol=1e-9) else 'MISMATCH'}")

# --- Dump results -----------------------------------------------------------
RESULTS["standard_gates"] = standard
RESULTS["beam_splitter"]  = bs_rows
RESULTS["tensor_identity"] = tensor_rows
RESULTS["grover"]         = grover_rows
RESULTS["teleportation"]  = {"I": I_tele, "i_bits": i_bits(I_tele),
                             "paper_I": 6.0, "paper_i_bits": math.log2(7),
                             "match": math.isclose(I_tele, 6.0, abs_tol=1e-9)}

# Summary matches
matches = sum(1 for r in standard if r["paper_claim"] is not None
              and math.isclose(r["I"], r["paper_claim"], abs_tol=1e-9))
total_claims = sum(1 for r in standard if r["paper_claim"] is not None)
print(f"\n=== SUMMARY: {matches}/{total_claims} standard-gate claims matched to machine precision.")

with open("results.json", "w") as f:
    json.dump(RESULTS, f, indent=2, default=float)
print("Wrote results.json")
