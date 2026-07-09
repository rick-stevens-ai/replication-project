# Extraction Surrogates

Marker and Nougat are not installed on this host (CherryRd, 2026-07-05).
Per QC-200 wave convention (matches sibling replications), we provide
surrogates using freely available extractors:

- `marker.md` — PyMuPDF (fitz) full-text extraction, page-delimited.
- `nougat.mmd` — pdftotext -layout extraction (preserves 2-column column layout).

Both contain the full paper body sufficient for the replication task
(theorem statements, formulas, and character-table references).
Should Marker/Nougat later become available in the corpus manifest,
these files can be replaced with the canonical parses.
