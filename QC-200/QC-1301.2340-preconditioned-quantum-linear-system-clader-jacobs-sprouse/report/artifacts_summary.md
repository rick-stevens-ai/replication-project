# Artifacts summary — arXiv:1301.2340

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1301.2340-preconditioned-quantum-linear-system-clader-jacobs-sprouse/`

## Required 8 artifacts

| # | Artifact | Path | Status | Bytes |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✓ present | 148,605 |
| 2 | Marker parse | `extraction/marker.md` | ✓ (pdftotext fallback with provenance note) | ~5 KB |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✓ (pdftotext + hand-normalised equations, provenance note) | ~2.7 KB |
| 4 | LaTeX report | `report/REPORT.tex` + compiled `report/REPORT.pdf` | ✓ compiled (5 pages) | 14 KB / 246 KB |
| 5 | Open questions | `report/open_questions.json` (+ § in report) | ✓ 5 substantive Qs | ~5 KB |
| 6 | Workflow | `report/workflow.md` | ✓ | ~4 KB |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✓ (this file) | — |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ | ~3 KB |

## Evidence + traces

| File | Purpose |
|---|---|
| `report/evidence/preconditioned_hhl_sim.py` | Full ~260-line reproduction script (numpy, deterministic) |
| `report/evidence/results.json` | Machine-readable results: 3 test cases × 2 preconditioners + 5-point scaling sweep |
| `report/evidence/results.txt` | Human-readable summary printed by the script |

## Work / intermediates

| File | Purpose |
|---|---|
| `work/paper.txt` | `pdftotext` dump of paper.pdf (source for extraction/*) |

## Reproducibility one-liner

```bash
python3 report/evidence/preconditioned_hhl_sim.py
```
Deterministic (seed 20260705). Runtime ~0.01 s. No network / no GPU / no LLM.

## Traces of the replication itself

- Paper fetch: `curl -sL -o paper.pdf https://arxiv.org/pdf/1301.2340`
- LaTeX compile: `pdflatex -interaction=nonstopmode REPORT.tex` (single pass, no errors)
- Total wall time end-to-end: ~9 minutes.
