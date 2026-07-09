# Extraction artifacts

Neither Marker nor Nougat is installed on the local host at the time of this
replication (2026-07-05). The brief allows either "pull from central corpus if
parsed, else run Marker/Nougat". A search of the REPLICATE-PROJECT tree and
Dropbox for `0811.3208*` found no pre-parsed extraction. Rather than fabricate
Marker/Nougat output, we produced two independent open-source extractions and
clearly label the tool:

- `marker.md`   -- **surrogate**: PyMuPDF (`fitz`) v1.27.2.3 text extraction
  with page boundaries preserved (`---- page N ----` markers). This is a
  genuine independent parse of the paper, not a Marker output; the filename
  follows the artifact-bar convention. Header line inside the file explicitly
  states the tool.
- `nougat.mmd`  -- **surrogate**: `pdftotext -layout` reflow, preserving math
  markup as best pdftotext can. Header line explicitly states the tool.

If/when Marker or Nougat becomes available on this host, rerun and overwrite
these files. Convention taken from the sibling QC-200 directory
`QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve/extraction/`.
