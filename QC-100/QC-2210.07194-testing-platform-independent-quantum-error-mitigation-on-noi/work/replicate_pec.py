#!/usr/bin/env python3
"""
Second mitigation method: Probabilistic Error Cancellation (PEC).

Paper Sec II.B.2: PEC assumes an ideal noise model of local depolarizing noise
after each 2-qubit gate (Eq. 10), constructs a quasi-probability decomposition,
samples k_PEC = 100 circuits with N/k_PEC = 100 shots each, and averages.

We reproduce this on 3-qubit RB circuits at d=1 (where mitigation is expected
to help most) under matched simulator noise. Paper Fig. 3 reports PEC mu ~1..2
on the 1% depolarizing simulator.
"""
import json, math, time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import random_clifford
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import pec
from mitiq.pec import execute_with_pec
from mitiq.pec.representations import (
    represent_operations_in_circuit_with_local_depolarizing_noise,
)
from mitiq.interface.mitiq_qiskit.conversions import from_qiskit

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

DEPOL_P = 0.01           # 1% two-qubit depolarizing (paper canonical)
N_QUBITS = 3
DEPTHS = [1, 3]          # PEC is expensive; only smallest depths
N_CIRCUITS = 4
N_TRIALS = 2             # PEC has internal averaging via k_PEC sampling
K_PEC = 100              # paper: k_PEC = 100 (num sampled circuits)
N_SHOTS_TOTAL = 10_000
SHOTS_PER_PEC = N_SHOTS_TOTAL // K_PEC
SEED = 20260704


def build_rb(n, d, rng):
    layers, prod = [], None
    for _ in range(d):
        cl = random_clifford(n, seed=int(rng.integers(0, 2**31 - 1)))
        layers.append(cl); prod = cl if prod is None else cl.compose(prod)
    inv = prod.adjoint()
    qc = QuantumCircuit(n)
    for cl in layers:
        qc.compose(cl.to_circuit(), inplace=True)
    qc.compose(inv.to_circuit(), inplace=True)
    return qc


def make_noise_model(p_2q):
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p_2q, 2), ["cx", "cz", "swap", "ecr"])
    return nm


def make_executor(shots, noise_model, n):
    sim = AerSimulator(noise_model=noise_model)
    target = "0" * n
    def executor(circuit) -> float:      # runtime annotation matters for mitiq
        # circuit will be a cirq.Circuit here because mitiq converts internally
        # We convert back to qiskit before running on Aer.
        try:
            import cirq
            if isinstance(circuit, cirq.Circuit):
                from mitiq.interface.mitiq_qiskit.conversions import to_qiskit
                circuit = to_qiskit(circuit)
        except Exception:
            pass
        qc = circuit.copy()
        qc.measure_all()
        tqc = transpile(qc, sim, optimization_level=0)
        counts = sim.run(tqc, shots=shots).result().get_counts()
        total = sum(counts.values())
        p0 = sum(c for bs, c in counts.items() if bs.replace(" ", "") == target)
        # Return expectation of Z-like observable that reduces to <A>=P(0..0)
        # (mitiq PEC linear-combines these expectation values with quasi-probability weights)
        return float(p0 / total)
    return executor


def run():
    rng = np.random.default_rng(SEED)
    noise = make_noise_model(DEPOL_P)
    exe_unmit = make_executor(N_SHOTS_TOTAL, noise, N_QUBITS)
    exe_pec   = make_executor(SHOTS_PER_PEC, noise, N_QUBITS)
    ideal = 1.0

    results = {
        "config": {
            "n_qubits": N_QUBITS, "depths": DEPTHS, "n_circuits": N_CIRCUITS,
            "n_trials": N_TRIALS, "k_pec": K_PEC, "shots_total": N_SHOTS_TOTAL,
            "shots_per_pec_circuit": SHOTS_PER_PEC,
            "depol_p_2q": DEPOL_P, "seed": SEED,
        },
        "per_depth": [],
    }
    print(f"# PEC replication, n={N_QUBITS}, p_2q={DEPOL_P}, k_PEC={K_PEC}")
    print(f"{'d':>2} {'A0_mean':>8} {'APEC_mean':>10} "
          f"{'RMSE_0':>8} {'RMSE_PEC':>9} {'mu_PEC':>7}")

    for d in DEPTHS:
        circuits = [build_rb(N_QUBITS, d, rng) for _ in range(N_CIRCUITS)]
        # Build PEC representations for each circuit (based on CX + local depol)
        # For simplicity: for each circuit, build representations of only the 2q gates
        A0_vals, APEC_vals = [], []
        for t in range(N_TRIALS):
            for circ in circuits:
                a0 = exe_unmit(circ)
                # Convert to cirq for mitiq PEC
                cirq_circ = from_qiskit(circ)
                # 2Q depolarizing noise level for representation matches sim noise
                reps = represent_operations_in_circuit_with_local_depolarizing_noise(
                    cirq_circ, noise_level=DEPOL_P,
                )
                try:
                    aPEC = execute_with_pec(
                        circuit=cirq_circ,
                        executor=exe_pec,
                        representations=reps,
                        num_samples=K_PEC,
                        force_run_all=True,
                        random_state=int(rng.integers(0, 2**31-1)),
                    )
                except Exception as e:
                    print(f"  PEC failed on d={d}: {type(e).__name__}: {e}")
                    aPEC = float("nan")
                A0_vals.append(a0); APEC_vals.append(aPEC)

        # Filter NaNs for stats
        pec_ok = [v for v in APEC_vals if not (isinstance(v, float) and math.isnan(v))]
        if not pec_ok:
            print(f"{d:>2}  (all PEC runs failed)")
            continue
        rmse0 = math.sqrt(np.mean([(a-ideal)**2 for a in A0_vals]))
        rmseP = math.sqrt(np.mean([(a-ideal)**2 for a in pec_ok]))
        sq0 = sum((a-ideal)**2 for a in A0_vals)
        sqP = sum((a-ideal)**2 for a in pec_ok)
        # Shot normalization: PEC uses N total shots too
        muP = (math.sqrt(N_SHOTS_TOTAL*sq0) /
               math.sqrt(N_SHOTS_TOTAL*sqP)) if sqP > 0 else float("inf")
        print(f"{d:>2} {np.mean(A0_vals):>8.4f} {np.mean(pec_ok):>10.4f} "
              f"{rmse0:>8.4f} {rmseP:>9.4f} {muP:>7.3f}")
        results["per_depth"].append({
            "d": d, "A0_mean": float(np.mean(A0_vals)),
            "APEC_mean": float(np.mean(pec_ok)),
            "RMSE_unmit": rmse0, "RMSE_PEC": rmseP,
            "mu_PEC": muP,
            "n_pec_ok": len(pec_ok), "n_pec_attempted": len(APEC_vals),
        })

    out = OUT / "pec_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"\nWall time: {time.time()-t0:.1f}s")
