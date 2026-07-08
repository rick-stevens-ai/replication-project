"""
Replication of Melo, Earnest-Noble, Tacchino (arXiv:2211.01383)
"Pulse-efficient quantum machine learning"

Scope: gate-count / CX-count / classifier accuracy proxy for the paper's
QNN experiment (paper Fig. 1a + Fig. 2). Full pulse-level control is
hardware-specific (needs a real IBM backend calibration + PE transpiler
plugin) and out of scope; the observable proxy that reflects the paper's
core mechanism is:

  - Standard (CNOT-based, full or dense entanglement) ansatz vs
  - Compact / pulse-inspired ansatz (fewer entangling gates, still
    universal enough for the task) using linear (nearest-neighbor)
    entanglement + optional gate cancellation via transpiler level=3.

We measure:
  (i)  CX count and total gate count of both circuits after transpilation
       to a common ISA (basis = [rz, sx, x, cx], as on IBM Falcon/Eagle).
  (ii) Classification accuracy of both variants on:
        - synthetic moons (paper's synthetic 2-class dataset analog)
        - iris 2-class (setosa vs versicolor, 2 features)
       trained with Qiskit's SamplerQNN + COBYLA (real classical
       optimizer on real Aer sampler simulation).

The paper's headline claim is that PE circuits are shorter (fewer 2Q
"gate equivalents" of CX) while retaining -- and even improving --
classification accuracy. We check the shorter-circuit-and-retain-accuracy
half of that claim on a classical simulator; the "even improve" half
requires hardware noise, which we do NOT reproduce here.

Endpoint: none (purely classical simulation, no LLM calls).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from sklearn.datasets import make_moons, load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit_machine_learning.optimizers import COBYLA
from qiskit_machine_learning.algorithms.classifiers import NeuralNetworkClassifier

import qiskit
import qiskit_aer
import qiskit_machine_learning
import sklearn


OUT = Path(__file__).resolve().parents[1] / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


def build_standard_ansatz(num_qubits: int, reps: int = 2) -> QuantumCircuit:
    """Standard CNOT-based ansatz with FULL entanglement (dense CX web).
    Analog of the paper's 'regular' CNOT-based transpilation baseline."""
    return RealAmplitudes(num_qubits=num_qubits, entanglement="full", reps=reps)


def build_pulse_inspired_ansatz(num_qubits: int, reps: int = 2) -> QuantumCircuit:
    """Compact / pulse-inspired ansatz: linear (nearest-neighbor) entanglement.
    Uses far fewer CX gates than the full-entanglement baseline while remaining
    a universal ansatz family for these small tasks. This is the classical
    proxy for the paper's pulse-efficient (RZX-based) transpilation, whose
    net effect is: fewer/shorter 2Q gate schedules."""
    return RealAmplitudes(num_qubits=num_qubits, entanglement="linear", reps=reps)


def make_qnn(feature_map: QuantumCircuit, ansatz: QuantumCircuit, num_qubits: int) -> SamplerQNN:
    qc = QuantumCircuit(num_qubits)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)
    qc.measure_all()
    # Decompose all high-level gates so Aer knows every instruction.
    qc = qc.decompose().decompose().decompose()

    def parity(x: int) -> int:
        return bin(x).count("1") % 2

    sampler = AerSampler()
    qnn = SamplerQNN(
        circuit=qc,
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
        interpret=parity,
        output_shape=2,
        sampler=sampler,
    )
    return qnn


def transpile_and_count(qc: QuantumCircuit, basis=("rz", "sx", "x", "cx"), opt_level: int = 3) -> dict:
    tqc = transpile(qc, basis_gates=list(basis), optimization_level=opt_level, seed_transpiler=42)
    ops = dict(tqc.count_ops())
    return {
        "depth": tqc.depth(),
        "cx": int(ops.get("cx", 0)),
        "single_qubit": int(sum(v for k, v in ops.items() if k != "cx")),
        "total": int(sum(ops.values())),
        "ops": {k: int(v) for k, v in ops.items()},
    }


def get_moons(n=120, seed=0):
    X, y = make_moons(n_samples=n, noise=0.15, random_state=seed)
    X = MinMaxScaler(feature_range=(0, np.pi)).fit_transform(X)
    return train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)


def get_iris_2class(seed=0):
    d = load_iris()
    mask = d.target < 2  # setosa (0) vs versicolor (1)
    X = d.data[mask][:, :2]  # first 2 features -> 2 qubits
    y = d.target[mask]
    X = MinMaxScaler(feature_range=(0, np.pi)).fit_transform(X)
    return train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)


def train_eval(qnn, X_tr, y_tr, X_te, y_te, maxiter=60, seed=0):
    optimizer = COBYLA(maxiter=maxiter)
    clf = NeuralNetworkClassifier(neural_network=qnn, optimizer=optimizer)
    rng = np.random.default_rng(seed)
    n_weights = qnn.num_weights
    initial = rng.uniform(-np.pi, np.pi, n_weights)
    clf.initial_point = initial
    t0 = time.time()
    clf.fit(X_tr, y_tr)
    train_time = time.time() - t0
    y_pred_tr = clf.predict(X_tr)
    y_pred_te = clf.predict(X_te)
    return {
        "train_acc": float(accuracy_score(y_tr, y_pred_tr)),
        "test_acc": float(accuracy_score(y_te, y_pred_te)),
        "train_time_s": round(train_time, 2),
    }


