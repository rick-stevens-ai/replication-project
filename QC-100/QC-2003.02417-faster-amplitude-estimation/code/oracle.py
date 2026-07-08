"""Amplitude oracle A and Grover operator Q for a single-qubit target.

Following Nakaji 2020 (arXiv:2003.02417) Section 2.1:
  |Psi> = A|0>_n |0> = a|1>|1> + sqrt(1-a^2)|1>|0>  (target qubit encodes amplitude)
  We attenuate: |Psi'> = X|0>_n |00> with X = A tensor R, R|0> = (1/4)|1> + (sqrt(15)/4)|0>
  so sin(theta) = a/4 (theta in [0, 0.252]).
  Q = X (I - 2|0><0|) X^dagger (I - 2 I_n tensor |11><11|)

For a faithful+tractable simulation we use A as a single-qubit rotation:
  A|0> = a|1> + sqrt(1-a^2)|0>   (n = 1 target qubit)
so the full state lives on 3 qubits: [target] [ancilla_R] [ancilla_X_projector_qubit? no].
Actually per paper (2): X = A tensor R, so state on 2 qubits: q0 = A's qubit, q1 = R's qubit.
State |Psi'> = X|00> = sum over |q0 q1>.
The "good" state is q0=1 AND q1=1 (both). Amplitude of |11> = a * (1/4) = a/4 = sin(theta).

Q = X * S_0 * X^dagger * S_good, where
  S_0     = I - 2|00><00|   (flip phase on |00>)
  S_good  = I - 2|11><11|   (flip phase on |11>)  [in paper: I_n tensor |11><11|; here n=1 so single-qubit]

Wait, paper's (5): S_good = I - 2 I_n tensor |11><11|. Here "n" refers to the target register width;
|11><11| lives on the LAST TWO qubits (target + attenuation ancilla). So S_good flips phase iff those two = |1>|1>.
"""

from __future__ import annotations

import numpy as np


SQRT15 = np.sqrt(15.0)


def build_A(a: float) -> np.ndarray:
    """Single-qubit A: A|0> = sqrt(1-a^2)|0> + a|1>."""
    if not (0.0 <= a <= 1.0):
        raise ValueError(f"a={a} out of [0,1]")
    c = np.sqrt(1.0 - a * a)
    return np.array([[c, -a], [a, c]], dtype=complex)  # arbitrary phase on 2nd col; unitary


def build_R() -> np.ndarray:
    """R|0> = (sqrt(15)/4)|0> + (1/4)|1>."""
    return np.array([[SQRT15 / 4.0, -1.0 / 4.0], [1.0 / 4.0, SQRT15 / 4.0]], dtype=complex)


def build_X_op(a: float) -> np.ndarray:
    """X = A tensor R on 2 qubits (qubit 0 = A's target, qubit 1 = R's ancilla)."""
    A = build_A(a)
    R = build_R()
    return np.kron(A, R)  # matches statevector convention with qubit 0 as MSB in our indexing


def build_S0(dim: int = 4) -> np.ndarray:
    """Reflection about |0...0>: I - 2|0><0|."""
    S = np.eye(dim, dtype=complex)
    S[0, 0] = -1.0
    return S


def build_Sgood(dim: int = 4, good_index: int = 3) -> np.ndarray:
    """Reflection about |good>: I - 2|good><good|. For 2 qubits, |11> has index 3."""
    S = np.eye(dim, dtype=complex)
    S[good_index, good_index] = -1.0
    return S


def build_Q(a: float) -> np.ndarray:
    """Grover-like operator Q per paper eq (5)."""
    X = build_X_op(a)
    Xdag = X.conj().T
    S0 = build_S0(4)
    Sgood = build_Sgood(4, good_index=3)
    return X @ S0 @ Xdag @ Sgood


def exact_prob_good_after_Qm(a: float, m: int) -> float:
    """Return exact probability of measuring the good state |11> after applying Q^m|Psi'>.

    Analytically, this equals sin^2((2m+1)*theta) with sin(theta) = a/4.
    """
    X = build_X_op(a)
    psi = X @ np.array([1, 0, 0, 0], dtype=complex)  # |00>
    Q = build_Q(a)
    Qm = np.linalg.matrix_power(Q, m) if m > 0 else np.eye(4, dtype=complex)
    state = Qm @ psi
    # Prob of |11> (index 3) is |amplitude|^2
    return float(np.abs(state[3]) ** 2)


def theta_true(a: float) -> float:
    """True theta = arcsin(a/4) in [0, 0.252]."""
    return float(np.arcsin(a / 4.0))


if __name__ == "__main__":
    # Sanity check: prob_good after Q^m should match sin^2((2m+1)*theta) with sin theta = a/4
    for a in [0.1, 0.2, 0.3, 0.4]:
        th = theta_true(a)
        for m in [0, 1, 2, 4, 8, 16]:
            p_sim = exact_prob_good_after_Qm(a, m)
            p_ana = np.sin((2 * m + 1) * th) ** 2
            diff = abs(p_sim - p_ana)
            print(f"a={a}  m={m:3d}  p_sim={p_sim:.6f}  p_ana={p_ana:.6f}  diff={diff:.2e}")
        print()
