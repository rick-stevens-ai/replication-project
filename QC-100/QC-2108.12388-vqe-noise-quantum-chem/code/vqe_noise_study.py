"""VQE H2 (STO-3G, 4-qubit JW) noise study — replication of the reproducible
core of Sung, Saib, Akhalwaya, Wallden 2021 (arXiv:2108.12388).

Sweeps:
  (a) Noiseless statevector baseline
  (b) Shot-noise only: N_shots in {1024, 8192, 32768}   (grouped bases)
  (c) Depolarizing gate-noise: p in {1e-4, 1e-3, 1e-2}  (density-matrix)

Design choices to keep it tractable:
  * Statevector evaluator uses Statevector (exact).
  * Shot-noise evaluator groups the 15 Pauli terms into their commuting bases
    -- for the H2 JW Hamiltonian the natural grouping is: {all Z-strings}
    (measured in the computational basis) + one XXYY-type Pauli-word group.
    We use qubit-wise commuting grouping via SparsePauliOp.group_commuting,
    then run one measurement circuit per group.
  * Depolarizing-noise evaluator uses AerSimulator(method='density_matrix')
    with `save_density_matrix` -- no shot noise, no per-Pauli circuit blowup.
    Exact <H> = Tr(rho * H).

Ansatz: hardware-efficient RY-CZ, 1 repetition depth (paper: "circuits with
CZ" family, depth=1 as in sec IV.D).

Optimizer: SPSA (paper uses SPSA).  We use maxiter smaller than 200 for
runtime; the point is trajectory + final energy vs noise strength.
"""
import json, os, time, math, sys
from pathlib import Path
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_algorithms.optimizers import SPSA

from build_h2_hamiltonian import (
    build_h2, openfermion_to_qiskit_sparsepauliop,
)

DATA_DIR = Path("../data"); DATA_DIR.mkdir(exist_ok=True, parents=True)
FIG_DIR  = Path("../figures"); FIG_DIR.mkdir(exist_ok=True, parents=True)
LOG_DIR  = Path("../logs"); LOG_DIR.mkdir(exist_ok=True, parents=True)

# unbuffered
sys.stdout.reconfigure(line_buffering=True)


# ---------- Ansatz ----------
def hardware_efficient_ry_cz(n_qubits: int, reps: int = 1):
    n_params = n_qubits * (reps + 1)
    params = ParameterVector("θ", n_params)
    qc = QuantumCircuit(n_qubits)
    p_idx = 0
    for q in range(n_qubits):
        qc.ry(params[p_idx], q); p_idx += 1
    for _ in range(reps):
        for q in range(n_qubits - 1):
            qc.cz(q, q + 1)
        for q in range(n_qubits):
            qc.ry(params[p_idx], q); p_idx += 1
    return qc, list(params)


# ---------- Exact statevector energy ----------
def energy_statevector(qc, params_vals, hamiltonian: SparsePauliOp) -> float:
    bound = qc.assign_parameters(dict(zip(qc.parameters, params_vals)))
    sv = Statevector.from_instruction(bound)
    return float(sv.expectation_value(hamiltonian).real)


# ---------- Grouped shot-noise energy ----------
def _basis_change_for_pauli(pauli_str: str, n: int) -> QuantumCircuit:
    """Rotate each qubit into the Z basis for the given Pauli string.
    pauli_str[0] = qubit n-1 (Qiskit big-endian labelling)."""
    qc = QuantumCircuit(n)
    for i, ch in enumerate(pauli_str):
        q = n - 1 - i
        if ch == 'X':
            qc.h(q)
        elif ch == 'Y':
            qc.sdg(q); qc.h(q)
    return qc


def _pauli_eigval_from_bits(pauli_str: str, bitstr: str) -> int:
    val = 1
    for i, ch in enumerate(pauli_str):
        if ch == 'I':
            continue
        if bitstr[i] == '1':
            val *= -1
    return val


def _group_key(pauli_str: str) -> str:
    """The measurement basis is determined by the non-I letter on each qubit.
    Two Pauli strings can be measured with the same circuit iff for every
    qubit they agree on the non-I letter (I is a wildcard)."""
    # Turn to a canonical basis string: replace I with wildcard, but two Paulis
    # with (X,I) and (I,X) are compatible.  For grouping keep the sequence.
    return pauli_str  # not used directly; we compute groups manually


