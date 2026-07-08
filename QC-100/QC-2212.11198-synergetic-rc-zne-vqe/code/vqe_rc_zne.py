"""
Replication of Kurita et al. 2022 (arXiv:2212.11198):
"Synergetic quantum error mitigation by randomized compiling and zero-noise
 extrapolation for the variational quantum eigensolver"

Reproduces the core headline: on a small H2 VQE with coherent over-rotation
noise on the 2-qubit gate (plus a small depolarizing residual so ZNE folding
actually amplifies noise -- pure unitary noise on a statevector is a no-op
under U -> U U^dag U folding), RC alone or ZNE alone give limited improvement
but RC + ZNE combined reduces the energy error substantially.

Molecule: H2 in STO-3G at R=0.735 A, parity-mapped, 2 qubits.
Hamiltonian (electronic part, O'Malley et al. 2016 PRX 6, 031007 Table I).

Ansatz: DEEP hardware-efficient (many CX layers) so coherent errors accumulate
        over depth, matching the paper's "deep VQE" regime.

Noise (density-matrix Aer simulator):
  - coherent RX(eps) after every CX on both qubits (over-rotation)
  - coherent RZZ(eps/2) after every CX (small entangling coherent error)
  - small depolarizing channel p_dep=0.002 per 2q gate (Pauli-stochastic
    residual, so ZNE folding genuinely amplifies observable-level noise)

Mitigations:
  (i)   raw
  (ii)  RC only (average energy over N_rand twirled compilations)
  (iii) ZNE only (Mitiq LinearFactory scales [1,2,3], global folding)
  (iv)  RC + ZNE (ZNE where the per-scale executor is the RC-averaged energy)

Real Mitiq + Qiskit Aer simulation. No fabricated numbers.
"""

import json
import math
import os
import random
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import DensityMatrix, SparsePauliOp, Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne
from mitiq.zne.scaling import fold_global

# ---------------------------------------------------------------------------
# H2 / STO-3G at R=0.735 A, 2-qubit tapered Hamiltonian
# (O'Malley et al. 2016 PRX 6 031007 Table I).
# ---------------------------------------------------------------------------
NUC_REPULSION = 0.7137539  # Ha at R = 0.735 A
H2_HAM = SparsePauliOp.from_list(
    [
        ("II", -1.052373245772859),
        ("IZ", 0.39793742484318045),
        ("ZI", -0.39793742484318045),
        ("ZZ", -0.01128010425623538),
        ("XX", 0.18093119978423156),
    ]
)


def exact_ground_state_energy(hamiltonian: SparsePauliOp) -> float:
    return float(np.min(np.linalg.eigvalsh(hamiltonian.to_matrix())))


# ---------------------------------------------------------------------------
# Deep hardware-efficient ansatz. Each "rep" adds 2 params + 1 CX.
# Base block (3 params, 1 CX) is exactly expressive enough for H2 GS.
# ---------------------------------------------------------------------------
def ansatz_num_params(reps: int) -> int:
    return 3 + 2 * (reps - 1)


def build_ansatz(params, reps: int = 1) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.ry(params[0], 0)
    qc.ry(params[1], 1)
    qc.cx(0, 1)
    qc.ry(params[2], 1)
    p_idx = 3
    for _ in range(reps - 1):
        qc.ry(params[p_idx], 0)
        qc.ry(params[p_idx + 1], 1)
        qc.cx(0, 1)
        p_idx += 2
    return qc


# ---------------------------------------------------------------------------
# Coherent noise: appended into the circuit itself (unitary RX + RZZ after
# every CX). Combined with a depolarizing Aer NoiseModel on CX, this gives
# the paper's noise flavor: dominant coherent + small stochastic residual.
# ---------------------------------------------------------------------------
def inject_coherent_noise(circuit: QuantumCircuit, eps: float) -> QuantumCircuit:
    noisy = QuantumCircuit(circuit.num_qubits)
    for instr in circuit.data:
        op = instr.operation
        qargs = [circuit.find_bit(q).index for q in instr.qubits]
        noisy.append(op, qargs)
        if op.name == "cx":
            c, t = qargs
            noisy.rx(eps, c)
            noisy.rx(eps, t)
            noisy.rzz(eps / 2.0, c, t)
    return noisy


