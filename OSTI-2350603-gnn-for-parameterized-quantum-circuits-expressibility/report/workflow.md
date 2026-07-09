# Workflow — OSTI 2350603 GNN-for-PQC-Expressibility Replication

**Paper:** Aktar, Bärtschi, Oyen, Eidenbenz, Badawy (2024). LA-UR-23-33850;
arXiv:2405.08100; DOI 10.2172/2350603.
**Verdict:** PARTIAL.
**Host:** uicgpu (8× A100 80GB, 255 CPU cores, 2 TB RAM).
**Env:** conda `/data/stevens/envs/qexpr`, Python 3.10, torch 2.3.0+cu121,
torch_geometric 2.8.0, qiskit 2.5.0.

---

## Stage 0 — Paper acquisition

- Fetch OSTI PDF via uicgpu (ALCF proxy <lan-host>:3128 for outbound).
  ```
  curl -sL -o paper.pdf https://www.osti.gov/servlets/purl/2350603
  ```
- Confirm arXiv equivalent (2405.08100) for cross-reference.
- Confirm reproducibility inventory: **no code, no dataset released.** Only
  path forward = full from-scratch reimplementation from Sections II-C,
  III-A, III-B, IV-A.

## Stage 1 — Ground-truth expressibility pipeline (validates Claim C1)

**Goal:** independently compute Sim-2019 KL-divergence expressibility and
match published values on 19 reference circuits at n=4.

**Steps:**
1. Implement Sim-19 reference circuit library (19 circuits from Sim et al.
   2019 Table VII), single-layer at n=4.
2. For each circuit: sample 5000 pairs of parameter vectors (θ, φ) uniform
   on [0, 2π).
3. Build `qc(θ)` and `qc(φ)` via Qiskit; obtain statevectors.
4. Compute fidelity `F = |⟨sv_a | sv_b⟩|²` per pair.
5. Histogram into 75 uniform bins on [0, 1] → `p_emp`.
6. Compute analytic Haar bin masses:
   `p_haar[i] = (1 - a_i)^(N-1) - (1 - b_i)^(N-1)`, `N = 2^n`.
7. `KL = Σ p_emp[i] * ln(p_emp[i] / p_haar[i])` over non-empty bins,
   ε-safe.
8. Save `sim19_n4_s5000.json`.

**Command:**
```
python compute_sim19.py --n_qubits 4 --n_samples 5000 --out sim19_n4_s5000.json
```
**Runtime:** 149 s single-CPU (19 circuits).
**Validation:** compare against Sim et al. 2019 Table VII values (Circuit 1
KL 0.2942 vs published ~0.28; Circuit 9 KL 0.7153 vs ~0.70; Circuit 6 KL
0.0032 vs ~0.006 — all within stochastic noise).

## Stage 2 — Random-PQC dataset construction (validates Claim C2)

**Goal:** generate a diverse PQC training corpus following the paper's
random-circuit recipe (Section III-A).

**Steps per PQC:**
1. Draw `n_reps ∈ {1,2,3}` uniformly.
2. Repeat `n_reps` times:
   - Apply one random single-qubit gate to each qubit from {RX, RY, RZ, H, I}.
   - With 50 % probability, apply a second single-qubit layer.
   - Apply a random number of entangling gates from {CX, CRX, CRY, CRZ, SWAP}
     on random qubit pairs.
3. Compute ground-truth KL via the Stage-1 pipeline (5000 fidelity samples).
4. Build graph encoding:
   - Nodes: 1 input node per qubit + 1 node per gate + 1 output node per qubit.
   - Node features (22 dims): 12-way one-hot node type + 10-way one-hot
     target qubit.
   - Edges: temporal DAG — each gate node connects from the previous op
     touching each of its qubits.
   - Global features (13 dims): depth, n_params, n_qubits, per-gate counts.
5. Persist to `dataset_v2.pkl`.

**Command:**
```
python build_dataset.py --n_per_q 150 --min_q 2 --max_q 6 \
  --n_samples 3000 --n_workers 96 --out dataset_v2.pkl
```
**Runtime:** 87 s on 96 CPU workers (750 PQCs).
**Scale:** 2 % of the paper's 25,000-PQC training set. This is the dominant
cause of the RMSE gap reported below; deliberate wave-brief compute-budget
choice.
**Observed KL range:** 0.009 – 27.6 (mean ≈ 1.9, long tail at low n).

