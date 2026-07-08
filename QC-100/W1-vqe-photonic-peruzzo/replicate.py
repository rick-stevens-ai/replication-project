#!/usr/bin/env python
"""
QC-100 W1 — Classical replication of Peruzzo et al. 2014
"A variational eigenvalue solver on a photonic quantum processor"
Nature Communications 5, 4213 (2014).  doi:10.1038/ncomms5213

WHAT THIS SCRIPT DOES
---------------------
- Build the HeH+ and H2 electronic Hamiltonians in the STO-3G minimal basis
  via PennyLane's bundled differentiable Hartree-Fock + molecular-integral
  path (no PySCF required).
- Map to qubits with the Jordan-Wigner transform -> 4 qubits each
  (HeH+ and neutral H2 both have 2 electrons in 4 spin-orbitals in STO-3G).
- Build a UCCSD ansatz from the HF reference |1100> (this is the same
  flavor of unitary coupled-cluster ansatz the paper highlights as the
  "gold standard" eq. 4-8). It has 3 variational parameters at this size:
  2 singles + 1 double excitation.
- Run VQE with two classical optimizers:
    * Adam gradient descent (the noiseless statevector workhorse) — main.
    * Nelder-Mead simplex (the paper's actual choice on hardware) — also
      run for HeH+ at the equilibrium R as a methods-match cross-check.
- Compare VQE energies to *exact* diagonalization of the qubit Hamiltonian
  restricted to the physical N-electron sector at every bond length.
- Reproduce the dissociation curve (paper's Figure 4) for HeH+ and (bonus)
  for H2. Locate the equilibrium bond length R_eq by quadratic fit.

WHAT THIS DOES NOT DO
---------------------
- Photonic hardware (CNOT-MZ chip, phase shifters, photon counting).
- Shot/Poissonian sampling noise. Noiseless analytic statevector.
- Paper's exact Supplementary Table 2 Pauli coefficients are NOT shipped
  in paper.md, so we rebuild integrals from STO-3G geometry. This gives
  the same molecule and the same FCI ground-state energies to within
  standard convention; the absolute number can differ by a constant
  energy-zero shift versus the Peruzzo Supplementary Table.
- The paper reports E_min in "MJ mol^-1" with values near -2.865 — this
  appears to use a shifted energy zero relative to the bare electronic
  total energy (their figures span -2.4 to -2.9 MJ/mol over the
  dissociation curve, an ~0.5 MJ/mol range that matches OUR
  reduced-curve range; the absolute offset is documented in REPORT.md).

REPRODUCIBILITY
---------------
- Environment: /Users/stevens/opt/anaconda3/envs/pennylane (PennyLane 0.27.0,
  numpy, scipy, matplotlib). No PySCF, no qiskit, no openfermion required
  beyond what PennyLane bundles.
- Coordinates are passed to PennyLane in **Bohr** (atomic units), as the
  PennyLane qchem API requires. R_bohr = R_angstrom * 1.8897259886.
- Seed: 42 + R-index per bond length, 3 random restarts; best kept.
"""

