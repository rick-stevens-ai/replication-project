#!/usr/bin/env python3
"""
Independent replication for arXiv:2106.06463
"Quantum Chemistry Calculations using Energy Derivatives on Quantum Computers"
Azad & Singh (2021).

Reproduces:
  - VQE ground-state energy for H2 (STO-3G, 4 qubits) at several bond lengths.
  - Nuclear gradient dE/dR via (a) finite-difference and (b) Hellmann-Feynman.
  - Comparison against classical FCI energy + PySCF classical gradient.
  - Paper's headline: equilibrium bond length ~0.74 Å, E_min ~ -1.137 Ha.

Runs entirely on classical simulation (pennylane default.qubit / lightning.qubit)
- 4 qubits, Jordan-Wigner, Givens-rotation ansatz on HF reference |1100>.
"""
import json
import time
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

BOND_LENGTHS = [0.60, 0.70, 0.735, 0.80, 0.90]  # Angstroms
FD_STEP = 0.005  # Angstrom, symmetric finite-difference step for dE/dR

BOHR_PER_ANGSTROM = 1.0 / 0.529177210903  # PennyLane uses Bohr internally when unit='bohr'; we pass Å directly.


def build_H2_hamiltonian(bond_length_A):
    """Build H2 Hamiltonian at given bond length (Angstroms), STO-3G, JW mapping."""
    symbols = ["H", "H"]
    coordinates = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, bond_length_A]])
    H, qubits = qml.qchem.molecular_hamiltonian(
        symbols,
        coordinates,
        basis="sto-3g",
        mapping="jordan_wigner",
        unit="angstrom",
    )
    return H, qubits


def build_ansatz(num_qubits, num_electrons):
    """
    Simple hardware-efficient / chemistry-inspired ansatz:
    - HF reference (num_electrons in lowest orbitals) then a SingleExcitation+DoubleExcitation
      pair on the (1100) HOMO<->LUMO transition. For 4 qubits/2 electrons, one DoubleExcitation
      (0,1)->(2,3) captures the essential correlation.
    """
    hf_state = qml.qchem.hf_state(num_electrons, num_qubits)
    # Excitation generators for 4-qubit H2:
    singles, doubles = qml.qchem.excitations(num_electrons, num_qubits)
    # doubles = [[0,1,2,3]], singles = [[0,2],[1,3]] for 4-qubit H2
    n_params = len(singles) + len(doubles)

    def circuit(params, wires):
        qml.BasisState(hf_state, wires=wires)
        p = 0
        for s in singles:
            qml.SingleExcitation(params[p], wires=s)
            p += 1
        for d in doubles:
            qml.DoubleExcitation(params[p], wires=d)
            p += 1

    return circuit, n_params


def vqe_energy_and_params(bond_length_A, init_params=None, max_iter=200, tol=1e-8, verbose=False):
    """Run VQE at given bond length. Return (energy, optimal_params, H, num_qubits)."""
    H, num_qubits = build_H2_hamiltonian(bond_length_A)
    circuit, n_params = build_ansatz(num_qubits, num_electrons=2)

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def cost_fn(params):
        circuit(params, wires=range(num_qubits))
        return qml.expval(H)

    if init_params is None:
        params = pnp.zeros(n_params, requires_grad=True)
    else:
        params = pnp.array(init_params, requires_grad=True)

    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    prev_energy = None
    for it in range(max_iter):
        params, energy = opt.step_and_cost(cost_fn, params)
        if prev_energy is not None and abs(prev_energy - energy) < tol:
            break
        prev_energy = energy
        if verbose and it % 20 == 0:
            print(f"  iter {it:3d} E={energy:.8f}")
    final_energy = float(cost_fn(params))
    return final_energy, np.array(params), H, num_qubits


def fci_energy(bond_length_A):
    """Classical FCI reference via PySCF."""
    from pyscf import gto, scf, fci
    mol = gto.Mole()
    mol.atom = f"H 0 0 0; H 0 0 {bond_length_A}"
    mol.basis = "sto-3g"
    mol.unit = "Angstrom"
    mol.verbose = 0
    mol.build()
    mf = scf.RHF(mol).run(verbose=0)
    cisolver = fci.FCI(mf)
    e_fci, _ = cisolver.kernel()
    return float(e_fci)


def pyscf_gradient(bond_length_A):
    """Classical CI-based gradient at STO-3G, FCI is equivalent to CISD for H2 (2e-)."""
    from pyscf import gto, scf, grad
    mol = gto.Mole()
    mol.atom = f"H 0 0 0; H 0 0 {bond_length_A}"
    mol.basis = "sto-3g"
    mol.unit = "Angstrom"
    mol.verbose = 0
    mol.build()
    mf = scf.RHF(mol).run(verbose=0)
    # For H2 STO-3G (2 electrons, 2 orbitals) HF is not exact; use FCI energy but gradient
    # via numerical differentiation of FCI (analytical FCI grad not always available).
    return None  # We'll compare via FD of FCI instead.


def fci_gradient_fd(bond_length_A, h=FD_STEP):
    """dE_FCI/dR via central finite difference on classical FCI energy (Ha / Angstrom)."""
    e_plus = fci_energy(bond_length_A + h)
    e_minus = fci_energy(bond_length_A - h)
    return (e_plus - e_minus) / (2 * h)


def vqe_gradient_fd(bond_length_A, h=FD_STEP, init_params=None):
    """
    dE_VQE/dR via central finite difference on VQE energy (Ha / Angstrom).
    Re-optimizes VQE at each shifted geometry, warm-starting from init_params.
    """
    e_plus, p_plus, _, _ = vqe_energy_and_params(bond_length_A + h, init_params=init_params)
    e_minus, p_minus, _, _ = vqe_energy_and_params(bond_length_A - h, init_params=init_params)
    return (e_plus - e_minus) / (2 * h), p_plus, p_minus


