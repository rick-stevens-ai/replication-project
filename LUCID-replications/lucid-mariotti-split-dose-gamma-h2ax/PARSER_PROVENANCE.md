# PARSER_PROVENANCE — Mariotti 2013 (PLOS ONE 8:e79541)

## Pass 2 (this pass, 2026-06-23)

**Canonical text source:** Marker (UICGPU 2026-06-22 run).

- Path: `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/c716b571dcc2a9dc124bc81c581721d7ae697990/c716b571dcc2a9dc124bc81c581721d7ae697990.md`
- Length: 238 lines of Markdown, 9 extracted figure JPEGs (`_page_*_Figure_*.jpeg`, `_page_*_Picture_*.jpeg`).
- Equations (1)–(4) are rendered cleanly by Marker including the piecewise
  brace in eq.(4) and the Greek/Latin split between first/second exposure
  parameters. All numeric headline values used here were re-verified against
  Marker output (e.g. peak text "~21 and 37 foci/cell", "12 hours" recovery
  time, "~25 foci per cell nucleus per Gy", "<5 hrs" perturbation window).
- **No re-parse needed for Table S1** — the numerical fit parameters live in
  the supplementary DOCX (`data/TableS1.docx`) downloaded directly from PLOS,
  not in the main-text PDF. Marker output of the main text does not modify
  those values; both passes use identical Table S1 numbers.

## Pass 1 (original, 2026-05-30)

- pdftotext -layout of `data/paper.pdf`
- Hand digitisation of Fig 1A and Fig 5 (saved as `data/digitized_fig1A.csv`,
  `data/digitized_fig5.csv`).
- Table S1 read directly from `data/TableS1.docx` (PLOS supplementary file
  s001).

## Diff

I diffed the relevant equations and headline numbers between pdftotext output
and Marker output. **No discrepancies in numeric content** that affect the
replication. Marker preserves the LaTeX-y equation layout more faithfully
(Greek letters and the piecewise definition of eq.(4) survive the conversion),
but the actual numeric values used by the model are identical.

## Figure images

Marker emitted 9 figure JPEGs for this paper. They are mirrored into
`data/marker_figs/` for this pass. Pass-1 used `pdfimages`-extracted PNGs
(`data/paper_img-00*.png`), which are kept for reproducibility but
**superseded** by the Marker JPEGs for any new digitisation.
