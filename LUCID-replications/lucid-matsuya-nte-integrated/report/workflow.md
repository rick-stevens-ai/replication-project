# Workflow — Matsuya 2018 IMK model replication

## Steps
1. **Paper acquisition.** Downloaded CC-BY PDF from Sci Rep. Stored at
   `paper.pdf` (sha256 `eda2685eb056e546a68bfd2f937db32d79ee4796775cbd124078bb0b515659d8`)
   + supplement at `artifacts/MOESM1.pdf`. Text-layer extracted with
   `pdftotext` → `source-paper.txt` (57.8 KB) and `artifacts/MOESM1.txt`.
2. **Claim extraction.** Read paper end-to-end. Enumerated 10 explicit
   numeric claims spanning Eqs. 1–26 + Tables 1–2 + Figs. 2–5.
3. **Digitisation.** Hand-digitised the paper's Figs. 2 (survival),
   3 (DSB kinetics), 4 (CHO-K1 PARP), 5 (HRS deepening + LL max). Data
   arrays live in `code/reference_data.py`. Precision ±5–10 %.
4. **Model implementation.** Coded Eqs. 1–26 + SI in
   `code/imk_model.py` (pure NumPy/SciPy, CPU-only, no external deps
   beyond the standard scientific stack). Analytic closed forms used
   where possible; bounded-NLS (SciPy `trf`) for parameter refit.
5. **Figures + summary.** `code/make_figures.py` generates
   `figures/fig{0..6}_*.png` and dumps quantitative metrics to
   `results/summary.json`.
6. **Claim scoring.** Each claim scored REPLICATED / SPOT-CHECK /
   PARTIAL / CONTRADICTED against digitised data + paper text.
7. **Discrepancy triage.** Three paper-internal inconsistencies
   flagged (Claims 1, 5, 10) — likely typos or legend swaps. Tagged
   `paper-internal-inconsistency`, `paper-table-typo-suspect`,
   `paper-figure-legend-suspect` respectively.
8. **Backfill (2026-07-06).** Post-hoc generation of the 6 standard
   LUCID artifacts (REPORT.tex, open_questions.json, workflow.md,
   artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd)
   from the completed REPORT.md.

## Tools + versions
- Python 3.11+, NumPy 1.x, SciPy 1.x, Matplotlib 3.x (all CPU).
- `pdftotext` from poppler for text-layer extraction.
- Nougat GPU parse deferred (no GPU allocated during this run).
- No LLM in the loop for model coding; LLM only used for
  extraction/summarisation/reporting.
- Host: CPU-only replication (any modern laptop). Runtime ≈ 4 s.

## Work estimate
- Reading + claim extraction: ~2 h
- Digitisation (Figs. 2–5): ~2 h
- Coding IMK (Eqs. 1–26): ~4 h
- Figures + fits: ~2 h
- Reporting + triage of paper inconsistencies: ~2 h
- **Total: ~12 h wall clock** for the original replication.
- Backfill of 6 artifacts: ~30 min.

## Provenance
- No raw experimental data was accessed. All comparisons are
  digitised-paper vs. our-model.
- No public IMK source code was located as of 2026-05-28.
- All artifacts and code are entirely in this directory; nothing
  external is imported at replication time.
