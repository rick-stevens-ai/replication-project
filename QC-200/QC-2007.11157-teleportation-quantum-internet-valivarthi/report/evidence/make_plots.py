#!/usr/bin/env python3
"""Plot fidelity vs channel dephasing sweep, with paper anchor line."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace, state_fidelity
from qiskit_aer import AerSimulator

HERE = Path(__file__).resolve().parent

# Import sim helpers by execfile-style
import sys
sys.path.insert(0, str(HERE))
from teleport_sim import (
    build_dephasing_noise,
    prep_state,
    target_statevector,
    teleportation_circuit,
)

ideal_labels = ["0", "1", "+", "-", "+i", "-i"]


def mean_fidelity_for_prob(prob: float) -> float:
    Fs = []
    for lab in ideal_labels:
        prep = prep_state(lab)
        qc = teleportation_circuit(prep)
        qc.save_density_matrix()
        noise = build_dephasing_noise(prob)
        sim = AerSimulator(method="density_matrix", noise_model=noise)
        res = sim.run(qc, shots=1).result()
        rho = DensityMatrix(np.asarray(res.data(0)["density_matrix"]))
        rho_bob = partial_trace(rho, [0, 1])
        psi = target_statevector(lab)
        Fs.append(state_fidelity(rho_bob, psi))
    return float(np.mean(Fs))


def main() -> None:
    probs = np.linspace(0.0, 0.6, 25)
    Fs = [mean_fidelity_for_prob(float(p)) for p in probs]

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(probs, Fs, "o-", label="Qiskit-Aer simulation")
    ax.axhline(0.89, color="C3", linestyle="--", label="Paper $F_{avg}=0.89$")
    ax.axhline(2 / 3, color="0.5", linestyle=":", label="Classical limit $F=2/3$")
    ax.set_xlabel("Phase-damping parameter $\\lambda_{pd}$ on entangled channel")
    ax.set_ylabel(r"Mean teleportation fidelity $\langle F\rangle$")
    ax.set_title("QC-2007.11157 replication: fidelity vs channel dephasing")
    ax.set_ylim(0.5, 1.02)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(HERE / "fig_fidelity_vs_noise.png", dpi=150)
    fig.savefig(HERE / "fig_fidelity_vs_noise.pdf")

    with open(HERE / "sweep.json", "w") as f:
        json.dump({"lambda_pd": probs.tolist(), "mean_fidelity": Fs,
                   "paper_experimental_F_avg": 0.89,
                   "classical_limit": 2 / 3}, f, indent=2)
    print(f"wrote fig_fidelity_vs_noise.png + .pdf (n={len(probs)})")


if __name__ == "__main__":
    main()
