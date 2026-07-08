#!/usr/bin/env python3
"""
Replication of Mitiq ZNE core claim, LaRose et al. 2020 (arXiv:2009.04417).

Paper claim (Sec 2 / Fig 3): a single line `execute_with_zne(circuit, executor)`
extrapolates a noisy expectation value back toward the noiseless limit, giving a
mitigated value closer to truth than the unmitigated one.

We use a benchmark analogous to Fig 3 (randomized-benchmarking-style circuits where
the ideal observable <00|rho|00> = 1): mitiq's built-in RB benchmark circuits, a
Cirq density-matrix executor with depolarizing noise, and default ZNE
(random local unitary folding + Richardson extrapolation).

Testable prediction: mean |mitigated - 1| < mean |unmitigated - 1| across circuits.
"""
import json, numpy as np
import cirq
from mitiq import zne
from mitiq.benchmarks import generate_rb_circuits

np.random.seed(7)
NOISE_P = 0.01
N_CIRCUITS = 20

def make_executor(p):
    def executor(circ: cirq.Circuit) -> float:
        noisy = circ.with_noise(cirq.depolarize(p=p))
        rho = cirq.DensityMatrixSimulator().simulate(noisy).final_density_matrix
        return float(np.real(rho[0, 0]))  # <00|rho|00>, ideal = 1 for RB (identity) circuit
    return executor

executor = make_executor(NOISE_P)

# RB circuits (Clifford, compile to identity => ideal <00|rho|00> = 1)
circuits = generate_rb_circuits(n_qubits=2, num_cliffords=10, trials=N_CIRCUITS)

ideal = 1.0
unmit_errs, mit_errs = [], []
rows = []
for i, c in enumerate(circuits):
    unmit = executor(c)
    mit = zne.execute_with_zne(c, executor)  # default: local folding + Richardson
    mit = float(mit[0]) if isinstance(mit, tuple) else float(mit)
    ue, me = abs(unmit - ideal), abs(mit - ideal)
    unmit_errs.append(ue); mit_errs.append(me)
    rows.append({"circuit": i, "unmitigated": unmit, "mitigated": mit,
                 "err_unmit": ue, "err_mit": me})

mean_unmit = float(np.mean(unmit_errs))
mean_mit = float(np.mean(mit_errs))
out = {
    "noise_p": NOISE_P,
    "n_circuits": N_CIRCUITS,
    "ideal_value": ideal,
    "mean_abs_err_unmitigated": mean_unmit,
    "mean_abs_err_mitigated": mean_mit,
    "error_reduction_factor": mean_unmit / mean_mit if mean_mit > 0 else None,
    "zne_helps_on_average": mean_mit < mean_unmit,
    "fraction_circuits_improved": float(np.mean([r["err_mit"] < r["err_unmit"] for r in rows])),
    "per_circuit": rows,
}
print(json.dumps({k: v for k, v in out.items() if k != "per_circuit"}, indent=2))
with open("evidence_zne.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nSaved evidence_zne.json")
