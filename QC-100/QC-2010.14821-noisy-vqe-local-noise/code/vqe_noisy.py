#!/usr/bin/env python3
"""
Independent replication of arXiv:2010.14821
"Simulating noisy variational quantum eigensolver with local noise models"
Zeng, Wu, Cao, Zhang, Hou, Xu, Zeng (2020)

Reproduce the central claim: for hardware-efficient VQE ansatz with local
depolarizing noise, the ground-state energy of a small spin Hamiltonian
degrades monotonically with the per-gate error probability p, and the
relative error (E - E0)/|E0| grows roughly linearly at small p.

We use n=4 qubits, TIsing model (J=h=1), d=2 logical layers.
Per paper Table I, TIsing at n=4 needs d=2 for the noiseless VQE to reach
E/E0 >= 98%.

Ansatz per paper Fig. 2:
- 2n qubits (here 2n=4 -> n_block=2)
- Each logical layer d:
   * Layer A: for i in [0, n_block-1]: CNOT(2i, 2i+1); Ry+Rz on qubits 2i and 2i+1
   * Layer B: for j in [0, n_block-2]: CNOT(2j+1, 2j+2); Ry+Rz on 2j+1 and 2j+2
  (2n-1)*4d parameters total.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ---------- Hamiltonian construction ----------
def tising_hamiltonian(n_qubits: int, J: float = 1.0, h: float = 1.0, pbc: bool = True) -> SparsePauliOp:
    """H = -J sum_j Z_j Z_{j+1} - h sum_j X_j.

    (Note: sign convention doesn't affect (E-E0)/|E0| for ground state.)
    Paper's TIsing eq (7): H = -J sum sigma^z sigma^z - h sum sigma^x.
    """
    paulis = []
    coeffs = []
    for j in range(n_qubits - (0 if pbc else 1)):
        s = ["I"] * n_qubits
        s[j] = "Z"
        s[(j + 1) % n_qubits] = "Z"
        paulis.append("".join(reversed(s)))  # Qiskit uses little-endian string
        coeffs.append(-J)
    for j in range(n_qubits):
        s = ["I"] * n_qubits
        s[j] = "X"
        paulis.append("".join(reversed(s)))
        coeffs.append(-h)
    if n_qubits == 2:
        # For n=2, PBC would double-count the bond; use OBC.
        return tising_hamiltonian(2, J, h, pbc=False) if pbc else SparsePauliOp(paulis, coeffs=coeffs)
    return SparsePauliOp(paulis, coeffs=coeffs)


def exact_ground_energy(H: SparsePauliOp) -> float:
    mat = H.to_matrix()
    eigs = np.linalg.eigvalsh(mat)
    return float(eigs[0])


# ---------- Ansatz per paper Fig. 2 ----------
def build_ansatz(n_qubits: int, d: int, params: np.ndarray) -> QuantumCircuit:
    """Hardware-efficient ansatz from paper Fig. 2.

    n_qubits = 2 * n_block (must be even).
    Per logical layer:
      Layer A: for i in [0..n_block-1]: CNOT(2i, 2i+1); then Ry(theta), Rz(phi) on 2i and 2i+1
      Layer B: for j in [0..n_block-2]: CNOT(2j+1, 2j+2); then Ry, Rz on 2j+1 and 2j+2
    Total single-qubit gates per layer = 2*(2*n_block + 2*(n_block-1))
                                       = 2*(4*n_block - 2)
                                       = 8*n_block - 4
                                       = 4*(2*n_block - 1)
                                       = 4*(n_qubits - 1)  -> (n_qubits-1)*4d total parameters
    """
    assert n_qubits % 2 == 0
    n_block = n_qubits // 2
    n_params_per_layer = 4 * (n_qubits - 1)
    expected = n_params_per_layer * d
    assert len(params) == expected, f"expected {expected} params, got {len(params)}"
    qc = QuantumCircuit(n_qubits)
    idx = 0
    for _layer in range(d):
        # Layer A
        for i in range(n_block):
            q0, q1 = 2 * i, 2 * i + 1
            qc.cx(q0, q1)
            qc.ry(params[idx], q0); idx += 1
            qc.rz(params[idx], q0); idx += 1
            qc.ry(params[idx], q1); idx += 1
            qc.rz(params[idx], q1); idx += 1
        # Layer B
        for j in range(n_block - 1):
            q0, q1 = 2 * j + 1, 2 * j + 2
            qc.cx(q0, q1)
            qc.ry(params[idx], q0); idx += 1
            qc.rz(params[idx], q0); idx += 1
            qc.ry(params[idx], q1); idx += 1
            qc.rz(params[idx], q1); idx += 1
    return qc


def num_params(n_qubits: int, d: int) -> int:
    return (n_qubits - 1) * 4 * d


def count_gates(n_qubits: int, d: int) -> dict:
    n_block = n_qubits // 2
    cx_per_layer = n_block + (n_block - 1)
    sq_per_layer = 2 * (2 * n_block + 2 * (n_block - 1))
    return {
        "cx_total": cx_per_layer * d,
        "single_qubit_rot_total": sq_per_layer * d,
    }


# ---------- Noise model ----------
def make_depolarizing_noise(p: float) -> NoiseModel:
    """Local depolarizing noise on single- and two-qubit gates, per-gate prob p."""
    nm = NoiseModel()
    if p > 0:
        err1 = depolarizing_error(p, 1)
        err2 = depolarizing_error(p, 2)
        # Apply to the ansatz's native gates.
        nm.add_all_qubit_quantum_error(err1, ["ry", "rz"])
        nm.add_all_qubit_quantum_error(err2, ["cx"])
    return nm


# ---------- VQE energy evaluation ----------
def energy_noiseless(H: SparsePauliOp, n_qubits: int, d: int, params: np.ndarray) -> float:
    qc = build_ansatz(n_qubits, d, params)
    sv = Statevector.from_instruction(qc)
    return float(np.real(sv.expectation_value(H)))


def energy_noisy(H: SparsePauliOp, n_qubits: int, d: int, params: np.ndarray,
                 noise_model: NoiseModel) -> float:
    """Use Aer density-matrix simulator for an exact noisy expectation value
    (no shot noise, so we isolate the noise-model effect)."""
    sim = AerSimulator(method="density_matrix", noise_model=noise_model)
    qc = build_ansatz(n_qubits, d, params)
    qc.save_density_matrix()
    tqc = qc.decompose()
    # Run
    result = sim.run(tqc).result()
    rho = result.data(0)["density_matrix"]
    rho_np = np.asarray(rho)
    Hmat = H.to_matrix()
    return float(np.real(np.trace(rho_np @ Hmat)))


# ---------- VQE optimization ----------
def run_vqe_noiseless(H: SparsePauliOp, n_qubits: int, d: int, seed: int = 0,
                      maxiter: int = 400):
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(-np.pi, np.pi, size=num_params(n_qubits, d))
    def obj(x):
        return energy_noiseless(H, n_qubits, d, x)
    res = minimize(obj, x0, method="COBYLA", options={"maxiter": maxiter, "rhobeg": 0.3})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-qubits", type=int, default=4)
    ap.add_argument("--d", type=int, default=2)
    ap.add_argument("--p-values", type=str,
                    default="0,1e-4,3e-4,1e-3,3e-3,1e-2")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-seeds", type=int, default=3,
                    help="Number of random inits to average over (paper uses 3).")
    ap.add_argument("--maxiter", type=int, default=400)
    ap.add_argument("--outdir", type=str, required=True)
    ap.add_argument("--model", type=str, default="tising")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    n = args.n_qubits
    d = args.d

    if args.model == "tising":
        H = tising_hamiltonian(n, J=1.0, h=1.0, pbc=True)
    else:
        raise SystemExit(f"unknown model {args.model}")

    E0 = exact_ground_energy(H)
    gates = count_gates(n, d)
    ntot_gates = gates["cx_total"] + gates["single_qubit_rot_total"]
    print(f"[info] model={args.model} n={n} d={d} E0={E0:.6f}")
    print(f"[info] ansatz gates: {gates} total={ntot_gates}")
    print(f"[info] params={num_params(n,d)}")

    # Step 1: run noiseless VQE with multiple seeds; keep best.
    t0 = time.time()
    seeds = list(range(args.seed, args.seed + args.n_seeds))
    best = None
    all_runs = []
    for s in seeds:
        res = run_vqe_noiseless(H, n, d, seed=s, maxiter=args.maxiter)
        E = float(res.fun)
        nit = int(getattr(res, 'nit', getattr(res, 'nfev', -1)))
        all_runs.append({"seed": s, "E_noiseless_opt": E, "nit": nit, "success": bool(res.success)})
        print(f"[noiseless] seed={s} E_opt={E:.6f} (E-E0)/|E0|={(E-E0)/abs(E0):.4e} nit={nit}")
        if best is None or E < best["E"]:
            best = {"seed": s, "E": E, "x": res.x.copy()}
    t_noiseless = time.time() - t0
    print(f"[noiseless] best seed={best['seed']} E={best['E']:.6f} ratio E/E0={best['E']/E0:.4f}")

    # Use the best noiseless params for the noisy sweep (paper effectively studies
    # noisy VQE by optimizing again per p; here we do BOTH:
    #  1. Fixed-params noisy energy sweep (isolates noise effect on the state)
    #  2. Optionally re-optimize under noise (skip for tractability)
    p_values = [float(x) for x in args.p_values.split(",")]

    sweep = []
    x_opt = best["x"]
    E_nl_check = energy_noiseless(H, n, d, x_opt)
    print(f"[check] E_noiseless(x_opt)={E_nl_check:.6f}")
    for p in p_values:
        nm = make_depolarizing_noise(p)
        t1 = time.time()
        E_p = energy_noisy(H, n, d, x_opt, nm)
        dt = time.time() - t1
        rel = (E_p - E0) / abs(E0)
        row = {"p": p, "E_noisy": E_p, "rel_err": rel, "time_s": dt}
        sweep.append(row)
        print(f"[noisy]  p={p:>9.2e}  E={E_p:+.6f}  (E-E0)/|E0|={rel:+.4e}  ({dt:.1f}s)")

    out = {
        "paper": "arXiv:2010.14821",
        "model": args.model,
        "n_qubits": n,
        "d": d,
        "E0_exact": E0,
        "ansatz_gates": gates,
        "num_params": num_params(n, d),
        "noiseless_runs": all_runs,
        "noiseless_best": {"seed": best["seed"], "E": best["E"], "ratio_E_over_E0": best["E"] / E0},
        "noisy_sweep": sweep,
        "elapsed_noiseless_s": t_noiseless,
    }
    (outdir / "results.json").write_text(json.dumps(out, indent=2))
    print(f"[write] {outdir/'results.json'}")


if __name__ == "__main__":
    main()
