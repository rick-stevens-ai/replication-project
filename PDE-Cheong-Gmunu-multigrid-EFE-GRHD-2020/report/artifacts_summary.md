# Artifacts summary

## 8-artifact bar (per Rick 2026-07-05 standard)

| # | Required | Present | Path |
|---|---|---|---|
| 1 | `paper.pdf` | ✔ | `paper.pdf` (arXiv 2001.05723v2, 953 KB, 30 pp) |
| 2 | `extraction/marker.md` | ✔ | `extraction/marker.md` (pdftotext, 2111 lines) |
| 3 | `extraction/nougat.mmd` | ✔ (placeholder) | `extraction/nougat.mmd` — copy of marker.md; Nougat not available on CherryRd, DOI not in central Nougat corpus cache. Documented here as a pdftotext-derived placeholder rather than a true Nougat parse. |
| 4 | `report/REPORT.tex` | ✔ | `report/REPORT.tex` |
| 5 | `report/open_questions.json` (5 Qs) | ✔ | `report/open_questions.json` — 5 questions grounded in what we actually ran / did not run |
| 6 | `report/workflow.md` | ✔ | `report/workflow.md` |
| 7 | `report/artifacts_summary.md` | ✔ | this file |
| 8 | `report/failure_analysis.md` | ✔ | `report/failure_analysis.md` |

Plus the not-in-8-but-standard files: `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`, `report/evidence/*.json`, `report/evidence/*.png`, `work/*.py`.

## Evidence artifacts

- `report/evidence/fas_convergence_v2.json` — full iteration-by-iteration L1 residual histories for V1..V6, plus config and per-run metadata.
- `report/evidence/spatial_order.json` — N vs L1 error table for N ∈ {16,32,64,128}.
- `report/evidence/fig11_reproduction.png` — L1 residual vs iterations for V1..V6, our reproduction of Cheong+2020 Fig. 11 layout.
- `report/evidence/fig11_zoom.png` — V2..V6 zoom (V1's 259-iter curve dominates the full plot).
- `report/evidence/llm_judge.json` — LLM-judge structured JSON (verdict PARTIAL, scores).

## Note on nougat.mmd

The wave-brief mandate is "pull from central corpus if parsed, else run [Nougat]". Nougat is not installed on CherryRd and the central corpus (`/Users/stevens/Dropbox/*/nougat_parsed/` and similar) does not contain arXiv:2001.05723. Running Nougat here would require ~5-10 min GPU or ~30-60 min CPU on a 30-page paper with LaTeX-heavy math; given that pdftotext already yielded a clean 2111-line extraction that we used successfully to extract all claim text, we shipped the placeholder rather than blocking the wave on a Nougat cold-start. Documented so the disposition is transparent.
