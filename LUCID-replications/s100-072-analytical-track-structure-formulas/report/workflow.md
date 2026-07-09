# Workflow — s100-072 (Analytical track-structure formulas)

**Paper:** Kundrát et al., Sci. Rep. 10:15775 (2020). DOI 10.1038/s41598-020-72857-z. CC-BY 4.0.

**Replicator lane:** LUCID (Ollie, uicgpu-eligible; here CPU-only sufficed).
**Compute used:** Local CPU on CherryRd (Python 3, numpy, matplotlib). No MC, no GPU.
**Endpoint policy:** free endpoints only (Argo Opus 4.7 for reasoning; pdftotext/pdftoppm/tesseract for OCR fallback).

## Stage 1 — Ingest

1. Confirm PDF present at `source/paper.pdf` (1.16 MB, 11 pages, Scientific Reports formatting; CC-BY 4.0 so redistribution allowed within replication artifact).
2. First-pass text extraction: `pdftotext -layout source/paper.pdf ocr/paper.txt` (836 lines).
3. Second-pass targeted OCR: `pdftoppm -r 400 -f 3 -l 3 source/paper.pdf tmp_page3` then `tesseract tmp_page3-3.ppm page3_txt` — used to nail down the literal bracketing of Eqs. (1) and (2), which the first-pass `pdftotext` slightly garbled around the fraction bar.

## Stage 2 — Structure the paper's deliverable

The paper's deliverable is not a dataset; it is **two closed-form equations plus 540 fit parameters** across 9 ions × 3 channels × 5 damage classes. Structure the reproduction around that:

- Eq. (1) → SB, SSB (Lorentzian-dip form, plateau minus power-law minus log-Lorentzian).
- Eq. (2) → DSB, DSB clusters, DSB sites (power-law rise with logistic overkill).
- Table 1 → parameters for Eq. (1). 135 values.
- Table 2 → parameters for Eq. (2). 405 values.

## Stage 3 — Transcribe parameter tables

Both tables were transcribed by hand (visual inspection of PDF + cross-check against the OCR text). `N.A.` entries in the paper were converted to `NaN` in Python; `yield_eq1` and `yield_eq2` skip any term whose parameter set contains a NaN. This faithfully implements the paper's own convention.

## Stage 4 — Implement in Python

`code/reproduce.py` (~16 KB):

- `yield_eq1(LET, p1, p2, p3, p4, p5)` — Eq. (1), with NaN-skip on terms.
- `yield_eq2(LET, p1, p2, p3, p4, p5)` — Eq. (2), same convention.
- Parameter dictionaries keyed by `(ion, damage_class, channel)` → 540 entries.
- Per-figure plotting: for each of 5 damage classes, plot 9 ions × 3 channels (solid/dashed/dotted).
- Acceptance-probe block: compute quoted numerical claims (low-LET SB total, DSB peak, DSB direct/indirect split at low LET, etc.) and log to `evidence/console.log`.

## Stage 5 — Regenerate figures

Run `python3 code/reproduce.py`. Produces:

- `figures/fig1_SB.png` — reproduction of paper Fig. 1 (SB vs LET, 9 ions × 3 channels).
- `figures/fig2_SSB.png` — Fig. 2 (SSB).
- `figures/fig3_DSB.png` — Fig. 3 (DSB).
- `figures/fig4_DSBclusters.png` — Fig. 4 (DSB clusters).
- `figures/fig5_DSBsites.png` — Fig. 5 (DSB sites).

Symbols (PARTRAC MC datapoints) are not drawn because the underlying MC output is not published in the paper. Fitted curves are recovered exactly (same equation, same parameters → same curve, by construction).

## Stage 6 — Acceptance probes (quantitative)

Sampled at LET = 0.3, 1, 3, 10, 30, 100, 300, 1000 keV/µm; 10 rows per (ion, channel, damage class) written to `evidence/yield_samples.tsv` (135 rows × 10 columns of yields). Console-log the 10 numerical claims from paper body text and check each against the reproduction (all pass at 1–3%).

## Stage 7 — Verdict

The verdict is **REPLICATED (analytical-scope)**:
- 5/5 figures reproduced.
- 540/540 fit parameters transcribed and used.
- 10/10 body-text numerical claims recovered to 1–3%.

The verdict is **not upgraded to FULL-VALIDATED** because no independent MC (Geant4-DNA, TRAX, KURBUC) was run to cross-check the fits. That is a separate multi-week study, out of scope for this dir. See `failure_analysis.md` for the honest scope caveat.

## Stage 8 — Report + backfill

- `report/REPORT.md` (original, prose).
- `report/REPORT.tex` (LaTeX version, same content with critique section formalized).
- `report/open_questions.json` + `report/open_questions_section.tex` (5 grounded open questions with next-steps).
- `report/workflow.md` (this file).
- `report/artifacts_summary.md` (file inventory + sizes).
- `report/failure_analysis.md` (honest what-did-NOT-happen critique).
- `extraction/nougat.mmd` (stub — nougat OCR not required for this paper since pdftotext+tesseract were sufficient; stub documents the decision).
