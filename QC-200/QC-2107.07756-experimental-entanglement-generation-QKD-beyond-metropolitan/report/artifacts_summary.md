# Artifacts inventory

All paths are relative to
`~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2107.07756-experimental-entanglement-generation-QKD-beyond-metropolitan/`.

## 8 required artifacts (per QC-200 brief)

| # | Path | Size | Description |
|---|------|------|-------------|
| 1 | `paper.pdf` | 850 KB | Original arXiv:2107.07756 v4 PDF (peer-reviewed Quantum 6, 822 (2022)) |
| 2 | `extraction/marker.md` | ~50 KB | Text extraction (pdftotext fallback; marker not installed centrally) |
| 3 | `extraction/nougat.mmd` | ~50 KB | Text extraction (pdftotext fallback; nougat not installed centrally) |
| 4 | `report/REPORT.tex` + `report/REPORT.pdf` | 14 KB / ~120 KB | Full section-by-section replication report with verdict |
| 5 | `report/open_questions.json` (+ `## Open Questions` in REPORT.tex) | ~4 KB | 5 grounded open questions with basis + next steps |
| 6 | `report/workflow.md` | ~5 KB | Comprehensive workflow, tools/versions, work estimate |
| 7 | `report/artifacts_summary.md` | this file | Inventory + traces |
| 8 | `report/failure_analysis.md` | ~4 KB | Honest failure analysis, friction, residual gaps |

## Evidence (code + outputs)

| Path | Description |
|------|-------------|
| `report/evidence/bbm92_key_rate.py` | ~400-line self-contained Python implementation of Eqs. (1)-(4). Uses only numpy/scipy. |
| `report/evidence/plot_results.py` | Matplotlib plotting: Fig 6 replication + distance rolloff |
| `report/evidence/outputs/summary.json` | Machine-readable headline results, constants used, Λ(λ) sanity, all five key-rate scaling comparisons, distance curve, CHSH S |
| `report/evidence/outputs/key_rate_vs_power.csv` | 40 rows: (scenario, spacing, n_pairs, pump_mW, dlam_nm, R_bps) |
| `report/evidence/outputs/key_rate_vs_distance.csv` | 5 rows: (distance_km, R_bps) |
| `report/evidence/outputs/fig6_replication.png` | Fig 6 replication with paper claim stars overlaid |
| `report/evidence/outputs/distance_replication.png` | Fiber distance rolloff |
| `report/evidence/run.log` | Full stdout log of latest bbm92_key_rate.py run |

## Intermediates

| Path | Description |
|------|-------------|
| `work/paper.txt` | 794-line pdftotext -layout extraction of paper.pdf (source of truth for text mining) |

## Provenance chain

Every number in REPORT.tex Section 4 (Results vs paper) traces to:
1. `summary.json` (machine-readable)
2. → written by `bbm92_key_rate.py` (~400 lines Python, no external deps beyond numpy/scipy)
3. → driven by constants extracted from `work/paper.txt` (which is `pdftotext -layout paper.pdf`)
4. → paper.pdf hash:

```
$ shasum -a 256 paper.pdf
(computed at REPORT.pdf compile time; see next section)
```

## Reproducibility

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2107.07756-experimental-entanglement-generation-QKD-beyond-metropolitan
python3 report/evidence/bbm92_key_rate.py   # writes outputs/*.{csv,json}
python3 report/evidence/plot_results.py     # writes outputs/*.png
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex   # writes REPORT.pdf
```

Total wall time ~1 min on M1 CPU. No GPU, no HPC, no network beyond the
initial arXiv PDF download.
