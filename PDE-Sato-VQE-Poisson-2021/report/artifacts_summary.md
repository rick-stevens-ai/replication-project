# Artifacts Summary

Complete inventory of files in this replication dir with what each contains.

## Root
| File | Purpose |
|---|---|
| `paper.pdf` | Sato et al. 2021 arXiv preprint (v1), the source of truth. |

## `extraction/`
| File | Purpose |
|---|---|
| `marker.md` | pdftotext-layout text extraction (marker.md project-convention mirror; marker binary not available locally). |
| `nougat.mmd` | Same, nougat.mmd mirror. |

## `work/`
| File | Purpose |
|---|---|
| `paper.txt` | Raw `pdftotext -layout` extraction (1224 lines). |
| `vqe_poisson.py` | Independent implementation: gate primitives, Poisson linear system, cost function, L-BFGS-B driver, full sweep for n∈{2,3,4,5} × {dirichlet, periodic}. |
| `test_gates.py` | Unit tests for the gate primitives (endianness probe, CNOT probe, ansatz overlap sanity, Poisson matrix sanity). |
| `vqe_n5_deep.py` | Best-of-3 multistart study at n=5 Dirichlet — reproduces Fig. 4's <0.01 target. |
| `verify_o1_cost.py` | Full Pauli decomposition of A and A² for n=2..5, counts non-trivial terms → confirms the O(n)-vs-O(1) structural gap. |
| `judge.py` | LLM-judge harness. Prompts Argo `gpt-5.2` (fallback for the broken Opus routes today) with the results summary and asks for a verdict. |

## `report/`
| File | Purpose |
|---|---|
| `REPORT.md` | Full replication report: paper summary, claims table (C1..C8 with type + testable + tested + result), method (12 numbered steps), results-vs-paper tables, verdict, file index, open questions. **Verdict: REPLICATED.** |
| `REPORT.tex` | LaTeX section-by-section report with what worked / what didn't per paper section (cost function, ansatz, trace-distance, norm recovery, O(1) scaling, iteration scaling, periodic/Neumann BC). |
| `brief.md` | 1-paragraph what/why (WAVE-brief-shaped). |
| `attempt_log.md` | Chronological log of what was done, what worked, what failed. |
| `artifact_harvest.md` | Every public artifact pulled: URL, size, notes; includes the wrong-arXiv-ID triage. |
| `artifacts_summary.md` | This file — inventory of everything with per-file purpose. |
| `workflow.md` | Pipeline diagram, tools/versions, effort estimate, compute footprint. |
| `failure_analysis.md` | Everything that went wrong or needed a fix, categorized. |
| `open_questions.json` | 5 heavy-duty open research questions each `{q, basis, next_steps}`. |

## `report/evidence/`
| File | Purpose |
|---|---|
| `results_summary.json` | Per-n mean/max trace_distance, quantum & classical norms, iteration counts, wall time. Both Dirichlet and periodic BC. |
| `n5_dirichlet_3restart.json` | n=5 Dirichlet best-of-3 restarts: per-trial ε_tr list, mean, max, norms. |
| `n5_full_solutions.json` | Full ψ_opt, u_quantum, u_ref vectors for every n=5 trial (both BCs). |
| `o1_cost_analysis.txt` | Pauli-term counts for A and A² at n=2..5, with structural interpretation. |
| `run.log` | Console log of the main sweep (per-n line prints). |
| `judge_raw.json` | Full Argo API response for the LLM judge call. |
| `judge_response.json` | Parsed verdict JSON: verdict, confidence, core_claims_reproduced, reasoning, one_line_summary. |

## 8-artifact completion bar

| # | Required artifact | Local file | Status |
|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` | ✅ |
| 2 | `extraction/marker.md` | `extraction/marker.md` | ✅ (pdftotext fallback) |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` | ✅ (pdftotext fallback) |
| 4 | `report/REPORT.tex` | `report/REPORT.tex` | ✅ |
| 5 | `report/open_questions.json` + `## Open Questions` in REPORT | `report/open_questions.json` + REPORT.md §6 | ✅ |
| 6 | `report/workflow.md` | `report/workflow.md` | ✅ |
| 7 | `report/artifacts_summary.md` | this file | ✅ |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✅ |

All 8 present.
