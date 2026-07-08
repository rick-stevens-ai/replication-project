"""
MC-VQE replication for Parrish et al. 2019 (arXiv:1901.01234)
=============================================================

Implements the *actual* method of the paper (multistate contracted VQE) on a
small ab-initio-style exciton model. Paper uses N=18 monomers (2^18 = 262144
Hilbert space); we use N=2 and N=4 (faithful, tractable). Same Hamiltonian
family (Eq 8: single-Z + XX/XZ/ZX/ZZ two-body), same state-averaged VQE
entangler, same contracted reference states, same classical subspace
diagonalization.

Central paper claim tested: MC-VQE with a single entangler layer produces
excitation energies matching FCI within ~10s of µeV, i.e. well inside
chemical accuracy (1 kcal/mol ~ 43 meV).

Implementation note: to keep runtime tractable we bypass PennyLane's autograd
tracing for the ansatz and build the entangler as a dense unitary via direct
Kronecker products (same math, ~1000x faster for N<=6). Optimization uses
scipy L-BFGS with finite-difference gradients on this dense unitary.
"""
import json, time
import numpy as np
from scipy.optimize import minimize

RNG = np.random.default_rng(20260703)

# --- single-qubit gates ---
I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

def RY(t):  return np.cos(t/2)*I2 - 1j*np.sin(t/2)*Y
def RZ(t):  return np.array([[np.exp(-1j*t/2), 0],[0, np.exp(1j*t/2)]], dtype=complex)

