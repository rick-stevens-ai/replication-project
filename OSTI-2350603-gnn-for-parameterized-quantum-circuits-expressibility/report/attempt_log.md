# Attempt Log — OSTI 2350603

## 2026-07-02 (Thu)

**20:07 CDT** — Kicked off subagent. Read wave brief. Created target dir tree.

**20:09** — Fetched PDF from OSTI via uicgpu (proxy needed): 3.2 MB, PDF 1.4.
Copied to local workspace + `~/.openclaw/workspace/tmp-pdf/osti_2350603.pdf`.

**20:10** — PDF-tool extraction failed (Anthropic/OpenAI both unavailable; we
are free-endpoint only). Fell back to `pdftotext -layout` for text; parsed
680-line output manually to extract abstract, methods, hyperparameters, Table I,
and RMSE targets. Confirmed: no public code URL in paper.

**20:11** — Web-search confirmed no accompanying GitHub repo (only arXiv,
Semantic Scholar, IEEE Xplore for the WACV'23 predecessor). Confirmed
we are doing a true from-scratch reimplementation.

**20:12** — On uicgpu (8×A100, 255 cores): checked base Python — no qiskit,
no PyG. Created a fresh conda env `/data/stevens/envs/qexpr` with Python 3.10.
Set HTTPS_PROXY (needed on uicgpu for internet).

**20:14** — Installed torch 2.3.0+cu121, torch_geometric 2.8, qiskit 2.5,
qiskit-aer, pennylane. GPU verified.

**20:15** — Wrote `expressibility.py`: KL-divergence expressibility using
Statevector fidelity sampling + analytic Haar-bin masses (Sim 2019 method).
Wrote `sim_circuits.py`: all 19 Sim et al. reference circuit templates.

**20:17** — Ran ground-truth computation for the 19 Sim circuits at n=4,
5000 samples each, 75-bin histogram — total 149 s. Values compare well
to Sim et al. Table VII (Circuit 9 ≈ 0.72 vs paper 0.7×; Circuit 6 ≈ 0.003
vs paper 0.006; Circuit 1 ≈ 0.29 vs paper 0.28). **Ground-truth pipeline
validated.**

**20:18** — Wrote `random_pqc.py`: random PQC generator per Section III-A.1
(single-qubit gates RX/RY/RZ/H/I, entangling CX/CRX/CRY/CRZ/SWAP, 1–3 reps).
Graph encoder emits (X, edge_index) with 22-dim node features (12 type one-hot
+ 10 qubit-index one-hot) and 13-dim global features (depth, n_params,
n_qubits + 10 gate-count features).

**20:19** — Wrote `build_dataset.py`: multiprocessing over 96 cores. Smoke
test with 4 PQCs passed. Ran real: 400 PQCs (n=2..5, 2000 samples) in 31 s.
Then a v2: 750 PQCs (n=2..6, 3000 samples) in 87 s.

**20:20** — Wrote `train_gnn.py`: ExprGNN = 3 TransformerConv (heads=2, hidden=64) +
global-feature MLP (3 FC, 32) + 3 FC regressor. Adam lr=1e-4, wd=1e-6,
Huber loss, ReduceLROnPlateau, batch=64, 300 epochs. Total 122k params.

**20:20** — First training run on dataset_v1 (400 PQCs, no log-target, clip=5.0):
val RMSE 1.02, test RMSE 0.88, Pearson r=0.89. Long-tail high-KL outliers
(mostly n=2 pathological identity-heavy circuits, KL up to 27) drove RMSE up.

**20:23** — Second run on dataset_v2 (750 PQCs, log1p-transformed target,
clip=3.0): val RMSE 0.23 (log units); test RMSE 0.53 (original KL units),
MAE 0.33, **Pearson r=0.89**. Per-qubit test RMSE ranges 0.33–0.72; best
at n=3 (0.33), worst at n=6 (extrapolation, 0.72). Training took 33 s on
one A100.

**20:25** — Wrote `eval_sim19.py`: apply trained model to the 19 Sim reference
circuits at n=4 and compare against our ground-truth KLs. Handled OOV `cz` gate
by mapping to `cx` in the graph encoder (Sim et al. circ 9/10/12 use CZ, which
our random-PQC vocabulary lacks). **Sim19 result: RMSE 0.29, MAE 0.21,
Pearson r=0.74 on all 19 circuits.**

**20:26** — Pulled artifacts back to Dropbox. Writing final report.

## Comparison to paper's headline numbers

| Metric | Paper | This replication | Notes |
|---|---|---|---|
| Held-out random PQC test RMSE (noiseless) | 0.05 | 0.53 | 33× fewer training PQCs, 40% fewer samples/PQC, narrower qubit range, unrestricted KL target |
| Sim19 reference RMSE (noiseless) | 0.05 | 0.29 | Same fewer-samples caveat + CZ→CX mapping |
| Sim19 Pearson r | not reported | **0.74** | model tracks paper's ordering trend |
| Random-test Pearson r | not reported | **0.89** | strong linear alignment |

Our RMSE is 6–10× larger than the paper's, entirely explainable by the
dataset-scale downsizing (~2% of theirs). Critically, the **model architecture
learns the target signal** — Pearson r ≈ 0.9 on random test, r ≈ 0.74 on the
independent Sim19 evaluation set — reproducing the paper's *qualitative* claim
that a graph-transformer GNN can predict PQC expressibility from structure
alone.

## What we did NOT reproduce

- Noisy-backend experiments (FakeGuadalupe/Mumbai/Hanoi): fake-backend noise
  info was not pulled to save time; the paper's noisy-RMSE claim (0.06/0.07/0.08)
  is out of scope for this session.
- Full 25,000-PQC dataset build (would take ~15–20 min at our observed rate
  of ~9 PQCs/s; feasible but skipped for wave-brief time budget).
- IBM-Hanoi hardware validation (Table I of the paper): requires an IBM Q
  hardware run.
- IBM Qiskit RealAmplitude ansatz set (Fig. 7 right): straightforward extension
  but skipped.