def qubitwise_commuting_groups(H: SparsePauliOp):
    """Group Pauli terms of H by qubit-wise commuting (QWC) sets.
    Returns list of (basis_string, list_of_(pauli_str, coeff)) where
    basis_string has X/Y/Z on each qubit (I means 'any' -> we pick Z)."""
    n = H.num_qubits
    pauli_strings = [str(p) for p in H.paulis]
    coeffs = [complex(c).real for c in H.coeffs]

    groups = []  # each: (basis, list of (pstr, coef))
    for pstr, coef in zip(pauli_strings, coeffs):
        placed = False
        for g in groups:
            basis = g[0]
            ok = True
            for i in range(n):
                b, p = basis[i], pstr[i]
                if p == 'I' or b == 'I':
                    continue
                if b != p:
                    ok = False; break
            if ok:
                # merge basis: fill Is with p's non-I letters
                new_basis = ''.join(
                    (basis[i] if basis[i] != 'I' else pstr[i]) for i in range(n)
                )
                g[0] = new_basis
                g[1].append((pstr, coef))
                placed = True
                break
        if not placed:
            groups.append([pstr, [(pstr, coef)]])
    # Replace any remaining I in basis with Z (arbitrary choice)
    finalized = []
    for basis, terms in groups:
        b = ''.join('Z' if c == 'I' else c for c in basis)
        finalized.append((b, terms))
    return finalized


def energy_sampled(qc, params_vals, groups, backend, shots, n_qubits) -> float:
    """Estimate <H> via one measurement circuit per QWC group."""
    bound = qc.assign_parameters(dict(zip(qc.parameters, params_vals)))
    energy = 0.0
    # Identity contributions
    for basis, terms in groups:
        for pstr, c in terms:
            if set(pstr) == {'I'}:
                energy += c
    # Non-identity groups
    circuits = []
    circuit_meta = []  # list of (basis, terms_without_identity)
    for basis, terms in groups:
        non_id = [(p, c) for (p, c) in terms if set(p) != {'I'}]
        if not non_id:
            continue
        rot = _basis_change_for_pauli(basis, n_qubits)
        circ = bound.compose(rot)
        circ.measure_all()
        circuits.append(circ)
        circuit_meta.append((basis, non_id))
    if not circuits:
        return energy
    tqcs = transpile(circuits, backend, optimization_level=0)
    job = backend.run(tqcs, shots=shots)
    result = job.result()
    for i, (basis, non_id) in enumerate(circuit_meta):
        counts = result.get_counts(i)
        total = sum(counts.values())
        # accumulate per-term
        for pstr, c in non_id:
            exp = 0.0
            for bs, cnt in counts.items():
                bs = bs.replace(' ', '')
                exp += _pauli_eigval_from_bits(pstr, bs) * cnt
            exp /= total
            energy += c * exp
    return energy


# ---------- Density-matrix exact <H> under noise ----------
def energy_density_matrix(qc, params_vals, hamiltonian: SparsePauliOp,
                          backend: AerSimulator) -> float:
    bound = qc.assign_parameters(dict(zip(qc.parameters, params_vals)))
    tqc = transpile(bound, backend, optimization_level=0)
    tqc.save_density_matrix()
    result = backend.run(tqc, shots=1).result()
    rho = DensityMatrix(result.data(0)['density_matrix'])
    return float(rho.expectation_value(hamiltonian).real)


# ---------- SPSA loop ----------
def run_vqe(evaluator, x0, maxiter, tag):
    history = []
    def wrapped(theta):
        e = evaluator(list(theta))
        history.append(float(e))
        if len(history) % 25 == 0:
            print(f"      [{tag}] eval={len(history)} E={e:.6f}")
        return e
    spsa = SPSA(maxiter=maxiter)
    t0 = time.time()
    res = spsa.minimize(wrapped, x0)
    dt = time.time() - t0
    return {
        "tag": tag,
        "final_energy": float(res.fun),
        "final_params": [float(x) for x in res.x],
        "history": history,
        "n_evals": len(history),
        "wall_seconds": dt,
    }


# ---------- Noise model ----------
def build_depolarizing_noise(p: float) -> NoiseModel:
    nm = NoiseModel()
    err1 = depolarizing_error(p, 1)
    err2 = depolarizing_error(min(10 * p, 1.0), 2)
    nm.add_all_qubit_quantum_error(err1, ['u1', 'u2', 'u3', 'rx', 'ry', 'rz',
                                          'x', 'y', 'z', 'h', 's', 'sdg'])
    nm.add_all_qubit_quantum_error(err2, ['cx', 'cz'])
    return nm


