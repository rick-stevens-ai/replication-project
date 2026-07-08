# Workflow — Replication of arXiv:1801.02809

**Paper:** Byrnes, Forster, Tessler (2018), *Generalized Grover's algorithm for
multiple phase inversion states*, arXiv:1801.02809v1.
**Wave:** QC-100. **Replicator:** Ollie. **Original run:** 2026-07-03.
**Backfill:** 2026-07-06.

## Stages

### 1. Ingest
- Downloaded paper PDF + text to `work/1801.02809.pdf` and `work/1801.02809.txt`.
- Identified 5 checkable claims (C1..C5) covering spectrum, constructed-state Rabi
  oscillation (continuous + gate), naive-init failure, and textbook-Grover anchor.

### 2. Environment
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1801.02809-generalized-grover-multiphase
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet qiskit==2.5.0 qiskit-aer==0.17.2 numpy scipy
```
- Python 3.13, Qiskit 2.5.0, Qiskit Aer 0.17.2, NumPy 2.5.0, SciPy 1.18.0.
- Isolated venv; no host-Python interference.

### 3. Implementation
- `code/generalized_grover.py` (v1): built P_S, P_T, computed
  `c_n = svd(P_T P_S)`, tried an SVD-based construction of Eq. 12 → clean but
  needed convention-fixing.
- `code/generalized_grover_v2.py` (v2, canonical): built H = P_S + P_T directly,
  diagonalized, identified largest-c_n eigenpair, assembled Eq. 12 with Eq. 9
  sign convention, ran continuous-time (scipy.linalg.expm) and gate iteration
  (numpy) and gate iteration (Qiskit Aer via QuantumCircuit.initialize +
  Operator(U_G @ U_O)). Also ran textbook single-target Grover as sanity anchor.

### 4. Execution
```bash
python code/generalized_grover_v2.py 2>&1 | tee logs/run2.log
```
- Ideal Aer statevector, no noise model.
- Seed 20260703 for the random orthonormal source states.
- Wall time: seconds (small n=5).

### 5. Verification
- Cross-check: numpy statevector vs Qiskit Aer statevector agree to 6 decimals
  (0.99908 vs 0.99908) on the same iteration.
- Cross-check: continuous-time peak time matches predicted π/(2 c_1) to 0.3%.
- Cross-check: textbook Grover matches (π/4)√D optimum to nearest integer.

### 6. Report
- Machine-verifiable numbers extracted to `data/v2_summary.json`.
- `report/REPORT.md` written 2026-07-03.
- Backfill 2026-07-06: `report/REPORT.tex`, `open_questions.json`,
  `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`,
  `failure_analysis.md`, `extraction/nougat.mmd` (stub).

## Backfill provenance (2026-07-06)
- No sims re-run; all numbers preserved from `data/v2_summary.json` and REPORT.md.
- Free endpoints only (local Qiskit Aer at original run; no LLM calls at backfill).
- Verdict preserved: **REPLICATED**.
