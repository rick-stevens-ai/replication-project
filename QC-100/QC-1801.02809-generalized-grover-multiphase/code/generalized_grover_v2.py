#!/usr/bin/env python3
"""
Independent replication of arXiv:1801.02809 -- v2, correct Eq.12 construction.

We build the initial state |Psi_n(t=0)> by directly diagonalizing the
generalized Grover Hamiltonian H = P_S + P_T, identifying the pair of
eigenvalues (1+c_n, 1-c_n) belonging to the n-th block, forming
|eps_n^T> = P_T (|1+c_n> - |1-c_n>) / normalization and
|eps_n^Tbar> = P_Tbar (|1+c_n> + |1-c_n>) / normalization (up to sign
conventions), then constructing |Psi_n(0)> per Eq. 12.

Equivalently, and simpler: the 2D invariant subspace of the Hamiltonian
that mixes T and Tbar for mode n is exactly span(|1+c_n>, |1-c_n>).
The state |Psi_n(0)> lives in this 2D subspace with the specific
coefficients so that at t=pi/(2 c_n), it flips into the pure-T basis state.

Concretely: let v_p = eigenvector with eigenvalue 1+c_n and v_m with
eigenvalue 1-c_n.  Their T-projection lengths are:
  |P_T v_p|^2 = (1+c_n)/2      (from Eq. 9)
  |P_T v_m|^2 = (1-c_n)/2
Their T-projections point along the SAME |eps_n^T>. So
  |eps_n^T> propto P_T v_p  (or -P_T v_m).
And their Tbar-projections point along the SAME |eps_n^Tbar>:
  |eps_n^Tbar> propto P_Tbar v_p (or +P_Tbar v_m).

Then per Eq. 12:
  |Psi_n(0)> = sqrt((1+c_n)/2) v_p + sqrt((1-c_n)/2) v_m
             = sqrt(1-c_n) |eps_n^Tbar>  + [source-space piece]
             = 100% in T at t=pi/(2 c_n).

We evolve BOTH continuous-time (expm) and gate-based (G*O)^k and record
P_T(t) and P_T(k). We reproduce Fig. 2(b),(c) qualitatively.
"""
import json
import numpy as np
from pathlib import Path
from scipy.linalg import expm

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator

RNG_SEED = 20260703
rng = np.random.default_rng(RNG_SEED)

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
DATA.mkdir(parents=True, exist_ok=True)


def random_orthonormal_source_states(D, N, target_indices, rng):
    X = rng.standard_normal((N, D)) + 1j * rng.standard_normal((N, D))
    Q, _ = np.linalg.qr(X.T)
    psi = Q.T
    for n in range(N):
        w = float(np.sum(np.abs(psi[n, target_indices]) ** 2))
        assert w > 1e-9
    return psi


def build_projector(vectors_as_rows):
    V = np.asarray(vectors_as_rows)
    return V.conj().T @ V


def target_basis_projector(D, target_indices):
    P = np.zeros((D, D), dtype=complex)
    for t in target_indices:
        P[t, t] = 1.0
    return P


def unitary_from_projector(P):
    D = P.shape[0]
    return np.eye(D) - 2.0 * P


def find_grover_eigenpair(H, P_T, mode_index):
    """Diagonalize H, find the mode_index-th pair of eigenvalues (1+c, 1-c)
    with c > 0 (ordered by descending c). Return (c, v_plus, v_minus)."""
    w, V = np.linalg.eigh(H)
    # We want pairs (1+c, 1-c) with c > 0.
    # Find eigenvalues > 1 (these are 1+c_n).
    idx_plus = np.where(w > 1 + 1e-6)[0]
    # Sort descending in c_n (i.e. descending in w)
    idx_plus_sorted = idx_plus[np.argsort(-w[idx_plus])]
    if mode_index >= len(idx_plus_sorted):
        raise ValueError(f"mode {mode_index} out of range; only {len(idx_plus_sorted)} pairs")
    i_p = idx_plus_sorted[mode_index]
    lam_p = w[i_p]
    c_n = lam_p - 1.0
    # Find matching 1 - c_n eigenvalue
    target_lam_m = 1.0 - c_n
    diffs = np.abs(w - target_lam_m)
    i_m = int(np.argmin(diffs))
    lam_m = w[i_m]
    assert abs(lam_m - target_lam_m) < 1e-6, f"couldn't pair: got {lam_m} vs expected {target_lam_m}"
    v_p = V[:, i_p]
    v_m = V[:, i_m]

    # Fix phases so that P_T v_p and P_T v_m are parallel (same eps_n^T).
    # Compute their T-components and align sign of v_m so that P_T v_m is
    # anti-parallel to P_T v_p (matches Eq. 9 sign convention: |eps^+> has
    # +|eps^T> and |eps^-> has -|eps^T>).
    Pt_vp = P_T @ v_p
    Pt_vm = P_T @ v_m
    # inner product (should be real up to global phase, and negative)
    ip = np.vdot(Pt_vp, Pt_vm)
    # Rotate v_m by phase so that <Pt_vp, Pt_vm> is a negative real number
    phase = -ip / np.abs(ip) if np.abs(ip) > 1e-12 else 1.0
    v_m = v_m * phase
    return c_n, v_p, v_m


