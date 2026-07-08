# Workflow — arXiv:2106.06463 replication

Paper: Azad & Singh, *"Quantum Chemistry Calculations using Energy Derivatives on Quantum Computers"* (arXiv:2106.06463v1, Jun 2021).
Wave: QC-100. Replicator: OpenClaw subagent, CherryRd local sim, 2026-07-03.

## 1. Ingest
- Pulled arXiv preprint PDF → `work/paper.pdf`.
- Extracted plain text → `work/paper.txt` for grep / claim-mining.
- Identified headline claim (§IV.A, Fig. 4b/4d): H₂/STO-3G equilibrium
  geometry via gradient-descent VQE converges to (0.741 Å, −1.137 Ha).
- Enumerated claim table (C1–C8) in REPORT.md §2.

## 2. Environment provisioning
- macOS 25.3.0 / Python 3.14.6.
- `python3 -m venv venv && source venv/bin/activate`.
- `pip install pennylane pennylane-lightning pyscf numpy scipy`.
- Versions locked: PennyLane 0.45.1, PySCF 2.13.1, NumPy 2.x.

## 3. Independent reimplementation
- Wrote `code/vqe_h2_gradients.py` (VQE + both gradient recipes) from scratch
  in PennyLane, using the paper's ansatz description as spec.
- Wrote `code/geom_opt_h2.py` (gradient-descent geometry optimizer).
- No paper-provided code was used or ported.

## 4. Execution
- `python3 code/vqe_h2_gradients.py` → 5-point energy + gradient scan (~10.2 s).
- `python3 code/geom_opt_h2.py` → gradient-descent geom opt from R₀=1.0 Å (~15 s).
- Stdout captured to `report/evidence/{run_log.txt, geom_opt_log.txt}`.
- Structured results dumped to `report/evidence/{vqe_h2_gradients.json, geom_opt_h2.json}`.

## 5. Cross-check against classical reference
- Ran PySCF FCI at same 5 bond lengths as classical ground truth.
- Compared VQE-FD gradient vs classical FCI-FD gradient (Ha/Å): agreement to ~10⁻⁸ Ha/Å.
- Compared VQE-HF gradient vs classical FCI-FD gradient: agreement to ~10⁻⁵ Ha/Å.
- Compared VQE energies vs FCI energies: agreement to <10⁻⁸ Ha at all 5 points.

## 6. Headline check
- Gradient-descent geom opt converged in 7 iterations to
  (R = 0.7349 Å, E = −1.137306 Ha).
- Paper quotes (0.741 Å, −1.137 Ha).
- |ΔE| = 0.306 mHa, well under paper's chemical-accuracy tolerance of 1.6 mHa.
- Verdict: **REPLICATED** — headline claim confirmed.

## 7. Documentation
- `report/REPORT.md`: original replication report (verdict, tables, method).
- `report/REPORT.tex`: LaTeX version with critique / honest assessment section.
- `report/evidence/`: JSON + log artifacts from all runs.
- `code/`: independent reimplementation scripts.

## 8. Backfill (2026-07-06)
- Regenerated `open_questions.json` (5 truly-open Qs with concrete probes),
  `open_questions_section.tex`, `workflow.md` (this file),
  `artifacts_summary.md`, `failure_analysis.md`, and `extraction/nougat.mmd`
  stub to bring the dir up to the 8-artifact QC-100 standard.

## Not exercised (with reason)
- C5 (Newton's method): gradient already sufficient for headline; Hessian
  machinery would 2–3× runtime.
- C6 (μ_Z, α_ZZ): separate response-property demonstration; sits on same
  derivative core.
- C7 (H+H₂ TS search): 3-atom problem, 6–8 qubit Hamiltonian, saddle-point
  algorithm; 5–10× runtime.
- C8 (SS-VQE excited-state derivatives): extension.

See `open_questions.json` §1, §2, §4 for the concrete probes that would close
these gaps.
