# Artifacts summary

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9906059-quantum-fourier-transform-implementation/`

## 8 mandatory artifacts (brief 2026-07-05)

| # | Path | Present | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | ✅ | 220 kB, arXiv:quant-ph/9906059v1 (Weinstein/Lloyd/Cory 1999) |
| 2 | `extraction/marker.md` | ✅ | MarkItDown fallback (Marker model weights not installed on host; see `failure_analysis.md`) |
| 3 | `extraction/nougat.mmd` | ✅ | Hand-marked `pdftotext` dump with LaTeX math delimiters, flagged as Nougat stand-in |
| 4 | `report/REPORT.tex` | ✅ | Full section-by-section report + Verdict = REPLICATED for algorithmic claims |
| 5 | `report/open_questions.json` + `## Open Questions` in report | ✅ | 5 grounded open questions with `q`, `basis`, `next_steps` |
| 6 | `report/workflow.md` | ✅ | Timeline, tools, versions, work estimate |
| 7 | `report/artifacts_summary.md` | ✅ | This file |
| 8 | `report/failure_analysis.md` | ✅ | Honest friction / residual gaps |

## Code + evidence

| Path | Purpose |
|---|---|
| `report/evidence/qft_replication.py` | Full replication driver (Qiskit) |
| `report/evidence/results.json` | Machine-readable results for every claim |
| `work/paper.txt` | `pdftotext -layout` dump used for skim + nougat stand-in |
| `.venv/` | Isolated Python env (Qiskit 2.5.0, NumPy 2.5.1, MarkItDown) |

## Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9906059-quantum-fourier-transform-implementation
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit numpy markitdown
python report/evidence/qft_replication.py
# Expected last lines:
#   n=3:  H=3/3  CP=3/3  max amp err=1.42e-15  vs Qiskit err=0.00e+00
#   n=4:  H=4/4  CP=6/6  max amp err=3.78e-15  vs Qiskit err=0.00e+00
#   n=5:  H=5/5  CP=10/10 max amp err=5.62e-15 vs Qiskit err=0.00e+00
#   Eq. 4 QFT_4 matrix: match=True  err=1.15e-16
```