# ---------------------------------------------------------------------------
# Aer density-matrix simulator with a small depolarizing NoiseModel on CX.
# ZNE folding of the circuit will then correctly amplify observable-level
# noise: each folded copy applies the depolarizing channel one more time.
# ---------------------------------------------------------------------------
_SIM = AerSimulator(method="density_matrix")


def build_noise_model(p_dep: float = 0.002) -> NoiseModel:
    nm = NoiseModel()
    # 2q depolarizing after every CX
    err = depolarizing_error(p_dep, 2)
    nm.add_all_qubit_quantum_error(err, ["cx"])
    return nm


def expval_density(circuit: QuantumCircuit, hamiltonian: SparsePauliOp,
                   noise_model: NoiseModel) -> float:
    """Simulate on Aer density-matrix backend, return <H>."""
    qc = circuit.copy()
    qc.save_density_matrix()
    # Skip Qiskit-side transpile; Aer natively handles ry/rx/rzz/cx.
    result = _SIM.run(qc, noise_model=noise_model, shots=1).result()
    rho = result.data(0)["density_matrix"]
    rho_arr = rho.data if hasattr(rho, "data") else np.asarray(rho)
    H = hamiltonian.to_matrix()
    return float(np.real(np.trace(rho_arr @ H)))


# ---------------------------------------------------------------------------
# Randomized compiling (Pauli twirl of CX). We twirl the CX and its
# immediately following coherent-noise sandwich, then let Aer add the
# depolarizing part on top (which is already Pauli-stochastic, twirl-invariant).
# ---------------------------------------------------------------------------
CX_TWIRL_TABLE = {
    ("I", "I"): ("I", "I"), ("I", "X"): ("I", "X"),
    ("I", "Y"): ("Z", "Y"), ("I", "Z"): ("Z", "Z"),
    ("X", "I"): ("X", "X"), ("X", "X"): ("X", "I"),
    ("X", "Y"): ("Y", "Z"), ("X", "Z"): ("Y", "Y"),
    ("Y", "I"): ("Y", "X"), ("Y", "X"): ("Y", "I"),
    ("Y", "Y"): ("X", "Z"), ("Y", "Z"): ("X", "Y"),
    ("Z", "I"): ("Z", "I"), ("Z", "X"): ("Z", "X"),
    ("Z", "Y"): ("I", "Y"), ("Z", "Z"): ("I", "Z"),
}
PAULIS = ["I", "X", "Y", "Z"]


def _apply_pauli(qc: QuantumCircuit, p: str, q: int):
    if p == "I":
        return
    getattr(qc, p.lower())(q)


def randomized_compile(circuit: QuantumCircuit, rng: random.Random) -> QuantumCircuit:
    """Twirl every CX + its trailing coherent-noise block with random Paulis."""
    twirled = QuantumCircuit(circuit.num_qubits)
    data = list(circuit.data)
    i = 0
    while i < len(data):
        instr = data[i]
        op = instr.operation
        qargs = [circuit.find_bit(q).index for q in instr.qubits]
        if op.name == "cx":
            c, t = qargs
            pc, pt = rng.choice(PAULIS), rng.choice(PAULIS)
            pc_after, pt_after = CX_TWIRL_TABLE[(pc, pt)]
            _apply_pauli(twirled, pc, c)
            _apply_pauli(twirled, pt, t)
            twirled.cx(c, t)
            # Copy the coherent-noise block that immediately follows this CX
            j = i + 1
            while j < len(data):
                nq = [circuit.find_bit(q).index for q in data[j].qubits]
                nname = data[j].operation.name
                if nname in ("rx", "rzz") and set(nq).issubset({c, t}):
                    twirled.append(data[j].operation, nq)
                    j += 1
                else:
                    break
            _apply_pauli(twirled, pc_after, c)
            _apply_pauli(twirled, pt_after, t)
            i = j
        else:
            twirled.append(op, qargs)
            i += 1
    return twirled


