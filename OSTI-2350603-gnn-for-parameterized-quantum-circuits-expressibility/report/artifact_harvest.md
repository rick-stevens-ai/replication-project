# Artifact Harvest — OSTI 2350603

## Papers

- **Primary paper (this OSTI ID):** LA-UR-23-33850, "Graph Neural Networks
  for Parameterized Quantum Circuits Expressibility Estimation (Rev.1)",
  Aktar et al., 2024-05-09.
  URL: https://www.osti.gov/servlets/purl/2350603
  Size: 3,281,707 bytes (3.13 MB)
  Local: `work/paper.pdf`
- **Predecessor:** arXiv:2309.06975 (Poster at IEEE QCE'23) — same authors,
  smaller-scale prototype of the same idea. NOT downloaded (superseded by
  primary).
- **Ground-truth reference:** Sim, Johnson, Aspuru-Guzik, "Expressibility and
  entangling capability of parameterized quantum circuits …", arXiv:1905.10876,
  2019 — defines the 19 reference circuits used here.

## Datasets

- **No dataset published by the authors.** The paper's 25,000-PQC dataset is
  not released. We generated our own 750-PQC dataset from scratch following
  the recipe in Section III-A.1.
  - Local: `work/remote_output/dataset_v2.pkl`  (2,091,231 bytes)
  - Content: 750 randomly-generated PQCs, n ∈ {2,3,4,5,6}, 150 per n,
    each with 3000 fidelity samples for KL computation.
  - Seed: 20260702.

## Code

- **No code released by authors.** All implementation is our own:
  - `work/expressibility.py` — Sim-2019 statistical expressibility method
  - `work/sim_circuits.py` — Sim et al. 19 reference-circuit templates
  - `work/random_pqc.py` — random-PQC generator + graph encoder
  - `work/build_dataset.py` — multiprocessing dataset builder
  - `work/train_gnn.py` — TransformerConv GNN training script
  - `work/eval_sim19.py` — Sim19 evaluation script
  - `work/compute_sim19.py` — ground-truth KL for Sim19

## Software / tool versions (uicgpu env `/data/stevens/envs/qexpr`)

- Python 3.10
- torch 2.3.0+cu121 (CUDA 12.1)
- torch_geometric 2.8.0
- qiskit 2.5.0
- qiskit-aer (bundled)
- pennylane (installed but unused in final pipeline)
- numpy, scipy, scikit-learn

## Hardware

- uicgpu: 8× NVIDIA A100 80 GB PCIe, 255 CPU cores.
  - Training used 1 A100 (CUDA_VISIBLE_DEVICES=0). Trivial GPU cost (~30 s).
  - Dataset build used 96 CPU workers.

## Output evidence

- `report/evidence/sim19_n4_s5000.json` — ground-truth KL of Sim19 circuits (validates our KL pipeline).
- `report/evidence/train_v2.json` — GNN training config + test RMSE/MAE/Pearson.
- `report/evidence/train_v2_preds.npz` — per-test-sample predictions + labels + qubit counts.
- `report/evidence/eval_sim19_n4.json` — Sim19 prediction accuracy.
