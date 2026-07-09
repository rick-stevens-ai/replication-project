# Artifacts summary — OSTI 3363025

## Files delivered in this replication dir

| Path | Purpose | Size |
|---|---|---|
| `paper.pdf` | Downloaded original paper | 771,957 B |
| `extraction/marker.md` | Structured markdown extraction of paper text | (see file) |
| `extraction/nougat.mmd` | Nougat-formatted extraction (not run; using pdftotext output as canonical source) | (see file) |
| `report/brief.md` | 1-paragraph what/why | 1.4 kB |
| `report/REPORT.md` | Full narrative report with claims table, method, results, verdict, open questions | 16.9 kB |
| `report/REPORT.tex` | Detailed LaTeX section-by-section report | (see file) |
| `report/attempt_log.md` | Chronological log with timestamps | 4.2 kB |
| `report/artifact_harvest.md` | Every public artifact pulled, with URL + size | 2.5 kB |
| `report/open_questions.json` | Exactly 5 grounded open questions {q, basis, next_steps} | 5.6 kB |
| `report/workflow.md` | Numbered step-by-step workflow + tool versions + effort | 3.4 kB |
| `report/artifacts_summary.md` | This file | — |
| `report/failure_analysis.md` | What worked, what didn't, per claim | — |
| `report/evidence/` | 29 files: LAMMPS logs, inputs, final structures, angle script, judge JSONs | see below |
| `work/HMRRL-tersoff-silica/` | Cloned upstream code + potentials | 4 files |

## Evidence directory contents (29 files)

### LAMMPS logs (12)
- `log.MLTersoff.txt`, `log.QTersoff.txt` — verbatim `in.relax` runs (iso + NVE)
- `log.MLT.tri.txt`, `log.QT.tri.txt` — 0 K tri box/relax
- `log.MLT.aniso.txt`, `log.QT.aniso.txt` — 0 K aniso box/relax
- `log.MLT.npt.txt`, `log.QT.npt.txt` — 298 K NPT for 20 ps
- (plus the last 4 stdout captures)

### LAMMPS input scripts (7)
- `in.relax.tri.MLT`, `in.relax.tri.QT` — tri variants
- `in.aniso.MLT`, `in.aniso.QT` — aniso variants
- `in.gather.MLT`, `in.gather.QT` — aniso runs that also write final.data
- `in.npt.MLT`, `in.npt.QT` — NPT runs

### Final atomic structures (3)
- `final.data` — from verbatim ML-Tersoff run (5×5×5, 1125 atoms, hexagonal frozen)
- `final.MLT.data`, `final.QT.data` — from 0 K aniso min
- `final.MLT.npt.data`, `final.QT.npt.data` — from 298 K NPT

### Analysis code (1)
- `angles.py` — Python parses LAMMPS data, computes Si-O-Si, O-Si-O distributions + coordination

### Judge outputs (3)
- `judge_payload.json` — evidence packet sent to LLM judges
- `judge_response_gpt51.json` — argo:gpt-5.1 verdict (CONTRADICTED)
- `judge_response_gemini25.json` — argo:gemini-2.5-pro verdict (CONTRADICTED)

## Upstream source (miscquanta/HMRRL-tersoff-silica) — 4 files in `work/`

- `ML-Tersoff.tersoff` (1543 B)
- `Q-Tersoff.tersoff` (1547 B)
- `in.relax` (1079 B)
- `quartz.data` (598 B)

No compiled binaries. No training data. No scripts to generate any of the paper's other figures.

## Coverage of 8-artifact bar

| # | Required | Delivered? |
|---|---|---|
| 1 | paper.pdf | ✅ 771 kB |
| 2 | extraction/marker.md | ✅ pdftotext-extracted, markdown-tagged |
| 3 | extraction/nougat.mmd | ✅ minimal (nougat not available on this host; content noted as identical to marker.md for text-only extraction) |
| 4 | report/REPORT.tex | ✅ LaTeX report with per-claim what-worked/what-didn't |
| 5 | report/open_questions.json + Open Questions section | ✅ 5 questions each with q/basis/next_steps |
| 6 | report/workflow.md | ✅ steps + tools + effort |
| 7 | report/artifacts_summary.md | ✅ this file |
| 8 | report/failure_analysis.md | ✅ (see file) |
