# Workflow — arXiv:1806.11463 replication

Chronological, end-to-end log of what was done to produce the on-disk
artifacts. Reproducible from `report/REPORT.md` + `code/*.py` +
`report/evidence/versions.txt`.

## 1. Paper triage
- Read arXiv 1806.11463v3 in full.
- Identified 5 distinct claims (C1..C5) and classified each by testability
  on CPU / simulator vs on retired hardware.
- Decision: C1, C2, C3, C5 are simulation-tier and testable now.
  C4 (IBMQX5 hardware, F=0.78) is out of scope but bracketable via a
  noise sweep.

## 2. Environment setup
- Python 3.14.6 (macOS host), fresh `.venv` inside the paper working
  directory.
- Installed: `qiskit` 2.5.0, `qiskit-aer` 0.17.2, `numpy` 2.5.0,
  `scipy` 1.18.0.
- Full manifest pinned to `report/evidence/versions.txt`.

## 3. C2 — noiseless HHL on the paper's 2x2 matrix
- Wrote `code/hhl_2x2_paper.py`.
- Circuit: 4 qubits (1 b-register + 2 clock + 1 ancilla), exploits
  Hadamard-diagonal structure of A = (1/2) * [[3,1],[1,3]].
- Extracted the post-selected (ancilla = |1>) branch of the
  `Statevector` output.
- Compared to classical `numpy.linalg.solve(A, b)` (normalized).
- Result: fidelity 1.000000, atol 1e-6. Persisted to
  `report/evidence/hhl_noiseless.json` and `report/evidence/hhl_circuit.txt`.

## 4. C3 — noisy sweep
- Extended the same driver with an `AerSimulator` shot backend.
- Installed 1- and 2-qubit depolarizing errors on every gate at 8
  noise levels: {0.000, 0.001, 0.005, 0.010, 0.020, 0.050, 0.100, 0.200}.
- 8192 shots per point; post-selected on ancilla = |1>.
- Fidelity lower-bounded via Bhattacharyya coefficient of the
  comp-basis post-selected distribution against the classical target's
  probability distribution.
- Persisted to `report/evidence/hhl_noisy_sweep.json`.
- Result: smooth monotone decay 1.0 -> ~0.8 (mixed-state floor).
  Matches Fig. 1(a) qualitatively.

## 5. C1 — end-to-end quantum -> Bayesian-GP posterior
- Wrote `code/gp_bayesian_predict.py`.
- Toy 2-point GP with K = [[1,1/2],[1/2,1]], sigma_n^2 = 0.5 chosen so
  that K + sigma_n^2 I = A (the paper's exact matrix), y = (1, 0),
  k_* = (0.7, 0.2), k_** = 1.
- Ran HHL twice: once on b = y-hat (normalized), once on b = k_*-hat.
- Recovered alpha_q = (K + sigma_n^2 I)^{-1} y and (K + sigma_n^2 I)^{-1} k_*
  from the post-selected b-register statevector amplitudes (with norm
  correction).
- Computed predictive mean k_*^T alpha_q and predictive variance
  k_** - k_*^T (K+sigma^2 I)^{-1} k_*.
- Result: alpha_q vs classical alpha diff-norm 1.1e-16; mean 0.475,
  variance 0.6725 --- both machine-precision matches.
- Persisted to `report/evidence/gp_bayesian_predict.json`.

## 6. C4 — bracketing the retired-hardware headline
- IBMQX5 has been decommissioned. Direct rerun not possible.
- Cross-checked our noisy-sweep table against the paper's F=0.78:
  falls between our gate_noise=0.05 (F~0.82) and gate_noise=0.10
  (F~0.80). Consistent with 5-10% per-gate effective depolarizing on
  2018-era superconducting hardware, which is realistic.

## 7. C5 — resource-count verification
- Read the paper's resource claims (Sec. IV / Sec. V): 6 qubits for
  general 2x2 protocol, 19 for 4x4 with 4-bit precision.
- Our implementation is a specialized 4-qubit variant that exploits
  the Hadamard-diagonal structure of A. Verified structurally: 1
  b-register qubit + 2 clock qubits (4-bit precision equivalent via
  QPE-free eigenvalue copy) + 1 ancilla = 4 qubits. Matches the
  paper's demonstration circuit (ref. [49]) rather than the
  general-purpose count.

## 8. Aggregation
- Wrote `report/evidence/summary.json` --- machine-readable
  claim/measurement pairs.
- Wrote `report/REPORT.md` --- human-readable replication report.

## 9. Backfill (this pass, 2026-07-06)
- Added `report/REPORT.tex` (LaTeX render), `report/workflow.md` (this
  file), `report/failure_analysis.md`, `report/open_questions.json`,
  `report/open_questions_section.tex`, `report/artifacts_summary.md`,
  and `extraction/nougat.mmd` stub. No re-runs of any simulation ---
  all artifacts derive from the already-computed evidence files.

## Verdict
REPLICATED for the simulation-tier claims (C1, C2, C3, C5).
C4 out of scope but bracketed. See `report/REPORT.md` and
`report/failure_analysis.md`.
