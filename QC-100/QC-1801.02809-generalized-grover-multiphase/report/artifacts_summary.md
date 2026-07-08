# Artifacts Summary

**Paper:** arXiv:1801.02809 (Byrnes, Forster, Tessler 2018)
**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1801.02809-generalized-grover-multiphase/`
**Wave:** QC-100. **Verdict:** REPLICATED.

## Files

### Paper source
- `work/1801.02809.pdf` — original paper.
- `work/1801.02809.txt` — plain-text extraction (source for claim identification).

### Extraction
- `extraction/nougat.mmd` — Nougat OCR stub (backfilled 2026-07-06; original
  replication used the plain-text `.txt` extraction, not Nougat).

### Code
- `code/generalized_grover.py` — v1: SVD-based construction of Eq. 12
  (superseded, retained for reference).
- `code/generalized_grover_v2.py` — v2 (canonical): H-diagonalization construction
  of Eq. 12; continuous-time + gate iteration in numpy and Qiskit Aer; standard
  Grover anchor.
- `code/debug_construction.py` — debugging harness for the eigenpair
  identification step.

### Data
- `data/v2_summary.json` — full quantitative results (curves, peaks, spectrum,
  claim booleans) from the canonical v2 run.
- `data/naive_run.json` — v1 output: naive-init gate iteration curve.
- `data/constructed_run.json` — v1 output: constructed-init curve.
- `data/standard_grover.json` — v1 output: textbook single-target Grover anchor.

### Logs
- `logs/run2.log` — captured stdout of v2 canonical run (full P_T(k) tables).

### Report (root)
- `report/REPORT.md` — canonical human-readable replication report (2026-07-03).
- `report/REPORT.tex` — LaTeX version, with honest critique section (2026-07-06).
- `report/open_questions.json` — 5 truly-open questions with basis + next_steps
  (bare JSON list).
- `report/open_questions_section.tex` — LaTeX rendering of the 5 open questions,
  `\input{}` at end of REPORT.tex.
- `report/workflow.md` — stage-by-stage workflow log.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique of scope, gaps, and limits.

## Claim → evidence map

| Claim | Evidence file | Key number |
|---|---|---|
| C1 (Eq.12 cont. P_T = 1 at t = π/(2 c_1)) | `data/v2_summary.json`, `logs/run2.log` | 1.0000 at t=2.526 (predicted 2.533) |
| C2 (gate iter, P_T ≈ 1 at k ≈ 3) | `data/v2_summary.json` | 0.9991 at k=3 (numpy = Qiskit Aer) |
| C3 (naive init peak ~ 0.3) | `data/naive_run.json`, `logs/run2.log` | 0.30 at k=34 |
| C4 (spectrum 1 ± c_n structure) | `data/v2_summary.json` | 4 distinct c_n pairs + 1 near-degenerate |
| C5 (standard Grover P_T ≈ 1 at k ≈ (π/4)√D) | `data/standard_grover.json` | 0.9992 at k=4 (predicted 4.44) |

## Bit-level cross-check
- `peak_P_T_constructed_gate_numpy`  = 0.99908
- `peak_P_T_constructed_gate_qiskit` = 0.99908
- Δ = 0 to 6 decimals → Qiskit reduction faithful to direct math.

## Backfill provenance (2026-07-06)
- No re-simulation; all numbers preserved from 2026-07-03 run.
- No paid endpoints; local Qiskit Aer only during original run.
- Verdict preserved: **REPLICATED**.
