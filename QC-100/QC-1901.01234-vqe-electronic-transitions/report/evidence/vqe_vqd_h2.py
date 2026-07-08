"""
Companion check: VQE ground state + VQD (Variational Quantum Deflation)
first excited state of H2 in the STO-3G basis (4 qubits, Jordan-Wigner).

This is the task-requested cross-method demo. VQD (Higgott et al. 2019 -
arXiv:1805.08138) is closely related in spirit to MC-VQE (both compute
multiple eigenstates on a QC). We recover E0 and E1 and compare to exact
diagonalization within chemical accuracy (< 1.6 mHa).

We use PennyLane's built-in molecular H2 Hamiltonian at R = 0.742 Å
(equilibrium).
"""
import json, time
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp
from scipy.optimize import minimize

RNG = np.random.default_rng(20260703)

# --- Build H2 electronic Hamiltonian (STO-3G, 4 qubits Jordan-Wigner) ------
symbols = ["H", "H"]
coords = np.array([[0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.742]])  # angstroms (PennyLane wants bohr; use unit='angstrom')

H_mol, n_qubits = qml.qchem.molecular_hamiltonian(
    symbols, coords.flatten(),
    basis="STO-3G", unit="angstrom", mapping="jordan_wigner",
)
try:
    n_terms = len(H_mol.terms()[0])
except Exception:
    n_terms = -1
print(f"H2 Hamiltonian: {n_qubits} qubits, {n_terms} Pauli terms")

# Exact ground/excited energies via full diagonalization of the sparse H
Hmat = qml.matrix(H_mol, wire_order=list(range(n_qubits)))
exact_eigs = np.sort(np.linalg.eigvalsh(Hmat).real)
E0_exact, E1_exact = exact_eigs[0], exact_eigs[1]
print(f"Exact E0 = {E0_exact:.8f} Ha    E1 = {E1_exact:.8f} Ha    gap = {(E1_exact-E0_exact)*1000:.3f} mHa")

# --- Ansatz: hardware-efficient RY + entangling (works for H2 in 4 qubits) --
dev = qml.device("default.qubit", wires=n_qubits)

def ansatz(theta, wires):
    # Start from HF |0011> (2 electrons, JW) using X gates
    qml.PauliX(wires=0); qml.PauliX(wires=1)
    # Layer 1
    for w in wires:
        qml.RY(theta[w], wires=w)
    for a, b in [(0,1),(1,2),(2,3)]:
        qml.CNOT(wires=[a,b])
    # Layer 2
    for w in wires:
        qml.RY(theta[n_qubits + w], wires=w)
    for a, b in [(0,1),(1,2),(2,3)]:
        qml.CNOT(wires=[a,b])
    # Layer 3
    for w in wires:
        qml.RY(theta[2*n_qubits + w], wires=w)

n_params = 3 * n_qubits

@qml.qnode(dev, interface="autograd")
def get_state(theta):
    ansatz(theta, list(range(n_qubits)))
    return qml.state()

def energy(theta, H_matrix):
    psi = get_state(theta)
    return float(np.real(np.conjugate(psi) @ (H_matrix @ psi)))

# --------- VQE for ground state ------------------------------------------
print("\n--- VQE for ground state ---")
t0 = time.time()
best = None
for trial in range(3):
    theta0 = 0.1 * RNG.standard_normal(n_params)
    r = minimize(lambda t: energy(t, Hmat), theta0, method="L-BFGS-B",
                 options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-9})
    if best is None or r.fun < best.fun:
        best = r
theta_g = best.x
E0_vqe = best.fun
t_vqe = time.time() - t0
print(f"VQE E0 = {E0_vqe:.8f} Ha  (exact {E0_exact:.8f})  |err|={abs(E0_vqe-E0_exact)*1000:.4f} mHa   [{t_vqe:.1f}s, iters={best.nit}]")

# --------- VQD for first excited state -----------------------------------
# VQD cost:  L(theta) = <psi(theta)|H|psi(theta)> + beta * |<psi(theta)|psi_g>|^2
# where beta is a penalty larger than gap.
print("\n--- VQD for first excited state ---")
psi_g = get_state(theta_g)
beta = 5.0  # much larger than the H2 gap (~0.65 Ha)

def vqd_cost(theta):
    psi = get_state(theta)
    e = float(np.real(np.conjugate(psi) @ (Hmat @ psi)))
    overlap = abs(np.vdot(psi_g, psi)) ** 2
    return e + beta * overlap

t0 = time.time()
best_e = None
for trial in range(5):
    theta0 = 0.3 * RNG.standard_normal(n_params)
    r = minimize(vqd_cost, theta0, method="L-BFGS-B",
                 options={"maxiter": 800, "ftol": 1e-12, "gtol": 1e-9})
    # Recompute pure energy (drop penalty) for comparison
    psi = get_state(r.x)
    e_pure = float(np.real(np.conjugate(psi) @ (Hmat @ psi)))
    overlap = float(abs(np.vdot(psi_g, psi)) ** 2)
    if best_e is None or e_pure < best_e[0]:
        # Only accept if overlap with ground is small (state actually orthogonal)
        if overlap < 0.05:
            best_e = (e_pure, r, overlap)
if best_e is None:
    print("  VQD failed to find an orthogonal excited state in 5 trials")
    E1_vqd = None; overlap = None
else:
    E1_vqd, res1, overlap = best_e
t_vqd = time.time() - t0
if E1_vqd is not None:
    print(f"VQD E1 = {E1_vqd:.8f} Ha  (exact {E1_exact:.8f})  |err|={abs(E1_vqd-E1_exact)*1000:.4f} mHa"
          f"  <psi|psi_g>^2={overlap:.2e}   [{t_vqd:.1f}s]")

# --- Chemical-accuracy check ---------------------------------------------
chem_acc_Ha = 1.6e-3  # ~ 1 kcal/mol
err0 = abs(E0_vqe - E0_exact)
err1 = abs(E1_vqd - E1_exact) if E1_vqd is not None else None
print("\n=== Chemical-accuracy check (threshold 1.6 mHa) ===")
print(f"  E0 err = {err0*1000:.4f} mHa  {'PASS' if err0 < chem_acc_Ha else 'FAIL'}")
if err1 is not None:
    print(f"  E1 err = {err1*1000:.4f} mHa  {'PASS' if err1 < chem_acc_Ha else 'FAIL'}")

out = {
    "n_qubits": int(n_qubits), "n_pauli_terms": int(n_terms),
    "geometry_R_angstrom": 0.742,
    "E0_exact_Ha": float(E0_exact), "E1_exact_Ha": float(E1_exact),
    "gap_exact_mHa": float((E1_exact - E0_exact) * 1000),
    "E0_vqe_Ha": float(E0_vqe), "E0_err_mHa": float(err0 * 1000),
    "E1_vqd_Ha": float(E1_vqd) if E1_vqd is not None else None,
    "E1_err_mHa": float(err1 * 1000) if err1 is not None else None,
    "vqd_overlap_with_ground": float(overlap) if E1_vqd is not None else None,
    "chemical_accuracy_threshold_mHa": chem_acc_Ha * 1000,
    "E0_within_chem_acc": bool(err0 < chem_acc_Ha),
    "E1_within_chem_acc": bool(err1 < chem_acc_Ha) if err1 is not None else None,
    "vqe_wall_s": t_vqe, "vqd_wall_s": t_vqd,
}
with open("h2_vqe_vqd_results.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nWrote h2_vqe_vqd_results.json")
