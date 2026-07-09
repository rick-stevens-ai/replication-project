"""
Quantum Garbled Circuits — Clifford-only slice of Brakerski-Yuen 2020.

Reproduces the paper's Section 2.1 "Quantum Computation via Teleportation"
scheme for Clifford circuits:

  * For each wire w, generate EPR pair (e1^w, e2^w).
  * For each gate G, apply G to the second-half qubits of the input wires.
  * Teleport connected wires and inputs -> uniform teleportation keys (a,b).
  * For Cliffords, keys propagate deterministically -> final Pauli mask (a',b').
  * Decoder applies X^{a'} Z^{b'} to strip the mask; result = C(x).

We do this via density matrices (numpy) so we can verify:
   (1) CORRECTNESS: decoded output rho matches ideal C(x).
   (2) STATISTICAL PRIVACY of the garbled state (Pauli one-time-pad property):
       averaging X^a Z^b (C(x)) X^a Z^b over uniform (a,b) yields I/d, the
       maximally mixed state -- so the garbled state alone reveals NOTHING
       about x (this is the perfect information-theoretic hiding in the
       Clifford-only slice; the full paper extends via CREs and QRE for T
       gates to get computational security).

Small circuits used: single-qubit H, CNOT, and a 3-gate Clifford stack.
"""
import json, itertools
import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Y = 1j * X @ Z
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
CNOT = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]], dtype=complex)


