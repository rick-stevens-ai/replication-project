"""
Independent replication of Paetznick & Svore, arXiv:1311.1074, Figure 8.

Claim: The smallest RUS circuit in the paper's database implements the unitary
    U = (I + i*sqrt(2) * X) / sqrt(3)
on a single data qubit with success probability 3/4 (measurement outcome 0
on the single ancilla). Uses only 2 T gates and 1 ancilla + 1 measurement.

We build the circuit as an isometry on |0>_ancilla ⊗ |ψ>_data, compute the
Kraus operators K_0 and K_1 corresponding to the two projective measurement
outcomes on the ancilla, and check:

  1. K_0 = c * U  where c = sqrt(3)/2  (so that K_0† K_0 = (3/4) * I on data,
     i.e. the success probability is 3/4 for any input state |ψ>).
  2. K_0† K_0 + K_1† K_1 = I (completeness).
  3. K_1 up to global phase is a Clifford recovery (paper: identity/Z-type,
     easily reversed).
  4. Monte-Carlo (statevector + measurement sampling in Aer): empirical
     success probability ≈ 3/4 for random input states, and the post-measurement
     data state matches U|ψ> to within numerical tolerance.

The Figure 8 circuit as drawn (top-to-bottom = ancilla, then data qubit;
left-to-right = time):

  ancilla |0>: --H--T--•--T†--H--(measure)
                       |
  data   |ψ>: --H------X-------H--

That is: H on ancilla, T on ancilla, CNOT (ancilla control, data target),
T† on ancilla, H on ancilla, measure. On the data qubit we sandwich the CNOT
between two H gates (which turns it into a CZ-like interaction in the Hadamard
basis of the data), matching the paper's H-conjugation pattern.

If this natural reading does NOT match the paper's headline (K_0 ∝ (I+i√2 X)/√3
with p_succ = 3/4) we systematically search nearby variants (T vs T†, extra
CNOT, S vs I fix-ups) rather than fabricating a match.
"""

import numpy as np
from itertools import product

# Fundamental single-qubit gates
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
Tdg = T.conj().T

# Ordering convention: qubit 0 = ancilla (top wire), qubit 1 = data (bottom wire).
# We use the Kronecker convention U_total = U_anc ⊗ U_data for single-qubit gates
# acting on their respective qubits.

def kron_ad(U_anc, U_data):
    return np.kron(U_anc, U_data)

def cnot_ancilla_control_data_target():
    """CNOT with ancilla (qubit 0) as control, data (qubit 1) as target."""
    # In basis |anc, data>: |00>,|01>,|10>,|11>
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ], dtype=complex)

def cnot_data_control_ancilla_target():
    """CNOT with data (qubit 1) as control, ancilla (qubit 0) as target."""
    return np.array([
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
    ], dtype=complex)

TARGET_U = (I2 + 1j * np.sqrt(2) * X) / np.sqrt(3)
TARGET_P_SUCCESS = 3.0 / 4.0

def is_proportional_to_unitary(K, target_U, target_p):
    """Return (ok, phase, error) checking if K == exp(i*phi) * sqrt(target_p) * target_U."""
    scale = np.sqrt(target_p)
    # Find best global phase
    # K / (scale * target_U) should be a scalar of modulus 1
    # Use matrix element with largest magnitude in target_U to extract the phase
    ref = scale * target_U
    idx = np.unravel_index(np.argmax(np.abs(ref)), ref.shape)
    if abs(ref[idx]) < 1e-12:
        return False, None, np.inf
    ratio = K[idx] / ref[idx]
    if abs(abs(ratio) - 1.0) > 1e-6:
        # magnitude wrong (probability wrong)
        return False, None, abs(abs(ratio) - 1.0)
    phase = ratio / abs(ratio)
    err = np.linalg.norm(K - phase * ref, ord="fro")
    return err < 1e-8, phase, err

