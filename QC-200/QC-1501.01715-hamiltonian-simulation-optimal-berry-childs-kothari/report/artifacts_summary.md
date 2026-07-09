# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1501.01715-hamiltonian-simulation-optimal-berry-childs-kothari/`

## 8 required artifacts (Rick 2026-07-05 completion bar)

| # | Artifact | Path | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` | arXiv:1501.01715v3, 256 KB, fetched 2026-07-05 |
| 2 | `extraction/marker.md` | `extraction/marker.md` | pdftotext fallback (Marker not installed; header notes provenance honestly) |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` | pdftotext + LaTeX headers for the 3 main theorems (Nougat not installed) |
| 4 | `report/REPORT.tex` | `report/REPORT.tex` | Detailed section-by-section LaTeX report with claims table, methods, results-vs-paper tables, verdict |
| 5 | `report/open_questions.json` | `report/open_questions.json` | 5 open questions, each `{q, basis, next_steps}`; also mirrored in REPORT.tex `## Open questions` |
| 6 | `report/workflow.md` | `report/workflow.md` | End-to-end workflow, tools+versions table, work-effort estimate |
| 7 | `report/artifacts_summary.md` | this file | inventory + traces |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | Honest failure/friction/gap analysis |

## Evidence & code

Under `report/evidence/`:

- `bck_lcu_replication.py` — main numerical harness (LCU-of-Bessel + Trotter-2 baseline).
- `plot_results.py` — generates `convergence.png`.
- `results.json` — machine-readable results (Experiments A, B, C + comparison).
- `convergence.png` — two-panel figure: (a) LCU truncation error vs k, (b) k(ε) scaling vs paper's log/loglog prediction.

## Intermediates

Under `work/`:

- `paper.pdf` — fetched arXiv PDF (mirror of top-level artifact 1).
- `paper.txt` — `pdftotext -layout` output, 1273 lines. Source for the extraction stubs.

## Traces (commands actually run)

```bash
# 1. Fetch
curl -sL https://arxiv.org/pdf/1501.01715 -o work/paper.pdf
# 2. Skim
pdftotext -layout work/paper.pdf work/paper.txt
grep -n -i -E "theorem|complex|queries|O\(τ" work/paper.txt
# 3. Numerical replication
python3 report/evidence/bck_lcu_replication.py
# 4. Plot
python3 report/evidence/plot_results.py
```

## Provenance of extraction files

Both `extraction/marker.md` and `extraction/nougat.mmd` include a top-of-file HTML/comment note stating:
- Marker/Nougat were not installed on this host.
- The central `_LUCID100_ADMIN/marker_md_uicgpu_20260622/` and `marker_vs_nougat_20260622/` corpora do not contain 1501.01715 (checked).
- The files are pdftotext-derived proxies; no fabricated tokenisation, no fabricated equation LaTeX beyond the three theorems transcribed by hand from the paper for the Nougat stub.

This is the honest fallback per the QC wave brief's "else run" clause; a full uicgpu Marker/Nougat run for a single paper was not booked (small-OCR → uicgpu rule).
