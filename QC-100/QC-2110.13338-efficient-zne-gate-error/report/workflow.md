# Workflow — arXiv:2110.13338 replication

Chronological workflow of the QC-100 replication attempt for
Pascuzzi et al., *Computationally Efficient Zero Noise Extrapolation for
Quantum Gate Error Mitigation*.

## 1. Ingest
- Pulled `2110.13338v3.pdf` into `work/paper.pdf`; extracted plain text with
  `pdftotext -layout` into `work/paper.txt`.
- Read Sections I–III + Fig 2/3 caption to identify the reproducible headline
  example (2-qubit CNOT ladder, ε=1% depolarising + T₁=50µs amp damping,
  Pr(|11>) observable).

## 2. Claims tabulation
- Enumerated six candidate claims (C1–C6) as in the REPORT.
- Down-selected to C1–C4 for the headline replication under the QC-100
  small-instance constraint. C5 (LIIM per-CNOT list) and C6 (multi-device
  parallel RIIM) tagged out-of-scope.

## 3. Environment
- `python3.12 -m venv venv`; `pip install mitiq qiskit qiskit-aer cirq numpy
  scipy matplotlib ply`.
- Pinned versions recorded in `report/evidence/results.json.tools`:
  mitiq 1.0.0, qiskit 2.5.0, qiskit-aer 0.17.2, cirq 1.6.1, CPython 3.12.
- All CPU, no HPC/GPU needed.

## 4. Noise model reconstruction
- Two-qubit depolarising `ε = 0.01` on `cx` (from paper caption).
- Amplitude damping via
  `thermal_relaxation_error(T1=50e-6, T2=T1, t=200e-9)` on each qubit of the
  `cx`, composed after the depolarising channel (matches paper's
  ε + T₁-decoherence recipe).
- Single-qubit gates noiseless (matches paper convention that ZNE targets
  CNOTs only).

## 5. Circuit family
- `X0 X1` to prepare |11>, then `n_c` CNOTs on the same pair, for
  `n_c ∈ {2,4,6,8,10,12,14,16,20,24,30}` — even so noiseless target = 1.

## 6. ZNE arms
- **Full (FIIM-like):** `mitiq.zne.execute_with_zne` with
  `RichardsonFactory(scale_factors=[1.0, 2.0, 3.0])` and `fold_global` — 3
  auxiliary circuits per data point.
- **Efficient:** `LinearFactory(scale_factors=[1.0, 3.0])` with
  `fold_gates_at_random` — 2 auxiliary circuits per data point.
- Shots: 8192/subcircuit → 24 576 (full) vs 16 384 (efficient) = 66.7 % of
  full budget.

## 7. Runs
- `python report/evidence/zne_reproduction.py` → CNOT sweep,
  `results.json`.
- `python report/evidence/make_plot.py` → `fig2_replication.png`.
- `python report/evidence/precision_vs_shots.py` → 30-trial precision
  study, `precision_vs_shots.json`.
- Runtimes: sweep ≈ 6 s, precision study ≈ 50 s (all CPU).

## 8. Comparison against paper
- Raw decay 0.97→0.68 over n_c 2→30 matches Fig 2's raw curve shape.
- Full ZNE: mean 1.005, MAE 0.056 across 11 points → holds near truth.
- Efficient ZNE: MAE 0.048 at 66.7 % shots → matches/beats full.
- Precision study: efficient variant has ~3× smaller empirical std than
  full at equal shots, at n_c=10.

## 9. Verdict
- Called REPLICATED on headline C1–C4.
- Called out C5 (LIIM per-CNOT list) and C6 (multi-device parallel RIIM)
  as untested extensions.

## 10. Backfill (2026-07-06)
- Added: REPORT.tex (with honest Critique section),
  open_questions.json (5 items),
  open_questions_section.tex,
  workflow.md,
  artifacts_summary.md,
  failure_analysis.md,
  extraction/nougat.mmd (stub — see failure_analysis).
- No sims re-run. All original evidence files preserved.
- Verdict preserved: REPLICATED.
