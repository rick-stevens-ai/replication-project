# Artifacts Summary

## Paper artifact
| Path | Size | Description |
|---|---|---|
| `paper.pdf` | 175 050 B | Ambainis, "Quantum Search Algorithms", arXiv:quant-ph/0504012 (SIGACT News column, 12 pp, 2005). Fetched from `https://arxiv.org/pdf/quant-ph/0504012`. |
| `work/source.tar.gz` | 14 180 B | arXiv e-print source (gzipped .tex). Fetched from `https://arxiv.org/e-print/quant-ph/0504012`. |
| `work/sigact_arxiv.tex` | 28 644 B | Ungzipped LaTeX source of paper (interesting: paper was originally submitted with a `sigact_arxiv.tex` filename). |

## Extractions
| Path | Size | Tool |
|---|---|---|
| `extraction/paper.txt` | 40 347 B | `pdftotext -layout` (Poppler 25.03.0) |
| `extraction/marker.md` | 34 624 B | Marker surrogate: PyMuPDF 1.28.0 per-page dump (project convention) |
| `extraction/nougat.mmd` | 40 486 B | Nougat surrogate: pdftotext output with nougat-surrogate header (project convention) |

## Report
| Path | Size | Description |
|---|---|---|
| `report/REPORT.md` | 13 540 B | Full replication report with claims table, method, results, verdict, Open Questions Q1..Q5 |
| `report/REPORT.tex` | 10 250 B | LaTeX version with per-claim detailed writeup |
| `report/open_questions.json` | 5 751 B | 5 heavy `{q, basis, next_steps}` questions arising from THIS replication |
| `report/workflow.md` | 5 555 B | Chronological workflow, tools, versions, effort estimate |
| `report/artifacts_summary.md` | (this file) | This inventory |
| `report/failure_analysis.md` | see file | What went wrong during the replication and how it was fixed |

## Evidence (actual numerical outputs)
| Path | Size | Contents |
|---|---|---|
| `report/evidence/results.json` | 18 306 B | Complete per-experiment records (curves, per-N stats, scaling fits) |
| `report/evidence/summary.json` | 847 B | Compact log-log slope summary for each claim |
| `report/evidence/run_log.txt` | 4 159 B | Full stdout of `replication.py` run |
| `report/evidence/llm_judge.json` | 3 103 B | Parsed Argo Opus 4.8 verdict per claim + overall |
| `report/evidence/llm_judge.txt` | 3 094 B | Raw LLM response |

## Code
| Path | Size | Description |
|---|---|---|
| `work/replication.py` | 22 725 B | Full replication driver: Grover primitives, C1..C5 experiments, log-log fits |
| `work/extract_marker.py` | 668 B | Marker-surrogate extractor (PyMuPDF) |
| `work/llm_judge.py` | 7 409 B | LLM-judge caller (Argo Opus 4.8 via localhost:44497) |
| `work/venv/` | (large) | Python venv with qiskit 2.5.0 + qiskit-aer 0.17.2 + numpy 2.4.3 + pymupdf 1.28.0 |

## Public artifacts harvested
| URL | Size | Access | Verified |
|---|---|---|---|
| `https://arxiv.org/pdf/quant-ph/0504012` | 175 050 B | free, no auth | ✓ |
| `https://arxiv.org/e-print/quant-ph/0504012` | 14 180 B (gz) | free, no auth | ✓ |
| `http://localhost:44497/v1/models` | (JSON) | free (Argo proxy, key=stevens) | ✓ 44 models listed |
| `http://localhost:44497/v1/chat/completions` | (JSON POST) | free (Argo proxy, argo:claude-opus-4.8) | ✓ 60-sec judge call succeeded |

## What is NOT in the target dir
- No external data downloads (paper is entirely mathematical; no experimental
  datasets exist for this paper).
- No PDF regenerated from REPORT.tex (LaTeX build was not required by the brief;
  the .tex source is present and buildable with pdflatex if desired).
- No sibling-dir contamination (the pre-existing sibling
  `QC-quant-ph-0504012-quantum-search-algorithms-ambainis-survey/` was NOT touched;
  preserve-rule respected).
