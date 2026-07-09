# Artifacts summary — QC-2504.01077 Double-Bracket QSP

Directory root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2504.01077-double-bracket-QSP-no-postselection/`

## 8 mandatory artifacts (Rick 2026-07-05 standard)

| # | Artifact | Path | Size | Notes |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ~1.30 MB, 2 phys pages | fetched from arxiv.org/pdf/2504.01077 |
| 2 | Marker parse | `extraction/marker.md` | 7,516 lines | **substituted with pdftotext -raw** (Python 3.14 wheel gap; documented in-file + failure_analysis §1) |
| 3 | Nougat parse | `extraction/nougat.mmd` | 4,187 lines | **substituted with pdftotext -layout** (same wheel gap; documented in-file + failure_analysis §2) |
| 4 | Detailed report | `report/REPORT.tex` (+ `REPORT.pdf`) | 11.4 KB TeX / 4-page PDF | section-by-section per-claim comparison, compiled cleanly with pdflatex |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | 4.8 KB JSON, 5 items | each item = {q, basis, next_steps}, grounded in numbers from this run |
| 6 | Workflow | `report/workflow.md` | 3.6 KB | timeline, tools/versions, effort estimate, reproduction quickstart |
| 7 | This inventory | `report/artifacts_summary.md` | this file | — |
| 8 | Failure analysis | `report/failure_analysis.md` | 5.4 KB | 8 numbered items, incl. Marker/Nougat substitution + a couple of interesting findings |

## Evidence + code (`report/evidence/`)
| File | Size | Role |
|---|---|---|
| `db_qsp.py` | 16 KB | full replication code — 4 experiments R1–R4, deterministic seed 20260705 |
| `run.log` | ~1.8 KB | captured stdout from `python db_qsp.py` |
| `results.json` | structured | every trial, every N, every step, every diagnostic — machine-readable |

## Intermediates (`work/`)
| File | Role |
|---|---|
| `paper.pdf` | duplicate of top-level for keeping work/ self-contained |
| `paper.txt` | `pdftotext -layout` output (4,187 lines) |
| `paper_raw.txt` | `pdftotext -raw` output (7,514 lines) |

## Environment
- Per-project venv `.venv/` (Python 3.14.6, numpy 2.5.1, scipy 1.18.0).
- No global installs, no paid API calls, no LLM inference used for the numerical verdict.
- Reproduction wall time: **16 ms**.

## Traceability
- Every number in `REPORT.tex` traces back to a specific line in `report/evidence/run.log` or a specific key in `report/evidence/results.json`.
- Every claim (C1–C4) has explicit paper-equation citation + explicit code lines in `db_qsp.py` (functions `synthesize_linear`, `group_commutator_approx`, `experiment_R1..R4`).
- Random seed hard-coded (`RNG = np.random.default_rng(20260705)`); results are byte-reproducible.

## Verdict
**REPLICATED** — see `REPORT.tex` §Verdict.
