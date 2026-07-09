# Extraction artifacts

Neither Marker nor Nougat is installed on the local host (CherryRd) at the
time of this replication (2026-07-05). The brief allows either "pull from
central corpus if parsed, else run Marker/Nougat". A search of
`~/Dropbox/REPLICATE-PROJECT/` for `1701.08669*` returned no pre-parsed
extraction. Rather than fabricate Marker/Nougat output, we produced two
independent open-source extractions and clearly label the tool in each file:

- `marker.md`  — **surrogate**: PyMuPDF (`fitz`) text extraction with page
  boundaries preserved (`---- page N ----` markers). This is a genuine
  independent parse of the paper, not a Marker output; the filename follows
  the 8-artifact naming convention. Header line inside the file explicitly
  states the tool.
- `nougat.mmd` — **surrogate**: `pdftotext -layout` reflow, preserving math
  markup as best pdftotext can. Header line explicitly states the tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files.

Same convention as sibling QC-200 dirs (e.g.
`QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve/`).
