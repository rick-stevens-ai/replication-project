"""
Independent replication core of arXiv:2107.13470
"Unifying and benchmarking state-of-the-art quantum error mitigation techniques"
(Bultrini, Gordon, Czarnik, Arrasmith, Cerezo, Coles, Cincio; Quantum 2023).

The paper's headline: for a local observable produced by a noisy quantum circuit
(random quantum circuit / QAOA), multiple data-driven QEM techniques (ZNE, CDR,
VD) all reduce absolute error vs the raw noisy expectation value, with different
techniques winning at different shot budgets.

Reproducible core (Mitiq + Qiskit Aer):
  circuit  : small random Clifford+non-Clifford Qiskit circuit on N=4 qubits
  observable: <Z_0>
  noise    : depolarizing noise on 1- and 2-qubit gates via Qiskit Aer NoiseModel
  methods  :
    (a) raw noisy
    (b) Zero-Noise Extrapolation (ZNE)   -- mitiq.zne
    (c) Probabilistic Error Cancellation (PEC) -- mitiq.pec
    (d) Clifford Data Regression (CDR)   -- mitiq.cdr

  headline check: does each mitigated estimator beat |noisy - exact|?

Real simulation only. No fabrication.
"""

import json, os, sys, time, math, random
from pathlib import Path

import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne, cdr, pec
from mitiq.pec.representations.depolarizing import (
    represent_operations_in_circuit_with_local_depolarizing_noise,
)

REPORT_DIR = Path(__file__).resolve().parent.parent / "report"
EVID_DIR = REPORT_DIR / "evidence"
EVID_DIR.mkdir(parents=True, exist_ok=True)

RNG_SEED = 20260703
np.random.seed(RNG_SEED)
random.seed(RNG_SEED)

# ----------------------------------------------------------------------
# 1. Small circuit + observable
# ----------------------------------------------------------------------
NQ = 2  # keep low so exact statevector + PEC are cheap
DEPTH = 3

def build_circuit(nq: int = NQ, depth: int = DEPTH, seed: int = 0) -> QuantumCircuit:
    """Small circuit with real rotations so ideal <Z_0> is non-trivial
    (well away from 0, +1, -1). Gates used are {rx, ry, cx} which mitiq's
    depolarizing PEC representation function supports.
    """
    rng = random.Random(seed)
    qc = QuantumCircuit(nq)
    for layer in range(depth):
        for q in range(nq):
            theta = rng.uniform(0.2, 1.2)
            g = rng.choice(["rx", "ry"])
            getattr(qc, g)(theta, q)
        for q in range(nq - 1):
            qc.cx(q, q + 1)
    # Final rotation layer on qubit 0 to bias <Z_0>
    qc.ry(0.4, 0)
    return qc


def exact_expval_Z0(qc: QuantumCircuit) -> float:
    """Exact noiseless <Z_0> from the statevector."""
    sv = Statevector.from_instruction(qc)
    # Z on qubit 0, identity on the rest. Qiskit qubit-0 == rightmost in string.
    op = Operator.from_label("I" * (qc.num_qubits - 1) + "Z")
    return float(np.real(sv.expectation_value(op)))


# ----------------------------------------------------------------------
# 2. Noise model + executor
# ----------------------------------------------------------------------
P1 = 0.005   # 1-qubit depolarizing rate
P2 = 0.02    # 2-qubit depolarizing rate

def make_noise_model(p1: float = P1, p2: float = P2) -> NoiseModel:
    nm = NoiseModel()
    e1 = depolarizing_error(p1, 1)
    e2 = depolarizing_error(p2, 2)
    nm.add_all_qubit_quantum_error(e1, ["h", "x", "y", "z", "s", "sdg", "sx", "rx", "ry", "rz"])
    nm.add_all_qubit_quantum_error(e2, ["cx", "cz", "iswap"])
    return nm

BACKEND = AerSimulator(noise_model=make_noise_model())
BACKEND_IDEAL = AerSimulator()  # for CDR training-set "exact" measurement helper

SHOTS = 20000  # per circuit execution


def _to_qiskit(qc):
    """Ensure we hand Qiskit Aer a QuantumCircuit. Mitiq may pass cirq.Circuit
    or qiskit.QuantumCircuit to executors depending on the mitigator; convert."""
    import cirq
    if isinstance(qc, cirq.Circuit):
        from mitiq.interface.conversions import convert_from_mitiq
        qc = convert_from_mitiq(qc, "qiskit")
    return qc


def _run_and_expval(qc: QuantumCircuit, backend: AerSimulator, shots: int = SHOTS) -> float:
    qc = qc.copy()
    # Only add measure_all if there are no measure ops already
    has_meas = any(inst.operation.name == "measure" for inst in qc.data)
    if not has_meas:
        qc.measure_all()
    tqc = transpile(qc, backend, optimization_level=0)
    result = backend.run(tqc, shots=shots, seed_simulator=RNG_SEED).result()
    counts = result.get_counts()
    total = sum(counts.values())
    val = 0.0
    for bs, c in counts.items():
        bit0 = bs.replace(" ", "")[-1]  # last char = qubit 0
        val += (1 if bit0 == "0" else -1) * c
    return val / total


def executor_noisy(circuit) -> float:
    """Return noisy <Z_0> for the given circuit using Qiskit Aer + depolarizing noise."""
    qc = _to_qiskit(circuit)
    return _run_and_expval(qc, BACKEND)