def kron_list(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def single_qubit_gate(U1, target, N):
    """Return 2^N x 2^N unitary that applies U1 on `target` (0=leftmost), identity elsewhere."""
    mats = [I2] * N
    mats[target] = U1
    return kron_list(mats)

def cnot_gate(control, target, N):
    """Return 2^N x 2^N CNOT with control<target OR control>target."""
    dim = 2 ** N
    U = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        bits = [(i >> (N - 1 - k)) & 1 for k in range(N)]
        if bits[control] == 1:
            bits[target] ^= 1
        j = 0
        for k in range(N):
            j |= bits[k] << (N - 1 - k)
        U[j, i] = 1.0
    return U


# --------------------------------------------------------------------------
# 1. Build a small ab-initio-style exciton Hamiltonian (Eq 8 of paper).
# --------------------------------------------------------------------------
def build_exciton_hamiltonian(N, seed=0):
    rng = np.random.default_rng(seed)
    ZA = 0.75 + 0.02 * rng.standard_normal(N)          # eV
    XA = 0.005 * rng.standard_normal(N)                # eV
    coup_scale = 0.03                                  # eV, ~30 meV NN coupling
    E = -0.75 * N

    dim = 2 ** N
    H = E * np.eye(dim, dtype=complex)

    def pauli_string(op_by_wire):
        mats = []
        for w in range(N):
            mats.append(op_by_wire.get(w, I2))
        return kron_list(mats)

    for A in range(N):
        H += ZA[A] * pauli_string({A: Z})
        H += XA[A] * pauli_string({A: X})
    for A in range(N):
        for B in range(A + 1, N):
            # only nearest-neighbour cyclic
            if not (B - A == 1 or (A == 0 and B == N - 1 and N > 2)):
                continue
            xx = coup_scale * (1 + 0.05 * rng.standard_normal())
            xz = 0.2 * coup_scale * rng.standard_normal()
            zx = 0.2 * coup_scale * rng.standard_normal()
            zz = 0.3 * coup_scale * rng.standard_normal()
            H += xx * pauli_string({A: X, B: X})
            H += xz * pauli_string({A: X, B: Z})
            H += zx * pauli_string({A: Z, B: X})
            H += zz * pauli_string({A: Z, B: Z})
    # sanity: Hermitian
    H = 0.5 * (H + H.conj().T)
    return H


# --------------------------------------------------------------------------
# 2. Contracted CIS-like reference states (ground config + singly-excited).
# --------------------------------------------------------------------------
def cis_reference_states(N, Hmat, n_states):
    dim = 2 ** N
    basis_cols = [np.eye(dim)[:, 0]]                       # |0..0>
    for A in range(N):
        idx = 1 << (N - 1 - A)                             # |0..1_A..0>
        basis_cols.append(np.eye(dim)[:, idx])
    B = np.stack(basis_cols, axis=1)
    Hcis = B.T @ Hmat @ B
    Hcis = 0.5 * (Hcis + Hcis.conj().T)
    eigvals, eigvecs = np.linalg.eigh(Hcis)
    ref = B @ eigvecs[:, :n_states]
    return ref.astype(complex), eigvals[:n_states].real


# --------------------------------------------------------------------------
# 3. Build ansatz unitary U(theta) as a dense 2^N x 2^N matrix.
#    Per layer: per-qubit RY+RZ, then a CNOT ladder + ring, then per-qubit RY.
# --------------------------------------------------------------------------
def n_params_for(N, layers):
    return layers * (3 * N)

def ansatz_unitary(theta, N, layers):
    dim = 2 ** N
    U = np.eye(dim, dtype=complex)
    i = 0
    for _ in range(layers):
        for w in range(N):
            U = single_qubit_gate(RY(theta[i]), w, N) @ U; i += 1
            U = single_qubit_gate(RZ(theta[i]), w, N) @ U; i += 1
        for A in range(N - 1):
            U = cnot_gate(A, A + 1, N) @ U
        if N > 2:
            U = cnot_gate(N - 1, 0, N) @ U
        for w in range(N):
            U = single_qubit_gate(RY(theta[i]), w, N) @ U; i += 1
    return U


# --------------------------------------------------------------------------
# 4. MC-VQE: minimize sum_Theta <Phi_Theta| U^dag H U |Phi_Theta>
# --------------------------------------------------------------------------
def mcvqe_run(N, n_states=None, layers=1, seed=0, maxiter=500, n_trials=3):
    Hmat = build_exciton_hamiltonian(N, seed=seed)
    dim = 2 ** N
    if n_states is None:
        n_states = min(N + 1, dim)

    ref_states, cis_energies = cis_reference_states(N, Hmat, n_states)
    n_params = n_params_for(N, layers)

    def sa_cost(theta):
        U = ansatz_unitary(theta, N, layers)
        # Prepared states: U @ ref_states[:, k]
        Psi = U @ ref_states                             # dim x n_states
        # <psi_k | H | psi_k> = diag(Psi^dag H Psi)
        HP = Hmat @ Psi
        return float(np.real(np.sum(np.conjugate(Psi) * HP)))

    best_res = None
    t0 = time.time()
    for trial in range(n_trials):
        theta0 = 0.05 * RNG.standard_normal(n_params)
        r = minimize(sa_cost, theta0, method="L-BFGS-B",
                     options={"maxiter": maxiter, "ftol": 1e-13, "gtol": 1e-10})
        if best_res is None or r.fun < best_res.fun:
            best_res = r
    opt_time = time.time() - t0

    theta_star = best_res.x

    # Subspace Hamiltonian H_ThetaTheta' = <Phi|U^dag H U|Phi'>
    U_star = ansatz_unitary(theta_star, N, layers)
    Psi = U_star @ ref_states
    Hsub = Psi.conj().T @ Hmat @ Psi
    Hsub = 0.5 * (Hsub + Hsub.conj().T)
    mcvqe_eigs = np.linalg.eigvalsh(Hsub).real

    exact_eigs = np.linalg.eigvalsh(Hmat).real
    exact_low = exact_eigs[:n_states]

    return {
        "N": N, "layers": layers, "n_states": n_states, "n_params": n_params,
        "opt_iters": int(best_res.nit), "opt_final_cost_eV": float(best_res.fun),
        "opt_time_s": float(opt_time), "opt_success": bool(best_res.success),
        "n_trials": n_trials,
        "cis_energies_eV": cis_energies.tolist(),
        "mcvqe_energies_eV": mcvqe_eigs.tolist(),
        "exact_lowest_eV": exact_low.tolist(),
        "abs_err_energy_eV": [float(abs(mcvqe_eigs[i] - exact_low[i]))
                              for i in range(n_states)],
    }


def format_res(tag, r):
    print(f"\n=== {tag}  (N={r['N']}, layers={r['layers']}, states={r['n_states']}, params={r['n_params']}) ===")
    print(f"L-BFGS trials={r['n_trials']} best_iters={r['opt_iters']} success={r['opt_success']} "
          f"final SA cost={r['opt_final_cost_eV']:.6f} eV  [{r['opt_time_s']:.1f}s]")
    print("  state |    exact (eV) |   MC-VQE (eV) |  |err| eV     | |err| meV | |err| µeV")
    for i, (e, m, err) in enumerate(zip(r['exact_lowest_eV'], r['mcvqe_energies_eV'], r['abs_err_energy_eV'])):
        print(f"   {i:2d}   | {e:+.6f}    | {m:+.6f}    | {err:.3e}    | {err*1e3:.3f}    | {err*1e6:.1f}")
    if len(r['exact_lowest_eV']) > 1:
        print(f"  excitation-energy errors (µeV) — paper claim 'tens of µeV':")
        for i in range(1, len(r['exact_lowest_eV'])):
            ex_exc = r['exact_lowest_eV'][i] - r['exact_lowest_eV'][0]
            mc_exc = r['mcvqe_energies_eV'][i] - r['mcvqe_energies_eV'][0]
            print(f"    E({i})-E(0):  exact={ex_exc*1e3:+.3f} meV  MC-VQE={mc_exc*1e3:+.3f} meV  err={abs(ex_exc-mc_exc)*1e6:.2f} µeV")


if __name__ == "__main__":
    all_results = {}
    # (N, n_states, layers)
    configs = [
        (2, 3, 1),
        (2, 3, 2),
        (4, 3, 1),
        (4, 3, 2),
        (4, 3, 3),
    ]
    for N, ns, layers in configs:
        tag = f"N{N}_S{ns}_L{layers}"
        r = mcvqe_run(N=N, n_states=ns, layers=layers, seed=42, maxiter=1000, n_trials=3)
        format_res(tag, r)
        all_results[tag] = r
    out = "mcvqe_results.json"
    with open(out, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nWrote {out}")
