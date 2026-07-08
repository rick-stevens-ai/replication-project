"""
VQE with UCCSD ansatz on H2 (STO-3G) over a range of bond lengths.
Reproduces the canonical VQE/UCC quantum-chemistry pipeline surveyed in
Cao, Romero, Olson, ..., Aspuru-Guzik (2018), arXiv:1812.09976.

Compares VQE energy against FCI (exact diagonalization of the qubit Hamiltonian)
at each bond length. Writes JSON + CSV evidence + a PNG plot.
"""
import json
import time
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

# --- H2 in STO-3G: 4 spin-orbitals -> 4 qubits (Jordan-Wigner)
SYMBOLS = ["H", "H"]
BOND_LENGTHS = [0.4, 0.6, 0.741, 0.9, 1.2, 1.5, 2.0, 2.5]   # in Angstrom (0.741 A is exp. equil.)

def run_h2(bond_a):
    """Build H2 Hamiltonian at given H-H bond length (Angstrom), run VQE+UCCSD, return dict."""
    # PennyLane wants coords in Bohr by default (units='bohr'), we pass Angstrom via units flag
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
    )
    electrons = 2
    hf_state = qml.qchem.hf_state(electrons, qubits)

    # UCCSD: build all single + double excitations
    singles, doubles = qml.qchem.excitations(electrons, qubits)
    s_wires, d_wires = qml.qchem.excitations_to_wires(singles, doubles)
    n_params = len(singles) + len(doubles)

    dev = qml.device("default.qubit", wires=qubits)

    @qml.qnode(dev, diff_method="backprop")
    def circuit(params):
        qml.UCCSD(params, wires=range(qubits), s_wires=s_wires, d_wires=d_wires, init_state=hf_state)
        return qml.expval(H)

    # Init params near zero (HF is close to ground state for H2 near equilibrium)
    params = pnp.zeros(n_params, requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=0.4)

    e_hist = []
    max_iter = 60
    conv_tol = 1e-8
    for it in range(max_iter):
        params, e = opt.step_and_cost(circuit, params)
        e_hist.append(float(e))
        if it > 0 and abs(e_hist[-1] - e_hist[-2]) < conv_tol:
            break
    e_vqe = float(e_hist[-1])

    # Exact reference: diagonalize the Hamiltonian matrix (this is FCI in this basis)
    H_sparse = H.sparse_matrix()
    # small system -> dense diag is fine
    H_dense = H_sparse.toarray()
    eigvals = np.linalg.eigvalsh(H_dense)
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
        print(f"[H2 bond = {r:.3f} A] ... ", end="", flush=True)
        res = run_h2(r)
        print(f"E_VQE = {res['vqe_energy_Ha']:.6f} Ha, E_FCI = {res['fci_energy_Ha']:.6f} Ha, "
              f"err = {res['abs_error_mHa']:.3f} mHa, iters = {res['iterations']}")
        results.append(res)
    elapsed = time.time() - t0

    out = {
        "system": "H2",
        "basis": "STO-3G",
        "mapping": "Jordan-Wigner",
        "ansatz": "UCCSD",
        "reference": "arXiv:1812.09976 (Cao et al. 2018)",
        "pennylane_version": qml.__version__,
        "bond_lengths_A": BOND_LENGTHS,
        "results": results,
        "elapsed_seconds": elapsed,
    }
    import os
    outdir = os.path.join(os.path.dirname(__file__), "..", "report", "evidence")
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "h2_vqe_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    with open(os.path.join(outdir, "h2_vqe_results.csv"), "w") as f:
        f.write("bond_A,vqe_energy_Ha,fci_energy_Ha,abs_error_mHa,iterations\n")
        for r in results:
            f.write(f"{r['bond_A']},{r['vqe_energy_Ha']:.8f},{r['fci_energy_Ha']:.8f},"
                    f"{r['abs_error_mHa']:.6f},{r['iterations']}\n")

    # Plot
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 5))
    bond = [r["bond_A"] for r in results]
    ax.plot(bond, [r["fci_energy_Ha"] for r in results], "k-o", label="FCI (exact diag)")
    ax.plot(bond, [r["vqe_energy_Ha"] for r in results], "r--x", label="VQE + UCCSD (PennyLane)")
    ax.set_xlabel("H–H bond length (Å)")
    ax.set_ylabel("Ground-state energy (Ha)")
    ax.set_title("H$_2$ potential-energy curve, STO-3G basis, JW mapping\nreproducing the canonical VQE/UCC pipeline (Cao et al. 2018)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "h2_pes.png"), dpi=140)

    max_err = max(r["abs_error_mHa"] for r in results)
    mean_err = sum(r["abs_error_mHa"] for r in results) / len(results)
    print(f"\n[H2 summary] max |VQE-FCI| = {max_err:.3f} mHa, mean = {mean_err:.3f} mHa, "
          f"elapsed = {elapsed:.1f} s")
    print(f"Wrote: {outdir}/h2_vqe_results.json, .csv, h2_pes.png")

if __name__ == "__main__":
    main()
