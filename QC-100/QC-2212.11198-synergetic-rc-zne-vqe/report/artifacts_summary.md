# Artifacts Summary — QC-2212.11198

Target directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2212.11198-synergetic-rc-zne-vqe/`

## Original artifacts (pre-backfill)

| Path | Type | Purpose |
|------|------|---------|
| `report/REPORT.md`                     | Markdown | Full independent replication write-up (paper summary, claims table, method, results, judge scores, verdict) |
| `code/vqe_rc_zne.py`                   | Python   | Full replication driver: H₂ Hamiltonian, deep HEA ansatz, coherent+depol noise model, RC twirl (N_rand=30), Mitiq ZNE, 4-way sweep, JSON+CSV output |
| `code/llm_judge.py`                    | Python   | Argo multi-judge (GPT-4.1 + Claude-Opus-4.7 + Gemini-2.5-Pro) verdict script |
| `report/evidence/results.json`         | JSON     | Full per-ε results incl. Hamiltonian, ansatz metadata, all 4 executor energies, elapsed time, package versions |
| `report/evidence/results_table.csv`    | CSV      | Machine-readable results table for downstream aggregation |
| `report/evidence/llm_judge.txt`        | Text     | Full judge transcripts (2 successful, 1 upstream 502) |
| `logs/run6.log`                        | Text     | Real simulation stdout (final successful run) |
| `work/2212.11198.pdf`                  | PDF      | Source paper (arXiv, CC-BY 4.0) |
| `work/2212.11198.txt`                  | Text     | `pdftotext -layout` extraction for grep-friendly reference |

## Backfill artifacts (2026-07-06)

| Path | Type | Purpose |
|------|------|---------|
| `report/REPORT.tex`                    | LaTeX    | Publication-form replication write-up with genuine critique section |
| `report/open_questions.json`           | JSON     | Bare list of 5 open-question objects (q / basis / next_steps), no wrapper |
| `report/open_questions_section.tex`    | LaTeX    | Same 5 open questions formatted as a `\section{Open questions}` block |
| `report/workflow.md`                   | Markdown | End-to-end procedural log (fetch → env → implement → run → judge → verdict → backfill) |
| `report/artifacts_summary.md`          | Markdown | This file — index of every artifact |
| `report/failure_analysis.md`           | Markdown | Honest critique of scope-vs-headline gap, ansatz substitution, noise-model coverage, judge coverage |
| `extraction/nougat.mmd`                | MMD stub | Placeholder for a future Nougat extraction of the paper's structured content (headline claim + Fig. 4 table); not run in this backfill (paper is short + already have full pdftotext) |

## Total count
- Original: 9 files
- Backfill: 7 files (this wave)
- **Grand total: 16 files**

## Reproducibility summary
- Runs in < 10 s on a laptop CPU.
- Free endpoints only (Argo judges are free per standing rule).
- No paid API calls at any point.
- Pinned deps: qiskit 2.5.0, qiskit-aer 0.17.2, mitiq 1.0.0, python 3.12.13.