import json
import os
import sys
import time
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp  # autograd-tracked numpy for VQE params
from pennylane import qchem
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(ROOT, "logs")
FIGS = os.path.join(ROOT, "figures")
os.makedirs(LOGS, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

HA_TO_KJMOL = 2625.4996394798254
HA_TO_MJMOL = HA_TO_KJMOL / 1000.0
ANG_TO_BOHR = 1.8897259886
ANG_TO_PM = 100.0
CHEMICAL_ACCURACY_HA = 1.6e-3  # 1.6 mHa ~ 1 kcal/mol


def build_hamiltonian(symbols, coords_ang, charge=0, basis="sto-3g"):
    """Build qubit Hamiltonian via pennylane.qchem (Jordan-Wigner).
    PennyLane requires coordinates in **Bohr**."""
    coords_bohr = np.asarray(coords_ang, dtype=float) * ANG_TO_BOHR
    H, n_qubits = qchem.molecular_hamiltonian(
        symbols, coords_bohr.flatten(),
        charge=charge, basis=basis, mapping="jordan_wigner",
    )
    return H, n_qubits


def exact_ground_in_sector(H, n_qubits, n_electrons):
    """Diagonalize H, return the lowest eigenvalue in the N-electron sector
    (Jordan-Wigner basis state |b_{n-1}...b_0>: bitcount = electron count)."""
    mat = qml.matrix(H, wire_order=range(n_qubits))
    eigs, vecs = np.linalg.eigh(mat)
    N_op = np.array([bin(b).count("1") for b in range(2 ** n_qubits)])
    sector_eigs = []
    for i in range(len(eigs)):
        v = vecs[:, i]
        n_e = float(np.sum(np.abs(v) ** 2 * N_op))
        # eigenstates are pure-N (H conserves number) so this is ~int
        if abs(n_e - n_electrons) < 1e-3:
            sector_eigs.append((eigs[i], n_e))
    sector_eigs.sort()
    e_ground = float(sector_eigs[0][0])
    full_ground = float(eigs[0])
    return e_ground, full_ground, [float(e) for e, _ in sector_eigs[:4]]


def uccsd_cost_factory(H, n_qubits, n_electrons):
    """Return (cost_qnode, n_params, hf_state, singles, doubles)."""
    hf_state = qchem.hf_state(n_electrons, n_qubits)
    singles, doubles = qchem.excitations(n_electrons, n_qubits)
    n_params = len(singles) + len(doubles)
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev, diff_method="backprop")
    def cost(params):
        qml.AllSinglesDoubles(
            weights=params, wires=range(n_qubits),
            hf_state=hf_state, singles=singles, doubles=doubles,
        )
        return qml.expval(H)

    return cost, n_params, hf_state, singles, doubles


def run_vqe_adam(cost, n_params, max_iter=300, n_restarts=3, seed=0,
                 lr=0.1, log_every=50, label="", conv_tol=1e-9, conv_window=10):
    """Adam optimizer (gradient descent). Returns best-of-restarts."""
    best = {"energy_ha": np.inf, "history": [], "params": None,
            "n_iters": 0, "wall_seconds": 0.0}
    for restart in range(n_restarts):
        rng = np.random.default_rng(seed + 1000 * restart)
        # restart 0: start at HF (zeros); other restarts: small random
        if restart == 0:
            theta0 = pnp.zeros(n_params, requires_grad=True)
        else:
            theta0 = pnp.array(rng.uniform(-0.2, 0.2, size=n_params),
                               requires_grad=True)
        history = []
        t0 = time.time()
        params = theta0
        opt = qml.AdamOptimizer(stepsize=lr)
        for it in range(max_iter):
            params, e = opt.step_and_cost(cost, params)
            history.append(float(e))
            if log_every and (it + 1) % log_every == 0:
                print(f"  [{label} r{restart}] iter {it+1:4d}  E = {float(e): .8f} Ha")
            if len(history) > conv_window:
                delta = abs(min(history[-conv_window:]) -
                            min(history[-2 * conv_window:-conv_window]))
                if delta < conv_tol:
                    break
        dt = time.time() - t0
        e_final = float(min(history))
        if e_final < best["energy_ha"]:
            best = {"energy_ha": e_final, "history": history,
                    "params": np.array(params).tolist(),
                    "n_iters": len(history), "wall_seconds": dt,
                    "restart_used": restart}
    return best


def run_vqe_neldermead(cost, n_params, max_iter=500, n_restarts=3, seed=0,
                       log_every=100, label=""):
    """Nelder-Mead (the paper's optimizer). Cost evaluated with grad-untracked params."""
    best = {"energy_ha": np.inf, "history": [], "params": None,
            "n_iters": 0, "wall_seconds": 0.0}

    def cost_np(p):
        # cost qnode accepts plain numpy if not differentiated
        return float(cost(np.asarray(p, dtype=float)))

    for restart in range(n_restarts):
        rng = np.random.default_rng(seed + 2000 * restart)
        theta0 = (np.zeros(n_params) if restart == 0
                  else rng.uniform(-0.3, 0.3, size=n_params))
        history = []
        t0 = time.time()

        def objective(p):
            e = cost_np(p)
            history.append(e)
            if log_every and len(history) % log_every == 0:
                print(f"  [{label} NM r{restart}] eval {len(history):4d}  E = {e: .8f} Ha")
            return e

        res = minimize(objective, theta0, method="Nelder-Mead",
                       options={"xatol": 1e-6, "fatol": 1e-8,
                                "maxiter": max_iter, "adaptive": True})
        dt = time.time() - t0
        if float(res.fun) < best["energy_ha"]:
            best = {"energy_ha": float(res.fun), "history": history,
                    "params": res.x.tolist(), "n_iters": len(history),
                    "wall_seconds": dt, "restart_used": restart}
    return best


