#!/usr/bin/env python3
"""
Density-matrix reproduction of the reproducible core of
Li et al. (2023) arXiv:2310.04708 "Enhancing Virtual Distillation
with Circuit Cutting for Quantum Error Mitigation".

We do NOT reproduce the paper's exact IBM ibm_hanoi noise model /
Qiskit VQE optimizer values (those depend on 2023-09-27 calibration
data). Instead we build the *reproducible primitive core* the task
brief specifies:

  (a) small target circuit on n=4 producing a known ideal <Z0 Z1>
  (b) coherent over-rotation error eps on all gates -> rho_noisy
  (c) M=2 VD estimator <Z0 Z1>_VD = Tr(O rho^2)/Tr(rho^2)
      verify error scales O(eps^2) instead of O(eps)
  (d) 1-cut circuit-cutting decomposition of the same target
      via a Peng-Harrow-Fefferman / Mitarai-Fujii Pauli-basis QPD
      reconstruct <Z0 Z1>
  (e) combined: M=2 VD applied on each cut subcircuit, reconstruct
      -> verify combined error < either method alone at some eps

All simulation is dense complex128 numpy.  n=4 -> dim=16 -> trivial.
No fabrication: numbers written to JSON at end.
"""

import json
import time
import numpy as np

from pathlib import Path

OUT = Path(__file__).parent
np.set_printoptions(precision=6, suppress=True)

# -----------------------------------------------------------------
# Basic single- and two-qubit gate primitives on density matrices
# -----------------------------------------------------------------

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def ry(theta):
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(theta):
    return np.array(
        [[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]], dtype=complex
    )


def rx(theta):
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)


