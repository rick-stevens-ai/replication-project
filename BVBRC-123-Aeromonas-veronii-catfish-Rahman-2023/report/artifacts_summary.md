# Artifacts Summary — BVBRC-123

## 8 Mandatory Artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Requirement | Location | Status |
|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` (2,264,853 B, Europe PMC OA render of PMC10636080) | ✅ |
| 2 | `extraction/marker.md` | `extraction/marker.md` (pdftotext fallback; marker server not on-demand available) | ✅ |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` (pdftotext fallback; nougat server not on-demand available) | ✅ |
| 4 | `report/REPORT.tex` | `report/REPORT.tex` (LaTeX version with same claim-by-claim structure) | ✅ |
| 5 | `report/open_questions.json` (5 heavy-duty Qs, each with q/basis/next_steps) + `## Open Questions` in REPORT.md | `report/open_questions.json`; `## Open Questions (Q1..Q5)` section at bottom of `report/REPORT.md` | ✅ |
| 6 | `report/workflow.md` (workflow + tools/codes + effort) | `report/workflow.md` | ✅ |
| 7 | `report/artifacts_summary.md` (this file) | `report/artifacts_summary.md` | ✅ |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✅ |

## Additional Standard Files (from wave brief)

| File | Purpose | Present |
|---|---|---|
| `report/REPORT.md` | Main narrative report | ✅ |
| `report/brief.md` | 1-paragraph what/why | ✅ |
| `report/attempt_log.md` | Chronological log | ✅ |
| `report/artifact_harvest.md` | Every artifact pulled | ✅ |
| `report/evidence/replication_metrics.json` | Structured evidence for LLM-judge | ✅ |
| `work/` | Code + downloaded data + intermediate | ✅ (~15 MB total) |

## Data Downloaded (persistent in `work/`)

| Item | Size | Source |
|---|---|---|
| GCA_026738955.1 assembly FASTA | 4.56 MB | NCBI Datasets v2 |
| GCF_026738955.1 (RefSeq + PGAP annotation) | 3.81 MB zip | NCBI Datasets v2 |
| TH0426 reference | 1.46 MB zip | NCBI Datasets v2 |
| B565 reference | 1.35 MB zip | NCBI Datasets v2 |
| FDAARGOS_632 reference | 1.34 MB zip | NCBI Datasets v2 |
| paper.txt (extracted) | 29 KB | pdftotext |
| abricate output (5 databases) | ~43 KB | local abricate 1.4.0 |
| pubmlst_result.json | ~500 B | pubMLST REST |
| fastani.tsv | ~500 B | local fastANI |
| skani.log | ~500 B | local skani |

## Compute Used
- Local (CherryRd), no GPU, no uicgpu. Wall clock ~30 min end-to-end.
- Free endpoints only: NCBI Datasets v2, pubMLST REST, Europe PMC, Argo local (via cherryrd litellm aggregator).
- Zero paid API calls; zero Anthropic/OpenAI/OpenRouter direct.
