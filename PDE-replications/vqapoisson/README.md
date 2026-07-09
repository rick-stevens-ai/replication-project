# VQAPoisson Replication

Reproduction of **Sato, Kondo, Koide, Takamatsu, Imoto — "Variational quantum
algorithm based on the minimum potential energy for solving the Poisson
equation"**, Phys. Rev. A 104, 052409 (2021).

Upstream repo: <https://github.com/ToyotaCRDL/VQAPoisson> (Apache-2.0).

## Layout

```
vqapoisson/
├── README.md                  # this file
├── PROGRESS.md                # live progress log (updated as the agent works)
├── REPORT.md                  # final report (written when run completes)
├── repo/                      # upstream clone (untouched)
├── scripts/
│   ├── vqa_poisson_modern.py  # modernized port of vqa_poisson.py to Qiskit 2.x
│   └── run_experiment.py      # BFGS experiment driver, Periodic|Dirichlet|Neumann
├── logs/                      # stdout/stderr from runs
├── results/                   # PNGs + JSON summaries per run
└── .venv/                     # Python 3.12 venv (qiskit 2.4, qiskit-aer 0.17)
```

## What was changed vs. upstream

The upstream code targets Python 3.7 + qiskit 0.23.6 + `qiskit.aqua` 0.8.2,
all long since end-of-lifed. The algorithm/circuits are unchanged; only the
backend scaffolding was modernized:

| upstream (2021) | this port |
| --- | --- |
| `from qiskit.aqua import QuantumInstance` | local `_StatevectorQI` shim |
| `execute(qc, backend).result().get_statevector()` | `qiskit.quantum_info.Statevector.from_instruction(qc)` |
| `qc.mct(...)` | `qc.mcx(...)` |
| Py 3.7 / qiskit 0.23 | Py 3.12 / qiskit 2.4 / qiskit-aer 0.17 |

Ansatz, parameter-shift gradient, A-matrix construction for the three boundary
conditions, and the BFGS optimization loop are byte-identical in behavior to
the upstream.

## How to reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-replications/vqapoisson
source .venv/bin/activate
cd scripts
python run_experiment.py --num-qubits 3 --num-layers 4 --maxiter 300 --seed 0
```

Outputs land in `../results/` as `sol_<bc>_n<N>_L<L>.png` plus a JSON summary.