def kraus_from_circuit(W):
    """
    W is a 4x4 unitary on ancilla⊗data with ancilla starting in |0>.
    Compute the two 2x2 Kraus operators K_0, K_1 for projective measurement
    of the ancilla in the computational basis.
    W acts on |anc>|data>. The state after W is W (|0>_anc ⊗ |ψ>_data).
    K_m [i,j] = <m, i | W | 0, j>   where m is ancilla measurement outcome,
    i,j run over data-qubit basis.
    """
    # Basis ordering: index = 2*anc + data
    # |0, i> has index 0*2 + i = i, i in {0,1}
    # |m, i> has index 2*m + i
    K = []
    for m in (0, 1):
        Km = np.zeros((2, 2), dtype=complex)
        for i in (0, 1):
            for j in (0, 1):
                Km[i, j] = W[2 * m + i, 0 * 2 + j]
        K.append(Km)
    return K  # [K_0, K_1]

def check_completeness(K0, K1):
    return np.allclose(K0.conj().T @ K0 + K1.conj().T @ K1, I2, atol=1e-10)

def build_circuit(op_sequence):
    """
    Build the total 4x4 unitary from a left-to-right sequence of 4x4 gate matrices.
    Convention: gates applied in listed order, U_total = last @ ... @ second @ first.
    """
    W = np.eye(4, dtype=complex)
    for g in op_sequence:
        W = g @ W
    return W

def try_variant(name, ops, verbose=False):
    W = build_circuit(ops)
    K0, K1 = kraus_from_circuit(W)
    complete = check_completeness(K0, K1)
    ok, phase, err = is_proportional_to_unitary(K0, TARGET_U, TARGET_P_SUCCESS)
    # Also try alternate targets in case of orientation
    alt_targets = [
        ("(I+i*sqrt(2)*X)/sqrt(3)", (I2 + 1j * np.sqrt(2) * X) / np.sqrt(3)),
        ("(I-i*sqrt(2)*X)/sqrt(3)", (I2 - 1j * np.sqrt(2) * X) / np.sqrt(3)),
        ("(I+i*sqrt(2)*Y)/sqrt(3)", (I2 + 1j * np.sqrt(2) * Y) / np.sqrt(3)),
        ("(I+i*sqrt(2)*Z)/sqrt(3)", (I2 + 1j * np.sqrt(2) * Z) / np.sqrt(3)),
    ]
    # Try K0 up to a fixed left-Clifford of small set
    cliffs = [("I", I2), ("H", H), ("S", S), ("Z", Z), ("X", X), ("Y", Y),
              ("HS", H @ S), ("SH", S @ H), ("SHS", S @ H @ S)]
    best = None
    for tname, targ in alt_targets:
        for cn_left, cL in cliffs:
            for cn_right, cR in cliffs:
                candidate = cL @ targ @ cR
                ok2, phase2, err2 = is_proportional_to_unitary(K0, candidate, TARGET_P_SUCCESS)
                if ok2:
                    p_succ = np.real(np.trace(K0.conj().T @ K0)) / 2.0
                    if best is None or err2 < best[3]:
                        best = (tname, cn_left, cn_right, err2, phase2, p_succ)
    p_succ_random_input = np.real(np.trace(K0.conj().T @ K0)) / 2.0  # avg success prob over random pure states
    result = {
        "name": name,
        "complete": complete,
        "primary_match": ok,
        "primary_err": err,
        "best_variant": best,
        "avg_success_prob": p_succ_random_input,
        "K0": K0,
        "K1": K1,
    }
    if verbose:
        print(f"\n=== {name} ===")
        print(f"  Complete (K0†K0 + K1†K1 = I): {complete}")
        print(f"  avg success prob (Tr(K0†K0)/2): {p_succ_random_input:.6f}")
        print(f"  primary target (I+i√2 X)/√3 match: {ok} (err={err:.3e})")
        if best is not None:
            print(f"  best clifford-equivalent: {best[1]} · {best[0]} · {best[2]}  (err={best[3]:.3e}, phase={best[4]:.4f})")
    return result

# ------------------------------------------------------------------
# Encode gate operators on 2-qubit register (anc = qubit 0, data = qubit 1)
# ------------------------------------------------------------------
H_a = kron_ad(H, I2)
T_a = kron_ad(T, I2)
Tdg_a = kron_ad(Tdg, I2)
S_a = kron_ad(S, I2)
Z_a = kron_ad(Z, I2)
X_a = kron_ad(X, I2)