# ---------------------------------------------------------------------------
# Executors
# ---------------------------------------------------------------------------
def make_raw_executor(hamiltonian, noise_model, eps: float):
    """Executor for ZNE-on-ansatz path: input is a (possibly folded) CLEAN
    ansatz (no injected noise). We inject coherent noise here so that folding
    the clean ansatz first, then injecting noise, correctly amplifies the
    physical noise (each folded CX carries its own noise block).
    """

    def executor(clean_ansatz):
        noisy = inject_coherent_noise(clean_ansatz, eps)
        return expval_density(noisy, hamiltonian, noise_model)

    return executor


def make_rc_executor(hamiltonian, noise_model, eps: float, n_rand, seed):
    """Executor for RC (or RC+ZNE) on ansatz. Takes a clean ansatz, injects
    coherent noise, then Pauli-twirls each CX+noise block, averaged over
    n_rand random compilations.
    """
    rng = random.Random(seed)

    def executor(clean_ansatz):
        noisy = inject_coherent_noise(clean_ansatz, eps)
        vals = []
        for _ in range(n_rand):
            tw = randomized_compile(noisy, rng)
            vals.append(expval_density(tw, hamiltonian, noise_model))
        return float(np.mean(vals))

    return executor


# ---------------------------------------------------------------------------
# Four-method comparison at fixed theta.
# ---------------------------------------------------------------------------
def evaluate_four_methods(theta, hamiltonian, eps, reps, p_dep,
                          n_rand=20, seed=0):
    ansatz = build_ansatz(theta, reps=reps)
    # Noiseless reference (statevector)
    sv = Statevector.from_instruction(ansatz).data
    H = hamiltonian.to_matrix()
    e_noiseless = float(np.real(np.conj(sv) @ H @ sv))

    nm = build_noise_model(p_dep=p_dep)

    # Executors operate on the CLEAN ansatz; they inject noise internally.
    raw_exec = make_raw_executor(hamiltonian, nm, eps=eps)
    rc_exec = make_rc_executor(hamiltonian, nm, eps=eps, n_rand=n_rand, seed=seed)

    # (i) raw noisy = executor at scale 1 (no folding)
    e_raw = raw_exec(ansatz)
    # (ii) RC only = RC executor at scale 1
    e_rc = rc_exec(ansatz)

    # ZNE: fold the CLEAN ansatz to scale factors [1,2,3], then executor injects
    # noise per-CX so folded circuits genuinely have more noise.
    factory_z = zne.inference.LinearFactory(scale_factors=[1.0, 2.0, 3.0])
    factory_rz = zne.inference.LinearFactory(scale_factors=[1.0, 2.0, 3.0])
    e_zne = zne.execute_with_zne(
        ansatz, raw_exec, factory=factory_z, scale_noise=fold_global,
    )
    e_rc_zne = zne.execute_with_zne(
        ansatz, rc_exec, factory=factory_rz, scale_noise=fold_global,
    )

    return {
        "noiseless": e_noiseless,
        "raw": e_raw,
        "rc": e_rc,
        "zne": e_zne,
        "rc_zne": e_rc_zne,
    }


# ---------------------------------------------------------------------------
# Noiseless VQE (find theta* via Nelder-Mead multi-start).
# ---------------------------------------------------------------------------
from scipy.optimize import minimize