def run_experiment(name: str, X_tr, X_te, y_tr, y_te, num_qubits: int, reps: int, maxiter: int, seed: int):
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=1)

    print(f"\n=== {name} | qubits={num_qubits} reps={reps} maxiter={maxiter} ===")
    results = {}
    for variant, builder in [
        ("standard_full_entanglement", build_standard_ansatz),
        ("pulse_inspired_linear",       build_pulse_inspired_ansatz),
    ]:
        ansatz = builder(num_qubits, reps=reps)
        # Compose for transpile counting
        full = QuantumCircuit(num_qubits)
        full.compose(feature_map, inplace=True)
        full.compose(ansatz, inplace=True)
        counts = transpile_and_count(full)
        print(f"  {variant}: depth={counts['depth']} cx={counts['cx']} single_q={counts['single_qubit']} total={counts['total']}")

        qnn = make_qnn(feature_map, ansatz, num_qubits)
        m = train_eval(qnn, X_tr, y_tr, X_te, y_te, maxiter=maxiter, seed=seed)
        print(f"    train_acc={m['train_acc']:.3f}  test_acc={m['test_acc']:.3f}  time={m['train_time_s']}s")
        results[variant] = {"circuit": counts, "metrics": m}

    std = results["standard_full_entanglement"]
    pei = results["pulse_inspired_linear"]
    results["comparison"] = {
        "cx_reduction_frac":        round(1.0 - pei["circuit"]["cx"] / max(1, std["circuit"]["cx"]), 3),
        "depth_reduction_frac":     round(1.0 - pei["circuit"]["depth"] / max(1, std["circuit"]["depth"]), 3),
        "gate_reduction_frac":      round(1.0 - pei["circuit"]["total"] / max(1, std["circuit"]["total"]), 3),
        "test_acc_delta":           round(pei["metrics"]["test_acc"] - std["metrics"]["test_acc"], 3),
    }
    return results


def main():
    seed = 0
    np.random.seed(seed)
    print("Versions:", {
        "qiskit": qiskit.__version__,
        "qiskit_aer": qiskit_aer.__version__,
        "qiskit_machine_learning": qiskit_machine_learning.__version__,
        "sklearn": sklearn.__version__,
        "numpy": np.__version__,
    })

    all_results = {"versions": {
        "qiskit": qiskit.__version__,
        "qiskit_aer": qiskit_aer.__version__,
        "qiskit_machine_learning": qiskit_machine_learning.__version__,
        "sklearn": sklearn.__version__,
        "numpy": np.__version__,
    }, "seed": seed}

    # Experiment A: MOONS (paper's synthetic 2-class analog), 2 qubits, reps=2
    X_tr, X_te, y_tr, y_te = get_moons(n=120, seed=seed)
    all_results["moons_n2_reps2"] = run_experiment(
        "moons/n=2/reps=2", X_tr, X_te, y_tr, y_te, num_qubits=2, reps=2, maxiter=60, seed=seed
    )

    # Experiment B: MOONS at 4 qubits (feature-mapped repeat), tests scaling of CX savings
    #   Use a 4-qubit feature map by tiling the two features into 4 qubits via ZZFeatureMap
    X_tr, X_te, y_tr, y_te = get_moons(n=120, seed=seed)
    X_tr4 = np.hstack([X_tr, X_tr])
    X_te4 = np.hstack([X_te, X_te])
    all_results["moons_n4_reps2"] = run_experiment(
        "moons/n=4/reps=2", X_tr4, X_te4, y_tr, y_te, num_qubits=4, reps=2, maxiter=60, seed=seed
    )

    # Experiment C: IRIS 2-class (setosa vs versicolor, 2 features -> 2 qubits)
    X_tr, X_te, y_tr, y_te = get_iris_2class(seed=seed)
    all_results["iris_n2_reps2"] = run_experiment(
        "iris/n=2/reps=2", X_tr, X_te, y_tr, y_te, num_qubits=2, reps=2, maxiter=60, seed=seed
    )

    # Experiment D: scaling — 5 qubits (matches paper's n=2..5 QNN sweep upper bound)
    X_tr, X_te, y_tr, y_te = get_moons(n=120, seed=seed)
    X_tr5 = np.hstack([X_tr, X_tr, X_tr[:, :1]])
    X_te5 = np.hstack([X_te, X_te, X_te[:, :1]])
    all_results["moons_n5_reps2"] = run_experiment(
        "moons/n=5/reps=2", X_tr5, X_te5, y_tr, y_te, num_qubits=5, reps=2, maxiter=80, seed=seed
    )

    out_json = OUT / "results.json"
    out_json.write_text(json.dumps(all_results, indent=2))
    print(f"\nWrote {out_json}")

    # Summary table
    print("\n=== SUMMARY (paper's claim: PE fewer 2Q ops, retained/improved accuracy) ===")
    print(f"{'experiment':<20} {'std_cx':>7} {'pei_cx':>7} {'cx_red%':>8} {'std_acc':>8} {'pei_acc':>8} {'d_acc':>7}")
    for k, v in all_results.items():
        if not isinstance(v, dict) or "comparison" not in v:
            continue
        std = v["standard_full_entanglement"]
        pei = v["pulse_inspired_linear"]
        c = v["comparison"]
        print(f"{k:<20} {std['circuit']['cx']:>7} {pei['circuit']['cx']:>7} {100*c['cx_reduction_frac']:>7.1f}% "
              f"{std['metrics']['test_acc']:>8.3f} {pei['metrics']['test_acc']:>8.3f} {c['test_acc_delta']:>+7.3f}")


if __name__ == "__main__":
    main()
