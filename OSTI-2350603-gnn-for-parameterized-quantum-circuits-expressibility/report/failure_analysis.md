# Failure Analysis — OSTI 2350603

**Paper:** Aktar, Bärtschi, Oyen, Eidenbenz, Badawy (2024). GNN for PQC
Expressibility Estimation.
**Verdict:** PARTIAL — qualitative claims replicate; the paper's headline
absolute-RMSE numbers do not, at our compute-budget scale.

This file itemises **where the replication fell short**, why, and what
would be required to close each gap. It is deliberately separated from
REPORT.md to make the failure surface easy to audit.

---

## 1. Quantitative miss on headline RMSE (Claims C4, C5)

**Paper:** RMSE 0.05 on held-out noiseless random PQCs (C4); RMSE 0.05 on
19 Sim reference circuits at n=4, three layer counts (C5).

**This replication:** RMSE **0.53** held-out; RMSE **0.29** on Sim-19
(single-layer). 6–10× worse than paper.

**Attribution (in order of estimated contribution, non-exclusive):**

1. **Training-data scale gap: 33×.** We trained on 750 PQCs; paper trained
   on 25,000 PQCs. This is the dominant single factor. GNN regression on
   scalar physics targets is well-known to be data-hungry, and the paper's
   scaling is far above the empirical convergence knee for this class of
   architecture.
2. **Fidelity samples per PQC gap: 40 % fewer.** Paper uses 5000 samples
   per PQC as the training target (Section III-A of paper); some evidence
   the paper's dataset construction may effectively use fewer per-PQC
   samples in practice. Our targets carry higher noise, which propagates
   into higher irreducible test loss.
3. **Narrower qubit range: n ≤ 6 vs n ≤ 8 (+ extrapolation to 10).** The
   Hilbert-space dimension N = 2^n enters analytically in `P_Haar(F)`.
   Missing the top of the range shifts the training distribution and may
   under-constrain the model's calibration at n=6 (edge of our
   distribution), producing the per-qubit RMSE degradation we observe
   (0.33 at n=3 → 0.72 at n=6).
4. **Long-tail unbounded target.** Small-qubit non-entangling structures
   produce very high KL (up to 27.6 in our dataset). We mitigate with
   `log1p(KL)` target and clipping at 3.0, but the paper's larger circuits
   naturally cluster KL near zero, giving them a milder target
   distribution.

**Would running full-scale close the gap?** Almost certainly yes for C4;
plausibly yes for C5. Extrapolation at our observed 9 PQC/s throughput:
25,000 PQCs ≈ 46 min of wall time, plus ~30 min GPU training. Well within
a follow-up compute budget. We did not run this because the wave-brief
scope was scale-limited.

**Confidence in attribution:** medium. We did not run a scaling ablation
(300/750/1500/…/25000 PQCs). A single-scale replication cannot
conclusively rule out that there is *also* an unstated implementation
detail in the paper (data augmentation, target normalisation, learning-rate
schedule, weight init, or something in the graph construction) that
contributes some of the gap. This is a **residual risk** on the paper's
headline numbers that only a full-scale replication can retire.

---

## 2. Not-tested claims (out-of-scope for wave brief)

### C6 — Noisy-backend RMSE ≤ 0.08 (Figs 5/9/10, Table I)
**Requirements to close:**
- Load FakeGuadalupe, FakeMumbai, FakeHanoi calibration data (Qiskit
  `qiskit_ibm_runtime.fake_provider`).
- Expand node features from 22 → 23 dims per paper: T1, T2, gate error,
  readout error keyed per qubit.
- Generate 4000 additional random PQCs per backend and re-run Stage 1
  ground-truth pipeline with noise model.
- Retrain and test.

**Blocker:** none technical; skipped for time.

### C8 — Extrapolation trained-on-n≤5, tested-on-n=10 (Fig 11)
**Requirements to close:**
- Extend Stage-1 pipeline to n = 7, 8, 9, 10 (statevector cost grows
  2^n; n=10 = 1024-dim statevectors, still tractable single-CPU per
  circuit but slower fidelity computation).
- Retrain on n ≤ 5 subset, test on n = 6, 7, 8, 9, 10.

**Blocker:** none technical; skipped for time. Our data hints at
degradation (0.33 → 0.72 across n=3 → n=6), which is not consistent
with paper's flat-RMSE extrapolation claim — but this could be a data-scale
artefact (see §1) rather than a genuine failure of extrapolation.

### C9 — Real IBM-Hanoi hardware Table I (Circuit 3: hardware KL 0.280 vs predicted 0.402)
**Requirements to close:**
- IBM Quantum runtime account with queue access.
- Reproduce circuits, submit to `ibmq_hanoi`, wait for queue, retrieve
  results.

