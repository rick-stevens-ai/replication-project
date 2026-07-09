# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-05). The QC wave brief allows "pull from central corpus if
parsed, else run Marker/Nougat". A search of the local
`~/Dropbox/REPLICATE-PROJECT/` tree found no pre-parsed extraction for
`quant-ph/0406180`. Rather than fabricate Marker/Nougat output, we produced
two independent open-source extractions and clearly label the tool used:

- `marker.md`   — **surrogate**: PyMuPDF (`fitz`) text extraction with page
  boundaries preserved (`---- page N ----` markers). This is a genuine
  independent parse of the paper, not Marker output; the filename follows the
  QC-200 artifact-bar convention. Header line inside the file explicitly
  states the actual tool.
- `nougat.mmd`  — **surrogate**: `pdftotext -layout` reflow, preserving math
  markup as best pdftotext can. Header line explicitly states the actual tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files.
