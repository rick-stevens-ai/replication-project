# Artifacts Summary — QC-quant-ph-0011023 Watrous replication

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0011023-quantum-algorithms-solvable-groups/`

## 8 mandatory artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status | Notes |
|---|----------|------|--------|-------|
| 1 | Paper PDF | `paper.pdf` | ✅ | 13 pages, 174 KB, arXiv:quant-ph/0011023v2 |
| 2 | Marker parse | `extraction/marker.md` | ✅ (fallback) | Marker CLI not installed on CherryRd; pdftotext -layout fallback with clear disclaimer |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ (fallback) | Nougat CLI not installed on CherryRd; pdftotext fallback with clear disclaimer |
| 4 | LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf` if pdflatex compiles) | ✅ | Section-by-section, claims-by-claim; imports `open_questions_body.tex` |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` section imported into REPORT | ✅ | 5 questions, each with `q`, `basis`, `next_steps` |
| 6 | Workflow doc | `report/workflow.md` | ✅ | Timeline, tools+versions, design decisions, work estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | Honest gaps + oracle-ordering debugging story |

## Evidence artifacts (under `report/evidence/`)

| Path | Purpose |
|------|---------|
| `report/evidence/hsp_cyclic.py` | Full HSP + uniform-state + scaling code (~350 lines) |
| `report/evidence/dihedral_d4.py` | D_4 non-abelian solvable demo (~200 lines) |
| `report/evidence/results/results.json` | JSON with all HSP-cyclic + uniform-state + scaling numeric results |
| `report/evidence/results/d4_results.json` | JSON with D_4 uniform-state + coset-decomposition results |

## Work/staging (`work/`)

| Path | Purpose |
|------|---------|
| `work/paper.txt` | pdftotext (default layout, 665 lines) |
| `work/paper_layout.txt` | pdftotext -layout (structured columns, 646 lines) |
| `work/venv/` | Python venv containing qiskit 2.5.0, qiskit-aer, numpy |

## Reproducibility

- Full run: `cd <target_dir> && source work/venv/bin/activate && python report/evidence/hsp_cyclic.py && python report/evidence/dihedral_d4.py` (total ~90 s wall on CPU).
- Deterministic (fixed seeds throughout).
- Zero external network calls after PDF fetch.
- Zero paid endpoints or API calls.
