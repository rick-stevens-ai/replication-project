"""
VQE with UCCSD ansatz on LiH (STO-3G) at a few bond lengths.
Demonstrates the same canonical pipeline (surveyed in arXiv:1812.09976)
on a slightly larger active-space molecule.

LiH STO-3G: 6 spatial orbs -> 12 spin-orbs. To keep classical simulation
compact + fast, we freeze the Li 1s core and use an active space of 3
spatial orbs (6 spin-orbs = 6 qubits) around HOMO/LUMO. This is the standard
'active-space' approximation described in the review.
"""
import json
import os
import time
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

SYMBOLS = ["Li", "H"]
BOND_LENGTHS = [1.2, 1.5, 1.595, 1.8, 2.2, 2.8]  # 1.595 A ~ exp. equilibrium

ACTIVE_ELECTRONS = 2
ACTIVE_ORBITALS = 3   # -> 6 qubits (JW)


def run_lih(bond_a):
    coords = np.array([[0.0, 0.0, 0.0],
                       [0.0, 0.0, bond_a]])
    H, qubits = qml.qchem.molecular_hamiltonian(
        SYMBOLS,
        coords,
        charge=0,
        mult=1,
        basis="STO-3G",
        method="pyscf",
        unit="angstrom",
        active_electrons=ACTIVE_ELECTRONS,
        active_orbitals=ACTIVE_ORBITALS,
    )
    hf_state = qml.qchem.hf_state(ACTIVE_ELECTRONS, qubits)
    singles, doubles = qml.qchem.excitations(ACTIVE_ELECTRONS, qubits)
    s_wires, d_wires = qml.qchem.excitations_to_wires(singles, doubles)
    n_params = len(singles) + len(doubles)

    dev = qml.device("default.qubit", wires=qubits)

    @qml.qnode(dev, diff_method="backprop")
    def circuit(params):
        qml.UCCSD(params, wires=range(qubits), s_wires=s_wires, d_wires=d_wires, init_state=hf_state)
        return qml.expval(H)

    params = pnp.zeros(n_params, requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=0.4)

    e_hist = []
    max_iter = 80
    conv_tol = 1e-8
    for it in range(max_iter):
        params, e = opt.step_and_cost(circuit, params)
        e_hist.append(float(e))
        if it > 0 and abs(e_hist[-1] - e_hist[-2]) < conv_tol:
            break
    e_vqe = float(e_hist[-1])

    # Exact reference in the same active space
    H_mat = H.sparse_matrix().toarray()
    eigvals = np.linalg.eigvalsh(H_mat)
    e_fci = float(eigvals[0])

    return {
        "bond_A": bond_a,
        "n_qubits": int(qubits),
        "n_uccsd_params": int(n_params),
        "vqe_energy_Ha": e_vqe,
        "fci_energy_Ha": e_fci,
        "abs_error_Ha": abs(e_vqe - e_fci),
        "abs_error_mHa": abs(e_vqe - e_fci) * 1000.0,
        "iterations": len(e_hist),
    }


def main():
    t0 = time.time()
    results = []
    for r in BOND_LENGTHS:
        print(f"[LiH bond = {r:.3f} A] ... ", end="", flush=True)
        res = run_lih(r)
        print(f"E_VQE = {res['vqe_energy_Ha']:.6f} Ha, E_FCI(active) = {res['fci_energy_Ha']:.6f} Ha, "
              f"err = {res['abs_error_mHa']:.3f} mHa, qubits = {res['n_qubits']}, iters = {res['iterations']}")
        results.append(res)
    elapsed = time.time() - t0

    out = {
        "system": "LiH",
        "basis": "STO-3G",
        "active_space": f"{ACTIVE_ELECTRONS}e, {ACTIVE_ORBITALS}o",
        "mapping": "Jordan-Wigner",
        "ansatz": "UCCSD (in active space)",
        "reference": "arXiv:1812.09976 (Cao et al. 2018)",
        "pennylane_version": qml.__version__,
        "bond_lengths_A": BOND_LENGTHS,
        "results": results,
        "elapsed_seconds": elapsed,
    }
    outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "report", "evidence"))
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "lih_vqe_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    with open(os.path.join(outdir, "lih_vqe_results.csv"), "w") as f:
        f.write("bond_A,vqe_energy_Ha,fci_energy_Ha,abs_error_mHa,iterations\n")
        for r in results:
            f.write(f"{r['bond_A']},{r['vqe_energy_Ha']:.8f},{r['fci_energy_Ha']:.8f},"
                    f"{r['abs_error_mHa']:.6f},{r['iterations']}\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 5))
    bond = [r["bond_A"] for r in results]
    ax.plot(bond, [r["fci_energy_Ha"] for r in results], "k-o", label="FCI (active-space exact diag)")
    ax.plot(bond, [r["vqe_energy_Ha"] for r in results], "b--x", label="VQE + UCCSD (PennyLane)")
    ax.set_xlabel("Li–H bond length (Å)")
    ax.set_ylabel("Ground-state energy (Ha)")
    ax.set_title(f"LiH potential-energy curve, STO-3G basis, ({ACTIVE_ELECTRONS}e,{ACTIVE_ORBITALS}o) active space, JW\ndemonstrating framework generalization (Cao et al. 2018)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "lih_pes.png"), dpi=140)

    max_err = max(r["abs_error_mHa"] for r in results)
    mean_err = sum(r["abs_error_mHa"] for r in results) / len(results)
    print(f"\n[LiH summary] max |VQE-FCI| = {max_err:.3f} mHa, mean = {mean_err:.3f} mHa, "
          f"elapsed = {elapsed:.1f} s")
    print(f"Wrote: {outdir}/lih_vqe_results.json, .csv, lih_pes.png")


if __name__ == "__main__":
    main()