def vqe_noiseless(hamiltonian, reps, n_restarts=8, seed=1):
    rng = np.random.default_rng(seed)
    best = (None, np.inf)
    for _ in range(n_restarts):
        x0 = rng.uniform(-np.pi, np.pi, size=ansatz_num_params(reps))
        res = minimize(
            lambda t: float(np.real(
                np.conj(Statevector.from_instruction(build_ansatz(t, reps=reps)).data)
                @ hamiltonian.to_matrix()
                @ Statevector.from_instruction(build_ansatz(t, reps=reps)).data
            )),
            x0=x0,
            method="Nelder-Mead",
            options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 5000},
        )
        if res.fun < best[1]:
            best = (res.x, res.fun)
    return best


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    out_dir = Path(__file__).resolve().parent.parent
    ev_dir = out_dir / "report" / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)

    fci_electronic = exact_ground_state_energy(H2_HAM)
    fci_total = fci_electronic + NUC_REPULSION
    print(f"[FCI] electronic = {fci_electronic:.8f}  total = {fci_total:.8f} Ha")

    REPS = 6                       # deep -> 6 CX gates
    P_DEP = 0.002                  # small stochastic residual
    N_RAND = 30                    # RC randomizations
    theta_opt, e_noiseless_opt = vqe_noiseless(H2_HAM, reps=REPS,
                                               n_restarts=20, seed=42)
    print(f"[VQE noiseless] reps={REPS} theta* found; E* = {e_noiseless_opt:.8f}")
    assert abs(e_noiseless_opt - fci_electronic) < 1e-3

    eps_list = [0.02, 0.05, 0.08, 0.10]
    all_results = []
    t0 = time.time()
    for eps in eps_list:
        print(f"\n=== eps = {eps} rad ({math.degrees(eps):.2f} deg), "
              f"p_dep={P_DEP} ===")
        res = evaluate_four_methods(theta_opt, H2_HAM, eps=eps, reps=REPS,
                                    p_dep=P_DEP, n_rand=N_RAND, seed=7)
        row = {"eps_rad": eps, "eps_deg": math.degrees(eps)}
        for k, v in res.items():
            row[k + "_Ha"] = v
            if k != "noiseless":
                row[k + "_err_mHa"] = (v - res["noiseless"]) * 1000.0
        for k in ("noiseless", "raw", "rc", "zne", "rc_zne"):
            print(f"  {k:10s} E = {res[k]:+.6f} Ha  "
                  f"err = {(res[k]-res['noiseless'])*1000:+.3f} mHa")
        all_results.append(row)
    elapsed = time.time() - t0
    print(f"\nElapsed: {elapsed:.1f} s")

    # Summary
    summary = {
        "paper": "arXiv:2212.11198 (Kurita et al. 2022)",
        "molecule": "H2 / STO-3G at R=0.735 A, 2-qubit tapered",
        "hamiltonian_terms": [
            (str(p), float(c))
            for p, c in zip(H2_HAM.paulis.to_labels(), H2_HAM.coeffs.real)
        ],
        "nuclear_repulsion_Ha": NUC_REPULSION,
        "fci_electronic_Ha": fci_electronic,
        "fci_total_Ha": fci_total,
        "vqe_noiseless_theta": [float(x) for x in theta_opt],
        "vqe_noiseless_energy_Ha": e_noiseless_opt,
        "ansatz": f"Deep HEA reps={REPS}: (Ry Ry CX) x reps  "
                  f"({REPS} CX gates, {ansatz_num_params(REPS)} params)",
        "reps": REPS,
        "noise_model": (f"coherent RX(eps) on both qubits after every CX + "
                        f"RZZ(eps/2), plus 2q depolarizing p_dep={P_DEP} via "
                        f"Aer NoiseModel; density-matrix backend."),
        "n_rand": N_RAND,
        "p_dep": P_DEP,
        "zne_scale_factors": [1.0, 2.0, 3.0],
        "zne_extrapolation": "linear (Mitiq LinearFactory, fold_global)",
        "eps_sweep_Ha": all_results,
        "elapsed_s": elapsed,
        "versions": {
            "qiskit": __import__("qiskit").__version__,
            "qiskit_aer": __import__("qiskit_aer").__version__,
            "mitiq": __import__("mitiq").__version__,
            "python": os.sys.version.split()[0],
        },
    }
    with open(ev_dir / "results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[wrote] {ev_dir/'results.json'}")

    lines = ["eps_rad,eps_deg,method,E_Ha,error_mHa,|error|_mHa"]
    for row in all_results:
        for m in ("raw", "rc", "zne", "rc_zne"):
            lines.append(
                f"{row['eps_rad']},{row['eps_deg']:.2f},{m},"
                f"{row[m+'_Ha']:.6f},{row[m+'_err_mHa']:+.4f},"
                f"{abs(row[m+'_err_mHa']):.4f}"
            )
    (ev_dir / "results_table.csv").write_text("\n".join(lines) + "\n")
    print(f"[wrote] {ev_dir/'results_table.csv'}")
    return summary


if __name__ == "__main__":
    main()
