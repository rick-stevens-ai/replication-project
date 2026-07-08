#!/usr/bin/env python3
"""
VQE baseline for H2/STO-3G: reproduces the ground-state energy curve vs
bond distance to within a few mHa of exact / FCI (full CI on 4 qubits =
exact for STO-3G / minimal basis).

The paper (Wang, Higgott, Brierley 2018, arXiv:1802.00171) proposes an
acceleration of the *measurement subroutine* inside VQE (alpha-VQE / alpha-QPE).
The chemistry test-bed used implicitly throughout the VQE literature the
paper builds on is H2/STO-3G (see e.g. Peruzzo 2014, O'Malley 2016,
McClean 2016 - all cited by the paper). Reproducing the *VQE energy
accuracy* on that test-bed is the minimum reproducible core of any
VQE-family paper, and we do that here.

We do:
    1. Build the H2/STO-3G electronic Hamiltonian at N bond lengths
       (Bohr) using PennyLane + PySCF.
    2. Compute the exact ground-state energy by direct diagonalisation of
       the 4-qubit Hamiltonian matrix (= FCI for STO-3G / minimal basis).
    3. Run VQE with a hardware-efficient / UCCSD-style ansatz and
       gradient-based optimisation on `default.qubit` (statevector sim).
    4. Compare VQE energy to exact at each bond length; report max/mean
       absolute error. Target: < 1.6 mHa (chemical accuracy) at every
       bond length; a "few mHa" is acceptable per the wave brief.
"""
from __future__ import annotations

import json
import os
import time

import numpy as np
import pennylane as qml
from pennylane import qchem

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "report", "evidence")
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "figures")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def build_h2_hamiltonian(bond_bohr: float):
    """Return (H, n_qubits) for H2 at given bond distance (bohr, STO-3G)."""
    sym = ["H", "H"]
    coord = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, float(bond_bohr)]])
    H, qubits = qchem.molecular_hamiltonian(sym, coord, basis="STO-3G",
                                            method="pyscf", unit="bohr")
    return H, qubits


def exact_ground_state_energy(H) -> float:
    mat = qml.matrix(H)
    evals = np.linalg.eigvalsh(mat)
    return float(evals[0].real)


def run_vqe(H, qubits: int, max_iters: int = 200, tol: float = 1e-8,
            seed: int = 42) -> tuple[float, np.ndarray, list[float]]:
    """UCCSD-like ansatz on 4 qubits for 2-electron H2. Return (E, params, history)."""
    hf = qml.qchem.hf_state(electrons=2, orbitals=qubits)
    singles, doubles = qml.qchem.excitations(electrons=2, orbitals=qubits)
    s_wires, d_wires = qml.qchem.excitations_to_wires(singles, doubles)
    dev = qml.device("default.qubit", wires=qubits)

    @qml.qnode(dev, interface="autograd")
    def cost(params):
        qml.UCCSD(params, wires=range(qubits), init_state=hf,
                  s_wires=s_wires, d_wires=d_wires)
        return qml.expval(H)

    n_params = len(singles) + len(doubles)
    rng = np.random.default_rng(seed)
    from pennylane import numpy as pnp
    theta = pnp.array(rng.normal(0, 0.05, size=n_params), requires_grad=True)

    opt = qml.AdamOptimizer(stepsize=0.1)
    history = []
    prev = None
    for i in range(max_iters):
        theta, e = opt.step_and_cost(cost, theta)
        e = float(e)
        history.append(e)
        if prev is not None and abs(prev - e) < tol:
            break
        prev = e
    return float(history[-1]), np.array(theta), history


