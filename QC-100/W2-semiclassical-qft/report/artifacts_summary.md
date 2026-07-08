# Artifacts Summary — W2-semiclassical-qft

**Set:** QC-100
**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/W2-semiclassical-qft/`
**Paper:** Griffiths & Niu, PRL **76**, 3228 (1996)
**Verdict preserved:** REPLICATED

## Files at replication time (2026-06-26, by Ollie)

| Path | Purpose |
|---|---|
| `REPORT.md` (top level) | Primary human-readable replication report (kept in place). |
| `replicate.py` | Correct implementation of both coherent iQFT and semiclassical measure-and-feed-forward, plus the sweep harness. Pure numpy. |
| `replicate_subagent_buggy.py` | Preserved buggy first-cut for provenance (bit-order convention error, TV~1.0). |
| `results.json` | Machine-readable table of the 8 experiments (φ, k, QFT estimate, semiclassical estimate, TV distance). |

## Files added at backfill time (2026-07-06, by Kukla)

| Path | Purpose |
|---|---|
| `report/REPORT.tex` | LaTeX version of the primary report with expanded critique section. |
| `report/open_questions.json` | Bare JSON list of 5 open questions with basis + concrete next_steps. |
| `report/open_questions_section.tex` | LaTeX include for open questions (referenced from REPORT.tex). |
| `report/workflow.md` | Step-by-step workflow of the replication and backfill. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Honest critique of what the replication does NOT establish. |
| `extraction/nougat.mmd` | Stub — Nougat MMD extraction was not performed (backfill placeholder). |

## Preservation
No pre-existing file was moved, deleted, or edited during backfill.
`REPORT.md` remains at the top level as the primary record.
