# Artifacts Summary — QC-2105.01063 pulse-efficient CR

**Paper:** Earnest, Tornow, Egger (2021). *Pulse-efficient circuit
transpilation for quantum applications on cross-resonance-based
hardware.* arXiv:2105.01063.
**Set:** QC-100. **Verdict:** REPLICATED.

## Artifact index

| # | Path | Type | Purpose |
|---|------|------|---------|
| 1 | `report/REPORT.md` | narrative | Original replication report (pre-existing). |
| 2 | `report/REPORT.tex` | LaTeX | Formal report with critique + open-Q import. |
| 3 | `report/open_questions.json` | JSON list | 5 open questions (structured). |
| 4 | `report/open_questions_section.tex` | LaTeX | Rendered open-Q section. |
| 5 | `report/workflow.md` | Markdown | Reproducible env + step sequence. |
| 6 | `report/artifacts_summary.md` | Markdown | This file. |
| 7 | `report/failure_analysis.md` | Markdown | Honest scope / gaps / risks. |
| 8 | `extraction/nougat.mmd` | text | Paper-text extraction stub. |
| — | `code/replicate.py` | Python | Single-script replication (~330 LOC). |
| — | `report/evidence/C1_rzz_sweep.json` | JSON | Per-θ metrics (12 pts). |
| — | `report/evidence/C2_qaoa_sweep.json` | JSON | Per-(γ,β) metrics (25 pts). |
| — | `report/evidence/summary.json` | JSON | Headline reduction numbers. |

## Headline results

- **C1 (RZZ(θ) sweep):** median relative-error reduction **+42.5 %**;
  peak **55 %** at θ≈1.21 (paper: "up to 50 %"). Matches.
- **C2 (K4 QAOA):** max-abs-deviation reduction **+35.4 %**
  (paper 11-node: 38 %). Pulse-θ reduction **19–49 %** across
  γ grid (paper: 42–52 %). Matches within a few pp.

## Scope

- **Exercised:** C1 (RZZ fidelity, coherence-limited noise) and C2
  (QAOA cut-error + schedule-time). Headline claims: **matched**.
- **Not exercised:** C3 (SU(4) generalisation), C4 (calibration-free
  hardware validation), pulse-level Fig. 2 curves. Hardware-only
  content is out of laptop scope.

## Compute

- CPU only, ~7 s wall.
- Endpoint policy: no LLM endpoints used; pure Qiskit sim.
