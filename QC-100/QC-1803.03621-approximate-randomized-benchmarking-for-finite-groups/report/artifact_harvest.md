# Artifact Harvest — arXiv:1803.03621

| Artifact | Source | Size | Notes |
|---|---|---|---|
| `1803.03621.pdf` | `https://arxiv.org/pdf/1803.03621` | 590,656 B | arXiv v2 (14 Aug 2018), 6 pages published J. Phys. A 2018 |
| `1803.03621.txt` | `pdftotext -layout` of the PDF | 82 KB | text extraction, 1793 lines |

**No external code or datasets available** — this is a pure-theory paper with in-paper numerical examples. Authors' code is not published to a public repo (checked arXiv metadata; no GitHub or Zenodo link). All simulation code is our own implementation from the paper's equations (esp. eq. 56 for noise, eq. 58 for Clifford generators, Definitions 22-23 for MU(d,n), Lemma 24 for channel structure).

## Files we generated

Under `work/`:
- `monomial_rb.py` (14.7 KB) — MU(d,n) group implementation + RB protocol + Table 1 replication driver
- `clifford_generator_rb.py` (10.2 KB) — 2-qubit Clifford generator RB + Table 3-style driver
- `compare_protocols.py` (7.9 KB) — three-protocol comparison on same channel
- `plot_results.py` (2.4 KB) — matplotlib figures
- `judge.py` (5.0 KB) — LLM-judge caller

Under `report/evidence/`:
- `results_monomial.json` — Table 1 replication data (all 6 (d, M) cells)
- `results_clifford.json` — Table 3-style Clifford RB data (3 p-values)
- `results_compare.json` — three-protocol comparison, all per-channel data
- `rb_three_protocols.png` — survival-curve plot
- `monomial_error_vs_d.png` — error-scaling plot
- `llm_judge_verdict.md` — Argo GPT-5.2 verdict
- `monomial_run.log`, `clifford_run.log`, `compare_run.log` — console logs from experiments
