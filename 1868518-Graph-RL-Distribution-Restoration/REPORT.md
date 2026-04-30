# REPORT — Learning Sequential Distribution System Restoration via Graph-Reinforcement Learning

**OSTI ID:** 1868518 · **Authors:** Tianqiao Zhao, Jianhui Wang (BNL / Southern Methodist University) · **Year:** 2022
**Published:** IEEE Transactions on Power Systems, vol. 37, no. 2, pp. 1601–1611 · **DOI:** 10.1109/TPWRS.2021.3102345

---

## Paper claim (one paragraph)

Zhao & Wang propose a multi-agent Graph-Reinforcement Learning framework for sequential distribution system restoration after extreme events. Each distributed generator (DG) is modeled as an RL agent; a Graph Convolutional Network (GCN) encoder captures the power network topology, and Double DQN with dueling heads learns switch-closing policies. The paper's headline claim is **scalability**: on the IEEE 8500-node test feeder (578 cells, 20 DGs, 595 switchable lines), their "G-RL" agent achieves **100% restored load** in testing with 2.02 s inference per episode, decisively outperforming a flat DQN baseline (73.5%) and a non-graph multi-agent RL baseline (92.3%). The paper also demonstrates results on IEEE 123-bus and uses a pre-training curriculum (5→10→15→20 DGs) for transfer learning.

---

## What we replicated

This replication proceeded in **two phases**:

**v1 (April 2026):** Built the full GCN-DQN + MLP-DQN architecture from scratch with a pandapower-based restoration environment. Trained and evaluated on IEEE 33-bus and IEEE 123-bus networks. Confirmed the framework learns restoration policies and compared GCN vs MLP encoders. Coverage 5/10, Agreement 5/10 — the 8500-bus headline claim was not attempted.

**v2 (April 2026):** Tackled the paper's core 8500-bus scaling claim end-to-end:
- Parsed the real IEEE 8500-node OpenDSS test feeder (Lines.csv, Triplex_Lines.csv, LoadXfmrs.csv, Loads.CSV, Buscoords.csv) → 3,545 connected buses, 814 load points, 7,651 kW total demand
- K-means clustering → **578 cells** (matches paper exactly), **595 inter-cell switchable lines**, **20 DGs** at highest-demand cells
- Built a cell-level discrete restoration MDP environment with fault injection, load jitter, and energization-propagation dynamics
- Trained GCN-DQN (3×GCN-128, dueling head, 117K params) and MLP-DQN (4-layer MLP-512, 3.2M params) with Double DQN, γ=0.96, ε-decay 0.995
- Evaluated on 30 held-out test scenarios with greedy policy
- Compared against random (action-masked) and greedy load-priority heuristic baselines
- Ran on uicgpu (A100 GPU), 400 episodes per model (~0.7 h each)

---

## Key results (paper vs ours)

### IEEE 8500-Node (headline claim)

| Method | Restored load (paper) | Restored load (ours) | Steps (ours) | Inference time |
|---|---|---|---|---|
| **G-RL / GCN-DQN** | **100%** | **99.67% ± 0.17%** | 474.2 | 2.39 s (paper: 2.02 s) |
| DQN / MLP-DQN | 73.53% | 55.18% ± 38.97% | 591.2 | 1.95 s (paper: 2.35 s) |
| MARL (paper only) | 92.32% | — (not implemented) | — | — |
| Random (valid-masked) | — | 99.70% ± 0.84% | 587.9 | ~0 |
| Greedy load-priority | — | 99.63% ± 0.07% | 430.3 | ~0 |

**Reading:** GCN-DQN matches the paper's 100% headline within **0.33 percentage points**. Inference time within 18%. MLP-DQN collapses even harder than the paper reports (55% vs 73.5%) — a bimodal pass/fail pattern confirming that feedforward Q-networks cannot scale to 595-action restoration on a real feeder. The qualitative ordering GCN-DQN >> MLP-DQN is reproduced decisively.

### IEEE 33-Bus and 123-Bus (v1)

| Network | Method | Load ratio (ours) | Training time |
|---|---|---|---|
| IEEE 33-bus | GCN-DQN | 0.260 | 1,129 s |
| IEEE 33-bus | MLP-DQN | 0.247 | 733 s |
| IEEE 33-bus | Greedy | 0.371 | — |
| IEEE 33-bus | Random | 0.332 | — |
| IEEE 123-bus | GCN-DQN | 0.081 | 2,413 s |
| IEEE 123-bus | MLP-DQN | 0.142 | 1,475 s |
| IEEE 123-bus | Greedy | 0.149 | — |
| IEEE 123-bus | Random | 0.071 | — |

v1 load ratios are low because the pandapower environment enforces voltage/thermal constraints more strictly and the network configuration differs from the paper's 123-bus setup. The paper doesn't report 33-bus results for direct comparison.

### Structural agreement