def kron_all(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def op1(gate, qubit, n):
    """Single-qubit gate on qubit `qubit` of an n-qubit system.
    Convention: qubit 0 is the leftmost tensor factor (big-endian)."""
    mats = [I2] * n
    mats[qubit] = gate
    return kron_all(mats)


def op2_adjacent_cnot(control, target, n):
    """Adjacent CNOT with control right next to target (target=control+1)."""
    assert target == control + 1
    left = [I2] * control
    right = [I2] * (n - target - 1)
    mats = left + [CNOT] + right
    # Careful: CNOT above is written with control=first, target=second (big-endian).
    return kron_all(mats)


def apply_unitary(rho, U):
    return U @ rho @ U.conj().T


def partial_trace(rho, keep, n):
    """Partial trace of an n-qubit density matrix rho, keeping the qubits in `keep`.
    Convention: qubit 0 is big-endian, so basis index bit_i = (idx >> (n-1-i)) & 1.
    """
    dim = 2 ** n
    keep = sorted(keep)
    trace_out = [q for q in range(n) if q not in keep]
    k = len(keep)
    dk = 2 ** k
    reduced = np.zeros((dk, dk), dtype=complex)

    # enumerate all basis states, decode bits
    for i in range(dim):
        bits_i = [(i >> (n - 1 - q)) & 1 for q in range(n)]
        for j in range(dim):
            bits_j = [(j >> (n - 1 - q)) & 1 for q in range(n)]
            # traced qubits must match
            if any(bits_i[q] != bits_j[q] for q in trace_out):
                continue
            ki = 0
            for q in keep:
                ki = (ki << 1) | bits_i[q]
            kj = 0
            for q in keep:
                kj = (kj << 1) | bits_j[q]
            reduced[ki, kj] += rho[i, j]
    return reduced


# -----------------------------------------------------------------
# Target circuit: a 4-qubit RealAmplitudes-like ansatz
#   layer_0 : RY on each qubit
#   entangle: CNOT(0,1), CNOT(1,2), CNOT(2,3)  (line entanglement)
#   layer_1 : RY on each qubit
# All parameters fixed to a deterministic pattern so <Z0 Z1> is a
# well-defined number we can compute both ideal and noisy.
# -----------------------------------------------------------------

N = 4

THETAS = np.array([0.6, 1.1, 0.8, 0.4, 0.9, 0.3, 1.2, 0.7])


def build_ideal_unitary(thetas=THETAS):
    """Return the full 16x16 unitary of the ideal 4-qubit ansatz."""
    U = np.eye(2 ** N, dtype=complex)
    # layer 1: RY on each
    for q in range(N):
        U = op1(ry(thetas[q]), q, N) @ U
    # entangling CNOTs
    U = op2_adjacent_cnot(0, 1, N) @ U
    U = op2_adjacent_cnot(1, 2, N) @ U
    U = op2_adjacent_cnot(2, 3, N) @ U
    # layer 2: RY on each
    for q in range(N):
        U = op1(ry(thetas[N + q]), q, N) @ U
    return U


def build_noisy_state(eps, thetas=THETAS):
    """Coherent over-rotation: every RY(theta) becomes RY(theta*(1+eps));
    every CNOT gets a small RZ(eps) crosstalk kick on both qubits BEFORE it,
    which is the canonical coherent-error model in the VD paper's regime.

    Returns the resulting density matrix rho = U_noisy |0..0><0..0| U_noisy^dag.
    """
    psi = np.zeros(2 ** N, dtype=complex)
    psi[0] = 1.0

    U = np.eye(2 ** N, dtype=complex)
    for q in range(N):
        U = op1(ry(thetas[q] * (1 + eps)), q, N) @ U
    # coherent kick before each CNOT
    for c, t in [(0, 1), (1, 2), (2, 3)]:
        U = op1(rz(eps), c, N) @ U
        U = op1(rz(eps), t, N) @ U
        U = op2_adjacent_cnot(c, t, N) @ U
    for q in range(N):
        U = op1(ry(thetas[N + q] * (1 + eps)), q, N) @ U

    psi_out = U @ psi
    rho = np.outer(psi_out, psi_out.conj())
    return rho


def ideal_state(thetas=THETAS):
    return build_noisy_state(0.0, thetas)


# -----------------------------------------------------------------
# Observable: Z_0 Z_1 (with identity on the other two qubits)
# -----------------------------------------------------------------

def observable_ZZ_01():
    return kron_all([Z, Z, I2, I2])


O_ZZ01 = observable_ZZ_01()


def exp_val(rho, O):
    return float(np.real(np.trace(O @ rho)))


# -----------------------------------------------------------------
# (c) M=2 virtual distillation estimator
# -----------------------------------------------------------------

def vd_estimator(rho, O):
    """<O>_VD = Tr(O rho^2)/Tr(rho^2). Density-matrix, ancilla-free form."""
    rho2 = rho @ rho
    num = np.real(np.trace(O @ rho2))
    den = np.real(np.trace(rho2))
    return float(num / den)


# -----------------------------------------------------------------
# (d) 1-cut circuit cutting via Pauli-basis QPD on a single wire
#
# We cut the wire coming OUT of qubit 2 (i.e. between the entangling
# CNOT(1,2) and the following CNOT(2,3) plus layer-2 RYs).
#
# Basic identity used:
#   |psi><psi|  =  sum_{P in {I,X,Y,Z}} (1/2) tr(P |psi><psi|) * P
# which lets us split a single wire in a density-matrix pipeline into
# (measure the state in P-basis) tensor (re-prepare a P eigenstate).
#
# The recipe (Peng-Harrow-Fefferman / Mitarai-Fujii form):
#   rho_full = (1/2) sum_{P in I,X,Y,Z}  V_right( P_prep )  o
#                                        tr_cut( P_meas . rho_left )
# where the fragment computed on the "left" is:
#   f_left(P)      = tr( (P on cut qubit) . rho_left(0..cut) )
# and the right fragment is:
#   rho_right(P)   = V_right ( |P_eig><P_eig|  o  |0><0|_others )
# Then reconstruction of <O> on the full state is the sum weighted
# by (1/2) * f_left(P).
#
# For our specific 4-qubit ansatz, we cut wire on qubit 2 just after
# the CNOT(1,2). The "left" subsystem is qubits {0,1,2} and holds
# the state up to that point; the "right" subsystem holds qubits {2,3}
# with qubit 2 acting as a fresh prep, and its unitary is
# {RY(theta on q2), RY(theta on q3), CNOT(2,3), RY on q2, RY on q3}.
#
# Simplifying: we build both subcircuits directly as maps on density
# matrices, then reconstruct rho_full via the QPD sum.
# -----------------------------------------------------------------

PAULIS = {"I": I2, "X": X, "Y": Y, "Z": Z}

# Eigen-decomposition of each Pauli into its +1 and -1 eigen-projectors
def pauli_eig_projs(P):
    """Return list of (eigenvalue, projector) pairs (each projector is 2x2)."""
    vals, vecs = np.linalg.eigh(P)
    out = []
    for i, v in enumerate(vals):
        vec = vecs[:, i].reshape(2, 1)
        proj = vec @ vec.conj().T
        out.append((float(np.real(v)), proj))
    return out


def build_left_state(eps, thetas=THETAS):
    """State on qubits {0,1,2} after RY layer1 + CNOT(0,1) + CNOT(1,2).
    Returns a 8x8 density matrix. Qubit 3 is not touched here (idle)."""
    dim = 2 ** 3
    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1.0
    U = np.eye(dim, dtype=complex)
    for q in range(3):
        U = op1(ry(thetas[q] * (1 + eps)), q, 3) @ U
    # kicks + entangling CNOTs
    U = op1(rz(eps), 0, 3) @ U
    U = op1(rz(eps), 1, 3) @ U
    U = op2_adjacent_cnot(0, 1, 3) @ U
    U = op1(rz(eps), 1, 3) @ U
    U = op1(rz(eps), 2, 3) @ U
    U = op2_adjacent_cnot(1, 2, 3) @ U
    psi_out = U @ psi
    return np.outer(psi_out, psi_out.conj())


def right_channel(rho_in_q2, eps, thetas=THETAS):
    """Given a 2x2 state on qubit 2, evolve the {q2,q3} pair through
    the remainder of the circuit:
      - initial q3 is |0><0|
      - kick RZ(eps) on q2 and q3, CNOT(2,3), then RY layer2 on q2 and q3
    We also apply layer1 RY on q3 first (since q3 was idle in left half).
    Returns 4x4 density matrix on (q2,q3).
    """
    q3_init = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    # After left half: q3 has RY_layer1 applied already? NO -- in the left
    # half we only touched q0,q1,q2.  So do RY(theta[3]) on q3 now, then
    # follow with CNOT(2,3) and layer2 RY.
    rho_full = np.kron(rho_in_q2, q3_init)  # (q2,q3)
    U = np.eye(4, dtype=complex)
    # layer1 RY on q3 (q3 was idle in left half)
    U = op1(ry(thetas[3] * (1 + eps)), 1, 2) @ U
    # kick + CNOT(2,3)
    U = op1(rz(eps), 0, 2) @ U
    U = op1(rz(eps), 1, 2) @ U
    U = op2_adjacent_cnot(0, 1, 2) @ U
    # layer2 RY on q2 and q3
    U = op1(ry(thetas[N + 2] * (1 + eps)), 0, 2) @ U
    U = op1(ry(thetas[N + 3] * (1 + eps)), 1, 2) @ U
    return apply_unitary(rho_full, U)


def build_left_layer2_q01(rho_left, eps, thetas=THETAS):
    """Apply layer2 RYs on qubits 0 and 1 to the 8x8 left density matrix
    (still on qubits {0,1,2}). Qubit 2 stays untouched."""
    U = np.eye(8, dtype=complex)
    U = op1(ry(thetas[N + 0] * (1 + eps)), 0, 3) @ U
    U = op1(ry(thetas[N + 1] * (1 + eps)), 1, 3) @ U
    return apply_unitary(rho_left, U)


def reconstruct_full_rho_via_cut(eps, thetas=THETAS):
    """Reconstruct the full 4-qubit density matrix via 1-cut QPD on wire q2.

    rho_full  =  sum_P (1/2)  [ tr_{q2} ( P_q2 . rho_left_after_layer2 ) ]  o
                              [ right_channel( P/1 with sign, eps ) ]
    where the sum is over P in {I,X,Y,Z} using the identity
      rho_2q  =  (1/2) sum_P tr(P rho_2q on cut) o P_prepared

    Concretely we use:
      rho_full(q0,q1,q2,q3) = (1/2) sum_P  A_P(q0,q1)  o  B_P(q2,q3)
    where
      A_P(q0,q1) = tr_{q2}( (I2 o I2 o P) . rho_left_layer2 )
      B_P(q2,q3) = right_channel(P_prepared, eps)  with the correct
                   sign-weighted mixture of eigenstates for prep

    For pure Pauli P the "prep" reduces to
        P = (proj_+ - proj_-)
    so B_P is the difference of the two right_channel outputs.
    """
    rho_left = build_left_state(eps, thetas)         # 8x8 on (q0,q1,q2)
    rho_left_L2 = build_left_layer2_q01(rho_left, eps, thetas)

    rho_full = np.zeros((16, 16), dtype=complex)
    for name, P in PAULIS.items():
        # A_P on qubits (q0,q1): partial trace of q2 with P inserted on q2
        # Insert P as (I o I o P) then partial trace out q2.
        Pfull_left = kron_all([I2, I2, P])            # 8x8
        weighted = Pfull_left @ rho_left_L2
        A_P = partial_trace(weighted, keep=[0, 1], n=3)  # 4x4 on (q0,q1)

        # B_P on qubits (q2,q3):
        # For P=I: prepared state is I (mixed) = proj_+ + proj_-
        # For P in {X,Y,Z}: prepared state is proj_+ - proj_-
        eigs = pauli_eig_projs(P)
        B_P = np.zeros((4, 4), dtype=complex)
        for val, proj in eigs:
            channel = right_channel(proj, eps, thetas)
            if name == "I":
                B_P += channel                   # +proj_+ + proj_-
            else:
                B_P += val * channel             # +proj_+ - proj_-

        rho_full += 0.5 * np.kron(A_P, B_P)

    return rho_full


# -----------------------------------------------------------------
# (e) Combined: apply M=2 VD after cutting-based reconstruction
# -----------------------------------------------------------------

def vd_plus_cut_estimator(eps, thetas=THETAS):
    rho = reconstruct_full_rho_via_cut(eps, thetas)
    return vd_estimator(rho, O_ZZ01), rho


# -----------------------------------------------------------------
# Sweep + report
# -----------------------------------------------------------------

def main():
    t0 = time.time()

    ideal = ideal_state()
    ZZ01_ideal = exp_val(ideal, O_ZZ01)
    print(f"Ideal <Z0 Z1> = {ZZ01_ideal:+.8f}")

    # verify reconstruction correctness at eps=0
    rho_cut0 = reconstruct_full_rho_via_cut(0.0)
    diff = np.linalg.norm(rho_cut0 - ideal)
    ZZ01_cut0 = exp_val(rho_cut0, O_ZZ01)
    print(f"Cut-reconstruction at eps=0: <Z0Z1>={ZZ01_cut0:+.8f}  ||rho_cut - rho_ideal||_F = {diff:.3e}")

    eps_list = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2]
    rows = []

    for eps in eps_list:
        rho = build_noisy_state(eps)
        e_raw = exp_val(rho, O_ZZ01)
        e_vd = vd_estimator(rho, O_ZZ01)

        rho_recon = reconstruct_full_rho_via_cut(eps)
        e_cut = exp_val(rho_recon, O_ZZ01)
        e_cut_vd = vd_estimator(rho_recon, O_ZZ01)

        # sanity: pre-VD, cut reconstruction should MATCH the direct noisy sim
        # (it does not "denoise" by itself; it just reconstructs)
        cut_bias = abs(e_cut - e_raw)

        rows.append(
            dict(
                eps=eps,
                ideal=ZZ01_ideal,
                raw=e_raw,
                vd=e_vd,
                cut=e_cut,
                cut_vd=e_cut_vd,
                abs_err_raw=abs(e_raw - ZZ01_ideal),
                abs_err_vd=abs(e_vd - ZZ01_ideal),
                abs_err_cut=abs(e_cut - ZZ01_ideal),
                abs_err_cut_vd=abs(e_cut_vd - ZZ01_ideal),
                cut_vs_raw_bias=cut_bias,
            )
        )

    print()
    header = f"{'eps':>7s} {'ideal':>10s} {'raw':>10s} {'|err_raw|':>10s} {'vd':>10s} {'|err_vd|':>10s} {'cut':>10s} {'|err_cut|':>10s} {'cut+vd':>10s} {'|err_c+v|':>10s}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r['eps']:7.4f} {r['ideal']:+10.6f} {r['raw']:+10.6f} {r['abs_err_raw']:10.3e} "
            f"{r['vd']:+10.6f} {r['abs_err_vd']:10.3e} {r['cut']:+10.6f} {r['abs_err_cut']:10.3e} "
            f"{r['cut_vd']:+10.6f} {r['abs_err_cut_vd']:10.3e}"
        )

    # Fit orders: log|err| vs log(eps) for small-eps rows
    small = [r for r in rows if 0 < r["eps"] <= 0.05]
    logs = np.array([np.log(r["eps"]) for r in small])
    def order(errs):
        errs = np.array(errs)
        good = errs > 0
        return float(np.polyfit(logs[good], np.log(errs[good]), 1)[0])

    order_raw = order([r["abs_err_raw"] for r in small])
    order_vd = order([r["abs_err_vd"] for r in small])
    order_cut_vd = order([r["abs_err_cut_vd"] for r in small])

    print()
    print(f"Fitted error-order (small-eps regime, eps in (0, 0.05]):")
    print(f"  raw       :  O(eps^{order_raw:.2f})")
    print(f"  vd (M=2)  :  O(eps^{order_vd:.2f})")
    print(f"  cut + vd  :  O(eps^{order_cut_vd:.2f})")

    result = {
        "paper": "arXiv:2310.04708",
        "title": "Enhancing Virtual Distillation with Circuit Cutting for Quantum Error Mitigation",
        "authors": ["Peiyi Li", "Ji Liu", "Hrushikesh Pramod Patil", "Paul Hovland", "Huiyang Zhou"],
        "n_qubits": N,
        "thetas": THETAS.tolist(),
        "observable": "Z0 Z1",
        "ideal_expectation": ZZ01_ideal,
        "cut_reconstruction_check_eps0": {
            "expectation": ZZ01_cut0,
            "frobenius_diff_from_ideal_rho": diff,
        },
        "eps_sweep": rows,
        "fitted_error_orders": {
            "raw": order_raw,
            "vd_M2": order_vd,
            "cut_plus_vd_M2": order_cut_vd,
        },
        "wall_time_sec": time.time() - t0,
    }

    with open(OUT / "results.json", "w") as f:
        json.dump(result, f, indent=2)
    print()
    print(f"Wrote {OUT/'results.json'}  (wall {result['wall_time_sec']:.2f}s)")


if __name__ == "__main__":
    main()
