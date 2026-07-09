# Workflow — LUCID-100 slot 67 (Friedland, Kundrát & Jacob 2012)

## Timeline
- **2026-06-09** — first pass by Ollie subagent; AMBER-KEEP verdict; provenance + smoke reduction complete.
- **2026-06-22** — deeper audit (this slot's REPORT.md); LET-sweep added; SPOT-CHECK verdict.
- **2026-06-25** — re-tiered to NO-GO under Rick's hard-ceiling rule (nothing quantitatively reproducible → NO-GO).
- **2026-07-06** — backfill run: added the 8-artifact standard files (REPORT.tex, open_questions.json, open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd stub). Preserves NO-GO verdict; flags queue mismatch (queue=REPLICATED, disk=NO-GO).

## Tools and versions used
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.x (system) | driver |
| numpy | latest via pip | array math |
| scipy | latest via pip | `optimize.curve_fit` bounded NLS |
| matplotlib | latest via pip | rejoining & LET-sweep plots |
| Semantic Scholar API | live 2026-06-09 | metadata + TLDR |
| OpenAlex API | live 2026-06-09 | 14-reference graph |
| Unpaywall API | live 2026-06-09 | OA status (confirms is_oa=false, no locations) |
| GitHub search | manual 2026-06-09 | PARTRAC source search (none found) |
| Ollie subagent | Argo Opus 4.7/4.8 | authoring + backfill |
| CherryRd | local mac | all compute |

## Codes written in-slot
1. `code/smoke_friedland2012.py` — 5-parameter biexponential-plus-labile analytical model + bounded NLS fit + 6 smoke checks.
2. `code/let_sweep_friedland2012.py` — Hill-saturation LET sweep over 8 LET points; 6 trend checks (4/6 pass).

## Codes / data NOT accessible
- PARTRAC source (Helmholtz Zentrum München, proprietary; no public mirror).
- Paper PDF (Taylor & Francis IJRB, DOI 10.3109/09553002.2011.611404; no preprint, S2 abstract elided).
- Precursor Friedland 2010 (RR1965) parameter tables — closed.
- Stenerlöw 2000 measured rejoining kinetics — closed.

## Effort estimate
| Item | Estimate |
|---|---|
| Wall clock (all phases combined) | ~2 person-hours (first pass) + ~2 person-hours (deep audit) + ~15 min (this backfill) |
| Compute time | sub-second per script; total <10 s |
| Agent steps (first + deep + backfill) | ~40–60 total tool calls |
| Lines of code written in-slot | ~350 (both scripts combined) |
| Runs of smoke script | 2 (initial + repro check) |
| Runs of LET sweep script | 1 |
| HPC used | none |
| Paid APIs used | none |

## Argo / model usage
- Metadata & authoring done via free Argo endpoint (localhost:44497, key=stevens) on Claude Opus 4.7/4.8.
- No paid inference calls.

## Data flow
```
S2/OpenAlex/Unpaywall  ─┐
                        ├─►  source/*.json + references_table.md
GitHub search (PARTRAC) ─┘

Literature-typical Co-60 γ + N-ion reference curves
        │
        ▼
 smoke_friedland2012.py ── scipy.curve_fit ──► smoke_fit_results.json + smoke_rejoining.png
        │
        ▼
 let_sweep_friedland2012.py ── Hill saturation ──► let_sweep_results.json + let_sweep.png
        │
        ▼
        REPORT.md (deep audit) → this backfill (REPORT.tex + support files)
```
