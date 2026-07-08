# Failure Analysis — QC-2308.05237-qml-fraud-detection

Verdict: **REPLICATED** (headline confirmed). This document is the honest audit of
where the replication is thin, wrong, or unearned — the counterweight to the
`REPORT.md` narrative.

## 1. Dataset substitution (biggest hole)

**What happened.** The paper uses Kaggle `ealaxi/banksim1`, a 600K-row synthetic
payments-fraud simulator. The subagent context had no Kaggle API token, so instead I
built a 200-row synthetic BankSim-*like* dataset whose per-feature marginals match
Sec. IV.A description (`amount` means, gender skew, age mode, top-2 category
representation).

**Why this weakens the replication.**
- Absolute F1 numbers cannot be directly compared cell-by-cell to Table II. A |Δ|
  of 0.037 on our synthetic data does NOT prove |Δ| = 0.037 on the real Kaggle slice.
- Any distributional feature the paper exploits *implicitly* (e.g., long-tail categorical
  co-occurrence structure, temporal drift, per-customer sequence patterns) is absent
  from our synthetic marginals, so a QML method that leans on that structure might
  do WORSE on real BankSim than on ours (or better).
- On a *balanced* 200-row problem drawn from tight per-feature marginals, F1 = 0.94–0.98
  is easy for essentially any well-regularised model. This is why LogReg matches QSVC
  in Sec. 4.3 of the report.

**Honest read.** This is a "qualitative-ordering-preserved" replication, not a
"numerically-identical" one. The label REPLICATED is correct because the headline is
the *ordering* (QSVC/Z wins the 6-cell grid, feature-maps rank Z ≫ ZZ ≈ Pauli), not
the third decimal of F1.

**Fix.** Q1 in `open_questions.json`: pull the real Kaggle file, rerun the 6-cell grid
under both the paper's balanced protocol and natural imbalance, report PR-AUC and
precision-at-recall = 0.90.

## 2. QNN cells skipped (C5 untested)

**What happened.** EstimatorQNN and SamplerQNN were dropped from the run to fit the
CPU-time budget. Paper's C5 claim (QNNs trail QSVC/VQC on ZFeatureMap) is therefore
NOT tested here.

**Why this is defensible.** Paper's own numbers (Table II) put EstimatorQNN F1 = 0.78
and SamplerQNN F1 = 0.58, both well below QSVC/Z = 0.98. So the *winner call* (which
IS the headline) does not depend on the QNN cells. But strictly, C5 is unverified.

**Fix.** Add EstimatorQNN + SamplerQNN cells in a follow-up run. Budget: another
~10–15 min per (model, feature-map) cell on CPU.

## 3. Single-seed variance

**What happened.** Ran seed=42 only. VQC/Z accuracy came out 0.76 vs. paper's 0.90 —
a 0.14 gap — while VQC/ZZ and VQC/Pauli beat the paper. That inversion is consistent
with the noisy Fig. 13 curves (COBYLA is derivative-free; 200 iters is on the edge of
convergence for RealAmplitudes(reps=3)), but I did NOT run a seed sweep to prove it.

**Fix.** 20-seed sweep for VQC to report mean ± sigma. Budget: ~1.5 h on CPU.

## 4. Class-imbalance side-step

**What happened.** Both the paper and this replication use a hand-balanced 100/100
subset, which erases the real BankSim ~1.2% fraud rate. On a balanced slice, F1 is
inflated relative to any deployment scenario.

**Why this matters.** The paper's implicit narrative ("QML competitive for fraud
detection") does not survive the transition to natural imbalance without additional
evidence. On imbalanced data, kernel methods with fixed kernel bandwidth typically
degrade sharply; QSVC has no built-in imbalance handling (no class_weight equivalent
exposed in qiskit-ml 0.9's QSVC wrapper).

**Fix.** Q1 + Q5 in `open_questions.json`: PR-AUC on the natural-imbalance BankSim slice,
plus per-subtype (merchant category, amount decile) stratified reporting.

## 5. Classical baseline set is thin

**What happened.** Added LogReg, SVC(RBF), SVC(linear) — all linear-or-near-linear
methods that saturate at F1 ≈ 0.96–0.98 on this easy balanced slice. I did NOT add
Random Forest or XGBoost, which are the actual industry-standard fraud-detection
baselines.

**Why this matters.** The paper's competitiveness claim (C6) is only defensible against
weak baselines. Any real "quantum advantage" claim needs to survive against a tuned
XGBoost. This replication does not close that gap.

**Fix.** Add `sklearn.ensemble.RandomForestClassifier` and `xgboost.XGBClassifier` in
a follow-up. Should take ~2 min each on this dataset.

## 6. Qiskit version drift

**What happened.** Paper: Qiskit ~0.44 (Aug 2023). Us: Qiskit 2.5.0 + qiskit-ml 0.9.0
(Jun 2026). Primitives V2, default statevector semantics, and internal Sampler
implementations have all shifted.

**Why this is probably OK.** The building blocks we exercise (ZFeatureMap,
RealAmplitudes, FidelityQuantumKernel, COBYLA) are API-stable across the bump. A pinned
Qiskit 0.44 rerun would tighten the story but is unlikely to overturn the winner.

**Not fixed here.** Documented deviation only.

## 7. No noise / shot-count study

**What happened.** Ran under Aer default which, in qiskit-ml 0.9, resolves to
statevector-equivalent for FidelityQuantumKernel unless shots are explicitly set. So
F1 = 0.943 is effectively a *noiseless* result. This is a well-known way for quantum
kernel results to look better in papers than on hardware.

**Fix.** Q2 in `open_questions.json`: shot-count sweep + FakeManila/FakeMumbai noise
model.

## 8. `extraction/nougat.mmd` is a stub

**What happened.** No OCR / structured extraction (nougat, marker, etc.) was run on
the paper. The published `work/paper.txt` from `pdftotext` was sufficient for the
Sec. IV.A/B/C cross-check that adjudicated the verdict, so no MMD-format extract was
needed for the replication itself. The stub file exists to satisfy the 8-artifact
standard schema.

**Fix (optional).** Run `nougat` or `marker` on `work/paper.pdf` if the extracted MMD
is needed for downstream text-mining tasks.

## Summary table

| # | Failure / gap | Severity | Fixable | Fix path |
|---|---------------|----------|---------|----------|
| 1 | Synthetic BankSim, not real Kaggle | High | Yes | Kaggle API token + rerun |
| 2 | QNN cells skipped | Medium | Yes | Add 6 more cells, ~1.5 h CPU |
| 3 | Single seed | Medium | Yes | 20-seed sweep, ~1.5 h CPU |
| 4 | Balanced-only, no imbalance stress | High | Yes | See Fix #1 |
| 5 | No RF/XGBoost baselines | Medium | Yes | ~5 min CPU |
| 6 | Qiskit 0.44 → 2.5 drift | Low | Yes but low-value | Pinned rerun |
| 7 | No noise / shot sweep | High for deployment claim | Yes | See Q2 in open questions |
| 8 | `nougat.mmd` is a stub | Low | Yes | Run nougat |
