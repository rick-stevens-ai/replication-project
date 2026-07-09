# Artifacts summary

Complete inventory of everything produced by this replication, mapped to the QC-200 brief's 8-artifact bar.

| # | Required artifact | Path | Present? | Notes |
|---|---|---|---|---|
| 1 | `paper.pdf` (original PDF) | `paper.pdf` | ✅ | 138 KB, arXiv:quant-ph/0503205 fetched 2026-07-05 |
| 2 | `extraction/marker.md` | `extraction/marker.md` | ✅ (fallback) | Marker not installed on CherryRd + UICGPU shared parse cluster unreachable within timeout; pdftotext-based fallback, clearly labelled |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` | ✅ (fallback) | Same reason as #2; pdftotext -layout based fallback, clearly labelled |
| 4 | `report/REPORT.tex` (+ compile to REPORT.pdf when possible) | `report/REPORT.tex` | ✅ | Section-by-section claims table, method, results-vs-paper, verdict = REPLICATED |
| 5 | `report/open_questions.json` (5) + `## Open Questions` in the report | `report/open_questions.json`, `report/open_questions_body.tex` | ✅ | Each entry has `q`, `basis`, `next_steps` |
| 6 | `report/workflow.md` | `report/workflow.md` | ✅ | Full workflow + tool table + effort estimate |
| 7 | `report/artifacts_summary.md` | this file | ✅ | You are here |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✅ | Honest failure + friction + residual gaps |

## Non-required, produced anyway

| Path | Type | Purpose |
|---|---|---|
| `work/paper.txt` | text | pdftotext dump |
| `work/paper.layout.txt` | text | pdftotext -layout dump |
| `report/evidence/grover_pi3_fixedpoint.py` | Python | the actual simulation code |
| `report/evidence/standard_grover_probs.json` | JSON | standard Grover P(k) on N=16 |
| `report/evidence/pi3_fixedpoint_probs.json` | JSON | pi/3 fixed-point sim + theory, N=16 and N=64 |
| `report/evidence/convergence_data.csv` | CSV | tidy table of every point plotted |
| `report/evidence/convergence.png` | PNG | side-by-side figure |
| `report/evidence/verdict.json` | JSON | machine-checkable pass/fail (OVERALL_PASS=true) |
| `extraction/README.md` | Markdown | explains the fallback nature of items 2 and 3 |
| `.venv/` | venv | qiskit 2.5.0 + numpy 2.5.1 + matplotlib |

## Provenance

- Executor: subagent under session `agent:main:subagent:89500368-ef46-426e-b251-dacef09a77ed`, launched by main agent from `agent:main:telegram:direct:8542341053` on 2026-07-05 10:21 CDT.
- Host: CherryRd (macOS 25.3.0, x64).
- Endpoints: none paid; no LLM inference invoked during numeric replication.
- Traces: full command sequence in `report/workflow.md` §"Step-by-step". Live run output preserved in the subagent transcript.