def vqe_gradient_hellmann_feynman(bond_length_A, opt_params, h=FD_STEP):
    """
    Hellmann-Feynman-style analytical derivative:
      dE/dR = <psi(theta*)| dH/dR |psi(theta*)>
    with fixed optimal parameters theta* and dH/dR estimated by central FD on the
    Hamiltonian coefficients at bond_length_A ± h.

    This is analogous to the paper's Eq. 8 / Eq. 20 approach: differentiate the
    Hamiltonian (parameter of the chemical system) at fixed VQE state.
    """
    # Build H at R, R+h, R-h. Since H(R) has different Pauli strings potentially,
    # we compute <H_plus> - <H_minus> / 2h on the SAME state |psi(theta*, R)>.
    H_center, num_qubits = build_H2_hamiltonian(bond_length_A)
    H_plus, _ = build_H2_hamiltonian(bond_length_A + h)
    H_minus, _ = build_H2_hamiltonian(bond_length_A - h)

    circuit, n_params = build_ansatz(num_qubits, num_electrons=2)
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def expval_H(params, ham):
        circuit(params, wires=range(num_qubits))
        return qml.expval(ham)

    params = pnp.array(opt_params, requires_grad=False)
    ep = float(expval_H(params, H_plus))
    em = float(expval_H(params, H_minus))
    return (ep - em) / (2 * h)


def main():
    t0 = time.time()
    results = {"bond_lengths_A": BOND_LENGTHS, "fd_step_A": FD_STEP, "per_R": []}

    print("=" * 78)
    print("Independent replication: arXiv:2106.06463")
    print("VQE + energy derivatives for H2 (STO-3G, 4 qubits)")
    print("=" * 78)
    print(f"PennyLane {qml.__version__}")

    init_params = None
    for R in BOND_LENGTHS:
        print(f"\n--- Bond length R = {R:.3f} Å ---")
        # VQE ground state
        e_vqe, params_opt, H, nqubits = vqe_energy_and_params(R, init_params=init_params)
        init_params = params_opt  # warm-start next R
        # FCI reference
        e_fci = fci_energy(R)
        # HF for context
        from pyscf import gto, scf
        mol = gto.Mole()
        mol.atom = f"H 0 0 0; H 0 0 {R}"
        mol.basis = "sto-3g"
        mol.unit = "Angstrom"
        mol.verbose = 0
        mol.build()
        mf = scf.RHF(mol).run(verbose=0)
        e_hf = float(mf.e_tot)
        # Gradients
        g_fci = fci_gradient_fd(R)
        g_vqe_fd, _, _ = vqe_gradient_fd(R, init_params=params_opt)
        g_vqe_hf = vqe_gradient_hellmann_feynman(R, params_opt)

        diff_energy_mHa = (e_vqe - e_fci) * 1000
        diff_grad_fd_vs_fci = g_vqe_fd - g_fci
        diff_grad_hf_vs_fci = g_vqe_hf - g_fci

        print(f"  qubits={nqubits}, VQE params={len(params_opt)}")
        print(f"  E_HF   = {e_hf:.8f} Ha")
        print(f"  E_FCI  = {e_fci:.8f} Ha")
        print(f"  E_VQE  = {e_vqe:.8f} Ha   Δ(VQE-FCI) = {diff_energy_mHa:+.4f} mHa")
        print(f"  dE/dR classical(FCI, FD) = {g_fci:+.6f} Ha/Å")
        print(f"  dE/dR VQE (FD)           = {g_vqe_fd:+.6f} Ha/Å   Δ = {diff_grad_fd_vs_fci:+.2e}")
        print(f"  dE/dR VQE (Hellmann-F.)  = {g_vqe_hf:+.6f} Ha/Å   Δ = {diff_grad_hf_vs_fci:+.2e}")

        results["per_R"].append({
            "R_A": R,
            "n_qubits": nqubits,
            "n_params": len(params_opt),
            "E_HF_Ha": e_hf,
            "E_FCI_Ha": e_fci,
            "E_VQE_Ha": e_vqe,
            "diff_VQE_FCI_mHa": diff_energy_mHa,
            "dEdR_FCI_HaPerA": g_fci,
            "dEdR_VQE_FD_HaPerA": g_vqe_fd,
            "dEdR_VQE_HellmannFeynman_HaPerA": g_vqe_hf,
            "params_opt": params_opt.tolist(),
        })

    # Paper's headline: minimum near R=0.74 Å, E_min ~ -1.137 Ha
    energies = [r["E_VQE_Ha"] for r in results["per_R"]]
    idx_min = int(np.argmin(energies))
    R_min = BOND_LENGTHS[idx_min]
    E_min = energies[idx_min]
    results["summary"] = {
        "R_min_sampled_A": R_min,
        "E_min_sampled_Ha": E_min,
        "paper_headline_R_A": 0.741,
        "paper_headline_E_Ha": -1.137,
        "chemical_accuracy_Ha": 1.6e-3,
        "runtime_sec": time.time() - t0,
    }

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Best sampled VQE point: R={R_min:.3f} Å, E={E_min:.6f} Ha")
    print(f"Paper headline:          R=0.741 Å, E=-1.137 Ha")
    print(f"|ΔE| = {abs(E_min + 1.137)*1000:.4f} mHa  (chemical accuracy = 1.6 mHa)")

    # Save JSON evidence
    out_json = "/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2106.06463-qc-chem-energy-derivatives/report/evidence/vqe_h2_gradients.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nEvidence JSON: {out_json}")
    print(f"Runtime: {results['summary']['runtime_sec']:.1f} s")


if __name__ == "__main__":
    main()
