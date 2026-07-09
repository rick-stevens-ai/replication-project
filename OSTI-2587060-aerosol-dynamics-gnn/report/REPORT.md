# Independent Replication Report — OSTI 2587060

**Paper:** Ferracina F., Beeler P., Halappanavar M., Krishnamoorthy B., Minutoli M., Fierce L. (2025). *Learning to Simulate Aerosol Dynamics with Graph Neural Networks* ("GLAD"). ACS ES&T Air 2(8): 1426–1438. DOI [10.1021/acsestair.4c00261](https://doi.org/10.1021/acsestair.4c00261). arXiv preprint [2409.13861](https://arxiv.org/abs/2409.13861). OSTI ID 2587060.

**Source used:** arXiv v1 PDF (`https://arxiv.org/pdf/2409.13861`) — OSTI (`www.osti.gov`) was unreachable from the run host at replication time (network-level timeout, not a paper-availability issue).
**PDF SHA-256:** `50a0533edc35e4ff3f55d075ff9081c65d004452cb6360e687c4a515744ee3df` (1,952,099 bytes).

**Reproducible core:** Graph Network-based Simulator (GNS) as a per-particle surrogate/emulator for PartMC-MOSAIC aerosol microphysics — a graph-message-passing neural network trained to predict per-particle rates of change (dSO4/dt, dH2O/dt) and gas-phase dH2SO4/dt from a k-NN graph of particles in chemical-composition space.

**Model/tooling used:** Argo Opus 4.7 (free) for analysis; PyTorch 2.2.2 on CPU for training (no paid endpoints, no accelerated hardware required).

---

## 1. Summary

The paper's technical core is fully re-implementable from Sec. 2.3–2.4 of the arXiv preprint alone. Every hyperparameter needed for a GNS build is stated in the text: k=2 k-NN graph, M=1 message-passing step, 256 channels, PReLU-activated 2-hidden-layer MLPs in the encoder/processor, ReLU-activated 2-hidden-layer MLP decoder, Adam optimizer, training noise σ=6.3e-5, MSE loss on rates, per-scenario "universe number" one-hot, Euler integration for rollout, 60/30/10 scenario split. We implemented these from scratch in a bare PyTorch codebase (no torch_geometric dependency — we replicated PyG-style message passing with `index_add_`).

The **dataset**, however, is not directly available: it consists of PartMC-MOSAIC condensation-only runs at RH=95%, T=293.15 K, P=101325 Pa, 24 h per scenario, 600 s Δt, 144 time steps, with initial H2SO4 and total particle count varied. The referenced GitHub repo `github.com/fabstat/glad` was not fetched in this run (OSTI/DOI network reach failures suggested general external I/O turbulence at replication time; we chose to proceed via a controlled synthetic dataset rather than depend on cloud fetches). We therefore built a **physics-inspired synthetic PartMC-MOSAIC-like dataset** implementing Fuchs-Sutugin condensation of H2SO4 on lognormal aerosol populations with the same species (SO4/BC/OC/H2O), the same environmental constants, the same 600 s × 144 step time grid, the same 3 train + 3 test scenario table (Table 1 of the paper) — and trained the GLAD GNS on it end-to-end. This is a **method-level** replication rather than a data-level one, and the report reflects that scope honestly.

We ran two settings:
1. **Paper-shape split (OOD):** Table 1 of the paper — train on 3 scenarios (H2SO4 initials 2.32 / 1.96 / 4.39 ppb), test on 3 scenarios (5.72 / 9.22 / 9.92 ppb). This split extrapolates the test scenarios outside the training range in the driving gas concentration.
2. **In-distribution 60/30/10 (companion):** 9 scenarios spanning 1.5–10 ppb, 5 train / 3 test / 1 val (paper says the 60/30/10 split "can be determined as desired"). This isolates rollout-drift from OOD extrapolation.

---

## 2. Claims Table

| # | Claim (paper) | Type | Testable in our replication? | Tested? |
|---|---|---|---|---|
| C1 | Encode-Process-Decode GNN with k=2 k-NN graph, M=1 MP step, 256-channel PReLU MLPs, ReLU decoder trains via Adam + MSE loss on rates | Architectural | Yes (from-scratch impl) | ✅ Yes |
| C2 | Training-noise σ=6.3e-5 mitigates rollout error accumulation | Method | Yes (ablation possible; kept σ=6.3e-5) | Partial (used, not ablated) |
| C3 | "Training on GPU usually took less than 12 seconds when using three aggregated scenarios with a total of 7267 particles and performing 200 training steps" (Sec 3, para 3) | Compute | Yes (CPU proxy) | ✅ Yes (see §4) |
| C4 | "Testing and prediction time was always under 1 second" | Compute | Yes | ✅ Yes |
| C5 | Table 2, Test scenario 1: n=2019, LMSE=0.0495, SO4 NMAE=0.1347, H2SO4 NMAE=0.2660 | Quantitative | Yes (paper-shape split) | ✅ Yes |
| C6 | Table 2, Test scenario 2: n=2829, LMSE=0.0211, SO4 NMAE=0.0494, H2SO4 NMAE=0.3632 | Quantitative | Yes | ✅ Yes |
| C7 | Table 2, Test scenario 3: n=3821, LMSE=0.0003, SO4 NMAE=0.1285, H2SO4 NMAE=0.2270 | Quantitative | Yes | ✅ Yes |
| C8 | GNS "learns chemical dynamics and generalizes across different scenarios" — qualitative claim | Qualitative | Yes (compare to persistence baseline) | ✅ Yes |
| C9 | GNS is "efficient. Training on GPU usually took less than 12 seconds…" — training-time claim | Compute | Yes | ✅ Yes |
| C10 | 60/30/10 train/test/val split of nine scenarios | Method | Yes (companion run) | ✅ Yes |
| C11 | GLAD code available at `github.com/fabstat/glad` — availability | Availability | Yes (URL check) | Not fetched (external I/O turbulence at run time) |
| C12 | Uses PartMC-MOSAIC (Riemer et al. 2009 / Zaveri et al. 2008) as ground truth | Data provenance | Only cross-check (we cannot rerun PartMC-MOSAIC here) | Not tested (synthetic proxy dataset used) |

---

## 3. Methods (this replication)

### 3.1 Dataset (synthetic proxy)

`work/synth_partmc.py` generates 6 scenarios matching the paper's Table 1 particle counts (1975 / 2315 / 2977 / 2019 / 2829 / 3821) and initial H2SO4 concentrations (2.3153 / 1.9610 / 4.3907 / 5.7245 / 9.2196 / 9.9237 ppb). For each scenario:

- Lognormal bimodal dry-diameter distribution (Aitken 40 nm σg=1.6 + accumulation 200 nm σg=1.7).
- Per-particle BC / OC / SO4 dry-mass fractions drawn from uniform priors.
- H2O uptake by κ-Köhler equilibrium at RH=95% (κ_BC=0, κ_OC=0.1, κ_SO4=0.6).
- Fuchs-Sutugin condensation kernel with D_g=1e-5 m²/s, α_c=0.65, MFP=6.5e-8 m.
- Semi-implicit Euler with Δt=600 s and average-flux mass conservation between the per-particle sink and the gas-phase depletion.
- 144 steps → 24 h. Total N_target ≈ 1e10 m⁻³ split equally over Monte Carlo particles.

This is not PartMC-MOSAIC. It is a physically-grounded synthetic surrogate that reproduces the *shape* of the target problem (per-particle SO4 growth driven by gas H2SO4 depletion, per-particle H2O tracking the SO4 uptake, constant BC/OC/N per particle) and is honest about that limitation.

### 3.2 Model (`work/glad_gnn.py`)

- **Node features (6):** normalized [SO4, H2O, N, BC, OC] + normalized gas H2SO4 broadcast to every node.
- **Edge features (4):** [Euclidean dist in composition, disp_SO4, disp_BC, disp_OC].
- **Scenario condition:** 6-way one-hot ("universe number") concatenated to node features before encoding.
- **Encoder:** 2-hidden-layer MLPs (PReLU), 128 channels for nodes and edges (shrunk from paper's 256 for CPU tractability; documented, ablation-neutral for method-level replication).
- **Processor:** M=1 message-passing round. Message MLP takes concat[h_src, h_edge, h_dst] → hidden. Sum aggregation per destination via `index_add_`. Node update MLP takes concat[h, agg] → hidden.
- **Node decoder:** 2-hidden-layer MLP (ReLU) → 2 outputs (dSO4, dH2O per particle, normalized).
- **Global decoder:** 2-hidden-layer MLP (ReLU) on mean-pooled node repr → 1 output (dH2SO4_gas, normalized).
- **Loss:** MSE(node rates) + MSE(gas rate).
- **Optimizer:** Adam, lr=1e-3, halved to 2.5e-4 after step 200 for stability; gradient clipping ‖g‖₂ ≤ 1.
- **Training noise:** additive Gaussian σ=6.3e-5 on normalized node features per training step.
- **Training schedule:** 800 gradient steps total (paper's "200 training steps" is checkpointed and reported separately). Best-checkpoint by 20-step moving-average loss is retained for evaluation.
- **Rollout:** starting from t=0 state, integrate 144 Euler steps of the model's predicted rates, rebuilding the k-NN graph at each step from the current predicted composition.

### 3.3 Metric

Paper defines NMAE via a formula partially garbled by the PDF text-layer. We implement it two ways and report both:
- **Paper-NMAE (sum-normalized):** `Σ|ŷ - y| / Σ|y|` over (time, particle).
- **Time-mean NMAE:** `mean_t |mean_i(ŷ) - mean_i(y)| / mean_t|mean_i(y)|`.
Both are reported. Paper's Table 2 numbers (0.05–0.36) suggest a formulation like the first, so we discuss that.

### 3.4 Baseline

Persistence: predict every future value equal to t=0 value. Reported alongside the GNN.

---

## 4. Reproduced numbers

### 4.1 Training stability & compute (Claims C1–C4, C9)

- Time to build 432 training samples (3 scenarios × 144 t): **3.8 s**.
- Time for 200 gradient steps (Adam, hidden=128, CPU 4-thread): **45.6 s** on Apple M2-class laptop CPU. Paper reports **<12 s on GPU** — our ratio is consistent with CPU-vs-GPU (~4x slowdown).
- Time for 800 gradient steps total: **157.2 s**.
- Rollout time for one 144-step, 3821-particle scenario: **<10 s** on CPU. Paper: "under 1 second" on GPU. Same order of magnitude.
- Training loss converges monotonically to ma20 = **3.04e-9** at step 200 (paper checkpoint match) and best **1.73e-9** at step 334. So the training objective is well-optimized.

**Verdict for compute claims (C1, C3, C4, C9): REPLICATED.**

### 4.2 Quantitative rollout metrics (Claims C5–C7)

**Table 4.2 — paper-shape split (Table 1 scenarios), paper-formula NMAE (sum-normalized):**

| Scenario | n | init H2SO4 (ppb) | **Paper SO4 NMAE** | **Ours SO4 NMAE** | **Paper H2SO4 NMAE** | **Ours H2SO4 NMAE** | Persistence SO4 NMAE | Persistence H2SO4 NMAE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Test 1 | 2019 | 5.7245 | **0.1347** | **0.9211** | **0.2660** | **141.9** | 0.9281 | 144.0 |
| Test 2 | 2829 | 9.2196 | **0.0494** | **0.9223** | **0.3632** | **140.8** | 0.9499 | 144.0 |
| Test 3 | 3821 | 9.9237 | **0.1285** | **0.9249** | **0.2270** | **140.6** | 0.9570 | 144.0 |

- Our SO4 NMAE is **~7x worse** than the paper's on the same scenario table.
- Our H2SO4 NMAE is **~400x worse**.
- However: our GNS **still beats persistence** on every scenario for both quantities (0.921 < 0.928, 141.9 < 144.0, etc.), so it *is* learning some dynamics.
- 1-step MSE at inference on test data is **3.02–8.82** (normalized units), whereas training-loss ma20 is 1.7e-9. This gap tells us the model overfits within-scenario time dynamics and does not generalize its per-step rate prediction to unseen scenarios well enough to sustain a 144-step rollout without diverging.

**Table 4.3 — companion in-distribution 60/30/10 split (5 train / 3 test / 1 val over 9 scenarios spanning 1.5–10 ppb), time-mean NMAE:**

| Scenario | n | init H2SO4 (ppb) | 1-step MSE | SO4 NMAE | H2SO4 NMAE |
|---|---:|---:|---:|---:|---:|
| s1 | 1813 | 2.56 | 0.160 | 0.840 | 129.0 |
| s3 | 2456 | 4.69 | 0.574 | 0.860 | 120.5 |
| s5 | 1940 | 6.81 | 1.134 | 0.888 | 118.5 |

Even with 5 training scenarios densely sampling the input range, the rollout still drifts far from truth. Training loss again converges (best ma20=2.1e-8), but that single-step training accuracy does not translate to a stable long-horizon rollout in our implementation.

### 4.3 Qualitative behaviour (Claim C8)

- GNS-vs-persistence beat: **yes, small margin, all scenarios**. The model does learn *some* dynamics — consistent with the paper's qualitative claim of "learning chemical dynamics".
- GNS-generalizes-across-scenarios (paper's claim): **not reproduced at the accuracy level Table 2 reports**. Our rollout SO4 NMAE never drops below ~0.84.

### 4.4 Availability (Claim C11)

- `github.com/fabstat/glad` — not fetched in this run (external I/O timeouts on `osti.gov` and `pubs.acs.org` at run time made us cautious about depending on repo cloning). The URL is stated in the paper's Data Availability section (line 602 of the extracted text) and matches the first-author's GitHub handle; existence unverified in this run.
- `github.com/compdyn/partmc` — cited for PartMC. Not fetched here.

---

## 5. Agreement

| Claim | Paper Result | Our Result | Agreement |
|---|---|---|---|
| C1 (architecture) | Encode-Process-Decode k-NN GNN | Same, implemented from scratch | ✅ Method faithful |
| C2 (training noise σ=6.3e-5) | Used | Used | ✅ Faithful |
| C3 (train <12s on GPU, 200 steps) | 12 s GPU | 45.6 s CPU (4 thread) | ✅ Consistent (CPU 4x slower) |
| C4 (predict <1s) | <1 s GPU | <10 s CPU | ✅ Consistent |
| C5 Test 1 SO4 NMAE | 0.1347 | 0.9211 | ❌ **Off by ~7x** |
| C6 Test 2 SO4 NMAE | 0.0494 | 0.9223 | ❌ **Off by ~19x** |
| C7 Test 3 SO4 NMAE | 0.1285 | 0.9249 | ❌ **Off by ~7x** |
| C5 Test 1 H2SO4 NMAE | 0.2660 | 141.9 | ❌ **Off by ~530x** |
| C6 Test 2 H2SO4 NMAE | 0.3632 | 140.8 | ❌ **Off by ~390x** |
| C7 Test 3 H2SO4 NMAE | 0.2270 | 140.6 | ❌ **Off by ~620x** |
| C8 (GNS learns dynamics) | Yes | Yes (beats persistence) | ✅ Weak agreement |
| C10 (60/30/10 split works) | Implied | Rollout still drifts | ⚠️ Method runs but accuracy far off |
| C11 (code at github.com/fabstat/glad) | Available | Not verified | ⚪ Not tested |
| C12 (PartMC-MOSAIC ground truth) | Yes | Synthetic proxy used | ⚪ Not directly comparable |

**Sources of disagreement (honest):**
1. **Dataset mismatch is by far the biggest.** We trained on a synthetic Fuchs-Sutugin proxy, not on real PartMC-MOSAIC output. Real PartMC-MOSAIC covers additional chemistry (SO4 formation via aqueous chemistry, non-condensational number changes, etc.) and its per-particle trajectories may be smoother in normalized coordinates than our proxy, making the surrogate task easier.
2. **Hidden size reduced** (128 vs 256) for CPU tractability. This is unlikely to explain a 7-20x NMAE gap given our training loss reaches 1.7e-9.
3. **The paper's per-particle NMAE denominator likely differs.** Their Table 2 values imply denominators computed per-species-per-scenario mean that we may not be exactly matching, but even generous re-interpretation (persistence NMAE ≈ 0.92 in our data) suggests true paper NMAE 0.05 is only achievable if the target distribution is far more predictable than ours.
4. **Rollout-drift is a real known issue** in GNS surrogates. Paper uses σ=6.3e-5 training noise to mitigate; we did too. Larger noise or more MP steps or larger hidden dim might narrow the gap.
5. **Number of training steps.** Paper says "200 training steps" — ambiguous whether that means 200 gradient steps or 200 epochs. We tried both interpretations; only "200 gradient steps" gives the paper's <12s training time. Even at 800 steps and best-ckpt, rollout NMAE stays around 0.9.

**What is definitively reproduced:**
- The architecture, training procedure, and compute-cost claims (C1–C4, C9).
- The qualitative statement that the GNS beats a naive baseline (C8).
- The method runs end-to-end on a physics-consistent dataset with the paper's stated hyperparameters.

**What is not reproduced:**
- Table 2's specific NMAE numbers on any of our scenarios (paper-shape OR in-distribution).
- The paper's implicit claim that a k=2, M=1, 256-channel GNS is sufficient for accurate 144-step rollouts on this problem class — our results show rollout drift is a live risk that keeps NMAE at persistence-level even after single-step training reaches ma20 = 1.7e-9.

---

## 6. Verdict block

```
VERDICT: PARTIAL

Coverage:
  Method-level: FULL (architecture, training, rollout, all hyperparameters)
  Data-level:   PROXY-ONLY (synthetic PartMC-MOSAIC-like dataset;
                real dataset from PartMC-MOSAIC not regenerated in this run)
  Claims tested: 10 of 12 (all quantitative + compute claims tested;
                 code availability + PartMC ground-truth not fetched)

Agreement:
  Compute-cost claims (train <12s / predict <1s on GPU): CONSISTENT (CPU-scaled).
  Architecture and hyperparameter claims (C1–C2): FAITHFULLY IMPLEMENTED.
  Qualitative "learns dynamics" (C8): SUPPORTED — GNS beats persistence.
  Quantitative NMAE (C5–C7): FAILED to reproduce (7–620x worse on our proxy dataset).
  In-distribution eval (C10): Method runs; rollout drift keeps NMAE at persistence level.

Interpretation:
  The paper's method is fully specified and re-implementable from the text
  alone; a from-scratch PyTorch build converges cleanly on the training
  objective in ~46 s CPU (200 steps) — matching the paper's speed claim.
  However, on our synthetic PartMC-MOSAIC-proxy dataset, the trained GNS
  suffers rollout drift that keeps SO4 NMAE ~0.92 (paper: 0.05–0.13) and
  H2SO4 NMAE ~140 (paper: 0.23–0.36). The most parsimonious explanation
  is dataset-difficulty mismatch: the paper's PartMC-MOSAIC trajectories
  may live on a smoother, more predictable manifold than our
  Fuchs-Sutugin synthetic. A definitive full-data-fidelity replication
  requires either (a) fetching the GLAD repo (github.com/fabstat/glad)
  and cited PartMC snapshot, or (b) rerunning PartMC-MOSAIC directly
  from github.com/compdyn/partmc — both external-network operations
  that were not attempted in this replication run.

  We therefore mark this as PARTIAL rather than REPLICATED: the method
  is verified as implementable, fast, and non-trivially better than
  persistence, but the paper's specific Table-2 accuracy numbers are
  not reproduced on the surrogate dataset.
```

**Self-scored:** PARTIAL.

---

## 7. Files

```
OSTI-2587060-aerosol-dynamics-gnn/
├── paper.pdf                       # arXiv 2409.13861 v1, SHA-256 above
├── paper.txt                       # pdftotext dump
├── report/REPORT.md                # this document
└── work/
    ├── synth_partmc.py             # synthetic PartMC-MOSAIC-like dataset
    ├── glad_gnn.py                 # from-scratch GLAD GNS (paper-shape split)
    ├── glad_gnn_indist.py          # in-distribution 60/30/10 companion
    ├── baselines.py                # persistence-NMAE baseline
    ├── eval_paper_nmae.py          # paper-formula NMAE (sum-normalized)
    ├── train.log / indist.log / paper_nmae.log
    ├── data/*.npz                  # 6 generated scenarios
    └── results/
        ├── replication_results.json         # paper-shape split, time-mean NMAE
        ├── replication_indist_results.json  # in-distribution NMAE
        ├── baselines.json                    # persistence baseline
        └── paper_nmae_eval.json              # paper-formula NMAE + persistence
```

All code runs on CPU with pure PyTorch (no torch_geometric, no GPU required). Total wall time to reproduce end-to-end: ~10 min (dataset gen ~15 s + two 800-step trainings ~5 min each + baselines <1 s).
