# PARSER PROVENANCE — OSTI 2217719

## Source
- **PDF:** `2217719.pdf` (Hartanto et al., 2024, *Annals of Nuclear Energy* 196, 110236)
- **Local file:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/2217719-SCALE-depletion-capabilities-for-molten-salt/2217719.pdf`
- **Size / pages:** 2.73 MB, 10 pages

## Parser used (re-pass, 2026-06-23)
- **Tool:** `pdftotext` (Poppler) version 26.06.0, `/usr/local/bin/pdftotext`
- **Flags:** `-layout` (preserves columnar layout so Tables 1–3 stay tabular)
- **Output:** `results/repass/paper.txt` (869 lines, plain UTF-8)
- **Reproduce:** `pdftotext -layout 2217719.pdf results/repass/paper.txt`

## Notes / caveats
- `pdftotext -layout` emits one Poppler `Syntax Warning: Invalid number of shared object groups` to stderr; output text is intact (verified by reading Tables 1, 2, 3 and equations 17–21 cleanly).
- Math symbols (subscripts/superscripts, Greek letters) render as best-effort Unicode (e.g., `𝜆`, `233 Pa`); numeric values and units are preserved.
- For numeric extraction (rates, k, pcm, days, masses) we read directly from the layout text.
- No OCR was needed (the PDF has embedded text). No AI summarization was used to extract paper claims; all claims below are pulled verbatim from `results/repass/paper.txt`.

## Pass-1 provenance (historical, prior pass)
- Original Phase 1/Phase 2 work used a different (un-documented) extraction path. The pass-1 deliverables (`replication/replication/code/...`, `data/...`, `figures/...`) are preserved unchanged in this re-pass.