**Blocker:** hardware access + queue latency; single-data-point comparison
in paper is already weak evidence, so this is a low-value follow-up unless
run alongside a broader hardware campaign.

### Fig 7 right — 64 IBM Qiskit RealAmplitude circuits, RMSE 0.06
**Requirements to close:**
- Enumerate the 64 configurations (RealAmplitude has a defined
  entanglement pattern × n_qubits × n_reps grid; can be reconstructed).
- Compute ground-truth KL for each.
- Evaluate trained GNN on each.

**Blocker:** none technical; skipped for time.

### Fig 8 — Sample-size ablation
**Requirements to close:** rerun the pipeline with per-PQC sample counts
in {500, 1000, 2000, 5000, 10000}. Cheap.

---

## 3. Honest limitations of THIS replication (methodological caveats)

### 3.1 Single-seed runs, no confidence intervals
All reported Pearson r and RMSE are from a single training seed. The
qualitative claim "GNN learns the expressibility signal" (r ≈ 0.89) is
strong enough that a seed sweep would probably not overturn it, but we
have not established this empirically. **Fix:** rerun with 10 seeds and
report mean ± std.

### 3.2 CZ mapped to CX in graph encoder (OOV handling)
Sim circuits 9/10/12 use CZ, which is not in our random-PQC gate
vocabulary. We map CZ → CX in the graph encoder (structurally lossy since
CZ = H · CX · H). This is a plausible partial cause of the Circuit-9
outlier (predicted vs true KL off by ≈0.55). **Fix:** extend the training
gate vocabulary to include CZ natively (adds one node-type one-hot bit
and re-runs Stages 2/3).

### 3.3 Single-layer Sim-19 vs paper's 3-layer × 19
Paper evaluates on 57 circuits (19 base × 3 layer counts). We evaluated
on 19 (single-layer only). Our Sim-19 RMSE 0.29 is therefore not a
like-for-like comparison to the paper's 0.05. **Fix:** extend Stage-4 to
iterate over layer_count ∈ {1, 2, 3}.

### 3.4 Sim-2019 published values read to two significant figures
Our Δ column in the ground-truth validation table (e.g. Circuit 3 Δ =
-0.00) claims sub-hundredth agreement, but the published Sim reference
values themselves are read from the Sim paper's plots/tables to roughly
two significant figures. Sub-percent Δ claims are within reading
precision, not sub-percent numerical agreement. This does not weaken the
Stage-1 conclusion (pipeline reproduces published values within noise),
but it does bound how tightly we can quantify that agreement.

### 3.5 Global-features branch attribution not ablated
We did not run: pure global-MLP-only (no GNN), pure GNN-only (no globals),
random baseline. Without these, we cannot say how much of the r ≈ 0.89
signal comes from graph topology vs bulk count statistics. Paper likely
faces the same ambiguity. **Fix:** three-way ablation.

---

## 4. What did NOT fail (positive controls)

- Ground-truth Sim-2019 KL pipeline: **fully reproduced** against
  published values (Circuits 1, 2, 3, 6, 7, 9, 11, 19 all match within
  stochastic-sampling noise).
- Random-PQC generator: produced KL range 0.009 – 27.6, consistent with
  paper's implied variance.
- GNN training loop: converged cleanly over 300 epochs with
  ReduceLROnPlateau; no NaNs, no divergence, no overfitting collapse.
- Pearson r on both held-out and Sim-19: **strong positive signal that
  the architecture is doing the right thing.**
- Nothing failed technically. No crashes, no missing dependencies, no
  environment collapses.

---

## 5. Residual risk to the paper's claims

Given what we did and did not test, our replication is consistent with
three possible worlds for the paper:

- **World A (most likely, prior ~70 %):** Paper is fully correct.
  Absolute RMSE 0.05 is achievable at full 25,000-PQC scale, and our
  scale-limited replication is exactly what one would expect at 2 % data.
- **World B (~25 %):** Paper is qualitatively correct but has one or
  more unstated implementation details (target normalisation, data
  augmentation, LR schedule) that contribute a real fraction of the gap.
  Full-scale independent replication would reach maybe RMSE 0.10–0.15
  rather than 0.05.
- **World C (~5 %):** Paper's headline RMSE is measured under a subtly
  different metric (e.g. after target-transform, without back-transform)
  and is not directly comparable to our RMSE on raw KL.

Only a full-scale, seed-swept replication (Stage 6 above) can distinguish
A from B/C. Our current evidence is sufficient to say the paper's
**scientific contribution** (GNN can regress PQC expressibility from
structure) reproduces cleanly. It is insufficient to say the paper's
**engineering result** (RMSE 0.05) reproduces cleanly.

**This is why the verdict is PARTIAL, not REPLICATED and not FAILED.**
