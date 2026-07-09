# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-05). No pre-parsed extraction was found in the
REPLICATE-PROJECT tree (`corpus/marker/1411.5729*` and `corpus/nougat/1411.5729*`
both empty). Rather than fabricate Marker/Nougat output, we produced two
independent open-source extractions and clearly label the tool:

- `marker.md`   -- **surrogate**: PyMuPDF (`fitz`) v1.27.2.3 text extraction with
  page boundaries preserved (`---- page N ----` markers). This is a genuine
  independent parse of the paper, not a Marker output; the filename follows the
  8-artifact-bar convention. Header line inside the file explicitly states the
  tool.
- `nougat.mmd`  -- **surrogate**: `pdftotext -layout` reflow, preserving math
  layout as best pdftotext can. Header line explicitly states the tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files.
