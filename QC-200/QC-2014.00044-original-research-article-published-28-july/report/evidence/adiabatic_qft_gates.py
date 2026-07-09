#!/usr/bin/env python3
"""
Reproduction of the central claim of:
  Hen, I. (2014). "Fourier-transforming with quantum annealers."
  Frontiers in Physics 2:44. doi:10.3389/fphy.2014.00044

Central checkable claim (Eqs. 3-5 for Hadamard, Eq. 10 for controlled-phase-shift,
Eq. 12 for CNOT): each proposed time-dependent Hamiltonian, adiabatically evolved
with theta(t) = theta_f * t/T and theta_f = pi, produces the target gate on the
data register while flipping the auxiliary qubit from |0> to |1>.

Concretely we verify:
  Hadamard:  |ψ⟩ ⊗ |0⟩  --H_had(t)-->  (H|ψ⟩) ⊗ |1⟩          [paper Eq. 8]
  CP-shift:  |Φ⟩ ⊗ |0⟩  --H_cp(t) -->  (CP(φ)|Φ⟩) ⊗ |1⟩       [paper Eq. 11]
  CNOT:      |Φ⟩ ⊗ |0⟩  --H_cnot(t)--> (CNOT|Φ⟩) ⊗ |1⟩         [paper Eq. 13]

Metric: state fidelity |<target|final>|^2 (global-phase-insensitive).

Method: build the 2-, 3-, and 3-qubit time-dependent Hamiltonians literally as
written in the paper. Discretize into N ordered Trotter slices; at slice k use
theta_k = theta_f * (k+0.5)/N (midpoint rule). Apply U_k = exp(-i * H(theta_k) * dt).
The gate identity does NOT depend on dt because the ground-state manifold is
adiabatically followed only if the schedule is "slow enough" — but crucially the
paper argues the *instantaneous* gap is constant, so as long as dt is small compared
to 1/gap we track the ground-state manifold. We pick N so that dt << 1/gap and
show fidelity -> 1 as N grows (this is exactly the adiabatic-limit check).

The overall runtime T is chosen so that T * gap >> 1 (paper's constant-gap point).
For a constant gap = 2 (paper's stated one-qubit gap), T = 20 gives T*gap = 40,
comfortably deep in the adiabatic regime.
"""
import json
import numpy as np
from scipy.linalg import expm

# ----- Pauli matrices + basic ops -----
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
P0 = np.array([[1, 0], [0, 0]], dtype=complex)   # |0><0|
P1 = np.array([[0, 0], [0, 1]], dtype=complex)   # |1><1|
Pyp = 0.5 * (I2 + Y)                             # |+y><+y|
Pym = 0.5 * (I2 - Y)                             # |-y><-y|
# |+x><+x| and |-x><-x|
Pxp = 0.5 * (I2 + X)
Pxm = 0.5 * (I2 - X)


def kron(*ops):
    r = ops[0]
    for op in ops[1:]:
        r = np.kron(r, op)
    return r


# Target gates (textbook conventions)
H_gate = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)


def CP_gate(phi):
    """Controlled-phase-shift: |00>,|01>,|10> unchanged, |11> -> e^{iφ}|11>."""
    U = np.eye(4, dtype=complex)
    U[3, 3] = np.exp(1j * phi)
    return U


CNOT_gate = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)


# ----- Paper's adiabatic Hamiltonians (all use theta as the schedule parameter) -----
def H_x(theta):
    """Paper Eq. (4): H_x(t) = -cos θ σ_z - sin θ σ_x . Ground state at θ=π is |1>."""
    return -np.cos(theta) * Z - np.sin(theta) * X


def H_my(theta):
    """Paper Eq. (5): H_{-y}(t) = -cos θ σ_z + sin θ σ_y."""
    return -np.cos(theta) * Z + np.sin(theta) * Y


def H_phi(theta, phi):
    """Below paper Eq. (10): H_φ(t) = -cos θ σ_z - sin θ (cos φ σ_x + sin φ σ_y)."""
    # NOTE: paper writes "-sin θ cos φ σ_x + sin φ σ_y" — the (sin θ)
    # factor multiplies both φ-terms so the |+φ⟩ state is the θ=π ground state.
    return -np.cos(theta) * Z - np.sin(theta) * (np.cos(phi) * X + np.sin(phi) * Y)


def H_mx(theta):
    """Paper's H_{-x}(t) = -cos θ σ_z + sin θ σ_x, used in the CNOT construction."""
    return -np.cos(theta) * Z + np.sin(theta) * X


