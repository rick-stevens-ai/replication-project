# Artifacts Summary — Jurrus-APBS-2017 replication

## The 8-artifact bar (Rick 2026-07-05 standard)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Paper PDF | `paper.pdf` (1.71 MB) | ✅ |
| 2 | Marker extraction | `extraction/marker.md` (555 lines) | ✅ |
| 3 | Nougat extraction | `extraction/nougat.mmd` (415 lines) | ✅ |
| 4 | LaTeX detailed report | `report/REPORT.tex` | ✅ |
| 5 | Open questions (5 non-superficial) | `report/open_questions.json` + `## Open Questions` in REPORT.md | ✅ |
| 6 | Workflow + tools + effort | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | ✅ |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Additional supporting artifacts

- `report/brief.md` — 1-paragraph what/why summary
- `report/REPORT.md` — full markdown report (13 KB)
- `report/attempt_log.md` — chronological log
- `report/artifact_harvest.md` — full pull-list with URLs + sizes
- `report/evidence/` — 12 files: logs, inputs, PQRs, potential stats JSON, LLM judge output
- `work/` — 15 files: raw PDBs, PQRs, APBS inputs, DX grids (34 MB total)

## Verdict

**PARTIAL** — mainstream mg-auto multigrid workflow (Fig 1 of paper) fully reproduced end-to-end on paper's own demo protein (1FAS); PB-AM / PB-SAM / TABI-PB / geometric-flow / graph-theory pKa headline new solvers not individually exercised. Independent LLM judge (argo:gpt-5.2): coverage 0.55, agreement 0.75.

## Numerics summary

| System | Config | Total ELEC energy (kJ/mol) | Grid | Wall time |
|---|---|---|---|---|
| 1FAS | LPBE, 0M | 1.0959×10⁵ | 129×97×129 | 2.6 s |
| 1FAS | NPBE, 0.15M | 1.0957×10⁵ | 129×97×129 | 3.8 s |
| 1CRN | LPBE, 0M | 3.5009×10⁴ | 97³ | 1.5 s |
| 1CRN | LPBE, 0.15M | 3.5005×10⁴ | 97³ | 1.3 s |

Debye length at 0.15 M NaCl: **7.86 Å** (matches theory: √(εε₀kT / 2N_A e² I) ≈ 7.87 Å).

LPBE↔NPBE relative error on 1FAS: **< 0.02 %** (confirms linearized approximation validity in this regime).
