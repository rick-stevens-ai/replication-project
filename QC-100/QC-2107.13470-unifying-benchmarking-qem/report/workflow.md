# Workflow — QC-2107.13470 replication

Chronological workflow for the replication of Bultrini et al.
(arXiv:2107.13470v2), *Unifying and benchmarking state-of-the-art
quantum error mitigation techniques* (Quantum 7, 1034).

## 1. Ingest
- Paper PDF pulled to `work/paper.pdf`; `pdftotext` extract to
  `work/paper.txt` for grep-based claim extraction.
- Nougat MMD extract stub at `extraction/nougat.mmd` (not re-run in
  backfill; scaffolding only).

## 2. Claim extraction
- Read paper §§1, 4, 5, and Appendix H (noise model).
- Extracted 6 claims (C1–C6, see `report/REPORT.md` §2 and
  `report/REPORT.tex` §2.3).
- Identified C1 as the testable qualitative headline; C3, C4 as out of
  scope (need paper's IonQ noise model + $N_{tot}=10^{10}$ + UNITED).

## 3. Environment
- Python 3.12 venv at
  `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2107.13470-unifying-benchmarking-qem/.venv/`.
- Packages: `mitiq==1.0.0 qiskit==2.5.0 qiskit-aer==0.17.2 cirq==1.6.1`
  plus numpy, scipy, ply.
- Free-endpoints-only: everything runs local CPU on CherryRd; no cloud,
  no paid QPU.

## 4. Circuit + noise
- 2-qubit, depth-3 random circuit built from `{Rx, Ry, CX}` with
  θ ~ U(0.2, 1.2), plus a biasing `Ry(0.4)` on q0.
- Ground truth: noiseless `Statevector` `<Z_0>`.
- Noise: Qiskit Aer `NoiseModel` — 1q depolarizing p1=0.005, 2q
  depolarizing p2=0.02 (stand-in for paper's trapped-ion model; same
  qualitative regime).

## 5. QEM executors (Mitiq 1.0)
- `raw`: `executor_noisy(qc)` → single AerSimulator call, 20 000 shots.
- `zne`: `execute_with_zne` with `RichardsonFactory(scale_factors=[1,2,3])`,
  gate-folding scaling (`fold_gates_at_random`).
- `pec`: `execute_with_pec` with local-depolarizing representations at
  p2=0.02, budget swept ∈ {100, 300, 1000, 3000}.
- `cdr`: `execute_with_cdr` with `num_training_circuits=10`,
  `fraction_non_clifford=0.3`, `executor_ideal` (noiseless AerSimulator)
  as classical training oracle.

## 6. Runs
- Single seed (seed=2): `code/replicate_qem.py` — ~4 min.
- 5-seed ensemble (seeds 1–5, 2 skipped as `|<Z_0>_exact| < 0.05`):
  `code/replicate_multi_seed.py` — ~5 min.
- PEC sample sweep: `code/pec_shot_budget.py` — ~5 min.

## 7. Scoring
- Per-instance `|est - exact|`, then mean across the 3 non-null seeds.
- ZNE: `-40%` mean err vs. raw. CDR: `-50%` mean err vs. raw. PEC:
  `+240%` (worse — representation mismatch, not a paper method).

## 8. Verdict
- Headline C1 (data-driven QEM > raw noisy) **REPLICATED** — two
  paper-relevant methods (ZNE, CDR) both beat raw over 3 seeds.
- C2 (shot-budget-dependent ranking) marked PARTIAL (no $N_{tot}$ sweep).
- C3, C4 (specific $20\times$ number; UNITED) marked out of scope.
- C6 (UNITED = CDR+ZNE+VD; PEC not in paper) verified from paper text.

## 9. Backfill (2026-07-06)
- Added `report/REPORT.tex`, `report/open_questions.json`,
  `report/open_questions_section.tex`, `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`, and
  `extraction/nougat.mmd` stub. No re-runs.