def executor_ideal(circuit) -> float:
    """Return NOISELESS <Z_0> — used by CDR as its 'simulator' oracle for the
    near-Clifford training circuits (which are efficiently classically simulable,
    exactly as CDR requires in the paper)."""
    qc = _to_qiskit(circuit)
    return _run_and_expval(qc, BACKEND_IDEAL)


# ----------------------------------------------------------------------
# 3. Run all four methods
# ----------------------------------------------------------------------
def main():
    t0 = time.time()

    qc = build_circuit(seed=2)  # seed 2 gives ideal <Z_0> ~ -0.53
    exact = exact_expval_Z0(qc)
    print(f"[circuit] {NQ} qubits, depth {DEPTH}, {qc.size()} gates")
    print(f"[exact ] <Z_0> = {exact:+.6f}")

    # Convert to mitiq-native (cirq.Circuit) once for the mitigators. Mitiq
    # accepts qiskit circuits directly, so we can also just pass qc.
    circuit_for_mitiq = qc

    # (a) raw noisy
    raw = executor_noisy(qc)
    print(f"[raw   ] <Z_0> = {raw:+.6f}   |err| = {abs(raw-exact):.4f}")

    # (b) ZNE — Richardson extrapolation, folding scale factors [1, 2, 3]
    from mitiq.zne.scaling.folding import fold_gates_at_random
    from mitiq.zne.inference import RichardsonFactory
    from mitiq import Executor
    fac = RichardsonFactory(scale_factors=[1.0, 2.0, 3.0])
    # Wrap in explicit Executor so return type is unambiguous for mitiq 1.0
    exec_noisy = Executor(executor_noisy, max_batch_size=1)
    zne_val = zne.execute_with_zne(
        circuit_for_mitiq,
        exec_noisy,
        factory=fac,
        scale_noise=fold_gates_at_random,
    )
    zne_val = float(zne_val)
    print(f"[ZNE   ] <Z_0> = {zne_val:+.6f}   |err| = {abs(zne_val-exact):.4f}")

    # (c) PEC — local depolarizing representations
    from mitiq import Executor
    from cirq import Circuit as CirqCircuit
    from mitiq.interface.conversions import convert_to_mitiq
    mitiq_circ, _in_type = convert_to_mitiq(qc)
    reps = represent_operations_in_circuit_with_local_depolarizing_noise(
        mitiq_circ, noise_level=P2  # dominant 2-qubit rate — mitiq's built-in
    )
    pec_val = pec.execute_with_pec(
        mitiq_circ,
        executor_noisy,
        representations=reps,
        num_samples=200,
        random_state=RNG_SEED,
    )
    # newer mitiq returns tuple (val, data); older returns float
    if isinstance(pec_val, tuple):
        pec_val = pec_val[0]
    pec_val = float(pec_val)
    print(f"[PEC   ] <Z_0> = {pec_val:+.6f}   |err| = {abs(pec_val-exact):.4f}")

    # (d) CDR — Clifford Data Regression
    # Since our circuit is already all-Clifford, mitiq's Clifford-substitution
    # training set is trivial but still exercises the real code path (near-Clifford
    # training circuits are simulated 'ideally' via executor_ideal).
    cdr_val = cdr.execute_with_cdr(
        circuit_for_mitiq,
        exec_noisy,
        simulator=executor_ideal,
        num_training_circuits=10,
        fraction_non_clifford=0.3,
        random_state=RNG_SEED,
    )
    cdr_val = float(cdr_val)
    print(f"[CDR   ] <Z_0> = {cdr_val:+.6f}   |err| = {abs(cdr_val-exact):.4f}")

    elapsed = time.time() - t0
    results = {
        "paper": "arXiv:2107.13470",
        "replication_date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "circuit": {"nqubits": NQ, "depth": DEPTH, "gates": qc.size()},
        "noise_model": {"depolarizing_1q": P1, "depolarizing_2q": P2},
        "shots_per_execution": SHOTS,
        "observable": "<Z_0>",
        "exact": exact,
        "raw_noisy": raw,
        "zne": zne_val,
        "pec": pec_val,
        "cdr": cdr_val,
        "abs_error": {
            "raw": abs(raw - exact),
            "zne": abs(zne_val - exact),
            "pec": abs(pec_val - exact),
            "cdr": abs(cdr_val - exact),
        },
        "elapsed_seconds": elapsed,
        "seed": RNG_SEED,
        "versions": {},
    }
    import mitiq, qiskit, qiskit_aer, cirq
    results["versions"] = {
        "mitiq": mitiq.__version__,
        "qiskit": qiskit.__version__,
        "qiskit_aer": qiskit_aer.__version__,
        "cirq": cirq.__version__,
        "python": sys.version.split()[0],
    }

    # verdict tally
    raw_err = results["abs_error"]["raw"]
    beats = {k: results["abs_error"][k] < raw_err for k in ("zne", "pec", "cdr")}
    n_beats = sum(beats.values())
    results["methods_beating_raw"] = beats
    results["n_methods_beating_raw"] = n_beats
    print(f"\n[VERDICT] methods that beat raw noisy: {n_beats}/3 -> {beats}")

    out = EVID_DIR / "replication_results.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"[write ] {out}")


if __name__ == "__main__":
    main()
