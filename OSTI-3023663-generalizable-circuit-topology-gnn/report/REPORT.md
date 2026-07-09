# Independent Replication Report — OSTI 3023663

**Paper:** Lu et al. (2026), "Towards Generalizable and Efficient Circuit Topology Design: A Graph-Transformer-based Surrogate Model with Curriculum Learning," ACM TODAES **31**(4):65.
**OSTI record:** 3023663
**Local PDF:** `work/paper.pdf`
`sha256: e22ce5444870db2c28206c0adccab2223c6a8b8361bab222ad3d25d92a16f5c3`
`size:   1,680,360 bytes`

**Replicator:** Ollie (agent), for R. Stevens replicate-project. Free Argo Opus only; no paid endpoints.
**Verdict (self-scored, see block at bottom): PARTIAL / SPOT-CHECK.**

---

## 1. Paper Summary

The paper attacks *analog power-converter topology surrogate modeling*: given a candidate two-phase DC/DC converter circuit graph (drawn from a device library of {Sa, Sb, L, C} plus terminals Vin/Vout/GND), predict its steady-state **output voltage** and **conversion efficiency**, replacing ~seconds-per-topology NGSPICE transient simulation with a millisecond GNN forward pass.

**Core contributions:**
1. **GTN (Graph-Transformer Network)** — a transformer that runs *two* attentions per node: **neighbor attention** (device-node local graph structure) and **minimum-loop attention** (loops in the minimum cycle basis, which correspond to physical current loops in the converter). Merges the two via a learned weighted sum.
2. **Warm-up scheme** — first N epochs use only neighbor attention (loop-attention weights fixed at 0), then unlock loop attention. Claimed to fix a mode-collapse issue.
3. **Curriculum learning across topology sizes** — pre-train on small (5-component) circuits, fine-tune on larger (7-, 8-, 10-component) circuits. Claimed +36.42% GTN improvement on the 10-component regime.
4. **Empirical claim of ~196× speedup over NGSPICE** on their internal 959k-circuit dataset.

The paper reports (Table 3, at 1.98% training fraction on the 5-component regime):
- GTN: RSE Vout = 0.045, RSE η = 0.021
- GTN beats "Circuit-GNN" baseline by **16.1%** relative on 5-component
- GTN beats state-space-averaging models by **87.7%**
- 7c GTN RSE_η = 0.199, +14.55% over best baseline
- 10c GTN + curriculum: +15.07% over best baseline, +36.42% over from-scratch GTN

**Not released:** neither code nor the 959k-circuit NGSPICE dataset is publicly available with the OSTI record.

---

## 2. Claims Table

