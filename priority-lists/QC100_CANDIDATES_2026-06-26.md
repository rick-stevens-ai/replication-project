# QC-100 Quantum-Computing Replication Candidates

Generated 2026-06-26. **130 feasibility-passing candidates** (target ≥110 to clear 100 after attrition).

**Source pool:** 422 arXiv papers across 22 quantum-computing subtopic queries (cat:quant-ph filter), enriched with Semantic Scholar citation counts (authenticated S2 API).

**Filter:** dropped 12 as reviews/roadmaps/hardware-only. Remaining were scored by `log(1+cites) + algo-core hits + recency + OA-PDF + code-mention − collab/no-algo penalties`, then balanced per subtopic (cap 12).

## Subtopic distribution

| Subtopic | Count | Primary simulator |
|---|---:|---|
| qec-surface-code | 12 | Stim + PyMatching / Qiskit |
| qaoa | 12 | Qiskit / PennyLane / Cirq + classical optimizer |
| ham-sim-trotter | 10 | Qiskit / Cirq / QuTiP |
| vqe | 9 | Qiskit Nature / PennyLane / OpenFermion + NumPy |
| quantum-chemistry | 8 | OpenFermion / Qiskit Nature / PennyLane |
| error-mitigation | 7 | Mitiq + Qiskit / Cirq noisy sim |
| algorithms-shor | 7 | Qiskit (small N) / Cirq numerics |
| benchmarking-qv | 6 | Qiskit / Cirq noisy sim |
| algorithms-amplitude-estimation | 6 | Qiskit / Cirq statevector + MLE |
| compilation-transpilation | 6 | Qiskit transpiler / t|ket> / BQSKit |
| benchmarking-rb | 6 | Qiskit / Cirq / Stim noisy sim |
| noise-models | 6 | Qiskit Aer / Cirq / Stim depolarizing models |
| qec-general | 5 | Stim / Qiskit / custom decoder code |
| qml | 5 | PennyLane / TensorFlow Quantum / Qiskit ML |
| classical-sim-stabilizer | 4 | Stim / Cirq Clifford |
| algorithms-phase-estimation | 4 | Qiskit / Cirq statevector |
| classical-sim-tensor-network | 4 | ITensor / quimb / TeNPy |
| algorithms-grover | 4 | Qiskit / Cirq / PennyLane statevector |
| ham-sim-qubitization | 3 | Qiskit / OpenFermion / NumPy linalg |
| qec-stim | 2 | Stim + PyMatching |
| resource-estimation | 2 | Azure Quantum RE / Qualtran / pen-and-paper + sim |
| algorithms-hhl-linsys | 2 | Qiskit statevector / NumPy linalg |

## Top 15 by feasibility+impact score

| Rank | Cites | Year | Subtopic | Title (arXiv) |
|---:|---:|---:|---|---|
| 1 | 1686 | 2018 | quantum-chemistry | Quantum Chemistry in the Age of Quantum Computing ([1812.09976](https://arxiv.org/abs/1812.09976)) |
| 2 | 663 | 2021 | qec-stim | Stim: a fast stabilizer circuit simulator ([2103.02202](https://arxiv.org/abs/2103.02202)) |
| 3 | 319 | 2021 | qec-surface-code | Realization of an Error-Correcting Surface Code with Superconducting Qubits ([2112.13505](https://arxiv.org/abs/2112.13505)) |
| 4 | 429 | 2018 | classical-sim-stabilizer | Simulation of quantum circuits by low-rank stabilizer decompositions ([1808.00128](https://arxiv.org/abs/1808.00128)) |
| 5 | 495 | 2020 | benchmarking-qv | Demonstration of quantum volume 64 on a superconducting quantum computing system ([2008.08571](https://arxiv.org/abs/2008.08571)) |
| 6 | 290 | 2019 | algorithms-amplitude-estimation | Amplitude estimation without phase estimation ([1904.10246](https://arxiv.org/abs/1904.10246)) |
| 7 | 308 | 2019 | qec-surface-code | Repeated Quantum Error Detection in a Surface Code ([1912.09410](https://arxiv.org/abs/1912.09410)) |
| 8 | 238 | 2019 | vqe | Quantum Computation of Electronic Transitions using a Variational Quantum Eigensolver ([1901.01234](https://arxiv.org/abs/1901.01234)) |
| 9 | 208 | 2018 | vqe | Accelerated Variational Quantum Eigensolver ([1802.00171](https://arxiv.org/abs/1802.00171)) |
| 10 | 149 | 2020 | error-mitigation | Mitiq: A software package for error mitigation on noisy quantum computers ([2009.04417](https://arxiv.org/abs/2009.04417)) |
| 11 | 133 | 2023 | qec-surface-code | Relaxing Hardware Requirements for Surface Code Circuits using Time-dynamics ([2302.02192](https://arxiv.org/abs/2302.02192)) |
| 12 | 125 | 2021 | qaoa | Parameter Concentration in Quantum Approximate Optimization ([2103.11976](https://arxiv.org/abs/2103.11976)) |
| 13 | 165 | 2018 | qec-surface-code | Tailoring surface codes for highly biased noise ([1812.08186](https://arxiv.org/abs/1812.08186)) |
| 14 | 156 | 2017 | algorithms-phase-estimation | Experimental Bayesian Quantum Phase Estimation on a Silicon Photonic Chip ([1703.05169](https://arxiv.org/abs/1703.05169)) |
| 15 | 113 | 2021 | algorithms-phase-estimation | A randomized quantum algorithm for statistical phase estimation ([2110.12071](https://arxiv.org/abs/2110.12071)) |

## Notes

- All entries are reproducible on simulators (Qiskit / Cirq / PennyLane / Stim / OpenFermion / tensor-network libs). No real QPU required.
- Spot-check before download: confirm abstract really describes a concrete algorithm/method (not just a literature review or hardware-only demo). Heuristic feasibility filter is fast but coarse.
- PDFs are one `curl https://arxiv.org/pdf/{arxiv_id}.pdf` away when needed.
