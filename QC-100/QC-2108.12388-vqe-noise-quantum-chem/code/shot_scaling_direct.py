"""Direct verification of the 1/sqrt(N) shot-noise scaling.

At a FIXED parameter point (the noiseless-VQE optimum), repeatedly estimate
<H> with N shots and compute the empirical std across repetitions.  Then
regress log(std) vs log(N) -- paper (and standard theory) predicts slope
-0.5.
"""
import json, math, sys
from pathlib import Path
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator

from build_h2_hamiltonian import build_h2, openfermion_to_qiskit_sparsepauliop
from vqe_noise_study import (
    hardware_efficient_ry_cz, qubitwise_commuting_groups, energy_sampled,
)

sys.stdout.reconfigure(line_buffering=True)

DATA = Path("../data/vqe_results.json")
res = json.loads(DATA.read_text())
# Recover optimal params from the noiseless run
nl = [r for r in res["runs"] if r["noise_type"] == "noiseless"][0]
opt_params = nl["final_params"]

mol, qham, hf, fci = build_h2(0.735)
H = openfermion_to_qiskit_sparsepauliop(qham, mol.n_qubits)
ansatz, params = hardware_efficient_ry_cz(mol.n_qubits, reps=1)
groups = qubitwise_commuting_groups(H)
backend = AerSimulator()

print("=== Direct 1/sqrt(N) shot-noise scaling ===")
print("Fixed params from noiseless-VQE optimum; energy re-sampled many times per N.")
Ns = [128, 512, 2048, 8192, 32768]
n_reps = 40
results = []
for N in Ns:
    samples = []
    for _ in range(n_reps):
        e = energy_sampled(ansatz, opt_params, groups, backend, N, mol.n_qubits)
        samples.append(e)
    mean = float(np.mean(samples))
    std  = float(np.std(samples, ddof=1))
    print(f"  N={N:>6d}  mean={mean:.6f}  std={std:.6f}  1/sqrt(N)={1/math.sqrt(N):.4f}")
    results.append({"N": N, "mean": mean, "std": std, "n_reps": n_reps})

# fit log(std) = alpha*log(N) + b
logN = np.log10([r["N"] for r in results])
logS = np.log10([r["std"] for r in results])
alpha, b = np.polyfit(logN, logS, 1)
print(f"\nFit: std ~ N^{alpha:.3f}  (theory: N^-0.5)")
print(f"|alpha - (-0.5)| = {abs(alpha+0.5):.3f}")

out = {
    "Ns": Ns,
    "n_reps_per_N": n_reps,
    "opt_params": opt_params,
    "samples_summary": results,
    "power_law_alpha": float(alpha),
    "power_law_intercept": float(b),
    "theory_alpha": -0.5,
    "matches_theory": bool(abs(alpha+0.5) < 0.15),
}
Path("../data/shot_scaling_direct.json").write_text(json.dumps(out, indent=2))
print("\nWrote ../data/shot_scaling_direct.json")

# Figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4.5))
Nv = np.array([r["N"] for r in results])
Sv = np.array([r["std"] for r in results])
ax.loglog(Nv, Sv, 'o-', label=f'measured std (n_reps={n_reps})')
Nfine = np.logspace(np.log10(Nv.min()), np.log10(Nv.max()), 50)
# fit line
ax.loglog(Nfine, 10**b * Nfine**alpha, '--', color='r',
          label=f'fit: std ~ N^{alpha:.2f}')
ax.loglog(Nfine, Sv[0] * (Nv[0]/Nfine)**0.5, ':', color='k',
          label='theory: N^-0.5')
ax.set_xlabel('N shots'); ax.set_ylabel('empirical std of <H> (Ha)')
ax.set_title('Shot-noise scaling of <H> (fixed VQE-optimum params)\n'
             'arXiv:2108.12388 replication')
ax.grid(alpha=0.3, which='both'); ax.legend()
fig.tight_layout()
fig.savefig("../figures/shot_scaling.png", dpi=130)
print("Wrote ../figures/shot_scaling.png")
