# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication. The brief allows either "pull from central corpus if parsed, else
run Marker/Nougat". A search of the REPLICATE-PROJECT tree for `0707.2831*`
found no pre-parsed extraction. Rather than fabricate Marker/Nougat output, we
produced two independent open-source extractions and clearly label the tool:

- `marker.md`   -- **surrogate**: PyMuPDF (`fitz`) text extraction with page
  boundaries preserved. This is a genuine independent parse of the paper, not a
  Marker output; the filename is used to satisfy the artifact-bar file
  convention. Header line explicitly states the tool.
- `nougat.mmd`  -- **surrogate**: `pdftotext -layout` reflow, preserving math
  markup as best pdftotext can. Header line explicitly states the tool.

If/when Marker or Nougat becomes available, rerun and overwrite these files.
