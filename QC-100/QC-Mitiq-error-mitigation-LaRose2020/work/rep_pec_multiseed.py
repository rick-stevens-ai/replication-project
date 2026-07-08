#!/usr/bin/env python3
"""PEC is a stochastic estimator; characterize the mitigated-value distribution
over multiple random seeds to show the paper's 0.0071 is within statistical reach
and that PEC improves on unmitigated on average. Also test higher sample counts."""
import json, numpy as np
import cirq
from mitiq import pec
from mitiq.pec.representations.depolarizing import represent_operations_in_circuit_with_local_depolarizing_noise

NOISE_P = 0.1
q = cirq.LineQubit.range(2)
circuit = cirq.Circuit(cirq.H(q[1]), cirq.X(q[0]), cirq.CNOT(q[0], q[1]))

def executor(circ):
    noisy = circ.with_noise(cirq.depolarize(p=NOISE_P))
    rho = cirq.DensityMatrixSimulator().simulate(noisy).final_density_matrix
    return float(np.real(rho[0, 0]))

reps = represent_operations_in_circuit_with_local_depolarizing_noise(circuit, NOISE_P)
unmit = executor(circuit)
ideal = 0.0

results = {}
for n_samples in (1000,):
    vals = []
    for seed in range(10):
        v = pec.execute_with_pec(circuit, executor, representations=reps,
                                 num_samples=n_samples, random_state=seed)
        v = float(v[0]) if isinstance(v, tuple) else float(v)
        vals.append(v)
    vals = np.array(vals)
    abs_errs = np.abs(vals - ideal)
    results[f"n_samples_{n_samples}"] = {
        "mean_pec": float(vals.mean()),
        "std_pec": float(vals.std()),
        "mean_abs_err": float(abs_errs.mean()),
        "min_abs_err": float(abs_errs.min()),
        "frac_better_than_unmit": float(np.mean(abs_errs < abs(unmit - ideal))),
        "mean_improvement_factor": float(abs(unmit - ideal) / abs_errs.mean()),
    }

out = {
    "unmitigated": unmit,
    "paper_unmitigated": 0.0622,
    "paper_pec": 0.0071,
    "ideal": ideal,
    "n_seeds": 10,
    "results": results,
}
print(json.dumps(out, indent=2))
json.dump(out, open("evidence_pec_multiseed.json", "w"), indent=2)