def construct_initial_state_from_H(H, P_T, mode_index):
    """|Psi_n(0)> per Eq. 12, built from the true H eigenvectors."""
    c_n, v_p, v_m = find_grover_eigenpair(H, P_T, mode_index)
    coeff_p = np.sqrt((1 + c_n) / 2.0)
    coeff_m = np.sqrt((1 - c_n) / 2.0)
    Psi = coeff_p * v_p + coeff_m * v_m
    Psi = Psi / np.linalg.norm(Psi)
    return Psi, c_n


def run_gate_iterations(initial_state, U_G, U_O, P_T, k_max):
    U_step = U_G @ U_O
    state = initial_state.astype(complex).copy()
    prob = [float(np.real(state.conj() @ P_T @ state))]
    for k in range(1, k_max + 1):
        state = U_step @ state
        state = state / np.linalg.norm(state)
        prob.append(float(np.real(state.conj() @ P_T @ state)))
    return prob


def run_continuous_time(initial_state, H, P_T, t_vals):
    probs = []
    for t in t_vals:
        U_t = expm(-1j * H * t)
        st = U_t @ initial_state
        p = float(np.real(st.conj() @ P_T @ st))
        probs.append(p)
    return probs


def qiskit_gate_run(initial_state, U_G, U_O, P_T, k_max, n_qubits):
    """Cross-check: run the same iteration inside Qiskit Aer statevector."""
    sim = AerSimulator(method="statevector")
    step_op = Operator(U_G @ U_O)
    probs = []
    for k in range(k_max + 1):
        qc = QuantumCircuit(n_qubits)
        qc.initialize(initial_state.tolist(), range(n_qubits))
        for _ in range(k):
            qc.append(step_op, range(n_qubits))
        qc.save_statevector()
        res = sim.run(qc).result()
        sv = np.asarray(res.get_statevector(qc))
        p = float(np.real(sv.conj() @ P_T @ sv))
        probs.append(p)
    return probs


def standard_grover_qiskit(n_qubits, marked_index, k_iter):
    D = 2 ** n_qubits
    Pmark = np.zeros((D, D), dtype=complex)
    Pmark[marked_index, marked_index] = 1.0
    U_oracle = np.eye(D) - 2.0 * Pmark
    plus = np.ones(D, dtype=complex) / np.sqrt(D)
    Pplus = np.outer(plus, plus.conj())
    U_diff = 2.0 * Pplus - np.eye(D)

    sim = AerSimulator(method="statevector")
    step_op = Operator(U_diff @ U_oracle)
    probs = []
    for k in range(k_iter + 1):
        qc = QuantumCircuit(n_qubits)
        qc.h(range(n_qubits))
        for _ in range(k):
            qc.append(step_op, range(n_qubits))
        qc.save_statevector()
        res = sim.run(qc).result()
        sv = np.asarray(res.get_statevector(qc))
        probs.append(float(np.abs(sv[marked_index]) ** 2))
    return probs


