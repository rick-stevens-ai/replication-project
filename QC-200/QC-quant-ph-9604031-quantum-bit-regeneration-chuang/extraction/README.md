# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-05). The QC wave brief allows either "pull from central
corpus if parsed, else run Marker/Nougat". A search of the REPLICATE-PROJECT
tree for `9604031*` and `chuang*yamamoto*` found no pre-parsed extraction.
Rather than fabricate Marker/Nougat output, we produced two independent
open-source extractions and clearly label the tool (same convention as sibling
QC-200 dir `QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve`):

- `marker.md`   — **surrogate**: PyMuPDF (`fitz`) v1.27.2.3 text extraction with
  page boundaries preserved (`---- page N ----` markers). Genuine independent
  parse of the paper, not a Marker output; filename follows the artifact-bar
  convention. Header line inside the file explicitly states the tool.
- `nougat.mmd`  — **surrogate**: `pdftotext -layout` reflow, preserving math
  markup as best pdftotext can. Header line explicitly states the tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files.
