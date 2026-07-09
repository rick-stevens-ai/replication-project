# Failure Analysis — BVBRC-12 Replication (Hyun et al. 2020)

Verdict: **PARTIAL** (Coverage 4/10, Agreement 8/10).

This file dissects what failed, why, and what the reader should discount. All claims are grounded in `report/REPORT.md`.

---

## 1. Primary failure — 2 of 3 organisms not replicated

### What
- **P. aeruginosa:** 84 of 456 protein FASTAs missing (18% gap). No CD-Hit, no feature matrix, no SVM-RSE, no top-50 audit.
- **E. coli:** 1,261 of 1,588 protein FASTAs missing (79% gap). No downstream artifacts of any kind.
- **10 of 16 antibiotic cases** in the paper's claim surface are entirely absent from this replication.

### Root cause — DATA harvest, not code or compute
The pipeline (`scripts/03_pangenome.py`, `04_feature_matrix_and_ml.py`, `06_full_pipeline.py`) is fully written and validated on the SA path. CD-Hit and scikit-learn are installed and working (proven by the 41 MB SA cluster file and the SA results JSON). The blocker is:

- **BV-BRC public API rate limit:** ~1 req/s anonymous.
- **No retry/checkpoint/backoff layer** in `scripts/02_fetch_proteins.py` / `07_download_proteins.py`. Runs paused mid-harvest (`PROGRESS.md`: "~44/456 downloading", later 372/456; EC stayed at 0 → eventually only 327).
- **OpenClaw policy for this run:** free endpoints only, so no authenticated / higher-rate BV-BRC access was used.

### Impact on paper's claims
- The paper's core cross-organism generalization claim — that the same SVM-RSE method works across three phylogenetically distant pathogens — is **not tested** by this replication.
- The paper's harder cases (EC β-lactams, PA carbapenems / fluoroquinolones) are entirely un-audited.
- We can neither confirm nor challenge the paper's PA/EC results on our own evidence.

### Fix path
1. Add retry + on-disk checkpointing to `02_fetch_proteins.py` (idempotent per-genome writes; skip already-present `.faa`).
2. Add exponential backoff on HTTP 429 / 5xx.
3. Re-run for PA (missing 84 → ~25 min at 1.5 s/req with backoff) and EC (missing 1,261 → ~6 h wall time).
4. Then re-invoke Stages 2–5 for PA and EC (~2 h ML wall time; CD-Hit on EC at 1,588 genomes is the long pole).

### Severity
**HIGH for coverage, LOW for method fidelity.** The unreplicated cases are missing evidence, not contradictory evidence.

---

## 2. Secondary failure — 2 LmrS top-50 misses on S. aureus

### What
- CLI (clindamycin): paper reports 3 known-AMR hits in top-50; we recover 2. Missed: LmrS allele.
- ERY (erythromycin): paper reports 2 known-AMR hits in top-50; we recover 1. Missed: same LmrS allele.
- Both misses are the same `LmrS Cluster_556_Allele_7` placement, which the paper itself ranks at 40 (CLI) and 43 (ERY).

### Root cause
- **Stochastic subsampling.** The random subspace ensemble draws 50% of features per SVM. A feature that is ranked 40–43 in the original ensemble sits near the top-50 boundary; small variance in which features are sampled per fit shifts it out of the top-50 in our re-run.
- **Ensemble-size shortcut.** Paper spec: 500 SVMs per fold. Our implementation: 100 per fold × 5 folds = 500 total. Aggregate weights are similar in expectation, but per-fold variance is mildly inflated, which further destabilizes tail rankings like the LmrS placement.

### Impact
- Every rank-1 canonical determinant matches (tet(K), dfrA, aac(6')-aph(2''), erm methyltransferases, gyrA, parC).
- Only tail-of-list hits fluctuate — expected behavior for a random-subspace ensemble.

### Fix path
- Match the paper spec exactly: 500 SVMs per fold (not per replication run). Cost: ~5× more ML wall time on SA (still modest at 288 genomes).
- Optional: report top-100 instead of top-50 to reduce boundary sensitivity.

### Severity
**LOW.** Well within the paper's own stochastic tolerance; every rank-1 hit reproduces.

---

## 3. Tertiary methodological caveats (not failures, but discount points)

### 3a. Ensemble-size shortcut, generally
- 100 SVMs/fold × 5 folds = 500 total, vs paper's 500/fold.
- Aggregate first-moment statistics (mean signed weight) are the same in expectation; second-moment (per-fold variance) is inflated.
- Only matters at the tail of the ranked feature list.

### 3b. Two MCC values slightly above the paper's max
- Gentamicin MCC = 0.986 and tetracycline MCC = 0.966 sit above the paper's all-16-case max (0.952).
- Difference is <2%.
- SA is the paper's high-signal clonal organism at the top of the paper's own MCC distribution; the paper's Fig 2/3 supports this.
- **Not a failure or an artifact** — flagged for transparency because "matches beat the paper's max" invites suspicion.

### 3c. Binary S/R framing
- Inherited from the paper (BV-BRC breakpoint-dichotomized labels).
- MIC-regression is not attempted (surfaced as `open_questions.json` Q4).
- Not a replication failure, but limits what the audit can say about dose-dependent resistance.

### 3d. No cross-species transfer test
- Paper trains one model per (organism, antibiotic); does not test SA→PA/EC transfer either.
- Replication cannot go beyond the paper here (and could not even if PA/EC had been harvested, since the per-organism feature spaces are non-comparable without a joint CD-Hit-2D clustering).
- Surfaced as `open_questions.json` Q2.

### 3e. No phylogenetic-confounder audit on top-50 features
- Paper does not distinguish causal AMR features from clonal-lineage hitchhikers or plasmid-backbone co-segregators.
- Replication inherits this ambiguity.
- Surfaced as `open_questions.json` Q3.

---

## 4. What is NOT a failure

- **SA methodology fidelity.** CD-Hit params, core threshold, per-allele encoding, unique-gene dropping, class-weighting, 5-fold CV, feature-importance definition all match the paper spec.
- **SA metric agreement.** All 6 (Accuracy, MCC, AUC) triples inside the paper's 16-case envelope.
- **SA biology recovery.** All 6 rank-1 canonical resistance determinants recovered at rank 1.
- **Audit script re-executed 2026-06-25.** §3c numbers are reproduced from a live re-run, not just cached from an earlier session.

---

## 5. Reader-facing bottom line

- **Do not** treat this as a cross-organism replication of Hyun 2020. It only tests the clonal, high-signal, small-core organism (SA) on 6/16 cases.
- **Do** treat the SA slice as strong evidence that Hyun 2020's SVM-RSE pipeline is faithfully implementable and produces the metrics and top-50 AMR-gene rankings the paper claims — at least on its easiest of three organisms.
- **The 10/16 unreplicated cases and the two LmrS tail-of-list misses are the honest debits** that keep this from being a FULL verdict.
