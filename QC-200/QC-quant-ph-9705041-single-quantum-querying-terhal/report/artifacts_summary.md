# Artifacts Summary — quant-ph/9705041 (Terhal & Smolin) Replication

Inventory of every artifact produced/pulled during this replication, with
sizes (bytes) and first-16 hex of the SHA-256 for spot-checkable provenance.

## 8-artifact completion bar (per REPLICATION_DIR_STANDARD_2026-07-05.md)
| # | Required artifact | Path | Size | SHA-256 (16) | Status |
|---|---|---|---:|---|---|
| 1 | Original PDF | `paper.pdf` | 142,309 | `d0d45b414f90996e` | present |
| 2 | Marker extraction | `extraction/marker.md` | 42,680 | `d17cbd762fc47f0e` | present (pdftotext fallback, labeled) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | 25,775 | `345bcb481d92a58f` | present (pdftotext fallback, labeled) |
| 4 | Detailed LaTeX report | `report/REPORT.tex` | 11,487 | `65b8d286e884fc22` | present (verdict = REPLICATED) |
| 5 | 5 open questions | `report/open_questions.json` | 5,604 | `612a6f9ea2110e0f` | present (each with basis + next_steps) |
| 6 | Workflow + tools + effort | `report/workflow.md` | 3,577 | `a430e39bc27be4f6` | present |
| 7 | Artifacts summary (this file) | `report/artifacts_summary.md` | — | — | present |
| 8 | Failure analysis | `report/failure_analysis.md` | — | — | present |

## Evidence files (real simulation outputs)
| Path | Size | SHA-256 (16) | Description |
|---|---:|---|---|
| `report/evidence/bv_single_query.py` | 6,980 | `2ef3666c74527242` | BV single-query circuit, n=4 sweep of all 16 databases |
| `report/evidence/bv_results.json` | 4,381 | `5f0919a4dd459c8f` | Per-y exact + shot success probabilities |
| `report/evidence/coin_weighing.py` | 3,280 | `2acd4122f0a8f23e` | Coin-weighing n=4 HW1 + n=8 (256-database sweep) |
| `report/evidence/coin_weighing_results.json` | 1,106 | `8cf5fc4f0a7d222e` | Coin-weighing per-case success rates |

## Working intermediates
| Path | Size | SHA-256 (16) | Description |
|---|---:|---|---|
| `work/paper.pdf` | 142,309 | `d0d45b414f90996e` | Downloaded arXiv PDF (identical to `paper.pdf`) |
| `work/paper.txt` | 25,376 | `49d5ddd82e73b162` | `pdftotext` default extraction |
| `work/paper_layout.txt` | 42,297 | `aa3bca26af3000dc` | `pdftotext -layout` (source for Marker fallback) |
| `work/paper_raw.txt` | 25,243 | `d07c0107a7ab8c7a` | `pdftotext -raw` (source for Nougat fallback) |

## Run traces
- BV run (16 databases, n=4): all 16 lines "OK P_exact=1.000000 P_shots=1.0000" in stdout; captured in `report/evidence/bv_results.json` — see `min_exact_success_prob` = `max_exact_success_prob` = `mean_shot_success_prob_4096` = 1.0.
- Coin-weighing n=8 (256 databases): `n_recovered_with_p_ge_0.999` = 256; `min_p` = `mean_p` = 1.0.

## External references
- arXiv: <https://arxiv.org/abs/quant-ph/9705041>
- Published: Phys. Rev. A 58, 1822 (1998), DOI 10.1103/PhysRevA.58.1822
- Ancestor algorithm: Bernstein & Vazirani, STOC 1993 / SIAM J. Comput. 26 (1997)

## Environment
- Host: CherryRd (Darwin 25.3.0, x64)
- Python 3.14 in `.venv/`
- qiskit 2.5.0 · qiskit-aer 0.17.2 · numpy 2.5.1
- All Argo/LLM inference (none required this pass): would use `http://localhost:44497/v1` key=stevens if needed.
