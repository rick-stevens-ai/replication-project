"""
Independent numerical replication of Lo & Chau, "Is Quantum Bit Commitment
Really Possible?" (arXiv:quant-ph/9603004, PRL 78, 3410 (1997)).

This is an impossibility-proof paper: there is no algorithm to reproduce.
What CAN be reproduced is the mathematical core of the argument:

  (P1) Ideal (perfectly-concealing) case: given a QBC protocol in which
       Alice's commitment leaves Bob's marginal state identical for b=0 and
       b=1 (rho_B_0 = rho_B_1), there exists a unitary U on Alice's system
       alone that maps her AB-purification |Psi_0> to |Psi_1>.  Consequently
       a cheating Alice always wins.
  (P2) Non-ideal (epsilon-concealing) case: if the two Bob-marginals have
       fidelity F(rho_B_0, rho_B_1) = 1 - delta (delta small), then there
       is a unitary on Alice's system that takes |Psi_0> to a state |psi_0>
       with |<psi_0|Psi_1>| = 1 - delta, giving Alice a large cheating
       success probability.  Equivalently, when concealing is imperfect at
       the epsilon level (1 - F on Bob's side), Alice's cheating probability
       is 1 - O(sqrt(epsilon)) --- i.e. large.

We use Qiskit statevector + qiskit.quantum_info exclusively, with numpy as
a linear-algebra fallback for polar/SVD steps.  No paid endpoints, no
LLM-generated numbers.  Every reported value is computed live.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
from numpy.linalg import svd

import qiskit
from qiskit.quantum_info import (
    Statevector,
    DensityMatrix,
    partial_trace,
    state_fidelity,
    Operator,
)

RESULTS: dict = {"env": {}, "P1_ideal": {}, "P2_nonideal": {}}
RESULTS["env"] = {
    "qiskit_version": qiskit.__version__,
    "numpy_version": np.__version__,
    "python": sys.version.split()[0],
}

EVIDENCE_DIR = Path(__file__).resolve().parent
OUT_JSON = EVIDENCE_DIR / "results.json"
CSV_TRADEOFF = EVIDENCE_DIR / "tradeoff_curve.csv"
CSV_ANGLE_SCAN = EVIDENCE_DIR / "angle_scan.csv"


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def dm_from_sv(sv: Statevector, keep: list[int], total_qubits: int) -> np.ndarray:
    """Return Bob's reduced density matrix by tracing out Alice's qubits.

    Qiskit convention: qubits are indexed 0..n-1 with qubit 0 as the least
    significant bit; partial_trace() argument is the list of qubit indices
    to trace OUT (i.e. Alice's qubits).
    """
    trace_out = [q for q in range(total_qubits) if q not in keep]
    rho = partial_trace(sv, trace_out)
    return np.asarray(rho.data)


def unitary_via_polar_decomposition(psi0: np.ndarray, psi1: np.ndarray,
                                     dimA: int, dimB: int) -> np.ndarray:
    """Given two AB-pure states with the SAME Bob-marginal, construct the
    unitary U on Alice's system such that (U_A otimes I_B)|psi0> = |psi1>.

    Reshape each vector to a dimA x dimB matrix M_k (Alice-index in rows,
    Bob-index in cols).  Then rho_B = M_k^dagger M_k.  If rho_B is common,
    write the SVDs M_0 = U_0 S V_0^dagger and M_1 = U_1 S V_1^dagger with
    the SAME singular values S and the SAME right singular vectors V (up to
    kernel choice for zero singular values).  The Alice-side unitary is
    then U_A = U_1 U_0^dagger acting on Alice's dimA-dim space so that
    (U_A otimes I_B) |psi_0> reshaped = U_A M_0 = M_1.
    """
    M0 = psi0.reshape(dimA, dimB)
    M1 = psi1.reshape(dimA, dimB)

    # Bob-density check
    rho_B_0 = M0.conj().T @ M0
    rho_B_1 = M1.conj().T @ M1
    if not np.allclose(rho_B_0, rho_B_1, atol=1e-10):
        raise ValueError(
            "Bob marginals differ; cannot build exact Alice-side unitary."
        )

    # Reduced SVDs  M_k = U_k * diag(s_k) * Vh_k, shapes
    #   U_k: (dimA, r),  s_k: (r,), Vh_k: (r, dimB)   where r = min(dimA,dimB).
    # We take FULL matrices for U (dimA x dimA) so U0 U0^dag = I on Alice.
    U0, s0, Vh0 = svd(M0, full_matrices=True)
    U1, s1, Vh1 = svd(M1, full_matrices=True)

    # Because rho_B_0 = rho_B_1, s0 and s1 are the same set (up to ordering,
    # which numpy already returns sorted descending -> identical here). But
    # the SVD is not unique when Bob's rho has degenerate spectrum; we must
    # explicitly align the shared Bob-space basis.
    #
    # Strategy: rotate M1 on the Bob side so its right-singular vectors
    # match those of M0.  Define R_B = Vh1^dag @ Vh0 restricted to the
    # row-space (nonzero singular values); this is unitary on that
    # subspace.  We complete it to a full dimB x dimB unitary R_B_full via
    # Gram-Schmidt on the kernel (irrelevant to (U_A x I)|psi0> since the
    # kernel is unpopulated by M0 as well).

    # For our concrete protocols dimA >= dimB and s > 0 always -> just:
    R_B_full = Vh1.conj().T @ Vh0        # dimB x dimB
    # Sanity: check it's unitary (may fail with degenerate spectra)
    if not np.allclose(R_B_full.conj().T @ R_B_full, np.eye(dimB), atol=1e-8):
        # Fallback: build U_A directly via nuclear-norm / polar decomposition
        # of  M0 M1^dagger  (Uhlmann-optimal alignment).
        Y = M0 @ M1.conj().T             # dimA x dimA
        Uy, sy, Vhy = svd(Y, full_matrices=True)
        # U_A that maximizes Re Tr(M1^dag U_A M0) is  U_A = Vhy^dag Uy^dag
        U_A = Vhy.conj().T @ Uy.conj().T
        return U_A

    # Now M1_aligned = M1 @ R_B_full = U1 diag(s) Vh0   ->   U_A M0 = M1_aligned
    # with U_A = U1 U0^dag.  But we want U_A M0 to equal M1 (not M1_aligned),
    # so we absorb the Bob-side rotation into the definition by noting that
    # applying U_A x I on the AB state produces reshape (U_A M0) = M1_aligned;
    # BUT M1 = M1_aligned @ R_B_full^dagger, i.e. M1 lives in a different
    # Bob-basis. Since the physics only cares about the AB pure state up to
    # the Bob basis (Bob's marginal is unchanged), the correct statement is:
    # <Psi_1 | (U_A x I) | Psi_0> = <vec(M1) | vec(U_A M0)> = Tr(M1^dag U_A M0).
    # The optimal U_A that maximizes this is the polar / Uhlmann one:
    #     U_A = argmax  Re Tr(M1^dag U M0)
    # which is Vhy^dag Uy^dag from SVD of Y = M0 M1^dag.
    Y = M0 @ M1.conj().T                 # dimA x dimA
    Uy, sy, Vhy = svd(Y, full_matrices=True)
    U_A = Vhy.conj().T @ Uy.conj().T
    return U_A


def cheating_success_probability(psi0: np.ndarray, psi1_target: np.ndarray) -> float:
    """|<psi_1_target | psi_0>|^2 is the probability Bob's verification
    (which expects |psi_1_target>) succeeds when Alice actually sends
    |psi_0>.  When perfect-concealing holds we can rotate |psi_0> onto
    |psi_1_target> so the overlap becomes 1.
    """
    return float(np.abs(np.vdot(psi1_target, psi0)) ** 2)


# ------------------------------------------------------------------
# PART 1: IDEAL / PERFECTLY CONCEALING PROTOCOL
# ------------------------------------------------------------------
# Concrete concealing protocol: Alice holds two qubits (A0, A1) and sends
# Bob one qubit (B) that is entangled with A depending on b.
#
#   b = 0 :  |Psi_0>_ABtot = (1/sqrt(2)) ( |0>_A0 |0>_A1 |0>_B  +  |1>_A0 |1>_A1 |1>_B )
#            = |00>_A |0>_B/sqrt(2) + |11>_A |1>_B/sqrt(2)     (a GHZ-like state)
#   b = 1 :  |Psi_1>_ABtot = (1/sqrt(2)) ( |+>_A0 |+>_A1 |+>_B + |->_A0 |->_A1 |->_B )
#
# In both cases Bob's marginal is I/2  ->  perfectly concealing.
# We compute the Schmidt decomposition explicitly and construct the
# Alice-side unitary U_A on the 2-qubit Alice register.
#
# Convention: qubit 0 = Bob, qubits 1 and 2 = Alice's A0 and A1.
# --------------------------------------------------------------

def build_ideal_pair():
    """Return |Psi_0>, |Psi_1> as Statevectors on 3 qubits (qubit 0 = Bob).
    """
    dim = 8
    psi0 = np.zeros(dim, dtype=complex)
    # basis |q2 q1 q0> = |A1 A0 B>
    # |00>_A |0>_B  ->  bitstring q2 q1 q0 = 0 0 0 -> index 0
    # |11>_A |1>_B  ->  bitstring q2 q1 q0 = 1 1 1 -> index 7
    psi0[0] = 1 / np.sqrt(2)
    psi0[7] = 1 / np.sqrt(2)

    # b = 1 : (|+>_A1 |+>_A0 |+>_B + |->_A1 |->_A0 |->_B)/sqrt(2)
    def kron3(a, b, c):
        return np.kron(np.kron(a, b), c)

    plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    minus = np.array([1, -1], dtype=complex) / np.sqrt(2)
    # ordering in np.kron: outermost is highest qubit (qubit 2 = A1)
    # so kron(A1, A0, B) -> index bit ordering (q2 q1 q0)
    psi1 = (kron3(plus, plus, plus) + kron3(minus, minus, minus)) / np.sqrt(2)

    return Statevector(psi0), Statevector(psi1)


def run_part1_ideal():
    sv0, sv1 = build_ideal_pair()
    total_qubits = 3
    bob_qubits = [0]

    # (a) Verify rho_B_0 == rho_B_1
    rhoB0 = dm_from_sv(sv0, bob_qubits, total_qubits)
    rhoB1 = dm_from_sv(sv1, bob_qubits, total_qubits)
    diff = float(np.linalg.norm(rhoB0 - rhoB1))
    # F between the two Bob marginals
    F_B = float(state_fidelity(DensityMatrix(rhoB0), DensityMatrix(rhoB1)))

    # (b) Also compute Alice's marginals for reference
    alice_qubits = [1, 2]
    rhoA0 = dm_from_sv(sv0, alice_qubits, total_qubits)
    rhoA1 = dm_from_sv(sv1, alice_qubits, total_qubits)

    # Build Alice-side unitary U_A
    # We need Alice's register on one side, Bob on the other.  Currently
    # qubit 0 = Bob, so reshape to (dimA=4, dimB=2).  numpy indexing:
    # vector index = q2 q1 q0 = a1 a0 b, so if we reshape (4,2) with 'C'
    # ordering the outer index is (q2 q1) = Alice and inner is q0 = Bob.
    psi0v = np.asarray(sv0.data)
    psi1v = np.asarray(sv1.data)

    U_A_2x2_alice_only = unitary_via_polar_decomposition(psi0v, psi1v,
                                                          dimA=4, dimB=2)

    # Sanity: is U_A unitary?
    unit_err = float(np.linalg.norm(U_A_2x2_alice_only.conj().T @ U_A_2x2_alice_only
                                     - np.eye(4)))

    # Apply (U_A otimes I_B) to |Psi_0>
    U_full = np.kron(U_A_2x2_alice_only, np.eye(2))
    psi0_rotated = U_full @ psi0v

    # Bring to canonical Statevector for fidelity comparison
    sv0_rot = Statevector(psi0_rotated)
    # Overlap with |Psi_1>
    overlap_amp = complex(np.vdot(psi1v, psi0_rotated))
    overlap_prob = float(abs(overlap_amp) ** 2)
    fidelity_after_U = float(state_fidelity(sv0_rot, sv1))

    RESULTS["P1_ideal"] = {
        "bob_rho_frobenius_diff": diff,
        "bob_fidelity_before_U": F_B,
        "rhoB0_diag": [float(x.real) for x in np.diag(rhoB0)],
        "rhoB1_diag": [float(x.real) for x in np.diag(rhoB1)],
        "U_A_unitarity_error": unit_err,
        "overlap_amp": {"re": overlap_amp.real, "im": overlap_amp.imag},
        "overlap_prob_|<Psi1|U_A|Psi0>|^2": overlap_prob,
        "fidelity_after_U_between_psi0_rot_and_psi1": fidelity_after_U,
        "alice_rho0_purity_Tr(rho^2)": float(np.trace(rhoA0 @ rhoA0).real),
        "alice_rho1_purity_Tr(rho^2)": float(np.trace(rhoA1 @ rhoA1).real),
    }

    print("=== PART 1: IDEAL / PERFECT CONCEALING ===")
    print(f"  ||rho_B_0 - rho_B_1||_F     = {diff:.3e}   (perfect concealing => 0)")
    print(f"  F(rho_B_0, rho_B_1)         = {F_B:.10f}   (=1 iff equal)")
    print(f"  U_A unitarity error         = {unit_err:.3e}")
    print(f"  |<Psi_1|(U_A x I)|Psi_0>|^2 = {overlap_prob:.10f}  (cheat succ. prob)")
    print(f"  F( (U_A x I)|Psi_0>, |Psi_1>) = {fidelity_after_U:.10f}")
    print()


# ------------------------------------------------------------------
# PART 2: NON-IDEAL epsilon-CONCEALING PROTOCOL
# ------------------------------------------------------------------
# We introduce a tunable imperfection.  Take
#
#   |Psi_0(theta)>  =  cos(theta) |0>_A |0>_B  + sin(theta) |1>_A |1>_B     (Bell-like)
#   |Psi_1(theta)>  =  cos(theta) |0>_A |1>_B  + sin(theta) |1>_A |0>_B     (flipped)
#
# For theta = pi/4 both Bob marginals are I/2 (perfect concealing).  For
# other theta they differ, and the difference is the imperfection.
#
# Fidelity between the two Bob marginals:
#   rho_B_0 = diag(cos^2 theta, sin^2 theta)
#   rho_B_1 = diag(sin^2 theta, cos^2 theta)
# F(rho_B_0, rho_B_1) = (sqrt(c^2 s^2) + sqrt(s^2 c^2))^2 = (2|cs|)^2  -- NO.
# F = Tr(sqrt(sqrt(rho0) rho1 sqrt(rho0)))^2  =  (2 |cos theta sin theta|)^2
#   = sin^2(2 theta).
#
# We call epsilon = 1 - F.
# Alice's optimal cheating success probability (Uhlmann) is
#     P_cheat = max_U |<Psi_1|(U_A x I)|Psi_0>|^2 = F(rho_B_0, rho_B_1)
# so cheat_prob = 1 - epsilon = sin^2(2 theta).
# In the ideal limit theta = pi/4, cheat_prob = 1 (perfect cheating).
# Near theta = pi/4, write theta = pi/4 + delta ->
#     cheat_prob = sin^2(pi/2 + 2 delta) = cos^2(2 delta) ~ 1 - 4 delta^2
#     1 - epsilon ~ 1 - 4 delta^2  =>  epsilon ~ 4 delta^2
# so 1 - cheat_prob = O(epsilon) = O(sqrt(epsilon) * sqrt(epsilon))  -- the
# paper's qualitative statement is that cheat probability is 1 - O(sqrt(eps))
# in general; our worked example actually achieves 1 - O(epsilon), which is
# STRONGER (i.e. cheating is even easier).  We report the curve and let the
# reader see the trade-off.
# ------------------------------------------------------------------

def build_bell_like_pair(theta: float):
    """Return |Psi_0>, |Psi_1> as 4-dim Statevectors on 2 qubits (Alice, Bob).
    Convention: qubit 0 = Bob, qubit 1 = Alice.  Vector-index bit order
    (q1 q0) = (Alice, Bob).
    """
    c, s = np.cos(theta), np.sin(theta)
    psi0 = np.zeros(4, dtype=complex)
    # |0>_A |0>_B -> q1=0, q0=0 -> index 0
    # |1>_A |1>_B -> q1=1, q0=1 -> index 3
    psi0[0] = c
    psi0[3] = s

    psi1 = np.zeros(4, dtype=complex)
    # |0>_A |1>_B -> q1=0, q0=1 -> index 1
    # |1>_A |0>_B -> q1=1, q0=0 -> index 2
    psi1[1] = c
    psi1[2] = s

    return Statevector(psi0), Statevector(psi1)


def bob_pair_fidelity(theta: float) -> tuple[float, float]:
    """Return (Bob-fidelity F, analytic sin^2(2theta) reference)."""
    sv0, sv1 = build_bell_like_pair(theta)
    rhoB0 = dm_from_sv(sv0, keep=[0], total_qubits=2)
    rhoB1 = dm_from_sv(sv1, keep=[0], total_qubits=2)
    F = float(state_fidelity(DensityMatrix(rhoB0), DensityMatrix(rhoB1)))
    return F, float(np.sin(2 * theta) ** 2)


def optimal_cheat_prob_via_uhlmann(psi0: np.ndarray, psi1: np.ndarray,
                                    dimA: int, dimB: int) -> float:
    """Uhlmann: max over unitaries U_A of |<psi1|(U_A x I)|psi0>| equals
    F(rho_B_0, rho_B_1)^(1/2), so the probability equals F.

    We compute it directly: reshape M0, M1 and use
        max_U |Tr(M1^dagger U M0)|  where the maximizer is U = V W^dagger
    with SVD  M0 M1^dagger = W diag(s) V^dagger.  The maximum equals
    sum_i s_i = ||M0 M1^dagger||_* (trace/nuclear norm).
    Then P = (that value)^2  =  F(rho_B_0, rho_B_1).
    """
    M0 = psi0.reshape(dimA, dimB)
    M1 = psi1.reshape(dimA, dimB)
    X = M1.conj() @ M0.T  # dimA x dimA   NOT quite; we want  M0 M1^dagger
    Y = M0 @ M1.conj().T  # dimA x dimA
    _, s, _ = svd(Y, full_matrices=False)
    return float(np.sum(s) ** 2)


def run_part2_nonideal():
    print("=== PART 2: NON-IDEAL / eps-CONCEALING ===")
    thetas = np.linspace(0.05, np.pi / 2 - 0.05, 41)
    rows = []
    for theta in thetas:
        F_B, F_analytic = bob_pair_fidelity(theta)
        eps = 1.0 - F_B
        sv0, sv1 = build_bell_like_pair(theta)
        P_cheat = optimal_cheat_prob_via_uhlmann(np.asarray(sv0.data),
                                                  np.asarray(sv1.data),
                                                  dimA=2, dimB=2)
        rows.append({
            "theta": float(theta),
            "F_bob": F_B,
            "F_analytic_sin2_2theta": F_analytic,
            "epsilon_1_minus_F": eps,
            "P_cheat_uhlmann": P_cheat,
            "one_minus_P_cheat": 1.0 - P_cheat,
            "sqrt_epsilon": float(np.sqrt(eps)),
        })

    # Write CSV
    import csv
    with open(CSV_TRADEOFF, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Ideal check at theta = pi/4
    theta_ideal = np.pi / 4
    sv0, sv1 = build_bell_like_pair(theta_ideal)
    rhoB0 = dm_from_sv(sv0, keep=[0], total_qubits=2)
    rhoB1 = dm_from_sv(sv1, keep=[0], total_qubits=2)
    F_ideal, _ = bob_pair_fidelity(theta_ideal)
    P_cheat_ideal = optimal_cheat_prob_via_uhlmann(np.asarray(sv0.data),
                                                    np.asarray(sv1.data), 2, 2)

    # Explicit U_A construction at ideal theta (perfect concealing)
    U_A = unitary_via_polar_decomposition(np.asarray(sv0.data),
                                          np.asarray(sv1.data), dimA=2, dimB=2)
    U_full = np.kron(U_A, np.eye(2))
    psi0_rot = U_full @ np.asarray(sv0.data)
    overlap_ideal = float(abs(np.vdot(np.asarray(sv1.data), psi0_rot)) ** 2)

    RESULTS["P2_nonideal"] = {
        "ideal_theta_pi_over_4": {
            "F_bob": F_ideal,
            "P_cheat_uhlmann": P_cheat_ideal,
            "explicit_U_overlap": overlap_ideal,
        },
        "curve_csv": str(CSV_TRADEOFF),
        "curve_rows": rows,
    }

    print(f"  theta = pi/4 (perfect concealing):")
    print(f"    F(rho_B_0, rho_B_1)   = {F_ideal:.10f}")
    print(f"    P_cheat (Uhlmann)     = {P_cheat_ideal:.10f}")
    print(f"    explicit-U overlap    = {overlap_ideal:.10f}")
    print(f"  Trade-off curve written: {CSV_TRADEOFF}")
    print("  Sample rows (theta, eps, P_cheat, 1-P_cheat):")
    for r in rows[::8]:
        print(f"    theta={r['theta']:.4f}  eps={r['epsilon_1_minus_F']:.4e}  "
              f"P_cheat={r['P_cheat_uhlmann']:.6f}  "
              f"1-P_cheat={r['one_minus_P_cheat']:.4e}")

    # Fit  1 - P_cheat  vs  epsilon:
    # theoretically 1 - P_cheat = 1 - F_B = epsilon (equality here!)
    # so we verify equality to numerical precision.
    eq_err = max(abs(r["one_minus_P_cheat"] - r["epsilon_1_minus_F"]) for r in rows)
    RESULTS["P2_nonideal"]["|1-P_cheat  minus  eps|_max"] = float(eq_err)
    print(f"  max |[(1-P_cheat)] - eps| across curve = {eq_err:.3e}"
          f"    (Uhlmann: P_cheat = F = 1 - eps, so this is 0 to num prec.)")
    print()


# ------------------------------------------------------------------
# Extra: reproduce the Bennett-Brassard '84 EPR cheating attack directly
# with Qiskit statevector (the paper's motivating example).
# ------------------------------------------------------------------
def run_part3_bb84_epr_cheat():
    """Alice prepares one EPR pair per qubit, sends the second half to Bob.
    In the commit phase Bob's marginal is I/2 for either committed bit.
    In the reveal phase Alice chooses to measure in Z (announces b=0) or in
    X (announces b=1); her result is anti-correlated with Bob's in the
    corresponding basis, so Bob cannot detect the cheat.
    """
    from qiskit import QuantumCircuit
    # 1 EPR pair, s=1 for clarity; extendable
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)     # qubit 0 = Alice, qubit 1 = Bob
    sv = Statevector.from_instruction(qc)

    # Bob's marginal (trace out Alice = qubit 0)
    rhoB = partial_trace(sv, [0])
    rhoB_arr = np.asarray(rhoB.data)
    id_over_2 = 0.5 * np.eye(2)
    max_norm = float(np.max(np.abs(rhoB_arr - id_over_2)))

    # Cheating: measure Alice's qubit in Z -> Bob's collapses; alternatively
    # in X.  Compute conditional Bob-density given Alice's outcome.
    from qiskit.quantum_info import Pauli
    # Z on Alice = qubit 0; project onto |0><0|_A x I and |1><1|_A x I
    P0 = np.diag([1, 1, 0, 0]).astype(complex)   # (|00><00| + |01><01|) in q1 q0
    P1 = np.diag([0, 0, 1, 1]).astype(complex)
    v = np.asarray(sv.data)
    p0 = float(np.real(v.conj() @ P0 @ v))
    p1 = float(np.real(v.conj() @ P1 @ v))

    RESULTS["P3_bb84_epr_cheat"] = {
        "bob_marginal_is_maximally_mixed_max_norm": max_norm,
        "alice_Z_outcome_prob0": p0,
        "alice_Z_outcome_prob1": p1,
        "note": ("Bob marginal = I/2 => concealing; Alice can pick basis at "
                 "reveal time via EPR correlation => cheating undetectable"),
    }
    print("=== PART 3: BB84 EPR-attack sanity ===")
    print(f"  ||rho_B - I/2||_inf = {max_norm:.3e}   (should be 0)")
    print(f"  Prob(Alice Z outcome 0/1) = {p0:.4f} / {p1:.4f}")
    print()


# ------------------------------------------------------------------
if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=True)
    run_part1_ideal()
    run_part2_nonideal()
    run_part3_bb84_epr_cheat()
    with open(OUT_JSON, "w") as fh:
        json.dump(RESULTS, fh, indent=2)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {CSV_TRADEOFF}")