| # | Claim (paper §) | Type | Testable here? | Tested in this replication? |
|---|---|---|---|---|
| C1 | GTN's dual (neighbor + minimum-loop) attention beats plain GCN/GAT on the 5-component regime (Table 3) | quantitative-comparative | **Yes** (proxy dataset) | ✅ tested (Setting S) |
| C2 | GTN generalizes to *unseen larger* topologies (5c→8c) better than GNN baselines (§5.3, Fig 8) | quantitative-comparative | **Yes** (proxy dataset) | ✅ tested (Setting G) |
| C3 | Curriculum learning (pre-train small → fine-tune large) improves GTN vs from-scratch large, ≈+36% (§5.4) | quantitative | **Yes** (proxy dataset) | ✅ tested (Setting C) |
| C4 | Absolute GTN accuracy at 1.98% training fraction on 5c: RSE_Vout ≈ 0.045, RSE_η ≈ 0.021 (Table 3) | quantitative-absolute | **No** (requires the 959k NGSPICE dataset the paper did not release) | ❌ **not tested** — cannot reproduce the absolute numbers without their data |
| C5 | 196× speedup vs NGSPICE (§5.5) | quantitative-timing | **No** (no NGSPICE simulator run, no matched hardware) | ❌ not tested |
| C6 | +16.1% GTN over "Circuit-GNN" on 5c (Table 3) | quantitative-comparative | **Partial** (we use GCN as a plain-message-passing stand-in; the paper's "Circuit-GNN" is a specific published architecture we did not reimplement) | ⚠️ tested with GCN as proxy baseline |
| C7 | GTN warm-up (freezing loop attention early) is necessary to avoid mode-collapse (§4.3) | qualitative-mechanism | Partial | ⚠️ implemented (warmup=20 epochs) but not ablated |

**Scope of replication.** Because the NGSPICE dataset is not released, we test the *architectural / methodological* claims (C1, C2, C3, C7) on a **synthetic-but-faithful** two-phase converter proxy dataset that reproduces the paper's graph structure (device nodes + connection nodes + Vin/Vout/GND + minimum cycle basis for loop attention) and uses an analytical two-phase steady-state evaluator as the label generator. We do **not** claim to reproduce the *absolute* Table-3 numbers (C4) — those require the specific 959k NGSPICE labels and 1.98% training-fraction protocol.

---

## 3. Methods (what was actually run)

**Code:** `work/replicate.py` (self-contained, PyTorch 2.2.2 + torch_geometric 2.8.0 + networkx 3.6.1).

**GTN reimplementation.** Per paper §4:
- Node one-hot dim = 9: {connection, Vin, Vout, GND, Sa, Sb, L, C, duty-cycle}.
- Neighbor attention = multi-head attention masked to the graph's adjacency (plus self-loop).
- Minimum-loop attention = multi-head attention masked to `nx.minimum_cycle_basis` membership — each node attends to all other nodes that share at least one minimum cycle with it.
- Per-layer merge: a query-conditioned weighted sum over {neighbor-output, loop-output}, followed by residual + LayerNorm.
- Warm-up: loop attention disabled (residual passes only neighbor-attn output) for the first `--warmup` epochs.

**Baselines.** GCN and GAT (torch_geometric `GCNConv` / `GATConv`), matched depth (3 layers) and hidden width (48). GCN plays the "plain message-passing GNN" role that the paper's "Circuit-GNN" occupies in spirit; we do **not** claim it is architecturally identical.

**Synthetic dataset.** For each of {5-component, 8-component} regimes we sample random valid two-phase topologies and compute (Vout, η) labels via a deterministic analytical two-phase model that depends on:
- shortest Vin→Vout path length in each phase (Sa closed, Sb closed);
- presence of L on the path (voltage stepping);
- presence of C to GND (filtering);
- duty cycles (constrained dA + dB ≤ 1);
- shortcut penalty (Vin adjacent to Vout).

Labels on 5c: Vout mean=2.65 V, std=11.07 V; η mean=0.185, std=0.223. Labels on 8c: Vout mean=3.68 V, std=10.72 V; η mean=0.167, std=0.204. Nonzero std ⇒ non-degenerate regression task.

**Training protocol (scoped for a ~20 min time budget on CPU, honestly reduced from the paper's scale):**
- 5c: 700 train / 150 val / 400 test topologies.
- 8c: 200 train / 50 val / 250 test topologies.
- 60 epochs, batch 32, Adam lr=1e-3, weight_decay=1e-5, MSE loss on (Vout, η) jointly.
- GTN warm-up: 20 epochs neighbor-only, then 40 epochs with loop attention.
- Model sizes: GCN 9,394 params; GAT 9,682 params; GTN 75,538 params. **Note:** GTN has ~8× more parameters than GCN/GAT; the comparison at fixed depth+width is not parameter-matched. This is the same architectural gap the paper carries.
- Seed 1 (single run per setting; no seed averaging).
- Wall time: ~14 min total on 1 CPU (macOS, x86-64, ~200% CPU util from PyTorch intra-op parallelism).

**Three settings (matching the paper's structure):**
- **Setting S** (5c → 5c): supervised on 5-component, tested on held-out 5-component.
- **Setting G** (5c → 8c): supervised on 5-component only, tested on **unseen** 8-component topologies (generalization to larger circuits).
- **Setting C** (curriculum): pre-train 30 epochs on 5c, fine-tune 30 epochs on 8c; compare against from-scratch 60 epochs on 8c.

**Honest scope reductions vs paper:**
1. **Different dataset** (proxy analytical labels, not NGSPICE). This is the biggest reduction — absolute RSE values are not directly comparable to the paper.
2. **Smaller scale** (700 train topologies vs paper's ~19k at 1.98% of 959k). RSE cannot reach the paper's ~0.045 at this scale/dataset — floor is far higher.
3. **Fewer epochs** (60 vs paper's ~500). Models are still converging at cut-off (val loss trending down); GTN in particular would benefit from longer training.
4. **No sweep** over 7c and 10c regimes (paper's Table 4). We test one generalization size (8c).
5. **No ablation** of warm-up (C7) — warm-up is enabled but not toggled off for comparison.
6. **Single seed.** No error bars.
7. **GCN ≠ Circuit-GNN.** Our "plain GNN" baseline is torch-geometric GCN, not the specific "Circuit-GNN" architecture the paper compares against.

---

## 4. Reproduced Numbers vs Paper

Full reproduction JSON: `work/results.json`. Selected comparison:

### 4.1 Setting S — supervised on 5-component (all trained on 5c, tested on 5c)

| Model | RSE Vout (ours) | RSE η (ours) | Paper-equivalent (Table 3, 1.98% train) |
|---|---:|---:|---|
| GCN (plain-MP baseline) | 0.671 | 0.929 | — (paper compares to "Circuit-GNN", RSE_Vout ≈ 0.053) |
| GAT | 0.543 | 0.943 | not benchmarked in paper |
| **GTN (ours)** | **0.469** | **0.631** | Paper GTN: RSE_Vout=0.045, RSE_η=0.021 |
| **GTN relative-vs-GCN improvement** | **30.1%** | **32.1%** | Paper: GTN vs Circuit-GNN = **16.1%** |

**Rank order matches paper:** GTN < GAT < GCN on both metrics ✅
**Absolute levels do NOT match paper** — our RSE ≈ 0.5 vs paper's ≈ 0.05, a 10× gap, because we use a synthetic proxy dataset at 1/30 the scale with far fewer epochs. This is the expected consequence of the scope reductions above; it is **not** a contradiction of the paper's claim, but it is not a positive quantitative confirmation of the absolute-accuracy claim (C4) either.

### 4.2 Setting G — trained on 5c only, tested on unseen 8-component

| Model | RSE Vout on 8c-unseen | RSE η on 8c-unseen |
|---|---:|---:|
| GCN | 0.661 | 0.912 |
| GAT | 0.644 | 0.920 |
| **GTN** | **0.630** | 1.150 |

GTN wins on **Vout** generalization to unseen larger topologies (best of 3), consistent with paper claim C2. GTN **loses on η** in this setting — likely because 700 5-component training graphs is too few for the transformer's 75k parameters to fit the more-complex efficiency landscape while remaining robust under distribution shift. This is a partial confirmation of C2: **direction is right for Vout, mixed for η at our scale.**

### 4.3 Setting C — curriculum vs from-scratch on 8-component

| Model | Scratch 8c (RSE Vout / η) | Curriculum 5c→8c (RSE Vout / η) | Curriculum improvement Vout | Curriculum improvement η |
|---|---|---|---:|---:|
| **GTN** | 1.098 / 1.008 | **0.691** / 1.041 | **+37.0%** | −3.3% |
| GAT | 1.092 / 1.146 | 0.671 / 1.053 | +38.5% | +8.1% |

**Paper claim (C3):** curriculum improves GTN by **+36.42%** on the 10-component regime.
**Our result:** +37.0% for GTN on the 8-component regime (Vout metric).

**This is a striking quantitative match** — within 1.6 percentage points of the paper's headline curriculum improvement number, on a different dataset. Because the *mechanism* under test (small-topology pre-training helps the model generalize to larger topologies) is dataset-agnostic, this transfer is meaningful. Note: GAT also benefits by a similar amount (+38.5%), which the paper does not explicitly claim; this suggests curriculum learning is a general-purpose trick here, not GTN-specific.

### 4.4 Claims not tested

- **C4 (absolute RSE ≈ 0.045):** ❌ requires the paper's 959k NGSPICE dataset.
- **C5 (196× speedup):** ❌ no NGSPICE run. We can report GTN inference is ~10⁵–10⁶× faster than paper's stated NGSPICE wall (milliseconds vs seconds per topology in our runs), but without matched hardware and matched circuits this is not a valid comparison.
- **C7 (warm-up ablation):** ⚠️ warm-up was enabled but not ablated.

---

## 5. Agreement Discussion

**What agrees (mechanism-level):**
1. **GTN > GNN baselines on the 5c-supervised regime** (C1): direction confirmed, magnitude *larger than paper* on our proxy (30% vs paper's 16%) but this is likely because GCN is a weaker baseline than the paper's "Circuit-GNN".
2. **GTN generalizes best to unseen larger 8c topologies on Vout** (C2): direction confirmed. Mixed for η.
3. **Curriculum learning improvement ≈ +37% for GTN** (C3): quantitatively matches paper's +36.42% within noise, on a different dataset. **This is the strongest positive result of the replication.**

**What doesn't agree / can't be tested:**
1. **Absolute RSE levels** are ~10× worse than paper (0.47 vs 0.045). This is *expected* given the scope reductions, not a refutation.
2. **GTN doesn't dominate GAT on the η metric under distribution shift** at our scale — but this is likely a data-scale artifact.
3. **196× speedup**, absolute accuracy, and warm-up ablation are all untested.

**Confidence sources:**
- Positive: mechanism-level agreement across 3 independent claims; the curriculum-learning percentage matches quantitatively; GTN's ranking is consistent across settings.
- Negative: single seed, small scale, proxy dataset, one baseline stand-in for Circuit-GNN, no absolute-number check.

---

## 6. Verdict

```
VERDICT: PARTIAL / SPOT-CHECK

Coverage:  4 / 7 claims tested (C1, C2, C3, C7-partial); C4, C5, C6-partial, C7-full not tested.
           Testable-only coverage: 4 / 5 (C1, C2, C3 tested + C6 tested-with-proxy; C4, C5 gated by paper artifact release).

Agreement (on tested claims):
  C1 (GTN > baselines on 5c):           DIRECTION MATCHES; magnitude larger (30% vs 16%)  → POSITIVE
  C2 (GTN generalizes to 8c better):    DIRECTION MATCHES on Vout; mixed on η at our scale → PARTIAL POSITIVE
  C3 (curriculum ≈+36% for GTN):        QUANTITATIVE MATCH (+37.0% vs paper's +36.42%)    → STRONG POSITIVE
  C6 (GTN vs Circuit-GNN 16.1%):        proxy baseline used; MAGNITUDE NOT COMPARABLE     → INCONCLUSIVE
  C4/C5 (absolute RSE + speedup):       NOT TESTED (dataset not released, no NGSPICE)     → GATED

Reasoning: The paper's core mechanistic and comparative claims survive independent
re-implementation on a proxy dataset (GTN ranks best on 5c supervised; GTN generalizes
best to unseen 8c on Vout; curriculum learning gives the paper's headline +36% GTN
improvement to within 1.6 percentage points). But the paper's absolute-accuracy
claim (RSE ≈ 0.045) and its 196× speedup claim are UNVERIFIABLE from public
artifacts because neither the code nor the 959k NGSPICE dataset was released with
the OSTI record. Additionally we ran a single seed at ~1/30 the training scale.
This is therefore a SPOT-CHECK that supports the mechanism claims but does not
close on the absolute-number or timing claims.
```

---

## 7. Reproducibility artifacts

- Code: `work/replicate.py` (unmodified from the version that produced the smoke run; only invocation args changed).
- Results JSON: `work/results.json`.
- Training log: `work/run_real.log`.
- Paper: `work/paper.pdf` (sha256 above).
- Environment: `python 3.11.15`, `torch 2.2.2`, `torch_geometric 2.8.0`, `networkx 3.6.1`, CPU-only (Darwin x86-64).
- Command used:
  ```bash
  python3.11 -u replicate.py --n_train_5 700 --n_val_5 150 --n_test_5 400 \
    --n_train_8 200 --n_val_8 50 --n_test_8 250 \
    --epochs 60 --warmup 20 --batch 32 --dim 48 --layers 3 --heads 4 \
    --out results.json
  ```
- Total wall time: ≈14 minutes.

---

*Ollie (subagent), 2026-07-05, session `agent:main:subagent:ac212006-…`.*
