#!/usr/bin/env python3
"""
Replication of Mitiq Fig. 5 (PEC toy example), LaRose et al. 2020 (arXiv:2009.04417).

Paper setup (Sec 3.3):
  Circuit U = CNOT_{1,2} o X_1 o H_2  (chronological R->L: H on q2, X on q1, then CNOT)
  Observable O = |00><00|, exact ideal value = 0.
  Noise model: local single-qubit depolarizing after EACH gate, p = 0.1.
  Density-matrix simulation (no shot noise). 1000 PEC samples.
Paper results:
  unmitigated expectation = 0.0622
  PEC-mitigated           = 0.0071  (~order of magnitude improvement)
"""
import json, numpy as np
import cirq
from mitiq import pec
from mitiq.pec.representations.depolarizing import represent_operations_in_circuit_with_local_depolarizing_noise

np.random.seed(42)
NOISE_P = 0.1
N_SAMPLES = 1000

# --- Build the circuit U = CNOT_{1,2} o X_1 o H_2 ---
q = cirq.LineQubit.range(2)
q0, q1 = q[0], q[1]  # q0 == qubit "1", q1 == qubit "2" in paper's 1-indexing
circuit = cirq.Circuit(
    cirq.H(q1),          # H_2
    cirq.X(q0),          # X_1
    cirq.CNOT(q0, q1),   # CNOT_{1,2}
)
print("Circuit:")
print(circuit)

# --- Executor: density-matrix sim with local depolarizing noise after each gate ---
def executor(circ: cirq.Circuit) -> float:
    """Return <00|rho|00> under single-qubit depolarizing noise p after each gate."""
    noisy = circ.with_noise(cirq.depolarize(p=NOISE_P))
    rho = cirq.DensityMatrixSimulator().simulate(noisy).final_density_matrix
    # <00|rho|00> is the (0,0) diagonal element (population of |00>)
    return float(np.real(rho[0, 0]))

# --- Ideal (noiseless) value for reference ---
ideal_rho = cirq.DensityMatrixSimulator().simulate(circuit).final_density_matrix
ideal_val = float(np.real(ideal_rho[0, 0]))

# --- Unmitigated noisy value ---
unmitigated = executor(circuit)

# --- PEC: build quasi-probability reps for local depolarizing noise, then mitigate ---
reps = represent_operations_in_circuit_with_local_depolarizing_noise(circuit, NOISE_P)
pec_value = pec.execute_with_pec(
    circuit, executor, representations=reps, num_samples=N_SAMPLES, random_state=1
)
# execute_with_pec may return float or (value, data); normalize
if isinstance(pec_value, tuple):
    pec_value = pec_value[0]
pec_value = float(pec_value)

# --- Compare to paper ---
paper = {"unmitigated": 0.0622, "pec": 0.0071}
out = {
    "ideal_value": ideal_val,
    "unmitigated": unmitigated,
    "pec_mitigated": pec_value,
    "abs_err_unmitigated": abs(unmitigated - ideal_val),
    "abs_err_pec": abs(pec_value - ideal_val),
    "improvement_factor": (abs(unmitigated - ideal_val) / abs(pec_value - ideal_val))
        if abs(pec_value - ideal_val) > 1e-12 else None,
    "paper_unmitigated": paper["unmitigated"],
    "paper_pec": paper["pec"],
    "noise_p": NOISE_P,
    "n_samples": N_SAMPLES,
}
print(json.dumps(out, indent=2))
with open("evidence_pec.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nSaved evidence_pec.json")
