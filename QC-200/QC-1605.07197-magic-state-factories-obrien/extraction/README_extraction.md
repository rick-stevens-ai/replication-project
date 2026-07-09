# Extraction artifacts — arXiv:1605.07197

**Paper:** O'Gorman & Campbell, "Quantum computation with realistic magic state factories," arXiv:1605.07197v2 (24 Dec 2016).

## Provenance

Neither Marker (VikParuchuri/marker) nor Nougat (facebookresearch/nougat) is installed in this environment as of 2026-07-05, and the central corpus at `~/Dropbox/REPLICATE-PROJECT/CORPUS-EXTRACTED/` does not exist. Following the precedent set by the sibling directory `QC-1612.02058-error-mitigation-short-depth/extraction/`, both `marker.md` and `nougat.mmd` are populated with a pdftotext-derived, lightly-cleaned linear extraction of `../paper.pdf`.

- **Backend:** pdftotext (Poppler)
- **Source PDF:** arXiv:1605.07197v2, 7.36 MB, 20 pages
- **Content fidelity:** structure/equations/tables are lossy. Section headings, prose, key equations, and Table I are captured. Fine LaTeX math markup is not preserved.
- **File layout:**
  - `marker.md` — pdftotext output with light Markdown headers added.
  - `nougat.mmd` — same source, mmd/tex-flavoured. (Since real Nougat is unavailable, this is a placeholder that flags itself as such.)

## Notes on the paper's authorship

The upstream QC-200 wave task originally listed the authors as "O'Brien, Fowler, Goerbig". This is **incorrect** — the actual arXiv:1605.07197 authors are **Joe O'Gorman (Oxford, Materials)** and **Earl T. Campbell (Sheffield, Physics & Astronomy)**. Following the QC brief's "trust arxiv id, verify authors from fetched PDF" rule, the reproduction is against the O'Gorman-Campbell paper. The directory name still contains "obrien" for stable path continuity, but the report clearly names the correct authors.