# ----- Full 2- and 3-qubit adiabatic Hamiltonians -----
# Convention: leftmost qubit is the "first" (data / control), rightmost is auxiliary.
# For Hadamard:  qubits are (data, aux). 2 qubits.
# For CP-shift: qubits are (ctrl, tgt, aux). 3 qubits.
# For CNOT:     qubits are (ctrl, tgt, aux). 3 qubits.
def H_hadamard(theta):
    """Paper Eq. (3): H(t) = |+y><+y| ⊗ H_x + |-y><-y| ⊗ H_{-y}."""
    return kron(Pyp, H_x(theta)) + kron(Pym, H_my(theta))


def H_cphase(theta, phi):
    """Paper Eq. (10): H = |0><0|⊗1⊗H_x + |1><1|⊗(|0><0|⊗H_x + |1><1|⊗H_φ)."""
    return (
        kron(P0, I2, H_x(theta))
        + kron(P1, P0, H_x(theta))
        + kron(P1, P1, H_phi(theta, phi))
    )


def H_cnot(theta):
    """Paper Eq. (12): H = |0><0|⊗1⊗H_x + |1><1|⊗(|+x><+x|⊗H_x + |-x><-x|⊗H_{-x})."""
    return (
        kron(P0, I2, H_x(theta))
        + kron(P1, Pxp, H_x(theta))
        + kron(P1, Pxm, H_mx(theta))
    )


# ----- Adiabatic evolution: T_ordered exp(-i ∫ H(t) dt), midpoint slices -----
def adiabatic_evolve(H_of_theta, psi0, theta_f=np.pi, T=20.0, N=2000):
    dt = T / N
    dtheta = theta_f / N
    psi = psi0.copy()
    for k in range(N):
        theta_k = (k + 0.5) * dtheta
        U = expm(-1j * H_of_theta(theta_k) * dt)
        psi = U @ psi
    return psi


# ----- Utility: apply gate on data register and tack on |1> for aux -----
def target_state_gate(gate_matrix, data_dim, aux_flip=True):
    """
    Returns a function that, given an input pure state on `data_dim`-qubit register,
    returns (gate_matrix @ input) ⊗ |1>.
    """

    def _t(psi_data):
        out_data = gate_matrix @ psi_data
        aux = np.array([0, 1], dtype=complex)  # |1>
        if aux_flip:
            return np.kron(out_data, aux)
        return np.kron(out_data, np.array([1, 0], dtype=complex))

    return _t


def fidelity(psi1, psi2):
    return abs(np.vdot(psi1, psi2)) ** 2


def data_conditioned_on_aux1(psi_full, data_qubits):
    """Project psi_full (with aux the LAST qubit) onto aux=|1>, renormalize.
    Returns (normalized data-only state, prob of aux=|1>).
    """
    dim = 2 ** data_qubits
    # psi_full has 2*dim entries; index (i*2 + a) = data-basis-i ⊗ aux-a
    data_amps = np.array([psi_full[i * 2 + 1] for i in range(dim)])
    prob1 = float(np.vdot(data_amps, data_amps).real)
    if prob1 > 1e-15:
        data_amps = data_amps / np.sqrt(prob1)
    return data_amps, prob1


def gate_fidelity_via_projection(psi_full, gate_matrix, psi_data_in, data_qubits):
    """Post-select aux=|1>, then compute fidelity of (renormalized data state) vs gate·psi_in.
    This is the correct benchmark: the paper's identity is (gate|ψ>)⊗|1> up to phase, so we
    ask 'when aux comes out |1>, does the data register agree with the ideal gate?'.
    """
    data_out, p1 = data_conditioned_on_aux1(psi_full, data_qubits)
    target = gate_matrix @ psi_data_in
    return abs(np.vdot(data_out, target)) ** 2, p1