def scan_dissociation(symbols, charge, n_electrons, r_values_ang,
                      name="mol", max_iter=250):
    """Compute exact and VQE ground-state energies across bond lengths."""
    results = []
    for i, R in enumerate(r_values_ang):
        coords = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, R]])
        print(f"\n=== {name}  R = {R:.3f} Å  ({R*ANG_TO_PM:.1f} pm) ===")
        H, n_qubits = build_hamiltonian(symbols, coords, charge=charge)
        e_exact, e_full, sector_eigs = exact_ground_in_sector(H, n_qubits, n_electrons)
        print(f"  exact (N={n_electrons}): {e_exact: .8f} Ha   "
              f"(full lowest = {e_full: .6f}, qubits={n_qubits}, terms={len(H.ops)})")
        cost, n_params, hf, singles, doubles = uccsd_cost_factory(H, n_qubits, n_electrons)
        vqe = run_vqe_adam(cost, n_params, max_iter=max_iter, n_restarts=3,
                           seed=42 + i, label=f"{name} R={R:.3f}")
        err_mha = (vqe["energy_ha"] - e_exact) * 1000.0
        chem_ok = abs(vqe["energy_ha"] - e_exact) < CHEMICAL_ACCURACY_HA
        print(f"  vqe (Adam)  : {vqe['energy_ha']: .8f} Ha   "
              f"err = {err_mha:+.5f} mHa   chem_acc={chem_ok}   "
              f"iters={vqe['n_iters']}  ({vqe['wall_seconds']:.1f}s)  "
              f"n_params={n_params}")
        # Variational principle sanity check
        assert vqe["energy_ha"] >= e_exact - 1e-7, \
            f"Variational principle violated at R={R}"
        results.append({
            "R_ang": float(R), "R_pm": float(R * ANG_TO_PM),
            "n_qubits": int(n_qubits), "n_pauli_terms": int(len(H.ops)),
            "n_uccsd_params": int(n_params),
            "e_exact_sector_ha": float(e_exact),
            "e_full_lowest_ha": float(e_full),
            "sector_eigs_ha": sector_eigs,
            "e_vqe_ha": float(vqe["energy_ha"]),
            "err_mha": float(err_mha),
            "chemical_accuracy": bool(chem_ok),
            "vqe_n_iters": int(vqe["n_iters"]),
            "vqe_wall_seconds": float(vqe["wall_seconds"]),
        })
    return results


def plot_dissociation(results, title, outpath,
                      exact_label="Exact FCI (STO-3G, N=2 sector)"):
    Rpm = [r["R_pm"] for r in results]
    e_exact = [r["e_exact_sector_ha"] for r in results]
    e_vqe = [r["e_vqe_ha"] for r in results]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    # Ha plot
    ax1.plot(Rpm, e_exact, "k-", lw=2, label=exact_label)
    ax1.plot(Rpm, e_vqe, "ro", ms=6, label="VQE (UCCSD, Adam)")
    ax1.set_xlabel("Bond length R (pm)")
    ax1.set_ylabel("Energy (Ha)")
    ax1.set_title(title + "  [Hartree]")
    ax1.legend(); ax1.grid(alpha=0.3)
    # MJ/mol plot
    ax2.plot(Rpm, [e * HA_TO_MJMOL for e in e_exact], "k-", lw=2, label=exact_label)
    ax2.plot(Rpm, [e * HA_TO_MJMOL for e in e_vqe], "ro", ms=6, label="VQE")
    ax2.set_xlabel("Bond length R (pm)")
    ax2.set_ylabel("Energy (MJ mol$^{-1}$)")
    ax2.set_title(title + "  [MJ mol$^{-1}$]")
    ax2.legend(); ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=140)
    plt.close(fig)
    print(f"  wrote {outpath}")