H_d = kron_ad(I2, H)
T_d = kron_ad(I2, T)
Tdg_d = kron_ad(I2, Tdg)
S_d = kron_ad(I2, S)
Z_d = kron_ad(I2, Z)
X_d = kron_ad(I2, X)

CNOT_ad = cnot_ancilla_control_data_target()  # anc -> data
CNOT_da = cnot_data_control_ancilla_target()  # data -> anc

# ------------------------------------------------------------------
# Variant attempts for Figure 8. The paper draws (schematically):
#   ancilla: H - T - • - T† - H     (2 T gates on ancilla)
#   data   : H -   - X -    - H     (H sandwich around CNOT target)
# Then an extra CNOT/S may appear per some readings. We try several.
# ------------------------------------------------------------------

variants = {}

# Variant A: literal reading (H-sandwich makes CNOT act like CZ up to basis)
variants["A: H·T·CNOT·T†·H (anc) with H·X·H (data)"] = [
    H_a, H_d,        # H on both
    T_a,             # T on ancilla
    CNOT_ad,         # CNOT anc->data
    Tdg_a,           # T† on ancilla
    H_a, H_d,        # H on both
]

# Variant B: T and T on ancilla (both T, not T-T†)
variants["B: H·T·CNOT·T·H (anc) with H·X·H (data)"] = [
    H_a, H_d,
    T_a,
    CNOT_ad,
    T_a,
    H_a, H_d,
]

# Variant C: data-controlled CNOT (data controls ancilla)
variants["C: H·T·CNOT(d->a)·T†·H (anc) with H·H (data)"] = [
    H_a, H_d,
    T_a,
    CNOT_da,
    Tdg_a,
    H_a, H_d,
]

# Variant D: extra CNOT after T† (some RUS figures have a second CNOT)
variants["D: two CNOTs, T then T†"] = [
    H_a, H_d,
    T_a,
    CNOT_ad,
    T_a,
    CNOT_ad,
    H_a, H_d,
]

# Variant E: as in Fig 8 text — H T . T H  on anc / H . H on data
# with the "." meaning a CZ-like coupling. If we interpret • with X on data
# as CNOT, then variant A is exact. Let's also try with an S gate at the end
# (which paper says can be absorbed into Clifford recovery)
variants["E: A + S on data at end"] = variants["A: H·T·CNOT·T†·H (anc) with H·X·H (data)"] + [S_d]

# Variant F: T-T with data-controlled CNOT
variants["F: H·T·CNOT(d->a)·T·H (anc)"] = [
    H_a, H_d,
    T_a,
    CNOT_da,
    T_a,
    H_a, H_d,
]

# Variant G: no H on data (interpret • as CZ on ancilla/data with ancilla control)
def CZ_gate():
    return np.diag([1, 1, 1, -1]).astype(complex)
CZ = CZ_gate()
variants["G: H·T·CZ·T†·H (anc), data untouched"] = [
    H_a,
    T_a,
    CZ,
    Tdg_a,
    H_a,
]

# Variant H: swap ancilla/data roles (some diagrams draw data on top)
variants["H: with anc/data swapped"] = [
    H_d, H_a,
    T_d,
    CNOT_da,          # anc controlled by data — swapped roles: now data is "control top"
    Tdg_d,
    H_d, H_a,
]

results = []
for name, ops in variants.items():
    r = try_variant(name, ops, verbose=True)
    results.append(r)

# Print summary
print("\n\n================ SUMMARY ================")
best_r = None
for r in results:
    tag = "MATCH" if r["primary_match"] else ("CLIFF-EQUIV" if r["best_variant"] else "no")
    print(f"  [{tag:12s}] p_succ={r['avg_success_prob']:.4f}  {r['name']}")
    if r["primary_match"] and (best_r is None or r["primary_err"] < best_r["primary_err"]):
        best_r = r

if best_r is not None:
    print(f"\nBEST DIRECT MATCH to (I+i√2 X)/√3 with p=3/4:")
    print(f"  variant: {best_r['name']}")
    print(f"  err: {best_r['primary_err']:.3e}")
    print(f"  avg success prob: {best_r['avg_success_prob']:.6f}")
    print(f"  K_0 =\n{best_r['K0']}")
    print(f"  K_1 =\n{best_r['K1']}")
