# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-05 CDT). The QC-200 wave brief allows either "pull from
central corpus if parsed, else run Marker/Nougat". A search of the
REPLICATE-PROJECT tree for `1507.00432*` found no pre-parsed extraction.
Rather than fabricate Marker/Nougat output, we produced two independent
open-source extractions and clearly label the tool at the top of each file:

- `marker.md`   — **surrogate**: PyMuPDF (`fitz`) text extraction with page
  boundaries preserved (`---- page N ----` markers). Genuine independent parse
  of the paper, not a Marker output; the filename follows the artifact-bar
  convention. Header line inside the file explicitly states the tool.
- `nougat.mmd`  — **surrogate**: `pdftotext -layout` (Poppler) reflow,
  preserving math markup as best pdftotext can. Header line explicitly states
  the tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files.