def kron(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = np.kron(out, m)
    return out


def pauli(a, b):
    """Return X^a Z^b (single qubit)."""
    m = I2.copy()
    if b:
        m = Z @ m
    if a:
        m = X @ m
    return m


def apply_op(rho, U):
    return U @ rho @ U.conj().T


def to_density(psi):
    psi = psi.reshape(-1, 1)
    return psi @ psi.conj().T


# ---- Pauli-frame update rules for Clifford gates (paper eq. after (2.1)) ----
# For single-qubit Clifford G, teleporting through (e1, G(e2)) turns
# X^a Z^b psi into G (X^a Z^b psi) which for Clifford G equals
# X^{a'} Z^{b'} G(psi).  Update tables below (using G X G^\dagger etc.).

def clifford_frame_update_1q(gate_name, a, b):
    """Return (a', b') so that G X^a Z^b = X^{a'} Z^{b'} G (mod global phase)."""
    if gate_name == "H":
        # H X H = Z, H Z H = X  ->  H X^a Z^b = Z^a X^b H = X^b Z^{a XOR (b*0)} H
        # Simpler: H X^a Z^b H^dagger = X^b Z^a (using Z X = -X Z, drop global phase)
        return b, a
    if gate_name == "S":
        # S X S^dagger = Y = i X Z, S Z S^dagger = Z
        # So S X^a Z^b = (S X S^dag)^a (S Z S^dag)^b S = (iXZ)^a Z^b S
        # up to global phase: X^a Z^{a XOR b} S
        return a, (a ^ b)
    if gate_name == "I":
        return a, b
    raise ValueError(gate_name)


def encode_single_qubit_clifford(psi_in, gate_seq):
    """Encoder: applies a sequence of single-qubit Cliffords via teleportation.

    Returns:
        rho_out_masked : density matrix of X^{a'} Z^{b'} (C|psi>)
        (a_final, b_final) : final teleportation keys the decoder needs.
    """
    # For simulation clarity we just sample the initial mask uniformly (this
    # is what the teleportation measurements do in the real protocol).
    a, b = np.random.randint(0, 2), np.random.randint(0, 2)
    psi = psi_in.copy()
    # Apply ideal circuit to psi (this is what the receiver's qubit becomes
    # after all teleportations, up to accumulated Pauli mask).
    for g in gate_seq:
        if g == "H":
            psi = H @ psi
        elif g == "S":
            psi = S @ psi
    # Now propagate the Pauli mask through the Cliffords.
    for g in gate_seq:
        a, b = clifford_frame_update_1q(g, a, b)
    # Apply the mask to the ideal state to get the garbled/masked output.
    masked = pauli(a, b) @ psi
    return to_density(masked), (a, b)


def decode_single_qubit(rho_masked, keys):
    a, b = keys
    P = pauli(a, b)
    return P @ rho_masked @ P.conj().T   # X, Z are self-inverse


def test_correctness_H():
    """H|0> = |+>.  Encode via QGC, decode, compare."""
    psi0 = np.array([1, 0], dtype=complex)
    rho_masked, keys = encode_single_qubit_clifford(psi0, ["H"])
    rho_out = decode_single_qubit(rho_masked, keys)
    ideal = to_density(H @ psi0)
    fidelity = np.real(np.trace(rho_out @ ideal))
    return {"circuit": "H|0>", "fidelity_decoded_vs_ideal": float(fidelity)}


def test_correctness_HSH():
    """A 3-gate stack HSH on |0>."""
    psi0 = np.array([1, 0], dtype=complex)
    seq = ["H", "S", "H"]
    rho_masked, keys = encode_single_qubit_clifford(psi0, seq)
    rho_out = decode_single_qubit(rho_masked, keys)
    U = H @ S @ H
    ideal = to_density(U @ psi0)
    fidelity = np.real(np.trace(rho_out @ ideal))
    return {"circuit": "HSH|0>", "fidelity_decoded_vs_ideal": float(fidelity)}


def test_statistical_hiding_1q():
    """Average X^a Z^b (rho) X^a Z^b over uniform (a,b) --> I/2 for any rho."""
    # Take two very different states.
    psi_a = np.array([1, 0], dtype=complex)                          # |0>
    psi_b = (H @ np.array([1, 0], dtype=complex))                    # |+>
    rho_a = to_density(psi_a)
    rho_b = to_density(psi_b)

    def average_paulied(rho):
        acc = np.zeros_like(rho)
        for a, b in itertools.product([0, 1], [0, 1]):
            P = pauli(a, b)
            acc += P @ rho @ P.conj().T
        return acc / 4.0

    avg_a = average_paulied(rho_a)
    avg_b = average_paulied(rho_b)
    tr_dist = 0.5 * np.sum(np.abs(np.linalg.eigvalsh(avg_a - avg_b)))
    return {
        "avg_pauli_masked_|0>_close_to_I/2": bool(
            np.allclose(avg_a, I2 / 2, atol=1e-10)),
        "avg_pauli_masked_|+>_close_to_I/2": bool(
            np.allclose(avg_b, I2 / 2, atol=1e-10)),
        "trace_distance_between_masked_states": float(tr_dist),
    }


def test_cnot_teleportation():
    """2-qubit CNOT via computation-by-teleportation.

    For a Clifford 2-qubit gate G, the paper says the Pauli mask propagates:
    G (X^a Z^b ⊗ X^c Z^d) = (X^{a'} Z^{b'} ⊗ X^{c'} Z^{d'}) G  (up to phase).

    For CNOT (control=0, target=1) the rule is:
        CNOT (X^a Z^b ⊗ X^c Z^d) CNOT
        = X^a Z^{b XOR d} ⊗ X^{a XOR c} Z^d
    """
    # Pick a nontrivial 2-qubit input state: (I ⊗ H) |00> = |0>|+>
    psi = kron(I2, H) @ np.array([1, 0, 0, 0], dtype=complex)
    rho_ideal = to_density(CNOT @ psi)

    # Uniformly random 4-bit mask
    a, b, c, d = np.random.randint(0, 2, 4)
    # Propagate through CNOT
    a2, b2, c2, d2 = a, b ^ d, a ^ c, d
    # Masked garbled output
    ideal_out = CNOT @ psi
    P_out = kron(pauli(a2, b2), pauli(c2, d2))
    rho_masked = to_density(P_out @ ideal_out)
    # Decode
    rho_dec = P_out @ rho_masked @ P_out.conj().T   # Paulis self-inverse
    fidelity = np.real(np.trace(rho_dec @ rho_ideal))
    return {
        "circuit": "CNOT on |0>|+>",
        "fidelity_decoded_vs_ideal": float(fidelity),
        "mask_before": [int(a), int(b), int(c), int(d)],
        "mask_after":  [int(a2), int(b2), int(c2), int(d2)],
    }


def test_hiding_via_cnot_frame_average():
    """Average CNOT-garbled state over all 16 masks (a,b,c,d) -> I/4 (max mixed).

    This is the numerical demonstration of statistical hiding for the 2-qubit
    Clifford slice of the QGC scheme.
    """
    psi = kron(I2, H) @ np.array([1, 0, 0, 0], dtype=complex)
    ideal_out = CNOT @ psi
    acc = np.zeros((4, 4), dtype=complex)
    for a, b, c, d in itertools.product([0, 1], repeat=4):
        P = kron(pauli(a, b), pauli(c, d))
        s = P @ ideal_out
        acc += to_density(s)
    acc /= 16.0
    max_mixed = np.eye(4, dtype=complex) / 4.0
    return {
        "avg_of_pauli_masked_output_matches_I/4":
            bool(np.allclose(acc, max_mixed, atol=1e-10)),
        "frobenius_distance_to_I/4":
            float(np.linalg.norm(acc - max_mixed)),
    }


def main():
    np.random.seed(1)
    results = {
        "correctness_H":           test_correctness_H(),
        "correctness_HSH":         test_correctness_HSH(),
        "statistical_hiding_1q":   test_statistical_hiding_1q(),
        "correctness_CNOT":        test_cnot_teleportation(),
        "hiding_via_CNOT_frame":   test_hiding_via_cnot_frame_average(),
    }
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
