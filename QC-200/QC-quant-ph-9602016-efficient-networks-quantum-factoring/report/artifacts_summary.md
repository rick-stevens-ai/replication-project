# Artifacts summary — QC-200 quant-ph/9602016

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9602016-efficient-networks-quantum-factoring/`

## 8 required artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Path | Size | Role |
| :- | :-- | :-- | :-- |
| 1 | `paper.pdf` | 490 992 B | Original PDF fetched from arXiv. |
| 2 | `extraction/marker.md` | 5 716 B | Structured markdown extraction (pdftotext + hand-formatted fallback; Marker not installed on host — noted in file). |
| 3 | `extraction/nougat.mmd` | 4 017 B | LaTeX/Mathpix-flavored extraction of the equations we exercise (Nougat not installed on host — noted in file). |
| 4 | `report/REPORT.tex` + `report/REPORT.pdf` | 13 864 B + 248 145 B (5 pages) | Detailed replication report with claims table, method, results-vs-paper table, verdict, and 5 open questions. |
| 5 | `report/open_questions.json` | 5 035 B | Five heavy-duty follow-on research questions, each with `q`, `basis`, and `next_steps`. Also present in REPORT.pdf §Open Questions. |
| 6 | `report/workflow.md` | ~4 KB | Comprehensive stage-by-stage workflow, tool versions, and effort estimate. |
| 7 | `report/artifacts_summary.md` | (this file) | This inventory. |
| 8 | `report/failure_analysis.md` | ~3 KB | Honest failure/friction analysis. |

## Evidence and traces

| Path | Purpose |
| :-- | :-- |
| `code/expn_7_15.py` | Qiskit implementation of Eq. (7.5) EXP N(x=7, N=15); the single script that produces every reproducible number in the report. |
| `logs/expn_7_15.log` | tee'd stdout of the simulation run. |
| `report/evidence/expn_7_15_result.json` | Machine-readable full result: lookup-table check for each a, entangled-state fidelity, gate/pulse counts, QFT y distribution, verdict flag. |
| `report/evidence/expn_7_15_circuit.txt` | ASCII circuit diagram of the Eq. (7.5) network as constructed in Qiskit. |
| `work/paper.txt` | pdftotext -layout of the paper (2 976 lines). |
| `work/paper_raw.txt` | pdftotext -raw of the paper (3 525 lines). |
| `.venv/` | Ephemeral Python 3.11 virtualenv with qiskit 2.5.0 / qiskit-aer 0.17.2 / numpy 2.4.6. |

## Reproducibility one-liner

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9602016-efficient-networks-quantum-factoring
source .venv/bin/activate
python code/expn_7_15.py
```

Expected final line of stdout:
```
all_claims_match_first_construction_Eq_7.5 = True
```
