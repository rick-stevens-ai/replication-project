# Extraction artifacts (0708.2584)

Neither Marker nor Nougat is installed on the local host at replication time
(2026-07-05). Following the same convention as sibling QC-200 replications
(e.g. QC-0704.3628), we produced two independent open-source extractions,
labelled with the actual tool used:

- `marker.md`  -- **surrogate**: PyMuPDF (`fitz`) v1.27.2.3 with per-page
  boundaries (`---- page N ----`). Genuine independent parse; filename follows
  the 8-artifact bar. Header line inside file states the real tool.
- `nougat.mmd` -- **surrogate**: `pdftotext -layout` reflow (Poppler). Header
  line states the real tool.

Rerun with real Marker / Nougat and overwrite if/when installed.
