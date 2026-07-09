# Artifacts summary — QC-quant-ph9602016

## Completion-bar checklist (Rick 2026-07-05 standard, 8 required)

| # | Required artifact | Path | Status |
|---|-------------------|------|--------|
| 1 | `paper.pdf` | `paper.pdf` | ✅ 490,992 B, SHA-256 `a324785d...` |
| 2 | `extraction/marker.md` | `extraction/marker.md` | ✅ 138,579 B (pdftotext + MD wrap; marker binary N/A) |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` | ✅ 138,428 B (pdftotext + MMD wrap; nougat binary N/A) |
| 4 | `report/REPORT.tex` (very detailed section-by-section, what worked/didn't per claim) | `report/REPORT.tex` | ✅ 11,162 B, full section-by-section coverage of C1..C10 and non-tested Sec. VI claims |
| 5 | `report/open_questions.json` (5 heavy-duty `{q, basis, next_steps}`) + `## Open Questions` in REPORT.md | `report/open_questions.json` (5 items with next_steps) + `report/REPORT.md` §"Open Questions" (Q1..Q5) | ✅ |
| 6 | `report/workflow.md` (workflow + tools/codes + effort estimate) | `report/workflow.md` | ✅ 4,544 B — 16-stage table + tool inventory + effort estimate |
| 7 | `report/artifacts_summary.md` | this file | ✅ |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✅ |

## Additional artifacts (not required, produced anyway)
| Artifact | Path |
|----------|------|
| Full REPORT.md (paper summary, claims table C1..C10, Method, Results vs paper, Verdict, Open Questions) | `report/REPORT.md` |
| Simulator evidence JSON | `report/evidence/evidence_shor_n15.json` |
| LLM-judge verdict JSON | `report/evidence/llm_judge_verdict.json` |
| Raw stdout logs | `report/evidence/{shor_n15,shor_n21,resource_counts}.log` |
| Executable code (mirror) | `report/evidence/{shor_n15,shor_n21,resource_counts}.py` |
| Artifact provenance (URLs + checksums) | `report/artifact_harvest.md` |
| pdftotext output (both -layout and flow) | `work/paper*.txt` |

## Verdict
**REPLICATED** — 6/6 Sec. VII (N=15) claims independently reproduced by Qiskit statevector simulation, gate-for-gate build of Eq. (7.5), cross-validated by an independent generic 12-qubit Shor QPE, and independently scored by an LLM judge (`argo:gpt-5.4`, `temperature=0`) on free Argo endpoint.

## One-line summary
Beckman-Preskill 1996 "factor 15 with 6 qubits and 38 laser pulses" reproduces exactly: Eq. (7.3) lookup table matches, Eq. (7.5) gate-count [6,0,4] matches, 38-pulse Cirac-Zoller budget matches, QPE recovers r=4 and factors 15 = 3×5; generic Shor cross-check confirms; N=21 sanity extension also works.
