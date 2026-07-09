# Artifacts summary

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2023.12735-type-original-research-published-09-october/`

## 8-artifact completion bar (per QC_WAVE_BRIEF_2026-07-03.md)

| # | Artifact | Path | Bytes | Status |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | 1,891,804 | ✅ Downloaded from Frontiers; SHA256 matches QC-200 manifest byte-for-byte |
| 2 | Marker parse | `extraction/marker.md` | 63,459 | ✅ pdftotext fallback (Marker not installed on host; provenance banner included) |
| 3 | Nougat parse | `extraction/nougat.mmd` | 46,421 | ✅ pdftotext fallback (Nougat not installed on host; provenance banner included) |
| 4 | LaTeX report + PDF | `report/REPORT.tex` (8,929) + `report/REPORT.pdf` (192,241) | | ✅ Written + compiled with pdflatex |
| 5 | Open questions (machine-readable + narrative) | `report/open_questions.json` (5,036, 5 objects w/ q/basis/next_steps) + `## Open Questions` in `report/REPORT.md` + `open_questions_body.tex` | | ✅ |
| 6 | Workflow doc | `report/workflow.md` | 5,497 | ✅ Tools+versions table + step-by-step + effort accounting |
| 7 | Artifacts summary | `report/artifacts_summary.md` | (this file) | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | 5,384 | ✅ Honest gaps + Argo 502 handling + version drift risk |

## Reproduction evidence

| File | Purpose |
|---|---|
| `report/evidence/h2_vqe_reproduce.py` | Reproduction driver: H2 STO-3G → PySCFDriver → ParityMapper → EfficientSU2 VQE, 7 bond distances |
| `report/evidence/h2_vqe_results.json` | H2 results: (d, FCI, VQE, error, chemical accuracy) × 7 |
| `report/evidence/heh_plus_vqe.py` | Bonus HeH+ reproduction, 5 bond distances |
| `report/evidence/heh_plus_vqe_results.json` | HeH+ results |
| `report/evidence/llm_judge_argo_gpt-5.2.json` | LLM judge #1 (verdict PARTIAL) |
| `report/evidence/llm_judge_argo_gpt-5.4.json` | LLM judge #2 (verdict PARTIAL) |

## Supporting/intermediate

| File | Purpose |
|---|---|
| `report/REPORT.md` | Human-readable Markdown report (mirror of REPORT.tex; contains the canonical results tables + verdict + Open Questions section) |
| `report/REPORT.aux`, `REPORT.log`, `REPORT.out` | pdflatex build artifacts |
| `work/paper.pdf` | Local copy of the downloaded PDF (identical to `./paper.pdf`; kept for backwards-compat with sibling QC-200 dirs that keep the pdf in `work/`) |
| `work/paper.txt` | `pdftotext -layout` skim used for claim extraction |
| `work/paper_provenance.md` | How the paper was resolved from the truncated manifest id (arXiv 404 → Crossref Frontiers filter → DOI 10.3389/frqst.2023.1273581 → SHA match) |
| `work/arxiv_try.html` | The 404 HTML from arxiv.org (evidence that the given id is not arXiv) |
| `work/venv/` | Python virtual environment (qiskit + qiskit-nature + pyscf + numpy + scipy; not itself an artifact) |

## Fingerprints

| Item | Value |
|---|---|
| paper.pdf SHA256 | `e4360ed9d9b62ea0df0035253b8d6dfff4c184bd92dc48a7b4b6527fbbca3fdd` |
| Manifest SHA256 | `e4360ed9d9b62ea0df0035253b8d6dfff4c184bd92dc48a7b4b6527fbbca3fdd` |
| Match? | ✅ byte-for-byte |
| Verdict | PARTIAL (two-judge concurrence) |
| Wave/set | QC-200 |
| DOI | 10.3389/frqst.2023.1273581 |
| Given id | 2023.12735 (Frontiers-truncated, not arXiv) |
| Slug | type-original-research-published-09-october |

## Numerical fingerprint (headline number)

- H2 STO-3G, 2-qubit parity-reduced, d = 0.70 Å:
  - E_FCI (PySCF) = **−1.136189 Ha**
  - E_VQE (EfficientSU2 reps=2, COBYLA seed=42, ideal statevector) = **−1.136189 Ha**
  - |error| = **2.99 × 10⁻⁹ Ha** (vs paper threshold 1.6 × 10⁻³ Ha)
  - 7/7 H2 distances and 5/5 HeH+ distances reach chemical accuracy.