def main():
    n_qubits = 5
    D = 2 ** n_qubits
    N = 5
    M = 5
    k_max = 40

    target_indices = list(range(M))
    psi = random_orthonormal_source_states(D, N, target_indices, rng)
    P_S = build_projector(psi)
    P_T = target_basis_projector(D, target_indices)
    H_gen = P_S + P_T
    U_G = unitary_from_projector(P_S)
    U_O = unitary_from_projector(P_T)

    # Sanity: H eigenspectrum
    w = np.linalg.eigvalsh(H_gen)
    print("H eigenvalues:")
    print(np.round(sorted(w), 6))

    # -- (A) Naive: initial state = |psi_1>
    psi1 = psi[0]
    naive_gate = run_gate_iterations(psi1, U_G, U_O, P_T, k_max)
    naive_cont = run_continuous_time(psi1, H_gen, P_T, np.linspace(0, np.pi * 4, 200))
    # -- (B) Constructed via true H eigenpair (mode 0 = largest c_n)
    Psi_init, c_n = construct_initial_state_from_H(H_gen, P_T, mode_index=0)
    print(f"\nUsing mode 0 with c_n = {c_n:.6f}, expected k_peak ~ pi/(2 c_n) = {np.pi/(2*c_n):.2f}")
    constructed_gate = run_gate_iterations(Psi_init, U_G, U_O, P_T, k_max)
    constructed_cont = run_continuous_time(Psi_init, H_gen, P_T, np.linspace(0, np.pi * 2, 200))
    # -- (B') Qiskit cross-check for constructed init
    qiskit_gate = qiskit_gate_run(Psi_init, U_G, U_O, P_T, k_max, n_qubits)

    # Print gate curves at every k
    print("\nP_T after k gate iterations:")
    print(f"  {'k':>3s}  {'naive':>8s}  {'construct':>10s}  {'qiskit':>8s}")
    for k in range(k_max + 1):
        print(f"  {k:3d}  {naive_gate[k]:8.4f}  {constructed_gate[k]:10.4f}  {qiskit_gate[k]:8.4f}")

    # -- (C) Standard single-target Grover on Qiskit
    std = standard_grover_qiskit(n_qubits, marked_index=0, k_iter=k_max)

    # Peaks
    peak_naive = max(naive_gate); k_naive = int(np.argmax(naive_gate))
    peak_ctr = max(constructed_gate); k_ctr = int(np.argmax(constructed_gate))
    peak_qk = max(qiskit_gate); k_qk = int(np.argmax(qiskit_gate))
    peak_std = max(std); k_std = int(np.argmax(std))
    peak_ctr_cont = max(constructed_cont); t_ctr_cont = np.linspace(0, np.pi * 2, 200)[int(np.argmax(constructed_cont))]

    print(f"\nPeaks: naive_gate={peak_naive:.4f} (k={k_naive}), "
          f"constructed_gate={peak_ctr:.4f} (k={k_ctr}), qiskit={peak_qk:.4f} (k={k_qk}), "
          f"std_grover={peak_std:.4f} (k={k_std})")
    print(f"constructed_cont peak={peak_ctr_cont:.4f} at t={t_ctr_cont:.3f} "
          f"(expected pi/(2 c_n)={np.pi/(2*c_n):.3f})")

    # Save
    out = {
        "paper": "arXiv:1801.02809 (Byrnes, Forster, Tessler 2018)",
        "setup": {"n_qubits": n_qubits, "D": D, "N": N, "M": M,
                  "target_indices": target_indices, "rng_seed": RNG_SEED},
        "H_eigenvalues": [float(x) for x in np.sort(w).tolist()],
        "c_n_mode0": float(c_n),
        "expected_k_peak_pi_over_2c": float(np.pi / (2 * c_n)),
        "expected_t_peak_pi_over_2c": float(np.pi / (2 * c_n)),
        "gate_iterations": {
            "k_range": list(range(k_max + 1)),
            "P_T_naive_init": naive_gate,
            "P_T_constructed_init_numpy": constructed_gate,
            "P_T_constructed_init_qiskit": qiskit_gate,
        },
        "continuous_time": {
            "t_range": np.linspace(0, np.pi * 2, 200).tolist(),
            "P_T_constructed_init": constructed_cont,
        },
        "standard_grover": {
            "k_range": list(range(k_max + 1)),
            "P_T": std,
        },
        "peaks": {
            "peak_P_T_naive_gate": float(peak_naive), "k_naive_gate": k_naive,
            "peak_P_T_constructed_gate_numpy": float(peak_ctr), "k_constructed_gate_numpy": k_ctr,
            "peak_P_T_constructed_gate_qiskit": float(peak_qk), "k_constructed_gate_qiskit": k_qk,
            "peak_P_T_constructed_continuous_time": float(peak_ctr_cont),
            "peak_P_T_standard_grover": float(peak_std), "k_standard_grover": k_std,
        },
        "paper_claim_check": {
            "C1_constructed_state_gives_high_P_T": bool(peak_ctr_cont > 0.98),
            "C1_gate_iteration_gives_high_P_T":    bool(peak_ctr > 0.85),
            "C2_naive_init_reaches_only_low_P_T":  bool(peak_naive < 0.60),
            "C3_qiskit_matches_numpy":             bool(abs(peak_ctr - peak_qk) < 1e-6),
            "C4_standard_grover_single_target_works": bool(peak_std > 0.95),
            "C5_continuous_time_peak_at_pi_over_2c":  bool(abs(t_ctr_cont - np.pi/(2*c_n)) < 0.05),
        },
    }
    (DATA / "v2_summary.json").write_text(json.dumps(out, indent=2))
    print("\nWrote data/v2_summary.json")


if __name__ == "__main__":
    main()