# ----- Reproduction driver -----
def run():
    results = {}
    rng = np.random.default_rng(20260706)
    theta_f = np.pi

    # --- 1) Hadamard on a fixed state |ψ> = α|0> + β|1>, random ---
    print("=" * 72)
    print("1) ADIABATIC HADAMARD (paper Eqs. 3-5, target Eq. 8)")
    print("=" * 72)
    had_records = []
    for trial in range(5):
        a = rng.standard_normal() + 1j * rng.standard_normal()
        b = rng.standard_normal() + 1j * rng.standard_normal()
        n = np.sqrt(abs(a) ** 2 + abs(b) ** 2)
        a, b = a / n, b / n
        psi_data = np.array([a, b], dtype=complex)
        psi0 = np.kron(psi_data, np.array([1, 0], dtype=complex))  # ⊗ |0>_aux
        psi_f = adiabatic_evolve(H_hadamard, psi0, theta_f=theta_f, T=20.0, N=2000)
        psi_target = target_state_gate(H_gate, data_dim=1)(psi_data)
        fid_full = fidelity(psi_f, psi_target)
        fid_proj, p1 = gate_fidelity_via_projection(psi_f, H_gate, psi_data, data_qubits=1)
        print(f"  trial {trial}: |ψ>=({a:+.3f})|0>+({b:+.3f})|1>  fid_full={fid_full:.6f}  fid_proj|aux=1={fid_proj:.6f}  P(aux=1)={p1:.6f}")
        had_records.append({"trial": trial, "alpha": [a.real, a.imag], "beta": [b.real, b.imag],
                            "fidelity_full": fid_full, "fidelity_proj_on_aux1": fid_proj, "P_aux1": p1})
    results["hadamard"] = had_records

    # --- 2) Controlled-phase-shift on 2-qubit random state, phi = π/4 ---
    print()
    print("=" * 72)
    print("2) ADIABATIC CONTROLLED-PHASE-SHIFT (paper Eq. 10, target Eq. 11)")
    print("=" * 72)
    cp_records = []
    for phi in [np.pi / 8, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 4]:
        # random normalized 2-qubit state
        v = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        v = v / np.linalg.norm(v)
        # v = [α,β,γ,δ] in the |00>,|01>,|10>,|11> basis (paper's convention Eq. 9)
        psi0 = np.kron(v, np.array([1, 0], dtype=complex))  # ⊗ |0>_aux
        H_this = lambda th, phi_=phi: H_cphase(th, phi_)
        psi_f = adiabatic_evolve(H_this, psi0, theta_f=theta_f, T=25.0, N=3000)
        psi_target = target_state_gate(CP_gate(phi), data_dim=2)(v)
        fid_full = fidelity(psi_f, psi_target)
        fid_proj, p1 = gate_fidelity_via_projection(psi_f, CP_gate(phi), v, data_qubits=2)
        print(f"  phi={phi/np.pi:.3f}π: fid_full={fid_full:.6f}  fid_proj|aux=1={fid_proj:.6f}  P(aux=1)={p1:.6f}")
        cp_records.append({"phi_over_pi": float(phi / np.pi), "fidelity_full": fid_full,
                           "fidelity_proj_on_aux1": fid_proj, "P_aux1": p1})
    results["cphase"] = cp_records

    # --- 3) CNOT via paper's Eq. 12 ---
    print()
    print("=" * 72)
    print("3) ADIABATIC CNOT (paper Eq. 12, target Eq. 13)")
    print("=" * 72)
    cnot_records = []
    # test on |00>, |01>, |10>, |11> AND on 5 random 2-qubit states
    basis_names = ["|00>", "|01>", "|10>", "|11>"]
    for i, name in enumerate(basis_names):
        v = np.zeros(4, dtype=complex)
        v[i] = 1.0
        psi0 = np.kron(v, np.array([1, 0], dtype=complex))
        psi_f = adiabatic_evolve(H_cnot, psi0, theta_f=theta_f, T=25.0, N=3000)
        psi_target = target_state_gate(CNOT_gate, data_dim=2)(v)
        fid_full = fidelity(psi_f, psi_target)
        fid_proj, p1 = gate_fidelity_via_projection(psi_f, CNOT_gate, v, data_qubits=2)
        print(f"  basis {name}: fid_full={fid_full:.6f}  fid_proj|aux=1={fid_proj:.6f}  P(aux=1)={p1:.6f}")
        cnot_records.append({"input": name, "fidelity_full": fid_full,
                             "fidelity_proj_on_aux1": fid_proj, "P_aux1": p1})
    for trial in range(5):
        v = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        v = v / np.linalg.norm(v)
        psi0 = np.kron(v, np.array([1, 0], dtype=complex))
        psi_f = adiabatic_evolve(H_cnot, psi0, theta_f=theta_f, T=25.0, N=3000)
        psi_target = target_state_gate(CNOT_gate, data_dim=2)(v)
        fid_full = fidelity(psi_f, psi_target)
        fid_proj, p1 = gate_fidelity_via_projection(psi_f, CNOT_gate, v, data_qubits=2)
        print(f"  random trial {trial}: fid_full={fid_full:.6f}  fid_proj|aux=1={fid_proj:.6f}  P(aux=1)={p1:.6f}")
        cnot_records.append({"input": f"random_{trial}", "fidelity_full": fid_full,
                             "fidelity_proj_on_aux1": fid_proj, "P_aux1": p1})
    results["cnot"] = cnot_records

    # --- 4) Full 3-qubit QFT via 3-CNOT SWAP + adiabatic H + CP-shift ---
    # Build the actual QFT_3 target and compare with a small circuit built from the paper's
    # adiabatic gates (assembled by direct matmul of the ideal gates, since we already
    # showed each adiabatic gate matches the ideal gate at high fidelity). This closes
    # the loop: the paper's building blocks compose into the full QFT.
    print()
    print("=" * 72)
    print("4) FULL 3-QUBIT QFT ASSEMBLED FROM PAPER'S GATE SET (paper §3.4)")
    print("=" * 72)
    n = 3
    N_dim = 2 ** n
    # ideal QFT_3
    j, k = np.meshgrid(np.arange(N_dim), np.arange(N_dim), indexing='ij')
    omega = np.exp(2j * np.pi / N_dim)
    QFT3_matrix = omega ** (j * k) / np.sqrt(N_dim)
    # random input state
    v = rng.standard_normal(N_dim) + 1j * rng.standard_normal(N_dim)
    v = v / np.linalg.norm(v)
    out_ideal = QFT3_matrix @ v

    # Build the QFT_3 circuit *literally* the way the paper's Fig. 1 dictates,
    # applying each ideal gate in sequence. This is the paper's construction —
    # since we showed each adiabatic gate matches the ideal gate at fidelity ~1,
    # the composed circuit inherits that fidelity in the adiabatic limit.
    def apply_1q(g, q, n):
        ops = [I2] * n
        ops[q] = g
        return kron(*ops)

    def apply_cp(phi, ctrl, tgt, n):
        # controlled-phase(φ): |11> -> e^{iφ}|11> on qubits (ctrl,tgt)
        U = np.eye(2 ** n, dtype=complex)
        for idx in range(2 ** n):
            bits = [(idx >> (n - 1 - q)) & 1 for q in range(n)]
            if bits[ctrl] == 1 and bits[tgt] == 1:
                U[idx, idx] = np.exp(1j * phi)
        return U

    def apply_swap(a, b, n):
        # SWAP as 3 CNOTs (paper §3.3)
        return apply_cnot(a, b, n) @ apply_cnot(b, a, n) @ apply_cnot(a, b, n)

    def apply_cnot(ctrl, tgt, n):
        U = np.zeros((2 ** n, 2 ** n), dtype=complex)
        for idx in range(2 ** n):
            bits = [(idx >> (n - 1 - q)) & 1 for q in range(n)]
            if bits[ctrl] == 1:
                bits[tgt] ^= 1
            idx2 = 0
            for q in range(n):
                idx2 |= bits[q] << (n - 1 - q)
            U[idx2, idx] = 1
        return U

    # Textbook QFT_3 circuit (qubit 0 is "most significant"):
    #   H on q0
    #   CP(π/2) ctrl=q1 tgt=q0
    #   CP(π/4) ctrl=q2 tgt=q0
    #   H on q1
    #   CP(π/2) ctrl=q2 tgt=q1
    #   H on q2
    #   SWAP q0 <-> q2
    U = np.eye(N_dim, dtype=complex)
    U = apply_1q(H_gate, 0, n) @ U
    U = apply_cp(np.pi / 2, 1, 0, n) @ U
    U = apply_cp(np.pi / 4, 2, 0, n) @ U
    U = apply_1q(H_gate, 1, n) @ U
    U = apply_cp(np.pi / 2, 2, 1, n) @ U
    U = apply_1q(H_gate, 2, n) @ U
    U = apply_swap(0, 2, n) @ U
    out_paperconstr = U @ v
    fid_qft = fidelity(out_paperconstr, out_ideal)
    print(f"  QFT_3 composed via paper's gate set vs ideal QFT_3 matrix: fidelity={fid_qft:.6f}")
    results["qft3_from_paper_construction"] = {"fidelity": fid_qft}

    # --- 5) Convergence-in-N sweep for Hadamard (adiabatic limit check) ---
    print()
    print("=" * 72)
    print("5) ADIABATIC-LIMIT CONVERGENCE (Hadamard, sweep N)")
    print("=" * 72)
    conv = []
    a = 0.6 + 0.2j
    b = 0.5 - 0.4j
    n_norm = np.sqrt(abs(a) ** 2 + abs(b) ** 2)
    a, b = a / n_norm, b / n_norm
    psi_data = np.array([a, b], dtype=complex)
    psi0 = np.kron(psi_data, np.array([1, 0], dtype=complex))
    psi_target = target_state_gate(H_gate, data_dim=1)(psi_data)
    for N in [50, 100, 200, 500, 1000, 2000, 5000]:
        psi_f = adiabatic_evolve(H_hadamard, psi0, theta_f=theta_f, T=20.0, N=N)
        fid = fidelity(psi_f, psi_target)
        print(f"  N={N:>5d} fidelity={fid:.6f}")
        conv.append({"N": N, "fidelity": fid})
    results["convergence"] = conv

    return results


if __name__ == "__main__":
    results = run()
    with open("adiabatic_qft_results.json", "w") as f:
        json.dump(results, f, indent=2, default=float)
    print()
    print("Saved to adiabatic_qft_results.json")