def main() -> None:
    print("[VQE-H2] arXiv:1802.00171 chemistry-baseline reproduction")
    # Bond lengths in bohr: cover the potential-energy curve including the
    # equilibrium (~1.4 bohr) and stretched (~3.0 bohr).
    bond_lengths_bohr = [0.6, 0.8, 1.0, 1.2, 1.401, 1.6, 1.8, 2.0, 2.5, 3.0]
    results = []
    t0 = time.time()
    for r in bond_lengths_bohr:
        print(f"  R = {r:.3f} bohr ...", end=" ", flush=True)
        ta = time.time()
        H, qubits = build_h2_hamiltonian(r)
        e_exact = exact_ground_state_energy(H)
        e_vqe, theta, hist = run_vqe(H, qubits, max_iters=250)
        err_mha = 1000.0 * (e_vqe - e_exact)
        n_iter = len(hist)
        print(f"E_exact={e_exact:+.6f}  E_VQE={e_vqe:+.6f}  "
              f"dE={err_mha:+.3f} mHa  ({n_iter} iter, {time.time()-ta:.1f}s)")
        results.append({
            "R_bohr": r,
            "R_angstrom": r * 0.52917721,
            "n_qubits": int(qubits),
            "E_exact_Ha": e_exact,
            "E_VQE_Ha": e_vqe,
            "abs_error_mHa": abs(err_mha),
            "signed_error_mHa": err_mha,
            "n_opt_iters": n_iter,
            "final_history_last5": hist[-5:],
        })

    total_t = time.time() - t0
    max_err = max(r["abs_error_mHa"] for r in results)
    mean_err = float(np.mean([r["abs_error_mHa"] for r in results]))
    print(f"\n[VQE-H2] total {total_t:.1f}s   "
          f"max |ΔE| = {max_err:.4f} mHa   "
          f"mean |ΔE| = {mean_err:.4f} mHa   "
          f"chemical accuracy (<1.6 mHa) at "
          f"{sum(r['abs_error_mHa'] < 1.6 for r in results)}/{len(results)} points")

    summary = {
        "paper": "arXiv:1802.00171 (Wang, Higgott, Brierley 2018)",
        "test": "VQE baseline: H2/STO-3G ground-state PES vs FCI-exact",
        "n_qubits": 4,
        "ansatz": "UCCSD (PennyLane qml.UCCSD)",
        "optimizer": "Adam, lr=0.1, up to 250 iter, tol 1e-8",
        "device": "default.qubit (statevector)",
        "total_time_s": total_t,
        "max_abs_error_mHa": max_err,
        "mean_abs_error_mHa": mean_err,
        "chem_acc_frac": sum(r['abs_error_mHa'] < 1.6 for r in results) / len(results),
        "points": results,
    }
    with open(os.path.join(OUT_DIR, "vqe_h2_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(OUT_DIR, "vqe_h2_pes.csv"), "w") as f:
        f.write("R_bohr,R_angstrom,E_exact_Ha,E_VQE_Ha,abs_error_mHa\n")
        for r in results:
            f.write(f"{r['R_bohr']:.4f},{r['R_angstrom']:.4f},"
                    f"{r['E_exact_Ha']:.8f},{r['E_VQE_Ha']:.8f},"
                    f"{r['abs_error_mHa']:.6f}\n")
    print(f"[VQE-H2] wrote evidence/vqe_h2_summary.json and vqe_h2_pes.csv")

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        Rs = [r["R_bohr"] for r in results]
        Es = [r["E_exact_Ha"] for r in results]
        Ev = [r["E_VQE_Ha"] for r in results]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
        ax1.plot(Rs, Es, "k-", label="exact / FCI")
        ax1.plot(Rs, Ev, "rx", label="VQE (UCCSD)")
        ax1.set_xlabel("R (bohr)")
        ax1.set_ylabel("Energy (Ha)")
        ax1.set_title("H2 / STO-3G ground-state PES")
        ax1.legend()
        ax1.grid(True, ls=":", alpha=0.5)
        errs = [r["abs_error_mHa"] for r in results]
        ax2.semilogy(Rs, errs, "b-o")
        ax2.axhline(1.6, color="green", ls="--", label="1.6 mHa (chem. acc.)")
        ax2.set_xlabel("R (bohr)")
        ax2.set_ylabel("|E_VQE - E_exact| (mHa)")
        ax2.set_title("VQE error vs exact")
        ax2.grid(True, which="both", ls=":", alpha=0.5)
        ax2.legend()
        fig.tight_layout()
        fig_path = os.path.join(FIG_DIR, "vqe_h2_pes.png")
        fig.savefig(fig_path, dpi=140)
        print(f"[VQE-H2] wrote {fig_path}")
    except Exception as e:
        print(f"[VQE-H2] plot failed: {e}")


if __name__ == "__main__":
    main()
