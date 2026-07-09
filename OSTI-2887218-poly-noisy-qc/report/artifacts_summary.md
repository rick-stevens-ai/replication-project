# Artifacts summary — OSTI 2887218

## What is here

| Artifact | Location | Size / Rows | Notes |
|---|---|---|---|
| Paper PDF | `paper.pdf` | 1,202,652 bytes, 31 pp. | Fetched from `https://www.osti.gov/servlets/purl/2887218` via uicgpu proxy |
| Text extraction (marker fallback) | `extraction/marker.md` | 2,227 lines | `pdftotext -layout`; the `pdf` MCP tool was blocked by credit exhaustion + Dropbox path restriction |
| Text extraction (nougat) | `extraction/nougat.mmd` | 31 pages, MMD | `facebook/nougat-small` on uicgpu |
| Algorithm 1 code | `work/replication.py` | ~350 LOC | Independent implementation of paper's Algorithm 1 with per-layer local factorisation |
| RMS driver | `work/rms_experiment.py` | ~60 LOC | Runs 12 random circuits × 5 γ × 5 ℓ = 300 sims |
| Dev sanity code | `work/dev_verify.py`, `work/dev_schrod_pauli.py` | ~150 LOC combined | Used to isolate bugs B2, B3, B4 |
| Numerical evidence (V1, V3) | `report/evidence/results.json` | ~15 KB | Convergence table + poly-n scaling table |
| Numerical evidence (V2) | `report/evidence/rms.json` | ~5 KB | RMS-over-ensemble table |
| Run logs | `report/evidence/run.log`, `report/evidence/rms.log` | ~10 KB | Full stdout from the two experiments |
| Report (markdown) | `report/REPORT.md` | ~14 KB | Full replication report |
| Report (LaTeX) | `report/REPORT.tex` | ~11 KB | Section-by-section LaTeX version of the report |
| Brief | `report/brief.md` | 1 paragraph | For dashboards/rollups |
| Attempt log | `report/attempt_log.md` | Chronological | Timestamped log of the whole session |
| Artifact harvest | `report/artifact_harvest.md` | Table | Every data / code source touched |
| Open questions | `report/open_questions.json` | 5 Q&A | Ground in observations from THIS replication |
| Workflow doc | `report/workflow.md` | Table | Pipeline + tools + effort |
| Failure analysis | `report/failure_analysis.md` | 4 bugs | Root cause + fix for each bug caught |

## Reproduction one-liner

```bash
scp work/replication.py    uicgpu:/tmp/osti-2887218/
scp work/rms_experiment.py uicgpu:/tmp/osti-2887218/
ssh uicgpu 'cd /tmp/osti-2887218 && python3 -u replication.py && python3 -u rms_experiment.py'
```

Total wall time: ~90 seconds. No external dependencies beyond numpy.
