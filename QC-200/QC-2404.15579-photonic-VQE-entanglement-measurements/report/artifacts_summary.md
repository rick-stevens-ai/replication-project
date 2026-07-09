# Artifacts inventory — arXiv:2404.15579 replication (QC-200)

All 8 mandatory artifacts per the wave brief (2026-07-05 REPLICATION_DIR_STANDARD).

| # | Artifact | Path | Present? | Notes |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` (also `work/paper.pdf`) | ✓ | 2 558 868 bytes, PDF v1.5, arXiv:2404.15579v1 (24 Apr 2024) |
| 2 | Marker parse | `extraction/marker.md` | ✓ (surrogate) | 32 864 bytes; poppler `pdftotext` surrogate — Marker not installed on host, provenance in `extraction/README.md`; QC-200 corpus norm |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✓ (surrogate) | 32 671 bytes; PyMuPDF `get_text` surrogate — Nougat not installed on host, provenance in `extraction/README.md`; QC-200 corpus norm |
| 4 | Detailed LaTeX report | `report/REPORT.tex` | ✓ | Section-by-section per-claim analysis, results tables, verdict; ~15 KB; also `report/REPORT.pdf` if pdflatex was available |
| 5 | Open questions (5, heavy-duty) | `report/open_questions.json` + `## Open Questions` section in report | ✓ | JSON: 5 objects with q/basis/next_steps; report inline via `report/open_questions_tex.tex` |
| 6 | Workflow doc | `report/workflow.md` | ✓ | Chronological steps + tool versions + work estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | ✓ | — |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ | Honest friction / gaps / non-replicated items |

## Evidence & traces

| Path | Kind | Description |
|---|---|---|
| `report/evidence/vqe_bell_replication.py` | code | Main replication — Parts A, B, C (28 KB) |
| `report/evidence/vqe_bell_refinements.py` | code | R1 (paper's HeH+ grouping) + R2 (tight Heisenberg VQE-E) (9 KB) |
| `report/evidence/results.json` | data | Full numerical output of the main run |
| `report/evidence/refinements.json` | data | Full numerical output of the refinements |
| `report/evidence/run.log` | log | Captured stdout of the main run |
| `report/evidence/refine.log` | log | Captured stdout of the refinements |
| `work/paper.pdf` | raw | Cached copy of the fetched PDF |
| `work/paper.txt` | raw | `pdftotext -layout` dump used for eq/reference extraction |
| `extraction/README.md` | doc | Surrogate provenance for artifacts 2 & 3 |

## Key numerical results at a glance

- **Heisenberg (H = XX + YY + ZZ)**: 3 Pauli bases → 1 Bell basis (66.7% reduction). VQE-P best = -2.998, VQE-E best = -3.000. Exact = -3.
- **HeH+ (R=0.9 Å, paper Appendix A)**: 9 Pauli strings → 4 QWC groups → 3 paper GC groups (25% reduction QWC→GC, matches paper exactly). Best VQE (paper 3-basis, 4000 shots each) = -5.7259 MJ/mol vs exact -5.7252 MJ/mol → error 0.7 mMJ/mol.
- **H2/STO-3G 4-qubit** (task-brief extension): 15 Pauli strings → 5 QWC → 2 GC (60% QWC→GC, 86.7% naive→GC). VQE-exact reaches -1.132721 Ha (FCI to <10⁻⁴ mHa).

## Verdict

**REPLICATED.** All three headline claims (basis reduction on Heisenberg; basis reduction on HeH+; energy accuracy under same shot budget) reproduce with high fidelity; extension to H2/STO-3G exceeds every threshold in the brief.