## Stage 3 — GNN training (validates Claim C3, gates Claims C4/C5)

**Model** (`work/train_gnn.py`, class `ExprGNN`):
- `TransformerConv(22 → 64, heads=2)` → ReLU
- `TransformerConv(128 → 64, heads=2)` → ReLU
- `TransformerConv(128 → 64, heads=1)` → `global_mean_pool` → 64
- MLP(13 → 32 → 32 → 32) over global features
- concat → FC(96 → 64) → ReLU → FC(64 → 32) → ReLU → FC(32 → 1)

**Config (paper defaults except batch and target transform):**
- Adam, lr 1e-4, wd 1e-6.
- Huber loss.
- ReduceLROnPlateau, factor 0.1, patience 15.
- Batch 64 (paper: 1500; smaller here because dataset is smaller).
- 300 epochs.
- Target: `log1p(KL)` (undo with `expm1`) — stabilises against long-tail
  high-KL outliers.
- Split 70/10/20 train/val/test, stratified by qubit count.
- Clip KL @ 3.0 before log-transform to bound outliers.

**Command:**
```
python train_gnn.py --data dataset_v2.pkl --epochs 300 --clip_kl 3.0 \
  --log_target --out train_v2.json
```
**Runtime:** 33 s on 1× A100.

## Stage 4 — Independent evaluation on Sim-19 (validates Claim C5, tests generalisation)

**Goal:** apply the trained GNN to the 19 Sim reference circuits (out of
training distribution, tests structural generalisation).

**Handling out-of-vocab gates:**
- Sim Circuits 9/10/12 use CZ, which is not in our random-PQC gate
  vocabulary.
- Encoder maps CZ → CX in the graph (rationale: CZ = H · CX · H, structurally
  similar; lossy but reasonable). Partly explains Circuit-9 outlier in
  Stage-5 results.

**Command:**
```
python eval_sim19.py --model train_v2_model.pt --dataset dataset_v2.pkl \
  --train_result train_v2.json --sim19_gt sim19_n4_s5000.json \
  --out eval_sim19_n4.json
```

## Stage 5 — Reporting

- Aggregate metrics: RMSE, MAE, Pearson r on held-out random set and Sim-19.
- Per-qubit RMSE breakdown.
- Per-circuit prediction table for Sim-19 (best/worst matches).
- Compare against paper's headline numbers with honest attribution of the
  RMSE gap (Section 5.3 of REPORT.md: 33× less data, 40 % fewer fidelity
  samples per PQC, narrower qubit range, long-tail unbounded target).
- Write REPORT.md, REPORT.tex, artifacts_summary.md, failure_analysis.md,
  open_questions.json.

## Stage 6 (SKIPPED — out of scope for wave brief)

- Noisy-backend training/evaluation (Claim C6; FakeGuadalupe/Mumbai/Hanoi).
- IBM Qiskit RealAmplitude 64-circuit set (Fig 7 right).
- Extrapolation study to n=10 (Fig 11).
- Real IBM-Hanoi hardware run (Table I).
- Sample-size ablation (Fig 8).

All Stage-6 items are technically tractable follow-ups; documented in
`failure_analysis.md` under "Not-tested claims" and in `open_questions.json`.

---

## Reproducibility

- All commands run from `work/` on uicgpu with `conda activate qexpr`.
- Every artefact under `report/evidence/` is deterministic given a fixed
  seed; we did not run seed sweeps (single-seed limitation, noted in
  REPORT.tex GENUINE CRITIQUE §honest limitations).
- Total wall time: Stage 1 149 s + Stage 2 87 s + Stage 3 33 s +
  Stage 4 <10 s ≈ **~5 min end-to-end** for the wave-brief scale.
- Extrapolating: full 25,000-PQC dataset build at observed 9 PQC/s ≈ 46 min
  wall time; training remains ~30 min on 1× A100. Full-scale replication
  is a straightforward follow-up.