def main():
    print("=== Building H2 Hamiltonian ===", flush=True)
    mol, qham, hf, fci = build_h2(0.735)
    H = openfermion_to_qiskit_sparsepauliop(qham, mol.n_qubits)
    exact_gs = float(np.linalg.eigvalsh(H.to_matrix())[0].real)
    print(f"HF={hf:.6f}  FCI={fci:.6f}  exact_diag={exact_gs:.6f} Ha")
    print(f"Paper reference: -1.1373 Ha")

    n_qubits = mol.n_qubits
    ansatz, params = hardware_efficient_ry_cz(n_qubits, reps=1)
    n_2q = sum(1 for i in ansatz.data if i.operation.num_qubits == 2)
    n_1q = sum(1 for i in ansatz.data if i.operation.num_qubits == 1)
    print(f"Ansatz: RY-CZ reps=1  n_params={len(params)}  depth={ansatz.depth()}")
    print(f"Gate counts: 1q={n_1q}  2q={n_2q}")

    # QWC groups
    groups = qubitwise_commuting_groups(H)
    print(f"QWC groups: {len(groups)} (was 15 unique Paulis)")
    for i, (b, t) in enumerate(groups):
        print(f"  group{i}: basis={b}  terms={len(t)}")

    SEED = 20260703
    rng = np.random.default_rng(SEED)
    x0 = rng.uniform(-math.pi, math.pi, size=len(params))

    results = {
        "meta": {
            "molecule": "H2",
            "bond_length_angstrom": 0.735,
            "basis": "sto-3g",
            "mapping": "jordan-wigner",
            "n_qubits": n_qubits,
            "hf_energy_ha": hf,
            "fci_energy_ha": fci,
            "qiskit_exact_diag_ha": exact_gs,
            "paper_reference_ha": -1.1373,
            "ansatz": "hardware-efficient RY-CZ reps=1",
            "n_params": len(params),
            "n_2q_gates": n_2q,
            "n_1q_gates": n_1q,
            "n_qwc_groups": len(groups),
            "optimizer": "SPSA",
            "seed": SEED,
            "qiskit_version": __import__('qiskit').__version__,
            "aer_version": __import__('qiskit_aer').__version__,
            "openfermion_version": __import__('openfermion').__version__,
        },
        "runs": []
    }

    # === (a) Noiseless statevector ===
    print("\n--- (a) Noiseless statevector baseline ---", flush=True)
    def eval_sv(theta):
        return energy_statevector(ansatz, theta, H)
    r = run_vqe(eval_sv, x0.copy(), maxiter=100, tag="noiseless")
    r.update({"noise_type": "noiseless", "noise_param": 0.0, "shots": None,
              "error_vs_paper": float(r["final_energy"] - (-1.1373)),
              "error_vs_fci":   float(r["final_energy"] - fci)})
    print(f"  E_VQE = {r['final_energy']:.6f}  err_vs_FCI={r['error_vs_fci']:+.2e}  wall={r['wall_seconds']:.1f}s", flush=True)
    results["runs"].append(r)

    # Save incrementally
    with open(DATA_DIR / "vqe_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # === (b) Shot-noise ===
    print("\n--- (b) Shot-noise-only sweep ---", flush=True)
    backend_clean = AerSimulator()
    for shots in [1024, 8192, 32768]:
        print(f"  Shots = {shots}", flush=True)
        def eval_shot(theta, _shots=shots):
            return energy_sampled(ansatz, theta, groups, backend_clean, _shots, n_qubits)
        r = run_vqe(eval_shot, x0.copy(), maxiter=60, tag=f"shots_{shots}")
        tail = r["history"][-15:]
        r.update({"noise_type": "shots", "noise_param": float(1.0 / math.sqrt(shots)),
                  "shots": shots, "tail_std": float(np.std(tail)),
                  "error_vs_paper": float(r["final_energy"] - (-1.1373)),
                  "error_vs_fci":   float(r["final_energy"] - fci)})
        print(f"    E_VQE={r['final_energy']:.6f}  err_vs_FCI={r['error_vs_fci']:+.2e}  tail_std={r['tail_std']:.4f}  wall={r['wall_seconds']:.1f}s", flush=True)
        results["runs"].append(r)
        with open(DATA_DIR / "vqe_results.json", "w") as f:
            json.dump(results, f, indent=2)

    # === (c) Depolarizing noise via density-matrix method ===
    print("\n--- (c) Depolarizing-noise sweep (density-matrix, exact <H>) ---", flush=True)
    for p in [1e-4, 1e-3, 1e-2]:
        print(f"  p = {p}", flush=True)
        nm = build_depolarizing_noise(p)
        backend_dm = AerSimulator(method='density_matrix', noise_model=nm)
        def eval_dm(theta, _b=backend_dm):
            return energy_density_matrix(ansatz, theta, H, _b)
        r = run_vqe(eval_dm, x0.copy(), maxiter=80, tag=f"depol_{p}")
        r.update({"noise_type": "depolarizing", "noise_param": float(p),
                  "shots": None,
                  "error_vs_paper": float(r["final_energy"] - (-1.1373)),
                  "error_vs_fci":   float(r["final_energy"] - fci)})
        print(f"    E_VQE={r['final_energy']:.6f}  err_vs_FCI={r['error_vs_fci']:+.2e}  wall={r['wall_seconds']:.1f}s", flush=True)
        results["runs"].append(r)
        with open(DATA_DIR / "vqe_results.json", "w") as f:
            json.dump(results, f, indent=2)

    print(f"\nAll runs complete. Wrote {DATA_DIR/'vqe_results.json'}", flush=True)
    return results


if __name__ == "__main__":
    main()
