# Artifacts summary

Inventory of every file produced (or downloaded) for this replication, with traces.

## Required 8-artifact bar (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Present | Notes |
|---|---|---|:---:|---|
| 1 | Original PDF | `paper.pdf` | ✅ | 10 pp., 731094 bytes, SHA256 `d511c3f0...b8fd4f1` verified against the given hash |
| 2 | Marker parse | `extraction/marker.md` | ✅ | Fallback: pdftotext-layout output with an honest header (no central QC Marker corpus exists) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ | Fallback: pdftotext-layout output with an honest header (no central QC Nougat corpus exists) |
| 4 | Detailed LaTeX report | `report/REPORT.tex` + `report/REPORT.pdf` | ✅ | Compiles cleanly to 4-page PDF |
| 5 | Open-questions JSON + Markdown section | `report/open_questions.json` + `## Open Questions` in `REPORT.md` | ✅ | 5 non-superficial questions, each with `q`, `basis`, `next_steps` |
| 6 | Workflow doc | `report/workflow.md` | ✅ | 10-step workflow + tool table + compute footprint + explicit "what was NOT done" list |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ | (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | Honest analysis of the Hadamard mismatch + Argo 502 + Marker/Nougat substitution |

## Complete file inventory (excluding venv + `__pycache__`)

### Top-level
- `paper.pdf` — canonical PDF, SHA-verified.

### `work/` (downloads + intermediates)
- `paper.pdf` (working copy)
- `paper.txt` — pdftotext-layout extraction (473 lines)
- `paper_provenance.md` — full ID-resolution trail
- `crossref_1.json` — first (failed) Crossref query with wrong filter
- `crossref_2.json` — successful Crossref query returning the single Frontiers hit
- `venv/` — Python 3.13 venv (numpy 2.5.1, scipy 1.18.0, qiskit 2.5.0). Excluded from inventory counts.

### `extraction/`
- `marker.md` — fallback (see #2 above), 51 KB
- `nougat.mmd` — fallback (see #3 above), 51 KB

### `report/`
- `REPORT.md` — 14 KB Markdown report (verdict, claims, methods, results, Open Questions)
- `REPORT.tex` — 10 KB LaTeX source
- `REPORT.pdf` — 217 KB compiled 4-page PDF
- `REPORT.aux`, `REPORT.log`, `REPORT.out` — pdflatex build artifacts (kept for audit)
- `workflow.md` — 6 KB workflow narrative
- `artifacts_summary.md` — this file
- `failure_analysis.md` — friction / gaps
- `open_questions.json` — 5 JSON objects `{q, basis, next_steps}`

### `report/evidence/` (code + real outputs)
- `adiabatic_qft_gates.py` — 15 KB, the main replication code (numpy statevector, Eqs. 3–5, 10, 12 literal, sweep of 5 phases, 4 basis + 5 random 2-qubit inputs, QFT composition sanity check, convergence sweep)
- `adiabatic_qft_results.json` — 4 KB, machine-readable results per-trial fidelity
- `run_output.log` — 3 KB, stdout of the main run
- `debug_hadamard.py` — 857 B, single-input diagnostic that revealed the Hadamard anomaly
- `hadamard_variants.py` — 2 KB, 4-way sign-variant sweep
- `hadamard_variants.log` — 2 KB, run output of the variant sweep
- `llm_judge.py` — 5 KB, Argo-judge caller (falls back through 3 URLs, uses `argo:gpt-5.2`)
- `llm_judge_response.json` — 7 KB, full judge JSON with the PARTIAL verdict (confidence 0.86) and justification
- `llm_judge.log` — 3 KB, judge-call stdout

## Traceability

- Every numerical claim in `REPORT.md` §4 is directly reproducible by rerunning `adiabatic_qft_gates.py` in the venv; the exact numbers are also serialized in `adiabatic_qft_results.json`.
- Every LLM-judge word in `REPORT.md` §5 is present verbatim in `llm_judge_response.json` under `response_content`.
- The paper-identity claim is byte-verifiable by rerunning `sha256sum paper.pdf` and comparing with `d511c3f043cc25c9a5aad3c09d229cfbf20ebb246199b10a41c1223d5b8fd4f1`.