def fit_equilibrium(results):
    """Quadratic fit near minimum -> R_eq, E_min."""
    Rpm = np.array([r["R_pm"] for r in results])
    Eha = np.array([r["e_vqe_ha"] for r in results])
    i_min = int(np.argmin(Eha))
    lo = max(0, i_min - 3)
    hi = min(len(Rpm), i_min + 4)
    sub_R = Rpm[lo:hi]
    sub_E = Eha[lo:hi]
    if len(sub_R) < 3:
        return None
    coefs = np.polyfit(sub_R, sub_E, 2)
    R_eq = -coefs[1] / (2 * coefs[0])
    E_min_ha = float(np.polyval(coefs, R_eq))
    return {"R_eq_pm": float(R_eq), "E_min_ha": E_min_ha,
            "E_min_mjmol": float(E_min_ha * HA_TO_MJMOL),
            "fit_window_pm": [float(sub_R.min()), float(sub_R.max())]}


def main():
    log_path = os.path.join(LOGS, "run.log")
    sys.stdout = open(log_path, "w", buffering=1)
    print("=" * 70)
    print("QC-100 W1 — VQE replication of Peruzzo et al. 2014")
    print("Started:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Constants: 1 Ha = {HA_TO_KJMOL} kJ/mol = {HA_TO_MJMOL} MJ/mol")
    print(f"           1 Å  = {ANG_TO_BOHR} Bohr")
    print("=" * 70)

    # ===== HeH+ =====
    print("\n## HeH+  (charge=+1, 2 electrons, STO-3G -> 4 qubits JW)\n")
    # Paper's reported equilibrium: R ~ 92.3 pm. Scan 50..220 pm.
    heh_R_pm = np.arange(50, 230, 10)
    heh_R_ang = heh_R_pm / 100.0
    heh_results = scan_dissociation(["He", "H"], charge=1, n_electrons=2,
                                    r_values_ang=heh_R_ang, name="HeH+",
                                    max_iter=250)
    plot_dissociation(heh_results,
                      "HeH$^+$ dissociation curve",
                      os.path.join(FIGS, "heh_dissociation.png"))
    heh_eq = fit_equilibrium(heh_results)
    print("\nHeH+ equilibrium (quadratic fit on VQE energies):")
    print(f"  R_eq    = {heh_eq['R_eq_pm']:.2f} pm   (paper: 92.3 ± 0.1 pm)")
    print(f"  E_min   = {heh_eq['E_min_ha']:.6f} Ha = {heh_eq['E_min_mjmol']:.4f} MJ/mol")
    print(f"                                              (paper: -2.865 ± 0.008 MJ/mol)")

    # Nelder-Mead cross-check at R = 0.92 Å (paper's optimizer)
    print("\n## HeH+ Nelder-Mead methods-match cross-check at R = 0.92 Å\n")
    coords_eq = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.92]])
    H_eq, n_eq = build_hamiltonian(["He", "H"], coords_eq, charge=1)
    e_exact_eq, _, _ = exact_ground_in_sector(H_eq, n_eq, 2)
    cost_eq, n_params_eq, _, _, _ = uccsd_cost_factory(H_eq, n_eq, 2)
    nm = run_vqe_neldermead(cost_eq, n_params_eq, max_iter=400, n_restarts=3,
                            seed=12345, label="HeH+ R=0.92")
    nm_err_mha = (nm["energy_ha"] - e_exact_eq) * 1000.0
    print(f"\nNelder-Mead result: {nm['energy_ha']:.8f} Ha  "
          f"err = {nm_err_mha:+.5f} mHa  "
          f"evals = {nm['n_iters']}  ({nm['wall_seconds']:.1f}s)")
    print(f"Exact at R=0.92 (N=2): {e_exact_eq:.8f} Ha")

    # ===== H2 (bonus) =====
    print("\n## H2  (neutral, 2 electrons, STO-3G -> 4 qubits JW)\n")
    h2_R_pm = np.arange(40, 220, 10)
    h2_R_ang = h2_R_pm / 100.0
    h2_results = scan_dissociation(["H", "H"], charge=0, n_electrons=2,
                                   r_values_ang=h2_R_ang, name="H2",
                                   max_iter=250)
    plot_dissociation(h2_results, "H$_2$ dissociation curve",
                      os.path.join(FIGS, "h2_dissociation.png"))
    h2_eq = fit_equilibrium(h2_results)
    print("\nH2 equilibrium (quadratic fit on VQE energies):")
    print(f"  R_eq    = {h2_eq['R_eq_pm']:.2f} pm   (literature: ~74 pm)")
    print(f"  E_min   = {h2_eq['E_min_ha']:.6f} Ha = {h2_eq['E_min_mjmol']:.4f} MJ/mol")

    # ===== Summary tables =====
    def print_table(name, results):
        print(f"\n## Summary table — {name}\n")
        print(f"{'R(pm)':>7} {'E_exact(Ha)':>14} {'E_vqe(Ha)':>14} {'err(mHa)':>10} "
              f"{'chem':>5} {'E_vqe(MJ/mol)':>15}")
        for r in results:
            print(f"{r['R_pm']:>7.1f} {r['e_exact_sector_ha']:>14.6f} "
                  f"{r['e_vqe_ha']:>14.6f} {r['err_mha']:>10.5f} "
                  f"{'OK' if r['chemical_accuracy'] else '--':>5} "
                  f"{r['e_vqe_ha']*HA_TO_MJMOL:>15.4f}")
    print_table("HeH+", heh_results)
    print_table("H2", h2_results)

    def aggregate(results):
        max_e = max(abs(r["err_mha"]) for r in results)
        mean_e = float(np.mean([abs(r["err_mha"]) for r in results]))
        frac = sum(r["chemical_accuracy"] for r in results) / len(results)
        return {"max_err_mha": max_e, "mean_err_mha": mean_e,
                "chem_acc_fraction": frac}
    heh_agg = aggregate(heh_results)
    h2_agg = aggregate(h2_results)
    print("\n## Aggregate accuracy")
    print(f"HeH+:  mean |err| = {heh_agg['mean_err_mha']:.5f} mHa,  "
          f"max |err| = {heh_agg['max_err_mha']:.5f} mHa,  "
          f"chem-acc at {heh_agg['chem_acc_fraction']*100:.0f}% of points")
    print(f"H2 :   mean |err| = {h2_agg['mean_err_mha']:.5f} mHa,  "
          f"max |err| = {h2_agg['max_err_mha']:.5f} mHa,  "
          f"chem-acc at {h2_agg['chem_acc_fraction']*100:.0f}% of points")

    out = {
        "heh_plus": heh_results,
        "heh_plus_equilibrium": heh_eq,
        "heh_plus_aggregate": heh_agg,
        "heh_plus_neldermead_at_eq": {
            "R_ang": 0.92, "energy_ha": nm["energy_ha"],
            "err_mha": nm_err_mha, "evals": nm["n_iters"],
            "wall_seconds": nm["wall_seconds"], "exact_ha": e_exact_eq,
        },
        "h2": h2_results,
        "h2_equilibrium": h2_eq,
        "h2_aggregate": h2_agg,
        "constants": {"HA_TO_MJMOL": HA_TO_MJMOL,
                      "CHEMICAL_ACCURACY_HA": CHEMICAL_ACCURACY_HA,
                      "ANG_TO_BOHR": ANG_TO_BOHR},
        "paper_targets": {
            "HeH+_R_eq_pm": 92.3, "HeH+_R_eq_pm_err": 0.1,
            "HeH+_E_min_MJmol": -2.865, "HeH+_E_min_MJmol_err": 0.008,
        },
    }
    with open(os.path.join(LOGS, "results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nWrote logs/results.json and figures/")
    print("\nFinished:", time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
