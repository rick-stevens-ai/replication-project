# Workflow — arXiv:2204.00340 (QAOA for qudit systems)

## Stages

1. **Paper acquisition.** Fetched `2204.00340v2.pdf` from arXiv (May 2023
   version, published as Phys. Rev. Research 5, 033039). Text conversion
   via pdftotext for skim + section IV location.

2. **Claim extraction.** Read Sec. IV (case study) + Figs. 4, 5 + Table I.
   Identified 6 discrete claims (C1–C6). Focused on C1–C4 as those are
   what actually appears in the numerical results section and is
   testable on a CPU in <20 min.

3. **Design of independent implementation.** Chose from-scratch NumPy
   (no Qiskit, no Cirq, no PennyLane) to make the replication
   genuinely independent of the paper's tooling. Wrote:
   - qutrit shift matrix X (3x3), mixer `H_M = Σ_j (X_j + X_j†)`;
   - diagonal cost `H_C[c] = λ·(monochromatic edge count under c)`;
   - QAOA layer `|ψ⟩ ← exp(−iβ H_M)·exp(−iγ H_C)|ψ⟩` via
     one-shot Hermitian eigendecomposition of H_M.

4. **Matched qubit control.** Same N=6, same edges, same λ. 2 qubits
   per node with invalid-pattern penalty 50. Standard transverse-field
   mixer applied factorized per qubit.

5. **Classical outer loop.** L-BFGS-B with 15 random restarts per
   (p, encoding). Best-of-restart reported; all 15 restarts stored for
   the C4 multi-modality check.

6. **Exact enumeration for ground truth.** Enumerated all 3^6=729
   colorings → E_min=0 with 18-fold-degenerate optimal manifold.

7. **Sweep.** p ∈ {1..5} × encodings {qudit, qubit} × 15 restarts.
   Total wall = 1193 s on one CPU core.

8. **Verdict + writeup.** Cross-checked C1-C4 vs paper; wrote REPORT.md
   with tables and honest caveats.

## Data/compute cost

- 1 CPU core, macOS/CherryRd.
- Peak memory: 729×729 complex128 mixer + 4096-dim qubit state = <100 MB.
- No GPU, no external services, no paid endpoints.

## Reproducibility

`cd code && python3 -u qudit_qaoa.py 2>&1 | tee ../results/run.log`
with Python 3.13.7, NumPy 2.4.3, SciPy 1.18.0.
Seed for random restarts is captured in `results/replication_results.json`.

## Backfill (2026-07-06)

Added report/{REPORT.tex, open_questions.json,
open_questions_section.tex, workflow.md, artifacts_summary.md,
failure_analysis.md} and extraction/nougat.mmd stub. No sim reruns;
original claims/tables preserved verbatim.
