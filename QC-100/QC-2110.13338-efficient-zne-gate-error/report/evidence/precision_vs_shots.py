#!/usr/bin/env python3
"""
Reproduce the paper's precision-vs-measurement trade-off (Eq 10/11):
- fiim-like: 3 scale factors, global folding (fewer measurements per fixed budget).
- riim-like / efficient: 2 scale factors, less folding (more measurements per fixed budget
  at same wall-clock, but per Eq 10 more measurements REQUIRED to match fiim precision).

Here we hold total shots per point equal across variants and measure the empirical
std-dev of the extrapolated value from N independent trials for a fixed circuit
(nc=10). This is a direct check of the "efficient variant achieves similar accuracy
at reduced sampling cost" claim.
"""
import json
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error

from mitiq import zne
from mitiq.zne.scaling import fold_global, fold_gates_at_random
from mitiq.zne.inference import LinearFactory, RichardsonFactory

HERE = Path(__file__).parent
OUT = HERE / "precision_vs_shots.json"

EPSILON = 0.01
T1_NS = 50_000.0
TCNOT_NS = 200.0
NC = 10           # fixed circuit depth
N_TRIALS = 30     # trials per shot budget
SHOT_BUDGETS = [4096, 8192, 16384]
SEED = 20260703

rng = np.random.default_rng(SEED)


def build_noise_model():
    nm = NoiseModel()
    depo = depolarizing_error(EPSILON, 2)
    ad_1q = thermal_relaxation_error(t1=T1_NS, t2=T1_NS, time=TCNOT_NS, excited_state_population=0.0)
    ad_2q = ad_1q.expand(ad_1q)
    nm.add_all_qubit_quantum_error(depo.compose(ad_2q), ["cx"])
    return nm


NM = build_noise_model()


def make_circuit(nc):
    qc = QuantumCircuit(2)
    qc.x(0); qc.x(1)
    for _ in range(nc):
        qc.cx(0, 1)
    return qc


def make_backend(seed):
    return AerSimulator(noise_model=NM, seed_simulator=int(seed))


def executor(circuit, shots, seed):
    backend = make_backend(seed)
    qc = circuit.copy()
    qc.measure_all()
    tqc = transpile(qc, backend, optimization_level=0)
    r = backend.run(tqc, shots=shots).result()
    return r.get_counts().get("11", 0) / shots


def one_trial(circuit, method, shots, seed):
    """method in {'raw', 'full', 'eff'}"""
    def exe(c):
        # Each subcircuit gets its own seed so trials are independent
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        return executor(c, shots, seed)

    if method == "raw":
        return exe(circuit)
    if method == "full":
        fac = RichardsonFactory(scale_factors=[1.0, 2.0, 3.0])
        return float(zne.execute_with_zne(circuit, executor=exe, factory=fac, scale_noise=fold_global))
    if method == "eff":
        fac = LinearFactory(scale_factors=[1.0, 3.0])
        return float(zne.execute_with_zne(circuit, executor=exe, factory=fac, scale_noise=fold_gates_at_random))
    raise ValueError(method)


def main():
    circuit = make_circuit(NC)

    results = {}
    for shots in SHOT_BUDGETS:
        results[shots] = {}
        for method in ("raw", "full", "eff"):
            vals = []
            t0 = time.perf_counter()
            for k in range(N_TRIALS):
                seed = SEED + 10_000 * shots + k
                vals.append(one_trial(circuit, method, shots, seed))
            dt = time.perf_counter() - t0
            arr = np.array(vals)
            results[shots][method] = dict(
                mean=float(arr.mean()),
                std=float(arr.std(ddof=1)),
                bias_vs_truth=float(arr.mean() - 1.0),
                mae_vs_truth=float(np.mean(np.abs(arr - 1.0))),
                n_trials=N_TRIALS,
                total_wall_s=dt,
            )
            print(f"shots={shots:5d}  method={method:4s}  mean={arr.mean():.4f}  std={arr.std(ddof=1):.4f}  "
                  f"mae_vs_1.0={np.mean(np.abs(arr-1.0)):.4f}  ({dt:.1f}s)")

    out = dict(
        paper="arXiv:2110.13338",
        circuit_cnots=NC,
        epsilon=EPSILON,
        t1_ns=T1_NS,
        tcnot_ns=TCNOT_NS,
        n_trials=N_TRIALS,
        shot_budgets=SHOT_BUDGETS,
        results=results,
        # Key comparison: at equal shots/circuit, does the efficient variant match full?
        # We compare bias (systematic accuracy) and std (statistical precision).
    )
    OUT.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
