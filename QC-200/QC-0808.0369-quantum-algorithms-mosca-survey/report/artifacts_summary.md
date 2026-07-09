# Artifacts Summary — QC-0808.0369 Mosca survey replication

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0808.0369-quantum-algorithms-mosca-survey/`

## Required 8-artifact bar
| # | Artifact | Path | Status | Notes |
|---|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` (also `work/paper.pdf`) | ✅ present | arXiv 0808.0369v1, 515548 bytes |
| 2 | Marker extraction | `extraction/marker.md` | ✅ present (pdftotext -layout fallback) | Marker not installed; stanza calls this out |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✅ present (pdftotext -raw fallback) | Nougat not installed; stanza calls this out |
| 4 | REPORT.tex | `report/REPORT.tex` | ✅ present | Verdict SPOT-CHECK; claims C1..C6 table; results-vs-paper; Open Questions |
| 5 | Open questions | `report/open_questions.json` (5 items, each with q/basis/next_steps) + `Open Questions` section in REPORT.tex | ✅ present | 5 questions grounded in what we actually ran |
| 6 | Workflow doc | `report/workflow.md` | ✅ present | Steps + tools + versions + effort estimate |
| 7 | Artifacts summary | this file | ✅ present | Inventory of everything with traces |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ present | Honest gaps and friction log |

## Evidence + code
| Path | Kind | Content |
|---|---|---|
| `report/evidence/grover_N8.py` | source | Grover-on-N=8 statevector demo (140 LOC) |
| `report/evidence/grover_N8.log` | log | Full stdout of the run |
| `report/evidence/grover_N8_result.json` | result | Structured JSON: p_marked_simulation=0.9453125, matches theory to 1e-6 |
| `report/evidence/orderfinding_a7_N15.py` | source | Shor order-finding statevector demo (140 LOC), a=7, N=15, m=8 |
| `report/evidence/orderfinding_a7_N15.log` | log | Full stdout of the run |
| `report/evidence/orderfinding_a7_N15_result.json` | result | 4 peaks at k={0,64,128,192} each P=0.25, sum=1.0, r=4 recovered |

## Intermediates + fetched data
| Path | Kind |
|---|---|
| `work/paper.pdf` | duplicate of the fetched arXiv PDF (kept so the top-level `paper.pdf` and the `work/` tree stay consistent with sibling dirs) |
| `work/paper.txt` | pdftotext skim used to identify the two spot-check targets |
| `work/paper_layout.txt` | pdftotext -layout intermediate (source of `extraction/marker.md`) |
| `work/paper_raw.txt` | pdftotext -raw intermediate (source of `extraction/nougat.mmd`) |

## Environment traces
| Item | Value |
|---|---|
| Host | CherryRd (Darwin 25.3.0, node v24.14.1) |
| Python | 3.13 in local `.venv/` |
| Qiskit | 2.5.0 (via `pip install qiskit qiskit-aer numpy`) |
| LLM endpoint | none used for the reproduction itself |

## Verdict
**SPOT-CHECK** — both Qiskit reproductions match the closed-form theory Mosca quotes to machine precision. See REPORT.tex Section 4 (Results vs Paper) and Section 5 (Verdict) for full justification.