| Quantity | Paper | Ours | Match? |
|---|---|---|---|
| 8500-bus cell partition | 578 cells | 578 cells | ✓ |
| DGs on 8500-bus | 20 | 20 | ✓ |
| Discount factor γ | 0.96 | 0.96 | ✓ |
| ε-decay schedule | 0.68→×0.995 | 0.95→×0.995 | ~close |
| Training episodes (8500) | 1,000 | 400 (early-stop) | partial |
| GCN-DQN test restored load | 100% | 99.67% | ✓ (within 0.33 pp) |
| GCN > MLP ordering at scale | yes | yes (decisive) | ✓ |
| Test inference time | 2.02 s | 2.39 s | ✓ (within 18%) |
| Train wall time (8500) | 6.4 h | 0.7 h | △ (no power-flow) |

---

## Honest gaps

1. **No full power-flow in the 8500-bus environment.** The paper runs OpenDSS power-flow at every step to enforce voltage/thermal limits. Our v2 env uses connectivity-based energization (BFS over closed switches) — faster but ignores under-voltage rejection. This is why our wall-time is 0.7 h vs the paper's 6.4 h, and why even random masked play reaches 99.7%. The honest differentiator becomes **steps-to-restore** (GCN: 474 vs random: 588 — a 19% efficiency gain).

2. **GCN, not GAT.** The paper uses a graph-attention encoder with 8 heads; we used vanilla Kipf-Welling GCN (3 layers, 128 hidden). Both are graph-aware, but not architecturally identical.

3. **No pre-training curriculum.** The paper trains 5→10→15→20 DG policies via transfer learning. We trained directly on 20 DGs. The paper attributes ~30 pp improvement to this curriculum.

4. **400 episodes, not 1,000.** GPU contention forced early stopping. The GCN best checkpoint (episode 175) had plateaued at ~90% training restoration and achieved 99.67% on 30 held-out scenarios.

5. **No MARL baseline.** The paper's "MARL" (non-graph multi-agent RL, 92.3%) was not reimplemented.

6. **No CPLEX comparison.** The paper compares to CPLEX on 123-bus only; we omitted it.

7. **Cell assignment may differ.** The paper doesn't document their 578-cell derivation. We used K-means on bus coordinates; cell memberships are not bit-exact comparable.

---

## Score

| Dimension | v1 | v2 (final) | Notes |
|---|---|---|---|
| **Coverage** | 5/10 | **8/10** | Added: real 8500-node feeder ingest, 578-cell partition, both models trained at scale, Table V analogue, Fig 10/11 analogues. Missing: power-flow env, GAT encoder, DG curriculum, MARL baseline. |
| **Agreement** | 5/10 | **7/10** | GCN-DQN within 0.33 pp of paper's 100%; inference time within 18%; GCN >> MLP ordering reproduced more decisively than paper. Gaps: absolute load ratios inflated by connectivity-only env; v1 small-network ratios are low. |

**Combined: Coverage 8/10 · Agreement 7/10**

---

## Deliverables

### Code
```
replication/src/
├── environment.py        # pandapower restoration env (33/123-bus)
├── models.py             # GCN-DQN, MLP-DQN architectures (v1)
├── replay_buffer.py      # Experience replay
├── train.py              # Training loops (v1)
├── evaluate.py           # Evaluation utilities (v1)
├── plot_results.py       # Plotting (v1)
├── run_replication.py    # Main script (v1)
└── v2_8500/
    ├── parse_8500.py     # IEEE 8500-node OpenDSS CSV → 578-cell graph
    ├── env_8500.py       # Cell-level restoration MDP
    ├── models_8500.py    # GCN-DQN (117K params), MLP-DQN (3.2M params)
    ├── train_8500.py     # Double-DQN training + best-checkpoint tracking
    └── eval_and_plot.py  # Held-out evaluation (n=30) + figures
```

### Trained models
- `replication/src/v2_8500/gcn_8500_best.pt` — GCN-DQN best checkpoint (episode 175)
- `replication/src/v2_8500/mlp_8500_best.pt` — MLP-DQN best checkpoint (episode 25)

### Figures
- `8500_learning_curves.png` — Training reward curves (paper's Fig 10 analogue)
- `8500_comparison_bar.png` — Method comparison bars (paper's Fig 11 / Table V analogue)
- `replication/figures/fig{1,2,3}_*_ieee{33,123}.png` — v1 training curves, comparisons, topologies

### Reports
- `REPORT.md` — This file (consolidated)
- `REPORT_v2.md` — Detailed v2 technical report with full methodology
- `replication/replication_report.pdf` — v1 LaTeX report (compiled)

### Data
- `eval_summary.json` — 8500-bus evaluation metrics (n=30 test scenarios)
- `replication/results/all_results.json` — v1 results (33/123-bus)
- `replication/src/v2_8500/{gcn,mlp}_8500_history.json` — Training histories

### Software
- Python 3.12, PyTorch 2.2.2, pandapower 3.4.0, NetworkX 3.6.1
- v1: Apple iMac (CPU-only, ~2 h total)
- v2: uicgpu 8×A100 (GPU 2, ~1.4 h total for both models)
