"""
VQE for H2 at bond length 0.735 Angstrom (STO-3G, 2-qubit tapered form).

The 4-qubit STO-3G H2 Hamiltonian can be reduced to 2 qubits by symmetry
tapering (Bravyi-Kitaev + Z2 symmetries). We use the well-known 2-qubit
form with coefficients at R = 0.735 A from O'Malley et al. 2016
(PRX 6, 031007) / Kandala et al. 2017:

  H = g0 I + g1 Z0 + g2 Z1 + g3 Z0 Z1 + g4 X0 X1 + g5 Y0 Y1

At R = 0.735 A (standard reference):
  g0 = -0.4804
  g1 = +0.3435
  g2 = -0.4347
  g3 = +0.5716
  g4 = +0.0910
  g5 = +0.0910
(numbers from Kandala 2017 Nature Table 1 / O'Malley 2016 PRX Table 1 form.)

Exact FCI ground state energy of H2 at R=0.735 A / STO-3G ~ -1.1373 Ha.
Chemical accuracy = 1.6 mHa.

Ansatz: hardware-efficient RY + CZ, 2 layers (matches Kandala Fig 1 form)
Real numpy statevector, classical COBYLA minimizer.
"""
import numpy as np
from scipy.optimize import minimize
import json, os, time

# Pauli matrices
I2 = np.eye(2, dtype=np.complex128)
X  = np.array([[0,1],[1,0]], dtype=np.complex128)
Y  = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
Z  = np.array([[1,0],[0,-1]], dtype=np.complex128)

def kron(*ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

# 2-qubit H2 Hamiltonian at R = 0.735 A (STO-3G, tapered)
# Coefficients: O'Malley et al. 2016 PRX 6, 031007 (Table I after tapering)
# NOTE: g["I"] is the *electronic* Hamiltonian constant; the total ground-state
# energy also requires adding the nuclear-repulsion term E_NR = 1 / R (a.u.)
# = 1 / (0.735 / 0.529177) = 0.7137 Ha at R = 0.735 A.
g = {"I": -0.4804, "Z0": 0.3435, "Z1": -0.4347, "Z0Z1": 0.5716,
     "X0X1": 0.0910, "Y0Y1": 0.0910}
E_NR = 1.0 / (0.735 / 0.5291772)   # nuclear repulsion in Ha

# Build 4x4 Hamiltonian matrix
H = ( g["I"]    * kron(I2, I2)
    + g["Z0"]   * kron(Z, I2)
    + g["Z1"]   * kron(I2, Z)
    + g["Z0Z1"] * kron(Z, Z)
    + g["X0X1"] * kron(X, X)
    + g["Y0Y1"] * kron(Y, Y) )

# Exact ground state via diagonalization
eigs = np.linalg.eigvalsh(H)
E_exact = float(eigs[0])
print(f"H2 (R=0.735 A, STO-3G, 2-qubit tapered)")
print(f"Exact ground-state E (diagonalization) = {E_exact:.6f} Ha")
print(f"Literature FCI value ~ -1.1373 Ha (chemical accuracy = 1.6e-3 Ha)")

# Hardware-efficient ansatz: 2 layers of (RY per qubit) + CZ entangler
# 2 qubits, L=2 layers => 3 rotation blocks * 2 qubits = 6 parameters
# Structure: RY(t0)_0 RY(t1)_1  CZ  RY(t2)_0 RY(t3)_1  CZ  RY(t4)_0 RY(t5)_1
# Start state |00>

def ry(t):
    c, s = np.cos(t/2), np.sin(t/2)
    return np.array([[c, -s],[s, c]], dtype=np.complex128)

CZ = np.diag([1,1,1,-1]).astype(np.complex128)

def ansatz(theta):
    psi = np.zeros(4, dtype=np.complex128); psi[0] = 1.0
    U = kron(ry(theta[0]), ry(theta[1]))
    psi = U @ psi
    psi = CZ @ psi
    U = kron(ry(theta[2]), ry(theta[3]))
    psi = U @ psi
    psi = CZ @ psi
    U = kron(ry(theta[4]), ry(theta[5]))
    psi = U @ psi
    return psi

def energy(theta):
    psi = ansatz(theta)
    return float(np.real(psi.conj() @ H @ psi))

# Multi-start VQE
rng = np.random.default_rng(20260705)
best = None
n_restarts = 40
t0 = time.time()
for k in range(n_restarts):
    x0 = rng.uniform(-np.pi, np.pi, size=6)
    res = minimize(energy, x0, method="COBYLA", options={"maxiter": 800, "rhobeg": 0.3})
    if (best is None) or (res.fun < best["E"]):
        best = {"E": float(res.fun), "theta": res.x.tolist(), "k": k}

E_vqe_elec = best["E"]                       # electronic-only
E_vqe_total = E_vqe_elec + E_NR              # total ground-state energy
E_exact_total = E_exact + E_NR
E_FCI_lit = -1.1373
gap_elec = E_vqe_elec - E_exact
gap_vs_FCI_lit = E_vqe_total - E_FCI_lit
chem_acc = 1.6e-3
print(f"\nNuclear repulsion E_NR = {E_NR:.6f} Ha")
print(f"Exact electronic E   = {E_exact:.6f} Ha")
print(f"Exact total E        = {E_exact_total:.6f} Ha  (literature FCI ~ {E_FCI_lit})")
print(f"\nVQE best electronic E = {E_vqe_elec:.6f} Ha  (restart #{best['k']})")
print(f"VQE best total E      = {E_vqe_total:.6f} Ha")
print(f"|E_VQE_total - E_FCI_lit| = {abs(gap_vs_FCI_lit)*1000:.4f} mHa")
print(f"|E_VQE - E_exact (same H)| = {abs(gap_elec)*1000:.4f} mHa")
print(f"Chemical accuracy (1.6 mHa) reached vs FCI literature? {abs(gap_vs_FCI_lit) < chem_acc}")
print(f"elapsed {time.time()-t0:.1f} s")

out = {
    "paper": "arXiv:1710.01022 (Moll et al. IBM 2017)",
    "hamiltonian_source": "O'Malley et al. 2016 PRX 6, 031007 (2-qubit tapered H2 at R=0.735 A / STO-3G)",
    "coefficients": g,
    "E_NR_Ha": E_NR,
    "E_exact_electronic_Ha": E_exact,
    "E_exact_total_Ha": E_exact_total,
    "E_FCI_literature_Ha": E_FCI_lit,
    "E_vqe_electronic_Ha": E_vqe_elec,
    "E_vqe_total_Ha": E_vqe_total,
    "gap_vqe_vs_exact_same_H_mHa": gap_elec * 1000,
    "gap_vqe_total_vs_FCI_literature_mHa": gap_vs_FCI_lit * 1000,
    "chemical_accuracy_mHa": 1.6,
    "chemical_accuracy_reached_vs_FCI_lit": bool(abs(gap_vs_FCI_lit) < chem_acc),
    "ansatz": "hardware-efficient RY+CZ, 2 entangler layers, 6 parameters",
    "n_restarts": n_restarts,
    "best_theta": best["theta"],
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "vqe_h2_results.json"), "w") as f:
    json.dump(out, f, indent=2)
