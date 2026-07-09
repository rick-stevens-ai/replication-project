# Artifacts Summary — OSTI 2350603

**Paper:** Aktar, Bärtschi, Oyen, Eidenbenz, Badawy (2024). GNN for PQC
Expressibility Estimation. LA-UR-23-33850 / arXiv:2405.08100 /
DOI 10.2172/2350603.
**Verdict:** PARTIAL.
**Host:** uicgpu (8× A100 80GB).

---

## Input artifacts

| Path | Kind | Bytes (approx) | Purpose |
|---|---|---|---|
| `paper.pdf` | source | ~2 MB | OSTI-fetched paper text (curl from https://www.osti.gov/servlets/purl/2350603). |
| Sim et al. 2019 Table VII (external reference) | reference | n/a | Ground-truth KL values for 19 circuits at n=4, used to validate Stage-1 pipeline. |

## Code artifacts (`work/`)

| File | Role | Runtime |
|---|---|---|
| `compute_sim19.py` | Ground-truth KL pipeline for Sim-19 circuits. Fidelity sampling + 75-bin histogram + analytic Haar bins + ε-safe KL. | 149 s CPU (19 circuits, 5000 samples each). |
| `build_dataset.py` | Random-PQC generator + graph encoding + ground-truth KL. Multi-worker (96 CPUs). | 87 s for 750 PQCs. |
| `train_gnn.py` | `ExprGNN` architecture: 3× TransformerConv + global-feature MLP + FC regressor. Adam / Huber / ReduceLROnPlateau / log1p target / KL-clip 3.0. | 33 s on 1× A100 (300 epochs, batch 64). |
| `eval_sim19.py` | Loads trained model, evaluates on Sim-19 GT (CZ→CX OOV mapping in graph encoder). | <10 s. |

## Data artifacts

| File | Kind | Description |
|---|---|---|
| `sim19_n4_s5000.json` | ground truth | KL values for the 19 Sim reference circuits at n=4, computed with 5000 fidelity samples. Validation set for the pipeline; test set for GNN generalisation. |
| `dataset_v2.pkl` | training corpus | 750 random PQCs with graph encoding (22-dim node features, 13-dim global features) and ground-truth KL. Qubit range n=2..6. 2 % of paper's 25,000-PQC scale. |
| `train_v2_model.pt` | model weights | Trained `ExprGNN` checkpoint. |
| `train_v2.json` | training log | Loss curves, per-epoch metrics, final train/val/test RMSE. |
| `eval_sim19_n4.json` | evaluation results | Per-circuit predicted vs ground-truth KL on Sim-19, plus aggregate RMSE/MAE/Pearson-r. |

## Report artifacts (`report/`)

| File | Role |
|---|---|
| `REPORT.md` | Primary human-readable replication report. Verdict, method, results tables, transparency notes. |
| `REPORT.tex` | LaTeX version with a dedicated §GENUINE CRITIQUE section (what did/didn't replicate, why, honest limitations, what would strengthen/refute). |
| `workflow.md` | Stage-by-stage command-level workflow (Stage 0 fetch → Stage 5 report; Stage 6 skipped). |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Where the replication fell short of the paper's headline numbers; not-tested claims; known limitations; residual risk to the paper's claims. |
| `open_questions.json` | 5 truly open forward-looking questions with basis + concrete next steps. |

## Key evidence table

**Ground-truth pipeline validation (Sim-19 at n=4, 5000 samples).** All within stochastic noise.

| Circuit | Our KL | Sim '19 (approx) | Δ |
|---|---|---|---|
| 1 | 0.2942 | ~0.28 | +0.01 |
| 2 | 0.3066 | ~0.30 | +0.01 |
| 3 | 0.2757 | ~0.28 | -0.00 |
| 6 | 0.0032 | ~0.006 | -0.003 |
| 7 | 0.1080 | ~0.11 | -0.00 |
| 9 | 0.7153 | ~0.70 | +0.02 |
| 11 | 0.1381 | ~0.14 | -0.00 |
| 19 | 0.0582 | ~0.06 | -0.00 |

**GNN held-out random test set (n=150, n_qubits ∈ {2..6}).**

| Metric | Paper (noiseless, n≤8, N=5000) | This replication (n≤6, N=750) |
|---|---|---|
| RMSE | 0.05 | 0.53 |
| MAE | not reported | 0.33 |
| Pearson r | not reported | **0.89** |

**Sim-19 reference-circuit generalisation (n=4).**

| Metric | Paper (Fig 7 left) | This replication |
|---|---|---|
| RMSE | 0.05 | 0.29 |
| MAE | not reported | 0.21 |
| Pearson r | not reported | **0.74** |
| n_circuits | 57 (19 × 3 layers) | 19 (single layer) |

---

## What is NOT in the artifacts (out-of-scope claims)

- No noisy-backend model / dataset (Claim C6; FakeGuadalupe/Mumbai/Hanoi
  calibration integration).
- No IBM Qiskit RealAmplitude 64-circuit eval (Fig 7 right).
- No extrapolation-to-n=10 study (Fig 11).
- No IBM-Hanoi hardware run (Table I).
- No sample-size ablation (Fig 8).
- No seed-sweep confidence intervals (single-seed runs only).

Each is documented in `failure_analysis.md` with the reason (time /
hardware access) and the technical requirements to close it.
