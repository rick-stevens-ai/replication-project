# Artifacts inventory — QC-quant-ph-9705002 BHT replication

## The 8 mandatory artifacts

| # | Path | Bytes | What it is |
|---|---|---|---|
| 1 | `paper.pdf` | ~112 kB | Original arXiv PDF, quant-ph/9705002v1 (Brassard/Høyer/Tapp 1997) |
| 2 | `extraction/marker.md` | ~14 kB | Marker-format text extraction (pdftotext -layout fallback; Marker unavailable on Py 3.14) |
| 3 | `extraction/nougat.mmd` | ~10 kB | Nougat-format text extraction (pdftotext -raw fallback; Nougat unavailable) |
| 4 | `report/REPORT.tex` | ~12 kB | Detailed LaTeX report — abstract, method, results, verdict, per-claim table, open questions |
| 5 | `report/open_questions.json` | ~4 kB | 5 heavy-duty open questions with `{q, basis, next_steps}` fields |
| 6 | `report/workflow.md` | ~5 kB | Workflow narrative, tool versions, chronology, reproduce commands, effort estimate |
| 7 | `report/artifacts_summary.md` | (this file) | Inventory of everything produced + provenance |
| 8 | `report/failure_analysis.md` | ~5 kB | Honest failure/friction analysis and residual gaps |

## Supporting evidence (under `report/evidence/`)

| Path | What |
|---|---|
| `bht_collision.py` | Full BHT algorithm implementation with real Qiskit statevector Grover subroutine |
| `make_plot.py` | Log-log scaling plot generator |
| `bht_results.json` | Machine-readable results: per-N mean/median queries, success rate, Grover iterations, log-log fit slopes |
| `bht_scaling.csv` | Same data in CSV form (per-N row) |
| `bht_scaling.png` | Log-log plot: BHT vs classical vs N^{1/3}/√N reference lines |

## Intermediates (under `work/`)

| Path | What |
|---|---|
| `paper.txt` | Full pdftotext dump (used for skim) |

## Provenance & reproducibility signals
- **arXiv ID verified against fetched PDF:** authors match (Brassard/Høyer/Tapp), title matches ("Quantum Algorithm for the Collision Problem"), date matches (1 May 1997, v1). No mismatch between the assigned ID and the actual paper.
- **Deterministic seeds:** `base_seed=42`, per-(N, trial) offset `1000*N + t`. Any subsequent run of `bht_collision.py` will reproduce these numbers exactly.
- **No LLM contamination of numeric results.** Only the report prose was human/LLM-written; the JSON/CSV/PNG are pure Qiskit-simulation output.
- **Free-endpoint compliance:** no paid API called at any point; drafting used Argo Opus 4.7 at localhost:44497 (free).

## Central-corpus opt-in
This paper was NOT pre-parsed in the central corpus at replication time (checked `~/Dropbox/REPLICATE-PROJECT/parsed*`). If Marker/Nougat runs are eventually done centrally for arXiv:quant-ph/9705002, `extraction/marker.md` and `extraction/nougat.mmd` here can be transparently replaced by the higher-quality outputs; the numeric replication does not depend on the extraction quality.
